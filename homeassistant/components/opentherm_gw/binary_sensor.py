"""Support for OpenTherm Gateway binary sensors."""

from dataclasses import dataclass

from pyotgw import vars as gw_vars

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ID, EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    BOILER_DEVICE_DESCRIPTION,
    DATA_GATEWAYS,
    DATA_OPENTHERM_GW,
    GATEWAY_DEVICE_DESCRIPTION,
    THERMOSTAT_DEVICE_DESCRIPTION,
    OpenThermDataSource,
)
from .entity import OpenThermEntityDescription, OpenThermStatusEntity


@dataclass(frozen=True, kw_only=True)
class OpenThermBinarySensorEntityDescription(
    OpenThermEntityDescription, BinarySensorEntityDescription
):
    """Describes opentherm_gw binary sensor entity."""


BINARY_SENSOR_DESCRIPTIONS: tuple[OpenThermBinarySensorEntityDescription, ...] = (
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_FAULT_IND,
        REDACTED_VALUE"fault_indication",
        device_class=BinarySensorDeviceClass.PROBLEM,
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_CH_ACTIVE,
        REDACTED_VALUE"central_heating_n",
        translation_placeholders={"circuit_number": "1"},
        device_class=BinarySensorDeviceClass.RUNNING,
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_CH2_ACTIVE,
        REDACTED_VALUE"central_heating_n",
        translation_placeholders={"circuit_number": "2"},
        device_class=BinarySensorDeviceClass.RUNNING,
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_DHW_ACTIVE,
        REDACTED_VALUE"hot_water",
        device_class=BinarySensorDeviceClass.RUNNING,
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_FLAME_ON,
        REDACTED_VALUE"flame",
        device_class=BinarySensorDeviceClass.HEAT,
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_COOLING_ACTIVE,
        REDACTED_VALUE"cooling",
        device_class=BinarySensorDeviceClass.RUNNING,
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_DIAG_IND,
        REDACTED_VALUE"diagnostic_indication",
        device_class=BinarySensorDeviceClass.PROBLEM,
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_DHW_PRESENT,
        REDACTED_VALUE"supports_hot_water",
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_CONTROL_TYPE,
        REDACTED_VALUE"control_type",
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_COOLING_SUPPORTED,
        REDACTED_VALUE"supports_cooling",
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_DHW_CONFIG,
        REDACTED_VALUE"hot_water_config",
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_MASTER_LOW_OFF_PUMP,
        REDACTED_VALUE"supports_pump_control",
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_CH2_PRESENT,
        REDACTED_VALUE"supports_ch_2",
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_SERVICE_REQ,
        REDACTED_VALUE"service_required",
        device_class=BinarySensorDeviceClass.PROBLEM,
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_REMOTE_RESET,
        REDACTED_VALUE"supports_remote_reset",
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_LOW_WATER_PRESS,
        REDACTED_VALUE"low_water_pressure",
        device_class=BinarySensorDeviceClass.PROBLEM,
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_GAS_FAULT,
        REDACTED_VALUE"gas_fault",
        device_class=BinarySensorDeviceClass.PROBLEM,
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_AIR_PRESS_FAULT,
        REDACTED_VALUE"air_pressure_fault",
        device_class=BinarySensorDeviceClass.PROBLEM,
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_WATER_OVERTEMP,
        REDACTED_VALUE"water_overtemperature",
        device_class=BinarySensorDeviceClass.PROBLEM,
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_REMOTE_TRANSFER_MAX_CH,
        REDACTED_VALUE"supports_central_heating_setpoint_transfer",
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_REMOTE_RW_MAX_CH,
        REDACTED_VALUE"supports_central_heating_setpoint_writing",
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_REMOTE_TRANSFER_DHW,
        REDACTED_VALUE"supports_hot_water_setpoint_transfer",
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_REMOTE_RW_DHW,
        REDACTED_VALUE"supports_hot_water_setpoint_writing",
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.OTGW_GPIO_A_STATE,
        REDACTED_VALUE"gpio_state_n",
        translation_placeholders={"gpio_id": "A"},
        device_description=GATEWAY_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.OTGW_GPIO_B_STATE,
        REDACTED_VALUE"gpio_state_n",
        translation_placeholders={"gpio_id": "B"},
        device_description=GATEWAY_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.OTGW_IGNORE_TRANSITIONS,
        REDACTED_VALUE"ignore_transitions",
        device_description=GATEWAY_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.OTGW_OVRD_HB,
        REDACTED_VALUE"override_high_byte",
        device_description=GATEWAY_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_MASTER_CH_ENABLED,
        REDACTED_VALUE"central_heating_n",
        translation_placeholders={"circuit_number": "1"},
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_MASTER_CH2_ENABLED,
        REDACTED_VALUE"central_heating_n",
        translation_placeholders={"circuit_number": "2"},
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_MASTER_DHW_ENABLED,
        REDACTED_VALUE"hot_water",
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_MASTER_COOLING_ENABLED,
        REDACTED_VALUE"cooling",
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_MASTER_OTC_ENABLED,
        REDACTED_VALUE"outside_temp_correction",
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_ROVRD_MAN_PRIO,
        REDACTED_VALUE"override_manual_change_prio",
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_ROVRD_AUTO_PRIO,
        REDACTED_VALUE"override_program_change_prio",
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_FAULT_IND,
        REDACTED_VALUE"fault_indication",
        device_class=BinarySensorDeviceClass.PROBLEM,
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_CH_ACTIVE,
        REDACTED_VALUE"central_heating_n",
        translation_placeholders={"circuit_number": "1"},
        device_class=BinarySensorDeviceClass.RUNNING,
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_CH2_ACTIVE,
        REDACTED_VALUE"central_heating_n",
        translation_placeholders={"circuit_number": "2"},
        device_class=BinarySensorDeviceClass.RUNNING,
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_DHW_ACTIVE,
        REDACTED_VALUE"hot_water",
        device_class=BinarySensorDeviceClass.RUNNING,
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_FLAME_ON,
        REDACTED_VALUE"flame",
        device_class=BinarySensorDeviceClass.HEAT,
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_COOLING_ACTIVE,
        REDACTED_VALUE"cooling",
        device_class=BinarySensorDeviceClass.RUNNING,
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_DIAG_IND,
        REDACTED_VALUE"diagnostic_indication",
        device_class=BinarySensorDeviceClass.PROBLEM,
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_DHW_PRESENT,
        REDACTED_VALUE"supports_hot_water",
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_CONTROL_TYPE,
        REDACTED_VALUE"control_type",
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_COOLING_SUPPORTED,
        REDACTED_VALUE"supports_cooling",
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_DHW_CONFIG,
        REDACTED_VALUE"hot_water_config",
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_MASTER_LOW_OFF_PUMP,
        REDACTED_VALUE"supports_pump_control",
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_CH2_PRESENT,
        REDACTED_VALUE"supports_ch_2",
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_SERVICE_REQ,
        REDACTED_VALUE"service_required",
        device_class=BinarySensorDeviceClass.PROBLEM,
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_REMOTE_RESET,
        REDACTED_VALUE"supports_remote_reset",
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_LOW_WATER_PRESS,
        REDACTED_VALUE"low_water_pressure",
        device_class=BinarySensorDeviceClass.PROBLEM,
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_GAS_FAULT,
        REDACTED_VALUE"gas_fault",
        device_class=BinarySensorDeviceClass.PROBLEM,
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_AIR_PRESS_FAULT,
        REDACTED_VALUE"air_pressure_fault",
        device_class=BinarySensorDeviceClass.PROBLEM,
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_SLAVE_WATER_OVERTEMP,
        REDACTED_VALUE"water_overtemperature",
        device_class=BinarySensorDeviceClass.PROBLEM,
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_REMOTE_TRANSFER_MAX_CH,
        REDACTED_VALUE"supports_central_heating_setpoint_transfer",
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_REMOTE_RW_MAX_CH,
        REDACTED_VALUE"supports_central_heating_setpoint_writing",
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_REMOTE_TRANSFER_DHW,
        REDACTED_VALUE"supports_hot_water_setpoint_transfer",
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_REMOTE_RW_DHW,
        REDACTED_VALUE"supports_hot_water_setpoint_writing",
        device_description=THERMOSTAT_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_MASTER_CH_ENABLED,
        REDACTED_VALUE"central_heating_n",
        translation_placeholders={"circuit_number": "1"},
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_MASTER_CH2_ENABLED,
        REDACTED_VALUE"central_heating_n",
        translation_placeholders={"circuit_number": "2"},
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_MASTER_DHW_ENABLED,
        REDACTED_VALUE"hot_water",
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_MASTER_COOLING_ENABLED,
        REDACTED_VALUE"cooling",
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_MASTER_OTC_ENABLED,
        REDACTED_VALUE"outside_temp_correction",
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_ROVRD_MAN_PRIO,
        REDACTED_VALUE"override_manual_change_prio",
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
    OpenThermBinarySensorEntityDescription(
        key=gw_vars.DATA_ROVRD_AUTO_PRIO,
        REDACTED_VALUE"override_program_change_prio",
        device_description=BOILER_DEVICE_DESCRIPTION,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the OpenTherm Gateway binary sensors."""
    gw_hub = hass.data[DATA_OPENTHERM_GW][DATA_GATEWAYS][config_entry.data[CONF_ID]]

    async_add_entities(
        OpenThermBinarySensor(gw_hub, description)
        for description in BINARY_SENSOR_DESCRIPTIONS
    )


class OpenThermBinarySensor(OpenThermStatusEntity, BinarySensorEntity):
    """Represent an OpenTherm Gateway binary sensor."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    entity_description: OpenThermBinarySensorEntityDescription

    @callback
    def receive_report(self, status: dict[OpenThermDataSource, dict]) -> None:
        """Handle status updates from the component."""
        state = status[self.entity_description.device_description.data_source].get(
            self.entity_description.key
        )
        self._attr_is_on = None if state is None else bool(state)
        self.async_write_ha_state()
