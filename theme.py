#!/usr/bin/python3
class Affixes:
  def __init__(self):
    self.buffs=[]
    self.debuffs=[]

class Theme:
  def __init__(self,n):
    self.name=n
    self.player=Affixes()
    self.player.debuffs=False
    self.monster=Affixes()
    
  def count(self):
    return sum(len(affixes) for affixes in [self.player.buffs,self.monster.buffs,self.monster.debuffs])

class Infernal(Theme):
  def __init__(self):
    super().__init__('Infernal')
    self.player.buffs=['MAP_BURNING','MAP_FIRE_DAMAGE_PERCENT_BONUS_15'] 
    self.monster.buffs=['MAP_BURNING','MAP_EXPLODEONDEATH']

class Galvanic(Theme):
  def __init__(self):
    super().__init__('Galvanic')
    self.player.buffs=['MAP_ELECTRIC_DAMAGE_PERCENT_BONUS_15'] 
    self.monster.buffs=['MAP_ELECTRIC_DAMAGE_PERCENT_BONUS_15','MAP_MONSTER_SPEED_PERCENT_BONUS_10'] 

class Glacial(Theme):
  def __init__(self):
    super().__init__('Glacial')
    self.player.buffs=['MAP_FREEZING','MAP_ICE_DAMAGE_PERCENT_BONUS_15']
    self.monster.buffs=['MAP_FREEZING','MAP_ICE_DAMAGE_PERCENT_BONUS_15']
    self.monster.debuffs=['MAP_MONSTER_MOVE_PENALTY']

class Brutal(Theme):
  def __init__(self):
    super().__init__('Brutal')
    self.player.buffs=['MAP_PLAYER_BIG_HITS']
    self.monster.buffs=['MAP_MONSTER_DAMAGE_PERCENT_BONUS_15','MAP_MONSTER_SPEED_PERCENT_BONUS_10']
    
class Vigorous(Theme):
  def __init__(self):
    super().__init__('Vigorous')
    self.player.buffs=['MAP_PLAYER_HEALTH_REGEN']
    self.monster.buffs=['MAP_MONSTER_HEALTH_PERCENT_BONUS_15','MAP_PLAYER_HEALTH_REGEN']
    self.monster.debuffs=['MAP_MONSTER_DAMAGE_PERCENT_PENALTY_15']

class Lucky(Theme):
  def __init__(self):
    super().__init__('Lucky')
    self.player.buffs=['MAP_PLAYER_EXP_BONUS_5','MAP_PLAYER_GOLD_BONUS','MAP_PLAYER_MF_BONUS_15']

class Arcane(Theme):
  def __init__(self):
    super().__init__('Arcane')
    self.player.buffs=['MAP_PLAYER_SUMMON_SKULL','MAP_PLAYER_REDUCE_MANA_COST']
    self.monster.buffs=['CHAMPIONHAUNTED']

class Warped(Theme):
  def __init__(self):
    super().__init__('Warped')
    self.monster.buffs=['CHAMPIONRANDOMTELEPORT','CHAMPIONRANDOMTELEPORTONSTRUCK','CHAMPIONTELEPORTING']

class Toxic(Theme):
  def __init__(self):
    super().__init__('Toxic')
    self.player.buffs=['MAP_POISON_DAMAGE_PERCENT_BONUS_15']
    self.monster.buffs=['MAP_NOXIOUS','MAP_POISON_DAMAGE_PERCENT_BONUS_15']

themes=[t() for t in [Infernal,Galvanic,Glacial,Brutal,Vigorous,Lucky,Arcane,Warped,Toxic]]

count=0
for t in themes:
  print(t,t.count())
  count+=t.count()
print(count)
