FROM debian:11-slim as generation

ENV DEBIAN_FRONTEND noninteractive

RUN mkdir -p /generation
WORKDIR /generation

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-lxml \
    && rm -rf /var/lib/apt/lists/*

COPY scripts/placements.py .
RUN /usr/bin/python3 placements.py > placements.xml

COPY scripts/generate/shields.py .
RUN /usr/bin/python3 shields.py

FROM node:14-buster-slim as build

RUN mkdir -p /build
WORKDIR /build

RUN npm install -g carto

COPY --from=generation /generation/placements.xml placements.xml
COPY carto/map-it/project.mml .
COPY carto/map-it/styles.mss .

# Generate Mapnik XML using Carto
RUN carto project.mml > mapnik.xml

# The CDATA tags are stripped of symbolizers where <Placement/> tags are inserted from placements.xml
# Also see https://github.com/mapbox/carto/issues/238#issuecomment-19673987
RUN sed -i -E "s@<!\[CDATA\[(.*)--PLACEMENTS--]]>@\1$(cat placements.xml)@g" mapnik.xml

FROM debian:11-slim

ENV DEBIAN_FRONTEND noninteractive

LABEL maintainer="Hidde Wieringa <hidde@hiddewieringa.nl>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-mapnik \
    python3-pypdf2 \
    curl \
    fonts-noto-cjk \
    fonts-noto-hinted \
    fonts-noto-unhinted \
    fonts-hanazono \
    fonts-unifont \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /map-it
WORKDIR /map-it

ENV MAPNIK_CONFIGURATION mapnik.xml

RUN mkdir style
COPY --from=generation /generation/symbols/shields style/symbols/shields
COPY --from=build /build/mapnik.xml mapnik.xml
COPY scripts/environment.py .
COPY scripts/bounds.py .
COPY scripts/generate.py .
COPY scripts/generate.sh .
COPY scripts/tiles.py .
COPY style style

CMD ["bash", "generate.sh"]