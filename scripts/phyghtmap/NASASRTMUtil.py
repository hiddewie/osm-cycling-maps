from __future__ import print_function

__author__ = "Adrian Dempwolff (phyghtmap@aldw.de)"
__version__ = "2.23"
__copyright__ = "Copyright (c) 2009-2021 Adrian Dempwolff"
__license__ = "GPLv2+"

import sys
import urllib
from http import cookiejar as cookielib
import base64
import os
from bs4 import BeautifulSoup
import zipfile
from matplotlib import __version__ as mplversion
if mplversion < "1.3.0":
	from matplotlib.nxutils import points_inside_poly
else:
	from matplotlib.path import Path as PolygonPath
import numpy


class NASASRTMUtilConfigClass(object):
	"""The config is stored in a class, to be configurable from outside

	Don't change configuration during usage, only at the beginning!
	You can use the member call CustomHgtSaveDir for configuration from outside:
  NASASRTMUtil.NASASRTMUtilConfig.CustomHgtSaveDir(custom_hgt_directory)
  """

	# C'Tor setting the defaults
	def __init__(self):
		# Set the default ght directory
		self.CustomHgtSaveDir("hgt")
		# Other config
		############################################################
		### NASA SRTM specific variables ###########################
		############################################################
		self.NASAhgtFileDirs = {3: ["Africa", "Australia", "Eurasia", "Islands",
			"North_America", "South_America"],
			1: ["Region_0{0:d}".format(i) for i in range(1, 8)]}
		self.NASAhgtSaveSubDirRe = "SRTM{0:d}v{1:.1f}"
		self.earthexplorerUser = None
		self.earthexplorerPassword = None
		############################################################
		### www.vierfinderpanoramas.org specific variables #########
		############################################################
		self.VIEWfileDictPageRe = "http://www.viewfinderpanoramas.org/Coverage%20map%20viewfinderpanoramas_org{0:d}.htm"
		self.VIEWhgtSaveSubDirRe = "VIEW{0:d}"

	def getSRTMFileServer(self, resolution, srtmVersion):
		if srtmVersion == 2.1:
			return "https://dds.cr.usgs.gov/srtm/version2_1/SRTM{0:d}".format(resolution)
		elif srtmVersion == 3.0:
			if resolution == 1:
				urlRe = "https://earthexplorer.usgs.gov/download/5e83a3efe0103743/SRTM1{:s}V3/EE"
			elif resolution == 3:
				urlRe = "https://earthexplorer.usgs.gov/download/5e83a43cb348f8ec/SRTM3{:s}V2/EE"
			return urlRe

	def getSRTMIndexUrl(self, resolution, srtmVersion):
		if srtmVersion == 2.1:
			return self.getSRTMFileServer(resolution, srtmVersion)
		elif srtmVersion == 3.0:
			indexServerUrl = "https://dds.cr.usgs.gov/ee-data/coveragemaps/kml/ee/srtm_v3_srtmgl{:d}.kml".format(
				resolution)
			return indexServerUrl

	def CustomHgtSaveDir(self, directory):
		"""Set a custom directory to store the hgt files

		<directory>:  Directory to use
		"""
		############################################################
		### general config variables ###############################
		############################################################
		# Default value
		self.hgtSaveDir = directory
		self.NASAhgtIndexFileRe = os.path.join(self.hgtSaveDir,
			"hgtIndex_{0:d}_v{1:.1f}.txt")
		self.VIEWhgtIndexFileRe = os.path.join(self.hgtSaveDir,
			"viewfinderHgtIndex_{0:d}.txt")

	def earthexplorerCredentials(self, user, password):
		self.earthexplorerUser = user
		self.earthexplorerPassword = password

# Create the config object
NASASRTMUtilConfig = NASASRTMUtilConfigClass()

texAreas = []

