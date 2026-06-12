from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.reports.service import (
    get_daily_report,
    get_dashboard_report,
    get_monthly_report,
    get_yearly_report,
)

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


@router.get("/dashboard")
async def dashboard_report_api(db: AsyncSession = Depends(get_db)) -> dict:
    return await get_dashboard_report(db)


@router.get("/daily")
async def daily_report_api(
    report_date: str = Query(..., description="YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db),
) -> dict:
    return await get_daily_report(db, report_date)


@router.get("/monthly")
async def monthly_report_api(
    month: str = Query(..., description="YYYY-MM"),
    db: AsyncSession = Depends(get_db),
) -> dict:
    return await get_monthly_report(db, month)


@router.get("/yearly")
async def yearly_report_api(
    year: str = Query(..., description="YYYY"),
    db: AsyncSession = Depends(get_db),
) -> dict:
    return await get_yearly_report(db, year)
