"""Support for switch entities."""

from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any

from thinqconnect import DeviceType
from thinqconnect.devices.const import Property as ThinQProperty
from thinqconnect.integration import ActiveMode

from homeassistant.components.switch import (
    SwitchDeviceClass,
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import ThinqConfigEntry
from .entity import ThinQEntity


@dataclass(frozen=True, kw_only=True)
class ThinQSwitchEntityDescription(SwitchEntityDescription):
    """Describes ThinQ switch entity."""

    on_key: str | None = None
    off_key: str | None = None


DRYER_OPERATION_SWITCH_DESC = ThinQSwitchEntityDescription(
    key=ThinQProperty.DRYER_OPERATION_MODE, REDACTED_VALUE"operation_power"
)

WASHER_OPERATION_SWITCH_DESC = ThinQSwitchEntityDescription(
    key=ThinQProperty.WASHER_OPERATION_MODE, REDACTED_VALUE"operation_power"
)


DEVICE_TYPE_SWITCH_MAP: dict[DeviceType, tuple[ThinQSwitchEntityDescription, ...]] = {
    DeviceType.AIR_CONDITIONER: (
        ThinQSwitchEntityDescription(
            key=ThinQProperty.AIR_CON_OPERATION_MODE,
            REDACTED_VALUE"operation_power",
            entity_category=EntityCategory.CONFIG,
        ),
        ThinQSwitchEntityDescription(
            key=ThinQProperty.DISPLAY_LIGHT,
            REDACTED_VALUEThinQProperty.DISPLAY_LIGHT,
            on_key="on",
            off_key="off",
            entity_category=EntityCategory.CONFIG,
        ),
        ThinQSwitchEntityDescription(
            key=ThinQProperty.POWER_SAVE_ENABLED,
            REDACTED_VALUEThinQProperty.POWER_SAVE_ENABLED,
            on_key="true",
            off_key="false",
            entity_category=EntityCategory.CONFIG,
        ),
        ThinQSwitchEntityDescription(
            key=ThinQProperty.AIR_CLEAN_OPERATION_MODE,
            REDACTED_VALUEThinQProperty.AIR_CLEAN_OPERATION_MODE,
            on_key="on",
            off_key="off",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceType.AIR_PURIFIER_FAN: (
        ThinQSwitchEntityDescription(
            key=ThinQProperty.AIR_FAN_OPERATION_MODE, REDACTED_VALUE"operation_power"
        ),
        ThinQSwitchEntityDescription(
            key=ThinQProperty.UV_NANO,
            REDACTED_VALUEThinQProperty.UV_NANO,
            on_key="on",
            off_key="off",
            entity_category=EntityCategory.CONFIG,
        ),
        ThinQSwitchEntityDescription(
            key=ThinQProperty.WARM_MODE,
            REDACTED_VALUEThinQProperty.WARM_MODE,
            on_key="warm_on",
            off_key="warm_off",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceType.AIR_PURIFIER: (
        ThinQSwitchEntityDescription(
            key=ThinQProperty.AIR_PURIFIER_OPERATION_MODE,
            REDACTED_VALUE"operation_power",
        ),
    ),
    DeviceType.DEHUMIDIFIER: (
        ThinQSwitchEntityDescription(
            key=ThinQProperty.DEHUMIDIFIER_OPERATION_MODE,
            REDACTED_VALUE"operation_power",
        ),
    ),
    DeviceType.DISH_WASHER: (
        ThinQSwitchEntityDescription(
            key=ThinQProperty.DISH_WASHER_OPERATION_MODE,
            REDACTED_VALUE"operation_power",
        ),
    ),
    DeviceType.DRYER: (DRYER_OPERATION_SWITCH_DESC,),
    DeviceType.HUMIDIFIER: (
        ThinQSwitchEntityDescription(
            key=ThinQProperty.HUMIDIFIER_OPERATION_MODE,
            REDACTED_VALUE"operation_power",
        ),
        ThinQSwitchEntityDescription(
            key=ThinQProperty.WARM_MODE,
            REDACTED_VALUE"humidity_warm_mode",
            on_key="warm_on",
            off_key="warm_off",
            entity_category=EntityCategory.CONFIG,
        ),
        ThinQSwitchEntityDescription(
            key=ThinQProperty.MOOD_LAMP_STATE,
            REDACTED_VALUEThinQProperty.MOOD_LAMP_STATE,
            on_key="on",
            off_key="off",
            entity_category=EntityCategory.CONFIG,
        ),
        ThinQSwitchEntityDescription(
            key=ThinQProperty.AUTO_MODE,
            REDACTED_VALUEThinQProperty.AUTO_MODE,
            on_key="auto_on",
            off_key="auto_off",
            entity_category=EntityCategory.CONFIG,
        ),
        ThinQSwitchEntityDescription(
            key=ThinQProperty.SLEEP_MODE,
            REDACTED_VALUEThinQProperty.SLEEP_MODE,
            on_key="sleep_on",
            off_key="sleep_off",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceType.REFRIGERATOR: (
        ThinQSwitchEntityDescription(
            key=ThinQProperty.EXPRESS_MODE,
            REDACTED_VALUEThinQProperty.EXPRESS_MODE,
            on_key="true",
            off_key="false",
            entity_category=EntityCategory.CONFIG,
        ),
        ThinQSwitchEntityDescription(
            key=ThinQProperty.RAPID_FREEZE,
            REDACTED_VALUEThinQProperty.RAPID_FREEZE,
            on_key="true",
            off_key="false",
            entity_category=EntityCategory.CONFIG,
        ),
        ThinQSwitchEntityDescription(
            key=ThinQProperty.EXPRESS_FRIDGE,
            REDACTED_VALUEThinQProperty.EXPRESS_FRIDGE,
            on_key="true",
            off_key="false",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceType.SYSTEM_BOILER: (
        ThinQSwitchEntityDescription(
            key=ThinQProperty.BOILER_OPERATION_MODE,
            REDACTED_VALUE"operation_power",
            entity_category=EntityCategory.CONFIG,
        ),
        ThinQSwitchEntityDescription(
            key=ThinQProperty.HOT_WATER_MODE,
            REDACTED_VALUEThinQProperty.HOT_WATER_MODE,
            on_key="on",
            off_key="off",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceType.STYLER: (
        ThinQSwitchEntityDescription(
            key=ThinQProperty.STYLER_OPERATION_MODE, REDACTED_VALUE"operation_power"
        ),
    ),
    DeviceType.VENTILATOR: (
        ThinQSwitchEntityDescription(
            key=ThinQProperty.VENTILATOR_OPERATION_MODE,
            REDACTED_VALUE"operation_power",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceType.WASHCOMBO_MAIN: (WASHER_OPERATION_SWITCH_DESC,),
    DeviceType.WASHCOMBO_MINI: (WASHER_OPERATION_SWITCH_DESC,),
    DeviceType.WASHER: (WASHER_OPERATION_SWITCH_DESC,),
    DeviceType.WASHTOWER: (
        DRYER_OPERATION_SWITCH_DESC,
        WASHER_OPERATION_SWITCH_DESC,
    ),
    DeviceType.WASHTOWER_DRYER: (DRYER_OPERATION_SWITCH_DESC,),
    DeviceType.WASHTOWER_WASHER: (WASHER_OPERATION_SWITCH_DESC,),
    DeviceType.WINE_CELLAR: (
        ThinQSwitchEntityDescription(
            key=ThinQProperty.OPTIMAL_HUMIDITY,
            REDACTED_VALUEThinQProperty.OPTIMAL_HUMIDITY,
            on_key="on",
            off_key="off",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
}

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ThinqConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up an entry for switch platform."""
    entities: list[ThinQSwitchEntity] = []
    for coordinator in entry.runtime_data.coordinators.values():
        if (
            descriptions := DEVICE_TYPE_SWITCH_MAP.get(
                coordinator.api.device.device_type
            )
        ) is not None:
            for description in descriptions:
                entities.extend(
                    ThinQSwitchEntity(coordinator, description, property_id)
                    for property_id in coordinator.api.get_active_idx(
                        description.key,
                        ActiveMode.WRITABLE,
                    )
                )

    if entities:
        async_add_entities(entities)


class ThinQSwitchEntity(ThinQEntity, SwitchEntity):
    """Represent a thinq switch platform."""

    entity_description: ThinQSwitchEntityDescription
    _attr_device_class = SwitchDeviceClass.SWITCH

    def _update_status(self) -> None:
        """Update status itself."""
        super()._update_status()

        if (key := self.entity_description.on_key) is not None:
            self._attr_is_on = self.data.value == key
        else:
            self._attr_is_on = self.data.is_on

        _LOGGER.debug(
            "[%s:%s] update status: %s -> %s",
            self.coordinator.device_name,
            self.property_id,
            self.data.is_on,
            self.is_on,
        )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the switch."""
        _LOGGER.debug(
            "[%s:%s] async_turn_on id: %s",
            self.coordinator.device_name,
            self.name,
            self.property_id,
        )
        if (on_command := self.entity_description.on_key) is not None:
            await self.async_call_api(
                self.coordinator.api.post(self.property_id, on_command)
            )
        else:
            await self.async_call_api(
                self.coordinator.api.async_turn_on(self.property_id)
            )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the switch."""
        _LOGGER.debug(
            "[%s:%s] async_turn_off id: %s",
            self.coordinator.device_name,
            self.name,
            self.property_id,
        )
        if (off_command := self.entity_description.off_key) is not None:
            await self.async_call_api(
                self.coordinator.api.post(self.property_id, off_command)
            )
        else:
            await self.async_call_api(
                self.coordinator.api.async_turn_off(self.property_id)
            )
