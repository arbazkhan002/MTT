'''
Created on Apr 15, 2013

@author: FelixLiu
'''
from nltk.tag.stanford import NERTagger

st = NERTagger('../stanford-ner-2012-11-11/classifiers/english.all.3class.distsim.crf.ser.gz', '../stanford-ner-2012-11-11/stanford-ner.jar')

print "Shields Street , between High Street and Mt. alexander Road".split()
print st.tag("Shields Street , between High Street and Mt. alexander Road".split())