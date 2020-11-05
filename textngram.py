import nltk
from nltk import ngrams
from nltk.corpus import wordnet
nltk.download('wordnet')
import collections
import random
import syllables

class Text_NGRAM:
    """
    A class that contains our methods for our ngrams model...

    Methods
    -------

    Attributes
    ----------
    source_words: a huge list of words that we will use to make our RNN

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

    def generate_next(self, words):
        """generates the next word in our poem..."""
        values = self.word_ngram_map[tuple(words)]
        num_list = []

        for entry in values:
            num_list.append(entry[1])

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
        line_lim = int(random.choice(self.lengths)) # uniformly chooses number of lines from prior Dickinson poems

        while line_len < line_lim:
            placeholder = len(word_list)

            next_word = self.generate_next(word_list[(placeholder - self.n + 1):placeholder])

            if next_word != "--":
                syll_count += syllables.estimate(next_word)

            word_list.append(next_word)
            string += next_word + " "

            if 6 <= syll_count < 8 and is_six:  # creating our meter, flipping back and forth
                string += "\n"
                syll_count = 0
                is_six = False
                line_len += 1
            if syll_count >= 8:
                string += "\n"
                syll_count = 0
                is_six = True
                line_len += 1


        return string

