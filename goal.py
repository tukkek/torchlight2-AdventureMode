#!/usr/bin/python3
# further modifies a generate.Dungeon with explicit, strategic rewards
import dataclasses,textwrap

NPC=textwrap.dedent('''
  <FLOAT>NPCS_MIN:0
  <FLOAT>NPCS_MAX:1
  <STRING>NPCSPAWNCLASS:{}
  ''').strip()

@dataclasses.dataclass
class Goal:
  name:str
  spawnclass:str
  generic:str=''
  
  def reward(self):
    raise Exception('unimplemented')
  
@dataclasses.dataclass
class Vendor(Goal):
  def __post_init__(self):
    self.generic='vendor'
    
  def reward(self):
    return NPC.format(self.spawnclass)

vendors=[Vendor('enchanter','AM_NPC_ENCHANTERS'),Vendor('set merchant','AM_NPC_SETS'),Vendor('socketer','AM_NPC_SOCKETER')]#TODO UNIT:GAMBLER_SECRETROOM

def search():
  import load,generate
  rewards={}
  for dungeon in load.scan():
    for line in generate.read(dungeon.dungeon):
      if next((search for search in ['PROP','NPC'] if search in line),False):
        line=line.strip().split(':')
        key=line[0]
        if key not in rewards:
          rewards[key]=set()
        rewards[key].add(line[1])
  for r in rewards:
    print(f'{r}: {rewards[r]}')
    
def reward():
  affixes={}
  for i,v in enumerate(vendors):
    affixes[f"{v.name}"]=v
    affixes[f"{v.generic}{i+1}"]=v
  for a in sorted(affixes.keys()):
    yield a,affixes[a]