def calcBbox(area, corrx=0.0, corry=0.0):
	"""calculates the appropriate bouding box for the needed files
	"""
	minLon, minLat, maxLon, maxLat = [float(value)-inc for value, inc in
		zip(area.split(":"), [corrx, corry, corrx, corry])]
	if minLon < 0:
		if minLon % 1 == 0:
			bboxMinLon = int(minLon)
		else:
			bboxMinLon = int(minLon) - 1
	else:
		bboxMinLon = int(minLon)
	if minLat < 0:
		if minLat % 1 == 0:
			bboxMinLat = int(minLat)
		else:
			bboxMinLat = int(minLat) - 1
	else:
		bboxMinLat = int(minLat)
	if maxLon < 0:
		bboxMaxLon = int(maxLon)
	else:
		if maxLon % 1 == 0:
			bboxMaxLon = int(maxLon)
		else:
			bboxMaxLon = int(maxLon) + 1
	if maxLat < 0:
		bboxMaxLat = int(maxLat)
	else:
		if maxLat % 1 == 0:
			bboxMaxLat = int(maxLat)
		else:
			bboxMaxLat = int(maxLat) + 1
	return bboxMinLon, bboxMinLat, bboxMaxLon, bboxMaxLat

"""
def writeTex(milo, mila, malo, mala, color):
	texAreas.append("{0:s}/{1:.2f}/{2:.2f}/{3:.2f}/{4:.2f}".format(
		color, milo, mila, malo, mala))
"""

def getLowInt(n):
	if n%1==0:
		return int(n)
	if n < 0:
		return int(n)-1
	else:
		return int(n)

def getHighInt(n):
	if n < 0 or n%1==0:
		return int(n)
	else:
		return int(n)+1

def getCloseInt(n):
	a = getHighInt(n)
	b = getLowInt(n)
	da = abs(n - a)
	db = abs(n - b)
	if da < db:
		return a
	else:
		return b

def getRange(a, b):
	a, b = sorted([a, b])
	l, h = getHighInt(a), getHighInt(b)
	return range(l, h)

def intersecTiles(polygonList, corrx, corry):
	if not polygonList:
		return []
	secs = []
	for polygon in polygonList:
		x_last, y_last = polygon[0]
		x_last -= corrx
		y_last -= corry
		for x, y in polygon[1:]:
			x -= corrx
			y -= corry
			secs.append((getLowInt(x), getLowInt(y)))
			if x-x_last == 0:
				# vertical vertex, don't calculate s
				secs.extend([(getLowInt(x), getLowInt(Y)) for Y in getRange(
					y, y_last)])
			elif y-y_last == 0:
				# horizontal vertex
				secs.extend([(getLowInt(X), getLowInt(y)) for X in getRange(
					x, x_last)])
			else:
				s = (y-y_last)/(x-x_last)
				o = y_last-x_last*s
				for X in getRange(x, x_last):
					# determine intersections with latitude degrees
					Y = getLowInt(s*X+o)
					secs.append((X-1, Y)) # left
					secs.append((X, Y)) # right
				for Y in getRange(y, y_last):
					# determine intersections with longitude degrees
					X = getLowInt((Y-o)/s)
					secs.append((X, Y-1)) # below
					secs.append((X, Y)) # above
			x_last, y_last = x, y
	return [makeFileNamePrefix(x, y) for x, y in set(secs)]

def areaNeeded(lat, lon, bbox, polygon, corrx, corry):
	"""checks if a source file is needed depending on the bounding box and
	the passed polygon.
	"""
	if polygon==None:
		return True, False
	minLat = lat + corry
	maxLat = minLat + 1
	minLon = lon + corrx
	maxLon = minLon + 1
	MinLon, MinLat, MaxLon, MaxLat = bbox
	MinLon += corrx
	MaxLon += corrx
	MinLat += corry
	MaxLat += corry
	print("checking if area {0:s} intersects with polygon ...".format(
		makeFileNamePrefix(lon, lat)), end=" ")
	if minLon==MinLon and minLat==MinLat and maxLon==MaxLon and maxLat==MaxLat:
		# the polygon is completely inside the bounding box
		print("yes")
		#writeTex(lon, lat, lon+1, lat+1, "green")
		return True, True
	# the area is not or completely inside one of the polygons passed to
	# <polygon>.  We just look if the corners are inside the polygons.
	points = []
	for lo in [minLon, maxLon]:
		for la in [minLat, maxLat]:
			points.append((lo, la))
	inside = numpy.zeros((1, 4))
	for p in polygon:
		if mplversion < "1.3.0":
			inside += points_inside_poly(points, p)
		else:
			inside += PolygonPath(p).contains_points(points)
	if numpy.all(inside):
		# area ist completely inside
		print("yes")
		#writeTex(lon, lat, lon+1, lat+1, "green")
		return True, False
	elif not numpy.any(inside):
		# area is completely outside
		print("no")
		#writeTex(lon, lat, lon+1, lat+1, "red")
		return False, False
	else:
		# This only happens it a polygon vertex is on the tile border.
		# Because in this case points_inside_poly() returns unpredictable
		# results, we better return True here.
		print("maybe")
		#writeTex(lon, lat, lon+1, lat+1, "pink")
		return True, True

