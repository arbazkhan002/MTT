from networkGraph import *
from threading import Thread
from time import sleep
import probabTable
import pickle
import random
import logger
import Queue
#~ SRC='0101000020847F0000704DF34E47D0194118485024FD5F4641'
#~ DEST='0101000020847F0000B0627FD91ED019411851DABB05604641'
SRC='0101000020847F0000704DF34E47D0194118485024FD5F4641'
DEST='0101000020847F00008CDD071EC5DF1941C8D53D59AA5F4641'
CLIENT_WAIT_TIME=0.05
SERVER_WAIT_TIME=0.005

LOG=logger.logger("logfile.txt")
rfile=open("rfile.txt","w")
sfile=open("sfile.txt","w")
conn = connect("dbname=demo user=postgres host=localhost password=indian")
sys_debug=1

class user:
	time=0
	currpt=None
	prevpt=None
	path=None
	speed=5.0
	Pd=0.5
	visited=[]
	path=[]
	pathind=0
	alive=1
	# just extra.. redundant information.. needed for debugging
	visitedE=[]

	def __init__(self,graph):
		self.g=graph
		self.time=0

	def makemove(self,nextpt,edgewt):
		global POS
		#~ print "edgewt:",edgewt,
		#~ print "time:",self.gettime()
		for i in range(int(edgewt/float(self.speed))):
			sleep(CLIENT_WAIT_TIME)
			self.time+=1
			#~ if self.pathind==0:
				#~ try:
					#~ sect = queue.get(False)
					#~ #check if sect is in visited
					#~ print "Runner: Yes!"
					#~ ans.put(1)
					#~ queue.task_done()
				#~ except Queue.Empty:
					#~ pass
				#~ continue	

			self.listen()	

		if int(edgewt/float(self.speed))==0:
			self.listen()
		#~ print "edgewt:",edgewt,
		#~ print "time:",self.gettime()
		self.time+=edgewt/float(self.speed)-int(edgewt/float(self.speed))
		self.prevpt=self.currpt	
		self.currpt=nextpt
		#~ print "Expecting a question"
		
	def listen(self):
		try:
			sect = queue.get(True,SERVER_WAIT_TIME)
			#~ self.visited.sort()

			#check if sect is in visited
			if sect not in self.visited:
				#~ rfile.write(repr((sect, self.visited)))
				while sect not in self.visited and sect!=None and sect!="proceed":
					ans.put(0)
					queue.task_done()
					sectp=sect
					sect=queue.get(True)		
					if sect!="proceed":	
						print "Runner: "," No!" ,"(",sectp,")"

				if sect=="proceed":
					#~ print sect, "Proceeded"		
					queue.task_done()	
					return

				else:
					if sect!=None:
						if sys_debug==1:
							print "#######################################",map(lambda x:x.splitId, self.visitedE)
							print "#######################################",self.visited,sect					
						
						print "Runner: ","Yes!","(",sect,")"
					ans.put(1)
					queue.task_done()
					path=queue.get(True)
					if path is not None:
						self.path=path 
						self.pathind=-1 #(to null the increment after self.makemove)
						self.visited=[]	# Old visited edgeIds are no longer required. They pose problems in answers to queries for reorientation.
					queue.task_done()
					return
			
			if sect in self.visited:
				if sys_debug==1:
					print "#######################################",map(lambda x:x.splitId, self.visitedE)
					print "#######################################",self.visited,sect
				print "Runner: Yes!"
				ans.put(1)
			
			queue.task_done()
				
		except Queue.Empty:
			if sys_debug==1:
				print "No questions incoming"
			pass				

	
	def position(self):
		return self.currpt	
	
	def gettime(self):
		return self.time		
	
	#To walk in a random fashion (pick random edges at each decision point)
	def explore(self, start, edge):
		print "<--- runner(e) '%s' @'%s after %s time units' --->" %(self.position().nodeid,edge.splitId,self.time)		 		
		#If the path is set, break explore mode			
		if self.path is not None:											
			print "Runner: Reached Destination"
			self.alive=0
			return
		if start==self.g.getNode(DEST):
			print "Runner: Reached Destination"
			self.alive=0
			return	

		for edgeuv in random.sample(self.g.adj(start),len(self.g.adj(start))):
			v=edgeuv.v #if edgeuv.v!=start else edgeuv.u			

			# when dead ends (deg<=1) or start points (prevpt is None) 
			if v!=self.prevpt or len(self.g.adj(start))<=1 or self.prevpt==None:
				#~ print v==self.prevpt, edge==edgeuv, edgeuv.splitId
				self.makemove(v,edgeuv.length)
				self.visited.append(edgeuv.edgeId)
				self.visitedE.append(edgeuv)

				if self.path is None:
					return self.explore(v, edgeuv)
				else:
					if sys_debug==1:
						print "<--- runner reoriented @ ",edgeuv.edgeId,"--->"
					break

		if self.path is not None:
			return self.run()		
		else:
			print "Assertion ERROR ",len(self.g.adj(start)),self.g.adj(start)[0].splitId
	
	# To follow a path
	def run(self):
		path=self.path
		
		# To tackle disorientation
		newpath=None
		#Take complement of u
		self.currpt=self.g.coedgeint(path[1],path[0])
		u=self.g.edgeint(path[1],path[0])
		self.makemove(u,path[0].length)
		#~ try:
			#~ sect = queue.get(False)
			#~ #check if sect is in visited
			#~ x=self.gettime()
			#~ ans.put(x)
			#~ queue.task_done()
		#~ except Queue.Empty:
			#~ pass		
		#~ temp=self.currpt
		#~ print "first check"
		update=[] #Stores all traversed paths 
				  #A traversed path is of the form [Edgeprev, Edgenext,Inpath] to update probability tables
				  #Idea is to update probability table for each edge edgeprev such that the record1 <edgeprev,edgenext,inpath>
				  #gets 1% probability of every record2 of type <edgeprev,_,(!inpath)> (except record1)
				  # for all record2, probab=0.99probab, sum+=0.01probab
				  # for record1, probab+=sum   (so that the net probab is 1 always)
		#~ print len(path)  #-- 196
		self.pathind=1
		i=self.pathind
		self.visited.append(path[0].edgeId)
		self.visitedE.append(path[0])
		while i<len(path):
			#~ print i,"th part"
			i=self.pathind
			if random.random()>self.Pd or len(self.g.adj(path[i].u))<=2:	
				update.append([path[i-1].edgeId,path[i].edgeId,int(True)])
				self.makemove(self.g.coedgeint(path[i-1],path[i]),path[i].length)
				#only after move is made, mark visited.. else for long edges, you would give a "yes" before even completing it.
				self.visited.append(path[i].edgeId)
				self.visitedE.append(path[i])
				#~ print self.visited
				#print path[i].u
				print "<--- runner '%s' @'%s after %s time units' --->" %(self.position().nodeid,path[i].splitId,self.time)		 

			else:
				#dist = self.g.linearDistance(temp,self.currpt,path)
				#print dist,temp==self.currpt	
				print "Diverting: ",path[i].splitId
				update.append([path[i-1].edgeId,path[i].edgeId,int(False)])
				self.path=None
				break
			self.pathind+=1
			i=self.pathind	

		LOG.write(update)				
		
		return self.explore(self.currpt, path[i-1])	
	pass

