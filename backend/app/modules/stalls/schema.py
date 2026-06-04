from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StallBase(BaseModel):
    stall_code: str
    canteen_id: int
    name: str
    category: str
    floor: str | None = None
    status: str = "ACTIVE"
    remark: str | None = None


class StallCreate(StallBase):
    pass


class StallUpdate(BaseModel):
    stall_code: str | None = None
    canteen_id: int | None = None
    name: str | None = None
    category: str | None = None
    floor: str | None = None
    status: str | None = None
    remark: str | None = None


class StallStatusUpdate(BaseModel):
    status: str


class StallRead(StallBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
