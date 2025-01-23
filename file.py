"""
Mission Blue Module that holds file handling functions for saving and loading data
"""

import csv
import os
import sys
from difflib import unified_diff
import requests
import urllib3
import pandas as pd


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


def validate_url(url: str) -> bool:
    """
    Validate URL to ensure it is a valid URL.
    Args:
        url (str): URL to validate.
    Returns:
        bool: True if URL is valid, False otherwise.
    """
    no_content_template = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, viewport-fit=cover">
  <meta name="referrer" content="origin-when-cross-origin">
  <!--
    Preconnect to essential domains
  -->
  <link rel="preconnect" href="https://bsky.social">
  <link rel="preconnect" href="https://bsky.network">
  <title>Bluesky</title>

  <!-- Hello Humans! API docs at https://atproto.com -->

  <link rel="preload" as="font" type="font/woff2" href="https://web-cdn.bsky.app/static/media/InterVariable.c504db5c06caaf7cdfba.woff2" crossorigin>

  <style>
    /**
     * Minimum styles required to render splash.
     *
     * ALL OTHER STYLES BELONG IN `src/style.css`
     *
     * THIS NEEDS TO BE DUPLICATED IN `bskyweb/templates/base.html`
     */
    @font-face {
      font-family: 'InterVariable';
      src: url("https://web-cdn.bsky.app/static/media/InterVariable.c504db5c06caaf7cdfba.woff2") format('woff2');
      font-weight: 300 1000;
      font-style: normal;
      font-display: swap;
    }
    @font-face {
      font-family: 'InterVariableItalic';
      src: url("https://web-cdn.bsky.app/static/media/InterVariable-Italic.01dcbad1bac635f9c9cd.woff2") format('woff2');
      font-weight: 300 1000;
      font-style: italic;
      font-display: swap;
    }
    html {
      background-color: white;
    }
    @media (prefers-color-scheme: dark) {
      html {
        background-color: black;
      }
    }
    html,
    body {
      margin: 0px;
      padding: 0px;
      font-family: InterVariable, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Liberation Sans', Helvetica, Arial, sans-serif;
      text-rendering: optimizeLegibility;
      /* Platform-specific reset */
      -webkit-overflow-scrolling: touch;
      -webkit-text-size-adjust: 100%;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      -ms-overflow-style: scrollbar;
      font-synthesis-weight: none;
    }
    html,
    body,
    #root {
      display: flex;
      flex: 1 0 auto;
      min-height: 100%;
      width: 100%;
    }
    #splash {
      position: fixed;
      width: 100px;
      left: 50%;
      top: 50%;
      transform: translateX(-50%) translateY(-50%) translateY(-50px);
    }
    /**
     * We need these styles to prevent shifting due to scrollbar show/hide on
     * OSs that have them enabled by default. This also handles cases where the
     * screen wouldn't otherwise scroll, and therefore hide the scrollbar and
     * shift the content, by forcing the page to show a scrollbar.
     */
    body {
      width: 100%;
      overflow-y: scroll;
    }
  </style>

  <script defer="defer" src="https://web-cdn.bsky.app/static/js/94.34d93bfe.js"></script>
<link rel="stylesheet" href="https://web-cdn.bsky.app/static/css/main.183e8650.css">
<script defer="defer" src="https://web-cdn.bsky.app/static/js/main.df7c994b.js"></script>
  <link rel="apple-touch-icon" sizes="180x180" href="https://web-cdn.bsky.app/static/apple-touch-icon.png">
  <link rel="icon" type="image/png" sizes="32x32" href="https://web-cdn.bsky.app/static/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="https://web-cdn.bsky.app/static/favicon-16x16.png">
  <link rel="mask-icon" href="https://web-cdn.bsky.app/static/safari-pinned-tab.svg" color="#1185fe">
  <meta name="theme-color">
  <meta name="application-name" content="Bluesky">
  <meta name="generator" content="bskyweb">
  <meta property="og:site_name" content="Bluesky Social" />
  <link type="application/activity+json" href="" />

  
