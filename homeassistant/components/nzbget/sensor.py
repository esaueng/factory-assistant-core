"""Monitor the NZBGet API."""
from __future__ import annotations

from datetime import datetime, timedelta
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, UnitOfDataRate, UnitOfInformation
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.util.dt import utcnow

from . import NZBGetEntity
from .const import DATA_COORDINATOR, DOMAIN
from .coordinator import NZBGetDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="ArticleCacheMB",
        REDACTED_VALUE"article_cache",
        native_unit_of_measurement=UnitOfInformation.MEGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
    ),
    SensorEntityDescription(
        key="AverageDownloadRate",
        REDACTED_VALUE"average_speed",
        device_class=SensorDeviceClass.DATA_RATE,
        native_unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
        suggested_unit_of_measurement=UnitOfDataRate.MEGABYTES_PER_SECOND,
    ),
    SensorEntityDescription(
        key="DownloadPaused",
        REDACTED_VALUE"download_paused",
    ),
    SensorEntityDescription(
        key="DownloadRate",
        REDACTED_VALUE"speed",
        device_class=SensorDeviceClass.DATA_RATE,
        native_unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
        suggested_unit_of_measurement=UnitOfDataRate.MEGABYTES_PER_SECOND,
    ),
    SensorEntityDescription(
        key="DownloadedSizeMB",
        REDACTED_VALUE"size",
        native_unit_of_measurement=UnitOfInformation.MEGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
    ),
    SensorEntityDescription(
        key="FreeDiskSpaceMB",
        REDACTED_VALUE"disk_free",
        native_unit_of_measurement=UnitOfInformation.MEGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
    ),
    SensorEntityDescription(
        key="PostJobCount",
        REDACTED_VALUE"post_processing_jobs",
        native_unit_of_measurement="Jobs",
    ),
    SensorEntityDescription(
        key="PostPaused",
        REDACTED_VALUE"post_processing_paused",
    ),
    SensorEntityDescription(
        key="RemainingSizeMB",
        REDACTED_VALUE"queue_size",
        native_unit_of_measurement=UnitOfInformation.MEGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
    ),
    SensorEntityDescription(
        key="UpTimeSec",
        REDACTED_VALUE"uptime",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
    SensorEntityDescription(
        key="DownloadLimit",
        REDACTED_VALUE"speed_limit",
        device_class=SensorDeviceClass.DATA_RATE,
        native_unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
        suggested_unit_of_measurement=UnitOfDataRate.MEGABYTES_PER_SECOND,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up NZBGet sensor based on a config entry."""
    coordinator: NZBGetDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        DATA_COORDINATOR
    ]
    entities = [
        NZBGetSensor(coordinator, entry.entry_id, entry.data[CONF_NAME], description)
        for description in SENSOR_TYPES
    ]

    async_add_entities(entities)


class NZBGetSensor(NZBGetEntity, SensorEntity):
    """Representation of a NZBGet sensor."""

    def __init__(
        self,
        coordinator: NZBGetDataUpdateCoordinator,
        entry_id: str,
        entry_name: str,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize a new NZBGet sensor."""
        super().__init__(
            coordinator=coordinator,
            entry_id=entry_id,
            entry_name=entry_name,
        )

        self.entity_description = description
        self._attr_unique_id = f"{entry_id}_{description.key}"

    @property
    def native_value(self) -> StateType | datetime:
        """Return the state of the sensor."""
        sensor_type = self.entity_description.key
        value = self.coordinator.data["status"].get(sensor_type)

        if value is not None and "UpTimeSec" in sensor_type and value > 0:
            uptime = utcnow().replace(microsecond=0) - timedelta(seconds=value)
            if not isinstance(self._attr_native_value, datetime) or abs(
                uptime - self._attr_native_value
            ) > timedelta(seconds=5):
                return uptime
        return value
