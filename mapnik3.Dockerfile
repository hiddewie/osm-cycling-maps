#   Copyright 2015-2019 Jawg Maps
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

FROM debian:stretch-slim

#ENV MAPNIK_VERSION v3.0.22

ENV BUILD_DEPENDENCIES="build-essential \
    ca-certificates \
    git \
    icu-devtools \
    libboost-dev \
    libboost-filesystem-dev \
    libboost-program-options-dev \
    libboost-regex-dev \
    libboost-thread-dev \
    libboost-system-dev \
    libcairo-dev \
    libfreetype6-dev \
    libgdal-dev \
    libharfbuzz-dev \
    libicu-dev \
    libjpeg-dev \
    libpq-dev  \
    libproj-dev \
    librasterlite2-dev \
    libsqlite3-dev \
    libtiff-dev \
    libwebp-dev"

ENV DEPENDENCIES="libboost-filesystem1.62.0 \
    libboost-program-options1.62.0 \
    libboost-regex1.62.0 \
    libboost-thread1.62.0 \
    libboost-system1.62.0 \
    libcairo2 \
    libfreetype6 \
    libgdal20 \
    libharfbuzz-gobject0 \
    libharfbuzz-icu0 \
    libharfbuzz0b \
    libicu57 \
    libjpeg62-turbo \
    libpq5 \
    libproj12 \
    librasterlite2-1 \
    libsqlite3-0 \
    libtiff5 \
    libtiffxx5 \
    libwebp6  \
    libwebpdemux2 \
    libwebpmux2 \
    python"

RUN apt-get update 
RUN apt-get install -y --no-install-recommends $BUILD_DEPENDENCIES
RUN apt-get install -y --no-install-recommends $DEPENDENCIES
RUN git clone https://github.com/mapnik/mapnik.git /mapnik 
WORKDIR /mapnik 
RUN git checkout v3.0.x
RUN git submodule update --init 
RUN python scons/scons.py INPUT_PLUGINS='all' -j4
RUN make JOBS=4 
RUN make install 


RUN git clone https://github.com/mapnik/python-mapnik.git /python-mapnik
WORKDIR /python-mapnik
RUN git checkout v3.0.x
RUN apt install -y python-setuptools python-dev libboost-python-dev libcairo2-dev python-cairo-dev
RUN PYCAIRO=true python setup.py install

RUN  cd / \
    && rm -r mapnik \
    && apt-get autoremove -y --purge $BUILD_DEPENDENCIES \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /usr/local/lib/mapnik /usr/lib/mapnik

