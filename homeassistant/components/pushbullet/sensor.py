"""Pushbullet platform for sensor component."""

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import CONF_NAME, MAX_LENGTH_STATE_STATE
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import PushbulletConfigEntry
from .api import PushBulletNotificationProvider
from .const import DATA_UPDATED, DOMAIN

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="application_name",
        REDACTED_VALUE"application_name",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="body",
        REDACTED_VALUE"body",
    ),
    SensorEntityDescription(
        key="notification_id",
        REDACTED_VALUE"notification_id",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="notification_tag",
        REDACTED_VALUE"notification_tag",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="package_name",
        REDACTED_VALUE"package_name",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="receiver_email",
        REDACTED_VALUE"receiver_email",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="sender_email",
        REDACTED_VALUE"sender_email",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="source_device_iden",
        REDACTED_VALUE"source_device_identifier",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="title",
        REDACTED_VALUE"title",
    ),
    SensorEntityDescription(
        key="type",
        REDACTED_VALUE"type",
        entity_registry_enabled_default=False,
    ),
)

SENSOR_KEYS: list[str] = [desc.key for desc in SENSOR_TYPES]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PushbulletConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Pushbullet sensors from config entry."""

    pb_provider = entry.runtime_data

    entities = [
        PushBulletNotificationSensor(entry.data[CONF_NAME], pb_provider, description)
        for description in SENSOR_TYPES
    ]

    async_add_entities(entities)


class PushBulletNotificationSensor(SensorEntity):
    """Representation of a Pushbullet Sensor."""

    _attr_should_poll = False
    _attr_has_entity_name = True

    def __init__(
        self,
        name: str,
        pb_provider: PushBulletNotificationProvider,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the Pushbullet sensor."""
        self.entity_description = description
        self.pb_provider = pb_provider
        self._attr_unique_id = (
            f"{pb_provider.pushbullet.user_info['iden']}-{description.key}"
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, pb_provider.pushbullet.user_info["iden"])},
            name=name,
            entry_type=DeviceEntryType.SERVICE,
        )

    @callback
    def async_update_callback(self) -> None:
        """Fetch the latest data from the sensor.

        This will fetch the 'sensor reading' into self._state but also all
        attributes into self._state_attributes.
        """
        try:
            value = self.pb_provider.data[self.entity_description.key]
            # Truncate state value to MAX_LENGTH_STATE_STATE while preserving full content in attributes
            if isinstance(value, str) and len(value) > MAX_LENGTH_STATE_STATE:
                self._attr_native_value = value[: MAX_LENGTH_STATE_STATE - 3] + "..."
            else:
                self._attr_native_value = value
            self._attr_extra_state_attributes = self.pb_provider.data
        except KeyError, TypeError:
            pass
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, DATA_UPDATED, self.async_update_callback
            )
        )
