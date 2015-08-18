__author__ = 'prnbs'

from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords

# client = MongoClient()
# db = client['yelp']
# reviews = db['reviews']
# documents = reviews.find({},{'text' : 1}).limit(20)
# for doc in documents:
#     print(doc.get('text'))


text = ''' No Dr. Sinha 'I want you to die'. No no it is not I.'''

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

print('\n-----\n'.join(sent_detector.tokenize(text.strip())))

# words = [word for word in tokenized_text if word not in stopwords.words('english')]
# bigram = nltk.trigrams(words)
# fdist = nltk.FreqDist(bigram)
# for k, v in fdist.items():
#     print k,v
