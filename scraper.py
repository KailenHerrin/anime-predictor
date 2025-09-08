import requests
from time import sleep
from datetime import date
import sys

REQUEST_DELAY_TIME = 1
MAX_ATTEMPTS = 3

"""
Given a valid URL, fetches it's contents.
If URL is invalid print error
"""
def fetch_html(url, parse_json=False):
    headers = {"User-Agent": "Mozilla/5.0"} # Prevents websites from blocking scripts
    # ^^^ Note: May need to impliment more detailed user agents and mutliple random rotating agents
    
    attempts = 0
    while attempts < MAX_ATTEMPTS: 
        attempts += 1

        response = requests.get(url, headers=headers)
        # Check if response is valid and return website information
        if response.status_code == 200:
            if parse_json is True: 
                return response.json() # Return the json formatted HTML text
            return response.text # Return the raw HTML text
        
        elif response.status_code == 429:
            sleep(REQUEST_DELAY_TIME + attempts)

        else:
            print(f"Failed to fetch {url} (Status Code: {response.status_code})")

            return None # Invalid url. Return nothing and print error message
"""
Extracts info from MAL and returns it as a dictionary
"""
def scrape_mal(season_data_raw):
    
    status = season_data_raw["data"]["status"]
    score = season_data_raw["data"]["score"]
    #studio = season_data_raw["data"]["studios"][0].get("name")
    episodes = season_data_raw["data"]["episodes"]
    dates = season_data_raw["data"]["aired"]["prop"]
    rank = season_data_raw["data"]["rank"]
    popularity = season_data_raw["data"]["popularity"]
    members = season_data_raw["data"]["members"]
    favorites = season_data_raw["data"]["favorites"]

    if status == "Not yet aired": # Checks for a confirmed sequal that is yet to air
        print("A sequel has already been confirmed. YAY!")
        sys.exit() # Exit process as a new season has been confirmed

    # Format start and end dates using datetime.date class
    start_date = date(dates["from"]["year"], 
                      dates["from"]["month"], 
                      dates["from"]["day"])
    

    end_date = start_date
    # Check if data is for a movie or for a season. If for a season get end dates. 
    # If for a movie end date is the same as start date
    if season_data_raw["data"]["type"] == "TV":
        # Check if show is currently airing
        if status != "Currently Airing":                  
            end_date = date(dates["to"]["year"], 
                            dates["to"]["month"], 
                            dates["to"]["day"])
        else: # A sequel is currenty being aired
            print("A sequel is currently airing. Enjoy!")
            sys.exit() # Exit process as a new season is currently in production
    

    # Store data as a library and then return it
    data = {
        "episodes": episodes,
        "score": score,
        "start_date": start_date,
        "end_date": end_date,
        "rank": rank,
        "popularity": popularity,
        "members": members,
        "favorites": favorites
    }
    return data

"""
Fetches the offical English and Japanese names that are most similar to the one provided by user
Used to confirm with user that predictor is predicing the correct show.
"""
def fetch_names(season_data_raw):
    names_list = season_data_raw["data"]["titles"]
    english_name, romaji_name = None, None

    for name in names_list:
        if name.get("type") == "English":
            english_name = name.get("title")
        elif name.get("type") == "Default":
            romaji_name = name.get("title")

    return english_name, romaji_name

"""
Needs Comment
"""
def check_sequel(prev_season_id):

    related_response = fetch_html(f"https://api.jikan.moe/v4/anime/{prev_season_id}/relations", parse_json=True)["data"]

    for response in related_response:

        if response['relation'] == "Sequel":
            return response.get("entry")[0].get("mal_id")
    
    return None
        