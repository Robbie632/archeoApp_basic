import numpy as np 
import pandas as pd 

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation
from keras.layers import Bidirectional, GlobalMaxPool1D
from keras.models import Model
from keras.models import Sequential
from keras.optimizers import SGD
from keras import initializers, regularizers, constraints, optimizers, layers




#function removes punctuation from a sentence

def remove_punctuation(sentence):
    
    from string import punctuation
    
    for punct in punctuation:
        sentence = sentence.replace(punct, '')

    return(sentence)


#function removes stop words from a sentence
def removeStopWords(sentence):
    from nltk.corpus import stopwords
    import nltk
    
    return(' '.join(word for word in sentence.split() if word not in stopwords.words()))
    

#function stems words according to Porter stemmer rules
def stemWords(sentence):
    
    from nltk.stem import PorterStemmer 
    ps = PorterStemmer() 
    
    return(' '.join(ps.stem(word) for word in sentence.split()))
        



