#!/usr/bin/env python3
"""Seal the single targeted round and exact one-direction corollary."""
import hashlib
import json
import time
from fractions import Fraction as F
from pathlib import Path
t0=time.process_time()
HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((HERE/'targeted-receipt.json').read_text())
c=json.loads((HERE/'six-step-candidate.json').read_text())
prefix=json.loads((HERE/'inputs/accepted-prefix.json').read_text())
assert len(c['steps'])==6 and c['steps'][:5]==prefix['steps']
assert r['status']=='ONE_TARGETED_ROUND_INCONCLUSIVE' and r['final_ratio']=='1'
assert len(r['lp_proposals'])==7
core=[i for i in range(51) if i not in (2,21,25,6,7,37)]
faces=[(i,s) for i in core for s in (-1,1) if F(c['final_bounds'][i][0 if s<0 else 1])==s]
assert faces==[(44,-1)]
rho=max(max(abs(F(v)) for v in c['final_bounds'][i]) for i in core if i!=44)
assert rho==F(378457789018409,500000000000000) and rho<F(757,1000)
reduction={'status':'PRODUCER_CONDITIONAL_ONE_DIRECTION_REDUCTION_REQUIRES_SEPARATE_REVIEW',
 'only_core_norm_face':[[44,-1]],'all_other_core_radius_at_most':str(rho),
 'clean_bound_strictly_less_than':'757/1000',
 'meaning':'If0<R<=1/5000 under accepted normalized physical hypotheses, then h44=-R and everyothercore|hj|<=rhoR.',
 'not_implied':['zero core','physical feasibility of remaining face','finite capture','optimality']}
(HERE/'direction-reduction.json').write_text(json.dumps(reduction,indent=2)+'\n')
manifest={'status':'SIX_FACES_EXCLUDED_ONE_DIRECTION_REMAINS_REQUIRES_SEPARATE_INDEPENDENT_REVIEW',
 'producer':'Codex contributor 06','global_B5_model':True,'LP_proposals':7,'new_exact_objectives':92,
 'strict_target_objectives':6,'unclosed_target':[44,1],'final_ratio':'1',
 'only_norm_face':[44,-1],'other_core_radius':str(rho),'full_rigidity_checker_run':False,
 'no_finite_LP_tree_or_subdivision':True,'producer_cpu_cap_seconds':30,'independent_review_cap_seconds':30,
 'producer_cpu_charged_seconds':3,'cpu_seconds_preparation':json.loads((HERE/'preparation.json').read_text())['cpu_seconds'],
 'cpu_seconds_targeted':r['cpu_seconds'],
 'files_sha256':{str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='PRODUCER_MANIFEST.json'},
 'seal_cpu_seconds':time.process_time()-t0}
(HERE/'PRODUCER_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'manifest_sha256':sha(HERE/'PRODUCER_MANIFEST.json'),'seal_cpu_seconds':time.process_time()-t0}))
