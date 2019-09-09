
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

You may edit the constants in the download and generate scripts to generate maps for other countries.

[Example PDF Output](https://github.com/hiddewie/map-it/releases/download/v1.0.0/output.pdf)

![Expected output](assets/cover.jpg)

