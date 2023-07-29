#!/usr/bin/env python3

# Generate legend OSM XML content.

import sys

import lxml.etree
import yaml

# Global ID generator
_nextNodeId = -0
_nextWayId = -1000
_nextRelationId = -2000


def nextNodeId():
    global _nextNodeId
    _nextNodeId -= 1
    return _nextNodeId


def nextWayId():
    global _nextWayId
    _nextWayId -= 1
    return _nextWayId


def nextRelationId():
    global _nextRelationId
    _nextRelationId -= 1
    return _nextRelationId


def interpolate(min, max, alpha):
    return min + alpha * (max - min)


def equalProportions(count):
    if count < 1:
        return

    yield from (1 / count for _ in range(count))


def split(min, max, proportions, padding):
    s = 0
    listedProportions = list(proportions)
    for index, proportion in enumerate(listedProportions):
        yield {
            'min': interpolate(min, max, interpolate(s, s + proportion, padding if index != 0 else 0)),
            'max': interpolate(min, max, interpolate(s, s + proportion, 1.0 - (padding if index != len(listedProportions) - 1 else 0))),
        }
        s += proportion


def splitEqualHorizontal(bounds, count, padding):
    yield from splitProportionalHorizontal(bounds, equalProportions(count), padding)


def splitEqualVertical(bounds, count, padding):
    yield from splitProportionalVertical(bounds, equalProportions(count), padding)


def splitProportionalHorizontal(bounds, proportions, padding):
    for lon in split(bounds['lon']['min'], bounds['lon']['max'], proportions, padding):
        yield {
            'lat': bounds['lat'],
            'lon': lon,
        }


def splitProportionalVertical(bounds, proportions, padding):
    for lat in reversed(list(split(bounds['lat']['min'], bounds['lat']['max'], reversed(list(proportions)), padding))):
        yield {
            'lat': lat,
            'lon': bounds['lon'],
        }


def center(bounds):
    return interpolate(bounds['lat']['min'], bounds['lat']['max'], 0.5), interpolate(bounds['lon']['min'], bounds['lon']['max'], 0.5)


def generateTag(key, value):
    tag = lxml.etree.Element('tag')

    tag.set('k', key)
    tag.set('v', value)

    return tag


def generateNode(id, position, tags):
    node = lxml.etree.Element('node')

    lat, lon = position

    node.set('id', str(id))
    node.set('lat', str(lat))
    node.set('lon', str(lon))

    for name, value in tags.items():
        node.append(generateTag(name, value))

    return node


def generateNd(ref):
    nd = lxml.etree.Element('nd')
    nd.set('ref', str(ref))
    return nd


def generateWay(id, nodes, tags):
    way = lxml.etree.Element('way')

    way.set('id', str(id))

    for node in nodes:
        way.append(generateNd(node))

    for name, value in tags.items():
        way.append(generateTag(name, value))

    return way


def generateMember(role, ref):
    member = lxml.etree.Element('member')
    member.set('type', 'way')
    member.set('ref', str(ref))
    member.set('role', role)
    return member


def generateRelation(id, members, tags):
    relation = lxml.etree.Element('relation')

    relation.set('id', str(id))

    for role, ref in members.items():
        relation.append(generateMember(role, ref))

    for name, value in tags.items():
        relation.append(generateTag(name, value))

    return relation


