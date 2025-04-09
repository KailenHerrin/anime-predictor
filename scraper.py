import requests
import show
from bs4 import BeautifulSoup
import urllib.parse
from datetime import date

#import praw (THIS IS REDDIT's API) I will impliment in the future

"""
Given a valid URL, fetches it's contents.
If URL is invalid print error
"""
def fetch_html(url, json=False):
    headers = {"User-Agent": "Mozilla/5.0"} # Prevents websites from blocking scripts
    # ^^^ Note: Will need to impliment more detailed user agents and mutliple random rotating agents

    response = requests.get(url, headers=headers)

    # Check if response is valid and return website information
    if response.status_code == 200:
        if json is True: 
            return response.json() # Return the json formatted HTML text
        return response.text # Return the raw HTML text
    else:
        print(f"Failed to fetch {url} (Status Code: {response.status_code})") 
        return None # Invalid url. Return nothing and print error message
"""
Needs a comment

Returns a show object

Needs to be able to check for a sequel, and if so loop creating Seasons
before adding them to the Show object

NEED TO BREAK THIS UP INTO A FEW METHODS!!!
"""
def scrape_mal(english_title, romaji_title, jikan_response):
    # Get link to myanimelist 
    mal_link = jikan_response["data"][0]["url"]

    jikan_status = jikan_response["data"][0]["status"]
    
    score = jikan_response["data"][0]["score"]
    studio = jikan_response["data"][0]["studios"][0]["name"]
    episodes = jikan_response["data"][0]["episodes"]
    dates = jikan_response["data"][0]["aired"]["prop"]
    rank = jikan_response["data"][0]["rank"]
    popularity = jikan_response["data"][0]["popularity"]
    members = jikan_response["data"][0]["members"]
    favorites = jikan_response["data"][0]["favorites"]

    # Format start and end dates using datetime.date class
    start_date = date(dates["from"]["year"], 
                      dates["from"]["month"], 
                      dates["from"]["day"])
    end_date = date(dates["to"]["year"], 
                      dates["to"]["month"], 
                      dates["to"]["day"])
    
    seasons = []
    cur_season = show.Season(
        episodes = episodes,
        score = score,
        start_date = start_date,
        end_date = end_date, 
        rank = rank, 
        popularity = popularity, 
        members = members, 
        favorites = favorites
    )
    seasons.append(cur_season)

    cur_show = show.Show(
        english_title = english_title, 
        romaji_title = romaji_title, 
        studio = studio, 
        seasons=seasons 
    )

    cur_show.print_show_info()
    #mal_data_raw = fetch_html(mal_link)
    
