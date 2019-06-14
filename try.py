# Python
import requests
import wikipediaapi
import re

houses = ['Martell', 'Frey', 'Bolton', 'Targaryen', 'Stark', 'Lannister', 'Greyjoy', 'Arryn', 'Baratheon', 'Tully',
          'Tyrell', 'Mormont']

class Character(object):
    def __init__(self, name, line, gender, house):
        self.name = name
        self.lines = [line]
        self.wordCounte = 0
        self.gender = gender
        self.house = house


wiki = wikipediaapi.Wikipedia('en')
mutcd = wiki.page('List of Game of Thrones characters')
main_characters = mutcd.section_by_title('Main characters').sections
supporting_characters = mutcd.section_by_title('Supporting characters').sections
characters = []
name_list = ["Ned", "Jon", "Bran", "Littlefinger"]
for character in main_characters:
    if all(n not in character.title for n in name_list):
        name = character.title
        name1 = name.replace(' ', '_')
        # print(name1)
        data = requests.get(f'http://dbpedia.org/data/{name1}.json').json()
        character_db = data.get(f'http://dbpedia.org/resource/{name1}')
        ch_house = None
        gender = None
        if character_db:
            gender = character_db.get('http://dbpedia.org/property/gender')
            if gender:
                gender = gender[0]['value']
                # print(gender)
            else:
                gen = 0
                text = character.text.lower()
                if re.search(r"\bshe\b", text):
                    gender = 'Female'
                    gen += 1
                if re.search(r"\bhe\b", text):
                    gender = 'Male'
                    gen += 1
                if gen == 2:
                    if re.search(r"\bhe\b", text).start() < re.search(r"\bhe\b", text).start():
                        gender = 'Male'
                    else:
                        gender = 'Female'
                # print(name, gender)
            for i, house in enumerate(houses):
                if house in name:
                    ch_house = house
                    break
            if not ch_house:
                ch_house = character_db.get('http://dbpedia.org/property/family')
                if ch_house:
                    ch_house = ch_house[0]['value']
                else:
                    for relative in character_db.get('http://dbpedia.org/ontology/relative', []):
                        if "House" in relative['value']:
                            ch_house = relative['value'].split('_')[-1]
                            # print(ch_house)

        new_character = Character(name, ' ', gender, ch_house)
        characters.append(new_character)
for c in characters:
    print('Name: ', c.name)
    print('Gender: ', c.gender)
    print('House: ', c.house)
