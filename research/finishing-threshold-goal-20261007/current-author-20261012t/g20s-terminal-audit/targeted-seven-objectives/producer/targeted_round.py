#!/usr/bin/env python3
"""At most seven HiGHS proposals on one global B5 model, exact residual proof."""
import hashlib
import json
import resource
import signal
import sys
import time
import warnings
from fractions import Fraction as F
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(27,29))
START=time.process_time()
HERE=Path(__file__).resolve().parent
CODE=HERE/'instance/research/uniform-capture-20261007'
STATE={'status':'RUNNING','lp_proposals':[],'maximum_lp_proposals':7,'one_global_B5_model':True}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def save():
    STATE['cpu_seconds']=time.process_time()-START
    dump(HERE/'targeted-receipt.json',STATE)
def stop(signum,frame):
    STATE['status']='STOPPED_AT_CPU_CAP';save();sys.exit(2)
signal.signal(signal.SIGXCPU,stop)
sys.path.insert(0,str(CODE))
import uniform as u
import bridge as b
import root_geometry as g
import rigidity as r

def residual_bound(parsed,bounds,i,sign,weights):
    residual=[F(sign if k==i else 0) for k in range(u.DIMENSION)]
    rhs=F(0)
    for key,value in weights.items():
        index=int(key);weight=F(value)
        assert weight>=0 and 0<=index<len(parsed)
        aa,bb=parsed[index];rhs+=weight*bb
        for j,a in aa:residual[j]-=weight*a
    correction=sum((v*(lo if v>=0 else hi) for v,(lo,hi) in zip(residual,bounds)),F(0))
    return rhs+correction,{'weighted_rhs':str(rhs),'box_residual_floor':str(correction),
      'residual':{str(j):str(v) for j,v in enumerate(residual) if v}}

