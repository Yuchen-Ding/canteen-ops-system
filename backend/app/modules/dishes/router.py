from app.common.router_factory import create_crud_router
from app.modules.dishes.schema import DishCreate, DishRead, DishStatusUpdate, DishUpdate
from app.modules.dishes.service import dish_service


router = create_crud_router(
    prefix="/api/v1/dishes",
    tag="dishes",
    service=dish_service,
    create_schema=DishCreate,
    update_schema=DishUpdate,
    status_schema=DishStatusUpdate,
    read_schema=DishRead,
)
