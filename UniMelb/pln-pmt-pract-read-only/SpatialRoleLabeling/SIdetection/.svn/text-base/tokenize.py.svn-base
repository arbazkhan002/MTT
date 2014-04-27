import nltk
import xml.dom.minidom
from nltk.tokenize import RegexpTokenizer
import cPickle
from subprocess import call
from pprint import pprint

def tokenize_dataset():
    # Read xml file                                                                        
    doc = xml.dom.minidom.parse("sprl_semeval3_trial0.xml")
    contents = doc.getElementsByTagName("CONTENT")

    for content in contents:
        sentence = content.childNodes[0].data
        print "\n***Original sentence:\n", sentence    
        words = tokenize(sentence)
        content.childNodes[0].data = ' '.join(words)

    f = open('tokenized.xml', 'w')
    doc.writexml(f)
    f.close()

def tokenize(string):
    
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
    #tokenizer = RegexpTokenizer('[a-zA-Z]+')       #palabras
    words = tokenizer.tokenize(string)
    for w in words:
        if "'t" is w:
            w = "not"
    return words

if __name__ == '__main__':
    tokenize_dataset()
