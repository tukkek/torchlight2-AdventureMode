#!/usr/bin/bash
set -e

echo Clearing GUTS data
rm -rf 'guts/Adventure mode/media/dungeons/'
rm -rf 'guts/Adventure mode/media/units/items/maps/'
rm -rf 'guts/Adventure mode/media/spawnclasses/'

echo Copy dungeons
gcp -r 'media/dungeons/' 'guts/Adventure mode/media/dungeons/'

echo Copy maps
gcp -r 'media/units/items/maps/' 'guts/Adventure mode/media/units/items/maps/'

echo Copy spawnclasses
gcp -r 'static/media/spawnclasses/' 'guts/Adventure mode/media/spawnclasses/'
