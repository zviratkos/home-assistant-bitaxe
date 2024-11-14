import logging
from homeassistant.helpers.entity import Entity

# Set up logging for debugging
_LOGGER = logging.getLogger(__name__)

# Define the integration domain
DOMAIN = "bitaxe"

# Mapping for sensor-names
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
    coordinator = hass.data[DOMAIN]["coordinator"]
    device_name = entry.data["device_name"]  # Gerätname abrufen

    # Create sensors based on the fetched data from the coordinator
    sensors = [
        BitAxeSensor(coordinator, "power", device_name),
        BitAxeSensor(coordinator, "temp", device_name),
        BitAxeSensor(coordinator, "hashRate", device_name),
        BitAxeSensor(coordinator, "bestDiff", device_name),
        BitAxeSensor(coordinator, "bestSessionDiff", device_name),
        BitAxeSensor(coordinator, "sharesAccepted", device_name),
        BitAxeSensor(coordinator, "sharesRejected", device_name),
        BitAxeSensor(coordinator, "fanspeed", device_name),
        BitAxeSensor(coordinator, "fanrpm", device_name),
        BitAxeSensor(coordinator, "uptimeSeconds", device_name),
    ]

    # Add sensors to Home Assistant with an initial update
    async_add_entities(sensors, update_before_add=True)

class BitAxeSensor(Entity):
    """Representation of a BitAxe sensor."""

    def __init__(self, coordinator, sensor_type, device_name):
        """Initialize the sensor with its type, data coordinator, and device name."""
        self.coordinator = coordinator
        self.sensor_type = sensor_type
        self._attr_name = f"{device_name} {SENSOR_NAME_MAP.get(sensor_type, f'BitAxe {sensor_type.capitalize()}')}"
        self._attr_unique_id = f"{device_id}_{sensor_type}"
        self._attr_icon = self._get_icon(sensor_type)

    @property
    def state(self):
        """Return the state of the sensor."""
        value = self.coordinator.data.get(self.sensor_type)

        # Handle special formatting for uptime, power, and hash rate
        if self.sensor_type == "uptimeSeconds" and value is not None:
            return self._format_uptime(value)
        elif self.sensor_type == "power" and value is not None:
            return round(value, 1)  # Round power to one decimal place
        elif self.sensor_type == "hashRate" and value is not None:
            return int(value)  # Display hash rate in GH/s as an integer
        return value

    @staticmethod
    def _format_uptime(seconds):
        """Convert uptime in seconds to a readable format."""
        days, remainder = divmod(seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{days}d {hours}h {minutes}m {seconds}s"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement for each sensor."""
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
        """Return the appropriate MDI icon for each sensor type."""
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
        return "mdi:help-circle"  # Default icon if none matched
