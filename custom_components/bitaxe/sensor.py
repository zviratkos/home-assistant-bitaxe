import logging
from homeassistant.helpers.entity import Entity, DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

DOMAIN = "bitaxe"

SENSOR_NAME_MAP = {
    "power": "Power Consumption",
    "temp": "Temperature",
    "hashRate": "Hash Rate",
    "bestDiff": "All-Time Best Difficulty",
    "bestSessionDiff": "Best Difficulty Since System Boot",
    "sharesAccepted": "Shares Accepted",
    "sharesRejected": "Shares Rejected",
    "fanspeed": "Fan Speed",
    "fanrpm": "Fan RPM",
    "uptimeSeconds": "Uptime",
}

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up BitAxe sensors from a config entry."""
    coordinator = hass.data[DOMAIN][entry.unique_id]["coordinator"]
    device_name = entry.data.get("device_name", "default_device_name")
    ip_address = entry.data.get("ip_address")

    _LOGGER.debug(f"Setting up sensors for device: {device_name} ({ip_address})")

    sensors = [
        BitAxeSensor(coordinator, "power", device_name, ip_address),
        BitAxeSensor(coordinator, "temp", device_name, ip_address),
        BitAxeSensor(coordinator, "hashRate", device_name, ip_address),
        BitAxeSensor(coordinator, "bestDiff", device_name, ip_address),
        BitAxeSensor(coordinator, "bestSessionDiff", device_name, ip_address),
        BitAxeSensor(coordinator, "sharesAccepted", device_name, ip_address),
        BitAxeSensor(coordinator, "sharesRejected", device_name, ip_address),
        BitAxeSensor(coordinator, "fanspeed", device_name, ip_address),
        BitAxeSensor(coordinator, "fanrpm", device_name, ip_address),
        BitAxeSensor(coordinator, "uptimeSeconds", device_name, ip_address),
    ]

    async_add_entities(sensors, update_before_add=True)


class BitAxeSensor(Entity):
    """Representation of a BitAxe sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator, sensor_type: str, device_name: str, ip_address: str):
        super().__init__()
        self.coordinator = coordinator
        self.sensor_type = sensor_type
        self._device_name = device_name
        self._ip_address = ip_address
        self._attr_name = f"{SENSOR_NAME_MAP.get(sensor_type, f'BitAxe {sensor_type.capitalize()}')} ({device_name})"
        self._attr_unique_id = f"{ip_address}_{sensor_type}"  # unikátní ID založené na IP
        self._attr_icon = self._get_icon(sensor_type)

        _LOGGER.debug(f"Initialized BitAxeSensor: {self._attr_name} with unique ID: {self._attr_unique_id}")

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information so HA creates a device in the registry."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._ip_address)},
            name=self._device_name,
            manufacturer="Bitaxe",
            model="Bitaxe miner",
            sw_version=self.coordinator.data.get("fw_version"),
        )

    @property
    def state(self):
        value = self.coordinator.data.get(self.sensor_type, None)

        if self.sensor_type == "uptimeSeconds" and value is not None:
            return self._format_uptime(value)
        elif self.sensor_type == "power" and value is not None:
            return round(value, 1)
        elif self.sensor_type == "hashRate" and value is not None:
            return int(value)
        return value if value is not None else "N/A"

    @staticmethod
    def _format_uptime(seconds):
        days, remainder = divmod(seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{days}d {hours}h {minutes}m {seconds}s"

    @property
    def unit_of_measurement(self):
        if self.sensor_type == "power":
            return "W"
        elif self.sensor_type == "hashRate":
            return "GH/s"
        elif self.sensor_type == "temp":
            return "°C"
        elif self.sensor_type == "fanspeed":
            return "%"
        elif self.sensor_type == "fanrpm":
            return "RPM"
        return None

    def _get_icon(self, sensor_type):
        if sensor_type == "bestSessionDiff":
            return "mdi:star"
        elif sensor_type == "bestDiff":
            return "mdi:trophy"
        elif sensor_type in ["fanspeed", "fanrpm"]:
            return "mdi:fan"
        elif sensor_type == "hashRate":
            return "mdi:speedometer"
        elif sensor_type == "power":
            return "mdi:flash"
        elif sensor_type == "sharesAccepted":
            return "mdi:share"
        elif sensor_type == "sharesRejected":
            return "mdi:share-off"
        elif sensor_type == "temp":
            return "mdi:thermometer"
        elif sensor_type == "uptimeSeconds":
            return "mdi:clock"
        return "mdi:help-circle"
