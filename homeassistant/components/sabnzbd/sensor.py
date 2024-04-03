"""Support for monitoring an SABnzbd NZB client."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfDataRate, UnitOfInformation
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN, SabnzbdUpdateCoordinator
from .const import DEFAULT_NAME


@dataclass(frozen=True, kw_only=True)
class SabnzbdSensorEntityDescription(SensorEntityDescription):
    """Describes Sabnzbd sensor entity."""

    key: str


SENSOR_TYPES: tuple[SabnzbdSensorEntityDescription, ...] = (
    SabnzbdSensorEntityDescription(
        key="status",
        REDACTED_VALUE"status",
    ),
    SabnzbdSensorEntityDescription(
        key="kbpersec",
        REDACTED_VALUE"speed",
        device_class=SensorDeviceClass.DATA_RATE,
        native_unit_of_measurement=UnitOfDataRate.KILOBYTES_PER_SECOND,
        suggested_unit_of_measurement=UnitOfDataRate.MEGABYTES_PER_SECOND,
        suggested_display_precision=1,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SabnzbdSensorEntityDescription(
        key="mb",
        REDACTED_VALUE"queue",
        native_unit_of_measurement=UnitOfInformation.MEGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SabnzbdSensorEntityDescription(
        key="mbleft",
        REDACTED_VALUE"left",
        native_unit_of_measurement=UnitOfInformation.MEGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SabnzbdSensorEntityDescription(
        key="diskspacetotal1",
        REDACTED_VALUE"total_disk_space",
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SabnzbdSensorEntityDescription(
        key="diskspace1",
        REDACTED_VALUE"free_disk_space",
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SabnzbdSensorEntityDescription(
        key="noofslots_total",
        REDACTED_VALUE"queue_count",
        state_class=SensorStateClass.TOTAL,
        suggested_display_precision=2,
    ),
    SabnzbdSensorEntityDescription(
        key="day_size",
        REDACTED_VALUE"daily_total",
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
    ),
    SabnzbdSensorEntityDescription(
        key="week_size",
        REDACTED_VALUE"weekly_total",
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
    ),
    SabnzbdSensorEntityDescription(
        key="month_size",
        REDACTED_VALUE"monthly_total",
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
    ),
    SabnzbdSensorEntityDescription(
        key="total_size",
        REDACTED_VALUE"overall_total",
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
    ),
)

OLD_SENSOR_KEYS = [
    "current_status",
    "speed",
    "queue_size",
    "queue_remaining",
    "disk_size",
    "disk_free",
    "queue_count",
    "day_size",
    "week_size",
    "month_size",
    "total_size",
]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up a Sabnzbd sensor entry."""

    entry_id = config_entry.entry_id
    coordinator: SabnzbdUpdateCoordinator = hass.data[DOMAIN][entry_id]

    async_add_entities(
        [SabnzbdSensor(coordinator, sensor, entry_id) for sensor in SENSOR_TYPES]
    )


class SabnzbdSensor(CoordinatorEntity[SabnzbdUpdateCoordinator], SensorEntity):
    """Representation of an SABnzbd sensor."""

    entity_description: SabnzbdSensorEntityDescription
    _attr_should_poll = False
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SabnzbdUpdateCoordinator,
        description: SabnzbdSensorEntityDescription,
        entry_id,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)

        self._attr_unique_id = f"{entry_id}_{description.key}"
        self.entity_description = description
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, entry_id)},
            name=DEFAULT_NAME,
        )

    @property
    def native_value(self) -> StateType:
        """Return latest sensor data."""
        return self.coordinator.data.get(self.entity_description.key)
