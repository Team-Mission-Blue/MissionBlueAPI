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
python3 BlueSkyScraper.py
```

You will then be prompted to enter your query string.

Once you run the script you should see a directory named DataMiningProcessing. Within this directory will contain csv files that contain the posts corresponding to each sport scraped.
