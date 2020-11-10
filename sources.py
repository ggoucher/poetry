import requests as rq
from poem import Poem
from os import path
import json


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

        with open(poem_path, 'r') as f:  # writes a JSON file with our poem information
            poem_data = json.load(f)

            poem_obj = Poem(poem_data["title"], poem_data["lines"], poem_data["linecount"])
            Sources(poem_obj)


class Sources:
    """
    A class representing our poem sources from Emily Dickinson!

    Attributes
    ----------
    poem : Poem
        the individual poem we wish to store in our sources class

    source_info : List
        the list of strings containing individual words in Dickinson's poems

    poem_lengths : List
        the list of Dickinson's poem lengths

    Methods
    -------
    get_source_info(self):
        gets our source info list with our words

    get_poem_length(self):
        gets our poem length list with our poem lengths

    """
    source_info = []
    poem_lengths = []

    def __init__(self, poem):
        self.poem = poem
        for line in poem.lines:
            words_to_add = line.lower().split()
            for word in words_to_add:
                self.source_info.append(word)
        self.poem_lengths.append(poem.length)

    def get_source_info(self):
        """Gets the list of the words in Dickinson's poems"""
        return self.source_info

    def get_poem_length(self):
        """Gets the lengths of Dickinson's poems"""
        return self.poem_lengths
