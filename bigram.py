import math
import nltk
import nltk.data
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
import pickle

# Objective: Create bigram and unigram dictionaries for English, French, and Italian using the provided training data 
# where the key is the unigram or bigram text and the value is the count of that unigram or bigram in the data. Then for the test data, 
# calculate probabilities for each language and compare against the true labels.

# function to calculate a probability for each language 
def compute_prob(text, unigram_dict, bigram_dict):
    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))

    N = len(unigram_dict)
    V = len(set(unigram_dict))
    p_gt = 1
    p_laplace = 1

    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        n_gt = bigram_dict[bigram] if bigram in bigram_dict else 1/N
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        if d == 0:
            p_gt = p_gt * (1 / N)
        else:
            p_gt = p_gt * (n_gt / d)
        p_laplace = p_laplace * ((d + 1) / (n + V))
        
    return p_laplace

# read in your pickled dictionaries
with open('english_unigram.pickle', 'rb') as handle:
    english_unigram_dict = pickle.load(handle)

with open('english_bigram.pickle', 'rb') as handle:
    english_bigram_dict = pickle.load(handle)

with open('french_unigram.pickle', 'rb') as handle:
    french_unigram_dict = pickle.load(handle)

with open('french_bigram.pickle', 'rb') as handle:
    french_bigram_dict = pickle.load(handle)

with open('italian_unigram.pickle', 'rb') as handle:
    italian_unigram_dict = pickle.load(handle)

with open('italian_bigram.pickle', 'rb') as handle:
    italian_bigram_dict = pickle.load(handle)

f = open('LangIdResults.txt','w+')
line_count = 1

# for each line in the test file, calculate a probability for each language, and write the language with the highest probability to a file
with open('LangId.test') as file:
    for line in file:
        eng_prob = compute_prob(line, english_unigram_dict, english_bigram_dict)
        fre_prob = compute_prob(line, french_unigram_dict, french_bigram_dict)
        it_prob = compute_prob(line, italian_unigram_dict, italian_bigram_dict)
        if (eng_prob >= fre_prob) and (eng_prob >= it_prob):
            largest = eng_prob
            lang = "English"
        elif (fre_prob >= eng_prob) and (fre_prob >= it_prob):
            largest = fre_prob
            lang = "French"
        else:
            largest = it_prob
            lang = "Italian"
        value = "{} {}\n"
        f.write(value.format(line_count, lang))
        line_count += 1
f.close()

correct_count = 0
total_count = 0
incorrect_lines_list = []

# the file LangId.sol holds the correct classifications
with open('LangId.sol') as sol_file:
    lines = sol_file.readlines()

# compare the results in the LangIdResults file with the LangId.sol correct classifications
with open('LangIdResults.txt') as res_file:
    for res_line in res_file:
        total_count += 1
        if res_line == lines[total_count - 1]:
            correct_count += 1
        else:
            incorrect_lines_list.append(total_count)
        
# compute and output the accuracy as the percentage of correctly classified instances in the test set as well as the line numbers of the incorrectly classified items       
accuracy = (correct_count/total_count) * 100
print("\nThe accuracy as the percentage of correctly classified instances in the test set is: %.2f" % (accuracy) + "%")
if len(incorrect_lines_list) == 0:
    print("There were no incorrectly classified items during processing.")
else:
    print("Incorrectly classified items on:")
    for incorrect_line in incorrect_lines_list:
        print('Line %d' % incorrect_line)


