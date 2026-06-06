"""Growatt Sensor definitions for Totals."""

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfEnergy, UnitOfPower

from .sensor_entity_description import GrowattSensorEntityDescription

TOTAL_SENSOR_TYPES: tuple[GrowattSensorEntityDescription, ...] = (
    GrowattSensorEntityDescription(
        key="total_money_today",
        REDACTED_VALUE"total_money_today",
        api_key="plantMoneyText",
        currency=True,
    ),
    GrowattSensorEntityDescription(
        key="total_money_total",
        REDACTED_VALUE"total_money_total",
        api_key="totalMoneyText",
        currency=True,
    ),
    GrowattSensorEntityDescription(
        key="total_energy_today",
        REDACTED_VALUE"total_energy_today",
        api_key="todayEnergy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    GrowattSensorEntityDescription(
        key="total_output_power",
        REDACTED_VALUE"total_output_power",
        api_key="invTodayPpv",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    GrowattSensorEntityDescription(
        key="total_energy_output",
        REDACTED_VALUE"total_energy_output",
        api_key="totalEnergy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
    ),
    GrowattSensorEntityDescription(
        key="total_maximum_output",
        REDACTED_VALUE"total_maximum_output",
        api_key="nominalPower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)
