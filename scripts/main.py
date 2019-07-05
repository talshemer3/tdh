import itertools
import json
import os
import csv
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from scripts.objects import Line
from scripts.objects import Character

characters = None


# extract transcripts to text files using selenium
def open_script():
    text = []
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(ChromeDriverManager().install())
    for season in range(2, 9):
        url = f"https://genius.com/albums/Game-of-thrones/Season-{season}-scripts"
        driver.get(url)
        episodes = driver.find_elements_by_class_name("chart_row-content")
        hrefs = []
        for episode in episodes:
            hrefs.append(episode.find_element_by_tag_name('a').get_attribute('href'))

        for i, href in enumerate(hrefs):
            driver.get(href)
            content = driver.find_element_by_class_name('lyrics')
            text.append({"season": season, "episode": 1 + i, "text": content.text})
    driver.close()
    for ep in text:
        text_file = open(f"season{ep['season']}-episode{ep['episode']}.txt", "w", encoding="utf-8")
        text_file.write(ep['text'])
        text_file.close()


# Iterating the text files (transcripts) with supporting some episodes with another encoding
def parser_helper():
    for file in os.listdir("episodes"):
        try:
            with open(f"episodes/{file}", 'r') as episode:
                parser(episode.read(), int(file[6]), int(file[:-4][15:]))
        except Exception:
            # print(file, Exception)
            with open(f"episodes/{file}", 'r', encoding='utf8') as episode:
                parser(episode.read(), int(file[6]), int(file[:-4][15:]))


not_important = []


# Parse transcript of content of ep in season (go over characters names and lines and update character list
def parser(content, season, ep):
    lines = content.splitlines()
    for l in lines:
        parts = l.split(":")
        if len(parts) >= 2 and len(parts[0]) < 20 and '[' not in parts[0]:
            # line of character
            character = get_character(parts[0])
            if character:
                add_line(character, season, ep, parts[1].strip())
            else:
                if parts[0] not in not_important:
                    not_important.append(parts[0])


# Create character object array from the character list lson created in characters.py
def create_characters_arr():
    global characters
    file = open('character_list_with_aliases.json', 'r')
    characters = json.load(file)
    characters = [Character(character['name'], character['aliases'], character['gender'], character['house']) for
                  character in characters]


# Return character object by name if not exist return None
def get_character(name):
    global characters
    name = name.split('(')[0].lower().strip()
    for c in characters:
        if re.search(fr'\b{name}\b', c.name.lower()):
            return c
        for alias in c.aliases:
            if re.search(fr'\b{name}\b', alias.lower()):
                return c


# Add line object to the line list of the given character
def add_line(character, season, ep, text):
    line = Line(season, ep, text)
    character.lines[str(season)].append(line)


# Calculate number of words in each season and in total eor each character and update counters in the character object
def count_words_per_season():
    global characters
    for character in characters:
        for season in range(1, 9):
            character.season_counter[str(season)] = sum([l.wordCounter for l in character.lines[str(season)]])
        character.total_words = sum(character.season_counter.values())


# [Name,Gender,House, number of words per season for each season, # of Words in total] csv creation
def create_main_csv():
    global characters
    first_row = ['Name', 'Gender', 'House', 'Season1', 'Season2', 'Season3', 'Season4', 'Season5', 'Season6', 'Season7',
                 'Season8', 'Total']
    with open('csvs/main.csv', 'w') as csvFile:
        writer = csv.writer(csvFile, lineterminator='\n')
        writer.writerow(first_row)
        for character in characters:
            row = [character.name, character.gender, character.house, *character.season_counter.values(),
                   character.total_words]
            writer.writerow(row)


# [Name,Gender,House, Season number, # of Words] csv creation
def main_separately_csv():
    with open('character_list_results.json', 'r') as file:
        characters_tmp = json.load(file)
    first_row = ['Name', 'Gender', 'House', 'Season', 'Total']
    with open('csvs/main_seasons_separately.csv', 'w') as csvFile:
        writer = csv.writer(csvFile, lineterminator='\n')
        writer.writerow(first_row)
        for character in characters_tmp:
            for key, season_counter in character["season_counter"].items():
                row = [character["name"], character["gender"], character["house"], key, season_counter]
                writer.writerow(row)


# [Name,Gender,# of Words] csv creation for each season
def create_csv_per_season():
    global characters
    first_row = ['Name', 'Gender', 'Words']
    for se in range(1, 9):
        with open(f'csvs/seasons/words_se_{str(se)}.csv', 'w') as csvFile:
            writer = csv.writer(csvFile, lineterminator='\n')
            writer.writerow(first_row)
            for c in characters:
                row = [c.name, c.gender, c.season_counter[str(se)]]
                writer.writerow(row)


# [season number, # of words] csv creation for each character
def create_csv_per_character():
    global characters
    first_row = ['Season', 'Words']
    for c in characters:
        file_name = c.name + '.csv'
        with open(f'csvs/characters/{file_name}.csv', 'w') as csvFile:
            writer = csv.writer(csvFile, lineterminator='\n')
            writer.writerow(first_row)
            for se in range(1, 9):
                row = [se, c.season_counter[str(se)]]
                writer.writerow(row)


# [season number, # of episodes] csv creation
def season_episodes_csv():
    arr = [10, 10, 10, 11, 11, 10, 7, 4]
    with open(f'csvs/episodes.csv', 'w') as csvFile:
        writer = csv.writer(csvFile, lineterminator='\n')
        writer.writerow(["season", "#episodes"])
        for i in range(1, 9):
            writer.writerow([i, arr[i - 1]])


# export character list with lines and counters to a json file
def export_result():
    with open('character_list_results.json', 'w', encoding="utf-8") as output:
        json.dump(characters, output, default=lambda c: c.__dict__)


houses = ['Tarly', 'Martell', 'Frey', 'Bolton', 'Targaryen', 'Stark', 'Lannister', 'Greyjoy', 'Arryn', 'Baratheon',
          'Tully', 'Tyrell', 'Mormont']


# [house, # of appearances in text] csv creation
def house_occurrences():
    with open('character_list_results.json', 'r') as file:
        characters_tmp = json.load(file)
        dom_house = {house: 0 for house in houses}
        for c in characters_tmp:
            for line in itertools.chain.from_iterable(c["lines"].values()):
                for house in houses:
                    dom_house[house] += line["text"].count(house)
    with open(f'csvs/houses_occurrences.csv', 'w') as csvFile:
        writer = csv.writer(csvFile, lineterminator='\n')
        writer.writerow(["house", "appearances"])
        for house in dom_house:
            writer.writerow([house, dom_house[house]])


if __name__ == '__main__':
    open_script()
    create_characters_arr()
    parser_helper()
    count_words_per_season()
    export_result()
    create_main_csv()
    create_csv_per_season()
    create_csv_per_character()
    house_occurrences()
    main_separately_csv()
    season_episodes_csv()
    print("done")
