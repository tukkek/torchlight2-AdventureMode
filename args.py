#!/usr/bin/python3
import argparse

debug=False
reference='/media/sda2/windows/steam/steamapps/common/Torchlight II/'

def setup():
  global debug,reference
  p=argparse.ArgumentParser()
  p.add_argument('-r','--reference',action='store',help='path to the "Torchlight II" installation directory',required=True)
  p.add_argument('--debug',action='store_true')
  args=p.parse_args()
  debug=args.debug
  r=args.reference
  
setup()
