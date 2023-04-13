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
  rarity=1
  data=''
  
  def __post_init__(self):
    self.data=NPC.format(self.spawnclass)

vendors=[Goal('vendor','AM_NPC'),Goal('enchanter','AM_NPC_ENCHANTERS'),
         Goal('set merchant','AM_NPC_SETS'),Goal('socketer','AM_NPC_SOCKETER')]#TODO UNIT:GAMBLER_SECRETROOM
categories=[vendors,]

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

def distribute():
  percategory=1/len(categories)
  for c in categories:
    rarity=percategory/2
    c[0].rarity=rarity
    rarity/=len(c)-1
    for goal in c[1:]:
      goal.rarity=rarity

def reward():
  distribute()
  for c in categories:
    for goal in c:
      yield goal
