"""
    Testing suite for the mission_blue module.
"""

import tempfile
import os
import unittest


from file import (
    remove_duplicates,
    extract_post_data,
    extract_post_data_from_csv,
    validate_url,
)


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


class TestMissionBlueFileMethods(unittest.TestCase):
    """
    Run tests for the mission_blue module.
    """

    def test_validate_url(self):
        """
        Test case for the validate_url function.
        This test verifies that the given url contains the correct post data.
        Test data:
        - Post Links with valid and invalid post urls.
        - An expected result boolean.
        Assertions:
        - The result of validate_url(data) should match the expected_result.
        """

        cases = {
            "Post Exists": TestCase(
                data="https://bsky.app/profile/witheringtales.bsky.social/post/3legkyuzjs22m",
                expected_result=True,
            ),
            "Post Doesn't Exist": TestCase(
                data="https://bsky.app/profile/witheringtales.bsky.social/post/3legkyuzjs22",
                expected_result=False,
            ),
        }

        for case_name, case in cases.items():
            with self.subTest(case_name):
                result = validate_url(case.get_data())
                self.assertEqual(result, case.get_expected_result())

    def test_extract_post_data(self):
        """
        Test case for the extract_post_data function.
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
            "No Post Data": TestCase(
                data=[],
                expected_result=[],
            ),
            "Bad Post Data": TestCase(
                data=[
                    {
                        "record": {"text": ""},
                        "author": {"handle": ""},
                        "indexedAt": "",
                        "uri": "12345",
                    }
                ],
                expected_result=[],
            ),
            "Contains Post Data": TestCase(
                data=[
                    {
                        "record": {"text": "contentABC"},
                        "author": {"handle": "witheringtales.bsky.social"},
                        "indexedAt": "2023-01-01",
                        "uri": "3legkyuzjs22m",
                    }
                ],
                expected_result=[
                    {
                        "author": "witheringtales.bsky.social",
                        "content": "contentABC",
                        "created_at": "2023-01-01",
                        # pylint: disable=line-too-long
                        "post_link": "https://bsky.app/profile/witheringtales.bsky.social/post/3legkyuzjs22m",
                    },
                ],
            ),
        }

        for case_name, case in cases.items():
            with self.subTest(case_name):
                result = extract_post_data(case.get_data())
                self.assertEqual(result, case.get_expected_result())
                
    def test_extract_post_data_from_csv(self):
        cases = {
            "No Path": TestCase(data="", expected_result=[]),
            "File Contains Content": TestCase(
                data="""author,content,created_at,post_link\nuser1,"post1",2023-01-01,link1\nuser2,"post2",2023-01-02,link2\nuser3,"post3",2023-01-03,link3""",
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
                        "author": "user3",
                        "content": "post3",
                        "created_at": "2023-01-03",
                        "post_link": "link3",
                    },
                ],
            ),
        }
        
        

        for case_name, case in cases.items():
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
                with self.subTest(case_name):
                    content = case.get_data()
                    if temp.write(content):
                        # If this line is commented, the test will fail. I believe that it is because
                        # the temp file is deleted once it is writen to causing the file to be empty
                        # when the extract_post_data_from_csv function is called in the next line.
                        print(f"file: {temp.read()}")
                        result = extract_post_data_from_csv(temp.name)
                        self.assertListEqual(result, case.get_expected_result())

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
