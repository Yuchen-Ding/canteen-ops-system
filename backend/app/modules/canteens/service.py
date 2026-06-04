from app.common.crud import MasterDataService
from app.modules.canteens.model import Canteen


canteen_service = MasterDataService(Canteen, ["canteen_code", "name", "city", "location"])
