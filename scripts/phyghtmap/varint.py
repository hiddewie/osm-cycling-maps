__author__ = "Adrian Dempwolff (phyghtmap@aldw.de)"
__version__ = "2.23"
__copyright__ = "Copyright (c) 2009-2021 Adrian Dempwolff"
__license__ = "GPLv2+"

def int2str(n):
	b = n&127
	n >>= 7
	s = []
	while n:
		s.append(b|128)
		b = n&127
		n >>= 7
	s.append(b)
	return bytes(s)

def sint2str(n):
	if n > -1:
		# 0 or positive, shift 1 to the left
		n <<= 1
		return int2str(n)
	# negative number, take abs(n), decrease by 1, shift 1 to the left, add 1
	# as negative bit
	n = ((-n-1)<<1)|1
	return int2str(n)

def str2bytes(string, encoding="utf-8"):
	return bytes(string, encoding=encoding)

def writableInt(integer):
	return bytes((integer, ))

def writableString(string):
	return str2bytes(string)

def join(sequence):
	"""takes a sequence of bytes-like objects and returns them as joined bytes object
	"""
	return b"".join(sequence)

bboxStringtypes = (type(str()), type(bytes()), type(bytearray()))

