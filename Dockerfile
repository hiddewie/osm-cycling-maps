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
    curl
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs \
  && apt-get autoclean \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /map-it
WORKDIR /map-it

ENV MAPNIK_CONFIGURATION mapnik.xml
RUN npm install -g carto

COPY project.mml .
COPY styles.mss .
RUN carto project.mml > $MAPNIK_CONFIGURATION

COPY generate.py .

CMD /usr/bin/python generate.py