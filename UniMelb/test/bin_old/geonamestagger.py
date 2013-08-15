'''
Created on Apr 7, 2013

@author: FelixLiu
'''
import urllib2
import json
import geonames
from ler import AnnotatedDataReader

def set_proxy():
    proxy_support = urllib2.ProxyHandler({"http":"http://fliu3:63421390@wwwproxy.student.unimelb.edu.au:8000"})
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)

def search_geonames_json(query):
    return geonames.fetchJson("searchJSON", {'q' : query, 'maxRows' : '1', 'country' : 'AU'})

def write_geonames(annotations):
    with open("./geonames.json", "w") as f:
        string = ""
        counter = 0
        for anno in annotations:
            if anno.identifiability == "yes_unamb":
                if anno.notes:
                    query = anno.notes
                else:
                    query = anno.get_placename()
                if counter >= 1900:
                    break
                js = search_geonames_json(query)
                counter += 1
                if js['totalResultsCount'] == 1:
                    js['geonames'][0]['tid'] = anno.tid
                    print anno.tid
                    print query
                    print str(js['geonames'][0])
                    string += json.dumps(js['geonames'][0]) + '\n'
        f.write(string)
                
def read_geonames():
    geo = {}
    with open("./geonames.json", "r") as f:
        for line in f:
            data = None
            if line == "":
                continue
            data = json.loads(line)
            geo[data['tid']] = data
    return geo
    

def main():
    
    set_proxy()
    
#    result = AnnotatedDataReader.read_annotated_data("../resources/tuw_chunked_data.ann")
#    
#    result.sort(key = lambda k : k.start)
#    
#    write_geonames(result)
    
    read_geonames()
    
#    with open("./geonames.json", "w") as f:
#        string = ""
#        for anno in result:
#            if anno.identifiability == "yes_unamb":
#                if anno.notes:
#                    query = anno.notes
#                else:
#                    query = anno.get_placename()
#                print anno.tid
#                print query
#                
##                js = geonames.fetchJson("searchJSON", {'q' : query, 'maxRows' : '1', 'country' : 'AU'})
##                string = ""
##                if js['totalResultsCount'] == 1:
##                    print str(js['geonames'][0])
##                    string += str(js['geonames'][0]) + '\n'
#                print ''
#        js = geonames.fetchJson("searchJSON", {'q' : 'University of Melbourne', 'maxRows' : '1', 'country' : 'AU'})
#        string = ""
#        if js['totalResultsCount'] == 1:
#            js['geonames'][0]['tid'] = 'T34'
#            print json.dumps(js['geonames'][0])
#            string += json.dumps(js['geonames'][0]) + '\n'
#        
#        f.write(string)
#    
    
if __name__ == "__main__":
    main()