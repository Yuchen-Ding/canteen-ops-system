from typing import Literal

from pydantic import BaseModel, Field

MealType = Literal["BREAKFAST", "LUNCH", "DINNER", "OTHER"]
VisitorPaymentMethod = Literal["VISITOR_QR", "MOCK_ALIPAY", "MOCK_WECHAT"]


class PosOrderItem(BaseModel):
    dish_id: int
    quantity: int = Field(gt=0)


class EmployeeCardPaymentRequest(BaseModel):
    card_no: str
    device_id: int
    stall_id: int
    meal_type: MealType
    items: list[PosOrderItem]


class VisitorQrPaymentRequest(BaseModel):
    visitor_id: int | None = None
    visitor_name: str | None = None
    device_id: int
    stall_id: int
    meal_type: MealType
    payment_method: VisitorPaymentMethod
    items: list[PosOrderItem]
