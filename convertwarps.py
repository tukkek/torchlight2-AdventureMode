#!/usr/bin/python3
import glob,os,generate

LABELS=['Enter','Warp','To','The','Travel','Portal to','Return','Nether','Brood Hive','Slavers','Frosted Hills','Arena of Slaughter','Rotting Crypt','Abandoned Sawmill','Reeking Cellar',"Vyrax's Tower","Locked Vyrax's Tower",'Plunder Cove','Faceless King','Elemental Oasis','3 sisters']

class ReplaceDungeon(generate.Replace):
  def __init__(self):
    self.pattern='<STRING>DUNGEON:'
    self.replacement=f'\t\t\t\t\t\t<STRING>DUNGEON:ESTHERIANCITY\n'#probably unnecessary to be uppercase, but originals were this way

class ReplaceDungeonName(generate.Replace):
  def __init__(self):
    self.pattern='<STRING>DUNGEON NAME:'
    self.replacement=f'\t\t\t\t\t\t<STRING>DUNGEON NAME:EstherianCity\n'
    
class ReplaceLabel(generate.Replace):
  def __init__(self,label):
    self.pattern=f'<STRING>TEXT:{label}'
    self.replacement=f'\t\t\t\t\t\t<STRING>TEXT:Return To Town\n'
    
warpers=set()
dungeons=set()
r=[ReplaceDungeon(),ReplaceDungeonName()]+[ReplaceLabel(l) for l in LABELS]

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
    generate.modify(w,os.path.basename(w),replace=r,extension='')
