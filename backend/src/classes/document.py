
class Document:
	def __init__(self, path, name, extension, vector = None):
		self.path = path
		self.name = name
		self.extension = extension
		self.vector = vector