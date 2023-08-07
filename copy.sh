#!/usr/bin/bash
#TODO turn into makefile?
set -e

echo For development and testing only!

echo Copy dungeons...
nice rm -rf 'guts/Adventure mode/media/dungeons/'
nice gcp -r 'media/dungeons/' 'guts/Adventure mode/media/'
nice chmod -R 0777 'guts/Adventure mode/media/dungeons/'

echo Copy units...
nice rm -rf 'guts/Adventure mode/media/units/'
nice gcp -r 'media/units/' 'guts/Adventure mode/media/'
nice chmod -R 0777 'guts/Adventure mode/media/units/'

echo Copy spawnclasses...
nice rm -rf 'guts/Adventure mode/media/spawnclasses/'
nice gcp -r 'static/media/spawnclasses/' 'guts/Adventure mode/media/'
nice chmod -R 0777 'guts/Adventure mode/media/spawnclasses/'
