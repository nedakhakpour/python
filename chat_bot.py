import pickle
import nltk
from os import path
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# Neda Khakpour
# CS 4395
# Chat Bot Project
# Due Date: December 1, 2019

# Create a chatbot using Python and NLP techniques. The chatbot should be able to carry on a limited conversation in a
# particular domain using a knowledge base scraped from the web and knowledge it learns from the user.

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)

GREETING_RESPONSES = ["Hi", "Hey", "Howdy", "Hello", "Hiya"]

THANKFUL_RESPONSES = ["No problem", "You bet", "Not a problem", "You're welcome", "You are welcome", "Sure thing",
                      "For sure"]

SUPERBOWL_RESPONSES = [
    "Well, we currently have 5 Superbowl victories. The last one being during the 1996 season...but hopefully we get 6 this year! *robo fingers crossed*",
    "The Dallas Cowboys have won the Superbowl 5 times, with victories over the Dolphins, Broncos, Bill (twice), and Steelers.",
    "8 tries, 5 wins...1972, 1978, 1993, 1994, and 1996...ahhh do I miss the 90's....",
]

TICKET_RESPONSES = [
    "Although I don't know the exact pricing...the games are typically expensive. That's what happens when you're the most popular football in the world!",
    "Not too sure...but you can find them at any ticket retailer online. Preferably ticketmaster.com, our sponsor ;)",
]

STADIUM_RESPONSES = [
    "We play at THE AT&T Stadium in Arlington, TX. Have you been?",
    "We play at 1 AT&T Way, Arlington, TX 76011, aka AT&T Stadium. It's a nice looking place.",
    "Well, the Cowboys play at AT&T Stadium, don't really care about any other teams...",
]

NO_RESPONSES = [
    "Yeah...I'm not sure about that one...",
    "My guess is as good as yours on that one...",
    "I have no idea.",
    "I'm  afraid I do not know..."
]


# checks if user's input is a greeting, return a greeting response
def check_for_greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# handle some weird edge cases in parsing, like 'i' needing to be capitalized to be correctly identified as a pronoun
def preprocess_text(sentence):
    cleaned = []
    words = sentence.split(' ')
    for w in words:
        if w == 'i':
            w = 'I'
        if w == "i'm":
            w = "I'm"
        cleaned.append(w)

    return ' '.join(cleaned)


# parse the user's inbound sentence and find candidate terms that make up a best-fit response
def respond(sentence):
    cleaned = preprocess_text(sentence)

    resp = check_for_greeting(cleaned)

    if "superbowl" in cleaned:
        return random.choice(SUPERBOWL_RESPONSES)
    if "superbowls" in cleaned:
        return random.choice(SUPERBOWL_RESPONSES)
    if "where" in cleaned:
        return random.choice(STADIUM_RESPONSES)
    if "stadium" in cleaned:
        return random.choice(STADIUM_RESPONSES)
    if "price" in cleaned:
        return random.choice(TICKET_RESPONSES)
    if "tickets" in cleaned:
        return random.choice(TICKET_RESPONSES)
    if "ticket" in cleaned:
        return random.choice(TICKET_RESPONSES)

    if not resp:
        return random.choice(NO_RESPONSES)

    return resp


# function to extract at least 10 important terms from the pages using the importance measure term frequency
def build_dictionary(file_name):
    word_dict = {}
    keys = []

    with open(file_name, 'rb') as handle:
        text = pickle.load(handle)

    # create a dictionary of unique terms where the key is the token and the value is the count
    word_tokens = word_tokenize(text)
    for word in word_tokens:
        if word in word_dict.keys():
            word_dict[word] += 1
        else:
            word_dict[word] = 1


    top_word_count = 0
    for key in word_dict.keys():
        if top_word_count < 4:
            keys.append(key)

    return keys


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


# save the new or updated user model file
def save_user_model(user_name, words):
    file_name = '%s_user_model.pickle' % user_name
    with open(file_name, 'wb') as handle:
        pickle.dump(words, handle)


# check if the user model file exists
def user_model_exists(user_name):
    return path.exists('%s_user_model.pickle' % user_name)


# main body of code

user_words = ""
flag = True
has_name = False
print('Dallas Cowboys Bot: ' + random.choice(
    GREETING_RESPONSES) + '! My name is Dallas Cowboys Bot. I can help answer any questions you have about the '
                          'Dallas Cowboys Football Club. Before we start, what shall I call you?')
name_response = input('User: ')

# make sure user types a name. if no name is entered, continue until name is entered.
while not has_name:
    if name_response == '' or name_response is None:
        print(
            'Dallas Cowboys Bot: Sorry, couldn\'t catch that. Please type your name so we can continue! Or say \'bye\' to sadly end our conversation.')
        name_response = input()
    else:
        if user_model_exists(name_response):
            file_name = '%s_user_model.pickle' % name_response
            keys = build_dictionary(file_name)
            user_model_dict = ''
            if len(keys) != 0:
                user_model_dict = 'Last time we chatted about ' + keys[0] + ', ' + keys[1] + ', and ' + keys[2] + '.'
            print(
                'Dallas Cowboys Bot: Nice to chat with you again, ' + name_response + '. ' + user_model_dict + ' How can I help you this time?')
            has_name = True
        else:
            print('Dallas Cowboys Bot: Awesome! Nice to meet you, ' + name_response + '. How can I help you?')
            has_name = True

# while dialogue is there and user has not left
while flag:
    user_response = input(name_response + ': ')
    user_response = user_response.lower()
    if user_response != 'bye':
        cleaned_response = clean(user_response)
        word_tokens = nltk.word_tokenize(cleaned_response)
        for word in word_tokens:
            user_words += word
            user_words += '\n'

        if user_response == 'thanks' or user_response == 'thank you':
            print('Dallas Cowboys Bot: ' + random.choice(THANKFUL_RESPONSES) + '!')
        else:
            if check_for_greeting(user_response) is not None:
                print("Dallas Cowboys Bot: " + check_for_greeting(user_response))
            else:
                print(respond(user_response))
    else:
        flag = False
        print("Dallas Cowboys Bot: Bye! Go Cowboys!")

save_user_model(name_response, user_words)
