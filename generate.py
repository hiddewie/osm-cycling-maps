#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math

import mapnik
import cairo
import os
import sys
import re

def exitError(message, exitCode = 1):
    print(message)
    exit(exitCode)

def env(key, default=None):
    return os.getenv(key, default)

def requireEnvironment(name):
    value = env(name)

    if value is None:
        return exitError("The environment variable '%s' is required" % (name,))

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

    if not os.path.exists(OUTPUT_PATH):
        print 'Creating output directory %s' % (OUTPUT_PATH,)
        os.makedirs(OUTPUT_PATH)

    if mapnik.has_pycairo():
        print 'Rendering PDF'

        pdf_surface = cairo.PDFSurface(OUTPUT_PATH + name + '.pdf', m.width, m.height)
        mapnik.render(m, pdf_surface, 1 / 2.0, 0, 0)
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
            return exitError("Input '%s' does not match %s" % (current, pattern.pattern))
        ret.append(current)

    return ret

def determinePaperDimensions(paperSize):
    # Paper sizes in meter
    paperSizes = {
        'A4': { 'width': 0.210, 'height': 0.297 },
        'A3': { 'width': 0.297, 'height': 0.420 },
        'A2': { 'width': 0.420, 'height': 0.594 },
        'A1': { 'width': 0.594, 'height': 0.841 },
        'A0': { 'width': 0.841, 'height': 1.189 },
    }

    millimeters = re.match(r'^(\d+\.?\d*) mm [x×] (\d+\.?\d*) mm$', paperSize)
    meters = re.match(r'^(\d+\.?\d*) m [x×] (\d+\.?\d*) m$', paperSize)
    inches = re.match(r'^(\d+\.?\d*) in [x×] (\d+\.?\d*) in$', paperSize)
    if paperSize in paperSizes:
        return paperSizes[paperSize]['width'], paperSizes[paperSize]['height']
    elif millimeters:
        return float(millimeters.group(1)) / 1000, float(millimeters.group(2)) / 1000
    elif meters:
        return float(meters.group(1)), float(meters.group(2))
    elif inches:
        return float(inches.group(1)) * 0.0254, float(inches.group(2)) * 0.0254
    else:
        exitError("The paper size should be one of the values %s or of the form `A mm x B mm`, `A m x B m` or `A in x B in`, but %s was given" % (paperSizes.keys(), paperSize))
        return

def main():
    print('Python version %s' % (sys.version,))
    print('Mapnik version %s' % (mapnik.paths.__all__,))

    name = env('MAP_NAME', 'map')
    print ('Using name \'%s\'' % (name, ))

    BBOX = requireEnvironment('BBOX')
    bboxMatch = re.match(r'^(\d+\.?\d*):(\d+\.?\d*):(\d+\.?\d*):(\d+\.?\d*)$', BBOX)

    if not bboxMatch:
        exitError("The bounding box must be of the form A:B:C:D with (A, B) the bottom left corner and (C, D) the top right corner. %s was given" % (BBOX,))
        return

    EPSG_4326 = mapnik.Projection('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
    EPSG_3857 = mapnik.Projection('+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over')
    latitudeLongitudeToWebMercator = mapnik.ProjTransform(EPSG_4326, EPSG_3857)

    bbox = latitudeLongitudeToWebMercator.forward(mapnik.Box2d(
        float(bboxMatch.group(1)),
        float(bboxMatch.group(2)),
        float(bboxMatch.group(3)),
        float(bboxMatch.group(4)),
    ))

    ORIENTATION_LANDSCAPE = 'landscape'
    ORIENTATION_PORTRAIT = 'portrait'
    paperOrientations = {
        ORIENTATION_LANDSCAPE,
        ORIENTATION_PORTRAIT,
    }
    orientation = env('PAPER_ORIENTATION', ORIENTATION_PORTRAIT)
    if not orientation in paperOrientations:
        exitError("The paper orientation should be one of the values %s but %s was given" % (paperOrientations, orientation))
        return

    paperSize = env('PAPER_SIZE', 'A4')
    width, height = determinePaperDimensions(paperSize)

    if orientation == ORIENTATION_LANDSCAPE:
        width, height = height, width
    print('Rendering map with page width paper size %s (%s m × %s m)' % (paperSize, width, height))

    # Default 1 cm on the map is 1.5 km in the world
    scale = env('SCALE', '1:150000')
    if not scale.strip().startswith('1:'):
        exitError("The scale should be of the form 1:N but %s was given" % (scale,))
        return
    try:
        scale = float(scale[2:])
    except:
        exitError("The scale should parsable as a floating point number but got %s" % (scale[2:],))
        return

    print('Rendering map with scale %s' % (scale,))

    # Dots per inch (1 point = 1/72 inch, see https://pycairo.readthedocs.io/en/latest/reference/surfaces.html#class-pdfsurface-surface)
    dpi = 72
    # Dots per m
    dpm = dpi * 100 / 2.54

    # A 'data' pixel is 1 meter (in UTM projection)
    pageWidth = width * scale
    pageHeight = height * scale

    # Find number of pages to print that fit the bounding box
    numPagesHorizontal = int(math.ceil((bbox.maxx - bbox.minx) / pageWidth))
    numPagesVertical = int(math.ceil((bbox.maxy - bbox.miny) / pageHeight))

    # Fit the generated pages perfectly 'around' the bounding box
    paddingX = ((numPagesHorizontal * pageWidth) - (bbox.maxx - bbox.minx)) / 2
    paddingY = ((numPagesVertical * pageHeight) - (bbox.maxy - bbox.miny)) / 2

    mapWidth = int(width * dpm)
    mapHeight = int(height * dpm)

    mapnikConfiguration = requireEnvironment('MAPNIK_CONFIGURATION')
    print('Loading Mapnik configuration file %s' % (mapnikConfiguration,))
    m = loadMapFromFile(mapnikConfiguration, mapWidth, mapHeight)
    print('Loaded Mapnik configuration')

    print('Rendering %s pages, %s horizontal and %s vertical' % (numPagesHorizontal * numPagesVertical, numPagesHorizontal, numPagesVertical))
    for i in range(numPagesHorizontal):
        for j in range(numPagesVertical):
            topLeft = int(bbox.minx - paddingX + i * pageWidth), int(bbox.maxy + paddingY - j * pageHeight)
            bottomRight = int(topLeft[0] + pageWidth), int(topLeft[1] - pageHeight)

            print('Generating page (%s, %s) from top left (%s, %s) to bottom right (%s, %s)' % (i + 1, j + 1, topLeft[0], topLeft[1], bottomRight[0], bottomRight[1]))

            suffixedName = name if numPagesHorizontal * numPagesVertical == 1 else ('%s_%s_%s' % (name, i + 1, j + 1))
            renderMap(m, suffixedName, topLeft, bottomRight)
            print('Done rendering page (%s, %s)' % (i + 1, j + 1))

    print('Done rendering pages')

if __name__ == '__main__':
    main()