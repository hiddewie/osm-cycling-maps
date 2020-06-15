FROM debian:buster-slim

LABEL maintainer="Hidde Wieringa <hidde@hiddewieringa.nl>"

RUN apt-get update && apt-get install -y \
    python-mapnik

COPY environment.py .
COPY bounds.py .

CMD /usr/bin/python bounds.py