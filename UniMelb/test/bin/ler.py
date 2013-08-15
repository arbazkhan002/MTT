'''
Created on 20/03/2013

@author: Fei Liu
'''
import config
#import tokenizer
import wordclass
import urllib2
import geonamestagger
from annotateddatareader import AnnotatedDataReader
from chunkeddatareader import ChunkedDataReader
from lexicalnormalizer import LexcialNormalizer
from geonamesreader import GeoNamesReader
from vicnames import VicNamesReader
from locativeindictor import LocativeIndictor
from locativeindictor2 import LocativeIndictor2
import tokenizer
import math

ln = LexcialNormalizer()

class Output:
    def __init__(self,
                 token = None,
                 chunk = None,
                 label = None,
                 identifiability = None, 
                 gran_level = None, 
                 normalised = False, 
                 vernacular = False,
                 notes = None,
                 anno_total_len = -1,
                 anno_pos = -1,
                 preposition = None,
                 chunk_total_len = -1,
                 token_pos = -1,
                 fcl = None,
                 fcode = None,
                 preposition_chunk = None,
                 first_token = None,
                 first_token_pos = None,
                 sentence_pos = None,
                 chunk_idx = None,
                 second_token = None,
                 second_token_pos = None
                 ):
        self.token = token
        self.chunk = chunk
        self.label = label
        self.identifiability = identifiability
        self.gran_level = gran_level
        self.normalised = normalised
        self.vernacular = vernacular
        self.notes = notes
        self.ex_total_len = anno_total_len
        self.ex_pos = anno_pos
        self.preposition = preposition
        self.chunk_total_len = chunk_total_len
        self.token_pos = token_pos
        self.fcl_geo = fcl
        self.fcode = fcode
        self.preposition_chunk = preposition_chunk
        self.first_token = first_token
        self.first_token_pos = first_token_pos
        self.sentence_pos = sentence_pos
        self.chunk_idx = -1
        self.second_token = second_token
        self.second_token_pos = second_token_pos
        self.most_pos_tag_chunk = None
        self.most_pos_tag_num_chunk = None
        self.chunk_tag_IOB = None
        self.is_case_sensitive = None
        self.fcl_vic = None
        
    def is_all_caps(self):
        return self.token.isupper()
    
    def is_all_lower(self):
        return self.token.islower()
    
    def is_first_letter_cap(self):
        return self.token[0].isupper()
    
    def __append__(self, string, add):
#        if add is None:
#            return string + config.splitter + "None"
        return string + config.splitter + str(add)
        
    def __str__(self):
        if self.token is None and self.pos_tag is None and self.label is None:
            return ""
#        string = self.__append__(tokenizer.normalize(self.token.token), self.token.pos_tag)
        string = self.__append__(self.token.token, self.token.pos_tag)
        string = self.__append__(string, self.identifiability)
        string = self.__append__(string, self.gran_level)
        string = self.__append__(string, self.normalised)
        string = self.__append__(string, self.vernacular)
        string = self.__append__(string, wordclass.get_word_class(self.token.token))
        string = self.__append__(string, wordclass.get_brief_word_class(self.token.token))
        string = self.__append__(string, str(len(self.token.token)))
        string = self.__append__(string, str(self.ex_total_len))
        string = self.__append__(string, str(self.ex_pos))
        string = self.__append__(string, self.chunk.chunk_tag)
        string = self.__append__(string, str(self.preposition))
        string = self.__append__(string, str(len(self.chunk.tokens)))
        string = self.__append__(string, self.token_pos)
        string = self.__append__(string, self.fcl_geo)
        string = self.__append__(string, self.fcode)
        string = self.__append__(string, self.preposition_chunk)
        string = self.__append__(string, self.first_token)
        string = self.__append__(string, self.first_token_pos)
        string = self.__append__(string, self.sentence_pos)
        string = self.__append__(string, self.chunk_idx)
        string = self.__append__(string, self.second_token)
        string = self.__append__(string, self.second_token_pos)
        string = self.__append__(string, self.most_pos_tag_chunk)
        string = self.__append__(string, self.most_pos_tag_num_chunk)
        string = self.__append__(string, ln.normalize(self.token.token))
        string = self.__append__(string, self.chunk_tag_IOB)
        string = self.__append__(string, self.token.token.isupper())
        string = self.__append__(string, self.token.fcl_IOB)
        string = self.__append__(string, self.token.fcode_IOB)
        string = self.__append__(string, self.token.fcl_IOB_vic)
        string = self.__append__(string, self.token.is_locative_indictor)
        string = self.__append__(string, self.token.is_motion_verb)
        string = self.__append__(string, len(self.chunk.tokens))
        string = self.__append__(string, tokenizer.normalize(self.token.token, self.token.pos_tag))
        string = self.__append__(string, self.chunk.get_contains_num())
        string = self.__append__(string, self.chunk.get_first_num_idx())
        string = self.__append__(string, self.token.is_first_letter_capitalized())
        string = self.__append__(string, self.is_case_sensitive)
        string = self.__append__(string, self.fcl_vic)
        
        return self.__append__(string, self.label)

