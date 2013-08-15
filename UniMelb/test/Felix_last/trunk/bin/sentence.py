'''
Created on Apr 14, 2013

@author: FelixLiu
'''
class Sentence:
    def __init__(self,
                 chunks = [],
                 start = None,
                 end = None,
                 text = None):
        self.chunks = chunks
        self.start = start
        self.end = end
        self.text = text
        self.case_sensitive = None
        
    def is_case_sensitive(self):
        if self.case_sensitive is not None:
            return self.case_sensitive
        for token in self.get_all_tokens():
            if token.is_first_letter_capitalized():
                self.case_sensitive = True
                return self.case_sensitive
        self.case_sensitive = False
        return self.case_sensitive
    
    def __str__(self):
        string = ""
        for chunk in self.chunks:
            string += str(chunk) + " "
        return string[:-1]
    
    def get_all_tokens(self):
        ret = []
        for chunk in self.chunks:
            for token in chunk.tokens:
                token.chunk_tag = chunk.chunk_tag
                ret.append(token)
        return ret
    
    def get_token_str(self):
        ret = []
        for chunk in self.chunks:
            for token in chunk.get_token_str():
                ret.append(token)
        return ret
    
    def get_char_count(self):
        char_count = 0
        for chunk in self.chunks:
            for token in chunk.get_token_str():
                char_count += (len(token) + 1)
        return char_count - 1
    
    def get_sentences(self):
        sentences = []
        sentence = []
        is_added = False
        for chunk in self.chunks:
            for token in chunk.get_token_str():
                sentence.append(token)
                is_added = False
                if not token.isalpha() and not token.isdigit():
                    sentences.append(sentence)
                    sentence = []
                    is_added = True
        if not is_added:
            sentences.append(sentence)
        return sentences