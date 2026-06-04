from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class DishBase(BaseModel):
    dish_code: str
    stall_id: int
    name: str
    category: str
    unit_price: Decimal
    is_available: bool = True
    status: str = "ACTIVE"
    remark: str | None = None


class DishCreate(DishBase):
    pass


class DishUpdate(BaseModel):
    dish_code: str | None = None
    stall_id: int | None = None
    name: str | None = None
    category: str | None = None
    unit_price: Decimal | None = None
    is_available: bool | None = None
    status: str | None = None
    remark: str | None = None


class DishStatusUpdate(BaseModel):
    status: str


class DishRead(DishBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
