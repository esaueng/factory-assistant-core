"""Support for the NextDNS service."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Generic

from aiohttp import ClientError
from aiohttp.client_exceptions import ClientConnectorError
from nextdns import ApiError, Settings

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import CoordinatorDataT, NextDnsSettingsUpdateCoordinator
from .const import ATTR_SETTINGS, DOMAIN

PARALLEL_UPDATES = 1


@dataclass(frozen=True)
class NextDnsSwitchRequiredKeysMixin(Generic[CoordinatorDataT]):
    """Class for NextDNS entity required keys."""

    state: Callable[[CoordinatorDataT], bool]


@dataclass(frozen=True)
class NextDnsSwitchEntityDescription(
    SwitchEntityDescription, NextDnsSwitchRequiredKeysMixin[CoordinatorDataT]
):
    """NextDNS switch entity description."""


SWITCHES = (
    NextDnsSwitchEntityDescription[Settings](
        key="block_page",
        REDACTED_VALUE"block_page",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.block_page,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="cache_boost",
        REDACTED_VALUE"cache_boost",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.cache_boost,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="cname_flattening",
        REDACTED_VALUE"cname_flattening",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.cname_flattening,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="anonymized_ecs",
        REDACTED_VALUE"anonymized_ecs",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.anonymized_ecs,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="logs",
        REDACTED_VALUE"logs",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.logs,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="web3",
        REDACTED_VALUE"web3",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.web3,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="allow_affiliate",
        REDACTED_VALUE"allow_affiliate",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.allow_affiliate,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_disguised_trackers",
        REDACTED_VALUE"block_disguised_trackers",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.block_disguised_trackers,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="ai_threat_detection",
        REDACTED_VALUE"ai_threat_detection",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.ai_threat_detection,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_csam",
        REDACTED_VALUE"block_csam",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.block_csam,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_ddns",
        REDACTED_VALUE"block_ddns",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.block_ddns,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_nrd",
        REDACTED_VALUE"block_nrd",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.block_nrd,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_parked_domains",
        REDACTED_VALUE"block_parked_domains",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.block_parked_domains,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="cryptojacking_protection",
        REDACTED_VALUE"cryptojacking_protection",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.cryptojacking_protection,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="dga_protection",
        REDACTED_VALUE"dga_protection",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.dga_protection,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="dns_rebinding_protection",
        REDACTED_VALUE"dns_rebinding_protection",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.dns_rebinding_protection,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="google_safe_browsing",
        REDACTED_VALUE"google_safe_browsing",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.google_safe_browsing,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="idn_homograph_attacks_protection",
        REDACTED_VALUE"idn_homograph_attacks_protection",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.idn_homograph_attacks_protection,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="threat_intelligence_feeds",
        REDACTED_VALUE"threat_intelligence_feeds",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.threat_intelligence_feeds,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="typosquatting_protection",
        REDACTED_VALUE"typosquatting_protection",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.typosquatting_protection,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_bypass_methods",
        REDACTED_VALUE"block_bypass_methods",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.block_bypass_methods,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="safesearch",
        REDACTED_VALUE"safesearch",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.safesearch,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="youtube_restricted_mode",
        REDACTED_VALUE"youtube_restricted_mode",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.youtube_restricted_mode,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_9gag",
        REDACTED_VALUE"block_9gag",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_9gag,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_amazon",
        REDACTED_VALUE"block_amazon",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_amazon,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_bereal",
        REDACTED_VALUE"block_bereal",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_bereal,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_blizzard",
        REDACTED_VALUE"block_blizzard",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_blizzard,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_chatgpt",
        REDACTED_VALUE"block_chatgpt",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_chatgpt,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_dailymotion",
        REDACTED_VALUE"block_dailymotion",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_dailymotion,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_discord",
        REDACTED_VALUE"block_discord",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_discord,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_disneyplus",
        REDACTED_VALUE"block_disneyplus",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_disneyplus,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_ebay",
        REDACTED_VALUE"block_ebay",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_ebay,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_facebook",
        REDACTED_VALUE"block_facebook",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_facebook,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_fortnite",
        REDACTED_VALUE"block_fortnite",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_fortnite,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_google_chat",
        REDACTED_VALUE"block_google_chat",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_google_chat,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_hbomax",
        REDACTED_VALUE"block_hbomax",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_hbomax,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_hulu",
        name="Block Hulu",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_hulu,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_imgur",
        REDACTED_VALUE"block_imgur",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_imgur,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_instagram",
        REDACTED_VALUE"block_instagram",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_instagram,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_leagueoflegends",
        REDACTED_VALUE"block_leagueoflegends",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_leagueoflegends,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_mastodon",
        REDACTED_VALUE"block_mastodon",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_mastodon,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_messenger",
        REDACTED_VALUE"block_messenger",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_messenger,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_minecraft",
        REDACTED_VALUE"block_minecraft",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_minecraft,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_netflix",
        REDACTED_VALUE"block_netflix",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_netflix,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_pinterest",
        REDACTED_VALUE"block_pinterest",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_pinterest,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_playstation_network",
        REDACTED_VALUE"block_playstation_network",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_playstation_network,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_primevideo",
        REDACTED_VALUE"block_primevideo",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_primevideo,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_reddit",
        REDACTED_VALUE"block_reddit",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_reddit,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_roblox",
        REDACTED_VALUE"block_roblox",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_roblox,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_signal",
        REDACTED_VALUE"block_signal",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_signal,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_skype",
        REDACTED_VALUE"block_skype",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_skype,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_snapchat",
        REDACTED_VALUE"block_snapchat",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_snapchat,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_spotify",
        REDACTED_VALUE"block_spotify",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_spotify,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_steam",
        REDACTED_VALUE"block_steam",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_steam,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_telegram",
        REDACTED_VALUE"block_telegram",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_telegram,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_tiktok",
        REDACTED_VALUE"block_tiktok",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_tiktok,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_tinder",
        REDACTED_VALUE"block_tinder",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_tinder,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_tumblr",
        REDACTED_VALUE"block_tumblr",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_tumblr,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_twitch",
        REDACTED_VALUE"block_twitch",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_twitch,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_twitter",
        REDACTED_VALUE"block_twitter",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_twitter,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_vimeo",
        REDACTED_VALUE"block_vimeo",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_vimeo,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_vk",
        REDACTED_VALUE"block_vk",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_vk,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_whatsapp",
        REDACTED_VALUE"block_whatsapp",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_whatsapp,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_xboxlive",
        REDACTED_VALUE"block_xboxlive",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_xboxlive,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_youtube",
        REDACTED_VALUE"block_youtube",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_youtube,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_zoom",
        REDACTED_VALUE"block_zoom",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_zoom,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_dating",
        REDACTED_VALUE"block_dating",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_dating,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_gambling",
        REDACTED_VALUE"block_gambling",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_gambling,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_online_gaming",
        REDACTED_VALUE"block_online_gaming",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_online_gaming,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_piracy",
        REDACTED_VALUE"block_piracy",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_piracy,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_porn",
        REDACTED_VALUE"block_porn",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_porn,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_social_networks",
        REDACTED_VALUE"block_social_networks",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_social_networks,
    ),
    NextDnsSwitchEntityDescription[Settings](
        key="block_video_streaming",
        REDACTED_VALUE"block_video_streaming",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_video_streaming,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Add NextDNS entities from a config_entry."""
    coordinator: NextDnsSettingsUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        ATTR_SETTINGS
    ]

    switches: list[NextDnsSwitch] = []
    for description in SWITCHES:
        switches.append(NextDnsSwitch(coordinator, description))

    async_add_entities(switches)


