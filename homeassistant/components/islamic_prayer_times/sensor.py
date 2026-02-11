"""Platform to retrieve Islamic prayer times information for Home Assistant."""

from datetime import datetime

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import IslamicPrayerTimesConfigEntry
from .const import DOMAIN, NAME
from .coordinator import IslamicPrayerDataUpdateCoordinator

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="Fajr",
        REDACTED_VALUE"fajr",
    ),
    SensorEntityDescription(
        key="Sunrise",
        REDACTED_VALUE"sunrise",
    ),
    SensorEntityDescription(
        key="Dhuhr",
        REDACTED_VALUE"dhuhr",
    ),
    SensorEntityDescription(
        key="Asr",
        REDACTED_VALUE"asr",
    ),
    SensorEntityDescription(
        key="Maghrib",
        REDACTED_VALUE"maghrib",
    ),
    SensorEntityDescription(
        key="Isha",
        REDACTED_VALUE"isha",
    ),
    SensorEntityDescription(
        key="Midnight",
        REDACTED_VALUE"midnight",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: IslamicPrayerTimesConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Islamic prayer times sensor platform."""

    coordinator = config_entry.runtime_data
    async_add_entities(
        IslamicPrayerTimeSensor(coordinator, description)
        for description in SENSOR_TYPES
    )


class IslamicPrayerTimeSensor(
    CoordinatorEntity[IslamicPrayerDataUpdateCoordinator], SensorEntity
):
    """Representation of an Islamic prayer time sensor."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: IslamicPrayerDataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the Islamic prayer time sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}-{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name=NAME,
            entry_type=DeviceEntryType.SERVICE,
        )

    @property
    def native_value(self) -> datetime:
        """Return the state of the sensor."""
        return self.coordinator.data[self.entity_description.key]
