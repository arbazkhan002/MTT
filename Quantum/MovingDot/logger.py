class logger:
	f=None
	def __init__(self,fname):
		self.f=open(fname,"w")
	
	def write(self,loglist):
		for string in loglist:
			self.f.write(" ".join(map(lambda x: str(x),string))+"\n")
		
		
	
