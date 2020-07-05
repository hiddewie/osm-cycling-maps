FROM node:14-buster-slim as build

RUN mkdir -p /build
WORKDIR /build

RUN npm install -g carto
COPY project.mml .
COPY styles.mss .
RUN carto project.mml > mapnik.xml

FROM ubuntu:focal

LABEL maintainer="Hidde Wieringa <hidde@hiddewieringa.nl>"

RUN apt-get update && apt-get install -y \
    python3-mapnik \
    curl \
    fonts-noto-cjk \
    fonts-noto-hinted \
    fonts-noto-unhinted \
    fonts-hanazono \
    ttf-unifont \
  && apt-get autoclean \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /map-it
WORKDIR /map-it

ENV MAPNIK_CONFIGURATION mapnik.xml

COPY --from=build /build/mapnik.xml mapnik.xml
COPY environment.py .
COPY bounds.py .
COPY generate.py .

CMD /usr/bin/python3 generate.py