def generateXml(config):
    osm = lxml.etree.Element('osm')
    osm.set('version', '0.6')
    osm.set('upload', 'false')

    nodes = []
    ways = []
    relations = []

    bounds = {
        'lat': {
            'min': -0.03,
            'max': 0.125
        },
        'lon': {
            'min': -0.025,
            'max': 0.18,
        },
    }

    nodes.append(generateNode(nextNodeId(), (bounds['lat']['max'], interpolate(bounds['lon']['min'], bounds['lon']['max'], 0.5)), {'place': 'city', 'name': 'Legend'}))

    for column, columnBounds in zip(config['columns'], splitEqualHorizontal(list(splitProportionalVertical(bounds, [0.1, 0.9], 0.0))[1], len(config['columns']), 0.05)):
        for row, rowBounds in zip(column['rows'], splitEqualVertical(columnBounds, len(column['rows']), 0.05)):
            contentRowBounds, legendRowBounds = splitProportionalHorizontal(rowBounds, [0.75, 0.25], 0.05)

            if 'description' in row:
                nodes.append(generateNode(nextNodeId(), center(legendRowBounds), {
                    'name': row['description'],
                    'place': 'village',
                }))

            for section, sectionBounds in zip(row['sections'], splitEqualHorizontal(contentRowBounds, len(row['sections']), 0.05)):

                if 'node' in section:
                    node = section['node']
                    tags = node['tags']
                    duplication = node['duplicate'] if 'duplicate' in node else 1
                    for i in range(duplication):
                        nodes.append(generateNode(nextNodeId(), center(sectionBounds), tags))

                elif 'way' in section:
                    way = section['way']
                    tags = way['tags']
                    n1, n2 = nextNodeId(), nextNodeId()
                    nodes.append(generateNode(n1, (interpolate(sectionBounds['lat']['min'], sectionBounds['lat']['max'], 0.5), sectionBounds['lon']['min']), {}))
                    nodes.append(generateNode(n2, (interpolate(sectionBounds['lat']['min'], sectionBounds['lat']['max'], 0.5), sectionBounds['lon']['max']), {}))
                    ways.append(generateWay(nextWayId(), [n1, n2], tags))

                    if 'middle' in way:
                        middle = way['middle']
                        tags = middle['tags']
                        nodes.append(generateNode(nextNodeId(), center(sectionBounds), tags))

                elif 'area' in section:
                    area = section['area']
                    tags = area['tags']
                    n1, n2, n3, n4 = nextNodeId(), nextNodeId(), nextNodeId(), nextNodeId()
                    nodes.append(generateNode(n1, (sectionBounds['lat']['min'], sectionBounds['lon']['min']), {}))
                    nodes.append(generateNode(n2, (sectionBounds['lat']['max'], sectionBounds['lon']['min']), {}))
                    nodes.append(generateNode(n3, (sectionBounds['lat']['max'], sectionBounds['lon']['max']), {}))
                    nodes.append(generateNode(n4, (sectionBounds['lat']['min'], sectionBounds['lon']['max']), {}))
                    ways.append(generateWay(nextWayId(), [n1, n2, n3, n4, n1], tags))

                    if 'way' in area:
                        way = area['way']
                        tags = way['tags']
                        n1, n2 = nextNodeId(), nextNodeId()
                        startTags = way['start']['tags'] if 'start' in way else {}
                        endTags = way['end']['tags'] if 'end' in way else {}
                        nodes.append(generateNode(n1, (interpolate(sectionBounds['lat']['min'], sectionBounds['lat']['max'], 0.5), sectionBounds['lon']['min']), startTags))
                        nodes.append(generateNode(n2, (interpolate(sectionBounds['lat']['min'], sectionBounds['lat']['max'], 0.5), sectionBounds['lon']['max']), endTags))
                        ways.append(generateWay(nextWayId(), [n1, n2], tags))

                elif 'multipolygon' in section:
                    multipolygon = section['multipolygon']
                    tags = multipolygon['tags']

                    members = {}

                    if 'inner' in multipolygon:
                        n1, n2, n3, n4 = nextNodeId(), nextNodeId(), nextNodeId(), nextNodeId()
                        nodes.append(generateNode(n1, (sectionBounds['lat']['min'], sectionBounds['lon']['min']), {}))
                        nodes.append(generateNode(n2, (sectionBounds['lat']['max'], sectionBounds['lon']['min']), {}))
                        nodes.append(generateNode(n3, (sectionBounds['lat']['max'], sectionBounds['lon']['max']), {}))
                        nodes.append(generateNode(n4, (sectionBounds['lat']['min'], sectionBounds['lon']['max']), {}))
                        members['inner'] = nextWayId()
                        ways.append(generateWay(members['inner'], [n1, n2, n3, n4, n1], multipolygon['inner']['tags']))

                    if 'outer' in multipolygon:
                        n1, n2, n3, n4 = nextNodeId(), nextNodeId(), nextNodeId(), nextNodeId()
                        nodes.append(generateNode(n1, (sectionBounds['lat']['min'], sectionBounds['lon']['min']), {}))
                        nodes.append(generateNode(n2, (sectionBounds['lat']['max'], sectionBounds['lon']['min']), {}))
                        nodes.append(generateNode(n3, (sectionBounds['lat']['max'], sectionBounds['lon']['max']), {}))
                        nodes.append(generateNode(n4, (sectionBounds['lat']['min'], sectionBounds['lon']['max']), {}))
                        members['outer'] = nextWayId()
                        ways.append(generateWay(members['outer'], [n1, n2, n3, n4, n1], multipolygon['outer']['tags']))

                    relations.append(generateRelation(nextRelationId(), members, tags | {'type': 'multipolygon'}))

    for node in nodes:
        osm.append(node)

    for way in ways:
        osm.append(way)

    for relation in relations:
        osm.append(relation)

    return osm


def main():
    arguments = sys.argv
    if len(arguments) != 1 + 1:
        print('One argument required: YAML file to parse', file=sys.stderr)
        exit(1)

    configPath = arguments[1]
    with open(configPath, 'r') as configFile:
        config = yaml.safe_load(configFile)

    root = generateXml(config)

    print(lxml.etree.tostring(root, encoding='utf-8', xml_declaration=True, pretty_print=True).decode('utf-8'))


if __name__ == "__main__":
    main()
