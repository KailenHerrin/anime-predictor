import scraper
import re

# Checks that this is a valid anime using Jikan API 
# if not prints message to user, and terminates process
# If valid, returns Romaji (Japanese) name 
def process_anime(anime_name):
    # Get api response from jikan api 
    jikan_url = f"https://api.jikan.moe/v4/anime?q={anime_name}&limit=1"
    jikan_response = scraper.fetch_html((jikan_url), json=True)

    english_name = ""
    romaji_name = ""

    # Iterate through all titles to find English and Romaji titles
    for title in jikan_response["data"][0]["titles"]:
        if title["type"] == "Default":
            romaji_name = title["title"]
        elif title["type"] == "English":
            english_name = title["title"]

    # Check if english title is the same as the requested title
    if normalize_string(english_name) != normalize_string(anime_name):
        print(f"""Couldn't find results for: {anime_name} 
              Did you mean: {english_name}""")
    else:
        print(f"Searching the web for data on: {english_name}...")
    
    # Get link to myanimelist
    my_anime_list_link = jikan_response["data"][0]["url"]

    my_anime_list_html_raw = scraper.fetch_html(my_anime_list_link)
    #print(my_anime_list_html_raw)
    


# Takes a string as input
# Removes spaces, capitals, symbols, and punctuation
# Returns normalized string
def normalize_string(string):
    string = re.sub(r'[^a-zA-Z0-9]', '', string.lower().strip())
    return string


if __name__ == "__main__":
    # Main shouldn't be run directly. Print warning message to user if attempted
    print("This file cannot be run directly. Please use 'anime_predictor.py'")