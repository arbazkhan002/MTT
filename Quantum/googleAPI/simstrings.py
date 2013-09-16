""" Program to extract all the names in wikimapia inside IIT Kanpur's bounding box"""

from urllib import *
from bs4 import BeautifulSoup
from pickle import *
from psycopg2 import *
import difflib
#~ import simstring

conn = connect("dbname=demo user=postgres host=localhost password=indian")
cur	= conn.cursor()

cur.execute("select name from poi;")
results=[]
for row in cur.fetchall():
	results.append(row[0])
print difflib.get_close_matches("theater",results,3,0.3);

#~ results=open("names.txt","w")
#~ for row in cur.fetchall():
	#~ results.write(str(row[0])+"\n")
#~ 
#~ results.close()
#~ db = simstring.reader("names.txt")
#~ db.measure = simstring.cosine
#~ db.threshold = 0.9
#~ print db.retrieve('canteen')

conn.commit()			
	
cur.close()
conn.close()	
