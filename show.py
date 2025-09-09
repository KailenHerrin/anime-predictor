import datetime
import utils
from tabnanny import check
import scraper
from typing import Optional, Sequence
"""
Class description for a Show

Attributes: English and Japanese titles, 
a list of seasons with a length >= 0 date information, 
start and end date as <datetime> objects
"""
class Show:
    def __init__(self, english_title: str, romaji_title: str, seasons: list['Season'], status: str):
        self.english_title = english_title
        self.romaji_title = romaji_title
        self.seasons = seasons if seasons else []
        self.start_date = seasons[0].start_date if seasons else None
        self.end_date = seasons[-1].end_date if seasons else None
        self.status = status if status else None
    
    """
    Formats a show object when printed into a readable format.
    """
    def __str__(self):
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
    
    """
    Alternate Constructor for a show. 
    Intended to be the main constructor and used as part of the data pipeline.
    """
    @classmethod
    def create_show(cls, mal_id, requested_title):
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
            status = seasons[-1].status
        )
    
    """
    Returns the average score of a show.
    If show has no seasons return None
    """
    def get_score(self):
        if not self.seasons:
            return None
        
        return sum(season.score for season in self.seasons if season.score is not None) / len(self.seasons)
    
    """
    Returns the average rank of a show.
    If show has no seasons return None
    """
    def get_rank(self):
        if not self.seasons:
                return None
            
        return sum(season.rank for season in self.seasons if season.rank is not None) / len(self.seasons)
   
    """
    Returns the average popularity of a show.
    If show has no seasons return None
    """       
    def get_popularity(self):
        if not self.seasons:
                return None
            
        return sum(season.popularity for season in self.seasons if season.popularity is not None) / len(self.seasons)

    """
    Returns the total number of members belonging to a show.
    If show has no seasons return 0
    """
    def get_members(self):
        total_members = 0
        for cur in self.seasons:
            total_members += cur.members
        
        return total_members

    """
    Returns the total number of favorites belonging to a show.
    If show has no seasons return 0
    """ 
    def get_favorites(self):
        total_favorites = 0
        for cur in self.seasons:
            total_favorites += cur.favorites
        
        return total_favorites
    

"""
Class description
"""
class Season:
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

    """
    Alternate Constructor for a season. 
    Intended to be the main constructor and used as part of the data pipeline.
    """
    @classmethod
    def from_raw_data(cls, data: dict):
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
        
        
         