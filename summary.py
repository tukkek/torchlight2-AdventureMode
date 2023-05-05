import generate,goal,textwrap

TIERS=textwrap.dedent('''
  {} tiers generated for:
  {}
''')
REWARDS=textwrap.dedent('''
  {} map reward categories, {} reward types:
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
  for g in sorted(goals,key=lambda k:len(k),reverse=True):
    name=goal.names[goals.index(g)]
    ntypes=len(g)
    entry=f'{name}'
    if ntypes>1:
      types='; '.join(goaltype.name for goaltype in g)
      entry=f'{ntypes} for {name} ({types})'
    rewards.append(f'- {entry}')
  ngoals=sum(len(g) for g in goals)
  rewards=REWARDS.format(len(goals),ngoals,'\n'.join(rewards))
  s=SUMMARY.format(tiers.strip(),rewards.strip(),f'{count:,}').strip()
  print(s)
  print(s,file=open('summary.txt','w'))
