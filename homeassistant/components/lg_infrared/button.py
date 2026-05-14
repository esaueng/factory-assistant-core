"""Button platform for LG IR integration."""

from dataclasses import dataclass

from infrared_protocols.codes.lg.tv import LGTVCode

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_DEVICE_TYPE, CONF_INFRARED_ENTITY_ID, LGDeviceType
from .entity import LgIrEntity

PARALLEL_UPDATES = 1


@dataclass(frozen=True, kw_only=True)
class LgIrButtonEntityDescription(ButtonEntityDescription):
    """Describes LG IR button entity."""

    command_code: LGTVCode


TV_BUTTON_DESCRIPTIONS: tuple[LgIrButtonEntityDescription, ...] = (
    LgIrButtonEntityDescription(
        key="power", REDACTED_VALUE"power", command_code=LGTVCode.POWER
    ),
    LgIrButtonEntityDescription(
        key="power_on", REDACTED_VALUE"power_on", command_code=LGTVCode.POWER_ON
    ),
    LgIrButtonEntityDescription(
        key="power_off", REDACTED_VALUE"power_off", command_code=LGTVCode.POWER_OFF
    ),
    LgIrButtonEntityDescription(
        key="hdmi_1", REDACTED_VALUE"hdmi_1", command_code=LGTVCode.HDMI_1
    ),
    LgIrButtonEntityDescription(
        key="hdmi_2", REDACTED_VALUE"hdmi_2", command_code=LGTVCode.HDMI_2
    ),
    LgIrButtonEntityDescription(
        key="hdmi_3", REDACTED_VALUE"hdmi_3", command_code=LGTVCode.HDMI_3
    ),
    LgIrButtonEntityDescription(
        key="hdmi_4", REDACTED_VALUE"hdmi_4", command_code=LGTVCode.HDMI_4
    ),
    LgIrButtonEntityDescription(
        key="exit", REDACTED_VALUE"exit", command_code=LGTVCode.EXIT
    ),
    LgIrButtonEntityDescription(
        key="info", REDACTED_VALUE"info", command_code=LGTVCode.INFO
    ),
    LgIrButtonEntityDescription(
        key="guide", REDACTED_VALUE"guide", command_code=LGTVCode.GUIDE
    ),
    LgIrButtonEntityDescription(
        key="up", REDACTED_VALUE"up", command_code=LGTVCode.NAV_UP
    ),
    LgIrButtonEntityDescription(
        key="down", REDACTED_VALUE"down", command_code=LGTVCode.NAV_DOWN
    ),
    LgIrButtonEntityDescription(
        key="left", REDACTED_VALUE"left", command_code=LGTVCode.NAV_LEFT
    ),
    LgIrButtonEntityDescription(
        key="right", REDACTED_VALUE"right", command_code=LGTVCode.NAV_RIGHT
    ),
    LgIrButtonEntityDescription(
        key="ok", REDACTED_VALUE"ok", command_code=LGTVCode.OK
    ),
    LgIrButtonEntityDescription(
        key="back", REDACTED_VALUE"back", command_code=LGTVCode.BACK
    ),
    LgIrButtonEntityDescription(
        key="home", REDACTED_VALUE"home", command_code=LGTVCode.HOME
    ),
    LgIrButtonEntityDescription(
        key="menu", REDACTED_VALUE"menu", command_code=LGTVCode.MENU
    ),
    LgIrButtonEntityDescription(
        key="input", REDACTED_VALUE"input", command_code=LGTVCode.INPUT
    ),
    LgIrButtonEntityDescription(
        key="num_0", REDACTED_VALUE"num_0", command_code=LGTVCode.NUM_0
    ),
    LgIrButtonEntityDescription(
        key="num_1", REDACTED_VALUE"num_1", command_code=LGTVCode.NUM_1
    ),
    LgIrButtonEntityDescription(
        key="num_2", REDACTED_VALUE"num_2", command_code=LGTVCode.NUM_2
    ),
    LgIrButtonEntityDescription(
        key="num_3", REDACTED_VALUE"num_3", command_code=LGTVCode.NUM_3
    ),
    LgIrButtonEntityDescription(
        key="num_4", REDACTED_VALUE"num_4", command_code=LGTVCode.NUM_4
    ),
    LgIrButtonEntityDescription(
        key="num_5", REDACTED_VALUE"num_5", command_code=LGTVCode.NUM_5
    ),
    LgIrButtonEntityDescription(
        key="num_6", REDACTED_VALUE"num_6", command_code=LGTVCode.NUM_6
    ),
    LgIrButtonEntityDescription(
        key="num_7", REDACTED_VALUE"num_7", command_code=LGTVCode.NUM_7
    ),
    LgIrButtonEntityDescription(
        key="num_8", REDACTED_VALUE"num_8", command_code=LGTVCode.NUM_8
    ),
    LgIrButtonEntityDescription(
        key="num_9", REDACTED_VALUE"num_9", command_code=LGTVCode.NUM_9
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up LG IR buttons from config entry."""
    infrared_entity_id = entry.data[CONF_INFRARED_ENTITY_ID]
    device_type = entry.data[CONF_DEVICE_TYPE]
    if device_type == LGDeviceType.TV:
        async_add_entities(
            LgIrButton(entry, infrared_entity_id, description)
            for description in TV_BUTTON_DESCRIPTIONS
        )


class LgIrButton(LgIrEntity, ButtonEntity):
    """LG IR button entity."""

    entity_description: LgIrButtonEntityDescription

    def __init__(
        self,
        entry: ConfigEntry,
        infrared_entity_id: str,
        description: LgIrButtonEntityDescription,
    ) -> None:
        """Initialize LG IR button."""
        super().__init__(entry, infrared_entity_id, unique_id_suffix=description.key)
        self.entity_description = description

    async def async_press(self) -> None:
        """Press the button."""
        await self._send_command(self.entity_description.command_code)
