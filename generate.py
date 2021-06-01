#!/usr/bin/python3
#TODO README
#TODO use a different map icon for each tier
#TODO all normal dungeons that don't require changing the exits
#TODO all bosses that don't require changing the exits
#TODO all remaining dungeons
#TODO all wildernesses
#TODO at some point fixed-level ranges might be worth exploring rather than using offsets, it would give more of a sense of progress and adventure - it should be relatively easy to pull too with the right level ranges, drop ranges and constant scroll rarity
#TODO make this cross-platform (see #convert for starters)
import sys,os,shutil,dataclasses

ENCODING='utf-16'
DIRMEDIA='media'
DIRDUNGEONS='media/dungeons'
DIRMAPS='media/units/items/maps'
REFERENCE='/media/sda2/windows/steam/steamapps/common/Torchlight II/'#TODO make argument
OPENPORTAL='''	[EFFECT]
		<STRING>NAME:{}
		<STRING>ACTIVATION:DYNAMIC
		<STRING>DURATION:INSTANT
		<STRING>TYPE:OPEN PORTAL
		<BOOL>SAVE:TRUE
		<FLOAT>MIN:0
		<FLOAT>MAX:0
	[/EFFECT]
'''
PARENT='ESTHERIANCITY'
GUIDWARNING='''For extra safety make sure to check GUIDs on GUTS before publishing your mod.
If there are any collisions, regenerating the files again should solve the problem.'''

@dataclasses.dataclass
class Dungeon:
  name:str
  dungeon:str
  scroll:str='catacombsmapa105' #technically a Map but that's a highlighted Python function
  
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
    self.replacement=f'\t<TRANSLATE>DESCRIPTION:Right-click to enter {dungeon.name} (Tier {tier.name})\n'

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
  def __init__(self,t):
    self.pattern='<INTEGER>PLAYER_LVL_MATCH_MIN:'
    self.replacement=f'\t<INTEGER>PLAYER_LVL_MATCH_MIN:{t.minlevel}\n'
    
class ReplaceMaxMatchLevel(Replace):
  def __init__(self,t):
    self.pattern='<INTEGER>PLAYER_LVL_MATCH_MAX:'
    self.replacement=f'\t<INTEGER>PLAYER_LVL_MATCH_MAX:{t.maxlevel}\n'
    
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
    
class ReplaceIsMap(Replace):
  def __init__(self):
    self.pattern='<BOOL>MAP:'
    self.replacement=False
    
class ReplaceValue(Replace):
  def __init__(self,tier):
    self.pattern='<INTEGER>VALUE:'
    self.replacement=f'\t<INTEGER>VALUE:{tier.value}\n'
    
class ReplaceLevel(Replace):
  def __init__(self,tier):
    self.pattern='<INTEGER>LEVEL:'
    self.replacement=f'\t<INTEGER>LEVEL:{tier.minlevel}\n'
    
class ReplaceMinLevel(Replace):
  def __init__(self,tier):
    self.pattern='<INTEGER>MINLEVEL:'
    self.replacement=f'\t<INTEGER>MINLEVEL:{tier.mindroplevel}\n'
    
class ReplaceMaxLevel(Replace):
  def __init__(self,tier):
    self.pattern='<INTEGER>MAXLEVEL:'
    self.replacement=f'\t<INTEGER>MAXLEVEL:{tier.maxdroplevel}\n'
    
class ReplaceUses(Replace):
  def __init__(self):
    self.pattern='<STRING>USES:'
    self.replacement=f'\t<STRING>USES:1\n'

NUMERALS=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII']
TIERS=13

@dataclasses.dataclass
class Tier:
  tier:int
  name:str=''
  minlevel:int=''
  maxlevel:int=''
  offset:int=0
  mindroplevel:int=''
  maxdroplevel:int=''
  rarity:int=0
  value:int=0
  
  def __post_init__(self):
    t=self.tier
    self.name=NUMERALS[t]
    if t==0:
      self.minlevel=1
    elif t>10:
      self.minlevel=100
    else:
      self.minlevel=t*10
    self.maxlevel=(t+1)*10
    if t>=9:
      self.offset=(t-9)*10
    self.mindroplevel=self.maxlevel-20
    if self.mindroplevel<1:
      self.mindroplevel=1
    self.maxdroplevel=self.maxlevel+10
    self.rarity=TIERS-t
    self.value=t+1

