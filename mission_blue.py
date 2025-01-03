"""
This module conatins the BlueSky Web Scrapper
"""

import os
import sys
import shutil
from dotenv import load_dotenv
import requests
import pandas as pd
from alive_progress import alive_bar
import click

# pylint: disable=C0301

lang_dict = {
    'Afar': 'aa',
    'Abkhazian': 'ab',
    'Afrikaans': 'af',
    'Akan': 'ak',
    'Albanian': 'sq',
    'Amharic': 'am',
    'Arabic': 'ar',
    'Aragonese': 'an',
    'Armenian': 'hy',
    'Assamese': 'as',
    'Avaric': 'av',
    'Avestan': 'ae',
    'Aymara': 'ay',
    'Azerbaijani': 'az',
    'Bashkir': 'ba',
    'Bambara': 'bm',
    'Basque': 'eu',
    'Belarusian': 'be',
    'Bengali': 'bn',
    'Bihari languages': 'bh',
    'Bislama': 'bi',
    'Tibetan': 'bo',
    'Bosnian': 'bs',
    'Breton': 'br',
    'Bulgarian': 'bg',
    'Burmese': 'my',
    'Catalan': 'ca',
    'Czech': 'cs',
    'Chamorro': 'ch',
    'Chechen': 'ce',
    'Chinese': 'zh',
    'Church Slavic': 'cu',
    'Chuvash': 'cv',
    'Cornish': 'kw',
    'Corsican': 'co',
    'Cree': 'cr',
    'Welsh': 'cy',
    'Danish': 'da',
    'German': 'de',
    'Divehi': 'dv',
    'Dzongkha': 'dz',
    'Greek, Modern (1453-)': 'el',
    'English': 'en',
    'Esperanto': 'eo',
    'Estonian': 'et',
    'Ewe': 'ee',
    'Faroese': 'fo',
    'Persian': 'fa',
    'Fijian': 'fj',
    'Finnish': 'fi',
    'French': 'fr',
    'Western Frisian': 'fy',
    'Fulah': 'ff',
    'Georgian': 'ka',
    'Gaelic': 'gd',
    'Irish': 'ga',
    'Galician': 'gl',
    'Manx': 'gv',
    'Guarani': 'gn',
    'Pushto': 'ps',
    'Quechua': 'qu',
    'Romansh': 'rm',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Sango': 'sg',
    'Sanskrit': 'sa',
    'Sinhala': 'si',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Northern Sami': 'se',
    'Samoan': 'sm',
    'Shona': 'sn',
    'Sindhi': 'sd',
    'Somali': 'so',
    'Sotho, Southern': 'st',
    'Spanish': 'es',
    'Sardinian': 'sc',
    'Serbian': 'sr',
    'Swati': 'ss',
    'Sundanese': 'su',
    'Swahili': 'sw',
    'Swedish': 'sv',
    'Tahitian': 'ty',
    'Tamil': 'ta',
    'Tatar': 'tt',
    'Telugu': 'te',
    'Tajik': 'tg',
    'Tagalog': 'tl',
    'Thai': 'th',
    'Tigrinya': 'ti',
    'Tonga (Tonga Islands)': 'to',
    'Tswana': 'tn',
    'Tsonga': 'ts',
    'Turkmen': 'tk',
    'Turkish': 'tr',
    'Twi': 'tw',
    'Uighur': 'ug',
    'Ukrainian': 'uk',
    'Urdu': 'ur',
    'Uzbek': 'uz',
    'Venda': 've',
    'Vietnamese': 'vi',
    'Volapük': 'vo',
    'Walloon': 'wa',
    'Wolof': 'wo',
    'Xhosa': 'xh',
    'Yiddish': 'yi',
    'Yoruba': 'yo',
    'Zhuang': 'za',
    'Zulu': 'zu',
    '':''
}


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


def resolve_handle_to_did(handle: str, token: str) -> str:
    """
    Resolve a Bluesky handle to DID
    """

    url = f"{BASE_URL}/com.atproto.identity.resolveHandle"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers, params={"handle": handle}, timeout=10)
        response.raise_for_status()
        return response.json().get("did", handle)
    except requests.exceptions.RequestException as err:
        print(f"Error resolving handle: {err}")
        return handle


