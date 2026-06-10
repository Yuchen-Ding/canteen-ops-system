from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.refunds.schema import RefundCreate
from app.modules.refunds.service import create_refund, get_refund_detail, list_refunds

router = APIRouter(tags=["refunds"])


@router.post("/api/v1/orders/{order_id}/refund")
async def create_refund_api(
    order_id: int,
    payload: RefundCreate,
    db: AsyncSession = Depends(get_db),
) -> dict:
    return await create_refund(db, order_id, payload)


@router.get("/api/v1/refunds")
async def list_refund_api(
    keyword: str | None = Query(default=None),
    refund_status: str | None = Query(default=None),
    start_date: datetime | None = Query(default=None),
    end_date: datetime | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> dict:
    return await list_refunds(
        db,
        keyword=keyword,
        refund_status=refund_status,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size,
    )


@router.get("/api/v1/refunds/{refund_id}")
async def get_refund_detail_api(refund_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    return await get_refund_detail(db, refund_id)