#use scan.py to help generate this
dungeons=[Dungeon('Defiled Cemetery','map_catacombs_b_66'),Dungeon('Estherian Depths','map_estherian_a'),Dungeon('Frostbitten Caverns','map_icecaves_a'),Dungeon('Defiled Burrow','map_catacombs_2'),Dungeon('Ghastly Vault','map_catacombs_3'),Dungeon('Infernal Necropolis','map_catacombs_a_105'),Dungeon('Cursed Tombs','map_catacombs_a_56'),Dungeon('Cursed Mausoleum','map_catacombs_a_66'),Dungeon('Infernal Catacombs','map_catacombs_a_76'),Dungeon('Infernal Tombs','map_catacombs_a_86'),Dungeon('Infernal Mausoleum','map_catacombs_a_96'),Dungeon('Desecrated Sepulcher','map_catacombs_b_105'),Dungeon('Defiled Graves','map_catacombs_b_56'),Dungeon('Desecrated Burrow','map_catacombs_b_76'),Dungeon('Desecrated Graves','map_catacombs_b_86'),Dungeon('Desecrated Cemetery','map_catacombs_b_96'),Dungeon('Bloody Boneyard','map_catacombs_c_105'),Dungeon('Ghastly Crypt','map_catacombs_c_56'),Dungeon('Ghastly Mortuary','map_catacombs_c_66'),Dungeon('Bloody Vault','map_catacombs_c_76'),Dungeon('Bloody Crypt','map_catacombs_c_86'),Dungeon('Bloody Mortuary','map_catacombs_c_96'),Dungeon('Shadowy Grotto','map_caves_a'),Dungeon('Abyssal Fissure','map_caves_a_105'),Dungeon('Shadowy Pit','map_caves_a_56'),Dungeon('Shadowy Caves','map_caves_a_66'),Dungeon('Abyssal Grotto','map_caves_a_76'),Dungeon('Abyssal Pit','map_caves_a_86'),Dungeon('Abyssal Caves','map_caves_a_96'),Dungeon('Wyvern Keep','map_dragon_a'),Dungeon('Dragon Bastion','map_dragon_a105'),Dungeon('Wyvern Stronghold','map_dragon_a56-65'),Dungeon('Wyvern Citadel','map_dragon_a66-75'),Dungeon('Dragon Keep','map_dragon_a76-85'),Dungeon('Dragon Stronghold','map_dragon_a86-95'),Dungeon('Dragon Citadel','map_dragon_a96-105'),Dungeon('Forgotten Labs','map_dwarvenlabs_a'),Dungeon('Deserted Foundry','map_dwarvenlabs_a_105'),Dungeon('Forgotten Workshop','map_dwarvenlabs_a_56'),Dungeon('Forgotten Factory','map_dwarvenlabs_a_66'),Dungeon('Deserted Labs','map_dwarvenlabs_a_76'),Dungeon('Deserted Workshop','map_dwarvenlabs_a_86'),Dungeon('Deserted Factory','map_dwarvenlabs_a_96'),Dungeon('Ruined Shrine','map_estherian_b'),Dungeon('Desolate Chantry','map_estherian_b105'),Dungeon('Ruined Sanctuary','map_estherian_b56'),Dungeon('Ruined Temple','map_estherian_b66'),Dungeon('Desolate Shrine','map_estherian_b76'),Dungeon('Desolate Sanctuary','map_estherian_b86'),Dungeon('Desolate Temple','map_estherian_b96'),Dungeon('Infected Hollow','map_estherian_c'),Dungeon('Blighted Sanctum','map_estherian_c_105'),Dungeon('Infected Retreat','map_estherian_c_56'),Dungeon('Infected Depths','map_estherian_c_66'),Dungeon('Blighted Hollow','map_estherian_c_76'),Dungeon('Blighted Retreat','map_estherian_c_86'),Dungeon('Blighted Depths','map_estherian_c_96'),Dungeon('Frostshorn Breach','map_icecaves_a_105'),Dungeon('Frostbitten Ravine','map_icecaves_a_56'),Dungeon('Frostbitten Chasm','map_icecaves_a_66'),Dungeon('Frostshorn Caverns','map_icecaves_a_76'),Dungeon('Frostshorn Ravine','map_icecaves_a_86'),Dungeon('Frostshorn Chasm','map_icecaves_a_96'),Dungeon('Ransacked Halls','map_vaults_a'),Dungeon('Ezrohir Treasury','map_vaults_a105'),Dungeon('Ransacked Commons','map_vaults_a56'),Dungeon('Ransacked Vault','map_vaults_a66'),Dungeon('Ezrohir Halls','map_vaults_a76'),Dungeon('Ezrohir Commons','map_vaults_a86'),Dungeon('Ezrohir Vault','map_vaults_a96'),Dungeon('Cursed Catacombs','maproom_catacombs_1')]
tiers=[Tier(i) for i in range(0,TIERS)]

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
  return generated

maps=0
for d in dungeons:
  print(f'{d.name}...')
  for t in tiers:
    basename=f'{d.name.lower()}_{t.tier}'
    while ' ' in basename:
      basename=basename.replace(' ','_')
    dungeonname=f'am_{basename}'
    r=[ReplaceDisplayName(f'{d.name} (Tier {t.name})'),
       ReplaceName(dungeonname),ReplaceParentDungeon(),
       ReplaceParentTown(),ReplaceMinMatchLevel(t),
       ReplaceMaxMatchLevel(t),ReplaceIsMap()]
    a=[f'\t<INTEGER>PLAYER_LVL_MATCH_OFFSET:{t.offset}\n']
    modify(d.dungeon,dungeonname,replace=r,add=a)
    mapname=f'am_map_{basename}'
    r=[ReplaceDisplayName(f'{d.name} map ({t.name})'),
       ReplaceName(mapname),ReplaceDescription(d,t),
       ReplaceRarity(t),ReplaceDungeon(dungeonname),
       ReplaceGuid(mapname),ReplaceValue(t),
       ReplaceLevel(t),ReplaceMinLevel(t),
       ReplaceMaxLevel(t),ReplaceUses()]
    a=[OPENPORTAL.format(dungeonname)]
    modify(d.scroll,mapname,replace=r,add=a)
    maps+=1
print()
print(f'Generated {len(dungeons)} dungeons, {len(tiers)} tiers, {maps} maps.')
print(GUIDWARNING)
