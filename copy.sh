#!/usr/bin/bash
set -e

echo For development and testing only!

echo Clearing GUTS data...
nice rm -rf 'guts/Adventure mode/media/dungeons/'
nice rm -rf 'guts/Adventure mode/media/units/items/maps/'
nice rm -rf 'guts/Adventure mode/media/spawnclasses/'

echo Copy dungeons...
nice gcp -r 'media/dungeons/' 'guts/Adventure mode/media/'

echo Copy maps...
nice gcp -r 'media/units/' 'guts/Adventure mode/media/'

echo Copy spawnclasses...
nice gcp -r 'static/media/spawnclasses/' 'guts/Adventure mode/media/'

echo Setting permissions...
nice chmod -R 0777 'guts/Adventure mode/media/'
