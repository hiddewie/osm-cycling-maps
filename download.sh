#!/usr/bin/env bash

DATA_DIR=/data

python -V
gdalinfo --version
osm2pgsql --version
psql --version
osmium --version

echo "Using latitudes '$LATITUDES'"
echo "Using longitudes '$LONGITUDES'"
echo "Using feature countries '$FEATURE_COUNTRIES'"
echo 

PGPASSWORD="$PG_PASSWORD"
POSTGRES_ARGS="-h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DATABASE""

mkdir -p $DATA_DIR

echo
echo " -- Height, contours & shade -- "
echo

FILES=""
for LAT in $LATITUDES
do
  for LON in $LONGITUDES
  do
    NAME="${LAT}${LON}"

    echo "Get $NAME"
    wget https://dds.cr.usgs.gov/srtm/version2_1/SRTM3/Eurasia/$NAME.hgt.zip -O $DATA_DIR/$NAME.hgt.zip || exit 1

    echo "Unzip $NAME"
    unzip -o $DATA_DIR/$NAME.hgt.zip -d $DATA_DIR || exit 1
    rm $DATA_DIR/$NAME.hgt.zip || exit 1

    FILES="$FILES $DATA_DIR/$NAME.hgt"

    echo "Done $NAME"
  done
done

echo "Merge height data for combination into one height file for files$FILES"
gdal_merge.py -o $DATA_DIR/combined.raw.hgt -of GTiff $FILES
COMBINED_SIZE=$(gdalinfo combined.raw.hgt | grep -oP 'Size is \K\d+')
rm -f combined.hgt || exit 1
gdalwarp -ts $((4 * $COMBINED_SIZE)) 0 -r cubic -co "TFW=YES" $DATA_DIR/combined.raw.hgt  -of GTiff $DATA_DIR/combined.hgt

echo "Contours"
rm -f $DATA_DIR/combined.shp || exit 1
gdal_contour -i 20 -snodata -32768 -a height $DATA_DIR/combined.hgt $DATA_DIR/combined.shp || exit 1

ARGS="-I -d"
echo "Import contours"
shp2pgsql $ARGS -g way -s 4326 $DATA_DIR/combined.shp contours | psql $POSTGRES_ARGS | grep -v 'INSERT' || exit 1

echo "Shade"
rm -f $DATA_DIR/combined.tif || exit 1
gdaldem hillshade -s 111120 -compute_edges $DATA_DIR/combined.hgt $DATA_DIR/combined.raw.tif || exit 1
gdaldem color-relief combined.raw.tif -alpha $DATA_DIR/shade.ramp $DATA_DIR/combined.tif || exit 1
rm -f $DATA_DIR/combined.{dbf,hgt.aux.xml,prj,shp,shx,raw.tif,tfw} || exit 1

echo "Done"

sleep 1

echo
echo " -- Map content -- "
echo

FILES=""
for COUNTRY in $FEATURE_COUNTRIES
do
  echo "Downloading $COUNTRY from http://download.geofabrik.de/$COUNTRY-latest.osm.pbf"
  FILE=$DATA_DIR/$COUNTRY.osm.pbf
  mkdir -p -- "${FILE%/*}"
  wget http://download.geofabrik.de/$COUNTRY-latest.osm.pbf -O $DATA_DIR/$COUNTRY.osm.pbf || exit 1
  FILES="$FILES $DATA_DIR/$COUNTRY.osm.pbf"

  echo "Done $COUNTRY"
done

echo "Merging OSM data"

echo "Merging files $FILES to $DATA_DIR/combined.osm.pbf"
osmium merge --output=$DATA_DIR/combined.osm.pbf --overwrite $FILES

echo "Done combining OSM data"

echo "Importing combined OSM data"

# The following values can be tweaked
# See https://github.com/gravitystorm/openstreetmap-carto/blob/master/scripts/docker-startup.sh
# TODO: specify --style? (see openstreetmap-carto.style)
# TODO: specify --tag-transform-script? (see openstreetmap-carto.lua)
# TODO: specify --multi-geometry?
OSM2PGSQL_CACHE=512
OSM2PGSQL_NUMPROC=1
PGPASS=$PG_PASSWORD

echo "Using OSM2PGSQL_CACHE = $OSM2PGSQL_CACHE"
echo "Using $OSM2PGSQL_NUMPROC processes"

echo "Starting import from $DATA_DIR/combined.osm.pbf"

osm2pgsql \
  --cache $OSM2PGSQL_CACHE \
  --number-processes $OSM2PGSQL_NUMPROC \
  --hstore \
  --multi-geometry \
  --host $PG_HOST \
  --database $PG_DATABASE \
  --username $PG_USER \
  --unlogged \
  --slim \
  --drop \
  $DATA_DIR/combined.osm.pbf

echo "Done importing OSM data"

echo "Done"
