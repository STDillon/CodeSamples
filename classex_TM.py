import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import PlaintextCorpusReader
from nltk import *
import re
import wordcloud
import matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy

file0 = nltk.corpus.gutenberg.fileids( ) [0]
emmatext = nltk.corpus.gutenberg.raw(file0)

lemmatizer = WordNetLemmatizer()
emmatokens = nltk.word_tokenize(emmatext)
emmawords = [w.lower( ) for w in emmatokens]

# Creating a frequency distribution of words
ndist = FreqDist(emmawords)
stopwords = nltk.corpus.stopwords.words('english')

def alpha_filter(w):
  # pattern to match word of non-alphabetical characters
  pattern = re.compile('^[^a-z]+$')
  if (pattern.match(w)):
    return True
  else:
    return False

# apply the function to emmawords
alphaemmawords = [w for w in emmawords if not alpha_filter(w)]
stopwords = nltk.corpus.stopwords.words('english')

#finaldf = ' '.join([lemmatizer.lemmatize(w) for w in stoppeddf])

stoppedemmawords = [w for w in alphaemmawords if not w in stopwords]
finaldf = ' '.join([lemmatizer.lemmatize(w) for w in stoppedemmawords])
emmadist = FreqDist(stoppedemmawords)
emmaitems = emmadist.most_common(100)
emmahist = emmadist.most_common(100)
for item in emmaitems:
  print(item)

#h = numpy.histogram(word_items)
h2 = plt.hist(emmahist, bins = 1, density = True)
plt.show(h2)

wordcloud = WordCloud().generate(finaldf)
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
