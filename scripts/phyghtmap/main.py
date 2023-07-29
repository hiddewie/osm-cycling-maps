#!/usr/bin/python3

#import psyco
#psyco.full()

from __future__ import print_function

__author__ = "Adrian Dempwolff (phyghtmap@aldw.de)"
__version__ = "2.23"
__copyright__ = "Copyright (c) 2009-2021 Adrian Dempwolff"
__license__ = "GPLv2+"

import sys
import os
import select
from optparse import OptionParser
import time

# from phyghtmap import hgt
# from phyghtmap import osmUtil
import NASASRTMUtil
# from phyghtmap import pbfUtil
# from phyghtmap import o5mUtil
# from phyghtmap import configUtil

profile = False

configFilename = os.path.join(os.path.expanduser("~"), ".phyghtmaprc")

def parseCommandLine():
	"""parses the command line.
	"""
	parser = OptionParser(usage="%prog [options] [<hgt or GeoTiff file>] [<hgt or GeoTiff files>]"
    "\nphyghtmap generates contour lines from NASA SRTM and smiliar data"
		"\nas well as from GeoTiff data"
		"\nin OSM formats.  For now, there are three ways to achieve this. First,"
		"\nit can be used to process existing source files given as arguments"
		"\non the command line.  Note that the filenames must have the format"
		"\n[N|S]YY[W|E]XXX.hgt, with YY the latitude and XXX the longitude of the"
		"\nlower left corner of the tile.  Second, it can be used with an area"
		"\ndefinition as input.  The third way to use phyghtmap is to specify a"
		"\npolygon definition.  In the last two cases, phyghtmap will look for a"
		"\ncache directory (per default: ./hgt/) and the needed SRTM files.  If"
		"\nno cache directory is found, it will be created.  It then downloads"
		"\nall the needed NASA SRTM data files automatically if they are not cached"
		"\nyet.  There is also the possibility of masking the NASA SRTM data with"
		"\ndata from www.viewfinderpanoramas.org which fills voids and other data"
		"\nlacking in the original NASA data set.  Since the 3 arc second data available"
		"\nfrom www.viewfinderpanoramas.org is complete for the whole world,"
		"\ngood results can be achieved by specifying --source=view3.  For higher"
		"\nresolution, the 1 arc second SRTM data in version 3.0 can be used by"
		"\nspecifying --source=srtm1 in combination with --srtm-version=3.0. "
		"\nSRTM 1 arc second data is, however, only available for latitudes"
		"\nbetween 59 degrees of latitude south and 60 degrees of latitude north.")
	parser.add_option("-a", "--area", help="choses the area to generate osm SRTM"
		"\ndata for by bounding box. If necessary, files are downloaded from"
		"\nthe NASA server. "
		"\nSpecify as <left>:<bottom>:<right>:<top> in degrees of latitude"
		"\nand longitude, respectively. Latitudes south of the equator and"
		"\nlongitudes west of Greenwich may be given as negative decimal numbers."
		"\nIf this option is given, specified hgt"
		"\nfiles will be omitted.",
	  dest="area", metavar="LEFT:BOTTOM:RIGHT:TOP", action="store", default=None)
	parser.add_option("--polygon", help="use polygon FILENAME as downloaded from"
		"\nhttp://download.geofabrik.de/clipbounds/ as bounds for the output contour"
		"\ndata.  The computation time will be somewhat higher then.  If specified,"
		"\na bounding box passed to the --area option will be ignored.",
		dest="polygon", action="store", metavar="FILENAME", default=None)
	parser.add_option("--download-only", help="only download needed files,"
		"\ndon't write contour data.", action="store_true", default=False,
		dest="downloadOnly")
	parser.add_option("-s", "--step", help="specify contour line step size in"
		"\nmeters or feet, if using the --feet option. The default value is 20.",
		dest="contourStepSize", metavar="STEP", action="store", default='20')
	parser.add_option("-f", "--feet", help="output contour lines in feet steps"
		"\nrather than in meters.", action="store_true", default=False,
		dest="contourFeet")
	parser.add_option("-0", "--no-zero-contour", help="say this, if you don't want"
		"\nthe sea level contour line (0 m) (which sometimes looks rather ugly) to"
		"\nappear in the output.", action="store_true", default=False, dest="noZero")
	parser.add_option("-o", "--output-prefix", help="specify a prefix for the"
		"\nfilenames of the output osm file(s).", dest="outputPrefix",
		metavar="PREFIX", action="store", default=None)
	parser.add_option("-p", "--plot", help="specify the prefix for the files to write"
		"\nlongitude/latitude/elevation data to instead of generating contour"
		"\nosm.", dest="plotPrefix",
		action="store", default=None)
	parser.add_option("-c", "--line-cat", help="specify a string of two comma"
		"\nseperated integers for major and medium elevation categories, e. g."
		"\n'200,100' which is the default. This is needed for fancy rendering.",
		dest="lineCats", metavar="ELEVATION_MAJOR,ELEVATION_MEDIUM", action="store",
		default='200,100')
	parser.add_option("-j", "--jobs", help="number of jobs to be run"
		" in parallel (POSIX only)", dest="nJobs", action="store",
		type="int", default=1)
	parser.add_option("--osm-version", help="pass a number as OSM-VERSION to"
		"\nuse for the output.  The default value is 0.6.  If you need an older"
		"\nversion, try 0.5.",
		metavar="OSM-VERSION", dest="osmVersion", action="store", default=0.6,
		type="float")
	parser.add_option("--write-timestamp", help="write the timestamp attribute of"
		"\nnode and way elements in OSM XML and o5m output.  This might be needed by some"
		"\ninterpreters.  In o5m output, this also triggers writing of changeset and"
		"\nuser information.", dest="writeTimestamp", action="store_true",
		default=False)
	parser.add_option("--start-node-id", help="specify an integer as id of"
		"\nthe first written node in the output OSM xml.  It defaults to 10000000"
		"\nbut some OSM xml mergers are running into trouble when encountering non"
		"\nunique ids.  In this case and for the moment, it is safe to say"
		"\n10000000000 (ten billion) then.", dest="startId", type="int",
		default=10000000, action="store", metavar="NODE-ID")
	parser.add_option("--start-way-id", help="specify an integer as id of"
		"\nthe first written way in the output OSM xml.  It defaults to 10000000"
		"\nbut some OSM xml mergers are running into trouble when encountering non"
		"\nunique ids.  In this case and for the moment, it is safe to say"
		"\n10000000000 (ten billion) then.", dest="startWayId", type="int",
		default=10000000, action="store", metavar="WAY-ID")
	parser.add_option("--max-nodes-per-tile", help="specify an integer as a maximum"
		"\nnumber of nodes per generated tile.  It defaults to 1000000,"
		"\nwhich is approximately the maximum number of nodes handled properly"
		"\nby mkgmap.  For bigger tiles, try higher values.  For a single file"
		"\noutput, say 0 here.",
		dest="maxNodesPerTile", type="int", default=1000000, action="store")
	parser.add_option("--max-nodes-per-way", help="specify an integer as a maximum"
		"\nnumber of nodes per way.  It defaults to 2000, which is the maximum value"
		"\nfor OSM api version 0.6.  Say 0 here, if you want unsplitted ways.",
		dest="maxNodesPerWay", type="int", default=2000, action="store")
	parser.add_option("--simplifyContoursEpsilon", help="simplify contour lines"
		"\nusing the Ramer-Douglas-Peucker (RDP) algorithm with this EPSILON value. "
		"\nThe larger the value, the more simplified the contour lines.  The"
		"\nvalue passed will be directly used, i. e. in case of WGS84 based"
		"\nreference systems like EPSG:4326, the passed value is interpreted as"
		"\ndegrees of latitude and longitude, respectively.  Use a value of 0.0 to"
		"\nremove only vertices on straight lines.  Sensible values to reduce the"
		"\noutput file size while preserving resonable accuracy are dependent on"
		"\nthe file resolution.  For SRTM3 data, some value between 0.0001 and"
		"\n0.0005 seems reasonable, reducing the file size by something like one"
		"\nor two thirds.  Note that using contour line simplification will slow"
		"\ndown contour line generation.  The default is not to use RDP.",
		dest="rdpEpsilon", type="float", default=None, action="store",
		metavar="EPSILON")
	parser.add_option("--simplifyContoursMaxDistance", help="Do not delete all"
		"\nvertices while simplifying a contour line using RDP but only delete"
		"\npoints within this range.  The default is to delete all dispensable"
		"\nvertices.  Only use this option if you want to get the benefit of RDP"
		"\nbut need somehow close-lying points because of rendering issues or so."
		"\nUsing this option will dramatically slow down contour line generation.",
		dest="rdpMaxVertexDistance", type="float", default=None, action="store",
		metavar="MAX_VERTEX_DISTANCE")
	parser.add_option("--gzip", help="turn on gzip compression of output files."
		"\nThis reduces the needed disk space but results in higher computation"
		"\ntimes.  Specifiy an integer between 1 and 9.  1 means low compression and"
		"\nfaster computation, 9 means high compression and lower computation.",
		dest="gzip", action="store", default=0, metavar="COMPRESSLEVEL",
		type="int")
	parser.add_option("--pbf", help="write protobuf binary files instead of OSM"
		"\nXML.  This reduces the needed disk space. Be sure the programs you"
		"\nwant to use the output files with are capable of pbf parsing.  The"
		"\noutput files will have the .osm.pbf extension.", action="store_true",
		default=False, dest="pbf")
	parser.add_option("--o5m", help="write o5m binary files instead of OSM"
		"\nXML.  This reduces the needed disk space. Be sure the programs you"
		"\nwant to use the output files with are capable of o5m parsing.  The"
		"\noutput files will have the .o5m extension.", action="store_true",
		default=False, dest="o5m")
	parser.add_option("--srtm", help="use SRTM resolution of SRTM-RESOLUTION"
		"\narc seconds.  Possible values are 1 and 3, the default value is 3. "
		"\nFor different SRTM data versions and map coverage, see the --srtm-version"
		"\noption.",  metavar="SRTM-RESOLUTION", dest="srtmResolution", action="store",
		type="int", default=3)
	parser.add_option("--srtm-version", help="use this VERSION of SRTM data."
		"\nSupported SRTM versions are 2.1 and 3.  Version 2.1 has voids which"
		"\nwere filled in version 3 using ASTER GDEM and other data.  In version"
		"\n2.1, only the US territory is included in the 1 arc second dataset.  In"
		"\nversion 3, nearly the whole world is covered.  The default for this"
		"\noption is 3.  If you want the old version, say --srtm-version=2.1 here",
		dest="srtmVersion", action="store", metavar="VERSION", default=3.0,
		type="float")
	parser.add_option("--earthexplorer-user", help="the username to use for"
		"\nearthexplorer login.  This is needed if you want to use NASA SRTM sources"
		"\nin version 3.0.  If you do not yet have an earthexplorer login, visit"
		"\nhttps://ers.cr.usgs.gov/register/ and create one.  Once specified,"
		"\nphyghtmap will store the earthexplorer login credentials unencrypted in a"
		"\nfile called '.phyghtmaprc' in your home directory.  I. e., you only"
		"\nhave to specify this option (and the --earthexplorer-password option) once. "
		"\nIn addition, the password specified on the command line may be read"
		"\nby every user on your system.  So, don't choose a password which you"
		"\ndon't want to be disclosed to others.  This option should be specified"
		"\nin combination with the --earthexplorer-password option.",
		dest="earthexplorerUser", action="store", default=None,
		metavar="EARTHEXPLORER_USERNAME")
	parser.add_option("--earthexplorer-password", help="the password to use for"
		"\nearthexplorer login.  This option should be specified in combination with"
		"\nthe --earthexplorer-user option.  For further explanation, see the help"
		"\ngiven for the --earthexplorer-user option.", dest="earthexplorerPassword",
		action="store", default=None, metavar="EARTHEXPLORER_PASSWORD")
	parser.add_option("--viewfinder-mask", help="if specified, NASA SRTM data"
 		"\nare masked with data from www.viewfinderpanoramas.org.  Possible values"
		"\nare 1 and 3 (for explanation, see the --srtm option).",
		metavar="VIEWFINDER-RESOLUTION", type="int", default=0, action="store",
		dest="viewfinder")
	parser.add_option("--source", "--data-source", help="specify a list of"
		"\nsources to use as comma-seperated string.  Available sources are"
		"\n'srtm1', 'srtm3', 'view1' and 'view3'.  If specified, the data source"
		"\nwill be selected using this option as preference list.  Specifying"
		"\n--source=view3,srtm3 for example will prefer viewfinder 3 arc second"
		"\ndata to NASA SRTM 3 arc second data.  Also see the --srtm-version"
		"\noption for different versions of SRTM data.", metavar="DATA-SOURCE",
		action="store", default=None, dest="dataSource")
	parser.add_option("--corrx", help="correct x offset of contour lines."
		"\n A setting of --corrx=0.0005 was reported to give good results."
		"\n However, the correct setting seems to depend on where you are, so"
		"\nit is may be better to start with 0 here.",
		metavar="SRTM-CORRX", dest="srtmCorrx", action="store",
		type="float", default=0)
	parser.add_option("--corry", help="correct y offset of contour lines."
		"\n A setting of --corry=0.0005 was reported to give good results."
		"\n However, the correct setting seems to depend on where you are, so"
		"\nit may be better to start with 0 here.",
		metavar="SRTM-CORRY", dest="srtmCorry", action="store",
		type="float", default=0)
	parser.add_option("--hgtdir", help="Cache directory for hgt files."
		"\nThe downloaded SRTM files are stored in a cache directory for later use."
		"\nThe default directory for this is ./hgt/ in the current directory.  You can"
		"\nspecify another cache directory with this option.",
		dest="hgtdir", action="store", default=None, metavar="DIRECTORY")
	parser.add_option("--rewrite-indices", help="rewrite the index files and"
		"\nexit.  Try this if phyghtmap encounters problems when trying to download"
		"\ndata files.", dest="rewriteIndices", action="store_true", default=False)
	parser.add_option("--void-range-max", help="extend the void value range"
		"\nup to this height.  The hgt file format uses a void value which is"
		"\n-0x8000 or, in terms of decimal numbers, -32768.  Some hgt files"
		"\ncontain other negative values which are implausible as height values,"
		"\ne. g. -0x4000 (-16384) or similar.  Since the lowest place on earth is"
		"\nabout -420 m below sea level, it should be safe to say -500 here in"
		"\ncase you encounter strange phyghtmap behaviour such as program aborts"
		"\ndue to exceeding the maximum allowed number of recursions.",
		default=-0x8000, type="int", metavar="MINIMUM_PLAUSIBLE_HEIGHT_VALUE",
		action="store", dest="voidMax")
	parser.add_option("-v", "--version", help="print version and exit.",
		dest="version", action="store_true", default=False)
	opts, args = parser.parse_args()
	if opts.version:
		print("phyghtmap {0:s}".format(__version__))
		sys.exit(0)
	if opts.hgtdir:  # Set custom ./hgt/ directory
		NASASRTMUtil.NASASRTMUtilConfig.CustomHgtSaveDir(opts.hgtdir)
	if opts.rewriteIndices:
		NASASRTMUtil.rewriteIndices()
		sys.exit(0)
	if opts.pbf and opts.gzip:
		sys.stderr.write("You can't combine the --gzip and --pbf options.\n")
		sys.exit(1)
	if opts.o5m and opts.gzip:
		sys.stderr.write("You can't combine the --gzip and --o5m options.\n")
		sys.exit(1)
	if opts.o5m and opts.pbf:
		sys.stderr.write("You can't combine the --pbf and --o5m options.\n")
		sys.exit(1)
	for supportedVersion in [2.1, 3]:
		if opts.srtmVersion == supportedVersion:
			break
	else:
		# unsupported SRTM data version
		sys.stderr.write("Unsupported SRTM data version '{0:.1f}'.  See the"
			" --srtm-version option for details.\n\n".format(opts.srtmVersion))
		parser.print_help()
		sys.exit(1)
	if opts.srtmResolution not in [1, 3]:
		sys.stderr.write("The --srtm option can only take '1' or '3' as values."
			"  Defaulting to 3.\n")
		opts.srtmResolution = 3
	if opts.viewfinder not in [0, 1, 3]:
		sys.stderr.write("The --viewfinder-mask option can only take '1' or '3' as values."
			"  Won't use viewfinder data.\n")
		opts.viewfinder = 0
	if opts.dataSource:
		opts.dataSource = [el.strip() for el in
			opts.dataSource.lower().split(",")]
		for s in opts.dataSource:
			if not s[:5] in ["view1", "view3", "srtm1", "srtm3"]:
				print("Unknown data source: {0:s}".format(s))
				sys.exit(1)
			elif s in ["srtm1", "srtm3"]:
				while s in opts.dataSource:
					opts.dataSource[opts.dataSource.index(s)] = "{0:s}v{1:.1f}".format(
						s, opts.srtmVersion)
	else:
		opts.dataSource = []
		if opts.viewfinder != 0:
			opts.dataSource.append("view{0:d}".format(opts.viewfinder))
		opts.dataSource.append("srtm{0:d}v{1:.1f}".format(opts.srtmResolution,
			opts.srtmVersion))
		if not opts.area and not opts.polygon:
			# this is a hint for makeOsmFilename() that files are specified on the
			# command line
			opts.dataSource = []
	needsEarthexplorerLogin = False
	for s in opts.dataSource:
		if s.startswith("srtm") and "v3" in s:
			needsEarthexplorerLogin = True
	if needsEarthexplorerLogin:
		# we need earthexplorer login credentials handling then
		earthexplorerUser = configUtil.Config(configFilename).setOrGet(
			"earthexplorer_credentials", "user", opts.earthexplorerUser)
		earthexplorerPassword = configUtil.Config(configFilename).setOrGet(
			"earthexplorer_credentials", "password", opts.earthexplorerPassword)
		if not all((earthexplorerUser, earthexplorerPassword)):
			print("Need earthexplorer login credentials to continue.  See the help for the")
			print("--earthexplorer-user and --earthexplorer-password options for details.")
			print("-"*60)
			parser.print_help()
			sys.exit(1)
		NASASRTMUtil.NASASRTMUtilConfig.earthexplorerCredentials(
			earthexplorerUser, earthexplorerPassword)
	if len(args) == 0 and not opts.area and not opts.polygon:
		parser.print_help()
		sys.exit(1)
	if opts.polygon:
		try:
			os.stat(opts.polygon)
		except OSError:
			print("Couldn't find polygon file: {0:s}".format(opts.polygon))
			sys.exit(1)
		if not os.path.isfile(opts.polygon):
			print("Polygon file '{0:s}' is not a regular file".format(opts.polygon))
			sys.exit(1)
		opts.area, opts.polygon = hgt.parsePolygon(opts.polygon)
	elif opts.downloadOnly and not opts.area:
		# no area, no polygon, so nothing to download
		sys.stderr.write("Nothing to download.  Combine the --download-only option with"
			"\neither one of the --area and --polygon options.\n")
		sys.exit(1)
	return opts, args

