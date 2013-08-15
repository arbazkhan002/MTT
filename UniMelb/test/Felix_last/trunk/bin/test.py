'''
Created on 24/03/2013

@author: fliu3
'''
import re
from chunkeddatareader import ChunkedDataReader

def main():
#    reg_t = re.compile("^(T\d+)\s+(NE_NP|NP_NP)\s+(\d+)\s+(\d+)\s+(.+)$")
#    reg_identifiability = re.compile("^(A\d+)\s+identifiability\s+(T\d+)\s+(no|yes_unamb|yes_amb)$")
#    reg_gran_level = re.compile("^(A\d+)\s+gran_level\s+(T\d+)\s+(\d+)$")
#    reg_normalised = re.compile("^(A\d+)\s+normalised\s+(T\d+)$")
#    reg_notes = re.compile("^(#\d+)\s+AnnotatorNotes\s+(T\d+)\s+(.+)$")
##     reg_t = re.compile("^(T[\d]+)\s+([A-Z_]{5})\s+(.+)$")
#    m = reg_t.match("T1    NP_NP 57 77    [NP my_PRP$ desk_NN]")
#    print m.groups()
#    m = reg_gran_level.match("A88    gran_level T42 4")
#    print m.groups()
#    m = reg_normalised.match("A79    normalised T40")
#    print m.groups()
#    m = reg_notes.match("#6    AnnotatorNotes T40    Wonthaggi")
#    print m.groups()
#    reg_sentence = re.compile("((\[[\w\s$\\.,?!'#:;&-]*\]\s?)| ([\w\\.,?!'#:;&-]+_[A-Z$'.,#:;&-]{1,4}\s?))")
#    m = reg_sentence.search(" 6592882940_CD")
#    print m.groups()
##     reg_test = re.compile("([\w\\.,?!'#:;&-]+_[A-Z$'.,#:;&-]{1,4}\s?)")
#    reg_test = re.compile("\\\\")
#    m = reg_test.search("\\_CC")
#    print m.groups()
    string = "I am at a 3 stories town house , number 7 <span class=\"loc\">Chetwynd</span> Place . The house is located in a small alley behind a row of town house along <span class=\"loc\">Chetwynd</span> Street , near the corner between <span class=\"loc\">Chetwynd Street</span> and <span class=\"loc\">Queensberry Street</span> . There is a construction site in the alley . Its the 3 rd house from the head of the alley .\n"
#    reg_unlock = re.compile("^(([\w\d\"=<>/])[ |\n])+$")
    reg_unlock = re.compile("(([\w$\\\\.,?!'#:;&\-/\(\)@\"*$]+|<span class=\"loc\">([\w$\\\\.,?!'#:;&\-/\(\)@\"*$ ])+</span>)[ |\n])")
#    for word in reg_unlock.finditer(string):
#        print word.group(2)
    counter = 0
    sentences = ChunkedDataReader.read_chunked_data("../resources/tuw_chunked_data.txt")
    with open("result_unlock.txt", "r") as f:
        for idx, line in enumerate(f):
            word_count = 0
            line_str = ""
            for word in reg_unlock.finditer(line):
                line_str += word.group(2) + " "
                word_count += 1
                counter += 1
            if word_count != len(sentences[idx].get_all_tokens()):
                print idx
                print line_str
                print str(sentences[idx])
                print
            
    print counter   

if __name__ == '__main__':
    main()
    