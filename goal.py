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

vendors=[Vendor('enchanters','AM_NPC_ENCHANTERS'),
         Vendor('set merchants','AM_NPC_SETS'),Vendor('socketers','AM_NPC_SOCKETER')]#TODO UNIT:GAMBLER_SECRETROOM
potions=[Goal('potions','AM_POTION',0,12)]
shrines=[Goal('shrines','AM_SHRINE')]
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
maxgoals=max(len(c) for c in categories)

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
  for c in categories:
    rarity=1/len(c)
    for goal in c:
      goal.rarity=rarity

def reward():
  distribute()
  for c in categories if args.debug else categories:
    for goal in c:
      yield goal
