from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.orders.model import Order
from app.modules.payments.model import Payment


def _payment_row_to_dict(row) -> dict:
    payment = row[0]
    return jsonable_encoder(
        {
            "id": payment.id,
            "payment_no": payment.payment_no,
            "order_id": payment.order_id,
            "order_no": row.order_no,
            "payment_method": payment.payment_method,
            "payment_amount": payment.payment_amount,
            "payment_status": payment.payment_status,
            "paid_at": payment.paid_at,
            "failure_reason": payment.failure_reason,
            "created_at": payment.created_at,
            "updated_at": payment.updated_at,
        }
    )


def _apply_payment_filters(
    statement: Select,
    *,
    payment_status: str | None,
    payment_method: str | None,
    start_date: datetime | None,
    end_date: datetime | None,
) -> Select:
    if payment_status:
        statement = statement.where(Payment.payment_status == payment_status)
    if payment_method:
        statement = statement.where(Payment.payment_method == payment_method)
    if start_date:
        statement = statement.where(Payment.created_at >= start_date)
    if end_date:
        statement = statement.where(Payment.created_at <= end_date)
    return statement


async def list_payments(
    db: AsyncSession,
    *,
    payment_status: str | None,
    payment_method: str | None,
    start_date: datetime | None,
    end_date: datetime | None,
    page: int,
    page_size: int,
) -> dict:
    count_statement = _apply_payment_filters(
        select(func.count()).select_from(Payment),
        payment_status=payment_status,
        payment_method=payment_method,
        start_date=start_date,
        end_date=end_date,
    )
    total = await db.scalar(count_statement)

    statement = _apply_payment_filters(
        select(Payment, Order.order_no.label("order_no")).join(Order, Order.id == Payment.order_id),
        payment_status=payment_status,
        payment_method=payment_method,
        start_date=start_date,
        end_date=end_date,
    ).order_by(Payment.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(statement)
    return {
        "items": [_payment_row_to_dict(row) for row in result.all()],
        "total": total or 0,
        "page": page,
        "page_size": page_size,
    }
