#!/usr/bin/env jython
import sys
sys.path.append("/Users/Alberto/LLAVERO/Software/stanford-parser-2008-10-26/stanford-parser.jar")  
from subprocess import call
from java.io import CharArrayReader
from edu.stanford.nlp import *

from pprint import pprint
import cPickle

lp = parser.lexparser.LexicalizedParser("/Users/Alberto/LLAVERO/Software/stanford-parser-2008-10-26/englishPCFG.ser.gz")
tlp = trees.PennTreebankLanguagePack()
lp.setOptionFlags(["-maxLength", "80", "-retainTmpSubcategories", "-outputFormat", "wordsAndTags,penn,typedDependencies"])
 
wordlist = cPickle.load(open('save.p', 'rb')) 
if (lp.parse(wordlist)):
    parse = lp.getBestParse()
 
gsf = tlp.grammaticalStructureFactory()
gs = gsf.newGrammaticalStructure(parse)
tdl = gs.typedDependenciesCollapsed() #typedDependencyList

#pprint(parse)
pprint(tdl)

list = []
# extract RlDep from preps
print "\n***DepRl\n"
for td in tdl:
    if td.reln().getShortName() == 'prep':
        print "***"
        rel = td.reln().getSpecific()
        gov = td.gov().label().toString('value')
        dep = td.dep().label().toString('value')
        list.append([rel, gov, dep])

# write output to file
f1 = open('tree.p', 'w')
f1.write(parse.toString())
f1.close()

#write prep rels
cPickle.dump(list, open('postag.p', 'wb'))
