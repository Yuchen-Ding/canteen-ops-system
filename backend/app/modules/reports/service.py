from calendar import monthrange
from datetime import date, datetime, time, timedelta
from decimal import Decimal
import re
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.canteens.model import Canteen
from app.modules.orders.model import Order, OrderItem
from app.modules.refunds.model import Refund
from app.modules.stalls.model import Stall

REPORT_TIMEZONE = ZoneInfo("Asia/Shanghai")
REPORTABLE_ORDER_STATUSES = ("COMPLETED", "REFUNDED")
REPORTABLE_PAYMENT_STATUSES = ("PAID", "REFUNDED")


def _day_range(report_date: date) -> tuple[datetime, datetime]:
    start = datetime.combine(report_date, time.min, tzinfo=REPORT_TIMEZONE)
    return start, start + timedelta(days=1)


def _month_range(month: str) -> tuple[date, datetime, datetime]:
    if not re.fullmatch(r"\d{4}-\d{2}", month):
        raise HTTPException(status_code=400, detail="报表月份格式错误，请使用 YYYY-MM。")
    try:
        month_date = datetime.strptime(month, "%Y-%m").date().replace(day=1)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="报表月份格式错误，请使用 YYYY-MM。") from exc
    last_day = monthrange(month_date.year, month_date.month)[1]
    start = datetime.combine(month_date, time.min, tzinfo=REPORT_TIMEZONE)
    end = datetime.combine(month_date.replace(day=last_day), time.max, tzinfo=REPORT_TIMEZONE) + timedelta(microseconds=1)
    return month_date, start, end


def parse_report_date(value: str) -> date:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise HTTPException(status_code=400, detail="报表日期格式错误，请使用 YYYY-MM-DD。")
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="报表日期格式错误，请使用 YYYY-MM-DD。") from exc


def _order_time_filters(start: datetime, end: datetime) -> tuple:
    return (
        Order.transaction_time >= start,
        Order.transaction_time < end,
        Order.order_status.in_(REPORTABLE_ORDER_STATUSES),
        Order.payment_status.in_(REPORTABLE_PAYMENT_STATUSES),
    )


async def _order_summary(db: AsyncSession, start: datetime, end: datetime) -> dict:
    filters = _order_time_filters(start, end)
    row = (
        await db.execute(
            select(
                func.count(Order.id).label("order_count"),
                func.coalesce(func.sum(Order.payable_amount), 0).label("revenue"),
                func.count(Order.id).filter(Order.customer_type == "EMPLOYEE").label("employee_orders"),
                func.count(Order.id).filter(Order.customer_type == "VISITOR").label("visitor_orders"),
                func.count(Order.id).filter(Order.payment_status == "PAID").label("paid_orders"),
                func.count(Order.id).filter(Order.payment_status == "REFUNDED").label("refunded_orders"),
            ).where(*filters)
        )
    ).one()
    return {
        "order_count": row.order_count or 0,
        "revenue": row.revenue or Decimal("0.00"),
        "employee_orders": row.employee_orders or 0,
        "visitor_orders": row.visitor_orders or 0,
        "paid_orders": row.paid_orders or 0,
        "refunded_orders": row.refunded_orders or 0,
    }


async def _refund_summary(db: AsyncSession, start: datetime, end: datetime) -> dict:
    row = (
        await db.execute(
            select(
                func.count(Refund.id).label("refund_count"),
                func.coalesce(func.sum(Refund.refund_amount), 0).label("refund_amount"),
            ).where(
                Refund.refund_status == "SUCCESS",
                Refund.refunded_at >= start,
                Refund.refunded_at < end,
            )
        )
    ).one()
    return {
        "refund_count": row.refund_count or 0,
        "refund_amount": row.refund_amount or Decimal("0.00"),
    }


async def _revenue_by_canteen(db: AsyncSession, start: datetime, end: datetime) -> list[dict]:
    result = await db.execute(
        select(
            Canteen.id,
            Canteen.name,
            func.count(Order.id).label("order_count"),
            func.coalesce(func.sum(Order.payable_amount), 0).label("revenue"),
        )
        .join(Order, Order.canteen_id == Canteen.id)
        .where(*_order_time_filters(start, end))
        .group_by(Canteen.id, Canteen.name)
        .order_by(func.sum(Order.payable_amount).desc())
    )
    return [
        {"id": row.id, "name": row.name, "order_count": row.order_count, "revenue": row.revenue}
        for row in result.all()
    ]


