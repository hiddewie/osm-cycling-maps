# -*- encoding: utf-8 -*-

__author__ = "Adrian Dempwolff (phyghtmap@aldw.de)"
__version__ = "2.23"
__copyright__ = "Copyright (c) 2009-2021 Adrian Dempwolff"
__license__ = "GPLv2+"

import zlib
from struct import pack
import time
import numpy

from phyghtmap.varint import int2str, sint2str, join, writableInt, writableString
#from phyghtmap.pbfint import int2str, sint2str # same as above, C version

NANO = 1000000000

class Output(object):
	def __init__(self, filename, osmVersion, phyghtmapVersion, bbox=[],
		elevClassifier=None):
		self.outf = open(filename, "wb")
		self.bbox = bbox
		self.granularity = 100
		self.date_granularity = 1000
		self.elevClassifier = elevClassifier
		self.maxNodesPerNodeBlock = 8000
		self.maxNodesPerWayBlock = 32000
		self.timestamp = int(time.mktime(time.localtime()))
		self.timestampString = writableString("") # dummy attribute, needed by main.py
		self.makeHeader(osmVersion, phyghtmapVersion)

	def makeVarIdent(self, vType, vId):
		vTypes = {"V": 0, "D": 1, "S": 2, "I": 5}
		vTypeNum = vTypes[vType]
		varIdentNum = vTypeNum + (vId<<3)
		return int2str(varIdentNum)

	def makeVar(self, vType, vId, content, func=None):
		varIdent = self.makeVarIdent(vType, vId)
		if vType == "S":
			return join([
				varIdent,
				int2str(len(content)),
				content, ])
		elif vType == "V":
			# V means varint, so content is an int.
			return join([
				varIdent,
				func(content), ])

	def makeHeader(self, osmVersion, phyghtmapVersion):
		blobHeader = []
		# type, id=1
		blobHeader.append(self.makeVarIdent(vType="S", vId=1))
		# len("OSMHeader") == 9
		blobHeader.append(int2str(9))
		blobHeader.append(writableString("OSMHeader"))
		# datasize, id=3
		blobHeader.append(self.makeVarIdent(vType="V", vId=3))
		blob = self.makeHeaderBlob(osmVersion, phyghtmapVersion)
		blobHeader.append(int2str(len(blob)))
		blobHeader = join(blobHeader)
		self.outf.write(pack('!L', len(blobHeader)))
		self.outf.write(blobHeader)
		self.outf.write(blob)

	def makeHeaderBlob(self, osmVersion, phyghtmapVersion):
		blob = []
		headerBlock = self.makeHeaderBlock(osmVersion, phyghtmapVersion)
		# raw_size, id=2
		blob.append(self.makeVarIdent("V", 2))
		blob.append(int2str(len(headerBlock)))
		# zlib_data, id=3
		zlib_data = zlib.compress(headerBlock)
		blob.append(self.makeVar("S", 3, zlib_data))
		return join(blob)

	def makeHeaderBlock(self, osmVersion, phyghtmapVersion):
		headerBlock = []
		# bbox, id=1
		bbox = self.makeHeaderBBox()
		headerBlock.append(self.makeVar("S", 1, bbox))
		# required_features, id=4
		requiredFeatures = [
			writableString("OsmSchema-V{0:.1f}".format(osmVersion)),
			writableString("DenseNodes"),
		]
		for requiredFeature in requiredFeatures:
			headerBlock.append(self.makeVar("S", 4, requiredFeature))
		# writingprogram, id=16
		writingprogram = writableString(
			"phyghtmap {0:s} (http://wiki.openstreetmap.org/wiki/phyghtmap)".format(
			phyghtmapVersion))
		headerBlock.append(self.makeVar("S", 16, writingprogram))
		return join(headerBlock)

	def makeHeaderBBox(self):
		bbox = []
		left, bottom, right, top = [sint2str(int(i*NANO))
			for i in self.bbox]
		# left, id=1
		bbox.append(self.makeVarIdent("V", 1))
		bbox.append(left)
		# right, id=2
		bbox.append(self.makeVarIdent("V", 2))
		bbox.append(right)
		# top, id=3
		bbox.append(self.makeVarIdent("V", 3))
		bbox.append(top)
		# bottom, id=4
		bbox.append(self.makeVarIdent("V", 4))
		bbox.append(bottom)
		return join(bbox)

	def writeNodes(self, nodes, startNodeId):
		"""writes nodes to self.outf.  nodeList shall be a list of
		(<lon>, <lat>) duples of ints in nanodegrees of longitude and latitude,
		respectively.

		The nodelist is split up to make sure the pbf blobs will not be too big.
		"""
		for i in range(0, len(nodes), self.maxNodesPerNodeBlock):
			self.writeNodesChunk(nodes[i:i+self.maxNodesPerNodeBlock], startNodeId+i)

	def writeNodesChunk(self, nodes, startNodeId):
		blobHeader = []
		# type, id=1
		blobHeader.append(self.makeVar(vType="S", vId=1, content=writableString("OSMData")))
		# datasize, id=3
		blobHeader.append(self.makeVarIdent(vType="V", vId=3))
		blob = self.makeNodeBlob(startNodeId, nodes)
		blobHeader.append(int2str(len(blob)))
		blobHeader = join(blobHeader)
		self.outf.write(pack('!L', len(blobHeader)))
		self.outf.write(blobHeader)
		self.outf.write(blob)

	def makeNodeBlob(self, startNodeId, nodes):
		blob = []
		nodePrimitiveBlock = self.makeNodePrimitiveBlock(startNodeId, nodes)
		# raw_size, id=2
		blob.append(self.makeVarIdent("V", 2))
		blob.append(int2str(len(nodePrimitiveBlock)))
		# zlib_data, id=3
		zlib_data = zlib.compress(nodePrimitiveBlock)
		blob.append(self.makeVar("S", 3, zlib_data))
		return join(blob)

	def makeStringTable(self, stringList):
		"""takes a list of str objects and returns a stringtable variable.
		"""
		# s, id=1
		return join([self.makeVar("S", 1, writableString(s)) for s in stringList])

	def makeNodePrimitiveBlock(self, startNodeId, nodes):
		nodePrimitiveBlock = []
		# stringtable, id=1
		stringtable = self.makeStringTable(["", ])
		nodePrimitiveBlock.append(self.makeVar("S", 1, stringtable))
		# primitivegroup, id=2
		nodePrimitiveGroup = self.makeNodePrimitiveGroup(
			startNodeId, nodes)
		nodePrimitiveBlock.append(self.makeVar("S", 2, nodePrimitiveGroup))
		# granularity, id=17
		nodePrimitiveBlock.append(self.makeVar("V", 17, self.granularity, int2str))
		# date_granularity, id=18
		nodePrimitiveBlock.append(self.makeVar("V", 18, self.date_granularity, int2str))
		# lat_offset, id=19
		nodePrimitiveBlock.append(self.makeVar("V", 19, 0, int2str))
		# lon_offset, id=20
		nodePrimitiveBlock.append(self.makeVar("V", 20, 0, int2str))
		return join(nodePrimitiveBlock)

	def makeNodePrimitiveGroup(self, startNodeId, nodes):
		denseNodes = self.makeDenseNodes(startNodeId, nodes)
		# dense, id=2
		return self.makeVar("S", 2, denseNodes)

	def makeDenseInfo(self, times):
		denseInfo = []
		# version, id=1
		version = int2str(1)*times
		denseInfo.append(self.makeVar("S", 1, version))
		# timestamp, id=2
		timestamp = sint2str(self.timestamp)+(sint2str(0)*(times-1))
		denseInfo.append(self.makeVar("S", 2, timestamp))
		# changeset, id=3
		changeset = sint2str(1)*times
		denseInfo.append(self.makeVar("S", 3, changeset))
		# uid, id=4
		uid = sint2str(0)*times
		denseInfo.append(self.makeVar("S", 4, uid))
		# user_sid, id=5
		user_sid = sint2str(0)*times
		denseInfo.append(self.makeVar("S", 5, user_sid))
		return join(denseInfo)

	def makeDenseNodes(self, startNodeId, nodeList):
		dense = []
		Lon = [nodeList[0][0]//self.granularity, ]
		Lat = [nodeList[0][1]//self.granularity, ]
		last_lon = Lon[0]
		last_lat = Lat[0]
		for lon, lat in nodeList[1:]:
			lon = lon//self.granularity
			lat = lat//self.granularity
			lon_diff = lon - last_lon
			lat_diff = lat - last_lat
			Lon.append(lon_diff)
			Lat.append(lat_diff)
			last_lon = lon
			last_lat = lat
		# id, id=1
		id = sint2str(startNodeId)+sint2str(1)*(len(Lon)-1)
		dense.append(self.makeVar("S", 1, id))
		# denseinfo, id=5
		dense.append(self.makeVar("S", 5, self.makeDenseInfo(len(Lon))))
		# lat, id=8
		LAT = join([sint2str(l) for l in Lat])
		dense.append(self.makeVar("S", 8, LAT))
		# lon, id=9
		LON = join([sint2str(l) for l in Lon])
		dense.append(self.makeVar("S", 9, LON))
		return join(dense)

	def writeWays(self, ways, startWayId):
		"""writes ways to self.outf.  ways shall be a list of
		(<startNodeId>, <length>, <isCycle>, <elevation>) tuples.

		The waylist is split up to make sure the pbf blobs will not be too big.
		"""
		curWays = []
		curNumOfNodes = 0
		for ind, way in enumerate(ways):
			length = way[1]
			if curNumOfNodes+length > self.maxNodesPerWayBlock:
				self.writeWaysChunk(curWays, startWayId+ind-len(curWays))
				curNumOfNodes = length
				curWays = [way, ]
			else:
				curWays.append(way)
				curNumOfNodes += length
		else:
			if len(curWays) > 0:
				self.writeWaysChunk(curWays, startWayId+len(ways)-len(curWays))

	def writeWaysChunk(self, ways, startWayId):
		blobHeader = []
		# type, id=1
		blobHeader.append(self.makeVar(vType="S", vId=1,
			content=writableString("OSMData")))
		# datasize, id=3
		blobHeader.append(self.makeVarIdent(vType="V", vId=3))
		blob = self.makeWayBlob(startWayId, ways)
		blobHeader.append(int2str(len(blob)))
		blobHeader = join(blobHeader)
		self.outf.write(pack('!L', len(blobHeader)))
		self.outf.write(blobHeader)
		self.outf.write(blob)

	def makeWayBlob(self, startWayId, ways):
		blob = []
		wayPrimitiveBlock = self.makeWayPrimitiveBlock(startWayId, ways)
		# raw_size, id=2
		blob.append(self.makeVarIdent("V", 2))
		blob.append(int2str(len(wayPrimitiveBlock)))
		# zlib_data, id=3
		zlib_data = zlib.compress(wayPrimitiveBlock)
		blob.append(self.makeVar("S", 3, zlib_data))
		return join(blob)

	def makeWayPrimitiveBlock(self, startWayId, ways):
		wayPrimitiveBlock = []
		strings = []
		wayPrimitiveGroup = self.makeWayPrimitiveGroup(
			startWayId, ways, strings)
		stringtable = self.makeStringTable(strings)
		# stringtable, id=1
		wayPrimitiveBlock.append(self.makeVar("S", 1, stringtable))
		# primitivegroup, id=2
		wayPrimitiveBlock.append(self.makeVar("S", 2, wayPrimitiveGroup))
		# granularity, id=17
		wayPrimitiveBlock.append(self.makeVar("V", 17, self.granularity, int2str))
		# date_granularity, id=18
		wayPrimitiveBlock.append(self.makeVar("V", 18, self.date_granularity, int2str))
		# lat_offset, id=19
		wayPrimitiveBlock.append(self.makeVar("V", 19, 0, int2str))
		# lon_offset, id=20
		wayPrimitiveBlock.append(self.makeVar("V", 20, 0, int2str))
		return join(wayPrimitiveBlock)

	def makeWayPrimitiveGroup(self, startWayId, ways, stringtable):
		ways = self.makeWays(startWayId, ways, stringtable)
		# ways, id=3
		return join([self.makeVar("S", 3, w) for w in ways])

	def makeWays(self, startWayId, wayList, strings):
		strings.append("")                 # 0
		strings.append("ele")              # 1
		strings.append("contour")          # 2
		strings.append("elevation")        # 3
		strings.append("contour_ext")      # 4
		strings.append("elevation_minor")  # 5
		strings.append("elevation_medium") # 6
		strings.append("elevation_major")  # 7
		ways = []
		for ind, w in enumerate(wayList):
			wId = startWayId+ind
			ways.append(self.makeWay(w, wId, strings))
		return ways

	def makeWay(self, w, wayId, strings):
		way = []
		startNodeId, length, isCycle, elevation = w
		if not str(elevation) in strings:
			strings.append(str(elevation))
		# id, id=1
		way.append(self.makeVar("V", 1, wayId, int2str))
		# keys, id=2
		keys = join([int2str(el) for el in [1, 2, 4]])
		way.append(self.makeVar("S", 2, keys))
		# ways, id=3
		vals = join([int2str(el) for el in [strings.index(str(elevation)),
			3, strings.index(self.elevClassifier(elevation))]])
		way.append(self.makeVar("S", 3, vals))
		# info, id=4
		info = self.makeWayInfo()
		way.append(self.makeVar("S", 4, info))
		# refs, id=8
		refs = sint2str(startNodeId)+sint2str(1)*(length-1)
		if isCycle:
			refs += sint2str(-(length-1))
		way.append(self.makeVar("S", 8, refs))
		return join(way)

	def makeWayInfo(self):
		info = []
		# version, id=1
		info.append(self.makeVar("V", 1, 1, int2str))
		# timestamp, id=2
		info.append(self.makeVar("V", 2, self.timestamp, int2str))
		# changeset, id=3
		info.append(self.makeVar("V", 3, 1, int2str))
		# uid, id=4
		info.append(self.makeVar("V", 4, 0, int2str))
		# user_sid, id=5
		info.append(self.makeVar("V", 5, 0, int2str))
		return join(info)

	def write(self, nodeString):
		"""wrapper imitating osmUtil.Output's write method.
		"""
		startNodeId, nodes = eval(nodeString.strip())
		self.writeNodes(nodes, startNodeId)

	def flush(self):
		self.outf.flush()

	def done(self):
		self.__del__()

	def __del__(self):
		self.outf.close()


class Id(object):
	"""a counter, constructed with the first number to return.

	Count using the getId method.
	"""
	def __init__(self, offset):
		self.curId = offset

	def getId(self):
		self.curId += 1
		return self.curId-1


def _makePoints(path, elevation, IDCounter):
	ids, nodes = [], []
	for lon, lat in path:
		IDCounter.curId += 1
		nodes.append((int(lon*NANO), int(lat*NANO)))
		ids.append(IDCounter.curId-1)
	if numpy.all(path[0]==path[-1]):  # close contour
		del nodes[-1]  # remove last node
		del ids[-1]
		ids.append(ids[0])
		IDCounter.curId -= 1
	return nodes, ids

def _makeNodesWays(contourList, elevation, IDCounter):
	ways = []
	nodes = []
	for path in contourList:
		newNodes, nodeRefs = _makePoints(path, elevation, IDCounter)
		nodes.extend(newNodes)
		if nodeRefs[0] == nodeRefs[-1]:
			ways.append((nodeRefs[0], len(nodeRefs)-1, True, elevation))
		else:
			ways.append((nodeRefs[0], len(nodeRefs), False, elevation))
	return nodes, ways

def writeNodes(output, contourData, elevations, timestampString, # dummy option
	opts):
	IDCounter = Id(opts.startId)
	ways = []
	nodes = []
	startId = opts.startId
	for elevation in elevations:
		contourList = contourData.trace(elevation)[0]
		if not contourList:
			continue
		newNodes, newWays = _makeNodesWays(contourList, elevation, IDCounter)
		ways.extend(newWays)
		nodes.extend(newNodes)
		if len(nodes) > 32000:
			output.write(str((startId, nodes))+"\n")
			output.flush()
			startId = IDCounter.curId
			nodes = []
	#newId = opts.startId + len(nodes)#sum([length for _, length, _, _ in ways])
	newId = IDCounter.getId()
	if len(nodes) > 0:
		output.write(str((startId, nodes))+"\n")
		output.flush()
	return newId, ways

