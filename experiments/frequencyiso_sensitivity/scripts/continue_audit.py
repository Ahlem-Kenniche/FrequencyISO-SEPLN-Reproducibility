import sys,json,time,csv,zipfile,re
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parents[1]
import zipfile,xml.etree.ElementTree as E,numpy as np,json
from pathlib import Path
P=str(Path(__file__).resolve().parents[1] / 'data')+'/'

def read(f):
 z=zipfile.ZipFile(P+f);ss=[]
 if 'xl/sharedStrings.xml' in z.namelist():
  with z.open('xl/sharedStrings.xml') as s:
   for _,el in E.iterparse(s,events=('end',)):
    if el.tag.endswith('}si'):
     ss.append(''.join(t.text or '' for t in el.iter() if t.tag.endswith('}t')));el.clear()
 rows=[]
 with z.open('xl/worksheets/sheet1.xml') as s:
  for _,el in E.iterparse(s,events=('end',)):
   if el.tag.endswith('}row'):
    row={}
    for c in el:
     if not c.tag.endswith('}c'):continue
     col=''.join(x for x in c.attrib['r'] if x.isalpha());v=next((x.text for x in c if x.tag.endswith('}v')),None)
     if c.attrib.get('t')=='s' and v is not None:v=ss[int(v)]
     row[col]=v
    rows.append(row);el.clear()
 return rows

def classify(X):
 m=len(X); sums=X.sum(axis=0);p=np.divide(X,sums,out=np.zeros_like(X),where=sums!=0)
 log=np.zeros_like(p);np.log(p,out=log,where=p>0)
 e=-(p*log).sum(axis=0)/np.log(m);d=np.where(sums>0,1-e,0);w=d/d.sum();s=p@w
 l=np.full(m,3,dtype=np.int8);l[s>s.mean()+s.std()]=1
 remain=s[l!=1];l[(l!=1)&(s>remain.mean()+remain.std()/2)]=2
 return l,w

classify=classify
def leave_one_out(X,block=128):
 n,k=X.shape; old,_=classify(X)
 S=X.sum(axis=0); xlog=np.where(X>0,X*np.log(np.maximum(X,1)),0); Q=xlog.sum(axis=0)
 affecting=0; changed_labels=0; maximum=0; mismatches=[]
 logn=np.log(n-1)
 for start in range(0,n,block):
  ids=np.arange(start,min(start+block,n)); xx=X[ids]; T=S-xx; q=Q-xlog[ids]
  entropy=(np.log(T)-q/T)/logn
  d=1-entropy; w=d/d.sum(axis=1,keepdims=True)
  # Scores [deletions, population] using full cohort; exclude removed diagonal.
  factors=w/T; score=factors@X.T
  score[np.arange(len(ids)),ids]=np.nan
  mu=1/(n-1); std=np.sqrt(np.nansum((score-mu)**2,axis=1)/(n-1))
  is1=score>mu+std[:,None]
  rem=np.where(is1,np.nan,score)
  rem_count=np.sum(~np.isnan(rem),axis=1)
  rem_mean=np.nansum(rem,axis=1)/rem_count
  rem_std=np.sqrt(np.nansum((rem-rem_mean[:,None])**2,axis=1)/rem_count)
  new=np.full(score.shape,3,dtype=np.int8)
  new[is1]=1
  new[(~is1)&(score>rem_mean[:,None]+0.5*rem_std[:,None])]=2
  diff=(new!=old[None,:]);diff[np.arange(len(ids)),ids]=False
  counts=diff.sum(axis=1)
  affecting+=int((counts>0).sum());changed_labels+=int(counts.sum());maximum=max(maximum,int(counts.max()))
  for idx,c in zip(ids,counts):
   if c: mismatches.append((int(idx),int(c)))
 return {'deletions':n,'affecting':affecting,'changed_labels':changed_labels,'max_per_deletion':maximum,'top_deletions':sorted(mismatches,key=lambda t:-t[1])[:10]}

def perturb(X,repeats=200,seed=42):
 rng=np.random.default_rng(seed);original,_=classify(X)
 sums=[]
 for _ in range(repeats):
  Y=X.copy();Y[:,-1]*=rng.uniform(0.9,1.1,size=len(X));new,_=classify(Y)
  sums.append(int((new!=original).sum()))
 return {'protocol':'independent per-entry uniform multipliers in [0.9,1.1], page views only','seed':seed,'repeats':repeats,'mean_changed_pct':round(100*np.mean(sums)/len(X),4),'min_changed_pct':round(100*min(sums)/len(X),4),'max_changed_pct':round(100*max(sums)/len(X),4),'std_changed_pct':round(100*np.std(sums)/len(X),4)}

# archive labels indexed by prolexeme id and year, streaming regex
raw=(HERE.parent.parent/'data'/'database'/'prolexbase_without_derivatives_instances.sql').read_text(encoding='utf8'); out={}
for lang,f in [('FR','celebrity_fra.xlsx'),('EN','celebrity_eng.xlsx')]:
 print('START',lang,flush=True);rows=read(f)[1:];IDs=[int(r['A']) for r in rows];a=np.array([[float(r[k]) for k in ['C','F','E','D','M','N']] for r in rows],float)
 labels=[classify(a[:,[0,1,2,3,j]])[0] for j in [4,5]]
 suffix={'FR':'fra','EN':'eng'}[lang]
 matches=re.findall(r'INSERT INTO `frequency_'+suffix+r'`[^;]*;',raw,re.S)
 mapping={}
 for m in matches:
  for pid,y,l in re.findall(r'\((\d+),\s*(\d+),\s*(\d+|NULL)\)',m):
   if int(y) in (22,23):mapping[(int(pid),int(y))]=int(l) if l!='NULL' else None
 comp={}
 for year,lab in [(22,labels[0]),(23,labels[1])]:
  comparable=[(pid,int(pred),mapping.get((pid,year))) for pid,pred in zip(IDs,lab) if mapping.get((pid,year)) in (1,2,3)]
  diff=[(pid,pred,arch) for pid,pred,arch in comparable if pred!=arch]
  comp[str(year)]={'ids_in_xlsx':len(IDs),'with_archived_ordinal_record':len(comparable),'agree':len(comparable)-len(diff),'disagree':len(diff),'no_archived_record_or_nonordinal':len(IDs)-len(comparable),'examples_disagree':diff[:8]}
 print('SQL',lang,comp,flush=True)
 print('LOO',lang,flush=True);start=time.time();loo=leave_one_out(a[:,[0,1,2,3,4]])
 print('DONE LOO',lang,loo,'seconds',round(time.time()-start,1),flush=True)
 pr=perturb(a[:,[0,1,2,3,4]])
 print('PERTURB',lang,pr,flush=True)
 out[lang]={'archive_match':comp,'leave_one_out':loo,'perturbation':pr}
 (HERE/'audit_results.json').write_text(json.dumps(out,indent=2))

rows=read('before_noto.xlsx')[1:]
X=np.array([[float(r[k]) for k in ['F','G','H','I','J']] for r in rows],float)
loo_ar=leave_one_out(X)
print('LOO AR',loo_ar,flush=True)
out['AR']={'leave_one_out':loo_ar}
(HERE/'audit_results.json').write_text(json.dumps(out,indent=2))
