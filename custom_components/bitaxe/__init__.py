from datetime import timedelta
import aiohttp
import logging
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.event import async_track_time_interval

DOMAIN = "bitaxe"
_LOGGER = logging.getLogger(__name__)

# Mapping for sensor names
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

async def async_setup_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry):
    """Set up BitAxe from a config entry."""
    ip_address = entry.data["ip_address"]

    # Create a coordinator for the data
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="BitAxe Sensor Data",
        update_method=lambda: fetch_bitaxe_data(ip_address),
        update_interval=timedelta(seconds=30),  # Intervall auf 30 Sekunden setzen
    )

    # Start the coordinator
    await coordinator.async_refresh()

    # Store the coordinator in hass.data
    hass.data[DOMAIN] = {"coordinator": coordinator}

    # Set up the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    # Schedule the update interval without threading issues
    async_track_time_interval(
        hass,
        _update_coordinator(coordinator),  # Callback als Funktion übergeben
        timedelta(seconds=30)  # Update-Intervall auf 30 Sekunden
    )

    return True

def _update_coordinator(coordinator: DataUpdateCoordinator):
    """Create a function to refresh the coordinator safely."""
    async def refresh(now):
        await coordinator.async_request_refresh()
    return refresh

async def fetch_bitaxe_data(ip_address):
    """Fetch data from the BitAxe API."""
    url = f"http://{ip_address}/api/system/info"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                _LOGGER.debug("Fetched data: %s", data)
                return data
    except Exception as e:
        _LOGGER.error("Error fetching data from BitAxe API: %s", e)
        return None
