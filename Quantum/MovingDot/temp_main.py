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
import math
#~ SRC='0101000020847F0000704DF34E47D0194118485024FD5F4641'
#~ DEST='0101000020847F0000B0627FD91ED019411851DABB05604641'
SRC='0101000020847F0000704DF34E47D0194118485024FD5F4641'
DEST='0101000020847F00008CDD071EC5DF1941C8D53D59AA5F4641'
CLIENT_WAIT_TIME=0.05
SERVER_WAIT_TIME=0.005
TOPRINT=1		#whether to log(print the results to result file)
THRESHHOLD=0.5	#This is the factor threshhold, which indicates how many iterations do we make before, we instead of probing 
				# ask the user to interrupt when the intersection is crossed 
				#For example, if threshhold is 1, only once we ask the question did you cross the intersection? thereafter we wait for him endlessly
FORGETDIST=100	# if the distance gap between any element is farther than FORGETDIST from current position, forget it			
ERRORFACTOR=1.5 # it indicates how much more than expected, can a driver overshoot by. If its 2.5, then he may be found at 2.5*dist while we are
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
	speed=25.0
	Pd=0.33
	visited=[]
	path=[]
	pathind=0
	alive=1
	modifier=None
	pos=None
	remembers=[] #a 2d array of distance stamps of each visited section, e.g, [[123,0],[124,4.5123],[125,10.34432],...]
	# just extra.. redundant information.. needed for debugging
	visitedE=[]

	def __init__(self,graph):
		self.g=graph
		self.time=0
		self.modifier=attmodifier.modifier(conn)
		self.categoricalSpeed=random.lognormvariate(2.7,0.5)

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
		self.pos=edge
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

			l=self.listen()
			if l==1:
				self.forget(False)
				return	
				
			if l==-1:
				raise Exception
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
				reply=self.react()
				if reply==1:	
					path=queue.get(True)
					print "Path: ", path if path is None else type(path)
					if path is not None:
						self.path=path 
						self.pathind=-1 #(to null the increment after self.makemove)
						self.visited=[]	# Old visited edgeIds are no longer required. They pose problems in answers to queries for reorientation.
						queue.task_done()
						return 1
					queue.task_done()
					return -1
				elif reply==0:
					return -1
				else:
					return 0		
				
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
						print "Runner: Asked ",sect,							
						ans.put(1)
						queue.task_done()
						path=queue.get(True)
						print "Path: ", path if path is None else type(path)
						if path is not None:
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
				if len(self.g.adj(path[i].u))>2:
					self.speed=self.categoricalSpeed+random(0,self.categoricalSpeed/10)
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
		print "================= RUNNER: REACT MODE ",self.pos.sectId," ",self.pos.splitId," ========================"
		allLandmarks=self.g.getLandmarks(conn,self.pos.sectId)
		print allLandmarks
		#~ if not allLandmarks:
		allLandmarks=list(set(reduce(lambda x,y:x+y,allLandmarks.values())))
		mat=self.modifier.getAttr(allLandmarks)
		print mat
		
		try:
			sect=queue.get(True)
			while sect!="proceed" and sect!="reorient":
				print "Runner: Reacting to :",sect
				atuple=map(lambda x:int(x),sect.split(":"))
				if not filter(lambda x:mat[x][atuple[0]]==atuple[1],mat):
					reply=0
				else:
					reply=1
				ans.put(reply)
				queue.task_done()	
				sect=queue.get(True)
			print "==============================================================="				
			if sect=="proceed":
				queue.task_done()
				return -1
			else:
				sect=queue.get(True)
				print "Runner: REORIENT message--> ",sect,None if not self.pos else self.pos.sectId
				if sect==self.pos.sectId:
					ans.put(1)
					return 1
				else:
					ans.put(0)
					return -1	
				queue.task_done()
					

		except Queue.Empty:
			if sys_debug==1:
				print "Empty Queue"
			print "==============================================================="
		#~ for lm in mat:
			#~ if mat[sect[0]]==sect[1]:
				#~ #respond Yes
		#~ '''
		pass



lock=1

