#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import tempfile
import time

import PyPDF2
import cairo
import mapnik

import bounds
import environment

OUTPUT_PATH = 'output/'


def loadMapFromFile(file, mapWidth, mapHeight):
    m = mapnik.Map(mapWidth, mapHeight)
    print('Loading map from file %s' % (file,))
    mapnik.load_map(m, file)
    return m


def renderMap(m, file, bbox):
    print('Rendering map with dimensions %s, %s' % (m.width, m.height))
    m.zoom_to_box(bbox)

    if mapnik.has_pycairo():
        print('Rendering PDF')

        pdf_surface = cairo.PDFSurface(file, m.width, m.height)
        mapnik.render(m, pdf_surface, 0.7, 0, 0)
        pdf_surface.finish()

        print('Rendered PDF')

    print('Rendering done')


def main():
    print('Python version %s' % (sys.version,))
    print('Mapnik version %s' % (mapnik.paths.__all__,))

    name = environment.env('MAP_NAME', 'map')
    print('Using name \'%s\'' % (name,))

    size = environment.env('PAPER_SIZE', 'A4')
    orientation = environment.env('PAPER_ORIENTATION', bounds.ORIENTATION_PORTRAIT)
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

    boundingBoxes = []
    for boundingBox in environment.require('BBOX').split(','):
        boundingBoxes += bounds.boundingBoxes(
            bounds.determineBoundingBox(boundingBox.strip()),
            pageOverlap,
            scale,
            (printPaperWidth, printPaperHeight)
        )
    print('Rendering %s pages' % (len(boundingBoxes),))

    pdfWriter = PyPDF2.PdfFileMerger()
    page = 1
    for boundingBox in boundingBoxes:
        tileBoundingBox = bounds.latitudeLongitudeToWebMercator.forward(boundingBox)

        print('Generating page %s for bounding box (%.3f, %.3f) × (%.3f, %.3f)' %
              (page, boundingBox.minx, boundingBox.miny, boundingBox.maxx, boundingBox.maxy))

        with tempfile.NamedTemporaryFile() as tempFile:
            startTime = time.time()
            renderMap(m, tempFile, tileBoundingBox)

            stats = os.stat(tempFile.name)
            print('Done rendering page %s in %.1f sec with generated page size %.1f MB' % (page, time.time() - startTime, stats.st_size / (1024 * 1024)))
            pdfWriter.append(PyPDF2.PdfFileReader(tempFile))

            print('Done writing PDF page %s' % (page,))

        page += 1
    print('Done rendering pages')

    if not os.path.exists(OUTPUT_PATH):
        print('Creating output directory %s' % (OUTPUT_PATH,))
        os.makedirs(OUTPUT_PATH)

    print('Writing output file')
    with open('%s/%s.pdf' % (OUTPUT_PATH, name), 'wb') as outputFile:
        pdfWriter.write(outputFile)
    print('Done writing output file')


if __name__ == '__main__':
    main()
