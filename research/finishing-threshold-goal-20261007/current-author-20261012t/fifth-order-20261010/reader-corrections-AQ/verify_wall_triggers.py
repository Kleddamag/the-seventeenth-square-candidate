"""Read-only literal trigger check. All directions are modulo square quarter turns."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
D=Path(__file__).resolve().parent;W=D.parents[1];load=lambda p:json.loads(Path(p).read_text());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();pin=lambda p:dict(file=str(p),sha256=sha(p))
m=load(W/'second-order-20261010/theorem/THEOREM_MANIFEST.json');rho=F(207107,500000);assert rho*rho+2*rho-1>0
rows=[]
for r in m['base_capture_rows']+[m['slab_capture']]:
 name=r.get('name',r.get('id'));q=name.startswith('Q_');pw=name.startswith('PW_')
 if not (q or pw or name=='SL11_T020'):continue
 assert sha(r['file'])==r['sha256'];d=load(r['file']);c=d['classes'][1];assert c['threshold']=='4' and len(c['slots'])==1
 slot=c['slots'][0];assert list(map(F,slot['angle_tan_half']))==[-rho,rho]
 if q:
  k=int(name[2:]);typ='loose_Q' if k in [3,4,15,17] else 'rigid_Q';yl=F(24137,10000);yh=F(13,5) if typ=='loose_Q' else F(129,50)
 elif pw:typ='PW';yl,yh=F(129,50),F(29637,10000)
 else:typ='slab';yl,yh=F(129,50),F(13,5)
 expected=[[F(-131,250),yl],[F(53,100),yl],[F(53,100),yh],[F(-131,250),yh]]
 assert [[F(v) for v in p] for p in slot['centre']['polygon']]==expected
 rows.append(dict(name=name,type=typ,file=r['file'],sha256=r['sha256'],polygon=slot['centre']['polygon'],angle_tan_half=slot['angle_tan_half']))
assert len(rows)==29
print(json.dumps(dict(status='PASS_ALL_29_WALL_TRIGGER_LITERALS',script=pin(__file__),rho=str(rho),quarter_turn_cover_test=str(rho*rho+2*rho-1),rows=rows,scope='Exact trigger geometry and complete orientation cover only. Captured targets, budgets and local admissions are separately imported.'),indent=2))
