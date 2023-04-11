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
  scanned=[]
  for m in glob.glob(query):
    if 'QA_ARENA' in m:
      print(f'skip arena: {m}...')
      continue
    try:
      name=os.path.basename(m)
      name=name[:name.index('.')]
      #name=findnames(m)[0]
      displayname=findnames(f'{REFERENCE}/{DIRDUNGEONS}/{name.upper()}.DAT')[0]
      scanned.append(f'Dungeon("{displayname}","{name.lower()}")')
    except Exception as e:
      print('error: '+m)
      raise e
  return scanned

dungeons.extend(scan(f'{REFERENCE}/{DIRDUNGEONS}/MAP_*.DAT'))
dungeons.extend(scan(f'{REFERENCE}/{DIRDUNGEONS}/MAPROOM_*.DAT'))
print(f"[{','.join(dungeons)}]")
print(f'{len(dungeons)} dungeons found')
