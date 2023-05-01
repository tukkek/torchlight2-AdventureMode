#!/usr/bin/bash
set -e

echo For development and testing only!

echo Clearing GUTS data...
nice rm -rf 'guts/Adventure mode/media/dungeons/'
nice rm -rf 'guts/Adventure mode/media/units/'
nice rm -rf 'guts/Adventure mode/media/spawnclasses/'

echo Copy dungeons...
nice gcp -r 'media/dungeons/' 'guts/Adventure mode/media/'

echo Copy maps...
nice gcp -r 'media/units/' 'guts/Adventure mode/media/'

echo Copy props...
nice gcp -r 'static/media/units/props' 'guts/Adventure mode/media/units/'

echo Copy spawnclasses...
nice gcp -r 'static/media/spawnclasses/' 'guts/Adventure mode/media/'

echo Setting permissions...
nice chmod -R 0777 'guts/Adventure mode/media/'
