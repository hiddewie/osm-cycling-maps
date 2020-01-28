FROM debian:jessie-slim

LABEL maintainer="Hidde Wieringa <hidde@hiddewieringa.nl>"

RUN apt-get update && apt-get install -y \
    libmapnik-dev \
    libmapnik2-dev \
    libmapnik2.2 \
    mapnik-doc \
    mapnik-utils \
    python-mapnik \
    python-mapnik2 \
  && apt-get autoclean \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /map-it
WORKDIR /map-it

CMD ["/usr/bin/python", "./generate.py"]