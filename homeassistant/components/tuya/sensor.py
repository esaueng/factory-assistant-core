"""Support for Tuya sensors."""

from dataclasses import dataclass

from tuya_device_handlers.definition.sensor import (
    SensorDefinition,
    get_default_definition,
)
from tuya_device_handlers.device_wrapper.common import (
    DPCodeEnumWrapper,
    DPCodeTypeInformationWrapper,
)
from tuya_device_handlers.device_wrapper.sensor import (
    DeltaIntegerWrapper,
    ElectricityCurrentJsonWrapper,
    ElectricityCurrentRawWrapper,
    ElectricityPowerJsonWrapper,
    ElectricityPowerRawWrapper,
    ElectricityVoltageJsonWrapper,
    ElectricityVoltageRawWrapper,
    WindDirectionEnumWrapper,
)
from tuya_sharing import CustomerDevice, Manager

from homeassistant.components.sensor import (
    DEVICE_CLASS_UNITS as SENSOR_DEVICE_CLASS_UNITS,
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    EntityCategory,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import (
    DEVICE_CLASS_UNITS,
    DOMAIN,
    LOGGER,
    TUYA_DISCOVERY_NEW,
    DeviceCategory,
    DPCode,
)
from .coordinator import TuyaConfigEntry
from .entity import TuyaEntity

CURRENT_WRAPPER = (ElectricityCurrentRawWrapper, ElectricityCurrentJsonWrapper)
POWER_WRAPPER = (ElectricityPowerRawWrapper, ElectricityPowerJsonWrapper)
VOLTAGE_WRAPPER = (ElectricityVoltageRawWrapper, ElectricityVoltageJsonWrapper)


@dataclass(frozen=True)
class TuyaSensorEntityDescription(SensorEntityDescription):
    """Describes Tuya sensor entity."""

    dpcode: DPCode | None = None
    wrapper_class: tuple[type[DPCodeTypeInformationWrapper], ...] | None = None


# Commonly used battery sensors, that are reused in the sensors down below.
BATTERY_SENSORS: tuple[TuyaSensorEntityDescription, ...] = (
    TuyaSensorEntityDescription(
        key=DPCode.BATTERY_PERCENTAGE,
        REDACTED_VALUE"battery",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    TuyaSensorEntityDescription(
        key=DPCode.BATTERY,  # Used by non-standard contact sensor implementations
        REDACTED_VALUE"battery",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    TuyaSensorEntityDescription(
        key=DPCode.BATTERY_STATE,
        REDACTED_VALUE"battery_state",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    TuyaSensorEntityDescription(
        key=DPCode.BATTERY_VALUE,
        REDACTED_VALUE"battery",
        device_class=SensorDeviceClass.BATTERY,
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    TuyaSensorEntityDescription(
        key=DPCode.VA_BATTERY,
        REDACTED_VALUE"battery",
        device_class=SensorDeviceClass.BATTERY,
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)

# All descriptions can be found here. Mostly the Integer data types in the
# default status set of each category (that don't have a set instruction)
# end up being a sensor.
SENSORS: dict[DeviceCategory, tuple[TuyaSensorEntityDescription, ...]] = {
    DeviceCategory.AQCZ: (
        TuyaSensorEntityDescription(
            key=DPCode.CUR_CURRENT,
            REDACTED_VALUE"current",
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            entity_registry_enabled_default=False,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUR_POWER,
            REDACTED_VALUE"power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            entity_registry_enabled_default=False,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUR_VOLTAGE,
            REDACTED_VALUE"voltage",
            device_class=SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=UnitOfElectricPotential.VOLT,
            entity_registry_enabled_default=False,
        ),
    ),
    DeviceCategory.BH: (
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"current_temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT_F,
            REDACTED_VALUE"current_temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.STATUS,
            REDACTED_VALUE"status",
        ),
    ),
    DeviceCategory.CL: (
        TuyaSensorEntityDescription(
            key=DPCode.TIME_TOTAL,
            REDACTED_VALUE"last_operation_duration",
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
    ),
    DeviceCategory.CO2BJ: (
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY_VALUE,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CO2_VALUE,
            REDACTED_VALUE"carbon_dioxide",
            device_class=SensorDeviceClass.CO2,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CH2O_VALUE,
            REDACTED_VALUE"formaldehyde",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.VOC_VALUE,
            REDACTED_VALUE"voc",
            device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.PM25_VALUE,
            REDACTED_VALUE"pm25",
            device_class=SensorDeviceClass.PM25,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.PM10,
            REDACTED_VALUE"pm10",
            device_class=SensorDeviceClass.PM10,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.COBJ: (
        TuyaSensorEntityDescription(
            key=DPCode.CO_VALUE,
            REDACTED_VALUE"carbon_monoxide",
            device_class=SensorDeviceClass.CO,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.CS: (
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_INDOOR,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY_INDOOR,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
    ),
    DeviceCategory.CWJWQ: (
        TuyaSensorEntityDescription(
            key=DPCode.WORK_STATE_E,
            REDACTED_VALUE"odor_elimination_status",
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.CWWSQ: (
        *BATTERY_SENSORS,
        TuyaSensorEntityDescription(
            key=DPCode.FEED_REPORT,
            REDACTED_VALUE"last_amount",
            state_class=SensorStateClass.MEASUREMENT,
        ),
    ),
    DeviceCategory.CWYSJ: (
        TuyaSensorEntityDescription(
            key=DPCode.UV_RUNTIME,
            REDACTED_VALUE"uv_runtime",
            device_class=SensorDeviceClass.DURATION,
            state_class=SensorStateClass.MEASUREMENT,
            entity_registry_enabled_default=False,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.PUMP_TIME,
            REDACTED_VALUE"pump_time",
            device_class=SensorDeviceClass.DURATION,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.FILTER_DURATION,
            REDACTED_VALUE"filter_duration",
            device_class=SensorDeviceClass.DURATION,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.WATER_TIME,
            REDACTED_VALUE"water_time",
            device_class=SensorDeviceClass.DURATION,
            state_class=SensorStateClass.MEASUREMENT,
            entity_registry_enabled_default=False,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.WATER_LEVEL, REDACTED_VALUE"water_level_state"
        ),
    ),
    DeviceCategory.DGNBJ: (
        TuyaSensorEntityDescription(
            key=DPCode.GAS_SENSOR_VALUE,
            REDACTED_VALUE"gas",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CH4_SENSOR_VALUE,
            REDACTED_VALUE"gas",
            name="Methane",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.VOC_VALUE,
            REDACTED_VALUE"voc",
            device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.PM25_VALUE,
            REDACTED_VALUE"pm25",
            device_class=SensorDeviceClass.PM25,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CO_VALUE,
            REDACTED_VALUE"carbon_monoxide",
            device_class=SensorDeviceClass.CO,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CO2_VALUE,
            REDACTED_VALUE"carbon_dioxide",
            device_class=SensorDeviceClass.CO2,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.EC_CURRENT,
            device_class=SensorDeviceClass.CONDUCTIVITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CH2O_VALUE,
            REDACTED_VALUE"formaldehyde",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.BRIGHT_STATE,
            REDACTED_VALUE"luminosity",
        ),
        TuyaSensorEntityDescription(
            key=DPCode.BRIGHT_VALUE,
            REDACTED_VALUE"illuminance",
            device_class=SensorDeviceClass.ILLUMINANCE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY_VALUE,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.ORP_CURRENT,
            REDACTED_VALUE"oxydo_reduction_potential",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.PH_CURRENT,
            device_class=SensorDeviceClass.PH,
            # pH is unitless; treat any Tuya-reported "pH"/"ph" unit as unitless
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.SMOKE_SENSOR_VALUE,
            REDACTED_VALUE"smoke_amount",
            entity_category=EntityCategory.DIAGNOSTIC,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.DLQ: (
        TuyaSensorEntityDescription(
            key=DPCode.TOTAL_FORWARD_ENERGY,
            REDACTED_VALUE"total_energy",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.ADD_ELE,
            REDACTED_VALUE"total_energy",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.FORWARD_ENERGY_TOTAL,
            REDACTED_VALUE"total_energy",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.REVERSE_ENERGY_TOTAL,
            REDACTED_VALUE"total_production",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.SUPPLY_FREQUENCY,
            REDACTED_VALUE"supply_frequency",
            device_class=SensorDeviceClass.FREQUENCY,
            entity_category=EntityCategory.DIAGNOSTIC,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.PHASE_A}electriccurrent",
            dpcode=DPCode.PHASE_A,
            REDACTED_VALUE"phase_a_current",
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=CURRENT_WRAPPER,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.PHASE_A}power",
            dpcode=DPCode.PHASE_A,
            REDACTED_VALUE"phase_a_power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=POWER_WRAPPER,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.PHASE_A}voltage",
            dpcode=DPCode.PHASE_A,
            REDACTED_VALUE"phase_a_voltage",
            device_class=SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=VOLTAGE_WRAPPER,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.PHASE_B}electriccurrent",
            dpcode=DPCode.PHASE_B,
            REDACTED_VALUE"phase_b_current",
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=CURRENT_WRAPPER,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.PHASE_B}power",
            dpcode=DPCode.PHASE_B,
            REDACTED_VALUE"phase_b_power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=POWER_WRAPPER,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.PHASE_B}voltage",
            dpcode=DPCode.PHASE_B,
            REDACTED_VALUE"phase_b_voltage",
            device_class=SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=VOLTAGE_WRAPPER,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.PHASE_C}electriccurrent",
            dpcode=DPCode.PHASE_C,
            REDACTED_VALUE"phase_c_current",
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=CURRENT_WRAPPER,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.PHASE_C}power",
            dpcode=DPCode.PHASE_C,
            REDACTED_VALUE"phase_c_power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=POWER_WRAPPER,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.PHASE_C}voltage",
            dpcode=DPCode.PHASE_C,
            REDACTED_VALUE"phase_c_voltage",
            device_class=SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=VOLTAGE_WRAPPER,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUR_CURRENT,
            REDACTED_VALUE"current",
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            entity_registry_enabled_default=False,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUR_POWER,
            REDACTED_VALUE"power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            entity_registry_enabled_default=False,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUR_VOLTAGE,
            REDACTED_VALUE"voltage",
            device_class=SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=UnitOfElectricPotential.VOLT,
            entity_registry_enabled_default=False,
        ),
    ),
    DeviceCategory.FS: (
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
    ),
    DeviceCategory.GGQ: BATTERY_SENSORS,
    DeviceCategory.HJJCY: (
        TuyaSensorEntityDescription(
            key=DPCode.AIR_QUALITY_INDEX,
            REDACTED_VALUE"air_quality_index",
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY_VALUE,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CO2_VALUE,
            REDACTED_VALUE"carbon_dioxide",
            device_class=SensorDeviceClass.CO2,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CH2O_VALUE,
            REDACTED_VALUE"formaldehyde",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.VOC_VALUE,
            REDACTED_VALUE"voc",
            device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.PM25_VALUE,
            REDACTED_VALUE"pm25",
            device_class=SensorDeviceClass.PM25,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.PM10,
            REDACTED_VALUE"pm10",
            device_class=SensorDeviceClass.PM10,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.JQBJ: (
        TuyaSensorEntityDescription(
            key=DPCode.CO2_VALUE,
            REDACTED_VALUE"carbon_dioxide",
            device_class=SensorDeviceClass.CO2,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.VOC_VALUE,
            REDACTED_VALUE"voc",
            device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.PM25_VALUE,
            REDACTED_VALUE"pm25",
            device_class=SensorDeviceClass.PM25,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.VA_HUMIDITY,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.VA_TEMPERATURE,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CH2O_VALUE,
            REDACTED_VALUE"formaldehyde",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.JSQ: (
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY_CURRENT,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT_F,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.LEVEL_CURRENT,
            REDACTED_VALUE"water_level",
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
    ),
    DeviceCategory.JWBJ: (
        TuyaSensorEntityDescription(
            key=DPCode.CH4_SENSOR_VALUE,
            REDACTED_VALUE"methane",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.KG: (
        TuyaSensorEntityDescription(
            key=DPCode.CUR_CURRENT,
            REDACTED_VALUE"current",
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            entity_registry_enabled_default=False,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUR_POWER,
            REDACTED_VALUE"power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            entity_registry_enabled_default=False,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUR_VOLTAGE,
            REDACTED_VALUE"voltage",
            device_class=SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=UnitOfElectricPotential.VOLT,
            entity_registry_enabled_default=False,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.ADD_ELE,
            REDACTED_VALUE"total_energy",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.PRO_ADD_ELE,
            REDACTED_VALUE"total_production",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
    ),
    DeviceCategory.KJ: (
        TuyaSensorEntityDescription(
            key=DPCode.FILTER,
            REDACTED_VALUE"filter_utilization",
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.PM25,
            REDACTED_VALUE"pm25",
            device_class=SensorDeviceClass.PM25,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TVOC,
            REDACTED_VALUE"total_volatile_organic_compound",
            device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.ECO2,
            REDACTED_VALUE"concentration_carbon_dioxide",
            device_class=SensorDeviceClass.CO2,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TOTAL_TIME,
            REDACTED_VALUE"total_operating_time",
            state_class=SensorStateClass.TOTAL_INCREASING,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TOTAL_PM,
            REDACTED_VALUE"total_absorption_particles",
            state_class=SensorStateClass.TOTAL_INCREASING,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.AIR_QUALITY,
            REDACTED_VALUE"air_quality",
        ),
    ),
    DeviceCategory.LDCG: (
        TuyaSensorEntityDescription(
            key=DPCode.BRIGHT_STATE,
            REDACTED_VALUE"luminosity",
        ),
        TuyaSensorEntityDescription(
            key=DPCode.BRIGHT_VALUE,
            REDACTED_VALUE"illuminance",
            device_class=SensorDeviceClass.ILLUMINANCE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY_VALUE,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CO2_VALUE,
            REDACTED_VALUE"carbon_dioxide",
            device_class=SensorDeviceClass.CO2,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.MC: BATTERY_SENSORS,
    DeviceCategory.MCS: BATTERY_SENSORS,
    DeviceCategory.MSP: (
        TuyaSensorEntityDescription(
            key=DPCode.CAT_WEIGHT,
            REDACTED_VALUE"cat_weight",
            device_class=SensorDeviceClass.WEIGHT,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.EXCRETION_TIME_DAY,
            REDACTED_VALUE"excretion_time_day",
            device_class=SensorDeviceClass.DURATION,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.EXCRETION_TIMES_DAY,
            REDACTED_VALUE"excretion_times_day",
        ),
        TuyaSensorEntityDescription(
            key=DPCode.STATUS,
            REDACTED_VALUE"cat_litter_box_status",
        ),
    ),
    DeviceCategory.MZJ: (
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"current_temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.STATUS,
            REDACTED_VALUE"sous_vide_status",
        ),
        TuyaSensorEntityDescription(
            key=DPCode.REMAIN_TIME,
            REDACTED_VALUE"remaining_time",
            native_unit_of_measurement=UnitOfTime.MINUTES,
        ),
    ),
    DeviceCategory.PIR: BATTERY_SENSORS,
    DeviceCategory.PM2_5: (
        TuyaSensorEntityDescription(
            key=DPCode.PM25_VALUE,
            REDACTED_VALUE"pm25",
            device_class=SensorDeviceClass.PM25,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CH2O_VALUE,
            REDACTED_VALUE"formaldehyde",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.VOC_VALUE,
            REDACTED_VALUE"voc",
            device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CO2_VALUE,
            REDACTED_VALUE"carbon_dioxide",
            device_class=SensorDeviceClass.CO2,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY_VALUE,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.PM1,
            REDACTED_VALUE"pm1",
            device_class=SensorDeviceClass.PM1,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.PM10,
            REDACTED_VALUE"pm10",
            device_class=SensorDeviceClass.PM10,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.QN: (
        TuyaSensorEntityDescription(
            key=DPCode.WORK_POWER,
            REDACTED_VALUE"power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
        ),
    ),
    DeviceCategory.QXJ: (
        TuyaSensorEntityDescription(
            key=DPCode.VA_TEMPERATURE,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT_EXTERNAL,
            REDACTED_VALUE"temperature_external",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT_EXTERNAL_1,
            REDACTED_VALUE"indexed_temperature_external",
            translation_placeholders={"index": "1"},
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT_EXTERNAL_2,
            REDACTED_VALUE"indexed_temperature_external",
            translation_placeholders={"index": "2"},
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT_EXTERNAL_3,
            REDACTED_VALUE"indexed_temperature_external",
            translation_placeholders={"index": "3"},
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.VA_HUMIDITY,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY_VALUE,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY_OUTDOOR,
            REDACTED_VALUE"humidity_outdoor",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY_OUTDOOR_1,
            REDACTED_VALUE"indexed_humidity_outdoor",
            translation_placeholders={"index": "1"},
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY_OUTDOOR_2,
            REDACTED_VALUE"indexed_humidity_outdoor",
            translation_placeholders={"index": "2"},
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY_OUTDOOR_3,
            REDACTED_VALUE"indexed_humidity_outdoor",
            translation_placeholders={"index": "3"},
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.ATMOSPHERIC_PRESSTURE,
            REDACTED_VALUE"air_pressure",
            device_class=SensorDeviceClass.PRESSURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.BRIGHT_VALUE,
            REDACTED_VALUE"illuminance",
            device_class=SensorDeviceClass.ILLUMINANCE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.WINDSPEED_AVG,
            device_class=SensorDeviceClass.WIND_SPEED,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.RAIN_24H,
            REDACTED_VALUE"precipitation_today",
            device_class=SensorDeviceClass.PRECIPITATION,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.RAIN_RATE,
            REDACTED_VALUE"precipitation_intensity",
            device_class=SensorDeviceClass.PRECIPITATION_INTENSITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.UV_INDEX,
            REDACTED_VALUE"uv_index",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.WIND_DIRECT,
            REDACTED_VALUE"wind_direction",
            device_class=SensorDeviceClass.WIND_DIRECTION,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=(WindDirectionEnumWrapper,),
        ),
        TuyaSensorEntityDescription(
            key=DPCode.DEW_POINT_TEMP,
            REDACTED_VALUE"dew_point_temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.FEELLIKE_TEMP,
            REDACTED_VALUE"feels_like_temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.HEAT_INDEX,
            REDACTED_VALUE"heat_index_temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.WINDCHILL_INDEX,
            REDACTED_VALUE"wind_chill_index_temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.RQBJ: (
        TuyaSensorEntityDescription(
            key=DPCode.GAS_SENSOR_VALUE,
            name=None,
            REDACTED_VALUE"gas",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.SD: (
        TuyaSensorEntityDescription(
            key=DPCode.CLEAN_AREA,
            REDACTED_VALUE"cleaning_area",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CLEAN_TIME,
            REDACTED_VALUE"cleaning_time",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TOTAL_CLEAN_AREA,
            REDACTED_VALUE"total_cleaning_area",
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TOTAL_CLEAN_TIME,
            REDACTED_VALUE"total_cleaning_time",
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TOTAL_CLEAN_COUNT,
            REDACTED_VALUE"total_cleaning_times",
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.DUSTER_CLOTH,
            REDACTED_VALUE"duster_cloth_life",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.EDGE_BRUSH,
            REDACTED_VALUE"side_brush_life",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.FILTER_LIFE,
            REDACTED_VALUE"filter_life",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.ROLL_BRUSH,
            REDACTED_VALUE"rolling_brush_life",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.ELECTRICITY_LEFT,
            REDACTED_VALUE"battery",
            device_class=SensorDeviceClass.BATTERY,
            entity_category=EntityCategory.DIAGNOSTIC,
            state_class=SensorStateClass.MEASUREMENT,
        ),
    ),
    DeviceCategory.SFKZQ: (
        # Total seconds of irrigation. Read-write value; the device appears to ignore the write action (maybe firmware bug)
        TuyaSensorEntityDescription(
            key=DPCode.TIME_USE,
            REDACTED_VALUE"total_watering_time",
            state_class=SensorStateClass.TOTAL_INCREASING,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.SGBJ: BATTERY_SENSORS,
    DeviceCategory.SJ: BATTERY_SENSORS,
    DeviceCategory.SOS: BATTERY_SENSORS,
    DeviceCategory.SP: (
        TuyaSensorEntityDescription(
            key=DPCode.SENSOR_TEMPERATURE,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.SENSOR_HUMIDITY,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.WIRELESS_ELECTRICITY,
            REDACTED_VALUE"battery",
            device_class=SensorDeviceClass.BATTERY,
            entity_category=EntityCategory.DIAGNOSTIC,
            state_class=SensorStateClass.MEASUREMENT,
        ),
    ),
    DeviceCategory.SWTZ: (
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT_2,
            REDACTED_VALUE"indexed_temperature",
            translation_placeholders={"index": "2"},
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.SZ: (
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY_CURRENT,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
    ),
    DeviceCategory.SZJCY: (
        TuyaSensorEntityDescription(
            key=DPCode.TDS_IN,
            REDACTED_VALUE"total_dissolved_solids",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.SZJQR: BATTERY_SENSORS,
    DeviceCategory.TDQ: (
        TuyaSensorEntityDescription(
            key=DPCode.CUR_CURRENT,
            REDACTED_VALUE"current",
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            entity_registry_enabled_default=False,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUR_POWER,
            REDACTED_VALUE"power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            entity_registry_enabled_default=False,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUR_VOLTAGE,
            REDACTED_VALUE"voltage",
            device_class=SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=UnitOfElectricPotential.VOLT,
            entity_registry_enabled_default=False,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.ADD_ELE,
            REDACTED_VALUE"total_energy",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.VA_TEMPERATURE,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.VA_HUMIDITY,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY_VALUE,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.BRIGHT_VALUE,
            REDACTED_VALUE"illuminance",
            device_class=SensorDeviceClass.ILLUMINANCE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.TYNDJ: BATTERY_SENSORS,
    DeviceCategory.VOC: (
        TuyaSensorEntityDescription(
            key=DPCode.CO2_VALUE,
            REDACTED_VALUE"carbon_dioxide",
            device_class=SensorDeviceClass.CO2,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.PM25_VALUE,
            REDACTED_VALUE"pm25",
            device_class=SensorDeviceClass.PM25,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CH2O_VALUE,
            REDACTED_VALUE"formaldehyde",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY_VALUE,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.VOC_VALUE,
            REDACTED_VALUE"voc",
            device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.WG2: (*BATTERY_SENSORS,),
    DeviceCategory.WK: (*BATTERY_SENSORS,),
    DeviceCategory.WKCZ: (
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY_VALUE,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUR_CURRENT,
            REDACTED_VALUE"current",
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            entity_registry_enabled_default=False,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUR_POWER,
            REDACTED_VALUE"power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            entity_registry_enabled_default=False,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUR_VOLTAGE,
            REDACTED_VALUE"voltage",
            device_class=SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=UnitOfElectricPotential.VOLT,
            entity_registry_enabled_default=False,
        ),
    ),
    DeviceCategory.WKF: BATTERY_SENSORS,
    DeviceCategory.WNYKQ: (
        TuyaSensorEntityDescription(
            key=DPCode.VA_TEMPERATURE,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.VA_HUMIDITY,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUR_CURRENT,
            REDACTED_VALUE"current",
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            entity_category=EntityCategory.DIAGNOSTIC,
            entity_registry_enabled_default=False,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUR_POWER,
            REDACTED_VALUE"power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            entity_category=EntityCategory.DIAGNOSTIC,
            entity_registry_enabled_default=False,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUR_VOLTAGE,
            REDACTED_VALUE"voltage",
            device_class=SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_unit_of_measurement=UnitOfElectricPotential.VOLT,
            entity_category=EntityCategory.DIAGNOSTIC,
            entity_registry_enabled_default=False,
        ),
    ),
    DeviceCategory.WSDCG: (
        TuyaSensorEntityDescription(
            key=DPCode.VA_TEMPERATURE,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.VA_HUMIDITY,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY_VALUE,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.BRIGHT_VALUE,
            REDACTED_VALUE"illuminance",
            device_class=SensorDeviceClass.ILLUMINANCE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.WXKG: BATTERY_SENSORS,
    DeviceCategory.XNYJCN: (
        TuyaSensorEntityDescription(
            key=DPCode.CURRENT_SOC,
            REDACTED_VALUE"battery_soc",
            device_class=SensorDeviceClass.BATTERY,
            state_class=SensorStateClass.MEASUREMENT,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.PV_POWER_TOTAL,
            REDACTED_VALUE"total_pv_power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.PV_POWER_CHANNEL_1,
            REDACTED_VALUE"pv_channel_power",
            translation_placeholders={"index": "1"},
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.PV_POWER_CHANNEL_2,
            REDACTED_VALUE"pv_channel_power",
            translation_placeholders={"index": "2"},
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.BATTERY_POWER,
            REDACTED_VALUE"battery_power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.INVERTER_OUTPUT_POWER,
            REDACTED_VALUE"inverter_output_power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUMULATIVE_ENERGY_GENERATED_PV,
            REDACTED_VALUE"lifetime_pv_energy",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUMULATIVE_ENERGY_OUTPUT_INV,
            REDACTED_VALUE"lifetime_inverter_output_energy",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUMULATIVE_ENERGY_DISCHARGED,
            REDACTED_VALUE"lifetime_battery_discharge_energy",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUMULATIVE_ENERGY_CHARGED,
            REDACTED_VALUE"lifetime_battery_charge_energy",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.CUML_E_EXPORT_OFFGRID1,
            REDACTED_VALUE"lifetime_offgrid_port_energy",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
    ),
    DeviceCategory.YLCG: (
        TuyaSensorEntityDescription(
            key=DPCode.PRESSURE_VALUE,
            name=None,
            device_class=SensorDeviceClass.PRESSURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.YWBJ: (
        TuyaSensorEntityDescription(
            key=DPCode.SMOKE_SENSOR_VALUE,
            REDACTED_VALUE"smoke_amount",
            entity_category=EntityCategory.DIAGNOSTIC,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        *BATTERY_SENSORS,
    ),
    DeviceCategory.YWCGQ: (
        TuyaSensorEntityDescription(
            key=DPCode.LIQUID_STATE,
            REDACTED_VALUE"liquid_state",
        ),
        TuyaSensorEntityDescription(
            key=DPCode.LIQUID_DEPTH,
            REDACTED_VALUE"depth",
            device_class=SensorDeviceClass.DISTANCE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.LIQUID_LEVEL_PERCENT,
            REDACTED_VALUE"liquid_level",
            state_class=SensorStateClass.MEASUREMENT,
        ),
    ),
    DeviceCategory.ZD: BATTERY_SENSORS,
    DeviceCategory.ZNDB: (
        TuyaSensorEntityDescription(
            key=DPCode.FORWARD_ENERGY_TOTAL,
            REDACTED_VALUE"total_energy",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.REVERSE_ENERGY_TOTAL,
            REDACTED_VALUE"total_production",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.POWER_TOTAL,
            REDACTED_VALUE"total_power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.TOTAL_POWER}power",
            dpcode=DPCode.TOTAL_POWER,
            REDACTED_VALUE"total_power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.SUPPLY_FREQUENCY,
            REDACTED_VALUE"supply_frequency",
            device_class=SensorDeviceClass.FREQUENCY,
            entity_category=EntityCategory.DIAGNOSTIC,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.PHASE_A}electriccurrent",
            dpcode=DPCode.PHASE_A,
            REDACTED_VALUE"phase_a_current",
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=CURRENT_WRAPPER,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.PHASE_A}power",
            dpcode=DPCode.PHASE_A,
            REDACTED_VALUE"phase_a_power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=POWER_WRAPPER,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.PHASE_A}voltage",
            dpcode=DPCode.PHASE_A,
            REDACTED_VALUE"phase_a_voltage",
            device_class=SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=VOLTAGE_WRAPPER,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.PHASE_B}electriccurrent",
            dpcode=DPCode.PHASE_B,
            REDACTED_VALUE"phase_b_current",
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=CURRENT_WRAPPER,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.PHASE_B}power",
            dpcode=DPCode.PHASE_B,
            REDACTED_VALUE"phase_b_power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=POWER_WRAPPER,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.PHASE_B}voltage",
            dpcode=DPCode.PHASE_B,
            REDACTED_VALUE"phase_b_voltage",
            device_class=SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=VOLTAGE_WRAPPER,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.PHASE_C}electriccurrent",
            dpcode=DPCode.PHASE_C,
            REDACTED_VALUE"phase_c_current",
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=CURRENT_WRAPPER,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.PHASE_C}power",
            dpcode=DPCode.PHASE_C,
            REDACTED_VALUE"phase_c_power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=POWER_WRAPPER,
        ),
        TuyaSensorEntityDescription(
            key=f"{DPCode.PHASE_C}voltage",
            dpcode=DPCode.PHASE_C,
            REDACTED_VALUE"phase_c_voltage",
            device_class=SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            wrapper_class=VOLTAGE_WRAPPER,
        ),
    ),
    DeviceCategory.ZNNBQ: (
        TuyaSensorEntityDescription(
            key=DPCode.REVERSE_ENERGY_TOTAL,
            REDACTED_VALUE"total_energy",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.POWER_TOTAL,
            REDACTED_VALUE"power",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            suggested_unit_of_measurement=UnitOfPower.WATT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
    ),
    DeviceCategory.ZNRB: (
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
    ),
    DeviceCategory.ZWJCY: (
        TuyaSensorEntityDescription(
            key=DPCode.TEMP_CURRENT,
            REDACTED_VALUE"temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        TuyaSensorEntityDescription(
            key=DPCode.HUMIDITY,
            REDACTED_VALUE"humidity",
            device_class=SensorDeviceClass.HUMIDITY,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        *BATTERY_SENSORS,
    ),
}

# Socket (duplicate of `kg`)
SENSORS[DeviceCategory.CZ] = SENSORS[DeviceCategory.KG]

# Smart Camera - Low power consumption camera (duplicate of `sp`)
SENSORS[DeviceCategory.DGHSXJ] = SENSORS[DeviceCategory.SP]

# Power Socket (duplicate of `kg`)
SENSORS[DeviceCategory.PC] = SENSORS[DeviceCategory.KG]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TuyaConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Tuya sensor dynamically through Tuya discovery."""
    manager = entry.runtime_data.manager

    @callback
    def async_discover_device(device_ids: list[str]) -> None:
        """Discover and add a discovered Tuya sensor."""
        entities: list[TuyaSensorEntity] = []
        for device_id in device_ids:
            device = manager.device_map[device_id]
            if descriptions := SENSORS.get(device.category):
                entities.extend(
                    TuyaSensorEntity(device, manager, description, definition)
                    for description in descriptions
                    if (
                        definition := get_default_definition(
                            device,
                            description.dpcode or description.key,
                            description.wrapper_class,
                        )
                    )
                )

        async_add_entities(entities)

    async_discover_device([*manager.device_map])

    entry.async_on_unload(
        async_dispatcher_connect(hass, TUYA_DISCOVERY_NEW, async_discover_device)
    )


class TuyaSensorEntity(TuyaEntity, SensorEntity):
    """Tuya Sensor Entity."""

    entity_description: TuyaSensorEntityDescription

    def __init__(
        self,
        device: CustomerDevice,
        device_manager: Manager,
        description: TuyaSensorEntityDescription,
        definition: SensorDefinition,
    ) -> None:
        """Init Tuya sensor."""
        super().__init__(device, device_manager, description)
        self._dpcode_wrapper = definition.sensor_wrapper

        if description.native_unit_of_measurement is None:
            self._attr_native_unit_of_measurement = (
                definition.sensor_wrapper.native_unit
            )
        if description.suggested_unit_of_measurement is None:
            self._attr_suggested_unit_of_measurement = (
                definition.sensor_wrapper.suggested_unit
            )
        if (
            description.device_class is None
            # For enum type DPs, we can assume it's an ENUM sensor
            and isinstance(definition.sensor_wrapper, DPCodeEnumWrapper)
        ):
            self._attr_device_class = SensorDeviceClass.ENUM
            self._attr_options = definition.sensor_wrapper.options
        if (
            description.state_class is None
            # For integer type DPs with "sum" report type, we can assume it's a total
            # increasing sensor
            and isinstance(definition.sensor_wrapper, DeltaIntegerWrapper)
        ):
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING

        self._validate_device_class_unit()

    def _validate_device_class_unit(self) -> None:
        """Validate device class unit compatibility."""

        # Logic to ensure the set device class and API received Unit Of Measurement
        # match Home Assistants requirements.
        if (
            self.device_class is not None
            and self.device_class != SensorDeviceClass.ENUM
            and not self.device_class.startswith(DOMAIN)
            and self.entity_description.native_unit_of_measurement is None
            # we do not need to check mappings if the API UOM is allowed
            and self.native_unit_of_measurement
            not in SENSOR_DEVICE_CLASS_UNITS[self.device_class]
        ):
            # We cannot have a device class, if the UOM isn't set or the
            # device class cannot be found in the validation mapping.
            if (
                self.native_unit_of_measurement is None
                or self.device_class not in DEVICE_CLASS_UNITS
            ):
                LOGGER.debug(
                    "Device class %s ignored for incompatible unit %s in sensor entity %s",
                    self.device_class,
                    self.native_unit_of_measurement,
                    self.unique_id,
                )
                self._attr_device_class = None
                self._attr_suggested_unit_of_measurement = None
                return

            uoms = DEVICE_CLASS_UNITS[self.device_class]
            uom = uoms.get(self.native_unit_of_measurement) or uoms.get(
                self.native_unit_of_measurement.lower()
            )

            # Unknown unit of measurement, device class should not be used.
            if uom is None:
                self._attr_device_class = None
                self._attr_suggested_unit_of_measurement = None
                return

            # Found unit of measurement, use the standardized Unit
            # Use the target conversion unit (if set)
            self._attr_native_unit_of_measurement = uom.unit

    @property
    def native_value(self) -> StateType:
        """Return the value reported by the sensor."""
        return self._read_wrapper(self._dpcode_wrapper)

    async def _process_device_update(
        self,
        updated_status_properties: list[str],
        dp_timestamps: dict[str, int] | None,
    ) -> bool:
        """Called when Tuya device sends an update with updated properties.

        Returns True if the Home Assistant state should be written,
        or False if the state write should be skipped.
        """
        return not self._dpcode_wrapper.skip_update(
            self.device, updated_status_properties, dp_timestamps
        )
