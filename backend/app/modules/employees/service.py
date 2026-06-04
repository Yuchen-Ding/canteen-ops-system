from app.common.crud import MasterDataService
from app.modules.employees.model import Employee


employee_service = MasterDataService(Employee, ["employee_no", "name", "department", "card_no", "phone"])
