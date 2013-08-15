'''
Created on Apr 12, 2013

@author: FelixLiu
'''
import re
import operator

class GeoNamesEntity:
    def __init__(self):
        self.geonameid = None
        self.name = None
        self.asciiname = None
        self.alternatenames = []
        self.latitude = None
        self.longitude = None
        self.featureclass = None
        self.featurecode = None
        self.countrycode = None
        self.cc2 = None
        self.admin1code = None
        self.admin2code = None
        self.admin3code = None
        self.admin4code = None
        self.population = None
        self.elevation = None
        self.dem = None
        self.timezone = None
        self.modificationdate = None

class GeoNamesReader:
    
    def __init__(self):
        self.dict = {}
    
    def read(self):
        self.dict = {}
        counter = 0
        reg = re.compile("^([^\t\n]*)\t([^\t\n]*)\t([^\t\n]*)\t([^\t\n]*)\t([^\t\n]*)\t([^\t\n]*)\t([^\t\n]*)\t([^\t\n]*)\t([^\t\n]*)\t([^\t\n]*)\t([^\t\n]*)\t([^\t\n]*)\t([^\t\n]*)\t([^\t\n]*)\t([^\t\n]*)\t([^\t\n]*)\t([^\t\n]*)\t([^\t\n]*)\t([^\t\n]*)\n$")
        with open("../resources/AU.txt", "r") as f:
            for line in f:
                m = reg.match(line)
                if m is None:
                    print line
                    raise
                else:
                    gne = GeoNamesEntity()
                    gne.geonameid = m.group(1)
                    gne.name = m.group(2)
                    gne.asciiname = m.group(3)
                    if m.group(4) != "":
                        gne.alternatenames = m.group(4).split(",")
                    gne.latitude = float(m.group(5))
                    gne.longitude = float(m.group(6))
                    gne.featureclass = m.group(7)
                    gne.featurecode = m.group(8)
                    gne.countrycode = m.group(9)
                    gne.cc2 = m.group(10)
                    gne.admin1code = m.group(11)
                    gne.admin2code = m.group(12)
                    gne.admin3code = m.group(13)
                    gne.admin4code = m.group(14)
                    gne.population = m.group(15)
                    gne.elevation = m.group(16)
                    gne.dem = m.group(17)
                    gne.timezone = m.group(18)
                    gne.modificationdate = m.group(19)
                    if gne.name.lower() in self.dict:
                        counter += 1
                    self.dict[gne.name.lower()] = gne
                    for alternatename in gne.alternatenames:
                        self.dict[alternatename.lower()] = gne
#                    print m.group(1)
#                    print m.group(2)
#                    print m.group(3)
#                    print m.group(4)
#                    print m.group(5)
#                    print m.group(6)
#                    print m.group(7)
#                    print m.group(8)
#                    print m.group(9)
#                    print m.group(10)
#                    print m.group(11)
#                    print m.group(12)
#                    print m.group(13)
#                    print m.group(14)
#                    print m.group(15)
#                    print m.group(16)
#                    print m.group(17)
#                    print m.group(18)
##                    print m.group(19)
#                    print

