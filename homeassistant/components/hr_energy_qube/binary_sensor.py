"""Binary sensor platform for Qube Heat Pump."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory

from .coordinator import QubeData
from .entity import QubeEntity

PARALLEL_UPDATES = 0

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

    from . import QubeConfigEntry
    from .coordinator import QubeCoordinator


@dataclass(frozen=True, kw_only=True)
class QubeBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Binary sensor entity description for Qube Heat Pump."""

    value_fn: Callable[[QubeData], bool | None]


BINARY_SENSOR_TYPES: tuple[QubeBinarySensorEntityDescription, ...] = (
    # Outputs
    QubeBinarySensorEntityDescription(
        key="source_pump",
        REDACTED_VALUE"source_pump",
        value_fn=lambda data: data.state.dout_srcpmp_val,
    ),
    QubeBinarySensorEntityDescription(
        key="user_pump",
        REDACTED_VALUE"user_pump",
        value_fn=lambda data: data.state.dout_usrpmp_val,
    ),
    QubeBinarySensorEntityDescription(
        key="four_way_valve",
        REDACTED_VALUE"four_way_valve",
        value_fn=lambda data: data.state.dout_fourwayvlv_val,
    ),
    QubeBinarySensorEntityDescription(
        key="cooling_output",
        REDACTED_VALUE"cooling_output",
        value_fn=lambda data: data.state.dout_cooling_val,
    ),
    QubeBinarySensorEntityDescription(
        key="three_way_valve",
        REDACTED_VALUE"three_way_valve",
        value_fn=lambda data: data.state.dout_threewayvlv_val,
    ),
    QubeBinarySensorEntityDescription(
        key="buffer_pump",
        REDACTED_VALUE"buffer_pump",
        value_fn=lambda data: data.state.dout_bufferpmp_val,
    ),
    QubeBinarySensorEntityDescription(
        key="heater_step_1",
        REDACTED_VALUE"heater_step_1",
        value_fn=lambda data: data.state.dout_heaterstep1_val,
    ),
    QubeBinarySensorEntityDescription(
        key="heater_step_2",
        REDACTED_VALUE"heater_step_2",
        value_fn=lambda data: data.state.dout_heaterstep2_val,
    ),
    QubeBinarySensorEntityDescription(
        key="heater_step_3",
        REDACTED_VALUE"heater_step_3",
        value_fn=lambda data: data.state.dout_heaterstep3_val,
    ),
    # System status
    QubeBinarySensorEntityDescription(
        key="keypad",
        REDACTED_VALUE"keypad",
        value_fn=lambda data: data.state.keybonoff,
    ),
    QubeBinarySensorEntityDescription(
        key="day_mode",
        REDACTED_VALUE"day_mode",
        value_fn=lambda data: data.state.daynightmode,
    ),
    # Alarms
    QubeBinarySensorEntityDescription(
        key="alarm_antilegionella_timeout",
        REDACTED_VALUE"alarm_antilegionella_timeout",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.state.al_maxtime_antileg_active,
    ),
    QubeBinarySensorEntityDescription(
        key="alarm_dhw_timeout",
        REDACTED_VALUE"alarm_dhw_timeout",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.state.al_maxtime_dhw_active,
    ),
    QubeBinarySensorEntityDescription(
        key="alarm_dewpoint",
        REDACTED_VALUE"alarm_dewpoint",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.state.al_dewpoint_active,
    ),
    QubeBinarySensorEntityDescription(
        key="alarm_supply_too_hot",
        REDACTED_VALUE"alarm_supply_too_hot",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.state.al_underfloorsafety_active,
    ),
    QubeBinarySensorEntityDescription(
        key="alarm_flow",
        REDACTED_VALUE"alarm_flow",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.state.alrm_flw,
    ),
    QubeBinarySensorEntityDescription(
        key="alarm_central_heating",
        REDACTED_VALUE"alarm_central_heating",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.state.usralrms,
    ),
    QubeBinarySensorEntityDescription(
        key="alarm_cooling",
        REDACTED_VALUE"alarm_cooling",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.state.coolingalrms,
    ),
    QubeBinarySensorEntityDescription(
        key="alarm_heating",
        REDACTED_VALUE"alarm_heating",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.state.heatingalrms,
    ),
    QubeBinarySensorEntityDescription(
        key="alarm_working_hours",
        REDACTED_VALUE"alarm_working_hours",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.state.alarmmng_al_workinghour,
    ),
    QubeBinarySensorEntityDescription(
        key="alarm_source",
        REDACTED_VALUE"alarm_source",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.state.srsalrm,
    ),
    QubeBinarySensorEntityDescription(
        key="alarm_global",
        REDACTED_VALUE"alarm_global",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.state.glbal,
    ),
    QubeBinarySensorEntityDescription(
        key="alarm_compressor",
        REDACTED_VALUE"alarm_compressor",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.state.alarmmng_al_pwrplus,
    ),
    # Sensor/controller status
    QubeBinarySensorEntityDescription(
        key="room_sensor_enabled",
        REDACTED_VALUE"room_sensor_enabled",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda data: data.state.roomprb_en,
    ),
    QubeBinarySensorEntityDescription(
        key="plant_sensor_enabled",
        REDACTED_VALUE"plant_sensor_enabled",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda data: data.state.plantprb_en,
    ),
    QubeBinarySensorEntityDescription(
        key="buffer_sensor_enabled",
        REDACTED_VALUE"buffer_sensor_enabled",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda data: data.state.bufferprb_en,
    ),
    QubeBinarySensorEntityDescription(
        key="dhw_controller_enabled",
        REDACTED_VALUE"dhw_controller_enabled",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda data: data.state.en_dhwpid,
    ),
    # Demand signals
    QubeBinarySensorEntityDescription(
        key="plant_demand",
        REDACTED_VALUE"plant_demand",
        value_fn=lambda data: data.state.plantdemand,
    ),
    QubeBinarySensorEntityDescription(
        key="external_demand",
        REDACTED_VALUE"external_demand",
        value_fn=lambda data: data.state.id_demand,
    ),
    QubeBinarySensorEntityDescription(
        key="thermostat_demand",
        REDACTED_VALUE"thermostat_demand",
        value_fn=lambda data: data.state.thermostatdemand,
    ),
    # Digital inputs
    QubeBinarySensorEntityDescription(
        key="summer_mode",
        REDACTED_VALUE"summer_mode",
        value_fn=lambda data: data.state.id_summerwinter,
    ),
    QubeBinarySensorEntityDescription(
        key="dewpoint",
        REDACTED_VALUE"dewpoint",
        value_fn=lambda data: data.state.dewpoint,
    ),
    QubeBinarySensorEntityDescription(
        key="booster_security",
        REDACTED_VALUE"booster_security",
        value_fn=lambda data: data.state.boostersecurity,
    ),
    QubeBinarySensorEntityDescription(
        key="source_flow",
        REDACTED_VALUE"source_flow",
        value_fn=lambda data: data.state.srcflw,
    ),
    QubeBinarySensorEntityDescription(
        key="anti_legionella",
        REDACTED_VALUE"anti_legionella",
        value_fn=lambda data: data.state.req_antileg_1,
    ),
    # Energy
    QubeBinarySensorEntityDescription(
        key="pv_surplus",
        REDACTED_VALUE"pv_surplus",
        value_fn=lambda data: data.state.surplus_pv,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: QubeConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Qube binary sensors."""
    coordinator = entry.runtime_data.coordinator

    async_add_entities(
        QubeBinarySensor(coordinator, entry, description)
        for description in BINARY_SENSOR_TYPES
    )


class QubeBinarySensor(QubeEntity, BinarySensorEntity):
    """Qube binary sensor entity."""

    entity_description: QubeBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: QubeCoordinator,
        entry: QubeConfigEntry,
        description: QubeBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator, entry)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}-{description.key}"

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        return self.entity_description.value_fn(self.coordinator.data)
