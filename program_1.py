import nltk
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
import pickle


# Objective: Create bigram and unigram dictionaries for English, French, and Italian using the provided training data 
# where the key is the unigram or bigram text and the value is the count of that unigram or bigram in the data. Then for the test data, 
# calculate probabilities for each language and compare against the true labels.

# create a function with a filename as argument
def function(filename):
    # read in the text
    file = open(filename, 'r')
    raw_file_text = file.read()

    # remove new lines
    file_text = raw_file_text.replace('\n', ' ')

    # tokenize the text
    text_tokens = word_tokenize(file_text)

    # use nltk to create a bigrams list
    bigrams = ngrams(text_tokens, 2)

    # use nltk to create a unigrams list
    unigrams = ngrams(text_tokens, 1)

    # use the bigram list to create a bigram dictionary of bigrams and counts
    bigram_dict = {}
    for bigram in set(bigrams):
        if bigram not in bigram_dict:
            bi = bigram[0] + ' ' + bigram[1]
            bigram_dict[bi] = file_text.count(bi)
    
    # use the unigram list to create a unigram dictionary of unigrams and counts
    unigram_dict = {}
    for unigram in set(unigrams):
        unigram_dict[unigram[0]] = file_text.count(unigram[0])

    # return the unigram dictionary and bigram dictionary from the function
    return unigram_dict, bigram_dict


# in the main body of code:

# call the function 3 times for each training file
english_unigram_dict, english_bigram_dict = function("LangId.train.English")
french_unigram_dict, french_bigram_dict = function("LangId.train.French")
italian_unigram_dict, italian_bigram_dict = function("LangId.train.Italian")

# pickle the 6 dictionaries and save to files with appropriate names
with open('english_unigram.pickle', 'wb') as handle:
    pickle.dump(english_unigram_dict, handle)

with open('english_bigram.pickle', 'wb') as handle:
    pickle.dump(english_bigram_dict, handle)

with open('french_unigram.pickle', 'wb') as handle:
    pickle.dump(french_unigram_dict, handle)

with open('french_bigram.pickle', 'wb') as handle:
    pickle.dump(french_bigram_dict, handle)

with open('italian_unigram.pickle', 'wb') as handle:
    pickle.dump(italian_unigram_dict, handle)

with open('italian_bigram.pickle', 'wb') as handle:
    pickle.dump(italian_bigram_dict, handle)
