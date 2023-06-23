"""Binary sensor indicating if there is hot water at a specified thermal point"""
import logging

import async_timeout

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from collections.abc import Mapping
from typing import Any

from .const import SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

CMTEB_STATE_URL = "https://www.cmteb.ro/functionare_sistem_termoficare.php"
START_OF_DATA_COMMENT = "<!-- start: toate sectoarele -->"
DATA_TABLE_START = "<table"
DATA_TABLE_END = "</table>"
DATA_TABLE_COLUMN_START = "<td>"
DATA_TABLE_COLUMN_END = "</td>"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Hello World Sensor from a config entry."""

    session = async_get_clientsession(hass)
    # session = async_create_clientsession(
    #     hass, verify_ssl=False, cookie_jar=CookieJar(unsafe=True)
    # )

    # async_add_entities([ExampleSensor(session, entry.data["username"])])

    async_add_entities(
        [
            HotWaterBinarySensor(
                session, entry.data["address_name"], entry.data["thermal_point"]
            )
        ],
        update_before_add=True,
    )

    return True


class HotWaterBinarySensor(BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.HEAT

    def __init__(self, session, address_name, thermal_point) -> None:
        self.session = session
        self.address_name = address_name
        self.thermal_point = thermal_point

        self.affected_thermal_agent = ""
        self.description = ""
        self.estimated_fix_date = ""

        self._attr_name = "hot_water_" + self.address_name

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
        try:
            async with async_timeout.timeout(5):
                headers = {"User-Agent": "HA"}
                response = await self.session.get(
                    CMTEB_STATE_URL,
                    allow_redirects=True,
                    headers=headers,
                )

                html = await response.text()

                self.reset_data()
                self.parse_html(html)
        except Exception as err:
            _LOGGER.error("Error: %s", err)

    def parse_html(self, html: str):
        # All the date is stored in a <table> following a specific html comment
        start_index = html.find(START_OF_DATA_COMMENT)
        start_index = html.find(DATA_TABLE_START, start_index)
        end_index = html.find(DATA_TABLE_END, start_index)

        table_data = html[start_index:end_index]

        # How the thermal point will appear in the table
        possible_strings = [
            f"Punct termic: <strong>{ self.thermal_point }</strong>",
            f"Punct termic: { self.thermal_point }",
        ]

        for possible_string in possible_strings:
            index = table_data.find(possible_string)

            if index != -1:
                self._attr_is_on = False

                _LOGGER.info("Thermal point is affected: %s", self.thermal_point)

                index, self.affected_thermal_agent = self.extract_column_data(
                    table_data, index
                )
                index, self.description = self.extract_column_data(table_data, index)
                index, self.estimated_fix_date = self.extract_column_data(
                    table_data, index
                )

                break

    def extract_column_data(self, table_data: str, start_index: int):
        if start_index == -1:
            return (-1, "")

        start_index = table_data.find(DATA_TABLE_COLUMN_START, start_index)
        end_index = table_data.find(DATA_TABLE_COLUMN_END, start_index)

        if start_index == -1 or end_index == -1:
            return (-1, "")

        start_index += len(DATA_TABLE_COLUMN_START)
        return (end_index, table_data[start_index:end_index].strip())

    def reset_data(self):
        self._attr_is_on = True
        self.affected_thermal_agent = ""
        self.description = ""
        self.estimated_fix_date = ""
