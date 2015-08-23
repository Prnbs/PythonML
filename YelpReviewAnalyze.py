__author__ = 'prnbs'

import nltk
import PyMLUtils as PyM
from nltk.corpus import stopwords
from timeit import default_timer as timer
import operator
import re
import multiprocessing as mp


def createNGram(doc):
    text = doc.get('text')
    # smartish word tokenizer, not too reliable
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    sentences = sent_detector.tokenize(text.lower().strip())
    stopped_sent = []
    ngram = []
    pattern=re.compile("[^\w']")
    # remove stopwords
    for sentence in sentences:
        # print sentence
        # clear up punctuations
        cleanedSentence = str(pattern.sub(' ', sentence))
        # remove stopwords
        words = [word for word in cleanedSentence.split() if word not in stopwords.words('english')]
        joint = ""
        if len(words) > 0:
            joint = " ".join(words)
        # print joint
        stopped_sent.append(joint)
    # create bigrams
    for sentence in stopped_sent:
        ngram += nltk.trigrams(sentence.split())
    return ngram


def parallel():
    query = ["stars", 5]
    projection = ["text", 1]
    # Params: query, collection name, projection, limit
    documents = PyM.fetchFromDb(query, 'reviews', projection,3000)
    starttime = timer()

    pool = mp.Pool(processes=4)

    results = [pool.apply_async(createNGram, args=(doc,)) for doc in documents]

    output = [p.get() for p in results]

    flat_ngram_list = [item for sublist in output for item in sublist]

    endtime = timer()

    fdist = nltk.FreqDist(flat_ngram_list)
    sorted_x = sorted(fdist.items(), key=operator.itemgetter(1), reverse=True)
    for k in sorted_x[:5]:
        print " ".join(k[0]) + ":" + str(k[1])

    print "Elapsed time " + str(endtime - starttime)

def singleTh():
    query = ["stars", 5]
    projection = ["text", 1]
    # Params: query, collection name, projection, limit
    documents = PyM.fetchFromDb(query, 'reviews', projection,3000)
    starttime = timer()

    gram = []
    for doc in documents:
        gram += createNGram(doc)

    # print type(gram[0])
    endtime = timer()

    fdist = nltk.FreqDist(gram)
    sorted_x = sorted(fdist.items(), key=operator.itemgetter(1), reverse=True)
    for k in sorted_x[:5]:
        print " ".join(k[0]) + ":" + str(k[1])

    print "Elapsed time " + str(endtime - starttime)

if __name__ == '__main__':
    print "Parallel..."
    parallel()
    print "Single..."
    singleTh()
