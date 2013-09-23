from pickle import *
from psycopg2 import *	

class reg(object):
	"""Python class to access results by field names"""
	def __init__(self, cursor, row):
		for (attr, val) in zip((d[0] for d in cursor.description), row) :
			setattr(self, attr, val)

def flip(deg):
	"""Flip an angle by 180"""
	temp=deg+180
	if temp>=360:
		temp-=360
	return temp

def	discourse(conn):
	prev_deg=-360
	
	cur	= conn.cursor()

	cur.execute("SELECT * FROM network_extended JOIN (SELECT * FROM shortest_path('%s', 260, 261, false, false)) AS route ON network_extended.split_id = route.edge_id;" 
				% ("SELECT split_id AS id, start_id::int4 AS source, end_id::int4 AS target, length::float8 AS cost FROM network_extended"))

	for row in cur:
		row=reg(cur,row)
		if (row.vertex_id==row.start_id):
			orientation=True
		
			if prev_deg==-360:
				prev_deg = row.end_angle
				
			deg = row.start_angle
			x = deg - prev_deg
			prev_deg = row.end_angle
			
		# else store the start angle	
		else:
			orientation = False; #Going in the opp direction as the edge (endid to startid)
			
			if prev_deg==-360:
				prev_deg = flip(row.start_angle)
				continue
			
			
			deg = flip(row.end_angle)
			x = deg - prev_deg
			prev_deg = flip(row.start_angle)
			
		
		# print 'ID:% ORIENTATION % StartConnections % and ANGLE %',row.vertex_id,orientation,row.start_connections,x;
		
		if (orientation==True and row.start_connections==True) or  (orientation==False and row.end_connections==True): 
			print 'On ',row.vertex_id
			alt=conn.cursor()
			alt.execute("SELECT n.split_id,acad_building,facility,fence FROM network_extended as n,edget6  WHERE edget6.split_id=n.split_id AND n.split_id=%s" % (row.split_id))
			for col in alt:
				col=reg(alt,col)
				print "fence:%s building:%s" % (col.fence,col.facility)

			if x>=45 and x<=135:
				print 'GO RIGHT'

			elif x>=225 and x<=315:
				print 'GO LEFT'

			elif x>=-135 and x<=-45:
				print 'GO LEFT'

			elif x>=-315 and x<=-225:
				print 'GO RIGHT'	
				
			else:
				print 'GO STRAIGHT'			 
			
		
if __name__=="__main__":
	conn = connect("dbname=demo user=postgres host=localhost password=indian")
	discourse(conn)
