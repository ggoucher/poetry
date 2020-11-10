from sources import Sources, poems_from_web
from textngram import Text_NGRAM, poem_strip
import os
import sys

from sklearn.feature_extraction.text import TfidfVectorizer


def tf_idf_poems(poems):
    """intakes a bunch of poems and performs a TF-IDF analysis on them. We take the most interesting poem and read it
    out!"""

    vectorizer = TfidfVectorizer(use_idf=True)  # initiating the model and using IDF

    tf_idf_array = vectorizer.fit_transform(poems).toarray()  # fitting the model

    poem_scores = []
    for entry in tf_idf_array:  # finding the max scores in the model
        poem_scores.append(sum(entry))

    for i in range(len(poem_scores)):  # standardizes our scores across sizes
        poem_scores[i] /= len(poems[i].split())
        print(poem_scores[i])

    return poems[poem_scores.index(max(poem_scores))]  # returns the document with the relative highest tf-idf value


def main():
    poems_from_web("https://poetrydb.org/author/Emily Dickinson/title")

    n_grams = 3  # our default value.
    default_word = "home"
    if len(sys.argv) > 1:
        n_grams = int(sys.argv[1])
        default_word = sys.argv[2]

    dickinson_nltk = Text_NGRAM(Sources.get_source_info(Sources), n_grams, Sources.get_poem_length(Sources))
    synonym = dickinson_nltk.generate_first_term(default_word)

    poems = []
    for i in range(10):
        poem = dickinson_nltk.generate_poem(synonym[0], synonym[1])
        poems.append(poem)

    poem = tf_idf_poems(poems)

    print(poem)

    stripped_poem = poem_strip(poem)

    with open("output.txt", "w") as file:  # only one output at a time, Dickinson rarely named her poems!
        file.write(stripped_poem)

    os.system("say -v Victoria -r 140 -f output.txt")


if __name__ == "__main__":
    main()
