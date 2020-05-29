FROM ubuntu:18.04

LABEL maintainer="Hidde Wieringa <hidde@hiddewieringa.nl>"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gdal-bin \
    postgresql-client \
    postgis \
    python-gdal \
  && apt-get autoclean \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /data
RUN mkdir /script

WORKDIR /data

COPY ./countries.txt /script/countries.txt
COPY ./download.sh /script/download.sh

RUN chmod +x /script/download.sh

CMD ["/script/download.sh"]