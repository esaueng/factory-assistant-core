"""Provides a sensor to track various status aspects of a NUT device."""

import logging
from typing import Final

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    EntityCategory,
    UnitOfApparentPower,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import KEY_STATUS, KEY_STATUS_DISPLAY, STATE_TYPES
from .coordinator import NutConfigEntry
from .entity import NUTBaseEntity

# Coordinator is used to centralize the data updates
PARALLEL_UPDATES = 0

AMBIENT_PRESENT = "ambient.present"
AMBIENT_SENSORS = {
    "ambient.humidity",
    "ambient.humidity.status",
    "ambient.temperature",
    "ambient.temperature.status",
}
BATTERY_CHARGER_STATUS_OPTIONS = [
    "charging",
    "discharging",
    "floating",
    "resting",
    "unknown",
    "disabled",
    "off",
]
FREQUENCY_STATUS_OPTIONS = [
    "good",
    "out-of-range",
]
THRESHOLD_STATUS_OPTIONS = [
    "good",
    "warning-low",
    "critical-low",
    "warning-high",
    "critical-high",
]
UPS_BEEPER_STATUS_OPTIONS = [
    "enabled",
    "disabled",
    "muted",
]

_LOGGER = logging.getLogger(__name__)


SENSOR_TYPES: Final[dict[str, SensorEntityDescription]] = {
    "ambient.humidity": SensorEntityDescription(
        key="ambient.humidity",
        REDACTED_VALUE"ambient_humidity",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "ambient.humidity.status": SensorEntityDescription(
        key="ambient.humidity.status",
        REDACTED_VALUE"ambient_humidity_status",
        device_class=SensorDeviceClass.ENUM,
        options=THRESHOLD_STATUS_OPTIONS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "ambient.temperature": SensorEntityDescription(
        key="ambient.temperature",
        REDACTED_VALUE"ambient_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "ambient.temperature.status": SensorEntityDescription(
        key="ambient.temperature.status",
        REDACTED_VALUE"ambient_temperature_status",
        device_class=SensorDeviceClass.ENUM,
        options=THRESHOLD_STATUS_OPTIONS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "battery.alarm.threshold": SensorEntityDescription(
        key="battery.alarm.threshold",
        REDACTED_VALUE"battery_alarm_threshold",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.capacity": SensorEntityDescription(
        key="battery.capacity",
        REDACTED_VALUE"battery_capacity",
        native_unit_of_measurement="Ah",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.charge": SensorEntityDescription(
        key="battery.charge",
        REDACTED_VALUE"battery_charge",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "battery.charge.low": SensorEntityDescription(
        key="battery.charge.low",
        REDACTED_VALUE"battery_charge_low",
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.charge.restart": SensorEntityDescription(
        key="battery.charge.restart",
        REDACTED_VALUE"battery_charge_restart",
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.charge.warning": SensorEntityDescription(
        key="battery.charge.warning",
        REDACTED_VALUE"battery_charge_warning",
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.charger.status": SensorEntityDescription(
        key="battery.charger.status",
        REDACTED_VALUE"battery_charger_status",
        device_class=SensorDeviceClass.ENUM,
        options=BATTERY_CHARGER_STATUS_OPTIONS,
    ),
    "battery.current": SensorEntityDescription(
        key="battery.current",
        REDACTED_VALUE"battery_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.current.total": SensorEntityDescription(
        key="battery.current.total",
        REDACTED_VALUE"battery_current_total",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.date": SensorEntityDescription(
        key="battery.date",
        REDACTED_VALUE"battery_date",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.mfr.date": SensorEntityDescription(
        key="battery.mfr.date",
        REDACTED_VALUE"battery_mfr_date",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.packs": SensorEntityDescription(
        key="battery.packs",
        REDACTED_VALUE"battery_packs",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.packs.bad": SensorEntityDescription(
        key="battery.packs.bad",
        REDACTED_VALUE"battery_packs_bad",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.runtime": SensorEntityDescription(
        key="battery.runtime",
        REDACTED_VALUE"battery_runtime",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.runtime.low": SensorEntityDescription(
        key="battery.runtime.low",
        REDACTED_VALUE"battery_runtime_low",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.runtime.restart": SensorEntityDescription(
        key="battery.runtime.restart",
        REDACTED_VALUE"battery_runtime_restart",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.temperature": SensorEntityDescription(
        key="battery.temperature",
        REDACTED_VALUE"battery_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.type": SensorEntityDescription(
        key="battery.type",
        REDACTED_VALUE"battery_type",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.voltage": SensorEntityDescription(
        key="battery.voltage",
        REDACTED_VALUE"battery_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.voltage.high": SensorEntityDescription(
        key="battery.voltage.high",
        REDACTED_VALUE"battery_voltage_high",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.voltage.low": SensorEntityDescription(
        key="battery.voltage.low",
        REDACTED_VALUE"battery_voltage_low",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.voltage.nominal": SensorEntityDescription(
        key="battery.voltage.nominal",
        REDACTED_VALUE"battery_voltage_nominal",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.bypass.current": SensorEntityDescription(
        key="input.bypass.current",
        REDACTED_VALUE"input_bypass_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.bypass.frequency": SensorEntityDescription(
        key="input.bypass.frequency",
        REDACTED_VALUE"input_bypass_frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.bypass.L1.current": SensorEntityDescription(
        key="input.bypass.L1.current",
        REDACTED_VALUE"input_bypass_l1_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.bypass.L1-N.voltage": SensorEntityDescription(
        key="input.bypass.L1-N.voltage",
        REDACTED_VALUE"input_bypass_l1_n_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.bypass.L1.realpower": SensorEntityDescription(
        key="input.bypass.L1.realpower",
        REDACTED_VALUE"input_bypass_l1_realpower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.bypass.L2.current": SensorEntityDescription(
        key="input.bypass.L2.current",
        REDACTED_VALUE"input_bypass_l2_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.bypass.L2-N.voltage": SensorEntityDescription(
        key="input.bypass.L2-N.voltage",
        REDACTED_VALUE"input_bypass_l2_n_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.bypass.L2.realpower": SensorEntityDescription(
        key="input.bypass.L2.realpower",
        REDACTED_VALUE"input_bypass_l2_realpower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.bypass.L3.current": SensorEntityDescription(
        key="input.bypass.L3.current",
        REDACTED_VALUE"input_bypass_l3_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.bypass.L3-N.voltage": SensorEntityDescription(
        key="input.bypass.L3-N.voltage",
        REDACTED_VALUE"input_bypass_l3_n_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.bypass.L3.realpower": SensorEntityDescription(
        key="input.bypass.L3.realpower",
        REDACTED_VALUE"input_bypass_l3_realpower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.bypass.phases": SensorEntityDescription(
        key="input.bypass.phases",
        REDACTED_VALUE"input_bypass_phases",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.bypass.realpower": SensorEntityDescription(
        key="input.bypass.realpower",
        REDACTED_VALUE"input_bypass_realpower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.bypass.voltage": SensorEntityDescription(
        key="input.bypass.voltage",
        REDACTED_VALUE"input_bypass_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.current": SensorEntityDescription(
        key="input.current",
        REDACTED_VALUE"input_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    "input.current.status": SensorEntityDescription(
        key="input.current.status",
        REDACTED_VALUE"input_current_status",
        device_class=SensorDeviceClass.ENUM,
        options=THRESHOLD_STATUS_OPTIONS,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.frequency": SensorEntityDescription(
        key="input.frequency",
        REDACTED_VALUE"input_frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.frequency.nominal": SensorEntityDescription(
        key="input.frequency.nominal",
        REDACTED_VALUE"input_frequency_nominal",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.frequency.status": SensorEntityDescription(
        key="input.frequency.status",
        REDACTED_VALUE"input_frequency_status",
        device_class=SensorDeviceClass.ENUM,
        options=FREQUENCY_STATUS_OPTIONS,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.L1.current": SensorEntityDescription(
        key="input.L1.current",
        REDACTED_VALUE"input_l1_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.L1.frequency": SensorEntityDescription(
        key="input.L1.frequency",
        REDACTED_VALUE"input_l1_frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.L1-N.voltage": SensorEntityDescription(
        key="input.L1-N.voltage",
        REDACTED_VALUE"input_l1_n_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.L1.realpower": SensorEntityDescription(
        key="input.L1.realpower",
        REDACTED_VALUE"input_l1_realpower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.L2.current": SensorEntityDescription(
        key="input.L2.current",
        REDACTED_VALUE"input_l2_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.L2.frequency": SensorEntityDescription(
        key="input.L2.frequency",
        REDACTED_VALUE"input_l2_frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.L2-N.voltage": SensorEntityDescription(
        key="input.L2-N.voltage",
        REDACTED_VALUE"input_l2_n_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.L2.realpower": SensorEntityDescription(
        key="input.L2.realpower",
        REDACTED_VALUE"input_l2_realpower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.L3.current": SensorEntityDescription(
        key="input.L3.current",
        REDACTED_VALUE"input_l3_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.L3.frequency": SensorEntityDescription(
        key="input.L3.frequency",
        REDACTED_VALUE"input_l3_frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.L3-N.voltage": SensorEntityDescription(
        key="input.L3-N.voltage",
        REDACTED_VALUE"input_l3_n_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.L3.realpower": SensorEntityDescription(
        key="input.L3.realpower",
        REDACTED_VALUE"input_l3_realpower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.load": SensorEntityDescription(
        key="input.load",
        REDACTED_VALUE"input_load",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "input.phases": SensorEntityDescription(
        key="input.phases",
        REDACTED_VALUE"input_phases",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.power": SensorEntityDescription(
        key="input.power",
        REDACTED_VALUE"input_power",
        native_unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
        device_class=SensorDeviceClass.APPARENT_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.realpower": SensorEntityDescription(
        key="input.realpower",
        REDACTED_VALUE"input_realpower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.sensitivity": SensorEntityDescription(
        key="input.sensitivity",
        REDACTED_VALUE"input_sensitivity",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.transfer.high": SensorEntityDescription(
        key="input.transfer.high",
        REDACTED_VALUE"input_transfer_high",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.transfer.low": SensorEntityDescription(
        key="input.transfer.low",
        REDACTED_VALUE"input_transfer_low",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.transfer.reason": SensorEntityDescription(
        key="input.transfer.reason",
        REDACTED_VALUE"input_transfer_reason",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.voltage": SensorEntityDescription(
        key="input.voltage",
        REDACTED_VALUE"input_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "input.voltage.nominal": SensorEntityDescription(
        key="input.voltage.nominal",
        REDACTED_VALUE"input_voltage_nominal",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.voltage.status": SensorEntityDescription(
        key="input.voltage.status",
        REDACTED_VALUE"input_voltage_status",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "outlet.current": SensorEntityDescription(
        key="outlet.current",
        REDACTED_VALUE"outlet_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "outlet.power": SensorEntityDescription(
        key="outlet.power",
        REDACTED_VALUE"outlet_power",
        native_unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
        device_class=SensorDeviceClass.APPARENT_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "outlet.realpower": SensorEntityDescription(
        key="outlet.realpower",
        REDACTED_VALUE"outlet_realpower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "outlet.voltage": SensorEntityDescription(
        key="outlet.voltage",
        REDACTED_VALUE"outlet_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "output.current": SensorEntityDescription(
        key="output.current",
        REDACTED_VALUE"output_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.current.nominal": SensorEntityDescription(
        key="output.current.nominal",
        REDACTED_VALUE"output_current_nominal",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.frequency": SensorEntityDescription(
        key="output.frequency",
        REDACTED_VALUE"output_frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.frequency.nominal": SensorEntityDescription(
        key="output.frequency.nominal",
        REDACTED_VALUE"output_frequency_nominal",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.L1.current": SensorEntityDescription(
        key="output.L1.current",
        REDACTED_VALUE"output_l1_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.L1-N.voltage": SensorEntityDescription(
        key="output.L1-N.voltage",
        REDACTED_VALUE"output_l1_n_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.L1.power.percent": SensorEntityDescription(
        key="output.L1.power.percent",
        REDACTED_VALUE"output_l1_power_percent",
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.L1.realpower": SensorEntityDescription(
        key="output.L1.realpower",
        REDACTED_VALUE"output_l1_realpower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.L2.current": SensorEntityDescription(
        key="output.L2.current",
        REDACTED_VALUE"output_l2_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.L2-N.voltage": SensorEntityDescription(
        key="output.L2-N.voltage",
        REDACTED_VALUE"output_l2_n_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.L2.power.percent": SensorEntityDescription(
        key="output.L2.power.percent",
        REDACTED_VALUE"output_l2_power_percent",
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.L2.realpower": SensorEntityDescription(
        key="output.L2.realpower",
        REDACTED_VALUE"output_l2_realpower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.L3.current": SensorEntityDescription(
        key="output.L3.current",
        REDACTED_VALUE"output_l3_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.L3-N.voltage": SensorEntityDescription(
        key="output.L3-N.voltage",
        REDACTED_VALUE"output_l3_n_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.L3.power.percent": SensorEntityDescription(
        key="output.L3.power.percent",
        REDACTED_VALUE"output_l3_power_percent",
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.L3.realpower": SensorEntityDescription(
        key="output.L3.realpower",
        REDACTED_VALUE"output_l3_realpower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.phases": SensorEntityDescription(
        key="output.phases",
        REDACTED_VALUE"output_phases",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.power": SensorEntityDescription(
        key="output.power",
        REDACTED_VALUE"output_power",
        native_unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
        device_class=SensorDeviceClass.APPARENT_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.power.nominal": SensorEntityDescription(
        key="output.power.nominal",
        REDACTED_VALUE"output_power_nominal",
        native_unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
        device_class=SensorDeviceClass.APPARENT_POWER,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.realpower": SensorEntityDescription(
        key="output.realpower",
        REDACTED_VALUE"output_realpower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.realpower.nominal": SensorEntityDescription(
        key="output.realpower.nominal",
        REDACTED_VALUE"output_realpower_nominal",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "output.voltage": SensorEntityDescription(
        key="output.voltage",
        REDACTED_VALUE"output_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "output.voltage.nominal": SensorEntityDescription(
        key="output.voltage.nominal",
        REDACTED_VALUE"output_voltage_nominal",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.alarm": SensorEntityDescription(
        key="ups.alarm",
        REDACTED_VALUE"ups_alarm",
    ),
    "ups.beeper.status": SensorEntityDescription(
        key="ups.beeper.status",
        REDACTED_VALUE"ups_beeper_status",
        device_class=SensorDeviceClass.ENUM,
        options=UPS_BEEPER_STATUS_OPTIONS,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.contacts": SensorEntityDescription(
        key="ups.contacts",
        REDACTED_VALUE"ups_contacts",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.delay.reboot": SensorEntityDescription(
        key="ups.delay.reboot",
        REDACTED_VALUE"ups_delay_reboot",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.delay.shutdown": SensorEntityDescription(
        key="ups.delay.shutdown",
        REDACTED_VALUE"ups_delay_shutdown",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.delay.start": SensorEntityDescription(
        key="ups.delay.start",
        REDACTED_VALUE"ups_delay_start",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.display.language": SensorEntityDescription(
        key="ups.display.language",
        REDACTED_VALUE"ups_display_language",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.efficiency": SensorEntityDescription(
        key="ups.efficiency",
        REDACTED_VALUE"ups_efficiency",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.id": SensorEntityDescription(
        key="ups.id",
        REDACTED_VALUE"ups_id",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.load": SensorEntityDescription(
        key="ups.load",
        REDACTED_VALUE"ups_load",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "ups.load.high": SensorEntityDescription(
        key="ups.load.high",
        REDACTED_VALUE"ups_load_high",
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.power": SensorEntityDescription(
        key="ups.power",
        REDACTED_VALUE"ups_power",
        native_unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
        device_class=SensorDeviceClass.APPARENT_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.power.nominal": SensorEntityDescription(
        key="ups.power.nominal",
        REDACTED_VALUE"ups_power_nominal",
        native_unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
        device_class=SensorDeviceClass.APPARENT_POWER,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.realpower": SensorEntityDescription(
        key="ups.realpower",
        REDACTED_VALUE"ups_realpower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.realpower.nominal": SensorEntityDescription(
        key="ups.realpower.nominal",
        REDACTED_VALUE"ups_realpower_nominal",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.shutdown": SensorEntityDescription(
        key="ups.shutdown",
        REDACTED_VALUE"ups_shutdown",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.start.auto": SensorEntityDescription(
        key="ups.start.auto",
        REDACTED_VALUE"ups_start_auto",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.start.battery": SensorEntityDescription(
        key="ups.start.battery",
        REDACTED_VALUE"ups_start_battery",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.start.reboot": SensorEntityDescription(
        key="ups.start.reboot",
        REDACTED_VALUE"ups_start_reboot",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.status": SensorEntityDescription(
        key="ups.status",
        REDACTED_VALUE"ups_status",
    ),
    "ups.status.display": SensorEntityDescription(
        key="ups.status.display",
        REDACTED_VALUE"ups_status_display",
    ),
    "ups.temperature": SensorEntityDescription(
        key="ups.temperature",
        REDACTED_VALUE"ups_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.test.date": SensorEntityDescription(
        key="ups.test.date",
        REDACTED_VALUE"ups_test_date",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.test.interval": SensorEntityDescription(
        key="ups.test.interval",
        REDACTED_VALUE"ups_test_interval",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.test.result": SensorEntityDescription(
        key="ups.test.result",
        REDACTED_VALUE"ups_test_result",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.timer.reboot": SensorEntityDescription(
        key="ups.timer.reboot",
        REDACTED_VALUE"ups_timer_reboot",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.timer.shutdown": SensorEntityDescription(
        key="ups.timer.shutdown",
        REDACTED_VALUE"ups_timer_shutdown",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.timer.start": SensorEntityDescription(
        key="ups.timer.start",
        REDACTED_VALUE"ups_timer_start",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.type": SensorEntityDescription(
        key="ups.type",
        REDACTED_VALUE"ups_type",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.watchdog.status": SensorEntityDescription(
        key="ups.watchdog.status",
        REDACTED_VALUE"ups_watchdog_status",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: NutConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the NUT sensors."""
    valid_sensor_types: dict[str, SensorEntityDescription]

    pynut_data = config_entry.runtime_data
    coordinator = pynut_data.coordinator
    data = pynut_data.data
    unique_id = pynut_data.unique_id
    status = coordinator.data

    # Dynamically add outlet sensors to valid sensors dictionary
    if (num_outlets := status.get("outlet.count")) is not None:
        additional_sensor_types: dict[str, SensorEntityDescription] = {}
        for outlet_num in range(1, int(num_outlets) + 1):
            outlet_num_str: str = str(outlet_num)
            outlet_name: str = (
                status.get(f"outlet.{outlet_num_str}.name") or outlet_num_str
            )
            additional_sensor_types |= {
                f"outlet.{outlet_num_str}.current": SensorEntityDescription(
                    key=f"outlet.{outlet_num_str}.current",
                    REDACTED_VALUE"outlet_number_current",
                    translation_placeholders={"outlet_name": outlet_name},
                    native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
                    device_class=SensorDeviceClass.CURRENT,
                    state_class=SensorStateClass.MEASUREMENT,
                ),
                f"outlet.{outlet_num_str}.current_status": SensorEntityDescription(
                    key=f"outlet.{outlet_num_str}.current_status",
                    REDACTED_VALUE"outlet_number_current_status",
                    translation_placeholders={"outlet_name": outlet_name},
                    entity_category=EntityCategory.DIAGNOSTIC,
                    entity_registry_enabled_default=False,
                ),
                f"outlet.{outlet_num_str}.desc": SensorEntityDescription(
                    key=f"outlet.{outlet_num_str}.desc",
                    REDACTED_VALUE"outlet_number_desc",
                    translation_placeholders={"outlet_name": outlet_name},
                ),
                f"outlet.{outlet_num_str}.power": SensorEntityDescription(
                    key=f"outlet.{outlet_num_str}.power",
                    REDACTED_VALUE"outlet_number_power",
                    translation_placeholders={"outlet_name": outlet_name},
                    native_unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
                    device_class=SensorDeviceClass.APPARENT_POWER,
                    state_class=SensorStateClass.MEASUREMENT,
                ),
                f"outlet.{outlet_num_str}.realpower": SensorEntityDescription(
                    key=f"outlet.{outlet_num_str}.realpower",
                    REDACTED_VALUE"outlet_number_realpower",
                    translation_placeholders={"outlet_name": outlet_name},
                    native_unit_of_measurement=UnitOfPower.WATT,
                    device_class=SensorDeviceClass.POWER,
                    state_class=SensorStateClass.MEASUREMENT,
                ),
            }

        valid_sensor_types = {**SENSOR_TYPES, **additional_sensor_types}
    else:
        valid_sensor_types = SENSOR_TYPES

    # If device reports ambient sensors are not present, then remove
    has_ambient_sensors: bool = status.get(AMBIENT_PRESENT) != "no"
    resources = [
        sensor_id
        for sensor_id in valid_sensor_types
        if sensor_id in status
        and (has_ambient_sensors or sensor_id not in AMBIENT_SENSORS)
    ]

    # Display status is a special case that falls back to the status value
    # of the UPS instead.
    if KEY_STATUS in status:
        resources.append(KEY_STATUS_DISPLAY)

    async_add_entities(
        NUTSensor(
            coordinator,
            valid_sensor_types[sensor_type],
            data,
            unique_id,
        )
        for sensor_type in resources
    )


class NUTSensor(NUTBaseEntity, SensorEntity):
    """Representation of a sensor entity for NUT status values."""

    @property
    def native_value(self) -> str | None:
        """Return entity state from NUT device."""
        status = self.coordinator.data
        if self.entity_description.key == KEY_STATUS_DISPLAY:
            return _format_display_state(status)
        return status.get(self.entity_description.key)


def _format_display_state(status: dict[str, str]) -> str | None:
    """Return UPS display state."""
    try:
        return ", ".join(STATE_TYPES[state] for state in status[KEY_STATUS].split())
    except KeyError:
        return None
