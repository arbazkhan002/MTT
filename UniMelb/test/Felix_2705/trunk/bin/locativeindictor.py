'''
Created on Apr 16, 2013

@author: FelixLiu
'''
import nltk
from nltk.corpus.reader.wordnet import WordNetCorpusReader
from chunkeddatareader import ChunkedDataReader
from nltk.stem.wordnet import WordNetLemmatizer
from lexicalnormalizer import LexcialNormalizer

class LocativeIndictor:
    
    def __init__(self, add, sub):
        self.add = add
        self.sub = sub
        self.wn = WordNetCorpusReader(nltk.data.find('corpora/wordnet'))
        self.dic = []
        self.__create_dict__()
        self.lmtzr = WordNetLemmatizer()
        self.ln = LexcialNormalizer()
    
    def __create_dict__(self):
        add_list = []
        with open(self.add, "r") as f:
            for line in f:
                add_list.append(line[:-1])
        sub_list = []
        with open(self.sub, "r") as f:
            for line in f:
                sub_list.append(line[:-1])
        self.dic = []
        for word in add_list:
#            self.dic.append(self.wn.synset(word))
            self.dic += self.find_all_hyponyms(self.wn.synset(word), sub_list)
    
    def find_all_hyponyms(self, word, sub_list):
        ret = []
        for hyponym in word.hyponyms():
            if hyponym.name in sub_list:
                continue
            ret.append(hyponym)
            ret += self.find_all_hyponyms(hyponym, sub_list)
        return ret
    
    def mark_locative_indictor_sentences(self, sentences):
        for sentence in sentences:
            self.mark_locative_indictor(sentence)
    
    def mark_locative_indictor(self, sentence):
        tokens = sentence.get_all_tokens()
        i = 0
        while i < len(tokens):
#            if not tokens[i].pos_tag.startswith("N"):
#                i += 1
#                continue
            for indictor in self.dic:
                indictors = indictor.name.split('.')[0].split('_')
                j = 0
                while j < len(indictors) and j + i < len(tokens) and self.lmtzr.lemmatize(self.ln.normalize(tokens[i + j].token.lower()), 'n') == indictors[j]:
                    j += 1
                    pass
                if j == len(indictors):
                    if j > 1:
                        pass
                    for k in range(i, i + j):
                        tokens[k].is_locative_indictor = True
                    i += j - 1
                    break
            i += 1
                

#li = LocativeIndictor('../resources/add.txt', '../resources/sub.txt')
#sentences = ChunkedDataReader.read_chunked_data("../resources/tuw_chunked_data.txt")
#for sentence in sentences[15:]:
#    li.mark_locative_indictor(sentence)