import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Access credentials from the environment variables
BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")
BLUESKY_APP_PASSWORD = os.getenv("BLUESKY_APP_PASSWORD")

# Base URL
BASE_URL = "https://bsky.social/xrpc"


def create_session():
    """
    Authenticate and create a session to get the access token.

    :return: Access token (accessJwt) for authentication.
    """
    url = f"{BASE_URL}/com.atproto.server.createSession"
    payload = {"identifier": BLUESKY_HANDLE, "password": BLUESKY_APP_PASSWORD}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        session = response.json()
        return session["accessJwt"]
    except requests.exceptions.RequestException as e:
        print("Error during authentication:", e)
        print("Response:", response.text if "response" in locals() else "No response")
        exit(1)


# Figure Out
def search_posts(
    query, access_token, since, until, limit=25, sort="top", cursor="", posts=[]
):
    """
    Search for posts using the BlueSky API.

    :param query: The search query string.
    :param access_token: Access token for authentication.
    :param limit: Number of posts to fetch, can change in main.
    :param sort: Sorting order ('latest' or 'top').
    :return: List of posts.
    """
    url = f"{BASE_URL}/app.bsky.feed.searchPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    params = {
        "q": query,
        "sort": sort,
        "since": since,
        "until": until,
        "limit": limit,
        "cursor": cursor,
    }
    counter = 0
    while True:
        counter += 1
        try:
            response = requests.get(url, headers=headers, params=params)
            # print(response)
            response.raise_for_status()
            posts = response.json().get("posts", []) + posts
            data = response.json()

            next_cursor = data.get("cursor")
            if not next_cursor:
                return posts

            params["cursor"] = next_cursor
        except requests.exceptions.RequestException as e:
            print(f"Error fetching posts: {e}")
            print(
                "Response:", response.text if "response" in locals() else "No response"
            )
            return []


def extract_post_data(posts):
    """
    Extract relevant data from posts and filter by date range.

    :param posts: List of raw posts.
    :param start_date: Start date for filtering (YYYY-MM-DD).
    :param end_date: End date for filtering (YYYY-MM-DD).
    :return: List of dictionaries containing post data.
    """
    extracted_data = []
    # if start_date and end_date:
    #     start_date = datetime.strptime(start_date, "%Y-%m-%d")
    #     end_date = datetime.strptime(end_date, "%Y-%m-%d")

    for post in posts:
        try:
            post_content = post["record"].get("text", "")  # Extract the text content
            author_handle = post["author"]["handle"]  # Extract the author's handle
            created_at = post["indexedAt"]  # Extract the indexed timestamp
            # cid = post["cid"]
            # keys = post.keys()
            postId = post["uri"].split("/")[-1]
            postLink = f"https://bsky.app/profile/{author_handle}/post/{postId}"

            # Filter by date range
            # if start_date <= created_at_date <= end_date:
            extracted_data.append(
                {
                    "author": author_handle,
                    "content": post_content,
                    "created_at": created_at,
                    # "cid": cid,
                    # "keys": keys,
                    "postLink": postLink,
                }
            )
        except KeyError as e:
            print(f"Missing data in post: {e}")
    return extracted_data


def save_to_csv(post_data, filename):
    """
    Save post data to a CSV file.

    :param post_data: List of post data dictionaries.
    :param filename: Output CSV filename.
    """
    if post_data:
        if os.path.isfile(filename):
            os.remove(filename)
        df = pd.DataFrame(post_data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No posts to save.")


if __name__ == "__main__":
    # Get user input for the search query and date range
    sport_name = input("Enter the sport you're querying: ")
    search_query = "Olympics 2024 " + sport_name
    print(search_query)
    start_date = "2024-06-28T00:00:00Z"
    end_date = "2024-09-28T23:59:59Z"

    # Authenticate and create a session
    print("Authenticating...")
    access_token = create_session()
    print("Authentication successful.")

    # Fetch posts
    print("Fetching posts...")
    raw_posts = search_posts(
        search_query,
        access_token,
        start_date,
        end_date,
        limit=100,
        sort="latest",
        cursor="",
    )  # Can change limit

    # Extract post data
    print("Extracting post data...")
    post_data = extract_post_data(raw_posts)

    # print("Here is the data:", post_data)

    # Save posts to CSV
    print("Saving posts to CSV...")
    save_to_csv(post_data, f"{sport_name}.csv")
