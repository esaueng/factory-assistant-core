"""Provides a sensor to track various status aspects of a UPS."""
from __future__ import annotations

from dataclasses import asdict
import logging
from typing import Final, cast

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_MANUFACTURER,
    ATTR_MODEL,
    ATTR_SW_VERSION,
    PERCENTAGE,
    STATE_UNKNOWN,
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
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from . import PyNUTData
from .const import (
    COORDINATOR,
    DOMAIN,
    KEY_STATUS,
    KEY_STATUS_DISPLAY,
    PYNUT_DATA,
    PYNUT_UNIQUE_ID,
    STATE_TYPES,
)

NUT_DEV_INFO_TO_DEV_INFO: dict[str, str] = {
    "manufacturer": ATTR_MANUFACTURER,
    "model": ATTR_MODEL,
    "firmware": ATTR_SW_VERSION,
}

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES: Final[dict[str, SensorEntityDescription]] = {
    "ups.status.display": SensorEntityDescription(
        key="ups.status.display",
        REDACTED_VALUE"ups_status_display",
        icon="mdi:information-outline",
    ),
    "ups.status": SensorEntityDescription(
        key="ups.status",
        REDACTED_VALUE"ups_status",
        icon="mdi:information-outline",
    ),
    "ups.alarm": SensorEntityDescription(
        key="ups.alarm",
        REDACTED_VALUE"ups_alarm",
        icon="mdi:alarm",
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
    "ups.load": SensorEntityDescription(
        key="ups.load",
        REDACTED_VALUE"ups_load",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:gauge",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "ups.load.high": SensorEntityDescription(
        key="ups.load.high",
        REDACTED_VALUE"ups_load_high",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:gauge",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.id": SensorEntityDescription(
        key="ups.id",
        REDACTED_VALUE"ups_id",
        icon="mdi:information-outline",
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
    "ups.timer.start": SensorEntityDescription(
        key="ups.timer.start",
        REDACTED_VALUE"ups_timer_start",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
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
        icon="mdi:information-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.test.date": SensorEntityDescription(
        key="ups.test.date",
        REDACTED_VALUE"ups_test_date",
        icon="mdi:calendar",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.display.language": SensorEntityDescription(
        key="ups.display.language",
        REDACTED_VALUE"ups_display_language",
        icon="mdi:information-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.contacts": SensorEntityDescription(
        key="ups.contacts",
        REDACTED_VALUE"ups_contacts",
        icon="mdi:information-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.efficiency": SensorEntityDescription(
        key="ups.efficiency",
        REDACTED_VALUE"ups_efficiency",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:gauge",
        state_class=SensorStateClass.MEASUREMENT,
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
    "ups.beeper.status": SensorEntityDescription(
        key="ups.beeper.status",
        REDACTED_VALUE"ups_beeper_status",
        icon="mdi:information-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.type": SensorEntityDescription(
        key="ups.type",
        REDACTED_VALUE"ups_type",
        icon="mdi:information-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.watchdog.status": SensorEntityDescription(
        key="ups.watchdog.status",
        REDACTED_VALUE"ups_watchdog_status",
        icon="mdi:information-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.start.auto": SensorEntityDescription(
        key="ups.start.auto",
        REDACTED_VALUE"ups_start_auto",
        icon="mdi:information-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.start.battery": SensorEntityDescription(
        key="ups.start.battery",
        REDACTED_VALUE"ups_start_battery",
        icon="mdi:information-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.start.reboot": SensorEntityDescription(
        key="ups.start.reboot",
        REDACTED_VALUE"ups_start_reboot",
        icon="mdi:information-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "ups.shutdown": SensorEntityDescription(
        key="ups.shutdown",
        REDACTED_VALUE"ups_shutdown",
        icon="mdi:information-outline",
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
        icon="mdi:gauge",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.charge.restart": SensorEntityDescription(
        key="battery.charge.restart",
        REDACTED_VALUE"battery_charge_restart",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:gauge",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.charge.warning": SensorEntityDescription(
        key="battery.charge.warning",
        REDACTED_VALUE"battery_charge_warning",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:gauge",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.charger.status": SensorEntityDescription(
        key="battery.charger.status",
        REDACTED_VALUE"battery_charger_status",
        icon="mdi:information-outline",
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
    "battery.voltage.nominal": SensorEntityDescription(
        key="battery.voltage.nominal",
        REDACTED_VALUE"battery_voltage_nominal",
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
    "battery.voltage.high": SensorEntityDescription(
        key="battery.voltage.high",
        REDACTED_VALUE"battery_voltage_high",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.capacity": SensorEntityDescription(
        key="battery.capacity",
        REDACTED_VALUE"battery_capacity",
        native_unit_of_measurement="Ah",
        icon="mdi:flash",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
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
    "battery.temperature": SensorEntityDescription(
        key="battery.temperature",
        REDACTED_VALUE"battery_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
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
    "battery.alarm.threshold": SensorEntityDescription(
        key="battery.alarm.threshold",
        REDACTED_VALUE"battery_alarm_threshold",
        icon="mdi:information-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.date": SensorEntityDescription(
        key="battery.date",
        REDACTED_VALUE"battery_date",
        icon="mdi:calendar",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.mfr.date": SensorEntityDescription(
        key="battery.mfr.date",
        REDACTED_VALUE"battery_mfr_date",
        icon="mdi:calendar",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.packs": SensorEntityDescription(
        key="battery.packs",
        REDACTED_VALUE"battery_packs",
        icon="mdi:information-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.packs.bad": SensorEntityDescription(
        key="battery.packs.bad",
        REDACTED_VALUE"battery_packs_bad",
        icon="mdi:information-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "battery.type": SensorEntityDescription(
        key="battery.type",
        REDACTED_VALUE"battery_type",
        icon="mdi:information-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.sensitivity": SensorEntityDescription(
        key="input.sensitivity",
        REDACTED_VALUE"input_sensitivity",
        icon="mdi:information-outline",
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
    "input.transfer.high": SensorEntityDescription(
        key="input.transfer.high",
        REDACTED_VALUE"input_transfer_high",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.transfer.reason": SensorEntityDescription(
        key="input.transfer.reason",
        REDACTED_VALUE"input_transfer_reason",
        icon="mdi:information-outline",
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
        icon="mdi:information-outline",
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
    "input.bypass.phases": SensorEntityDescription(
        key="input.bypass.phases",
        REDACTED_VALUE"input_bypass_phases",
        icon="mdi:information-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.current": SensorEntityDescription(
        key="input.current",
        REDACTED_VALUE"input_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "input.phases": SensorEntityDescription(
        key="input.phases",
        REDACTED_VALUE"input_phases",
        icon="mdi:information-outline",
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
    "output.power.nominal": SensorEntityDescription(
        key="output.power.nominal",
        REDACTED_VALUE"output_power_nominal",
        native_unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
        device_class=SensorDeviceClass.APPARENT_POWER,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
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
    "output.phases": SensorEntityDescription(
        key="output.phases",
        REDACTED_VALUE"output_phases",
        icon="mdi:information-outline",
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
    "ambient.humidity": SensorEntityDescription(
        key="ambient.humidity",
        REDACTED_VALUE"ambient_humidity",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "ambient.temperature": SensorEntityDescription(
        key="ambient.temperature",
        REDACTED_VALUE"ambient_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "watts": SensorEntityDescription(
        key="watts",
        REDACTED_VALUE"watts",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
}


def _get_nut_device_info(data: PyNUTData) -> DeviceInfo:
    """Return a DeviceInfo object filled with NUT device info."""
    nut_dev_infos = asdict(data.device_info)
    nut_infos = {
        info_key: nut_dev_infos[nut_key]
        for nut_key, info_key in NUT_DEV_INFO_TO_DEV_INFO.items()
        if nut_dev_infos[nut_key] is not None
    }

    return cast(DeviceInfo, nut_infos)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the NUT sensors."""

    pynut_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = pynut_data[COORDINATOR]
    data = pynut_data[PYNUT_DATA]
    unique_id = pynut_data[PYNUT_UNIQUE_ID]
    status = coordinator.data

    resources = [sensor_id for sensor_id in SENSOR_TYPES if sensor_id in status]
    # Display status is a special case that falls back to the status value
    # of the UPS instead.
    if KEY_STATUS in resources:
        resources.append(KEY_STATUS_DISPLAY)

    entities = [
        NUTSensor(
            coordinator,
            SENSOR_TYPES[sensor_type],
            data,
            unique_id,
        )
        for sensor_type in resources
    ]

    async_add_entities(entities, True)


class NUTSensor(CoordinatorEntity[DataUpdateCoordinator[dict[str, str]]], SensorEntity):
    """Representation of a sensor entity for NUT status values."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DataUpdateCoordinator[dict[str, str]],
        sensor_description: SensorEntityDescription,
        data: PyNUTData,
        unique_id: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = sensor_description

        device_name = data.name.title()
        self._attr_unique_id = f"{unique_id}_{sensor_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, unique_id)},
            name=device_name,
        )
        self._attr_device_info.update(_get_nut_device_info(data))

    @property
    def native_value(self) -> str | None:
        """Return entity state from ups."""
        status = self.coordinator.data
        if self.entity_description.key == KEY_STATUS_DISPLAY:
            return _format_display_state(status)
        return status.get(self.entity_description.key)


def _format_display_state(status: dict[str, str]) -> str:
    """Return UPS display state."""
    try:
        return " ".join(STATE_TYPES[state] for state in status[KEY_STATUS].split())
    except KeyError:
        return STATE_UNKNOWN
