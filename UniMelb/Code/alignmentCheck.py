# Base file for Di.txt
# Checks the identifiability of the triplets on a scale 1 to 3.
# 1 - completely identified as it is
# 2 - identified all pieces
# 3 - not identified as whole or as pieces
import sys
#~ Check for port number 
if (len(sys.argv) < 2):
	 print "ERROR, no file_number provided\nusage: python ",sys.argv[0]," file_no"
	 exit(1);     
	 
i = sys.argv[1]

f=open("all_"+i+".txt")
g=open("Descr-Relations_Rev_"+i+".csv")
#~ h=open("output.csv","w")
#~ desc = f.read
words=[]
for line in f:
	l = line.upper().split()	
	words.extend(l)

wordsOrig = " ".join(words).upper()
doc=[]
for line in g:
	l=line.strip().split(",")[:3]
	
	trip = ["","",""]
	
	#~ l is a list [RO,i,L]
	#~ exp is an element of l, word is a word in RO/i/L
	for index,exp in enumerate(l):
		flag=0
		if exp.upper() in wordsOrig:
			trip[index]=[1,exp]
			flag=1

		if flag==1:
			continue
		annot=""
		
		#~ print exp,flag, "*2*"		
		
		if flag==0 and (len(exp.split())>1):
			for word in exp.split():
				flag=0
					
				for j in words:
					if word.upper() in j:				
						flag=1
				
				if flag==1:
					annot+=word + " "
				else:
					break
		if flag==1:
			trip[index]=[2,annot]

		else:
			trip[index]=[3,exp]			
	doc.append(trip)

for i in doc:
	for j in i:
		print j,
	print	
	
