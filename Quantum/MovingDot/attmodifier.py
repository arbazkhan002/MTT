from psycopg2 import *
import dbfields
import random

class modifier: 
	def __init__(self,conn):
		self.T=0
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
				row=dbfield.reg(cur,row)
				self.N=cur.m
				
	def getT(self):
		return self.T
 
	def getN(self):
		return self.N
 
	def modify(self,T,N):
		self.T=T+1
		self.N=N
		
		cur=self.conn.cursor()
		
		for i in range(1,self.T):
			cur.execute("alter table test add column a"+str(i)+" integer")
			self.N=random.randint(1,self.N)	
			cur.execute("update test set a%s=trunc(random()*%s+1)" % (i,self.N))
		conn.commit()	
		cur.close()

	#returns a dict of keys=landmarkids and values=[a1,a2,a3,...]
	def getAttr(self,arr):
		cur=conn.cursor()
		#~ i=1
		s=["a"+str(i) for i in range(1,self.T)]
		s=",".join(s)
		cur.execute('select id as lid,'+s+' from test where id=any(%s)',[arr])
		ret={}	
		for row in cur:
			row=dbfields.reg(cur,row)
			#basically have an array, [row.a1, row.a2, ... ]
			entry=map(lambda x:eval("row."+x),s.split(','))
			ret[row.lid]=entry
		cur.close()	
		return ret


	def clear(self):
		cur=self.conn.cursor()
		for i in range(1,self.T):
			cur.execute("alter table test drop column a"+str(i)+" ;") 
		self.T=0
		self.N=0
		cur.close()
		conn.commit()

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
