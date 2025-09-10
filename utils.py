import sys
import re

def normalize_string(string):
    """
    Takes a string as input
    Removes spaces, capitals, symbols, and punctuation
    Returns normalized string
    """

    string = re.sub(r'[^a-zA-Z0-9.,!?]', '', string.lower().strip())
    return string

def verify_name(requested_name, english_name):
    """
    Verifys that provided name is valid and exists in Jikan database. 
    Normalizes string to handle case sensitivity, trailing spaces, etc
    Returns the english and romaji names as they appear in Jikan databse. 
    """
    
    # Check if english title is the same as the requested title
    if normalize_string(english_name) != normalize_string(requested_name):
        answer = input(f"""Couldn't find results for: {requested_name}\nDid you mean: {english_name} """)
        
        if answer == "yes":
            print(f"Searching the web for data on: {english_name}...")     
        else:
            sys.exit()
    else:
        print(f"Searching the web for data on: {english_name}...")
