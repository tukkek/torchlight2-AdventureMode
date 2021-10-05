#!/usr/bin/python3
import glob,os,generate

class ReplaceWarp(generate.Replace):
  def __init__(self):
    self.pattern='<STRING>DUNGEON NAME:'
    self.replacement=f'\t\t\t\t\t\t<STRING>DUNGEON NAME:EstherianCity\n'

warpers=set()
dungeons=set()

def scan(query):
  for path in glob.glob(query,recursive=True):
    try:
      with open(path,encoding='utf-16') as f:
        for l in f.readlines():
          l=l.lower()
          if 'warper' in l:
            warpers.add(path)
          if '<string>dungeon name:' in l:
            dungeons.add(path)
    except:
      continue
    
scan(f'{generate.REFERENCE}/MEDIA/LAYOUTS/**/*.LAYOUT')
scan(f'{generate.REFERENCE}/MEDIA/LEVELSETS/PROPS/**/*.LAYOUT')
for w in sorted(warpers):
  if w in dungeons:
    w='./'+w.replace(generate.REFERENCE,'')
    generate.modify(w,os.path.basename(w),replace=[ReplaceWarp()],extension='')
