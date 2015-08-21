__author__ = 'prnbs'

import nltk
import PyMLUtils as PyM
from nltk.corpus import stopwords
from timeit import default_timer as timer
import operator
import re


if __name__ == '__main__':
    query = ["stars", 5]
    projection = ["text", 1]
    documents = PyM.fetchFromDb(query, 'reviews', projection, 3000)
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    ngram = []
    starttime = timer()
    pattern=re.compile("[^\w']")
    for doc in documents:
        text = doc.get('text')
        # smartish word tokenizer, not too reliable
        sentences = sent_detector.tokenize(text.lower().strip())
        stopped_sent = []

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
            ngram += nltk.bigrams(sentence.split())
    endtime = timer()

    fdist = nltk.FreqDist(ngram)
    sorted_x = sorted(fdist.items(), key=operator.itemgetter(1))
    for k in sorted_x:
        print " ".join(k[0]) + ":" + str(k[1])

    print "Elapsed time " + str(endtime - starttime)

