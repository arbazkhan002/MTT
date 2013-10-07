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
			for row1 in cur1:	
				row1=dbfields.reg(cur1,row1)
				nextnode=self.makeNode(row1.point,row.split_id)
				temp=conn.cursor()
				temp.execute("SELECT st_distance('%s','%s') as l" % (prevnode.geom,nextnode.geom))
				length=dbfields.reg(temp,temp.fetchone()).l
				self.insertEdge(prevnode,nextnode,length)
				prevnode=nextnode
				
	def dfs(self, s, t):
		finished=False
		visited={}
		parent={}

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
	
	def findPoint(self,s,dist,path):
		span=None
		for edgeuv in path:
			if edgeuv.u==s:
				span=0
				
			if span is not None:
				if (span+edgeuv.length) >=dist:
					return edgeuv.v
			
		return float("inf")	
							

''' 
USAGE
if __name__=="__main__":
	conn = connect("dbname=demo user=postgres host=localhost password=indian")
	g=networkGraph()
	g.build_graph(conn)
	for i in g.edges[g.getNode('0101000020847F0000165E0110C94B1A41079011A6B6584641')]:
		print i.geom
'''
