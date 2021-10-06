#!/usr/bin/python3
import glob,os

DIRDUNGEONS='MEDIA/DUNGEONS'
REFERENCE='/media/sda2/windows/steam/steamapps/common/Torchlight II/'#TODO make argument

dungeons=[]

def findnames(path):
  names=[]
  with open(path,encoding='utf-16') as f:
    for l in f.readlines():
      if 'DISPLAYNAME:' in l:
        names.append(l[l.index(':')+1:l.index('\n')])
  return names

def scan(query):
  global dungeons
  for m in glob.glob(query):
    if 'QA_ARENA' in m:
      print(f'skip arena: {m}...')
      continue
    try:
      dungeonname=os.path.basename(m)
      dungeonname=dungeonname[:dungeonname.index('.')]
      #dungeonname=findnames(m)[0]
      displayname=findnames(f'{REFERENCE}/{DIRDUNGEONS}/{dungeonname.upper()}.DAT')[0]
      dungeons.append(f"Dungeon('{displayname}','{dungeonname.lower()}')")
    except Exception as e:
      print('error: '+m)
      raise e
    
scan(f'{REFERENCE}/{DIRDUNGEONS}/MAP_*.DAT')
scan(f'{REFERENCE}/{DIRDUNGEONS}/MAPROOM_*.DAT')
print(f"[{','.join(dungeons)}]")
print(f'{len(dungeons)} dungeons found')
