#!/bin/bash 
set -e

#TODO would be great to make this cross-platform but since generate.py depends on dos2unix right now, this is more elegantly done in BASh:
rm -rf media/
cp -r static/media media/
find media/ui/icons/|grep -e .xcf -e .md|xargs rm
echo "Converting warps..."
nice python3 convertwarps.py
echo "Generating maps..."
PYTHONHASHSEED=0 nice python3 generate.py --reference install/
echo "Altering zoom..."
nice python3 zoom.py
echo "Scaling vanilla areas..."
nice python3 scale.py
