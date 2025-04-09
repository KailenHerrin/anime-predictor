import datetime
"""
Class description
"""
class Show:
    def __init__(self, english_title: str, romaji_title: str, studio: str, seasons: list['Season']):
        self.english_title = english_title
        self.romaji_title = romaji_title
        self.studio = studio if studio else None
        self.seasons = seasons if seasons else []
        self.start_date = seasons[0].start_date if seasons[0] else None
        self.end_date = seasons[-1].end_date if seasons[-1] else None
    
    def print_show_info(self):
        print(f"""Show names: {self.english_title}, {self.romaji_title}""")
        print(f"""Studio name: {self.studio}""")
        print(f"""Number of Seasons: {len(self.seasons)}""")
        print(f"""Aired from: {self.start_date} to: {self.end_date}""")
        print(f"""Average score: {self.get_score()}""")
        print(f"""Average rank: {self.get_rank()}""")
        print(f"""Average popularity: {self.get_popularity()}""")
        print(f"""Total members: {self.get_members()}""")
        print(f"""Total favorites: {self.get_favorites()}""")

    def get_score(self):
        total_score = 0
        for cur in self.seasons:
            total_score += cur.score
        
        return total_score / len(self.seasons)

    def get_rank(self):
        total_rank = 0
        for cur in self.seasons:
            total_rank += cur.rank
        
        return total_rank / len(self.seasons)
    
    def get_popularity(self):
        total_popularity = 0
        for cur in self.seasons:
            total_popularity += cur.popularity
        
        return total_popularity / len(self.seasons)

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
        self.episodes = episodes if episodes else []    
        self.score = score if score else None
        self.start_date = start_date if start_date else None
        self.end_date = end_date if end_date else None
        self.rank = rank if rank else None
        self.popularity = popularity if popularity else None
        self.members = members if members else None
        self.favorites = favorites if favorites else None

