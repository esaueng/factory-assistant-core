"""Support for EZVIZ sensors."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import EzvizConfigEntry, EzvizDataUpdateCoordinator
from .entity import EzvizEntity

PARALLEL_UPDATES = 1

SENSOR_TYPES: dict[str, SensorEntityDescription] = {
    "battery_level": SensorEntityDescription(
        key="battery_level",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
    ),
    "alarm_sound_mod": SensorEntityDescription(
        key="alarm_sound_mod",
        REDACTED_VALUE"alarm_sound_mod",
        entity_registry_enabled_default=False,
    ),
    "last_alarm_time": SensorEntityDescription(
        key="last_alarm_time",
        REDACTED_VALUE"last_alarm_time",
        entity_registry_enabled_default=False,
    ),
    "Seconds_Last_Trigger": SensorEntityDescription(
        key="Seconds_Last_Trigger",
        REDACTED_VALUE"seconds_last_trigger",
        entity_registry_enabled_default=False,
    ),
    "last_alarm_pic": SensorEntityDescription(
        key="last_alarm_pic",
        REDACTED_VALUE"last_alarm_pic",
        entity_registry_enabled_default=False,
    ),
    "supported_channels": SensorEntityDescription(
        key="supported_channels",
        REDACTED_VALUE"supported_channels",
    ),
    "local_ip": SensorEntityDescription(
        key="local_ip",
        REDACTED_VALUE"local_ip",
    ),
    "wan_ip": SensorEntityDescription(
        key="wan_ip",
        REDACTED_VALUE"wan_ip",
    ),
    "PIR_Status": SensorEntityDescription(
        key="PIR_Status",
        REDACTED_VALUE"pir_status",
    ),
    "last_alarm_type_code": SensorEntityDescription(
        key="last_alarm_type_code",
        REDACTED_VALUE"last_alarm_type_code",
    ),
    "last_alarm_type_name": SensorEntityDescription(
        key="last_alarm_type_name",
        REDACTED_VALUE"last_alarm_type_name",
    ),
    "Record_Mode": SensorEntityDescription(
        key="Record_Mode",
        REDACTED_VALUE"record_mode",
        entity_registry_enabled_default=False,
    ),
    "battery_camera_work_mode": SensorEntityDescription(
        key="battery_camera_work_mode",
        REDACTED_VALUE"battery_camera_work_mode",
        entity_registry_enabled_default=False,
    ),
    "powerStatus": SensorEntityDescription(
        key="powerStatus",
        REDACTED_VALUE"power_status",
        entity_registry_enabled_default=False,
    ),
    "OnlineStatus": SensorEntityDescription(
        key="OnlineStatus",
        REDACTED_VALUE"online_status",
        entity_registry_enabled_default=False,
    ),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: EzvizConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up EZVIZ sensors based on a config entry."""
    coordinator = entry.runtime_data
    entities: list[EzvizSensor] = []

    for camera, sensors in coordinator.data.items():
        entities.extend(
            EzvizSensor(coordinator, camera, sensor)
            for sensor, value in sensors.items()
            if sensor in SENSOR_TYPES and value is not None
        )

        optionals = sensors.get("optionals", {})
        entities.extend(
            EzvizSensor(coordinator, camera, optional_key)
            for optional_key in ("powerStatus", "OnlineStatus")
            if optional_key in optionals
        )

        if "mode" in optionals.get("Record_Mode", {}):
            entities.append(EzvizSensor(coordinator, camera, "mode"))

    async_add_entities(entities)


class EzvizSensor(EzvizEntity, SensorEntity):
    """Representation of a EZVIZ sensor."""

    def __init__(
        self, coordinator: EzvizDataUpdateCoordinator, serial: str, sensor: str
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, serial)
        self._sensor_name = sensor
        self._attr_unique_id = f"{serial}_{self._camera_name}.{sensor}"
        self.entity_description = SENSOR_TYPES[sensor]

    @property
    def native_value(self) -> int | str:
        """Return the state of the sensor."""
        return self.data[self._sensor_name]