def makeOsmFilename(borders, opts, srcNames):
	"""generate a filename for the output osm file. This is done using the bbox
	of the current hgt file.
	"""
	minLon, minLat, maxLon, maxLat = borders
	if opts.outputPrefix:
		prefix = "{0:s}_".format(opts.outputPrefix)
	else:
		prefix = ""
	srcNameMiddles = [os.path.split(os.path.split(srcName)[0])[1].lower() for srcName in
		srcNames]
	for srcNameMiddle in set(srcNameMiddles):
		if srcNameMiddle.lower()[:5] in ["srtm1", "srtm3", "view1", "view3"]:
			continue
		elif not opts.dataSource:
			# files from the command line, this could be something custom
			srcTag = ",".join(set(srcNameMiddles))
			#osmName = hgt.makeBBoxString(borders).format(prefix) + "_{0:s}.osm".format(srcTag)
			osmName = hgt.makeBBoxString(borders).format(prefix) + "_local-source.osm"
			break
		else:
			osmName = hgt.makeBBoxString(borders).format(prefix) + ".osm"
			break
	else:
		srcTag = ",".join([s for s in opts.dataSource if s in
			set(srcNameMiddles)])
		osmName = hgt.makeBBoxString(borders).format(prefix) + "_{0:s}.osm".format(srcTag)
	if opts.gzip:
		osmName += ".gz"
	elif opts.pbf:
		osmName += ".pbf"
	elif opts.o5m:
		osmName = osmName[:-4]+".o5m"
	return osmName

