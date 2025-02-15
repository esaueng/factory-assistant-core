"""Common fixtures for the One-Time Password (OTP) tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from homeassistant.components.otp.const import DOMAIN
from homeassistant.const import CONF_NAME, CONF_TOKEN

from tests.common import MockConfigEntry


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
        "homeassistant.components.otp.async_setup_entry", return_value=True
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture
def mock_pyotp() -> Generator[MagicMock]:
    """Mock a pyotp."""
    with (
        patch(
            "homeassistant.components.otp.config_flow.pyotp",
        ) as mock_client,
        patch("homeassistant.components.otp.sensor.pyotp", new=mock_client),
    ):
        mock_totp = MagicMock()
        mock_totp.now.return_value = 123456
        mock_totp.verify.return_value = True
        mock_totp.provisioning_uri.return_value = "otpauth://totp/Home%20Assistant:OTP%20Sensor?secret=REDACTED_VALUE&issuer=Home%20Assistant"
        mock_client.TOTP.return_value = mock_totp
        mock_client.random_base32.return_value = "REDACTED_VALUE"
        yield mock_client


@pytest.fixture(name="otp_config_entry")
def mock_otp_config_entry() -> MockConfigEntry:
    """Mock otp configuration entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_NAME: "OTP Sensor",
            CONF_TOKEN: "REDACTED_VALUE",
        },
        unique_id="REDACTED_VALUE",
    )
