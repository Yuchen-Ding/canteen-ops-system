from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Select, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.orders.model import Order
from app.modules.payments.model import Payment
from app.modules.refunds.model import Refund
from app.modules.refunds.schema import RefundCreate


def _generate_refund_no() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    return f"REF{timestamp}{uuid4().hex[:6].upper()}"


def _refund_row_to_dict(row) -> dict:
    refund = row[0]
    return jsonable_encoder(
        {
            "id": refund.id,
            "refund_no": refund.refund_no,
            "order_id": refund.order_id,
            "order_no": row.order_no,
            "payment_id": refund.payment_id,
            "payment_no": row.payment_no,
            "refund_amount": refund.refund_amount,
            "refund_reason": refund.refund_reason,
            "refund_status": refund.refund_status,
            "requested_by": refund.requested_by,
            "refunded_at": refund.refunded_at,
            "failure_reason": refund.failure_reason,
            "remark": refund.remark,
            "created_at": refund.created_at,
            "updated_at": refund.updated_at,
        }
    )


def _base_refund_statement() -> Select:
    return (
        select(
            Refund,
            Order.order_no.label("order_no"),
            Payment.payment_no.label("payment_no"),
        )
        .join(Order, Order.id == Refund.order_id)
        .join(Payment, Payment.id == Refund.payment_id)
    )


def _apply_filters(
    statement: Select,
    *,
    keyword: str | None,
    refund_status: str | None,
    start_date: datetime | None,
    end_date: datetime | None,
) -> Select:
    if keyword:
        keyword_filter = f"%{keyword}%"
        statement = statement.where(or_(Refund.refund_no.ilike(keyword_filter), Order.order_no.ilike(keyword_filter)))
    if refund_status:
        statement = statement.where(Refund.refund_status == refund_status)
    if start_date:
        statement = statement.where(Refund.created_at >= start_date)
    if end_date:
        statement = statement.where(Refund.created_at <= end_date)
    return statement


async def create_refund(db: AsyncSession, order_id: int, payload: RefundCreate) -> dict:
    order_result = await db.execute(select(Order).where(Order.id == order_id).with_for_update())
    order = order_result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在。")
    if order.payment_status == "REFUNDED" or order.order_status == "REFUNDED":
        raise HTTPException(status_code=400, detail="订单已退款，不能重复退款。")
    if order.payment_status != "PAID" or order.order_status != "COMPLETED":
        raise HTTPException(status_code=400, detail="订单未支付，不能退款。")
    if order.payable_amount <= 0:
        raise HTTPException(status_code=400, detail="退款金额异常。")

    existing_refund = await db.scalar(select(Refund).where(Refund.order_id == order.id))
    if existing_refund:
        raise HTTPException(status_code=400, detail="订单已存在退款记录，不能重复退款。")

    payment_result = await db.execute(select(Payment).where(Payment.order_id == order.id).with_for_update())
    payment = payment_result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="未找到支付记录。")
    if payment.payment_status != "PAID":
        raise HTTPException(status_code=400, detail="支付记录状态不允许退款。")

    now = datetime.now(timezone.utc)
    refund = Refund(
        refund_no=_generate_refund_no(),
        order_id=order.id,
        payment_id=payment.id,
        refund_amount=order.payable_amount,
        refund_reason=payload.refund_reason,
        refund_status="SUCCESS",
        requested_by=payload.requested_by,
        refunded_at=now,
        remark=payload.remark,
    )
    db.add(refund)
    order.payment_status = "REFUNDED"
    order.order_status = "REFUNDED"
    order.updated_at = now
    payment.payment_status = "REFUNDED"
    payment.updated_at = now

    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail="订单已退款，不能重复退款。") from exc
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail="模拟退款失败，请稍后重试。") from exc

    await db.refresh(refund)
    result = await db.execute(_base_refund_statement().where(Refund.id == refund.id))
    return _refund_row_to_dict(result.one())


async def list_refunds(
    db: AsyncSession,
    *,
    keyword: str | None,
    refund_status: str | None,
    start_date: datetime | None,
    end_date: datetime | None,
    page: int,
    page_size: int,
) -> dict:
    count_statement = _apply_filters(
        select(func.count()).select_from(Refund).join(Order, Order.id == Refund.order_id),
        keyword=keyword,
        refund_status=refund_status,
        start_date=start_date,
        end_date=end_date,
    )
    total = await db.scalar(count_statement)

    statement = _apply_filters(
        _base_refund_statement(),
        keyword=keyword,
        refund_status=refund_status,
        start_date=start_date,
        end_date=end_date,
    ).order_by(Refund.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(statement)
    return {
        "items": [_refund_row_to_dict(row) for row in result.all()],
        "total": total or 0,
        "page": page,
        "page_size": page_size,
    }


async def get_refund_detail(db: AsyncSession, refund_id: int) -> dict:
    result = await db.execute(_base_refund_statement().where(Refund.id == refund_id))
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="退款记录不存在。")
    return _refund_row_to_dict(row)
