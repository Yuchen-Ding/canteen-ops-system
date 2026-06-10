from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel

PaymentMethod = Literal["EMPLOYEE_CARD", "VISITOR_QR", "CASH", "MOCK_ALIPAY", "MOCK_WECHAT"]
PaymentStatus = Literal["PENDING", "PAID", "FAILED", "REFUNDED"]


class PaymentRead(BaseModel):
    id: int
    payment_no: str
    order_id: int
    order_no: str | None = None
    payment_method: str
    payment_amount: Decimal
    payment_status: str
    paid_at: datetime | None = None
    failure_reason: str | None = None
    created_at: datetime
    updated_at: datetime
