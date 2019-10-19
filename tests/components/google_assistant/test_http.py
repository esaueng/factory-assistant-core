"""Test Google http services."""
from datetime import datetime, timezone, timedelta
from asynctest import patch, ANY

from homeassistant.components.google_assistant.http import (
    GoogleConfig,
    _get_homegraph_jwt,
    _get_homegraph_token,
)
from homeassistant.components.google_assistant import GOOGLE_ASSISTANT_SCHEMA
from homeassistant.components.google_assistant.const import (
    REPORT_STATE_BASE_URL,
    HOMEGRAPH_TOKEN_URL,
)
from homeassistant.auth.models import User

DUMMY_CONFIG = GOOGLE_ASSISTANT_SCHEMA(
    {
        "project_id": "1234",
        "service_account": {
            "private_key": "REDACTED_VALUE\n",
            "client_email": "dummy@dummy.iam.gserviceaccount.com",
        },
    }
)
MOCK_TOKEN = {"access_token": "dummtoken", "expires_in": 3600}
MOCK_JSON = {"devices": {}}
MOCK_URL = "https://dummy"
MOCK_HEADER = {
    "Authorization": "Bearer {}".format(MOCK_TOKEN["access_token"]),
    "X-GFE-SSL": "yes",
}


async def test_get_jwt(hass):
    """Test signing of key."""

    jwt = "REDACTED_VALUE"
    res = _get_homegraph_jwt(
        datetime(2019, 10, 14, tzinfo=timezone.utc),
        DUMMY_CONFIG["service_account"]["client_email"],
        DUMMY_CONFIG["service_account"]["private_key"],
    )
    assert res == jwt


async def test_get_access_token(hass, aioclient_mock):
    """Test the function to get access token."""
    jwt = "dummyjwt"

    aioclient_mock.post(
        HOMEGRAPH_TOKEN_URL,
        status=200,
        json={"access_token": "1234", "expires_in": 3600},
    )

    await _get_homegraph_token(hass, jwt)
    assert aioclient_mock.call_count == 1
    assert aioclient_mock.mock_calls[0][3] == {
        "Authorization": "Bearer {}".format(jwt),
        "Content-Type": "application/x-www-form-urlencoded",
    }


async def test_update_access_token(hass):
    """Test the function to update access token when expired."""
    jwt = "dummyjwt"

    config = GoogleConfig(hass, DUMMY_CONFIG)

    base_time = datetime(2019, 10, 14, tzinfo=timezone.utc)
    with patch(
        "homeassistant.components.google_assistant.http._get_homegraph_token"
    ) as mock_get_token, patch(
        "homeassistant.components.google_assistant.http._get_homegraph_jwt"
    ) as mock_get_jwt, patch(
        "homeassistant.core.dt_util.utcnow"
    ) as mock_utcnow:
        mock_utcnow.return_value = base_time
        mock_get_jwt.return_value = jwt
        mock_get_token.return_value = MOCK_TOKEN

        await config._async_update_token()
        mock_get_token.assert_called_once()

        mock_get_token.reset_mock()

        mock_utcnow.return_value = base_time + timedelta(seconds=3600)
        await config._async_update_token()
        mock_get_token.assert_not_called()

        mock_get_token.reset_mock()

        mock_utcnow.return_value = base_time + timedelta(seconds=3601)
        await config._async_update_token()
        mock_get_token.assert_called_once()


async def test_call_homegraph_api(hass, aioclient_mock, hass_storage):
    """Test the function to call the homegraph api."""
    config = GoogleConfig(hass, DUMMY_CONFIG)
    with patch(
        "homeassistant.components.google_assistant.http._get_homegraph_token"
    ) as mock_get_token:
        mock_get_token.return_value = MOCK_TOKEN

        aioclient_mock.post(MOCK_URL, status=200, json={})

        await config.async_call_homegraph_api(MOCK_URL, MOCK_JSON)

        assert mock_get_token.call_count == 1
        assert aioclient_mock.call_count == 1

        call = aioclient_mock.mock_calls[0]
        assert call[2] == MOCK_JSON
        assert call[3] == MOCK_HEADER


async def test_call_homegraph_api_retry(hass, aioclient_mock, hass_storage):
    """Test the that the calls get retried with new token on 401."""
    config = GoogleConfig(hass, DUMMY_CONFIG)
    with patch(
        "homeassistant.components.google_assistant.http._get_homegraph_token"
    ) as mock_get_token:
        mock_get_token.return_value = MOCK_TOKEN

        aioclient_mock.post(MOCK_URL, status=401, json={})

        await config.async_call_homegraph_api(MOCK_URL, MOCK_JSON)

        assert mock_get_token.call_count == 2
        assert aioclient_mock.call_count == 2

        call = aioclient_mock.mock_calls[0]
        assert call[2] == MOCK_JSON
        assert call[3] == MOCK_HEADER
        call = aioclient_mock.mock_calls[1]
        assert call[2] == MOCK_JSON
        assert call[3] == MOCK_HEADER


async def test_report_state(hass, aioclient_mock, hass_storage):
    """Test the report state function."""
    config = GoogleConfig(hass, DUMMY_CONFIG)
    message = {"devices": {}}
    owner = User(name="Test User", perm_lookup=None, groups=[], is_owner=True)

    with patch.object(config, "async_call_homegraph_api") as mock_call, patch.object(
        hass.auth, "async_get_owner"
    ) as mock_get_owner:
        mock_get_owner.return_value = owner

        await config.async_report_state(message)
        mock_call.assert_called_once_with(
            REPORT_STATE_BASE_URL,
            {"requestId": ANY, "agentUserId": owner.id, "payload": message},
        )
