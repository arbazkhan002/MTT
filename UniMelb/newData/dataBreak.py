f=open("newData.txt")
counter=0
new=2

for char in f.read():
	if char=="\t":
		new = 1 if new==0 else new-1
		if new==1:
			#~ new-=1
			#~ g.close()
			counter+=1
			g=open("campus"+str(counter)+".txt","w")
	
	else:
		
		if new==0:
			g.write(char)
		else:
			print new,char	
