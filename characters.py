import json
import re
import requests
import wikipediaapi
from objects import Character

houses = ['Tarly', 'Martell', 'Frey', 'Bolton', 'Targaryen', 'Stark', 'Lannister', 'Greyjoy', 'Arryn', 'Baratheon',
          'Tully', 'Tyrell', 'Mormont']
houses_in_text = ['of House Tarly', 'of House Martell', 'of House Frey', 'of House Bolton', 'of House Targaryen',
                  'of House Stark', 'of House Lannister', 'of House Greyjoy', 'of House Arryn', 'of House Baratheon',
                  'of House Tully', 'of House Tyrell', 'of House Mormont']

exceptions_name_list = ["Ned", "Jon", "Bran", "Littlefinger"]
correct_name_list = ["Ned Stark", "Jon Snow (character)", "Bran Stark", "Petyr Baelish"]

characters = []
supporting_characters = None
main_characters = None


def print_characters():
    for character in characters:
        print(character)


def open_page():
    global supporting_characters, main_characters
    wiki = wikipediaapi.Wikipedia('en')
    mutcd = wiki.page('List of Game of Thrones characters')
    supporting_characters = mutcd.section_by_title('Supporting characters').sections
    main_characters = mutcd.section_by_title('Main characters').sections


def extract_gender(text):
    gender = None
    gen = 0
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
    return gender


def parse_supporting_characters():
    global supporting_characters
    for house in supporting_characters:
        if 'House' in house.title:
            characters_in_house = house.text.split('\n')
            for character in characters_in_house:
                # extract name:
                name = character.title().split('(')[0][:-1]
                # extract house/family
                ch_house = None
                for i, family in enumerate(houses):
                    if family in name or houses_in_text[i] in character.title():
                        ch_house = family.replace('House ', '')
                        break
                # to lower case:
                text = character.title().lower()
                # extract gender:
                gender = extract_gender(text)
                characters.append(Character(name, [], gender, ch_house))


def parse_main_characters():
    global main_characters
    for character in main_characters:
        name_tmp = None
        aliases = []
        for i, exep in enumerate(exceptions_name_list):
            if exep in character.title:
                name = correct_name_list[i].replace(' (character)', '')
                name_tmp = correct_name_list[i]
                aliases.append(character.title)
                break
        if not name_tmp:
            name_tmp = character.title
            name = character.title
        tmp_name = name_tmp.replace(' ', '_')
        data = requests.get(f'http://dbpedia.org/data/{tmp_name}.json').json()
        character_dbpedia = data.get(f'http://dbpedia.org/resource/{tmp_name}')
        ch_house = None
        gender = None
        # extract data
        # from dbpedia
        if character_dbpedia:
            aliases += [alias['value'] for alias in character_dbpedia.get('http://dbpedia.org/ontology/alias', [])]
            gender = character_dbpedia.get('http://dbpedia.org/property/gender')
        if gender:
            gender = gender[0]['value']
        else:
            # from wikipedia api
            text = character.text.lower()
            gender = extract_gender(text)
        # extract house
        # by name
        for i, house in enumerate(houses):
            if house in name_tmp:
                ch_house = house
                break
        if not ch_house and character_dbpedia:
            # by dbpedia
            ch_house = character_dbpedia.get('http://dbpedia.org/property/family')
            if ch_house:
                ch_house = ch_house[0]['value'].replace('House ', '')
            else:
                for relative in character_dbpedia.get('http://dbpedia.org/ontology/relative', []):
                    if "House" in relative['value']:
                        ch_house = relative['value'].split('_')[-1].replace('House ', '')
        characters.append(Character(name, aliases, gender, ch_house))


def export():
    with open('character_list_with.json', 'w') as output:
        json.dump(characters, output, default=lambda c: c.__dict__)


open_page()
parse_main_characters()
parse_supporting_characters()
print_characters()
export()
