from app.common.crud import MasterDataService
from app.modules.visitors.model import Visitor


visitor_service = MasterDataService(Visitor, ["visitor_no", "name", "phone", "company"])
