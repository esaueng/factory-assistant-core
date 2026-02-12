"""Support for Homevolt sensors."""

from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS,
    EntityCategory,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import HomevoltConfigEntry, HomevoltDataUpdateCoordinator

PARALLEL_UPDATES = 0  # Coordinator-based updates

_LOGGER = logging.getLogger(__name__)


SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="available_charging_energy",
        REDACTED_VALUE"available_charging_energy",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
    ),
    SensorEntityDescription(
        key="available_charging_power",
        REDACTED_VALUE"available_charging_power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="available_discharge_energy",
        REDACTED_VALUE"available_discharge_energy",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
    ),
    SensorEntityDescription(
        key="available_discharge_power",
        REDACTED_VALUE"available_discharge_power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="rssi",
        REDACTED_VALUE"rssi",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="average_rssi",
        REDACTED_VALUE"average_rssi",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="charge_cycles",
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement="cycles",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="energy_exported",
        REDACTED_VALUE"energy_exported",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
    ),
    SensorEntityDescription(
        key="energy_imported",
        REDACTED_VALUE"energy_imported",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
    ),
    SensorEntityDescription(
        key="frequency",
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="l1_current",
        REDACTED_VALUE"l1_current",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
    ),
    SensorEntityDescription(
        key="l1_l2_voltage",
        REDACTED_VALUE"l1_l2_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    ),
    SensorEntityDescription(
        key="l1_power",
        REDACTED_VALUE"l1_power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="l1_voltage",
        REDACTED_VALUE"l1_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="l2_current",
        REDACTED_VALUE"l2_current",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
    ),
    SensorEntityDescription(
        key="l2_l3_voltage",
        REDACTED_VALUE"l2_l3_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    ),
    SensorEntityDescription(
        key="l2_power",
        REDACTED_VALUE"l2_power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="l2_voltage",
        REDACTED_VALUE"l2_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="l3_current",
        REDACTED_VALUE"l3_current",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
    ),
    SensorEntityDescription(
        key="l3_l1_voltage",
        REDACTED_VALUE"l3_l1_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    ),
    SensorEntityDescription(
        key="l3_power",
        REDACTED_VALUE"l3_power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="l3_voltage",
        REDACTED_VALUE"l3_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="schedule_id",
        REDACTED_VALUE"schedule_id",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="schedule_max_discharge",
        REDACTED_VALUE"schedule_max_discharge",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="schedule_max_power",
        REDACTED_VALUE"schedule_max_power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="schedule_power_setpoint",
        REDACTED_VALUE"schedule_power_setpoint",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="schedule_type",
        REDACTED_VALUE"schedule_type",
        device_class=SensorDeviceClass.ENUM,
        options=[
            "idle",
            "inverter_charge",
            "inverter_discharge",
            "grid_charge",
            "grid_discharge",
            "grid_charge_discharge",
            "frequency_reserve",
            "solar_charge",
            "solar_charge_discharge",
            "full_solar_export",
        ],
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="state_of_charge",
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        key="system_temperature",
        REDACTED_VALUE"system_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="tmax",
        REDACTED_VALUE"tmax",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="tmin",
        REDACTED_VALUE"tmin",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HomevoltConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Homevolt sensor."""
    coordinator = entry.runtime_data
    entities: list[HomevoltSensor] = []
    sensors_by_key = {sensor.key: sensor for sensor in SENSORS}
    for sensor_key, sensor in coordinator.data.sensors.items():
        if (description := sensors_by_key.get(sensor.type)) is None:
            _LOGGER.warning("Unsupported sensor '%s' found during setup", sensor)
            continue
        entities.append(
            HomevoltSensor(
                description,
                coordinator,
                sensor_key,
            )
        )
    async_add_entities(entities)


class HomevoltSensor(CoordinatorEntity[HomevoltDataUpdateCoordinator], SensorEntity):
    """Representation of a Homevolt sensor."""

    entity_description: SensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        description: SensorEntityDescription,
        coordinator: HomevoltDataUpdateCoordinator,
        sensor_key: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        unique_id = coordinator.data.unique_id
        self._attr_unique_id = f"{unique_id}_{sensor_key}"
        sensor_data = coordinator.data.sensors[sensor_key]
        self._sensor_key = sensor_key

        device_metadata = coordinator.data.device_metadata.get(
            sensor_data.device_identifier
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{unique_id}_{sensor_data.device_identifier}")},
            configuration_url=coordinator.client.base_url,
            manufacturer=MANUFACTURER,
            model=device_metadata.model if device_metadata else None,
            name=device_metadata.name if device_metadata else None,
        )

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self._sensor_key in self.coordinator.data.sensors

    @property
    def native_value(self) -> StateType:
        """Return the native value of the sensor."""
        return self.coordinator.data.sensors[self._sensor_key].value
