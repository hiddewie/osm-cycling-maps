# Adapted from https://github.com/mapnik/mapnik/wiki/GettingStartedInPython
#              with https://github.com/mapnik/mapnik/issues/3258 to work with current bindings

import mapnik

m = mapnik.Map(2048, 1024)
m.background = mapnik.Color('steelblue')
s = mapnik.Style()
r = mapnik.Rule()

polygon_symbolizer = mapnik.PolygonSymbolizer()
polygon_symbolizer.fill = mapnik.Color('#f2eff9')
r.symbols.append(polygon_symbolizer)

line_symbolizer = mapnik.LineSymbolizer()
line_symbolizer.fill = mapnik.Color('rgb(50%,50%,50%)')
line_symbolizer.opacity = 0.1
r.symbols.append(line_symbolizer)

s.rules.append(r)
m.append_style('My Style', s)

layer = mapnik.Layer('world')
layer.datasource = mapnik.Shapefile(file='ne_110m_admin_0_countries.shp')
layer.styles.append('My Style')

m.layers.append(layer)
m.zoom_all()
mapnik.render_to_file(m, 'world.png', 'png')
print("rendered image to 'world.png'")