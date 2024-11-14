import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import ipaddress  # Import für IP-Adressenvalidierung

from .const import DOMAIN

class BitAxeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            ip_address = user_input["ip_address"]
            device_name = user_input["device_name"]

            # Validierung der IP-Adresse
            try:
                ipaddress.ip_address(ip_address)
            except ValueError:
                errors["ip_address"] = "Invalid IP address format."
                return self.async_show_form(
                    step_id="user",
                    data_schema=self.get_data_schema(),
                    errors=errors
                )

            # Entry mit IP-Adresse und Gerätenamen erstellen
            return self.async_create_entry(
                title=device_name,
                data={"ip_address": ip_address, "device_name": device_name}
            )

        return self.async_show_form(
            step_id="user",
            data_schema=self.get_data_schema(),
            errors=errors
        )

    def get_data_schema(self):
        """Return the schema for user input."""
        return vol.Schema({
            vol.Required("ip_address"): str,
            vol.Required("device_name"): str,
        })

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return BitAxeOptionsFlowHandler(config_entry)

class BitAxeOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return self.async_show_form(step_id="init")
