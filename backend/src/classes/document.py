# SPDX-License-Identifier: Apache-2.0

class Document:
	def __init__(self, path, name, extension, modified_time, creation_time, size, link, id = None):
		self.path = path
		self.name = name
		self.extension = extension
		self.modified_time = modified_time
		self.creation_time = creation_time
		self.size = size
		self.link = link
		self.id = id
