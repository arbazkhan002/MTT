'''
Created on Apr 13, 2013

@author: FelixLiu
'''
from xlrd import open_workbook
import operator

class VicNamesEntity:
    
    def __init__(self):
        self.state = None
        self.municipality = None
        self.nameid = None
        self.placename = None
        self.placenamestatus = None
        self.featurecode = None
        self.longitude = None
        self.latitude = None
        self.placeid = None
        self.historyinformation = None
        self.originlanguage = None
        self.australianindigenouslanguage = None
        self.datefirstrecordedday = None
        self.datefirstrecordedmonth = None
        self.datefirstrecordedyear = None
        self.source = None
        self.author = None
        self.title = None
        self.datepublishedday = None
        self.datepublishedmonth = None
        self.datepublishedyear = None
        self.publisher = None
        self.placeofpublication = None
        self.page = None
        self.editor = None
        self.chaptertitle = None
        self.journalname = None
        self.issue = None
        self.year = None
        self.newspaper = None
        self.filenumber = None
        self.siteowner = None
        self.pagetitle = None
        self.sitetitle = None
        self.url = None
        self.location = None
        self.typeofartefact = None
        self.cartographer = None
        self.scale = None
        self.informat = None
        self.tapetitle = None
        self.tapenumber = None

class VicNamesReader:
    
    def __init__(self):
        self.dict = {}
        
    def read(self):
        book = open_workbook("../resources/placeNames.xlsx")
        sheet = book.sheet_by_index(0)
        rowcount = sheet.nrows
        counter = 0
        for i in range(rowcount - 1):
            row = sheet.row_slice(i + 1)
            vne = VicNamesEntity()
            vne.state = str(row[0].value)
            vne.municipality = str(row[1].value)
            vne.nameid = str(row[2].value)
            vne.placename = row[3].value
            vne.placenamestatus = str(row[4].value)
            vne.featurecode = str(row[5].value)
            vne.longitude = str(row[6].value)
            vne.latitude = str(row[7].value)
            vne.placeid = str(row[8].value)
#            vne.historyinformation = str(row[9].value)
            if vne.placename.lower() in self.dict:
                counter += 1
            self.dict[vne.placename.lower()] = vne
            
#        print counter
#        print rowcount

    @staticmethod
    def search_vicnames(sentences):
        vnr = VicNamesReader()
        vnr.read()
        counter = 0
        i = 0
        geovic_count = 0
        vic_en = {}
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
                if query.lower() in vnr.dict:
                    vne = vnr.dict[query.lower()]
                    for c in range(j, k):
                        flag = True
                        for token_idx, t in enumerate(sentence.chunks[c].tokens):
                            if c == j and token_idx == 0:
                                t.fcl_IOB_vic = "B-" + vne.featurecode
                                if t.fcl_IOB and not t.fcl_IOB.startswith("B-"):
                                    flag = False
                                if vne.featurecode in vic_en:
                                    vic_en[vne.featurecode] += 1
                                else:
                                    vic_en[vne.featurecode] = 1
                            else:
                                t.fcl_IOB_vic = "I-" + vne.featurecode
                                if t.fcl_IOB and not t.fcl_IOB.startswith("I-"):
                                    flag = False
                        if flag:
                            geovic_count += 1
                    j = k
                    counter += 1
    #                print i + 1
    #                print "chunk"
    #                print query
    #                print vnr.dict[query.lower()].name
    #                print
                else:
                    query_chunk = chunk.get_placenames()
                    if query_chunk.lower() in vnr.dict:
                        vne = vnr.dict[query_chunk.lower()]
                        counter += 1
                        for token_idx, t in enumerate(chunk.tokens):
                            flag = True
                            if token_idx == 0:
                                t.fcl_IOB_vic = "B-" + vne.featurecode
                                if t.fcl_IOB and not t.fcl_IOB.startswith("B-"):
                                    flag = False
                                if vne.featurecode in vic_en:
                                    vic_en[vne.featurecode] += 1
                                else:
                                    vic_en[vne.featurecode] = 1
                            else:
                                t.fcl_IOB_vic = "I-" + vne.featurecode
                                if t.fcl_IOB and not t.fcl_IOB.startswith("I-"):
                                    flag = False
                            if flag:
                                geovic_count += 1
                    else:
                        for t in chunk.tokens:
                            if t.token.lower() in vnr.dict:
                                vne = vnr.dict[t.token.lower()]
                                t.fcl_IOB_vic = "B-" + vne.featurecode
                                counter += 1
                                if t.fcl_IOB and not t.fcl_IOB.startswith("B-"):
                                    geovic_count += 1
                                if vne.featurecode in vic_en:
                                    vic_en[vne.featurecode] += 1
                                else:
                                    vic_en[vne.featurecode] = 1
                            else:
                                t.fcl_IOB_vic = "O"
#                                t.fcl_IOB_vic = None
        #                        print i + 1
        #                        print "token"
        #                        print t.token.lower()
        #                        print vnr.dict[t.token.lower()].name
        #                        print
                    j += 1
            i += 1
        print "vicnames: " + str(counter)
        print "tagged in both geonames and vicnames: " + str(geovic_count)
        sorted_vic_en = sorted(vic_en.iteritems(), key = operator.itemgetter(1))
        print "reader vic_en: " + str(sorted_vic_en)

#vnr = VicNamesReader()
#vnr.read()
#print vnr.dict["airport west post office"].placename