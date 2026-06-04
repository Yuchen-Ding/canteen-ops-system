from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db


def create_crud_router(
    prefix: str,
    tag: str,
    service,
    create_schema,
    update_schema,
    status_schema,
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=[tag])

    @router.get("")
    async def list_items(
        keyword: str | None = Query(default=None),
        status: str | None = Query(default=None),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=20, ge=1, le=100),
        db: AsyncSession = Depends(get_db),
    ) -> dict:
        return await service.list_items(db, keyword, status, page, page_size)

    @router.get("/{item_id}")
    async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
        return await service.get_item(db, item_id)

    @router.post("")
    async def create_item(payload: create_schema, db: AsyncSession = Depends(get_db)):  # type: ignore[valid-type]
        return await service.create_item(db, payload.model_dump(exclude_unset=True))

    @router.put("/{item_id}")
    async def update_item(
        item_id: int,
        payload: update_schema,  # type: ignore[valid-type]
        db: AsyncSession = Depends(get_db),
    ):
        return await service.update_item(db, item_id, payload.model_dump(exclude_unset=True))

    @router.patch("/{item_id}/status")
    async def update_status(
        item_id: int,
        payload: status_schema,  # type: ignore[valid-type]
        db: AsyncSession = Depends(get_db),
    ):
        return await service.update_status(db, item_id, payload.status)

    return router
