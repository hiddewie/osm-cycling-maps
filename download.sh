#!/usr/bin/env bash

DATA_DIR=/data
COUNTRIES_LOCATION="/script/countries.txt"

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

echo "Merge height data for combination into one height file for files $FILES"
gdal_merge.py -o $DATA_DIR/combined.raw.hgt $FILES
COMBINED_SIZE=$(gdalinfo combined.raw.hgt | grep -oP 'Size is \K\d+')
rm -f combined.hgt || exit 1
gdalwarp -ts $((4 * $COMBINED_SIZE)) 0 -r cubic -co "TFW=YES" $DATA_DIR/combined.raw.hgt $DATA_DIR/combined.hgt

echo "Contours"
rm -f $DATA_DIR/combined.shp || exit 1
gdal_contour -i 20 -snodata -32768 -a height $DATA_DIR/combined.hgt $DATA_DIR/combined.shp || exit 1

ARGS="-I -d"
echo "Import contours"
shp2pgsql $ARGS -s 4326 $DATA_DIR/combined.shp contours | psql $POSTGRES_ARGS | grep -v 'INSERT' || exit 1

echo "Shade"
rm -f $DATA_DIR/combined.tif || exit 1
gdaldem hillshade -s 111120 -compute_edges $DATA_DIR/combined.hgt $DATA_DIR/combined.raw.tif || exit 1
gdaldem color-relief combined.raw.tif -alpha $DATA_DIR/shade.ramp $DATA_DIR/combined.tif || exit 1
rm -f $DATA_DIR/combined.{dbf,hgt.aux.xml,prj,shp,shx,raw.tif,tfw} || exit 1

echo "Done"

sleep 1

echo
echo " -- Country borders -- "
echo

echo "Get all country borders"
wget  "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries.zip" \
  -O $DATA_DIR/countries.zip || exit 1
mkdir $DATA_DIR/countries
unzip $DATA_DIR/countries.zip -d $DATA_DIR/countries

shp2pgsql -I -d -s 4326 $DATA_DIR/countries/ne_10m_admin_0_countries country_border | psql $POSTGRES_ARGS | grep -v 'INSERT'

rm -r $DATA_DIR/countries || exit 1

echo "Done"

sleep 1

echo
echo " -- Map content -- "
echo

ARGS="-I -d"
for COUNTRY in $FEATURE_COUNTRIES
do
  mkdir -p $DATA_DIR/$COUNTRY

  echo "Get $COUNTRY"
  wget http://download.geofabrik.de/$COUNTRY-latest-free.shp.zip -O $DATA_DIR/$COUNTRY.hgt.zip || exit 1

  echo "Unzip $COUNTRY"
  unzip -o $DATA_DIR/$COUNTRY.hgt.zip -d $DATA_DIR/$COUNTRY || exit 1
  rm $DATA_DIR/$COUNTRY.hgt.zip || exit 1

  echo "Import data $COUNTRY"
  shp2pgsql $ARGS -s 4326 $DATA_DIR/$COUNTRY/gis_osm_water_a_free_1.shp water_a | psql $POSTGRES_ARGS | grep -v 'INSERT' || exit 1
  shp2pgsql $ARGS -s 4326 $DATA_DIR/$COUNTRY/gis_osm_landuse_a_free_1.shp landuse_a | psql $POSTGRES_ARGS  | grep -v 'INSERT' || exit 1
  shp2pgsql $ARGS -s 4326 $DATA_DIR/$COUNTRY/gis_osm_waterways_free_1.shp waterways | psql $POSTGRES_ARGS | grep -v 'INSERT' || exit 1
  shp2pgsql $ARGS -s 4326 $DATA_DIR/$COUNTRY/gis_osm_natural_free_1.shp natural | psql $POSTGRES_ARGS | grep -v 'INSERT' || exit 1
  shp2pgsql $ARGS -s 4326 $DATA_DIR/$COUNTRY/gis_osm_railways_free_1.shp railways | psql $POSTGRES_ARGS | grep -v 'INSERT' || exit 1
  shp2pgsql $ARGS -s 4326 $DATA_DIR/$COUNTRY/gis_osm_roads_free_1.shp roads | psql $POSTGRES_ARGS | grep -v 'INSERT' || exit 1
  shp2pgsql $ARGS -s 4326 $DATA_DIR/$COUNTRY/gis_osm_places_free_1.shp places | psql $POSTGRES_ARGS | grep -v 'INSERT' || exit 1
  shp2pgsql $ARGS -s 4326 $DATA_DIR/$COUNTRY/gis_osm_transport_free_1.shp transport | psql $POSTGRES_ARGS | grep -v 'INSERT' || exit 1
  shp2pgsql $ARGS -s 4326 $DATA_DIR/$COUNTRY/gis_osm_pois_free_1.shp poi | psql $POSTGRES_ARGS | grep -v 'INSERT' || exit 1
  shp2pgsql $ARGS -s 4326 $DATA_DIR/$COUNTRY/gis_osm_pois_a_free_1.shp poi_a | psql $POSTGRES_ARGS | grep -v 'INSERT' || exit 1
  shp2pgsql $ARGS -s 4326 $DATA_DIR/$COUNTRY/gis_osm_pofw_free_1.shp pofw | psql $POSTGRES_ARGS | grep -v 'INSERT' || exit 1
  shp2pgsql $ARGS -s 4326 $DATA_DIR/$COUNTRY/gis_osm_natural_free_1.shp natural_a | psql $POSTGRES_ARGS | grep -v 'INSERT' || exit 1

  echo "Delete shape data $COUNTRY"
  rm -r $DATA_DIR/$COUNTRY || exit 1

  echo "Done $COUNTRY"

  ARGS="-a"
done

echo "Done"
