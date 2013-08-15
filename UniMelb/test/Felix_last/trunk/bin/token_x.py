'''
Created on Apr 14, 2013

@author: FelixLiu
'''

class Token:
    def __init__(self, 
                 pos = None, 
                 tok = None,
                 start = None,
                 end = None):
        self.pos_tag = pos
        self.token = tok
        self.start = start
        self.end = end
        self.fcl_IOB = None
        self.fcode_IOB = None
        self.fcl_IOB_vic = None
        
    def equals(self, token):
        return (self.pos_tag == token.pos_tag) \
            and (self.token == token.token) \
            and (self.start == token.start) \
            and (self.end == token.end)
