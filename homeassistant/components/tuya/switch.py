"""Support for Tuya switches."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from tuya_sharing import CustomerDevice, Manager

from homeassistant.components.switch import (
    DOMAIN as SWITCH_DOMAIN,
    SwitchDeviceClass,
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.issue_registry import (
    IssueSeverity,
    async_create_issue,
    async_delete_issue,
)

from . import TuyaConfigEntry
from .const import DOMAIN, TUYA_DISCOVERY_NEW, DeviceCategory, DPCode
from .entity import TuyaEntity


@dataclass(frozen=True, kw_only=True)
class TuyaDeprecatedSwitchEntityDescription(SwitchEntityDescription):
    """Describes Tuya deprecated switch entity."""

    deprecated: str
    breaks_in_ha_version: str


# All descriptions can be found here. Mostly the Boolean data types in the
# default instruction set of each category end up being a Switch.
# https://developer.tuya.com/en/docs/iot/standarddescription?id=K9i5ql6waswzq
SWITCHES: dict[DeviceCategory, tuple[SwitchEntityDescription, ...]] = {
    DeviceCategory.BH: (
        SwitchEntityDescription(
            key=DPCode.START,
            REDACTED_VALUE"start",
        ),
        SwitchEntityDescription(
            key=DPCode.WARM,
            REDACTED_VALUE"heat_preservation",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.BZYD: (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            name=None,
        ),
        SwitchEntityDescription(
            key=DPCode.CHILD_LOCK,
            REDACTED_VALUE"child_lock",
            icon="mdi:account-lock",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_MUSIC,
            REDACTED_VALUE"music",
            icon="mdi:music",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.SNOOZE,
            REDACTED_VALUE"snooze",
            icon="mdi:alarm-snooze",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.CL: (
        SwitchEntityDescription(
            key=DPCode.CONTROL_BACK,
            REDACTED_VALUE"reverse",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.OPPOSITE,
            REDACTED_VALUE"reverse",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.CN: (
        SwitchEntityDescription(
            key=DPCode.DISINFECTION,
            REDACTED_VALUE"disinfection",
        ),
        SwitchEntityDescription(
            key=DPCode.WATER,
            REDACTED_VALUE"water",
        ),
    ),
    DeviceCategory.CS: (
        SwitchEntityDescription(
            key=DPCode.ANION,
            REDACTED_VALUE"ionizer",
            icon="mdi:atom",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.CHILD_LOCK,
            REDACTED_VALUE"child_lock",
            icon="mdi:account-lock",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.FILTER_RESET,
            REDACTED_VALUE"filter_reset",
            icon="mdi:filter",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.CWJWQ: (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
        ),
    ),
    DeviceCategory.CWWSQ: (
        SwitchEntityDescription(
            key=DPCode.SLOW_FEED,
            REDACTED_VALUE"slow_feed",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.CWYSJ: (
        SwitchEntityDescription(
            key=DPCode.FILTER_RESET,
            REDACTED_VALUE"filter_reset",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.PUMP_RESET,
            REDACTED_VALUE"water_pump_reset",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"power",
        ),
        SwitchEntityDescription(
            key=DPCode.WATER_RESET,
            REDACTED_VALUE"reset_of_water_usage_days",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.UV,
            REDACTED_VALUE"uv_sterilization",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.DJ: (
        # There are sockets available with an RGB light
        # that advertise as `dj`, but provide an additional
        # switch to control the plug.
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"plug",
        ),
    ),
    DeviceCategory.DLQ: (
        SwitchEntityDescription(
            key=DPCode.CHILD_LOCK,
            REDACTED_VALUE"child_lock",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
        ),
    ),
    DeviceCategory.DR: (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            name="Power",
            icon="mdi:power",
            device_class=SwitchDeviceClass.SWITCH,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_1,
            name="Side A Power",
            icon="mdi:alpha-a",
            device_class=SwitchDeviceClass.SWITCH,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_2,
            name="Side B Power",
            icon="mdi:alpha-b",
            device_class=SwitchDeviceClass.SWITCH,
        ),
        SwitchEntityDescription(
            key=DPCode.PREHEAT,
            name="Preheat",
            icon="mdi:radiator",
            device_class=SwitchDeviceClass.SWITCH,
        ),
        SwitchEntityDescription(
            key=DPCode.PREHEAT_1,
            name="Side A Preheat",
            icon="mdi:radiator",
            device_class=SwitchDeviceClass.SWITCH,
        ),
        SwitchEntityDescription(
            key=DPCode.PREHEAT_2,
            name="Side B Preheat",
            icon="mdi:radiator",
            device_class=SwitchDeviceClass.SWITCH,
        ),
    ),
    DeviceCategory.FS: (
        SwitchEntityDescription(
            key=DPCode.ANION,
            REDACTED_VALUE"anion",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.HUMIDIFIER,
            REDACTED_VALUE"humidification",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.OXYGEN,
            REDACTED_VALUE"oxygen_bar",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.FAN_COOL,
            REDACTED_VALUE"natural_wind",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.FAN_BEEP,
            REDACTED_VALUE"sound",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.CHILD_LOCK,
            REDACTED_VALUE"child_lock",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.FSD: (
        SwitchEntityDescription(
            key=DPCode.FAN_BEEP,
            REDACTED_VALUE"sound",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.GGQ: (
        SwitchEntityDescription(
            key=DPCode.SWITCH_1,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "1"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_2,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "2"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_3,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "3"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_4,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "4"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_5,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "5"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_6,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "6"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_7,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "7"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_8,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "8"},
        ),
    ),
    DeviceCategory.HXD: (
        SwitchEntityDescription(
            key=DPCode.SWITCH_1,
            REDACTED_VALUE"radio",
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_2,
            REDACTED_VALUE"indexed_alarm",
            translation_placeholders={"index": "1"},
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_3,
            REDACTED_VALUE"indexed_alarm",
            translation_placeholders={"index": "2"},
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_4,
            REDACTED_VALUE"indexed_alarm",
            translation_placeholders={"index": "3"},
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_5,
            REDACTED_VALUE"indexed_alarm",
            translation_placeholders={"index": "4"},
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_6,
            REDACTED_VALUE"sleep_aid",
        ),
    ),
    DeviceCategory.JSQ: (
        SwitchEntityDescription(
            key=DPCode.SWITCH_SOUND,
            REDACTED_VALUE"voice",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.SLEEP,
            REDACTED_VALUE"sleep",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.STERILIZATION,
            REDACTED_VALUE"sterilization",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.KG: (
        SwitchEntityDescription(
            key=DPCode.CHILD_LOCK,
            REDACTED_VALUE"child_lock",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_1,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "1"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_2,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "2"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_3,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "3"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_4,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "4"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_5,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "5"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_6,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "6"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_7,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "7"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_8,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "8"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_USB1,
            REDACTED_VALUE"indexed_usb",
            translation_placeholders={"index": "1"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_USB2,
            REDACTED_VALUE"indexed_usb",
            translation_placeholders={"index": "2"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_USB3,
            REDACTED_VALUE"indexed_usb",
            translation_placeholders={"index": "3"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_USB4,
            REDACTED_VALUE"indexed_usb",
            translation_placeholders={"index": "4"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_USB5,
            REDACTED_VALUE"indexed_usb",
            translation_placeholders={"index": "5"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_USB6,
            REDACTED_VALUE"indexed_usb",
            translation_placeholders={"index": "6"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
            device_class=SwitchDeviceClass.OUTLET,
        ),
    ),
    DeviceCategory.KJ: (
        SwitchEntityDescription(
            key=DPCode.ANION,
            REDACTED_VALUE"ionizer",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.FILTER_RESET,
            REDACTED_VALUE"filter_cartridge_reset",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.LOCK,
            REDACTED_VALUE"child_lock",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"power",
        ),
        SwitchEntityDescription(
            key=DPCode.WET,
            REDACTED_VALUE"humidification",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.UV,
            REDACTED_VALUE"uv_sterilization",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.KT: (
        SwitchEntityDescription(
            key=DPCode.ANION,
            REDACTED_VALUE"ionizer",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.LOCK,
            REDACTED_VALUE"child_lock",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.KS: (
        SwitchEntityDescription(
            key=DPCode.ANION,
            REDACTED_VALUE"ionizer",
        ),
    ),
    DeviceCategory.MAL: (
        SwitchEntityDescription(
            key=DPCode.SWITCH_ALARM_SOUND,
            # This switch is called "Arm Beep" in the official Tuya app
            REDACTED_VALUE"arm_beep",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_ALARM_LIGHT,
            # This switch is called "Siren" in the official Tuya app
            REDACTED_VALUE"siren",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.MZJ: (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.START,
            REDACTED_VALUE"start",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.PC: (
        SwitchEntityDescription(
            key=DPCode.CHILD_LOCK,
            REDACTED_VALUE"child_lock",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_1,
            REDACTED_VALUE"indexed_socket",
            translation_placeholders={"index": "1"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_2,
            REDACTED_VALUE"indexed_socket",
            translation_placeholders={"index": "2"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_3,
            REDACTED_VALUE"indexed_socket",
            translation_placeholders={"index": "3"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_4,
            REDACTED_VALUE"indexed_socket",
            translation_placeholders={"index": "4"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_5,
            REDACTED_VALUE"indexed_socket",
            translation_placeholders={"index": "5"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_6,
            REDACTED_VALUE"indexed_socket",
            translation_placeholders={"index": "6"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_USB1,
            REDACTED_VALUE"indexed_usb",
            translation_placeholders={"index": "1"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_USB2,
            REDACTED_VALUE"indexed_usb",
            translation_placeholders={"index": "2"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_USB3,
            REDACTED_VALUE"indexed_usb",
            translation_placeholders={"index": "3"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_USB4,
            REDACTED_VALUE"indexed_usb",
            translation_placeholders={"index": "4"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_USB5,
            REDACTED_VALUE"indexed_usb",
            translation_placeholders={"index": "5"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_USB6,
            REDACTED_VALUE"indexed_usb",
            translation_placeholders={"index": "6"},
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"socket",
            device_class=SwitchDeviceClass.OUTLET,
        ),
    ),
    DeviceCategory.QCCDZ: (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
        ),
    ),
    DeviceCategory.QJDCZ: (
        SwitchEntityDescription(
            key=DPCode.SWITCH_1,
            REDACTED_VALUE"switch",
        ),
    ),
    DeviceCategory.QN: (
        SwitchEntityDescription(
            key=DPCode.ANION,
            REDACTED_VALUE"ionizer",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.LOCK,
            REDACTED_VALUE"child_lock",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.QXJ: (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
            device_class=SwitchDeviceClass.OUTLET,
        ),
    ),
    DeviceCategory.SD: (
        SwitchEntityDescription(
            key=DPCode.SWITCH_DISTURB,
            REDACTED_VALUE"do_not_disturb",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.VOICE_SWITCH,
            REDACTED_VALUE"mute_voice",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.SFKZQ: (
        TuyaDeprecatedSwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
            deprecated="deprecated_entity_new_valve",
            breaks_in_ha_version="2026.4.0",
        ),
    ),
    DeviceCategory.SGBJ: (
        SwitchEntityDescription(
            key=DPCode.MUFFLING,
            REDACTED_VALUE"mute",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.SJZ: (
        SwitchEntityDescription(
            key=DPCode.CHILD_LOCK,
            REDACTED_VALUE"child_lock",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.SP: (
        SwitchEntityDescription(
            key=DPCode.WIRELESS_BATTERYLOCK,
            REDACTED_VALUE"battery_lock",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.CRY_DETECTION_SWITCH,
            REDACTED_VALUE"cry_detection",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.DECIBEL_SWITCH,
            REDACTED_VALUE"sound_detection",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.RECORD_SWITCH,
            REDACTED_VALUE"video_recording",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.MOTION_RECORD,
            REDACTED_VALUE"motion_recording",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.BASIC_PRIVATE,
            REDACTED_VALUE"privacy_mode",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.BASIC_FLIP,
            REDACTED_VALUE"flip",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.BASIC_OSD,
            REDACTED_VALUE"time_watermark",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.BASIC_WDR,
            REDACTED_VALUE"wide_dynamic_range",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.MOTION_TRACKING,
            REDACTED_VALUE"motion_tracking",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.MOTION_SWITCH,
            REDACTED_VALUE"motion_alarm",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.SZ: (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"power",
        ),
        SwitchEntityDescription(
            key=DPCode.PUMP,
            REDACTED_VALUE"pump",
        ),
    ),
    DeviceCategory.SZJQR: (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
        ),
    ),
    DeviceCategory.TDQ: (
        SwitchEntityDescription(
            key=DPCode.SWITCH_1,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "1"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_2,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "2"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_3,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "3"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_4,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "4"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_5,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "5"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_6,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "6"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.CHILD_LOCK,
            REDACTED_VALUE"child_lock",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.TYNDJ: (
        SwitchEntityDescription(
            key=DPCode.SWITCH_SAVE_ENERGY,
            REDACTED_VALUE"energy_saving",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.WG2: (
        SwitchEntityDescription(
            key=DPCode.MUFFLING,
            REDACTED_VALUE"mute",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.WK: (
        SwitchEntityDescription(
            key=DPCode.CHILD_LOCK,
            REDACTED_VALUE"child_lock",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.FROST,
            REDACTED_VALUE"frost_protection",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.WKCZ: (
        SwitchEntityDescription(
            key=DPCode.SWITCH_1,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "1"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_2,
            REDACTED_VALUE"indexed_switch",
            translation_placeholders={"index": "2"},
            device_class=SwitchDeviceClass.OUTLET,
        ),
    ),
    DeviceCategory.WKF: (
        SwitchEntityDescription(
            key=DPCode.CHILD_LOCK,
            REDACTED_VALUE"child_lock",
            entity_category=EntityCategory.CONFIG,
        ),
        SwitchEntityDescription(
            key=DPCode.WINDOW_CHECK,
            REDACTED_VALUE"open_window_detection",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.WNYKQ: (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            name=None,
        ),
    ),
    DeviceCategory.WSDCG: (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
            device_class=SwitchDeviceClass.OUTLET,
        ),
    ),
    DeviceCategory.XDD: (
        SwitchEntityDescription(
            key=DPCode.DO_NOT_DISTURB,
            REDACTED_VALUE"do_not_disturb",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.XNYJCN: (
        SwitchEntityDescription(
            key=DPCode.FEEDIN_POWER_LIMIT_ENABLE,
            REDACTED_VALUE"output_power_limit",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.XXJ: (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"power",
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_SPRAY,
            REDACTED_VALUE"spray",
        ),
        SwitchEntityDescription(
            key=DPCode.SWITCH_VOICE,
            REDACTED_VALUE"voice",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.YWBJ: (
        SwitchEntityDescription(
            key=DPCode.MUFFLING,
            REDACTED_VALUE"mute",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    DeviceCategory.ZNDB: (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
        ),
    ),
    DeviceCategory.ZNJXS: (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
        ),
    ),
    DeviceCategory.ZNRB: (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
        ),
    ),
}

# Socket (duplicate of `pc`)
SWITCHES[DeviceCategory.CZ] = SWITCHES[DeviceCategory.PC]

# Smart Camera - Low power consumption camera (duplicate of `sp`)
SWITCHES[DeviceCategory.DGHSXJ] = SWITCHES[DeviceCategory.SP]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TuyaConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up tuya sensors dynamically through tuya discovery."""
    manager = entry.runtime_data.manager
    entity_registry = er.async_get(hass)

    @callback
    def async_discover_device(device_ids: list[str]) -> None:
        """Discover and add a discovered tuya sensor."""
        entities: list[TuyaSwitchEntity] = []
        for device_id in device_ids:
            device = manager.device_map[device_id]
            if descriptions := SWITCHES.get(device.category):
                entities.extend(
                    TuyaSwitchEntity(device, manager, description)
                    for description in descriptions
                    if description.key in device.status
                    and _check_deprecation(
                        hass,
                        device,
                        description,
                        entity_registry,
                    )
                )

        async_add_entities(entities)

    async_discover_device([*manager.device_map])

    entry.async_on_unload(
        async_dispatcher_connect(hass, TUYA_DISCOVERY_NEW, async_discover_device)
    )


