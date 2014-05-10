from psycopg2 import *
from graph import *
from priodict import priorityDictionary 
import dbfields 


class networkNode(node):
	split_id=None
	nodeid=None
		
	def setId(self, split_id_,nodeid_):
		self.split_id=split_id_
		self.nodeid=nodeid_	

class networkGraph(graph):
	geomNodes={}
	count=0
	def getNode(self,point):
		if point in self.geomNodes:
			return self.geomNodes[point]
		else:
			return None
				
	def makeNode(self,point,edgeid):
		"""geom to networkNode"""
		if point not in self.geomNodes:
			self.count+=1
			self.geomNodes[point]=networkNode(point)
			self.geomNodes[point].setId(edgeid,self.count)
			
		return self.geomNodes[point]

	def adj(self, v):
		return self.edges[v]
		
	def edgeint(self, edge1, edge2):
		if edge1.u in [edge2.u,edge2.v]:
			return edge1.u
		if edge1.v in [edge2.u,edge2.v]:				
			return edge1.v
		return None				

	def coedgeint(self,edge1,edge2):
		u=self.edgeint(edge1,edge2)
		if u==edge2.u:
			u=edge2.v
		else:
			u=edge2.u
		return u	

	def build_graph(self,conn):	
		cur	= conn.cursor()		
		cur.execute("SELECT * from network_extended")

		for row in cur:
			row=dbfields.reg(cur,row)
			cur1=conn.cursor()
			cur1.execute("SELECT (s.points).geom as point FROM ( SELECT ST_DumpPoints('%s') as points) as s " % row.geom)
			prevpt=dbfields.reg(cur1,cur1.fetchone()).point
			prevnode=self.makeNode(prevpt,row.split_id)
			temp=conn.cursor()
			for row1 in cur1:	
				row1=dbfields.reg(cur1,row1)
				nextnode=self.makeNode(row1.point,row.split_id)
				temp.execute("SELECT st_distance('%s','%s') as l" % (prevnode.geom,nextnode.geom))
				length=dbfields.reg(temp,temp.fetchone()).l
				#temp.execute("INSERT INTO network_dumppoints (geomline, angle, split_id, gid, geom) VALUES \
				#	(st_makeline('%s','%s'), degrees( ST_Azimuth('%s'::geometry,'%s'::geometry) ),'%s', '%s', '%s') " 
				#	% (prevnode.geom,nextnode.geom,prevnode.geom,nextnode.geom, row.split_id , row.gid, row.geom ))
				edgesInserted=self.insertEdge(prevnode,nextnode,length)
				map(lambda x: x.setId(row.split_id),edgesInserted)		#Store corresponding splitIDs 
				for e in edgesInserted:			
					temp.execute("SELECT degrees( ST_Azimuth('%s'::geometry,'%s'::geometry) ) as angle" % (e.u.geom,e.v.geom))
					angle=dbfields.reg(temp,temp.fetchone()).angle
					e.setangle(angle)
				prevnode=nextnode
			temp.close()
			cur1.close()
		cur.close()		
				
	def build_sectgraph(self,conn):
		cur	= conn.cursor()		
		cur.execute("SELECT * from network_dumppoints_copy")

		for row in cur:
			row=dbfields.reg(cur,row)
			cur1=conn.cursor()
			cur1.execute("SELECT (s.points).geom as point FROM ( SELECT ST_DumpPoints('%s') as points) as s " % row.geomline)
			prevpt=dbfields.reg(cur1,cur1.fetchone()).point
			prevnode=self.makeNode(prevpt,row.dump_id)
			temp=conn.cursor()
			for row1 in cur1:	
				row1=dbfields.reg(cur1,row1)
				nextnode=self.makeNode(row1.point,row.dump_id)
				#~ temp.execute("SELECT st_distance('%s','%s') as l" % (prevnode.geom,nextnode.geom))
				length=row.length
				#temp.execute("INSERT INTO network_dumppoints (geomline, angle, split_id, gid, geom) VALUES \
				#	(st_makeline('%s','%s'), degrees( ST_Azimuth('%s'::geometry,'%s'::geometry) ),'%s', '%s', '%s') " 
				#	% (prevnode.geom,nextnode.geom,prevnode.geom,nextnode.geom, row.split_id , row.gid, row.geom ))
				edgesInserted=self.insertEdge(prevnode,nextnode,length)
				map(lambda x: x.setId(row.dump_id),edgesInserted)		#Store corresponding splitIDs 
				map(lambda x: x.setsectId(row.split_id),edgesInserted)		#Store corresponding sectIDs 
				for e in edgesInserted:			
					temp.execute("SELECT degrees( ST_Azimuth('%s'::geometry,'%s'::geometry) ) as angle" % (e.u.geom,e.v.geom))
					angle=dbfields.reg(temp,temp.fetchone()).angle
					e.setangle(angle)
				prevnode=nextnode
			temp.close()
			cur1.close()
		cur.close()
	
	#patches the edges with different splitId but same atomic edge
	def correctgraph(self,conn):
		cur=conn.cursor()
		nodeDict=priorityDictionary()
		for node in self.edges:
			if len(self.edges[node])<=2:
				nodeDict[node]=min(map(lambda x:x.sectId, self.edges[node]))
		
		print len(nodeDict)
		count=0
		visited=[]
		for node in nodeDict:
			count+=1
			#~ print count
			cur.execute("update network_dumppoints_copy set split_id=%s \
				where st_startpoint(geomline)='%s' or st_endpoint(geomline)='%s'" % (nodeDict[node],node.geom,node.geom))			
			for nbr in self.adj(node):
				if nbr.u==node:
					if nbr.v not in visited and nbr.v in nodeDict:
						nodeDict[nbr.v]=nodeDict[node]
				else:
					if nbr.u not in visited and nbr.u in nodeDict:
						nodeDict[nbr.u]=nodeDict[node]
			visited.append(node)				
		conn.commit()	

						
				
	def dfs(self, s, t):
		finished=False
		visited={}
		parent={}			#parent[childvertex]=(parentvertex,connectingEdgeNode)

		#Trace path using parent pointers
		def getpath(s,t,parent,path):
			path.append(parent[t][1])
			return (getpath(s,parent[t][0],parent,path) if s!=parent[t][0] else path)
		
		def dfshelper(s,t,visited,parent,finished):			
			visited[s]=True		
			for edgeuv in self.adj(s):
				v=edgeuv.v
				#~ print v.geom
				if (visited[v]==False):
					parent[v]=(s,edgeuv)
					if (v!=t and finished==False):
						finished=dfshelper(v,t,visited,parent,finished) 	
					else:
						finished=True
						return finished			
			return finished			
		
		for i in self.geomNodes:
			visited[self.geomNodes[i]]=False
		finished=dfshelper(s,t,visited,parent,finished)
		path=[]
		#~ print getpath(s,t,parent,path).reverse()
		#~ print parent
		if finished==True:
			path=getpath(s,t,parent,path)
			path.reverse()
			return path
		else:
			return []	
	
	# Calculate linear distance from s to t along a path
	# Return None if either of s,t is not on the path
	def linearDistance(self,s,t,path):
		dist=None
		#~ print s,t,"#####"
		for edgeuv in path:
			if edgeuv.u==s:
				dist=0

			if dist is not None:
				dist+=edgeuv.length
			
			if edgeuv.v==t:
				break
				
		if edgeuv.v!=t:
			dist=None					
		return dist		
	
	#inverse of linear distance wrt dist and t 
	def findPoint(self,s,dist,path):
		span=None
		for edgeuv in path:
			if edgeuv.u==s:
				span=0
				
			if span is not None:
				if (span+edgeuv.length) >=dist:
					return edgeuv.v
				else:
					span=span+edgeuv.length	
			
		return float("inf")	
	
	#find all paths that are of length less than dist originating at s
	#Returns a list of paths (set of node ids)
	#Note : visited nodes not counted again, but what if several intersecting paths? (paths with atleast one vertex in common)
	#		some paths would end in a visited node. Take care!
	def findPaths(self,s,dist):
		def pathfinder(s,dist,visited):
			if dist<=0:
				return [[s]]
			flag=False	
			paths=[]
			for edgeuv in self.adj(s):
				v=edgeuv.v
				if v not in visited:
					flag=True		#atleast one non visited nbr		
					visited[v]=True
					rest=pathfinder(v,dist-edgeuv.length,visited) 	#'rest' is a list of paths
					rest=map(lambda x : x+[s], rest)
					paths+=rest
			if flag==False:
				return [[s]]	
			else:
				return paths
		
		
		visited={}
		return pathfinder(s,dist,visited)
		
	# Same as findPaths but returns edges instead
	# returns a list of tuples of the form (x,e) where x is distance from s, e is an edge instance						
	def findPathEdges(self,s,distance):
		sfile=open("sfile.txt","a")
		ddict={}   #stores reverse distances wrt distance i.e if ddict[x]=y then, the end of x is (distance-y) units from s
		
		
		# returns a set of all the singleton list each containing edgeIds encountered on the path
		# e.g. ans= [[232],[132],[111]]
		def makeset(ans):
			toret=[]
			for path in ans:
				for edge in path:
					if [edge] not in toret:
						toret.append([edge])
			return toret
			
		# makes a pair of true_dist,edge for each edge 	
		def addDist(ans,dist):
			for i in range(len(ans)):
				ans[i].insert(0,distance-ddict[ans[i][-1]])				
		
		def pathfinder(s,dist,visited):
			if dist<=0:
				return [[]]
			flag=False	
			paths=[]
			visited[s]=True
			for edgeuv in self.adj(s):
				v=edgeuv.v
				sfile.write(repr(edgeuv.splitId))
				if v not in visited:
					flag=True		#atleast one non visited nbr		
					rest=pathfinder(v,dist-edgeuv.length,visited) 	#'rest' is a list of paths
					rest=map(lambda x : x+[edgeuv], rest)
					if edgeuv not in ddict:
						ddict[edgeuv]=dist-edgeuv.length
					else:
						if ddict[edgeuv]<dist-edgeuv.length:
							ddict[edgeuv]=dist-edgeuv.length	
					paths+=rest
				sfile.write("\n")
			del visited[s]		
			if flag==False:
				return [[]]	
			else:
				return paths
		
		sfile.write("new path\n")
		visited={}
		
		ans=pathfinder(s,distance,visited)					
		sfile.close()
		#~ print distance, map(lambda x:x[-1].splitId,ans)
		ans=makeset(ans)
		addDist(ans,distance)
		#~ print "FROM NETWRKGRAPH: ",map(lambda x:[x[0],x[1].splitId],ans)
		return ans
	

	
	
	#find all paths that are of length less than dist originating at a section in the direction from endpoint s on it
	#Returns a list of paths (set of edges)
	#Note : visited sections are counted again
	def findallPaths(self,sect,s,dist):
		def pathfinder(sect,s,dist,visited):
			if dist<=0:
				return [[]]
			flag=False	
			paths=[]
			for edgeuv in self.adj(s):
				v=edgeuv.v
				if edgeuv.splitId not in visited:
					flag=True		#atleast one non visited nbr		
					visited[edgeuv.splitId]=True							
					rest=pathfinder(edgeuv,v,dist-edgeuv.length,visited) 	#'rest' is a list of paths
					del visited[edgeuv.splitId]						
					rest=map(lambda x : x+[edgeuv], rest)
					paths+=rest
			 		
			return paths
		
		
		visited={}
		return pathfinder(sect,s,dist,visited)					
		
	def getLandmarks(self, conn, path):

		landmarks={}
		for ind,i in enumerate(path):
			landmarks[i]=[]

		#~ landmarks=[0 for i in range(len(path))]	 # ref_ids of landmark at each section
												 # landmark corresponding to section path[i] is landmarks[i]
												 # 0 indicates no landmark nearby to that section
												 
		cur=conn.cursor()
		cur.execute(cur.mogrify("select dump_id,ref_id from sectlandmark where dump_id = ANY( \
			select dump_id from network_dumppoints where split_id=%s)", (map(lambda x: x.sectId, path),)))
		
		for row in cur:
			row=dbfields.reg(cur,row)
			landmarks[row.dump_id].append(row.ref_id)
		
		return landmarks

	#~ http://code.activestate.com/recipes/119466-dijkstras-algorithm-for-shortest-paths/		
	def djikstra(self,s,t):
		D = {}	# dictionary of final distances
		P = {}	# dictionary of predecessors
		Q = priorityDictionary()   # est.dist. of non-final vert.
		Q[s] = 0
		Path = []
		
		for v in Q:
			D[v] = Q[v]
			if v == t:
				while 1:
					if t == s: break
					Path.append(P[t][1])
					t = P[t][0]
				Path.reverse()
				return Path
				
			
			for edgew in self.adj(v):
				w=edgew.v
				vwLength = D[v] + edgew.length
				if w in D:
					if vwLength < D[w]:
						raise ValueError, "Dijkstra: found better path to already-final vertex"
				elif w not in Q or vwLength < Q[w]:
					Q[w] = vwLength
					P[w] = [v, edgew]
		return Path			
		
				
	#~ Returns the shortest distances from source to all other vertices 
	def djikstraExtended(self,s,t):
		D = {}	# dictionary of final distances
		P = {}	# dictionary of predecessors
		Q = priorityDictionary()   # est.dist. of non-final vert.
		Q[s] = 0
		Path = []
		
		for v in Q:
			D[v] = Q[v]
			if v == t:
				while 1:
					if t == s: break
					Path.append(P[t][1])
					t = P[t][0]
				Path.reverse()
				return Path,Q
				
			
			for edgew in self.adj(v):
				w=edgew.v
				vwLength = D[v] + edgew.length
				if w in D:
					if vwLength < D[w]:
						raise ValueError, "Dijkstra: found better path to already-final vertex"
				elif w not in Q or vwLength < Q[w]:
					Q[w] = vwLength
					P[w] = [v, edgew]
		return Path,Q			
		
				
''' 
USAGE
if __name__=="__main__":
	conn = connect("dbname=demo user=postgres host=localhost password=indian")
	g=networkGraph()
	g.build_graph(conn)
	for i in g.edges[g.getNode('0101000020847F0000165E0110C94B1A41079011A6B6584641')]:
		print i.geom
'''
