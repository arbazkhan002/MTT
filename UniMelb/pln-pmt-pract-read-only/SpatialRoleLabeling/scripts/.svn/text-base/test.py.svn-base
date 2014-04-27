import nltk
import xml.dom.minidom
from nltk.tokenize import RegexpTokenizer

#read xml file
doc = xml.dom.minidom.parse("sprl_semeval3_trial0.xml")
contents = doc.getElementsByTagName("CONTENT")

#TOKENIZE
sentence = contents[0].childNodes[0].data

tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
#tokenizer = RegexpTokenizer('[a-zA-Z]+')
words = tokenizer.tokenize(sentence)
print sentence
print words

#POS TAGGER
tagged = nltk.pos_tag(words)
print tagged

pos_tags = [pos for (token,pos) in tagged]

#PARSE
simple_grammar = nltk.parse_cfg("""
  S -> NP VP
  PP -> P NP
  NP -> Det N | Det N PP
  VP -> V NP | VP PP
  Det -> 'DT'
  N -> 'NN'
  V -> 'VBZ'
  P -> 'PP'
  """)
parser = nltk.ChartParser(simple_grammar)
tree = parser.parse(pos_tags)
