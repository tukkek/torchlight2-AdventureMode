#!/bin/bash 
#TODO would be great to make this cross-platform but since generate.py depends on dos2unix right now, this is more elegantly done in BASh:
rm -rf media/
mkdir -p media/dungeons
mkdir -p media/units/items/maps
cp -r static/media/* media/
./generate.py
