"""
    Testing suite for the mission_blue module.
"""

#pylint: disable=W0613
#pylint: disable=C0301
#pylint: disable=E0401

import unittest
from unittest.mock import patch
from auth import load_credentials

class TestLoadCredentials(unittest.TestCase):
    """
    Testing the load_credentials method
    """

    @patch("auth.load_dotenv", return_value=False)
    def test_no_env(self, mock_load_dotenv):
        """
        Test if .env file does not exist
        """
        with self.assertRaises(SystemExit) as cm:
            load_credentials()
        self.assertEqual(cm.exception.code, 1)

        mock_load_dotenv.assert_called_once()

    @patch("os.getenv", side_effect=lambda key: "" if key in ["BLUESKY_HANDLE", "BLUESKY_APP_PASSWORD"] else None)
    @patch("auth.load_dotenv", return_value=True)
    def test_env_with_no_credentials(self, mock_load_dotenv, mock_getenv):
        """
        Test if .env exist but username and password are empty
        """
        with self.assertRaises(AssertionError) as cm:
            load_credentials()
        self.assertIn("can not be empty", str(cm.exception))

    @patch("auth.load_dotenv", return_value=True)
    @patch("os.getenv", side_effect=lambda key: "any_value" if key in ["BLUESKY_HANDLE", "BLUESKY_APP_PASSWORD"] else None)
    def test_env_exist_with_valid_credentials(self, mock_load_dotenv, mock_getenv):
        """
        Test if .env exists with valid username and password
        """
        credentials = load_credentials()
        self.assertTrue(all(credentials))


if __name__ == "__main__":
    unittest.main()
