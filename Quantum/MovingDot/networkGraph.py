from psycopg2 import *
from graph import * 
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
		cur.execute("SELECT * from network_dumppoints")

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
				for e in edgesInserted:			
					temp.execute("SELECT degrees( ST_Azimuth('%s'::geometry,'%s'::geometry) ) as angle" % (e.u.geom,e.v.geom))
					angle=dbfields.reg(temp,temp.fetchone()).angle
					e.setangle(angle)
				prevnode=nextnode
			temp.close()
			cur1.close()
		cur.close()		
								
				
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
	#Note : visited nodes not counted again, but what if loops in paths?
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
	def findPathEdges(self,s,dist):
		def pathfinder(s,dist,visited):
			if dist<=0:
				return [[]]
			flag=False	
			paths=[]
			for edgeuv in self.adj(s):
				v=edgeuv.v
				if v not in visited:
					flag=True		#atleast one non visited nbr		
					visited[v]=True
					rest=pathfinder(v,dist-edgeuv.length,visited) 	#'rest' is a list of paths
					rest=map(lambda x : x+[edgeuv], rest)
					paths+=rest
			if flag==False:
				return [[]]	
			else:
				return paths
		
		
		visited={}
		return pathfinder(s,dist,visited)					
	
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
		sections={}

		for ind,i in enumerate(path):
			sections[i]=ind
		landmarks=[0 for i in range(len(path))]	 # ref_ids of landmark at each section
												 # landmark corresponding to section path[i] is landmarks[i]
												 # 0 indicates no landmark nearby to that section
												 
		cur=conn.cursor()
		cur.execute(cur.mogrify("select dump_id,ref_id from sectlandmark where dump_id = ANY(%s)", (map(lambda x: x.splitId, path),)))
		
		for row in cur:
			row=dbfields.reg(cur,row)
			landmarks[sections[row.dump_id]-1]=row.ref_id
		
		return landmarks
				
''' 
USAGE
if __name__=="__main__":
	conn = connect("dbname=demo user=postgres host=localhost password=indian")
	g=networkGraph()
	g.build_graph(conn)
	for i in g.edges[g.getNode('0101000020847F0000165E0110C94B1A41079011A6B6584641')]:
		print i.geom
'''
