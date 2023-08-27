"""Summary data from Nextcoud."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Final, cast

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfInformation, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN
from .coordinator import NextcloudDataUpdateCoordinator
from .entity import NextcloudEntity

UNIT_OF_LOAD: Final[str] = "load"

SENSORS: Final[dict[str, SensorEntityDescription]] = {
    "activeUsers_last1hour": SensorEntityDescription(
        key="activeUsers_last1hour",
        REDACTED_VALUE"nextcloud_activeusers_last1hour",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:account-multiple",
    ),
    "activeUsers_last24hours": SensorEntityDescription(
        key="activeUsers_last24hours",
        REDACTED_VALUE"nextcloud_activeusers_last24hours",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:account-multiple",
    ),
    "activeUsers_last5minutes": SensorEntityDescription(
        key="activeUsers_last5minutes",
        REDACTED_VALUE"nextcloud_activeusers_last5minutes",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:account-multiple",
    ),
    "database_type": SensorEntityDescription(
        key="database_type",
        REDACTED_VALUE"nextcloud_database_type",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:database",
    ),
    "database_version": SensorEntityDescription(
        key="database_version",
        REDACTED_VALUE"nextcloud_database_version",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:database",
    ),
    "server_php_max_execution_time": SensorEntityDescription(
        key="server_php_max_execution_time",
        REDACTED_VALUE"nextcloud_server_php_max_execution_time",
        device_class=SensorDeviceClass.DURATION,
        entity_category=EntityCategory.CONFIG,
        icon="mdi:language-php",
        native_unit_of_measurement=UnitOfTime.SECONDS,
    ),
    "server_php_memory_limit": SensorEntityDescription(
        key="server_php_memory_limit",
        REDACTED_VALUE"nextcloud_server_php_memory_limit",
        device_class=SensorDeviceClass.DATA_SIZE,
        entity_category=EntityCategory.CONFIG,
        icon="mdi:language-php",
        native_unit_of_measurement=UnitOfInformation.BYTES,
        suggested_display_precision=1,
        suggested_unit_of_measurement=UnitOfInformation.MEGABYTES,
    ),
    "server_php_upload_max_filesize": SensorEntityDescription(
        key="server_php_upload_max_filesize",
        REDACTED_VALUE"nextcloud_server_php_upload_max_filesize",
        device_class=SensorDeviceClass.DATA_SIZE,
        entity_category=EntityCategory.CONFIG,
        icon="mdi:language-php",
        native_unit_of_measurement=UnitOfInformation.BYTES,
        suggested_display_precision=1,
        suggested_unit_of_measurement=UnitOfInformation.MEGABYTES,
    ),
    "server_php_version": SensorEntityDescription(
        key="server_php_version",
        REDACTED_VALUE"nextcloud_server_php_version",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:language-php",
    ),
    "server_webserver": SensorEntityDescription(
        key="server_webserver",
        REDACTED_VALUE"nextcloud_server_webserver",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "shares_num_fed_shares_sent": SensorEntityDescription(
        key="shares_num_fed_shares_sent",
        REDACTED_VALUE"nextcloud_shares_num_fed_shares_sent",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "shares_num_fed_shares_received": SensorEntityDescription(
        key="shares_num_fed_shares_received",
        REDACTED_VALUE"nextcloud_shares_num_fed_shares_received",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "shares_num_shares": SensorEntityDescription(
        key="shares_num_shares",
        REDACTED_VALUE"nextcloud_shares_num_shares",
    ),
    "shares_num_shares_groups": SensorEntityDescription(
        key="shares_num_shares_groups",
        REDACTED_VALUE"nextcloud_shares_num_shares_groups",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "shares_num_shares_link": SensorEntityDescription(
        key="shares_num_shares_link",
        REDACTED_VALUE"nextcloud_shares_num_shares_link",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "shares_num_shares_link_no_password": SensorEntityDescription(
        key="shares_num_shares_link_no_password",
        REDACTED_VALUE"nextcloud_shares_num_shares_link_no_password",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "shares_num_shares_mail": SensorEntityDescription(
        key="shares_num_shares_mail",
        REDACTED_VALUE"nextcloud_shares_num_shares_mail",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "shares_num_shares_room": SensorEntityDescription(
        key="shares_num_shares_room",
        REDACTED_VALUE"nextcloud_shares_num_shares_room",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "shares_num_shares_user": SensorEntityDescription(
        key="server_num_shares_user",
        REDACTED_VALUE"nextcloud_shares_num_shares_user",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "storage_num_files": SensorEntityDescription(
        key="storage_num_files",
        REDACTED_VALUE"nextcloud_storage_num_files",
    ),
    "storage_num_storages": SensorEntityDescription(
        key="storage_num_storages",
        REDACTED_VALUE"nextcloud_storage_num_storages",
    ),
    "storage_num_storages_home": SensorEntityDescription(
        key="storage_num_storages_home",
        REDACTED_VALUE"nextcloud_storage_num_storages_home",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "storage_num_storages_local": SensorEntityDescription(
        key="storage_num_storages_local",
        REDACTED_VALUE"nextcloud_storage_num_storages_local",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "storage_num_storages_other": SensorEntityDescription(
        key="storage_num_storages_other",
        REDACTED_VALUE"nextcloud_storage_num_storages_other",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "storage_num_users": SensorEntityDescription(
        key="storage_num_users",
        REDACTED_VALUE"nextcloud_storage_num_users",
    ),
    "system_apps_num_installed": SensorEntityDescription(
        key="system_apps_num_installed",
        REDACTED_VALUE"nextcloud_system_apps_num_installed",
    ),
    "system_apps_num_updates_available": SensorEntityDescription(
        key="system_apps_num_updates_available",
        REDACTED_VALUE"nextcloud_system_apps_num_updates_available",
        icon="mdi:update",
    ),
    "system_cpuload": SensorEntityDescription(
        key="system_cpuload",
        REDACTED_VALUE"nextcloud_system_cpuload",
        icon="mdi:chip",
    ),
    "system_freespace": SensorEntityDescription(
        key="system_freespace",
        REDACTED_VALUE"nextcloud_system_freespace",
        device_class=SensorDeviceClass.DATA_SIZE,
        icon="mdi:harddisk",
        native_unit_of_measurement=UnitOfInformation.BYTES,
        suggested_display_precision=2,
        suggested_unit_of_measurement=UnitOfInformation.GIGABYTES,
    ),
    "system_mem_free": SensorEntityDescription(
        key="system_mem_free",
        REDACTED_VALUE"nextcloud_system_mem_free",
        device_class=SensorDeviceClass.DATA_SIZE,
        icon="mdi:memory",
        native_unit_of_measurement=UnitOfInformation.KILOBYTES,
        suggested_display_precision=2,
        suggested_unit_of_measurement=UnitOfInformation.GIGABYTES,
    ),
    "system_mem_total": SensorEntityDescription(
        key="system_mem_total",
        REDACTED_VALUE"nextcloud_system_mem_total",
        device_class=SensorDeviceClass.DATA_SIZE,
        icon="mdi:memory",
        native_unit_of_measurement=UnitOfInformation.KILOBYTES,
        suggested_display_precision=2,
        suggested_unit_of_measurement=UnitOfInformation.GIGABYTES,
    ),
    "system_memcache.distributed": SensorEntityDescription(
        key="system_memcache.distributed",
        REDACTED_VALUE"nextcloud_system_memcache_distributed",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "system_memcache.local": SensorEntityDescription(
        key="system_memcache.local",
        REDACTED_VALUE"nextcloud_system_memcache_local",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "system_memcache.locking": SensorEntityDescription(
        key="system_memcache.locking",
        REDACTED_VALUE"nextcloud_system_memcache_locking",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    "system_swap_total": SensorEntityDescription(
        key="system_swap_total",
        REDACTED_VALUE"nextcloud_system_swap_total",
        device_class=SensorDeviceClass.DATA_SIZE,
        icon="mdi:memory",
        native_unit_of_measurement=UnitOfInformation.KILOBYTES,
        suggested_display_precision=2,
        suggested_unit_of_measurement=UnitOfInformation.GIGABYTES,
    ),
    "system_swap_free": SensorEntityDescription(
        key="system_swap_free",
        REDACTED_VALUE"nextcloud_system_swap_free",
        device_class=SensorDeviceClass.DATA_SIZE,
        icon="mdi:memory",
        native_unit_of_measurement=UnitOfInformation.KILOBYTES,
        suggested_display_precision=2,
        suggested_unit_of_measurement=UnitOfInformation.GIGABYTES,
    ),
    "system_theme": SensorEntityDescription(
        key="system_theme",
        REDACTED_VALUE"nextcloud_system_theme",
    ),
    "system_version": SensorEntityDescription(
        key="system_version",
        REDACTED_VALUE"nextcloud_system_version",
    ),
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Nextcloud sensors."""
    coordinator: NextcloudDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            NextcloudSensor(coordinator, name, entry, SENSORS[name])
            for name in coordinator.data
            if name in SENSORS
        ]
    )


class NextcloudSensor(NextcloudEntity, SensorEntity):
    """Represents a Nextcloud sensor."""

    @property
    def native_value(self) -> StateType | datetime:
        """Return the state for this sensor."""
        val = self.coordinator.data.get(self.item)
        if (
            getattr(self.entity_description, "device_class", None)
            == SensorDeviceClass.TIMESTAMP
        ):
            return datetime.fromtimestamp(cast(int, val), tz=UTC)
        return val
