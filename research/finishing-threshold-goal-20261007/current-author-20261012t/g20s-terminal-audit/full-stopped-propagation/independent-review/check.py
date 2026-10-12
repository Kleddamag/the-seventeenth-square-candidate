#!/usr/bin/env python3
"""Independent complete stopped-model propagation audit; no optimization."""
import copy
import hashlib
import importlib.abc
import itertools
import json
from pathlib import Path
import resource
import sys
import time
from fractions import Fraction as F

resource.setrlimit(resource.RLIMIT_CPU,(45,48))
START=time.process_time()
HERE=Path(__file__).resolve().parent
PROD=HERE.parent/'producer'
G=HERE.parents[1]
DIM=100
CORE=tuple(i for i in range(51) if i not in (2,6,7,21,25,37))
OBJECTIVES={(i,s) for i in CORE+(51,) for s in (-1,1)}
PRODUCTS=list(itertools.product((2,21,25),[i for i in range(34,51) if i!=37]))
GRID=10**15
class NoDiscovery(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0] in ('numpy','scipy','sympy'):
            raise RuntimeError('No solver or symbolic replay permitted')
sys.meta_path.insert(0,NoDiscovery())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def strings(box):return [list(map(str,v)) for v in box]
def refresh(base):
    assert len(base)==52
    result=list(base)
    for w,a in PRODUCTS:
        ends=[x*y for x in base[w] for y in base[a]]
        result.append((min(ends),max(ends)))
    assert len(result)==DIM
    return result
def roster(records):
    keys=[(v['coordinate'],v['sign']) for v in records]
    assert len(keys)==len(set(keys))==92 and set(keys)==OBJECTIVES
def exact_bound(rows,box,record):
    i,s=record['coordinate'],record['sign']
    assert (i,s) in OBJECTIVES and len(box)==DIM
    columns={};rhs=F(0)
    for key,value in record['weights'].items():
        assert str(int(key))==key and 0<=int(key)<len(rows) and F(value)>=0
        coeff,const=rows[int(key)];q=F(value);rhs+=q*const
        for j,a in coeff.items():columns[j]=columns.get(j,F(0))+q*a
    residual={j:(F(s) if j==i else F(0))-columns.get(j,F(0)) for j in set(columns)|{i}}
    residual={j:v for j,v in residual.items() if v}
    floor=sum((min(v*box[j][0],v*box[j][1]) for j,v in residual.items()),F(0))
    assert rhs==F(record['weighted_rhs']) and floor==F(record['box_residual_floor'])
    assert residual=={int(j):F(v) for j,v in record['residual'].items()}
    assert rhs+floor==F(record['bound'])
    return rhs+floor
