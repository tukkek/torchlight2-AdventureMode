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
PARENT='ESTHERIANCITY'

@dataclasses.dataclass
class Dungeon:
  name:str
  dungeon:str
  scroll:str #technically a Map but that's a highlighted Python function
  
  def topath(self,path,filename):
    return f'{path}/{filename}.dat'
  
  def __post_init__(self):
    self.dungeon=self.topath(DIRDUNGEONS,self.dungeon)
    self.scroll=self.topath(DIRMAPS,self.scroll)
    
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
  def __init__(self,to):
    self.pattern='<TRANSLATE>DISPLAYNAME:'
    self.replacement=f'\t<TRANSLATE>DISPLAYNAME:{to}\n'
    
class ReplaceParentDungeon(Replace):
  def __init__(self):
    self.pattern='<STRING>PARENT_DUNGEON:'
    self.replacement=f'\t<STRING>PARENT_DUNGEON:{PARENT}\n'
    
class ReplaceParentTown(Replace):
  def __init__(self):
    self.pattern='<STRING>PARENT_TOWN:'
    self.replacement=f'\t<STRING>PARENT_TOWN:{PARENT}\n'
    
class ReplaceMinMatchLevel(Replace):
  def __init__(self):
    self.pattern='<INTEGER>PLAYER_LVL_MATCH_MIN:'
    self.replacement=f'\t<INTEGER>PLAYER_LVL_MATCH_MIN:1\n'
    
class ReplaceMaxMatchLevel(Replace):
  def __init__(self):
    self.pattern='<INTEGER>PLAYER_LVL_MATCH_MAX:'
    self.replacement=f'\t<INTEGER>PLAYER_LVL_MATCH_MAX:105\n'
    
@dataclasses.dataclass
class Tier:
  name:str
  offset:int

dungeons=[Dungeon('Infernal Necropolis','map_catacombs_a_105','catacombsmapa105')] #TODO begging with all end-game dungeons
tiers=[Tier('hard',5)]#TODO

def modify(path,replace=[],add=[]):
  generated=[]
  with open(REFERENCE+path.upper(),encoding=ENCODING) as f:
    for line in f:
      for r in replace:
        if r.pattern in line:
          generated.append(r.replacement)
          break
      else:
        generated.append(line)
  for a in add:
    generated.insert(len(generated)-1,a)
  generated=''.join(generated)
  print(generated,file=open(path,'w',encoding=ENCODING))
  return generated

def setup():
  if os.path.exists(DIRMEDIA):
    shutil.rmtree(DIRMEDIA)
  os.makedirs(DIRDUNGEONS)
  os.makedirs(DIRMAPS)

setup()

for d in dungeons:
  for t in tiers:
    name=ReplaceName(f'{d.name} map ({t.name})')
    r=[ReplaceMinLevel(),ReplaceMaxLevel(),ReplaceDescription(d,t),name]
    a=[OPENPORTAL]
    modify(d.scroll,replace=r,add=a)
    r=[name,ReplaceParentDungeon(),ReplaceParentTown(),ReplaceMinMatchLevel(),ReplaceMaxMatchLevel()]
    a=[f'\t<INTEGER>PLAYER_LVL_MATCH_OFFSET:{t.offset}\n'] #TODO does adding this to the end rather than the "right" space impact in any way? hopefully not since its seems like XML. should be asy to test by just seeing if GUTS recognizes it when opening the data.
    print(modify(d.dungeon,replace=r,add=a))
    
