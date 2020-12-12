#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import cairo
import mapnik

from scripts import bounds, environment

OUTPUT_PATH = '../output/'


def loadMapFromFile(file, mapWidth, mapHeight):
    m = mapnik.Map(mapWidth, mapHeight)
    print('Loading map from file %s' % (file,))
    mapnik.load_map(m, file)
    return m


def renderMap(m, name, bbox):
    print('Rendering map with dimensions %s, %s' % (m.width, m.height))
    m.zoom_to_box(bbox)

    if not os.path.exists(OUTPUT_PATH):
        print('Creating output directory %s' % (OUTPUT_PATH,))
        os.makedirs(OUTPUT_PATH)

    if mapnik.has_pycairo():
        print('Rendering PDF')

        pdf_surface = cairo.PDFSurface(OUTPUT_PATH + name + '.pdf', m.width, m.height)
        mapnik.render(m, pdf_surface, 1 / 2.0, 0, 0)
        pdf_surface.finish()
        print('Rendered PDF to %s' % (OUTPUT_PATH + name + '.pdf',))

    xmlFilename = "mapnik_" + name + ".xml"
    print('Saving map configuration to %s' % (OUTPUT_PATH + xmlFilename,))
    mapnik.save_map(m, OUTPUT_PATH + xmlFilename)
    print('Done')


def main():
    print('Python version %s' % (sys.version,))
    print('Mapnik version %s' % (mapnik.paths.__all__,))

    name = environment.env('MAP_NAME', 'map')
    print('Using name \'%s\'' % (name,))

    size = environment.env('PAPER_SIZE', 'A4')
    orientation = environment.env('PAPER_ORIENTATION', bounds.ORIENTATION_PORTRAIT)
    boundingBox = bounds.determineBoundingBox(environment.require('BBOX'))
    pageOverlap = bounds.determinePageOverlap(environment.env('PAGE_OVERLAP', '5%'))
    # Default 1 cm on the map is 1.5 km in the world
    scale = bounds.determineScale(environment.env('SCALE', '1:150000'))
    paperWidth, paperHeight = bounds.determinePaperDimensions(size)
    orientation = bounds.determineOrientation(orientation)
    printPaperWidth, printPaperHeight = bounds.rotatePaper((paperWidth, paperHeight), orientation)

    print('Using paper size %s and orientation %s' % (size, orientation))
    mapWidth, mapHeight = bounds.mapDimensions((printPaperWidth, printPaperHeight))

    mapnikConfiguration = environment.require('MAPNIK_CONFIGURATION')
    print('Loading Mapnik configuration file %s' % (mapnikConfiguration,))
    m = loadMapFromFile(mapnikConfiguration, mapWidth, mapHeight)
    print('Loaded Mapnik configuration')

    boundingBoxes = bounds.boundingBoxes(boundingBox, pageOverlap, scale, (printPaperWidth, printPaperHeight))
    print('Rendering %s pages' % (len(boundingBoxes),))

    page = 1
    for boundingBox in boundingBoxes:
        tileBoundingBox = bounds.latitudeLongitudeToWebMercator.forward(boundingBox)

        print('Generating page %s for bounding box (%s, %s) × (%s, %s)' % (page, boundingBox.minx, boundingBox.miny, boundingBox.maxx, boundingBox.maxy))

        suffixedName = name if len(boundingBoxes) == 1 else ('%s_%s' % (name, page))
        renderMap(m, suffixedName, tileBoundingBox)
        print('Done rendering page %s' % (page,))

        page += 1

    print('Done rendering pages')


if __name__ == '__main__':
    main()
