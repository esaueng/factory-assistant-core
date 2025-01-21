"""Viessmann ViCare sensor device."""

from __future__ import annotations

from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass
import logging

from PyViCare.PyViCareDevice import Device as PyViCareDevice
from PyViCare.PyViCareDeviceConfig import PyViCareDeviceConfig
from PyViCare.PyViCareHeatingDevice import (
    HeatingDeviceWithComponent as PyViCareHeatingDeviceComponent,
)
from PyViCare.PyViCareUtils import (
    PyViCareInvalidDataError,
    PyViCareNotSupportedFeatureError,
    PyViCareRateLimitError,
)
import requests

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    EntityCategory,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
    UnitOfVolume,
    UnitOfVolumeFlowRate,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    VICARE_CUBIC_METER,
    VICARE_KW,
    VICARE_KWH,
    VICARE_PERCENT,
    VICARE_W,
    VICARE_WH,
)
from .entity import ViCareEntity
from .types import ViCareConfigEntry, ViCareDevice, ViCareRequiredKeysMixin
from .utils import (
    filter_state,
    get_burners,
    get_circuits,
    get_compressors,
    get_device_serial,
    is_supported,
)

_LOGGER = logging.getLogger(__name__)

VICARE_UNIT_TO_DEVICE_CLASS = {
    VICARE_WH: SensorDeviceClass.ENERGY,
    VICARE_KWH: SensorDeviceClass.ENERGY,
    VICARE_W: SensorDeviceClass.POWER,
    VICARE_KW: SensorDeviceClass.POWER,
    VICARE_CUBIC_METER: SensorDeviceClass.GAS,
}

VICARE_UNIT_TO_HA_UNIT = {
    VICARE_PERCENT: PERCENTAGE,
    VICARE_W: UnitOfPower.WATT,
    VICARE_KW: UnitOfPower.KILO_WATT,
    VICARE_WH: UnitOfEnergy.WATT_HOUR,
    VICARE_KWH: UnitOfEnergy.KILO_WATT_HOUR,
    VICARE_CUBIC_METER: UnitOfVolume.CUBIC_METERS,
}


@dataclass(frozen=True)
class ViCareSensorEntityDescription(SensorEntityDescription, ViCareRequiredKeysMixin):
    """Describes ViCare sensor entity."""

    unit_getter: Callable[[PyViCareDevice], str | None] | None = None


