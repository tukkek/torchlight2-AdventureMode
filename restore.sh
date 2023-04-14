#!/usr/bin/bash
set -e

nice git restore media/dungeons/*.dat media/dungeons/*.DAT media/units/items/maps/*.dat
nice git status
