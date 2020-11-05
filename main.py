from sources import Sources, poems_from_web
from textrnn import Text_RNN
from textngram import Text_NGRAM



def main():

    poems_from_web("https://poetrydb.org/author/Emily Dickinson/title")

    # dickinson_rnn = Text_RNN(Sources.get_source_info(Sources))
    # dickinson_rnn.map_words()
    # dickinson_rnn.create_prediction()

    dickinson_nltk = Text_NGRAM(Sources.get_source_info(Sources), 3)



if __name__ == "__main__":
    main()
