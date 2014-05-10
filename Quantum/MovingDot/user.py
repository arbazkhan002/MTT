from networkGraph import *
from threading import Thread
from time import sleep
import probabTable
import pickle
import random
import logger
import Queue
import pdb
import os.path
import attmodifier

SRC='0101000020847F0000704DF34E47D0194118485024FD5F4641'
DEST='0101000020847F00008CDD071EC5DF1941C8D53D59AA5F4641'
CLIENT_WAIT_TIME=0.05
SERVER_WAIT_TIME=0.005
TOPRINT=1		#whether to log(print the results to result file)
THRESHHOLD=1	#This is the factor threshhold, which indicates how many iterations do we make before, we instead of probing 
				# ask the user to interrupt when the intersection is crossed 
				#For example, if threshhold is 1, only once we ask the question did you cross the intersection? thereafter we wait for him endlessly
FORGETDIST=100	# if the distance gap between any element is farther than FORGETDIST from current position, forget it			
OVERSHOOTFACTOR=1.5 # it indicates how much more than expected, can a driver overshoot by. If its 2.5, then he may be found at 2.5*dist while we are
					# expecting him at dist
LOG=logger.logger("logfile.txt")
TOLOGHSPEED=1
rfile=open("rfile.txt","w")
sfile=open("sfile.txt","w")
hspeedfile="hspeed.pkl"
hspeed={}		#hspeed[x]=(average speed, number of entries averaged upon)	
conn = connect("dbname=demo user=postgres host=localhost password=indian")
sys_debug=1
debugger=0


