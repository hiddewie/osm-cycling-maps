#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mapnik
import cairo
import os
import re

def env(key, default=None):
    return os.getenv(key, default)

def requireEnvironment(name):
    if env(name) is None:
        print ("The environment variable '%s' is required" % (name,))
        exit(1)

BASE_PATH = 'data/'
OUTPUT_PATH = 'output/'

def layer(name, srs, ds, group=None):
    lay = mapnik.Layer(name)
    lay.srs = srs
    lay.datasource = ds
    if group is not None:
        lay.group_by = group
    return lay


def shapeFile(name):
    return mapnik.Shapefile(file=BASE_PATH + name)


# Import with
#   shp2pgsql -I -d -s 4326 gis_osm_water_a_free_1.shp water_a | sudo -u postgres psql -U postgres -d gis
# -d -I is delete (and create index)
# -a is append
def postgres(table):
    return mapnik.PostGIS(host=env('PG_HOST', 'localhost'), user=env('PG_USER', 'postgres'), password=env('PG_PASSWORD', 'postgres'), dbname=env('PG_DATABASE', 'gis'), table=table)


def tableWithFclasses(table, *classes):
    return postgres('(select * from %s where %s) as subquery' % (table, 'fclass in (' + (', '.join('\'' + c + '\'' for c in classes)) + ')'))


def style(name, *rules):
    sty = mapnik.Style()
    sty.name = name

    for rule in rules:
        sty.rules.append(rule)

    return sty


def rule(symbol, filter=None):
    rul = mapnik.Rule()
    if filter is not None:
        rul.filter = mapnik.Expression(filter)
    rul.symbols.append(symbol)

    return rul


def line(width=1.0, color=None, dash=None, cap=None):
    stroke = mapnik.Stroke()
    if color is not None:
        stroke.color = color
    if dash is not None:
        stroke.add_dash(dash[0], dash[1])
    if cap is None:
        stroke.line_cap = mapnik.line_cap.ROUND_CAP
    elif cap == 'butt':
        stroke.line_cap = mapnik.line_cap.BUTT_CAP
    elif cap == 'square':
        stroke.line_cap = mapnik.line_cap.SQUARE_CAP
    stroke.line_join = mapnik.line_join.ROUND_JOIN
    stroke.width = width

    return mapnik.LineSymbolizer(stroke)


def lineStyle(name, filters, width, borderWidth, color, borderColor, dash=None, cap=None):
    return [
        style(name + '-border', rule(
            line(width + borderWidth, borderColor, cap=cap),
            *filters
        )),
        style(name + '-fill', rule(
            line(width, color, dash=dash, cap=cap),
            *filters
        )),
    ]


def polygon(fill=None):
    symbolizer = mapnik.PolygonSymbolizer()
    if fill is not None:
        symbolizer.fill = fill

    return symbolizer


def polygonWithBorderStyle(name, fill, borderWidth, borderColor, *rules):
    return style(
        name,
        rule(
            polygon(fill),
            *rules
        ),
        rule(
            line(borderWidth, borderColor),
            *rules
        ),
    )


def pattern(file):
    symbolizer = mapnik.PolygonPatternSymbolizer(mapnik.PathExpression(file))
    symbolizer.transform = 'scale(0.4, 0.4)'
    return symbolizer


def raster(opacity=1.0):
    symbolizer = mapnik.RasterSymbolizer()
    symbolizer.scaling = mapnik.scaling_method.BILINEAR8
    symbolizer.opacity = opacity
    return symbolizer


def point(color=None, stroke=None):
    symbolizer = mapnik.MarkersSymbolizer()
    symbolizer.transform = 'scale(0.3, 0.3)'
    if color is not None:
        symbolizer.fill = color
    if stroke is not None:
        symbolizer.stroke = stroke
    symbolizer.allow_overlap = True
    return symbolizer


def icon(file, transform=None, color=None, allowOverlap=False):
    symbolizer = mapnik.MarkersSymbolizer()
    symbolizer.filename = file
    symbolizer.allow_overlap = allowOverlap
    if color is not None:
        symbolizer.fill = color
    if transform is not None:
        symbolizer.transform = transform

    return symbolizer