def makeFileNamePrefix(lon, lat):
	if lon < 0:
		lonSwitch = "W"
	else:
		lonSwitch = "E"
	if lat < 0:
		latSwitch = "S"
	else:
		latSwitch = "N"
	return "{0:s}{1:0>2d}{2:s}{3:0>3d}".format(latSwitch, abs(lat),
		lonSwitch, abs(lon))

def makeFileNamePrefixes(bbox, polygon, corrx, corry, lowercase=False):
	"""generates a list of filename prefixes of the files containing data within the
	bounding box.
	"""
	minLon, minLat, maxLon, maxLat = bbox
	lon = minLon
	intersecAreas = intersecTiles(polygon, corrx, corry)
	prefixes = []
	if minLon > maxLon:
		# bbox covers the W180/E180 longitude
		lonRange = range(minLon, 180) + range(-180, maxLon)
	else:
		lonRange = range(minLon, maxLon)
	for lon in lonRange:
		for lat in range(minLat, maxLat):
			fileNamePrefix = makeFileNamePrefix(lon, lat)
			if fileNamePrefix in intersecAreas:
				prefixes.append((fileNamePrefix, True))
				#writeTex(lon, lat, lon+1, lat+1, "blue")
			else:
				needed, checkPoly = areaNeeded(lat, lon, bbox, polygon, corrx, corry)
				if needed:
					prefixes.append((fileNamePrefix, checkPoly))
	if lowercase:
		return [(p.lower(), checkPoly) for p, checkPoly in prefixes]
	else:
		return prefixes

def parseSRTMv3CoverageKml(kmlContents):
	polygons = []
	polygonSoup = BeautifulSoup(kmlContents, "lxml").findAll("polygon")
	for p in polygonSoup:
		for c in p.findAll("coordinates"):
			for cont in c.contents:
				coords = [el for el in cont.split() if el.strip()]
				polygons.append([
					(float(coord.split(",")[0]), float(coord.split(",")[1]))
					for coord in coords])
	return polygons

def getSRTMv3Areas(polygons):
	rawAreas = []
	for p in polygons:
		lons = sorted([el[0] for el in p])
		lats = sorted([el[1] for el in p])
		minLonRaw = lons[0]
		maxLonRaw = lons[-1]
		minLatRaw = lats[0]
		maxLatRaw = lats[-1]
		minLon = getCloseInt(minLonRaw)
		maxLon = getCloseInt(maxLonRaw)
		minLat = getCloseInt(minLatRaw)
		maxLat = getCloseInt(maxLatRaw)
		for lon in numpy.arange(minLon+0.5, maxLon, 1.0):
			for lat in numpy.arange(minLat+0.5, maxLat, 1.0):
				points = [(lon, lat), ]
				if mplversion < "1.3.0":
					inside = points_inside_poly(points, p)
				else:
					inside = PolygonPath(p).contains_points(points)
				if numpy.all(inside):
					areaName = makeFileNamePrefix(getLowInt(lon), getLowInt(lat))
					rawAreas.append(areaName)
	# some tiles are located in holes and may have been wrongly identified
	# as lying inside a polygon.  To eliminate those entries, only elements
	# occuring an odd number of times are kept
	areas = []
	for area in rawAreas:
		nOccurrences = rawAreas.count(area)
		if nOccurrences % 2 == 1 and not area in areas:
			areas.append(area)
	return sorted(areas)
	
