'''
Created on Apr 14, 2013

@author: FelixLiu
'''
import re
from token2 import Token
from chunk import Chunk
from sentence import Sentence

class ChunkedDataReader:
    @staticmethod
    def read_chunked_data(file_name):
        reg_sentence = re.compile("((\[[\w\s$\\\\.,?!'#:;&\-/\(\)@\"*$]*\] ?)|\s?([\w\\\\.,?!'#:;&\-/\(\)@\"*$]+_[A-Z$'.,#:;&\-/\(\)$^\n]{1,5} ?))")
        reg_chunk = re.compile("\[([A-Z]{2,5}) ([\w\s$\\\\.,?!'#:;&\-/\(\)@\"*$]*)\]")
        reg_other = re.compile("([\w\\\\.,?!'#:;&\-/\(\)@\"*$]+)_([A-Z$'.,#:;&\-/\(\)$]{1,5}) ?")
        reg_token = re.compile("(([\w\\\\.,?!'#:;&\-/\(\)@\"*$]+)_([A-Z$'.,#:;&\-/\(\)$]{1,5}) ?)")
        line_len = 0
        sentences = []
        with open(file_name) as f:
            for line in f:
                chunk_len = 0
                chunks = []
                first = True
                test = False
                for chunk in reg_sentence.finditer(line):
                    
                    trimmed = chunk.group(0)
                     
                    if first:
                        first = False
                        if trimmed[0:1] == " ":
                            test = True
                         
                    m = reg_chunk.match(trimmed)
                    if test:
                        start = line_len + chunk_len
                        end = line_len + chunk_len + len(trimmed)
                    else:
                        start = line_len + chunk_len + 1
                        end = line_len + chunk_len + len(trimmed) + 1
                    chunk_str = trimmed
                    chunk_tag = None
                    tokens = None
                    if m is not None:
                        chunk_tag = m.group(1)
                        tokens = []
                        rest = m.group(2)
                        token_start = len(chunk_tag) + 1 + 1
                        for token in reg_token.finditer(rest):
                            tokens.append(Token(token.group(3), token.group(2), start + token_start + token.start(), start + token_start + token.start() + len(token.group(0).strip())))
                    else:
                        tokens = []
                        for token in reg_other.finditer(trimmed):
                            tokens.append(Token(token.group(2), token.group(1), start + token.start(), start + token.start() + len(token.group(0).strip())))
                     
                    chunks.append(Chunk(start, end, chunk_tag, tokens, chunk_str))
                    chunk_len += len(chunk.group(0))
                
                sentences.append(Sentence(chunks, line_len, line_len + len(line), line))
                line_len += len(line)
        return sentences
