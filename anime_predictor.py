import argparse
from main import process_anime

"""
Parses command line arguments 
Currently only checks for one tag --anime
"""
def parse_args():
    parser = argparse.ArgumentParser(prog="Web-Scraper", 
                                     description="Scrapes the web for information on specified anime, predicts the status of the anime production.")    
    
    # Define CLI arguments
    parser.add_argument("--anime", type=str, required=True, help="Name of the anime to check.")

    return parser.parse_args()

"""
Takes CLI arguments and scrapes web for information
"""
def anime_predictor():
    args = parse_args()

    anime_name = args.anime

    status = process_anime(anime_name)

    print(status)


if __name__ == "__main__":
    anime_predictor()