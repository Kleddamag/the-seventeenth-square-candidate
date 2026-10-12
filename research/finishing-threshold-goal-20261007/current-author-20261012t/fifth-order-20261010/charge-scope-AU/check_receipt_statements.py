"""Small read-only inventory of merged class statements and literal frame data.

Does not rerun arithmetic, authenticate a previously unaudited execution, or
replace individually approved class aliases. Prints JSON; never edits evidence.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,re
R=Path('local-research/claude-20261002/results')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pin=lambda p:dict(file=str(p),sha256=sha(p))
load=lambda p:json.loads(p.read_text())
C=F(4675531,1000000);center=[F(1169,500)]*2
pattern=r'square of side ([0-9/]+), read in the frame with the container centre at \(([^,]+), ([^)]+)\)'
paths=sorted(set(R.glob('*/exact/receipt_python.json'))|set(R.glob('*/receipt_python.json')))
rows=[];not_complete=[];no_pair=[]
for pp in paths:
 p=load(pp)
 if p.get('status')!='PASS_CLASSES_EXACT_COVER':not_complete.append(str(pp));continue
 np=pp.with_name('receipt_node.json');cp=pp.with_name('classes.json')
 if not np.exists() or not cp.exists():no_pair.append(str(pp));continue
 n=load(np);cl=load(cp)
 assert n['status']=='PASS_CLASSES_EXACT_COVER'
 for key in ['schema','symmetry','bound','classes','total_intervals','required_units','budget_units','surplus','certificate_sha256','classes_sha256']:
  assert p[key]==n[key],(str(pp),key)
 for x in [p,n]:
  match=re.search(pattern,x.get('statement',''));assert match,(str(pp),'missing side/frame in statement')
  side,cx,cy=map(F,match.groups());assert side==C and [cx,cy]==center,(str(pp),'wrong cap/frame')
  assert x['classes_sha256']==sha(cp)
  assert F(x['bound'])*int(x['required_units'])-int(x['budget_units'])==F(x['surplus'])>0
 assert list(map(F,cl['frame']['center']))==center
 assert cl['symmetry']==p['symmetry'] and F(cl['bound'])==F(p['bound'])
 rows.append(dict(python=pin(pp),node=pin(np),literal_checked=pin(cp),certificate_sha256=p['certificate_sha256'],side='4675531/1000000',frame_center=['1169/500','1169/500'],symmetry=p['symmetry'],bound=p['bound'],surplus=p['surplus']))
print(json.dumps(dict(status='PASS_LITERAL_SIDE_FRAME_AND_STRICT_SURPLUS_INVENTORY_ONLY',rows=rows,count=len(rows),not_complete=not_complete,no_local_pair=no_pair,script=pin(Path(__file__)),scope='All complete paired merged class receipts found at results/*/exact or results/*, including reserves. Literal classes and both statement strings checked. No extra alias acceptance, provenance acceptance, row arithmetic, or selected-proof completeness inferred.'),indent=2))