def getOutput(opts, srcNames, bounds):
	outputFilename = makeOsmFilename(bounds, opts, srcNames)
	elevClassifier=osmUtil.makeElevClassifier(*[int(h) for h in
		opts.lineCats.split(",")])
	if opts.pbf:
		output = pbfUtil.Output(outputFilename, opts.osmVersion, __version__,
			bounds, elevClassifier)
	elif opts.o5m:
		output = o5mUtil.Output(outputFilename, opts.osmVersion, __version__,
			bounds, elevClassifier, writeTimestamp=opts.writeTimestamp)
	else:
		# standard XML output, possibly gzipped
		output = osmUtil.Output(outputFilename,
			osmVersion=opts.osmVersion, phyghtmapVersion=__version__,
			boundsTag=hgt.makeBoundsString(bounds), gzip=opts.gzip,
			elevClassifier=elevClassifier, timestamp=opts.writeTimestamp)
	return output

def writeNodes(*args, **kwargs):
	opts = args[-1]
	if opts.pbf:
		return pbfUtil.writeNodes(*args, **kwargs)
	elif opts.o5m:
		return o5mUtil.writeNodes(*args, **kwargs)
	else:
		return osmUtil.writeXML(*args, **kwargs)

def processHgtFile(srcName, opts, output=None, wayOutput=None, statsOutput=None,
	timestampString="", checkPoly=False):
	hgtFile = hgt.hgtFile(srcName, opts.srtmCorrx, opts.srtmCorry, opts.polygon,
		checkPoly, opts.voidMax, opts.contourFeet)
	hgtTiles = hgtFile.makeTiles(opts)
	if opts.plotPrefix:
		for tile in hgtTiles:
			tile.plotData(opts.plotPrefix)
		return []
	if opts.maxNodesPerTile == 0:
		singleOutput = True
	else:
		singleOutput = False
	if opts.doFork:
		# called from processQueue
		numOfPoints, numOfWays = 0, 0
		goodTiles = []
		for tile in hgtTiles:
			try:
				tile.elevations, tile.contourData = tile.contourLines(
					stepCont=int(opts.contourStepSize),
					maxNodesPerWay=opts.maxNodesPerWay, noZero=opts.noZero,
					rdpEpsilon=opts.rdpEpsilon,
					rdpMaxVertexDistance=opts.rdpMaxVertexDistance)
				goodTiles.append(tile)
			except ValueError: # tiles with the same value on every element
				continue
			numOfPointsAdd, numOfWaysAdd = tile.countNodes(
				maxNodesPerWay=opts.maxNodesPerWay, rdpEpsilon=opts.rdpEpsilon,
				rdpMaxVertexDistance=opts.rdpMaxVertexDistance)
			numOfPoints += numOfPointsAdd
			numOfWays += numOfWaysAdd
		hgtTiles = goodTiles
		statsOutput.write(str(numOfWays)+":"+str(numOfPoints))
		statsOutput.close()
		if singleOutput:
			# forked, single output, output is already defined
			#output = output
			ways = []
			for tile in hgtTiles:
				# there is only one tile
				elevations, contourData = tile.elevations, tile.contourData
				_, ways = writeNodes(output, contourData,
						elevations, timestampString, opts)
			output.close() # close the output pipe
			wayOutput.write(str(ways))
			wayOutput.close()
			return # we don't need to return something special
		else:
			# forked, multi output
			for tile in hgtTiles:
				output = getOutput(opts, [srcName, ], tile.bbox())
				elevations, contourData = tile.elevations, tile.contourData
				# we have multiple output files, so we need to count nodeIds here
				opts.startId, ways = writeNodes(output, contourData,
						elevations, output.timestampString, opts)
				output.writeWays(ways, opts.startWayId)
				# we have multiple output files, so we need to count wayIds here
				opts.startWayId += len(ways)
				output.done()
			return # we don't need to return something special
	else:
		if singleOutput:
			# not forked, single output, output is already defined
			# output = output
			ways = []
			for tile in hgtTiles:
				# there is only one tile
				try:
					elevations, contourData = tile.contourLines(
						stepCont=int(opts.contourStepSize),
						maxNodesPerWay=opts.maxNodesPerWay, noZero=opts.noZero,
						rdpEpsilon=opts.rdpEpsilon,
						rdpMaxVertexDistance=opts.rdpMaxVertexDistance)
				except ValueError: # tiles with the same value on every element
					continue
				opts.startId, ways = writeNodes(output, contourData,
						elevations, timestampString, opts)
			return ways # needed to complete file later
		else:
			# not forked, multi output
			for tile in hgtTiles:
				output = getOutput(opts, [srcName, ], tile.bbox())
				try:
					elevations, contourData = tile.contourLines(
						stepCont=int(opts.contourStepSize),
						maxNodesPerWay=opts.maxNodesPerWay, noZero=opts.noZero,
						rdpEpsilon=opts.rdpEpsilon,
						rdpMaxVertexDistance=opts.rdpMaxVertexDistance)
				except ValueError: # tiles with the same value on every element
					continue
				# we have multiple output files, so we need to count nodeIds here
				opts.startId, ways = writeNodes(output, contourData,
						elevations, output.timestampString, opts)
				output.writeWays(ways, opts.startWayId)
				# we have multiple output files, so we need to count wayIds here
				opts.startWayId += len(ways)
				output.done()
			return [] # don't need to return ways, since output is already complete


