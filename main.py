from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

import json
import re


class Line(object):
    def __init__(self, season, ep, text):
        self.season = season
        self.ep = ep
        self.text = text
        self.wordCounter = len(text.split())


class Character(object):
    def __init__(self, name, line):
        self.name = name
        self.lines = [line]
        self.wordCounte = 0


Characters = []


def add_character(name, season, ep, text):
    line = Line(season, ep, text)
    newCharacter = Character(name, line)
    Characters.append(newCharacter)


def exist_character(name):
    for c in Characters:
        if (c.name == name):
            return c
    return False


def add_text(character, season, ep, text):
    line = Line(season, ep, text)
    character.lines.append(line)


def count_word_per_character(character):
    counter = 0
    for l in character.lines:
        counter = counter + l.wordCounter
    return counter


def write_to_file():
    with open('data.json', 'w') as outfile:
        json.dump(Characters, outfile)


def open_script():
    text = []
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(ChromeDriverManager().install())
    for season in range(1, 9):
        url = f"https://genius.com/albums/Game-of-thrones/Season-{season}-scripts"
        driver.get(url)
        episodes = driver.find_elements_by_class_name("chart_row-content")
        hrefs = []
        for episode in episodes:
            hrefs.append(episode.find_element_by_tag_name('a').get_attribute('href'))

        for i, href in enumerate(hrefs):
            driver.get(href)
            content = driver.find_element_by_class_name('lyrics')
            text.append({"season": season, "episode": 1+i, "text": content.text})
    driver.close()
    for ep in text:
        text_file = open(f"season{ep['season']}-episode{ep['episode']}.txt", "w", encoding="utf-8")
        text_file.write(ep['text'])
        text_file.close()


def parser(content, season, ep):
    lines = content.text.splitlines()
    for l in lines:
        words = l.split(":")
        if len(words) >= 2:
            if True:
                c = exist_character(words[0])
                if c:
                    add_text(c, season, ep, words[1])
                else:
                    add_character(words[0], season, ep, words[1])


def print_for_check():
    for c in Characters:
        print('Name: ' + c.name)
        words = count_word_per_character(c)
        print('words: ' + str(words))
        # i = 1
        # for l in c.lines:
        #     # print('season: '+ l.season)
        #     # print('episode: ' + l.ep)
        #     print(str(i) + ' ' + l.text)
        #     i = i + 1


open_script()
