from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CanteenBase(BaseModel):
    canteen_code: str
    name: str
    city: str
    location: str
    status: str = "ACTIVE"
    remark: str | None = None


class CanteenCreate(CanteenBase):
    pass


class CanteenUpdate(BaseModel):
    canteen_code: str | None = None
    name: str | None = None
    city: str | None = None
    location: str | None = None
    status: str | None = None
    remark: str | None = None


class CanteenStatusUpdate(BaseModel):
    status: str


class CanteenRead(CanteenBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
