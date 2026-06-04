from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VisitorBase(BaseModel):
    visitor_no: str
    name: str
    phone: str | None = None
    company: str | None = None
    status: str = "ACTIVE"
    remark: str | None = None


class VisitorCreate(VisitorBase):
    pass


class VisitorUpdate(BaseModel):
    visitor_no: str | None = None
    name: str | None = None
    phone: str | None = None
    company: str | None = None
    status: str | None = None
    remark: str | None = None


class VisitorStatusUpdate(BaseModel):
    status: str


class VisitorRead(VisitorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
