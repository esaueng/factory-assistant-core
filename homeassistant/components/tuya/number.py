"""Support for Tuya number."""

from tuya_device_handlers.definition.number import (
    NumberDefinition,
    get_default_definition,
)
from tuya_sharing import CustomerDevice, Manager

from homeassistant.components.number import (
    DEVICE_CLASS_UNITS as NUMBER_DEVICE_CLASS_UNITS,
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
)
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfTime
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

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

NUMBERS: dict[DeviceCategory, tuple[NumberEntityDescription, ...]] = {
    DeviceCategory.BH: (
        NumberEntityDescription(
            key=DPCode.TEMP_SET,
            REDACTED_VALUE"temperature",
            device_class=NumberDeviceClass.TEMPERATURE,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.TEMP_SET_F,
            REDACTED_VALUE"temperature",
            device_class=NumberDeviceClass.TEMPERATURE,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.TEMP_BOILING_C,
            REDACTED_VALUE"temperature_after_boiling",
            device_class=NumberDeviceClass.TEMPERATURE,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.TEMP_BOILING_F,
            REDACTED_VALUE"temperature_after_boiling",
            device_class=NumberDeviceClass.TEMPERATURE,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.WARM_TIME,
            REDACTED_VALUE"heat_preservation_time",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.BZYD: (
        NumberEntityDescription(
            key=DPCode.VOLUME_SET,
            REDACTED_VALUE"volume",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.CO2BJ: (
        NumberEntityDescription(
            key=DPCode.ALARM_TIME,
            REDACTED_VALUE"alarm_duration",
            native_unit_of_measurement=UnitOfTime.SECONDS,
            device_class=NumberDeviceClass.DURATION,
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.CWWSQ: (
        NumberEntityDescription(
            key=DPCode.MANUAL_FEED,
            REDACTED_VALUE"feed",
        ),
        NumberEntityDescription(
            key=DPCode.VOICE_TIMES,
            REDACTED_VALUE"voice_times",
        ),
    ),
    DeviceCategory.DGNBJ: (
        NumberEntityDescription(
            key=DPCode.ALARM_TIME,
            REDACTED_VALUE"time",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.FS: (
        NumberEntityDescription(
            key=DPCode.TEMP,
            REDACTED_VALUE"temperature",
            device_class=NumberDeviceClass.TEMPERATURE,
        ),
    ),
    DeviceCategory.HPS: (
        NumberEntityDescription(
            key=DPCode.SENSITIVITY,
            REDACTED_VALUE"sensitivity",
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.NEAR_DETECTION,
            REDACTED_VALUE"near_detection",
            device_class=NumberDeviceClass.DISTANCE,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.FAR_DETECTION,
            REDACTED_VALUE"far_detection",
            device_class=NumberDeviceClass.DISTANCE,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.TARGET_DIS_CLOSEST,
            REDACTED_VALUE"target_dis_closest",
            device_class=NumberDeviceClass.DISTANCE,
        ),
    ),
    DeviceCategory.JSQ: (
        NumberEntityDescription(
            key=DPCode.TEMP_SET,
            REDACTED_VALUE"temperature",
            device_class=NumberDeviceClass.TEMPERATURE,
        ),
        NumberEntityDescription(
            key=DPCode.TEMP_SET_F,
            REDACTED_VALUE"temperature",
            device_class=NumberDeviceClass.TEMPERATURE,
        ),
    ),
    DeviceCategory.KFJ: (
        NumberEntityDescription(
            key=DPCode.WATER_SET,
            REDACTED_VALUE"water_level",
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.TEMP_SET,
            REDACTED_VALUE"temperature",
            device_class=NumberDeviceClass.TEMPERATURE,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.WARM_TIME,
            REDACTED_VALUE"heat_preservation_time",
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.POWDER_SET,
            REDACTED_VALUE"powder",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.MAL: (
        NumberEntityDescription(
            key=DPCode.DELAY_SET,
            # This setting is called "Arm Delay" in the official Tuya app
            REDACTED_VALUE"arm_delay",
            device_class=NumberDeviceClass.DURATION,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.ALARM_DELAY_TIME,
            REDACTED_VALUE"alarm_delay",
            device_class=NumberDeviceClass.DURATION,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.ALARM_TIME,
            # This setting is called "Siren Duration" in the official Tuya app
            REDACTED_VALUE"siren_duration",
            device_class=NumberDeviceClass.DURATION,
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.MSP: (
        NumberEntityDescription(
            key=DPCode.DELAY_CLEAN_TIME,
            REDACTED_VALUE"delay_clean_time",
            device_class=NumberDeviceClass.DURATION,
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.MZJ: (
        NumberEntityDescription(
            key=DPCode.COOK_TEMPERATURE,
            REDACTED_VALUE"cook_temperature",
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.COOK_TIME,
            REDACTED_VALUE"cook_time",
            native_unit_of_measurement=UnitOfTime.MINUTES,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.CLOUD_RECIPE_NUMBER,
            REDACTED_VALUE"cloud_recipe",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.SWTZ: (
        NumberEntityDescription(
            key=DPCode.COOK_TEMPERATURE,
            REDACTED_VALUE"cook_temperature",
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.COOK_TEMPERATURE_2,
            REDACTED_VALUE"indexed_cook_temperature",
            translation_placeholders={"index": "2"},
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.SD: (
        NumberEntityDescription(
            key=DPCode.VOLUME_SET,
            REDACTED_VALUE"volume",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.SFKZQ: (
        # Controls the irrigation duration for indexed water valves
        NumberEntityDescription(
            key=DPCode.COUNTDOWN_1,
            REDACTED_VALUE"indexed_irrigation_duration",
            translation_placeholders={"index": "1"},
            device_class=NumberDeviceClass.DURATION,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.COUNTDOWN_2,
            REDACTED_VALUE"indexed_irrigation_duration",
            translation_placeholders={"index": "2"},
            device_class=NumberDeviceClass.DURATION,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.COUNTDOWN_3,
            REDACTED_VALUE"indexed_irrigation_duration",
            translation_placeholders={"index": "3"},
            device_class=NumberDeviceClass.DURATION,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.COUNTDOWN_4,
            REDACTED_VALUE"indexed_irrigation_duration",
            translation_placeholders={"index": "4"},
            device_class=NumberDeviceClass.DURATION,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.COUNTDOWN_5,
            REDACTED_VALUE"indexed_irrigation_duration",
            translation_placeholders={"index": "5"},
            device_class=NumberDeviceClass.DURATION,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.COUNTDOWN_6,
            REDACTED_VALUE"indexed_irrigation_duration",
            translation_placeholders={"index": "6"},
            device_class=NumberDeviceClass.DURATION,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.COUNTDOWN_7,
            REDACTED_VALUE"indexed_irrigation_duration",
            translation_placeholders={"index": "7"},
            device_class=NumberDeviceClass.DURATION,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.COUNTDOWN_8,
            REDACTED_VALUE"indexed_irrigation_duration",
            translation_placeholders={"index": "8"},
            device_class=NumberDeviceClass.DURATION,
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.SGBJ: (
        NumberEntityDescription(
            key=DPCode.ALARM_TIME,
            REDACTED_VALUE"time",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.SP: (
        NumberEntityDescription(
            key=DPCode.BASIC_DEVICE_VOLUME,
            REDACTED_VALUE"volume",
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.IPC_BRIGHT,
            REDACTED_VALUE"video_brightness",
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.IPC_CONTRAST,
            REDACTED_VALUE"video_contrast",
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.IPC_SHARP,
            REDACTED_VALUE"video_sharpness",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.SZJQR: (
        NumberEntityDescription(
            key=DPCode.ARM_DOWN_PERCENT,
            REDACTED_VALUE"move_down",
            native_unit_of_measurement=PERCENTAGE,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.ARM_UP_PERCENT,
            REDACTED_VALUE"move_up",
            native_unit_of_measurement=PERCENTAGE,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.CLICK_SUSTAIN_TIME,
            REDACTED_VALUE"down_delay",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.TGKG: (
        NumberEntityDescription(
            key=DPCode.BRIGHTNESS_MIN_1,
            REDACTED_VALUE"indexed_minimum_brightness",
            translation_placeholders={"index": "1"},
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.BRIGHTNESS_MAX_1,
            REDACTED_VALUE"indexed_maximum_brightness",
            translation_placeholders={"index": "1"},
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.BRIGHTNESS_MIN_2,
            REDACTED_VALUE"indexed_minimum_brightness",
            translation_placeholders={"index": "2"},
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.BRIGHTNESS_MAX_2,
            REDACTED_VALUE"indexed_maximum_brightness",
            translation_placeholders={"index": "2"},
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.BRIGHTNESS_MIN_3,
            REDACTED_VALUE"indexed_minimum_brightness",
            translation_placeholders={"index": "3"},
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.BRIGHTNESS_MAX_3,
            REDACTED_VALUE"indexed_maximum_brightness",
            translation_placeholders={"index": "3"},
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.TGQ: (
        NumberEntityDescription(
            key=DPCode.BRIGHTNESS_MIN_1,
            REDACTED_VALUE"indexed_minimum_brightness",
            translation_placeholders={"index": "1"},
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.BRIGHTNESS_MAX_1,
            REDACTED_VALUE"indexed_maximum_brightness",
            translation_placeholders={"index": "1"},
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.BRIGHTNESS_MIN_2,
            REDACTED_VALUE"indexed_minimum_brightness",
            translation_placeholders={"index": "2"},
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.BRIGHTNESS_MAX_2,
            REDACTED_VALUE"indexed_maximum_brightness",
            translation_placeholders={"index": "2"},
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.WK: (
        NumberEntityDescription(
            key=DPCode.TEMP_CORRECTION,
            REDACTED_VALUE"temp_correction",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.XNYJCN: (
        NumberEntityDescription(
            key=DPCode.BACKUP_RESERVE,
            REDACTED_VALUE"battery_backup_reserve",
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.OUTPUT_POWER_LIMIT,
            REDACTED_VALUE"inverter_output_power_limit",
            device_class=NumberDeviceClass.POWER,
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.YWCGQ: (
        NumberEntityDescription(
            key=DPCode.MAX_SET,
            REDACTED_VALUE"alarm_maximum",
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.MINI_SET,
            REDACTED_VALUE"alarm_minimum",
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.INSTALLATION_HEIGHT,
            REDACTED_VALUE"installation_height",
            device_class=NumberDeviceClass.DISTANCE,
            entity_category=EntityCategory.CONFIG,
        ),
        NumberEntityDescription(
            key=DPCode.LIQUID_DEPTH_MAX,
            REDACTED_VALUE"maximum_liquid_depth",
            device_class=NumberDeviceClass.DISTANCE,
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.ZD: (
        NumberEntityDescription(
            key=DPCode.SENSITIVITY,
            REDACTED_VALUE"sensitivity",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.ZNRB: (
        NumberEntityDescription(
            key=DPCode.TEMP_SET,
            REDACTED_VALUE"temperature",
            device_class=NumberDeviceClass.TEMPERATURE,
        ),
    ),
}

# Smart Camera - Low power consumption camera (duplicate of `sp`)
NUMBERS[DeviceCategory.DGHSXJ] = NUMBERS[DeviceCategory.SP]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TuyaConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Tuya number dynamically through Tuya discovery."""
    manager = entry.runtime_data.manager

    @callback
    def async_discover_device(device_ids: list[str]) -> None:
        """Discover and add a discovered Tuya number."""
        entities: list[TuyaNumberEntity] = []
        for device_id in device_ids:
            device = manager.device_map[device_id]
            if descriptions := NUMBERS.get(device.category):
                entities.extend(
                    TuyaNumberEntity(device, manager, description, definition)
                    for description in descriptions
                    if (definition := get_default_definition(device, description.key))
                )

        async_add_entities(entities)

    async_discover_device([*manager.device_map])

    entry.async_on_unload(
        async_dispatcher_connect(hass, TUYA_DISCOVERY_NEW, async_discover_device)
    )


class TuyaNumberEntity(TuyaEntity, NumberEntity):
    """Tuya Number Entity."""

    def __init__(
        self,
        device: CustomerDevice,
        device_manager: Manager,
        description: NumberEntityDescription,
        definition: NumberDefinition,
    ) -> None:
        """Initialize a Tuya number entity."""
        super().__init__(device, device_manager, description)
        self._dpcode_wrapper = definition.number_wrapper

        self._attr_native_max_value = definition.number_wrapper.max_value
        self._attr_native_min_value = definition.number_wrapper.min_value
        self._attr_native_step = definition.number_wrapper.value_step
        if description.native_unit_of_measurement is None:
            self._attr_native_unit_of_measurement = (
                definition.number_wrapper.native_unit
            )

        self._validate_device_class_unit()

    def _validate_device_class_unit(self) -> None:
        """Validate device class unit compatibility."""

        # Logic to ensure the set device class and API received Unit Of Measurement
        # match Home Assistants requirements.
        if (
            self.device_class is not None
            and not self.device_class.startswith(DOMAIN)
            and self.entity_description.native_unit_of_measurement is None
            # we do not need to check mappings if the API UOM is allowed
            and self.native_unit_of_measurement
            not in NUMBER_DEVICE_CLASS_UNITS[self.device_class]
        ):
            # We cannot have a device class, if the UOM isn't set or the
            # device class cannot be found in the validation mapping.
            if (
                self.native_unit_of_measurement is None
                or self.device_class not in DEVICE_CLASS_UNITS
            ):
                LOGGER.debug(
                    "Device class %s ignored for incompatible unit %s in number entity %s",
                    self.device_class,
                    self.native_unit_of_measurement,
                    self.unique_id,
                )
                self._attr_device_class = None
                return

            uoms = DEVICE_CLASS_UNITS[self.device_class]
            uom = uoms.get(self.native_unit_of_measurement) or uoms.get(
                self.native_unit_of_measurement.lower()
            )

            # Unknown unit of measurement, device class should not be used.
            if uom is None:
                self._attr_device_class = None
                return

            # Found unit of measurement, use the standardized Unit
            # Use the target conversion unit (if set)
            self._attr_native_unit_of_measurement = uom.unit

    @property
    def native_value(self) -> float | None:
        """Return the entity value to represent the entity state."""
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

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        await self._async_send_wrapper_updates(self._dpcode_wrapper, value)
