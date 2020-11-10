import nltk
import collections
import random
import syllables
from nltk import ngrams
from nltk.corpus import wordnet

nltk.download('wordnet')

syntax_words = ["be", "the", "from", "form", "their", "there", "they're", "you", "yours", "to", "with", "is", "a",
                "did", "do"]

def poem_strip(string):
    """strips the '--' phrase from our poem in an attempt to ensure that the system reader function doesn't
    return an error... the '.' offers a similar break in the phrase."""

    return string.replace("--", ".")


class Text_NGRAM:
    """
    A class that contains our methods for our ngrams model...

    Methods
    -------
    generate_next(self, words):
        accesses our word_ngram_map with our two words, and chooses from all our possible values weighting on their
        frequencies

    generate_first_term(self, word):
        accesses our reverse_word_ngram_map with our starter word. If the starter isn't there, we try synonyms, and
        if they don't work, we'll just choose a random word from our word list. We use the reverse map to pick our first
        three words, setting us up for the rest of our generation.

    generate_poem(self, word, priors):
        Uses our inputted word and the prior words generated to start a string, and then uses ngrams to generate the
        rest of the poem. Additionally, we follow the aesthetic standard of an 8686 meter loosely, something that
        Dickinson liked to do.

    poem_string(self, poem):
        Strips a poem of "--" characters so that the system reader will read our poem without any errors...

    Attributes
    ----------
    word_list : List
        a huge list of words that we will use to make our NGRAMS model

    word_set : Set
        a set of the words that we will use to make our NGRAMS model

    n : Int
        the int n of our ngrams model

    lengths: List
        the list of all of our poem's lengths

    word_ngram_map: Dictionary
        a dictionary that stores the n-words prior to certain words in our NGRAM model

    word_ngram_map: Dictionary
        a dictionary that stores the n-words prior to certain words in our NGRAM model

    """

    def __init__(self, word_list, n, lengths):
        self.word_list = word_list
        self.word_set = set(word_list)
        self.n = n
        self.lengths = lengths

        self.word_ngram_map = dict()  # allows us to make a map to determine net words
        self.reverse_word_ngram_map = dict()  # allows us to make a map to determine net words

        model = ngrams(self.word_list, n)  # creates our ngram model

        model_count = collections.Counter(model)  # counts the frequency of our ngram results

        for entry in model_count:  # makes a dictionary of potential outcomes
            if entry[-1] not in self.reverse_word_ngram_map:
                self.reverse_word_ngram_map[entry[-1]] = [[entry[:-1], model_count[entry]]]
            else:
                self.reverse_word_ngram_map[entry[-1]].append([entry[:-1], model_count[entry]])

        for entry in model_count:  # makes a reverse dictionary for initial terms
            if entry[:-1] not in self.word_ngram_map:
                self.word_ngram_map[entry[:-1]] = [[entry[-1], model_count[entry]]]
            else:
                self.word_ngram_map[entry[:-1]].append([entry[-1], model_count[entry]])

    def generate_next(self, word_list):
        """generates the next word in our poem..."""

        placeholder = len(word_list)

        values = self.word_ngram_map[tuple(word_list[(placeholder - self.n + 1):placeholder])]

        num_list = []

        for entry in values:
            num_list.append(entry[1])

        for word in word_list:  # checking for synonyms in our text to establish a common theme
            synset = wordnet.synsets(word)
            synset_cleared = []

            for entry in synset:
                synset_cleared.append(entry.lemmas()[0].name())

            for i in range(len(values)):
                if values[i][0] in synset_cleared and values[i][0] not in syntax_words:
                    num_list[i] += 1

        return random.choices(values, weights=tuple(num_list), k=1)[0][0]

    def generate_first_term(self, word):
        """Chooses the first terms we'll use in our poems. If not currently present in our dictionaries, we will
        try to find synonyms..."""
        if word in self.reverse_word_ngram_map:
            values = self.reverse_word_ngram_map[word]  # finding the reverse terms to use
            num_list = []

            for entry in values:
                num_list.append(entry[1])
            return word, random.choices(values, weights=tuple(num_list), k=1)[0][0]  # choosing based on weights
        else:
            synset = wordnet.synsets(word)  # wishing to find synonyms in our outputs...
            for entry in synset:
                synonym = entry.lemmas()[0].name()
                if synonym in self.reverse_word_ngram_map:
                    return self.generate_first_term(synonym)

            return self.generate_first_term(random.choice(self.word_list))  # in case our synonym hunt doesn't work

    def generate_poem(self, word, priors):
        """Uses all prior gathered information and generates a poem using ngrams!"""
        word_list = list(priors)
        word_list.append(word)
        string = ""
        for item in word_list:
            string += item + " "

        syll_count = 0  # shows the syllabus count so that we can follow the 8686 meter...
        is_six = True

        line_len = 0  # shows us how many lines...
        line_lim = int(random.choice(self.lengths))  # uniformly chooses number of lines from prior Dickinson poems

        while line_len < line_lim:
            # generates our next word by calling the ngram dictionary with the two prior words...
            next_word = self.generate_next(word_list)

            if next_word != "--":  # sets us up to follow the 8686 meter.
                syll_count += syllables.estimate(next_word)

            word_list.append(next_word)  # stores our words thus far
            string += next_word + " "

            if 6 <= syll_count < 8 and is_six:  # creating our meter, flipping back and forth
                string += "\n"  # forms our aesthetic imagery
                syll_count = 0
                is_six = False
                line_len += 1
            if syll_count >= 8:
                string += "\n"
                syll_count = 0
                is_six = True
                line_len += 1

        if string[:2] == "-- ":  # makes sure that we don't start with grammatical symbols common to Dickinson
            return string[3:]
        elif string[:1] == "- ":  # makes sure that we don't start with grammatical symbols common to Dickinson
            return string[2:]

        return string
