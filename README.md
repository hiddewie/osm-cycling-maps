
## Generating a custom cycling map with Mapnik

View blogpost at https://dev.to/hiddewie/creating-a-custom-cycling-map-3g2a.

## Getting started

### Manually

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

### Using Docker

Start a database with GIS extensions enabled using the image `openfirmware/postgres-osm`
```bash
docker run -d --name postgres-osm openfirmware/postgres-osm
```

Then, download and import the data of the map using the docker image `import.Dockerfile`. First build it using
```bash
docker build -t map-it-import -f import.Dockerfile .
``` 

Map the data directory of this project to the container. Some files are downloaded there that are used for shading the map. Run it using
```bash
docker run -ti --rm -v $PROJECT_DIR/data:/data --link postgres-osm:postgres-osm map-it-import
```
where `$PROJECT_DIR` is the project directory

Let's generate a map. Build the image using
```bash
docker build -t map-it .
```
and then run it using 
```bash
docker run -ti --rm -v $PROJECT_DIR:/map-it --link postgres-osm:db -e PG_HOST=db -e PG_USER=osm -e PG_DATABASE=gis map-it
```

The map will be written to the mapped volume in the `/output` directory. The mapnik XML config will also be written there.

### Examples

[Example PDF Output](https://github.com/hiddewie/map-it/releases/download/v1.0.0/output.pdf)

![Expected output](assets/cover.jpg)

