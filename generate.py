#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mapnik
import cairo
import os
import sys
import re

def env(key, default=None):
    return os.getenv(key, default)

def requireEnvironment(name):
    value = env(name)

    if value is None:
        print ("The environment variable '%s' is required" % (name,))
        exit(1)

    return value

OUTPUT_PATH = 'output/'

def layer(name, srs, ds, group=None):
    lay = mapnik.Layer(name)
    lay.srs = srs
    lay.datasource = ds
    if group is not None:
        lay.group_by = group
    return lay


def loadMapFromFile(file, mapWidth, mapHeight):
    m = mapnik.Map(mapWidth, mapHeight)
    print 'Loading map from file %s' % (file,)
    mapnik.load_map(m, file)
    return m

def renderMap(m, name, topLeft, bottomRight):
    print 'Rendering map with dimensions %s, %s' % (m.width, m.height)
    m.zoom_to_box(mapnik.Box2d(topLeft[0], topLeft[1], bottomRight[0], bottomRight[1]))
    im = mapnik.Image(m.width, m.height)
    mapnik.render(m, im)

    if not os.path.exists(OUTPUT_PATH):
        print 'Creating output directory %s' % (OUTPUT_PATH,)
        os.makedirs(OUTPUT_PATH)

    if mapnik.has_pycairo():
        print 'Rendering PDF'

        pdf_surface = cairo.PDFSurface(OUTPUT_PATH + name + '.pdf', m.width, m.height)
        mapnik.render(m, pdf_surface)
        pdf_surface.finish()
        print 'Rendered PDF to %s' % (OUTPUT_PATH + name + '.pdf',)

    xmlFilename = "mapnik_" + name + ".xml"
    print 'Saving map configuration to %s' % (OUTPUT_PATH + xmlFilename,)
    mapnik.save_map(m, OUTPUT_PATH + xmlFilename)
    print 'Done'


def envList(envString, pattern):
    ret = [] 
    pattern = re.compile(pattern)
    split = envString.split(' ')
    for s in split:
        current = s.strip()
        if not pattern.match(current):
            print ("Input '%s' does not match %s" % (current, pattern.pattern))
            exit(1)
        ret.append(current)

    return ret

print('Python version %s' % (sys.version,))
print('Mapnik version %s' % (mapnik.paths.__all__,))

name=env('MAP_NAME', 'map')

LATITUDES = envList(env('LATITUDES', 'N52'), '^[NS][0-9]{2}$')
LONGITUDES = envList(env('LONGITUDES', 'E006'), '^[EW][0-9]{3}$')

SHADE_NAMES = [lat + lon for lat in LATITUDES for lon in LONGITUDES]

print ('Using name \'%s\'' % (name, ))
print ('Using latitudes %s' % (LATITUDES, ))
print ('Using longitudes %s' % (LONGITUDES, ))

# Choose with https://epsg.io/map#srs=3857&x=2225846.263664&y=6275978.874398&z=8&layer=streets
# In EPSG:3857
TOP_LEFT_X=int(requireEnvironment('TOP_LEFT_X'))
TOP_LEFT_Y=int(requireEnvironment('TOP_LEFT_Y'))

OFFSET_PAGES_X=float(env('OFFSET_PAGES_X', 0))
OFFSET_PAGES_Y=float(env('OFFSET_PAGES_Y', 0))

PAGES_HORIZONTAL=int(env('PAGES_HORIZONTAL', 1))
PAGES_VERTICAL=int(env('PAGES_VERTICAL', 1))

ratio = 1.414
width = 8.27  # inch
height = ratio * width  # inch
dpi = 125

i = OFFSET_PAGES_X
j = OFFSET_PAGES_Y

numPagesHorizontal = PAGES_HORIZONTAL
numPagesVertical = PAGES_VERTICAL

pageWidth = 29693
pageHeight = - 1.414 * pageWidth
topLeft = int(TOP_LEFT_X + i * pageWidth), int(TOP_LEFT_Y + j * pageHeight)
bottomRight = int(topLeft[0] + numPagesHorizontal * pageWidth), int(topLeft[1] + numPagesVertical * pageHeight)

print ('Generating from top left (%s, %s) to bottom right (%s, %s) (%s pages horizontal and %s pages vertical)' % (topLeft[0], topLeft[1], bottomRight[0], bottomRight[1], numPagesHorizontal, numPagesVertical))

mapWidth = numPagesHorizontal * int(width * dpi)
mapHeight = numPagesVertical * int(height * dpi)

mapnikConfiguration = requireEnvironment('MAPNIK_CONFIGURATION')

print('using Mapnik configuration file %s' % (mapnikConfiguration,))
m = loadMapFromFile(mapnikConfiguration, mapWidth, mapHeight)
renderMap(m, name, topLeft, bottomRight)