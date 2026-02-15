"""Support for Tibber sensors."""

from __future__ import annotations

import logging
from typing import Any, cast

import aiohttp
from tibber import FatalHttpExceptionError, RetryableHttpExceptionError, TibberHome
from tibber.data_api import TibberDevice

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
    UnitOfLength,
    UnitOfPower,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, TibberConfigEntry
from .coordinator import (
    TibberDataAPICoordinator,
    TibberDataCoordinator,
    TibberRtDataCoordinator,
)
from .entity import TibberCoordinatorEntity, TibberRTCoordinatorEntity

_LOGGER = logging.getLogger(__name__)

PARALLEL_UPDATES = 0

RT_SENSORS_UNIQUE_ID_MIGRATION = {
    "accumulated_consumption_last_hour": "accumulated consumption current hour",
    "accumulated_production_last_hour": "accumulated production current hour",
    "current_l1": "current L1",
    "current_l2": "current L2",
    "current_l3": "current L3",
    "estimated_hour_consumption": "Estimated consumption current hour",
}

RT_SENSORS_UNIQUE_ID_MIGRATION_SIMPLE = {
    # simple migration can be done by replacing " " with "_"
    "accumulated_consumption",
    "accumulated_cost",
    "accumulated_production",
    "accumulated_reward",
    "average_power",
    "last_meter_consumption",
    "last_meter_production",
    "max_power",
    "min_power",
    "power_factor",
    "power_production",
    "signal_strength",
    "REDACTED_VALUE",
    "REDACTED_VALUE",
    "REDACTED_VALUE",
}


RT_SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="averagePower",
        REDACTED_VALUE"average_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="power",
        REDACTED_VALUE"power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="powerProduction",
        REDACTED_VALUE"power_production",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="minPower",
        REDACTED_VALUE"min_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="maxPower",
        REDACTED_VALUE"max_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="accumulatedConsumption",
        REDACTED_VALUE"accumulated_consumption",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL,
    ),
    SensorEntityDescription(
        key="accumulatedConsumptionLastHour",
        REDACTED_VALUE"accumulated_consumption_last_hour",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="estimatedHourConsumption",
        REDACTED_VALUE"estimated_hour_consumption",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    ),
    SensorEntityDescription(
        key="accumulatedProduction",
        REDACTED_VALUE"accumulated_production",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL,
    ),
    SensorEntityDescription(
        key="accumulatedProductionLastHour",
        REDACTED_VALUE"accumulated_production_last_hour",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="lastMeterConsumption",
        REDACTED_VALUE"last_meter_consumption",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="lastMeterProduction",
        REDACTED_VALUE"last_meter_production",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="voltagePhase1",
        REDACTED_VALUE"REDACTED_VALUE",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="voltagePhase2",
        REDACTED_VALUE"REDACTED_VALUE",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="voltagePhase3",
        REDACTED_VALUE"REDACTED_VALUE",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="currentL1",
        REDACTED_VALUE"current_l1",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="currentL2",
        REDACTED_VALUE"current_l2",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="currentL3",
        REDACTED_VALUE"current_l3",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="signalStrength",
        REDACTED_VALUE"signal_strength",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="accumulatedReward",
        REDACTED_VALUE"accumulated_reward",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.TOTAL,
    ),
    SensorEntityDescription(
        key="accumulatedCost",
        REDACTED_VALUE"accumulated_cost",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.TOTAL,
    ),
    SensorEntityDescription(
        key="powerFactor",
        REDACTED_VALUE"power_factor",
        device_class=SensorDeviceClass.POWER_FACTOR,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)

SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="month_cost",
        REDACTED_VALUE"month_cost",
        device_class=SensorDeviceClass.MONETARY,
    ),
    SensorEntityDescription(
        key="peak_hour",
        REDACTED_VALUE"peak_hour",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    ),
    SensorEntityDescription(
        key="peak_hour_time",
        REDACTED_VALUE"peak_hour_time",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
    SensorEntityDescription(
        key="month_cons",
        REDACTED_VALUE"month_cons",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="current_price",
        REDACTED_VALUE"electricity_price",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=3,
    ),
    SensorEntityDescription(
        key="max_price",
        REDACTED_VALUE"max_price",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=3,
    ),
    SensorEntityDescription(
        key="avg_price",
        REDACTED_VALUE"avg_price",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=3,
    ),
    SensorEntityDescription(
        key="min_price",
        REDACTED_VALUE"min_price",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=3,
    ),
    SensorEntityDescription(
        key="off_peak_1",
        REDACTED_VALUE"off_peak_1",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=3,
    ),
    SensorEntityDescription(
        key="peak",
        REDACTED_VALUE"peak",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=3,
    ),
    SensorEntityDescription(
        key="off_peak_2",
        REDACTED_VALUE"off_peak_2",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=3,
    ),
    SensorEntityDescription(
        key="intraday_price_ranking",
        REDACTED_VALUE"intraday_price_ranking",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
)

DATA_API_SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="cellular.rssi",
        REDACTED_VALUE"cellular_rssi",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="storage.stateOfCharge",
        REDACTED_VALUE"storage_state_of_charge",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="storage.targetStateOfCharge",
        REDACTED_VALUE"storage_target_state_of_charge",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="storage.ratedCapacity",
        REDACTED_VALUE"storage_rated_capacity",
        device_class=SensorDeviceClass.ENERGY_STORAGE,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="storage.ratedPower",
        REDACTED_VALUE"storage_rated_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="storage.availableEnergy",
        REDACTED_VALUE"storage_available_energy",
        device_class=SensorDeviceClass.ENERGY_STORAGE,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="powerFlow.battery.power",
        REDACTED_VALUE"power_flow_battery",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="powerFlow.grid.power",
        REDACTED_VALUE"power_flow_grid",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="powerFlow.load.power",
        REDACTED_VALUE"power_flow_load",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="powerFlow.toGrid",
        REDACTED_VALUE"power_flow_to_grid",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="powerFlow.toLoad",
        REDACTED_VALUE"power_flow_to_load",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="powerFlow.fromGrid",
        REDACTED_VALUE"power_flow_from_grid",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="powerFlow.fromLoad",
        REDACTED_VALUE"power_flow_from_load",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="energyFlow.hour.battery.charged",
        REDACTED_VALUE"energy_flow_hour_battery_charged",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energyFlow.hour.battery.discharged",
        REDACTED_VALUE"energy_flow_hour_battery_discharged",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energyFlow.hour.battery.source.grid",
        REDACTED_VALUE"energy_flow_hour_battery_source_grid",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="energyFlow.hour.battery.source.load",
        REDACTED_VALUE"energy_flow_hour_battery_source_load",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="energyFlow.hour.grid.imported",
        REDACTED_VALUE"energy_flow_hour_grid_imported",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energyFlow.hour.grid.exported",
        REDACTED_VALUE"energy_flow_hour_grid_exported",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energyFlow.hour.load.consumed",
        REDACTED_VALUE"energy_flow_hour_load_consumed",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energyFlow.hour.load.generated",
        REDACTED_VALUE"energy_flow_hour_load_generated",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energyFlow.hour.load.source.battery",
        REDACTED_VALUE"energy_flow_hour_load_source_battery",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="energyFlow.hour.load.source.grid",
        REDACTED_VALUE"energy_flow_hour_load_source_grid",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="energyFlow.month.battery.charged",
        REDACTED_VALUE"energy_flow_month_battery_charged",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energyFlow.month.battery.discharged",
        REDACTED_VALUE"energy_flow_month_battery_discharged",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energyFlow.month.battery.source.grid",
        REDACTED_VALUE"energy_flow_month_battery_source_grid",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="energyFlow.month.battery.source.battery",
        REDACTED_VALUE"energy_flow_month_battery_source_battery",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="energyFlow.month.battery.source.load",
        REDACTED_VALUE"energy_flow_month_battery_source_load",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="energyFlow.month.grid.imported",
        REDACTED_VALUE"energy_flow_month_grid_imported",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energyFlow.month.grid.exported",
        REDACTED_VALUE"energy_flow_month_grid_exported",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energyFlow.month.grid.source.battery",
        REDACTED_VALUE"energy_flow_month_grid_source_battery",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="energyFlow.month.grid.source.grid",
        REDACTED_VALUE"energy_flow_month_grid_source_grid",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="energyFlow.month.grid.source.load",
        REDACTED_VALUE"energy_flow_month_grid_source_load",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="energyFlow.month.load.consumed",
        REDACTED_VALUE"energy_flow_month_load_consumed",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energyFlow.month.load.generated",
        REDACTED_VALUE"energy_flow_month_load_generated",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energyFlow.month.load.source.battery",
        REDACTED_VALUE"energy_flow_month_load_source_battery",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="energyFlow.month.load.source.grid",
        REDACTED_VALUE"energy_flow_month_load_source_grid",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="range.remaining",
        REDACTED_VALUE"range_remaining",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=UnitOfLength.METERS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="charging.current.max",
        REDACTED_VALUE"charging_current_max",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="charging.current.offlineFallback",
        REDACTED_VALUE"charging_current_offline_fallback",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="temp.setpoint",
        REDACTED_VALUE"temp_setpoint",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="temp.current",
        REDACTED_VALUE"temp_current",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="temp.comfort",
        REDACTED_VALUE"temp_comfort",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="grid.phaseCount",
        REDACTED_VALUE"grid_phase_count",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TibberConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Tibber sensor."""

    _setup_data_api_sensors(entry, async_add_entities)
    await _async_setup_graphql_sensors(hass, entry, async_add_entities)


async def _async_setup_graphql_sensors(
    hass: HomeAssistant,
    entry: TibberConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Tibber sensor."""

    tibber_connection = await entry.runtime_data.async_get_client(hass)

    entity_registry = er.async_get(hass)

    coordinator: TibberDataCoordinator = entry.runtime_data.data_coordinator
    entities: list[TibberSensor] = []
    for home in tibber_connection.get_homes(only_active=False):
        try:
            await home.update_info()
        except TimeoutError as err:
            _LOGGER.error("Timeout connecting to Tibber home: %s ", err)
            raise PlatformNotReady from err
        except (
            RetryableHttpExceptionError,
            FatalHttpExceptionError,
            aiohttp.ClientError,
        ) as err:
            _LOGGER.error("Error connecting to Tibber home: %s ", err)
            raise PlatformNotReady from err

        if home.has_active_subscription:
            entities.extend(TibberSensor(home, coordinator, desc) for desc in SENSORS)

        if home.has_real_time_consumption:
            entity_creator = TibberRtEntityCreator(
                async_add_entities, home, entity_registry
            )
            await home.rt_subscribe(
                TibberRtDataCoordinator(
                    hass,
                    entry,
                    entity_creator.add_sensors,
                    home,
                ).async_set_updated_data
            )

    async_add_entities(entities)


def _setup_data_api_sensors(
    entry: TibberConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up sensors backed by the Tibber Data API."""

    coordinator = entry.runtime_data.data_api_coordinator

    entities: list[TibberDataAPISensor] = []
    api_sensors = {sensor.key: sensor for sensor in DATA_API_SENSORS}

    for device in coordinator.data.values():
        for sensor in device.sensors:
            description: SensorEntityDescription | None = api_sensors.get(sensor.id)
            if description is None:
                continue
            entities.append(TibberDataAPISensor(coordinator, device, description))
    async_add_entities(entities)


class TibberDataAPISensor(CoordinatorEntity[TibberDataAPICoordinator], SensorEntity):
    """Representation of a Tibber Data API capability sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: TibberDataAPICoordinator,
        device: TibberDevice,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)

        self._device_id: str = device.id
        self.entity_description = entity_description
        self._attr_translation_key = entity_description.translation_key

        self._attr_unique_id = f"{device.external_id}_{self.entity_description.key}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device.external_id)},
            name=device.name,
            manufacturer=device.brand,
            model=device.model,
        )

    @property
    def native_value(self) -> StateType:
        """Return the value reported by the device."""
        sensors = self.coordinator.sensors_by_device.get(self._device_id, {})
        sensor = sensors.get(self.entity_description.key)
        return sensor.value if sensor else None


