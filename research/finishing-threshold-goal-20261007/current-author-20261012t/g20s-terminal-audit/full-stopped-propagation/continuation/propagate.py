#!/usr/bin/env python3
"""At most twelve additional simultaneous rounds after the frozen three-round prefix."""
import hashlib
import json
import resource
import signal
import sys
import time
import warnings
from fractions import Fraction as F
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(50,53))
START=time.process_time();HERE=Path(__file__).resolve().parent
CODE=HERE/'instance/research/uniform-capture-20261007'
STATE={'status':'RUNNING','LP_calls':0,'maximum_LP_calls':1104,'rounds':[],
       'no_subdivision':True,'no_fixed_norm_face':True,'old_rigidity_check_called':False}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def save():
    STATE['CPU_seconds']=time.process_time()-START
    dump(HERE/'propagation-receipt.json',STATE)
def stop(signum,frame):
    STATE['status']='STOPPED_AT_CPU_CAP';save();sys.exit(2)
signal.signal(signal.SIGXCPU,stop)
sys.path.insert(0,str(CODE))
import uniform as u
import bridge as b
import root_geometry as g
import rigidity as r

def exact_bound(parsed,bounds,i,sign,weights):
    residual=[F(sign if j==i else 0) for j in range(u.DIMENSION)]
    rhs=F(0)
    for key,value in weights.items():
        index=int(key);weight=F(value)
        assert weight>=0 and 0<=index<len(parsed)
        aa,bb=parsed[index];rhs+=weight*bb
        for j,a in aa:residual[j]-=weight*a
    floor=sum((v*(lo if v>=0 else hi) for v,(lo,hi) in zip(residual,bounds)),F(0))
    return {'weighted_rhs':str(rhs),'residual':{str(j):str(v) for j,v in enumerate(residual) if v},
            'box_residual_floor':str(floor),'bound':str(rhs+floor)}

