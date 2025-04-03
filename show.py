class Show:
    def __init__(self, title, seasons):
        self.title = title
        self.seasons = seasons if seasons else []

class Season:
    def __init__(self, season_number, episodes):
        self.season_number = season_number
        self.episodes = episodes if episodes else []        