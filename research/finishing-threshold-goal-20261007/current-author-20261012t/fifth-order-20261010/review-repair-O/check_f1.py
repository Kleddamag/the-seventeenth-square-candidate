"""Small exact F1 identities. Does not replay imported charge arithmetic."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,itertools
O=Path(__file__).parent
x=json.loads((O/'LOOSE_IDENTITIES.json').read_text())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def box(slot):
 p=[[F(v) for v in q] for q in slot['centre']['polygon']]
 return (min(q[0] for q in p),max(q[0] for q in p),min(q[1] for q in p),max(q[1] for q in p))
def subset(a,b):return b[0]<=a[0]<=a[1]<=b[1] and b[2]<=a[2]<=a[3]<=b[3]
def apart(a,b):return a[1]<b[0] or b[1]<a[0] or a[3]<b[2] or b[3]<a[2]
lo,hi=map(F,x['physical_centre_box']);assert lo==(F(1169,250)-F(4675531,1000000))/2+F(1,2)
L9=tuple(map(F,['-131/250','4501/5000','24137/10000','29637/10000']))
U=F(1169,250);L17=(U-L9[1],U-L9[0],L9[2],L9[3]);slots=[]
for r in x['rows']:
 assert sha(r['literal']['file'])==r['literal']['sha256']
 for pin in r['accepted_proof']:assert sha(pin['file'])==pin['sha256']
 d=json.loads(Path(r['literal']['file']).read_text());cl=d['classes'];assert d['bound']=='20'
 assert [F(c['threshold']) for c in cl]==[4,0,0]
 assert cl[2]['slots']==[x['AQ']];assert subset(box(x['AQ']),L9)
 raw=box(cl[1]['slots'][0]);b=(max(lo,raw[0]),min(hi,raw[1]),max(lo,raw[2]),min(hi,raw[3]))
 assert b==tuple(map(F,r['physical_clipped_box']))
 assert (b[1]-b[0])**2+(b[3]-b[2])**2==F(r['diameter_squared'])<1
 assert apart(b,box(cl[0]['slots'][0])) and apart(b,L9)
 assert cl[1]['slots'][0]['angle_tan_half']==x['AQ']['angle_tan_half']
 assert (1+F(x['AQ']['angle_tan_half'][1]))**2>2
 if r['role']==17:assert subset(b,L17)
 slots.append(b)
assert all(apart(a,b) for a,b in itertools.combinations(slots,2))
assert sha(x['proof']['file'])==x['proof']['sha256']
print('PASS: literal hashes, accepted-proof pins, AQ containment, three clipped diameters, all pair/marker/L9 separations, L17 identity, all-direction gates')
