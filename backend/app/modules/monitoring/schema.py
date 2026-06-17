from decimal import Decimal

from pydantic import BaseModel


class MasterDataSummary(BaseModel):
    canteen_count: int
    stall_count: int
    dish_count: int
    meal_package_count: int
    employee_count: int
    visitor_count: int
    device_count: int


class StatusSummary(BaseModel):
    active_canteen_count: int
    active_stall_count: int
    available_dish_count: int
    online_device_count: int
    offline_device_count: int
    maintenance_device_count: int = 0
    inactive_employee_count: int
    inactive_visitor_count: int


class TodayBusinessSummary(BaseModel):
    today_order_count: int
    today_revenue: Decimal
    today_refund_amount: Decimal
    today_net_revenue: Decimal
    today_employee_order_count: int
    today_visitor_order_count: int


class MonitoringAlert(BaseModel):
    level: str
    title: str
    message: str
    source: str
    trigger_code: str


class MonitoringStatus(BaseModel):
    level: str
    label: str
    message: str
    alerts: list[MonitoringAlert]
