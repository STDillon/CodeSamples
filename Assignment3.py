import re
import pickle
import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC
from nltk.corpus import sentence_polarity
import random

data = PlaintextCorpusReader('.', '.*\.txt')
#split into a bunch of different files and change it each time
data_raw = data.raw('health_and_personal_care.txt')

stopwords = nltk.corpus.stopwords.words('english')

removegarbage = r'(?<=reviewText:)(.*?)(?=\s*overall:\d+)'

useful_data = re.findall(removegarbage, data_raw)
useful_data = ' '.join(useful_data)

sents = nltk.sent_tokenize(useful_data)

words = []
for sent in sents:
    tokens = nltk.word_tokenize(sent)
    lowercase = [w.lower() for w in tokens]
    nostopwords = [w for w in lowercase if not w in stopwords]
    words.append(nostopwords)

# tried to format this by breaking the line at punctuation, but adding
# a period made it break in spots I didnt want it to
for a in words:
    for b, c in enumerate(a):
        if a == '?' or a == '!':
            a[b] = '\n'
#change the length each time and add the files together
amazon1 = words
amazon = amazon1
documents = [(sent, cat) for cat in sentence_polarity.categories()
	for sent in sentence_polarity.sents(categories=cat)]

random.shuffle(documents)

all_words_list = [word for (sent,cat) in documents for word in sent]
all_words = nltk.FreqDist(all_words_list)
word_items = all_words.most_common(3000)
word_features = [word for (word,count) in word_items]

def document_features(document, word_features):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features

featuresets = [(document_features(d, word_features), c) for (d, c) in documents]

train_set1, test_set1 = featuresets[1000:], featuresets[:1000]

# way that bo found to do the classifier without training taking an eternity each time
# load saved classifier1 from pickle after the first time
#classifier1 = nltk.NaiveBayesClassifier.train(train_set1)
classifier1_f = open('classifier1.pickle', 'rb')
classifier1 = pickle.load(classifier1_f)
classifier1_f.close()

print('BOW Accuracy:', nltk.classify.accuracy(classifier1, test_set1))

def data_features(data, word_features):
    data_words = set(data)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in data_words)
    return features

testing_set = [data_features(d, word_features) for d in amazon]

cat1 = classifier1.classify_many(testing_set)

pos_f1 = open('BOW-pos3.txt', 'w')
neg_f1 = open('BOW-neg3.txt', 'w')

for (sent, cat) in zip(amazon, cat1):
    if cat == 'pos':
        pos_f1.write(' '.join(sent))
    elif cat == 'neg':
        neg_f1.write(' '.join(sent))
pos_f1.close()
neg_f1.close()

# save classifier1 as pickle file
# TODO: comment out after running
save_classifier1 = open('classifier1.pickle','wb')
pickle.dump(classifier1, save_classifier1)
save_classifier1.close()

def readSubjectivity(path):
    flexicon = open(path, 'r')
    sldict = { }
    for line in flexicon:
        fields = line.split()
        # split each field via "="
        strength = fields[0].split("=")[1]
        word = fields[2].split("=")[1]
        posTag = fields[3].split("=")[1]
        stemmed = fields[4].split("=")[1]
        polarity = fields[5].split("=")[1]
        if (stemmed == 'y'):
            isStemmed = True
        else:
            isStemmed = False
        sldict[word] = [strength, posTag, isStemmed, polarity]
    return sldict

SLpath = 'subjclueslen1-HLTEMNLP05.tff'

SL = readSubjectivity(SLpath)

def SL_features(document, word_features, SL):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)

    weakPos = 0
    strongPos = 0
    weakNeg = 0
    strongNeg = 0
    for word in document_words:
        if word in SL:
            strength, posTag, isStemmed, polarity = SL[word]
            if strength == 'weaksubj' and polarity == 'positive':
                weakPos += 1
            if strength == 'strongsubj' and polarity == 'positive':
                strongPos += 1
            if strength == 'weaksubj' and polarity == 'negative':
                weakNeg += 1
            if strength == 'strongsubj' and polarity == 'negative':
                strongNeg += 1
            features['positivecount'] = weakPos + (2 * strongPos)
            features['negativecount'] = weakNeg + (2 * strongNeg)
    return features

