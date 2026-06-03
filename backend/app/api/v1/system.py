from datetime import datetime, timezone

from fastapi import APIRouter

from app.core.config import settings
from app.core.database import check_database

router = APIRouter(tags=["system"])


@router.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "service": settings.system_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/health/db")
async def health_db() -> dict:
    database_status = await check_database()
    return {
        "status": "ok" if database_status["connected"] else "degraded",
        "database": database_status,
        "environment": settings.app_env,
    }


@router.get("/metrics")
async def metrics() -> dict:
    database_status = await check_database()
    return {
        "backend_status": 1,
        "database_status": 1 if database_status["connected"] else 0,
        "environment": settings.app_env,
        "metrics_mode": "mock",
    }


@router.get("/api/v1/system/info")
async def system_info() -> dict:
    return {
        "system_name": settings.system_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "ai_provider": settings.ai_provider,
    }