class TibberSensor(TibberCoordinatorEntity, SensorEntity):
    """Representation of a Tibber sensor reading from coordinator data."""

    def __init__(
        self,
        tibber_home: TibberHome,
        coordinator: TibberDataCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator=coordinator, tibber_home=tibber_home)
        self.entity_description = entity_description
        if self.entity_description.key == "current_price":
            # Preserve the existing unique ID for the electricity price
            # entity to avoid breaking user setups.
            self._attr_unique_id = self._tibber_home.home_id
        else:
            self._attr_unique_id = (
                f"{self._tibber_home.home_id}_{self.entity_description.key}"
            )
        self._device_name = self._home_name

    @property
    def available(self) -> bool:
        """Return whether the sensor is available."""
        return super().available and self._get_home_data() is not None

    @property
    def native_value(self) -> StateType:
        """Return the value of the sensor from coordinator data."""
        home_data = self._get_home_data()
        if home_data is None:
            return None
        return cast(StateType, home_data[self.entity_description.key])

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit from coordinator data for monetary sensors."""
        if (
            self.entity_description.device_class == SensorDeviceClass.MONETARY
            or self.entity_description.key
            in (
                "current_price",
                "max_price",
                "avg_price",
                "min_price",
                "off_peak_1",
                "peak",
                "off_peak_2",
            )
        ):
            home_data = self._get_home_data()
            if home_data is None:
                return None
            return (
                home_data.currency
                if self.entity_description.device_class == SensorDeviceClass.MONETARY
                else home_data.price_unit
            )
        return self.entity_description.native_unit_of_measurement


class TibberRtEntityCreator:
    """Create realtime Tibber entities."""

    def __init__(
        self,
        async_add_entities: AddConfigEntryEntitiesCallback,
        tibber_home: TibberHome,
        entity_registry: er.EntityRegistry,
    ) -> None:
        """Initialize the data handler."""
        self._async_add_entities = async_add_entities
        self._tibber_home = tibber_home
        self._added_sensors: set[str] = set()
        self._entity_registry = entity_registry

    @callback
    def _migrate_unique_id(self, sensor_description: SensorEntityDescription) -> None:
        """Migrate unique id if needed."""
        home_id = self._tibber_home.home_id
        translation_key = sensor_description.translation_key
        description_key = sensor_description.key
        entity_id: str | None = None
        if translation_key in RT_SENSORS_UNIQUE_ID_MIGRATION_SIMPLE:
            entity_id = self._entity_registry.async_get_entity_id(
                "sensor",
                DOMAIN,
                f"{home_id}_rt_{translation_key.replace('_', ' ')}",
            )
        elif translation_key in RT_SENSORS_UNIQUE_ID_MIGRATION:
            entity_id = self._entity_registry.async_get_entity_id(
                "sensor",
                DOMAIN,
                f"{home_id}_rt_{RT_SENSORS_UNIQUE_ID_MIGRATION[translation_key]}",
            )
        elif translation_key != description_key:
            entity_id = self._entity_registry.async_get_entity_id(
                "sensor",
                DOMAIN,
                f"{home_id}_rt_{translation_key}",
            )

        if entity_id is None:
            return

        new_unique_id = f"{home_id}_rt_{description_key}"

        _LOGGER.debug(
            "Migrating unique id for %s to %s",
            entity_id,
            new_unique_id,
        )
        try:
            self._entity_registry.async_update_entity(
                entity_id, new_unique_id=new_unique_id
            )
        except ValueError as err:
            _LOGGER.error(err)

    @callback
    def add_sensors(
        self, coordinator: TibberRtDataCoordinator, live_measurement: Any
    ) -> None:
        """Add sensor."""
        new_entities = []
        for sensor_description in RT_SENSORS:
            if sensor_description.key in self._added_sensors:
                continue
            state = live_measurement.get(sensor_description.key)
            if state is None:
                continue

            self._migrate_unique_id(sensor_description)
            entity = TibberRTCoordinatorEntity(
                self._tibber_home,
                sensor_description,
                state,
                coordinator,
            )
            new_entities.append(entity)
            self._added_sensors.add(sensor_description.key)
        if new_entities:
            self._async_add_entities(new_entities)
