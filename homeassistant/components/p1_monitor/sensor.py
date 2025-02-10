"""Support for P1 Monitor sensors."""

from __future__ import annotations

from typing import Literal

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    CONF_HOST,
    CURRENCY_EURO,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfVolume,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    SERVICE_PHASES,
    SERVICE_SETTINGS,
    SERVICE_SMARTMETER,
    SERVICE_WATERMETER,
)
from .coordinator import P1MonitorConfigEntry, P1MonitorDataUpdateCoordinator

SENSORS_SMARTMETER: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="gas_consumption",
        REDACTED_VALUE"gas_consumption",
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        device_class=SensorDeviceClass.GAS,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="power_consumption",
        REDACTED_VALUE"power_consumption",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="energy_consumption_high",
        REDACTED_VALUE"energy_consumption_high",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energy_consumption_low",
        REDACTED_VALUE"energy_consumption_low",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="power_production",
        REDACTED_VALUE"power_production",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="energy_production_high",
        REDACTED_VALUE"energy_production_high",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energy_production_low",
        REDACTED_VALUE"energy_production_low",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energy_tariff_period",
        REDACTED_VALUE"energy_tariff_period",
    ),
)

SENSORS_PHASES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="voltage_phase_l1",
        REDACTED_VALUE"voltage_phase_l1",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="voltage_phase_l2",
        REDACTED_VALUE"voltage_phase_l2",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="voltage_phase_l3",
        REDACTED_VALUE"voltage_phase_l3",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="current_phase_l1",
        REDACTED_VALUE"current_phase_l1",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="current_phase_l2",
        REDACTED_VALUE"current_phase_l2",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="current_phase_l3",
        REDACTED_VALUE"current_phase_l3",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="power_consumed_phase_l1",
        REDACTED_VALUE"power_consumed_phase_l1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="power_consumed_phase_l2",
        REDACTED_VALUE"power_consumed_phase_l2",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="power_consumed_phase_l3",
        REDACTED_VALUE"power_consumed_phase_l3",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="power_produced_phase_l1",
        REDACTED_VALUE"power_produced_phase_l1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="power_produced_phase_l2",
        REDACTED_VALUE"power_produced_phase_l2",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="power_produced_phase_l3",
        REDACTED_VALUE"power_produced_phase_l3",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)

SENSORS_SETTINGS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="gas_consumption_price",
        REDACTED_VALUE"gas_consumption_price",
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=f"{CURRENCY_EURO}/{UnitOfVolume.CUBIC_METERS}",
    ),
    SensorEntityDescription(
        key="energy_consumption_price_low",
        REDACTED_VALUE"energy_consumption_price_low",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=f"{CURRENCY_EURO}/{UnitOfEnergy.KILO_WATT_HOUR}",
    ),
    SensorEntityDescription(
        key="energy_consumption_price_high",
        REDACTED_VALUE"energy_consumption_price_high",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=f"{CURRENCY_EURO}/{UnitOfEnergy.KILO_WATT_HOUR}",
    ),
    SensorEntityDescription(
        key="energy_production_price_low",
        REDACTED_VALUE"energy_production_price_low",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=f"{CURRENCY_EURO}/{UnitOfEnergy.KILO_WATT_HOUR}",
    ),
    SensorEntityDescription(
        key="energy_production_price_high",
        REDACTED_VALUE"energy_production_price_high",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=f"{CURRENCY_EURO}/{UnitOfEnergy.KILO_WATT_HOUR}",
    ),
)

SENSORS_WATERMETER: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="consumption_day",
        REDACTED_VALUE"consumption_day",
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfVolume.LITERS,
        device_class=SensorDeviceClass.WATER,
    ),
    SensorEntityDescription(
        key="consumption_total",
        REDACTED_VALUE"consumption_total",
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        device_class=SensorDeviceClass.WATER,
    ),
    SensorEntityDescription(
        key="pulse_count",
        REDACTED_VALUE"pulse_count",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: P1MonitorConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up P1 Monitor Sensors based on a config entry."""
    entities: list[P1MonitorSensorEntity] = []
    entities.extend(
        P1MonitorSensorEntity(
            entry=entry,
            description=description,
            name="SmartMeter",
            service=SERVICE_SMARTMETER,
        )
        for description in SENSORS_SMARTMETER
    )
    entities.extend(
        P1MonitorSensorEntity(
            entry=entry,
            description=description,
            name="Phases",
            service=SERVICE_PHASES,
        )
        for description in SENSORS_PHASES
    )
    entities.extend(
        P1MonitorSensorEntity(
            entry=entry,
            description=description,
            name="Settings",
            service=SERVICE_SETTINGS,
        )
        for description in SENSORS_SETTINGS
    )
    if entry.runtime_data.has_water_meter:
        entities.extend(
            P1MonitorSensorEntity(
                entry=entry,
                description=description,
                name="WaterMeter",
                service=SERVICE_WATERMETER,
            )
            for description in SENSORS_WATERMETER
        )
    async_add_entities(entities)


class P1MonitorSensorEntity(
    CoordinatorEntity[P1MonitorDataUpdateCoordinator], SensorEntity
):
    """Defines an P1 Monitor sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        *,
        entry: P1MonitorConfigEntry,
        description: SensorEntityDescription,
        name: str,
        service: Literal["smartmeter", "watermeter", "phases", "settings"],
    ) -> None:
        """Initialize P1 Monitor sensor."""
        super().__init__(coordinator=entry.runtime_data)
        self._service_key = service

        self.entity_description = description
        self._attr_unique_id = (
            f"{entry.runtime_data.config_entry.entry_id}_{service}_{description.key}"
        )

        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={
                (DOMAIN, f"{entry.runtime_data.config_entry.entry_id}_{service}")
            },
            configuration_url=f"http://{entry.runtime_data.config_entry.data[CONF_HOST]}",
            manufacturer="P1 Monitor",
            name=name,
        )

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        value = getattr(
            self.coordinator.data[self._service_key], self.entity_description.key
        )
        if isinstance(value, str):
            return value.lower()
        return value  # type: ignore[no-any-return]
