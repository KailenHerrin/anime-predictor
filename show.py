import datetime
from tabnanny import check
import scraper
from typing import Optional, Sequence
"""
Class description
"""
class Show:
    def __init__(self, english_title: str, romaji_title: str, studio: str, seasons: list['Season']):
        self.english_title = english_title
        self.romaji_title = romaji_title
        self.studio = studio if studio else None
        self.seasons = seasons if seasons else []
        self.start_date = seasons[0].start_date if seasons else None
        self.end_date = seasons[-1].end_date if seasons else None
    
    def __str__(self):
        return (
            f"Show names: {self.english_title}, {self.romaji_title}\n"
            f"Studio name: {self.studio}\n"
            f"Number of Seasons: {len(self.seasons)}\n"
            f"Aired from: {self.start_date} to: {self.end_date}\n"
            f"Average score: {self.get_score()}\n"
            f"Average rank: {self.get_rank()}\n"
            f"Average popularity: {self.get_popularity()}\n"
            f"Total members: {self.get_members()}\n"
            f"Total favorites: {self.get_favorites()}\n"
        )

    @classmethod
    def create_show(cls, jikan_response):
        while True: 
        
            english_title, romaji_title = scraper.fetch_names(jikan_response)

            data = scraper.scrape_mal(jikan_response)

            season = Season.from_raw_data(data)

            #Add season to show

            sequal = scraper.check_sequel(jikan_response)

            break

            
        
        

        


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
            
    def get_popularity(self):
        if not self.seasons:
                return None
            
        return sum(season.popularity for season in self.seasons if season.popularity is not None) / len(self.seasons)

    def get_members(self):
        total_members = 0
        for cur in self.seasons:
            total_members += cur.members
        
        return total_members
    
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
                 favorites: int):
        self.episodes = episodes if episodes else 0    
        self.score = score if score else 0
        self.start_date = start_date if start_date else None
        self.end_date = end_date if end_date else None
        self.rank = rank if rank else 0
        self.popularity = popularity if popularity else 0
        self.members = members if members else 0
        self.favorites = favorites if favorites else 0

    @classmethod
    def from_raw_data(cls, data: dict):
        return
        
         