class NextDnsSwitch(CoordinatorEntity[NextDnsSettingsUpdateCoordinator], SwitchEntity):
    """Define an NextDNS switch."""

    _attr_has_entity_name = True
    entity_description: NextDnsSwitchEntityDescription

    def __init__(
        self,
        coordinator: NextDnsSettingsUpdateCoordinator,
        description: NextDnsSwitchEntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_device_info = coordinator.device_info
        self._attr_unique_id = f"{coordinator.profile_id}_{description.key}"
        self._attr_is_on = description.state(coordinator.data)
        self.entity_description = description

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_is_on = self.entity_description.state(self.coordinator.data)
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on switch."""
        await self.async_set_setting(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off switch."""
        await self.async_set_setting(False)

    async def async_set_setting(self, new_state: bool) -> None:
        """Set the new state."""
        try:
            result = await self.coordinator.nextdns.set_setting(
                self.coordinator.profile_id, self.entity_description.key, new_state
            )
        except (
            ApiError,
            ClientConnectorError,
            TimeoutError,
            ClientError,
        ) as err:
            raise HomeAssistantError(
                "NextDNS API returned an error calling set_setting for"
                f" {self.entity_id}: {err}"
            ) from err

        if result:
            self._attr_is_on = new_state
            self.async_write_ha_state()