GLOBAL_SENSORS: tuple[ViCareSensorEntityDescription, ...] = (
    ViCareSensorEntityDescription(
        key="outside_temperature",
        REDACTED_VALUE"outside_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getOutsideTemperature(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ViCareSensorEntityDescription(
        key="return_temperature",
        REDACTED_VALUE"return_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getReturnTemperature(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ViCareSensorEntityDescription(
        key="boiler_temperature",
        REDACTED_VALUE"boiler_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getBoilerTemperature(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ViCareSensorEntityDescription(
        key="boiler_supply_temperature",
        REDACTED_VALUE"boiler_supply_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getBoilerCommonSupplyTemperature(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ViCareSensorEntityDescription(
        key="primary_circuit_supply_temperature",
        REDACTED_VALUE"primary_circuit_supply_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getSupplyTemperaturePrimaryCircuit(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ViCareSensorEntityDescription(
        key="primary_circuit_return_temperature",
        REDACTED_VALUE"primary_circuit_return_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getReturnTemperaturePrimaryCircuit(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ViCareSensorEntityDescription(
        key="secondary_circuit_supply_temperature",
        REDACTED_VALUE"secondary_circuit_supply_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getSupplyTemperatureSecondaryCircuit(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ViCareSensorEntityDescription(
        key="secondary_circuit_return_temperature",
        REDACTED_VALUE"secondary_circuit_return_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getReturnTemperatureSecondaryCircuit(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ViCareSensorEntityDescription(
        key="hotwater_out_temperature",
        REDACTED_VALUE"hotwater_out_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getDomesticHotWaterOutletTemperature(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ViCareSensorEntityDescription(
        key="hotwater_max_temperature",
        REDACTED_VALUE"hotwater_max_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getDomesticHotWaterMaxTemperature(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="hotwater_min_temperature",
        REDACTED_VALUE"hotwater_min_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getDomesticHotWaterMinTemperature(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="dhw_storage_temperature",
        REDACTED_VALUE"dhw_storage_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getDomesticHotWaterStorageTemperature(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ViCareSensorEntityDescription(
        key="dhw_storage_top_temperature",
        REDACTED_VALUE"dhw_storage_top_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getHotWaterStorageTemperatureTop(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ViCareSensorEntityDescription(
        key="dhw_storage_bottom_temperature",
        REDACTED_VALUE"dhw_storage_bottom_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getHotWaterStorageTemperatureBottom(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ViCareSensorEntityDescription(
        key="hotwater_gas_consumption_today",
        REDACTED_VALUE"hotwater_gas_consumption_today",
        value_getter=lambda api: api.getGasConsumptionDomesticHotWaterToday(),
        unit_getter=lambda api: api.getGasConsumptionDomesticHotWaterUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    ViCareSensorEntityDescription(
        key="hotwater_gas_consumption_heating_this_week",
        REDACTED_VALUE"hotwater_gas_consumption_heating_this_week",
        value_getter=lambda api: api.getGasConsumptionDomesticHotWaterThisWeek(),
        unit_getter=lambda api: api.getGasConsumptionDomesticHotWaterUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="hotwater_gas_consumption_heating_this_month",
        REDACTED_VALUE"hotwater_gas_consumption_heating_this_month",
        value_getter=lambda api: api.getGasConsumptionDomesticHotWaterThisMonth(),
        unit_getter=lambda api: api.getGasConsumptionDomesticHotWaterUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="hotwater_gas_consumption_heating_this_year",
        REDACTED_VALUE"hotwater_gas_consumption_heating_this_year",
        value_getter=lambda api: api.getGasConsumptionDomesticHotWaterThisYear(),
        unit_getter=lambda api: api.getGasConsumptionDomesticHotWaterUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="gas_consumption_heating_today",
        REDACTED_VALUE"gas_consumption_heating_today",
        value_getter=lambda api: api.getGasConsumptionHeatingToday(),
        unit_getter=lambda api: api.getGasConsumptionHeatingUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    ViCareSensorEntityDescription(
        key="gas_consumption_heating_this_week",
        REDACTED_VALUE"gas_consumption_heating_this_week",
        value_getter=lambda api: api.getGasConsumptionHeatingThisWeek(),
        unit_getter=lambda api: api.getGasConsumptionHeatingUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="gas_consumption_heating_this_month",
        REDACTED_VALUE"gas_consumption_heating_this_month",
        value_getter=lambda api: api.getGasConsumptionHeatingThisMonth(),
        unit_getter=lambda api: api.getGasConsumptionHeatingUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="gas_consumption_heating_this_year",
        REDACTED_VALUE"gas_consumption_heating_this_year",
        value_getter=lambda api: api.getGasConsumptionHeatingThisYear(),
        unit_getter=lambda api: api.getGasConsumptionHeatingUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="gas_consumption_fuelcell_today",
        REDACTED_VALUE"gas_consumption_fuelcell_today",
        value_getter=lambda api: api.getFuelCellGasConsumptionToday(),
        unit_getter=lambda api: api.getFuelCellGasConsumptionUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    ViCareSensorEntityDescription(
        key="gas_consumption_fuelcell_this_week",
        REDACTED_VALUE"gas_consumption_fuelcell_this_week",
        value_getter=lambda api: api.getFuelCellGasConsumptionThisWeek(),
        unit_getter=lambda api: api.getFuelCellGasConsumptionUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="gas_consumption_fuelcell_this_month",
        REDACTED_VALUE"gas_consumption_fuelcell_this_month",
        value_getter=lambda api: api.getFuelCellGasConsumptionThisMonth(),
        unit_getter=lambda api: api.getFuelCellGasConsumptionUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="gas_consumption_fuelcell_this_year",
        REDACTED_VALUE"gas_consumption_fuelcell_this_year",
        value_getter=lambda api: api.getFuelCellGasConsumptionThisYear(),
        unit_getter=lambda api: api.getFuelCellGasConsumptionUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="gas_consumption_total_today",
        REDACTED_VALUE"gas_consumption_total_today",
        value_getter=lambda api: api.getGasConsumptionTotalToday(),
        unit_getter=lambda api: api.getGasConsumptionUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    ViCareSensorEntityDescription(
        key="gas_consumption_total_this_week",
        REDACTED_VALUE"gas_consumption_total_this_week",
        value_getter=lambda api: api.getGasConsumptionTotalThisWeek(),
        unit_getter=lambda api: api.getGasConsumptionUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="gas_consumption_total_this_month",
        REDACTED_VALUE"gas_consumption_total_this_month",
        value_getter=lambda api: api.getGasConsumptionTotalThisMonth(),
        unit_getter=lambda api: api.getGasConsumptionUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="gas_consumption_total_this_year",
        REDACTED_VALUE"gas_consumption_total_this_year",
        value_getter=lambda api: api.getGasConsumptionTotalThisYear(),
        unit_getter=lambda api: api.getGasConsumptionUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="gas_summary_consumption_heating_currentday",
        REDACTED_VALUE"gas_summary_consumption_heating_currentday",
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        value_getter=lambda api: api.getGasSummaryConsumptionHeatingCurrentDay(),
        unit_getter=lambda api: api.getGasSummaryConsumptionHeatingUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    ViCareSensorEntityDescription(
        key="gas_summary_consumption_heating_currentmonth",
        REDACTED_VALUE"gas_summary_consumption_heating_currentmonth",
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        value_getter=lambda api: api.getGasSummaryConsumptionHeatingCurrentMonth(),
        unit_getter=lambda api: api.getGasSummaryConsumptionHeatingUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="gas_summary_consumption_heating_currentyear",
        REDACTED_VALUE"gas_summary_consumption_heating_currentyear",
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        value_getter=lambda api: api.getGasSummaryConsumptionHeatingCurrentYear(),
        unit_getter=lambda api: api.getGasSummaryConsumptionHeatingUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="gas_summary_consumption_heating_lastsevendays",
        REDACTED_VALUE"gas_summary_consumption_heating_lastsevendays",
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        value_getter=lambda api: api.getGasSummaryConsumptionHeatingLastSevenDays(),
        unit_getter=lambda api: api.getGasSummaryConsumptionHeatingUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="hotwater_gas_summary_consumption_heating_currentday",
        REDACTED_VALUE"hotwater_gas_summary_consumption_heating_currentday",
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        value_getter=lambda api: api.getGasSummaryConsumptionDomesticHotWaterCurrentDay(),
        unit_getter=lambda api: api.getGasSummaryConsumptionDomesticHotWaterUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    ViCareSensorEntityDescription(
        key="hotwater_gas_summary_consumption_heating_currentmonth",
        REDACTED_VALUE"hotwater_gas_summary_consumption_heating_currentmonth",
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        value_getter=lambda api: api.getGasSummaryConsumptionDomesticHotWaterCurrentMonth(),
        unit_getter=lambda api: api.getGasSummaryConsumptionDomesticHotWaterUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="hotwater_gas_summary_consumption_heating_currentyear",
        REDACTED_VALUE"hotwater_gas_summary_consumption_heating_currentyear",
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        value_getter=lambda api: api.getGasSummaryConsumptionDomesticHotWaterCurrentYear(),
        unit_getter=lambda api: api.getGasSummaryConsumptionDomesticHotWaterUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="hotwater_gas_summary_consumption_heating_lastsevendays",
        REDACTED_VALUE"hotwater_gas_summary_consumption_heating_lastsevendays",
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        value_getter=lambda api: api.getGasSummaryConsumptionDomesticHotWaterLastSevenDays(),
        unit_getter=lambda api: api.getGasSummaryConsumptionDomesticHotWaterUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="energy_summary_consumption_heating_currentday",
        REDACTED_VALUE"energy_summary_consumption_heating_currentday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerSummaryConsumptionHeatingCurrentDay(),
        unit_getter=lambda api: api.getPowerSummaryConsumptionHeatingUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    ViCareSensorEntityDescription(
        key="energy_summary_consumption_heating_currentmonth",
        REDACTED_VALUE"energy_summary_consumption_heating_currentmonth",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerSummaryConsumptionHeatingCurrentMonth(),
        unit_getter=lambda api: api.getPowerSummaryConsumptionHeatingUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="energy_summary_consumption_heating_currentyear",
        REDACTED_VALUE"energy_summary_consumption_heating_currentyear",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerSummaryConsumptionHeatingCurrentYear(),
        unit_getter=lambda api: api.getPowerSummaryConsumptionHeatingUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="energy_summary_consumption_heating_lastsevendays",
        REDACTED_VALUE"energy_summary_consumption_heating_lastsevendays",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerSummaryConsumptionHeatingLastSevenDays(),
        unit_getter=lambda api: api.getPowerSummaryConsumptionHeatingUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="energy_consumption_cooling_today",
        REDACTED_VALUE"energy_consumption_cooling_today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerConsumptionCoolingToday(),
        unit_getter=lambda api: api.getPowerConsumptionCoolingUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    ViCareSensorEntityDescription(
        key="energy_consumption_cooling_this_month",
        REDACTED_VALUE"energy_consumption_cooling_this_month",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerConsumptionCoolingThisMonth(),
        unit_getter=lambda api: api.getPowerConsumptionCoolingUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="energy_consumption_cooling_this_year",
        REDACTED_VALUE"energy_consumption_cooling_this_year",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerConsumptionCoolingThisYear(),
        unit_getter=lambda api: api.getPowerConsumptionCoolingUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="energy_dhw_summary_consumption_heating_currentday",
        REDACTED_VALUE"energy_dhw_summary_consumption_heating_currentday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerSummaryConsumptionDomesticHotWaterCurrentDay(),
        unit_getter=lambda api: api.getPowerSummaryConsumptionDomesticHotWaterUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    ViCareSensorEntityDescription(
        key="energy_dhw_summary_consumption_heating_currentmonth",
        REDACTED_VALUE"energy_dhw_summary_consumption_heating_currentmonth",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerSummaryConsumptionDomesticHotWaterCurrentMonth(),
        unit_getter=lambda api: api.getPowerSummaryConsumptionDomesticHotWaterUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="energy_dhw_summary_consumption_heating_currentyear",
        REDACTED_VALUE"energy_dhw_summary_consumption_heating_currentyear",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerSummaryConsumptionDomesticHotWaterCurrentYear(),
        unit_getter=lambda api: api.getPowerSummaryConsumptionDomesticHotWaterUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="energy_summary_dhw_consumption_heating_lastsevendays",
        REDACTED_VALUE"energy_summary_dhw_consumption_heating_lastsevendays",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerSummaryConsumptionDomesticHotWaterLastSevenDays(),
        unit_getter=lambda api: api.getPowerSummaryConsumptionDomesticHotWaterUnit(),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="power_production_current",
        REDACTED_VALUE"power_production_current",
        native_unit_of_measurement=UnitOfPower.WATT,
        value_getter=lambda api: api.getPowerProductionCurrent(),
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ViCareSensorEntityDescription(
        key="power_production_today",
        REDACTED_VALUE"power_production_today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerProductionToday(),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    ViCareSensorEntityDescription(
        key="power_production_this_week",
        REDACTED_VALUE"power_production_this_week",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerProductionThisWeek(),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="power_production_this_month",
        REDACTED_VALUE"power_production_this_month",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerProductionThisMonth(),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="power_production_this_year",
        REDACTED_VALUE"power_production_this_year",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerProductionThisYear(),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="solar storage temperature",
        REDACTED_VALUE"solar_storage_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getSolarStorageTemperature(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ViCareSensorEntityDescription(
        key="collector temperature",
        REDACTED_VALUE"collector_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getSolarCollectorTemperature(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ViCareSensorEntityDescription(
        key="solar power production today",
        REDACTED_VALUE"solar_power_production_today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getSolarPowerProductionToday(),
        unit_getter=lambda api: api.getSolarPowerProductionUnit(),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    ViCareSensorEntityDescription(
        key="solar power production this week",
        REDACTED_VALUE"solar_power_production_this_week",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getSolarPowerProductionThisWeek(),
        unit_getter=lambda api: api.getSolarPowerProductionUnit(),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="solar power production this month",
        REDACTED_VALUE"solar_power_production_this_month",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getSolarPowerProductionThisMonth(),
        unit_getter=lambda api: api.getSolarPowerProductionUnit(),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="solar power production this year",
        REDACTED_VALUE"solar_power_production_this_year",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getSolarPowerProductionThisYear(),
        unit_getter=lambda api: api.getSolarPowerProductionUnit(),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="power consumption today",
        REDACTED_VALUE"power_consumption_today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerConsumptionToday(),
        unit_getter=lambda api: api.getPowerConsumptionUnit(),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    ViCareSensorEntityDescription(
        key="power consumption this week",
        REDACTED_VALUE"power_consumption_this_week",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerConsumptionThisWeek(),
        unit_getter=lambda api: api.getPowerConsumptionUnit(),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="power consumption this month",
        REDACTED_VALUE"power consumption this month",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerConsumptionThisMonth(),
        unit_getter=lambda api: api.getPowerConsumptionUnit(),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="power consumption this year",
        REDACTED_VALUE"power_consumption_this_year",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        value_getter=lambda api: api.getPowerConsumptionThisYear(),
        unit_getter=lambda api: api.getPowerConsumptionUnit(),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="buffer top temperature",
        REDACTED_VALUE"buffer_top_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getBufferTopTemperature(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ViCareSensorEntityDescription(
        key="buffer main temperature",
        REDACTED_VALUE"buffer_main_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getBufferMainTemperature(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ViCareSensorEntityDescription(
        key="volumetric_flow",
        REDACTED_VALUE"volumetric_flow",
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        value_getter=lambda api: api.getVolumetricFlowReturn() / 1000,
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ViCareSensorEntityDescription(
        key="ess_state_of_charge",
        REDACTED_VALUE"ess_state_of_charge",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        value_getter=lambda api: api.getElectricalEnergySystemSOC(),
        unit_getter=lambda api: api.getElectricalEnergySystemSOCUnit(),
    ),
    ViCareSensorEntityDescription(
        key="ess_power_current",
        REDACTED_VALUE"ess_power_current",
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_getter=lambda api: api.getElectricalEnergySystemPower(),
        unit_getter=lambda api: api.getElectricalEnergySystemPowerUnit(),
    ),
    ViCareSensorEntityDescription(
        key="ess_state",
        REDACTED_VALUE"ess_state",
        device_class=SensorDeviceClass.ENUM,
        options=["charge", "discharge", "standby"],
        value_getter=lambda api: api.getElectricalEnergySystemOperationState(),
    ),
    ViCareSensorEntityDescription(
        key="ess_discharge_today",
        REDACTED_VALUE"ess_discharge_today",
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_getter=lambda api: api.getElectricalEnergySystemTransferDischargeCumulatedCurrentDay(),
        unit_getter=lambda api: api.getElectricalEnergySystemTransferDischargeCumulatedUnit(),
    ),
    ViCareSensorEntityDescription(
        key="ess_discharge_this_week",
        REDACTED_VALUE"ess_discharge_this_week",
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_getter=lambda api: api.getElectricalEnergySystemTransferDischargeCumulatedCurrentWeek(),
        unit_getter=lambda api: api.getElectricalEnergySystemTransferDischargeCumulatedUnit(),
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="ess_discharge_this_month",
        REDACTED_VALUE"ess_discharge_this_month",
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_getter=lambda api: api.getElectricalEnergySystemTransferDischargeCumulatedCurrentMonth(),
        unit_getter=lambda api: api.getElectricalEnergySystemTransferDischargeCumulatedUnit(),
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="ess_discharge_this_year",
        REDACTED_VALUE"ess_discharge_this_year",
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_getter=lambda api: api.getElectricalEnergySystemTransferDischargeCumulatedCurrentYear(),
        unit_getter=lambda api: api.getElectricalEnergySystemTransferDischargeCumulatedUnit(),
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="ess_discharge_total",
        REDACTED_VALUE"ess_discharge_total",
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_getter=lambda api: api.getElectricalEnergySystemTransferDischargeCumulatedLifeCycle(),
        unit_getter=lambda api: api.getElectricalEnergySystemTransferDischargeCumulatedUnit(),
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="pcc_transfer_power_exchange",
        REDACTED_VALUE"pcc_transfer_power_exchange",
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_getter=lambda api: api.getPointOfCommonCouplingTransferPowerExchange(),
    ),
    ViCareSensorEntityDescription(
        key="pcc_energy_consumption",
        REDACTED_VALUE"pcc_energy_consumption",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_getter=lambda api: api.getPointOfCommonCouplingTransferConsumptionTotal(),
        unit_getter=lambda api: api.getPointOfCommonCouplingTransferConsumptionTotalUnit(),
    ),
    ViCareSensorEntityDescription(
        key="pcc_energy_feed_in",
        REDACTED_VALUE"pcc_energy_feed_in",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_getter=lambda api: api.getPointOfCommonCouplingTransferFeedInTotal(),
        unit_getter=lambda api: api.getPointOfCommonCouplingTransferFeedInTotalUnit(),
    ),
    ViCareSensorEntityDescription(
        key="photovoltaic_power_production_current",
        REDACTED_VALUE"photovoltaic_power_production_current",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_getter=lambda api: api.getPhotovoltaicProductionCurrent(),
        unit_getter=lambda api: api.getPhotovoltaicProductionCurrentUnit(),
    ),
    ViCareSensorEntityDescription(
        key="photovoltaic_energy_production_today",
        REDACTED_VALUE"photovoltaic_energy_production_today",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_getter=lambda api: api.getPhotovoltaicProductionCumulatedCurrentDay(),
        unit_getter=lambda api: api.getPhotovoltaicProductionCumulatedUnit(),
    ),
    ViCareSensorEntityDescription(
        key="photovoltaic_energy_production_this_week",
        REDACTED_VALUE"photovoltaic_energy_production_this_week",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_getter=lambda api: api.getPhotovoltaicProductionCumulatedCurrentWeek(),
        unit_getter=lambda api: api.getPhotovoltaicProductionCumulatedUnit(),
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="photovoltaic_energy_production_this_month",
        REDACTED_VALUE"photovoltaic_energy_production_this_month",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_getter=lambda api: api.getPhotovoltaicProductionCumulatedCurrentMonth(),
        unit_getter=lambda api: api.getPhotovoltaicProductionCumulatedUnit(),
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="photovoltaic_energy_production_this_year",
        REDACTED_VALUE"photovoltaic_energy_production_this_year",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_getter=lambda api: api.getPhotovoltaicProductionCumulatedCurrentYear(),
        unit_getter=lambda api: api.getPhotovoltaicProductionCumulatedUnit(),
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="photovoltaic_energy_production_total",
        REDACTED_VALUE"photovoltaic_energy_production_total",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_getter=lambda api: api.getPhotovoltaicProductionCumulatedLifeCycle(),
        unit_getter=lambda api: api.getPhotovoltaicProductionCumulatedUnit(),
    ),
    ViCareSensorEntityDescription(
        key="photovoltaic_status",
        REDACTED_VALUE"photovoltaic_status",
        device_class=SensorDeviceClass.ENUM,
        options=["ready", "production"],
        value_getter=lambda api: filter_state(api.getPhotovoltaicStatus()),
    ),
    ViCareSensorEntityDescription(
        key="room_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_getter=lambda api: api.getTemperature(),
    ),
    ViCareSensorEntityDescription(
        key="room_humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_getter=lambda api: api.getHumidity(),
    ),
    ViCareSensorEntityDescription(
        key="ventilation_level",
        REDACTED_VALUE"ventilation_level",
        value_getter=lambda api: filter_state(api.getVentilationLevel().lower()),
        device_class=SensorDeviceClass.ENUM,
        options=["standby", "levelone", "leveltwo", "levelthree", "levelfour"],
    ),
    ViCareSensorEntityDescription(
        key="ventilation_reason",
        REDACTED_VALUE"ventilation_reason",
        value_getter=lambda api: api.getVentilationReason().lower(),
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        device_class=SensorDeviceClass.ENUM,
        options=[
            "standby",
            "permanent",
            "schedule",
            "sensordriven",
            "silent",
            "forcedlevelfour",
        ],
    ),
)

CIRCUIT_SENSORS: tuple[ViCareSensorEntityDescription, ...] = (
    ViCareSensorEntityDescription(
        key="supply_temperature",
        REDACTED_VALUE"supply_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_getter=lambda api: api.getSupplyTemperature(),
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)

BURNER_SENSORS: tuple[ViCareSensorEntityDescription, ...] = (
    ViCareSensorEntityDescription(
        key="burner_starts",
        REDACTED_VALUE"burner_starts",
        value_getter=lambda api: api.getStarts(),
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    ViCareSensorEntityDescription(
        key="burner_hours",
        REDACTED_VALUE"burner_hours",
        native_unit_of_measurement=UnitOfTime.HOURS,
        value_getter=lambda api: api.getHours(),
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    ViCareSensorEntityDescription(
        key="burner_modulation",
        REDACTED_VALUE"burner_modulation",
        native_unit_of_measurement=PERCENTAGE,
        value_getter=lambda api: api.getModulation(),
        state_class=SensorStateClass.MEASUREMENT,
    ),
)

COMPRESSOR_SENSORS: tuple[ViCareSensorEntityDescription, ...] = (
    ViCareSensorEntityDescription(
        key="compressor_starts",
        REDACTED_VALUE"compressor_starts",
        value_getter=lambda api: api.getStarts(),
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    ViCareSensorEntityDescription(
        key="compressor_hours",
        REDACTED_VALUE"compressor_hours",
        native_unit_of_measurement=UnitOfTime.HOURS,
        value_getter=lambda api: api.getHours(),
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    ViCareSensorEntityDescription(
        key="compressor_hours_loadclass1",
        REDACTED_VALUE"compressor_hours_loadclass1",
        native_unit_of_measurement=UnitOfTime.HOURS,
        value_getter=lambda api: api.getHoursLoadClass1(),
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="compressor_hours_loadclass2",
        REDACTED_VALUE"compressor_hours_loadclass2",
        native_unit_of_measurement=UnitOfTime.HOURS,
        value_getter=lambda api: api.getHoursLoadClass2(),
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="compressor_hours_loadclass3",
        REDACTED_VALUE"compressor_hours_loadclass3",
        native_unit_of_measurement=UnitOfTime.HOURS,
        value_getter=lambda api: api.getHoursLoadClass3(),
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="compressor_hours_loadclass4",
        REDACTED_VALUE"compressor_hours_loadclass4",
        native_unit_of_measurement=UnitOfTime.HOURS,
        value_getter=lambda api: api.getHoursLoadClass4(),
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="compressor_hours_loadclass5",
        REDACTED_VALUE"compressor_hours_loadclass5",
        native_unit_of_measurement=UnitOfTime.HOURS,
        value_getter=lambda api: api.getHoursLoadClass5(),
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    ViCareSensorEntityDescription(
        key="compressor_phase",
        REDACTED_VALUE"compressor_phase",
        value_getter=lambda api: api.getPhase(),
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


def _build_entities(
    device_list: list[ViCareDevice],
) -> list[ViCareSensor]:
    """Create ViCare sensor entities for a device."""

    entities: list[ViCareSensor] = []
    for device in device_list:
        # add device entities
        entities.extend(
            ViCareSensor(
                description,
                get_device_serial(device.api),
                device.config,
                device.api,
            )
            for description in GLOBAL_SENSORS
            if is_supported(description.key, description, device.api)
        )
        # add component entities
        for component_list, entity_description_list in (
            (get_circuits(device.api), CIRCUIT_SENSORS),
            (get_burners(device.api), BURNER_SENSORS),
            (get_compressors(device.api), COMPRESSOR_SENSORS),
        ):
            entities.extend(
                ViCareSensor(
                    description,
                    get_device_serial(device.api),
                    device.config,
                    device.api,
                    component,
                )
                for component in component_list
                for description in entity_description_list
                if is_supported(description.key, description, component)
            )
    return entities


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ViCareConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create the ViCare sensor devices."""
    async_add_entities(
        await hass.async_add_executor_job(
            _build_entities,
            config_entry.runtime_data.devices,
        ),
        # run update to have device_class set depending on unit_of_measurement
        True,
    )


class ViCareSensor(ViCareEntity, SensorEntity):
    """Representation of a ViCare sensor."""

    entity_description: ViCareSensorEntityDescription

    def __init__(
        self,
        description: ViCareSensorEntityDescription,
        device_serial: str | None,
        device_config: PyViCareDeviceConfig,
        device: PyViCareDevice,
        component: PyViCareHeatingDeviceComponent | None = None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            description.key, device_serial, device_config, device, component
        )
        self.entity_description = description

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._attr_native_value is not None

    def update(self) -> None:
        """Update state of sensor."""
        vicare_unit = None
        try:
            with suppress(PyViCareNotSupportedFeatureError):
                self._attr_native_value = self.entity_description.value_getter(
                    self._api
                )

                if self.entity_description.unit_getter:
                    vicare_unit = self.entity_description.unit_getter(self._api)
        except requests.exceptions.ConnectionError:
            _LOGGER.error("Unable to retrieve data from ViCare server")
        except ValueError:
            _LOGGER.error("Unable to decode data from ViCare server")
        except PyViCareRateLimitError as limit_exception:
            _LOGGER.error("Vicare API rate limit exceeded: %s", limit_exception)
        except PyViCareInvalidDataError as invalid_data_exception:
            _LOGGER.error("Invalid data from Vicare server: %s", invalid_data_exception)

        if vicare_unit is not None:
            if (
                device_class := VICARE_UNIT_TO_DEVICE_CLASS.get(vicare_unit)
            ) is not None:
                self._attr_device_class = device_class
            self._attr_native_unit_of_measurement = VICARE_UNIT_TO_HA_UNIT.get(
                vicare_unit
            )
