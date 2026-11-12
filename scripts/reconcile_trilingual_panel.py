import sys, csv, collections
sys.path.insert(0,'/mnt/data/fiso_work/FrequencyISO_SEPLN_Anonymous/scripts')
from audit_trilingual_panel import parse_sql
from pathlib import Path
p=Path(__file__).resolve().parent.parent; a=parse_sql((p/'data/database/prolexbase_without_derivatives_instances.sql').read_text()); langs=('arb','eng','fra')
common=set.intersection(*(set(a[l]) for l in langs)); unique=sorted(pid for pid in common if all(len(a[l][pid])==1 for l in langs))
print('common',len(common),'unique',len(unique),'ambiguous',len(common)-len(unique))
changing=0; at_least2=0; identical=0; ctr={l:collections.Counter() for l in langs}; bypair={l:collections.Counter() for l in langs}
with open(p/'data/recomputed/trilingual_panel_reconciled.csv','w') as f:
 w=csv.writer(f);w.writerow(['pivot','language','prolexeme_id','2019','2020','2021','2022','2023'])
 for pivot in unique:
  v={l:a[l][pivot][0][1] for l in langs}; all_changes=0
  for l in langs:
   pid=a[l][pivot][0][0]; w.writerow([pivot,l,pid,*v[l]])
   for idx,(previous,current) in enumerate(zip(v[l],v[l][1:])):
    if previous!=current:
     direction='higher' if current<previous else 'lower';ctr[l][direction]+=1; bypair[l][(2019+idx,direction)]+=1; all_changes+=1
  changing+=all_changes>0;at_least2+=all_changes>=2; identical+=len(set(v.values()))==1
print('constant',len(unique)-changing,'changing',changing, '>=2',at_least2, 'identical',identical)
for l in langs:print(l,ctr[l],sorted(bypair[l].items()))