def makeNasaHgtIndex(resolution, srtmVersion):
	"""generates an index file for the NASA SRTM server.
	"""
	hgtIndexFile = NASASRTMUtilConfig.NASAhgtIndexFileRe.format(resolution,
		srtmVersion)
	if srtmVersion == 2.1:
		hgtIndexFileOldName = hgtIndexFile[:-9] + hgtIndexFile[-4:]
		# we know that <hgtIndexFile> does not exist because else this function would
		# not have been called
		# so we look if there is a file with the old index filename and if yes, we
		# rename it
		try:
			os.stat(hgtIndexFileOldName)
			if os.path.isfile(hgtIndexFileOldName):
				# this is a regular file, so we rename it
				os.rename(hgtIndexFileOldName, hgtIndexFile)
				# we don't need to return something special
				print("Renamed old index file '{0:s}' to '{0:s}'.".format(
					hgtIndexFileOldName, hgtIndexFile))
				return
		except:
			# there is no old index file, so continue in this function and write a new
			# one
			pass
	hgtIndexUrl = NASASRTMUtilConfig.getSRTMIndexUrl(resolution, srtmVersion)
	print("generating index in {0:s} ...".format(hgtIndexFile), end=" ")
	try:
		index = open(hgtIndexFile, 'w')
	except:
		print()
		raise IOError("could not open {0:s} for writing".format(hgtIndexFile))
	index.write("# SRTM{0:d}v{1:.1f} index file, VERSION={2:d}\n".format(resolution,
		srtmVersion, desiredIndexVersion["srtm{0:d}v{1:.1f}".format(resolution, srtmVersion)]))
	if srtmVersion == 2.1:
		for continent in NASASRTMUtilConfig.NASAhgtFileDirs[resolution]:
			index.write("[{0:s}]\n".format(continent))
			url = "/".join([hgtIndexUrl, continent])
			continentHtml = urllib.request.urlopen(url).read()
			continentSoup = BeautifulSoup(continentHtml, "lxml")
			anchors = continentSoup.findAll("a")
			for anchor in anchors:
				if anchor.contents[0].endswith("hgt.zip"):
					zipFilename = anchor.contents[0].strip()
					index.write("{0:s}\n".format(zipFilename))
	elif srtmVersion == 3.0:
		indexKml = urllib.request.urlopen(hgtIndexUrl).read()
		polygons = parseSRTMv3CoverageKml(indexKml)
		areas = getSRTMv3Areas(polygons)
		for area in areas:
			index.write("{:s}\n".format(area))
	print("DONE")

def writeViewIndex(resolution, zipFileDict):
	hgtIndexFile = NASASRTMUtilConfig.VIEWhgtIndexFileRe.format(resolution)
	try:
		index = open(hgtIndexFile, 'w')
	except:
		print()
		raise IOError("could not open {0:s} for writing".format(hgtIndexFile))
	index.write("# VIEW{0:d} index file, VERSION={1:d}\n".format(resolution,
		desiredIndexVersion["view{0:d}".format(resolution)]))
	for zipFileUrl in sorted(zipFileDict):
		index.write("[{0:s}]\n".format(zipFileUrl))
		for areaName in zipFileDict[zipFileUrl]:
			index.write(areaName + "\n")
	index.close()
	print("DONE")