def shield():
    symbolizer = mapnik.ShieldSymbolizer(mapnik.Expression('[ref]'), 'DejaVu Sans Book', 8, mapnik.Color('black'),
                                         mapnik.PathExpression(BASE_PATH + '../shields/motorway_shield4.png'))
    # symbolizer.filename = file
    # symbolizer.allow_overlap = True
    # if color is not None:
    #     symbolizer.fill = color
    # if transform is not None:
    #     symbolizer.transform = transform
    symbolizer.min_distance = 300

    return symbolizer


def maki(name, color=None, scaleFactor=None, allowOverlap=False):
    scale = 0.68 * (scaleFactor if scaleFactor is not None else 1.0)
    return icon(BASE_PATH + 'icons/maki/' + name + '.svg', 'scale(%s, %s)' % (scale, scale),
                color=color if color is not None else mapnik.Color('black'),
                allowOverlap=allowOverlap)


def svg(name, color=None, scaleFactor=None, allowOverlap=False):
    scale = 0.03 * (scaleFactor if scaleFactor is not None else 1.0)
    return icon(BASE_PATH + 'icons/svg/' + name + '.svg', 'scale(%s, %s)' % (scale, scale),
                color=color if color is not None else mapnik.Color('black'),
                allowOverlap=allowOverlap)


def svgStyle(name, filter):
    return style(
        name,
        rule(
            maki('circle-11', color=mapnik.Color(250, 250, 250, 200), scaleFactor=1.5, allowOverlap=True),
            filter
        ),
        rule(
            svg(name, color=mapnik.Color(80, 0, 0), allowOverlap=True),
            filter
        ),
    )


def makiStyle(name, filter):
    return style(
        name,
        rule(
            maki('circle-11', color=mapnik.Color(250, 250, 250, 200), scaleFactor=1.5, allowOverlap=True),
            filter
        ),
        rule(
            maki(name, color=mapnik.Color('purple'), allowOverlap=True),
            filter
        ),
    )


def classFilter(*classes):
    return '(' + (' or '.join('[fclass] = \'' + c + '\'' for c in classes)) + ')'


def booleanFilter(property, value):
    return '[%s] = \'%s\'' % (property, 'T' if value else 'F')


def noBridge():
    return booleanFilter('bridge', False)


def bridge():
    return booleanFilter('bridge', True)


def andExpr(*expressions):
    return '(' + (' and '.join(expressions)) + ')'


def text(expression, size, color, fontVariant=None, haloRadius=None, halo=mapnik.Color(255, 255, 200), transform=None,
         placement=None, minPathLength=None):
    font = 'DejaVu Sans Book'
    if fontVariant is not None and fontVariant == 'bold':
        font = 'DejaVu Sans Bold'
    symbolizer = mapnik.TextSymbolizer(expression, font, size, color)

    symbolizer.label_placement = mapnik.label_placement.POINT_PLACEMENT
    if placement is not None and placement == 'line':
        symbolizer.label_placement = mapnik.label_placement.LINE_PLACEMENT
    if halo is not None:
        symbolizer.halo_fill = halo
    if haloRadius is not None:
        symbolizer.halo_radius = haloRadius
    symbolizer.placement_type = 'simple'
    
    symbolizer.avoid_edges = True
    symbolizer.allow_overlap = False
    if transform is not None:
        symbolizer.text_transform = transform

    if minPathLength is not None:
        symbolizer.minimum_distance = minPathLength
        symbolizer.minimum_path_length = minPathLength

    return symbolizer


def addLayerWithStylesToMap(m, layer, *styles):
    for s in styles:
        try:
            for ss in iter(s):
                addStyle(m, layer, ss)
        except TypeError:
            addStyle(m, layer, s)
    m.layers.append(layer)


def addStyle(m, layer, s):
    print 'Adding style %s' % (s.name,)
    m.append_style(s.name, s)
    layer.styles.append(s.name)


