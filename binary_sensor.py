"""Binary sensor indicating if there is hot water at a specified thermal point"""
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from collections.abc import Mapping
from typing import Any

from .const import SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Hello World Sensor from a config entry."""

    # session = async_get_clientsession(hass)
    # session = async_create_clientsession(
    #     hass, verify_ssl=False, cookie_jar=CookieJar(unsafe=True)
    # )

    # async_add_entities([ExampleSensor(session, entry.data["username"])])

    async_add_entities(
        [HotWaterBinarySensor(entry.data["address_name"], entry.data["thermal_point"])]
    )

    return True


class HotWaterBinarySensor(BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.HEAT

    def __init__(self, address_name, thermal_point) -> None:
        self.address_name = address_name
        self.thermal_point = thermal_point

        self.affected_thermal_agent = ""
        self.description = ""
        self.estimated_fix_date = ""

        self._attr_name = self.address_name

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        return {
            "address_name": self.address_name,
            "thermal_point": self.thermal_point,
            "affected_thermal_agent": self.affected_thermal_agent,
            "description": self.description,
            "estimated_fix_date": self.estimated_fix_date,
        }

    async def async_update(self) -> None:
        self._attr_is_on = False
