from networkGraph import *
from threading import Thread
from time import sleep
import probabTable
import pickle
import random
import logger
SRC='0101000020847F0000704DF34E47D0194118485024FD5F4641'
DEST='0101000020847F0000B0627FD91ED019411851DABB05604641'
LOG=logger.logger("logfile.txt")
conn = connect("dbname=demo user=postgres host=localhost password=indian")
class user:
	time=0
	currpt=None
	prevpt=None
	path=None
	speed=5.0
	Pd=0.0
	def __init__(self,graph):
		self.g=graph
		self.time=0
	
	def makemove(self,nextpt,edgewt):
		global POS
		sleep(0.2)
		self.time+=edgewt/self.speed
		self.prevpt=self.currpt	
		self.currpt=nextpt	
	
	def position(self):
		return self.currpt	
	
	def gettime(self):
		return self.time		
	
	#To walk in a random fashion (pick random edges at each decision point)
	def explore(self, start):
		#If the path is set, break explore mode			
		if self.path is not None:										
			return
		print "Runner(e): '%s' @'%s after %s time units'" %(self.position().nodeid,self.position().split_id,self.time)		 
		for edgeuv in random.sample(self.g.adj(start),len(self.g.adj(start))):
			v=edgeuv.v
			if v!=self.prevpt:
				self.makemove(v,edgeuv.length)
				return self.explore(v)
		return self.currpt		
	
	
	# To follow a path
	def run(self,path):
		self.path=path
		self.makemove(path[0].u,path[0].length)
		temp=self.currpt
		update=[] #Stores all traversed paths 
				  #A traversed path is of the form [Edgeprev, Edgenext,Inpath] to update probability tables
				  #Idea is to update probability table for each edge edgeprev such that the record1 <edgeprev,edgenext,inpath>
				  #gets 1% probability of every record2 of type <edgeprev,_,(!inpath)> (except record1)
				  # for all record2, probab=0.99probab, sum+=0.01probab
				  # for record1, probab+=sum   (so that the net probab is 1 always)
		print len(path)  #-- 196
		for i in range(len(path)):
			if random.random()>self.Pd:	
				update.append([path[i-1].edgeId,path[i].edgeId,int(True)])
				self.makemove(path[i].v,path[i].length)
				#print path[i].u
				print "Runner: '%s' @'%s after %s time units'" %(self.position().nodeid,self.position().split_id,self.time)		 
			else:
				#dist = self.g.linearDistance(temp,self.currpt,path)
				#print dist,temp==self.currpt	
				update.append([path[i-1].edgeId,path[i].edgeId,int(False)])
				self.path=None
				break
		
		LOG.write(update)
		
		self.explore(self.currpt)	
	pass

lock=1

class server:
	time=0
	def __init__(self,graph):
		self.g=graph
		self.time=0
		
	def wait(self):
		sleep(0.2)
		self.time+=1
	
	def checkcorrect(self,runner,ttime):
		return runner.gettime()-ttime
		
	def updatespeed(self,t1,t2,d):
		return d/(t1-t2)		
	
	def track(self,runner,path):
		prev=None
		prevtime=0
		pos=runner.position()
		while (prev is None):
			response0=self.time
			self.wait()
			prev=pos
			pos=runner.position()
			tracktime=prevtime=runner.gettime()	
		
		response1=self.time
		dist = self.g.linearDistance(prev,pos,path)
		#~ print dist#"response time", response1-response0	
		speed = dist / (response1-response0) if dist is not None else None
		#~ print "prev:",prev.nodeid,"\npos:", pos.nodeid
		#~ print "Speed track:", speed
		sections={}
		for ind,i in enumerate(path):
			sections[i]=ind
		landmarks=[0 for i in range(len(path))]	 # ref_ids of landmark at each section
												 # landmark corresponding to section path[i] is landmarks[i]
												 # 0 indicates no landmark nearby to that section
												 
		seen = [] #list of landmarks already seen
		#~ print map(lambda x: x.splitId, path)
		cur=conn.cursor()
		cur.execute(cur.mogrify("select dump_id,ref_id from sectlandmark where dump_id = ANY(%s)", (map(lambda x: x.splitId, path),)))
		
		for row in cur:
			row=dbfields.reg(cur,row)
			landmarks[sections[row.dump_id]-1]=row.ref_id
		
		#~ for i in range(len(path)):
			#~ tracktime+=path[i].length/speed
			#~ while self.checkcorrect(runner,tracktime)<0:
				#~ self.wait()
			#~ tracktime=runner.gettime()
			#~ self.updatespeed(tracktime,prevtime,path[i].length)		
			#~ prevtime=runner.gettime()
			#~ 

		
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
	g=networkGraph()
	g.build_sectgraph(conn)
	probabTable.build(g,conn)
	
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

	#------------- Finding all paths in distance 150 ----------------
	#~ for spath in g.findallPaths((g.edges[eg])[0],eg,150):
		#~ for i in spath:
			#~ print i.splitId
		#~ print probabTable.computeProbab(conn,[spath])	
		#~ print "############################"	
	#~ -----------------------------------------------------------------	
	path = g.dfs(g.getNode(SRC), g.getNode(DEST))
		
	#~ for i in path:
		#~ print i.u
	runner = user(g)
	tracker = server(g)
	try:
		pass
		r=Thread(target=runner.run, args=([path])).start()
		# r.daemon=True
		t=Thread(target=tracker.track, args=([runner,path])).start()
		# t.daemon=True
	finally:
		# t.join()
		# r.join()
		pass
