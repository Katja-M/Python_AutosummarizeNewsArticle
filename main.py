################################################################
# This exercise is based pretty much entirely off this excellent blog post:
# http://glowingpython.blogspot.in/2014/09/text-summarization-with-nl
#############################################################################

# nltk = naltural language processing toolkit which is a python library with support for natural language processing
# We will use these functions from nltk in this drill
#   sent_tokenize: given a group of text tokes, tokenize into sentences
#   word_tokenize: given a group of text tokes, tokenize (split) into words
#   stopwords.words('english'): to find and ignore very common words ('I', 'the', 'a,...)

# Anytime you want to use a resource that NLTK provides such as a set of stopwords,
# you should run nltk. download('Specify the resource you want to download')

import nltk
nltk.download('stopwords')
# The resource punkt is very helpful to tokenize text
nltk.download('punkt')

# Importing functions we need
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# 'defaultdict' This is a class that inherits from dictionary, but has one additional nice feature
# Defaultdict creates a default item and adds that key-value pair to the dictionary instead of throwing a
# KeyError if you try to get an item with a key that is not in the dictionary
# What default item will it use as the value?
# e.g. test = defaultdict(int); The argument , here int, allows as to specify what the default type should be

from collections import defaultdict
# The following built-in Python functionality checks if a symbol is a punctuation symbol
from string import punctuation
# The following built-in Python function will, when given a list, quickly and easily return the n largest elements in that list
from heapq import nlargest

##################################################################################
# First class: FrequencySummarizer
# This class encapsulates the following behavior
#   - eliminating the stop words
#   - finding out the frequency of the words in the text
#   - assigning a score of importance for each of the words in the text
#   - ranking sentences in our text by the score of importance
##################################################################################

class FrequencySummarizer:
    # The first member function is _init() which is the constructor of the FrequencySummarizer class
    # In Python, every time you set up a constructor, you use _init()
    # A constructor is a function that will be called every time an object of this class is instantiated/created
    # The constructor and every member function of a class will take in an argument called 'self'.
    # Self is a keyword that is used to refer to the object being instantiated and its member variables
    # Whenever you want to differentiate a variable as a member variable, we use the keyword 'self'
    def __init__(self, min_cut = 0.1, max_cut = 0.9):
        self._min_cult = min_cut
        self._max_cut = max_cut
        # The notation self._ means that these are member variables of this classs
        # We define as stopwords, words in english and punctuation.
        self._stopwords = set(stopwords.words('english')) + list(punctuation)
    
    # If you define a variable here, i.e. outside a member function but inside a class, that member variable becomes static.
    # The means that it belongs to the class and not to any individual instance (object) of the class

    #The following function will compute the frequency of each word in our piece of text
    def _compute_frequencies(self, word_sent):
        # word_sent is a list of sentences in a piece of text
        # This function will return a dictionary in which the keys are words, and the values are the frequencies of those words.

        # The variable freq will store the dictionary
        freq = defaultdict(int)

        # For loops to count the frequency of each word
        for sentence in word_sent:

            for word in sentence:
                # If statement such that the frequency count is only increased, when the word is not a stop word
                if word not in self._stopwords:
                    freq[word] += 1

        # Two additional steps
        # 1. Normalize the frequencies by dividing each by the highest frequency because it helps to make the frequencies comparable
        # 2. Filter out frequencies that are too high or too low with min_cut and max_cut as it helps to filter out almost stopwords (too high)
        #    and it was empirically found that one yields better results when too low words are also filtered out.
        
        # The variable max_freq will give us the highest frequency
        max_freq = float(max(freq.values()))

        for word in freq.keys():
            #Dividing each frequency by the highest frequency
            freq[word] = freq[word]/max_freq

            if freq[word] >= self._max_cut or freq[word] <= self._min_cut:
                #Delete that key-value pair from the dictionary
                del freq[word]
        
        return freq

    # The following function will assign a score to each sentence in the article based on how frequent the words in that sentence are
    def summarize(self, text, n):
        # Text is the text of the article we want to summarize
        # n is the number of sentences in the summary we wish to return

        # 1. Break up the raw piece of text into sentences
        sents = sent_tokenize(text)

        # Check whether the number of sentences used to summarize is not more than the number of sentences in the text itself
        assert n <= len(sents)
        # 'assert' is a way of making sure a condition holds true, else an exception is thrown. Used to carry out sanity checks
        
        # The following part of the code takes every sentence in the list sents,
        # then it converts every sentence to lower case
        # and then it splits each sentence into words.
        # There is 1 list of words per sentence and these lists are mushed into one giant list.
        word_sent = [word_tokenize(s.lower() for s in sents)]

        # By calling the method _compute_frequencies we get a dictionary with the frequency of all non-stop words back.
        self._freq = self._compute_frequencies(word_sent)

        #Create a rank for each sentences in the text
        rankings = defaultdict(int)

        for i,sent in enumerate(word_sent):
            # Use of the built-in funciton enumerate. When using the enumerate function, you will get a list of tuples
            # [(index of the element A, element A), (index of element B, element B), etc...]
            # Useful because it eliminates the need to have a counter variable to keep track of what index of the list we are currently on
            # However, this also means we need 2 loop variables, i and sent, not only one.

            for word in sent:
                if word in self._freq:
                    # Each time a word in a sentence is in the frequency dictionary, the ranking of that sentences is increase by the frequency of that word
                    rankings[i] += self._freq[word]

        # The variable sents_idx will be the list of sentences we want to use in our summary.
        # That means, the summary is formed by the most important sentences in our article
        # The function nlargest takes in n as number of sentences that it should return, ranking which is the dictionary that it is going to sort
        # and the key as well on which it going to sort it.
        sents_idx = nlargest(n, rankings, key = rankings.get())

    return [sents[j] for j in sents_idx]