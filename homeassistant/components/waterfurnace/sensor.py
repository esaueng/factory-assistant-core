"""Support for Waterfurnace."""

from __future__ import annotations

from homeassistant.components.sensor import (
    ENTITY_ID_FORMAT,
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, UnitOfPower, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import slugify

from . import DOMAIN, UPDATE_TOPIC, WaterFurnaceConfigEntry, WaterFurnaceData

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
]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: WaterFurnaceConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Waterfurnace sensors from a config entry."""

    data_collector = WaterFurnaceData(hass, config_entry.runtime_data)
    data_collector.start()

    async_add_entities(
        WaterFurnaceSensor(data_collector, description) for description in SENSORS
    )


class WaterFurnaceSensor(SensorEntity):
    """Implementing the Waterfurnace sensor."""

    _attr_should_poll = False
    _attr_has_entity_name = True

    def __init__(
        self, client: WaterFurnaceData, description: SensorEntityDescription
    ) -> None:
        """Initialize the sensor."""
        self.client = client
        self.entity_description = description

        # This ensures that the sensors are isolated per waterfurnace unit
        self.entity_id = ENTITY_ID_FORMAT.format(
            f"wf_{slugify(self.client.unit)}_{slugify(description.key)}"
        )
        self._attr_unique_id = f"{self.client.unit}_{description.key}"
        device_info = DeviceInfo(
            identifiers={(DOMAIN, self.client.unit)},
            manufacturer="WaterFurnace",
            name="WaterFurnace System",
        )

        if self.client.device_metadata:
            if self.client.device_metadata.description:
                # Eg. Series 7
                device_info["model"] = self.client.device_metadata.description
            if self.client.device_metadata.awlabctypedesc:
                # Eg. Series 7, 5 Ton
                device_info["name"] = self.client.device_metadata.awlabctypedesc

        self._attr_device_info = device_info

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, UPDATE_TOPIC, self.async_update_callback
            )
        )

    @callback
    def async_update_callback(self):
        """Update state."""
        if self.client.data is not None:
            self._attr_native_value = getattr(
                self.client.data, self.entity_description.key, None
            )
            self.async_write_ha_state()
