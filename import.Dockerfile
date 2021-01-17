FROM debian:buster-slim as compilation

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    libgdal-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /compilation
WORKDIR /compilation

COPY scripts/isolation.c .
RUN gcc -Wall -o isolation -lgdal -lm -O2 isolation.c

FROM debian:buster-slim

LABEL maintainer="Hidde Wieringa <hidde@hiddewieringa.nl>"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gdal-bin \
    osm2pgsql \
    postgresql-client \
    postgis \
    python-gdal \
    osmium-tool && \
    wget http://katze.tfiu.de/projects/phyghtmap/phyghtmap_2.21-1_all.deb && \
    dpkg -i phyghtmap_2.21-1_all.deb; \
    apt-get -f -y install && \
    rm phyghtmap_2.21-1_all.deb && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /data
RUN mkdir /style
RUN mkdir /script

WORKDIR /data

COPY --from=compilation /compilation/isolation /script
COPY style/map-it.style /script/map-it.style
COPY scripts/download.sh /script/download.sh
COPY style/shade /style/shade
RUN chmod +x /script/download.sh

CMD /script/download.sh
