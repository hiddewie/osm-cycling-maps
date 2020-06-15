# Taken from https://github.com/akx/docker-mapnik/blob/master/Dockerfile

FROM ubuntu:20.04

LABEL maintainer="Hidde Wieringa <hidde@hiddewieringa.nl>"

RUN apt update && apt install -y \
  --no-install-recommends \
  git \
  ca-certificates

RUN git clone https://github.com/mapnik/mapnik.git /mapnik
WORKDIR /mapnik
RUN git checkout v3.0.x
RUN git submodule update --init

RUN apt install -y --no-install-recommends python
RUN apt install -y --no-install-recommends build-essential

ARG DEBIAN_FRONTEND=noninteractive

RUN apt install -y --no-install-recommends libharfbuzz-dev
RUN apt install -y --no-install-recommends libicu-dev
RUN apt install -y --no-install-recommends libcairo-dev
RUN apt install -y --no-install-recommends libgdal-dev
RUN apt install -y --no-install-recommends libboost-dev libboost-filesystem-dev libboost-program-options-dev libboost-python-dev libboost-regex-dev libboost-system-dev libboost-thread-dev
RUN apt install -y --no-install-recommends libtiff5-dev libfreetype6-dev libxml2-dev libproj-dev libsqlite3-dev libgdal-dev libcairo-dev python-cairo-dev
RUN apt install -y --no-install-recommends clang

RUN clang --version

ENV CCACHE_TEMPDIR=/tmp/.ccache-temp
ENV CCACHE_COMPRESS=1
ENV CCACHE_DIR=/ccache

RUN export CXX="ccache clang++-10 -Qunused-arguments"
RUN export CC="clang-10"
RUN export ENABLE_GLIBC_WORKAROUND=true

RUN g++ --version
RUN clang++-10 --version
RUN clang++ --version

#RUN ./configure CXX="ccache clang++ -Qunused-arguments" CC="clang" ENABLE_GLIBC_WORKAROUND=true
RUN python scons/scons.py configure CXX="clang++-10 -Qunused-arguments" CC="clang++-10" ENABLE_GLIBC_WORKAROUND=true
RUN JOBS=4 make
RUN make install

#
## Prerequisites and runtimes
## COPY setup-node.sh /tmp/setup-node.sh
## RUN bash /tmp/setup-node.sh && rm /tmp/setup-node.sh
#RUN apt update && apt upgrade -y && apt install -y --no-install-recommends \
#    build-essential sudo software-properties-common curl \
#    libboost-dev libboost-filesystem-dev libboost-program-options-dev libboost-python-dev libboost-regex-dev libboost-system-dev libboost-thread-dev libicu-dev libtiff5-dev libfreetype6-dev libpng12-dev libxml2-dev libproj-dev libsqlite3-dev libgdal-dev libcairo-dev python-cairo-dev postgresql-contrib libharfbuzz-dev \
#    python3-dev python-dev git python-pip python-setuptools python-wheel python3-setuptools python3-pip python3-wheel
#
## nodejs
#
## Mapnik
#ENV MAPNIK_VERSION 3.0.10
#RUN curl -s https://mapnik.s3.amazonaws.com/dist/v${MAPNIK_VERSION}/mapnik-v${MAPNIK_VERSION}.tar.bz2 | tar -xj -C /tmp/
#RUN cd /tmp/mapnik-v${MAPNIK_VERSION} && python scons/scons.py configure
#RUN cd /tmp/mapnik-v${MAPNIK_VERSION} && make JOBS=1 && make install JOBS=1
#
## # Node Bindings
## ENV NODE_MAPNIK_VERSION 3.5.13
## RUN mkdir -p /opt/node-mapnik && curl -L https://github.com/mapnik/node-mapnik/archive/v${NODE_MAPNIK_VERSION}.tar.gz | tar xz -C /opt/node-mapnik --strip-components=1
## RUN cd /opt/node-mapnik && npm install --unsafe-perm=true --build-from-source && npm link
#
## Python Bindings
#ENV PYTHON_MAPNIK_COMMIT 3a60211dee366060acf4e5e0de8b621b5924f2e6
#RUN mkdir -p /opt/python-mapnik && curl -L https://github.com/mapnik/python-mapnik/archive/${PYTHON_MAPNIK_COMMIT}.tar.gz | tar xz -C /opt/python-mapnik --strip-components=1
#RUN cd /opt/python-mapnik && python2 setup.py install && python3 setup.py install && rm -r /opt/python-mapnik/build
#
## Tests
#RUN apt-get install -y unzip
#RUN mkdir -p /opt/demos
#COPY world.py /opt/demos/world.py
#COPY 110m-admin-0-countries.zip /opt/demos/110m-admin-0-countries.zip
#RUN cd /opt/demos && unzip 110m-admin-0-countries.zip && rm 110m-admin-0-countries.zip
## COPY world.js /opt/demos/world.js
#COPY stylesheet.xml /opt/demos/stylesheet.xml
#
#WORKDIR /opt/demos
#RUN python2 world.py
