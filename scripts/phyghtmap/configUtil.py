# -*- encoding: utf-8 -*-

__author__ = "Adrian Dempwolff (phyghtmap@aldw.de)"
__version__ = "2.23"
__copyright__ = "Copyright (c) 2009-2021 Adrian Dempwolff"
__license__ = "GPLv2+"

import base64

class Config(object):
	def __init__(self, filename):
		self.filename = filename
		self.parse()
		self.needsWrite = False

	def __del__(self):
		self.write()

	def _decodeLine(self, line):
		# this is not for obfuscation but for parsing issues
		b64Key, b64Value = line.split(":")
		key = base64.decodebytes(b64Key.encode()).decode()
		value = base64.decodebytes(b64Value.encode()).decode()
		return key, value

	def _encodeLine(self, key, value):
		# this is not for obfuscation but for parsing issues
		b64Key = base64.encodebytes(key.encode()).decode().replace("\n", "")
		b64Value = base64.encodebytes(value.encode()).decode().replace("\n", "")
		return "{:s}:{:s}".format(b64Key, b64Value)

	def parse(self):
		self.config = {}
		try:
			lines = [l.strip() for l in open(self.filename).read().split("\n") if
				l.strip()]
		except IOError:
			lines = []
		lines = [l for l in lines if not l.startswith("#")]
		curSection = None
		for l in lines:
			if l.startswith("[") and l.endswith("]"):
				# this is a section identifier
				curSection = l[1:-1]
			else:
				key, value = self._decodeLine(l)
				self.set(curSection, key, value)

	def write(self):
		if not self.needsWrite:
			return
		newConfig = open(self.filename, "w")
		for section in self.config:
			newConfig.write("\n[{:s}]\n".format(section))
			for key in self.config[section]:
				newConfig.write(self._encodeLine(key, self.config[section][key])+"\n")

	def set(self, section, key, value):
		if not section in self.config:
			self.config[section] = {}
		oldValue = self.get(section, key)
		if oldValue != value:
			self.config[section][key] = value
			self.needsWrite = True

	def get(self, section, key):
		if not section in self.config:
			return None
		elif key is None or not key in self.config[section]:
			return None
		else:
			return self.config[section][key]

	def setOrGet(self, section, key, value=None):
		if value == None:
			return self.get(section, key)
		else:
			self.set(section, key, value)
			return value

