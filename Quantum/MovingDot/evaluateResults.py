# USE TO RUN for i in {1..10}; do echo $i | python scriptToParseResults.py >> attTabularResults.txt; done
# UnComment out the lines and comment out the adjacent ones to change mode

#~ c=int(raw_input("att:"))
f=open("/home/arbazk/MTT/Quantum/MovingDot/resultsToTest.txt")
Gt=0
n=0
#~ stat=["status: ","questions: "]
stat=["G: ","Questions: ", "Mistakes: "]
result={}
N={}
map(lambda x:result.setdefault(x,[]),stat)
map(lambda x:N.setdefault(x,0),stat)

while 1:
	#~ try:
		st=""
		while not reduce(lambda x,y:x or y, map(lambda x: st.strip().startswith(x),stat)):
			st=f.readline()
			if not st:
				break
		if not st:
			break
		st=st.strip()		
		for string in stat:
			if st.startswith(string) and st.startswith("Mistakes"):
				result["Questions: "][-1]/=int(st[len(string):])*1.0
				result[string].append(int(st[len(string):]))	
				N[string]+=1.0
			elif st.startswith(string) and not st.startswith("Mistakes"):
				result[string].append(int(st[len(string):]))
				N[string]+=1.0
				
	#~ except Exception as e:
		#~ print e	
		#~ print "here"
		#~ break

#~ print c,map(lambda x: (x,result[x]/N[x] + (1 if x.startswith("questions") else 0)) ,result)
print map(lambda x: (x,sum(result[x])/N[x]) ,result)
