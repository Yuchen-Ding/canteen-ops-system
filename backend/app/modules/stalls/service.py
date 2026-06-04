from app.common.crud import MasterDataService
from app.modules.stalls.model import Stall


stall_service = MasterDataService(Stall, ["stall_code", "name", "category", "floor"])
