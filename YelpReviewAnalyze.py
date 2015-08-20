__author__ = 'prnbs'

from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords
from timeit import default_timer as timer
import pandas as pd
import itertools


def fetchFromDb (query, collect, projection="", limitTo=0,db='yelp', pandas=False):
    client = MongoClient()
    queryAsDict = dict(itertools.izip_longest(*[iter(query)] * 2, fillvalue=""))
    projectionAsDict = dict(itertools.izip_longest(*[iter(projection)] * 2, fillvalue=""))
    database = client[db]
    collection = database[collect]
    start = timer()
    if limitTo == 0:
        documents = collection.find(queryAsDict, projectionAsDict)
    else:
        documents = collection.find(queryAsDict, projectionAsDict).limit(limitTo)
    end = timer()
    print "DB lazy access in " + str(end - start) + "sec"
    if not pandas:
        return documents
    df = pd.DataFrame(documents)
    return df

if __name__ == '__main__':
    query = ["stars", 5]
    projection = ["text", 1]
    documents = fetchFromDb(query, 'reviews', projection, 20)
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    bigram = []
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