def makeViewHgtIndex(resolution):
	"""generates an index file for the viewfinder hgt files.
	"""
	def calcAreaNames(coordTag, resolution):
		if resolution == 3:
			viewfinderGraphicsDimension = 1800.0/360.0
		else:
			viewfinderGraphicsDimension = 1800.0/360.0
		l, t, r, b = [int(c) for c in coordTag.split(",")]
		w = int(l / viewfinderGraphicsDimension + 0.5) - 180
		e = int(r / viewfinderGraphicsDimension + 0.5) - 180
		s = 90 - int(b / viewfinderGraphicsDimension + 0.5)
		n = 90 - int(t / viewfinderGraphicsDimension + 0.5)
		names = []
		for lon in range(w, e):
			for lat in range(s, n):
				if lon < 0:
					lonName = "W{0:0>3d}".format(-lon)
				else:
					lonName = "E{0:0>3d}".format(lon)
				if s < 0:
					latName = "S{0:0>2d}".format(-lat)
				else:
					latName = "N{0:0>2d}".format(lat)
				name = "".join([latName, lonName])
				names.append(name)
		return names

	hgtIndexFile = NASASRTMUtilConfig.VIEWhgtIndexFileRe.format(resolution)
	hgtDictUrl = NASASRTMUtilConfig.VIEWfileDictPageRe.format(resolution)
	zipFileDict = {}
	for a in BeautifulSoup(urllib.request.urlopen(hgtDictUrl).read(), "lxml").findAll("area"):
		areaNames = calcAreaNames(a["coords"], resolution)
		zipFileUrl = a["href"].strip()
		if not zipFileUrl in zipFileDict:
			zipFileDict[zipFileUrl] = []
		zipFileDict[zipFileUrl].extend(sorted([aName.upper() for aName in
			areaNames]))
	print("generating index in {0:s} ...".format(hgtIndexFile), end=" ")
	writeViewIndex(resolution, zipFileDict)

def updateViewIndex(resolution, zipFileUrl, areaList):
	"""cleans up the viewfinder index.
	"""
	hgtIndexFile = NASASRTMUtilConfig.VIEWhgtIndexFileRe.format(resolution)
	try:
		os.stat(hgtIndexFile)
	except:
		print("Cannot update index file {0:s} because it's not there.".format(hgtIndexFile))
		return
	index = getIndex(hgtIndexFile, "view{0:d}".format(resolution))
	zipFileDict = {}
	for line in index:
		if line.startswith("["):
			url = line[1:-1]
			if not url in zipFileDict:
				zipFileDict[url] = []
		else:
			zipFileDict[url].append(line)
	if not zipFileUrl in zipFileDict:
		print("No such url in zipFileDict: {0:s}".format(zipFileUrl))
		return
	if sorted(zipFileDict[zipFileUrl]) != sorted(areaList):
		zipFileDict[zipFileUrl] = sorted(areaList)
		print("updating index in {0:s} ...".format(hgtIndexFile))
		writeViewIndex(resolution, zipFileDict)

def makeIndex(indexType):
	if indexType == "srtm1v2.1":
		makeNasaHgtIndex(1, 2.1)
	elif indexType == "srtm3v2.1":
		makeNasaHgtIndex(3, 2.1)
	elif indexType == "srtm1v3.0":
		makeNasaHgtIndex(1, 3.0)
	elif indexType == "srtm3v3.0":
		makeNasaHgtIndex(3, 3.0)
	elif indexType == "view1":
		makeViewHgtIndex(1)
	elif indexType == "view3":
		makeViewHgtIndex(3)

desiredIndexVersion = {
	"srtm1v2.1": 1,
	"srtm3v2.1": 2,
	"srtm1v3.0": 2,
	"srtm3v3.0": 2,
	"view1": 2,
	"view3": 4,
}

def rewriteIndices():
	for indexType in desiredIndexVersion.keys():
		makeIndex(indexType)

def getIndex(filename, indexType):
	index = open(filename, 'r').readlines()
	for l in index:
		if l.startswith("#"):
			indexVersion = int(l.replace("#",
				"").strip().split()[-1].split("=")[-1])
			break
	else:
		indexVersion = 1
	if indexVersion != desiredIndexVersion[indexType]:
		print("Creating new version of index file for source {0:s}.".format(indexType))
		makeIndex(indexType)
	index = [l.strip() for l in open(filename, 'r').readlines() if not l.startswith("#")]
	index = [l for l in index if l]
	return index

