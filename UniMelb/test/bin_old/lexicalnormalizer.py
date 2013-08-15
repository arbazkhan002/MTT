'''
Created on Apr 11, 2013

@author: FelixLiu
'''
import re

class LexcialNormalizer:
    
    def __init__(self):
        self.dict = None

    def read_dict(self):
        reg = re.compile("^([^\t\n]+)\t([^\t\n]+)\n$")
        result = {}
        with open("../resources/emnlp_dict.txt") as f:
            for line in f:
                m = reg.match(line)
                if m is not None:
                    result[m.group(1)] = m.group(2)
                else:
                    raise
        return result
    
    def normalize(self, word):
        if self.dict is None:
            self.dict = self.read_dict()
        if word in self.dict:
            return self.dict[word]
        return word