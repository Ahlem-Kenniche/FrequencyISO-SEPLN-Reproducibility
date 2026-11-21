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
result={}
for lang,fn in [('FR','celebrity_fra.xlsx'),('EN','celebrity_eng.xlsx')]:
 rows=read(fn)[1:];valid=[]
 for r in rows:
  try:
   a=np.array([float(r[k]) for k in ['C','F','E','D','M','N']]);
   if np.isfinite(a).all() and (a>=0).all():valid.append(a)
  except (ValueError,KeyError,TypeError):pass
 mat=np.array(valid);x22=np.column_stack([mat[:,:4],mat[:,4]]);x23=np.column_stack([mat[:,:4],mat[:,5]])
 l22,w22=classify(x22);l23,w23=classify(x23)
 l23f,_=classify_with_weights(x23,w22) if False else (None,None)
 changes=int((l22!=l23).sum());result[lang]={'entries':len(mat),'changes':changes,'labels22':np.bincount(l22,minlength=4)[1:].tolist(),'labels23':np.bincount(l23,minlength=4)[1:].tolist()}
 print(lang,result[lang],flush=True)
rows=read('before_noto.xlsx');result['AR']={'entries':len(rows)-1,'header':rows[0]}
print('AR entries',len(rows)-1,flush=True)
open(str(Path(__file__).resolve().parents[1] / 'verification_results.json'),'w').write(json.dumps(result,indent=2,ensure_ascii=False))
def classify_w(X,w=None):
 m=len(X); sums=X.sum(axis=0);p=np.divide(X,sums,out=np.zeros_like(X),where=sums!=0)
 if w is None:
  log=np.zeros_like(p);np.log(p,out=log,where=p>0)
  e=-(p*log).sum(axis=0)/np.log(m);d=np.where(sums>0,1-e,0);w=d/d.sum()
 score=p@w
 l=np.full(m,3,dtype=np.int8);l[score>score.mean()+score.std()]=1
 rem=score[l!=1];l[(l!=1)&(score>rem.mean()+rem.std()/2)]=2
 return l,w
for lang,fn in [('FR','celebrity_fra.xlsx'),('EN','celebrity_eng.xlsx')]:
 rows=read(fn)[1:];X=np.array([[float(r[k]) for k in ['C','F','E','D','M','N']] for r in rows],float)
 a=np.column_stack((X[:,:4],X[:,4]));b=np.column_stack((X[:,:4],X[:,5]));la,wa=classify_w(a);lb,wb=classify_w(b);lf,_=classify_w(b,wa)
 abl={}
 for i,k in enumerate(['contributors','size','inlinks','external_links','views']):
  l,_=classify_w(np.delete(b,i,axis=1));abl[k]=int((l!=lb).sum())
 print(lang,'frozen count',int((la!=lf).sum()),'frozen-vs-actual 2023',int((lf!=lb).sum()),'ablate 2023',abl,flush=True)
 result[lang]['frozen_transitions']=int((la!=lf).sum());result[lang]['frozen_vs_actual_2023']=int((lf!=lb).sum());result[lang]['ablation_2023']=abl
open(str(Path(__file__).resolve().parents[1] / 'verification_results.json'),'w').write(json.dumps(result,indent=2,ensure_ascii=False))
for lang,fn in [('FR','celebrity_fra.xlsx'),('EN','celebrity_eng.xlsx')]:
 rows=read(fn)[1:];X=np.array([[float(r[k]) for k in ['C','F','E','D','M']] for r in rows],float)
 full,_=classify_w(X);ab={}
 for i,k in enumerate(['contributors','size','inlinks','external_links','views']):
  l,_=classify_w(np.delete(X,i,axis=1));ab[k]=int((l!=full).sum())
 print(lang,'ablate 2022',ab,flush=True)
 result[lang]['ablation_2022']=ab
open(str(Path(__file__).resolve().parents[1] / 'verification_results.json'),'w').write(json.dumps(result,indent=2,ensure_ascii=False))
rows=read('before_noto.xlsx')[1:];X=np.array([[float(r[k]) for k in ['F','G','H','I','J']] for r in rows],float);lv,_=classify_w(X)
ab={}
for i,k in enumerate(['contributors','size','inlinks','external_links','views']):
 l,_=classify_w(np.delete(X,i,axis=1));ab[k]=int((l!=lv).sum())
result['AR']['ablation']=ab
print('AR ablation',ab)
open(str(Path(__file__).resolve().parents[1] / 'verification_results.json'),'w').write(json.dumps(result,indent=2,ensure_ascii=False))
