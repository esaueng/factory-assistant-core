"""Support for the NextDNS service."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from aiohttp import ClientError
from aiohttp.client_exceptions import ClientConnectorError
from nextdns import ApiError, InvalidApiKeyError, Settings

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import NextDnsConfigEntry
from .const import DOMAIN
from .coordinator import NextDnsUpdateCoordinator
from .entity import NextDnsEntity

PARALLEL_UPDATES = 1


@dataclass(frozen=True, kw_only=True)
class NextDnsSwitchEntityDescription(SwitchEntityDescription):
    """NextDNS switch entity description."""

    state: Callable[[Settings], bool]


SWITCHES = (
    NextDnsSwitchEntityDescription(
        key="block_page",
        REDACTED_VALUE"block_page",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.block_page,
    ),
    NextDnsSwitchEntityDescription(
        key="cache_boost",
        REDACTED_VALUE"cache_boost",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.cache_boost,
    ),
    NextDnsSwitchEntityDescription(
        key="cname_flattening",
        REDACTED_VALUE"cname_flattening",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.cname_flattening,
    ),
    NextDnsSwitchEntityDescription(
        key="anonymized_ecs",
        REDACTED_VALUE"anonymized_ecs",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.anonymized_ecs,
    ),
    NextDnsSwitchEntityDescription(
        key="bav",
        REDACTED_VALUE"bypass_age_verification",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.bav,
    ),
    NextDnsSwitchEntityDescription(
        key="logs",
        REDACTED_VALUE"logs",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.logs,
    ),
    NextDnsSwitchEntityDescription(
        key="web3",
        REDACTED_VALUE"web3",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.web3,
    ),
    NextDnsSwitchEntityDescription(
        key="allow_affiliate",
        REDACTED_VALUE"allow_affiliate",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.allow_affiliate,
    ),
    NextDnsSwitchEntityDescription(
        key="block_disguised_trackers",
        REDACTED_VALUE"block_disguised_trackers",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.block_disguised_trackers,
    ),
    NextDnsSwitchEntityDescription(
        key="ai_threat_detection",
        REDACTED_VALUE"ai_threat_detection",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.ai_threat_detection,
    ),
    NextDnsSwitchEntityDescription(
        key="block_csam",
        REDACTED_VALUE"block_csam",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.block_csam,
    ),
    NextDnsSwitchEntityDescription(
        key="block_ddns",
        REDACTED_VALUE"block_ddns",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.block_ddns,
    ),
    NextDnsSwitchEntityDescription(
        key="block_nrd",
        REDACTED_VALUE"block_nrd",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.block_nrd,
    ),
    NextDnsSwitchEntityDescription(
        key="block_parked_domains",
        REDACTED_VALUE"block_parked_domains",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.block_parked_domains,
    ),
    NextDnsSwitchEntityDescription(
        key="cryptojacking_protection",
        REDACTED_VALUE"cryptojacking_protection",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.cryptojacking_protection,
    ),
    NextDnsSwitchEntityDescription(
        key="dga_protection",
        REDACTED_VALUE"dga_protection",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.dga_protection,
    ),
    NextDnsSwitchEntityDescription(
        key="dns_rebinding_protection",
        REDACTED_VALUE"dns_rebinding_protection",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.dns_rebinding_protection,
    ),
    NextDnsSwitchEntityDescription(
        key="google_safe_browsing",
        REDACTED_VALUE"google_safe_browsing",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.google_safe_browsing,
    ),
    NextDnsSwitchEntityDescription(
        key="idn_homograph_attacks_protection",
        REDACTED_VALUE"idn_homograph_attacks_protection",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.idn_homograph_attacks_protection,
    ),
    NextDnsSwitchEntityDescription(
        key="threat_intelligence_feeds",
        REDACTED_VALUE"threat_intelligence_feeds",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.threat_intelligence_feeds,
    ),
    NextDnsSwitchEntityDescription(
        key="typosquatting_protection",
        REDACTED_VALUE"typosquatting_protection",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.typosquatting_protection,
    ),
    NextDnsSwitchEntityDescription(
        key="block_bypass_methods",
        REDACTED_VALUE"block_bypass_methods",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.block_bypass_methods,
    ),
    NextDnsSwitchEntityDescription(
        key="safesearch",
        REDACTED_VALUE"safesearch",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.safesearch,
    ),
    NextDnsSwitchEntityDescription(
        key="youtube_restricted_mode",
        REDACTED_VALUE"youtube_restricted_mode",
        entity_category=EntityCategory.CONFIG,
        state=lambda data: data.youtube_restricted_mode,
    ),
    NextDnsSwitchEntityDescription(
        key="block_9gag",
        REDACTED_VALUE"block_9gag",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_9gag,
    ),
    NextDnsSwitchEntityDescription(
        key="block_amazon",
        REDACTED_VALUE"block_amazon",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_amazon,
    ),
    NextDnsSwitchEntityDescription(
        key="block_bereal",
        REDACTED_VALUE"block_bereal",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_bereal,
    ),
    NextDnsSwitchEntityDescription(
        key="block_blizzard",
        REDACTED_VALUE"block_blizzard",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_blizzard,
    ),
    NextDnsSwitchEntityDescription(
        key="block_chatgpt",
        REDACTED_VALUE"block_chatgpt",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_chatgpt,
    ),
    NextDnsSwitchEntityDescription(
        key="block_dailymotion",
        REDACTED_VALUE"block_dailymotion",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_dailymotion,
    ),
    NextDnsSwitchEntityDescription(
        key="block_discord",
        REDACTED_VALUE"block_discord",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_discord,
    ),
    NextDnsSwitchEntityDescription(
        key="block_disneyplus",
        REDACTED_VALUE"block_disneyplus",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_disneyplus,
    ),
    NextDnsSwitchEntityDescription(
        key="block_ebay",
        REDACTED_VALUE"block_ebay",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_ebay,
    ),
    NextDnsSwitchEntityDescription(
        key="block_facebook",
        REDACTED_VALUE"block_facebook",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_facebook,
    ),
    NextDnsSwitchEntityDescription(
        key="block_fortnite",
        REDACTED_VALUE"block_fortnite",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_fortnite,
    ),
    NextDnsSwitchEntityDescription(
        key="block_google_chat",
        REDACTED_VALUE"block_google_chat",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_google_chat,
    ),
    NextDnsSwitchEntityDescription(
        key="block_hbomax",
        REDACTED_VALUE"block_hbomax",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_hbomax,
    ),
    NextDnsSwitchEntityDescription(
        key="block_hulu",
        name="Block Hulu",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_hulu,
    ),
    NextDnsSwitchEntityDescription(
        key="block_imgur",
        REDACTED_VALUE"block_imgur",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_imgur,
    ),
    NextDnsSwitchEntityDescription(
        key="block_instagram",
        REDACTED_VALUE"block_instagram",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_instagram,
    ),
    NextDnsSwitchEntityDescription(
        key="block_leagueoflegends",
        REDACTED_VALUE"block_leagueoflegends",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_leagueoflegends,
    ),
    NextDnsSwitchEntityDescription(
        key="block_mastodon",
        REDACTED_VALUE"block_mastodon",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_mastodon,
    ),
    NextDnsSwitchEntityDescription(
        key="block_messenger",
        REDACTED_VALUE"block_messenger",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_messenger,
    ),
    NextDnsSwitchEntityDescription(
        key="block_minecraft",
        REDACTED_VALUE"block_minecraft",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_minecraft,
    ),
    NextDnsSwitchEntityDescription(
        key="block_netflix",
        REDACTED_VALUE"block_netflix",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_netflix,
    ),
    NextDnsSwitchEntityDescription(
        key="block_pinterest",
        REDACTED_VALUE"block_pinterest",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_pinterest,
    ),
    NextDnsSwitchEntityDescription(
        key="block_playstation_network",
        REDACTED_VALUE"block_playstation_network",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_playstation_network,
    ),
    NextDnsSwitchEntityDescription(
        key="block_primevideo",
        REDACTED_VALUE"block_primevideo",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_primevideo,
    ),
    NextDnsSwitchEntityDescription(
        key="block_reddit",
        REDACTED_VALUE"block_reddit",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_reddit,
    ),
    NextDnsSwitchEntityDescription(
        key="block_roblox",
        REDACTED_VALUE"block_roblox",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_roblox,
    ),
    NextDnsSwitchEntityDescription(
        key="block_signal",
        REDACTED_VALUE"block_signal",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_signal,
    ),
    NextDnsSwitchEntityDescription(
        key="block_skype",
        REDACTED_VALUE"block_skype",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_skype,
    ),
    NextDnsSwitchEntityDescription(
        key="block_snapchat",
        REDACTED_VALUE"block_snapchat",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_snapchat,
    ),
    NextDnsSwitchEntityDescription(
        key="block_spotify",
        REDACTED_VALUE"block_spotify",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_spotify,
    ),
    NextDnsSwitchEntityDescription(
        key="block_steam",
        REDACTED_VALUE"block_steam",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_steam,
    ),
    NextDnsSwitchEntityDescription(
        key="block_telegram",
        REDACTED_VALUE"block_telegram",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_telegram,
    ),
    NextDnsSwitchEntityDescription(
        key="block_tiktok",
        REDACTED_VALUE"block_tiktok",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_tiktok,
    ),
    NextDnsSwitchEntityDescription(
        key="block_tinder",
        REDACTED_VALUE"block_tinder",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_tinder,
    ),
    NextDnsSwitchEntityDescription(
        key="block_tumblr",
        REDACTED_VALUE"block_tumblr",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_tumblr,
    ),
    NextDnsSwitchEntityDescription(
        key="block_twitch",
        REDACTED_VALUE"block_twitch",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_twitch,
    ),
    NextDnsSwitchEntityDescription(
        key="block_twitter",
        REDACTED_VALUE"block_twitter",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_twitter,
    ),
    NextDnsSwitchEntityDescription(
        key="block_vimeo",
        REDACTED_VALUE"block_vimeo",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_vimeo,
    ),
    NextDnsSwitchEntityDescription(
        key="block_vk",
        REDACTED_VALUE"block_vk",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_vk,
    ),
    NextDnsSwitchEntityDescription(
        key="block_whatsapp",
        REDACTED_VALUE"block_whatsapp",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_whatsapp,
    ),
    NextDnsSwitchEntityDescription(
        key="block_xboxlive",
        REDACTED_VALUE"block_xboxlive",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_xboxlive,
    ),
    NextDnsSwitchEntityDescription(
        key="block_youtube",
        REDACTED_VALUE"block_youtube",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_youtube,
    ),
    NextDnsSwitchEntityDescription(
        key="block_zoom",
        REDACTED_VALUE"block_zoom",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_zoom,
    ),
    NextDnsSwitchEntityDescription(
        key="block_dating",
        REDACTED_VALUE"block_dating",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_dating,
    ),
    NextDnsSwitchEntityDescription(
        key="block_gambling",
        REDACTED_VALUE"block_gambling",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_gambling,
    ),
    NextDnsSwitchEntityDescription(
        key="block_online_gaming",
        REDACTED_VALUE"block_online_gaming",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_online_gaming,
    ),
    NextDnsSwitchEntityDescription(
        key="block_piracy",
        REDACTED_VALUE"block_piracy",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_piracy,
    ),
    NextDnsSwitchEntityDescription(
        key="block_porn",
        REDACTED_VALUE"block_porn",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_porn,
    ),
    NextDnsSwitchEntityDescription(
        key="block_social_networks",
        REDACTED_VALUE"block_social_networks",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_social_networks,
    ),
    NextDnsSwitchEntityDescription(
        key="block_video_streaming",
        REDACTED_VALUE"block_video_streaming",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        state=lambda data: data.block_video_streaming,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: NextDnsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add NextDNS entities from a config_entry."""
    coordinator = entry.runtime_data.settings

    async_add_entities(
        NextDnsSwitch(coordinator, description) for description in SWITCHES
    )


class NextDnsSwitch(NextDnsEntity, SwitchEntity):
    """Define an NextDNS switch."""

    entity_description: NextDnsSwitchEntityDescription

    def __init__(
        self,
        coordinator: NextDnsUpdateCoordinator[Settings],
        description: NextDnsSwitchEntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, description)
        self._attr_is_on = description.state(coordinator.data)

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
                translation_domain=DOMAIN,
                REDACTED_VALUE"method_error",
                translation_placeholders={
                    "entity": self.entity_id,
                    "error": repr(err),
                },
            ) from err
        except InvalidApiKeyError:
            self.coordinator.config_entry.async_start_reauth(self.hass)
            return

        if result:
            self._attr_is_on = new_state
            self.async_write_ha_state()