#def output(token, pos_tag, label):
#    pass
##     print "%s\t%s\t%s" % (token, pos_tag, label)

def add_output(tokens, chunks, token_idx, chunk_idx, anno, index, label, output, prep, geo, is_sen_case_sensitive, g, v):
    if anno and anno.tag == "IRREL":
        temp = Output(tokens[token_idx], chunks[chunk_idx], "O")
    else:
        temp = Output(tokens[token_idx], chunks[chunk_idx], label)
    
    if chunks[chunk_idx].chunk_tag is None:
        temp.chunk_tag_IOB = "O"
    elif token_idx == 0:
        temp.chunk_tag_IOB = "B-" + chunks[chunk_idx].chunk_tag
    else:
        temp.chunk_tag_IOB = "I-" + chunks[chunk_idx].chunk_tag
    
    if anno:
        temp.identifiability = anno.identifiability
        temp.gran_level = anno.gran_level
        temp.normalised = anno.normalised
        temp.vernacular = anno.vernacular
        temp.notes = anno.notes
        temp.anno_total_len = len(anno.tokens)
        if geo is not None and anno.tid in geo:
#            temp.fcl = geo[anno.tid]['fcl'] 
            temp.fcode = geo[anno.tid]['fcode']
    temp.fcl_geo = g
    temp.fcl_vic = v
    temp.anno_pos = index
    temp.preposition = prep
#    temp.chunk_total_len = len(chunk.tokens)
    temp.token_pos = token_idx
    
    if chunks[chunk_idx].chunk_tag == "NP":
        if chunks[chunk_idx].tokens[0].token.lower() == "a" or chunks[chunk_idx].tokens[0].token.lower() == "the":
            temp.first_token = chunks[chunk_idx].tokens[0].token
            config.aaa += 1
    
    # pos tag of the first token of a chunk
    temp.first_token_pos = chunks[chunk_idx].tokens[0].pos_tag
    
    # pos tag of the second token of a chunk
    if len(chunks[chunk_idx].tokens) >= 2:
        temp.second_token = chunks[chunk_idx].tokens[1].token
        temp.second_token_pos = chunks[chunk_idx].tokens[1].pos_tag
    
    # calculate the position of a token in a sentence
    sentence_pos = 0
    for i in range(0, chunk_idx):
        sentence_pos += len(chunks[i].tokens)
    sentence_pos += token_idx
    temp.sentence_pos = sentence_pos
    
    # the position of the chunk in a given sentence
    temp.chunk_idx = chunk_idx
    
    # is sentence case sensitive
    temp.is_case_sensitive = is_sen_case_sensitive
    
    # most frequent pos tag in a chunk
    (temp.most_pos_tag_chunk, temp.most_pos_tag_num_chunk) = chunks[chunk_idx].get_most_frequent_pos_tag()
#    temp.most_pos_tag_chunk
    
    if chunk_idx > 0 and chunks[chunk_idx - 1].chunk_tag == "PP" and chunks[chunk_idx].chunk_tag == "NP":
        # prepositional word before a NP chunk
        temp.preposition_chunk = chunks[chunk_idx - 1].tokens[-1].token
#        print chunks[chunk_idx - 1].text + " "  + chunks[chunk_idx].text + " " + label
    
#    elif chunk_idx > 1 \
#        and chunks[chunk_idx - 1].chunk_tag is None \
#        and chunks[chunk_idx - 2].chunk_tag == "NP" \
#        and chunks[chunk_idx - 1].tokens[0].token == "-" \
#        and len(chunks[chunk_idx - 1].tokens) == 1:
#        # for [NP the_DT North_NNP] -_: [NP east_JJ corner_NN]
        
        
    
    output.append(temp)

def word_count(sentences):
    word_counter = 0
    for sentence in sentences:
        for chunk in sentence.chunks:
            word_counter += len(chunk.tokens)
    return word_counter

