from networkGraph import *
from threading import Thread
from time import sleep
import probabTable
import pickle
import random
SRC='0101000020847F0000704DF34E47D0194118485024FD5F4641'
DEST='0101000020847F0000B0627FD91ED019411851DABB05604641'


class user:
	time=0
	currpt=None
	prevpt=None
	path=None
	speed=5.0
	Pd=0.2
	def __init__(self,graph):
		self.g=graph
	
	def makemove(self,nextpt,edgewt):
		global POS
		sleep(0.2)
		self.time+=edgewt/self.speed
		self.prevpt=self.currpt	
		self.currpt=nextpt	
	
	def position(self):
		return self.currpt	
	
	def explore(self, start):
		#If the path is set, break explore mode			
		if self.path is not None:										
			return
		print "Runner(e): '%s' @'%s after %s time units'" %(self.position().nodeid,self.position().split_id,self.time)		 
		for edgeuv in self.g.adj(start):
			v=edgeuv.v
			if v!=self.prevpt:
				self.makemove(v,edgeuv.length)
				return self.explore(v)
		return self.currpt		
	
	def run(self,path):
		self.path=path
		self.makemove(path[0].u,path[0].length)
		temp=self.currpt
		print len(path)  #-- 196
		for i in range(len(path)):
			if random.random()>self.Pd:	
				self.makemove(path[i].v,path[i].length)
				#print path[i].u
				print "Runner: '%s' @'%s after %s time units'" %(self.position().nodeid,self.position().split_id,self.time)		 
			else:
				#dist = self.g.linearDistance(temp,self.currpt,path)
				#print dist,temp==self.currpt	
				self.path=None
				break
		
		
		self.explore(self.currpt)	
	pass

class server:
	time=0
	def __init__(self,graph):
		self.g=graph
		
	def wait(self):
		sleep(0.5)
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
		dist = self.g.linearDistance(prev,pos,path)
		#~ print dist#"response time", response1-response0	
		speed = dist / (response1-response0) if dist is not None else None
		#~ print "prev:",prev.nodeid,"\npos:", pos.nodeid
		#~ print "Speed track:", speed
		
		
		#------------- Finding all paths in distance 150 ----------------	
		#for spath in self.g.findallPaths(pos,150):
		#	for i in spath:
		#		print i.nodeid
		#	print "############################"	
		#-----------------------------------------------------------------
			
		while(pos!=prev):
			self.wait()
			prev=pos
			pos=runner.position()
			#~ if pos is not None:
				#~ print "tracker:",pos.nodeid
		pass	

if __name__=="__main__":
	global runner,tracker
	conn = connect("dbname=demo user=postgres host=localhost password=indian")
	g=networkGraph()
	g.build_graph(conn)
	#probabTable.build(g,conn)
	
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
		r=Thread(target=runner.run, args=([path])).start()
		# r.daemon=True
		t=Thread(target=tracker.track, args=([runner])).start()
		# t.daemon=True
	finally:
		# t.join()
		# r.join()
		pass
	
