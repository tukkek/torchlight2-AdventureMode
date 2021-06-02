# Map icon workflow

1. Edit `maps.xcf` with [GIMP](https://www.gimp.org/).
2. When ready to export, Save File then Flatten Image (Image menu) and export as `maps.png` and `maps.dds` (DXT1 compression).
3. Close without saving (or Undo History, Edit menu) to keep a copy of the layered source file. 

# To-do

1. Expand for Bosses using `map_dragon` as base.
2. Expand for non-Map Dungeons using `map_cave` as base.
3. Expand for Outdoors using `map_icecave` as base (probably)?

When creating new map icon sets, the best idea is probably to create a new folder and new set of files. The 4x4 grid works well enough for all tiers and GUTS seems to be really touchy about the image resolutions, regardless of the detailed coordinates on the `.imageset` mapping.
