import generate,goal,textwrap,theme

TIERS=textwrap.dedent('''
  {} tiers generated for:
  {}
''')
REWARDS=textwrap.dedent('''
  {} map reward categories, {} reward types:
  {}
''')
THEMES='{} thematic sets of map modifiers ({}).'
SUMMARY=textwrap.dedent('''
  {}
  
  {}
  
  {}
  
  For a total of {} generated maps.
''')

def show(count):
  categories=sorted(generate.categories,key=lambda x:len(x.maps),reverse=True)
  tiers='\n'.join(f'- {len(c.maps)} {c.category}' for c in categories)
  tiers=TIERS.format(len(generate.tiers),tiers).strip()
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
  rewards=REWARDS.format(len(goals),ngoals,'\n'.join(rewards)).strip()
  themes=', '.join(sorted(t.name.lower() for t in theme.themes))
  themes=THEMES.format(len(theme.themes),themes)
  s=SUMMARY.format(tiers,rewards,themes,f'{count:,}').strip()
  print(s)
  print(s,file=open('summary.txt','w'))
