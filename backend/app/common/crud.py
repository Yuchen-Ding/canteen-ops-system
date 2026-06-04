from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, Query
from sqlalchemy import Select, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


def _friendly_integrity_error(exc: IntegrityError) -> str:
    error_text = str(exc.orig or exc).lower()

    if "foreign key" in error_text:
        if "canteen_id" in error_text or "canteens" in error_text:
            return "所选餐厅不存在，请选择有效餐厅。"
        if "stall_id" in error_text or "stalls" in error_text:
            return "所选档口不存在，请选择有效档口。"
        if "dish_id" in error_text or "dishes" in error_text:
            return "所选菜品不存在，请选择有效菜品。"
        return "所选关联资料不存在，请重新选择。"

    if "unique" in error_text or "duplicate key" in error_text:
        if "card_no" in error_text:
            return "卡号已存在，请更换卡号。"
        if "phone" in error_text:
            return "手机号已存在，请更换手机号。"
        return "编码已存在，请更换编码。"

    return "资料保存失败，请检查编码和关联资料是否有效。"


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
            raise HTTPException(status_code=400, detail=_friendly_integrity_error(exc)) from exc

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
            raise HTTPException(status_code=400, detail=_friendly_integrity_error(exc)) from exc

    async def update_status(self, db: AsyncSession, item_id: int, status: str) -> Any:
        return await self.update_item(db, item_id, {"status": status})


def pagination_params(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> tuple[int, int]:
    return page, page_size
