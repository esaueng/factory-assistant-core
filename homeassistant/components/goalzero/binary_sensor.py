"""Support for Goal Zero Yeti Sensors."""

from typing import cast

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import GoalZeroConfigEntry
from .entity import GoalZeroEntity

PARALLEL_UPDATES = 0

BINARY_SENSOR_TYPES: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key="backlight",
        REDACTED_VALUE"backlight",
    ),
    BinarySensorEntityDescription(
        key="app_online",
        REDACTED_VALUE"app_online",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    BinarySensorEntityDescription(
        key="isCharging",
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
    ),
    BinarySensorEntityDescription(
        key="inputDetected",
        REDACTED_VALUE"input_detected",
        device_class=BinarySensorDeviceClass.POWER,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GoalZeroConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Goal Zero Yeti sensor."""
    async_add_entities(
        GoalZeroBinarySensor(entry.runtime_data, description)
        for description in BINARY_SENSOR_TYPES
    )


class GoalZeroBinarySensor(GoalZeroEntity, BinarySensorEntity):
    """Representation of a Goal Zero Yeti sensor."""

    @property
    def is_on(self) -> bool:
        """Return True if the service is on."""
        return cast(bool, self._api.data[self.entity_description.key] == 1)
