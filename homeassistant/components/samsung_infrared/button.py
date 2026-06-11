"""Button platform for Samsung IR integration."""

from dataclasses import dataclass

from infrared_protocols.codes.samsung.tv import SamsungTVCode

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.components.infrared import InfraredEmitterConsumerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_DEVICE_TYPE, CONF_INFRARED_EMITTER_ENTITY_ID, SamsungDeviceType
from .entity import SamsungIrEntity

PARALLEL_UPDATES = 1


@dataclass(frozen=True, kw_only=True)
class SamsungIrButtonEntityDescription(ButtonEntityDescription):
    """Describes Samsung IR button entity."""

    command_code: SamsungTVCode


TV_BUTTON_DESCRIPTIONS: tuple[SamsungIrButtonEntityDescription, ...] = (
    SamsungIrButtonEntityDescription(
        key="power", REDACTED_VALUE"power", command_code=SamsungTVCode.POWER
    ),
    SamsungIrButtonEntityDescription(
        key="source", REDACTED_VALUE"source", command_code=SamsungTVCode.SOURCE
    ),
    SamsungIrButtonEntityDescription(
        key="settings", REDACTED_VALUE"settings", command_code=SamsungTVCode.SETTINGS
    ),
    SamsungIrButtonEntityDescription(
        key="info", REDACTED_VALUE"info", command_code=SamsungTVCode.INFO
    ),
    SamsungIrButtonEntityDescription(
        key="exit", REDACTED_VALUE"exit", command_code=SamsungTVCode.EXIT
    ),
    SamsungIrButtonEntityDescription(
        key="return", REDACTED_VALUE"return", command_code=SamsungTVCode.RETURN
    ),
    SamsungIrButtonEntityDescription(
        key="home", REDACTED_VALUE"home", command_code=SamsungTVCode.HOME
    ),
    SamsungIrButtonEntityDescription(
        key="red", REDACTED_VALUE"red", command_code=SamsungTVCode.RED
    ),
    SamsungIrButtonEntityDescription(
        key="green", REDACTED_VALUE"green", command_code=SamsungTVCode.GREEN
    ),
    SamsungIrButtonEntityDescription(
        key="yellow", REDACTED_VALUE"yellow", command_code=SamsungTVCode.YELLOW
    ),
    SamsungIrButtonEntityDescription(
        key="blue", REDACTED_VALUE"blue", command_code=SamsungTVCode.BLUE
    ),
    SamsungIrButtonEntityDescription(
        key="up", REDACTED_VALUE"up", command_code=SamsungTVCode.NAV_UP
    ),
    SamsungIrButtonEntityDescription(
        key="down", REDACTED_VALUE"down", command_code=SamsungTVCode.NAV_DOWN
    ),
    SamsungIrButtonEntityDescription(
        key="left", REDACTED_VALUE"left", command_code=SamsungTVCode.NAV_LEFT
    ),
    SamsungIrButtonEntityDescription(
        key="right", REDACTED_VALUE"right", command_code=SamsungTVCode.NAV_RIGHT
    ),
    SamsungIrButtonEntityDescription(
        key="ok", REDACTED_VALUE"ok", command_code=SamsungTVCode.OK
    ),
    SamsungIrButtonEntityDescription(
        key="previous_channel",
        REDACTED_VALUE"previous_channel",
        command_code=SamsungTVCode.PREVIOUS_CHANNEL,
    ),
    SamsungIrButtonEntityDescription(
        key="num_0", REDACTED_VALUE"num_0", command_code=SamsungTVCode.NUM_0
    ),
    SamsungIrButtonEntityDescription(
        key="num_1", REDACTED_VALUE"num_1", command_code=SamsungTVCode.NUM_1
    ),
    SamsungIrButtonEntityDescription(
        key="num_2", REDACTED_VALUE"num_2", command_code=SamsungTVCode.NUM_2
    ),
    SamsungIrButtonEntityDescription(
        key="num_3", REDACTED_VALUE"num_3", command_code=SamsungTVCode.NUM_3
    ),
    SamsungIrButtonEntityDescription(
        key="num_4", REDACTED_VALUE"num_4", command_code=SamsungTVCode.NUM_4
    ),
    SamsungIrButtonEntityDescription(
        key="num_5", REDACTED_VALUE"num_5", command_code=SamsungTVCode.NUM_5
    ),
    SamsungIrButtonEntityDescription(
        key="num_6", REDACTED_VALUE"num_6", command_code=SamsungTVCode.NUM_6
    ),
    SamsungIrButtonEntityDescription(
        key="num_7", REDACTED_VALUE"num_7", command_code=SamsungTVCode.NUM_7
    ),
    SamsungIrButtonEntityDescription(
        key="num_8", REDACTED_VALUE"num_8", command_code=SamsungTVCode.NUM_8
    ),
    SamsungIrButtonEntityDescription(
        key="num_9", REDACTED_VALUE"num_9", command_code=SamsungTVCode.NUM_9
    ),
    SamsungIrButtonEntityDescription(
        key="fast_forward",
        REDACTED_VALUE"fast_forward",
        command_code=SamsungTVCode.FAST_FORWARD,
    ),
    SamsungIrButtonEntityDescription(
        key="rewind", REDACTED_VALUE"rewind", command_code=SamsungTVCode.REWIND
    ),
    SamsungIrButtonEntityDescription(
        key="record", REDACTED_VALUE"record", command_code=SamsungTVCode.RECORD
    ),
    SamsungIrButtonEntityDescription(
        key="tools", REDACTED_VALUE"tools", command_code=SamsungTVCode.TOOLS
    ),
    SamsungIrButtonEntityDescription(
        key="browser", REDACTED_VALUE"browser", command_code=SamsungTVCode.BROWSER
    ),
    SamsungIrButtonEntityDescription(
        key="ad_subtitle",
        REDACTED_VALUE"ad_subtitle",
        command_code=SamsungTVCode.AD_SUBTITLE,
    ),
    SamsungIrButtonEntityDescription(
        key="e_manual",
        REDACTED_VALUE"e_manual",
        command_code=SamsungTVCode.E_MANUAL,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Samsung IR buttons from config entry."""
    infrared_emitter_entity_id = entry.data[CONF_INFRARED_EMITTER_ENTITY_ID]
    device_type = entry.data[CONF_DEVICE_TYPE]
    if device_type != SamsungDeviceType.TV:
        return
    async_add_entities(
        [
            SamsungIrButton(entry, infrared_emitter_entity_id, description)
            for description in TV_BUTTON_DESCRIPTIONS
        ]
    )


class SamsungIrButton(SamsungIrEntity, InfraredEmitterConsumerEntity, ButtonEntity):
    """Samsung IR button entity."""

    entity_description: SamsungIrButtonEntityDescription

    def __init__(
        self,
        entry: ConfigEntry,
        infrared_emitter_entity_id: str,
        description: SamsungIrButtonEntityDescription,
    ) -> None:
        """Initialize Samsung IR button."""
        super().__init__(entry, unique_id_suffix=description.key)
        self._infrared_emitter_entity_id = infrared_emitter_entity_id
        self.entity_description = description

    async def async_press(self) -> None:
        """Press the button."""
        await self._send_command(self.entity_description.command_code.to_command())
