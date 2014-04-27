#!/usr/bin/python

import random


random.seed(42.23)
n = 100   #number of walks
wmin = 15 #min (incl.) number of actions in a walk
wmax = 16 #max (excl.) number of actions in a walk


distances={"city(a)":{"city(a)":0,"city(b)":8,"city(c)":14,"city(d)":10},
           "city(b)":{"city(a)":8,"city(b)":0,"city(c)":10,"city(d)":17},
           "city(c)":{"city(a)":14,"city(b)":10,"city(c)":0,"city(d)":12},
           "city(d)":{"city(a)":10,"city(b)":17,"city(c)":12,"city(d)":0}}


activities={"1":{           "city(b)":11,"city(c)":12,"city(d)":13},
            "2":{"city(a)":7,            "city(c)":8,"city(d)":9},
            "3":{"city(a)":2,"city(b)":3 },
            "4":{"city(a)":1},
            "5":{"city(a)":10,"city(b)":5,"city(c)":5,"city(d)":5},
            "6":{                         "city(c)":8,"city(d)":8},
            "7":{                         "city(c)":10},
            "8":{"city(a)":2, "city(c)":3,"city(d)":10}}

def processactivities() :
    result = {}
    for act in activities.keys():
        result["act("+str(act)+",normal)"]={}
        result["act("+str(act)+",fast)"]={}
        for city in activities[act].keys():
            result["act("+str(act)+",normal)"][city] = activities[act][city]
            tmp = 0
            if city=="city(a)":
                tmp=22
            elif city=="city(b)":
                tmp=50
            elif city=="city(c)":
                tmp=12
            elif city=="city(d)":
                tmp=10
            result["act("+str(act)+",fast)"][city] = activities[act][city]+tmp
    return result

activities = processactivities()



def calcCosts(activitylist,citylist) :
    if not len(citylist)==len(activitylist):
        return False
    costs = 0
    for i in range(len(activitylist)):
        #aktion in stadt nicht moeglich
        if not citylist[i] in activities[activitylist[i]].keys():
            return False
        costs += activities[activitylist[i]][citylist[i]]
        #weg in naechste Stadt nicht moeglich
        if i < len(activitylist)-1 :
            if not citylist[i+1] in distances[citylist[i]].keys() :
                return False
            costs += distances[citylist[i]][citylist[i+1]]
    return costs

def makeRandomActivitylist(l) :
    result= []
    for i in range(l):
        result += [random.choice(activities.keys())]
    return result

def makeallCitylists(activitylist) :
    if len(activitylist)==1:
        result=[]
        for c in activities[activitylist[0]].keys():
            result += [[c]]
        return result

    result = []
    for r in makeallCitylists(activitylist[1:]):
        for c in activities[activitylist[0]].keys():
            result += [[c]+r]
    return result

def getBestCitylistExact(a):
    best = False
    bestcosts = 0
    for b in makeallCitylists(a):
        c = calcCosts(a,b)
        if not c == False:
            if best == False:
                best = b
                bestcosts = c
            else:
                if c<bestcosts:
                    best=b
                    bestcosts=c                    
    return best

def getBestCitylistApprox(a):
    result=[]
    startindex=0
    while startindex<len(a):
        endindex = startindex+random.randrange(2,10)
        result += getBestCitylistExact(a[startindex:endindex])
        startindex=endindex
    return result


allwalks=[]

f=file("ausgabe.xml","w")


f.write("<data>\n")
f.write("<classatoms>\n")
for c in distances.keys() :
    f.write("    <atom>"+str(c)+"</atom>\n")
f.write("  </classatoms>\n")


for i in range(n):
    l = random.randrange(wmin,wmax)
    a = makeRandomActivitylist(l)
    b = getBestCitylistApprox(a)
    c = calcCosts(a,b)
    allwalks+=[(a,b,c)]    
    f.write("  <sequence number=\""+str(i+1)+"\" costs=\""+str(c)+"\">\n")
    f.write("    <input>\n")
    for element in a:
        f.write("      <entry>"+str(element)+"</entry>\n")
    f.write("    </input>\n")
    f.write("    <output>\n")
    for element in b:
        f.write( "      <entry>"+str(element)+"</entry>\n")
    f.write("    </output>\n")
    f.write("  </sequence>\n")
    print str(i+1)

f.write("</data>\n")
