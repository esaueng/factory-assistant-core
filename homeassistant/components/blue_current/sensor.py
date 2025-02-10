"""Support for Blue Current sensors."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    CURRENCY_EURO,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import BlueCurrentConfigEntry, Connector
from .const import DOMAIN
from .entity import BlueCurrentEntity, ChargepointEntity

SENSORS = (
    SensorEntityDescription(
        key="actual_v1",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        REDACTED_VALUE"actual_v1",
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="actual_v2",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        REDACTED_VALUE"actual_v2",
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="actual_v3",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        REDACTED_VALUE"actual_v3",
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="avg_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        REDACTED_VALUE"avg_voltage",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="actual_p1",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        REDACTED_VALUE"actual_p1",
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="actual_p2",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        REDACTED_VALUE"actual_p2",
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="actual_p3",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        REDACTED_VALUE"actual_p3",
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="avg_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        REDACTED_VALUE"avg_current",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="total_kw",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        REDACTED_VALUE"total_kw",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="actual_kwh",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        REDACTED_VALUE"actual_kwh",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="total_cost",
        native_unit_of_measurement=CURRENCY_EURO,
        device_class=SensorDeviceClass.MONETARY,
        REDACTED_VALUE"total_cost",
    ),
    SensorEntityDescription(
        key="vehicle_status",
        device_class=SensorDeviceClass.ENUM,
        options=["standby", "vehicle_detected", "ready", "no_power", "vehicle_error"],
        REDACTED_VALUE"vehicle_status",
    ),
    SensorEntityDescription(
        key="activity",
        device_class=SensorDeviceClass.ENUM,
        options=["available", "charging", "unavailable", "error", "offline"],
        REDACTED_VALUE"activity",
    ),
    SensorEntityDescription(
        key="max_usage",
        REDACTED_VALUE"max_usage",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="smartcharging_max_usage",
        REDACTED_VALUE"smartcharging_max_usage",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        entity_registry_enabled_default=False,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="max_offline",
        REDACTED_VALUE"max_offline",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        entity_registry_enabled_default=False,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="current_left",
        REDACTED_VALUE"current_left",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        entity_registry_enabled_default=False,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)

TIMESTAMP_SENSORS = (
    SensorEntityDescription(
        key="start_datetime",
        REDACTED_VALUE"start_datetime",
    ),
    SensorEntityDescription(
        key="stop_datetime",
        REDACTED_VALUE"stop_datetime",
    ),
    SensorEntityDescription(
        key="offline_since",
        REDACTED_VALUE"offline_since",
    ),
)

GRID_SENSORS = (
    SensorEntityDescription(
        key="grid_actual_p1",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        REDACTED_VALUE"grid_actual_p1",
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="grid_actual_p2",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        REDACTED_VALUE"grid_actual_p2",
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="grid_actual_p3",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        REDACTED_VALUE"grid_actual_p3",
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="grid_avg_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        REDACTED_VALUE"grid_avg_current",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="grid_max_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        REDACTED_VALUE"grid_max_current",
        state_class=SensorStateClass.MEASUREMENT,
    ),
)

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: HomeAssistant,
    entry: BlueCurrentConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Blue Current sensors."""
    connector = entry.runtime_data
    sensor_list: list[SensorEntity] = [
        ChargePointSensor(connector, sensor, evse_id)
        for evse_id in connector.charge_points
        for sensor in SENSORS
    ]

    sensor_list.extend(
        [
            ChargePointTimestampSensor(connector, sensor, evse_id)
            for evse_id in connector.charge_points
            for sensor in TIMESTAMP_SENSORS
        ]
    )

    sensor_list.extend(GridSensor(connector, sensor) for sensor in GRID_SENSORS)

    async_add_entities(sensor_list)


class ChargePointSensor(ChargepointEntity, SensorEntity):
    """Define a charge point sensor."""

    def __init__(
        self,
        connector: Connector,
        sensor: SensorEntityDescription,
        evse_id: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(connector, evse_id)

        self.key = sensor.key
        self.entity_description = sensor
        self._attr_unique_id = f"{sensor.key}_{evse_id}"

    @callback
    def update_from_latest_data(self) -> None:
        """Update the sensor from the latest data."""

        new_value = self.connector.charge_points[self.evse_id].get(self.key)

        if new_value is not None:
            self.has_value = True
            self._attr_native_value = new_value

        else:
            self.has_value = False


class ChargePointTimestampSensor(ChargePointSensor):
    """Define a timestamp sensor."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP

    @callback
    def update_from_latest_data(self) -> None:
        """Update the sensor from the latest data."""
        new_value = self.connector.charge_points[self.evse_id].get(self.key)

        # only update if the new_value is a newer timestamp.
        if new_value is not None and (
            self.has_value is False or self._attr_native_value < new_value
        ):
            self.has_value = True
            self._attr_native_value = new_value


class GridSensor(BlueCurrentEntity, SensorEntity):
    """Define a grid sensor."""

    def __init__(
        self,
        connector: Connector,
        sensor: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(connector, f"{DOMAIN}_grid_update")

        self.key = sensor.key
        self.entity_description = sensor
        self._attr_unique_id = sensor.key

    @callback
    def update_from_latest_data(self) -> None:
        """Update the grid sensor from the latest data."""

        new_value = self.connector.grid.get(self.key)

        if new_value is not None:
            self.has_value = True
            self._attr_native_value = new_value

        else:
            self.has_value = False
