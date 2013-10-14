class logger:
	f=None
	def __init__(self,fname):
		self.f=open(fname)
	
	def write(self,loglist):
		for string in loglist:
			self.f.write(str(string))
		self.f.write("\n")	
		
	
