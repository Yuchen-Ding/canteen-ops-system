from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

DeviceType = Literal["POS", "SELF_SERVICE", "MOBILE_TERMINAL"]
DeviceStatus = Literal["ONLINE", "OFFLINE", "MAINTENANCE", "ERROR"]


class DeviceBase(BaseModel):
    device_code: str
    device_name: str
    canteen_id: int
    stall_id: int | None = None
    device_type: DeviceType
    ip_address: str | None = None
    location: str | None = None
    status: DeviceStatus = "OFFLINE"
    last_heartbeat_time: datetime | None = None
    remark: str | None = None


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    device_code: str | None = None
    device_name: str | None = None
    canteen_id: int | None = None
    stall_id: int | None = None
    device_type: DeviceType | None = None
    ip_address: str | None = None
    location: str | None = None
    status: DeviceStatus | None = None
    last_heartbeat_time: datetime | None = None
    remark: str | None = None


class DeviceStatusUpdate(BaseModel):
    status: DeviceStatus


class DeviceRead(DeviceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
