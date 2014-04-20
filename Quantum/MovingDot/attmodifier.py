from psycopg2 import *
import dbfields
import random

class modifier: 
	T=0
	N=0
	
	def __init__(self,conn):
		self.conn=conn
 
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


	def getAttr(self,arr):
		cur=conn.cursor()
		#~ i=1
		s=["a"+str(i) for i in range(1,self.T)]
		s=",".join(s)
		cur.execute('select '+s+' from test where id=any(%s)',[arr])
		ret=[]	
		for row in cur:
			row=dbfields.reg(cur,row)
			ret.append(row)
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
		print map(lambda x:eval("x.a1"),s.getAttr([34,35]))
		#~ s.clear()
	finally:
		pass
		#~ s.clear()
