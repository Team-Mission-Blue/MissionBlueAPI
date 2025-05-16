"""Testing suite for the mission_blue module."""

# pylint: disable=W0613
# pylint: disable=C0301
# pylint: disable=E0401

import unittest
from unittest import mock
from unittest.mock import Mock, patch

import requests

from auth import create_session, load_credentials


class TestLoadCredentials(unittest.TestCase):
    """Testing the load_credentials method."""

    @patch("auth.load_dotenv", return_value=False)
    def test_no_env(self, mock_load_dotenv) -> None:
        """Test if .env file does not exist."""
        with self.assertRaises(SystemExit) as cm:
            load_credentials()
        self.assertEqual(cm.exception.code, 1)

    @patch(
        "os.getenv",
        side_effect=lambda key: (
            "" if key in ["BLUESKY_HANDLE", "BLUESKY_APP_PASSWORD"] else None
        ),
    )
    @patch("auth.load_dotenv", return_value=True)
    def test_env_with_no_credentials(
        self, mock_load_dotenv: mock.MagicMock, mock_getenv: mock.MagicMock
    ) -> None:
        """Test if .env exist but username and password are empty."""
        with self.assertRaises(AssertionError) as cm:
            load_credentials()
        self.assertIn("can not be empty", str(cm.exception))

    @patch("auth.load_dotenv", return_value=True)
    @patch(
        "os.getenv",
        side_effect=lambda key: (
            "any_value" if key in ["BLUESKY_HANDLE", "BLUESKY_APP_PASSWORD"] else None
        ),
    )
    def test_env_exist_with_valid_credentials(
        self, mock_load_dotenv: mock.MagicMock, mock_getenv: mock.MagicMock
    ) -> None:
        """Test if .env exists with valid username and password."""
        credentials = load_credentials()
        self.assertTrue(all(credentials))


class TestCreateBlueSkySession(unittest.TestCase):
    """Testing the create_bluesky_session() method."""

    def setUp(self) -> None:
        self.username: str = "ValidUsername"
        self.password: str = "ValidPassword"

    @patch("auth.requests.post")
    def test_successful_authentication(self, mock_post: mock.MagicMock) -> None:
        """ "
        Test if authentication was successful.
        """
        mock_response = Mock()
        mock_response.json.return_value = {"accessJwt": "mocked_jwt_token"}
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        result = create_session(username=self.username, password=self.password)
        self.assertEqual(result, "mocked_jwt_token")

    @patch("auth.requests.post")
    def test_unsuccessful_authentication(self, mock_post: mock.MagicMock) -> None:
        """Test if authentication was not successful.

        Password or User was incorrect
        """
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "401 Client Error: Unauthorized"
        )
        mock_post.return_value = mock_response

        with self.assertRaises(SystemExit):
            create_session(username=self.username, password=self.password)

    @patch("auth.requests.post")
    def test_invalid_request_error(self, mock_post: mock.MagicMock) -> None:
        """Test if authentication was not successful.

        Bad Request Status Code 400
        """
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "400 Client Error: Bad Request"
        )
        mock_post.return_value = mock_response

        with self.assertRaises(SystemExit):
            create_session(self.username, self.password)


if __name__ == "__main__":
    unittest.main()