SL_featuresets = [(SL_features(d, word_features, SL), c) for (d, c) in documents]

train_set2, test_set2 = SL_featuresets[1000:], SL_featuresets[:1000]

#classifier2 = nltk.NaiveBayesClassifier.train(train_set2)

classifier2_f = open('classifier2.pickle', 'rb')
classifier2 = pickle.load(classifier2_f)
classifier2_f.close()

print('Subjectivity Accuracy:',nltk.classify.accuracy(classifier2, test_set2))

cat2 = classifier2.classify_many(testing_set)

pos_f2 = open('Subjectivity-pos3.txt', 'w')
neg_f2 = open('Subjectivity-neg3.txt', 'w')

for (sent, cat) in zip(amazon, cat2):
    if cat == 'pos':
        pos_f2.write(' '.join(sent))
    elif cat == 'neg':
        neg_f2.write(' '.join(sent))
pos_f2.close()
neg_f2.close()


save_classifier2 = open('classifier2.pickle','wb')
pickle.dump(classifier2, save_classifier2)
save_classifier2.close()


negationwords = ['no', 'not', 'never', 'none', 'nowhere', 'nothing', 'noone', 'rather',
                 'hardly', 'scarcely', 'rarely', 'seldom', 'neither', 'nor', 'isn\'t', 'wasn\'t', 'can\'t', 'wont']

def NOT_features(document, word_features, negationwords):
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = False
        features['contains(NOT{})'.format(word)] = False

    for i in range(0, len(document)):
        word = document[i]
        if ((i + 1) < len(document)) and ((word in negationwords) or (word.endswith("n't"))):
            i += 1
            features['contains(NOT{})'.format(document[i])] = (document[i] in word_features)
        else:
            features['contains({})'.format(word)] = (word in word_features)
    return features

NOT_featuresets = [(NOT_features(d, word_features, negationwords), c) for (d, c) in documents]

train_set3, test_set3 = NOT_featuresets[1000:], NOT_featuresets[:1000]

#classifier3 = nltk.NaiveBayesClassifier.train(train_set3)


classifier3_f = open('classifier3.pickle', 'rb')
classifier3 = pickle.load(classifier3_f)
classifier3_f.close()

print('Negation Accuracy:',nltk.classify.accuracy(classifier3, test_set3))

cat3 = classifier3.classify_many(testing_set)

pos_f3 = open('Negation-pos3.txt', 'w')
neg_f3 = open('Negation-neg3.txt', 'w')

for (sent, cat) in zip(amazon, cat1):
    if cat == 'pos':
        pos_f3.write(' '.join(sent))
    elif cat == 'neg':
        neg_f3.write(' '.join(sent))
pos_f3.close()
neg_f3.close()


save_classifier3 = open('classifier3.pickle','wb')
pickle.dump(classifier3, save_classifier3)
save_classifier3.close()

#EXTRA CREDIT SECTION
#used sklearn
train_set4, test_set4 = train_set3, test_set3

#classifier4 = SklearnClassifier(BernoulliNB()).train(train_set4)


classifier4_f = open('classifier4.pickle', 'rb')
classifier4 = pickle.load(classifier4_f)
classifier4_f.close()

print('SKlearn Accuracy:', nltk.classify.accuracy(classifier4, test_set4))

cat4 = classifier4.classify_many(testing_set)

pos_f4 = open('SK-pos3.txt', 'w')
neg_f4 = open('SK-neg3.txt', 'w')

for (sent, cat) in zip(amazon, cat4):
    if cat == 'pos':
        pos_f4.write(' '.join(sent))
    elif cat == 'neg':
        neg_f4.write(' '.join(sent))
pos_f4.close()
neg_f4.close()

save_classifier4 = open('classifier4.pickle','wb')
pickle.dump(classifier4, save_classifier4)
save_classifier4.close()
