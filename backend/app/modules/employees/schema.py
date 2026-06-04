from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

EmployeeType = Literal["FULL_TIME", "CONTRACTOR", "OUTSOURCED", "INTERN", "MANAGEMENT"]


class EmployeeBase(BaseModel):
    employee_no: str
    name: str
    department: str
    employee_type: EmployeeType
    card_no: str | None = None
    phone: str | None = None
    status: str = "ACTIVE"
    remark: str | None = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    employee_no: str | None = None
    name: str | None = None
    department: str | None = None
    employee_type: EmployeeType | None = None
    card_no: str | None = None
    phone: str | None = None
    status: str | None = None
    remark: str | None = None


class EmployeeStatusUpdate(BaseModel):
    status: str


class EmployeeRead(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
