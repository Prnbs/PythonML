__author__ = 'prnbs'

from pymongo import MongoClient
import itertools
from timeit import default_timer as timer
import pandas as pd


def fetchFromDb (query, collect, projection="", limitTo=0, db='yelp', pandas=False):
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


