from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.canteens.model import Canteen
from app.modules.devices.model import Device
from app.modules.dishes.model import Dish
from app.modules.employees.model import Employee
from app.modules.orders.model import Order, OrderItem
from app.modules.payments.model import Payment
from app.modules.pos.schema import EmployeeCardPaymentRequest, PosOrderItem, VisitorQrPaymentRequest
from app.modules.stalls.model import Stall
from app.modules.visitors.model import Visitor


def _generate_no(prefix: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    return f"{prefix}{timestamp}{uuid4().hex[:6].upper()}"


def _money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"))


def _serialize_model(model) -> dict:
    return {
        column.name: getattr(model, column.name)
        for column in model.__table__.columns
    }


def _serialize_result(order: Order, items: list[OrderItem], payment: Payment) -> dict:
    return jsonable_encoder({
        "order": _serialize_model(order),
        "items": [_serialize_model(item) for item in items],
        "payment": _serialize_model(payment),
    })


async def _get_active_stall(db: AsyncSession, stall_id: int) -> Stall:
    stall = await db.get(Stall, stall_id)
    if not stall or stall.status != "ACTIVE":
        raise HTTPException(status_code=400, detail="档口不存在或已停用。")
    return stall


async def _get_online_device(db: AsyncSession, device_id: int, stall: Stall) -> Device:
    device = await db.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=400, detail="设备不存在。")
    if device.status != "ONLINE":
        raise HTTPException(status_code=400, detail="设备不存在或不在线。")
    if device.canteen_id != stall.canteen_id:
        raise HTTPException(status_code=400, detail="设备不属于当前档口所在餐厅。")
    if device.stall_id and device.stall_id != stall.id:
        raise HTTPException(status_code=400, detail="设备已绑定其他档口。")
    return device


async def _get_active_employee_by_card(db: AsyncSession, card_no: str) -> Employee:
    result = await db.execute(select(Employee).where(Employee.card_no == card_no))
    employee = result.scalar_one_or_none()
    if not employee or employee.status != "ACTIVE":
        raise HTTPException(status_code=400, detail="员工不存在或已停用。")
    return employee


async def _get_active_visitor(db: AsyncSession, visitor_id: int | None) -> Visitor | None:
    if visitor_id is None:
        return None
    visitor = await db.get(Visitor, visitor_id)
    if not visitor or visitor.status != "ACTIVE":
        raise HTTPException(status_code=400, detail="访客不存在或已停用。")
    return visitor


async def _build_order_items(db: AsyncSession, stall_id: int, request_items: list[PosOrderItem]) -> tuple[list[dict], Decimal]:
    if not request_items:
        raise HTTPException(status_code=400, detail="请选择至少一个菜品。")

    dish_ids = [item.dish_id for item in request_items]
    result = await db.execute(select(Dish).where(Dish.id.in_(dish_ids)))
    dishes = {dish.id: dish for dish in result.scalars().all()}

    item_payloads: list[dict] = []
    original_amount = Decimal("0.00")

    for request_item in request_items:
        dish = dishes.get(request_item.dish_id)
        if not dish:
            raise HTTPException(status_code=400, detail="菜品不存在或不可售。")
        if dish.stall_id != stall_id:
            raise HTTPException(status_code=400, detail="菜品不属于当前档口。")
        if not dish.is_available or dish.status != "ACTIVE":
            raise HTTPException(status_code=400, detail="菜品不存在或不可售。")

        quantity = request_item.quantity
        unit_price = _money(dish.unit_price)
        amount = _money(unit_price * quantity)
        original_amount += amount
        item_payloads.append(
            {
                "dish_id": dish.id,
                "item_type": "DISH",
                "item_name_snapshot": dish.name,
                "quantity": quantity,
                "unit_price": unit_price,
                "amount": amount,
            }
        )

    original_amount = _money(original_amount)
    if original_amount <= 0:
        raise HTTPException(status_code=400, detail="订单金额异常。")
    return item_payloads, original_amount


async def _create_paid_order(
    db: AsyncSession,
    *,
    stall: Stall,
    device: Device,
    customer_type: str,
    meal_type: str,
    item_payloads: list[dict],
    original_amount: Decimal,
    payment_method: str,
    employee: Employee | None = None,
    visitor: Visitor | None = None,
    visitor_name_snapshot: str | None = None,
) -> dict:
    now = datetime.now(timezone.utc)
    payable_amount = original_amount
    order = Order(
        order_no=_generate_no("ORD"),
        canteen_id=stall.canteen_id,
        stall_id=stall.id,
        device_id=device.id,
        customer_type=customer_type,
        employee_id=employee.id if employee else None,
        visitor_id=visitor.id if visitor else None,
        visitor_name_snapshot=visitor.name if visitor else visitor_name_snapshot,
        meal_type=meal_type,
        original_amount=original_amount,
        discount_amount=Decimal("0.00"),
        subsidy_amount=Decimal("0.00"),
        payable_amount=payable_amount,
        payment_status="PAID",
        order_status="COMPLETED",
        transaction_time=now,
        operator="mock_pos",
    )
    db.add(order)
    await db.flush()

    order_items = [OrderItem(order_id=order.id, **item_payload) for item_payload in item_payloads]
    db.add_all(order_items)

    payment = Payment(
        payment_no=_generate_no("PAY"),
        order_id=order.id,
        payment_method=payment_method,
        payment_amount=payable_amount,
        payment_status="PAID",
        paid_at=now,
    )
    db.add(payment)

    try:
        await db.commit()
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail="支付模拟失败，请检查订单资料。") from exc

    await db.refresh(order)
    await db.refresh(payment)
    for item in order_items:
        await db.refresh(item)
    return _serialize_result(order, order_items, payment)


async def create_employee_card_payment(db: AsyncSession, payload: EmployeeCardPaymentRequest) -> dict:
    employee = await _get_active_employee_by_card(db, payload.card_no)
    stall = await _get_active_stall(db, payload.stall_id)
    device = await _get_online_device(db, payload.device_id, stall)
    item_payloads, original_amount = await _build_order_items(db, stall.id, payload.items)
    return await _create_paid_order(
        db,
        stall=stall,
        device=device,
        customer_type="EMPLOYEE",
        meal_type=payload.meal_type,
        item_payloads=item_payloads,
        original_amount=original_amount,
        payment_method="EMPLOYEE_CARD",
        employee=employee,
    )


async def create_visitor_qr_payment(db: AsyncSession, payload: VisitorQrPaymentRequest) -> dict:
    visitor = await _get_active_visitor(db, payload.visitor_id)
    stall = await _get_active_stall(db, payload.stall_id)
    device = await _get_online_device(db, payload.device_id, stall)
    item_payloads, original_amount = await _build_order_items(db, stall.id, payload.items)
    return await _create_paid_order(
        db,
        stall=stall,
        device=device,
        customer_type="VISITOR",
        meal_type=payload.meal_type,
        item_payloads=item_payloads,
        original_amount=original_amount,
        payment_method=payload.payment_method,
        visitor=visitor,
        visitor_name_snapshot=payload.visitor_name or "临时访客",
    )