class user:
	time=0
	currpt=None
	prevpt=None
	path=None
	speed=5.0
	Pd=0.33
	visited=[]
	path=[]
	pathind=0
	alive=1
	modifier=None
	remembers=[] #a 2d array of distance stamps of each visited section, e.g, [[123,0],[124,4.5123],[125,10.34432],...]
	# just extra.. redundant information.. needed for debugging
	visitedE=[]

	def __init__(self,graph,conn):
		self.g=graph
		self.time=0
		self.modifier=attmodifier.modifier(conn)

	# simulates forgetting. If state is True, everything is cleared from memory
	def forget(self, state=True):
		if state==False:
			del self.remembers[:]
			return
			
		if not self.remembers:
			return
		else:	
			#~ print "\tBEFORE: ",self.remembers
			# if the distance gap between any element is farther than FORGETDIST from current position, forget it
			#~ self.remembers=filter(lambda x:self.remembers[-1][1]-x[1]<FORGETDIST, self.remembers)	


			#store the edge of previous visited sectId so that question on CI is answered 
			prevedge=None
			for i in range(0,len(self.remembers),-1):
				edgetuple=self.remembers[i]
				if edgetuple[0].sectId!=self.remembers[-1][0].sectId:
					prevedge=edgetuple
					break
					
			# only those edges which have the same sectId are retained
			self.remembers=filter(lambda x:self.remembers[-1][0].sectId==x[0].sectId, self.remembers)	
			if prevedge!=None:
				self.remembers.insert(0,prevedge)			
			#~ print "\tAFTER: ",map(lambda x:x[0].sectId, self.remembers)

	def makemove(self,nextpt,edge):
		global POS
		edgewt=edge.length
		#~ print "edgewt:",edgewt,
		#~ print "time:",self.gettime()
		#~ self.visited.append(edge.edgeId)
		#~ self.visitedE.append(edge)
		#~ self.remembers.append()
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

			if self.listen()==1:
				self.forget(False)
				return	

		if int(edgewt/float(self.speed))==0:
			self.listen()
		#~ print "edgewt:",edgewt,
		#~ print "time:",self.gettime()
		self.time+=edgewt/float(self.speed)-int(edgewt/float(self.speed))
		self.prevpt=self.currpt	
		self.currpt=nextpt
		#~ print "#######################################",map(lambda x:x[0].splitId, self.remembers)
		self.forget()
		#~ print "################ FORGOT ###############",map(lambda x:x[0].splitId, self.remembers)
		#~ print "#######################################",map(lambda x:x[0].edgeId, self.remembers)		
		#~ print "Expecting a question"
		
	def listen(self):
		try:
			sect = queue.get(True,SERVER_WAIT_TIME)						
			#~ self.visited.sort()
			if sect=="reactive":
				self.react()
				
			#check if sect is in visited
			else:
				self.remembersE=map(lambda x:x[0].edgeId, self.remembers)
				if sect not in self.remembersE:
					#~ rfile.write(repr((sect, self.visited)))
					while sect not in self.remembersE and sect!=None and sect!="proceed":
						if str(sect).startswith("CI"):
							if int(sect[2:]) in self.visited:
								break
						ans.put(0)
						queue.task_done()
						sectp=sect
						#~ print "#######################################",map(lambda x:x[0].splitId, self.remembers)
						#~ print "#######################################",map(lambda x:x[0].edgeId, self.remembers)						
						sect=queue.get(True)		
						if sect!="proceed":	
							print "Runner: "," No!" ,"(",sectp,")"

					if sect=="proceed":
						#~ print sect, "Proceeded"		
						queue.task_done()	
						return 0

					else:
						if sect!=None:			# print "Yes" for the case when sect in self.visited
							print "Runner: ","Yes!","(",sect,")"
							if sys_debug==1:
								#~ print "#######################################",map(lambda x:x.splitId, self.visitedE)
								#~ print "#######################################",self.visited,sect					
								pass
						
						print "runner asked on ",sect		
						ans.put(1)
						queue.task_done()
						path=queue.get(True)
						if path is not None:
							print "runner path to be changed ",sect		
							self.path=path 
							self.pathind=-1 #(to null the increment after self.makemove)
							self.visited=[]	# Old visited edgeIds are no longer required. They pose problems in answers to queries for reorientation.
							queue.task_done()
							return 1
						queue.task_done()
						return 0
							
				
				if sect in self.remembersE:
					if sys_debug==1:
						#~ print "#######################################",map(lambda x:x[0].splitId, self.remembers)
						#~ print "#######################################",map(lambda x:x[0].edgeId, self.remembers)
						#~ print "#######################################",map(lambda x:x.splitId, self.visitedE)
						#~ print "#######################################",self.visited,sect
						pass
					print "Runner: Yes!","(",sect,")"
					ans.put(1)
				
			queue.task_done()
			return 0
				
		except Queue.Empty:
			if sys_debug==1:
				print "No questions incoming"
			return 0
							

	
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
				self.makemove(v,edgeuv)
				self.visited.append(edgeuv.edgeId)
				self.visitedE.append(edgeuv)
				if not self.remembers:
					totaldist=0
				else:
					totaldist=self.remembers[-1][1]
				self.remembers.append([edgeuv,edgeuv.length+totaldist])
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
		if debugger==1:	
			pdb.set_trace()
		print "<--- path ahead (glimpse)-- ", map(lambda x:x.splitId, self.path[:10 if 10<len(path) else len(path)-1])
		# To tackle disorientation
		newpath=None
		#Take complement of u
		self.currpt=self.g.coedgeint(path[1],path[0])
		u=self.g.edgeint(path[1],path[0])
		self.makemove(u,path[0])
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
		self.remembers.append([path[0],path[0].length])
		while i<len(path):
			#~ print i,"th part"
			i=self.pathind				
			if random.random()>self.Pd or len(self.g.adj(path[i].u))<=2:	
				update.append([path[i-1].edgeId,path[i].edgeId,int(True)])
				self.makemove(self.g.coedgeint(path[i-1],path[i]),path[i])
				#only after move is made, mark visited.. else for long edges, you would give a "yes" before even completing it.
				self.visited.append(path[i].edgeId)
				self.visitedE.append(path[i])
				if not self.remembers:
					totaldist=0
				else:	
					totaldist=self.remembers[-1][1]
				self.remembers.append([path[i], path[i].length+totaldist])
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
	
	def react(self):
		pass



lock=1