def generate_query_params(
    token: str, query="", sort="", since="", until="",
    mentions="", author="", lang="", domain="", url="",
    tags=None, limit=25, cursor="", posts_limit=500
):
    # pylint: disable=R0917
    # pylint: disable=R0913
    # pylint: disable=C0301
    """Generates query parameters for the BlueSky search API.

    Args:
        token (str): The authorization token required to resolve handles.
        query (str, required): The search term for the BlueSky posts.
        sort (str, optional): The sorting criteria for results. 
            - Options include "top" for top posts or "latest" for the latest posts.
        since (str, optional): The start date for posts (ISO 8601 format).
        until (str, optional): The end date for posts (ISO 8601 format).
        mentions (str, optional): Mentions to filter posts by. 
            - Handles will be resolved to DIDs using the provided token.
        author (str, optional): The author of the posts (handle or DID).
            - Handles will be resolved to DIDs using the provided token.
        lang (str, optional): The language of the posts.
        domain (str, optional): A domain URL included in the posts.
        url (str, optional): A specific URL included in the posts.
        tags (list, optional): Tags to filter posts by (each tag <= 640 characters).
        limit (int, optional): The maximum number of posts to retrieve in a single response. 
            - Defaults to 25.
        cursor (str, optional): A pagination token to fetch a specific set of results.
            - Use the `cursor` value returned in the previous API response to navigate through paginated results.
            - If `cursor` is an empty string, the API fetches the first page of results.
            - Cursors are opaque strings generated by the API and should not be modified manually.
        posts_limit (int, optional): The maximum number of posts to retrieve across all responses.
            - Defaults to 500.

    Returns:
        dict: A dictionary containing the query parameters for the API request.
    """
    if mentions:
        mentions = resolve_handle_to_did(mentions, token)
    if author:
        author = resolve_handle_to_did(author, token)

    #print(f"Generated query parameters: {locals()}")
    return {
        "q": query,
        "sort": sort,
        "since": since,
        "until": until,
        "mentions": mentions,
        "author": author,
        "lang": lang,
        "domain": domain,
        "url": url,
        "tag": tags,
        "limit": limit,
        "cursor": cursor,
        "posts_limit": posts_limit
    }


def search_posts(params, token):
    # pylint: disable=E1102
    # pylint: disable=C0301

    """
    Search for posts using the BlueSky API.

    Args:
        params (dict): The query parameters for the API request.
            - query (str, required): The search term for the BlueSky posts.
            - sort (str, optional): The sorting criteria for results. 
               Options include "top" for top posts or "latest" for the latest posts.
            - since (str, optional): The start date for posts (ISO 8601 format).
            - until (str, optional): The end date for posts (ISO 8601 format).
            - mentions (str, optional): Mentions to filter posts by. 
            - Handles will be resolved to DIDs using the provided token.
            - author (str, optional): The author of the posts (handle or DID).
            - lang (str, optional): The language of the posts.
            - domain (str, optional): A domain URL included in the posts.
            - url (str, optional): A specific URL included in the posts.
            - tags (list, optional): Tags to filter posts by (each tag <= 640 characters).
            - limit (int, optional): The maximum number of posts to retrieve in a single response. 
                Defaults to 25.
            - cursor (str, optional): Pagination token for continuing from a previous request.
            - posts_limit (int, optional): The maximum number of posts to retrieve across all responses.
                Defaults to 500. 

    Returns:
        list: A list of posts matching the search criteria.

    Notes:
        - Progress is displayed using a progress bar indicating the number of posts fetched.
        - Handles pagination automatically until `posts_limit` is reached or no further results are available.
        - Logs and returns partial results if an error occurs during fetching.
    """
    posts = []
    url = f"{BASE_URL}/app.bsky.feed.searchPosts"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    total_fetched = 0
    posts_limit = params.get("posts_limit", 1000)

    with alive_bar(posts_limit) as progress:
        while True:
            try:
                response = requests.get(url, headers=headers, params=params, timeout=10)
                # print(response)
                response.raise_for_status()
                data = response.json()

                #Check if we have reached our overall posts limit
                new_posts = data.get("posts", [])
                posts.extend(new_posts)
                total_fetched += len(new_posts)

                #Update progress bar
                progress(len(new_posts))

                if posts_limit and total_fetched >= posts_limit:
                    print(f"Fetched {total_fetched} posts, total: {total_fetched}/{posts_limit}")
                    return posts[:posts_limit]

                #Move to the enxt page if available
                next_cursor = data.get("cursor")
                if not next_cursor:
                    print(f"All posts fetched. Total: {total_fetched}")
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


