from app.common.router_factory import create_crud_router
from app.modules.employees.schema import EmployeeCreate, EmployeeRead, EmployeeStatusUpdate, EmployeeUpdate
from app.modules.employees.service import employee_service


router = create_crud_router(
    prefix="/api/v1/employees",
    tag="employees",
    service=employee_service,
    create_schema=EmployeeCreate,
    update_schema=EmployeeUpdate,
    status_schema=EmployeeStatusUpdate,
    read_schema=EmployeeRead,
)
