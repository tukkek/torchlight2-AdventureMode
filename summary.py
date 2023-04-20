import generate,goal,textwrap

TIERS=textwrap.dedent('''
  {} tiers generated for:
  {}
''')
REWARDS=textwrap.dedent('''
  {} reward types:
  {}
''')
SUMMARY=textwrap.dedent('''
  {}
  
  {}
  
  For a total of {} generated maps.
''')

def show(count):
  categories=sorted(generate.categories,key=lambda x:len(x.maps),reverse=True)
  tiers='\n'.join(f'- {len(c.maps)} {c.category}' for c in categories)
  tiers=TIERS.format(len(generate.tiers),tiers)
  goals=goal.categories
  rewards=[]
  for g in goals:
    ntypes=len(g)
    types=''
    if ntypes==1:
      ntypes=''
    else:
      types=', '.join(goaltype.name for goaltype in g)
      types=f'({types})'
      ntypes-=1
    rewards.append(f'- {ntypes} {g[0].name} {types}'.strip().replace('  ',' '))
  rewards=REWARDS.format(len(goals),'\n'.join(rewards))
  print(SUMMARY.format(tiers.strip(),rewards.strip(),f'{count:,}').strip())
