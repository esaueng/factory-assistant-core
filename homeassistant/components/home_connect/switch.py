"""Provides a switch for Home Connect."""

import logging
from typing import Any, cast

from aiohomeconnect.model import OptionKey, SettingKey
from aiohomeconnect.model.error import HomeConnectError

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import UNDEFINED, UndefinedType

from .common import setup_home_connect_entry, should_add_option_entity
from .const import BSH_POWER_OFF, BSH_POWER_ON, BSH_POWER_STANDBY, DOMAIN
from .coordinator import HomeConnectApplianceCoordinator, HomeConnectConfigEntry
from .entity import HomeConnectEntity, HomeConnectOptionEntity
from .utils import get_dict_from_home_connect_error

_LOGGER = logging.getLogger(__name__)

PARALLEL_UPDATES = 1

SWITCHES = (
    SwitchEntityDescription(
        key=SettingKey.BSH_COMMON_CHILD_LOCK,
        REDACTED_VALUE"child_lock",
    ),
    SwitchEntityDescription(
        key=SettingKey.CONSUMER_PRODUCTS_COFFEE_MAKER_CUP_WARMER,
        REDACTED_VALUE"cup_warmer",
    ),
    SwitchEntityDescription(
        key=SettingKey.REFRIGERATION_FRIDGE_FREEZER_SUPER_MODE_FREEZER,
        REDACTED_VALUE"freezer_super_mode",
    ),
    SwitchEntityDescription(
        key=SettingKey.REFRIGERATION_FRIDGE_FREEZER_SUPER_MODE_REFRIGERATOR,
        REDACTED_VALUE"refrigerator_super_mode",
    ),
    SwitchEntityDescription(
        key=SettingKey.REFRIGERATION_COMMON_ECO_MODE,
        REDACTED_VALUE"eco_mode",
    ),
    SwitchEntityDescription(
        key=SettingKey.COOKING_OVEN_SABBATH_MODE,
        REDACTED_VALUE"sabbath_mode",
    ),
    SwitchEntityDescription(
        key=SettingKey.REFRIGERATION_COMMON_SABBATH_MODE,
        REDACTED_VALUE"sabbath_mode",
    ),
    SwitchEntityDescription(
        key=SettingKey.REFRIGERATION_COMMON_VACATION_MODE,
        REDACTED_VALUE"vacation_mode",
    ),
    SwitchEntityDescription(
        key=SettingKey.REFRIGERATION_COMMON_FRESH_MODE,
        REDACTED_VALUE"fresh_mode",
    ),
    SwitchEntityDescription(
        key=SettingKey.REFRIGERATION_COMMON_DISPENSER_ENABLED,
        REDACTED_VALUE"dispenser_enabled",
    ),
    SwitchEntityDescription(
        key=SettingKey.REFRIGERATION_COMMON_DOOR_ASSISTANT_FRIDGE,
        REDACTED_VALUE"door_assistant_fridge",
    ),
    SwitchEntityDescription(
        key=SettingKey.REFRIGERATION_COMMON_DOOR_ASSISTANT_FREEZER,
        REDACTED_VALUE"door_assistant_freezer",
    ),
)


POWER_SWITCH_DESCRIPTION = SwitchEntityDescription(
    key=SettingKey.BSH_COMMON_POWER_STATE,
    REDACTED_VALUE"power",
)

