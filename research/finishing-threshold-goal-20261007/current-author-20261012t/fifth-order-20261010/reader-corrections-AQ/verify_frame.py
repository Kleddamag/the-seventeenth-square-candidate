"""Small read-only frame checks; no tree replay or source generation."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
D=Path(__file__).resolve().parent;W=D.parents[1];load=lambda p:json.loads(Path(p).read_text());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();pin=lambda p:dict(file=str(p),sha256=sha(p))
m=load(W/'second-order-20261010/theorem/THEOREM_MANIFEST.json');ep=W/'second-order-20261010/theorem/EXACT_ENDPOINT_AND_CASES.json';Lhi=F(load(ep)['endpoint']['L_interval'][1]);ref=Path('upper-packing-certificate.json');d=load(ref);R=F(d['side']);eps=F(d['squares'][0]['x'])-F(1,2)
assert eps>0 and eps<F(1,1000000) and R-Lhi-2*eps>0
leftbottom=[(1,0),(5,0),(7,0),(1,1),(2,1),(3,1),(4,1)];righttop=[(2,0),(6,0),(8,0),(17,0),(7,1),(8,1),(15,1)]
for i,j in leftbottom:assert F(d['squares'][i-1]['xy'[j]])==F(1,2)+eps
for i,j in righttop:assert F(d['squares'][i-1]['xy'[j]])==R-F(1,2)-eps
roots=[]
for name,r in m['root_obligations'].items():
 assert sha(r['file'])==r['sha256'];b=load(r['file'])['window']['box']
 for i,j in leftbottom:assert F(b[str(i)][j][0])<=-F(1,1000000)<-eps
 for i,j in righttop:assert F(b[str(i)][j][1])>=0
 roots.append(dict(name=name,file=r['file'],sha256=r['sha256']))
expect=[]
for name in ['G20S','HW']:
 f=Path('research/window-extension-20261008/acceptance')/f'EXPECT_{name}.json';a=load(f);b=a['window'];core=F(b['core'])
 for i,j in leftbottom:
  if i==4:continue
  end=F(b['box'].get(str(i),{}).get(str(j+1),[-core,core])[0]);assert end<=-eps
 assert F(b['box']['2']['1'][1])==0
 expect.append(pin(f))
# HW tube cut by the preserved xi2,1<=0 implies the precise raw finite entry.
f=Path('research/window-extension-20261008/acceptance/EXPECT_HW.json');tube=load(f)['tube']
assert F(tube['core'])<=F(1,200) and F(tube['alpha']['default'])<=F(1,400)
assert list(map(F,tube['box']['2']['1']))==[-F(8,25),F(1,250)]
assert list(map(F,tube['box']['11']['2']))==[-F(1,5),F(1,20)]
assert list(map(F,tube['box']['13']['2']))==[-F(1,5),F(3,40)]
print(json.dumps(dict(status='PASS_FIXED_FRAME_WALL_ENDS_AND_T2_ENTRY',script=pin(__file__),endpoint=pin(ep),reference=pin(ref),eps=str(eps),minimum_right_top_slack=str(R-Lhi-eps),stronger_gap_R_minus_Lhi_minus_2eps=str(R-Lhi-2*eps),roots=roots,windows=expect,scope='Checks fixed reference wall coordinates, root lower/upper ends, physical endpoint margin and T2 entry inclusion. Other target-factor admissions remain the independently reviewed source; no tree arithmetic replay.'),indent=2))
