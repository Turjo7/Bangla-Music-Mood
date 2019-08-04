# -*- coding: utf-8 -*-
"""Bangla Music Mood Model Final_31_July.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LDQV9lCeW5p745WMXE1H6d9ROZhMPTbO
"""

!pip install watermark

# %load_ext watermark

# %watermark -d -v -a 'Sebastian Raschka' -p scikit-learn,nltk,numpy

import pandas as pd

df = pd.read_csv('sample_data/train_lyrics_bangla.txt')

df.head()

from sklearn.preprocessing import LabelEncoder
import pickle
import numpy as np

X_train = df['lyrics'].values 

y_train = df['mood'].values

print('before: %s ...' %y_train[:5])

le = LabelEncoder()
le.fit(y_train)
y_train = le.transform(y_train)

print('after: %s ...' %y_train[:])

# Save object to disk

import pickle

pickle_out = open('./lyrics_label_encoder_py.pkl', 'wb')
pickle.dump(le, pickle_out)
pickle_out.close()

!pip install cltk

from cltk.corpus.utils.importer import CorpusImporter
c = CorpusImporter('bengali')
c.list_corpora

import string
import re
import unicodedata
from cltk.tokenize.sentence import TokenizeSentence



def porter_tokenizer(text):
    """
    A Porter-Stemmer-Tokenizer hybrid to splits sentences into words (tokens) 
    and applies the porter stemming algorithm to each of the obtained token. 
    Tokens that are only consisting of punctuation characters are removed as well.
    Only tokens that consist of more than one letter are being kept.
    
    Parameters
    ----------
        
    text : `str`. 
      A sentence that is to split into words.
        
    Returns
    ----------
    
    no_punct : `str`. 
      A list of tokens after stemming and removing Sentence punctuation patterns.
    
    """
    tokenizer = TokenizeSentence('bengali')
    bengali_text_tokenize = tokenizer.tokenize(text)
    bengali_text_tokenize
    
    
    return bengali_text_tokenize

porter_tokenizer("নীল আকাশের নিচে আমি রাস্তা চলেছি'। একা এই সবুজ। শ্যামল মায়ায় দৃষ্টি পড়েছে ,ঢাকা। শনশন বাতাসের .গুঞ্জণ |হলো চঞ্চল করে ।এই মন আহা…ও ও হো…আহা। হা হা ও হো… ডাক দিয়ে| যায় কার দুটি| চোখ স্বপ্ন কাজল মাখা|")

import unicodedata
map(unicodedata.name, u'কয়া')

# Commented out to prevent overwriting files:
#
# stp = nltk.corpus.stopwords.words('english')
# with open('./stopwords_eng.txt', 'w') as outfile:
#    outfile.write('\n'.join(stp))
    
    
with open('sample_data/stopwords_bangla.txt', 'r') as infile:
   stop_words = infile.read().splitlines()
print('stop words %s ...' %stop_words[:])

# Count Vectorizer

from sklearn.feature_extraction.text import CountVectorizer

vec = CountVectorizer(
            encoding='utf-8',
            decode_error='replace',
            strip_accents='unicode',
            analyzer='word',
            binary=False,
            stop_words=stop_words,
            tokenizer=porter_tokenizer,
            ngram_range=(1,1)
    )

!pip install bangla

vocab = ["ঘুমিয়ে গেছে,ঘুমিয়ে গেছে শ্রান্ত.হয়ে আমার গানের বুলবুলি"]

vec = vec.fit(vocab)

sentence1 = vec.transform(['ঘুমিয়ে গেছ'])
sentence2 = vec.transform(['ঘুমিয়ে'])


print('TEST:')
print('Vocabulary: %s' %vec.get_feature_names())
print('Sentence 1: %s' %sentence1.toarray())
print('Sentence 2: %s' %sentence2.toarray())

