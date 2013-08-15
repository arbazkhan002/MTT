'''
Created on Apr 14, 2013

@author: FelixLiu
'''
import re
from token2 import Token
from annotation import Annotation

class AnnotatedDataReader:
    reg_t = re.compile("^(T\d+)\s+(NE_NP|NP_NP|IRREL)\s+(\d+)\s+(\d+)\s+(.+)$")
    reg_identifiability = re.compile("^(A\d+)\s+identifiability\s+(T\d+)\s+(no|yes_unamb|yes_amb)$")
    reg_gran_level = re.compile("^(A\d+)\s+gran_level\s+(T\d+)\s+(\d+|undef)$")
    reg_normalised = re.compile("^(A\d+)\s+normalised\s+(T\d+)$")
    reg_vernacular = re.compile("^(A\d+)\s+vernNE\s+(T\d+)$")
    reg_notes = re.compile("^(#\d+)\s+AnnotatorNotes\s+(T\d+)\s+(.+)$")
    reg_token = re.compile("(([\w\\\\.,?!'#:;&\-/\(\)@\"*$]+)_([A-Z$'.,#:;&\-/\(\)$]{1,5}) ?)")
    
    @staticmethod
    def read_annotated_data(file_to_read):
        result = {}
        with open(file_to_read) as f:
            counter = 0
#             anno = None
            for line in f:
                t = AnnotatedDataReader.reg_t.match(line)
                i = AnnotatedDataReader.reg_identifiability.match(line)
                g = AnnotatedDataReader.reg_gran_level.match(line)
                n = AnnotatedDataReader.reg_normalised.match(line)
                v = AnnotatedDataReader.reg_vernacular.match(line)
                notes = AnnotatedDataReader.reg_notes.match(line)
                if t is not None:
                    # lines that start with T
                    # T1    NP_NP 57 77    [NP my_PRP$ desk_NN]
                    anno = Annotation();
                    anno.tid = t.group(1)
                    anno.tag = t.group(2)
                    anno.start = int(t.group(3))
                    anno.end = int(t.group(4))
                    anno.original = t.group(5)
                    if anno.original.startswith("[") and anno.original.endswith("]"):
                        counter += 1
                    anno.tokens = []
                    for token in AnnotatedDataReader.reg_token.finditer(anno.original):
                        anno.tokens.append(Token(token.group(3), 
                                                 token.group(2), 
                                                 anno.start + token.start(), 
                                                 anno.start + token.start() + len(token.group(0).strip())))
                    result[anno.tid] = anno
                elif i is not None:
                    # identifiability
                    result[i.group(2)].identifiability = i.group(3)
                elif g is not None:
                    # gran_level
                    result[g.group(2)].gran_level = g.group(3)
                elif n is not None:
                    # normalised
                    result[n.group(2)].normalised = True
                elif v is not None:
                    # vernacular
                    result[v.group(2)].vernacular = True
                elif notes is not None:
                    # notes
                    result[notes.group(2)].notes = notes.group(3)
                else:
                    print line
                    raise
        print "number of annotations that are chunk: " + str(counter)
        print "number of annotations: " + str(len(result))
        return result.values()