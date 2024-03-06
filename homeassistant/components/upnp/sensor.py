"""Support for UPnP/IGD Sensors."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    EntityCategory,
    UnitOfDataRate,
    UnitOfInformation,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    BYTES_RECEIVED,
    BYTES_SENT,
    DATA_PACKETS,
    DATA_RATE_PACKETS_PER_SECOND,
    DOMAIN,
    KIBIBYTES_PER_SEC_RECEIVED,
    KIBIBYTES_PER_SEC_SENT,
    LOGGER,
    PACKETS_PER_SEC_RECEIVED,
    PACKETS_PER_SEC_SENT,
    PACKETS_RECEIVED,
    PACKETS_SENT,
    ROUTER_IP,
    ROUTER_UPTIME,
    WAN_STATUS,
)
from .coordinator import UpnpDataUpdateCoordinator
from .entity import UpnpEntity, UpnpEntityDescription


@dataclass(frozen=True)
class UpnpSensorEntityDescription(UpnpEntityDescription, SensorEntityDescription):
    """A class that describes a sensor UPnP entities."""


SENSOR_DESCRIPTIONS: tuple[UpnpSensorEntityDescription, ...] = (
    UpnpSensorEntityDescription(
        key=BYTES_RECEIVED,
        REDACTED_VALUE"data_received",
        device_class=SensorDeviceClass.DATA_SIZE,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=0,
    ),
    UpnpSensorEntityDescription(
        key=BYTES_SENT,
        REDACTED_VALUE"data_sent",
        device_class=SensorDeviceClass.DATA_SIZE,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=0,
    ),
    UpnpSensorEntityDescription(
        key=PACKETS_RECEIVED,
        REDACTED_VALUE"packets_received",
        native_unit_of_measurement=DATA_PACKETS,
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=0,
    ),
    UpnpSensorEntityDescription(
        key=PACKETS_SENT,
        REDACTED_VALUE"packets_sent",
        native_unit_of_measurement=DATA_PACKETS,
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=0,
    ),
    UpnpSensorEntityDescription(
        key=ROUTER_IP,
        REDACTED_VALUE"external_ip",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    UpnpSensorEntityDescription(
        key=ROUTER_UPTIME,
        REDACTED_VALUE"uptime",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=0,
    ),
    UpnpSensorEntityDescription(
        key=WAN_STATUS,
        REDACTED_VALUE"wan_status",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    UpnpSensorEntityDescription(
        key=BYTES_RECEIVED,
        REDACTED_VALUE"download_speed",
        value_key=KIBIBYTES_PER_SEC_RECEIVED,
        unique_id="KiB/sec_received",
        device_class=SensorDeviceClass.DATA_RATE,
        native_unit_of_measurement=UnitOfDataRate.KIBIBYTES_PER_SECOND,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    UpnpSensorEntityDescription(
        key=BYTES_SENT,
        REDACTED_VALUE"upload_speed",
        value_key=KIBIBYTES_PER_SEC_SENT,
        unique_id="KiB/sec_sent",
        device_class=SensorDeviceClass.DATA_RATE,
        native_unit_of_measurement=UnitOfDataRate.KIBIBYTES_PER_SECOND,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    UpnpSensorEntityDescription(
        key=PACKETS_RECEIVED,
        REDACTED_VALUE"packet_download_speed",
        value_key=PACKETS_PER_SEC_RECEIVED,
        unique_id="packets/sec_received",
        native_unit_of_measurement=DATA_RATE_PACKETS_PER_SECOND,
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    UpnpSensorEntityDescription(
        key=PACKETS_SENT,
        REDACTED_VALUE"packet_upload_speed",
        value_key=PACKETS_PER_SEC_SENT,
        unique_id="packets/sec_sent",
        native_unit_of_measurement=DATA_RATE_PACKETS_PER_SECOND,
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the UPnP/IGD sensors."""
    coordinator: UpnpDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities: list[UpnpSensor] = [
        UpnpSensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in SENSOR_DESCRIPTIONS
        if coordinator.data.get(entity_description.key) is not None
    ]

    LOGGER.debug("Adding sensor entities: %s", entities)
    async_add_entities(entities)


class UpnpSensor(UpnpEntity, SensorEntity):
    """Base class for UPnP/IGD sensors."""

    entity_description: UpnpSensorEntityDescription

    @property
    def native_value(self) -> str | datetime | int | float | None:
        """Return the state of the device."""
        if (key := self.entity_description.value_key) is None:
            return None
        return self.coordinator.data[key]
