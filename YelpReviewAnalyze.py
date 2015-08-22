__author__ = 'prnbs'

import nltk
import PyMLUtils as PyM
from nltk.corpus import stopwords
from timeit import default_timer as timer
import operator
import re


def createNGram(doc):
    text = doc.get('text')
    # smartish word tokenizer, not too reliable
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
        if len(words) > 0:
            joint = " ".join(words)
        # print joint
        stopped_sent.append(joint)
    # create bigrams
    for sentence in stopped_sent:
        ngram += nltk.trigrams(sentence.split())
    return ngram


if __name__ == '__main__':
    query = ["stars", 1]
    projection = ["text", 1]
    documents = PyM.fetchFromDb(query, 'reviews', projection, 24)
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    starttime = timer()
    ngram = []
    for doc in documents:
        ngram.append(createNGram(doc))
    flat_ngram_list = [item for sublist in ngram for item in sublist]

    endtime = timer()

    fdist = nltk.FreqDist(flat_ngram_list)
    sorted_x = sorted(fdist.items(), key=operator.itemgetter(1))
    for k in sorted_x:
        print " ".join(k[0]) + ":" + str(k[1])

    print "Elapsed time " + str(endtime - starttime)

