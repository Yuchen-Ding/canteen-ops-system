from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel

CustomerType = Literal["EMPLOYEE", "VISITOR"]
PaymentStatus = Literal["PENDING", "PAID", "FAILED", "REFUNDED"]
OrderStatus = Literal["CREATED", "COMPLETED", "CANCELLED", "REFUNDED"]


class OrderListQuery(BaseModel):
    keyword: str | None = None
    customer_type: CustomerType | None = None
    payment_status: PaymentStatus | None = None
    order_status: OrderStatus | None = None
    canteen_id: int | None = None
    stall_id: int | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    page: int = 1
    page_size: int = 20


class OrderRead(BaseModel):
    id: int
    order_no: str
    canteen_id: int
    canteen_name: str | None = None
    stall_id: int
    stall_name: str | None = None
    device_id: int
    device_name: str | None = None
    customer_type: str
    employee_id: int | None = None
    employee_name: str | None = None
    visitor_id: int | None = None
    visitor_name: str | None = None
    meal_type: str
    original_amount: Decimal
    discount_amount: Decimal
    subsidy_amount: Decimal
    payable_amount: Decimal
    payment_status: str
    order_status: str
    transaction_time: datetime
    operator: str | None = None
    remark: str | None = None