class ProcessQueue(object):
	def __init__(self, nJobs, fileList, **kwargs):
		self.nJobs, self.fileList = nJobs, fileList
		self.kwargs = kwargs
		self.opts = self.kwargs["opts"]
		self.children = {}
		if self.opts.maxNodesPerTile == 0:
			self.singleOutput = True
			bounds = [float(b) for b in self.opts.area.split(":")]
			srcNames = [s[0] for s in self.fileList]
			self.output = getOutput(self.opts, srcNames, bounds)
		else:
			self.singleOutput = False

	def _forkOneSingleOutput(self):
		nodeR, nodeW = os.pipe()
		wayR, wayW = os.pipe()
		statsR, statsW = os.pipe()
		pid = os.fork()
		srcName, checkPoly = self.fileList.pop()
		if pid==0:
			print("Computing {0:s}".format(srcName))
			os.close(statsR)
			statsWPipe = os.fdopen(statsW, "w")
			os.close(nodeR)
			nodeWPipe = os.fdopen(nodeW, "w")
			wayWPipe = os.fdopen(wayW, "w")
			processHgtFile(srcName, self.opts, nodeWPipe, wayWPipe, statsWPipe,
				self.output.timestampString, checkPoly=checkPoly)
			statsWPipe.close()
			nodeWPipe.close()
			wayWPipe.close()
			os._exit(0)
		else:
			os.close(statsW)
			statsRPipe = os.fdopen(statsR)
			statsRList, _, _ = select.select([statsRPipe, ], [], [])
			stats = statsRList[0].read()
			statsRPipe.close()
			numOfWays, numOfNodes = [int(el) for el in stats.split(":")]
			os.close(nodeW)
			os.close(wayW)
			nodeRPipe = os.fdopen(nodeR)
			wayRPipe = os.fdopen(wayR)
			self.children[pid] = (srcName, nodeRPipe, wayRPipe)
			self.instancePids.append(pid)
			self.Poll.register(nodeRPipe, select.POLLIN)
			return numOfWays, numOfNodes

	def processSingleOutput(self):
		self.Poll = select.poll()
		self.instancePids = []
		self.ways = []
		while self.fileList or self.children:
			while len(self.children)<self.nJobs and self.fileList:
				expectedNumOfWays, expectedNumOfNodes = self._forkOneSingleOutput()
				self.opts.startId += expectedNumOfNodes
				#self.opts.startWayId += expectedNumOfWays
			if self.children:
				# nodes have to be written in correct sequence so we need to process
				# them in the order the processes were forked;  for ways, we wouldn't
				# necessarily have to care about such an issue because these get their
				# ids later but we do for reasons of clarity
				nextRPipe = self.children[self.instancePids[0]][1]
				while not nextRPipe.fileno() in [i for i, _ in self.Poll.poll()]:
					# wait for the node pipe of the desired process to become ready
					time.sleep(.1)
				# the node pipe is ready now
				"""
				sys.stdout.write("writing nodes for area {:s} ... ".format(
					self.children[self.instancePids[0]][0]))
				sys.stdout.flush()
				"""
				while True:
					line = nextRPipe.readline()
					if len(line) == 0:
						break
					self.output.write(line)
				"""
				sys.stdout.write("DONE\n")
				sys.stdout.flush()
				"""
				# now read the way read pipe for the same process
				readyWayRPipe = select.select([self.children[self.instancePids[0]][2], ], [], [])[0]
				while True:
					readyWayRPipe = select.select([self.children[self.instancePids[0]][2], ], [], [])[0]
					if len(readyWayRPipe):
						break
					time.sleep(.1)
				"""
				sys.stdout.write("writing ways for area {:s} ... ".format(
					self.children[self.instancePids[0]][0]))
				sys.stdout.flush()
				"""
				while True:
					s = readyWayRPipe[0].read()
					if len(s) == 0:
						break
					self.ways.extend(eval(s))
				"""
				sys.stdout.write("DONE\n")
				sys.stdout.flush()
				"""
				# wait for the evaluated (earliest-started) process to complete
				while True:
					pid, res = os.waitpid(self.instancePids[0], os.WNOHANG)
					if pid == self.instancePids[0]:
						# process self.instancePids[0] exited
						break
					time.sleep(.1)
				if res:
					print("Panic: Didn't work:", self.children[pid][0])
				self.Poll.unregister(self.children[pid][1])
				self.children[pid][1].close()
				self.children[pid][2].close()
				del self.children[pid]
				del self.instancePids[0]
		self.output.writeWays(self.ways, self.opts.startWayId)
		self.output.done()

	def _forkOneMultiOutput(self):
		statsR, statsW = os.pipe()
		pid = os.fork()
		srcName, checkPoly = self.fileList.pop()
		if pid==0:
			print("Computing {0:s}".format(srcName))
			os.close(statsR)
			statsWPipe = os.fdopen(statsW, "w")
			processHgtFile(srcName, self.opts, None, None, statsWPipe,
				checkPoly=checkPoly)
			statsWPipe.close()
			os._exit(0)
		else:
			os.close(statsW)
			statsRPipe = os.fdopen(statsR)
			statsRList, _, _ = select.select([statsRPipe, ], [], [])
			stats = statsRList[0].read()
			statsRPipe.close()
			numOfWays, numOfNodes = [int(el) for el in stats.split(":")]
			self.children[pid] = (srcName, )
			return numOfWays, numOfNodes

	def processMultiOutput(self):
		while self.fileList or self.children:
			while len(self.children)<self.nJobs and self.fileList:
				expectedNumOfWays, expectedNumOfNodes = self._forkOneMultiOutput()
				self.opts.startId += expectedNumOfNodes
				self.opts.startWayId += expectedNumOfWays
			if self.children:
				pid, res = os.wait()
				if res:
					print("Panic: Didn't work:", self.children[pid][0])
				del self.children[pid]

	def process(self):
		if self.singleOutput:
			self.processSingleOutput()
		else:
			self.processMultiOutput()


