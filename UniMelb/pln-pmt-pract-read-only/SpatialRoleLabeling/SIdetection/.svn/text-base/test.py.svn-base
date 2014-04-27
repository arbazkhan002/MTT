import nltk
import xml.dom.minidom
from nltk.tokenize import RegexpTokenizer

# TODO: features extracted from TPP dict (senses)                                                       
prep = 'about'
doc = xml.dom.minidom.parse("tpp.xml")                                                                 

entries = [node for node in doc.getElementsByTagName("hw") if node.firstChild.nodeValue == 'about']
entry = entries[0].parentNode.parentNode.parentNode
senses = []
spatial = 0 #percentage of spatial acceptions
for sup in entry.getElementsByTagName('sup'):
    if sup.firstChild.nodeValue == 'Spatial': spatial += 1
spatial = float(spatial)/len(entry.getElementsByTagName('sup'))
print spatial    

# fins nlp.sup for every S in entry. If not only spatial, feature = multiple.                           

