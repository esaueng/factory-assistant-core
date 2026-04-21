"""Support for Tuya select."""

from __future__ import annotations

from tuya_device_handlers.definition.select import (
    TuyaSelectDefinition,
    get_default_definition,
)
from tuya_sharing import CustomerDevice, Manager

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import TUYA_DISCOVERY_NEW, DeviceCategory, DPCode
from .coordinator import TuyaConfigEntry
from .entity import TuyaEntity

# All descriptions can be found here. Mostly the Enum data types in the
# default instructions set of each category end up being a select.
SELECTS: dict[DeviceCategory, tuple[SelectEntityDescription, ...]] = {
    DeviceCategory.CL: (
        SelectEntityDescription(
            key=DPCode.CONTROL_BACK_MODE,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"curtain_motor_mode",
        ),
        SelectEntityDescription(
            key=DPCode.MODE,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"curtain_mode",
        ),
    ),
    DeviceCategory.CO2BJ: (
        SelectEntityDescription(
            key=DPCode.ALARM_VOLUME,
            REDACTED_VALUE"volume",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.CS: (
        SelectEntityDescription(
            key=DPCode.COUNTDOWN_SET,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"countdown",
        ),
        SelectEntityDescription(
            key=DPCode.DEHUMIDITY_SET_ENUM,
            REDACTED_VALUE"target_humidity",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.CWJWQ: (
        SelectEntityDescription(
            key=DPCode.WORK_MODE,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"odor_elimination_mode",
        ),
    ),
    DeviceCategory.DGNBJ: (
        SelectEntityDescription(
            key=DPCode.ALARM_VOLUME,
            REDACTED_VALUE"volume",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.DR: (
        SelectEntityDescription(
            key=DPCode.LEVEL,
            icon="mdi:thermometer-lines",
            REDACTED_VALUE"blanket_level",
        ),
        SelectEntityDescription(
            key=DPCode.LEVEL_1,
            icon="mdi:thermometer-lines",
            REDACTED_VALUE"indexed_blanket_level",
            translation_placeholders={"index": "1"},
        ),
        SelectEntityDescription(
            key=DPCode.LEVEL_2,
            icon="mdi:thermometer-lines",
            REDACTED_VALUE"indexed_blanket_level",
            translation_placeholders={"index": "2"},
        ),
    ),
    DeviceCategory.FS: (
        SelectEntityDescription(
            key=DPCode.FAN_VERTICAL,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"vertical_fan_angle",
        ),
        SelectEntityDescription(
            key=DPCode.FAN_HORIZONTAL,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"horizontal_fan_angle",
        ),
        SelectEntityDescription(
            key=DPCode.COUNTDOWN,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"countdown",
        ),
        SelectEntityDescription(
            key=DPCode.COUNTDOWN_SET,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"countdown",
        ),
    ),
    DeviceCategory.JSQ: (
        SelectEntityDescription(
            key=DPCode.SPRAY_MODE,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"humidifier_spray_mode",
        ),
        SelectEntityDescription(
            key=DPCode.LEVEL,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"humidifier_level",
        ),
        SelectEntityDescription(
            key=DPCode.MOODLIGHTING,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"humidifier_moodlighting",
        ),
        SelectEntityDescription(
            key=DPCode.COUNTDOWN,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"countdown",
        ),
        SelectEntityDescription(
            key=DPCode.COUNTDOWN_SET,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"countdown",
        ),
    ),
    DeviceCategory.KFJ: (
        SelectEntityDescription(
            key=DPCode.CUP_NUMBER,
            REDACTED_VALUE"cups",
        ),
        SelectEntityDescription(
            key=DPCode.CONCENTRATION_SET,
            REDACTED_VALUE"concentration",
            entity_category=EntityCategory.CONFIG,
        ),
        SelectEntityDescription(
            key=DPCode.MATERIAL,
            REDACTED_VALUE"material",
            entity_category=EntityCategory.CONFIG,
        ),
        SelectEntityDescription(
            key=DPCode.MODE,
            REDACTED_VALUE"mode",
        ),
    ),
    DeviceCategory.KG: (
        SelectEntityDescription(
            key=DPCode.RELAY_STATUS,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"relay_status",
        ),
        SelectEntityDescription(
            key=DPCode.LIGHT_MODE,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"light_mode",
        ),
    ),
    DeviceCategory.KJ: (
        SelectEntityDescription(
            key=DPCode.COUNTDOWN,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"countdown",
        ),
        SelectEntityDescription(
            key=DPCode.COUNTDOWN_SET,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"countdown",
        ),
    ),
    DeviceCategory.QN: (
        SelectEntityDescription(
            key=DPCode.LEVEL,
            REDACTED_VALUE"temperature_level",
        ),
    ),
    DeviceCategory.SD: (
        SelectEntityDescription(
            key=DPCode.CISTERN,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"vacuum_cistern",
        ),
        SelectEntityDescription(
            key=DPCode.COLLECTION_MODE,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"vacuum_collection",
        ),
        SelectEntityDescription(
            key=DPCode.MODE,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"vacuum_mode",
        ),
    ),
    DeviceCategory.SFKZQ: (
        # Irrigation will not be run within this set delay period
        SelectEntityDescription(
            key=DPCode.WEATHER_DELAY,
            REDACTED_VALUE"weather_delay",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.SGBJ: (
        SelectEntityDescription(
            key=DPCode.ALARM_STATE,
            REDACTED_VALUE"siren_mode",
            entity_category=EntityCategory.CONFIG,
        ),
        SelectEntityDescription(
            key=DPCode.ALARM_VOLUME,
            REDACTED_VALUE"volume",
            entity_category=EntityCategory.CONFIG,
        ),
        SelectEntityDescription(
            key=DPCode.BRIGHT_STATE,
            REDACTED_VALUE"brightness",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.SJZ: (
        SelectEntityDescription(
            key=DPCode.LEVEL,
            REDACTED_VALUE"desk_level",
            entity_category=EntityCategory.CONFIG,
        ),
        SelectEntityDescription(
            key=DPCode.UP_DOWN,
            REDACTED_VALUE"desk_up_down",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.SP: (
        SelectEntityDescription(
            key=DPCode.IPC_WORK_MODE,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"ipc_work_mode",
        ),
        SelectEntityDescription(
            key=DPCode.DECIBEL_SENSITIVITY,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"decibel_sensitivity",
        ),
        SelectEntityDescription(
            key=DPCode.RECORD_MODE,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"record_mode",
        ),
        SelectEntityDescription(
            key=DPCode.BASIC_NIGHTVISION,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"basic_nightvision",
        ),
        SelectEntityDescription(
            key=DPCode.BASIC_ANTI_FLICKER,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"basic_anti_flicker",
        ),
        SelectEntityDescription(
            key=DPCode.MOTION_SENSITIVITY,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"motion_sensitivity",
        ),
    ),
    DeviceCategory.SZJQR: (
        SelectEntityDescription(
            key=DPCode.MODE,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"fingerbot_mode",
        ),
    ),
    DeviceCategory.TDQ: (
        SelectEntityDescription(
            key=DPCode.RELAY_STATUS,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"relay_status",
        ),
        SelectEntityDescription(
            key=DPCode.LIGHT_MODE,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"light_mode",
        ),
    ),
    DeviceCategory.TGKG: (
        SelectEntityDescription(
            key=DPCode.RELAY_STATUS,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"relay_status",
        ),
        SelectEntityDescription(
            key=DPCode.LIGHT_MODE,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"light_mode",
        ),
        SelectEntityDescription(
            key=DPCode.LED_TYPE_1,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"indexed_led_type",
            translation_placeholders={"index": "1"},
        ),
        SelectEntityDescription(
            key=DPCode.LED_TYPE_2,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"indexed_led_type",
            translation_placeholders={"index": "2"},
        ),
        SelectEntityDescription(
            key=DPCode.LED_TYPE_3,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"indexed_led_type",
            translation_placeholders={"index": "3"},
        ),
    ),
    DeviceCategory.TGQ: (
        SelectEntityDescription(
            key=DPCode.LED_TYPE_1,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"indexed_led_type",
            translation_placeholders={"index": "1"},
        ),
        SelectEntityDescription(
            key=DPCode.LED_TYPE_2,
            entity_category=EntityCategory.CONFIG,
            REDACTED_VALUE"indexed_led_type",
            translation_placeholders={"index": "2"},
        ),
    ),
    DeviceCategory.XNYJCN: (
        SelectEntityDescription(
            key=DPCode.WORK_MODE,
            REDACTED_VALUE"inverter_work_mode",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
}

# Socket (duplicate of `kg`)
SELECTS[DeviceCategory.CZ] = SELECTS[DeviceCategory.KG]

# Smart Camera - Low power consumption camera (duplicate of `sp`)
SELECTS[DeviceCategory.DGHSXJ] = SELECTS[DeviceCategory.SP]

# Power Socket (duplicate of `kg`)
SELECTS[DeviceCategory.PC] = SELECTS[DeviceCategory.KG]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TuyaConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Tuya select dynamically through Tuya discovery."""
    manager = entry.runtime_data.manager

    @callback
    def async_discover_device(device_ids: list[str]) -> None:
        """Discover and add a discovered Tuya select."""
        entities: list[TuyaSelectEntity] = []
        for device_id in device_ids:
            device = manager.device_map[device_id]
            if descriptions := SELECTS.get(device.category):
                entities.extend(
                    TuyaSelectEntity(device, manager, description, definition)
                    for description in descriptions
                    if (definition := get_default_definition(device, description.key))
                )

        async_add_entities(entities)

    async_discover_device([*manager.device_map])

    entry.async_on_unload(
        async_dispatcher_connect(hass, TUYA_DISCOVERY_NEW, async_discover_device)
    )


class TuyaSelectEntity(TuyaEntity, SelectEntity):
    """Tuya Select Entity."""

    def __init__(
        self,
        device: CustomerDevice,
        device_manager: Manager,
        description: SelectEntityDescription,
        definition: TuyaSelectDefinition,
    ) -> None:
        """Initialize a Tuya select entity."""
        super().__init__(device, device_manager, description)
        self._dpcode_wrapper = definition.select_wrapper
        self._attr_options = definition.select_wrapper.options

    @property
    def current_option(self) -> str | None:
        """Return the selected entity option to represent the entity state."""
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

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        await self._async_send_wrapper_updates(self._dpcode_wrapper, option)
