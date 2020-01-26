FROM ubuntu:18.04

LABEL maintainer="Hidde Wieringa <hidde@hiddewieringa.nl>"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gdal-bin \
    postgresql-client \
    postgis \
  && apt-get autoclean \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /data
RUN mkdir /script

WORKDIR /data

# Database config
ENV PG_HOST postgres-osm
ENV PG_PORT 5432
ENV PG_USER osm
ENV PG_PASSWORD ""
ENV PG_DATABASE gis

COPY ./countries.txt /script/countries.txt
COPY ./download.sh /script/download.sh

CMD ["/script/download.sh"]