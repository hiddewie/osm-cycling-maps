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
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /data
RUN mkdir /script

WORKDIR /data

COPY ./download.sh /script/download.sh
RUN chmod +x /script/download.sh

CMD /script/download.sh
