from networkGraph import *
from threading import Thread
from time import sleep
import pickle
SRC='0101000020847F0000704DF34E47D0194118485024FD5F4641'
DEST='0101000020847F0000B0627FD91ED019411851DABB05604641'
P_ORIENTED=0.95

class user:
	time=0
	currpt=None
	nextpt=None
	def __init__(self,graph):
		self.g=graph
	
	def makemove(self,nextpt,nbr):
		global POS
		sleep(0.2)
		self.time+=1
		self.currpt=nextpt	
		self.nextpt=nbr
	
	def position(self):
		return self.currpt	
	
	def run(self,path):
		print len(path)  #-- 196
		for i in range(len(path)):
			self.makemove(path[i].u,path[i].v)
			#~ print path[i].u
			#~ print "Runner: '%s'" %(self.position().nodeid)		
	pass

class server:
	time=0
	def __init__(self,graph):
		self.g=graph
		
	def wait(self):
		sleep(0.6)
		self.time+=1
	
	def track(self,runner):
		prev=None
		
		pos=runner.position()
		while (prev is None):
			response0=self.time
			self.wait()
			prev=pos
			pos=runner.position()
		
		response1=self.time
		#~ print "response time", response1-response0	
		speed = self.g.linearDistance(prev,pos,path) / (response1-response0)
		print speed
			
		while(pos!=prev):
			self.wait()
			prev=pos
			pos=runner.position()
			#~ if pos is not None:
				#~ print "tracker:",pos.nodeid
		pass	

def buildProbabTable(g,conn):

	cur=conn.cursor()
	cur.execute("CREATE TABLE probabTable (node bigInt, edge1 bigInt, edge2 bigInt, inPath boolean, probability real)")

	for node in g.geomNodes.values():
		size=len(g.edges[node])
		for edge1 in g.edges[node]:
			for edge2 in g.edges[node]:
				if edge1==edge2:
					continue
				else:
					#pass
					cur.execute("INSERT INTO probabTable VALUES (%s, %s,%s,%s,%s)",(node.nodeid, edge1.edgeId,edge2.edgeId,True,P_ORIENTED));
					cur.execute("INSERT INTO probabTable VALUES (%s, %s,%s,%s,%s)", (node.nodeid, edge1.edgeId,edge2.edgeId,False,(1-P_ORIENTED)/size));
					
	cur.close()
	conn.commit()
	conn.close()				

#~ runner = None
#~ tracker = None
#inmem = connect(':memory:')

if __name__=="__main__":
	global runner,tracker
	conn = connect("dbname=demo user=postgres host=localhost password=indian")
	g=networkGraph()
	g.build_graph(conn)
	#buildProbabTable(g,conn)
	
	eg=g.getNode('0101000020847F0000165E0110C94B1A41079011A6B6584641')
	
	#*************** dfs test *************************
	#~ for i in g.dfs(g.getNode(SRC), g.getNode(DEST)):
	#~ for i in g.dfs(eg, g.edges[eg][0].v):
		#~ print len(g.edges[i.u])
	#********************************************

	#*************** route ***********************
	#~ for i in range(10):
		#~ print g.geomNodes[(g.geomNodes.keys()[i])].geom
	#*******************************************
	
	path = g.dfs(g.getNode(SRC), g.getNode(DEST))
	#~ for i in path:
		#~ print i.u
	runner = user(g)
	tracker = server(g)
	try:
		pass
		# r=Thread(target=runner.run, args=([path])).start()
		# r.daemon=True
		# t=Thread(target=tracker.track, args=([runner])).start()
		# t.daemon=True
	finally:
		# t.join()
		# r.join()
		pass
	
