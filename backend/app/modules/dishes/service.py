from app.common.crud import MasterDataService
from app.modules.dishes.model import Dish


dish_service = MasterDataService(Dish, ["dish_code", "name", "category"])