def in_dict_word_count(sentences):
    ln = LexcialNormalizer()
    ln.dict = ln.read_dict()
    word_count = 0
    for sentence in sentences:
        for chunk in sentence.chunks:
            for token in chunk.tokens:
                if token.token in ln.dict:
                    print token.token + "\t" + ln.dict[token.token]
                    word_count += 1
    return word_count



def match_sentences_annotations(sentences, annotations, geo, geonames, vicnames):
    O = "O"
    B_Loc = "B-NP"
#    B_Loc = "NP"
    I_Loc = "I-NP"
#    I_Loc = "NP"

    
    output_sentence = []
    
    index1 = 0
    index2 = 0
    
    loc_exp_counter = 0
    
    prepositional_loc_count = 0
    non_prepositional_loc_count = 0
    geonames_count = 0
    vicnames_count = 0
    for sentence in sentences:
        output = []
        preposition = None
        for chunk_idx, chunk in enumerate(sentence.chunks):
            for token_idx, token in enumerate(chunk.tokens):
                while token.start > annotations[index1].end:
                    if index2 != len(annotations[index1].tokens):
#                         for t in result[index1].tokens:
#                             print t.token + " ",
#                         print ""
                        print "ORIG:",annotations[index1].original
                        for i in annotations[index1].tokens:
							print i.token
                    index1 += 1
                    index2 = 0
                
#                 if (result[index1].start <= token.start) and (token.end <= result[index1].end):

#                 if index2 >= len(result[index1].tokens):
#                     print sentence.text
#                     pass

                if annotations[index1].tokens[index2].equals(token):
                    g = "O"
                    v = "O"
                    if annotations[index1].get_placename().lower() in geonames:
                        g = geonames[annotations[index1].get_placename().lower()].featureclass
                    if annotations[index1].get_placename().lower() in vicnames:
                        v = vicnames[annotations[index1].get_placename().lower()].featurecode
                    if index2 == 0:
                        if g != "O":
                            g = "B-" + g
                            geonames_count += 1
                        if v != "O":
                            v = "B-" + v
                            vicnames_count += 1
                        # the beginning of an annotation
                        if len(output) >= 2 and output[-1].token.token == "of" and output[-1].chunk.chunk_tag != "PRT" and output[-2].label != O:
#                            if output[-2].label != O:
                            output[-1].label = I_Loc
                            preposition = "of"
                            add_output(chunk.tokens, sentence.chunks, token_idx, chunk_idx, annotations[index1], index2, I_Loc, output, preposition, geo, sentence.is_case_sensitive(), g, v)
#                        elif len(output) >= 2 and output[-1].chunk.chunk_tag == "PRT":
##                            print output[-2].token + " " + output[-1].token
#                            pass
                        elif len(output) >= 2 and output[-1].token.token == "and" and output[-1].token.pos_tag == "CC" and output[-2].label != O:
#                            if output[-2].label != O:
                            output[-1].label = I_Loc
                            preposition = "and"
                            add_output(chunk.tokens, sentence.chunks, token_idx, chunk_idx, annotations[index1], index2, I_Loc, output, preposition, geo, sentence.is_case_sensitive(), g, v)
                        elif len(output) >= 1 and output[-1].chunk.chunk_tag == "PP":
                            output[-1].label = B_Loc
                            if annotations[index1].tag != "IRREL":
                                prepositional_loc_count += 1
                            loc_exp_counter += 1
#                            print output[-1].token.token + " " + token.token
                            preposition = output[-1].token.token
                            add_output(chunk.tokens, sentence.chunks, token_idx, chunk_idx, annotations[index1], index2, I_Loc, output, preposition, geo, sentence.is_case_sensitive(), g, v)
                        elif len(output) >= 2 and output[-1].token.token == "," and output[-1].token.pos_tag == "," and output[-2].label != O:
#                            if output[-2].label != O:
                            output[-1].label = I_Loc
                            preposition = ","
                            add_output(chunk.tokens, sentence.chunks, token_idx, chunk_idx, annotations[index1], index2, I_Loc, output, preposition, geo, sentence.is_case_sensitive(), g, v)
                        elif len(output) >= 4 and output[-3].token.token == "\\" and output[-2].token.token == "'" and output[-1].token.token == "s" and output[-4].label != O:
