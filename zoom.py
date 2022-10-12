#!/usr/bin/python3
import glob,generate,os,convertwarps

class ReplaceZoom(generate.Replace):
  def __init__(self):
    self.pattern=f'<FLOAT>CAMERAMULT:'
    self.replacement=f'\t<FLOAT>CAMERAMULT:1.4\n'

REPLACE=[ReplaceZoom()]
 
for path in glob.glob(f'{generate.REFERENCE}/MEDIA/LAYOUTS/**/*.TEMPLATE',recursive=True):
  path=convertwarps.translate(path)
  generate.modify(path,os.path.basename(path),replace=REPLACE,extension='')
