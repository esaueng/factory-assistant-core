"""Support for monitoring an SABnzbd NZB client."""

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfDataRate, UnitOfInformation
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import StateType

from .coordinator import SabnzbdConfigEntry
from .entity import SabnzbdEntity


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


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: SabnzbdConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up a Sabnzbd sensor entry."""
    coordinator = config_entry.runtime_data

    async_add_entities([SabnzbdSensor(coordinator, sensor) for sensor in SENSOR_TYPES])


class SabnzbdSensor(SabnzbdEntity, SensorEntity):
    """Representation of an SABnzbd sensor."""

    entity_description: SabnzbdSensorEntityDescription

    @property
    def native_value(self) -> StateType:
        """Return latest sensor data."""
        return self.coordinator.data.get(self.entity_description.key)
