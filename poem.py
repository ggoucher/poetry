

class Poem:
    """
    A class representing our poem sources from Emily Dickinson!

    Attributes
    ----------
    title: a poem's title
    lines: a list of the lines in a poem
    length: the line length of a poem


    Methods
    -------

    """

    def __init__(self, title, lines, length):
        self.title = title
        self.lines = lines
        self.length = length

    def __repr__(self):

        return self.title + " " + str(self.length)