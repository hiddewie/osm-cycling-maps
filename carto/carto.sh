#!/usr/bin/fish

yarn run carto -q project.mml --file ../mapnik_map.xml

sudo docker run -ti \
                            --rm \
                            -v (pwd)/..:/map-it \
                            --link postgres-osm:postgres-osm \
                            -e PG_HOST=postgres-osm \
                            -e PG_PORT=5432 \
                            -e PG_USER="osm" \
                            -e PG_PASSWORD="" \
                            -e PG_DATABASE="gis" \
                            -e MAP_NAME="map" \
                            -e LATITUDES="N52 N51" \
                            -e LONGITUDES="E006 E005" \
                            -e TOP_LEFT_X="644058" \
                            -e TOP_LEFT_Y="6872911" \
                            -e OFFSET_PAGES_X="0" \
                            -e OFFSET_PAGES_Y="0" \
                            -e PAGES_HORIZONTAL="1" \
                            -e PAGES_VERTICAL="1" \
                            hiddewie/map-it

