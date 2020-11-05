import nltk
from nltk import ngrams
import collections

class Text_NGRAM:
    """
    A class that contains our methods for our ngrams model...

    Methods
    -------

    Attributes
    ----------
    source_words: a huge list of words that we will use to make our RNN

    """

    def __init__(self, word_list, n):
        self.word_list = word_list
        self.word_set = set(word_list)
        self.word_ngram_map = dict()  # allows us to make a map to determine net words

        model = ngrams(self.word_list, n)
        # for entry in model:
        #     print(entry)

        result = collections.Counter(model)
        print(result)

        # for entry in model:
        #     if entry[0] in self.word_ngram_map:
        #         print(self.word_ngram_map[entry[0]])
        #         for sequence in self.word_ngram_map[entry[0]]:
        #             print("what")
        #             # print(entry[0])
        #             # print(self.word_ngram_map[entry[0]])
        #             # print(sequence[0])
        #             for i in range(len(self.word_ngram_map[entry[0]])):
        #                 # print(self.word_ngram_map[entry[0]][i][0])
        #                 if sequence[0] == self.word_ngram_map[entry[0]][i][0]:# == sequence[0]:
        #                     print("hi")
        #                     # self.word_ngram_map[entry[0]][i][1] += 1
        #                     sequence[1] += 1
        #     else:
        #         if entry[0] in self.word_ngram_map:
        #             self.word_ngram_map[entry[0]].append([entry[1:], 1])
        #         else:
        #             self.word_ngram_map[entry[0]] = [[entry[1:], 1]]

        print(self.word_ngram_map)
