'''
Created on Apr 14, 2013

@author: FelixLiu
'''
#import ner
import time
import geonamestagger
from chunkeddatareader import ChunkedDataReader
from annotateddatareader import AnnotatedDataReader
from nltk.tag.stanford import NERTagger
from geonamesreader import GeoNamesReader
from vicnames import VicNamesReader
import ler

def ner_to_str(result):
    ret = ""
    for token, _ in result:
        ret += token + " "
    return ret[:-1]

def main():
    sentences = ChunkedDataReader.read_chunked_data("../resources/tuw_chunked_data.txt")
    
    result = AnnotatedDataReader.read_annotated_data("../resources/tuw_chunked_data.ann")
    
    result.sort(key = lambda k : k.start)
    
    geo = geonamestagger.read_geonames()
    
    st = NERTagger('../stanford-ner-2012-11-11/classifiers/english.all.3class.distsim.crf.ser.gz', '../stanford-ner-2012-11-11/stanford-ner.jar')
    
#    print st.tag("I am at a 3 stories town house , number 7 Chetwynd Place ! The house is located in a small alley behind a row of town house along Chetwynd Street , near the corner between Chetwynd Street and Queensberry Street . There is a construction site in the alley . Its the 3 rd house from the head of the alley .".split())
    
    counter = 0
    
    gnr = GeoNamesReader()
    gnr.read()
    
    vnr = VicNamesReader()
    vnr.read()
    
    output_sentences = ler.match_sentences_annotations(sentences, result, geo, gnr.dict, vnr.dict)
    
#    sentences = sentences[148:]
#    output_sentences = output_sentences[148:]
    
    with open("stanford.log", "w") as f:
        f.write("")
    
    with open("result_stanford.txt", "w") as f:
        for sentence in sentences:
            if str(sentence) != "":
                result = []
                for s in sentence.get_sentences():
                    result += st.tag(s)
                result_IOB = []
                i = 0
                while i < len(result):
                    (token, tag) = result[i]
                    if tag == "LOCATION":
                        if len(result_IOB) >= 1:
                            (pre_token, pre_tag) = result_IOB[-1]
                        if len(result_IOB) >= 2:
                            (prepre_token, prepre_tag) = result_IOB[-2]
                        all_tokens = sentence.get_all_tokens()
                        if len(result_IOB) >= 2 and pre_token == "of" and all_tokens[i-1].chunk_tag != "PRT" and prepre_tag != "O":
                            result_IOB[-1] = (pre_token, "I-NP")
                            result_IOB.append((token, "I-NP"))
                        elif len(result_IOB) >= 2 and pre_token == "and" and all_tokens[i-1].pos_tag == "CC" and prepre_tag != "O":
                            result_IOB[-1] = (pre_token, "I-NP")
                            result_IOB.append((token, "I-NP"))
                        elif len(result_IOB) >= 1 and all_tokens[i-1].chunk_tag == "PP":
                            result_IOB[-1] = ((pre_token, "B-NP"))
                            result_IOB.append((token, "I-NP"))
                        elif len(result_IOB) >= 2 and pre_token == "," and all_tokens[i-1].pos_tag == "," and prepre_tag != "O":
                            result_IOB[-1] = ((pre_token, "I-NP"))
                            result_IOB.append((token, "I-NP"))
                        else:
                            result_IOB.append((token, "B-NP"))
                            
                        j = i + 1
                        while j < len(result):
                            (next_token, next_tag) = result[j]
                            if next_tag != tag:
#                                i = j - 1
                                break
                            result_IOB.append((next_token, "I-NP"))
                            i = j
                            j += 1
    #                    tag = "B-" + tag
                    else:
                        result_IOB.append((token, "O"))
                    i += 1
                    
                if len(result_IOB) != len(output_sentences[counter]):
                    with open("stanford.log", "a") as l:
                        l.write("Original:\n" )
                        l.write(str(sentence) + "\n")
                        l.write("StanfordNER:\n")
                        l.write(ner_to_str(result_IOB) + "\n")
                        l.write("\n")
                
                for idx, output_token in enumerate(output_sentences[counter]):
                    if idx < len(result_IOB):
                        (token, tag) = result_IOB[idx]
                        print output_token.token.token + " " + token + " " + output_token.label + " " + tag
                        f.write(output_token.token.token + " " + token + " " + output_token.label + " " + tag + "\n")
                    else:
                        print output_token.token.token + " " + "" + " " + output_token.label + " " + "O"
                        f.write(output_token.token.token + " " + "" + " " + output_token.label + " " + "O" + "\n")
                f.write("\n")
                
#                for idx, (token, tag) in enumerate(result_IOB):
#                    if token != output_sentences[counter][idx].token.token:
#                        print "########################################"
#                        print token + "\t" + output_sentences[counter][idx].token.token
#                        print "########################################"
#                        print
#                        time.sleep(20)
#                    try:
#                        print output_sentences[counter][idx].token.token + " " + output_sentences[counter][idx].label + " " + tag
#                    except:
#                        pass
#                    f.write(output_sentences[counter][idx].token.token + " " + output_sentences[counter][idx].label + " " + tag + "\n")
#                f.write("\n")
            counter += 1
            print ("%d / %d") % (counter, len(sentences))
            print

if __name__ == '__main__':
    main()