SWITCH_OPTIONS = (
    SwitchEntityDescription(
        key=OptionKey.CONSUMER_PRODUCTS_COFFEE_MAKER_MULTIPLE_BEVERAGES,
        REDACTED_VALUE"multiple_beverages",
    ),
    SwitchEntityDescription(
        key=OptionKey.DISHCARE_DISHWASHER_INTENSIV_ZONE,
        REDACTED_VALUE"intensiv_zone",
    ),
    SwitchEntityDescription(
        key=OptionKey.DISHCARE_DISHWASHER_BRILLIANCE_DRY,
        REDACTED_VALUE"brilliance_dry",
    ),
    SwitchEntityDescription(
        key=OptionKey.DISHCARE_DISHWASHER_VARIO_SPEED_PLUS,
        REDACTED_VALUE"vario_speed_plus",
    ),
    SwitchEntityDescription(
        key=OptionKey.DISHCARE_DISHWASHER_SILENCE_ON_DEMAND,
        REDACTED_VALUE"silence_on_demand",
    ),
    SwitchEntityDescription(
        key=OptionKey.DISHCARE_DISHWASHER_HALF_LOAD,
        REDACTED_VALUE"half_load",
    ),
    SwitchEntityDescription(
        key=OptionKey.DISHCARE_DISHWASHER_EXTRA_DRY,
        REDACTED_VALUE"extra_dry",
    ),
    SwitchEntityDescription(
        key=OptionKey.DISHCARE_DISHWASHER_HYGIENE_PLUS,
        REDACTED_VALUE"hygiene_plus",
    ),
    SwitchEntityDescription(
        key=OptionKey.DISHCARE_DISHWASHER_ECO_DRY,
        REDACTED_VALUE"eco_dry",
    ),
    SwitchEntityDescription(
        key=OptionKey.DISHCARE_DISHWASHER_ZEOLITE_DRY,
        REDACTED_VALUE"zeolite_dry",
    ),
    SwitchEntityDescription(
        key=OptionKey.COOKING_OVEN_FAST_PRE_HEAT,
        REDACTED_VALUE"fast_pre_heat",
    ),
    SwitchEntityDescription(
        key=OptionKey.LAUNDRY_CARE_COMMON_SILENT_MODE,
        REDACTED_VALUE"silent_mode",
    ),
    SwitchEntityDescription(
        key=OptionKey.LAUNDRY_CARE_WASHER_I_DOS_1_ACTIVE,
        REDACTED_VALUE"i_dos1_active",
    ),
    SwitchEntityDescription(
        key=OptionKey.LAUNDRY_CARE_WASHER_I_DOS_2_ACTIVE,
        REDACTED_VALUE"i_dos2_active",
    ),
    SwitchEntityDescription(
        key=OptionKey.LAUNDRY_CARE_WASHER_INTENSIVE_PLUS,
        REDACTED_VALUE"intensive_plus",
    ),
    SwitchEntityDescription(
        key=OptionKey.LAUNDRY_CARE_WASHER_LESS_IRONING,
        REDACTED_VALUE"less_ironing",
    ),
    SwitchEntityDescription(
        key=OptionKey.LAUNDRY_CARE_WASHER_MINI_LOAD,
        REDACTED_VALUE"mini_load",
    ),
    SwitchEntityDescription(
        key=OptionKey.LAUNDRY_CARE_WASHER_PREWASH,
        REDACTED_VALUE"prewash",
    ),
    SwitchEntityDescription(
        key=OptionKey.LAUNDRY_CARE_WASHER_RINSE_HOLD,
        REDACTED_VALUE"rinse_hold",
    ),
    SwitchEntityDescription(
        key=OptionKey.LAUNDRY_CARE_WASHER_SOAK,
        REDACTED_VALUE"soaking",
    ),
    SwitchEntityDescription(
        key=OptionKey.LAUNDRY_CARE_WASHER_WATER_PLUS,
        REDACTED_VALUE"water_plus",
    ),
)


def _get_entities_for_appliance(
    appliance_coordinator: HomeConnectApplianceCoordinator,
) -> list[HomeConnectEntity]:
    """Get a list of entities."""
    entities: list[HomeConnectEntity] = []
    if SettingKey.BSH_COMMON_POWER_STATE in appliance_coordinator.data.settings:
        entities.append(
            HomeConnectPowerSwitch(appliance_coordinator, POWER_SWITCH_DESCRIPTION)
        )
    entities.extend(
        HomeConnectSwitch(appliance_coordinator, description)
        for description in SWITCHES
        if description.key in appliance_coordinator.data.settings
    )
    return entities


def _get_option_entities_for_appliance(
    appliance_coordinator: HomeConnectApplianceCoordinator,
    entity_registry: er.EntityRegistry,
) -> list[HomeConnectEntity]:
    """Get a list of currently available option entities."""
    return [
        HomeConnectSwitchOptionEntity(appliance_coordinator, description)
        for description in SWITCH_OPTIONS
        if should_add_option_entity(
            description, appliance_coordinator.data, entity_registry, Platform.SWITCH
        )
    ]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HomeConnectConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Home Connect switch."""
    setup_home_connect_entry(
        hass,
        entry,
        _get_entities_for_appliance,
        async_add_entities,
        _get_option_entities_for_appliance,
    )


class HomeConnectSwitch(HomeConnectEntity, SwitchEntity):
    """Generic switch class for Home Connect Binary Settings."""

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on setting."""
        try:
            await self.coordinator.client.set_setting(
                self.appliance.info.ha_id,
                setting_key=SettingKey(self.bsh_key),
                value=True,
            )
        except HomeConnectError as err:
            self._attr_available = False
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                REDACTED_VALUE"turn_on",
                translation_placeholders={
                    **get_dict_from_home_connect_error(err),
                    "entity_id": self.entity_id,
                    "key": self.bsh_key,
                },
            ) from err

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off setting."""
        try:
            await self.coordinator.client.set_setting(
                self.appliance.info.ha_id,
                setting_key=SettingKey(self.bsh_key),
                value=False,
            )
        except HomeConnectError as err:
            self._attr_available = False
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                REDACTED_VALUE"turn_off",
                translation_placeholders={
                    **get_dict_from_home_connect_error(err),
                    "entity_id": self.entity_id,
                    "key": self.bsh_key,
                },
            ) from err

    def update_native_value(self) -> None:
        """Update the switch's status."""
        self._attr_is_on = self.appliance.settings[SettingKey(self.bsh_key)].value


