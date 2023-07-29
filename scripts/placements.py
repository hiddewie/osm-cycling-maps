#!/usr/bin/env python3

# Usage: python3 placements.py
# Output: a list of placements for places, in a grid determined by the parameters.
#
# Run this script to generate the file placements.xml which can be used for substitution in Mapnik XML.

grid = {
    'vertical': 30,
    'horizontal': 50,
}
step = 5

# Generate a list of placement tuples...
placements = [(x, y) for x in range(-grid['horizontal'], grid['horizontal'] + 1, step) for y in range(-grid['vertical'], grid['vertical'] + 1, step)]
# ...sorted by distance from the center outwards
placements.sort(key=lambda p: abs(p[0]) + abs(p[1]))

output = ''.join(map(lambda p: '<Placement dx=\'%s\' dy=\'%s\'/>' % p, placements))

print(output)
