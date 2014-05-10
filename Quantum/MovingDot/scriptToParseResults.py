f=open("resultsToTest.txt")
Gt=0
n=0
while 1:
	try:
		for i in range(7):
			f.readline()
		G=f.readline()
		Gt+=int(G[3:].strip())
		n+=1
		#~ print G
		for i in range(2):
			f.readline()
	except Exception as e:
		print e	
		break

print (Gt*1.0)/n
