from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, Query
from sqlalchemy import Select, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class MasterDataService:
    def __init__(self, model: type, keyword_columns: list[str]) -> None:
        self.model = model
        self.keyword_columns = keyword_columns

    def _build_filters(self, statement: Select, keyword: str | None, status: str | None) -> Select:
        if keyword:
            keyword_filter = f"%{keyword}%"
            clauses = [getattr(self.model, column).ilike(keyword_filter) for column in self.keyword_columns]
            statement = statement.where(or_(*clauses))
        if status:
            statement = statement.where(self.model.status == status)
        return statement

    async def list_items(
        self,
        db: AsyncSession,
        keyword: str | None,
        status: str | None,
        page: int,
        page_size: int,
    ) -> dict:
        base_statement = self._build_filters(select(self.model), keyword, status)
        count_statement = self._build_filters(select(func.count()).select_from(self.model), keyword, status)

        total = await db.scalar(count_statement)
        result = await db.execute(
            base_statement.order_by(self.model.id.desc()).offset((page - 1) * page_size).limit(page_size)
        )
        return {
            "items": result.scalars().all(),
            "total": total or 0,
            "page": page,
            "page_size": page_size,
        }

    async def get_item(self, db: AsyncSession, item_id: int) -> Any:
        item = await db.get(self.model, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Resource not found")
        return item

    async def create_item(self, db: AsyncSession, payload: dict) -> Any:
        item = self.model(**payload)
        db.add(item)
        try:
            await db.commit()
            await db.refresh(item)
            return item
        except IntegrityError as exc:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Resource violates unique or foreign key constraint") from exc

    async def update_item(self, db: AsyncSession, item_id: int, payload: dict) -> Any:
        item = await self.get_item(db, item_id)
        for key, value in payload.items():
            setattr(item, key, value)
        if hasattr(item, "updated_at"):
            item.updated_at = datetime.now(timezone.utc)
        try:
            await db.commit()
            await db.refresh(item)
            return item
        except IntegrityError as exc:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Resource violates unique or foreign key constraint") from exc

    async def update_status(self, db: AsyncSession, item_id: int, status: str) -> Any:
        return await self.update_item(db, item_id, {"status": status})


def pagination_params(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> tuple[int, int]:
    return page, page_size
