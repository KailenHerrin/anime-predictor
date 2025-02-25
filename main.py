import scraper

def process_anime(anime_name):
    print(f"Searching the web for data on: {anime_name}...")

    scraper.fetch_anime_url("https://anilist.co/search/anime?q=", "Horimiya")


if __name__ == "__main__":
    # Main shouldn't be run directly. Print warning message to user if attempted
    print("This file cannot be run directly.Please use 'anime_predictor.py'.")