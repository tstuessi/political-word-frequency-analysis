# utility functions and imports
from bs4 import BeautifulSoup
from collections import Counter
import requests
import re
import nltk
import operator

# I found myself writing this a lot.
def soupify_url(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')

# removes special characters from words
def clean_words(word_list):
    return [re.sub(r'[,".\'&|:]', "", w).lower() for w in word_list]

# Graphing function to make pretty graphs with matplotlib
import numpy as np
import pylab
import matplotlib.pyplot as plt

%matplotlib inline
def plotTwoLists (wf_ee, wf_bu, title):
    f = plt.figure (figsize=(10, 6))
    # this is painfully tedious....
    f .suptitle (title, fontsize=20)
    ax = f.add_subplot(111)
    ax .spines ['top'] .set_color ('none')
    ax .spines ['bottom'] .set_color ('none')
    ax .spines ['left'] .set_color ('none')
    ax .spines ['right'] .set_color ('none')
    ax .tick_params (labelcolor='w', top='off', bottom='off', left='off', right='off', labelsize=20)

    # Create two subplots, this is the first one
    ax1 = f .add_subplot (121)
    plt .subplots_adjust (wspace=.5)

    pos = np .arange (len(wf_ee)+1) 
    ax1 .tick_params (axis='both', which='major', labelsize=14)
    pylab .yticks (pos, [ x [0] for x in wf_ee ])
    ax1 .barh (range(len(wf_ee)), [ x [1] for x in wf_ee ], align='center')

    ax2 = f .add_subplot (122)
    ax2 .tick_params (axis='both', which='major', labelsize=14)
    pos = np .arange (len(wf_bu)+1) 
    pylab .yticks (pos, [ x [0] for x in wf_bu ])
    ax2 .barh (range (len(wf_bu)), [ x [1] for x in wf_bu ], align='center')

# collecting Hillary's data
# Aggregating the issues was a pain on Hillary's website due to some javascript stuff,
# so I just hard coded it.
from bs4 import BeautifulSoup
import requests
import re

# base issues page
h_base_url = 'https://www.hillaryclinton.com/issues/'

#Hillary issues
h_issues_list = ['a-fair-tax-system',
                 'addiction',
                 'an-economy-that-works-for-everyone',
                 'alzheimers-disease',
                 'autism',
                 'campaign-finance-reform',
                 'campus-sexual-assault',
                 'climate',
                 'combating-terrorism',
                 'criminal-justice-reform',
                 'disability-rights',
                 'early-childhood-education',
                 'fixing-americas-infrastructure',
                 'gun-violence-prevention',
                 'health-care',
                 'fighting-hiv-and-aids',
                 'immigration-reform',
                 'jobs',
                 'k-12-education',
                 'labor',
                 'lgbt-equality',
                 'college',
                 'manufacturing',
                 'mental-health',
                 'military-and-defense',
                 'national-security',
                 'paid-leave',
                 'protecting-animals-and-wildlife',
                 'racial-justice',
                 'rural-communities',
                 'small-business',
                 'social-security-and-medicare',
                 'technology-and-innovation',
                 'veterans',
                 'voting-rights',
                 'wall-street',
                 'womens-rights-and-opportunity',
                 'workforce-and-skills',
              ]

h_corpus = ''
# build the corpus of text data for Hillary
for ext in h_issues_list:
    soup = soupify_url(h_base_url+ext)
    
    # based on the structure of the web page,
    # this returns all the text in the description
    # of the issue.
    h_corpus += soup.find_all('article')[1].get_text()
    
# Trump's issues were a bit easier
d_base_url = 'https://www.donaldjtrump.com/positions'

# collect the urls for the expanded positions page
soup = soupify_url(d_base_url)

# note that d_issues_list is a list of urls whereas h_issues_list is a list of extensions
# again, this scraping comes from the format of the website
d_issues_list = [a['href'] for a in soup.find_all('a', 'issue_item')]

# collect the corpus from donald's website
d_corpus = ''
for d_url in d_issues_list:
    soup = soupify_url(d_url)
    
    #this again comes from the structure of the web page
    d_corpus += soup.find('article').get_text()

# create list of stop words that don't really matter
stop_words = nltk.corpus.stopwords.words('english')

# some words that I thought didn't add any value
stop_words.append('–')

# write a function to return the word counts
def calc_wf(corpus):
    stop_words = nltk.corpus.stopwords.words('english')
    stop_words.append('–')
    # create the word list
    word_list = clean_words(re.split('\s+', corpus))
    
    # counter counts the number of each element in the list
    # and puts it together into a nice list of tuples
    word_frequency = Counter(word_list)
    
    for w in stop_words:
        word_frequency.pop(w, None)
    
    return sorted(word_frequency.items(), key=operator.itemgetter(1))

h_word_frequency = calc_wf(h_corpus)
d_word_frequency = calc_wf(d_corpus)

num_to_compare = 15
# get the last num_to_compare items, as they will be the highest
plotTwoLists(h_word_frequency[len(h_word_frequency)-num_to_compare:], 
             d_word_frequency[len(d_word_frequency)-num_to_compare:], 
             "Comparing Hillary and Trump's Issue Pages")

# as an added measure and because I was curious, compute the average number of name mentions per page
print("Number of \"hillary\" mentions per page on her website: " + str(dict(h_word_frequency)["hillary"] / float(len(h_issues_list))))
print("Number of \"trump\" mentions per page on his website: " + str(dict(d_word_frequency)["trump"] / float(len(d_issues_list))))