class HomeConnectPowerSwitch(HomeConnectEntity, SwitchEntity):
    """Power switch class for Home Connect."""

    power_off_state: str | None | UndefinedType = UNDEFINED

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Switch the device on."""
        try:
            await self.coordinator.client.set_setting(
                self.appliance.info.ha_id,
                setting_key=SettingKey.BSH_COMMON_POWER_STATE,
                value=BSH_POWER_ON,
            )
        except HomeConnectError as err:
            self._attr_is_on = False
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                REDACTED_VALUE"power_on",
                translation_placeholders={
                    **get_dict_from_home_connect_error(err),
                    "appliance_name": self.appliance.info.name,
                },
            ) from err

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Switch the device off."""
        if self.power_off_state is UNDEFINED:
            await self.async_fetch_power_off_state()
            if self.power_off_state is UNDEFINED:
                raise HomeAssistantError(
                    translation_domain=DOMAIN,
                    REDACTED_VALUE"unable_to_retrieve_turn_off",
                    translation_placeholders={
                        "appliance_name": self.appliance.info.name
                    },
                )

        if self.power_off_state is None:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                REDACTED_VALUE"turn_off_not_supported",
                translation_placeholders={"appliance_name": self.appliance.info.name},
            )
        try:
            await self.coordinator.client.set_setting(
                self.appliance.info.ha_id,
                setting_key=SettingKey.BSH_COMMON_POWER_STATE,
                value=self.power_off_state,
            )
        except HomeConnectError as err:
            self._attr_is_on = True
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                REDACTED_VALUE"power_off",
                translation_placeholders={
                    **get_dict_from_home_connect_error(err),
                    "appliance_name": self.appliance.info.name,
                    "value": self.power_off_state,
                },
            ) from err

    def update_native_value(self) -> None:
        """Set the value of the entity."""
        power_state = self.appliance.settings[SettingKey.BSH_COMMON_POWER_STATE]
        value = cast(str, power_state.value)
        if value == BSH_POWER_ON:
            self._attr_is_on = True
        elif (
            isinstance(self.power_off_state, str)
            and self.power_off_state
            and value == self.power_off_state
        ):
            self._attr_is_on = False
        elif self.power_off_state is UNDEFINED and value in [
            BSH_POWER_OFF,
            BSH_POWER_STANDBY,
        ]:
            self.power_off_state = value
            self._attr_is_on = False
        else:
            self._attr_is_on = None

    async def async_fetch_power_off_state(self) -> None:
        """Fetch the power off state."""
        data = self.appliance.settings[SettingKey.BSH_COMMON_POWER_STATE]

        if not data.constraints or not data.constraints.allowed_values:
            try:
                data = await self.coordinator.client.get_setting(
                    self.appliance.info.ha_id,
                    setting_key=SettingKey.BSH_COMMON_POWER_STATE,
                )
            except HomeConnectError as err:
                _LOGGER.error("An error occurred fetching the power settings: %s", err)
                return
        if not data.constraints or not data.constraints.allowed_values:
            return

        if BSH_POWER_OFF in data.constraints.allowed_values:
            self.power_off_state = BSH_POWER_OFF
        elif BSH_POWER_STANDBY in data.constraints.allowed_values:
            self.power_off_state = BSH_POWER_STANDBY
        else:
            self.power_off_state = None


class HomeConnectSwitchOptionEntity(HomeConnectOptionEntity, SwitchEntity):
    """Switch option class for Home Connect."""

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the option."""
        await self.async_set_option(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the option."""
        await self.async_set_option(False)

    def update_native_value(self) -> None:
        """Set the value of the entity."""
        self._attr_is_on = cast(bool | None, self.option_value)
