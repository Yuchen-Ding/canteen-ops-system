from app.common.router_factory import create_crud_router
from app.modules.devices.schema import DeviceCreate, DeviceStatusUpdate, DeviceUpdate
from app.modules.devices.service import device_service


router = create_crud_router(
    prefix="/api/v1/devices",
    tag="devices",
    service=device_service,
    create_schema=DeviceCreate,
    update_schema=DeviceUpdate,
    status_schema=DeviceStatusUpdate,
)
