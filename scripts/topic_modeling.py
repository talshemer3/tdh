import itertools
from wordcloud import WordCloud
import gensim
import json

from nltk.corpus import stopwords

from textblob import TextBlob
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *

import nltk


# nltk.download('brown')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')
# nltk.download('punkt')

# stopwords = stopwords.words('english').append(['ll', 're', 'come', 'com', 'tell', 'think'])
# print(stopwords)

def lemmatize_stemming(text):
    stemmer = SnowballStemmer("english")
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))


# Tokenize and lemmatize
def preprocess1(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))

    return result


def modeling():
    with open('character_list_results.json', 'r') as f:
        characters = json.load(f)
        lines = list(
            itertools.chain.from_iterable(
                [itertools.chain.from_iterable(c["lines"].values()) for c in characters]))
    # processed_lines = [TextBlob(line["text"]).noun_phrases for line in lines]
    processed_lines = [[word.lower() for (word, pos) in nltk.pos_tag(nltk.word_tokenize(line["text"])) if pos[0] == 'N']
                       for line in lines]
    # print(processed_lines)

    dictionary = gensim.corpora.Dictionary(processed_lines)
    bow_corpus = [dictionary.doc2bow(line) for line in processed_lines]
    lda_model = gensim.models.LdaMulticore(bow_corpus,
                                           num_topics=8,
                                           id2word=dictionary,
                                           passes=10,
                                           workers=3)
    for idx, topic in lda_model.print_topics(-1):
        print("Topic: {} \nWords: {}".format(idx, topic))
        print("\n")


def word_cloud():
    wordcloud = WordCloud(background_color="white", width=900, height=400, max_words=400, contour_width=6,
                          stopwords={"one", "don", "thing", "come"})
    with open('character_list_results.json', 'r') as f:
        characters = json.load(f)
        lines = list(
            itertools.chain.from_iterable([itertools.chain.from_iterable(c["lines"].values()) for c in characters]))
    # processed_lines = [TextBlob(line["text"]).noun_phrases for line in lines]
    processed_lines = [[word.lower() for (word, pos) in nltk.pos_tag(nltk.word_tokenize(line["text"])) if pos[0] == 'N']
                       for
                       line in lines]
    wordcloud.generate(','.join(list(itertools.chain.from_iterable(processed_lines))))
    wordcloud.to_image().save('img3.png')


if __name__ == '__main__':
    word_cloud()
    modeling()
