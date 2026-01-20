"""Sensor platform for HDFury Integration."""

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import HDFuryConfigEntry
from .entity import HDFuryEntity

PARALLEL_UPDATES = 0

SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="RX0",
        REDACTED_VALUE"rx0",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="RX1",
        REDACTED_VALUE"rx1",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="TX0",
        REDACTED_VALUE"tx0",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="TX1",
        REDACTED_VALUE"tx1",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="AUD0",
        REDACTED_VALUE"aud0",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="AUD1",
        REDACTED_VALUE"aud1",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="AUDOUT",
        REDACTED_VALUE"audout",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="EARCRX",
        REDACTED_VALUE"earcrx",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="SINK0",
        REDACTED_VALUE"sink0",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="SINK1",
        REDACTED_VALUE"sink1",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="SINK2",
        REDACTED_VALUE"sink2",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="EDIDA0",
        REDACTED_VALUE"edida0",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="EDIDA1",
        REDACTED_VALUE"edida1",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="EDIDA2",
        REDACTED_VALUE"edida2",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HDFuryConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up sensors using the platform schema."""

    coordinator = entry.runtime_data

    async_add_entities(
        HDFurySensor(coordinator, description)
        for description in SENSORS
        if description.key in coordinator.data.info
    )


class HDFurySensor(HDFuryEntity, SensorEntity):
    """Base HDFury Sensor Class."""

    entity_description: SensorEntityDescription

    @property
    def native_value(self) -> str:
        """Set Sensor Value."""

        return self.coordinator.data.info[self.entity_description.key]
