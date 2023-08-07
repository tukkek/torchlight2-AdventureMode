import random

MIN='\t<INTEGER>MINRANDOMAFFIXES:{}'
MAX='\t<INTEGER>MAXRANDOMAFFIXES:{}'
AFFIX='	\t<STRING>AFFIX:{}'
PLAYERBUFFS='''
\t[RANDOMPLAYERAFFIXES]
{}
\t[/RANDOMPLAYERAFFIXES]
'''
MONSTERBUFFS='''
\t[RANDOMMONSTERAFFIXES]
{}
\t[/RANDOMMONSTERAFFIXES]
'''
MONSTERDEBUFFS='''
\t[RANDOMMONSTERPENALTYAFFIXES]
{}
\t[/RANDOMMONSTERPENALTYAFFIXES]
'''

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

class Blazing(Theme):
  def __init__(self):
    super().__init__('Blazing')
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

themes=[t() for t in [Blazing,Galvanic,Glacial,Brutal,Vigorous,Lucky,Arcane,Warped,Toxic]]

def clean(line):
  if 'MINRANDOMAFFIXES' in line or 'MAXRANDOMAFFIXES' in line:
    return True
  if 'RANDOM' in line and 'AFFIXES' in line:
    return True
  if '<STRING>AFFIX:' in line:
    return True
  return False

def splice(line,lines):
  lines.insert(len(lines)-1,line+'\n')

def add(affixes,template,lines):
  if len(affixes)==0:
    return
  affixes='\n'.join(AFFIX.format(a) for a in affixes)
  template=template.format(affixes)
  for line in template.split('\n'):
    if len(line.strip())>0:
      splice(line,lines)

'''
Affixes aren't the same in the actual dungeon as on the scroll.
This is probably because of using an item effect rather than mapworks prop?
Fix it by deciding affixes here at generation time.
There are tens of thousands of scrolls so it's virtually random either way.
Vast majority of scrolls are 0-4 affixes, so using that here too.
'''
def generate(filename,lines):
  scroll=False
  for i in reversed(range(len(lines))):
    if clean(lines[i]):
      lines.pop(i)
      scroll=True
  if not scroll:
    return
  random.seed(filename)
  t=random.choice(themes)
  for i in range(len(lines)):
    l=lines[i]
    if 'DISPLAYNAME:' in l:
      lines[i]=l.replace('DISPLAYNAME:',f'DISPLAYNAME:{t.name} ')
      break
  c=t.count()
  splice(MIN.format(c),lines)
  splice(MAX.format(c),lines)
  add(t.player.buffs,PLAYERBUFFS,lines)
  m=t.monster
  add(m.buffs,MONSTERBUFFS,lines)
  add(m.debuffs,MONSTERDEBUFFS,lines)
  
