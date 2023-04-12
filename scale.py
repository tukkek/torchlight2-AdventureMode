#!/usr/bin/python3
# scales vanilla maps (eg. phase-beast portals)
import generate,os,load

class ClearLevel(generate.Replace):
  def __init__(self):
    self.pattern='<INTEGER>LEVEL:'
    self.replacement=''
    
dungeons=load.scan()
replace=[generate.ReplaceParentDungeon(),generate.ReplaceParentTown(),generate.ReplaceMinMatchLevel(generate.tiers[0]),
         generate.ReplaceMaxMatchLevel(generate.tiers[-1]),ClearLevel()]
for d in dungeons:
  n=d.dungeonname
  if n=='town1':#static file
    continue
  generate.modify(f'MEDIA/DUNGEONS/{n}.DAT',n,replace)
  filename=f'{n}.dat'
  os.rename(f'media/dungeons/{filename}',f'media/dungeons/{filename.upper()}')
