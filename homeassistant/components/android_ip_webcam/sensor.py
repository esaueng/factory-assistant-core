"""Support for Android IP Webcam sensors."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from pydroid_ipcam import PyDroidIPCam

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN
from .coordinator import AndroidIPCamDataUpdateCoordinator
from .entity import AndroidIPCamBaseEntity


@dataclass(frozen=True, kw_only=True)
class AndroidIPWebcamSensorEntityDescription(SensorEntityDescription):
    """Entity description class for Android IP Webcam sensors."""

    value_fn: Callable[[PyDroidIPCam], StateType]
    unit_fn: Callable[[PyDroidIPCam], str | None] = lambda _: None


SENSOR_TYPES: tuple[AndroidIPWebcamSensorEntityDescription, ...] = (
    AndroidIPWebcamSensorEntityDescription(
        key="audio_connections",
        REDACTED_VALUE"audio_connections",
        name="Audio connections",
        state_class=SensorStateClass.TOTAL,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda ipcam: ipcam.status_data.get("audio_connections"),
    ),
    AndroidIPWebcamSensorEntityDescription(
        key="battery_level",
        name="Battery level",
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda ipcam: ipcam.get_sensor_value("battery_level"),
        unit_fn=lambda ipcam: ipcam.get_sensor_unit("battery_level"),
    ),
    AndroidIPWebcamSensorEntityDescription(
        key="battery_temp",
        REDACTED_VALUE"battery_temperature",
        name="Battery temperature",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda ipcam: ipcam.get_sensor_value("battery_temp"),
        unit_fn=lambda ipcam: ipcam.get_sensor_unit("battery_temp"),
    ),
    AndroidIPWebcamSensorEntityDescription(
        key="battery_voltage",
        name="Battery voltage",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda ipcam: ipcam.get_sensor_value("battery_voltage"),
        unit_fn=lambda ipcam: ipcam.get_sensor_unit("battery_voltage"),
    ),
    AndroidIPWebcamSensorEntityDescription(
        key="light",
        REDACTED_VALUE"light",
        name="Light level",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda ipcam: ipcam.get_sensor_value("light"),
        unit_fn=lambda ipcam: ipcam.get_sensor_unit("light"),
    ),
    AndroidIPWebcamSensorEntityDescription(
        key="motion",
        REDACTED_VALUE"motion",
        name="Motion",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda ipcam: ipcam.get_sensor_value("motion"),
        unit_fn=lambda ipcam: ipcam.get_sensor_unit("motion"),
    ),
    AndroidIPWebcamSensorEntityDescription(
        key="pressure",
        REDACTED_VALUE"pressure",
        name="Pressure",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda ipcam: ipcam.get_sensor_value("pressure"),
        unit_fn=lambda ipcam: ipcam.get_sensor_unit("pressure"),
    ),
    AndroidIPWebcamSensorEntityDescription(
        key="proximity",
        REDACTED_VALUE"proximity",
        name="Proximity",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda ipcam: ipcam.get_sensor_value("proximity"),
        unit_fn=lambda ipcam: ipcam.get_sensor_unit("proximity"),
    ),
    AndroidIPWebcamSensorEntityDescription(
        key="sound",
        REDACTED_VALUE"sound",
        name="Sound",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda ipcam: ipcam.get_sensor_value("sound"),
        unit_fn=lambda ipcam: ipcam.get_sensor_unit("sound"),
    ),
    AndroidIPWebcamSensorEntityDescription(
        key="video_connections",
        REDACTED_VALUE"video_connections",
        name="Video connections",
        state_class=SensorStateClass.TOTAL,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda ipcam: ipcam.status_data.get("video_connections"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the IP Webcam sensors from config entry."""

    coordinator: AndroidIPCamDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]
    sensor_types = [
        sensor
        for sensor in SENSOR_TYPES
        if sensor.key
        in coordinator.cam.enabled_sensors + ["audio_connections", "video_connections"]
    ]
    async_add_entities(
        IPWebcamSensor(coordinator, description) for description in sensor_types
    )


class IPWebcamSensor(AndroidIPCamBaseEntity, SensorEntity):
    """Representation of a IP Webcam sensor."""

    entity_description: AndroidIPWebcamSensorEntityDescription

    def __init__(
        self,
        coordinator: AndroidIPCamDataUpdateCoordinator,
        description: AndroidIPWebcamSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}-{description.key}"
        self.entity_description = description
        super().__init__(coordinator)

    @property
    def native_value(self) -> StateType:
        """Return native value of sensor."""
        return self.entity_description.value_fn(self.cam)

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return native unit of measurement of sensor."""
        return self.entity_description.unit_fn(self.cam)
