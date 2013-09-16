""" Program to create point geometry using lat/lon results in wikimapia/google"""

from urllib import *
from bs4 import BeautifulSoup
from pickle import *
from psycopg2 import *
import difflib
#~ import simstring

conn = connect("dbname=demo user=postgres host=localhost password=indian")
cur	= conn.cursor()
#~ cur.execute("select pid,lon,lat from poi;")  # For wikimapia 
cur.execute("alter table poigoogle add column geom geometry") # For google
cur.execute("select pid,lon,lat from poigoogle;") # For google
for row in cur.fetchall():
	cur.execute("update poigoogle set geom=st_transform(st_setSRID(st_makepoint(%s,%s),4326),32644) where pid='%s'" % (row[1],row[2],row[0]))

conn.commit()			
	
cur.close()
conn.close()	
