""" Program to extract all the names in wikimapia inside IIT Kanpur's bounding box"""

from urllib import *
from bs4 import BeautifulSoup
from pickle import *
from psycopg2 import *

conn = connect("dbname=demo user=postgres host=localhost password=indian")
cur	= conn.cursor()

#~ cur.execute("CREATE TABLE salience_helper (gid integer, name character varying(100), geom geometry, wiki integer);")

cur.execute("select table_name from information_schema.tables where table_type='BASE TABLE' and table_schema='public'")

for table in cur.fetchall():

	if table.startswith("edget") or table.startswith("salience_of_landmarks") or table.startswith("network") or table.startswith("node") or table.startswith("poi") or table.startswith("roads"):
		continue
	cur2	= conn.cursor()
	cur2.execute("select * from %s" % table)
	for row in cur2.fetchall():
		cur2.execute("insert into salience_of_landmarks VALUES (%s,%s,%s,0)" % (row[)
	
	
	cur2.execute("select column_name from information_schema.columns where table_name='parks'")
	if "name" in cur2.fetchall():
		

		
