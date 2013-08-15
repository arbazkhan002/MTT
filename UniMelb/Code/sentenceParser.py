# Appends a sentence number to each of the triplets
import sys
#~ Check for port number 
if (len(sys.argv) < 2):
	 print "ERROR, no file_number provided\nusage: python ",sys.argv[0]," file_no"
	 exit(1);     
	 
i = sys.argv[1]

f=open("all_"+i+".txt")
g=open("Descr-Relations_Rev_"+i+".csv")
