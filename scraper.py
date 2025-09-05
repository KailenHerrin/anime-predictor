import requests
import show
#from bs4 import BeautifulSoup
import urllib.parse
from datetime import date

#import praw (THIS IS REDDIT's API) I will impliment in the future

"""
Given a valid URL, fetches it's contents.
If URL is invalid print error
"""
def fetch_html(url, parse_json=False):
    headers = {"User-Agent": "Mozilla/5.0"} # Prevents websites from blocking scripts
    # ^^^ Note: Will need to impliment more detailed user agents and mutliple random rotating agents

    response = requests.get(url, headers=headers)

    # Check if response is valid and return website information
    if response.status_code == 200:
        if parse_json is True: 
            return response.json() # Return the json formatted HTML text
        return response.text # Return the raw HTML text
    else:
        print(f"Failed to fetch {url} (Status Code: {response.status_code})") 
        return None # Invalid url. Return nothing and print error message
"""
Extracts info from MAL and returns it as a dictionary
"""
def scrape_mal(jikan_response):
    # Get link to myanimelist 
    #mal_link = jikan_response["data"][0]["url"]
    status = jikan_response["data"][0]["status"]
    score = jikan_response["data"][0]["score"]
    studio = jikan_response["data"][0]["studios"][0]["name"] # Do I need this?
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

    # Check if show is currently airing, if it is airing there is no end_date
    if status != "Currently Airing":                  
        end_date = date(dates["to"]["year"], 
                        dates["to"]["month"], 
                        dates["to"]["day"])
    else:
        end_date = None

    # LIBRARY
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

def fetch_names(jikan_response):

    for title in jikan_response["data"][0]["titles"]:
        if title["type"] == "Default":
            romaji_name = title["title"]
        elif title["type"] == "English":
            english_name = title["title"]

    return english_name, romaji_name

def check_sequel(jikan_response):
    mal_id = jikan_response['data'][0]['mal_id']
    jikan_status = jikan_response["data"][0]["status"]

    related_response = fetch_html(f"https://api.jikan.moe/v4/anime/{mal_id}/relations", parse_json=True)
    
    sequel = related_response['data'][0]['relation']
    #print(sequel)
    if sequel == "Sequel":
        sequal_id = related_response['data'][0]['entry'][0]['name']
        sequel_response = fetch_html(f"https://api.jikan.moe/v4/anime/{mal_id}", parse_json=True)
        #scrape_mal(sequel_response)
        print(sequel_response['data']['score'])