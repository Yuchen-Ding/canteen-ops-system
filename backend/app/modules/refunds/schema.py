from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field

RefundStatus = Literal["PENDING", "SUCCESS", "FAILED"]


class RefundCreate(BaseModel):
    refund_reason: str = Field(min_length=1, max_length=500)
    requested_by: str = Field(min_length=1, max_length=120)
    remark: str | None = Field(default=None, max_length=500)


class RefundRead(BaseModel):
    id: int
    refund_no: str
    order_id: int
    order_no: str
    payment_id: int
    payment_no: str
    refund_amount: Decimal
    refund_reason: str
    refund_status: RefundStatus
    requested_by: str
    refunded_at: datetime | None = None
    failure_reason: str | None = None
    remark: str | None = None
    created_at: datetime
    updated_at: datetime
