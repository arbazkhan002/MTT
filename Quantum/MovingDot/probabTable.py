import dbfields
P_ORIENTED=0.95

def build(g,conn):

	cur=conn.cursor()
	cur.execute("DROP TABLE probabTable")
	cur.execute("CREATE TABLE probabTable (node bigInt, edge1 bigInt, edge2 bigInt, inPath boolean, probability real)")

	for node in g.geomNodes.values():
		size=len(g.edges[node])
		for edge1 in g.edges[node]:
			for edge2 in g.edges[node]:
				if edge1==edge2:
					continue
				else:
					#pass
					cur.execute("INSERT INTO probabTable VALUES (%s, %s,%s,%s,%s)",(node.nodeid, edge1.splitId,edge2.splitId,True,P_ORIENTED));
					if size>2:
						cur.execute("INSERT INTO probabTable VALUES (%s, %s,%s,%s,%s)", (node.nodeid, edge1.splitId,edge2.splitId,False,(1-P_ORIENTED)/(size-2))); #minus two in path edges
					else:	
						cur.execute("INSERT INTO probabTable VALUES (%s, %s,%s,%s,%s)", (node.nodeid, edge1.splitId,edge2.splitId,False,0.0));
					
	cur.close()
	conn.commit()


def computeProbab(conn, paths):	
	if len(paths)<1:
		return []
	edges=[]
	for path in paths:
		edges.extend(map(lambda x:x.splitId, path))
	
	cur=conn.cursor()	
	cur.execute(cur.mogrify("SELECT * from probabTable where edge1=ANY(%s) and edge2=ANY(%s)",(edges,edges,)))
	
	res=map(lambda x: dbfields.reg(cur,x),cur)
	
	table={}
	
	for row in res:
		if row.edge1 not in table:
			table[row.edge1]={}	
		if row.inpath==False:
			table[row.edge1][row.edge2]=row.probability
	
	ans=[1 for i in range(len(paths))]	
	i=0
	print table
	for path in paths:
		if len(path)<=1:
			i+=1
			continue
		prev=path[0]			
		for edge in path[1:]:
			ans[i]*=table[prev.splitId][edge.splitId]
			prev=edge
	return  ans
