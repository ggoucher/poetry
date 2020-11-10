<h1>DICKINSONGRAM Poetry</h1>
<h3>A project by Gerard Goucher 🧚</h3>

This project uses ngrams, tf-idf metrics, and synset to make interesting poems in the style of 
Emily Dickinson. Dickinson is noted for following a very nature-centric style, and loosely abided
by 8686 meter in her poems. 

<h4>Setting up the code</h4>

My project relies on the requests, os, json, nltk, system, scikit-learn, collection, random, and syllable modules, 
which mostly come pre-packaged with Python distributions, so make sure that you have Python version 3.7
or later installed. 

Run the following commands for this code to run. First, install pip 3 by running this:

    $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    
Then, run this line:

    $ python -m pip install requests
    
to install requests package.

The commands for installing the other packages are as follows:

    $ pip install syllables
    
    $ pip install -U scikit-learn
    
    $ pip install --user -U nltk

Then, simply run the m3.py script using whatever method you prefer, though I used the 
PyCharm IDE. If you wish to run this using the command line, navigate to the poetry
folder in your directory in the command line after downloading from GitHub and run the following command:

    $ python3 main.py <ngram amount (3 recommended)> <starter word>

<h2>Description</h2>

My poetry generation system relies off of Emily Dickinson's poems, beautiful works that focus on nature, and even more
beautifully, aren't copyrighted.

I first used PoetryDB to pull in all of Dickinson's poems, and made a json file for each
to be stored on a local system. After this, the real work begins. The Sources class is used to get all of the words, in
order, used in Dickinson's poems, and also collects the lengths of the poem, too. This will be
useful for later. This information is included because it is useful to emulate Dickinson's style, so using her vocabulary 
is helpful. Additionally, the aesthetic forms Dickinson takes can be emulated too, in her grammatical choices and in 
her usage of the 8686 meter. 

After this is done, our main class takes our sources, the inputted n, and makes an ngram model using
the Text_NGRAM class. This class uses the nltk package to make an ngram model, and I then use a dictionary
to count frequencies of values after n words in Dickinson's poem and vice-versa to make poetry
generation smooth and easy. 

After our ngram model is generated, we take our input input word and check for an exact match in the Dickinson
lexicon, or we seek to find synonym matches in the lexicon. If neither are present, we randomly draw a word from our 
lexicon to start with. The resulting word then has the two terms before it chosen for purposes of our ngram model.

After getting our first two terms, we run a loop of at least 10 generations of poems. Poem generation works by random 
selection of our line counts, and then follows an 8686 pattern of syllables. The ngram dictionary is used to select 
each new term, and the next term is prioritized by it's weight in the ngram dictionary and its appearances as synonyms
for other words in the poem. These two weights allow us to encourage coherence thematically and grammatically. After the 
line count is meant, the poem is returned. This process is repeated ten times.

Using the generated poems, we do a TF-IDF analysis of the poems generated. Then, we sum each poems score and divide by 
their word lengths, and then return the most interesting one. Then the system reads the most interesting poem, and saves
it as a text file.  


<h2>Personal Challenge</h2>

I found this system particularly challenging to implement because I was planning it from beginning to end, and the 
methods, too. This was tough, I initially approached the project by planning to use Recurrent Neural Networks, however
this approach became too difficult for the scope of the project. Instead, I decided to use ngrams to generate this.
Implementing ngrams was a new task for me, and it was challenging to think about how to get an ngram model
to make a poem, so I found the implementation pretty challenging. 

Furthermore, attempting to make poems both interesting and coherent was quite challenging. This is why I decided to 
implement TF-IDF metrics to choose poems that were the most interesting. Implementing the TF-IDF metric was a little 
confusing at first, but I have implemented the metric before, and this application was pretty simple.
 Additionally, I used a synonym check to try to 
make poems that adhered to ngram guidelines but also provided information that would construct a theme of sorts. In the 
end, I think that the poem could have had greater coherence, but I am glad I used mtrics that prioritize creativity
and thematic cohesion.

<h2>Journal Articles</h2>

[Chinese Poetry Generation](https://www.aclweb.org/anthology/D14-1074.pdf) - This article inspired me to use a word to
start generation, and also inspired me to adhere to a stylistic meter.

[Generating Topical Poetry](https://www.aclweb.org/anthology/D16-1126.pdf) - This article inspired me to attempt 
thematic coherence in the poem.

[Deep Learning-based Poetry Generation Given Visual Input](http://www.computationalcreativity.net/iccc2018/sites/default/files/papers/ICCC_2018_paper_59.pdf)
This article inspired me to use a word to start generation, and also encouraged me to better seek grammatical coherence.

<h2>Sources</h2>

Conversed with Sam Roussel and Stephen Crawford about project parameters and ideas. 

[JSON Writing Resource](https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file), used to
determine how to use Python to write JSON objects to a file

[TF-IDF Array Resource](https://stackoverflow.com/questions/53294482/how-to-get-tf-idf-scores-for-the-words/53294731), 
used to determine how to get a TF-IDF vector into an array object.  