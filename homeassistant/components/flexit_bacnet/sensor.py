"""The Flexit Nordic (BACnet) integration."""

from collections.abc import Callable
from dataclasses import dataclass

from flexit_bacnet import FlexitBACnet

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    REVOLUTIONS_PER_MINUTE,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import StateType

from .coordinator import FlexitConfigEntry, FlexitCoordinator
from .entity import FlexitEntity


@dataclass(kw_only=True, frozen=True)
class FlexitSensorEntityDescription(SensorEntityDescription):
    """Describes a Flexit sensor entity."""

    value_fn: Callable[[FlexitBACnet], float]


SENSOR_TYPES: tuple[FlexitSensorEntityDescription, ...] = (
    FlexitSensorEntityDescription(
        key="outside_air_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        REDACTED_VALUE"outside_air_temperature",
        value_fn=lambda data: data.outside_air_temperature,
    ),
    FlexitSensorEntityDescription(
        key="supply_air_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        REDACTED_VALUE"supply_air_temperature",
        value_fn=lambda data: data.supply_air_temperature,
    ),
    FlexitSensorEntityDescription(
        key="exhaust_air_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        REDACTED_VALUE"exhaust_air_temperature",
        value_fn=lambda data: data.exhaust_air_temperature,
    ),
    FlexitSensorEntityDescription(
        key="extract_air_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        REDACTED_VALUE"extract_air_temperature",
        value_fn=lambda data: data.extract_air_temperature,
    ),
    FlexitSensorEntityDescription(
        key="room_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        REDACTED_VALUE"room_temperature",
        value_fn=lambda data: data.room_temperature,
    ),
    FlexitSensorEntityDescription(
        key="fireplace_ventilation_remaining_duration",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        REDACTED_VALUE"fireplace_ventilation_remaining_duration",
        value_fn=lambda data: data.fireplace_ventilation_remaining_duration,
        suggested_display_precision=0,
    ),
    FlexitSensorEntityDescription(
        key="rapid_ventilation_remaining_duration",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        REDACTED_VALUE"rapid_ventilation_remaining_duration",
        value_fn=lambda data: data.rapid_ventilation_remaining_duration,
        suggested_display_precision=0,
    ),
    FlexitSensorEntityDescription(
        key="supply_air_fan_control_signal",
        state_class=SensorStateClass.MEASUREMENT,
        REDACTED_VALUE"supply_air_fan_control_signal",
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda data: data.supply_air_fan_control_signal,
    ),
    FlexitSensorEntityDescription(
        key="supply_air_fan_rpm",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        REDACTED_VALUE"supply_air_fan_rpm",
        value_fn=lambda data: data.supply_air_fan_rpm,
    ),
    FlexitSensorEntityDescription(
        key="exhaust_air_fan_control_signal",
        state_class=SensorStateClass.MEASUREMENT,
        REDACTED_VALUE"exhaust_air_fan_control_signal",
        value_fn=lambda data: data.exhaust_air_fan_control_signal,
        native_unit_of_measurement=PERCENTAGE,
    ),
    FlexitSensorEntityDescription(
        key="exhaust_air_fan_rpm",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        REDACTED_VALUE"exhaust_air_fan_rpm",
        value_fn=lambda data: data.exhaust_air_fan_rpm,
    ),
    FlexitSensorEntityDescription(
        key="electric_heater_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        REDACTED_VALUE"electric_heater_power",
        value_fn=lambda data: data.electric_heater_power,
        suggested_display_precision=3,
    ),
    FlexitSensorEntityDescription(
        key="air_filter_operating_time",
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=0,
        native_unit_of_measurement=UnitOfTime.HOURS,
        REDACTED_VALUE"air_filter_operating_time",
        value_fn=lambda data: data.air_filter_operating_time,
    ),
    FlexitSensorEntityDescription(
        key="heat_exchanger_efficiency",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        REDACTED_VALUE"heat_exchanger_efficiency",
        value_fn=lambda data: data.heat_exchanger_efficiency,
    ),
    FlexitSensorEntityDescription(
        key="heat_exchanger_speed",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        REDACTED_VALUE"heat_exchanger_speed",
        value_fn=lambda data: data.heat_exchanger_speed,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: FlexitConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Flexit (bacnet) sensor from a config entry."""
    coordinator = config_entry.runtime_data

    async_add_entities(
        FlexitSensor(coordinator, description) for description in SENSOR_TYPES
    )


# Coordinator is used to centralize the data updates
PARALLEL_UPDATES = 0


class FlexitSensor(FlexitEntity, SensorEntity):
    """Representation of a Flexit (bacnet) Sensor."""

    entity_description: FlexitSensorEntityDescription

    def __init__(
        self,
        coordinator: FlexitCoordinator,
        entity_description: FlexitSensorEntityDescription,
    ) -> None:
        """Initialize Flexit (bacnet) sensor."""
        super().__init__(coordinator)

        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.device.serial_number}-{entity_description.key}"
        )

    @property
    def native_value(self) -> StateType:
        """Return value of sensor."""
        return self.entity_description.value_fn(self.coordinator.data)
