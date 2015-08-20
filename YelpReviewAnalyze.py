__author__ = 'prnbs'

from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords
from timeit import default_timer as timer
import pandas as pd
import itertools
from sklearn.feature_extraction.text import CountVectorizer


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
    vect = CountVectorizer(ngram_range=(1,3), stop_words='english')
    for doc in documents:
        matrix = vect.fit(doc['text'].split('\n'))
        print matrix.get_feature_names()




