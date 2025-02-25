import requests
from bs4 import BeautifulSoup
import urllib.parse

#import praw (THIS IS REDDIT's API) I will impliment in the future

"""
Given a valid URL, fetches it's HTML contents.
If URL is invalid print error
"""
def fetch_html(url):
    headers = {"User-Agent: Mozilla/5.0"} # Prevents websites from blocking scripts
    # ^^^ Note: Will need to impliment more detailed user agents and mutliple random rotating agents

    response = requests.get(url, headers=headers)

    # Check if response is valid
    if response.status_code == 200:
        return response.text # Return the raw HTML file
    else:
        print(f"Failed to fetch {url} (Status Code: {response.status_code})") 
        return None # Invalid url. Return nothing and print error message

 
#def scrape_reddit(anime_name):
"""
Takes an anime name and a website base URL as arguments. 
Returns the first valid URL of the specified anime name on the specified website.

Most websites use the Japanese name, not the english name. Therefore the returned URL may use the Japanese name. 
"""
def fetch_anime_url(base_url, anime_name):
    anime_url = urllib.parse.quote(anime_name)

    search_url = base_url + anime_url

    print(search_url)

    html = fetch_html(search_url)
    if not html:
        return None
    
    soup = BeautifulSoup(html, "html.parser") # What does this do ?

    #print("E")
"""

"""
#def scrape_anime_forums(anime_name):
    

#def scrape_web():
    #scrape_anime_forums()
    #scrape_reddit()