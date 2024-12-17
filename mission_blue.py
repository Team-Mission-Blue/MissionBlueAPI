"""
This module conatins the BlueSky Web Scrapper
"""

import os
import sys
import re
import shutil
from dotenv import load_dotenv
import requests
import pandas as pd


# Load environment variables from the .env file
def load_credentials() -> tuple[str, str]:
    """
    Validates and returns user BlueSky credentials

    Returns:
        tuple[str, str]: This ordered pair contains the Bluesky Username and Password
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


DIRECTORY_NAME = "Scrapped Posts"

# Generates Directory where scrapped post will reside in
if not os.path.isdir(DIRECTORY_NAME):
    try:
        os.mkdir(DIRECTORY_NAME)
        print(f"Directory '{DIRECTORY_NAME}' created successfully.")
    except FileExistsError:
        print(f"Directory '{DIRECTORY_NAME}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{DIRECTORY_NAME}'.")


# Base URL
BASE_URL = "https://bsky.social/xrpc"


def create_session(username: str, password: str):
    """
    Authenticate and create a session to get the access token.

    :return: Access token (accessJwt) for authentication.
    """
    url = f"{BASE_URL}/com.atproto.server.createSession"
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


def generate_query_params(
    query: str, since: str, until: str, limit=25, sort="top", cursor=""
):
    # pylint: disable=R0917
    # pylint: disable=R0913
    """This functions

    Args:
        query (str): The search term for the BlueSky Posts
        since (str): The start date for posts
        until (str): The end date for posts
        limit (int, optional): Number of posts queried. Max is 100.
        sort (str): Query for top posts or latest post
        cursor (str, optional): _description_. Defaults to "".

    Returns:
        _type_: _description_
    """
    return {
        "q": query,
        "sort": sort,
        "since": since,
        "until": until,
        "limit": limit,
        "cursor": cursor,
    }


def search_posts(params, token):
    """
    Search for posts using the BlueSky API.

    :param query: The search query string.
    :param access_token: Access token for authentication.
    :param limit: Number of posts to fetch, can change in main.
    :param sort: Sorting order ('latest' or 'top').
    :return: List of posts.
    """
    posts = []
    url = f"{BASE_URL}/app.bsky.feed.searchPosts"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    counter = 0
    while True:
        counter += 1
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            # print(response)
            response.raise_for_status()
            posts = response.json().get("posts", []) + posts
            data = response.json()

            next_cursor = data.get("cursor")
            if not next_cursor:
                return posts

            params["cursor"] = next_cursor
        except requests.exceptions.RequestException as err:
            print(f"Error fetching posts: {err}")
            print(
                "Response:", response.text if "response" in locals() else "No response"
            )
            return posts


def extract_post_data(posts):
    """
    Extract relevant data from posts and filter by date range.

    :param posts: List of raw posts.
    :param START_DATE: Start date for filtering (YYYY-MM-DD).
    :param END_DATE: End date for filtering (YYYY-MM-DD).
    :return: List of dictionaries containing post data.
    """
    extracted_data = []

    for post in posts:
        try:
            post_content = post["record"].get("text", "")  # Extract the text content
            author_handle = post["author"]["handle"]  # Extract the author's handle
            created_at = post["indexedAt"]  # Extract the indexed timestamp
            post_id = post["uri"].split("/")[-1]
            post_link = f"https://bsky.app/profile/{author_handle}/post/{post_id}"

            extracted_data.append(
                {
                    "author": author_handle,
                    "content": post_content,
                    "created_at": created_at,
                    "post_link": post_link,
                }
            )
        except KeyError as err:
            print(f"Missing data in post: {err}")
    return extracted_data


def save_to_csv(data, filename):
    """
    Save post data to a CSV file.

    :param post_data: List of post data dictionaries.
    :param filename: Output CSV filename.
    """
    if data:
        if os.path.isfile(filename):
            os.remove(filename)
        data_frame = pd.DataFrame(data)
        data_frame.to_csv(filename, index=False)
        shutil.move(f"{filename}", DIRECTORY_NAME)
        print(f"Data saved to {DIRECTORY_NAME}/{filename}")
        print(f"Data saved to {filename}")
    else:
        print("No posts to save.")


if __name__ == "__main__":

    print("Loading Credentials...")
    BLUESKY_HANDLE, BLUESKY_APP_PASSWORD = load_credentials()

    # Authenticate and create a session
    print("Authenticating...")
    access_token = create_session(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD)
    print("Authentication successful.")

    # Get user input for the search query and date range
    sport_name = input("Enter the sport you're querying: ")
    search_query = "Olympics 2024 " + sport_name
    print(search_query)
    START_DATE = "2024-06-28T00:00:00Z"
    END_DATE = "2024-09-28T23:59:59Z"
    SORT = "top"

    query_param = generate_query_params(search_query, START_DATE, END_DATE)

    # Fetch posts
    print("Fetching posts...")
    raw_posts = search_posts(query_param, access_token)

    # Extract post data
    print("Extracting post data...")
    post_data = extract_post_data(raw_posts)

    # print("Here is the data:", post_data)

    # Save posts to CSV
    print("Saving posts to CSV...")
    save_to_csv(post_data, f"{sport_name}.csv")