# Begin Click CLI

@click.command()
@click.option(
    '-q',
    '--query',
    type=str,
    required=True,
    help='Search query string. Required'
)

@click.option(
    '-s',
    '--sort',
    type=click.Choice(['top', 'latest'], case_sensitive=False),
    required=False,
    help='Rank results by "top" or "latest',
)

@click.option(
    '--since',
    type=str,
    required=False,
    help=(
        'Filter results for posts after the specified datetime (inclusive). '
        'Use ISO 8601 format: "YYYY-MM-DD" or full datetime. Uses "sortAt" timestamp.'
    )
)

@click.option(
    '--until',
    type=str,
    required=False,
    help=(
        'Filter results for posts before the specified datetime (not inclusive). '
        'Use ISO 8601 format: "YYYY-MM-DD" or full datetime. Uses "sortAt" timestamp.'
    )
)

@click.option(
    '-m',
    '--mentions',
    type=str,
    help='Filter posts mentioning the specified account (omit the @ symbol).'
)

@click.option(
    '-a',
    '--author',
    type=str,
    required=False,
    help='Filter posts by the specified account (omit the @ symbol).'
)

@click.option(
    '-l',
    '--lang',
    type=str,
    required=False,
    help=f"Filter posts by language.\n\nLanguage Options:\n\n {', '.join(list(lang_dict.keys()))}\n\n"
)

@click.option(
    '-d',
    '--domain',
    type=str,
    required=False,
    help='Filter posts containing links to the specified domain.'
)

@click.option(
    '-u',
    '--url',
    type=str,
    required=False,
    help='Filter posts containing links to the specified url.'
)

@click.option(
    '-t',
    '--tags',
    type=str,
    multiple=True,
    required=False,
    help=(
        'Filter posts by hashtag (omit the # symbol). '
        'Multiple tags can be specified: -t tag1 -t tag2. OR -t "tag1, tag2"'
    )
)

@click.option(
    '--limit',
    type=click.IntRange(1, 100),
    required=False,
    default=25,
    help=(
        'Set the maximum number of posts to retrieve in a single API response. This controls the page size for requests. '
        'Pagination is always enabled, and this option determines how many posts each request retrieves, up to a maximum of 100. '
        'The default value is 25 if not specified.'
    )
)
@click.option(
    '--posts_limit',
    type=click.IntRange(1, None),
    required=False,
    help=(
        'Set the total number of posts to fetch from the API across all paginated responses. This value limits the total data retrieved '
        'even if multiple API calls are required. If not specified, 1000 posts will be recieved.'
    )
)

def main(query="", sort="", since="", until="", mentions="", author="", lang="", domain="", url="", tags=tuple(), limit=25, posts_limit=1000):
    """
    method that tests if each click param flag is being passed in correctly
    """
    # pylint: disable=R0913
    # pylint: disable=R0914
    # pylint: disable=R0917
    print("Loading Credentials...")
    bluesky_handle, bluesky_app_password = load_credentials()

    # Authenticate and create a session
    print("Authenticating...")
    access_token = create_session(bluesky_handle, bluesky_app_password)
    print("Authentication successful.")

    query_param = generate_query_params(
        access_token, query, sort, since, until, mentions,
        author, lang, domain, url, tags, limit, posts_limit=posts_limit, cursor="")


    # Fetch posts
    print("Fetching posts...")
    raw_posts = search_posts(query_param, access_token)

    # Extract post data
    print("Extracting post data...")
    post_data = extract_post_data(raw_posts)

    # print("Here is the data:", post_data)

    # Save posts to CSV
    print("Saving posts to CSV...")
    save_to_csv(post_data, f"{query}.csv")

if __name__ == "__main__":
    main()
