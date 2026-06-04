from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.payments.service import list_payments

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])


@router.get("")
async def list_payment_api(
    payment_status: str | None = Query(default=None),
    payment_method: str | None = Query(default=None),
    start_date: datetime | None = Query(default=None),
    end_date: datetime | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> dict:
    return await list_payments(
        db,
        payment_status=payment_status,
        payment_method=payment_method,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size,
    )
