
## Generating a custom cycling map with Mapnik

View blogpost at https://dev.to/hiddewie/creating-a-custom-cycling-map-ida-temp-slug-3451121.

### Getting started

Make sure you have a running Postgres database, with a `gis` schema with GIS extensions enabled.

Run the command 
```shell script
./download.sh
```
to download the data and insert it into the database.

Run the command 
```shell script
./generate.py
```
to generate the Mapnik XML configuration and the printable PDF map in the folder `output`.

![Expected output](assets/cover.jpg)