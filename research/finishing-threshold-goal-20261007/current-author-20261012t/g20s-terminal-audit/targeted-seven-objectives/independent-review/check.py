#!/usr/bin/env python3
"""Independent exact review of one global B5 targeted round; no LP calls."""
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

resource.setrlimit(resource.RLIMIT_CPU, (15, 18))
START=time.process_time()
HERE=Path(__file__).resolve().parent
PROD=HERE.parent/'producer'
GATE=HERE.parents[1]/'full-gate'
CORE=tuple(i for i in range(51) if i not in (2,6,7,21,25,37))
OBJECTIVES={(i,s) for i in CORE+(51,) for s in (-1,1)}
TARGETS={(8,-1),(14,1),(15,1),(41,1),(41,-1),(44,1),(49,1)}
PRODUCTS=list(itertools.product((2,21,25),[i for i in range(34,51) if i!=37]))
GRID=10**15

class NoSolver(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0] in ('numpy','scipy','sympy'):
            raise RuntimeError('No numerical proposal or symbolic replay permitted')
sys.meta_path.insert(0,NoSolver())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def stringify(box):return [list(map(str,v)) for v in box]
def roster(records):
    keys=[(v['coordinate'],v['sign']) for v in records]
    assert len(keys)==len(set(keys))==92 and set(keys)==OBJECTIVES
def residual_bound(rows,box,obj,weights):
    assert obj in OBJECTIVES
    sparse={}
    rhs=F(0)
    for k,q in weights.items():
        assert str(int(k))==k and 0<=int(k)<len(rows) and F(q)>=0
        coeff,const=rows[int(k)];q=F(q);rhs+=q*const
        for j,a in coeff.items():sparse[j]=sparse.get(j,F(0))+q*a
    i,s=obj
    residual={j:(F(s) if j==i else F(0))-sparse.get(j,F(0)) for j in set(sparse)|{i}}
    residual={j:v for j,v in residual.items() if v}
    correction=sum((min(v*box[j][0],v*box[j][1]) for j,v in residual.items()),F(0))
    return rhs+correction,rhs,correction,residual
def validate(rows,box,record,detail):
    value,rhs,correction,residual=residual_bound(rows,box,(record['coordinate'],record['sign']),record['weights'])
    assert value==F(record['bound'])==F(detail['bound'])
    assert rhs==F(detail['weighted_rhs']) and correction==F(detail['box_residual_floor'])
    assert residual=={int(k):F(v) for k,v in detail['residual'].items()}
    return value

manifest=load(PROD/'PRODUCER_MANIFEST.json')
manifest_hash=sha(PROD/'PRODUCER_MANIFEST.json')
assert manifest_hash==sys.argv[1]
for name,digest in manifest['files_sha256'].items():assert sha(PROD/name)==digest
prep=load(PROD/'preparation.json')
for item in prep['sources']:
    assert sha(PROD/item['path'])==item['sha256']
    assert (PROD/item['path']).read_bytes()==(GATE/'producer'/item['path']).read_bytes()
for name,digest in prep['inputs'].items():assert sha(PROD/'inputs'/name)==digest
assert sha(PROD/'inputs/accepted-prefix-review-manifest.json')=='7d9db75869c3bc781ca3a08e892dd12d4c3e5f5140fae3f0577ff32ddee2a901'
assert sha(PROD/'inputs/accepted-prefix.json')=='b79e7c9aced0b15a8abb470d70624b9f683771633220f22fd7702e084322ed80'
assert sha(PROD/'inputs/full-gate-review-manifest.json')=='a70b064bb81a55fca7f5ad9a9b19ea765c613877d8b243e041081760b9dc53dd'
assert sha(PROD/'inputs/seven-face-review-manifest.json')=='d98a4956589f65ff6fab859e12d9aeda6db27d04b1037625423f82863f633a60'
prefix=load(PROD/'inputs/accepted-prefix.json')
candidate=load(PROD/'six-step-candidate.json')
state=load(PROD/'targeted-receipt.json')
details=load(PROD/'round6-residuals.json')
assert candidate['steps'][:5]==prefix['steps'] and len(candidate['steps'])==6
assert candidate['history'][:5]==prefix['history']
assert candidate['schema']==prefix['schema']=='s17-uniform-rigidity-v1'
assert candidate['epsilon']==prefix['epsilon']=='1/5000'
box=[tuple(map(F,v)) for v in prefix['final_bounds']]
assert len(box)==100 and stringify(box)==state['B5']==details['incoming_B5']
assert sha(PROD/'six-step-candidate.json')==state['candidate_sha256']
assert sha(PROD/'round6-residuals.json')==state['round6_residuals_sha256']

