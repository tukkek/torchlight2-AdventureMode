#!/usr/bin/python3
import sys,os,shutil,dataclasses,load,goal,args,summary,theme

ENCODING='utf-16'
DIRMEDIA='media'
DIRDUNGEONS='media/dungeons'
REFERENCE=args.reference
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
GUIDWARNING='For extra safety make sure to check GUIDs on GUTS before publishing.'
FILES={}
NUMERALS=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI']
TIERS=len(NUMERALS)
#TODO move data to maps.yaml?
MAPS=['map_catacombs_b_66','map_estherian_a','map_icecaves_a','map_catacombs_2','map_catacombs_3','map_catacombs_a_105','map_catacombs_a_56','map_catacombs_a_66','map_catacombs_a_76','map_catacombs_a_86','map_catacombs_a_96','map_catacombs_b_105','map_catacombs_b_56','map_catacombs_b_76','map_catacombs_b_86','map_catacombs_b_96','map_catacombs_c_105','map_catacombs_c_56','map_catacombs_c_66','map_catacombs_c_76','map_catacombs_c_86','map_catacombs_c_96','map_caves_a','map_caves_a_105','map_caves_a_56','map_caves_a_66','map_caves_a_76','map_caves_a_86','map_caves_a_96','map_dragon_a','map_dragon_a105','map_dragon_a56-65','map_dragon_a66-75','map_dragon_a76-85','map_dragon_a86-95','map_dragon_a96-105','map_dwarvenlabs_a','map_dwarvenlabs_a_105','map_dwarvenlabs_a_56','map_dwarvenlabs_a_66','map_dwarvenlabs_a_76','map_dwarvenlabs_a_86','map_dwarvenlabs_a_96','map_estherian_b','map_estherian_b105','map_estherian_b56','map_estherian_b66','map_estherian_b76','map_estherian_b86','map_estherian_b96','map_estherian_c','map_estherian_c_105','map_estherian_c_56','map_estherian_c_66','map_estherian_c_76','map_estherian_c_86','map_estherian_c_96','map_icecaves_a_105','map_icecaves_a_56','map_icecaves_a_66','map_icecaves_a_76','map_icecaves_a_86','map_icecaves_a_96','map_vaults_a','map_vaults_a105','map_vaults_a56','map_vaults_a66','map_vaults_a76','map_vaults_a86','map_vaults_a96','maproom_catacombs_1']
DUNGEONS=['A3-banepits','a3werewolfcellar','desertcaves','witherways']#TODO scale NG_NW_ICELABS NG_SE_ICELABS A2Z1_CURSEDFEAR_DESERTCAVES'
BOSSES=['A3-3SISTERS','arenaofslaughter','cacklespitsrealm','cultistslair','deadshoals','jehannum','koraricave','manavent','ngbearcave','ngdwarfarmory','piratecove','riftkeep','thesawmill','a3-scrapworks','slaversden','manticorelair','swarmpoint','desertcatacombs','GOBLIN_EMBERCAVES','thegardenoftears','thing','towerofthemoon','undercurrents','vaultofsouls','a3-warforge','wellspringtreasury','crowspass_spidercave']
WILDS=['a3-battlefield','a3blightbogs','broodhive','crowspass','a3pass1','frostedhills','hauntedquarter','osseanwastes','pathofhonoreddead','a3pass2','saltbarrens','templesteppes','vulturepass']
NETHER=['nether','nether_a1z1','nether_a1z2','nether_a2z1','nether_a2z2','nether_a3z1','nether_a3z2']
CHALLENGES=['phasebeast_a1z1_all','phasebeast_a1z2_all','phasebeast_a2z1_all','phasebeast_a2z2_all','phasebeast_a2z2_JT','phasebeast_a3z1_all','phasebeast_a3z2_all','phasebeast_a3z2_lava','phasepillar','luminousarena']

@dataclasses.dataclass
class Replace:
  pattern:str
  replacement:str #if False, skip line
  
class ReplaceDescription(Replace):
  def __init__(self,dungeon,tier,goal=False):
    self.pattern='<TRANSLATE>DESCRIPTION:'
    self.replacement=f'\t<TRANSLATE>DESCRIPTION:'
    if goal:
      self.replacement+=f'May contain {goal.name}.\n'
    else:
      self.replacement+=f'Right-click to enter {dungeon.name} (Tier {tier.name})\n'

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
  def __init__(self,tier,ratio=1):
    self.pattern='<INTEGER>RARITY:'
    self.replacement=f'\t<INTEGER>RARITY:{round(tier.rarity*ratio)}\n'
    
class ReplaceDungeon(Replace):
  def __init__(self,name):
    self.pattern='<STRING>DUNGEON:'
    self.replacement=f'\t<STRING>DUNGEON:{name}\n'
    
class ReplaceGuid(Replace):
  def __init__(self,name):
    self.pattern='<STRING>UNIT_GUID:'
    self.replacement=f'\t<STRING>UNIT_GUID:{hash(name)}\n'
    
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
    
class ReplaceIcon(Replace):
  def __init__(self,icon,tier):
    self.pattern='<STRING>ICON:'
    self.replacement=f'\t<STRING>ICON:{icon}_{tier.tier}\n'
    