def getNASAUrl(area, resolution, srtmVersion):
	"""determines the NASA download url for a given area.
	"""
	hgtIndexFile = NASASRTMUtilConfig.NASAhgtIndexFileRe.format(resolution,
		srtmVersion)
	hgtFileServer = NASASRTMUtilConfig.getSRTMFileServer(resolution, srtmVersion)
	try:
		os.stat(hgtIndexFile)
	except:
		makeNasaHgtIndex(resolution, srtmVersion)
	# index rewriting if out of date happens in getIndex()
	index = getIndex(hgtIndexFile, "srtm{0:d}v{1:.1f}".format(resolution, srtmVersion))
	# the index is up to date now
	if srtmVersion == 2.1:
		file = "{0:s}.hgt.zip".format(area)
		fileFaulty = "{0:s}hgt.zip".format(area)
		fileMap = {}
		for line in index:
			if line.startswith("["):
				continent = line[1:-1]
			else:
				fileMap[line] = continent
		if file in fileMap:
			url = '/'.join([hgtFileServer, fileMap[file], file])
			return url
		elif fileFaulty in fileMap:
			url = '/'.join([hgtFileServer, fileMap[fileFaulty], fileFaulty])
			return url
		else:
			return None
	elif srtmVersion == 3.0:
		for line in index:
			if line.split(".")[0].lower() == area.lower():
				url = hgtFileServer.format(area)
				return url
		else:
			# no such area in index
			return None

def getViewUrl(area, resolution):
	"""determines the viewfinder download url for a given area.
	"""
	hgtIndexFile = NASASRTMUtilConfig.VIEWhgtIndexFileRe.format(resolution)
	try:
		os.stat(hgtIndexFile)
	except:
		makeViewHgtIndex(resolution)
	index = getIndex(hgtIndexFile, "view{0:d}".format(resolution))
	for line in index:
		if line.startswith("[") and line.endswith("]"):
			url = line[1:-1]
		elif line == area:
			return url
	return None

def unzipFile(saveZipFilename, area):
	"""unzip a zip file.
	"""
	print("{0:s}: unzipping file {1:s} ...".format(area, saveZipFilename))
	zipFile = zipfile.ZipFile(saveZipFilename)
	areaNames = []
	for name in zipFile.namelist():
		if os.path.splitext(name)[1].lower() != ".hgt":
			continue
		areaName = os.path.splitext(os.path.split(name)[-1])[0].upper().strip()
		if not areaName:
			continue
		areaNames.append(areaName)
		saveFilename = os.path.join(os.path.split(saveZipFilename)[0],
			areaName + ".hgt")
		saveFile = open(saveFilename, 'wb')
		saveFile.write(zipFile.read(name))
		saveFile.close()
	# destruct zipFile before removing it.  removing otherwise fails under windows
	zipFile.__del__()
	os.remove(saveZipFilename)
	#print("DONE")
	return areaNames

"""
def makePolygonCoords(polygonList):
	pathList = []
	for polygon in polygonList:
		coords = []
		for lon, lat in polygon:
			coords.append("({0:.7f}, {1:.7f})".format(lon, lat))
		pathList.append("\\draw[line width=2pt] plot coordinates{{{0:s}}} --cycle;".format(" ".join(coords)))
	return "\n\t".join(pathList)
"""

def mkdir(dirName):
	try:
		os.stat(dirName)
	except:
		os.mkdir(dirName)

def getDirNames(source):
	resolution = int(source[4])
	if source.startswith("srtm"):
		srtmVersion = float(source[6:])
		hgtSaveSubDir = os.path.join(NASASRTMUtilConfig.hgtSaveDir,
			NASASRTMUtilConfig.NASAhgtSaveSubDirRe.format(resolution, srtmVersion))
	elif source.startswith("view"):
		hgtSaveSubDir = os.path.join(NASASRTMUtilConfig.hgtSaveDir,
			NASASRTMUtilConfig.VIEWhgtSaveSubDirRe.format(resolution))
	return NASASRTMUtilConfig.hgtSaveDir, hgtSaveSubDir

