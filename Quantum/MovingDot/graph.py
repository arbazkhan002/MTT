class node:
	geom=None
	def __init__(self,geom_=None):
		self.geom=geom_

class edge:
	u=None
	v=None
	length=None
	edgeId=None				#EdgeIDs enumerated on decomposition of an atomic edge
	splitId=None			#dumpID (line between every two points on the map)
	sectId=None				#Actual SplitID (atomic edgeID - no decision points inside it)
	angle=None 				#absolute angle

	def __init__(self,u_=None, v_=None, length_=None, edgeId_=None):
		self.u=u_
		self.v=v_
		self.length=length_
		self.edgeId=edgeId_

	def	setId(self,splitId_):
		self.splitId=splitId_
		
	def	setsectId(self,sId_):
		self.sectId=sId_
	
	def setangle(self,angle_):
		self.angle=angle_
	

class graph:		
	edges={}
	nvertices=0
	nedges=0
	
	def __init__(self,edges_=None, nvertices_=None):
		edges=edges_
		nvertices=nvertices_

	def insertEdge(self, node1, node2,length=None, directed=False):
		edgesInserted=[]
		if node1 not in self.edges:
			self.edges[node1]=[]
		self.nedges+=1	
		e=edge(node1,node2,length,self.nedges)
		edgesInserted.append(e)	
		self.edges[node1].append(e)
		if directed==False:
			if node2 not in self.edges:
				self.edges[node2]=[]
			self.nedges+=1	
			e=edge(node2,node1,length,self.nedges)
			edgesInserted.append(e)
			self.edges[node2].append(e)
		return edgesInserted
