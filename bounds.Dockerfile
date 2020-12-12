FROM debian:buster-slim

LABEL maintainer="Hidde Wieringa <hidde@hiddewieringa.nl>"

RUN apt-get update && apt-get install -y \
    python-mapnik

COPY scripts/environment.py .
COPY scripts/bounds.py .

CMD /usr/bin/python bounds.py