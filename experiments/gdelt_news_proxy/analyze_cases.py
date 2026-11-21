import csv, pathlib
p=pathlib.Path(__file__).with_name('gdelt_case_counts.csv')
r=list(csv.DictReader(p.open(encoding='utf-8')))
t=[x for x in r if x['frequency_direction']!='stable']
match=sum(x['directional_match']=='yes' for x in t)
print(f'Transitions: {len(t)}; matches: {match}; proportion: {match/len(t):.4f}')
for x in r:
 a,b=int(x['sample1_articles_2022']),int(x['sample1_articles_2023'])
 print(x['entity'], f'{a}->{b}', 'undefined' if a==0 else f'{(b-a)/a*100:+.1f}%')
