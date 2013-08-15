'''
Created on Apr 14, 2013

@author: FelixLiu
'''
class Chunk:
    def __init__(self,
                 start = None,
                 end = None,
                 chunk_tag = None,
                 tokens = None,
                 text = None):
        self.start = start
        self.end = end
        self.chunk_tag = chunk_tag
        self.tokens = tokens
        self.text = text
        self.most_pos_tag = None
        self.most_pos_tag_num = 0
        self.contains_num = None
        self.first_num_idx = None
    
    def get_contains_num(self):
        if self.contains_num is not None:
            return self.contains_num
        self.__check_token_is_digit__()
        return self.contains_num
    
    def get_first_num_idx(self):
        if self.first_num_idx is not None:
            return self.first_num_idx
        self.__check_token_is_digit__()
        return self.first_num_idx
    
    def __check_token_is_digit__(self):
        for idx, token in enumerate(self.tokens):
            if token.token.isdigit():
                self.contains_num = True
                self.first_num_idx = idx
                return
        self.contains_num = False
        self.first_num_idx = -1
        
        
    def get_placenames(self):
        ret = ""
        for t in self.tokens:
            ret += t.token + " "
        return ret[0:-1]
    
    def get_most_frequent_pos_tag(self):
        if self.most_pos_tag is not None and self.most_pos_tag_num is not None:
            return (self.most_pos_tag, self.most_pos_tag_num)
        temp = {}
        for token in self.tokens:
            if token.pos_tag in temp:
                temp[token.pos_tag] += 1
            else:
                temp[token.pos_tag] = 1
        self.most_pos_tag = None
        self.most_pos_tag_num = 0
        for (pos, num) in temp.items():
            if num > self.most_pos_tag_num:
                self.most_pos_tag = pos
                self.most_pos_tag_num = num
        return (self.most_pos_tag, self.most_pos_tag_num)
    
    def __str__(self):
        string = ""
        for token in self.tokens:
            string += str(token) + " "
        return string[:-1]
    
    def get_token_str(self):
        ret = []
        for token in self.tokens:
            ret.append(token.token)
        return ret