"""Imeon inverter sensor support."""

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    EntityCategory,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import ATTR_BATTERY_STATUS, ATTR_INVERTER_STATE, ATTR_TIMELINE_STATUS
from .coordinator import InverterCoordinator
from .entity import InverterEntity

type InverterConfigEntry = ConfigEntry[InverterCoordinator]

_LOGGER = logging.getLogger(__name__)


SENSOR_DESCRIPTIONS = (
    # Battery
    SensorEntityDescription(
        key="battery_power",
        REDACTED_VALUE"battery_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="battery_soc",
        REDACTED_VALUE"battery_soc",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="battery_status",
        REDACTED_VALUE"battery_status",
        device_class=SensorDeviceClass.ENUM,
        options=ATTR_BATTERY_STATUS,
    ),
    SensorEntityDescription(
        key="battery_stored",
        REDACTED_VALUE"battery_stored",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="battery_consumed",
        REDACTED_VALUE"battery_consumed",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Grid
    SensorEntityDescription(
        key="grid_current_l1",
        REDACTED_VALUE"grid_current_l1",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="grid_current_l2",
        REDACTED_VALUE"grid_current_l2",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="grid_current_l3",
        REDACTED_VALUE"grid_current_l3",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="grid_frequency",
        REDACTED_VALUE"grid_frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="grid_voltage_l1",
        REDACTED_VALUE"grid_voltage_l1",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="grid_voltage_l2",
        REDACTED_VALUE"grid_voltage_l2",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="grid_voltage_l3",
        REDACTED_VALUE"grid_voltage_l3",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # AC Input
    SensorEntityDescription(
        key="input_power_l1",
        REDACTED_VALUE"input_power_l1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="input_power_l2",
        REDACTED_VALUE"input_power_l2",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="input_power_l3",
        REDACTED_VALUE"input_power_l3",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="input_power_total",
        REDACTED_VALUE"input_power_total",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Inverter settings
    SensorEntityDescription(
        key="inverter_charging_current_limit",
        REDACTED_VALUE"inverter_charging_current_limit",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="inverter_injection_power_limit",
        REDACTED_VALUE"inverter_injection_power_limit",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="manager_inverter_state",
        REDACTED_VALUE"manager_inverter_state",
        device_class=SensorDeviceClass.ENUM,
        options=ATTR_INVERTER_STATE,
    ),
    # Meter
    SensorEntityDescription(
        key="meter_power",
        REDACTED_VALUE"meter_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # AC Output
    SensorEntityDescription(
        key="output_current_l1",
        REDACTED_VALUE"output_current_l1",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="output_current_l2",
        REDACTED_VALUE"output_current_l2",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="output_current_l3",
        REDACTED_VALUE"output_current_l3",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="output_frequency",
        REDACTED_VALUE"output_frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="output_power_l1",
        REDACTED_VALUE"output_power_l1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="output_power_l2",
        REDACTED_VALUE"output_power_l2",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="output_power_l3",
        REDACTED_VALUE"output_power_l3",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="output_power_total",
        REDACTED_VALUE"output_power_total",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="output_voltage_l1",
        REDACTED_VALUE"output_voltage_l1",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="output_voltage_l2",
        REDACTED_VALUE"output_voltage_l2",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="output_voltage_l3",
        REDACTED_VALUE"output_voltage_l3",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Solar Panel
    SensorEntityDescription(
        key="pv_consumed",
        REDACTED_VALUE"pv_consumed",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="pv_injected",
        REDACTED_VALUE"pv_injected",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="pv_power_1",
        REDACTED_VALUE"pv_power_1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="pv_power_2",
        REDACTED_VALUE"pv_power_2",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="pv_power_total",
        REDACTED_VALUE"pv_power_total",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Temperature
    SensorEntityDescription(
        key="temp_air_temperature",
        REDACTED_VALUE"temp_air_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="temp_component_temperature",
        REDACTED_VALUE"temp_component_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Monitoring (data over the last 24 hours)
    SensorEntityDescription(
        key="monitoring_self_consumption",
        REDACTED_VALUE"monitoring_self_consumption",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.TOTAL,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="monitoring_self_sufficiency",
        REDACTED_VALUE"monitoring_self_sufficiency",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.TOTAL,
        suggested_display_precision=2,
    ),
    # Monitoring (instant minute data)
    SensorEntityDescription(
        key="monitoring_minute_building_consumption",
        REDACTED_VALUE"monitoring_minute_building_consumption",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="monitoring_minute_grid_consumption",
        REDACTED_VALUE"monitoring_minute_grid_consumption",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="monitoring_minute_grid_injection",
        REDACTED_VALUE"monitoring_minute_grid_injection",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="monitoring_minute_grid_power_flow",
        REDACTED_VALUE"monitoring_minute_grid_power_flow",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="monitoring_minute_solar_production",
        REDACTED_VALUE"monitoring_minute_solar_production",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    # Timeline
    SensorEntityDescription(
        key="timeline_type_msg",
        REDACTED_VALUE"timeline_type_msg",
        device_class=SensorDeviceClass.ENUM,
        options=ATTR_TIMELINE_STATUS,
    ),
    # Daily energy counters
    SensorEntityDescription(
        key="energy_pv",
        REDACTED_VALUE"energy_pv",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="energy_grid_injected",
        REDACTED_VALUE"energy_grid_injected",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="energy_grid_consumed",
        REDACTED_VALUE"energy_grid_consumed",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="energy_building_consumption",
        REDACTED_VALUE"energy_building_consumption",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="energy_battery_stored",
        REDACTED_VALUE"energy_battery_stored",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="energy_battery_consumed",
        REDACTED_VALUE"energy_battery_consumed",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: InverterConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Create each sensor for a given config entry."""

    coordinator = entry.runtime_data
    async_add_entities(
        InverterSensor(coordinator, entry, description)
        for description in SENSOR_DESCRIPTIONS
    )


class InverterSensor(InverterEntity, SensorEntity):
    """Representation of an Imeon inverter sensor."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> StateType | None:
        """Return the state of the entity."""
        return self.coordinator.data.get(self.data_key)
