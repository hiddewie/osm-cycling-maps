#!/usr/bin/env python3

import logging
import os
import re
import sys
import threading
import time
from math import pi, sin, log, exp, atan
from queue import Queue

import mapnik

import environment

# Followed https://wiki.openstreetmap.org/wiki/Creating_your_own_tiles
# This script is adapted from https://raw.githubusercontent.com/openstreetmap/mapnik-stylesheets/master/generate_tiles.py
# Also see http://tools.geofabrik.de/calc/#type=geofabrik_standard&bbox=2.659645,50.515134,7.746561,54.07489 for counting tiles
# Also see https://github.com/magellium/osmtilemaker, improve that?

logger = logging.getLogger("genTile")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(threadName)-12s %(levelname)-6s %(message)s', "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)


def closeLoggingStreamHandlers():
    logger.debug('Close logging streamHandlers')
    for handler in logger.handlers:
        handler.close()
        logger.removeFilter(handler)


DEG_TO_RAD = pi / 180
RAD_TO_DEG = 180 / pi

OUTPUT_PATH = 'output/tiles/'


def constrain(x, mi, ma):
    """Constrain the value of x such that mi <= x <= ma"""
    x = max(x, mi)
    x = min(x, ma)
    return x


class GoogleProjection:
    def __init__(self, levels=18):
        self.Bc = []
        self.Cc = []
        self.zc = []
        self.Ac = []
        c = 256

        for d in range(0, levels):
            e = c / 2
            self.Bc.append(c / 360.0)
            self.Cc.append(c / (2 * pi))
            self.zc.append((e, e))
            self.Ac.append(c)
            c *= 2

    def fromLLtoPixel(self, ll, zoom):
        d = self.zc[zoom]
        e = round(d[0] + ll[0] * self.Bc[zoom])
        f = constrain(sin(DEG_TO_RAD * ll[1]), -0.9999, 0.9999)
        g = round(d[1] + 0.5 * log((1 + f) / (1 - f)) * -self.Cc[zoom])
        return e, g

    def fromPixelToLL(self, px, zoom):
        e = self.zc[zoom]
        f = (px[0] - e[0]) / self.Bc[zoom]
        g = (px[1] - e[1]) / -self.Cc[zoom]
        h = RAD_TO_DEG * (2 * atan(exp(g)) - 0.5 * pi)
        return f, h


class RenderThread:
    def __init__(self, tile_dir, mapfile, queue, maxZoom, skipIfExists):
        self.tileDirectory = tile_dir
        self.queue = queue
        self.skipIfExists = skipIfExists
        self.map = mapnik.Map(256, 256)
        self.map.background = mapnik.Color('white')
        # Load style XML
        mapnik.load_map(self.map, mapfile, True)
        # Obtain <Map> projection
        self.projection = mapnik.Projection(self.map.srs)
        # Projects between tile pixel co-ordinates and LatLong (EPSG:4326)
        self.tileProjection = GoogleProjection(maxZoom + 1)

    def render_tile(self, tileFilename, x, y, z):

        # Calculate pixel positions of bottom-left & top-right
        p0 = (x * 256, (y + 1) * 256)
        p1 = ((x + 1) * 256, y * 256)

        # Convert to LatLong (EPSG:4326)
        l0 = self.tileProjection.fromPixelToLL(p0, z)
        l1 = self.tileProjection.fromPixelToLL(p1, z)

        # Convert to map projection (e.g. mercator co-ords EPSG:900913)
        c0 = self.projection.forward(mapnik.Coord(l0[0], l0[1]))
        c1 = self.projection.forward(mapnik.Coord(l1[0], l1[1]))

        # Bounding box for the tile
        bbox = mapnik.Box2d(c0.x, c0.y, c1.x, c1.y)
        render_size = 256
        self.map.resize(render_size, render_size)
        self.map.zoom_to_box(bbox)
        if self.map.buffer_size < 128:
            self.map.buffer_size = 128

        # Render image with default Agg renderer
        im = mapnik.Image(render_size, render_size)
        mapnik.render(self.map, im)
        im.save(tileFilename, 'png256')

    def loop(self):
        logger.info('RenderThread starting loop')
        while True:
            # Fetch a tile from the queue and render it
            r = self.queue.get()
            if r is None:
                self.queue.task_done()
                break
            else:
                (tileFilename, x, y, z) = r

            if self.skipIfExists and os.path.isfile(tileFilename):
                logger.info('Skipping {z = %s, x = %s, y = %s}, file exists', z, x, y)
            else:
                start = time.perf_counter()
                self.render_tile(tileFilename, x, y, z)
                logger.info('Rendered {z = %s, x = %s, y = %s} in %s sec', z, x, y, round((time.perf_counter() - start) * 100) / 100)
            self.queue.task_done()
        logger.info('RenderThread finished')


