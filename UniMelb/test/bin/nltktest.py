'''
Created on Apr 13, 2013

@author: FelixLiu
'''
import nltk
from nltk.corpus.reader.wordnet import WordNetCorpusReader,\
    WordNetICCorpusReader

def print_simple_path(word):
    paths = word.hypernym_paths()
    ret = []
    for path in paths:
        ret.append(simple_path(path))
    return ret

def simple_path(path):
    return [s.lemmas[0] for s in path]

def find_all_hyponyms(wn, word):
    ret = []
    for hyponym in word.hyponyms():
        ret.append(hyponym)
        ret += find_all_hyponyms(wn, hyponym)
    return ret

def print_hyponyms(hyponyms):
    with open("hyponyms.txt", "w") as f:
        for hyponym in hyponyms:
            f.write(str(hyponym) + "\n")
            for path in print_simple_path(hyponym):
                f.write(str(path) + "\n")
            f.write(str(hyponym.definition) + "\n\n")

def demo():
#    print('loading wordnet')
#    wn = WordNetCorpusReader(nltk.data.find('corpora/wordnet'))
#    print('done loading')
#    S = wn.synset
#    L = wn.lemma
#
#    print('getting a synset for go')
#    move_synset = S('go.v.21')
#    print(move_synset.name, move_synset.pos, move_synset.lexname)
#    print(move_synset.lemma_names)
#    print(move_synset.definition)
#    print(move_synset.examples)
#
#    zap_n = ['zap.n.01']
#    zap_v = ['zap.v.01', 'zap.v.02', 'nuke.v.01', 'microwave.v.01']
#
#    def _get_synsets(synset_strings):
#        return [S(synset) for synset in synset_strings]
#
#    zap_n_synsets = _get_synsets(zap_n)
#    zap_v_synsets = _get_synsets(zap_v)
#    zap_synsets = set(zap_n_synsets + zap_v_synsets)
#
#    print(zap_n_synsets)
#    print(zap_v_synsets)
#
#    print("Navigations:")
#    print(S('travel.v.01').hypernyms())
#    print(S('travel.v.02').hypernyms())
#    print(S('travel.v.03').hypernyms())
#
#    print(L('zap.v.03.nuke').derivationally_related_forms())
#    print(L('zap.v.03.atomize').derivationally_related_forms())
#    print(L('zap.v.03.atomise').derivationally_related_forms())
#    print(L('zap.v.03.zap').derivationally_related_forms())
#
#    print(S('dog.n.01').member_holonyms())
#    print(S('dog.n.01').part_meronyms())
#
#    print(S('breakfast.n.1').hypernyms())
#    print(S('meal.n.1').hyponyms())
#    print(S('Austen.n.1').instance_hypernyms())
#    print(S('composer.n.1').instance_hyponyms())
#
#    print(S('faculty.n.2').member_meronyms())
#    print(S('copilot.n.1').member_holonyms())
#
#    print(S('table.n.2').part_meronyms())
#    print(S('course.n.7').part_holonyms())
#
#    print(S('water.n.1').substance_meronyms())
#    print(S('gin.n.1').substance_holonyms())
#
#    print(L('leader.n.1.leader').antonyms())
#    print(L('increase.v.1.increase').antonyms())
#
#    print(S('snore.v.1').entailments())
#    print(S('heavy.a.1').similar_tos())
#    print(S('light.a.1').attributes())
#    print(S('heavy.a.1').attributes())
#
#    print(L('English.a.1.English').pertainyms())
#
#    print(S('person.n.01').root_hypernyms())
#    print(S('sail.v.01').root_hypernyms())
#    print(S('fall.v.12').root_hypernyms())
#
#    print(S('person.n.01').lowest_common_hypernyms(S('dog.n.01')))
#
#    print(S('dog.n.01').path_similarity(S('cat.n.01')))
#    print(S('dog.n.01').lch_similarity(S('cat.n.01')))
#    print(S('dog.n.01').wup_similarity(S('cat.n.01')))
#
#    wnic = WordNetICCorpusReader(nltk.data.find('corpora/wordnet_ic'),
#                                 '.*\.dat')
#    ic = wnic.ic('ic-brown.dat')
#    print(S('dog.n.01').jcn_similarity(S('cat.n.01'), ic))
#
#    ic = wnic.ic('ic-semcor.dat')
#    print(S('dog.n.01').lin_similarity(S('cat.n.01'), ic))
#
#    print(S('code.n.03').topic_domains())
#    print(S('pukka.a.01').region_domains())
#    print(S('freaky.a.01').usage_domains())

    wn = WordNetCorpusReader(nltk.data.find('corpora/wordnet'))
#    word = wn.synset('street.n.01')
#    
#    print word.lemma_names
#    print word.definition
#    print word.examples
#    print wn.lemma('dog.n.01.dog').synset
#    print word.hypernyms()
#    print word.hyponyms()
#    print word.member_holonyms()
#    print word.member_meronyms()
#    print word.root_hypernyms()
#    print
#    
#    
#    paths = word.hypernym_paths()
#    
#    
#    for path in paths:
#        print simple_path(path)
#        
#    from itertools import islice
#    for synset in islice(wn.all_synsets('n'), 5):
#        print synset, synset.hypernyms()
    
    
    
#    for synset in list(wn.all_synsets('n'))[:10]:
#        print synset
#    
#    print len(list(wn.all_synsets('n')))

#    road = wn.synsets("road", pos = wn.NOUN)
#    road = wn.synset('road.n.01')
#    paths = road.hypernym_paths()
#    
#    for path in paths:
#        print simple_path(path)
#        
#    paths = wn.synset("street.n.01").hypernym_paths()
#    for path in paths:
#        print simple_path(path)

#    print wn.synsets('geographic_area')

    
#    print_hyponyms(find_all_hyponyms(wn, wn.synset('way.n.06')))
    
#    print_hyponyms(find_all_hyponyms(wn, wn.synset('geological_formation.n.01')))
    
    
#    print wn.synsets('am', pos = wn.VERB)
    
#    print_hyponyms(find_all_hyponyms(wn, wn.synset('structure.n.01')))
    
#    syset = wn.synset('geographical_area.n.01').hyponyms()
#    syset = wn.synset('country.n.04').hyponyms()
#    for hyponym in syset:
#        print hyponym
#        print hyponym.definition
#        print
#    print len(syset)
    
#    print wn.synsets("institution", pos = wn.NOUN)

    for synset in wn.synsets('go', pos = wn.VERB):
        paths = synset.hypernym_paths()
        print synset
        print len(paths)
        print synset.definition
        for path in paths:
            print simple_path(path)
        print
    
#    go = wn.synset("mountain.n.01")
#    paths = go.hypernym_paths()
#    print len(paths)
#    for path in paths:
#        print simple_path(path)

#    counter = 0
#    for word in wn.all_synsets('n'):
#        paths = word.hypernym_paths()
#        for path in paths:
#            if 'travel' in simple_path(path):
#                print word
#                counter += 1
#                break
#    print counter

if __name__ == '__main__':
    demo()