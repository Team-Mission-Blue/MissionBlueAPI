"""Authentication module for the BlueSky API."""

import os
import sys

import requests
from dotenv import load_dotenv


# Load environment variables from the .env file
def load_credentials() -> tuple[str, str] | None:
    """Validates and returns user BlueSky credentials.

    Returns:
        tuple[str, str] | None: This ordered pair contains the Bluesky Username and Password or None if the .env file does not exist.

    """
    # pylint: disable=C0301
    if load_dotenv():
        # Access credentials from the environment variables
        handle = os.getenv("BLUESKY_HANDLE")
        password = os.getenv("BLUESKY_APP_PASSWORD")
        assert handle != "", "BLUESKY_HANDLE can not be empty"
        assert password != "", "BLUESKY_APP_PASSWORD can not be empty"
        return (handle, password)
    print(".env does not exist")
    sys.exit(1)


def create_session(username: str, password: str):
    """Authenticate and create a session to get the access token.

    :return: Access token (accessJwt) for authentication.
    """
    url = "https://bsky.social/xrpc/com.atproto.server.createSession"
    payload = {"identifier": username, "password": password}

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        session = response.json()
        return session["accessJwt"]
    except requests.exceptions.RequestException as err:
        print("Error during authentication:", err)
        print("Response:", response.text if "response" in locals() else "No response")
        sys.exit(1)