def renderTiles(bbox, mapnikConfiguration, tileDirectory, minZoom, maxZoom, numThreads, tmsScheme, skipIfExists):
    logger.info('Rendering tiles for bounding box %s, map file %s, output directory %s, zoom levels [%s, %s]', bbox, mapnikConfiguration, tileDirectory, minZoom, maxZoom)

    queue = Queue(32)
    renderers = {}
    logger.info('Launching %s rendering threads', numThreads)
    for i in range(numThreads):
        renderer = RenderThread(tileDirectory, mapnikConfiguration, queue, maxZoom, skipIfExists)
        render_thread = threading.Thread(target=renderer.loop, name='Rendering-%s' % (i + 1,))
        render_thread.start()
        renderers[i] = render_thread
    logger.info('Rendering threads started')

    startTime = time.time()
    if not os.path.isdir(tileDirectory):
        logger.info('Generating output directory %s', tileDirectory)
        os.mkdir(tileDirectory)

    gprj = GoogleProjection(maxZoom + 1)

    ll0 = (bbox[0], bbox[3])
    ll1 = (bbox[2], bbox[1])

    numTiles = 0
    for z in range(minZoom, maxZoom + 1):
        logger.info('Generating jobs for zoom level %s', z)
        px0 = gprj.fromLLtoPixel(ll0, z)
        px1 = gprj.fromLLtoPixel(ll1, z)

        # check if we have directories in place
        zoomDirectory = "%s%s" % (tileDirectory, z)
        if not os.path.isdir(zoomDirectory):
            os.mkdir(zoomDirectory)
            logger.info('Tile directory %s created', zoomDirectory)

        for x in range(int(px0[0] / 256.0), int(px1[0] / 256.0) + 1):
            # Validate x co-ordinate
            if (x < 0) or (x >= 2 ** z):
                continue

            # Check if we have directories in place
            targetDirectory = "%s/%s" % (zoomDirectory, x)
            if not os.path.isdir(targetDirectory):
                os.mkdir(targetDirectory)
                logger.info('Tile directory %s created', targetDirectory)

            for y in range(int(px0[1] / 256.0), int(px1[1] / 256.0) + 1):
                # Validate x co-ordinate
                if (y < 0) or (y >= 2 ** z):
                    continue

                # Flip y to match OSGEO TMS spec
                schemeY = y if not tmsScheme else ((2 ** z - 1) - y)
                fileFilename = "%s/%s.png" % (targetDirectory, schemeY)
                # Submit tile to be rendered into the queue
                queueJob = (fileFilename, x, schemeY, z)
                try:
                    queue.put(queueJob)
                    numTiles += 1
                except KeyboardInterrupt:
                    raise SystemExit("Ctrl-c detected, exiting...")

    # Signal render threads to exit by sending empty request to queue
    for i in range(numThreads):
        queue.put(None)

    # Wait for pending rendering jobs to complete
    logger.info('Waiting until all renderers have competed')
    queue.join()
    for i in range(numThreads):
        renderers[i].join()
    logger.info('All renderers have competed')

    logger.info('Rendered %s tiles in %s sec', numTiles, round((time.time() - startTime) * 10) / 10)


def determineBoundingBox(bbox):
    bboxMatch = re.match(r'^(\d+\.?\d*):(\d+\.?\d*):(\d+\.?\d*):(\d+\.?\d*)$', bbox)

    if not bboxMatch:
        environment.exitError("The bounding box must be of the form A:B:C:D with (A, B) the bottom left corner and (C, D) the top right corner. %s was given" % (bbox,))
        return

    return float(bboxMatch.group(1)), float(bboxMatch.group(2)), float(bboxMatch.group(3)), float(bboxMatch.group(4)),


def main():
    mapnikConfiguration = environment.require('MAPNIK_CONFIGURATION')
    logger.info('Using Mapnik configuration file %s', mapnikConfiguration)

    bbox = determineBoundingBox(environment.require('BBOX'))
    logger.info('Using bounding box %s', bbox)

    numThreads = int(environment.env('NUM_THREADS', 6))
    logger.info('Using %s threads', numThreads)

    minZoom = int(environment.env('MIN_ZOOM', 12))
    maxZoom = int(environment.env('MAX_ZOOM', 12))
    logger.info('Processing zoom levels [%s, %s]', minZoom, maxZoom)

    tmsScheme = environment.env('TMS_SCHEME', 'false') == 'true'
    if tmsScheme:
        logger.info('Using TMS scheme')

    skipIfExists = environment.env('SKIP_IF_EXISTS', 'true') != 'false'
    if skipIfExists:
        logger.info('Skipping tile generation if tile exists')

    renderTiles(bbox, mapnikConfiguration, OUTPUT_PATH, minZoom, maxZoom, numThreads, tmsScheme, skipIfExists)


if __name__ == '__main__':
    try:
        main()
    finally:
        closeLoggingStreamHandlers()
