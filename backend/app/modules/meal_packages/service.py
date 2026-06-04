from app.common.crud import MasterDataService
from app.modules.meal_packages.model import MealPackage


meal_package_service = MasterDataService(MealPackage, ["package_code", "name"])
