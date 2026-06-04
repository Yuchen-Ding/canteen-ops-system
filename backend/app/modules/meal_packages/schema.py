from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class MealPackageBase(BaseModel):
    package_code: str
    stall_id: int
    name: str
    package_price: Decimal
    status: str = "ACTIVE"
    remark: str | None = None


class MealPackageCreate(MealPackageBase):
    pass


class MealPackageUpdate(BaseModel):
    package_code: str | None = None
    stall_id: int | None = None
    name: str | None = None
    package_price: Decimal | None = None
    status: str | None = None
    remark: str | None = None


class MealPackageStatusUpdate(BaseModel):
    status: str


class MealPackageRead(MealPackageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
