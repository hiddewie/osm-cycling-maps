
## Generating a custom cycling map with Mapnik

View blogpost at ...

### Getting started

Make sure you have a running Postgres database, with a `gis` schema with GIS extensions enabled.

Run the command 
```shell script
./download.sh
```
to download the data and insert it into the database.

Run the command 
```shell script
./slovakia.py
```
to generate the Mapnik XML configuration and the printable PDF map in the folder `output`.

![Expected output](slovakia/assets/cover.jpg)