def generateMap(width, height, topLeft, bottomRight):
    m = mapnik.Map(width, height, "+init=epsg:3857")
    m.background = mapnik.Color('white')

    # Download layer data from http://download.geofabrik.de/europe.html

    addLayerWithStylesToMap(
        m,
        layer('Landuse', "+init=epsg:4326", tableWithFclasses('landuse_a', 'forest')),
        style('forest', rule(
            polygon(mapnik.Color(222, 245, 198)),
            classFilter('forest')
        )),
    )

    # Download at https://dds.cr.usgs.gov/srtm/version2_1/SRTM3/
    # Generate with
    #    gdaldem hillshade N49E019.hgt N49E019.tif
    for shade in SHADE_NAMES:
        addLayerWithStylesToMap(
            m,
            layer('shade-' + shade, "+init=epsg:4326", mapnik.Gdal(file=BASE_PATH + ('%s.tif' % (shade,)))),
            style('shade-', rule(
                raster(0.15),
            ))
        )

    # Generate with
    #    gdal_contour -i 20 -snodata -32768 -a height  /mnt/d/mapnik-data/slovakia/N49E019.hgt /mnt/d/mapnik-data/slovakia/N49E019.shp
    addLayerWithStylesToMap(
        m,
        layer('contours', "+init=epsg:4326", postgres('contours')),
        style(
            'contours',
            rule(
                line(0.5, mapnik.Color(145, 132, 83, 100)),
                '[height] % 100 != 0',
            ),
            rule(
                line(1.0, mapnik.Color(145, 132, 83, 140)),
                '[height] % 100 = 0',
            ),
            rule(
                text(mapnik.Expression('[height]'), 6, mapnik.Color(145, 132, 83), halo=mapnik.Color('white'),
                     haloRadius=1.0, placement='line'),
                '[height] % 100 = 0',
            ),
        )
    )

    addLayerWithStylesToMap(
        m,
        layer('Landuse', "+init=epsg:4326", tableWithFclasses('landuse_a', 'residential', 'military')),  # , tableWithFclasses('landuse_a', 'forest')),
        style('residential', rule(
            polygon(mapnik.Color(201, 180, 133)),
            classFilter('residential')
        )),
        # polygonWithBorderStyle(
        #     'national_park', mapnik.Color('purple'), 6.0, mapnik.Color('red'),
        #     classFilter('national_park')
        # ),
        polygonWithBorderStyle(
            'military', mapnik.Color(255, 51, 51, 150), 1.0, mapnik.Color(255, 0, 0),
            classFilter('military')
        ),
    )

    # Download from https://wambachers-osm.website/boundaries/
    addLayerWithStylesToMap(
        m,
        layer('countries', "+init=epsg:4326", postgres('country_border')),
        lineStyle('countries', [], 1, 9, mapnik.Color(0, 74, 24, 200), mapnik.Color(0, 219, 68, 120), dash=[10, 4]),
    )

    addLayerWithStylesToMap(
        m,
        layer('waterways', "+init=epsg:4326", postgres('waterways')),
        style('waterways', rule(
            line(1.0, mapnik.Color(53, 134, 212))
        ))
    )

    addLayerWithStylesToMap(
        m,
        layer('water', "+init=epsg:4326", postgres('water_a')),
        polygonWithBorderStyle('water', mapnik.Color(123, 179, 232), 1.0, mapnik.Color(53, 134, 212)),
    )

    addLayerWithStylesToMap(
        m,
        layer('natural', "+init=epsg:4326", tableWithFclasses('natural_a', 'spring')),
        style('spring', rule(
            point(mapnik.Color(123, 179, 232), mapnik.Stroke(mapnik.Color(53, 134, 212), 1)),
            classFilter('spring')
        )),
    )

    addLayerWithStylesToMap(
        m,
        layer('Train', "+init=epsg:4326", tableWithFclasses('railways', 'rail'), 'name'),
        style(
            'rail',
            rule(
                line(1.5, mapnik.Color('black'), cap='square'),
                classFilter('rail')
            ),
            rule(
                line(1, mapnik.Color('white'), cap='square'),
                classFilter('rail')
            ),
            rule(
                line(1, mapnik.Color('black'), [5, 5], cap='square'),
                classFilter('rail')
            )
        ),
    )

    trackColor = mapnik.Color(105, 105, 105)
    cycleColor, cycleBorderColor = mapnik.Color(176, 58, 240), mapnik.Color('white')
    unclassifiedColor, unclassifiedBorderColor = mapnik.Color('white'), mapnik.Color(82, 82, 82)
    tertiaryColor, tertiaryBorderColor = unclassifiedColor, unclassifiedBorderColor
    secondaryColor, secondaryBorderColor = mapnik.Color(232, 232, 16), mapnik.Color(99, 99, 6)
    primaryColor, primaryBorderColor = mapnik.Color(219, 143, 35), mapnik.Color(168, 109, 25)
    trunkColor, trunkBorderColor = mapnik.Color(158, 158, 158), mapnik.Color('white')
    highwayColor, highwayBorderColor = mapnik.Color(120, 120, 120), mapnik.Color('white')
    bridgeBaseBorderColor, bridgeBorderColor = mapnik.Color('white'), mapnik.Color('black')

    addLayerWithStylesToMap(
        m,
        layer('Unclassified tertiary', "+init=epsg:4326", postgres('roads')),

        style('track-bad', rule(
            line(1.0, trackColor, [4, 3], cap='butt'),
            classFilter('track_grade3', 'track_grade4', 'track_grade5')
        )),
        style('track', rule(
            line(1.0, trackColor),
            classFilter('track', 'track_grade1', 'track_grade2')
        )),

        style('unclassified-border', rule(
            line(2.0, unclassifiedBorderColor),
            classFilter('unclassified', 'residential')
        )),
        style('tertiary-border', rule(
            line(3.0, tertiaryBorderColor),
            classFilter('tertiary')
        )),
        style('secondary-border', rule(
            line(3.0, secondaryBorderColor),
            classFilter('secondary', 'secondary_link')
        )),
        
        style('cycleway-border', rule(
            line(2.0, cycleBorderColor),
            classFilter('cycleway')
        )),

        style('primary-border', rule(
            line(3.0, primaryBorderColor),
            classFilter('primary', 'primary_link')
        )),
        style('trunk-border', rule(
            line(3.0, trunkBorderColor),
            classFilter('trunk', 'trunk_link')
        )),
        style('highway-border', rule(
            line(3.0, highwayBorderColor),
            classFilter('motorway', 'motorway_link')
        )),

        style('secondary-link-fill', rule(
            line(2.0, secondaryColor),
            classFilter('secondary_link')
        )),
        style('primary-link-fill', rule(
            line(2.0, primaryColor),
            classFilter('primary_link')
        )),
        style('trunk-link-fill', rule(
            line(2.0, trunkColor),
            classFilter('trunk_link')
        )),
        style('highway-link-fill', rule(
            line(2.0, highwayColor),
            classFilter('motorway_link')
        )),

        style('unclassified-fill', rule(
            line(0.5, unclassifiedColor),
            classFilter('unclassified', 'residential')
        )),
        style('tertiary-fill', rule(
            line(2.0, tertiaryColor),
            classFilter('tertiary')
        )),
        style('secondary-fill', rule(
            line(2.0, secondaryColor),
            classFilter('secondary')
        )),

        style('cycleway', rule(
            line(1.0, cycleColor),
            classFilter('cycleway')
        )),

        style('primary-fill', rule(
            line(2.0, primaryColor),
            classFilter('primary')
        )),
        style('trunk-fill', rule(
            line(2.0, trunkColor),
            classFilter('trunk')
        )),
        style('highway-fill', rule(
            line(2.0, highwayColor),
            classFilter('motorway')
        )),

        ### Bridges

        lineStyle(
            'bridge-basis',
            [andExpr(
                bridge(),
                classFilter('secondary', 'secondary_link', 'primary', 'primary_link',
                            'trunk', 'trunk_link', 'motorway', 'motorway_link'),
            )],
            3.0, 1.0,
            bridgeBaseBorderColor, bridgeBorderColor,
            cap='butt'
        ),

        style('secondary-link-bridge-fill', rule(
            line(2.0, secondaryColor),
            andExpr(bridge(), classFilter('secondary_link'))
        )),
        style('primary-link-bridge-fill', rule(
            line(2.0, primaryColor),
            andExpr(bridge(), classFilter('primary_link'))
        )),
        style('trunk-link-bridge-fill', rule(
            line(2.0, trunkColor),
            andExpr(bridge(), classFilter('trunk_link'))
        )),
        style('highway-link-bridge-fill', rule(
            line(2.0, highwayColor),
            andExpr(bridge(), classFilter('motorway_link'))
        )),
        style('tertiary-bridge-fill', rule(
            line(2.0, tertiaryColor),
            andExpr(bridge(), classFilter('tertiary'))
        )),
        style('secondary-bridge-fill', rule(
            line(2.0, secondaryColor),
            andExpr(bridge(), classFilter('secondary'))
        )),

        style('cycleway', rule(
            line(1.0, cycleColor),
            andExpr(bridge(), classFilter('cycleway'))
        )),
        
        style('primary-bridge-fill', rule(
            line(2.0, primaryColor),
            andExpr(bridge(), classFilter('primary'))
        )),
        style('trunk-bridge-fill', rule(
            line(2.0, trunkColor),
            andExpr(bridge(), classFilter('trunk'))
        )),
        style('highway-bridge-fill', rule(
            line(2.0, highwayColor),
            andExpr(bridge(), classFilter('motorway'))
        )),
    )

    addLayerWithStylesToMap(
        m,
        layer('Populated Places', "+init=epsg:4326", tableWithFclasses('places', 'national_capital', 'city', 'town', 'village', 'hamlet', 'suburb', 'locality')),
        style('capital', rule(
            text(mapnik.Expression("[name]"), 18, mapnik.Color('black'), 'bold', 1, mapnik.Color(255, 255, 220, 180), mapnik.text_transform.UPPERCASE),
            classFilter('national_capital')
        )),
        style('city', rule(
            text(mapnik.Expression("[name]"), 14, mapnik.Color('black'), 'bold', 1, mapnik.Color(255, 255, 220, 180), mapnik.text_transform.UPPERCASE),
            classFilter('city')
        )),
        style('town', rule(
            text(mapnik.Expression("[name]"), 12, mapnik.Color('black'), 'bold', 1, mapnik.Color(255, 255, 220, 180)),
            classFilter('town')
        )),
        style('village', rule(
            text(mapnik.Expression("[name]"), 10, mapnik.Color('black'), None, 1, mapnik.Color(255, 255, 220, 180)),
            classFilter('village')
        )),
        style('hamlet-suburb', rule(
            text(mapnik.Expression("[name]"), 7, mapnik.Color('black'), None, 1, mapnik.Color(255, 255, 220, 180)),
            classFilter('hamlet', 'suburb')
        )),
        style('locality', rule(
            text(mapnik.Expression("[name]"), 7, mapnik.Color('black'), None, 1, mapnik.Color(255, 255, 220, 180), mapnik.text_transform.UPPERCASE),
            classFilter('locality') + ' and [population] > 0'
        )),
    )

    ### Names

    addLayerWithStylesToMap(
        m,
        layer('Unclassified tertiary', "+init=epsg:4326", tableWithFclasses('roads', 'tertiary', 'secondary', 'primary', 'trunk', 'motorway')),
        style('tertiary-name', rule(
            text(mapnik.Expression("[ref]"), 7, mapnik.Color('white'), 'bold', 1.0, mapnik.Color(82, 82, 82), placement='line', minPathLength=70),
            classFilter('tertiary')
        )),
        style('secondary-name', rule(
            text(mapnik.Expression("[ref]"), 8, mapnik.Color('white'), 'bold', 1.0, mapnik.Color(99, 99, 6), placement='line', minPathLength=70),
            classFilter('secondary')
        )),
        style('primary-name', rule(
            text(mapnik.Expression("[ref]"), 8, mapnik.Color('white'), 'bold', 1.0, mapnik.Color(168, 109, 25), placement='line', minPathLength=70),
            classFilter('primary')
        )),
        style('trunk-name', rule(
            text(mapnik.Expression("[ref]"), 8, mapnik.Color('white'), 'bold', 1.0, mapnik.Color(115, 35, 17), placement='line', minPathLength=70),
            classFilter('trunk')
        )),
        style('highway-name', rule(
            text(mapnik.Expression("[ref]"), 8, mapnik.Color('white'), 'bold', 1.0, mapnik.Color('black'), placement='line', minPathLength=70),
            classFilter('motorway')
        )),
    )

    addLayerWithStylesToMap(
        m,
        layer('contours-100', "+init=epsg:4326", postgres('contours')),
        style('contours-100-text', rule(
            text(mapnik.Expression('[height]'), 6, mapnik.Color(145, 132, 83), halo=mapnik.Color('white'),
                 haloRadius=1.0, placement='line', minPathLength=50),
            '[height] % 100 = 0',
        )),
    )

    addLayerWithStylesToMap(
        m,
        layer('transport', "+init=epsg:4326", tableWithFclasses('transport', 'railway_station', 'railway_halt', 'airfield', 'airport')),
        makiStyle('rail-11', classFilter('railway_station', 'railway_halt')),
        makiStyle('airfield-11', classFilter('airfield')),
        makiStyle('airport-11', classFilter('airport')),
    )

    poiStyles = [
        makiStyle('campsite-11', classFilter('camp_site')),
        makiStyle('hospital-11', classFilter('hospital')),
        makiStyle('swimming-11', classFilter('swimming_pool')),
        svgStyle('caravan_site', classFilter('caravan_site')),
        makiStyle('shop-11', classFilter('supermarket')),
        makiStyle('bicycle-11', classFilter('bicycle_shop')),
        makiStyle('castle-11', classFilter('castle', 'fort')),
        svgStyle('ruins', classFilter('ruins')),
        makiStyle('communications-tower-11', classFilter('tower_comms')),
        makiStyle('viewpoint-11', classFilter('tower_observation')),
        svgStyle('tower', classFilter('tower')),
        makiStyle('lighthouse-11', classFilter('lighthouse')),
    ]
    addLayerWithStylesToMap(
        m,
        layer('poi', "+init=epsg:4326", postgres('poi')),
        *poiStyles
    )
    addLayerWithStylesToMap(
        m,
        layer('poi-area', "+init=epsg:4326", postgres('poi_a')),
        *poiStyles
    )

    addLayerWithStylesToMap(
        m,
        layer('pofw', "+init=epsg:4326", postgres('pofw')),
        makiStyle(
            'religious-christian-11',
            classFilter(
                'christian',
                'christian_anglican',
                'christian_catholic',
                'christian_evangelical',
                'christian_lutheran',
                'christian_methodist',
                'christian_orthodox',
                'christian_protestant',
                'christian_babtist',
                'christian_mormon',
            )
        ),
        makiStyle('religious-jewish-11', classFilter('jewish')),
        makiStyle('religious-muslim-11', classFilter('muslim', 'muslim_sunni', 'muslim_shia')),
        makiStyle('religious-buddhist-11', classFilter('buddhist')),
    )

    m.zoom_to_box(mapnik.Box2d(topLeft[0], topLeft[1], bottomRight[0], bottomRight[1]))

    return m


