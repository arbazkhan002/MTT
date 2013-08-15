'''
Created on Apr 22, 2013

@author: FelixLiu
'''
import re
from chunkeddatareader import ChunkedDataReader
from annotateddatareader import AnnotatedDataReader
import geonamestagger
import ler
from geonamesreader import GeoNamesReader
from vicnames import VicNamesReader

class UnlockText:
    def __init__(self, token, label):
        self.token = token
        self.label = label

def main():
    sentences = ChunkedDataReader.read_chunked_data("../resources/tuw_chunked_data.txt")
    
    result = AnnotatedDataReader.read_annotated_data("../resources/tuw_chunked_data.ann")
    
    ne_np_count = 0
    for anno in result:
        if anno.tag == "NP_NP":
            ne_np_count += 1
    
    print "ne_np_count: " + str(ne_np_count)
    
    result.sort(key = lambda k : k.start)
    
    geo = geonamestagger.read_geonames()
    
    gnr = GeoNamesReader()
    gnr.read()
    
    vnr = VicNamesReader()
    vnr.read()
    
    output_sentences = ler.match_sentences_annotations(sentences, result, geo, gnr.dict, vnr.dict)
    
    reg_unlock = re.compile("(([\w$\\\\.,?!'#:;&\-/\(\)@\"*$]+|<span class=\"loc\">([\w$\\\\.,?!'#:;&\-/\(\)@\"*$ ])+</span>)[ |\n])")
    
    reg_loc = re.compile("^<span class=\"loc\">([\w$\\\\.,?!'#:;&\-/\(\)@\"*$ ]+)</span>$")
    
    reg_tok = re.compile("([\w$\\\\.,?!'#:;&\-/\(\)@\"*$]+)[ ]?")
    
    counter = 0
    
    unlock_sentences = []
    
    annotations = result
    
    index1 = 0
    
    identified_ne_np_count = 0
    
    identified_np_np_count = 0
    
    with open("result_unlock_temp.txt", "r") as f:
        for idx, line in enumerate(f):
            unlock_sentence = []
            word_count = 0
            line_str = ""
            idx4 = -1
            for idx3, word in enumerate(reg_unlock.finditer(line)):
                m = reg_loc.match(word.group(2))
                if m:
                    for idx2, word2 in enumerate(reg_tok.finditer(m.group(1))):
                        idx4 += 1
                        line_str += word2.group(1)
                        word_count += 1
                        counter += 1
                        if idx2 == 0:
                            if output_sentences[idx][idx4].anno_tag == "NE_NP":
                                identified_ne_np_count += 1
                            elif output_sentences[idx][idx4].anno_tag == "NP_NP":
                                identified_np_np_count += 1
                            
                            if len(unlock_sentence) >= 2 and output_sentences[idx][idx4-1].token.token == "of" and output_sentences[idx][idx4-1].chunk.chunk_tag != "PRT" and unlock_sentence[-2].label != "O":
                                unlock_sentence[-1].label = "I-NP"
                                tok = UnlockText(word2.group(1), "I-NP")
                            elif len(unlock_sentence) >= 2 and output_sentences[idx][idx4-1].token.token == "and" and output_sentences[idx][idx4-1].token.pos_tag == "CC" and unlock_sentence[-2].label != "O":
                                unlock_sentence[-1].label = "I-NP"
                                tok = UnlockText(word2.group(1), "I-NP")
                            elif len(unlock_sentence) >= 1 and output_sentences[idx][idx4-1].chunk.chunk_tag == "PP":
                                unlock_sentence[-1].label = "B-NP"
                                tok = UnlockText(word2.group(1), "I-NP")
                            elif len(unlock_sentence) >= 2 and output_sentences[idx][idx4-1].token.token == "," and output_sentences[idx][idx4-1].token.pos_tag == "," and unlock_sentence[-2].label != "O":
                                unlock_sentence[-1].label = "I-NP"
                                tok = UnlockText(word2.group(1), "I-NP")
                            elif len(unlock_sentence) >= 4 and output_sentences[idx][idx4-3].token.token == "\\" and output_sentences[idx][idx4-2].token.token == "'" and output_sentences[idx][idx4-1].token.token == "s" and unlock_sentence[-2].label != "O":
                                unlock_sentence[-3].label = "I-NP"
                                unlock_sentence[-2].label = "I-NP"
                                unlock_sentence[-1].label = "I-NP"
                                tok = UnlockText(word2.group(1), "I-NP")
                            else:
                                tok = UnlockText(word2.group(1), "B-NP")
                        else:
                            tok = UnlockText(word2.group(1), "I-NP")
                        unlock_sentence.append(tok)
                else:
                    idx4 += 1
                    line_str += word.group(2) + " "
                    word_count += 1
                    counter += 1
                    tok = UnlockText(word.group(2), "O")
                    unlock_sentence.append(tok)
            if word_count != len(sentences[idx].get_all_tokens()):
                print idx
                print line_str
                print str(sentences[idx])
                print
            unlock_sentences.append(unlock_sentence)
    print "identified_ne_np_count: " + str(identified_ne_np_count)
    print "identified_np_np_count: " + str(identified_np_np_count)
    with open("result_unlock.txt", "w") as f:
        for idx, sentence in enumerate(sentences):
            for idx2, token in enumerate(sentence.get_all_tokens()):
                if token.token != unlock_sentences[idx][idx2].token:
                    raise
                output_token = output_sentences[idx][idx2]
                unlock_token = unlock_sentences[idx][idx2]
                print output_token.token.token + " " + unlock_token.token + " " + output_token.label + " " + unlock_token.label
                f.write(output_token.token.token + " " + unlock_token.token + " " + output_token.label + " " + unlock_token.label + "\n")
            print
            f.write("\n")
                
            
    print counter


if __name__ == '__main__':
    main()