from decimal import Decimal

from pydantic import BaseModel


class NamedAmount(BaseModel):
    id: int
    name: str
    order_count: int
    revenue: Decimal


class TopDish(BaseModel):
    name: str
    quantity: int
    revenue: Decimal


class MonthlyRevenue(BaseModel):
    month: str
    order_count: int
    revenue: Decimal
    refund_amount: Decimal
    net_revenue: Decimal
