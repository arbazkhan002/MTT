#~ USE TO RUN for i in {1..10}; do echo $i | python scriptToParseResults.py >> attTabularResults.txt; done
#~ c=int(raw_input("att:"))
#~ f=open("att"+str(c)+".txt")
f=open("/home/arbazk/MTT/Quantum/MovingDot/resultsToTest.txt")
Gt=0
n=0
#~ stat=["status: ","questions: "]
stat=["G: "]
result={}
N={}
map(lambda x:result.setdefault(x,0),stat)
map(lambda x:N.setdefault(x,0),stat)

while 1:
	try:
		st=""
		while not reduce(lambda x,y:x or y, map(lambda x: st.strip().startswith(x),stat)):
			st=f.readline()
			if not st:
				break
		if not st:
			break
				
		for string in stat:
			if st.startswith(string):
				result[string]+=int(st[len(string):])
				N[string]+=1.0
				
	except Exception as e:
		print e	
		print "here"
		break

#~ print c,map(lambda x: (x,result[x]/N[x] + (1 if x.startswith("questions") else 0)) ,result)
print map(lambda x: (x,result[x]/N[x]) ,result)