#                            if output[-4].label != O:
                            output[-3].label = I_Loc
                            output[-2].label = I_Loc
                            output[-1].label = I_Loc
                            preposition = "s"
                            add_output(chunk.tokens, sentence.chunks, token_idx, chunk_idx, annotations[index1], index2, I_Loc, output, preposition, geo, sentence.is_case_sensitive(), g, v)
                        else:
                            add_output(chunk.tokens, sentence.chunks, token_idx, chunk_idx, annotations[index1], index2, B_Loc, output, None, geo, sentence.is_case_sensitive(), g, v)
                            preposition = None
                            loc_exp_counter += 1
                            if annotations[index1].tag != "IRREL":
                                non_prepositional_loc_count += 1
                    else:
                        if g != "O":
                            g = "I-" + g
                        if v != "O":
                            v = "I-" + v
                        # not the start of a locative expression
                        add_output(chunk.tokens, sentence.chunks, token_idx, chunk_idx, annotations[index1], index2, I_Loc, output, preposition, geo, sentence.is_case_sensitive(), g, v)
                    index2 += 1
                    
                else:
                    add_output(chunk.tokens, sentence.chunks, token_idx, chunk_idx, None, None, O, output, None, geo, sentence.is_case_sensitive(), "O", "O")
                    preposition = None
#                    temp = Output(token, chunk, O)
##                    temp.chunk_total_len = len(chunk.tokens)
#                    temp.token_pos = token_idx
#                    output.append(temp)
        output_sentence.append(output)
    print "locative expression counter: " + str(loc_exp_counter)
    print "prepositional_loc_count: " + str(prepositional_loc_count)
    print "non_prepositional_loc_count: " + str(non_prepositional_loc_count)
    print "geonames_count: " + str(geonames_count)
    print "vicnames_count: " + str(vicnames_count)
    return output_sentence

def main():
    
    proxy_support = urllib2.ProxyHandler({"http":"http://fliu3:63421390@wwwproxy.student.unimelb.edu.au:8000"})
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
    
    NUM_FOLD = 10
    
    result = AnnotatedDataReader.read_annotated_data("../resources/tuw_chunked_data.ann")
    
    anno_count = 0
    
    for anno in result:
        if anno.tag == "IRREL":
            continue
        anno_count += 1
    
    print anno_count
    
    result.sort(key = lambda k : k.start)
    
    geo = geonamestagger.read_geonames()
    
    li = LocativeIndictor('../resources/add.txt', '../resources/sub.txt')
    li2 = LocativeIndictor2('../resources/add2.txt', '../resources/sub2.txt')
    
#    unamb = 0
#    np_counter = 0
#    np_unamb = 0
#    for res in result:
#        if res.identifiability == "yes_unamb":
#            unamb += 1
#            if res.original.startswith("NP") or res.original.startswith("[NP"):
#                np_counter += 1
##        if res.original.startswith("NP") or res.original.startswith("[NP"):
##            np_counter += 1
##            if res.identifiability == "yes_unamb":
##                np_unamb += 1
##        print res.tid
##        print res.identifiability
##        print res.original
##        print ""
#    
#    print "%d / %d\t%.2f" % (np_counter, len(result), 100 * np_counter / len(result))
#    print "%d / %d\t%.2f" % (np_unamb, np_counter, 100 * np_unamb / np_counter)
#    print "%d / %d\t%.2f" % (np_counter, unamb, 100 * np_counter / unamb)
    
#    v_notes_num = 0
#    vernacular_num = 0
#    n_notes_num = 0
#    normalised_num= 0
#    identifiability_num = 0
#    for anno in result:
#        if anno.vernacular:
#            if anno.identifiability != "yes_unamb":
#                pass
#            vernacular_num += 1
#            if anno.notes:
#                v_notes_num += 1
#        if anno.normalised:
#            if anno.identifiability != "yes_unamb":
#                pass
#            normalised_num += 1
#            if anno.notes:
#                n_notes_num += 1
#        if anno.identifiability == "yes_unamb":
#            identifiability_num += 1
#            placename = anno.get_placename()
#            print placename
#            if anno.notes:
#                print anno.notes
#            print ""
#    print "v_notes_num = " + str(v_notes_num)
#    print "vernacular_num = " + str(vernacular_num)
#    print "n_notes_num = " + str(n_notes_num)
#    print "normalised_num = " + str(normalised_num)
#    print "identifiability_num = " + str(identifiability_num)
    
    
    sentences = ChunkedDataReader.read_chunked_data("../resources/tuw_chunked_data.txt")
    
    char_counter = 1
    word_counter = 0
    sen_counter = 0
    for sentence in sentences:
        word_counter += len(sentence.get_all_tokens())
        sen_counter += len(sentence.get_sentences())
        char_counter += sentence.get_char_count()
    print "word_counter: " + str(word_counter)
    print "len(sentences): " + str(len(sentences))
    print "mean length: " + str(word_counter / len(sentences))
    print "mean length sen: " + str(sen_counter)
    print "mean characters: " + str(char_counter)
    
    li.mark_locative_indictor_sentences(sentences)
    li2.mark_locative_indictor_sentences(sentences)
    
