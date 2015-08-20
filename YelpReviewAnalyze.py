__author__ = 'prnbs'

import nltk
from timeit import default_timer as timer
import PyMLUtils as PyM
from sklearn.feature_extraction.text import CountVectorizer




if __name__ == '__main__':
    query = ["stars", 5]
    projection = ["text", 1]
    documents = PyM.fetchFromDb(query, 'reviews', projection, 15500)
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    ngram = []
    vect = CountVectorizer(ngram_range=(1, 3), stop_words='english')
    start = timer()
    for doc in documents:
        matrix = vect.fit(doc['text'].split('\n'))
        ngram += matrix.get_feature_names()
    end = timer()
    print "Total elapsed " + str(end - start)
    # freqs = [(word, ngram.getcol(idx).sum()) for word, idx in vect.vocabulary]
    # for phrase ,times in sorted (freqs, key = lambda x : -x[1])[:25]:
    #     print phrase, times


