import scraper
from show import Show
import re
import sys

"""
Checks that this is a valid anime using Jikan API 
If not prints message to user, and terminates process
If valid, returns Romaji (Japanese) name 
"""
def process_anime(anime_name):
    # Get api response from jikan api 
    jikan_url = f"https://api.jikan.moe/v4/anime?q={anime_name}&limit=1"
    
    jikan_response = scraper.fetch_html((jikan_url), parse_json=True) 
    '''
        NSTEAD OF USING JIKAN RESPONSE HERE, USE THE RESPONSE WE GET FROM https://api.jikan.moe/v4/anime/< anime code >&limit=1
    '''
    
    #mal_id = jikan_response['data'][0]['mal_id']
    #related = (scraper.fetch_html(f"https://api.jikan.moe/v4/anime/{mal_id}/relations"))
    #print(related)

    # Verify anime name
    verify_name(anime_name, jikan_response)

    show = Show.create_show(jikan_response)
    #show.create_show(jikan_response)
    
    #print(show)
    
    # I need to change this to a bigger method called create_show
    #mal_data = scraper.scrape_mal(english_name, romaji_name, jikan_response)

    return show
    

"""
Takes a string as input
Removes spaces, capitals, symbols, and punctuation
Returns normalized string
"""
def normalize_string(string):
    string = re.sub(r'[^a-zA-Z0-9.,!?]', '', string.lower().strip())
    return string

"""
Verifys that provided name is valid and exists in Jikan database. 
Normalizes string to handle case sensitivity, trailing spaces, etc
Returns the english and romaji names as they appear in Jikan databse. 
"""
def verify_name(anime_name, jikan_response):
    english_name, romaji_name = scraper.fetch_names(jikan_response)
    
    # Check if english title is the same as the requested title
    if normalize_string(english_name) != normalize_string(anime_name):
        answer = input(f"""Couldn't find results for: {anime_name}\nDid you mean: {english_name} """)
        
        if answer == "yes":
            print(f"Searching the web for data on: {english_name}...")
            return english_name, romaji_name
        else:
            sys.exit()
    else:
        print(f"Searching the web for data on: {english_name}...")
        return english_name, romaji_name

if __name__ == "__main__":
    # Main shouldn't be run directly. Print warning message to user if attempted
    print("This file cannot be run directly. Please use 'anime_predictor.py'")