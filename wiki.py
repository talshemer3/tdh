import re

import wikipediaapi


class Character(object):
    def __init__(self, name, line, gender, house):
        self.name = name
        self.lines = [line]
        self.wordCounte = 0
        self.gender = gender
        self.house = house


wiki = wikipediaapi.Wikipedia('en')
mutcd = wiki.page('List of Game of Thrones characters')
supporting_characters = mutcd.section_by_title('Supporting characters').sections
main_characters = []
houses = ['Tarly', 'Martell', 'Frey', 'Bolton', 'Targaryen', 'Stark', 'Lannister', 'Greyjoy', 'Arryn', 'Baratheon',
          'Tully',
          'Tyrell', 'Mormont']
houses_in_text = ['of House Tarly', 'of House Martell', 'of House Frey', 'of House Bolton', 'of House Targaryen',
                  'of House Stark',
                  'of House Lannister', 'of House Greyjoy', 'of House Arryn', 'of House Baratheon', 'of House Tully',
                  'of House Tyrell', 'of House Mormont']
character = None
for house in supporting_characters:
    if 'House' in house.title:
        characters = house.text.split('\n')
        for character in characters:
            name = character.title().split('(')[0][:-1]
            ch_house = None
            for i, family in enumerate(houses):
                if family in name or houses_in_text[i] in character.title():
                    ch_house = family
                    break
            gen = 0
            text = character.title().lower()
            if re.search(r'\bshe\b', text):
                gender = 'Female'
                gen += 1
            if re.search(r'\bhe\b', text):
                gender = 'Male'
                gen += 1
            if gen == 2:
                if re.search(r'\bhe\b', text).start() < re.search(r'\bhe\b', text).start():
                    gender = 'Male'
                else:
                    gender = 'Female'
            # print(name, gender)
            new_character = Character(name, ' ', gender, ch_house)
            main_characters.append(new_character)

for c in main_characters:
    print('Name: ', c.name)
    print('Gender: ', c.gender)
    print('House: ', c.house)