lock=1

class server:
	time=0
	def __init__(self,graph):
		self.g=graph
		self.time=0


	# Make sure to call ans.task_done after calling wait()		
	def wait(self,t):
		try:
			sleep(t)
			reply=ans.get(False)
			return reply
		except Queue.Empty:	
			return -1
	
	def checkcorrect(self,runner,ttime):
		return runner.gettime()-ttime
		

	def track(self,runner,path):
		prev=None
		prevtime=0
		tracktime=0
		nextpath=[]
		speed=5
		if sys_debug==1:
			print "<--- Tracking runner..... --->"
		while True:
			dist=0
			speed=self.initSpeed()
			if sys_debug==1:
				print "Reinitializing everythin"
			i=0
			factor=1.0
			while i<len(path):
				dist+=path[i].length
								
				if len(g.edges[path[i].u])<=2 and i!=0:
					i+=1
					continue	

				if i>=1:
					nextpath=self.g.findPathEdges(self.g.edgeint(path[i-1],path[i]),path[i-1].length)
				
				speed=self.estimateSpeed()
				print i, " of ",len(path) ," completed"					
				print "Tracker: Prompt me 'Yes' when you see section ",path[i].splitId,"." "(",dist,speed,tracktime,")"

				tracktime=runner.gettime()			
				
				reply=0
				while speed!=0 and tracktime<prevtime+float(dist)*factor/speed and reply!=1:
					if runner.alive==0:
						print "Client dead"
						return
					
					# If below condition is not put then queue floods up due to unreplied queries
					if reply==0:
						queue.put(path[i].edgeId)
					reply=self.wait(SERVER_WAIT_TIME)
					#~ print "Received ",reply, queue.qsize()									
					tracktime=runner.gettime()
					
					# If the reply is negative, instruct to proceed and not wait for any questions
					if reply==0:
						ans.task_done()				# this is for calling self.wait()
						queue.put("proceed")
					#~ print tracktime
					#~ with queue.mutex:
						#~ queue.queue.clear()
					continue

				#~ print "qsize:",queue.qsize()
				# Suppose self.wait times out (reply=-1) and in the next iteration condition (tracktime<prevtime+..) fails
				# then queue top is an edgeId
				# If self.wait doesn't time out and reply is 0 and in the next iteration (tracktime<prevtime) fails
				# then queue top is "proceed"	
				if reply==-1:
					queue.queue.clear()
			
				#Below case should not be else if. As reply==-1 case need to be done the same as the case of reply==0
				if reply!=1:
					print "Tracker: Did you see section ",path[i].splitId,"?" "(",dist,speed,tracktime,")"

					tracktime=runner.gettime()			
					queue.put(path[i].edgeId)
					try:
						reply=ans.get(True, 1)
						
					except Queue.Empty:
						print "Client dead"
						return
					
				#reinitialize dist for next iteration
				#~ print reply
					# next path possesses a a list of paths (i.e. list of list of edgeIds)
					# Each path is stored in reverse order of travel (last edgeId is visited first)
					#~ print "*********",map(lambda x: map(lambda y:y.edgeId, x), nextpath), path[i].edgeId
				#~ sfile.write(repr((map(lambda x: map(lambda y:y.edgeId, x), nextpath), path[i].edgeId)))
				#~ print map(lambda x: map(lambda y:y.edgeId, x), nextpath), path[i].edgeId
				#~ sfile.close()
				# Get the landmarks on each path
				# filter zeroes from self.g.getLandmarks(conn, nextpath[i])
				
				if reply==0:
					j=0
					if sys_debug==1:
						print "<--- runner off track! --->" 
					while reply==0:
						if j<len(nextpath):
							print "Tracker: Did you see section ",nextpath[j][-1].splitId,"?"
							queue.put(nextpath[j][-1].edgeId)
						else:
							# Put none in the queue to signal that no path change is required as its the case, user's position is behind the tracker
							queue.put(None)
						ans.task_done()
						try:
							reply=ans.get(True, 1)
						except Queue.Empty:
							print "Client dead"	
							return
						j+=1
						
					if reply==1 and j<=len(nextpath):	
						path=self.g.djikstra(nextpath[j-1][-1].v,g.getNode(DEST))					
						#~ print path,'\n',self.g.djikstra(nextpath[j-1][-1].v,g.getNode(DEST))					
						#~ sfile.write(repr(path[i-1].splitId)+repr(map(lambda x:x.splitId, path)))
						queue.put(path)
						if sys_debug==1:
							print "<--- tracker conveyed new path to the runner --->"
						prevtime=tracktime
						break
					
					#all possible paths rejected.. fall back
					if j>len(nextpath):
						print "reply was ",reply
						queue.put(None)
						#~ ans.task_done()
						#we would come back to same track segment but assume 1-factor fraction is covered												
						dist-=path[i].length
						factor=0.5
						prevtime=tracktime
						continue
						#~ assert(False)
				
				if reply==1:
					factor=1.0
					speed=dist/(tracktime-prevtime)
					if sys_debug==1:
						print "<--- runner on track! with speed @", speed, "--->", "(",dist, tracktime,prevtime,")"
					prevtime=tracktime
				
				ans.task_done()
				dist=0
				i+=1

			#~ print "at the end: ",i+1	
			if i==len(path)-1:
				print "End tracking"
				return				
	
	def updatespeed(self,t1,t2,d):
		return d/(t1-t2)		
	
	def initSpeed(self):
		return 5.0

	def estimateSpeed(self):
		return 5.0
		

	def qtrack(self,runner,path):
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
		speed = dist / (response1-response0) if dist is not None else None
		sections={}

		for ind,i in enumerate(path):
			sections[i]=ind
		landmarks=[0 for i in range(len(path))]	 # ref_ids of landmark at each section
												 # landmark corresponding to section path[i] is landmarks[i]
												 # 0 indicates no landmark nearby to that section
												 
		seen = [] #list of landmarks already seen
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
	path = g.djikstra(g.getNode(SRC), g.getNode(DEST))
	#~ print map(lambda x: x.edgeId, g.djikstra(g.getNode(SRC), g.getNode(DEST)))
	queue= Queue.Queue()	
	ans = Queue.Queue()	
	#~ for i in path:
		#~ print i.u
	runner = user(g)
	tracker = server(g)
	try:
		pass
		runner.path=path
		r=Thread(target=runner.run, args=()).start()
		# r.daemon=True
		t=Thread(target=tracker.track, args=([runner,path])).start()
		# t.daemon=True
		queue.join()
		ans.join()
	finally:
		# t.join()
		# r.join()
		queue.join()
		ans.join()
		pass

	
	#~ def makemoveS(self,nextpt,edgewt):
		#~ global POS
		#~ sleep(0.05)
		#~ print "edgewt:",edgewt,
		#~ print "time:",self.gettime()
		#~ self.time+=edgewt/float(self.speed)
		#~ self.prevpt=self.currpt	
		#~ self.currpt=nextpt
		#~ # print "Expecting a question"
		#~ if self.pathind==0:
			#~ try:
				#~ sect = queue.get(False)
				#~ #check if sect is in visited
				#~ print "Runner: Yes!"
				#~ ans.put(1)
				#~ queue.task_done()
			#~ except Queue.Empty:
				#~ pass
			#~ return	
		#~ try:
			#~ sect = queue.get(False)
			#~ # self.visited.sort()
			#~ print "#######################################",self.visited,sect
			#~ #check if sect is in visited
			#~ if sect not in self.visited:
				#~ rfile.write(repr((sect, self.visited)))
				#~ while sect not in self.visited:
					#~ print "Runner: "," No!"
					#~ ans.put(0)
					#~ queue.task_done()
					#~ sect=queue.get(True)
				#~ 
				#~ print "Runner: ","Yes!"
				#~ ans.put(1)
				#~ queue.task_done()
				#~ self.path=queue.get(True)
				#~ self.pathind=-1 #(to null the increment after self.makemove)
				#~ queue.task_done()
				#~ return	
			#~ 
			#~ if sect in self.visited:
				#~ print "Runner: Yes!"
				#~ ans.put(1)
			#~ 
			#~ queue.task_done()
				#~ 
		#~ except Queue.Empty:
			#~ if sys_debug==1:
				#~ print "No questions incoming"
			#~ pass					
		#~ 	
