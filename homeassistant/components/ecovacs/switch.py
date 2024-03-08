"""Ecovacs switch module."""

from dataclasses import dataclass
from typing import Any

from deebot_client.capabilities import (
    Capabilities,
    CapabilitySetEnable,
    VacuumCapabilities,
)
from deebot_client.events import EnableEvent

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .controller import EcovacsController
from .entity import (
    CapabilityDevice,
    EcovacsCapabilityEntityDescription,
    EcovacsDescriptionEntity,
    EcovacsEntity,
)
from .util import get_supported_entitites


@dataclass(kw_only=True, frozen=True)
class EcovacsSwitchEntityDescription(
    SwitchEntityDescription,
    EcovacsCapabilityEntityDescription[CapabilityDevice, CapabilitySetEnable],
):
    """Ecovacs switch entity description."""


ENTITY_DESCRIPTIONS: tuple[EcovacsSwitchEntityDescription, ...] = (
    EcovacsSwitchEntityDescription[Capabilities](
        device_capabilities=Capabilities,
        capability_fn=lambda c: c.settings.advanced_mode,
        key="advanced_mode",
        REDACTED_VALUE"advanced_mode",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.CONFIG,
    ),
    EcovacsSwitchEntityDescription[VacuumCapabilities](
        device_capabilities=VacuumCapabilities,
        capability_fn=lambda c: c.clean.continuous,
        key="continuous_cleaning",
        REDACTED_VALUE"continuous_cleaning",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.CONFIG,
    ),
    EcovacsSwitchEntityDescription[VacuumCapabilities](
        device_capabilities=VacuumCapabilities,
        capability_fn=lambda c: c.settings.carpet_auto_fan_boost,
        key="carpet_auto_fan_boost",
        REDACTED_VALUE"carpet_auto_fan_boost",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.CONFIG,
    ),
    EcovacsSwitchEntityDescription[VacuumCapabilities](
        device_capabilities=VacuumCapabilities,
        capability_fn=lambda c: c.clean.preference,
        key="clean_preference",
        REDACTED_VALUE"clean_preference",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.CONFIG,
    ),
    EcovacsSwitchEntityDescription[Capabilities](
        device_capabilities=Capabilities,
        capability_fn=lambda c: c.settings.true_detect,
        key="true_detect",
        REDACTED_VALUE"true_detect",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.CONFIG,
    ),
    EcovacsSwitchEntityDescription[Capabilities](
        device_capabilities=Capabilities,
        capability_fn=lambda c: c.settings.border_switch,
        key="border_switch",
        REDACTED_VALUE"border_switch",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.CONFIG,
    ),
    EcovacsSwitchEntityDescription[Capabilities](
        device_capabilities=Capabilities,
        capability_fn=lambda c: c.settings.child_lock,
        key="child_lock",
        REDACTED_VALUE"child_lock",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.CONFIG,
    ),
    EcovacsSwitchEntityDescription[Capabilities](
        device_capabilities=Capabilities,
        capability_fn=lambda c: c.settings.moveup_warning,
        key="move_up_warning",
        REDACTED_VALUE"move_up_warning",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.CONFIG,
    ),
    EcovacsSwitchEntityDescription[Capabilities](
        device_capabilities=Capabilities,
        capability_fn=lambda c: c.settings.cross_map_border_warning,
        key="cross_map_border_warning",
        REDACTED_VALUE"cross_map_border_warning",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.CONFIG,
    ),
    EcovacsSwitchEntityDescription[Capabilities](
        device_capabilities=Capabilities,
        capability_fn=lambda c: c.settings.safe_protect,
        key="safe_protect",
        REDACTED_VALUE"safe_protect",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add entities for passed config_entry in HA."""
    controller: EcovacsController = hass.data[DOMAIN][config_entry.entry_id]
    entities: list[EcovacsEntity] = get_supported_entitites(
        controller, EcovacsSwitchEntity, ENTITY_DESCRIPTIONS
    )
    if entities:
        async_add_entities(entities)


class EcovacsSwitchEntity(
    EcovacsDescriptionEntity[CapabilityDevice, CapabilitySetEnable],
    SwitchEntity,
):
    """Ecovacs switch entity."""

    entity_description: EcovacsSwitchEntityDescription

    _attr_is_on = False

    async def async_added_to_hass(self) -> None:
        """Set up the event listeners now that hass is ready."""
        await super().async_added_to_hass()

        async def on_event(event: EnableEvent) -> None:
            self._attr_is_on = event.enable
            self.async_write_ha_state()

        self._subscribe(self._capability.event, on_event)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self._device.execute_command(self._capability.set(True))

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self._device.execute_command(self._capability.set(False))
