'''
Created on 24/03/2013

@author: fliu3
'''
import re

def main():
    reg_t = re.compile("^(T\d+)\s+(NE_NP|NP_NP)\s+(\d+)\s+(\d+)\s+(.+)$")
    reg_identifiability = re.compile("^(A\d+)\s+identifiability\s+(T\d+)\s+(no|yes_unamb|yes_amb)$")
    reg_gran_level = re.compile("^(A\d+)\s+gran_level\s+(T\d+)\s+(\d+)$")
    reg_normalised = re.compile("^(A\d+)\s+normalised\s+(T\d+)$")
    reg_notes = re.compile("^(#\d+)\s+AnnotatorNotes\s+(T\d+)\s+(.+)$")
#     reg_t = re.compile("^(T[\d]+)\s+([A-Z_]{5})\s+(.+)$")
    m = reg_t.match("T1    NP_NP 57 77    [NP my_PRP$ desk_NN]")
    print m.groups()
    m = reg_gran_level.match("A88    gran_level T42 4")
    print m.groups()
    m = reg_normalised.match("A79    normalised T40")
    print m.groups()
    m = reg_notes.match("#6    AnnotatorNotes T40    Wonthaggi")
    print m.groups()
    reg_sentence = re.compile("((\[[\w\s$\\.,?!'#:;&-]*\]\s?)| ([\w\\.,?!'#:;&-]+_[A-Z$'.,#:;&-]{1,4}\s?))")
    m = reg_sentence.search(" 6592882940_CD")
    print m.groups()
#     reg_test = re.compile("([\w\\.,?!'#:;&-]+_[A-Z$'.,#:;&-]{1,4}\s?)")
    reg_test = re.compile("\\\\")
    m = reg_test.search("\\_CC")
    print m.groups()

if __name__ == '__main__':
    main()
    