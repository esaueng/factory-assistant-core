"""Button entities for Tami4Edge."""
from collections.abc import Callable
from dataclasses import dataclass
import logging

from REDACTED_VALUE import REDACTED_VALUE

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import API, DOMAIN
from .entity import Tami4EdgeBaseEntity

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class Tami4EdgeButtonEntityDescription(ButtonEntityDescription):
    """A class that describes Tami4Edge button entities."""

    press_fn: Callable[[REDACTED_VALUE], None]


BUTTONS: tuple[Tami4EdgeButtonEntityDescription] = (
    Tami4EdgeButtonEntityDescription(
        key="boil_water",
        REDACTED_VALUE"boil_water",
        press_fn=lambda api: api.boil_water(),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Perform the setup for Tami4Edge."""
    api: REDACTED_VALUE = hass.data[DOMAIN][entry.entry_id][API]

    async_add_entities(
        Tami4EdgeButton(api, entity_description) for entity_description in BUTTONS
    )


class Tami4EdgeButton(Tami4EdgeBaseEntity, ButtonEntity):
    """Button entity for Tami4Edge."""

    entity_description: Tami4EdgeButtonEntityDescription

    def press(self) -> None:
        """Handle the button press."""
        self.entity_description.press_fn(self._api)
