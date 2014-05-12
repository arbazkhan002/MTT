#~ USE TO RUN for i in {1..10}; do echo $i | python scriptToParseResults.py >> attTabularResults.txt; done
c=int(raw_input("att:"))
f=open("att"+str(c)+".txt")
Gt=0
n=0
stat=["status: ","questions: "]
result={}
N={}
map(lambda x:result.setdefault(x,0),stat)
map(lambda x:N.setdefault(x,0),stat)
condition=0
print "Checking the number of questions asked when succeeded"
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
			if st.startswith(string) and string.startswith("questions") and condition==1:
				result[string]+=int(st[len(string):])
				N[string]+=1.0
				
			elif st.startswith(string) and not string.startswith("questions"): 
				output=int(st[len(string):])
				result[string]+=int(st[len(string):])
				N[string]+=1.0
		
		if output==1 and st.startswith("status"):
			condition=1
		else:
			condition=0	
				
	except Exception as e:
		print e	
		print "here"
		break

print c,map(lambda x: (x,result[x]/N[x] + (1 if x.startswith("questions") else 0)) ,result)