</head>
<body>
  <div id="root">
    <div id="splash">
      <!-- Bluesky SVG -->
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 320"><path fill="#0085ff" d="M180 142c-16.3-31.7-60.7-90.8-102-120C38.5-5.9 23.4-1 13.5 3.4 2.1 8.6 0 26.2 0 36.5c0 10.4 5.7 84.8 9.4 97.2 12.2 41 55.7 55 95.7 50.5-58.7 8.6-110.8 30-42.4 106.1 75.1 77.9 103-16.7 117.3-64.6 14.3 48 30.8 139 116 64.6 64-64.6 17.6-97.5-41.1-106.1 40 4.4 83.5-9.5 95.7-50.5 3.7-12.4 9.4-86.8 9.4-97.2 0-10.3-2-27.9-13.5-33C336.5-1 321.5-6 282 22c-41.3 29.2-85.7 88.3-102 120Z"/></svg>
    </div>
  </div>

  <noscript>
    <h1 lang="en">JavaScript Required</h1>
    <p lang="en">This is a heavily interactive web application, and JavaScript is required. Simple HTML interfaces are possible, but that is not what this is.
    <p lang="en">Learn more about Bluesky at <a href="https://bsky.social">bsky.social</a> and <a href="https://atproto.com">atproto.com</a>.
    
  </noscript>
</body>
</html>
"""

    try:
        page = urllib3.request("GET", url)
        content_string = page.data.decode("utf-8")
        diff = unified_diff(content_string, no_content_template)
        diff_string = "".join(diff)
        if diff_string == "":
            return False
        return True
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
        print("Page Not Found")
        sys.exit(1)


def extract_post_data(posts: list[dict])-> list[dict]:
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
            author_handle = post["author"].get(
                "handle", ""
            )  # Extract the author's handle
            created_at = post["indexedAt"]  # Extract the indexed timestamp
            post_id = post["uri"].split("/")[-1]
            post_link = f"https://bsky.app/profile/{author_handle}/post/{post_id}"

            if not validate_url(post_link):
                continue

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


def extract_post_data_from_csv(path: str) -> list[dict]:
    """
    Extract data from existing csv file.
    :param path: Path to file.
    :return: List of dictionaries containing post data from file.
    """
    post_from_csv = []
    with open(path, mode="r", encoding="utf-8") as file:
        csv_file = csv.DictReader(file)
        for lines in csv_file:
            post_from_csv.append(lines)
    return post_from_csv


def remove_duplicates(data: list[dict]) -> list[dict]:
    """
    This function removes duplicate entries from a list of dictionaries using the post_link key.
    Args:
        data list(dict): List of dictionaries with some duplicate entries.
    Returns:
        list(dict): List of dictionaries with duplicates removed.
    """
    post_links = set()
    unqiue_data = []
    for post in data:
        if post["post_link"] not in post_links:
            post_links.add(post["post_link"])
            unqiue_data.append(post)
    return unqiue_data


def save_to_csv(data: list[dict], path_to_file:str) -> None:
    """
    Save post data to a CSV file.
    :param post_data: List of post data dictionaries.
    :param filename: Output CSV filename.
    """
    if data:
        if os.path.isfile(path_to_file):
            data += extract_post_data_from_csv(path_to_file)
            data = remove_duplicates(data)
            os.remove(path_to_file)
        data_frame = pd.DataFrame(data)
        data_frame.to_csv(path_to_file, index=False)
        print(f"Data saved to {path_to_file}")
    else:
        print("No posts to save.")


# Valid URL
# validate_url("https://bsky.app/profile/witheringtales.bsky.social/post/3legkyuzjs22m")

# Invalid URL
# validate_url("https://bsky.app/profile/witheringtales.bsky.social/post/3legkyuzjs22")
