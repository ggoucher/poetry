import requests as rq
from poem import Poem
# import os
from os import path
import json
# from nltk.tokenize import TweetTokenizer #token
# import nltk
# import regex as re
# nltk.download('punkt')

def poems_from_web(url):
    """Takes an author url from the PoemDB site, and then creates poem objects for each of the author's poems."""

    r = rq.get(url).json()  # Allows us to loop through the list of the author's poems

    for poem in r:

        poem_path = "resources/" + poem["title"] + ".json"
        if not path.exists(poem_path):  # saves poems in local directory

            poem_url = url[:27] + ",title" + url[27:-6] + ";" + poem["title"]  # syntax allowing us to access poems
            poem_info = rq.get(poem_url).json()[0]

            with open(poem_path, 'w') as file:
                json.dump(poem_info, file)

        with open(poem_path, 'r') as f:
            poem_data = json.load(f)

            poem_obj = Poem(poem_data["title"], poem_data["lines"], poem_data["linecount"])
            Sources(poem_obj)


class Sources:
    """
    A class representing our poem sources from Emily Dickinson!

    Attributes
    ----------
    poem: a Poem object

    Methods
    -------

    """
    source_info = []

    def __init__(self, poem):
        self.poem = poem
        for line in poem.lines:
            words_to_add = line.lower().split()
            for word in words_to_add:
                self.source_info.append(word)

    def get_source_info(self):
        return self.source_info