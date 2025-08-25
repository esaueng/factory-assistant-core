"""Support for Tuya switches."""

from __future__ import annotations

from typing import Any

from tuya_sharing import CustomerDevice, Manager

from homeassistant.components.switch import (
    SwitchDeviceClass,
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TuyaConfigEntry
from .const import TUYA_DISCOVERY_NEW, DPCode
from .entity import TuyaEntity

# All descriptions can be found here. Mostly the Boolean data types in the
# default instruction set of each category end up being a Switch.
# https://developer.tuya.com/en/docs/iot/standarddescription?id=K9i5ql6waswzq
SWITCHES: dict[str, tuple[SwitchEntityDescription, ...]] = {
    # Smart Kettle
    # https://developer.tuya.com/en/docs/iot/fbh?id=K9gf484m21yq7
    "bh": (
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
    # Curtain
    # https://developer.tuya.com/en/docs/iot/f?id=K9gf46o5mtfyc
    "cl": (
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
    # EasyBaby
    # Undocumented, might have a wider use
    "cn": (
        SwitchEntityDescription(
            key=DPCode.DISINFECTION,
            REDACTED_VALUE"disinfection",
        ),
        SwitchEntityDescription(
            key=DPCode.WATER,
            REDACTED_VALUE"water",
        ),
    ),
    # Dehumidifier
    # https://developer.tuya.com/en/docs/iot/s?id=K9gf48r6jke8e
    "cs": (
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
    # Smart Odor Eliminator-Pro
    # Undocumented, see https://github.com/orgs/home-assistant/discussions/79
    "cwjwq": (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
        ),
    ),
    # Smart Pet Feeder
    # https://developer.tuya.com/en/docs/iot/categorycwwsq?id=Kaiuz2b6vydld
    "cwwsq": (
        SwitchEntityDescription(
            key=DPCode.SLOW_FEED,
            REDACTED_VALUE"slow_feed",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    # Pet Fountain
    # https://developer.tuya.com/en/docs/iot/f?id=K9gf46aewxem5
    "cwysj": (
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
    # Light
    # https://developer.tuya.com/en/docs/iot/f?id=K9i5ql3v98hn3
    "dj": (
        # There are sockets available with an RGB light
        # that advertise as `dj`, but provide an additional
        # switch to control the plug.
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"plug",
        ),
    ),
    # Circuit Breaker
    "dlq": (
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
    # Electric Blanket
    # https://developer.tuya.com/en/docs/iot/categorydr?id=Kaiuz22dyc66p
    "dr": (
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
    # Fan
    # https://developer.tuya.com/en/docs/iot/categoryfs?id=Kaiuz1xweel1c
    "fs": (
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
    # Ceiling Fan Light
    # https://developer.tuya.com/en/docs/iot/fsd?id=Kaof8eiei4c2v
    "fsd": (
        SwitchEntityDescription(
            key=DPCode.FAN_BEEP,
            REDACTED_VALUE"sound",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    # Irrigator
    # https://developer.tuya.com/en/docs/iot/categoryggq?id=Kaiuz1qib7z0k
    "ggq": (
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
    # Wake Up Light II
    # Not documented
    "hxd": (
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
    # Humidifier
    # https://developer.tuya.com/en/docs/iot/categoryjsq?id=Kaiuz1smr440b
    "jsq": (
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
    # Switch
    # https://developer.tuya.com/en/docs/iot/s?id=K9gf7o5prgf7s
    "kg": (
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
    # Air Purifier
    # https://developer.tuya.com/en/docs/iot/f?id=K9gf46h2s6dzm
    "kj": (
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
    # Air conditioner
    # https://developer.tuya.com/en/docs/iot/categorykt?id=Kaiuz0z71ov2n
    "kt": (
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
    # Undocumented tower fan
    # https://github.com/orgs/home-assistant/discussions/329
    "ks": (
        SwitchEntityDescription(
            key=DPCode.ANION,
            REDACTED_VALUE"ionizer",
        ),
    ),
    # Alarm Host
    # https://developer.tuya.com/en/docs/iot/alarm-hosts?id=K9gf48r87hyjk
    "mal": (
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
    # Sous Vide Cooker
    # https://developer.tuya.com/en/docs/iot/categorymzj?id=Kaiuz2vy130ux
    "mzj": (
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
    # Power Socket
    # https://developer.tuya.com/en/docs/iot/s?id=K9gf7o5prgf7s
    "pc": (
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
    # AC charging
    # Not documented
    "qccdz": (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
        ),
    ),
    # Unknown product with switch capabilities
    # Fond in some diffusers, plugs and PIR flood lights
    # Not documented
    "qjdcz": (
        SwitchEntityDescription(
            key=DPCode.SWITCH_1,
            REDACTED_VALUE"switch",
        ),
    ),
    # Heater
    # https://developer.tuya.com/en/docs/iot/categoryqn?id=Kaiuz18kih0sm
    "qn": (
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
    # SIREN: Siren (switch) with Temperature and Humidity Sensor with External Probe
    # New undocumented category qxj, see https://github.com/home-assistant/core/issues/136472
    "qxj": (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
            device_class=SwitchDeviceClass.OUTLET,
        ),
    ),
    # Robot Vacuum
    # https://developer.tuya.com/en/docs/iot/fsd?id=K9gf487ck1tlo
    "sd": (
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
    # Smart Water Timer
    "sfkzq": (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
        ),
    ),
    # Siren Alarm
    # https://developer.tuya.com/en/docs/iot/categorysgbj?id=Kaiuz37tlpbnu
    "sgbj": (
        SwitchEntityDescription(
            key=DPCode.MUFFLING,
            REDACTED_VALUE"mute",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    # Smart Camera
    # https://developer.tuya.com/en/docs/iot/categorysp?id=Kaiuz35leyo12
    "sp": (
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
    # Smart Gardening system
    # https://developer.tuya.com/en/docs/iot/categorysz?id=Kaiuz4e6h7up0
    "sz": (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"power",
        ),
        SwitchEntityDescription(
            key=DPCode.PUMP,
            REDACTED_VALUE"pump",
        ),
    ),
    # Fingerbot
    "szjqr": (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
        ),
    ),
    # IoT Switch?
    # Note: Undocumented
    "tdq": (
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
    # Solar Light
    # https://developer.tuya.com/en/docs/iot/tynd?id=Kaof8j02e1t98
    "tyndj": (
        SwitchEntityDescription(
            key=DPCode.SWITCH_SAVE_ENERGY,
            REDACTED_VALUE"energy_saving",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    # Gateway control
    # https://developer.tuya.com/en/docs/iot/wg?id=Kbcdadk79ejok
    "wg2": (
        SwitchEntityDescription(
            key=DPCode.MUFFLING,
            REDACTED_VALUE"mute",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    # Thermostat
    # https://developer.tuya.com/en/docs/iot/f?id=K9gf45ld5l0t9
    "wk": (
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
    # Two-way temperature and humidity switch
    # "MOES Temperature and Humidity Smart Switch Module MS-103"
    # Documentation not found
    "wkcz": (
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
    # Thermostatic Radiator Valve
    # Not documented
    "wkf": (
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
    # Air Conditioner Mate (Smart IR Socket)
    "wnykq": (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            name=None,
        ),
    ),
    # SIREN: Siren (switch) with Temperature and humidity sensor
    # https://developer.tuya.com/en/docs/iot/f?id=Kavck4sr3o5ek
    "wsdcg": (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
            device_class=SwitchDeviceClass.OUTLET,
        ),
    ),
    # Ceiling Light
    # https://developer.tuya.com/en/docs/iot/ceiling-light?id=Kaiuz03xxfc4r
    "xdd": (
        SwitchEntityDescription(
            key=DPCode.DO_NOT_DISTURB,
            REDACTED_VALUE"do_not_disturb",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    # Diffuser
    # https://developer.tuya.com/en/docs/iot/categoryxxj?id=Kaiuz1f9mo6bl
    "xxj": (
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
    # Smoke Detector
    # https://developer.tuya.com/en/docs/iot/categoryywbj?id=Kaiuz3f6sf952
    "ywbj": (
        SwitchEntityDescription(
            key=DPCode.MUFFLING,
            REDACTED_VALUE"mute",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    # Smart Electricity Meter
    # https://developer.tuya.com/en/docs/iot/smart-meter?id=Kaiuz4gv6ack7
    "zndb": (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
        ),
    ),
    # Hejhome whitelabel Fingerbot
    "znjxs": (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
        ),
    ),
    # Pool HeatPump
    "znrb": (
        SwitchEntityDescription(
            key=DPCode.SWITCH,
            REDACTED_VALUE"switch",
        ),
    ),
}

# Socket (duplicate of `pc`)
# https://developer.tuya.com/en/docs/iot/s?id=K9gf7o5prgf7s
SWITCHES["cz"] = SWITCHES["pc"]

# Smart Camera - Low power consumption camera (duplicate of `sp`)
# Undocumented, see https://github.com/home-assistant/core/issues/132844
SWITCHES["dghsxj"] = SWITCHES["sp"]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TuyaConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up tuya sensors dynamically through tuya discovery."""
    hass_data = entry.runtime_data

    @callback
    def async_discover_device(device_ids: list[str]) -> None:
        """Discover and add a discovered tuya sensor."""
        entities: list[TuyaSwitchEntity] = []
        for device_id in device_ids:
            device = hass_data.manager.device_map[device_id]
            if descriptions := SWITCHES.get(device.category):
                entities.extend(
                    TuyaSwitchEntity(device, hass_data.manager, description)
                    for description in descriptions
                    if description.key in device.status
                )

        async_add_entities(entities)

    async_discover_device([*hass_data.manager.device_map])

    entry.async_on_unload(
        async_dispatcher_connect(hass, TUYA_DISCOVERY_NEW, async_discover_device)
    )


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
