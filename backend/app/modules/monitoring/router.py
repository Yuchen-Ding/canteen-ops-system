from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.monitoring.service import get_canteen_overview

router = APIRouter(prefix="/api/v1/monitoring", tags=["monitoring"])


@router.get("/canteen-overview")
async def canteen_overview_api(db: AsyncSession = Depends(get_db)) -> dict:
    return jsonable_encoder(await get_canteen_overview(db))
