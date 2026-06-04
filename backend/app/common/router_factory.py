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
    read_schema,
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=[tag])

    def serialize_item(item) -> dict:
        return read_schema.model_validate(item).model_dump(mode="json")

    def serialize_page(page_data: dict) -> dict:
        return {
            "items": [serialize_item(item) for item in page_data["items"]],
            "total": page_data["total"],
            "page": page_data["page"],
            "page_size": page_data["page_size"],
        }

    @router.get("")
    async def list_items(
        keyword: str | None = Query(default=None),
        status: str | None = Query(default=None),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=20, ge=1, le=100),
        db: AsyncSession = Depends(get_db),
    ) -> dict:
        page_data = await service.list_items(db, keyword, status, page, page_size)
        return serialize_page(page_data)

    @router.get("/{item_id}")
    async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
        item = await service.get_item(db, item_id)
        return serialize_item(item)

    @router.post("")
    async def create_item(payload: create_schema, db: AsyncSession = Depends(get_db)):  # type: ignore[valid-type]
        item = await service.create_item(db, payload.model_dump(exclude_unset=True))
        return serialize_item(item)

    @router.put("/{item_id}")
    async def update_item(
        item_id: int,
        payload: update_schema,  # type: ignore[valid-type]
        db: AsyncSession = Depends(get_db),
    ):
        item = await service.update_item(db, item_id, payload.model_dump(exclude_unset=True))
        return serialize_item(item)

    @router.patch("/{item_id}/status")
    async def update_status(
        item_id: int,
        payload: status_schema,  # type: ignore[valid-type]
        db: AsyncSession = Depends(get_db),
    ):
        item = await service.update_status(db, item_id, payload.status)
        return serialize_item(item)

    return router