def update(box,records):
    # Derive both sides separately from one shared incoming box.
    lows={r['coordinate']:F(r['bound']) for r in records if r['sign']==1}
    highs={r['coordinate']:-F(r['bound']) for r in records if r['sign']==-1}
    raw=[(max(lo,lows.get(i,lo)),min(hi,highs.get(i,hi))) for i,(lo,hi) in enumerate(box[:52])]
    assert all(lo<=hi for lo,hi in raw)
    rounded=[(F((lo*GRID)//1,GRID),F(-((-hi*GRID)//1),GRID)) for lo,hi in raw]
    assert all(rl<=lo<=hi<=rh for (lo,hi),(rl,rh) in zip(raw,rounded))
    assert all(ol<=nl<=nh<=oh for (ol,oh),(nl,nh) in zip(box[:52],rounded))
    return refresh(rounded)

manifest=load(PROD/'PRODUCER_MANIFEST.json')
assert sha(PROD/'PRODUCER_MANIFEST.json')==sys.argv[1]
if 'files_sha256' in manifest:
    records=[{'path':k,'sha256':v} for k,v in manifest['files_sha256'].items()]
else:records=manifest['files']
assert len({v['path'] for v in records})==len(records)
for rec in records:assert sha(PROD/rec['path'])==rec['sha256']
prep=load(PROD/'preparation.json')
for rec in prep['sources']:
    assert sha(PROD/rec['path'])==rec['sha256']
    assert (PROD/rec['path']).read_bytes()==(G/'full-gate/producer'/rec['path']).read_bytes()
for name,digest in prep['inputs'].items():assert sha(PROD/'inputs'/name)==digest
assert sha(PROD/'stop-review-binding.json')==prep['stop_review_binding_sha256']
stopbinding=load(PROD/'stop-review-binding.json')
assert stopbinding['accepted'] is True
for rec in stopbinding['files']:assert sha(PROD/rec['path'])==rec['sha256']
assert sha(PROD/'inputs/accepted-targeted-review-manifest.json')=='b38fb735a1d3bdd84c662a68b37d7d10e806af71abf82b54c320424da79d1ad1'
assert sha(PROD/'inputs/accepted-six-step-prefix.json')=='9c44e8153a132d74d28a5aca1168ee2b6389560c1406f4738e13bbcdcdbb41b3'
assert sha(PROD/'inputs/full-gate-review-manifest.json')=='a70b064bb81a55fca7f5ad9a9b19ea765c613877d8b243e041081760b9dc53dd'
assert sha(PROD/'inputs/stop-review/manifest.json')=='e8af5453f7e97d18ee2dab652644d797218ce2382fb928b53a8cb151cee7645d'
mapping=G/'stop-coupled-finish/lp-review/PHYSICAL_SCOPE_MANIFEST.json'
assert sha(mapping)=='5a47ab81102b644f67ed4bd51b23f9c026a32141c4c6f284b4c69200aa920f63'
stop=load(PROD/'inputs/stop-review/manifest.json')
assert stop['unscaled_slider_indices']=={'a':2,'b':21,'z':25}
assert stop['epsilon_max']=='1/5000' and stop['claims']['b_plus_z_upper']=='3/125'

prefix=load(PROD/'inputs/accepted-six-step-prefix.json')
assert len(prefix['steps'])==6 and prefix['epsilon']=='1/5000'
B6=[tuple(map(F,v)) for v in prefix['final_bounds']]
assert len(B6)==DIM
base=list(B6[:52])
base[21]=(max(base[21][0],-F(17,50000)),base[21][1])
base[25]=(base[25][0],min(base[25][1],F(1,40)))
box=refresh(base)
assert box[44]==B6[44] and box[44][0]<box[44][1]
assert all(base[i]==B6[i] for i in range(52) if i not in (21,25))
for name,i in stop['unscaled_slider_indices'].items():
    lo,hi=map(F,stop['domain'][name]);assert lo<=box[i][0]<=box[i][1]<=hi
extra={'a':['0']*DIM,'b':'-3/125','label':'physical-stop-b-plus-z'}
extra['a'][21]=extra['a'][25]='-1'
chain=load(PROD/'stopped-chain.json')
state=load(PROD/'propagation-receipt.json')
assert chain['schema']=='s17-stopped-normalized-propagation-v1' and chain['epsilon']=='1/5000'
assert chain['accepted_B6_sha256']==sha(PROD/'inputs/accepted-six-step-prefix.json')
assert chain['accepted_stop_review_sha256']==sha(PROD/'inputs/stop-review/manifest.json')
assert chain['accepted_full_gate_review_sha256']==sha(PROD/'inputs/full-gate-review-manifest.json')
assert chain['initial_bounds']==strings(box) and chain['extra_row']==extra
assert 1<=len(chain['rounds'])<=3 and len(chain['rounds'])==len(state['rounds'])
assert state['no_subdivision'] and state['no_fixed_norm_face'] and not state['old_rigidity_check_called']
assert state['LP_calls']<=276

sys.path.insert(0,str(PROD/'instance/research/uniform-capture-20261007'))
import rigidity as kernel
import root_geometry
import bridge
root=[bridge.I(*v) for v in load(PROD/'inputs/accepted-root-gate.json')['root']['intervals']]
data=root_geometry.geometry(*root)
labels=load(PROD/'inputs/full-gate-receipt.json')['new_labels']
out={'status':'RUNNING','producer_manifest_sha256':sha(PROD/'PRODUCER_MANIFEST.json'),'rounds':[]}
for n,(entry,report) in enumerate(zip(chain['rounds'],state['rounds']),1):
    assert entry['round']==report['round']==n
    assert entry['path']==f'round-{n:02d}/round.json'
    rd=PROD/f'round-{n:02d}'
    assert sha(PROD/entry['path'])==entry['sha256']==report['round_sha256']
    record=load(PROD/entry['path'])
    assert record['round']==n and record['incoming_bounds']==strings(box)
    rows=kernel.model(box,F(1,5000),data,labels)
    assert len(rows)==244 and [r['label'] for r in rows[:52]]==labels
    rows.append(copy.deepcopy(extra))
    assert len(rows)==245 and all(len(r['a'])==DIM for r in rows)
    assert rows==load(rd/'model.json') and sha(rd/'model.json')==record['model_file_sha256']
    digest=hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()
    assert digest==record['model_kernel_sha256']
    sparse=[({j:F(a) for j,a in enumerate(r['a']) if F(a)},F(r['b'])) for r in rows]
    roster(record['results'])
    stop_uses=0
    for result in record['results']:
        i,s=result['coordinate'],result['sign']
        assert load(rd/f'objective-{i:02d}-{s:+d}.json')==result
        exact_bound(sparse,box,result)
        stop_uses+=F(result['weights'].get('244','0'))>0
    outgoing=update(box,record['results'])
    assert strings(outgoing)==record['final_bounds']
    assert all(-1<=outgoing[i][0]<=outgoing[i][1]<=1 for i in CORE)
    ratio=max(abs(v) for i in CORE for v in outgoing[i])
    assert ratio==F(record['core_ratio'])==F(report['core_ratio'])
    faces=[(i,s) for i in CORE for s in (-1,1) if F(s) in outgoing[i]]
    out['rounds'].append({'round':n,'model_digest':digest,'exact_objectives':92,'core_ratio':str(ratio),
        'remaining_norm_faces':[[i,str(s)] for i,s in faces],'objectives_using_stop_row':stop_uses,
        'max_other_than44_radius':str(max(abs(v) for i in CORE if i!=44 for v in outgoing[i])),
        'coordinate44_bounds':list(map(str,outgoing[44]))})
    if ratio<1:assert n==len(chain['rounds'])
    incoming=box;box=outgoing
assert strings(box)==chain['final_bounds']
assert ratio==F(chain['final_core_ratio'])==F(state['final_core_ratio'])
assert sum(v['LP_calls'] for v in state['rounds'])==state['LP_calls']
if ratio<1:
    assert state['status']=='STRICT_CONTRACTION_REQUIRES_SEPARATE_INDEPENDENT_EXACT_REVIEW'
else:
    assert state['status'] in ('THREE_ROUNDS_INCONCLUSIVE','VALID_PARTIAL_PROPOSAL_ROUND_CPU_STOP')
    if state['status']=='THREE_ROUNDS_INCONCLUSIVE':assert len(chain['rounds'])==3

controls=[]
def reject(name,fn):
    try:fn()
    except (AssertionError,ValueError):controls.append({'name':name,'status':'REJECTED'})
    else:raise AssertionError('Control accepted: '+name)
sample=copy.deepcopy(record['results'][0]);sample['bound']=str(F(sample['bound'])+F(1,10**12))
reject('corrupted objective bound',lambda:exact_bound(sparse,incoming,sample))
sample=copy.deepcopy(record['results'][0]);sample['weights']['244']='-1'
reject('negative stop-row weight',lambda:exact_bound(sparse,incoming,sample))
reject('missing signed objective',lambda:roster(record['results'][:-1]))
def stop_row_check(row):assert row==extra
bad=copy.deepcopy(extra);bad['a'][25]='1'
reject('wrong stop-row sign',lambda:stop_row_check(bad))
bad=copy.deepcopy(extra);bad['b']='-3/250'
reject('unproved stronger stop threshold',lambda:stop_row_check(bad))
assert not any(m in sys.modules for m in ('numpy','scipy','sympy'))
out.update(status='ACCEPTED_STRICT_NORMALIZED_STOPPED_CONTRACTION' if ratio<1 else 'ACCEPTED_STOPPED_PROPAGATION_INCONCLUSIVE',
    accepted_B6_review_sha256=sha(PROD/'inputs/accepted-targeted-review-manifest.json'),
    accepted_stop_review_sha256=sha(PROD/'inputs/stop-review/manifest.json'),
    accepted_physical_map_sha256=sha(mapping),
    prefix_inherited_not_replayed=True,full_starting_domain_no_face_restriction=True,
    exact_objectives_verified=92*len(chain['rounds']),final_core_ratio=str(ratio),final_bounds=strings(box),
    controls=controls,solver_symbolic_or_old_rigidity_checker_called=False,cpu_seconds=time.process_time()-START)
(HERE/'receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ('status','exact_objectives_verified','final_core_ratio','rounds','cpu_seconds')}))
