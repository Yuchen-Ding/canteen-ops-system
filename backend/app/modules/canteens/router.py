from app.common.router_factory import create_crud_router
from app.modules.canteens.schema import CanteenCreate, CanteenRead, CanteenStatusUpdate, CanteenUpdate
from app.modules.canteens.service import canteen_service


router = create_crud_router(
    prefix="/api/v1/canteens",
    tag="canteens",
    service=canteen_service,
    create_schema=CanteenCreate,
    update_schema=CanteenUpdate,
    status_schema=CanteenStatusUpdate,
    read_schema=CanteenRead,
)
