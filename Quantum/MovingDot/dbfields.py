class reg(object):
	"""Python class to access results by field names"""
	def __init__(self, cursor, row):
		for (attr, val) in zip((d[0] for d in cursor.description), row) :
			setattr(self, attr, val)
