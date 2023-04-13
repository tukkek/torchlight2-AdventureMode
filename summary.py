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
  tiers='\n'.join(f'- {len(c.maps)} {c.category}' for c in generate.categories)
  tiers=TIERS.format(len(generate.tiers),tiers)
  goals=goal.categories
  rewards='\n'.join(f'- {len(g)-1} {g[0].name}s' for g in goals)
  rewards=REWARDS.format(len(goals),rewards)
  print(SUMMARY.format(tiers.strip(),rewards.strip(),f'{count:,}').strip())