def main():
	opts, args = parseCommandLine()
	if opts.area:
		hgtDataFiles = NASASRTMUtil.getFiles(opts.area, opts.polygon,
			opts.srtmCorrx, opts.srtmCorry, opts.dataSource)
		if len(hgtDataFiles) == 0:
			if len(opts.dataSource) == 1:
				print("No files for this area {0:s} from desired source.".format(opts.area))
			else:
				print("No files for this area {0:s} from desired sources.".format(opts.area))
			sys.exit(0)
		elif opts.downloadOnly:
			sys.exit(0)
	else:
		hgtDataFiles = [(arg, False) for arg in args if
			os.path.splitext(arg)[1].lower() in (".hgt", ".tif", ".tiff", ".vrt")]
		opts.area = ":".join([str(i) for i in hgt.calcHgtArea(hgtDataFiles,
			opts.srtmCorrx, opts.srtmCorry)])

	if hasattr(os, "fork") and opts.nJobs != 1:
		opts.doFork = True
		queue = ProcessQueue(opts.nJobs, hgtDataFiles, opts=opts)
		queue.process()
	else:
		opts.doFork = False
		if opts.maxNodesPerTile == 0:
			bounds = [float(b) for b in opts.area.split(":")]
			srcNames = [s[0] for s in hgtDataFiles]
			output = getOutput(opts, srcNames, bounds)
		else:
			output = None
		ways = []
		for hgtDataFileName, checkPoly in hgtDataFiles:
			if output:
				ways.extend(processHgtFile(hgtDataFileName, opts, output,
					timestampString=output.timestampString, checkPoly=checkPoly))
			else:
				ways.extend(processHgtFile(hgtDataFileName, opts, output,
					checkPoly=checkPoly))
		if opts.maxNodesPerTile == 0:
			# writing to single file, need to complete it here
			output.writeWays(ways, opts.startWayId)
			output.done()

if __name__=="__main__":
	if profile:
		import cProfile
		cProfile.run("main()", "stats.profile")
		import pstats
		stats = pstats.Stats("stats.profile")
		stats.sort_stats("time").print_stats(20)
	else:
		main()
