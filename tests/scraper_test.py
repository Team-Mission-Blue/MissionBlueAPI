"""Testing suite for the mission_blue module."""

import unittest
from unittest.mock import Mock, patch

from scraper import (
    search_posts,
)


class TestCase:
    """Class used to store test data and expected results for the TestMissionBlue function."""

    def __init__(self, data, expected_result):
        self.data = data
        self.expected_result = expected_result

    def get_data(self):
        # pylint: disable=missing-function-docstring
        return self.data

    def get_expected_result(self):
        # pylint: disable=missing-function-docstring
        return self.expected_result


class TestSearchPosts(unittest.TestCase):
    """_summary_.

    Args:
        unittest (_type_): _description_

    """

    def test_search_posts(self):
        """Test case for the validate_url function.
        This test verifies that the given url contains the correct post data.
        Test data:
        - Post Links with valid and invalid post urls.
        - An expected result boolean.
        Assertions:
        - The result of validate_url(data) should match the expected_result.
        """
        # If any of the test cases fail, try looking at the no_content_template variable
        # within the validate_url function.
        cases = {
            "Post Exists": TestCase(
                data="https://bsky.app/profile/witheringtales.bsky.social/post/3legkyuzjs22m",
                expected_result=True,
            ),
            # If the test case fails, look at the validate_url function logic for guidance
            # on how to fix the test case.
            "Post Doesn't Exist": TestCase(
                data="https://bsky.app/profile/witheringtales.bsky.social/post/3legkyuzjs22",
                expected_result=False,
            ),
        }

        for case_name, case in cases.items():
            with self.subTest(case_name):
                result = validate_url(case.get_data())
                self.assertEqual(result, case.get_expected_result())


if __name__ == "__main__":
    unittest.main()
