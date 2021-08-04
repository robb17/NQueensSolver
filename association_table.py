class AssociationTable:
	''' Simple association table for which there exists no distinction between
		keys and values. For any item there can only exist one item with which
		that item is associated with. Items cannot be associated with themselves.
	'''
	def __init__(self, d):
		self.d = d
		for item in list(d.keys()):
			self.__setitem__(d[item], item)

	def get(self, key):
		return self.d.get(key)

	def __getitem__(self, key):
		return self.d.get(key)

	def __setitem__(self, key, value):
		if self.d.get(key):
			raise ValueError
		else:
			self.d[key] = value