from sklearn.feature_extraction.text import CountVectorizer
corpus = ['নতুন ভোর উঠলো সুরে নিলো তোমার ঘুমকে তুলে তখন ','বেদনার বর্ণ বিহীন এ জীবনে যেন আসে এমনি স্বপ্নের দিন সেই ভাবনায় ভাবি মনে ','তুমি ছুয়ে দিলে মন']
vec = CountVectorizer()
x = vec.fit_transform(corpus).toarray()
print(x.shape)
print(vec.get_feature_names())

vec = vec.fit(X_train.ravel())

print('Vocabulary size: %s' %len(vec.get_feature_names()))

corpus = ['নতুন ভোর উঠলো সুরে নিলো তোমার ঘুমকে তুলে তখন ','বেদনার বর্ণ বিহীন এ জীবনে যেন আসে এমনি স্বপ্নের দিন সেই ভাবনায় ভাবি মনে ','তুমি ছুয়ে দিলে মন']
vec = CountVectorizer()
x = vec.fit_transform(corpus).toarray()
print(x.shape)
print(vec.get_feature_names())

sentence1 = vec.transform([u'নতুন ভোর উঠলো সুরে নিলো তোমার ঘুমকে তুলে তখন'])
sentence2 = vec.transform(['বেদনার বর্ণ বিহীন এ জীবনে যেন আসে এমনি স্বপ্নের দিন'])


print('TEST:')
print('Vocabulary: %s' %vec.get_feature_names())
print('Sentence 1: %s' %sentence1.toarray())
print('Sentence 2: %s' %sentence2.toarray())

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(
            encoding='utf-8',
            decode_error='replace',
            strip_accents='unicode',
            analyzer='word',
            binary=False,
            stop_words=stop_words,
            tokenizer=porter_tokenizer
    )

tfidf = vec.fit(X_train.ravel())

print('Vocabulary size: %s' %len(tfidf.get_feature_names()))

from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.pipeline import Pipeline

# Custom scorer methods to account for positive-negative class labels

from sklearn import metrics

# `pos_label` for positive class, since we have sad=1, happy=0

f1_scorer = metrics.make_scorer(metrics.f1_score, greater_is_better=True, pos_label=0)

from sklearn.model_selection import GridSearchCV
from pprint import pprint

pipeline_1 = Pipeline([
    ('vect', CountVectorizer()),
    ('clf', BernoulliNB())
])

parameters_1 = dict(
    vect__binary=[True],
    vect__stop_words=[stop_words, None],
    vect__tokenizer=[porter_tokenizer, None],
    vect__ngram_range=[(1,1), (2,2), (3,3)],
)

grid_search_1 = GridSearchCV(pipeline_1, 
                           parameters_1, 
                           n_jobs=110, 
                           verbose=110,
                           scoring=f1_scorer,
                           cv=2
                )


print("Performing grid search...")
print("pipeline:", [name for name, _ in pipeline_1.steps])
print("parameters:")
pprint(parameters_1, depth=2)
grid_search_1.fit(X_train, y_train)
print("Best score: %0.3f" % grid_search_1.best_score_)
print("Best parameters set:")
best_parameters_1 = grid_search_1.best_estimator_.get_params()
for param_name in sorted(parameters_1.keys()):
    print("\t%s: %r" % (param_name, best_parameters_1[param_name]))

final_clf = Pipeline([
                ('vect', TfidfVectorizer(
                                         binary=False,
                                         stop_words=stop_words,
                                         tokenizer=porter_tokenizer,
                                         ngram_range=(1,1),
                                         )
                ),
                ('clf', MultinomialNB(alpha=1.0)),
               ])
final_clf.fit(X_train, y_train)

!pip install -U statsmodels

import matplotlib as mpl
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
cm = metrics.confusion_matrix(y_train, final_clf.predict(X_train))

np.set_printoptions(suppress=True)
mpl.rc("figure", figsize=(4, 2))

