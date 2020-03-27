# Web Crawler Project
**Project Objective:** Build a web crawler to collect information on your chosen topic and store the information in a knowledge bank using either Python objects (pickled) or a data base. 

**Details**
1. Web crawler and search techniques. 
        
    - Build  a web crawler function that starts with a url representing a topic (a sport, your favorite film, a celebrity, a political issue, etc.) and outputs a list of at least 15 relevant urls. The urls can be pages within the original domain but should have a few outside the original domain.  

    - Write a function to loop through your urls and scrape all text off each page. Store each page’s text in its own file. 

    - Write a function to clean up the text. Extract sentences with NLTK’s sentence tokenizer. Write the sentences for each file to a new file. That is, if you have 15 files in, you have 15 files out. 

    - Write a function to extract at least 10 important terms from the pages using an importance measure such as term frequency or tf-idf. First, you might want to lower-case everything, remove stopwords and punctuation. Then build a vocabulary of unique terms. Create a dictionary of unique terms where the key is the token and the value is the count or tf-idf across all documents.  Print the top 25-40 terms.

    - Manually determine the top 10 terms based on your domain knowledge or interests. 

    - Build a searchable knowledge bank of facts share related to the 10 terms. 


Deliverables timeline:
- October 20: Upload web crawler and search code. 
- October 21, 23: Present an overview of your code and results, as well as your knowledge bank and discuss your initial thoughts on how you envision a chatbot using this information.