async def _revenue_by_stall(db: AsyncSession, start: datetime, end: datetime) -> list[dict]:
    result = await db.execute(
        select(
            Stall.id,
            Stall.name,
            func.count(Order.id).label("order_count"),
            func.coalesce(func.sum(Order.payable_amount), 0).label("revenue"),
        )
        .join(Order, Order.stall_id == Stall.id)
        .where(*_order_time_filters(start, end))
        .group_by(Stall.id, Stall.name)
        .order_by(func.sum(Order.payable_amount).desc())
    )
    return [
        {"id": row.id, "name": row.name, "order_count": row.order_count, "revenue": row.revenue}
        for row in result.all()
    ]


async def _top_dishes(db: AsyncSession, start: datetime, end: datetime, limit: int = 10) -> list[dict]:
    result = await db.execute(
        select(
            OrderItem.item_name_snapshot.label("name"),
            func.sum(OrderItem.quantity).label("quantity"),
            func.coalesce(func.sum(OrderItem.amount), 0).label("revenue"),
        )
        .join(Order, Order.id == OrderItem.order_id)
        .where(*_order_time_filters(start, end))
        .group_by(OrderItem.item_name_snapshot)
        .order_by(func.sum(OrderItem.quantity).desc(), func.sum(OrderItem.amount).desc())
        .limit(limit)
    )
    return [
        {"name": row.name, "quantity": row.quantity or 0, "revenue": row.revenue}
        for row in result.all()
    ]


async def _build_report(db: AsyncSession, start: datetime, end: datetime) -> dict:
    order_summary = await _order_summary(db, start, end)
    refund_summary = await _refund_summary(db, start, end)
    refund_amount = refund_summary["refund_amount"]
    revenue = order_summary["revenue"]
    return {
        **order_summary,
        **refund_summary,
        "net_revenue": revenue - refund_amount,
        "revenue_by_canteen": await _revenue_by_canteen(db, start, end),
        "revenue_by_stall": await _revenue_by_stall(db, start, end),
        "top_dishes": await _top_dishes(db, start, end),
    }


async def get_dashboard_report(db: AsyncSession) -> dict:
    report_date = datetime.now(REPORT_TIMEZONE).date()
    start, end = _day_range(report_date)
    report = await _build_report(db, start, end)
    return jsonable_encoder(
        {
            "report_date": report_date.isoformat(),
            "today_order_count": report["order_count"],
            "today_revenue": report["revenue"],
            "today_refund_amount": report["refund_amount"],
            "today_net_revenue": report["net_revenue"],
            "today_refund_count": report["refund_count"],
            "today_employee_order_count": report["employee_orders"],
            "today_visitor_order_count": report["visitor_orders"],
            "paid_order_count": report["paid_orders"],
            "refunded_order_count": report["refunded_orders"],
            "top_dishes": report["top_dishes"],
            "revenue_by_canteen": report["revenue_by_canteen"],
            "revenue_by_stall": report["revenue_by_stall"],
        }
    )


async def get_daily_report(db: AsyncSession, report_date_text: str) -> dict:
    report_date = parse_report_date(report_date_text)
    start, end = _day_range(report_date)
    report = await _build_report(db, start, end)
    return jsonable_encoder(
        {
            "report_date": report_date.isoformat(),
            "total_orders": report["order_count"],
            "total_revenue": report["revenue"],
            "total_refund_amount": report["refund_amount"],
            "net_revenue": report["net_revenue"],
            "employee_orders": report["employee_orders"],
            "visitor_orders": report["visitor_orders"],
            "revenue_by_canteen": report["revenue_by_canteen"],
            "revenue_by_stall": report["revenue_by_stall"],
            "top_dishes": report["top_dishes"],
        }
    )


async def get_monthly_report(db: AsyncSession, month: str) -> dict:
    month_date, start, end = _month_range(month)
    report = await _build_report(db, start, end)
    return jsonable_encoder(
        {
            "month": month_date.strftime("%Y-%m"),
            "month_order_count": report["order_count"],
            "month_revenue": report["revenue"],
            "month_refund_amount": report["refund_amount"],
            "month_net_revenue": report["net_revenue"],
            "revenue_by_canteen": report["revenue_by_canteen"],
            "revenue_by_stall": report["revenue_by_stall"],
            "top_dishes": report["top_dishes"],
            "employee_consumption_summary": {
                "order_count": report["employee_orders"],
                "revenue": await db.scalar(
                    select(func.coalesce(func.sum(Order.payable_amount), 0)).where(
                        *_order_time_filters(start, end),
                        Order.customer_type == "EMPLOYEE",
                    )
                ),
            },
            "visitor_consumption_summary": {
                "order_count": report["visitor_orders"],
                "revenue": await db.scalar(
                    select(func.coalesce(func.sum(Order.payable_amount), 0)).where(
                        *_order_time_filters(start, end),
                        Order.customer_type == "VISITOR",
                    )
                ),
            },
        }
    )