hm = sns.heatmap(cm, 
            cbar=False,
            annot=True, 
            square=True,
            fmt='d',
            yticklabels=['happy','sad'],
            xticklabels=['happy','sad'],
            cmap='Blues'
            )
plt.title('Confusion matrix - Training dataset')
plt.ylabel('actual class')
plt.xlabel('predicted class')
plt.tight_layout()
plt.savefig('sample_data/confmat_training.eps', dpi=300)
plt.show()

df = pd.read_csv('sample_data/train_lyrics_bangla.txt')

X_valid = df['lyrics'].values 
y_valid = df['mood'].values

y_valid = le.transform(y_valid)

cm = metrics.confusion_matrix(y_valid, final_clf.predict(X_valid))

np.set_printoptions(suppress=True)
mpl.rc("figure", figsize=(4, 2))

hm = sns.heatmap(cm, 
            cbar=False,
            annot=True, 
            square=True,
            fmt='d',
            yticklabels=['happy','sad'],
            xticklabels=['happy','sad'],
            cmap='Blues'
            )
plt.title('Confusion matrix - Validation dataset')
plt.ylabel('actual class')
plt.xlabel('predicted class')
plt.tight_layout()
plt.savefig('sample_data/confmat_valid.eps', dpi=300)
plt.show()

# Custom scorer methods to account for positive-negative class labels

from sklearn import metrics

# `pos_label` for positive class, since we have sad=1, happy=0

acc_scorer = metrics.make_scorer(metrics.accuracy_score, greater_is_better=True)
pre_scorer = metrics.make_scorer(metrics.precision_score, greater_is_better=True, pos_label=0)
rec_scorer = metrics.make_scorer(metrics.recall_score, greater_is_better=True, pos_label=0)
f1_scorer = metrics.make_scorer(metrics.f1_score, greater_is_better=True, pos_label=0)
auc_scorer = metrics.make_scorer(metrics.roc_auc_score, greater_is_better=True)

d = {'Data':['Training', 'Validation'],
     'ACC (%)':[],
     'PRE (%)':[],
     'REC (%)':[],
     'F1 (%)':[],
     'ROC AUC (%)':[],
}

d['ACC (%)'].append(acc_scorer(estimator=final_clf, X=X_train, y_true=y_train))
d['PRE (%)'].append(pre_scorer(estimator=final_clf, X=X_train, y_true=y_train))
d['REC (%)'].append(rec_scorer(estimator=final_clf, X=X_train, y_true=y_train))
d['F1 (%)'].append(f1_scorer(estimator=final_clf, X=X_train, y_true=y_train))
d['ROC AUC (%)'].append(auc_scorer(estimator=final_clf, X=X_train, y_true=y_train))

d['ACC (%)'].append(acc_scorer(estimator=final_clf, X=X_valid, y_true=y_valid))
d['PRE (%)'].append(pre_scorer(estimator=final_clf, X=X_valid, y_true=y_valid))
d['REC (%)'].append(rec_scorer(estimator=final_clf, X=X_valid, y_true=y_valid))
d['F1 (%)'].append(f1_scorer(estimator=final_clf, X=X_valid, y_true=y_valid))
d['ROC AUC (%)'].append(auc_scorer(estimator=final_clf, X=X_valid, y_true=y_valid))

df_perform = pd.DataFrame(d)
df_perform = df_perform[['ACC (%)', 'PRE (%)', 'REC (%)', 'F1 (%)', 'ROC AUC (%)']]
df_perform.index=(['Training', 'Validation'])
df_perform = df_perform*100
df_perform = np.round(df_perform, decimals=2)
df_perform

df_perform.to_csv('sample_data/clf_performance.csv', index_label=False)

lyrics_clf_1000 = final_clf

pickle_out = open('sample_data/lyrics_clf_1000_py27_our_own.pkl', 'wb')
pickle.dump(lyrics_clf_1000, pickle_out)
pickle_out.close()