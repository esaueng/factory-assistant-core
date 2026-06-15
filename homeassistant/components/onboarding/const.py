"""Constants for the onboarding component."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DefaultArea:
    """Default area definition."""

    key: str
    icon: str


DOMAIN = "onboarding"
STEP_USER = "user"
STEP_CORE_CONFIG = "core_config"
STEP_INTEGRATION = "integration"
STEP_ANALYTICS = "analytics"
STEP_FACTORY_ASSISTANT_INDUSTRIAL = "factory_assistant_industrial"

STEPS = [
    STEP_USER,
    STEP_CORE_CONFIG,
    STEP_FACTORY_ASSISTANT_INDUSTRIAL,
    STEP_ANALYTICS,
    STEP_INTEGRATION,
]

DEFAULT_AREAS = (
    DefaultArea(key="living_room", icon="mdi:sofa"),
    DefaultArea(key="kitchen", icon="mdi:stove"),
    DefaultArea(key="bedroom", icon="mdi:bed"),
)
