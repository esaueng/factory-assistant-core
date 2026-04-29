"""Support for Waterfurnace."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfVolumeFlowRate,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import WaterFurnaceConfigEntry
from .coordinator import WaterFurnaceCoordinator
from .entity import WaterFurnaceEntity

SENSORS = [
    SensorEntityDescription(
        key="mode",
        REDACTED_VALUE"mode",
    ),
    SensorEntityDescription(
        key="totalunitpower",
        REDACTED_VALUE"total_unit_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="tstatactivesetpoint",
        REDACTED_VALUE"tstat_active_setpoint",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="leavingairtemp",
        REDACTED_VALUE"leaving_air_temp",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="tstatroomtemp",
        REDACTED_VALUE"room_temp",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="enteringwatertemp",
        REDACTED_VALUE"entering_water_temp",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="tstathumidsetpoint",
        REDACTED_VALUE"tstat_humid_setpoint",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="tstatrelativehumidity",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="compressorpower",
        REDACTED_VALUE"compressor_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="fanpower",
        REDACTED_VALUE"fan_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="auxpower",
        REDACTED_VALUE"aux_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="looppumppower",
        REDACTED_VALUE"loop_pump_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="actualcompressorspeed",
        REDACTED_VALUE"actual_compressor_speed",
    ),
    SensorEntityDescription(
        key="airflowcurrentspeed",
        REDACTED_VALUE"airflow_current_speed",
    ),
    SensorEntityDescription(
        key="tstatdehumidsetpoint",
        REDACTED_VALUE"tstat_dehumid_setpoint",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="leavingwatertemp",
        REDACTED_VALUE"leaving_water_temp",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="tstatheatingsetpoint",
        REDACTED_VALUE"tstat_heating_setpoint",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="tstatcoolingsetpoint",
        REDACTED_VALUE"tstat_cooling_setpoint",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="waterflowrate",
        REDACTED_VALUE"water_flow_rate",
        native_unit_of_measurement=UnitOfVolumeFlowRate.GALLONS_PER_MINUTE,
        device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: WaterFurnaceConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Waterfurnace sensors from a config entry."""
    async_add_entities(
        WaterFurnaceSensor(device_data.realtime, description)
        for device_data in config_entry.runtime_data.values()
        for description in SENSORS
    )


class WaterFurnaceSensor(WaterFurnaceEntity, SensorEntity):
    """Implementing the Waterfurnace sensor."""

    entity_description: SensorEntityDescription
    _attr_should_poll = False

    def __init__(
        self, coordinator: WaterFurnaceCoordinator, description: SensorEntityDescription
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.unit}_{description.key}"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return getattr(self.coordinator.data, self.entity_description.key, None)
