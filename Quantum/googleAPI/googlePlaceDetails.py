""" Program to extract all the details on radar search done with radius 2km centered at PK Kelkar Library"""

from urllib import *
from bs4 import BeautifulSoup
from pickle import *
import requests
import httplib
import socket
from httplib import HTTPConnection, HTTPS_PORT
import ssl
#~ 
#~ class HTTPSConnection(HTTPConnection):
    #~ "This class allows communication via SSL."
    #~ default_port = HTTPS_PORT
#~ 
    #~ def __init__(self, host, port=None, key_file=None, cert_file=None,
            #~ strict=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
            #~ source_address=None):
        #~ HTTPConnection.__init__(self, host, port, strict, timeout,
                #~ source_address)
        #~ self.key_file = key_file
        #~ self.cert_file = cert_file
#~ 
    #~ def connect(self):
        #~ "Connect to a host on a given (SSL) port."
        #~ sock = socket.create_connection((self.host, self.port),
                #~ self.timeout, self.source_address)
        #~ if self._tunnel_host:
            #~ self.sock = sock
            #~ self._tunnel()
        #~ # this is the only line we modified from the httplib.py file
        #~ # we added the ssl_version variable
        #~ self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)
#~ 
#~ #now we override the one in httplib
#~ httplib.HTTPSConnection = HTTPSConnection
# ssl_version corrections are done

xml_file= BeautifulSoup(open("/home/arbazk/MTT/Quantum/googleAPI/GoogleRadarSearch_keyword=iit.xml"))
result_file=open("googleplaceDetails_key=iit.xml","w")
count=0
for place in xml_file.find_all("result"):
	reference = place.reference.string

	params = urlencode({'key': 'AIzaSyCzhOo4mqXFIMa73xk5N-2A5mifzcpINfo',
			'reference': reference,
			'sensor':'false'}
			)
	conn = httplib.HTTPSConnection("maps.googleapis.com")
	conn.request("GET","/maps/api/place/details/xml?%s"% params)
	f=conn.getresponse()
	print f.status, f.reason,count
	result_file.write(f.read())
	count+=1
conn.close()
#~ 
	#~ res=BeautifulSoup(f) 
	#~ print (res.place==None)
	#~ if res.place==None:
		#~ break
	#~ for i in res.find_all("place"):
		#~ try:		
			#~ pid= i['id']
			#~ 
			#~ # Special use of name tag as i.name would give name of i rather than "name" tag of i
			#~ for nameid in i.find_all("name"):
				#~ pname= (nameid.string).replace("'","''")
				#~ 
			#~ plon= i.location.lon.string
			#~ plat=i.location.lat.string 
			#~ cur.execute("INSERT INTO poi VALUES (%s, '%s', %s, %s);" % (pid,pname,plon,plat))			
		#~ except Exception as e:
			#~ print 'here ',e
			#~ continue
	#~ page+=1

