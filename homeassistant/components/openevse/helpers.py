"""Helpers for OpenEVSE."""

from collections.abc import Iterator
from contextlib import contextmanager

from aiohttp import ContentTypeError, ServerTimeoutError
from openevsehttp.exceptions import (
    AuthenticationError,
    ParseJSONError,
    UnsupportedFeature,
)

from homeassistant.exceptions import (
    ConfigEntryAuthFailed,
    HomeAssistantError,
    ServiceValidationError,
)

from .const import DOMAIN


@contextmanager
def openevse_exception_handler(value: float) -> Iterator[None]:
    """Context manager to handle and translate OpenEVSE exceptions."""
    try:
        yield
    except ValueError as err:
        raise ServiceValidationError(
            translation_domain=DOMAIN,
            REDACTED_VALUE"invalid_value",
            translation_placeholders={"value": str(value)},
        ) from err
    except AuthenticationError as err:
        raise ConfigEntryAuthFailed(
            translation_domain=DOMAIN,
            REDACTED_VALUE"authentication_error",
        ) from err
    except UnsupportedFeature as err:
        raise HomeAssistantError(
            translation_domain=DOMAIN,
            REDACTED_VALUE"unsupported_feature",
        ) from err
    except (
        TimeoutError,
        ServerTimeoutError,
        ContentTypeError,
        ParseJSONError,
    ) as err:
        raise HomeAssistantError(
            translation_domain=DOMAIN,
            REDACTED_VALUE"communication_error",
        ) from err
