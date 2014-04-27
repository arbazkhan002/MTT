import xml.dom.minidom

def prep_redundancies():
    doc = xml.dom.minidom.parse("output.xml")
    sentences = doc.getElementsByTagName("SENTENCE")
    replist = []
    for s in sentences:
        preps = s.getElementsByTagName("PREP")
        reps = 0
        plist = []
        for p in preps:
            plist.append(p.childNodes[0].data)
            
        lset = len(set(plist))
        llist = len(plist)
        reps = llist -lset
        replist.append(reps)

    print replist
    
    print "0 reps:", replist.count(0)
    print "1 rep:", replist.count(1)
    print "2 reps:", replist.count(2)
    print "3 reps", replist.count(3)
    print "4 reps", replist.count(4)

if __name__ == "__main__":
    prep_redundancies()

