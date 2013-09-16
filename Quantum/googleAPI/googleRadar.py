""" Program to extract all the names in google Radar Search results"""

from urllib import *
from bs4 import BeautifulSoup
from pickle import *
from psycopg2 import *

conn = connect("dbname=demo user=postgres host=localhost password=indian")
cur	= conn.cursor()

cur.execute("CREATE TABLE POIGoogle (pid character varying(50), name character varying(100), lon real, lat real, rank integer);")

f = open("/home/arbazk/MTT/Quantum/googleAPI/PKLibrary2kmRadius.xml")
rank=0
res=BeautifulSoup(f) 
for i in res.find_all("result"):
	try:		
		pid= i.id.string
		
		# Special use of name tag as i.name would give name of i rather than "name" tag of i
		for nameid in i.find_all("name"):
			pname= (nameid.string).replace("'","''")
			
		plon= i.geometry.location.lng.string
		plat=i.geometry.location.lat.string 
		rank+=1
		print pid,pname,plon,plat
		cur.execute("INSERT INTO poiGoogle VALUES ('%s', '%s', %s, %s, %s);" % (pid,pname,plon,plat,rank))			
	except Exception as e:
		print 'here ',e
		continue

conn.commit()			
	
cur.close()
conn.close()	
