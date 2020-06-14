FROM mapnik-docker

LABEL maintainer="Hidde Wieringa <hidde@hiddewieringa.nl>"

RUN apt-get update && apt-get install -y \
    curl \
    fonts-noto-cjk \
    fonts-noto-hinted \
    fonts-noto-unhinted \
    fonts-hanazono \
    ttf-unifont \
    libcairo2-dev \
    python-cairo

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
