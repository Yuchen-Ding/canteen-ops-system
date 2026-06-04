from app.common.router_factory import create_crud_router
from app.modules.stalls.schema import StallCreate, StallRead, StallStatusUpdate, StallUpdate
from app.modules.stalls.service import stall_service


router = create_crud_router(
    prefix="/api/v1/stalls",
    tag="stalls",
    service=stall_service,
    create_schema=StallCreate,
    update_schema=StallUpdate,
    status_schema=StallStatusUpdate,
    read_schema=StallRead,
)