def initDirs(sources):
	mkdir(NASASRTMUtilConfig.hgtSaveDir)
	for source in sources:
		sourceType, sourceResolution = source[:4], int(source[4])
		if sourceType == "srtm":
			srtmVersion = float(source[6:])
			NASAhgtSaveSubDir = os.path.join(NASASRTMUtilConfig.hgtSaveDir,
				NASASRTMUtilConfig.NASAhgtSaveSubDirRe.format(sourceResolution, srtmVersion))
			if srtmVersion == 2.1:
				NASAhgtSaveSubDirOldName = NASAhgtSaveSubDir[:-4]
				try:
					# look if there is a directory with the old SRTM directory name
					os.stat(NASAhgtSaveSubDirOldName)
					if os.path.isdir(NASAhgtSaveSubDirOldName):
						try:
							# there is an old SRTM directory.  Rename it to the new name if
							# there is no such file or directory
							os.stat(NASAhgtSaveSubDir)
						except:
							# no new directory, so rename the old one to the new name
							os.rename(NASAhgtSaveSubDirOldName, NASAhgtSaveSubDir)
							print("Renamed the old hgt cache directory '{0:s}' to '{1:s}'.".format(
								NASAhgtSaveSubDirOldName, NASAhgtSaveSubDir))
				except OSError:
					# there is no directory with the old SRTM directory name
					pass
			# we can try the create the directory no matter if we already renamed
			# an old directory to this name
			mkdir(NASAhgtSaveSubDir)
		elif sourceType == "view":
			VIEWhgtSaveSubDir = os.path.join(NASASRTMUtilConfig.hgtSaveDir,
				NASASRTMUtilConfig.VIEWhgtSaveSubDirRe.format(sourceResolution))
			mkdir(VIEWhgtSaveSubDir)

def base64String(string):
	return base64.encodestring(string.encode()).decode()

def earthexplorerLogin():
	jar = cookielib.CookieJar(cookielib.DefaultCookiePolicy())
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
	opener.open("https://ers.cr.usgs.gov/") # needed for some cookies
	postData = {
		'username': NASASRTMUtilConfig.earthexplorerUser,
		'password': NASASRTMUtilConfig.earthexplorerPassword,
	}
	req1 = urllib.request.Request("https://ers.cr.usgs.gov/login/")
	res1 = opener.open(req1)
	formSoup = BeautifulSoup(res1.read(), "lxml").find("form", {"id": "loginForm"})
	for i in formSoup.findAll("input", {"type": "hidden"}):
		postData[i.attrs["name"]] = i.attrs["value"]
	encodedPostData = bytes(urllib.parse.urlencode(postData), "utf-8")
	req2 = urllib.request.Request("https://ers.cr.usgs.gov/login/", data=encodedPostData, method='POST')
	res2 = opener.open(req2)
	return opener

def downloadToFile_SRTMv3(url, filename):
	opener = earthexplorerLogin()
	# earthexplorer servers yield HTTP error 500 for some specific files like,
	# e.g.,  https://earthexplorer.usgs.gov/download/4960/SRTM3S11W139V2/GEOTIFF3/EE
	try:
		res = opener.open(url)
	except urllib.error.HTTPError as e:
		sys.stderr.write("\t: Error downloading file {0:s}, reason: {1:s}.\n".format(
			os.path.split(filename)[1], e.reason))
		return False
	open(filename, "wb").write(res.read())

def downloadToFile_Simple(url, filename):
	res = urllib.request.urlopen(url)
	open(filename, "wb").write(res.read())

def downloadToFile(url, filename, source):
	sourceType, sourceResolution = source[:4], int(source[4])
	if sourceType == "srtm":
		srtmVersion = float(source[6:])
		if srtmVersion == 3.0:
			return downloadToFile_SRTMv3(url, filename)
	return downloadToFile_Simple(url, filename)

def downloadAndUnzip(url, area, source):
	if source.lower().startswith("srtm") and "v3.0" in source.lower():
		return downloadAndUnzip_Tif(url, area, source)
	else:
		return downloadAndUnzip_Zip(url, area, source)

