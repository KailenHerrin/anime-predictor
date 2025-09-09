import show
from main import process_anime
import argparse

"""
Parses command line arguments 
Currently only checks for one tag --anime
"""
def parse_args():
    parser = argparse.ArgumentParser(prog="Web-Scraper", 
                                     description="Scrapes the web for information on specified anime, predicts the status of the anime production.")    
    # Define CLI arguments
    parser.add_argument("--anime", type=str, required=True, help="Name of the anime to check.")
    parser.add_argument("--output", type=str, required=False, default="print", choices=["print", "csv", "json"], help="Optional output options. By default prints to standart output but can also be flagged to CSV or JSON")
    parser.add_argument("--file", type=str, required=False, default=None, help="Optional output file pointer. Defaults to a new file if left blank")
    
    return parser.parse_args()

"""
Takes CLI arguments and scrapes web for information
"""
def anime_predictor():
    args = parse_args()
    
    # Handle CLI args
    anime_name = args.anime
    file_name = args.file if args.file else str(f"{anime_name.replace(" ", "_")}.{args.output}")

    # Start the data scraping pipeline
    show = process_anime(anime_name)

    # Output format according to --output flag in arguments
    if args.output == "print":
        print(show)
    elif args.output == "csv":
        print(f"Written to file: {file_name}")
    elif args.output == "json": # CURRENTLY DOES NOTHING
        print(f"Written to file: {file_name}")
    else:
        print("Unknown Output type")


if __name__ == "__main__":
    anime_predictor()