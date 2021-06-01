#!/usr/bin/python3
#TODO all maps
#TODO all normal dungeons that don't require changing the exits
#TODO all bosses that don't require changing the exits
#TODO all remaining dungeons
#TODO all wildernesses
#TODO at some point fixed-level ranges might be worth exploring rather than using offsets, it would give more of a sense of progress and adventure - it should be relatively easy to pull too with the right level ranges, drop ranges and constant scroll rarity
#TODO make this not linux-dependeant (see #convert for starters)
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
  replacement:str #if False, skip line
  
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
    
class ReplaceGuid(Replace):
  def __init__(self,name):
    self.pattern='<STRING>UNIT_GUID:'
    self.replacement=f'\t<STRING>UNIT_GUID:{hash(name)}\n'
    print(name)
    print(hash(name))
    
class ReplaceIsMap(Replace):
  def __init__(self):
    self.pattern='<BOOL>MAP:'
    self.replacement=False
    
@dataclasses.dataclass
class Tier:
  name:str
  offset:int
  rarity:int

dungeons=[Dungeon('Infernal Necropolis','map_catacombs_a_105','catacombsmapa105')] #TODO
tiers=[Tier('easy',0,20),Tier('normal',10,8),Tier('hard',20,4),Tier('epic',30,2),Tier('legendary',40,1),]
totalgenerated=0

'''
This is a shame but I have been unable to generate binary-identical .dat files with Python alone or understand 100% why I can't.
Thankfully the `unix2dos` utility (`apt-get install dos2unix` on Debian) does the job.
A workaround to this is opening the .dat files on Windows 10's `wordpad` manually and simply saving them but that's a lot of tedious, manual labor for every generated batch...
I believe this must have something to do with \r\n on Windows but I have tried adding those manually as well.
TODO solving this would be a necessary step to making this script cross-platform
'''
def convert(destination):
  os.system(f'cat {destination} | unix2dos -u  > {destination}.tmp')
  os.system(f'mv {destination}.tmp {destination}')

def modify(path,destination,replace=[],add=[]):
  generated=[]
  with open(REFERENCE+path.upper(),encoding=ENCODING) as f:
    for line in f:
      for r in replace:
        if r.pattern in line:
          if r.replacement:
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
  convert(destination)
  global totalgenerated
  totalgenerated+=1
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
    dungeonname=f'am_{basename}'
    r=[ReplaceDisplayName(f'{d.name}'),ReplaceName(dungeonname),
       ReplaceParentDungeon(),ReplaceParentTown(),
       ReplaceMinMatchLevel(),ReplaceMaxMatchLevel(),
       ReplaceIsMap()]
    a=[f'\t<INTEGER>PLAYER_LVL_MATCH_OFFSET:{t.offset}\n']
    modify(d.dungeon,dungeonname,replace=r,add=a)
    mapname=f'am_map_{basename}'
    r=[ReplaceDisplayName(f'{d.name} map ({t.name})'),
       ReplaceName(mapname),ReplaceMinLevel(),
       ReplaceMaxLevel(),ReplaceDescription(d,t),
       ReplaceRarity(t),ReplaceDungeon(dungeonname),
       ReplaceGuid(mapname)]
    a=[OPENPORTAL]
    modify(d.scroll,mapname,replace=r,add=a)
print(f'{totalgenerated} files generated.\nFor extra safety make sure to check GUIDs on GUTS before publishing your mod.')
os.system('cp -r static/media/* media/')
