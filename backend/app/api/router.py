from fastapi import APIRouter

from app.api.v1 import system
from app.modules.canteens.router import router as canteen_router
from app.modules.devices.router import router as device_router
from app.modules.dishes.router import router as dish_router
from app.modules.employees.router import router as employee_router
from app.modules.meal_packages.router import router as meal_package_router
from app.modules.orders.router import router as order_router
from app.modules.payments.router import router as payment_router
from app.modules.pos.router import router as pos_router
from app.modules.stalls.router import router as stall_router
from app.modules.visitors.router import router as visitor_router

api_router = APIRouter()
api_router.include_router(system.router)
api_router.include_router(canteen_router)
api_router.include_router(stall_router)
api_router.include_router(dish_router)
api_router.include_router(meal_package_router)
api_router.include_router(employee_router)
api_router.include_router(visitor_router)
api_router.include_router(device_router)
api_router.include_router(pos_router)
api_router.include_router(order_router)
api_router.include_router(payment_router)
