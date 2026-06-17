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


class DailyRevenueTrend(BaseModel):
    date: str
    revenue: Decimal


class DailyOrderTrend(BaseModel):
    date: str
    order_count: int


class CustomerTypeDistribution(BaseModel):
    customer_type: str
    label: str
    order_count: int
    amount: Decimal


class PaymentStatusDistribution(BaseModel):
    payment_status: str
    label: str
    count: int


class DashboardAlert(BaseModel):
    level: str
    title: str
    message: str
    source: str
    trigger_code: str
