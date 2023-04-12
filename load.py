#!/usr/bin/python3
import glob,os,dataclasses

DIRDUNGEONS='MEDIA/DUNGEONS'
REFERENCE='/media/sda2/windows/steam/steamapps/common/Torchlight II/'#TODO make argument
DIRMAPS='media/units/items/maps'

@dataclasses.dataclass
class Dungeon:
  name:str
  dungeonname:str
  scroll:str='catacombsmapa105' #technically a Map but that's a highlighted Python function
  
  def topath(self,path,filename):
    return f'{path}/{filename}.dat'
  
  def __post_init__(self):
    self.dungeon=self.topath(DIRDUNGEONS,self.dungeonname)
    self.scroll=self.topath(DIRMAPS,self.scroll)
    
dungeons=[]

def findnames(path):
  names=[]
  with open(path,encoding='utf-16') as f:
    for l in f.readlines():
      if 'DISPLAYNAME:' in l:
        names.append(l[l.index(':')+1:l.index('\n')])
  return names

def scan(query='*.DAT',prefix=f'{REFERENCE}/{DIRDUNGEONS}/'):
  scanned=[]
  duplicates=set()
  for m in glob.glob(prefix+query):
    if 'QA_ARENA' in m:
      print(f'skip arena: {m}...')
      continue
    try:
      name=os.path.basename(m)
      name=name[:name.index('.')]
      #name=findnames(m)[0]
      displayname=findnames(f'{REFERENCE}/{DIRDUNGEONS}/{name.upper()}.DAT')[0]
      d=Dungeon(displayname,name.lower())
      if d.dungeonname in duplicates:
        raise Exception('Duplicate name: '+self.name)
      duplicates.add(d.dungeonname)
      scanned.append(d)
    except Exception as e:
      print('error: '+m)
      raise e
  return scanned