def run():
    prep=json.loads((HERE/'preparation.json').read_text())
    for item in prep['sources']:assert sha(HERE/item['path'])==item['sha256']
    for name,digest in prep['inputs'].items():assert sha(HERE/'inputs'/name)==digest
    for item in prep['prefix_files']:assert sha(HERE/item['path'])==item['sha256']
    assert sha(HERE/'stop-review-binding.json')==prep['stop_review_binding_sha256']
    stopbinding=json.loads((HERE/'stop-review-binding.json').read_text())
    for item in stopbinding['files']:assert sha(HERE/item['path'])==item['sha256']
    assert stopbinding['accepted'] is True
    cert=json.loads((HERE/'inputs/accepted-six-step-prefix.json').read_text())
    assert len(cert['steps'])==6 and cert['epsilon']=='1/5000'
    original=[tuple(map(F,v)) for v in cert['final_bounds']]
    assert {(i,s) for i in u.CORE for s in (-1,1) if original[i][0 if s<0 else 1]==s}=={(44,-1)}
    bounds=list(original)
    bounds[21]=(max(bounds[21][0],-F(17,50000)),bounds[21][1])
    bounds[25]=(bounds[25][0],min(bounds[25][1],F(1,40)))
    bounds=u.refresh_products(bounds)
    assert sha(HERE/'prefix/PRODUCER_MANIFEST.json')=='a756cea10c4cbc60dd686bb7bc9c10ed83ae4853122f91e77803f3e0a7b58a2a'
    prefix=json.loads((HERE/'prefix/stopped-chain.json').read_text())
    assert len(prefix['rounds'])==3 and prefix['final_core_ratio']=='1'
    bounds=[tuple(map(F,v)) for v in prefix['final_bounds']]
    assert u.refresh_products(bounds)==bounds
    assert bounds[21][0]>=-F(17,50000) and bounds[25][1]<=F(1,40)
    gate=json.loads((HERE/'inputs/full-gate-receipt.json').read_text())
    rootgate=json.loads((HERE/'inputs/accepted-root-gate.json').read_text())
    data=g.geometry(*[b.I(*v) for v in rootgate['root']['intervals']])
    labels=gate['new_labels'];epsilon=F(1,5000)
    extra_a=['0']*u.DIMENSION;extra_a[21]=extra_a[25]='-1'
    extra={'a':extra_a,'b':'-3/125','label':'physical-stop-b-plus-z'}
    objectives=[(i,s) for i in u.CORE+(51,) for s in (-1,1)]
    assert len(objectives)==92 and len(set(objectives))==92
    chain={'schema':'s17-stopped-normalized-propagation-v1','epsilon':str(epsilon),
      'accepted_B6_sha256':sha(HERE/'inputs/accepted-six-step-prefix.json'),
      'accepted_stop_review_sha256':sha(HERE/'inputs/stop-review/manifest.json'),
      'accepted_full_gate_review_sha256':sha(HERE/'inputs/full-gate-review-manifest.json'),
      'initial_bounds':[list(map(str,v)) for v in bounds],'extra_row':extra,
      'prefix_manifest_sha256':sha(HERE/'prefix/PRODUCER_MANIFEST.json'),
      'prefix_chain_sha256':sha(HERE/'prefix/stopped-chain.json'),
      'rounds':[],'scope':'Exact normalized necessary enclosures; contraction claim requires final core ratio<1.'}
    dump(HERE/'stopped-chain.json',chain)
    import numpy as np
    import scipy
    from scipy.optimize import linprog
    STATE['runtime']={'numpy':np.__version__,'scipy':scipy.__version__,'native_threads':1,
      'options':{'threads':1,'time_limit':1.0}}
    budget_stop=False
    for iteration in range(4,16):
        rows=r.model(bounds,epsilon,data,labels);assert len(rows)==244
        rows.append(extra);assert len(rows)==245
        parsed=u.parse_exact_rows(rows)
        model_digest=hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()
        rundir=HERE/f'round-{iteration:02d}';rundir.mkdir(exist_ok=True)
        dump(rundir/'model.json',rows)
        incoming=[list(map(str,v)) for v in bounds]
        A=np.array([[float(F(v)) for v in row['a']] for row in rows])
        rhs=np.array([float(F(row['b'])) for row in rows])
        fbounds=[(float(lo),float(hi)) for lo,hi in bounds]
        results=[];updated=list(bounds);calls_before=STATE['LP_calls']
        for i,sign in objectives:
            if time.process_time()-START>=44:budget_stop=True
            weights={};diagnostic={'status':'NOT_PROPOSED_CPU_RESERVE'}
            if not budget_stop:
                c=np.zeros(u.DIMENSION);c[i]=sign
                before=time.process_time();STATE['LP_calls']+=1
                assert STATE['LP_calls']<=1104
                with warnings.catch_warnings(record=True) as caught:
                    warnings.simplefilter('always')
                    fit=linprog(c,A_ub=-A,b_ub=-rhs,bounds=fbounds,method='highs',
                                options={'threads':1,'time_limit':1.0})
                if fit.success:
                    weights={str(k):str(F(round(max(0,-v)*u.WEIGHT_GRID),u.WEIGHT_GRID))
                             for k,v in enumerate(fit.ineqlin.marginals) if -v>1e-12}
                diagnostic={'success':bool(fit.success),'status':int(fit.status),'message':str(fit.message),
                  'floating_objective':None if fit.fun is None else float(fit.fun),
                  'floating_primal':None if fit.x is None else [float(v) for v in fit.x],
                  'primal_scope':'DIAGNOSTIC_RELAXATION_ONLY_NOT_PHYSICAL',
                  'warnings':[str(w.message) for w in caught],
                  'LP_CPU_seconds':time.process_time()-before}
            proof=exact_bound(parsed,bounds,i,sign,weights)
            value=F(proof['bound'])
            assert u.exact_dual(rows,bounds,i,sign,weights,parsed)==value
            result={'coordinate':i,'sign':sign,'weights':weights,**proof,'diagnostic':diagnostic}
            results.append(result)
            dump(rundir/f'objective-{i:02d}-{sign:+d}.json',result)
            lo,hi=updated[i]
            updated[i]=(max(lo,value),hi) if sign==1 else (lo,min(hi,-value))
            if len(results)%8==0:
                STATE['current_round']=iteration;STATE['current_round_objectives']=len(results);save()
        assert len(results)==92 and all(lo<=hi for lo,hi in updated)
        outgoing=u.refresh_products(u.p.outward(updated[:52]))
        ratio=max(max(abs(v) for v in outgoing[i]) for i in u.CORE)
        record={'round':iteration,'incoming_bounds':incoming,'model_kernel_sha256':model_digest,
          'model_file_sha256':sha(rundir/'model.json'),'results':results,
          'final_bounds':[list(map(str,v)) for v in outgoing],
          'core_ratio':str(ratio),'LP_calls':STATE['LP_calls']-calls_before}
        dump(rundir/'round.json',record)
        chain['rounds'].append({'round':iteration,'path':f'round-{iteration:02d}/round.json',
                               'sha256':sha(rundir/'round.json')})
        chain['final_bounds']=record['final_bounds'];chain['final_core_ratio']=str(ratio)
        dump(HERE/'stopped-chain.json',chain)
        STATE['rounds'].append({'round':iteration,'core_ratio':str(ratio),'core_ratio_decimal':float(ratio),
                               'LP_calls':record['LP_calls'],'round_sha256':sha(rundir/'round.json')})
        STATE['final_core_ratio']=str(ratio);STATE['final_core_ratio_decimal']=float(ratio)
        save();print(json.dumps(STATE['rounds'][-1]),flush=True)
        bounds=outgoing
        if ratio<1:
            STATE['status']='STRICT_CONTRACTION_REQUIRES_SEPARATE_INDEPENDENT_EXACT_REVIEW';save();return
        if budget_stop:
            STATE['status']='VALID_PARTIAL_PROPOSAL_ROUND_CPU_STOP';save();return
    STATE['status']='TWELVE_ADDITIONAL_ROUNDS_INCONCLUSIVE'
    STATE['remaining_norm_faces']=[{'coordinate':i,'sign':s} for i in u.CORE for s in (-1,1)
       if bounds[i][0 if s<0 else 1]==s]
    save()

try:run()
except Exception as exc:
    STATE['status']='ERROR';STATE['error']=repr(exc);save();raise