def downloadAndUnzip_Tif(url, area, source):
	hgtSaveDir, hgtSaveSubDir = getDirNames(source)
	fileResolution = int(source[4])
	oldSaveFilename = os.path.join(hgtSaveSubDir, "{0:s}.hgt".format(area))
	saveFilename = os.path.join(hgtSaveSubDir, "{0:s}.tif".format(area))
	try:
		os.stat(oldSaveFilename)
		print("{0:s}: using file {1:s}.".format(area, oldSaveFilename))
		return oldSaveFilename
	except:
		pass
	try:
		os.stat(saveFilename)
	except:
		print("{0:s}: downloading file {1:s} to {2:s} ...".format(area, url, saveFilename))
		downloadToFile(url, saveFilename, source)
	try:
		os.stat(saveFilename)
		print("{0:s}: using file {1:s}.".format(area, saveFilename))
		return saveFilename
	except Exception as msg:
		print(msg)
		return None

def downloadAndUnzip_Zip(url, area, source):
	hgtSaveDir, hgtSaveSubDir = getDirNames(source)
	fileResolution = int(source[4])
	saveZipFilename = os.path.join(hgtSaveSubDir, url.split("/")[-1])
	saveFilename = os.path.join(hgtSaveSubDir, "{0:s}.hgt".format(area))
	try:
		os.stat(saveFilename)
		wantedSize = 2 * (3600//fileResolution + 1)**2
		foundSize = os.path.getsize(saveFilename)
		if foundSize != wantedSize:
			raise IOError("Wrong size: Expected {0:d}, found {1:d}".format(wantedSize,foundSize))
		print("{0:s}: using existing file {1:s}.".format(area, saveFilename))
		return saveFilename
	except:
		try:
			os.stat(saveZipFilename)
			areaNames = unzipFile(saveZipFilename, area)
			if source.startswith("view"):
				updateViewIndex(fileResolution, url, areaNames)
				viewUrl = getViewUrl(area, fileResolution)
				if not viewUrl:
					return None
				elif not viewUrl==url:
					print("Got the wrong zip file (area found multiple times in index file).")
					return downloadAndUnzip(viewUrl, area, source)
		except:
			print("{0:s}: downloading file {1:s} to {2:s} ...".format(area, url, saveZipFilename))
			downloadToFile(url, saveZipFilename, source)
			try:
				areaNames = unzipFile(saveZipFilename, area)
				if source.startswith("view"):
					updateViewIndex(fileResolution, url, areaNames)
					viewUrl = getViewUrl(area, fileResolution)
					if not viewUrl:
						return None
					elif not viewUrl==url:
						print("Got the wrong zip file (area found multiple times in index file).")
						return downloadAndUnzip(viewUrl, area, source)
			except Exception as msg:
				print(msg)
				print("{0:s}: file {1:s} from {2:s} is not a zip file".format(area, saveZipFilename, url))
	try:
		os.stat(saveFilename)
		wantedSize = 2 * (3600//fileResolution + 1)**2
		foundSize = os.path.getsize(saveFilename)
		if foundSize != wantedSize:
			raise IOError("{0:s}: wrong size: Expected {1:d}, found {2:d}".format(area,
				wantedSize,foundSize))
		print("{0:s}: using file {1:s}.".format(area, saveFilename))
		return saveFilename
	except Exception as msg:
		print(msg)
		return None

def getFile(area, source):
	fileResolution = int(source[4])
	if source.startswith("srtm"):
		srtmVersion = float(source[6:])
		url = getNASAUrl(area, fileResolution, srtmVersion)
	elif source.startswith("view"):
		url = getViewUrl(area, fileResolution)
	if not url:
		return None
	else:
		return downloadAndUnzip(url, area, source)

def getFiles(area, polygon, corrx, corry, sources):
	initDirs(sources)
	bbox = calcBbox(area, corrx, corry)
	areaPrefixes = makeFileNamePrefixes(bbox, polygon, corrx, corry)
	files = []
	for area, checkPoly in areaPrefixes:
		for source in sources:
			print("{0:s}: trying {1:s} ...".format(area, source))
			saveFilename = getFile(area, source)
			if saveFilename:
				files.append((saveFilename, checkPoly))
				break
		else:
			print("{0:s}: no file found on server.".format(area))
			continue
	return files

