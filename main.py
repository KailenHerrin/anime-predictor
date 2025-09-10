import scraper
from show import Show

def process_anime(anime_name):
    """
    Checks that this is a valid anime using Jikan API 
    If not prints message to user, and terminates process
    If valid, returns Romaji (Japanese) name 
    """
    
    # Get api response from jikan api 
    jikan_url = f"https://api.jikan.moe/v4/anime?q={anime_name}&limit=1"
    
    mal_id = scraper.fetch_html((jikan_url), parse_json=True)['data'][0]['mal_id']
    
    show = Show.create_show(mal_id, anime_name)

    return show
    
if __name__ == "__main__":
    # Main shouldn't be run directly. Print warning message to user if attempted
    print("This file cannot be run directly. Please use 'anime_predictor.py'")