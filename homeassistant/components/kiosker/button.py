"""Button platform for Kiosker."""

from collections.abc import Callable
from dataclasses import dataclass

from kiosker import KioskerAPI

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import KioskerConfigEntry
from .entity import KioskerEntity

PARALLEL_UPDATES = 1


@dataclass(frozen=True, kw_only=True)
class KioskerButtonEntityDescription(ButtonEntityDescription):
    """Describe a Kiosker button."""

    action_fn: Callable[[KioskerAPI], None] | None = None


BUTTONS: tuple[KioskerButtonEntityDescription, ...] = (
    KioskerButtonEntityDescription(
        key="ping",
        REDACTED_VALUE"ping",
        entity_category=EntityCategory.DIAGNOSTIC,
        action_fn=lambda api: api.ping(),
    ),
    KioskerButtonEntityDescription(
        key="navigateRefresh",
        REDACTED_VALUE"navigate_refresh",
        action_fn=lambda api: api.navigate_refresh(),
    ),
    KioskerButtonEntityDescription(
        key="navigateHome",
        REDACTED_VALUE"navigate_home",
        action_fn=lambda api: api.navigate_home(),
    ),
    KioskerButtonEntityDescription(
        key="navigateForward",
        REDACTED_VALUE"navigate_forward",
        action_fn=lambda api: api.navigate_forward(),
    ),
    KioskerButtonEntityDescription(
        key="navigateBackward",
        REDACTED_VALUE"navigate_backward",
        action_fn=lambda api: api.navigate_backward(),
    ),
    KioskerButtonEntityDescription(
        key="print",
        REDACTED_VALUE"print",
        action_fn=lambda api: api.print(),
    ),
    KioskerButtonEntityDescription(
        key="clearCache",
        REDACTED_VALUE"clear_cache",
        entity_category=EntityCategory.CONFIG,
        action_fn=lambda api: api.clear_cache(),
    ),
    KioskerButtonEntityDescription(
        key="clearCookies",
        REDACTED_VALUE"clear_cookies",
        entity_category=EntityCategory.CONFIG,
        action_fn=lambda api: api.clear_cookies(),
    ),
    KioskerButtonEntityDescription(
        key="screensaverInteract",
        REDACTED_VALUE"screensaver_interact",
        action_fn=lambda api: api.screensaver_interact(),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: KioskerConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Kiosker buttons based on a config entry."""
    coordinator = entry.runtime_data

    async_add_entities(
        KioskerButton(coordinator, description) for description in BUTTONS
    )


class KioskerButton(KioskerEntity, ButtonEntity):
    """Representation of a Kiosker button."""

    entity_description: KioskerButtonEntityDescription

    async def async_press(self) -> None:
        """Handle button press."""
        if action_fn := self.entity_description.action_fn:
            await self.hass.async_add_executor_job(action_fn, self.coordinator.api)
