import show
from main import process_anime
import argparse

def parse_args():
    """
    Parses command line arguments 
    Currently only checks for one tag --anime
    """

    parser = argparse.ArgumentParser(prog="Web-Scraper", 
                                     description="Scrapes the web for information on specified anime, predicts the status of the anime production.")    
    # Define CLI arguments
    parser.add_argument("--anime", type=str, required=True, help="Name of the anime to check.")
    parser.add_argument("--output", type=str, required=False, default="print", choices=["print", "csv", "json"], help="Optional output options. By default prints to standart output but can also be flagged to CSV or JSON")
    parser.add_argument("--file", type=str, required=False, default=None, help="Optional output file pointer. Defaults to a new file if left blank")
    
    return parser.parse_args()

def anime_predictor():
    """
    Takes CLI arguments and scrapes web for information
    """
    
    args = parse_args()
    
    # Handle CLI args
    anime_name = args.anime
    file_name = args.file if args.file else str(f"output.{args.output}")

    # Start the data scraping pipeline
    show = process_anime(anime_name)

    # Output format according to --output flag in arguments
    if args.output == "print":
        print(show)
    elif args.output == "csv":
        row = show.to_csv_row()
        print(row)
    elif args.output == "json": # CURRENTLY DOES NOTHING
        print("JSON not supported")
    else:
        print("Unknown output type")


if __name__ == "__main__":
    anime_predictor()