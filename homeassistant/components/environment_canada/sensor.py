"""Support for the Environment Canada weather service."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_LOCATION,
    DEGREE,
    PERCENTAGE,
    UV_INDEX,
    UnitOfLength,
    UnitOfPrecipitationDepth,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import device_info
from .const import ATTR_STATION, DOMAIN

ATTR_TIME = "alert time"


@dataclass(frozen=True, kw_only=True)
class ECSensorEntityDescription(SensorEntityDescription):
    """Describes Environment Canada sensor entity."""

    value_fn: Callable[[Any], Any]
    transform: Callable[[Any], Any] | None = None


SENSOR_TYPES: tuple[ECSensorEntityDescription, ...] = (
    ECSensorEntityDescription(
        key="condition",
        REDACTED_VALUE"condition",
        value_fn=lambda data: data.conditions.get("condition", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="dewpoint",
        REDACTED_VALUE"dewpoint",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.conditions.get("dewpoint", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="high_temp",
        REDACTED_VALUE"high_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.conditions.get("high_temp", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="humidex",
        REDACTED_VALUE"humidex",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.conditions.get("humidex", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.conditions.get("humidity", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="icon_code",
        REDACTED_VALUE"icon_code",
        name="Icon code",
        value_fn=lambda data: data.conditions.get("icon_code", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="low_temp",
        REDACTED_VALUE"low_temp",
        name="Low temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.conditions.get("low_temp", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="normal_high",
        REDACTED_VALUE"normal_high",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.conditions.get("normal_high", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="normal_low",
        REDACTED_VALUE"normal_low",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.conditions.get("normal_low", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="pop",
        REDACTED_VALUE"pop",
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda data: data.conditions.get("pop", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="precip_yesterday",
        REDACTED_VALUE"precip_yesterday",
        device_class=SensorDeviceClass.PRECIPITATION,
        native_unit_of_measurement=UnitOfPrecipitationDepth.MILLIMETERS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.conditions.get("precip_yesterday", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="pressure",
        REDACTED_VALUE"pressure",
        device_class=SensorDeviceClass.PRESSURE,
        native_unit_of_measurement=UnitOfPressure.KPA,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.conditions.get("pressure", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.conditions.get("temperature", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="tendency",
        REDACTED_VALUE"tendency",
        value_fn=lambda data: data.conditions.get("tendency", {}).get("value"),
        transform=lambda val: str(val).capitalize(),
    ),
    ECSensorEntityDescription(
        key="text_summary",
        REDACTED_VALUE"text_summary",
        value_fn=lambda data: data.conditions.get("text_summary", {}).get("value"),
        transform=lambda val: val[:255],
    ),
    ECSensorEntityDescription(
        key="timestamp",
        REDACTED_VALUE"timestamp",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda data: data.metadata.get("timestamp"),
    ),
    ECSensorEntityDescription(
        key="uv_index",
        REDACTED_VALUE"uv_index",
        native_unit_of_measurement=UV_INDEX,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.conditions.get("uv_index", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="visibility",
        REDACTED_VALUE"visibility",
        native_unit_of_measurement=UnitOfLength.KILOMETERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.conditions.get("visibility", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="wind_bearing",
        REDACTED_VALUE"wind_bearing",
        native_unit_of_measurement=DEGREE,
        value_fn=lambda data: data.conditions.get("wind_bearing", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="wind_chill",
        REDACTED_VALUE"wind_chill",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.conditions.get("wind_chill", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="wind_dir",
        REDACTED_VALUE"wind_dir",
        value_fn=lambda data: data.conditions.get("wind_dir", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="wind_gust",
        REDACTED_VALUE"wind_gust",
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.conditions.get("wind_gust", {}).get("value"),
    ),
    ECSensorEntityDescription(
        key="wind_speed",
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.conditions.get("wind_speed", {}).get("value"),
    ),
)


def _get_aqhi_value(data):
    if (aqhi := data.current) is not None:
        return aqhi
    if data.forecasts and (hourly := data.forecasts.get("hourly")) is not None:
        if values := list(hourly.values()):
            return values[0]
    return None


AQHI_SENSOR = ECSensorEntityDescription(
    key="aqhi",
    REDACTED_VALUE"aqhi",
    device_class=SensorDeviceClass.AQI,
    state_class=SensorStateClass.MEASUREMENT,
    value_fn=_get_aqhi_value,
)

ALERT_TYPES: tuple[ECSensorEntityDescription, ...] = (
    ECSensorEntityDescription(
        key="advisories",
        REDACTED_VALUE"advisories",
        value_fn=lambda data: data.alerts.get("advisories", {}).get("value"),
        transform=len,
    ),
    ECSensorEntityDescription(
        key="endings",
        REDACTED_VALUE"endings",
        value_fn=lambda data: data.alerts.get("endings", {}).get("value"),
        transform=len,
    ),
    ECSensorEntityDescription(
        key="statements",
        REDACTED_VALUE"statements",
        value_fn=lambda data: data.alerts.get("statements", {}).get("value"),
        transform=len,
    ),
    ECSensorEntityDescription(
        key="warnings",
        REDACTED_VALUE"warnings",
        value_fn=lambda data: data.alerts.get("warnings", {}).get("value"),
        transform=len,
    ),
    ECSensorEntityDescription(
        key="watches",
        REDACTED_VALUE"watches",
        value_fn=lambda data: data.alerts.get("watches", {}).get("value"),
        transform=len,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add a weather entity from a config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["weather_coordinator"]
    sensors: list[ECBaseSensor] = [ECSensor(coordinator, desc) for desc in SENSOR_TYPES]
    sensors.extend([ECAlertSensor(coordinator, desc) for desc in ALERT_TYPES])
    aqhi_coordinator = hass.data[DOMAIN][config_entry.entry_id]["aqhi_coordinator"]
    sensors.append(ECSensor(aqhi_coordinator, AQHI_SENSOR))
    async_add_entities(sensors)


class ECBaseSensor(CoordinatorEntity, SensorEntity):
    """Environment Canada sensor base."""

    entity_description: ECSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(self, coordinator, description):
        """Initialize the base sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._ec_data = coordinator.ec_data
        self._attr_attribution = self._ec_data.metadata["attribution"]
        self._attr_unique_id = f"{coordinator.config_entry.title}-{description.key}"
        self._attr_device_info = device_info(coordinator.config_entry)

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        value = self.entity_description.value_fn(self._ec_data)
        if value is not None and self.entity_description.transform:
            value = self.entity_description.transform(value)
        return value


class ECSensor(ECBaseSensor):
    """Environment Canada sensor for conditions."""

    def __init__(self, coordinator, description):
        """Initialize the sensor."""
        super().__init__(coordinator, description)
        self._attr_extra_state_attributes = {
            ATTR_LOCATION: self._ec_data.metadata.get("location"),
            ATTR_STATION: self._ec_data.metadata.get("station"),
        }


class ECAlertSensor(ECBaseSensor):
    """Environment Canada sensor for alerts."""

    @property
    def extra_state_attributes(self):
        """Return the extra state attributes."""
        value = self.entity_description.value_fn(self._ec_data)
        if not value:
            return None

        extra_state_attrs = {
            ATTR_LOCATION: self._ec_data.metadata.get("location"),
            ATTR_STATION: self._ec_data.metadata.get("station"),
        }
        for index, alert in enumerate(value, start=1):
            extra_state_attrs[f"alert_{index}"] = alert.get("title")
            extra_state_attrs[f"alert_time_{index}"] = alert.get("date")

        return extra_state_attrs
