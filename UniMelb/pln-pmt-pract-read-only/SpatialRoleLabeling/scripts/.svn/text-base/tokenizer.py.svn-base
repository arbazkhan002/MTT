import nltk.data
from nltk.tokenize import PunktWordTokenizer
from nltk.tokenize import PunktSentenceTokenizer
from nltk.tokenize import TreebankWordTokenizer

import xml.dom.minidom
from xml.dom.minidom import Node

doc = xml.dom.minidom.parse("sprl_semeval3_trial0.xml")

tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
#tokenizer = PunktWordTokenizer()
#tokenizer = PunktSentenceTokenizer()
tokenizer = TreebankWordTokenizer()

fileHandle = open ( 'test.txt', 'w' ) 
i = 1

for node in doc.getElementsByTagName("SENTENCE"):
  L = node.getElementsByTagName("CONTENT")
  for node2 in L:
    for node3 in node2.childNodes:
      if node3.nodeType == Node.TEXT_NODE:
		fileHandle.write('## SENTENCE ' + str(i) + ' ##\n')
		for line in tokenizer.tokenize(node3.data):
			fileHandle.write(line.replace(' ','\n'))
			fileHandle.write('\n')
		fileHandle.write('\n')
		i+=1
fileHandle.close() 