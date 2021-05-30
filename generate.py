#!/usr/bin/python3
#TODO guid
#TODO all maps
#TODO all normal dungeons that don't require changing the exits
#TODO all bosses that don't require changing the exits
#TODO all remaining dungeons
#TODO all wildernesses
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
    
class ReplaceDisplayName(Replace):
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
    
class ReplaceName(Replace):
  def __init__(self,to):
    self.pattern='<STRING>NAME:'
    self.replacement=f'\t<STRING>NAME:{to}\n'
    
class ReplaceRarity(Replace):
  def __init__(self,tier):
    self.pattern='<INTEGER>RARITY:'
    self.replacement=f'\t<INTEGER>RARITY:{tier.rarity}\n'
    
class ReplaceDungeon(Replace):
  def __init__(self,name):
    self.pattern='<STRING>DUNGEON:'
    self.replacement=f'\t<STRING>DUNGEON:{name}\n'
    
@dataclasses.dataclass
class Tier:
  name:str
  offset:int
  rarity:int

dungeons=[Dungeon('Infernal Necropolis','map_catacombs_a_105','catacombsmapa105')] #TODO
tiers=[Tier('easy',0,20),Tier('normal',10,8),Tier('hard',20,4),Tier('epic',30,2),Tier('legendary',40,1),]#TODO casual?

def modify(path,destination,replace=[],add=[]):
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
  destination=f'{os.path.dirname(path)}/{destination}.dat'
  with open(destination,'w',encoding=ENCODING) as f:
    f.write(generated)
  os.system(f'cat {destination} | unix2dos -u  > {destination}.tmp')
  os.system(f'mv {destination}.tmp {destination}')
  return generated

def setup():
  if os.path.exists(DIRMEDIA):
    shutil.rmtree(DIRMEDIA)
  os.makedirs(DIRDUNGEONS)
  os.makedirs(DIRMAPS)

setup()

for d in dungeons:
  for t in tiers[:1]:#TODO
    basename=f'{d.name.lower()}_{t.offset}'
    while ' ' in basename:
      basename=basename.replace(' ','_')
    displayname=ReplaceDisplayName(f'{d.name}')
    dungeon=f'am_{basename}'
    r=[displayname,ReplaceName(dungeon),ReplaceParentDungeon(),ReplaceParentTown(),ReplaceMinMatchLevel(),ReplaceMaxMatchLevel()]
    a=[f'\t<INTEGER>PLAYER_LVL_MATCH_OFFSET:{t.offset}\n'] #TODO does adding this to the end rather than the "right" space impact in any way? hopefully not since its seems like XML. should be asy to test by just seeing if GUTS recognizes it when opening the data.
    modify(d.dungeon,dungeon,replace=r,add=a)
    displayname=ReplaceDisplayName(f'{d.name} map ({t.name})')
    scroll=f'am_map_{basename}'
    r=[displayname,ReplaceName(scroll),ReplaceMinLevel(),ReplaceMaxLevel(),ReplaceDescription(d,t),ReplaceRarity(t),ReplaceDungeon(dungeon)]
    a=[OPENPORTAL]
    modify(d.scroll,scroll,replace=r,add=a)
os.system('cp -r static/* media/')
