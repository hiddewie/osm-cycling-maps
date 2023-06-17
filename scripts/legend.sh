#!/usr/bin/env bash

export PG_DATABASE=$PG_LEGEND_DATABASE
echo "Set legend database $PG_DATABASE"

export BBOX=0.0:0.0:0.3:0.2
echo "Set bounding box to $BBOX"

export PAPER_SIZE=A4
export PAPER_ORIENTATION=landscape
export SCALE=1:125000
echo "Set paper settings to $PAPER_SIZE $PAPER_ORIENTATION with scale $SCALE"

export MAP_NAME=legend
echo "Using map name $MAP_NAME"

echo "Generating legend..."
exec with_mapnik_environment.sh generate.py
