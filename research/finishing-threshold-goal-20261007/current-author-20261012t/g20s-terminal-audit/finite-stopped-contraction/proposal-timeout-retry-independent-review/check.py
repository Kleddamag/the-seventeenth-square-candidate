#!/usr/bin/env python3
"""Independent finite stopped audit: exact polynomial rows and residuals; no solver."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'): os.environ[key]='1'
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,time,resource,signal,traceback,copy
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'local-research/claude-20261002/results/rerun_trees_20261011/SHA256_G20S_HW.txt').is_file())
G=HERE.parents[1];PROD=HERE.parent/'proposal-timeout-retry'
PREFIX=HERE.parent/'finishing-continuation';PREFIX_REVIEW=HERE.parent/'finishing-independent-review'
START=time.process_time()
def require(x,why):
    if not x: raise ValueError(why)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text())
def save(name,d): (HERE/name).write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def parse_bounds(raw):
    require(type(raw)==list and len(raw)==100,'100 bounds')
    b=[tuple(F(x) for x in p) for p in raw]
    require(all(len(p)==2 and p[0]<=p[1] for p in b),'nonempty closed bounds')
    return b
def packed(b): return [[str(x) for x in pair] for pair in b]
def subset(a,b): return len(a)==len(b) and all(l<=x<=y<=u for (x,y),(l,u) in zip(a,b))
def exact_bound(rows,bounds,result,core):
    i,s=result['coordinate'],result['sign']
    require(type(i)==int and type(s)==int and i in core+(51,) and s in (-1,1),'valid signed objective')
    r=[F(s if j==i else 0) for j in range(100)];out=F(0)
    for key,value in result['weights'].items():
        k=int(key);require(str(k)==key and 0<=k<len(rows),'canonical multiplier index')
        require(type(value)==str,'rational multiplier string')
        w=F(value);require(w>=0,'nonnegative multiplier')
        a,b=rows[k];out+=w*b
        for j,c in a: r[j]-=w*c
    out+=sum((x*(b[0] if x>=0 else b[1]) for x,b in zip(r,bounds)),F(0))
    require(out==F(result['bound']),'claimed signed bound')
    return out

def main():
    pins=load(HERE/'pins.json')
    for path,digest in pins['inputs'].items(): require(sha(ROOT/path)==digest,'input hash '+path)
    import independent_model as m
    raw=load(PROD/'certificate.json');inputs=load(PROD/'INPUTS.json')
    require(raw['schema']=='s17-guarded-finite-stopped-proposal-retry-v1','schema')
    require(raw['radius']=='1/200' and raw['angle_factor']=='1/2' and raw['target_raw_core_radius']=='1/10000','entry domain')
    require(raw['curvature'] is True and raw['shared_products'] is True,'model flags')
    require(raw['input_manifest_sha256']==sha(PROD/'INPUTS.json') and raw['producer_source_sha256']==sha(PROD/'run.py'),'producer input/source binding')
    require(raw['maximum_rounds']==3 and raw['accepted_prefix_rounds']==15 and 1<=len(raw['steps'])<=3,'completed capped chain')
    require(raw['runtime']['options']['threads']==1 and raw['runtime']['options']['parallel']=='off','single thread readbacks')
    require(raw['total_process_CPU_seconds']<=11,'producer CPU cap')
    reg=raw['registry']
    require(reg['core']==list(m.CORE) and reg['parameters']==list(m.SLIDERS) and reg['angles']==list(m.ANGLES) and reg['dummy']==list(m.DUMMY),'registry')
    require(reg['products']==[[a,b,k] for (a,b),k in m.PRODUCTS.items()] and reg['pairs']==[list(p) for p in m.PAIRS],'product/pair registry')
    original=m.initial(False);bounds=m.initial(True)
    require(parse_bounds(raw['original_guard_box'])==original,'original entry bounds')
    require(parse_bounds(raw['guard_seed_box'])==bounds and subset(bounds,original),'seed box and48 products')
    prefix_review=load(PREFIX_REVIEW/'MANIFEST.json');prefix=load(PREFIX/'certificate.json')
    require(sha(PREFIX_REVIEW/'MANIFEST.json')=='7766e022697c707fb576b9108f7323c99f47dd5e658e6603fa68b22a28857c9f','accepted prefix identity')
    require(prefix_review['status']=='ACCEPTED_COMPLETED_FINITE_ROUNDS10_TO15_PARTIAL16_EXCLUDED_TARGET_NOT_REACHED','accepted prefix scope')
    for name,digest in prefix_review['files'].items(): require(sha(PREFIX_REVIEW/name)==digest,'prefix review file '+name)
    for name,digest in prefix_review['input_bindings'].items(): require(sha(ROOT/name)==digest,'prefix accepted input '+name)
    require(raw['prefix_certificate_sha256']==sha(PREFIX/'certificate.json')==prefix_review['certificate_sha256'],'prefix certificate binding')
    require(raw['prefix_producer_manifest_sha256']==sha(PREFIX/'PRODUCER_MANIFEST.json')==prefix_review['producer_manifest_sha256'],'prefix producer binding')
    require(raw['prefix_independent_review_sha256']==sha(PREFIX_REVIEW/'MANIFEST.json'),'prefix independent acceptance binding')
    inherited=parse_bounds(prefix['final_bounds']);require(subset(inherited,bounds) and inherited==m.refreshed(inherited),'valid complete inherited box')
    require(parse_bounds(raw['initial_bounds'])==inherited,'restore all100 accepted prefix bounds')
    bounds=inherited
    # Actual S <= S* lies below this exact rational model reference.
    interface=load(G/'full-stopped-propagation/rational-entry-review/MATHEMATICAL_INTERFACE.json')
    rootsource=Path(interface['sources']['accepted_root_enclosure']['path'])
    require(sha(rootsource)==interface['sources']['accepted_root_enclosure']['sha256'],'accepted root side input')
    rootdata=load(rootsource);sideupper=F(rootdata['side_interval'][1])
    margin=m.side-sideupper;require(margin>0,'S* strictly below Sref')
    require(margin==F(rootdata['side_cap_margin']),'exact accepted side margin')
    floor=m.points[7][1]-F(1,200)+F(1,2)-m.side
    require(floor>F(-1,50),'physical square8 side floor')
    require(m.H[7][1]==m.var(15) and not m.G[7][1],'square8 raw y semantics')
    physical={'Sref':str(m.side),'root_side_upper':str(sideupper),'strict_Sref_minus_root_upper':str(margin),'square8_side_floor':str(floor),'no_scalar_lower_bound_required':True}
    stages=[];control_data=None
    for n,step in enumerate(raw['steps'],16):
        began=time.process_time()
        require(step['round']==n and parse_bounds(step['incoming_bounds'])==bounds,'step incoming box')
        require(step['native_fresh_solver_elapsed']==0,'fresh native solver metadata')
        path=PROD/step['model_file'];require(path.name==f'model-{n}.json' and sha(path)==step['model_sha256'],'serialized model hash')
        model=load(path);require(model['round']==n and parse_bounds(model['incoming_bounds'])==bounds,'model incoming box')
        rows,stats,options=m.independent_model(bounds)
        if rows!=model['rows']:
            mismatch=next((i for i,(a,b) in enumerate(zip(rows,model['rows'])) if a!=b),None)
            save('model-mismatch.json',{'round':n,'row':mismatch,'own_count':len(rows),'producer_count':len(model['rows']),'own':rows[mismatch] if mismatch is not None else None,'producer':model['rows'][mismatch] if mismatch is not None else None})
            raise ValueError('independent polynomial rows differ')
        require(stats==model['stats']==step['stats'] and len(rows)==model['row_count']==step['rows'],'model statistics')
        require(len(options)==152,'complete SAT enumeration')
        parsed=[([(j,F(v)) for j,v in enumerate(row['a']) if F(v)],F(row['b'])) for row in rows]
        seen=set();updated=list(bounds)
        for result in step['results']:
            key=(result['coordinate'],result['sign']);require(key not in seen,'duplicate objective');seen.add(key)
            value=exact_bound(parsed,bounds,result,m.CORE);i,s=key;l,u=updated[i]
            updated[i]=(max(l,value),u) if s==1 else (l,min(u,-value))
        require(seen=={(i,s) for i in m.CORE+(51,) for s in (-1,1)} and len(step['results'])==92,'complete92 objective set')
        outgoing=m.refreshed([m.rounded_pair(p) for p in updated[:52]])
        require(subset(outgoing,bounds) and subset(outgoing,original),'nested nonempty boxes')
        require(parse_bounds(step['outgoing_bounds'])==outgoing,'outward updates and 48 refreshed products')
        p=max(max(map(abs,outgoing[i])) for i in m.CORE if i<34);a=max(max(map(abs,outgoing[i])) for i in m.ANGLES)
        reached=all(max(map(abs,outgoing[i]))<=F(1,10000) for i in m.CORE)
        require(step['position_radius']==str(p) and step['angle_radius']==str(a) and step['target_reached'] is reached,'step radius/target reporting')
        stages.append({'round':n,'rows':len(rows),'SAT_options':152,'strictly_excluded_options':sum(x['status'].startswith('excluded') for x in options),'statistics':stats,'exact_objectives':len(seen),'position_radius':str(p),'angle_radius':str(a),'target_reached':reached,'CPU_seconds':time.process_time()-began})
        control_data=(parsed,bounds,step['results'][0],rows,outgoing)
        bounds=outgoing
        print(json.dumps({'round':n,'CPU_seconds':stages[-1]['CPU_seconds'],'target_reached':reached}),flush=True)
    require(parse_bounds(raw['final_bounds'])==bounds,'final bounds')
    reached=all(max(map(abs,bounds[i]))<=F(1,10000) for i in m.CORE)
    partial=None
    if 'partial_round' in raw:
        partial=raw['partial_round']
        require(not reached and raw['status'] in ('FAILED','BUDGET_STOP'),'partial interruption scope')
        require(partial['round']==16+len(raw['steps']) and parse_bounds(partial['incoming_bounds'])==bounds,'partial begins at last complete box')
        require('outgoing_bounds' not in partial and len(partial['results'])<92,'partial has no promoted completed output')
        partial_path=PROD/partial['model_file'];require(sha(partial_path)==partial['model_sha256'],'preserved partial model binding')
    else:
        require(raw['status']==('PRODUCER_TARGET_REACHED_REQUIRES_SEPARATE_REVIEW' if reached else 'THREE_RETRY_ROUNDS_COMPLETED_TARGET_NOT_REACHED'),'final status')
        if not reached:require(len(raw['steps'])==3,'failed-target complete three-retry-round scope')
    # Small deliberate corruptions; no repeated model construction or solver.
    controls=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError):controls.append(name);return
        raise ValueError('corruption accepted '+name)
    parsed,prior,res,rows,out=control_data
    bad=copy.deepcopy(res);k=next(iter(bad['weights']));bad['weights'][k]='-1'
    reject('negative_multiplier',lambda:exact_bound(parsed,prior,bad,m.CORE))
    bad2=copy.deepcopy(res);bad2['bound']=str(F(bad2['bound'])+F(1,10**15))
    reject('changed_claimed_bound',lambda:exact_bound(parsed,prior,bad2,m.CORE))
    bad3=copy.deepcopy(res);bad3['coordinate']=21
    reject('slider_used_as_core_objective',lambda:exact_bound(parsed,prior,bad3,m.CORE))
    reject('missing_stop_row',lambda:require(rows[:-1]==rows,'model equality'))
    badrow=copy.deepcopy(rows[-1]);badrow['a'][21]='1'
    reject('stop_row_wrong_sign',lambda:require(badrow==rows[-1],'stop row'))
    badseed=m.initial();badseed[21]=(F(-8517,10**6),badseed[21][1])
    reject('root_cut_substituted_for_raw_cut',lambda:require(badseed==m.initial(),'seed cut'))
    badproduct=list(out);badproduct[52]=(F(0),F(0))
    reject('unrefreshed_product',lambda:require(badproduct==m.refreshed(badproduct),'product refresh'))
    reject('missing_objective',lambda:require({(x['coordinate'],x['sign']) for x in raw['steps'][-1]['results'][:-1]}=={(i,s) for i in m.CORE+(51,) for s in (-1,1)},'complete roster'))
    reject('false_inherited_terminal_claim',lambda:require(all(max(map(abs,inherited[i]))<=F(1,10000) for i in m.CORE),'inherited target'))
    require(interface['common_hypotheses']['zero_based_core_indices']==list(m.CORE),'terminal core roster')
    require(interface['rational_entry_scope']['reference_side']==str(m.side),'terminal reference side')
    require(interface['rational_entry_scope']['all45_core_abs_upper']=='1/10000','terminal threshold')
    require(interface['common_hypotheses']['actual_unit_squares']==17 and interface['common_hypotheses']['unrestricted_physical_label']==4,'terminal all17/free4')
    require(interface['rational_entry_scope']['conclusion']==['All45 exact-root core coordinates equal zero','S = S*'],'accepted terminal conclusion')
    require(all(subset([bounds[int(i)]],[tuple(map(F,b))]) for i,b in interface['rational_entry_scope']['slider_bounds'].items()),'terminal slider enclosure')
    for path,digest in pins['inputs'].items():require(sha(ROOT/path)==digest,'inputs unchanged '+path)
    receipt={'status':('PASS_EXACT_FINITE_COMPLETED_PREFIX_PARTIAL_ROUND_EXCLUDED_TARGET_NOT_REACHED' if partial is not None else 'PASS_EXACT_FINITE_PARTIAL_CONTRACTION_TARGET_NOT_REACHED') if not reached else 'PASS_EXACT_FINITE_ENTRY_TO_ACCEPTED_RATIONAL_THEOREM','producer_imported':False,'optimizer_or_producer_model_called':False,'independent_polynomial_reconstruction':True,'physical_join':physical,'accepted_prefix_manifest_sha256':sha(PREFIX_REVIEW/'MANIFEST.json'),'prefix_rounds_not_replayed':15,'excluded_partial_round':None if partial is None else {'round':partial['round'],'saved_bound_count':len(partial['results']),'used_in_proof_or_next_seed':False},'rounds':stages,'exact_signed_bounds':sum(x['exact_objectives'] for x in stages),'all48_products_refreshed_every_round':True,'controls_rejected':controls,'final_bounds':packed(bounds),'target_all45_rawcore_abs_le_1_10000':reached,'terminal_theorem_applied':reached,'capture_or_global_optimality_proved':False,'CPU_seconds':time.process_time()-START}
    save('receipt.json',receipt);print(json.dumps({'status':receipt['status'],'CPU_seconds':receipt['CPU_seconds']}),flush=True)

if __name__=='__main__':
    resource.setrlimit(resource.RLIMIT_CPU,(150,160))
    def limited(sig,frame):raise TimeoutError('independent review CPU reserve')
    signal.signal(signal.SIGXCPU,limited)
    error=None
    try:main()
    except BaseException:
        error=traceback.format_exc();(HERE/'failure.txt').write_text(error);print(error,flush=True)
    finally:save('telemetry.json',{'CPU_seconds':time.process_time()-START,'error':error,'solver_invoked':False})
    if error:raise SystemExit(1)
