#!/usr/bin/bash
set -e

echo Clearing GUTS data
nice rm -rf 'guts/Adventure mode/media/dungeons/'
nice rm -rf 'guts/Adventure mode/media/units/items/maps/'
nice rm -rf 'guts/Adventure mode/media/spawnclasses/'

echo Copy dungeons
nice gcp -r 'media/dungeons/' 'guts/Adventure mode/media/dungeons/'

echo Copy maps
nice gcp -r 'media/units/items/maps/' 'guts/Adventure mode/media/units/items/maps/'

echo Copy spawnclasses
nice gcp -r 'static/media/spawnclasses/' 'guts/Adventure mode/media/spawnclasses/'
