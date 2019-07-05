### About the project:

As a part of a Digital Humanities course for computer science students from Ben Gurion University taught by Yael Netzer,
we collected all the scripts of “Game of thrones” , analyzed the dominance of a character by spoken words and visualized
it into graphs according characters, gender and houses throughout the seasons and in the whole series.

#### Scrips directory:

objects.py - Line and Character object definition

character.py - Character list creation using wikipediapi and dbpedia

main.py - Includes open_script() func that extracts all Game of Throne transcripts from "genius" website
 to files using selenium library, parser() func that pars the files into characters and lines and update the
 character list (exporting it to json), func to each csv creation (for each character/season/main/houses and more)
 reading from the result character list.
 
topic_modeling.py - Includes two functions -
 1. Word cloud creation using nltk and Wordcloud libraries 2. Runs LDA (topic modeling) algorithm on the text.

#### transcripts directory:
All the text files (transcripts) extracted from "genius" website before parsing  - file per episode with indicative names.

#### word_cloud directory:
The result image of the word cloud function.

#### results directory:
Two jsons - 1. character list which includes the lines and the words counters.
            2. character list which include only details (name, gender, house and aliases)

#### cvcs directory: 
all the csv files created in main.py functions based on the result json. Different csvs with quiet same
 info for graph creation convenience (research and data visualization) 
 
*characters dir: csv for each character [season #, # of words]
    
*seasons dir: csv for each season includes all characters [Name,Gender,# of Words]
    
*episodes.csv - [# season, # episodes]
    
*houses_occurrences.csv - [house name, # of occurrences]
    
*main_seasons_separately.csv - [Name,Gender,House,Season,Total # of words]
    
*main_unify.csv - [Name,Gender,House,Season1,Season2,Season3,Season4,Season5,Season6,Season7,Season8,Total # of words]





