""" Natural Language Grammar to represent 'good quality' routes """
from networkGraph import *

SRC='0101000020847F0000704DF34E47D0194118485024FD5F4641'
DEST='0101000020847F0000B0627FD91ED019411851DABB05604641'
DESTS='0101000020847F0000A1C8E203E8CD1941390A322D06604641'
DESTLL='0101000020847F00008CDD071EC5DF1941C8D53D59AA5F4641'
MAXDIST=100				#Maximum qualifying distance for a landmark (Similar to assigning MAXINT) 
conn = connect("dbname=demo user=postgres host=localhost password=indian")

def getAngle(x):
	if x=='R':
		return [[45,135]]
		
	elif x=='L':
		return [[225,315]]
			
	elif x=='S':
		return [[0,45],[315,360]]			#A valid range as greater than 315 and less than 45 would count as straight. (Remember: Angles are measured clockwise 12o = 0', 3o=90' ...)

def getDirection(x):
	if x>=45 and x<=135:
		return 'R'

	elif x>=225 and x<=315:
		return 'L'

	elif x>=-135 and x<=-45:
		return 'L'

	elif x>=-315 and x<=-225:
		return 'R'	
		
	else:
		return 'S'			 	


def encode(g,path):
	pathstring=''
	if len(path)==0:
		return pathstring
	prev=path[0]
	cur=conn.cursor()
	
	landlist=[]
	
	for i in path:
		mindist = MAXDIST
		salienceId = None
		
		#Get landmarks
		cur.execute("select * from edgelandmark where split_id=%s" % i.splitId)
		
		for row in cur:
			row=dbfields.reg(cur,row)
			if row.dist<mindist:
				salienceId=row.salience_id
				mindist=row.dist
				landlist.append(salienceId)
			
		if mindist<MAXDIST:
			salienceId=str(salienceId)
			
		#print salienceId,mindist,i.splitId	
		
		if len(g.edges[i.u])>2:				#DecisionPoint
			x=i.angle-prev.angle
			pathstring+=getDirection(x)		#Concatenate instruction to pathstring
		prev=i
	return pathstring
	cur.close()

#Decode requires the source vertex and the source edge (edge on which to move next from source verteX)	
def decode(g,u,edge,pathstring):
	path=[edge]
	if u==edge.u:
		nextvertex=edge.v
		orientation=1
	else:
		nextvertex=edge.u
		orientation=-1
	prevedge=edge													#prevedge is actually the edge on which the dot currently is

	for i in range(len(pathstring)):	
		while len(g.edges[nextvertex])<=2:
			prevedge=filter(lambda x: x!=prevedge, g.edges[nextvertex])[0]			#filter out the visited edge and pick the only element in the filtered list to update prevedge
			nextvertex = prevedge.v if orientation==1 else prevedge.u
			path.append(prevedge)
		
		for nbr in g.adj(nextvertex):
			if nbr==prevedge: continue
			
			diff=(nbr.angle-prevedge.angle + 360)%360
		
			found=False
			
			for anglerange in getAngle(pathstring[i]):					#Check for each possible angle range					
				if diff >= anglerange[0] and diff <= anglerange[1]:
					prevedge = nbr													#update prevedge 
					nextvertex = prevedge.v if orientation==1 else prevedge.u
					found=True
					break
			
			if found==True:
				break		
			
		path.append(prevedge)
	return path	
		

if __name__=="__main__":
	g=networkGraph()
	g.build_graph(conn)
	###------------------------------------------------------------###
	# Pick any range to get two nodes
	#~ for i in range(15):
		#~ print g.geomNodes[(g.geomNodes.keys()[i])].geom	
	###------------------------------------------------------------###

	path = g.dfs(g.getNode(SRC), g.getNode(DESTS))
	
	#~ for i in path:
		#~ print i.splitId
	
	print "#######################"
	for ind,i in enumerate(decode(g,g.getNode(SRC),path[0],encode(g,path))):
		print ind, path[ind].splitId,i.splitId

conn.commit()
conn.close()
