from app.common.router_factory import create_crud_router
from app.modules.visitors.schema import VisitorCreate, VisitorStatusUpdate, VisitorUpdate
from app.modules.visitors.service import visitor_service


router = create_crud_router(
    prefix="/api/v1/visitors",
    tag="visitors",
    service=visitor_service,
    create_schema=VisitorCreate,
    update_schema=VisitorUpdate,
    status_schema=VisitorStatusUpdate,
)
