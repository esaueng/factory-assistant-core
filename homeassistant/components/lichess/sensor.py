"""Sensor platform for Lichess integration."""

from collections.abc import Callable
from dataclasses import dataclass

from aiolichess.models import LichessStatistics

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import LichessConfigEntry
from .coordinator import LichessCoordinator
from .entity import LichessEntity


@dataclass(kw_only=True, frozen=True)
class LichessEntityDescription(SensorEntityDescription):
    """Sensor description for Lichess player."""

    value_fn: Callable[[LichessStatistics], int | None]


SENSORS: tuple[LichessEntityDescription, ...] = (
    LichessEntityDescription(
        key="bullet_rating",
        REDACTED_VALUE"bullet_rating",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda state: state.bullet_rating,
    ),
    LichessEntityDescription(
        key="bullet_games",
        REDACTED_VALUE"bullet_games",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda state: state.bullet_games,
    ),
    LichessEntityDescription(
        key="blitz_rating",
        REDACTED_VALUE"blitz_rating",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda state: state.blitz_rating,
    ),
    LichessEntityDescription(
        key="blitz_games",
        REDACTED_VALUE"blitz_games",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda state: state.blitz_games,
    ),
    LichessEntityDescription(
        key="rapid_rating",
        REDACTED_VALUE"rapid_rating",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda state: state.rapid_rating,
    ),
    LichessEntityDescription(
        key="rapid_games",
        REDACTED_VALUE"rapid_games",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda state: state.rapid_games,
    ),
    LichessEntityDescription(
        key="classical_rating",
        REDACTED_VALUE"classical_rating",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda state: state.classical_rating,
    ),
    LichessEntityDescription(
        key="classical_games",
        REDACTED_VALUE"classical_games",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda state: state.classical_games,
    ),
    LichessEntityDescription(
        key="ultra_bullet_rating",
        REDACTED_VALUE"ultra_bullet_rating",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.ultra_bullet_rating,
    ),
    LichessEntityDescription(
        key="ultra_bullet_games",
        REDACTED_VALUE"ultra_bullet_games",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.ultra_bullet_games,
    ),
    LichessEntityDescription(
        key="correspondence_rating",
        REDACTED_VALUE"correspondence_rating",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.correspondence_rating,
    ),
    LichessEntityDescription(
        key="correspondence_games",
        REDACTED_VALUE"correspondence_games",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.correspondence_games,
    ),
    LichessEntityDescription(
        key="chess960_rating",
        REDACTED_VALUE"chess960_rating",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.chess960_rating,
    ),
    LichessEntityDescription(
        key="chess960_games",
        REDACTED_VALUE"chess960_games",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.chess960_games,
    ),
    LichessEntityDescription(
        key="crazyhouse_rating",
        REDACTED_VALUE"crazyhouse_rating",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.crazyhouse_rating,
    ),
    LichessEntityDescription(
        key="crazyhouse_games",
        REDACTED_VALUE"crazyhouse_games",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.crazyhouse_games,
    ),
    LichessEntityDescription(
        key="antichess_rating",
        REDACTED_VALUE"antichess_rating",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.antichess_rating,
    ),
    LichessEntityDescription(
        key="antichess_games",
        REDACTED_VALUE"antichess_games",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.antichess_games,
    ),
    LichessEntityDescription(
        key="atomic_rating",
        REDACTED_VALUE"atomic_rating",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.atomic_rating,
    ),
    LichessEntityDescription(
        key="atomic_games",
        REDACTED_VALUE"atomic_games",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.atomic_games,
    ),
    LichessEntityDescription(
        key="horde_rating",
        REDACTED_VALUE"horde_rating",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.horde_rating,
    ),
    LichessEntityDescription(
        key="horde_games",
        REDACTED_VALUE"horde_games",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.horde_games,
    ),
    LichessEntityDescription(
        key="king_of_the_hill_rating",
        REDACTED_VALUE"king_of_the_hill_rating",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.king_of_the_hill_rating,
    ),
    LichessEntityDescription(
        key="king_of_the_hill_games",
        REDACTED_VALUE"king_of_the_hill_games",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.king_of_the_hill_games,
    ),
    LichessEntityDescription(
        key="racing_kings_rating",
        REDACTED_VALUE"racing_kings_rating",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.racing_kings_rating,
    ),
    LichessEntityDescription(
        key="racing_kings_games",
        REDACTED_VALUE"racing_kings_games",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.racing_kings_games,
    ),
    LichessEntityDescription(
        key="three_check_rating",
        REDACTED_VALUE"three_check_rating",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.three_check_rating,
    ),
    LichessEntityDescription(
        key="three_check_games",
        REDACTED_VALUE"three_check_games",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.three_check_games,
    ),
    LichessEntityDescription(
        key="puzzle_rating",
        REDACTED_VALUE"puzzle_rating",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.puzzle_rating,
    ),
    LichessEntityDescription(
        key="puzzle_games",
        REDACTED_VALUE"puzzle_games",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda state: state.puzzle_games,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: LichessConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Initialize the entries."""
    coordinator = entry.runtime_data

    async_add_entities(
        LichessPlayerSensor(coordinator, description) for description in SENSORS
    )


class LichessPlayerSensor(LichessEntity, SensorEntity):
    """Lichess sensor."""

    entity_description: LichessEntityDescription

    def __init__(
        self,
        coordinator: LichessCoordinator,
        description: LichessEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.config_entry.unique_id}.{description.key}"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.coordinator.data)
