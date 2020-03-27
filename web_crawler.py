from collections import Counter
import requests
from bs4 import BeautifulSoup
import pickle
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string


# Neda Khakpour
# CS 4395
# Project 1, Part 1
# Due Date: October 20, 2019

# Build a web crawler to collect information on your chosen topic and store the information in a knowledge bank using
# either Python objects (pickled) or a data base.

# create web crawler function that starts with a url representing a topic and outputs a list of at least 15 relevant urls
def crawler(main_url):
    response = requests.get(main_url)
    data = response.text
    soup = BeautifulSoup(data, "html.parser")
    urls = []
    counter = 0
    print('List of relevant URLs:')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.startswith('https://'):
            print(link.get('href'))
            urls.append(href)
        counter += 1
    return urls


# function to loop through your urls and scrape all text off each page
def scrape_page_text(urls):
    index = 0
    file_names = []
    text = ""
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for b in soup.find_all('p'):
            text += b.getText()
            text = text.replace('\r\n', '')
            text = text.replace('\n', '')
            text = text.replace('\r', '')

        file_name = 'page_%d.pickle' % index
        file_names.append(file_name)
        # store each page’s text in its own file.
        with open(file_name, 'wb') as handle:
            pickle.dump(text, handle)
        index += 1
    return file_names


# function to clean up the text
def clean_up_text(text, index):
    # extract sentences with NLTK’s sentence tokenizer
    file_name = 'cleaned_page_%d.pickle' % index
    sentences = sent_tokenize(text)

    i = 0
    for sentence in sentences:
        sentences[i] = clean(sentence)
        i += 1

    # write the sentences for each file to a new file
    with open(file_name, 'wb') as handle:
        pickle.dump(sentences, handle)


# function to extract at least 10 important terms from the pages using the importance measure term frequency
def build_dictionary(file_names):
    word_dict = {}
    for file_name in file_names:

        with open('cleaned_' + file_name, 'rb') as handle:
            text = pickle.load(handle)

        # create a dictionary of unique terms where the key is the token and the value is the count
        for t in text:
            word_tokens = word_tokenize(t)
            for word in word_tokens:
                if word in word_dict.keys():
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1

    # print the top 25-40 terms
    top_word_count = 0
    print('The top 25 words based on the importance measure of Term Frequency are:')
    c = Counter(word_dict)
    for key in c.most_common():
        if top_word_count < 25:
            print(key)
            top_word_count += 1


# cleans the sentence by removing stop words, punctuation, and making it lower case
def clean(sentence):
    s = remove_stop_words(sentence)
    s = remove_punctuation(s)

    return s


# removes punctuation from the sentence
def remove_punctuation(sentence):
    s = sentence
    for symbol in string.punctuation:
        s = s.replace(symbol, '')

    return s


# removes stop words, and words with one letter from the sentence. returns the sentence in lower case
def remove_stop_words(sentence):
    stop_words = set(stopwords.words('english'))
    s = sentence
    word_tokens = word_tokenize(s)

    for word in word_tokens:
        if word in stop_words:
            s = s.replace(word, '')
        if len(word) == 1:
            s = s.replace(word, '')

    return s.lower()


# main body of code

# url for the Dallas Cowboys Football team
urls = crawler('https://www.dallascowboys.com')
file_names = scrape_page_text(urls)

i = 0
for file_name in file_names:
    with open(file_name, 'rb') as handle:
        text = pickle.load(handle)
    clean_up_text(text, i)
    i += 1

build_dictionary(file_names)