def run():
    prep=json.loads((HERE/'preparation.json').read_text())
    for item in prep['sources']:assert sha(HERE/item['path'])==item['sha256']
    for name,digest in prep['inputs'].items():assert sha(HERE/'inputs'/name)==digest
    cert=json.loads((HERE/'inputs/accepted-prefix.json').read_text())
    assert len(cert['steps'])==5 and cert['epsilon']=='1/5000'
    bounds=[tuple(map(F,v)) for v in cert['final_bounds']]
    incoming=[[str(lo),str(hi)] for lo,hi in bounds]
    old_gate=json.loads((HERE/'inputs/accepted-root-gate.json').read_text())
    gate=json.loads((HERE/'inputs/full-gate-receipt.json').read_text())
    root=[b.I(*v) for v in old_gate['root']['intervals']]
    data=g.geometry(*root);labels=gate['new_labels'];epsilon=F(1,5000)
    rows=r.model(bounds,epsilon,data,labels);assert len(rows)==244
    parsed=u.parse_exact_rows(rows)
    model_digest=hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()
    dump(HERE/'B5-model.json',rows)
    STATE['model_sha256']=model_digest
    STATE['B5_model_file_sha256']=sha(HERE/'B5-model.json')
    STATE['B5']=incoming
    targets=[tuple(v) for v in prep['target_objectives']]
    assert len(targets)==7 and len(set(targets))==7
    assert {(i,-s) for i,s in targets}=={(i,s) for i in u.CORE for s in (-1,1) if bounds[i][0 if s==-1 else 1]==s}
    save()

    # Only this block imports the numerical proposal engine. No solve is
    # hidden in the inherited exact checker or model code.
    import numpy as np
    import scipy
    from scipy.optimize import linprog
    STATE['runtime']={'numpy':np.__version__,'scipy':scipy.__version__,'method':'highs',
      'native_threads':1,'options':{'threads':1,'time_limit':2.0},
      'float_primal_status':'DIAGNOSTIC_ONLY_NOT_A_PHYSICAL_PACKING'}
    A=np.array([[float(F(v)) for v in row['a']] for row in rows])
    rhs=np.array([float(F(row['b'])) for row in rows])
    floating_bounds=[(float(lo),float(hi)) for lo,hi in bounds]
    proposed={}
    for i,sign in targets:
        if time.process_time()-START>=14:
            STATE['proposal_stop']='CPU_RESERVE_FOR_EXACT_OUTPUT_AND_REPLAY';save();break
        objective=np.zeros(u.DIMENSION);objective[i]=sign
        before=time.process_time()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            fit=linprog(objective,A_ub=-A,b_ub=-rhs,bounds=floating_bounds,method='highs',
                        options={'threads':1,'time_limit':2.0})
        diagnostic={'coordinate':i,'sign':sign,'success':bool(fit.success),'status':int(fit.status),
          'message':str(fit.message),'floating_objective':None if fit.fun is None else float(fit.fun),
          'floating_primal':None if fit.x is None else [float(v) for v in fit.x],
          'primal_scope':'DIAGNOSTIC_RELAXATION_VECTOR_ONLY',
          'iterations':None if getattr(fit,'nit',None) is None else int(fit.nit),
          'cpu_seconds':time.process_time()-before,'warnings':[str(w.message) for w in caught]}
        weights={}
        if fit.success:
            weights={str(k):str(F(round(max(0,-v)*u.WEIGHT_GRID),u.WEIGHT_GRID))
                     for k,v in enumerate(fit.ineqlin.marginals) if -v>1e-12}
        value=u.exact_dual(rows,bounds,i,sign,weights,parsed)
        check,detail=residual_bound(parsed,bounds,i,sign,weights)
        assert check==value
        diagnostic.update({'exact_bound':str(value),'exact_bound_decimal':float(value),
                           'strictly_above_minus_one':value>-1,'weights':weights,**detail})
        proposed[i,sign]=weights
        STATE['lp_proposals'].append(diagnostic)
        assert len(STATE['lp_proposals'])<=7
        save()
        print(json.dumps({k:diagnostic[k] for k in ('coordinate','sign','status','exact_bound_decimal','strictly_above_minus_one','cpu_seconds')}),flush=True)

    # Every objective is evaluated on exactly the same B5/model, and all
    # intersections are simultaneous. Empty weights retain incoming minima.
    updated=list(bounds);results=[];residuals=[]
    for i in u.CORE+(51,):
        for sign in (-1,1):
            weights=proposed.get((i,sign),{})
            value=u.exact_dual(rows,bounds,i,sign,weights,parsed)
            independently,detail=residual_bound(parsed,bounds,i,sign,weights)
            assert independently==value
            results.append({'coordinate':i,'sign':sign,'weights':weights,'bound':str(value)})
            residuals.append({'coordinate':i,'sign':sign,'bound':str(value),**detail})
            lo,hi=updated[i]
            updated[i]=(max(lo,value),hi) if sign==1 else (lo,min(hi,-value))
    assert len(results)==92 and all(lo<=hi for lo,hi in updated)
    final=u.refresh_products(u.p.outward(updated[:52]))
    ratio=max(max(abs(v) for v in final[i]) for i in u.CORE)
    cert['steps'].append({'model_sha256':model_digest,'results':results})
    cert['history'].append({'round':6,'ratio':float(ratio)})
    cert['final_bounds']=[list(map(str,v)) for v in final]
    dump(HERE/'six-step-candidate.json',cert)
    dump(HERE/'round6-residuals.json',{'incoming_B5':incoming,'model_sha256':model_digest,
      'results':residuals,'final_bounds':cert['final_bounds'],'ratio':str(ratio)})
    STATE['final_ratio']=str(ratio)
    STATE['final_ratio_decimal']=float(ratio)
    STATE['candidate_sha256']=sha(HERE/'six-step-candidate.json')
    STATE['round6_residuals_sha256']=sha(HERE/'round6-residuals.json')
    STATE['untargeted_empty_weight_objectives']=85
    STATE['unclosed_targets']=[{'coordinate':rec['coordinate'],'sign':rec['sign'],'bound':rec['exact_bound']}
        for rec in STATE['lp_proposals'] if not rec['strictly_above_minus_one']]
    STATE['status']='ONE_TARGETED_ROUND_INCONCLUSIVE' if ratio>=1 else 'STRICT_BOUND_PENDING_UNCHANGED_REPLAY'
    save()
    if ratio>=1:return
    if time.process_time()-START>=14:
        STATE['replay']='NOT_STARTED_TO_PRESERVE_CPU_CAP';save();return
    certpath=CODE/'uniform-rigidity.json';certpath.write_bytes((HERE/'six-step-candidate.json').read_bytes())
    before=time.process_time()
    checked=r.check(certpath)
    dump(HERE/'unchanged-rigidity-replay.json',checked)
    STATE['replay_cpu_seconds']=time.process_time()-before
    STATE['replay_receipt_sha256']=sha(HERE/'unchanged-rigidity-replay.json')
    STATE['status']='PASS_STRICT_TARGETED_ROUND_AND_UNCHANGED_RIGIDITY_REPLAY'
    STATE['scope']='All-scale exact-root rigidity only, no finite-entry theorem or tree/capture result.'
    save()
    print(json.dumps({k:STATE[k] for k in ('status','final_ratio','final_ratio_decimal','cpu_seconds','replay_cpu_seconds')}),flush=True)

try:run()
except Exception as exc:
    STATE['status']='ERROR';STATE['error']=repr(exc);save();raise
