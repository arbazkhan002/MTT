'''
Created on Apr 14, 2013

@author: FelixLiu
'''
import operator

class Annotation:
    def __init__(self, 
                 tid = None, 
                 tag = None, 
                 start = None, 
                 end = None, 
                 original = None,
                 tokens = [], 
                 identifiability = None, 
                 gran_level = None, 
                 normalised = False, 
                 vernacular = False,
                 notes = None):
        self.tid = tid
        self.tag = tag
        self.start = start
        self.end = end
        self.original = original
        self.tokens = tokens
        self.identifiability = identifiability
        self.gran_level = gran_level
        self.normalised = normalised
        self.vernacular = vernacular
        self.notes = notes
        self.filled = 0
        self.filled_str = ""
    
    def is_all_nnps(self):
        for t in self.tokens:
            if t.pos_tag != "NNP":
                return False
        return True
    def get_most_freq_pos(self):
        pos = {}
        for t in self.tokens:
            if t.pos_tag in pos:
                pos[t.pos_tag] += 1
            else:
                pos[t.pos_tag] = 1
        sorted_pos = sorted(pos.iteritems(), key = operator.itemgetter(1))
        return sorted_pos[-1]
    
    def get_placename(self):
        ret = ""
        for t in self.tokens:
            ret += t.token + " "
        return ret[0:-1]
        
    def fill(self, fill):
        self.filled_str += fill
        self.filled += len(fill)
        
    def is_filled(self):
        return len(self.filled_str.strip()) == self.end - self.start