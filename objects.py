class Character(object):
    def __init__(self, name, aliases, gender, house):
        self.name = name
        self.aliases = aliases
        self.lines = {str(i): [] for i in range(1, 9)}
        self.gender = gender
        self.house = house
        self.season_counter = {str(i): [] for i in range(1, 9)}
        self.total_words = 0

    def __str__(self):
        return f'Name: {self.name}, Aliases: {self.aliases}, Gender: {self.gender}, House: {self.house}'


class Line(object):
    def __init__(self, season, ep, text):
        self.season = season
        self.ep = ep
        self.text = text
        self.wordCounter = len(text.split(" "))
