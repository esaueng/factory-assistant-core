"""Summary binary data from Nextcoud."""

from typing import Final

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import NextcloudConfigEntry
from .entity import NextcloudEntity

BINARY_SENSORS: Final[list[BinarySensorEntityDescription]] = [
    BinarySensorEntityDescription(
        key="jit_enabled",
        REDACTED_VALUE"nextcloud_jit_enabled",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    BinarySensorEntityDescription(
        key="jit_on",
        REDACTED_VALUE"nextcloud_jit_on",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    BinarySensorEntityDescription(
        key="system_debug",
        REDACTED_VALUE"nextcloud_system_debug",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    BinarySensorEntityDescription(
        key="system_enable_avatars",
        REDACTED_VALUE"nextcloud_system_enable_avatars",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    BinarySensorEntityDescription(
        key="system_enable_previews",
        REDACTED_VALUE"nextcloud_system_enable_previews",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    BinarySensorEntityDescription(
        key="system_filelocking.enabled",
        REDACTED_VALUE"nextcloud_system_filelocking_enabled",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: NextcloudConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Nextcloud binary sensors."""
    coordinator = entry.runtime_data
    async_add_entities(
        NextcloudBinarySensor(coordinator, entry, sensor)
        for sensor in BINARY_SENSORS
        if sensor.key in coordinator.data
    )


class NextcloudBinarySensor(NextcloudEntity, BinarySensorEntity):
    """Represents a Nextcloud binary sensor."""

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        val = self.coordinator.data.get(self.entity_description.key)
        return val is True or val == "yes"
