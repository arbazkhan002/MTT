""" Program to extract all the names in wikimapia inside IIT Kanpur's bounding box"""

from urllib import *
from bs4 import BeautifulSoup
from pickle import *
from psycopg2 import *
import difflib
#~ import simstring

conn = connect("dbname=demo user=postgres host=localhost password=indian")
cur	= conn.cursor()

cur.execute("select pid,lon,lat from poi;")
for row in cur.fetchall():
	cur.execute("update poi set geom=st_transform(st_setSRID(st_makepoint(%s,%s),4326),32644) where pid=%s" % (row[1],row[2],row[0]))

conn.commit()			
	
cur.close()
conn.close()	
