#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import os
import sys
import tempfile
import time

import PyPDF2
import cairo
import mapnik
import mapnik.printing

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

        surface = cairo.PDFSurface(file, m.width, m.height)
        # context = cairo.Context(surface)
        mapnik.render(m, surface, 1 / 2.0, 0, 0)

        # page = mapnik.printing.PDFPrinter()
        # page.render_scale(m, context)

        fontSize = 4 # points
        padding = fontSize
        # surface
        # context.move_to(0 + padding, m.height - padding)
        # context.line_to(100, m.height - 100)
        # context.set_line_width(1)
        # context.stroke()

        # class Rectangle(object):
        #
        #     def __init__(self, x=0, y=0, width=0, height=0):
        #         self.x = x
        #         self.y = y
        #         self.width = width
        #         self.height = height
        #
        #     def __repr__(self):
        #         return "({}, {}, {}, {})".format(self.x, self.y, self.width, self.height)
        #
        #     def origin(self):
        #         """Returns the top left corner coordinates in pdf points."""
        #         return (self.x, self.y)
        #
        # def render_box(ctx, rectangle, text=None, stroke_color=(0.0, 0.0, 0.0), fill_color=(1.0, 1.0, 1.0)):
        #     """
        #     Renders a box with top left corner positioned at (x,y).
        #     Default design is white fill and black stroke.
        #     """
        #     ctx.save()
        #
        #     line_width = 1
        #
        #     ctx.set_line_width(line_width)
        #     ctx.set_source_rgb(*fill_color)
        #     ctx.rectangle(rectangle.x, rectangle.y, rectangle.width, rectangle.height)
        #     ctx.fill()
        #
        #     ctx.set_source_rgb(*stroke_color)
        #     ctx.rectangle(rectangle.x, rectangle.y, rectangle.width, rectangle.height)
        #     ctx.stroke()
        #
        #     if text:
        #         ctx.move_to(rectangle.x + 1, rectangle.y)
        #         write_text(ctx, text, size=rectangle.height - 2, stroke_color=[1 - z for z in fill_color])
        #
        #     ctx.restore()
        #
        # def write_text(ctx, text, size=10, stroke_color=(0.0, 0.0, 0.0)):
        #     """
        #     Writes text to the cairo Context specified as a parameter.
        #     Returns:
        #         A rectangle (x, y, width, height) representing the extents of the text drawn
        #     """
        #     ctx.rel_move_to(0, size)
        #     ctx.select_font_face(
        #         'Noto Sans Regular',
        #         cairo.FONT_SLANT_NORMAL,
        #         cairo.FONT_WEIGHT_NORMAL)
        #     ctx.set_font_size(size)
        #     ctx.set_source_rgb(*stroke_color)
        #     ctx.show_text(text)
        #
        #     ctx.rel_move_to(0, size)
        #
        #     return (0, 0, len(text) * size, size)
        #
        # def get_div_unit( div_size, div_unit_short="m", div_unit_long="km", div_unit_divisor=1000.0):
        #     """
        #     Returns the appropriate division unit based on the division size.
        #     Args:
        #         div_size: the size of the division
        #         div_unit_short: the default string for the division unit
        #         div_unit_long: the string for the division unit if div_size is large enough to be converted
        #             from div_unit_short to div_unit_long while keeping div_size greater than 1
        #         div_unit_divisor: the divisor applied to convert from div_unit_short to div_unit_long
        #     Note:
        #         Default values use the metric system
        #     """
        #     div_unit = div_unit_short
        #     if div_size > div_unit_divisor:
        #         div_size /= div_unit_divisor
        #         div_unit = div_unit_long
        #
        #     return div_unit
        #
        # def m2pt(x, pt_size=0.0254 / 72.0):
        #     """Converts distance from meters to points. Default value is PDF point size."""
        #     return x / pt_size
        #
        # def sequence_scale(scale, scale_sequence):
        #     """Sequence scale helper, this rounds scale to a 'sensible' value."""
        #     factor = math.floor(math.log10(scale))
        #     norm = scale / (10 ** factor)
        #
        #     for s in scale_sequence:
        #         if norm <= s:
        #             return s * 10 ** factor
        #
        #     return scale_sequence[0] * 10 ** (factor + 1)
        #
        # def _get_sensible_scalebar_size(m, num_divisions=8, width=-1):
        #     """
        #     Returns a sensible scalebar size based on the map envelope, the number of divisions expected
        #     in the scalebar, and optionally the width of the containing box.
        #     """
        #     div_size = sequence_scale(m.envelope().width() / num_divisions, [1, 2, 5])
        #
        #     # ensures we can fit the bar within page area width if specified
        #     page_div_size = m.width() * div_size / m.envelope().width()
        #     while width > 0 and page_div_size > width:
        #         div_size /= 2.0
        #         page_div_size /= 2.0
        #
        #     return (div_size, page_div_size)
        #
        # def render_scale_bar(m, ctx, width=0.05, w=0, h=0, num_divisions=3, bar_size=8.0):
        #     """
        #     Renders a graphic scale bar.
        #     Returns:
        #         The width and height of the scale bar rendered
        #     """
        #     # FIXME: bug. the scale bar divisions does not scale properly when the map envelope is huge
        #     # to reproduce render python-mapnik/test/data/good_maps/agg_poly_gamma_map.xml and call render_scale
        #
        #     scale_bar_extra_space_factor = 1.2
        #     div_width = width / num_divisions * scale_bar_extra_space_factor
        #     (div_size, page_div_size) = _get_sensible_scalebar_size(m, num_divisions=num_divisions,
        #                                                                  width=div_width)
        #
        #     div_unit = get_div_unit(div_size)
        #
        #     text = "0{}".format(div_unit)
        #
        #     ctx.save()
        #     if width > 0:
        #         ctx.translate(m2pt(width - num_divisions * page_div_size) / 2, 0)
        #     for ii in range(num_divisions):
        #         fill = (ii % 2,) * 3
        #         rectangle = Rectangle(m2pt(ii * page_div_size), h, m2pt(page_div_size), bar_size)
        #         render_box(ctx, rectangle, text, fill_color=fill)
        #         fill = [1 - z for z in fill]
        #         text = "{0}{1}".format((ii + 1) * div_size, div_unit)
        #
        #     w = (num_divisions) * page_div_size
        #     h += bar_size
        #     ctx.restore()
        #
        #     return (w, h)
        #
        # def render_scale(m, ctx=None, width=0.05, num_divisions=3, bar_size=8.0,
        #                  with_representative_fraction=True):
        #     """
        #     Renders two things:
        #         - a scale bar
        #         - a scale representative fraction just below it
        #     Args:
        #         m: the Map object to render the scale for
        #         ctx: A cairo context to render the scale into. If this is None, we create a context and find out
        #             the best location for the scale bar
        #         width: the width of area available for rendering the scale bar (in meters)
        #         num_divisions: the number of divisions for the scale bar
        #         bar_size: the size of the scale bar in points
        #         with_representative_fraction: whether we should render the representative fraction or not
        #     Returns:
        #         The size of the rendered scale block in points. (0, 0) if nothing is rendered.
        #     Notes:
        #         Does not render if lat lon maps or if the aspect ratio is not preserved.
        #         The scale bar divisions alternate between black fill / white stroke and white fill / black stroke.
        #     """
        #     (w, h) = (0, 0)
        #
        #     # don't render scale text if we are in lat lon
        #     # dont render scale text if we have warped the aspect ratio
        #     # if self._preserve_aspect and not self._is_latlon:
        #
        #     # if ctx is None:
        #     #     ctx = cairo.Context(su)
        #     #     (tx, ty) = self._get_meta_info_corner((self.map_box.width(), self.map_box.height()), m)
        #     #     ctx.translate(m2pt(tx), m2pt(ty))
        #
        #     (w, h) = render_scale_bar(m, ctx, width, w, h, num_divisions, bar_size)
        #
        #     # renders the scale representative fraction text
        #     if with_representative_fraction:
        #         bar_to_fraction_space = 2
        #         context.move_to(0, h + bar_to_fraction_space)
        #
        #         box_width = None
        #         if width > 0:
        #             box_width = m2pt(width)
        #         h += self._render_scale_representative_fraction(ctx, box_width)
        #
        #     return (w, h)

        # context.move_to(0, m.height)
        # context.rel_move_to(padding, -padding)
        # context.select_font_face(
        #     'Noto Sans Regular',
        #     cairo.FONT_SLANT_NORMAL,
        #     cairo.FONT_WEIGHT_NORMAL)
        # context.set_font_size(fontSize)
        # # context.set_source_rgb('red')
        # context.show_text('© OpenStreetMap contributors')
        #
        # context.move_to(0, m.height)
        # context.rel_move_to(padding, -padding)
        # # context.rel_move_to(0, 10)
        # context.fill()
        #
        # rectangle = {
        #     'x': 5,
        #     'y': m.height - 5,
        #     'width': 20,
        #     'height': 20,
        # }
        #
        # context.save()
        #
        # line_width = 1
        #
        # context.set_line_width(line_width)
        # context.set_source_rgb(0.0, 0.0, 0.0)
        # context.rectangle(rectangle['x'], rectangle['y'], rectangle['width'], rectangle['height'])
        # context.fill()
        #
        # context.set_source_rgb(1.0, 1.0, 1.0)
        # context.rectangle(rectangle['x'], rectangle['y'], rectangle['width'], rectangle['height'])
        # context.stroke()
        #
        # context.move_to(rectangle['x'] + 1, rectangle['y'])
        # # write_text(context, text, size=rectangle['height'] - 2, stroke_color=[1 - z for z in (0.0, 0.0, 0.0)])
        #
        # context.restore()

        surface.finish()

        print('Rendered PDF')

    # page = mapnik.printing.PDFPrinter(
    #     pagesize = mapnik.printing.formats.pagesizes["a5"],
    #     margin = 0.005,
    #     box = None,
    #     percent_box = None,
    #     scale_function = '1:150000',
    #     resolution = DPI_72,
    #     preserve_aspect = True,
    #     centering = CENTERING_CONSTRAINED_AXIS,
    #     is_latlon = False,
    #     use_ocg_layers = False,
    #     font_name = "DejaVu Sans"
    # )
    #
    # pagesize = pagesizes["a4"],):
    #
    # # m = mapnik.Map(100,100)
    # # mapnik.load_map(m, "test", True)
    # # m.zoom_all()
    # page.render_map(m, file)

    print('Rendering done')


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

    if not os.path.exists(OUTPUT_PATH):
        print('Creating output directory %s' % (OUTPUT_PATH,))
        os.makedirs(OUTPUT_PATH)

    pdfWriter = PyPDF2.PdfFileWriter()
    with open('%s/%s.pdf' % (OUTPUT_PATH, name), 'wb') as outputFile:

        page = 1
        for boundingBox in boundingBoxes:
            tileBoundingBox = bounds.latitudeLongitudeToWebMercator.forward(boundingBox)

            print('Generating page %s for bounding box (%.3f, %.3f) × (%.3f, %.3f)' % (
                page, boundingBox.minx, boundingBox.miny, boundingBox.maxx, boundingBox.maxy))

            with tempfile.TemporaryFile() as tempFile:
                startTime = time.time()
                renderMap(m, tempFile, tileBoundingBox)

                print('Done rendering page %s in %.1f sec' % (page, time.time() - startTime))

                pdfReader = PyPDF2.PdfFileReader(tempFile)
                pdfWriter.addPage(pdfReader.getPage(0))
                pdfWriter.write(outputFile)

                print('Done writing PDF page %s' % (page,))

            page += 1

    print('Done rendering pages')


if __name__ == '__main__':
    main()
