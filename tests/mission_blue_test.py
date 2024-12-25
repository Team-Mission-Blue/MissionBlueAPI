"""
    Testing suite for the mission_blue module.
"""

import unittest
# pylint: disable=import-error
from mission_blue import remove_duplicates



class TestCase:
    """
        Class used to store test data and expected results for the TestMissionBlue function.
    """
    def __init__(self, data, expected_result):
        self.data = data
        self.expected_result = expected_result
    def get_data(self):
        # pylint: disable=missing-function-docstring
        return self.data
    def get_expected_result(self):
        # pylint: disable=missing-function-docstring
        return self.expected_result


class TestMissionBlue(unittest.TestCase):
    """
        Run tests for the mission_blue module.
    """
    def test_remove_duplicates(self):
        """
        Test case for the remove_duplicates function.

        This test verifies that the remove_duplicates function correctly removes
        duplicate entries from a list of dictionaries. Each dictionary represents
        a post with the following keys: 'author', 'content', 'created_at', and 'post_link'.

        Test data:
        - A list of dictionaries with some duplicate entries.
        - An expected result list with duplicates removed.

        Assertions:
        - The result of remove_duplicates(data) should match the expected_result.
        """

        cases = {
            "Contains Duplicates": TestCase(
                data=[
                    {
                        "author": "user1",
                        "content": "post1",
                        "created_at": "2023-01-01",
                        "post_link": "link1",
                    },
                    {
                        "author": "user2",
                        "content": "post2",
                        "created_at": "2023-01-02",
                        "post_link": "link2",
                    },
                    {
                        "author": "user1",
                        "content": "post1",
                        "created_at": "2023-01-01",
                        "post_link": "link1",
                    },
                ],
                expected_result=[
                    {
                        "author": "user1",
                        "content": "post1",
                        "created_at": "2023-01-01",
                        "post_link": "link1",
                    },
                    {
                        "author": "user2",
                        "content": "post2",
                        "created_at": "2023-01-02",
                        "post_link": "link2",
                    },
                ],
            ),
            "Doesn't Contains Duplicates": TestCase(
                data=[
                    {
                        "author": "user1",
                        "content": "post1",
                        "created_at": "2023-01-01",
                        "post_link": "link1",
                    },
                    {
                        "author": "user2",
                        "content": "post2",
                        "created_at": "2023-01-02",
                        "post_link": "link2",
                    },
                    {
                        "author": "user1",
                        "content": "post1",
                        "created_at": "2023-01-01",
                        "post_link": "link3",
                    },
                ],
                expected_result=[
                    {
                        "author": "user1",
                        "content": "post1",
                        "created_at": "2023-01-01",
                        "post_link": "link1",
                    },
                    {
                        "author": "user2",
                        "content": "post2",
                        "created_at": "2023-01-02",
                        "post_link": "link2",
                    },
                    {
                        "author": "user1",
                        "content": "post1",
                        "created_at": "2023-01-01",
                        "post_link": "link3",
                    },
                ],
            ),
        }

        for case_name, case in cases.items():
            with self.subTest(case_name):
                result = remove_duplicates(case.get_data())
                self.assertEqual(result, case.get_expected_result())


if __name__ == "__main__":
    unittest.main()
