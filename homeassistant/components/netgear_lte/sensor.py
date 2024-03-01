"""Support for Netgear LTE sensors."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    EntityCategory,
    UnitOfInformation,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from . import ModemData
from .const import DOMAIN
from .entity import LTEEntity


@dataclass(frozen=True, kw_only=True)
class NetgearLTESensorEntityDescription(SensorEntityDescription):
    """Class describing Netgear LTE entities."""

    value_fn: Callable[[ModemData], StateType] | None = None


SENSORS: tuple[NetgearLTESensorEntityDescription, ...] = (
    NetgearLTESensorEntityDescription(
        key="sms",
        REDACTED_VALUE"sms",
        native_unit_of_measurement="unread",
        value_fn=lambda modem_data: sum(1 for x in modem_data.data.sms if x.unread),
    ),
    NetgearLTESensorEntityDescription(
        key="sms_total",
        REDACTED_VALUE"sms_total",
        native_unit_of_measurement="messages",
        value_fn=lambda modem_data: len(modem_data.data.sms),
    ),
    NetgearLTESensorEntityDescription(
        key="usage",
        REDACTED_VALUE"usage",
        device_class=SensorDeviceClass.DATA_SIZE,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        suggested_unit_of_measurement=UnitOfInformation.MEBIBYTES,
        suggested_display_precision=1,
        value_fn=lambda modem_data: modem_data.data.usage,
    ),
    NetgearLTESensorEntityDescription(
        key="radio_quality",
        REDACTED_VALUE"radio_quality",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=PERCENTAGE,
    ),
    NetgearLTESensorEntityDescription(
        key="rx_level",
        REDACTED_VALUE"rx_level",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    ),
    NetgearLTESensorEntityDescription(
        key="tx_level",
        REDACTED_VALUE"tx_level",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    ),
    NetgearLTESensorEntityDescription(
        key="upstream",
        REDACTED_VALUE"upstream",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    NetgearLTESensorEntityDescription(
        key="connection_text",
        REDACTED_VALUE"connection_text",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    NetgearLTESensorEntityDescription(
        key="connection_type",
        REDACTED_VALUE"connection_type",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    NetgearLTESensorEntityDescription(
        key="current_ps_service_type",
        REDACTED_VALUE"service_type",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    NetgearLTESensorEntityDescription(
        key="register_network_display",
        REDACTED_VALUE"register_network_display",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    NetgearLTESensorEntityDescription(
        key="current_band",
        REDACTED_VALUE"band",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    NetgearLTESensorEntityDescription(
        key="cell_id",
        REDACTED_VALUE"cell_id",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Netgear LTE sensor."""
    modem_data = hass.data[DOMAIN].get_modem_data(entry.data)

    async_add_entities(
        NetgearLTESensor(entry, modem_data, sensor) for sensor in SENSORS
    )


class NetgearLTESensor(LTEEntity, SensorEntity):
    """Base LTE sensor entity."""

    entity_description: NetgearLTESensorEntityDescription

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if self.entity_description.value_fn is not None:
            return self.entity_description.value_fn(self.modem_data)
        return getattr(self.modem_data.data, self.entity_description.key)
