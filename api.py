import aiohttp
from homeassistant.helpers.aiohttp_client import async_get_clientsession

async def fetch_bitaxe_data(hass, url):
    """Fetch data from the BitAxe API using the Home Assistant session."""
    session = async_get_clientsession(hass)
    
    try:
        async with session.get(url) as response:
            response.raise_for_status()  # Raises an error for HTTP error responses
            return await response.json()
    except aiohttp.ClientError as e:
        # Log and raise an exception for client errors
        _LOGGER.error(f"Client error occurred: {e}")
        raise Exception(f"Client error: {str(e)}")
    except Exception as e:
        # Handle other exceptions
        _LOGGER.error(f"An unexpected error occurred: {e}")
        raise Exception(f"An unexpected error: {str(e)}")
