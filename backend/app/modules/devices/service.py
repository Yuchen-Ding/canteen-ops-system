from app.common.crud import MasterDataService
from app.modules.devices.model import Device


device_service = MasterDataService(Device, ["device_code", "device_name", "device_type", "ip_address", "location"])
