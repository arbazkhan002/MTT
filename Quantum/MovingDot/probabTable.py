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
					cur.execute("INSERT INTO probabTable VALUES (%s, %s,%s,%s,%s)",(node.nodeid, edge1.edgeId,edge2.edgeId,True,P_ORIENTED));
					cur.execute("INSERT INTO probabTable VALUES (%s, %s,%s,%s,%s)", (node.nodeid, edge1.edgeId,edge2.edgeId,False,(1-P_ORIENTED)/size));
					
	cur.close()
	conn.commit()
	conn.close()				
