#!/usr/bin/env python3
"""Re-evaluate five old weight rounds on new G20S models. No solver."""
import hashlib
import json
import resource
import signal
import sys
import time
from fractions import Fraction as F
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(55,58))
START=time.process_time()
HERE=Path(__file__).resolve().parent
CODE=HERE/'instance/research/uniform-capture-20261007'
STATE={'status':'RUNNING','rounds':[],'no_solver_or_new_weights':True}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def save():
    STATE['cpu_seconds']=time.process_time()-START
    dump(HERE/'reuse-receipt.json',STATE)
def interrupted(signum,frame):
    STATE['status']='STOPPED_AT_CPU_CAP';save();sys.exit(2)
signal.signal(signal.SIGXCPU,interrupted)

sys.path.insert(0,str(CODE))
import uniform as u
import bridge as b
import root_geometry as g
import rigidity as r

def audit_residual(parsed,bounds,i,sign,weights):
    residual=[F(sign if j==i else 0) for j in range(u.DIMENSION)]
    rhs=F(0)
    for key,value in weights.items():
        k=int(key);q=F(value)
        assert q>=0 and 0<=k<len(parsed)
        row_a,row_b=parsed[k];rhs+=q*row_b
        for j,a in row_a:residual[j]-=q*a
    floor=sum((x*(lo if x>=0 else hi) for x,(lo,hi) in zip(residual,bounds)),F(0))
    return rhs+floor,{'weighted_rhs':str(rhs),'residual_box_floor':str(floor),
        'residual':{str(j):str(x) for j,x in enumerate(residual) if x}}

def run():
    prep=json.loads((HERE/'preparation.json').read_text())
    for rec in prep['sources']:
        assert sha(HERE/rec['relative_path'])==rec['sha256']
    for name,digest in prep['inputs'].items():assert sha(HERE/'inputs'/name)==digest
    old=json.loads((HERE/'inputs/old-uniform-rigidity.json').read_text())
    gate=json.loads((HERE/'inputs/full-gate-receipt.json').read_text())
    accepted=json.loads((HERE/'inputs/accepted-root-gate.json').read_text())
    assert gate['status']=='PASS_FULL_ROOT_ANALYTIC_GATE_NO_CONTRACTION_CLAIM'
    root=[b.I(*v) for v in accepted['root']['intervals']]
    data=g.geometry(*root)
    labels=gate['new_labels']
    assert len(labels)==52 and len(set(labels))==52
    assert sorted(labels)==sorted(gate['accepted_labels'])
    epsilon=F(1,5000)
    bounds=r.initial()
    assert {str(w):list(map(str,bounds[w])) for w in u.PARAMETERS}==gate['padded_box']
    STATE['old_certificate_sha256']=sha(HERE/'inputs/old-uniform-rigidity.json')
    STATE['full_gate_receipt_sha256']=sha(HERE/'inputs/full-gate-receipt.json')
    STATE['initial_bounds']=[list(map(str,v)) for v in bounds]
    STATE['epsilon']=str(epsilon)
    certificate={'schema':'s17-uniform-rigidity-v1','epsilon':str(epsilon),'steps':[],'history':[],
      'final_bounds':[list(map(str,v)) for v in bounds]}
    save()
    for step_number,old_step in enumerate(old['steps'],1):
        assert step_number<=5
        before=[list(map(str,v)) for v in bounds]
        rows=r.model(bounds,epsilon,data,labels)
        digest=hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()
        if step_number==1:assert digest==gate['normalized_model_kernel_digest']
        parsed=u.parse_exact_rows(rows)
        updated=list(bounds);results=[];residuals=[];seen=set()
        for rec in old_step['results']:
            # Deliberately read only objective and weights. Ignore old bounds,
            # old model hashes and old final boxes.
            i,sign=rec['coordinate'],rec['sign'];weights=rec['weights']
            assert (i,sign) not in seen
            seen.add((i,sign))
            value=u.exact_dual(rows,bounds,i,sign,weights,parsed)
            duplicate,detail=audit_residual(parsed,bounds,i,sign,weights)
            assert value==duplicate
            results.append({'coordinate':i,'sign':sign,'weights':weights,'bound':str(value)})
            residuals.append({'coordinate':i,'sign':sign,'bound':str(value),**detail})
            lo,hi=updated[i]
            updated[i]=(max(lo,value),hi) if sign==1 else (lo,min(hi,-value))
        assert seen=={(i,s) for i in u.CORE+(51,) for s in (-1,1)}
        assert all(lo<=hi for lo,hi in updated)
        bounds=u.refresh_products(u.p.outward(updated[:52]))
        ratio=max(max(abs(x) for x in bounds[i]) for i in u.CORE)
        certificate['steps'].append({'model_sha256':digest,'results':results})
        certificate['history'].append({'round':step_number,'ratio':float(ratio)})
        certificate['final_bounds']=[list(map(str,v)) for v in bounds]
        dump(HERE/'reuse-candidate.json',certificate)
        name=f'round-{step_number:02d}-residuals.json'
        dump(HERE/name,{'step':step_number,'bounds_before':before,'model_sha256':digest,'results':residuals,
                        'bounds_after':certificate['final_bounds'],'ratio':str(ratio)})
        worst=[{'coordinate':i,'bounds':list(map(str,bounds[i]))} for i in u.CORE if max(abs(x) for x in bounds[i])==ratio]
        STATE['rounds'].append({'round':step_number,'ratio':str(ratio),'ratio_decimal':float(ratio),
          'worst_coordinates':worst,'model_sha256':digest,'residual_receipt_sha256':sha(HERE/name),
          'cumulative_cpu_seconds':time.process_time()-START})
        save()
        print(json.dumps(STATE['rounds'][-1]),flush=True)
        if ratio<1:
            break
    STATE['final_ratio']=str(ratio)
    STATE['candidate_sha256']=sha(HERE/'reuse-candidate.json')
    if ratio>=1:
        STATE['status']='OLD_WEIGHTS_INCONCLUSIVE_NO_STRICT_CONTRACTION'
        STATE['meaning']='Only these reused weights are inconclusive; no feasible counterexample or failure of fresh G20S contraction follows.'
        save();return
    path=CODE/'uniform-rigidity.json'
    path.write_bytes((HERE/'reuse-candidate.json').read_bytes())
    STATE['status']='STRICT_REUSE_BOUND_PENDING_UNCHANGED_REPLAY';save()
    if time.process_time()-START>=35:
        STATE['replay']='NOT_STARTED_TO_PRESERVE_CPU_CAP';save();return
    replay_start=time.process_time()
    checked=r.check(path)
    dump(HERE/'unchanged-rigidity-replay.json',checked)
    STATE['replay_cpu_seconds']=time.process_time()-replay_start
    STATE['replay_receipt_sha256']=sha(HERE/'unchanged-rigidity-replay.json')
    STATE['status']='PASS_STRICT_REUSE_AND_UNCHANGED_RIGIDITY_REPLAY'
    STATE['scope']='All-scale exact-root rigidity only; no finite-entry or broad-capture theorem.'
    save()

try:run()
except Exception as exc:
    STATE['status']='ERROR';STATE['error']=repr(exc);save();raise
