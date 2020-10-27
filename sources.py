import requests as rq
from poem import Poem

def poems_from_web(url):
    """Takes an author url from the PoemDB site, and then creates poem objects for each of the author's poems."""

    r = rq.get(url).json()  # Allows us to loop through the list of the author's poems

    for poem in r:
        poem_url = url[:27] + ",title" + url[27:-6] + ";" + poem["title"]  # syntax allowing us to access poems
        poem_info = rq.get(poem_url).json()[0]

        poem_obj = Poem(poem_info["title"], poem_info["lines"], poem_info["linecount"])
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
        print(poem)