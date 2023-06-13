#!/usr/bin/env python
import mapnik

import environment

def main():
    mapnikConfiguration = environment.require('MAPNIK_CONFIGURATION')
    print('Using Mapnik configuration file %s' % (mapnikConfiguration,))

if __name__ == '__main__':
    main()
