'''
Created on Apr 1, 2013

@author: FelixLiu
'''
import geonames
import urllib2
from geopy import geocoders
import json

class Annotation:
    def __init__(self, 
                 tid = None, 
                 tag = None, 
                 start = None, 
                 end = None, 
                 original = None,
                 tokens = [], 
                 identifiability = None, 
                 gran_level = None, 
                 normalised = False, 
                 vernacular = False,
                 notes = None):
        self.tid = tid
        self.tag = tag
        self.start = start
        self.end = end
        self.original = original
        self.tokens = tokens
        self.identifiability = identifiability
        self.gran_level = gran_level
        self.normalised = normalised
        self.vernacular = vernacular
        self.notes = notes
        self.filled = 0
        self.filled_str = ""
        
    def fill(self, fill):
        self.filled_str += fill
        self.filled += len(fill)
        
    def is_filled(self):
        return len(self.filled_str.strip()) == self.end - self.start
    
    def jsonable(self):
        return self.__dict__
    
def ComplexHandler(Obj):
    if hasattr(Obj, 'jsonable'):
        return Obj.jsonable()
    else:
        raise TypeError, 'Object of tupe %s with value of %s is not JSON serialize'

def get_param(obj, param_name):
    for key, value in obj:
        if key == param_name:
            return value
    return None

def object_decoder(obj):
    tid = get_param(obj, 'tid')
    tag = get_param(obj, 'tag')
    try:
        start = int(get_param(obj, 'start'))
    except:
        start = None 
    try:
        end = int(get_param(obj, 'end'))
    except:
        end = None
    original = get_param(obj, 'original')
    tokens = get_param(obj, 'tokens')
    identifiability = get_param(obj, 'identifiability')
    try:
        gran_level = int(get_param(obj, 'normalised'))
    except:
        gran_level = None
    vernacular = get_param(obj, 'vernacular')
    notes = get_param(obj, 'notes')
    return Annotation(tid, tag, start, end, original, tokens, identifiability, gran_level, vernacular, notes)

def main():
    proxy_support = urllib2.ProxyHandler({"http":"http://fliu3:63421390@wwwproxy.student.unimelb.edu.au:8000"})
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
    
    js = geonames.fetchJson("searchJSON", {'q':'University of Melbourne', 'maxRows':'10', 'country':'AU'})
    
    print js
    print js['geonames'][0]
    print js['geonames'][0]['fcl']
    print js['geonames'][0]['fcode']
    
    anno = Annotation()
    anno.original = "ABCD"
    anno.tokens
    string = ""
#    print anno.__dict__
    with open("./json", "w") as f:
#        string = json.dumps(anno, default = ComplexHandler)
        json.dump(anno, f, default = ComplexHandler)
        
    with open("./json", "r") as f:
        json.load(f, object_pairs_hook = object_decoder)
#        ann = json.loads(string, object_pairs_hook = object_decoder)
#        print ann.original
    
#    print json.dump(anno, default = lambda o : o.__dict__)
    
    
#    g = geocoders.GeoNames()
#    g.country_bias = "AU"
#    place, (lat, lng) = g.geocode("Melbourne University", "AU")
#    print "%s: %.5f, %.5f" % (place, lat, lng)

if __name__ == '__main__':
    main()