def _check_deprecation(
    hass: HomeAssistant,
    device: CustomerDevice,
    description: SwitchEntityDescription,
    entity_registry: er.EntityRegistry,
) -> bool:
    """Check entity deprecation.

    Returns:
        `True` if the entity should be created, `False` otherwise.
    """
    # Not deprecated, just create it
    if not isinstance(description, TuyaDeprecatedSwitchEntityDescription):
        return True

    unique_id = f"tuya.{device.id}{description.key}"
    entity_id = entity_registry.async_get_entity_id(SWITCH_DOMAIN, DOMAIN, unique_id)

    # Deprecated and not present in registry, skip creation
    if not entity_id or not (entity_entry := entity_registry.async_get(entity_id)):
        return False

    # Deprecated and present in registry but disabled, remove it and skip creation
    if entity_entry.disabled:
        entity_registry.async_remove(entity_id)
        async_delete_issue(
            hass,
            DOMAIN,
            f"deprecated_entity_{unique_id}",
        )
        return False

    # Deprecated and present in registry and enabled, raise issue and create it
    async_create_issue(
        hass,
        DOMAIN,
        f"deprecated_entity_{unique_id}",
        breaks_in_ha_version=description.breaks_in_ha_version,
        is_fixable=False,
        severity=IssueSeverity.WARNING,
        REDACTED_VALUEdescription.deprecated,
        translation_placeholders={
            "name": f"{device.name} {entity_entry.name or entity_entry.original_name}",
            "entity": entity_id,
        },
    )
    return True


class TuyaSwitchEntity(TuyaEntity, SwitchEntity):
    """Tuya Switch Device."""

    def __init__(
        self,
        device: CustomerDevice,
        device_manager: Manager,
        description: SwitchEntityDescription,
    ) -> None:
        """Init TuyaHaSwitch."""
        super().__init__(device, device_manager)
        self.entity_description = description
        self._attr_unique_id = f"{super().unique_id}{description.key}"

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self.device.status.get(self.entity_description.key, False)

    def turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        self._send_command([{"code": self.entity_description.key, "value": True}])

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        self._send_command([{"code": self.entity_description.key, "value": False}])
