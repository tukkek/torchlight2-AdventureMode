# Map icon workflow

1. Edit `.xcf` with [GIMP](https://www.gimp.org/).
2. To export, Save File then Merge Visible Layers (Image menu), crop to image and export as `.png` and `.dds` (DXT1 compression).
3. Close without saving (or Undo History, Edit menu) to keep a copy of the layered source file. 

When creating new map icon sets, the best idea is probably to create a new folder and new set of files. The 4x4 grid works well enough for all tiers and GUTS seems to be really touchy about the image resolutions, regardless of the detailed coordinates on the `.imageset` mapping.
