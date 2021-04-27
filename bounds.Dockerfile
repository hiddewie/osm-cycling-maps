FROM ubuntu:21.04

LABEL maintainer="Hidde Wieringa <hidde@hiddewieringa.nl>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-mapnik \
    && rm -rf /var/lib/apt/lists/*

COPY scripts/environment.py .
COPY scripts/bounds.py .

CMD /usr/bin/python3 bounds.py