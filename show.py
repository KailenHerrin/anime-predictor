import datetime
import utils
import scraper
import os
import csv
from typing import Optional, Sequence

class Show:
    """
    Class description for a Show

    Attributes: English and Japanese titles, 
    a list of seasons with a length >= 0 date information, 
    start and end date as <datetime> objects

    Represents a show, made up of a list of seasons
    """

    def __init__(self, english_title: str, romaji_title: str, seasons: list['Season'], status: str):
        self.english_title = english_title
        self.romaji_title = romaji_title
        self.seasons = seasons if seasons else []
        self.start_date = seasons[0].start_date if seasons else None
        self.end_date = seasons[-1].end_date if seasons else None
        self.status = status if status else None
    
    def __str__(self):
        """
        Formats a show object when printed into a readable format.
        """

        return (
            f"Show names: {self.english_title}, {self.romaji_title}\n"
            f"Number of Seasons: {len(self.seasons)}\n"
            f"Aired from: {self.start_date} to: {self.end_date}\n"
            f"Average score: {self.get_score()}\n"
            f"Average rank: {self.get_rank()}\n"
            f"Average popularity: {self.get_popularity()}\n"
            f"Total members: {self.get_members()}\n"
            f"Total favorites: {self.get_favorites()}\n"
            f"Current Status: {self.status}\n"
        )
    
    @classmethod
    def create_show(cls, mal_id, requested_title):
        """
        Alternate Constructor for a show. 
        Intended to be the main constructor and used as part of the data pipeline.
        """

        seasons = []

        # Get raw data for initial season
        season_data_raw = scraper.fetch_html(f"https://api.jikan.moe/v4/anime/{mal_id}", parse_json=True)

        # Verify anime name
        english_title, romaji_title = scraper.fetch_names(season_data_raw)
        utils.verify_name(requested_title, english_title)

        while True: 
            data = scraper.scrape_mal(season_data_raw)

            seasons.append(Season.from_raw_data(data))

            sequel = scraper.check_sequel(mal_id)

            if sequel:
                mal_id = sequel
            else:
                break

            season_data_raw = scraper.fetch_html(f"https://api.jikan.moe/v4/anime/{mal_id}", parse_json=True)

        return cls (
            english_title = english_title,
            romaji_title = romaji_title,
            seasons = seasons if seasons[-1].status == "unconfirmed" else seasons[:-1], # Only include last season if it's finished airing
            status = cls.get_status(seasons[-1].status, len(seasons), seasons[-1].end_date)
        )
    
    def to_csv(self, filepath):
        """
        Converts current show to CSV. 
        If filepath is provided will attempt to append to file, if file does not exist it will first be created.
        If no filepath is provided will create new file in current directory named output.csv
        """
        
        header = ["anime", "seasons", "score", "rank", 
                  "popularity", "members", "favorites", 
                  "from", "until", "status"]
        
        row = [self.english_title, len(self.seasons), self.get_score(), self.get_rank(), 
               self.get_popularity(), self.get_members(), self.get_favorites(), 
               self.start_date, self.end_date, self.status]
        
        try: 
            # Attempt to open and write to filepath
            file_exists = os.path.isfile(filepath)

            with open(filepath, "a", newline="") as fp:
                writer = csv.writer(fp)

                if not file_exists:
                # Check if file exists, if not write a header 
                    writer.writerow(header)

                # Write row of data
                writer.writerow(row)
            
            print(f"Data saved to {filepath}")

        except FileNotFoundError:
            print("Error: The specified filepath is not valid.")

    def get_score(self):
        """
        Returns the average score of a show.
        If show has no seasons return None
        """

        if not self.seasons:
            return None
        
        return sum(season.score for season in self.seasons if season.score is not None) / len(self.seasons)
    
    def get_rank(self):
        """
        Returns the average rank of a show.
        If show has no seasons return None
        """
        
        if not self.seasons:
                return None
            
        return sum(season.rank for season in self.seasons if season.rank is not None) / len(self.seasons)
         
    def get_popularity(self):
        """
        Returns the average popularity of a show.
        If show has no seasons return None
        """ 

        if not self.seasons:
                return None
            
        return sum(season.popularity for season in self.seasons if season.popularity is not None) / len(self.seasons)

    def get_members(self):
        """
        Returns the total number of members belonging to a show.
        If show has no seasons return 0
        """

        total_members = 0
        for cur in self.seasons:
            total_members += cur.members
        
        return total_members

    def get_favorites(self):
        """
        Returns the total number of favorites belonging to a show.
        If show has no seasons return 0
        """ 

        total_favorites = 0
        for cur in self.seasons:
            total_favorites += cur.favorites
        
        return total_favorites
    
    @staticmethod
    def get_status(status, seasons, end_date):
        """
        Checks details on show status then returns a value to represent if a show has been
        confirmed
        unconfirmed
        finished
        discontinued

        Shows that are over <threshhold> years old and have multiple seasons are assumed to be finished
        Shows that are over <threshhold> years old and have only 1 season are assumed to be discontinued
        """

        # value to represent how old a show is before we consider it over
        threshold = 5
        
        # get threshold date 
        cur_date = datetime.date.today()
        threshold_date = cur_date.replace(year=cur_date.year - threshold)

        if status == "confirmed":
            return "confirmed"
        elif end_date < threshold_date and seasons > 1:
            return "finished"
        elif end_date < threshold_date and seasons == 1:
            return "discontinued"
        else:
            return "unconfirmed"

    
class Season:
    """
    Class description
    """

    def __init__(self, episodes: int, score: float, start_date: datetime.date, 
                 end_date: datetime.date, rank: int, popularity: int, members: int, 
                 favorites: int, status: str):
        self.episodes = episodes if episodes else 0    
        self.score = score if score else 0
        self.start_date = start_date if start_date else None
        self.end_date = end_date if end_date else None
        self.rank = rank if rank else 0
        self.popularity = popularity if popularity else 0
        self.members = members if members else 0
        self.favorites = favorites if favorites else 0
        self.status = status if status else None

    @classmethod
    def from_raw_data(cls, data: dict):
        """
        Alternate Constructor for a season. 
        Intended to be the main constructor and used as part of the data pipeline.
        """

        return cls (
            episodes=data.get("episodes", 0),
            score=data.get("score", 0),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            rank=data.get("rank", 0),
            popularity=data.get("popularity", 0),
            members=data.get("members", 0),
            favorites=data.get("favorites", 0),
            status=data.get("status")
        )
        
        
         