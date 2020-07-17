import tensorflow as tf

import pandas as pd
import re

import string
import matplotlib.pyplot as plt

import spacy
nlp = spacy.load('en_core_web_sm')
import nltk
nltk.download('words')
nltk.download('brown')
from nltk.corpus import brown
words = set(brown.words())
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('wordnet')

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

from main import transform_file
import pickle

def clean_text(text):
    text = re.sub(r'\b[a-zA-Z]\b', '', text)
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('|', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('[^\x00-\x7F\x80-\xFF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF]', '', text)
    return text

def remove_entity(text):
    words = set(brown.words())
    doc = nlp(text)
    remove = [ "".join(ent.text) for ent in doc.ents if ent.label_ in ('GPE','DATE','NORP') ] 
    #print(remove)
    for word in remove:
        token = word
        text = str(text).lower()
        text = " ".join(w for w in nltk.wordpunct_tokenize(text) if w.lower() in words or not w.isalpha())
        #print(text)
        return text

def remove_stopword(text):
    words = [word for word in text if word not in stopwords.words('english')]
    words = ' '.join(list_of_text)
    return words

def prepare_file(df):
    realtest = transform_file(df)
    realtest=realtest.iloc[:,0]
    pred = realtest.apply(lambda x: clean_text(x))
    pred = pred.apply(lambda x: remove_entity(x))
    tokenizer = nltk.tokenize.WhitespaceTokenizer()
    pred = pred.apply(lambda x: tokenizer.tokenize(x))
    pred = pred.apply(lambda x: remove_stopword(x))
    pred = pred.apply(lambda x: combine_text(x))
    stemmer = nltk.stem.PorterStemmer()
    lemmatizer=nltk.stem.WordNetLemmatizer()
    pred = pred.apply(lambda x: lemmatizer.lemmatize(x))
    count_vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
    pred_vectors = count_vectorizer.transform(pred)

    bst = pickle.load(open("pima.pickle.dat", "rb"))
    predictions = bst.predict(pred_vectors)	

    value = int(predictions[0])
    if value == 0:
        classified = 'Administration'
    elif value == 1:
        classified = 'Sales'
    elif value == 2:
        classified = 'Investment'
    elif value == 3:
        classified = 'Accounting-Finance'
    elif value == 4:
        classified = 'Legal'
    print(classified)
    return classified
