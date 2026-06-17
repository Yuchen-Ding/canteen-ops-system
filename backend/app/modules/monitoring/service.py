from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.canteens.model import Canteen
from app.modules.devices.model import Device
from app.modules.dishes.model import Dish
from app.modules.employees.model import Employee
from app.modules.meal_packages.model import MealPackage
from app.modules.reports.service import get_dashboard_report
from app.modules.stalls.model import Stall
from app.modules.visitors.model import Visitor


async def _count(db: AsyncSession, model, *filters) -> int:
    return int(await db.scalar(select(func.count()).select_from(model).where(*filters)) or 0)


def _build_monitoring_status(status_summary: dict, today_business_summary: dict) -> dict:
    alerts = []
    offline_device_count = status_summary["offline_device_count"]
    maintenance_device_count = status_summary["maintenance_device_count"]

    if offline_device_count > 0:
        alerts.append(
            {
                "level": "CRITICAL",
                "title": "存在离线 POS 设备",
                "message": f"当前有 {offline_device_count} 台 POS 设备离线，请检查设备状态。",
                "source": "DEVICE",
                "trigger_code": "POS_OFFLINE",
            }
        )
    if maintenance_device_count > 0:
        alerts.append(
            {
                "level": "WARNING",
                "title": "存在维护中 POS 设备",
                "message": f"当前有 {maintenance_device_count} 台 POS 设备处于维护中。",
                "source": "DEVICE",
                "trigger_code": "POS_MAINTENANCE",
            }
        )
    if status_summary["active_stall_count"] == 0:
        alerts.append(
            {
                "level": "CRITICAL",
                "title": "当前无启用档口",
                "message": "当前没有启用状态的档口，请维护档口资料或检查营业配置。",
                "source": "MASTER_DATA",
                "trigger_code": "NO_ACTIVE_STALL",
            }
        )
    if status_summary["available_dish_count"] == 0:
        alerts.append(
            {
                "level": "WARNING",
                "title": "当前无可售菜品",
                "message": "当前没有可售菜品，可能影响下单消费。",
                "source": "MASTER_DATA",
                "trigger_code": "NO_AVAILABLE_DISH",
            }
        )
    if today_business_summary["today_order_count"] == 0:
        alerts.append(
            {
                "level": "WARNING",
                "title": "今日暂无交易数据",
                "message": "今日尚未产生订单，请关注餐厅营业情况或数据采集状态。",
                "source": "BUSINESS",
                "trigger_code": "NO_TODAY_ORDER",
            }
        )

    if any(alert["level"] == "CRITICAL" for alert in alerts):
        return {
            "level": "CRITICAL",
            "label": "告警",
            "message": "当前存在需要优先处理的食堂运营告警。",
            "alerts": alerts,
        }
    if alerts:
        return {
            "level": "WARNING",
            "label": "注意",
            "message": "当前存在需要关注的食堂运营提醒。",
            "alerts": alerts,
        }
    return {
        "level": "NORMAL",
        "label": "正常",
        "message": "当前食堂系统运行正常。",
        "alerts": [],
    }


async def get_canteen_overview(db: AsyncSession) -> dict:
    dashboard = await get_dashboard_report(db)

    canteen_rows = await db.execute(
        select(
            Canteen.id,
            Canteen.canteen_code,
            Canteen.name,
            Canteen.city,
            Canteen.location,
            Canteen.status,
            func.count(Stall.id).label("stall_count"),
        )
        .outerjoin(Stall, Stall.canteen_id == Canteen.id)
        .group_by(Canteen.id)
        .order_by(Canteen.id)
    )
    stall_rows = await db.execute(
        select(
            Stall.id,
            Stall.stall_code,
            Stall.name,
            Stall.category,
            Stall.floor,
            Stall.status,
            Canteen.name.label("canteen_name"),
            func.count(Dish.id).label("dish_count"),
        )
        .join(Canteen, Canteen.id == Stall.canteen_id)
        .outerjoin(Dish, Dish.stall_id == Stall.id)
        .group_by(Stall.id, Canteen.name)
        .order_by(Stall.id)
    )
    device_rows = await db.execute(
        select(
            Device.id,
            Device.device_code,
            Device.device_name,
            Device.device_type,
            Device.status,
            Device.ip_address,
            Device.location,
            Device.last_heartbeat_time,
            Canteen.name.label("canteen_name"),
            Stall.name.label("stall_name"),
        )
        .join(Canteen, Canteen.id == Device.canteen_id)
        .outerjoin(Stall, Stall.id == Device.stall_id)
        .order_by(Device.id)
    )

    master_data_summary = {
        "canteen_count": await _count(db, Canteen),
        "stall_count": await _count(db, Stall),
        "dish_count": await _count(db, Dish),
        "meal_package_count": await _count(db, MealPackage),
        "employee_count": await _count(db, Employee),
        "visitor_count": await _count(db, Visitor),
        "device_count": await _count(db, Device),
    }
    status_summary = {
        "active_canteen_count": await _count(db, Canteen, Canteen.status == "ACTIVE"),
        "active_stall_count": await _count(db, Stall, Stall.status == "ACTIVE"),
        "available_dish_count": await _count(
            db, Dish, Dish.status == "ACTIVE", Dish.is_available.is_(True)
        ),
        "online_device_count": await _count(db, Device, Device.status == "ONLINE"),
        "offline_device_count": await _count(db, Device, Device.status == "OFFLINE"),
        "maintenance_device_count": await _count(db, Device, Device.status == "MAINTENANCE"),
        "inactive_employee_count": await _count(db, Employee, Employee.status != "ACTIVE"),
        "inactive_visitor_count": await _count(db, Visitor, Visitor.status != "ACTIVE"),
    }
    today_business_summary = {
        key: dashboard[key]
        for key in (
            "today_order_count",
            "today_revenue",
            "today_refund_amount",
            "today_net_revenue",
            "today_employee_order_count",
            "today_visitor_order_count",
        )
    }

    return {
        "monitoring_status": _build_monitoring_status(status_summary, today_business_summary),
        "master_data_summary": master_data_summary,
        "status_summary": status_summary,
        "today_business_summary": today_business_summary,
        "canteen_list": [dict(row._mapping) for row in canteen_rows.all()],
        "stall_list": [dict(row._mapping) for row in stall_rows.all()],
        "device_list": [dict(row._mapping) for row in device_rows.all()],
    }
