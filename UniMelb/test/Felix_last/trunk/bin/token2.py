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
        self.is_locative_indictor = False
        self.is_motion_verb = False
        self.timezone = None
        self.isInsideVic = None
        
    def equals(self, token):
        print token.token,self.token,self.pos_tag,token.pos_tag, self.start,token.start,self.end,token.end
        return (self.pos_tag == token.pos_tag) \
            and (self.token == token.token) \
            and (self.start == token.start) \
            and (self.end == token.end)
    
    def __str__(self):
        return str(self.token)
    
    def is_first_letter_capitalized(self):
        return self.token[0].isupper()