# Reuse accepted model semantics, but rebuild it from the full global B5.
sys.path.insert(0,str(PROD/'instance/research/uniform-capture-20261007'))
import rigidity as kernel
import root_geometry
import bridge
root=[bridge.I(*v) for v in load(PROD/'inputs/accepted-root-gate.json')['root']['intervals']]
gate=load(PROD/'inputs/full-gate-receipt.json')
rows=kernel.model(box,F(1,5000),root_geometry.geometry(*root),gate['new_labels'])
assert len(rows)==244 and all(len(row['a'])==100 for row in rows)
assert rows==load(PROD/'B5-model.json')
assert [row['label'] for row in rows[:52]]==gate['new_labels']
digest=hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()
step=candidate['steps'][5]
assert digest==step['model_sha256']==state['model_sha256']==details['model_sha256']
sparse=[({j:F(a) for j,a in enumerate(row['a']) if F(a)},F(row['b'])) for row in rows]
roster(step['results']);roster(details['results'])
detail_map={(v['coordinate'],v['sign']):v for v in details['results']}
proposals={(v['coordinate'],v['sign']):v for v in state['lp_proposals']}
assert len(state['lp_proposals'])==7 and set(proposals)==TARGETS
assert set(map(tuple,prep['target_objectives']))==TARGETS
updated=list(box)
new_bounds=[]
empty_untargeted=0
for rec in step['results']:
    obj=(rec['coordinate'],rec['sign'])
    value=validate(sparse,box,rec,detail_map[obj])
    if obj in TARGETS:
        proposal=proposals[obj]
        assert rec['weights']==proposal['weights'] and value==F(proposal['exact_bound'])
        assert (value>-1)==proposal['strictly_above_minus_one']
        new_bounds.append({'coordinate':obj[0],'sign':obj[1],'bound':str(value),
                           'strictly_above_minus_one':value>-1,'nonzero_weights':len(rec['weights'])})
    else:
        assert rec['weights']=={}
        assert value==min(obj[1]*v for v in box[obj[0]])
        empty_untargeted+=1
    i,s=obj;lo,hi=updated[i]
    updated[i]=(max(lo,value),hi) if s==1 else (lo,min(hi,-value))
assert empty_untargeted==85
assert all(lo<=hi for lo,hi in updated)
base=[(F((lo*GRID)//1,GRID),F(-((-hi*GRID)//1),GRID)) for lo,hi in updated[:52]]
assert all(rl<=lo<=hi<=rh for (lo,hi),(rl,rh) in zip(updated[:52],base))
final=list(base)
for w,a in PRODUCTS:
    vals=[x*y for x in base[w] for y in base[a]]
    final.append((min(vals),max(vals)))
assert stringify(final)==candidate['final_bounds']==details['final_bounds']
assert all(-1<=final[i][0]<=final[i][1]<=1 for i in CORE)
faces=[(i,s) for i in CORE for s in (-1,1) if F(s) in final[i]]
assert faces==[(44,-1)]
ratio=max(abs(v) for i in CORE for v in final[i])
assert ratio==F(state['final_ratio'])==F(details['ratio'])==1
other_max=max(abs(v) for i in CORE if i!=44 for v in final[i])
assert other_max<1
assert sum(v['strictly_above_minus_one'] for v in new_bounds)==6
assert state['status']=='ONE_TARGETED_ROUND_INCONCLUSIVE'
assert not (PROD/'unchanged-rigidity-replay.json').exists()

controls=[]
def rejected(name,fn):
    try:fn()
    except (AssertionError,ValueError):controls.append({'name':name,'status':'REJECTED'})
    else:raise AssertionError('Control failed: '+name)
target=next(rec for rec in step['results'] if (rec['coordinate'],rec['sign'])==(8,-1))
bad=copy.deepcopy(target);bad['bound']=str(F(bad['bound'])+F(1,10**12))
rejected('changed exact target bound',lambda:validate(sparse,box,bad,detail_map[(8,-1)]))
bad=copy.deepcopy(target);bad['weights']['0']='-1'
rejected('negative target multiplier',lambda:residual_bound(sparse,box,(8,-1),bad['weights']))
rejected('missing empty-weight objective',lambda:roster(step['results'][:-1]))
assert all(v['bound']=='-1' for v in new_bounds if v['coordinate']==44 and v['sign']==1)
assert not any(m in sys.modules for m in ('numpy','scipy','sympy'))
out={'status':'ACCEPTED_SIX_NORM_FACES_ELIMINATED_ONE_REMAINS',
     'producer_manifest_sha256':manifest_hash,'accepted_prefix_review_sha256':sha(PROD/'inputs/accepted-prefix-review-manifest.json'),
     'first_five_rounds_inherited_not_replayed':True,'global_B5_model_digest':digest,
     'all_92_exact_bounds_recomputed':True,'untargeted_empty_objectives':empty_untargeted,
     'target_bounds':new_bounds,'final_remaining_faces':[[i,str(s)] for i,s in faces],
     'max_other_44_core_radius':str(other_max),'square11_angle_upper':str(final[44][1]),
     'final_ratio':str(ratio),'final_box':stringify(final),'controls':controls,
     'no_solver_symbolic_or_full_rigidity_check_run_by_reviewer':True,
     'scope':'Global necessary B5 bounds, six closed norm faces eliminated; sole possible nonzero norm face x44=-1. No rigidity or primal feasibility claim.',
     'cpu_seconds':time.process_time()-START}
(HERE/'receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ('status','max_other_44_core_radius','cpu_seconds')}))
