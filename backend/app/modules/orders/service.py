from datetime import datetime

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.canteens.model import Canteen
from app.modules.devices.model import Device
from app.modules.employees.model import Employee
from app.modules.orders.model import Order, OrderItem
from app.modules.payments.model import Payment
from app.modules.stalls.model import Stall
from app.modules.visitors.model import Visitor


def _order_row_to_dict(row) -> dict:
    order = row[0]
    visitor_name = row.visitor_name or order.visitor_name_snapshot
    return jsonable_encoder(
        {
            "id": order.id,
            "order_no": order.order_no,
            "canteen_id": order.canteen_id,
            "canteen_name": row.canteen_name,
            "stall_id": order.stall_id,
            "stall_name": row.stall_name,
            "device_id": order.device_id,
            "device_name": row.device_name,
            "customer_type": order.customer_type,
            "employee_id": order.employee_id,
            "employee_name": row.employee_name,
            "visitor_id": order.visitor_id,
            "visitor_name": visitor_name,
            "meal_type": order.meal_type,
            "original_amount": order.original_amount,
            "discount_amount": order.discount_amount,
            "subsidy_amount": order.subsidy_amount,
            "payable_amount": order.payable_amount,
            "payment_status": order.payment_status,
            "order_status": order.order_status,
            "transaction_time": order.transaction_time,
            "operator": order.operator,
            "remark": order.remark,
        }
    )


def _model_to_dict(model) -> dict:
    return jsonable_encoder({column.name: getattr(model, column.name) for column in model.__table__.columns})


def _base_order_statement() -> Select:
    return (
        select(
            Order,
            Canteen.name.label("canteen_name"),
            Stall.name.label("stall_name"),
            Device.device_name.label("device_name"),
            Employee.name.label("employee_name"),
            Visitor.name.label("visitor_name"),
        )
        .join(Canteen, Canteen.id == Order.canteen_id)
        .join(Stall, Stall.id == Order.stall_id)
        .join(Device, Device.id == Order.device_id)
        .outerjoin(Employee, Employee.id == Order.employee_id)
        .outerjoin(Visitor, Visitor.id == Order.visitor_id)
    )


def _apply_order_filters(
    statement: Select,
    *,
    keyword: str | None,
    customer_type: str | None,
    payment_status: str | None,
    order_status: str | None,
    canteen_id: int | None,
    stall_id: int | None,
    start_date: datetime | None,
    end_date: datetime | None,
) -> Select:
    if keyword:
        statement = statement.where(Order.order_no.ilike(f"%{keyword}%"))
    if customer_type:
        statement = statement.where(Order.customer_type == customer_type)
    if payment_status:
        statement = statement.where(Order.payment_status == payment_status)
    if order_status:
        statement = statement.where(Order.order_status == order_status)
    if canteen_id:
        statement = statement.where(Order.canteen_id == canteen_id)
    if stall_id:
        statement = statement.where(Order.stall_id == stall_id)
    if start_date:
        statement = statement.where(Order.transaction_time >= start_date)
    if end_date:
        statement = statement.where(Order.transaction_time <= end_date)
    return statement


async def list_orders(
    db: AsyncSession,
    *,
    keyword: str | None,
    customer_type: str | None,
    payment_status: str | None,
    order_status: str | None,
    canteen_id: int | None,
    stall_id: int | None,
    start_date: datetime | None,
    end_date: datetime | None,
    page: int,
    page_size: int,
) -> dict:
    count_statement = _apply_order_filters(
        select(func.count()).select_from(Order),
        keyword=keyword,
        customer_type=customer_type,
        payment_status=payment_status,
        order_status=order_status,
        canteen_id=canteen_id,
        stall_id=stall_id,
        start_date=start_date,
        end_date=end_date,
    )
    total = await db.scalar(count_statement)

    statement = _apply_order_filters(
        _base_order_statement(),
        keyword=keyword,
        customer_type=customer_type,
        payment_status=payment_status,
        order_status=order_status,
        canteen_id=canteen_id,
        stall_id=stall_id,
        start_date=start_date,
        end_date=end_date,
    ).order_by(Order.transaction_time.desc()).offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(statement)
    return {
        "items": [_order_row_to_dict(row) for row in result.all()],
        "total": total or 0,
        "page": page,
        "page_size": page_size,
    }


async def get_order_detail(db: AsyncSession, order_id: int) -> dict:
    result = await db.execute(_base_order_statement().where(Order.id == order_id))
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="订单不存在。")

    items_result = await db.execute(select(OrderItem).where(OrderItem.order_id == order_id).order_by(OrderItem.id))
    payment_result = await db.execute(select(Payment).where(Payment.order_id == order_id))
    payment = payment_result.scalar_one_or_none()

    return {
        "order": _order_row_to_dict(row),
        "items": [_model_to_dict(item) for item in items_result.scalars().all()],
        "payment": _model_to_dict(payment) if payment else None,
    }
