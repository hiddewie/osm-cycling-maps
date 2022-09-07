#!/usr/bin/env bash

set -eo pipefail

# Replace credentials in Mapnik configuration
sed -i -E "s/@@PG_HOST@@/$PG_HOST/g" mapnik.xml
sed -i -E "s/@@PG_PORT@@/$PG_PORT/g" mapnik.xml
sed -i -E "s/@@PG_DATABASE@@/$PG_DATABASE/g" mapnik.xml
sed -i -E "s/@@PG_USER@@/$PG_USER/g" mapnik.xml
sed -i -E "s/@@PG_PASSWORD@@/$PG_PASSWORD/g" mapnik.xml

exec /usr/bin/python3 generate.py