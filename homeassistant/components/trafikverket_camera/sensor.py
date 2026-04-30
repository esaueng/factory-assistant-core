"""Sensor platform for Trafikverket Camera integration."""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import DEGREE
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import StateType

from . import TVCameraConfigEntry
from .coordinator import CameraData
from .entity import TrafikverketCameraNonCameraEntity

PARALLEL_UPDATES = 0


@dataclass(frozen=True, kw_only=True)
class TVCameraSensorEntityDescription(SensorEntityDescription):
    """Describes Trafikverket Camera sensor entity."""

    value_fn: Callable[[CameraData], StateType | datetime]


SENSOR_TYPES: tuple[TVCameraSensorEntityDescription, ...] = (
    TVCameraSensorEntityDescription(
        key="direction",
        REDACTED_VALUE"direction",
        native_unit_of_measurement=DEGREE,
        value_fn=lambda data: data.data.direction,
    ),
    TVCameraSensorEntityDescription(
        key="modified",
        REDACTED_VALUE"modified",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda data: data.data.modified,
        entity_registry_enabled_default=False,
    ),
    TVCameraSensorEntityDescription(
        key="photo_time",
        REDACTED_VALUE"photo_time",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda data: data.data.phototime,
    ),
    TVCameraSensorEntityDescription(
        key="photo_url",
        REDACTED_VALUE"photo_url",
        value_fn=lambda data: data.data.photourl,
        entity_registry_enabled_default=False,
    ),
    TVCameraSensorEntityDescription(
        key="status",
        REDACTED_VALUE"status",
        value_fn=lambda data: data.data.status,
        entity_registry_enabled_default=False,
    ),
    TVCameraSensorEntityDescription(
        key="camera_type",
        REDACTED_VALUE"camera_type",
        value_fn=lambda data: data.data.camera_type,
        entity_registry_enabled_default=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TVCameraConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Trafikverket Camera sensor platform."""

    coordinator = entry.runtime_data
    async_add_entities(
        TrafikverketCameraSensor(coordinator, entry.entry_id, description)
        for description in SENSOR_TYPES
    )


class TrafikverketCameraSensor(TrafikverketCameraNonCameraEntity, SensorEntity):
    """Representation of a Trafikverket Camera Sensor."""

    entity_description: TVCameraSensorEntityDescription

    @callback
    def _update_attr(self) -> None:
        """Update _attr."""
        self._attr_native_value = self.entity_description.value_fn(
            self.coordinator.data
        )