#    print word_count(sentences)
#    print in_dict_word_count(sentences)
    GeoNamesReader.search_geonames(sentences)
    VicNamesReader.search_vicnames(sentences)
    
    gnr = GeoNamesReader()
    gnr.read()
    
    vnr = VicNamesReader()
    vnr.read()
    
    output_sentence = match_sentences_annotations(sentences, result, geo, gnr.dict, vnr.dict)
    
    loc_exp_count = 0
    loc_exp_word_count = 0
    loc_words = []
    
    for output in output_sentence:
        word_count = 0
        for idx, o in enumerate(output):
            if o.label == "B-NP":
                loc_exp_count += 1
                loc_exp_word_count += 1
                word_count = 1
                if idx + 1 >= len(output) or output[idx + 1].label != "I-NP":
                    loc_words.append(word_count)
                    word_count = 0
            elif o.label == "I-NP":
                loc_exp_word_count += 1
                word_count += 1
                if idx + 1 >= len(output) or output[idx + 1].label != "I-NP":
                    loc_words.append(word_count)
                    word_count = 0
                    
    
    print "loc_exp_count: " + str(loc_exp_count)
    print "loc_exp_word_count: " + str(loc_exp_word_count)
    mean = float(loc_exp_word_count) / float(loc_exp_count)
    print "mean: " +  str(mean)
    c = 0
    m = {}
    for w in loc_words:
        c += (w - mean) ** 2
        if w in m:
            m[w] += 1
        else:
            m[w] = 1
    print "deviation: " + str(math.sqrt(math.sqrt(c) / (loc_exp_count - 1)))
    print "max: " + str(max(loc_words))
    print "min: " + str(min(loc_words))
    print m
    
    
    print config.aaa
    
#    counter_all_caps = 0
#    counter_all_lower = 0
#    
#    for s in sentences:
#        all_caps = True
#        all_lower = True
#        for c in s.chunks:
#            for t in c.tokens:
#                if t.token.isalpha():
#                    if not t.token.isupper():
#                        all_caps = False
#                    if not t.token.islower():
#                        all_lower = False
#        if all_caps:
#            counter_all_caps += 1
#        if all_lower:
##            print s.text
#            counter_all_lower += 1
#        
##    print counter_all_caps
##    print counter_all_lower


#    # count total length of an expression
#    # calculate the index of each token in each expression
#    for s in output_sentence:
#        length = 0
#        for i in range(0, len(s)):
#            if s[i].label == B_Loc:
#                s[i].ex_pos = 0
#                length = 1
#                for j in range(i + 1, len(s)):
#                    if s[j].label != I_Loc:
#                        break
#                    else:
#                        s[j].ex_pos = length
#                        length += 1
#                s[i].ex_total_len = length
#            elif s[i].label == I_Loc:
#                s[i].ex_total_len = length
#            else:
#                s[i].ex_pos = -1
#                s[i].ex_total_len = 0
#                length = 0
                        
    
    sentence_num = len(output_sentence)
    
    slice_num = sentence_num / NUM_FOLD + 1
    
    with open("./train", "w") as f:
        for sen in output_sentence:
            for o in sen:
                f.write(str(o) + "\n")
            f.write("\n")
    
    with open("./test", "w") as f:
        for sen in output_sentence:
            for o in sen:
                f.write(str(o) + "\n")
            f.write("\n")
    
    for i in range(0, NUM_FOLD):
        
        with open("./train" + str(i), "w") as f:
            for j in range(0, slice_num * i):
                # sentences before the slice
                for o in output_sentence[j]:
                    f.write(str(o) + "\n")
                f.write("\n")
            for j in range(slice_num * (i + 1), sentence_num):
                # sentences after the slice
                for o in output_sentence[j]:
                    f.write(str(o) + "\n")
                f.write("\n")
        with open("./test" + str(i), "w") as f:
            for j in range(slice_num * i, min(slice_num * (i + 1), sentence_num)):
                # sentences in the slice
                for o in output_sentence[j]:
                    f.write(str(o) + "\n")
                f.write("\n")

if __name__ == "__main__":
    main()