#        print counter
#        print len(self.dict)
#        print (counter + len(self.dict))
    
    @staticmethod
    def search_geonames(sentences):
        gnr = GeoNamesReader()
        gnr.read()
        counter = 0
        i = 0
        geo_en = {}
        geo_en_m = {}
        while i < len(sentences):
            j = 0
            sentence = sentences[i]
            while j < len(sentence.chunks):
                chunk = sentence.chunks[j]
                if chunk.chunk_tag != "NP":
                    j += 1
                    continue
                query = chunk.get_placenames()
                k = j + 1
                while k < len(sentence.chunks):
                    next_chunk = sentence.chunks[k]
                    if next_chunk.chunk_tag == "NP":
                        query += " " + next_chunk.get_placenames()
                    elif k + 1 < len(sentence.chunks) \
                        and next_chunk.chunk_tag == "PP" \
                        and sentence.chunks[k + 1].chunk_tag == "NP":
                        query += " " + next_chunk.get_placenames()
                    elif k + 1 < len(sentence.chunks) \
                        and next_chunk.chunk_tag is None \
                        and sentence.chunks[k + 1].chunk_tag == "NP" \
                        and (next_chunk.tokens[0].token == "," \
                             or next_chunk.tokens[0].token == "and"
                             ):
                        if next_chunk.tokens[0].token == ",":
                            query += next_chunk.get_placenames()
                        else:
                            query += " " + next_chunk.get_placenames()
                    else:
                        break
                    k += 1
                if query.lower() in gnr.dict:
                    gne = gnr.dict[query.lower()]
                    if (k - j) > 1:
                        pass
                    for c in range(j, k):
                        for token_idx, t in enumerate(sentence.chunks[c].tokens):
                            if c == j and token_idx == 0:
                                t.fcl_IOB = "B-" + gne.featureclass
                                t.fcode_IOB = "B-" + gne.featurecode
                                t.timezone = gne.timezone[10:]
                                if t.timezone == "Australia/Melbourne":
                                    t.isInsideVic = True
                                else:
                                    t.isInsideVic = False
                                if gne.featureclass in geo_en:
                                    geo_en[gne.featureclass] += 1
                                else:
                                    geo_en[gne.featureclass] = 1
                            else:
                                t.fcl_IOB = "I-" + gne.featureclass
                                t.fcode_IOB = "I-" + gne.featurecode
                                t.timezone = gne.timezone[10:]
                                if t.timezone == "Australia/Melbourne":
                                    t.isInsideVic = True
                                else:
                                    t.isInsideVic = False
                    j = k
                    counter += 1
    #                print i + 1
    #                print "chunk"
    #                print query
    #                print gnr.dict[query.lower()].name
    #                print
                else:
                    query_chunk = chunk.get_placenames()
                    if query_chunk.lower() in gnr.dict:
                        gne = gnr.dict[query_chunk.lower()]
                        counter += 1
                        for token_idx, t in enumerate(chunk.tokens):
                            if token_idx == 0:
                                t.fcl_IOB = "B-" + gne.featureclass
                                t.fcode_IOB = "B-" + gne.featurecode
                                t.timezone = gne.timezone[10:]
                                if t.timezone == "Australia/Melbourne":
                                    t.isInsideVic = True
                                else:
                                    t.isInsideVic = False
                                if gne.featureclass in geo_en:
                                    geo_en[gne.featureclass] += 1
                                else:
                                    geo_en[gne.featureclass] = 1
                            else:
                                t.fcl_IOB = "I-" + gne.featureclass
                                t.fcode_IOB = "I-" + gne.featurecode
                                t.timezone = gne.timezone[10:]
                                if t.timezone == "Australia/Melbourne":
                                    t.isInsideVic = True
                                else:
                                    t.isInsideVic = False
                    else:
                        for t in chunk.tokens:
                            if t.token.lower() in gnr.dict:
                                gne = gnr.dict[t.token.lower()]
                                t.fcl_IOB = "B-" + gne.featureclass
                                t.fcode_IOB = "B-" + gne.featurecode
                                t.timezone = gne.timezone[10:]
                                if t.timezone == "Australia/Melbourne":
                                    t.isInsideVic = True
                                else:
                                    t.isInsideVic = False
                                counter += 1
                                if gne.featureclass in geo_en:
                                    geo_en[gne.featureclass] += 1
                                else:
                                    geo_en[gne.featureclass] = 1
                            else:
                                t.fcl_IOB = "O"
                                t.fcode_IOB = "O"
#                                t.fcl_IOB = None
#                                t.fcode_IOB = None
        #                        print i + 1
        #                        print "token"
        #                        print t.token.lower()
        #                        print gnr.dict[t.token.lower()].name
        #                        print
                    j += 1
            i += 1
        print "geonames: " + str(counter)
        sorted_geo_en = sorted(geo_en.iteritems(), key = operator.itemgetter(1))
        print "reader geo_en: " + str(sorted_geo_en)

#gnr = GeoNamesReader()
#gnr.read()
#
#uni = gnr.dict['university of melboure']
#print uni.geonameid

#Yuna = gnr.dict['Mount Ziel'.lower()]
#
#print Yuna.geonameid
#print Yuna.name
#print Yuna.asciiname
#print Yuna.alternatenames
#print Yuna.latitude
#print Yuna.longitude
#print Yuna.featureclass
#print Yuna.featurecode
#print Yuna.countrycode
#print Yuna.cc2
#print Yuna.admin1code
#print Yuna.admin2code
#print Yuna.admin3code
#print Yuna.admin4code
#print Yuna.population
#print Yuna.elevation
#print Yuna.dem
#print Yuna.timezone
#print Yuna.modificationdate