"""Support for IntelliFire Binary Sensors."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import IntellifireDataUpdateCoordinator
from .const import DOMAIN
from .entity import IntellifireEntity


@dataclass(frozen=True)
class IntellifireBinarySensorRequiredKeysMixin:
    """Mixin for required keys."""

    value_fn: Callable[[IntellifireDataUpdateCoordinator], bool | None]


@dataclass(frozen=True)
class IntellifireBinarySensorEntityDescription(
    BinarySensorEntityDescription, IntellifireBinarySensorRequiredKeysMixin
):
    """Describes a binary sensor entity."""


INTELLIFIRE_BINARY_SENSORS: tuple[IntellifireBinarySensorEntityDescription, ...] = (
    IntellifireBinarySensorEntityDescription(
        key="on_off",  # This is the sensor name
        REDACTED_VALUE"flame",  # This is the translation key
        value_fn=lambda coordinator: coordinator.data.is_on,
    ),
    IntellifireBinarySensorEntityDescription(
        key="timer_on",
        REDACTED_VALUE"timer_on",
        value_fn=lambda coordinator: coordinator.data.timer_on,
    ),
    IntellifireBinarySensorEntityDescription(
        key="pilot_light_on",
        REDACTED_VALUE"pilot_light_on",
        value_fn=lambda coordinator: coordinator.data.pilot_on,
    ),
    IntellifireBinarySensorEntityDescription(
        key="thermostat_on",
        REDACTED_VALUE"thermostat_on",
        value_fn=lambda coordinator: coordinator.data.thermostat_on,
    ),
    IntellifireBinarySensorEntityDescription(
        key="error_pilot_flame",
        REDACTED_VALUE"pilot_flame_error",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda coordinator: coordinator.data.error_pilot_flame,
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    IntellifireBinarySensorEntityDescription(
        key="error_flame",
        REDACTED_VALUE"flame_error",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda coordinator: coordinator.data.error_flame,
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    IntellifireBinarySensorEntityDescription(
        key="error_fan_delay",
        REDACTED_VALUE"fan_delay_error",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda coordinator: coordinator.data.error_fan_delay,
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    IntellifireBinarySensorEntityDescription(
        key="error_maintenance",
        REDACTED_VALUE"maintenance_error",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda coordinator: coordinator.data.error_maintenance,
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    IntellifireBinarySensorEntityDescription(
        key="error_disabled",
        REDACTED_VALUE"disabled_error",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda coordinator: coordinator.data.error_disabled,
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    IntellifireBinarySensorEntityDescription(
        key="error_fan",
        REDACTED_VALUE"fan_error",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda coordinator: coordinator.data.error_fan,
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    IntellifireBinarySensorEntityDescription(
        key="error_lights",
        REDACTED_VALUE"lights_error",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda coordinator: coordinator.data.error_lights,
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    IntellifireBinarySensorEntityDescription(
        key="error_accessory",
        REDACTED_VALUE"accessory_error",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda coordinator: coordinator.data.error_accessory,
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    IntellifireBinarySensorEntityDescription(
        key="error_soft_lock_out",
        REDACTED_VALUE"soft_lock_out_error",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda coordinator: coordinator.data.error_soft_lock_out,
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    IntellifireBinarySensorEntityDescription(
        key="error_ecm_offline",
        REDACTED_VALUE"ecm_offline_error",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda coordinator: coordinator.data.error_ecm_offline,
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    IntellifireBinarySensorEntityDescription(
        key="error_offline",
        REDACTED_VALUE"offline_error",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda coordinator: coordinator.data.error_offline,
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    IntellifireBinarySensorEntityDescription(
        key="local_connectivity",
        REDACTED_VALUE"local_connectivity",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        value_fn=lambda coordinator: coordinator.fireplace.local_connectivity,
    ),
    IntellifireBinarySensorEntityDescription(
        key="cloud_connectivity",
        REDACTED_VALUE"cloud_connectivity",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        value_fn=lambda coordinator: coordinator.fireplace.cloud_connectivity,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up a IntelliFire On/Off Sensor."""
    coordinator: IntellifireDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        IntellifireBinarySensor(coordinator=coordinator, description=description)
        for description in INTELLIFIRE_BINARY_SENSORS
    )


class IntellifireBinarySensor(IntellifireEntity, BinarySensorEntity):
    """Extends IntellifireEntity with Binary Sensor specific logic."""

    entity_description: IntellifireBinarySensorEntityDescription

    @property
    def is_on(self) -> bool | None:
        """Use this to get the correct value."""
        return self.entity_description.value_fn(self.coordinator)
