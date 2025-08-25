"""Define const for Volvo unit tests."""

CLIENT_ID = "1234"
CLIENT_SECRET = "5678"

DEFAULT_API_KEY = "REDACTED_VALUE"
DEFAULT_MODEL = "xc40_electric_2024"
DEFAULT_VIN = "YV1REDACTED_VALUE"

MOCK_ACCESS_TOKEN = "mock-access-token"

REDIRECT_URI = "https://example.com/auth/external/callback"

SERVER_TOKEN_RESPONSE = {
    "refresh_token": "server-refresh-token",
    "access_token": "server-access-token",
    "token_type": "Bearer",
    "expires_in": 60,
}