def renderMap(m, name):
    print 'Rendering map with dimensions %s, %s' % (m.width, m.height)
    im = mapnik.Image(m.width, m.height)
    mapnik.render(m, im)

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

requireEnvironment('TOP_LEFT_X')
requireEnvironment('TOP_LEFT_Y')

name=env('MAP_NAME', 'map')

LATITUDES = envList(env('LATITUDES', 'N52'), '^[NS][0-9]{2}$')
LONGITUDES = envList(env('LONGITUDES', 'E006'), '^[EW][0-9]{3}$')

SHADE_NAMES = [lat + lon for lat in LATITUDES for lon in LONGITUDES]

print ('Using name \'%s\'' % (name, ))
print ('Using latitudes %s' % (LATITUDES, ))
print ('Using longitudes %s' % (LONGITUDES, ))

# Choose with https://epsg.io/map#srs=3857&x=2225846.263664&y=6275978.874398&z=8&layer=streets
# In EPSG:3857
TOP_LEFT_X=int(env('TOP_LEFT_X', 735324))
TOP_LEFT_Y=int(env('TOP_LEFT_Y', 6874058))

OFFSET_PAGES_X=int(env('OFFSET_PAGES_X', 0))
OFFSET_PAGES_Y=int(env('OFFSET_PAGES_Y', 0))

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

enschede = (TOP_LEFT_X, TOP_LEFT_Y)

pageWidth = 29693
pageHeight = - 1.414 * pageWidth
topLeft = int(enschede[0] + i * pageWidth), int(enschede[1] + j * pageHeight)
bottomRight = int(topLeft[0] + numPagesHorizontal * pageWidth), int(topLeft[1] + numPagesVertical * pageHeight)

print ('Generating from top left (%s, %s) to bottom right (%s, %s) (%s pages horizontal and %s pages vertical)' % (topLeft[0], topLeft[1], bottomRight[0], bottomRight[1], numPagesHorizontal, numPagesVertical))

m = generateMap(numPagesHorizontal * int(width * dpi), numPagesVertical * int(height * dpi), topLeft, bottomRight)
renderMap(m, name)