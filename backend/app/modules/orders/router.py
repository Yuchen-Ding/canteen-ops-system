from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.orders.service import get_order_detail, list_orders

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])


@router.get("")
async def list_order_api(
    keyword: str | None = Query(default=None),
    customer_type: str | None = Query(default=None),
    payment_status: str | None = Query(default=None),
    order_status: str | None = Query(default=None),
    canteen_id: int | None = Query(default=None),
    stall_id: int | None = Query(default=None),
    start_date: datetime | None = Query(default=None),
    end_date: datetime | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> dict:
    return await list_orders(
        db,
        keyword=keyword,
        customer_type=customer_type,
        payment_status=payment_status,
        order_status=order_status,
        canteen_id=canteen_id,
        stall_id=stall_id,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size,
    )


@router.get("/{order_id}")
async def get_order_detail_api(order_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    return await get_order_detail(db, order_id)
