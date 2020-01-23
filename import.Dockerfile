FROM ubuntu:18.04

LABEL maintainer="Hidde Wieringa <hidde@hiddewieringa.nl>"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    # aufs-tools \
    # automake \
    # build-essential \
    # python-mapnik \
    # python-cairo \
    wget \
    unzip \
    gdal-bin \
    postgresql-client \
    postgis \
    # mapnik \
    # libmapnik-dev \
    # all\
    # your\
    # other\
    # packages \
    # python \
  && apt-get autoclean \
  && rm -rf /var/lib/apt/lists/*

# RUN mapnik-config -v

RUN mkdir /data
RUN mkdir /script

WORKDIR /data

# PG_HOST=postgres-osm
# PG_HOST=a400e660c424e71c9ef9ddda5cdea0212cb81282409dcef69b93079b3cd37db3
# PG_PORT=5432
# PG_USER=osm
# PG_PASSWORD=""
# PG_DATABASE=gis


# Database config
ENV PG_HOST postgres-osm
# COPY ./countries.txt ./coutries.txt
ENV PG_PORT 5432
ENV PG_USER osm
ENV PG_PASSWORD ""
ENV PG_DATABASE gis

COPY ./countries.txt /script/countries.txt
COPY ./download.sh /script/download.sh

CMD ["/script/download.sh"]