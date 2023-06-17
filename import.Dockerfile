FROM debian:11-slim as compilation

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgdal-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /compilation
WORKDIR /compilation

COPY scripts/isolation.c .
RUN gcc isolation.c -Wall -o isolation -lgdal -lm -O2

FROM debian:11-slim

LABEL maintainer="Hidde Wieringa <hidde@hiddewieringa.nl>"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    wget \
    unzip \
    gdal-bin \
    osm2pgsql \
    postgresql-client \
    postgis \
    python3-gdal \
    libboost-all-dev \
    libgdal-dev \
    osmium-tool && \
    wget http://katze.tfiu.de/projects/phyghtmap/phyghtmap_2.23-1_all.deb && \
    dpkg -i phyghtmap_2.23-1_all.deb; \
    apt-get -f -y install && \
    rm phyghtmap_2.23-1_all.deb && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /data
RUN mkdir -p /style
RUN mkdir -p /script
ENV PATH $PATH:/script

WORKDIR /data

COPY --from=compilation /compilation/isolation /script
COPY style/map-it.style /script/map-it.style
COPY scripts/download.sh /script/download.sh
COPY style/shade /style/shade
COPY legend/legend.osm /legend/legend.osm
RUN chmod +x /script/download.sh

CMD ["download.sh"]
