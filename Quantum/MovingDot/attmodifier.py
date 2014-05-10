from psycopg2 import *
import dbfields
import random

# T is 1-indexed
# So, when there are 2 columns of attributes a1,a2 - self.T is 3

class modifier: 
	def __init__(self,conn):
		self.T=1
		self.N=0
		self.conn=conn
		cur=self.conn.cursor()
		cur.execute("\
				SELECT * \
				FROM information_schema.columns \
				WHERE \
				  table_name = 'test' and left(column_name,1)='a';")
		for row in cur:
			self.T+=1		  		
			
		if self.T>0:
			cur.execute("select max(a1) as m from test")
			for row in cur:
				row=dbfields.reg(cur,row)
				self.N=row.m
		
		print "T:",self.T
				
	def getT(self):
		return self.T
 
	def getN(self):
		return self.N
 
	def modify(self,T,N):		
		cur=self.conn.cursor()
		
		for i in range(self.T,T+1):
			cur.execute("alter table test add column a"+str(i)+" integer")
			cur.execute("update test set a%s=trunc(random()*%s+1)" % (i,N))
		self.conn.commit()			
		cur.close()
		self.T=T+1
		self.N=N
		

	#returns a dict of keys=landmarkIds and values=[a1,a2,a3,...]
	def getAttr(self,arr):
		cur=self.conn.cursor()
		#~ i=1
		s=["a"+str(i) for i in range(1,self.T)]
		s=",".join(s)
		cur.execute('select id as lid,'+s+' from test where id=any(%s)',[arr])
		ret={}	
		for row in cur:
			row=dbfields.reg(cur,row)
			#basically have an array, [row.a1, row.a2, ... ]
			entry=map(lambda x:("row."+x),s.split(','))
			ret[row.lid]=[]
			for i in range(len(entry)):
				ret[row.lid].append(eval(entry[i]))
		cur.close()	
		return ret


	def clear(self):
		cur=self.conn.cursor()
		for i in range(1,self.T):
			cur.execute("alter table test drop column a"+str(i)+" ;") 
		self.T=0
		self.N=0
		cur.close()
		self.conn.commit()

#~ conn = connect("dbname=demo user=postgres host=localhost password=indian")
#~ s=modifier(conn)
#~ s.modify(1,3)
if __name__=="__main__":		
	try:
		conn = connect("dbname=demo user=postgres host=localhost password=indian")
		s=modifier(conn)
		s.modify(1,3)
		
		#~ print map(lambda x:eval("x.a1"),s.getAttr([34,35]))
		print s.getAttr([34,35])
		#~ s.clear()
	finally:
		pass
		#~ s.clear()
