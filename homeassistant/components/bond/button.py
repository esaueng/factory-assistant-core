"""Support for bond buttons."""

from __future__ import annotations

from dataclasses import dataclass

from bond_async import Action

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import BondConfigEntry
from .entity import BondEntity
from .models import BondData
from .utils import BondDevice

# The api requires a step size even though it does not
# seem to matter what is is as the underlying device is likely
# getting an increase/decrease signal only
STEP_SIZE = 10


@dataclass(frozen=True, kw_only=True)
class BondButtonEntityDescription(ButtonEntityDescription):
    """Class to describe a Bond Button entity."""

    # BondEntity does not support UNDEFINED,
    # restrict the type to str | None
    name: str | None = None
    mutually_exclusive: Action | None
    argument: int | None


STOP_BUTTON = BondButtonEntityDescription(
    key=Action.STOP,
    name="Stop Actions",
    REDACTED_VALUE"stop_actions",
    mutually_exclusive=None,
    argument=None,
)


BUTTONS: tuple[BondButtonEntityDescription, ...] = (
    BondButtonEntityDescription(
        key=Action.TOGGLE_POWER,
        name="Toggle Power",
        REDACTED_VALUE"toggle_power",
        mutually_exclusive=Action.TURN_ON,
        argument=None,
    ),
    BondButtonEntityDescription(
        key=Action.TOGGLE_LIGHT,
        name="Toggle Light",
        REDACTED_VALUE"toggle_light",
        mutually_exclusive=Action.TURN_LIGHT_ON,
        argument=None,
    ),
    BondButtonEntityDescription(
        key=Action.INCREASE_BRIGHTNESS,
        name="Increase Brightness",
        REDACTED_VALUE"increase_brightness",
        mutually_exclusive=Action.SET_BRIGHTNESS,
        argument=STEP_SIZE,
    ),
    BondButtonEntityDescription(
        key=Action.DECREASE_BRIGHTNESS,
        name="Decrease Brightness",
        REDACTED_VALUE"decrease_brightness",
        mutually_exclusive=Action.SET_BRIGHTNESS,
        argument=STEP_SIZE,
    ),
    BondButtonEntityDescription(
        key=Action.TOGGLE_UP_LIGHT,
        name="Toggle Up Light",
        REDACTED_VALUE"toggle_up_light",
        mutually_exclusive=Action.TURN_UP_LIGHT_ON,
        argument=None,
    ),
    BondButtonEntityDescription(
        key=Action.TOGGLE_DOWN_LIGHT,
        name="Toggle Down Light",
        REDACTED_VALUE"toggle_down_light",
        mutually_exclusive=Action.TURN_DOWN_LIGHT_ON,
        argument=None,
    ),
    BondButtonEntityDescription(
        key=Action.START_DIMMER,
        name="Start Dimmer",
        REDACTED_VALUE"start_dimmer",
        mutually_exclusive=Action.SET_BRIGHTNESS,
        argument=None,
    ),
    BondButtonEntityDescription(
        key=Action.START_UP_LIGHT_DIMMER,
        name="Start Up Light Dimmer",
        REDACTED_VALUE"start_up_light_dimmer",
        mutually_exclusive=Action.SET_UP_LIGHT_BRIGHTNESS,
        argument=None,
    ),
    BondButtonEntityDescription(
        key=Action.START_DOWN_LIGHT_DIMMER,
        name="Start Down Light Dimmer",
        REDACTED_VALUE"start_down_light_dimmer",
        mutually_exclusive=Action.SET_DOWN_LIGHT_BRIGHTNESS,
        argument=None,
    ),
    BondButtonEntityDescription(
        key=Action.START_INCREASING_BRIGHTNESS,
        name="Start Increasing Brightness",
        REDACTED_VALUE"start_increasing_brightness",
        mutually_exclusive=Action.SET_BRIGHTNESS,
        argument=None,
    ),
    BondButtonEntityDescription(
        key=Action.START_DECREASING_BRIGHTNESS,
        name="Start Decreasing Brightness",
        REDACTED_VALUE"start_decreasing_brightness",
        mutually_exclusive=Action.SET_BRIGHTNESS,
        argument=None,
    ),
    BondButtonEntityDescription(
        key=Action.INCREASE_UP_LIGHT_BRIGHTNESS,
        name="Increase Up Light Brightness",
        REDACTED_VALUE"increase_up_light_brightness",
        mutually_exclusive=Action.SET_UP_LIGHT_BRIGHTNESS,
        argument=STEP_SIZE,
    ),
    BondButtonEntityDescription(
        key=Action.DECREASE_UP_LIGHT_BRIGHTNESS,
        name="Decrease Up Light Brightness",
        REDACTED_VALUE"decrease_up_light_brightness",
        mutually_exclusive=Action.SET_UP_LIGHT_BRIGHTNESS,
        argument=STEP_SIZE,
    ),
    BondButtonEntityDescription(
        key=Action.INCREASE_DOWN_LIGHT_BRIGHTNESS,
        name="Increase Down Light Brightness",
        REDACTED_VALUE"increase_down_light_brightness",
        mutually_exclusive=Action.SET_DOWN_LIGHT_BRIGHTNESS,
        argument=STEP_SIZE,
    ),
    BondButtonEntityDescription(
        key=Action.DECREASE_DOWN_LIGHT_BRIGHTNESS,
        name="Decrease Down Light Brightness",
        REDACTED_VALUE"decrease_down_light_brightness",
        mutually_exclusive=Action.SET_DOWN_LIGHT_BRIGHTNESS,
        argument=STEP_SIZE,
    ),
    BondButtonEntityDescription(
        key=Action.CYCLE_UP_LIGHT_BRIGHTNESS,
        name="Cycle Up Light Brightness",
        REDACTED_VALUE"cycle_up_light_brightness",
        mutually_exclusive=Action.SET_UP_LIGHT_BRIGHTNESS,
        argument=STEP_SIZE,
    ),
    BondButtonEntityDescription(
        key=Action.CYCLE_DOWN_LIGHT_BRIGHTNESS,
        name="Cycle Down Light Brightness",
        REDACTED_VALUE"cycle_down_light_brightness",
        mutually_exclusive=Action.SET_DOWN_LIGHT_BRIGHTNESS,
        argument=STEP_SIZE,
    ),
    BondButtonEntityDescription(
        key=Action.CYCLE_BRIGHTNESS,
        name="Cycle Brightness",
        REDACTED_VALUE"cycle_brightness",
        mutually_exclusive=Action.SET_BRIGHTNESS,
        argument=STEP_SIZE,
    ),
    BondButtonEntityDescription(
        key=Action.INCREASE_SPEED,
        name="Increase Speed",
        REDACTED_VALUE"increase_speed",
        mutually_exclusive=Action.SET_SPEED,
        argument=1,
    ),
    BondButtonEntityDescription(
        key=Action.DECREASE_SPEED,
        name="Decrease Speed",
        REDACTED_VALUE"decrease_speed",
        mutually_exclusive=Action.SET_SPEED,
        argument=1,
    ),
    BondButtonEntityDescription(
        key=Action.TOGGLE_DIRECTION,
        name="Toggle Direction",
        REDACTED_VALUE"toggle_direction",
        mutually_exclusive=Action.SET_DIRECTION,
        argument=None,
    ),
    BondButtonEntityDescription(
        key=Action.INCREASE_TEMPERATURE,
        name="Increase Temperature",
        REDACTED_VALUE"increase_temperature",
        mutually_exclusive=None,
        argument=1,
    ),
    BondButtonEntityDescription(
        key=Action.DECREASE_TEMPERATURE,
        name="Decrease Temperature",
        REDACTED_VALUE"decrease_temperature",
        mutually_exclusive=None,
        argument=1,
    ),
    BondButtonEntityDescription(
        key=Action.INCREASE_FLAME,
        name="Increase Flame",
        REDACTED_VALUE"increase_flame",
        mutually_exclusive=None,
        argument=STEP_SIZE,
    ),
    BondButtonEntityDescription(
        key=Action.DECREASE_FLAME,
        name="Decrease Flame",
        REDACTED_VALUE"decrease_flame",
        mutually_exclusive=None,
        argument=STEP_SIZE,
    ),
    BondButtonEntityDescription(
        key=Action.TOGGLE_OPEN,
        name="Toggle Open",
        mutually_exclusive=Action.OPEN,
        argument=None,
    ),
    BondButtonEntityDescription(
        key=Action.INCREASE_POSITION,
        name="Increase Position",
        REDACTED_VALUE"increase_position",
        mutually_exclusive=Action.SET_POSITION,
        argument=STEP_SIZE,
    ),
    BondButtonEntityDescription(
        key=Action.DECREASE_POSITION,
        name="Decrease Position",
        REDACTED_VALUE"decrease_position",
        mutually_exclusive=Action.SET_POSITION,
        argument=STEP_SIZE,
    ),
    BondButtonEntityDescription(
        key=Action.OPEN_NEXT,
        name="Open Next",
        REDACTED_VALUE"open_next",
        mutually_exclusive=None,
        argument=None,
    ),
    BondButtonEntityDescription(
        key=Action.CLOSE_NEXT,
        name="Close Next",
        REDACTED_VALUE"close_next",
        mutually_exclusive=None,
        argument=None,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: BondConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Bond button devices."""
    data = entry.runtime_data
    entities: list[BondButtonEntity] = []

    for device in data.hub.devices:
        device_entities = [
            BondButtonEntity(data, device, description)
            for description in BUTTONS
            if device.has_action(description.key)
            and (
                description.mutually_exclusive is None
                or not device.has_action(description.mutually_exclusive)
            )
        ]
        if device_entities and device.has_action(STOP_BUTTON.key):
            # Most devices have the stop action available, but
            # we only add the stop action button if we add actions
            # since its not so useful if there are no actions to stop
            device_entities.append(BondButtonEntity(data, device, STOP_BUTTON))
        entities.extend(device_entities)

    async_add_entities(entities)


class BondButtonEntity(BondEntity, ButtonEntity):
    """Bond Button Device."""

    entity_description: BondButtonEntityDescription

    def __init__(
        self,
        data: BondData,
        device: BondDevice,
        description: BondButtonEntityDescription,
    ) -> None:
        """Init Bond button."""
        self.entity_description = description
        super().__init__(data, device, description.name, description.key.lower())

    async def async_press(self) -> None:
        """Press the button."""
        description = self.entity_description
        key = description.key
        if argument := description.argument:
            action = Action(key, argument)
        else:
            action = Action(key)
        await self._bond.action(self._device_id, action)

    def _apply_state(self) -> None:
        """Apply the state."""
