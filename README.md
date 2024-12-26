# MissionBlueAPI

This is a Bluesky Web Scrapper

Before you can use the BlueSky Webscraper you need to register an account with [Bluesky](https://bsky.app/). Once you create your account you need to create a .env where you have 2 fields BLUESKY_HANDLE and BLUESKY_APP_PASSWORD. Your .env file look like this:

```text
BLUESKY_HANDLE="<Insert Bluesky Handle here>"
BLUESKY_APP_PASSWORD="<Insert Bluesky Password here>"
```

Once you have your creditinals set up the virtual enviornment for Mission Blue. Here are the following ways you can do it:

## For Mac OS and Linux

With Commands

```zsh
python3 -m venv .virtualenv
source .virtualenv/bin/activate
pip install -r requirements.txt
```

With Shell Script

```zsh
chmod +x ./setup.sh
./setup.sh
```

## For Windows

With Commands

```ps
python -m venv ./.virtualenv
.\.virtualenv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

With Powershell Script

```ps
.\setup.ps1
```

With exe file

```ps
start setup.exe
```

This will set up the Python virtual environment so that you can run the Bluesky Web Scraper and Sentiment Analysis Script.

Run this command to conduct the scrape:

```zsh
python3 mission_blue.py -q "Example search term"
```

Once you run the script you should see a directory named DataMiningProcessing. Within this directory will contain csv files that contain the posts corresponding to each sport scraped.

## Using the CLI to Search for Posts

The CLI is the main way to interact with this Python script, allowing you to search or BlueSky posts by providing query parameters. Here's how you can use it effectively:

* --query (required): The search term for the posts. This is mandatory.

* --limit: The maximum number of posts to retrieve in a single response (default: 25).

* --sort: The sorting criteria for the results. Available options:
   top: Retrieves top-ranked posts.
   latest: Fetches the most recent posts.

* --since: The start date for filtering posts (in ISO 8601 format).

* --until: The end date for filtering posts (in ISO 8601 format).

* --mentions: Filters posts mentioning a specific handle. Handles will be resolved to DIDs using the provided API token.

* --author: The author of the posts (handle or DID).

* --lang: Filters posts by language.

* --domain: Includes posts containing a specific domain URL.

* --url: Searches for posts containing a specific URL.

* --tags: Filters posts by tags (provide a comma-separated list).

* --posts_limit: The total number of posts to retrieve across all API responses (default: 500).

> [!TIP]
> Run the following code to find out any other aliases you can write to specify these flags and query params!
>
>```zsh
>python3 mission_blue.py --help
>```
