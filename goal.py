#!/usr/bin/python3
# further modifies a generate.Dungeon with explicit, strategic rewards
import dataclasses,textwrap,args

NPC=textwrap.dedent('''
  <FLOAT>NPCS_MIN:{}
  <FLOAT>NPCS_MAX:{}
  <STRING>NPCSPAWNCLASS:{}
  ''').strip()

@dataclasses.dataclass
class Goal:
  name:str
  spawnclass:str
  minimum:int=0
  maximum:int=6
  rarity:int=1
  data:str=''
  
  def __post_init__(self):
    self.data=NPC.format(self.minimum,self.maximum,self.spawnclass)
    
@dataclasses.dataclass
class Vendor(Goal):
  maximum:int=1

vendors=[Vendor('enchanters','am_npc_enchanters'),
         Vendor('set merchants','am_npc_sets'),Vendor('socketers','am_npc_socketer')]#TODO UNIT:GAMBLER_SECRETROOM
potions=[Goal('potions','am_potion',0,12)]
shrines=[Goal('shrines','am_shrine')]
weapons=[Goal('bows and crossbows','am_weapon_bow'),
         Goal('cannons, pistols and shotgonnes','am_weapon_firearm'),
         Goal('staves and wands','am_weapon_focus'),
         Goal('axes, claws, maces and swords','am_weapon_melee_small'),
         Goal('greataxes, greathammers, greatswords and polearms','am_weapon_melee_large'),]
armor=[Goal('boots','am_armor_boots'),Goal('chest armor','am_armor_chest'),
       Goal('gloves','am_armor_gloves'),Goal('helmets','am_armor_helmet'),Goal('pants','am_armor_pants'),
       Goal('shields','am_armor_shield'),Goal('shoulder armor','am_armor_shoulder')]
trinkets=[Goal('belts','am_trinket_belt'),Goal('necklaces','am_trinket_necklace'),
          Goal('rings','am_trinket_ring')]
categories=[weapons,armor,trinkets,
            vendors,potions,shrines,]
factor=0

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
  rarity=1/len(categories)
  for c in categories:
    crarity=rarity/len(c)
    for goal in c:
      goal.rarity=crarity
  global factor
  factor=min(goal.rarity for c in categories for goal in c)

def reward():
  for c in categories if args.debug else categories:
    for goal in c:
      yield goal

distribute()
