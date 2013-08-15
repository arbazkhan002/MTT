'''
Created on Apr 3, 2013

@author: FelixLiu
'''
import config
from nltk import PorterStemmer
from nltk import LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

def normalize(token, pos = None):
    if config.normalize == "LancasterStemmer":
        return LancasterStemmer().stem(token.lower())
    elif config.normalize == "PorterStemmer":
        return PorterStemmer().stem(token.lower())
    elif config.normalize == "Lemmatize":
        if pos is None:
            return WordNetLemmatizer().lemmatize(token.lower())
        else:
            if pos.startswith("V") or pos.startswith('N'):
                return WordNetLemmatizer().lemmatize(token.lower(), pos[0].lower())
            return WordNetLemmatizer().lemmatize(token.lower()) 
    elif config.normalize is None:
        return token
    else:
        raise
    