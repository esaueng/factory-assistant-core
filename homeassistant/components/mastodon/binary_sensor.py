"""Binary sensor platform for the Mastodon integration."""

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum

from mastodon.Mastodon import Account

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import MastodonConfigEntry
from .entity import MastodonEntity

# Coordinator is used to centralize the data updates
PARALLEL_UPDATES = 0


class MastodonBinarySensor(StrEnum):
    """Mastodon binary sensors."""

    BOT = "bot"
    SUSPENDED = "suspended"
    DISCOVERABLE = "discoverable"
    LOCKED = "locked"
    INDEXABLE = "indexable"
    LIMITED = "limited"
    MEMORIAL = "memorial"
    MOVED = "moved"


@dataclass(frozen=True, kw_only=True)
class MastodonBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Mastodon binary sensor description."""

    is_on_fn: Callable[[Account], bool | None]


ENTITY_DESCRIPTIONS: tuple[MastodonBinarySensorEntityDescription, ...] = (
    MastodonBinarySensorEntityDescription(
        key=MastodonBinarySensor.BOT,
        REDACTED_VALUEMastodonBinarySensor.BOT,
        is_on_fn=lambda account: account.bot,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    MastodonBinarySensorEntityDescription(
        key=MastodonBinarySensor.DISCOVERABLE,
        REDACTED_VALUEMastodonBinarySensor.DISCOVERABLE,
        is_on_fn=lambda account: account.discoverable,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    MastodonBinarySensorEntityDescription(
        key=MastodonBinarySensor.LOCKED,
        REDACTED_VALUEMastodonBinarySensor.LOCKED,
        is_on_fn=lambda account: account.locked,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    MastodonBinarySensorEntityDescription(
        key=MastodonBinarySensor.MOVED,
        REDACTED_VALUEMastodonBinarySensor.MOVED,
        is_on_fn=lambda account: account.moved is not None,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    MastodonBinarySensorEntityDescription(
        key=MastodonBinarySensor.INDEXABLE,
        REDACTED_VALUEMastodonBinarySensor.INDEXABLE,
        is_on_fn=lambda account: account.indexable,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    MastodonBinarySensorEntityDescription(
        key=MastodonBinarySensor.LIMITED,
        REDACTED_VALUEMastodonBinarySensor.LIMITED,
        is_on_fn=lambda account: account.limited is True,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    MastodonBinarySensorEntityDescription(
        key=MastodonBinarySensor.MEMORIAL,
        REDACTED_VALUEMastodonBinarySensor.MEMORIAL,
        is_on_fn=lambda account: account.memorial is True,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    MastodonBinarySensorEntityDescription(
        key=MastodonBinarySensor.SUSPENDED,
        REDACTED_VALUEMastodonBinarySensor.SUSPENDED,
        is_on_fn=lambda account: account.suspended is True,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MastodonConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the binary sensor platform."""
    coordinator = entry.runtime_data.coordinator

    async_add_entities(
        MastodonBinarySensorEntity(
            coordinator=coordinator,
            entity_description=entity_description,
            data=entry,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class MastodonBinarySensorEntity(MastodonEntity, BinarySensorEntity):
    """Mastodon binary sensor entity."""

    entity_description: MastodonBinarySensorEntityDescription

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        return self.entity_description.is_on_fn(self.coordinator.data)
