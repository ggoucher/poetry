
class Poem:
    """
    A class representing our poem sources from Emily Dickinson!

    Attributes
    ----------
    title : string
        a poem's title
    lines : list
        a list of the lines in a poem
    length : int
        the line length of a poem

    """

    def __init__(self, title, lines, length):
        self.title = title
        self.lines = lines
        self.length = length

    def __repr__(self):

        return self.title + " " + str(self.length)
