"""Button platform for LG IR integration."""

from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.components.infrared import (
    DATA_COMPONENT,
    InfraredEntity,
    NECInfraredCommand,
    NECInfraredProtocol,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.core import Event, EventStateChangedData, HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    CONF_DEVICE_TYPE,
    CONF_INFRARED_ENTITY_ID,
    DOMAIN,
    LG_ADDRESS,
    LGDeviceType,
    LGTVCommand,
)

_LOGGER = logging.getLogger(__name__)

LG_PROTOCOL = NECInfraredProtocol()


@dataclass(frozen=True, kw_only=True)
class LgIrButtonEntityDescription(ButtonEntityDescription):
    """Describes LG IR button entity."""

    command_code: int


TV_BUTTON_DESCRIPTIONS: tuple[LgIrButtonEntityDescription, ...] = (
    LgIrButtonEntityDescription(
        key="power_on",
        REDACTED_VALUE"power_on",
        command_code=LGTVCommand.POWER_ON,
    ),
    LgIrButtonEntityDescription(
        key="power_off",
        REDACTED_VALUE"power_off",
        command_code=LGTVCommand.POWER_OFF,
    ),
    LgIrButtonEntityDescription(
        key="hdmi_1",
        REDACTED_VALUE"hdmi_1",
        command_code=LGTVCommand.HDMI_1,
    ),
    LgIrButtonEntityDescription(
        key="hdmi_2",
        REDACTED_VALUE"hdmi_2",
        command_code=LGTVCommand.HDMI_2,
    ),
    LgIrButtonEntityDescription(
        key="hdmi_3",
        REDACTED_VALUE"hdmi_3",
        command_code=LGTVCommand.HDMI_3,
    ),
    LgIrButtonEntityDescription(
        key="hdmi_4",
        REDACTED_VALUE"hdmi_4",
        command_code=LGTVCommand.HDMI_4,
    ),
    LgIrButtonEntityDescription(
        key="exit",
        REDACTED_VALUE"exit",
        command_code=LGTVCommand.EXIT,
    ),
    LgIrButtonEntityDescription(
        key="info",
        REDACTED_VALUE"info",
        command_code=LGTVCommand.INFO,
    ),
    LgIrButtonEntityDescription(
        key="guide",
        REDACTED_VALUE"guide",
        command_code=LGTVCommand.GUIDE,
    ),
    LgIrButtonEntityDescription(
        key="up",
        REDACTED_VALUE"up",
        command_code=LGTVCommand.NAV_UP,
    ),
    LgIrButtonEntityDescription(
        key="down",
        REDACTED_VALUE"down",
        command_code=LGTVCommand.NAV_DOWN,
    ),
    LgIrButtonEntityDescription(
        key="left",
        REDACTED_VALUE"left",
        command_code=LGTVCommand.NAV_LEFT,
    ),
    LgIrButtonEntityDescription(
        key="right",
        REDACTED_VALUE"right",
        command_code=LGTVCommand.NAV_RIGHT,
    ),
    LgIrButtonEntityDescription(
        key="ok",
        REDACTED_VALUE"ok",
        command_code=LGTVCommand.OK,
    ),
    LgIrButtonEntityDescription(
        key="back",
        REDACTED_VALUE"back",
        command_code=LGTVCommand.BACK,
    ),
    LgIrButtonEntityDescription(
        key="home",
        REDACTED_VALUE"home",
        command_code=LGTVCommand.HOME,
    ),
    LgIrButtonEntityDescription(
        key="menu",
        REDACTED_VALUE"menu",
        command_code=LGTVCommand.MENU,
    ),
    LgIrButtonEntityDescription(
        key="input",
        REDACTED_VALUE"input",
        command_code=LGTVCommand.INPUT,
    ),
    LgIrButtonEntityDescription(
        key="num_0",
        REDACTED_VALUE"num_0",
        command_code=LGTVCommand.NUM_0,
    ),
    LgIrButtonEntityDescription(
        key="num_1",
        REDACTED_VALUE"num_1",
        command_code=LGTVCommand.NUM_1,
    ),
    LgIrButtonEntityDescription(
        key="num_2",
        REDACTED_VALUE"num_2",
        command_code=LGTVCommand.NUM_2,
    ),
    LgIrButtonEntityDescription(
        key="num_3",
        REDACTED_VALUE"num_3",
        command_code=LGTVCommand.NUM_3,
    ),
    LgIrButtonEntityDescription(
        key="num_4",
        REDACTED_VALUE"num_4",
        command_code=LGTVCommand.NUM_4,
    ),
    LgIrButtonEntityDescription(
        key="num_5",
        REDACTED_VALUE"num_5",
        command_code=LGTVCommand.NUM_5,
    ),
    LgIrButtonEntityDescription(
        key="num_6",
        REDACTED_VALUE"num_6",
        command_code=LGTVCommand.NUM_6,
    ),
    LgIrButtonEntityDescription(
        key="num_7",
        REDACTED_VALUE"num_7",
        command_code=LGTVCommand.NUM_7,
    ),
    LgIrButtonEntityDescription(
        key="num_8",
        REDACTED_VALUE"num_8",
        command_code=LGTVCommand.NUM_8,
    ),
    LgIrButtonEntityDescription(
        key="num_9",
        REDACTED_VALUE"num_9",
        command_code=LGTVCommand.NUM_9,
    ),
)

