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

    return {
        "master_data_summary": {
            "canteen_count": await _count(db, Canteen),
            "stall_count": await _count(db, Stall),
            "dish_count": await _count(db, Dish),
            "meal_package_count": await _count(db, MealPackage),
            "employee_count": await _count(db, Employee),
            "visitor_count": await _count(db, Visitor),
            "device_count": await _count(db, Device),
        },
        "status_summary": {
            "active_canteen_count": await _count(db, Canteen, Canteen.status == "ACTIVE"),
            "active_stall_count": await _count(db, Stall, Stall.status == "ACTIVE"),
            "available_dish_count": await _count(
                db, Dish, Dish.status == "ACTIVE", Dish.is_available.is_(True)
            ),
            "online_device_count": await _count(db, Device, Device.status == "ONLINE"),
            "offline_device_count": await _count(db, Device, Device.status == "OFFLINE"),
            "inactive_employee_count": await _count(db, Employee, Employee.status != "ACTIVE"),
            "inactive_visitor_count": await _count(db, Visitor, Visitor.status != "ACTIVE"),
        },
        "today_business_summary": {
            key: dashboard[key]
            for key in (
                "today_order_count",
                "today_revenue",
                "today_refund_amount",
                "today_net_revenue",
                "today_employee_order_count",
                "today_visitor_order_count",
            )
        },
        "canteen_list": [dict(row._mapping) for row in canteen_rows.all()],
        "stall_list": [dict(row._mapping) for row in stall_rows.all()],
        "device_list": [dict(row._mapping) for row in device_rows.all()],
    }
