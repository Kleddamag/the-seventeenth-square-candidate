"""Read-only exact replay. Prints deterministic JSON; NEVER writes source/output files.
Run from the repository root, optionally redirecting stdout to a NEW result file.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json,hashlib
D=Path(__file__).resolve().parent;V=D.parent;W=V.parent;R=V/'coarse-capacity-R'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
pin=lambda p:dict(file=str(p),sha256=sha(p))
load=lambda p:json.loads(Path(p).read_text())
U=F(1169,250);C=F(4675531,1000000);delta=(U-C)/2
lo,hi=delta+F(1,2),U-delta-F(1,2)
def box(slot):
 p=[[F(v) for v in q] for q in slot['centre']['polygon']]
 assert len(p)==4 and set(map(tuple,p))=={(x,y) for x in {q[0] for q in p} for y in {q[1] for q in p}}
 return min(q[0] for q in p),max(q[0] for q in p),min(q[1] for q in p),max(q[1] for q in p)
def clip(b):return max(lo,b[0]),min(hi,b[1]),max(lo,b[2]),min(hi,b[3])
def subset(a,b):return b[0]<=a[0]<=a[1]<=b[1] and b[2]<=a[2]<=a[3]<=b[3]
coarse={3:tuple(map(F,['129/100','2993/1500','-1/2','1411/1000'])),15:tuple(map(F,['19953/10000','26807/10000','1623/500','26/5'])),17:tuple(map(F,['3775331/1000000','5199531/1000000','24137/10000','29637/10000']))}
L9=tuple(map(F,['-131/250','4501/5000','24137/10000','29637/10000']));L17=(U-L9[1],U-L9[0],L9[2],L9[3])
assert subset(clip(L17),clip(coarse[17]))
assert L17[0]-coarse[17][0]==L17[1]-coarse[17][1]==U-C==F(469,1000000)
c17=clip(coarse[17]);dia=(c17[1]-c17[0])**2+(c17[3]-c17[2])**2
assert dia==F(1851391155161,4000000000000)<1
saved=load(R/'RESULT.json');mins={}
for k in [3,15]:
 w=coarse[k][1]-coarse[k][0];H=coarse[k][3]-delta if k==3 else U-delta-coarse[k][2]
 row=saved['tables'][str(k)];assert w==F(row['w']) and H==F(row['H'])
 p=[1-w,1-2*H,F(4),-1-2*H,1+w];out=[]
 for j in range(128):
  a,h=F(j,128),F(1,128)
  q=[sum(p[n]*comb(n,i)*a**(n-i)*h**i for n in range(i,5)) for i in range(5)]
  b=[sum(q[i]*F(comb(n,i),comb(4,i)) for i in range(n+1)) for n in range(5)]
  assert min(b)>0;out.append(list(map(str,b)))
 assert out==row['bernstein'];mins[str(k)]=str(min(F(x) for r in out for x in r));assert mins[str(k)]==row['least']
JD=Path('research/finishing-threshold-goal-20261007/clean-rerun-20261011/continuation-0340/graph/design');literals=[]
for k in [3,4,15,17]:
 f=JD/'classes'/f'L_L{k:02d}.json';d=load(f);assert d['bound']=='20' and [F(c['threshold']) for c in d['classes']]==[4,0,0]
 aq=box(d['classes'][2]['slots'][0]);assert subset(aq,L9) and aq[1]==F(53,100) and aq[3]==F(13,5)
 sk=clip(box(d['classes'][1]['slots'][0]))
 if k in coarse:assert subset(sk,clip(coarse[k]))
 if k==17:assert subset(sk,clip(L17))
 literals.append(pin(f))
m=load(W/'second-order-20261010/theorem/THEOREM_MANIFEST.json')
cs=[r for r in m['base_capture_rows'] if r['name'].startswith('C_') and r['name'] not in ['C_7','C_8']];assert len(cs)==10
old=load(JD/'classes/C_L01.json');ref=next(c for c in old['classes'] if c['name']=='X_some_loose_label_not_gated_exempt')
geom=lambda c:[(box(s),tuple(map(F,s['angle_tan_half']))) for s in c['slots']]
for r in cs:
 assert sha(r['file'])==r['sha256'];d=load(r['file']);x=next(c for c in d['classes'] if c['name']=='X_some_loose_label_not_gated_exempt')
 assert x['threshold']=='0' and len(x['slots'])==9;g=geom(x)
 assert g[:2]+g[3:]==geom(ref)[:2]+geom(ref)[3:]
 assert g[0]==(L9,(F(0),F(613,2000))) and g[1]==(L9,(-F(5803,14197),F(0)))
 assert g[2]==(aq,(F(613,2000),F(4197,10000)))
 for n,k in enumerate([3,15,17]):
  assert g[3+2*n]==(coarse[k],(F(1,20),F(207107,500000)))
  assert g[4+2*n]==(coarse[k],(-F(207107,500000),-F(1,20)))
 literals.append(dict(name=r['name'],file=r['file'],sha256=r['sha256']))
rho=F(207107,500000);assert rho*rho+2*rho-1>0
f=JD/'classes_v2/PS_L01_T09.json';assert sha(f)=='cf863943c8ad07d46ec51c7211e89c366108e935329a22615ce0c2a11c2ddb7a'
d=load(f);t9=d['classes'][1];assert t9['threshold']=='4' and len(t9['slots'])==1
a,b=map(F,t9['slots'][0]['angle_tan_half']);t=(1+a)/(1-a)
assert (a,b,t)==(F(-408817,1000000),F(61301,200000),F(591183,1408817))
assert b-F(613,2000)==F(1,200000)
assert (1-t)/(1+t)-F(5803,14197)==F(974949,14197000000)
print(json.dumps(dict(status='PASS_EXACT_CAPACITY_CURRENT_ESCAPES_FRAME_INCLUSION_AND_DERIVED_GATE',script=pin(__file__),bridge=pin(D/'PROOF_BRIDGE_V2.md'),proof=pin(R/'PROOF.md'),saved_tables=pin(R/'RESULT.json'),Bernstein_coefficients=1280,minima=mins,coarse17_diameter_squared=str(dia),frame17_subset_coarse17=True,reflection_shift=str(C-U),current_literals=literals,gate_source=pin(f),gate=[str(b),str(t)],old_outputs_unchanged=True,scope='Pure arithmetic/geometry replay only; no charge arithmetic, local trees or new independent acceptance of composition.'),indent=2))