HIFI_BUTTON_DESCRIPTIONS: tuple[LgIrButtonEntityDescription, ...] = (
    LgIrButtonEntityDescription(
        key="power_on",
        REDACTED_VALUE"power_on",
        command_code=LGTVCommand.POWER_ON,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up LG IR buttons from config entry."""
    infrared_entity_id = entry.data[CONF_INFRARED_ENTITY_ID]
    device_type = entry.data.get(CONF_DEVICE_TYPE, LGDeviceType.TV)
    if device_type == LGDeviceType.TV:
        async_add_entities(
            LgIrButton(entry, infrared_entity_id, description)
            for description in TV_BUTTON_DESCRIPTIONS
        )


class LgIrButton(ButtonEntity):
    """LG IR button entity."""

    _attr_has_entity_name = True
    _description: LgIrButtonEntityDescription

    def __init__(
        self,
        entry: ConfigEntry,
        infrared_entity_id: str,
        description: LgIrButtonEntityDescription,
    ) -> None:
        """Initialize LG IR button."""
        self._entry = entry
        self._infrared_entity_id = infrared_entity_id
        self._description = description
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)}, name="LG TV", manufacturer="LG"
        )

    async def async_added_to_hass(self) -> None:
        """Subscribe to infrared entity state changes."""
        await super().async_added_to_hass()

        @callback
        def _async_ir_state_changed(event: Event[EventStateChangedData]) -> None:
            """Handle infrared entity state changes."""
            new_state = event.data["new_state"]
            self._attr_available = (
                new_state is not None and new_state.state != STATE_UNAVAILABLE
            )
            self.async_write_ha_state()

        self.async_on_remove(
            async_track_state_change_event(
                self.hass, [self._infrared_entity_id], _async_ir_state_changed
            )
        )

        # Set initial availability based on current infrared entity state
        ir_state = self.hass.states.get(self._infrared_entity_id)
        self._attr_available = (
            ir_state is not None and ir_state.state != STATE_UNAVAILABLE
        )

    def _get_infrared_entity(self) -> InfraredEntity | None:
        """Get the infrared entity."""
        component = self.hass.data.get(DATA_COMPONENT)
        if component is None:
            return None
        return component.get_entity(self._infrared_entity_id)

    async def async_press(self) -> None:
        """Press the button."""
        entity = self._get_infrared_entity()
        if entity is None:
            _LOGGER.error("Infrared entity %s not found", self._infrared_entity_id)
            return

        command = NECInfraredCommand(
            address=LG_ADDRESS,
            command=self._description.command_code,
            protocol=LG_PROTOCOL,
            repeat_count=1,
        )
        await entity.async_send_command(command)