class server:
	time=0
	mistakes=0		#G related
	prompts=0		#G related
	prfactor=0
	modifier=None	
	uspeed_avg=15
	uspeed_n=1
	uspeed_dev=0
	decisions=[]		#G related
	questions=0
	def __init__(self,graph):
		self.g=graph
		self.modifier=attmodifier.modifier(conn)

	# Make sure to call ans.task_done after calling wait()		
	def wait(self,t):
		try:
			sleep(t)
			reply=ans.get(False)
			return reply
		except Queue.Empty:	
			return -1

	def reactive(self,allLandmarks):
		def bestValue(X,i):				#returns v if entropy of the value v is maximum in ith attribute of X
			size=len(X)	
			attDict={}		#storing the frequencies of each attribute value attDict=[{1: 25, 2:15, 3:10}, {1: 5, 2:10, 3:15}, ...]
			
			#calculate frequencies
			values=map(lambda x:x[i],X)			#values of attribute ai
			print "value array:",values,X
			
			for j in values:
				if j not in attDict:
					attDict[j]=0.0
				attDict[j]+=1
				
			maxentropy=None
			maxvalue=0

			for v in values:
				entropyvalue=0
				ec=attDict[v]/size
				entropyvalue-=0 if not ec else ec*(math.log(ec,2))
				print "value ",v,"-",ec,":",0 if not ec else ec*(math.log(ec,2))

				ec=(sum(attDict.values())-attDict[v])/size
				entropyvalue-=0 if not ec else ec*(math.log(ec,2))
				print "rest:",0 if not ec else ec*(math.log(ec,2))
				
				if maxentropy==None or maxentropy<entropyvalue:
					maxentropy=entropyvalue
					maxvalue=v
						
			return maxvalue,maxentropy

		def entropy(X,i):				#entropy of the ith attribute
			size=len(X)	
			attDict={}		#storing the frequencies of each attribute value attDict=[{1: 25, 2:15, 3:10}, {1: 5, 2:10, 3:15}, ...]
			
			#calculate frequencies
			values=map(lambda x:x[i],X)			#values of attribute ai
			
			for j in values:
				if j not in attDict:
					attDict[j]=0.0
				attDict[j]+=1
				
			entropyvalue=0

			for j in attDict:
				ec=attDict[j]/size
				entropyvalue-=0 if not ec else ec*(math.log(ec,2))

			
			return entropyvalue	
				
		def findbestattribute(X,asked):
			maxentropy=None	
			index=0			
			for i in range(len(X[0])):
				if i not in asked:			
					entropyi=entropy(X,i)
					if maxentropy==None or maxentropy<entropyi:
						maxentropy=entropyi
						index=i			
			return index		
								
		larray=list(set(reduce(lambda x,y:x+y,allLandmarks.values())))
		mat=self.modifier.getAttr(larray)
		queue.put("reactive")	
		asked=[]
		#keep questioning on attributes till there is only possible section left	
		while len(allLandmarks)>1:
			print mat
			X=mat.values()							#mat={125:[1,2,1], 131:[2,2,3], ..}
			if not X:
				print "Tracker: NO LANDMARKS (Move forward)",questions
				queue.put("proceed")
				return -1,self.questions	

			entropyvalue=0
			while entropyvalue==0:
				attindex=findbestattribute(X,asked)				
				value,entropyvalue=bestValue(X,attindex)
				if entropyvalue==0:
					asked.append(attindex)
				print "attindex, value, entropy,asked ",attindex, value, entropyvalue, asked 	
				if len(asked)==len(X[0]):
					break
			
			if len(asked)==len(X[0]):
				print "Tracker: EXHAUSTED ATTRIBUTE SET (Move forward)",self.questions
				queue.put("proceed")
				return -1,self.questions		

			queue.put(str(attindex)+":"+str(value))
			self.questions+=1
			atuple=(attindex,value)
			reply=ans.get(True)
			
			if reply==1:
				mat_left=filter(lambda x:mat[x][atuple[0]]==atuple[1],mat)
			else:
				mat_left=filter(lambda x:mat[x][atuple[0]]!=atuple[1],mat)
			
			mat_new={}
			
			for key in mat_left:
				mat_new[key]=mat[key]

			# check if mat is pruned
			if mat!=mat_new:
				mat=mat_new
				print "Tracker:",mat
				# prune	allLandmarks based on the new mat
				# keep all those edges from allLandmarks which contain atleast one landmark from mat
				mark=[]
				for sectid,lm in allLandmarks.iteritems():
					if not list(set(lm).intersection(set(mat.keys()))):
						mark.append(sectid)
				
				map(lambda x:(allLandmarks.pop(x,None)),mark)	
				ans.task_done()	
			
			else:
				queue.put("proceed")
				return -1,self.questions
						
		queue.put("reorient")
		queue.put(allLandmarks.keys()[0])			#this is equivalent of asking the orientation of the user wrt to the landmark
		self.questions+=1
		reply=ans.get(True)
		if reply==1:
			print "NARROWED DOWN:",allLandmarks
			self.mistakes+=1
			ans.task_done()
			return allLandmarks.keys()[0],self.questions		
		else:
			print "ASKING TO MOVE FORWARD",self.questions
			ans.task_done()
			return -1,self.questions	#can't narrow down, ask him to move forward
		'''
		#Prune landmarks by asking attribute values
		
		queue.put((i,med[i]))
		
		reply=ans.get(True,1)
		'''
		pass

			
	def reorder(self,path,dist,speed,curredge,prevedge):
		#~ return path
		# HOW IT WAS BEFORE CHANGE1.0
		#~ return sorted(path,key=lambda x:abs((x[0]-dist)/dist-self.prfactor))
		
		# From one splitId, pick exactly one entry (which is closest to source s)
		#~ '''
		sortedlist=sorted(path,key=lambda x:abs(x[0]-dist))
		seen=[curredge.sectId, prevedge.sectId] 	#no questions should be asked from the current sectId and prev sectId
		returnlist=[]
		for entry in sortedlist:
			if entry[1].sectId in seen:
				continue
			else:
				if entry[0]<=ERRORFACTOR*dist and entry[0]>=dist/ERRORFACTOR:
					returnlist.append(entry)
					seen.append(entry[1].sectId)			
		return returnlist
		'''
		return path	
		'''
		
	def getprfact(self,x,dist):
		return 1 #(x-dist)/dist
			
	def track(self,runner,path):
		prev=None
		prevtime=0
		checkpttime=0		#time of visit of last checkpoint
		self.time=0
		speed=5
		self.etime=reduce(lambda x,y:x+y,map(lambda x:x.length,path),0)/speed 
		if sys_debug==1:
			print "<--- Tracking runner..... --->"
		while True:
			if debugger==1:
				pdb.set_trace()
			if sys_debug==1:
				print "Reinitializing everythin"
			dist=0
			speed=self.initSpeed()
			i=0
			factor=1.0
			filteredSect=[]			#takes care of bombarding the prompts for errors at short lengthed sections
			nextpath=[]			
			newWaitDist=0			#for disorientation			
			crossedIntersection=0			#reset the variable			
			askedIntersection=0			#do not ask the intersection crossed(?) question again			
			flagIntersection=0			#do not set crossedIntersection more than once
			CIdist=0					#distance till previous intersection
			while i<len(path):
				if not filteredSect:			#non zero only when the edges in question differ greatly in size (ie. there is a short lengthed section)
					dist+=path[i].length
					filteredSect.append(path[i].sectId)
					newWaitDist=0			#initialized newWaitDist
				
				self.time=runner.gettime()							
				if len(g.edges[path[i].u])<=2 and i!=0:
					print "skip:",path[i].splitId
					i+=1
					filteredSect=[]
					continue

				index=i
				CIdist=0
				for index in range(i-1,-1,-1):
					if len(g.edges[path[index].u])>2:
						break	
					CIdist+=path[index].length
					
				
				self.decisions.append(path[i].u)	# a new decision to be made (if duplicate, it would sorted out when we convert list to a set
				speed=self.estimateSpeed()

				if i>=1:
					#~ nextpath=self.g.findPathEdges(self.g.edgeint(path[i-1],path[i]),OVERSHOOTFACTOR*path[i-1].length)					
					nextpath=self.g.findPathEdges(self.g.edgeint(path[i-1],path[i]),(self.time-checkpttime)*speed-CIdist)
					unordered=nextpath
					nextpath=self.reorder(nextpath,(self.time-checkpttime)*speed-CIdist,speed,path[i],path[i-1])
					
				print "=================================", i, " of ",len(path) ," completed",CIdist,path[i].length,"=================================================="
				self.prompt(" ".join(map(str,["Tracker: Prompt me 'Yes' when you see section ",path[i].splitId,"." "(",dist,speed,self.time,prevtime,")"])))
				
				reply=0

				#if factor gets less than threshhold, it waits indefinitely (if the intersection is not crossed) as the below condition is never violated
				#also if there are not yet any alternate paths possible, keep waiting till there is one
				while speed!=0 and (self.time<prevtime+(float(dist)*factor)/speed or (crossedIntersection==0 and factor<THRESHHOLD) or len(nextpath)==0) and reply!=1:
					if runner.alive==0:
						self.printStats()
						print "Client dead"
						return
					
					if (self.time<prevtime+(float(dist)*factor)/speed):
						condition=1
					elif len(nextpath)==0:
						condition=2
					else:
						condition=3		
					
					#when factor falls below threshhold, wait indefinitely
					if factor<THRESHHOLD and i>0 and crossedIntersection==0:
						#ask for intersection
						toqueue="CI"+str(path[i-1].edgeId)	
					else:
						toqueue=path[i].edgeId
					
					# If below condition is not put then queue floods up due to unreplied queries
					if reply==0:
						queue.put(toqueue)
					reply=self.wait(SERVER_WAIT_TIME)
					
					# If the reply is negative, instruct to proceed and not wait for any questions
					if reply==0:
						ans.task_done()				# this is for calling self.wait()
						queue.put("proceed")
					elif reply==1 and factor<THRESHHOLD:		#factor<threshhold means we were waiting for CI			
						crossedIntersection=1
						queue.put(None)							#need to do it
						i-=1									#since reply=1, index i to path would increment but it should not as path[i] is not crossed
					
					self.time=runner.gettime()
					
					#recalculate next path possibilities	
					if i>=1:
						#~ nextpath=self.g.findPathEdges(self.g.edgeint(path[i-1],path[i]),OVERSHOOTFACTOR*path[i-1].length)					
						nextpath=self.g.findPathEdges(self.g.edgeint(path[i-1],path[i]),(self.time-checkpttime)*speed-CIdist)
						unordered=nextpath
						nextpath=self.reorder(nextpath,(self.time-checkpttime)*speed-CIdist,speed,path[i],path[i-1])
						#~ print "UNORDERED ON ",(self.time-checkpttime)*speed,":",map(lambda x:[x[0],x[1].splitId],unordered)	
					continue
				
				print "condition:",condition
				if i>=1:
					print "FROM NETWORK GRAPH: ",map(lambda x:[x[0],x[1].splitId],unordered)
					print "REORDERED ON ",(self.time-checkpttime)*speed-CIdist,":",map(lambda x:[x[0],x[1].splitId],nextpath)

				# Suppose self.wait times out (reply=-1) and in the next iteration condition (self.time<prevtime+..) fails
				# then queue top is an edgeId
				# If self.wait doesn't time out and reply is 0 and in the next iteration (self.time<prevtime) fails
				# then queue top is "proceed"	
				if reply==-1:
					queue.queue.clear()
			
				#Below case should not be else if. As reply==-1 case need to be done the same as the case of reply==0
				if reply!=1:
					self.prompt(" ".join(map(str,["Tracker: Did you see section ",path[i].splitId,"?" "(",dist,speed,self.time,prevtime,")"])))

					self.time=runner.gettime()			
					queue.put(path[i].edgeId)
					try:
						reply=ans.get(True, 1)
						if reply==1 and crossedIntersection==1:
							dist=path[i].length			#as dist was changed to newWaitDist after CI, needs to be restored back
						
					except Queue.Empty:
						self.printStats()
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
						if crossedIntersection==1 and j<len(nextpath):
							self.prompt(" ".join(map(str,["Tracker: Did you see section ",nextpath[j][-1].splitId,"?" "(", \
								dist,speed,self.time,"$",self.prfactor,self.getprfact(nextpath[j][0],dist)," )"])))
							queue.put(nextpath[j][-1].edgeId)
						
						else: 	# need to ask first whether the intersection is crossed
							if (i>0) and askedIntersection==0:
								self.prompt(" ".join(map(str,["Tracker: (CI) Did you see section ",path[i-1].splitId,"?" "(",dist,speed,self.time,")"])))					
								queue.put("CI"+str(path[i-1].edgeId))
								askedIntersection=1
								flagIntersection=0

								
							else:		#when intersection is already asked for
								# Put none in the queue to signal that no path change is required as its the case, user's position is behind the tracker
								# the client replies 1 to a None signal
								queue.put(None)
								
						ans.task_done()
						try:
							reply=ans.get(True, 1)
							
							#if you have asked about the intersection and expecting a reply				
							if askedIntersection==1 and flagIntersection==0:
								crossedIntersection=reply
								flagIntersection=1
								continue
																
						except Queue.Empty:
							self.printStats()
							print "Client dead"	
							return
													
						j+=1
						if reply==1:
							break
						
					#if intersection was crossed but path disoriented then j>0 because j gets incremented before break
					#In deterministic case, reply would always be 1	
					if j<=len(nextpath) and j>0 and crossedIntersection==1:
						self.mistakes+=1
						filteredSect=[]
						self.recordPattern(" ".join(map(str,[nextpath[j-1][0],nextpath[j-1][1].splitId]))+" "+ " ".join(map(str, [speed, dist])))
						path=self.g.djikstra(nextpath[j-1][-1].v,g.getNode(DEST))					
						#~ print path,'\n',self.g.djikstra(nextpath[j-1][-1].v,g.getNode(DEST))					
						#~ sfile.write(repr(path[i-1].splitId)+repr(map(lambda x:x.splitId, path)))
						queue.put(path)
						if sys_debug==1:
							print "<--- tracker conveyed new path to the runner --->"
						prevtime=self.time
						checkpttime=self.time
						i=0		#so that control doesn't reach to tracking end after breaking
						break
					
					#all possible paths rejected.. intersection may have been crossed
					# reply can be 1 here due to a None signal on the queue 
					else:
						print "reply,factor,crossed: ",reply, factor, crossedIntersection
						
						#in the case wherer intersection was crossed, None needs to be put
						#Put a None to indicate no change in path						
						queue.put(None)
						
						#~ ans.task_done()
						#we would come back to same track segment but assume 1-factor fraction is covered												
							
						factor=factor*0.5
						
						#if intersection is crossed, wait on the new distance(longer)
						# example of this case : waiting for 3868 to be visited, user instead moves on 3741
						# another example : waiting for 4065, user moves to 3560						
						if len(nextpath)>0 and crossedIntersection==1:
							if newWaitDist==0:
								dist=path[i].length		#We have waited for path[i] units beyond the intersection
								newWaitDist=dist
							
							#~ currentsectEdges=filter(lambda x:x.sectId in filteredSect,nextpath)
							print						
							print "\t--------------------------- THE WAIT DISTANCE IS GETTING CHANGED ------------------------------------------------------"
							print 
							#~ restEdges=filter(lambda x:x[1].sectId not in filteredSect,nextpath)
							restEdges=[]
							# on the restEdges sorted by distance from the last checkpoint, pick up the distance of first index i.e. closest edge distance
							if not restEdges:	#all edges emanating from the cross section have been searched for	
								#-------------------------------------------------------------------------------#
								#Here, u enter the REACTIVE PHASE

								allLandmarks={}
								lookupEdge={}
								for pathentry in nextpath:
									pathi=pathentry[1]
									
									if pathi.sectId not in allLandmarks:
										allLandmarks[pathi.sectId]=[]
										lookupEdge[pathi.sectId]=pathi
										
									newLandmarks=self.g.getLandmarks(conn,pathi.sectId)
									for splitid in newLandmarks:
										for refid in newLandmarks[splitid]:
											if refid not in allLandmarks[pathi.sectId]:
												allLandmarks[pathi.sectId].append(refid) 
								
								print "\n\n\t\tIN REACTIVE PHASE\n\n"			
								status,questions=self.reactive(allLandmarks)
								print "\n\n\t\tIN REACTIVE PHASE\n\n",questions			
								if status!=None and status!=-1:
									path=self.g.djikstra(lookupEdge[status].v,g.getNode(DEST))					
									#~ print path,'\n',self.g.djikstra(nextpath[j-1][-1].v,g.getNode(DEST))					
									#~ sfile.write(repr(path[i-1].splitId)+repr(map(lambda x:x.splitId, path)))
									queue.put(path)
									if sys_debug==1:
										print "<--- tracker conveyed new path to the runner --->"
									prevtime=self.time
									checkpttime=self.time
									i=0		#so that control doesn't reach to tracking end after breaking
									self.updateResults(1,questions)
									break
								elif status==None:
									self.updateResults(0,questions)	
									print "EXCEPTION TO BE RAISED"
									raise Exception											
								#-------------------------------------------------------------------------------#
							else:	
								sortedTuple=sorted(restEdges,key=lambda x:x[0])
								closestTuple=sortedTuple[0]
								lastWaitDist=newWaitDist
								if closestTuple[0]-lastWaitDist>0:
									newWaitDist=closestTuple[0]-lastWaitDist
									filteredSect.append(closestTuple[1].sectId)						
									print
									print "\twait distance changes: ",path[i].length, " to ",newWaitDist
									print
									#~ dist-=lastWaitDist							
									dist=newWaitDist			#after crossing intersection, wait on not more than newWaitDist
								else:
									for itemtuple in sortedTuple:			# add all those sections which should have reached by now
										if itemtuple[0]-lastWaitDist>0:
											filteredSect.append(itemtuple[1].sectId)
									dist=0	 #next possible segment is shorter than this route segment, so no need to wait for crossing next possible segment
								factor=1.0													
						
						#if intersection is not crossed, wait on the old distance but with a reduced factor	
						elif crossedIntersection==0:
							askedIntersection=0		#need to ask again next time
						
						#intersection is crossed and no nextpath potential segments
						else:
							dist=path[i].length
						prevtime=self.time
						continue
						#~ assert(False)
				
				if reply==1:
					filteredSect=[]
					# if here and factor<threshhold, that means intersection was crossed
					crossedIntersection=1 if factor<THRESHHOLD else 0			#reset the variable
					askedIntersection=0			#reset the variable
					flagIntersection=0			#reset the variable
					factor=1.0
					speed=dist/(self.time-checkpttime)
					self.addToAverage(speed,path[i].sectId)

					# ---------------------- update the logs ----------------------
					if TOLOGHSPEED==1:
						hspeed=self.loadhspeed()
						speedlog=hspeed[path[i].sectId]
						#~ hspeed[path[i].sectId]=((speedlog[0]*speedlog[1]+speed)/(speedlog[1]+1.0),speedlog[1]+1)
						# same as above
						hspeed[path[i].sectId]=(((speedlog[0]/(speedlog[1]+1.0))*speedlog[1])+(speed/(speedlog[1]+1.0)),speedlog[1]+1)
						print " ******************************* ",hspeed[path[i].sectId]
						self.dumphspeed()
					# -------------------------------------------------------------
					
					if sys_debug==1:
						print "<--- runner on track! with speed @", speed, "--->", "(",dist, self.time,prevtime,factor,crossedIntersection,")"
					prevtime=self.time
					checkpttime=self.time
				
				ans.task_done()
				dist=0
				i+=1

			#~ print "at the end: ",i+1	
			if i==len(path):
				self.printStats()
				print "End tracking"
				return				
										
	def updatespeed(self,t1,t2,d):
		return d/(t1-t2)		
	
	def loadhspeed(self):
		return pickle.load(open(hspeedfile,"rb"))
	
	def dumphspeed(self):
		pickle.dump(hspeed,open(hspeedfile,"wb"))
	
	def initSpeed(self):
		return 5.0
	
	def prompt(self,string):
		print "PROMPT NO: ",self.prompts+1
		print string
		self.prompts+=1

	def addToAverage(self,speed,sectId):
		#Average Speed
		avg=self.uspeed_avg
		self.uspeed_avg=(avg*self.uspeed_n+speed)/(self.uspeed_n+1)
		
		#Average speed Deviation
		hspeed=self.loadhspeed()
		dev=abs(speed-hspeed[sectId][0])
		self.uspeed_dev=(self.uspeed_dev*self.uspeed_n+dev)/(self.uspeed_n+1)

		self.uspeed_n+=1
		
	def estimateSpeed(self):
		return 15.0
		#~ return self.uspeed_avg

	def checkcorrect(self,runner,ttime):
		return runner.gettime()-ttime

	def updateResults(self,status,questions):
		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"				
		'''
		filepath="/home/arbazk/MTT/Quantum/MovingDot/att"
		if not os.path.exists(filepath+str(self.modifier.getT()-1)+".txt"):
			f=open(filepath+str(self.modifier.getT()-1)+".txt","w")
		else:
			f=open(filepath+str(self.modifier.getT()-1)+".txt","a")
		f.write("//----------------------------------------/\n")
		f.write("Tracking Status\n")
		f.write("Actual Time: "+str(self.time)+"\n")
		f.write("Expected Time: "+str(self.etime)+"\n")
		f.write("Expected Time: "+str(self.etime)+"\n")
		f.write("# attrib: "+str(self.modifier.getT())+"\n")
		f.write("status: "+str(status)+"\n")
		f.write("questions: "+str(questions)+"\n")
		f.write("//----------------------------------------/\n\n")
		f.close()		
		'''
				
	def printStats(self):
		if TOPRINT==1:
			f=open("results.txt","a")
			f.write("//----------------------------------------/\n")
			f.write("Tracking Status\n")
			f.write("Actual Time: "+str(self.time)+"\n")
			f.write("Questions: "+str(self.questions)+"\n")
			f.write("Mistakes: "+str(self.mistakes)+"\n")
			f.write("Decisions: "+str(len(set(self.decisions)))+"\n")
			f.write("Prompts: "+str(self.prompts)+"\n")
			f.write("G: "+str((self.prompts-len(set(self.decisions)))/self.mistakes)+"\n")
			f.write("//----------------------------------------/\n\n")
			f.close()		

	def recordPattern(self,string):
		f=open("patterns.txt","a")
		f.write(string+"\n")
		f.close()	
		# prompt factor = (travelled dist - original dist) / original dist
		#~ self.prfactor=abs(float(string.split()[0])-float(string.split()[-1]))/float(string.split()[-1])

	def qtrack(self,runner,path):
		prev=None
		prevtime=0
		pos=runner.position()
		while (prev is None):
			response0=self.time
			self.wait()
			prev=pos
			pos=runner.position()
			self.time=prevtime=runner.gettime()	
		
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
			#~ self.time+=path[i].length/speed
			#~ while self.checkcorrect(runner,self.time)<0:
				#~ self.wait()
			#~ self.time=runner.gettime()
			#~ self.updatespeed(self.time,prevtime,path[i].length)		
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
	#~ g.correctgraph(conn)
	#~ '''
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
	
	#------------- Initialize historical speed data -------------
	if not os.path.isfile("hspeed.pkl"):
		for edge in list(set([item for lists in g.edges.values() for item in lists])):
			hspeed[edge.sectId]=(5,1)
		pickle.dump(hspeed,open(hspeedfile,"wb"))	
	else:		
		hspeed=pickle.load(open(hspeedfile,"rb"))
	#------------------------------------------------------------
	
		
	#~ print map(lambda x: x.edgeId, g.djikstra(g.getNode(SRC), g.getNode(DEST)))
	queue= Queue.Queue()	
	ans = Queue.Queue()	
	m=attmodifier.modifier(conn)
	#~ v=int(raw_input("Enter T:"))
	m.clear()
	m.modify(3,3)
	#~ print "modified"
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

	#~ '''		
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
