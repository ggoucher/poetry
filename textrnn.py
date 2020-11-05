import numpy as np
import tensorflow as tf

BATCH_SIZE = 64  # Recommended to be used by StackExchange and TensorFlow
BUFFER_SIZE = 6000  # A little more than the total number of unique words in Dickinson's Poetry
embedding_dim = 256  # why?
rnn_units = 1024  # why?

class Text_RNN:
    """
    A class that contains our methods for our recurrent neural network...

    Methods
    -------

    Attributes
    ----------
    source_words: a huge list of words that we will use to make our RNN

    """
    word_num_map = dict()
    num_word_map = dict()

    def __init__(self, word_list):
        self.word_list = word_list
        self.word_set = set(word_list)

        self.text_string = ""
        for word in word_list:
            self.text_string += word + " "


    def map_words(self):
        """Maps our word set to index terms to make it readily accessible for generation"""
        for num, word in enumerate(self.word_set):
            self.word_num_map[word] = num  # creates effective map for our words
            self.num_word_map[num] = word
        # self.num_word_map = np.array(self.word_set)

        self.word_as_num = np.array([self.word_num_map[w] for w in self.text_string.split()])

    def split_input_target(self, chunk):
        input_text = chunk[:-1]
        target_text = chunk[1:]
        return input_text, target_text

    def create_prediction(self):
        """Utilizes our input dataset to predictively determine next words..."""

        input_len = 10  # maximum amount of words that we want to allow in our input
        examples_epoch = len(self.word_set) // input_len

        word_dataset = tf.data.Dataset.from_tensor_slices(self.word_as_num)

        self.batching(word_dataset, input_len)

    def batching(self, dataset, input_len):
        """batches the database of words we have already to begin to have predictive metrics"""

        for i in dataset.take(5):
            print(self.num_word_map[i.numpy()])

        sequences = dataset.batch(input_len + 1, drop_remainder=True)
        for item in sequences.take(5):
            item_list = item.numpy()
            rep = ""
            for i in item_list:
                rep += " " + self.num_word_map[i]
            print(rep)

        dataset = sequences.map(self.split_input_target)  # takes our input list of words and then target list of words

        for input_example, target_example in dataset.take(1):  # draws what term to pull from in our dataset
            input_list = input_example.numpy()
            input_rep = ""
            for i in input_list:
                input_rep += " " + self.num_word_map[i]
            print('Input data: ', input_rep)

            target_list = target_example.numpy()
            target_rep = ""
            for i in target_list:
                target_rep += " " + self.num_word_map[i]
            print('Target data:', target_rep)

        #todo rewrite

        for i, (input_idx, target_idx) in enumerate(zip(input_example[:5], target_example[:5])):
            print("Step {:4d}".format(i))
            print("  input: {} ({:s})".format(input_idx, repr(self.num_word_map[input_idx.numpy()])))
            print("  expected output: {} ({:s})".format(target_idx, repr(self.num_word_map[target_idx.numpy()])))

        self.training_batches(dataset)


    def training_batches(self, dataset):
        """Takes a dataset input, and batches many different iterations so we can train our RNN"""

        word_data = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)
        print(word_data)

        model = self.construct_model(embedding_dim, BATCH_SIZE, rnn_units)

        for input_example_batch, target_example_batch in dataset.take(64):
            print(input_example_batch)
            # example_batch_predictions = model(input_example_batch)
            # print(example_batch_predictions.shape, "# (batch_size, sequence_length, vocab_size)")

    def construct_model(self, embedding_dim, batch_size, rnn_units):
        """brings our helper functions together and defines the necessary tools to get a model..."""

        word_size = len(self.word_set)

        # NOTE: THE FOLLOWING MODEL IS TAKEN FROM THE TENSOR FLOW WEBSITE
        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(word_size, embedding_dim,
                                      batch_input_shape=[batch_size, None]),
            tf.keras.layers.GRU(rnn_units,
                                return_sequences=True,
                                stateful=True,
                                recurrent_initializer='glorot_uniform'),
            tf.keras.layers.Dense(word_size)
        ])

        return model