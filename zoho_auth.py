
import os
import requests
from dotenv import load_dotenv

load_dotenv()

ZOHO_TOKEN_URL = "https://accounts.zoho.in/oauth/v2/token"

def get_access_token():
    """
    Fetch access token using refresh token.
    Raises a clear error only when actually used.
    """

    client_id = os.getenv("ZOHO_CLIENT_ID")
    client_secret = os.getenv("ZOHO_CLIENT_SECRET")
    refresh_token = os.getenv("ZOHO_REFRESH_TOKEN")

    if not client_id or not client_secret or not refresh_token:
        raise RuntimeError(
            "Zoho credentials missing. "
            "Set ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, ZOHO_REFRESH_TOKEN."
        )

    response = requests.post(
        ZOHO_TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
        },
        timeout=10,
    )

    response.raise_for_status()
    return response.json()["access_token"]
