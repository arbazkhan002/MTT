""" Program to extract all the names in wikimapia inside IIT Kanpur's bounding box"""

from urllib import *
from bs4 import BeautifulSoup
from pickle import *
from psycopg2 import *

conn = connect("dbname=demo user=postgres host=localhost password=indian")
cur	= conn.cursor()

cur.execute("CREATE TABLE POI (pid integer, name character varying(100), lon real, lat real);")

# Results occur in multiple pages, we need to iterate through all
page=2
while 1:
	
	params = urlencode({'key': '8CD4EFB5-75BA267B-50A173EB-0C2F4999-191CB031-4173BFC9-CDF91AD6-D3347C0B','function':'box',
			'lon_min':80.2183914,'lat_min':26.503299,'lon_max':80.2468657,'lat_max':26.5210697,'page':page,'count':100}
			)
	f = urlopen("http://api.wikimapia.org/?%s" % params)

	res=BeautifulSoup(f) 
	print (res.place==None)
	if res.place==None:
		break
	for i in res.find_all("place"):
		try:		
			pid= i['id']
			
			# Special use of name tag as i.name would give name of i rather than "name" tag of i
			for nameid in i.find_all("name"):
				pname= (nameid.string).replace("'","''")
				
			plon= i.location.lon.string
			plat=i.location.lat.string 
			cur.execute("INSERT INTO poi VALUES (%s, '%s', %s, %s);" % (pid,pname,plon,plat))			
		except Exception as e:
			print 'here ',e
			continue
	page+=1

conn.commit()			
	
cur.close()
conn.close()	
