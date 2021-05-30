#!/usr/bin/python3
import sys,os,shutil,dataclasses

ENCODING='utf-16'
DIRMEDIA='media'
DIRDUNGEONS='media/dungeons'
DIRMAPS='media/units/items/maps'
REFERENCE='/media/sda2/windows/steam/steamapps/common/Torchlight II/'#TODO make argument
OPENPORTAL='''	[EFFECT]
		<STRING>ACTIVATION:DYNAMIC
		<STRING>DURATION:INSTANT
		<STRING>TYPE:OPEN PORTAL
		<BOOL>SAVE:TRUE
		<FLOAT>MIN:0
		<FLOAT>MAX:0
	[/EFFECT]
'''

@dataclasses.dataclass
class Dungeon:
  name:str
  dungeon:str
  item:str
  
  def topath(self,path,filename):
    return f'{path}/{filename}.dat'
  
  def __post_init__(self):
    self.dungeon=self.topath(DIRDUNGEONS,self.dungeon)
    self.item=self.topath(DIRMAPS,self.item)
    
@dataclasses.dataclass
class Replace:
  pattern:str
  replacement:str
  
class ReplaceDescription(Replace):
  def __init__(self,dungeon,tier):
    self.pattern='<TRANSLATE>DESCRIPTION:'
    self.replacement=f'\t<TRANSLATE>DESCRIPTION:Right-click to enter the {dungeon.name} ({tier.name})\n'

class ReplaceMinLevel(Replace):
  def __init__(self):
    self.pattern='<INTEGER>MINLEVEL'
    self.replacement=f'\t<INTEGER>MINLEVEL:1\n'

class ReplaceMaxLevel(Replace):
  def __init__(self):
    self.pattern='<INTEGER>MAXLEVEL'
    self.replacement=f'\t<INTEGER>MAXLEVEL:110\n'
    
class ReplaceName(Replace):
  def __init__(self,dungeon,tier):
    self.pattern='<TRANSLATE>DISPLAYNAME:'
    self.replacement=f'\t<TRANSLATE>DISPLAYNAME:{dungeon.name} map ({tier.name})\n'
    
@dataclasses.dataclass
class Tier:
  name:str
  offset:int

dungeons=[Dungeon('Infernal Necropolis','map_catacombs_a_105','catacombsmapa105')]
replacements=[ReplaceMinLevel(),ReplaceMaxLevel()]
tiers=[Tier('hard',0)]#TODO

def modify(path,replace=[],add=[]):
  modified=[]
  with open(REFERENCE+path.upper(),encoding=ENCODING) as f:
    for line in f:
      for r in replace:
        if r.pattern in line:
          modified.append(r.replacement)
          break
      else:
        modified.append(line)
  for a in add:
    modified.insert(len(modified)-1,a)
  modified=''.join(modified)
  print(modified,file=open(path,'w',encoding=ENCODING))

def setup():
  if os.path.exists(DIRMEDIA):
    shutil.rmtree(DIRMEDIA)
  os.makedirs(DIRDUNGEONS)
  os.makedirs(DIRMAPS)

setup()

for d in dungeons:
  for t in tiers:
    r=replacements+[ReplaceDescription(d,t),ReplaceName(d,t)]
    a=[OPENPORTAL]
    modify(d.item,replace=r,add=a)
