__author__ = 'prnbs'

from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
bigram = []

client = MongoClient()
db = client['yelp']
reviews = db['reviews']
documents = reviews.find({"stars" : 5},{'text' : 1}).limit(200)
for doc in documents:
    text = doc.get('text')
    # smartish word tokenizer, not too reliable
    sentences = sent_detector.tokenize(text.lower().strip())
    stopped_sent = []

    # remove stopwords
    for sentence in sentences:
        words = [word for word in sentence.split() if word not in stopwords.words('english')]
        joint = " ".join(words)
        stopped_sent.append(joint)

    # create bigrams

    for sentence in stopped_sent:
        bigram += nltk.bigrams(sentence.split())

fdist = nltk.FreqDist(bigram)
for k, v in fdist.items():
    print k,v
