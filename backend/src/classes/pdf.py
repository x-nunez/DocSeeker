# SPDX-License-Identifier: Apache-2.0

from classes import document

class PDF (document.Document):
	def __init__(self, content):
		self.content = content
