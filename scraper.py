import requests
from bs4 import BeautifulSoup
import urllib.parse

#import praw (THIS IS REDDIT's API) I will impliment in the future

"""
Given a valid URL, fetches it's contents.
If URL is invalid print error
"""
def fetch_html(url, json=False):
    headers = {"User-Agent": "Mozilla/5.0"} # Prevents websites from blocking scripts
    # ^^^ Note: Will need to impliment more detailed user agents and mutliple random rotating agents

    response = requests.get(url, headers=headers)

    # Check if response is valid
    if response.status_code == 200:
        if json is True:
            return response.json() # Return the json formatted HTML text
        return response.text # Return the raw HTML text
    else:
        print(f"Failed to fetch {url} (Status Code: {response.status_code})") 
        return None # Invalid url. Return nothing and print error message