'''TODO
this does not work as intended, if you enter a map scroll portal a second time, it will be as it was, see http://torchmodders.com/forums/modding-questions/weird-guts-editor-bugs/ ( https://archive.ph/wip/BdA0v )
thankfully the chance of a repeat scroll of the same tier is less than 1% for each map generated in that tier and i've never had it happen while playtesting
apparently you could make every strata in a dungeon 'don't store" and that will repopulate (but not re-generate) but the drawback from that is that you also can't teleport back into a dungeon after using a town portal scroll
i imagine that ideally this should be covered by "is map" in the sense that it'd regenerate on accessing it but not opening a portal to return? alas, if there's no documentation and VOLATILE has no effect, there's not much that can be done
'''
class ReplaceVolatile(Replace):
  def __init__(self):
    self.pattern='<BOOL>VOLATILE:'
    self.replacement=False

class ReplaceIsMap(Replace):#removed with False then added in makedungeons
  def __init__(self):
    self.pattern='<BOOL>MAP:'
    self.replacement=False

class ClearGoalsMinMax(Replace):
  def __init__(self):
    self.pattern='<FLOAT>NPCS_'
    self.replacement=False

class ClearGoals(Replace):
  def __init__(self):
    self.pattern='<STRING>NPCSPAWNCLASS'
    self.replacement=False

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
    self.minlevel=(t+1)*5
    self.maxlevel=self.minlevel 
    if t==0:
      self.minlevel=1
      self.maxlevel=5
    elif t==TIERS-1:
      self.maxlevel=100
    self.mindroplevel=1
    self.maxdroplevel=self.maxlevel+5
    self.rarity=round(2**(TIERS-t-1)/goal.factor)
    self.value=t+1
    
@dataclasses.dataclass
class Category:
  maps:list
  icon:str
  category:str
  goals:bool=False

tiers=[Tier(i) for i in range(0,TIERS)]
categories=[Category(MAPS,'mapdg','maps',True),Category(DUNGEONS,'mapdg','dungeons',True),Category(WILDS,'mapwild','wilderness',True),
            Category(NETHER,'mapnether','netherrealm'),Category(BOSSES,'mapboss','bosses'),Category(CHALLENGES,'mapphase','challenges'),]
count=0

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

def read(path):
  with open(REFERENCE+path.upper(),encoding=ENCODING) as lines:
    for l in lines:
      yield l

def modify(path,destination,replace=[],add=[],strata='',extension='.dat'):
  generated=[]
  for line in read(path):
    for r in replace:
      if r.pattern in line:
        if r.replacement:
          generated.append(r.replacement)
        break
    else:
      generated.append(line)
      if len(strata)>0 and '[STRATA0]' in line:
        generated.extend(f'\t\t{line}\n' for line in strata.split('\n'))
  for a in add:
    generated.insert(len(generated)-1,a)
  if len(strata)>0:
    theme.generate(destination,generated)
  destination=f'{os.path.dirname(path)}/{destination}{extension}'.lower()
  os.makedirs(os.path.dirname(destination),exist_ok=True)
  with open(destination,'w',encoding=ENCODING) as f:
    for g in generated:
      f.write(g)
  convert(destination)
  return destination

def makedungeon(category,d,tier,goal=False):
  name=f'{d.dungeonname}_{tier.tier+1}'
  if goal:
    name+='_'+goal.spawnclass.replace('am_spawn_prop_','').replace('am_','')
  dungeonname=f'am_{name}'
  r=[ReplaceDisplayName(f'{d.name} (Tier {tier.name})'),
    ReplaceName(dungeonname),ReplaceParentDungeon(),
    ReplaceParentTown(),ReplaceMinMatchLevel(tier),
    ReplaceMaxMatchLevel(tier),ReplaceIsMap(),
    ClearGoalsMinMax(),ClearGoals(),]
  a=[f'\t<INTEGER>PLAYER_LVL_MATCH_OFFSET:{tier.offset}\n','\t<BOOL>MAP:true\n']
  g=goal.data if goal else ''
  modify(d.dungeon,dungeonname,replace=r,add=a,strata=g)
  mapname=f'am_map_{name}'
  rarity=goal.rarity if goal else 1
  r=[ReplaceDisplayName(f'{theme.rename(d.name)} map ({tier.name})'),
    ReplaceName(mapname),ReplaceDescription(d,tier,goal),
    ReplaceRarity(tier,rarity),ReplaceDungeon(dungeonname),
    ReplaceGuid(mapname),ReplaceValue(tier),
    ReplaceLevel(tier),ReplaceMinLevel(tier),
    ReplaceMaxLevel(tier),ReplaceUses(),ReplaceIcon(category.icon,tier)]
  a=[OPENPORTAL.format(dungeonname)]
  modify(d.scroll,mapname,replace=r,add=a)
  global count
  count+=1

def makedungeons(category):
  for m in category.maps:
    d=FILES[m.lower()]
    d.dungeonname=m #TODO preserves case, probably unnecesssary
    yield d
    for t in tiers[:1] if args.debug else tiers:
      if category.goals:
        for g in goal.reward():
          makedungeon(category,d,t,g)
      else:
        makedungeon(category,d,t)
        

if __name__ == '__main__':
  for dungeon in load.scan():
    FILES[dungeon.dungeonname.lower()]=dungeon
  for c in CHALLENGES:
    FILES[c.lower()].name='Challenge'
  total=sum(len(c.maps) for c in categories)
  progress=0
  for c in [categories[0]] if args.debug else categories:
    for d in makedungeons(c):
      print(f'{round(100*progress/total)}% {d.name}')
      progress+=1
  print()
  summary.show(count)
  print()
  print(GUIDWARNING)
