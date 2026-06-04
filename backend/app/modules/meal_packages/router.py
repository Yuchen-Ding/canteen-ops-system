from app.common.router_factory import create_crud_router
from app.modules.meal_packages.schema import MealPackageCreate, MealPackageRead, MealPackageStatusUpdate, MealPackageUpdate
from app.modules.meal_packages.service import meal_package_service


router = create_crud_router(
    prefix="/api/v1/meal-packages",
    tag="meal-packages",
    service=meal_package_service,
    create_schema=MealPackageCreate,
    update_schema=MealPackageUpdate,
    status_schema=MealPackageStatusUpdate,
    read_schema=MealPackageRead,
)
