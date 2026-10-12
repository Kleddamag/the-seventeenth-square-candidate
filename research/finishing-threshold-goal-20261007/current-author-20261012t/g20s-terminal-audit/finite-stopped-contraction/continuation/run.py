#!/usr/bin/env python3
"""At most six continuation rounds from the accepted three-round finite prefix."""
import os
THREAD_KEYS=('OMP_NUM_THREADS','OMP_THREAD_LIMIT','OPENBLAS_NUM_THREADS',
 'MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','RAYON_NUM_THREADS')
for key in THREAD_KEYS: os.environ[key]='1'
import hashlib, importlib.util, json, resource, signal, sys, time, traceback
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'local-research/claude-20261002/results/rerun_trees_20261011/SHA256_G20S_HW.txt').is_file())
G=HERE.parents[1]
RADIUS=F(1,200)
TARGET=F(1,10000)
STATE={'schema':'s17-guarded-finite-stopped-continuation-v1',
 'status':'PREPARING','steps':[],'maximum_rounds':6,'accepted_prefix_rounds':3,'producer_total_CPU_cap_seconds':30,
 'run_hard_CPU_seconds':29,'run_soft_CPU_seconds':27,
 'preparation_CPU_reserve_seconds':1,'target_raw_core_radius':str(TARGET),
 'physical_scope':'17 actual squares; free4; common frame/injective labels; actual S<=S*',
 'radius':str(RADIUS),'angle_factor':'1/2','curvature':True,'shared_products':True}

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path,data):
    tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n'); tmp.replace(path)
def packed(bounds): return [[str(lo),str(hi)] for lo,hi in bounds]
def within(inner,outer):
    return len(inner)==len(outer) and all(a<=x<=y<=b for (x,y),(a,b) in zip(inner,outer))
def remaining(): return 27-time.process_time()
def budget_check():
    if remaining()<2: raise TimeoutError('CPU reserve reached; no further proposal')
def limited(sig,frame): raise TimeoutError('CPU soft limit reached')

def native():
    import numpy as np
    import scipy
    from scipy.optimize._highspy import _core as h
    solver=h._Highs()
    opts={'output_flag':False,'threads':1,'parallel':'off','solver':'simplex',
      'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9}
    readback={}
    for key,value in opts.items():
        if solver.setOptionValue(key,value)!=h.HighsStatus.kOk: raise ValueError('native option rejected')
        status,read=solver.getOptionValue(key)
        if status!=h.HighsStatus.kOk or read!=value: raise ValueError('native option readback mismatch')
        readback[key]=read
    return np,h,solver,{'numpy':np.__version__,'scipy':scipy.__version__,
      'options':readback,'environment':{k:os.environ[k] for k in THREAD_KEYS}}

def main():
    if sys.argv[1:]!=['--run']: raise ValueError('explicit --run required')
    output=HERE/'certificate.json'
    if output.exists(): raise ValueError('refusing to replace certificate')
    pins=json.loads((HERE/'INPUTS.json').read_text())
    for rel,digest in pins['files'].items():
        if sha(ROOT/rel)!=digest: raise ValueError('source/input mismatch '+rel)
    STATE['input_manifest_sha256']=sha(HERE/'INPUTS.json')
    STATE['producer_source_sha256']=sha(Path(__file__))
    path=ROOT/pins['uniform_path']
    spec=importlib.util.spec_from_file_location('finite_uniform',path)
    u=importlib.util.module_from_spec(spec);spec.loader.exec_module(u)
    assert u.DIMENSION==100 and len(u.CORE)==45 and len(u.PRODUCTS)==48 and len(u.PAIRS)==19
    STATE['registry']={'core':list(u.CORE),'parameters':list(u.PARAMETERS),
      'angles':list(u.ANGLES),'dummy':list(u.DUMMY),
      'products':[[w,a,k] for (w,a),k in u.PRODUCTS.items()],'pairs':u.PAIRS}
    original=u.initial_bounds(RADIUS,F(1,2)); bounds=list(original)
    bounds[21]=(F(-213,25000),bounds[21][1]);bounds[25]=(bounds[25][0],F(33,1000))
    bounds=u.refresh_products(bounds)
    assert within(bounds,original)
    STATE['original_guard_box']=packed(original);STATE['initial_bounds']=packed(bounds)
    # This side floor follows from the top wall at physical8, without a scalar lower bound.
    side,points,axes,corners,H,Gg=u.geometry()
    side_floor=points[7][1]-RADIUS+F(1,2)-side
    assert H[7][1][15]==1 and all(x==0 for j,x in enumerate(H[7][1]) if j!=15)
    assert all(x==0 for x in Gg[7][1]) and side_floor>F(-1,50)
    STATE['side_floor_lemma']={'physical_label':8,'reference_y':str(points[7][1]),
      'Sref':str(side),'centre_y_core_index':15,'unit_square_vertical_support_lower':'1/2',
      'proved_delta_lower':str(side_floor),'model_delta_lower':'-1/50',
      'reason':'top containment; every unit square has vertical half support at least1/2'}
    prefix_path=ROOT/pins['prefix_certificate']
    prefix=json.loads(prefix_path.read_text())
    review=json.loads((ROOT/pins['prefix_review']).read_text())
    assert review['status']==pins['prefix_review_status'] and review['status'].startswith('ACCEPTED')
    assert prefix['schema']=='s17-guarded-finite-stopped-three-rounds-v1'
    assert prefix['status']=='THREE_ROUNDS_COMPLETED_TARGET_NOT_REACHED'
    assert len(prefix['steps'])==3 and prefix['steps'][-1]['outgoing_bounds']==prefix['final_bounds']
    expected_registry=json.loads(json.dumps(STATE['registry']))
    assert prefix['registry']==expected_registry
    restored=[tuple(map(F,interval)) for interval in prefix['final_bounds']]
    assert len(restored)==100 and within(restored,bounds)
    assert u.refresh_products(restored)==restored
    STATE['guard_seed_box']=packed(bounds)
    STATE['prefix_certificate_sha256']=sha(prefix_path)
    STATE['prefix_producer_manifest_sha256']=sha(ROOT/pins['prefix_producer_manifest'])
    STATE['prefix_independent_review_sha256']=sha(ROOT/pins['prefix_review'])
    bounds=restored;STATE['initial_bounds']=packed(bounds)
    STATE['status']='RUNNING';save(output,STATE)
    np,h,solver,readback=native();STATE['runtime']=readback
    from scipy.sparse import csc_matrix
    for number in range(4,10):
        budget_check(); started=time.process_time()
        rows,stats=u.model(bounds,True,True)
        extra=u.zero();extra[21]=extra[25]=F(-1)
        rows.append({'a':list(map(str,extra)),'b':'-49/2000','label':'accepted-physical-stop:minus-b-z'})
        parsed=u.parse_exact_rows(rows)
        model_path=HERE/('model-%d.json'%number)
        model={'incoming_bounds':packed(bounds),'rows':rows,'stats':stats,
          'row_count':len(rows),'round':number}
        save(model_path,model)
        active={'round':number,'model_file':model_path.name,'model_sha256':sha(model_path),
          'incoming_bounds':packed(bounds),'rows':len(rows),'stats':stats,'results':[]}
        STATE['partial_round']=active;save(output,STATE)
        rr=[];cc=[];dd=[]
        for k,(entries,rhs) in enumerate(parsed):
            for j,x in entries: rr.append(k);cc.append(j);dd.append(float(x))
        matrix=csc_matrix((dd,(rr,cc)),shape=(len(rows),100))
        lp=h.HighsLp();lp.num_col_=100;lp.num_row_=len(rows)
        lp.col_cost_=np.zeros(100)
        lp.col_lower_=np.array([float(lo/RADIUS) for lo,hi in bounds])
        lp.col_upper_=np.array([float(hi/RADIUS) for lo,hi in bounds])
        lp.row_lower_=np.array([float(rhs/RADIUS) for entries,rhs in parsed])
        lp.row_upper_=np.full(len(rows),np.inf)
        lp.a_matrix_.num_col_=100;lp.a_matrix_.num_row_=len(rows)
        lp.a_matrix_.format_=h.MatrixFormat.kColwise
        lp.a_matrix_.start_=matrix.indptr.astype(np.int32)
        lp.a_matrix_.index_=matrix.indices.astype(np.int32);lp.a_matrix_.value_=matrix.data
        if solver.passModel(lp)!=h.HighsStatus.kOk: raise ValueError('native model rejected')
        indices=np.arange(100,dtype=np.int32); updated=list(bounds)
        for coordinate in u.CORE+(51,):
            for sign in (1,-1):
                budget_check()
                solver.setOptionValue('time_limit',min(1.0,max(.01,remaining()-2)))
                cost=np.zeros(100);cost[coordinate]=sign
                if solver.changeColsCost(100,indices,cost)!=h.HighsStatus.kOk: raise ValueError('cost rejected')
                if solver.run()!=h.HighsStatus.kOk or solver.getModelStatus()!=h.HighsModelStatus.kOptimal:
                    raise RuntimeError('native proposal not optimal: '+solver.modelStatusToString(solver.getModelStatus()))
                solution=solver.getSolution()
                weights={str(k):str(F(round(max(0,float(v))*u.WEIGHT_GRID),u.WEIGHT_GRID))
                  for k,v in enumerate(solution.row_dual) if v>1e-12}
                bound=u.exact_dual(rows,bounds,coordinate,sign,weights,parsed)
                active['results'].append({'coordinate':coordinate,'sign':sign,
                  'weights':weights,'bound':str(bound)})
                lo,hi=updated[coordinate]
                updated[coordinate]=(max(lo,bound),hi) if sign==1 else (lo,min(hi,-bound))
        new=u.refresh_products(u.p.outward(updated[:52]))
        assert within(new,bounds) and within(new,original)
        active['outgoing_bounds']=packed(new)
        active['CPU_seconds']=time.process_time()-started
        active['position_radius']=str(max(max(map(abs,new[i])) for i in u.CORE if i<34))
        active['angle_radius']=str(max(max(map(abs,new[i])) for i in u.ANGLES))
        active['target_reached']=all(max(map(abs,new[i]))<=TARGET for i in u.CORE)
        assert len(active['results'])==92
        STATE['steps'].append(active);del STATE['partial_round'];bounds=new
        STATE['final_bounds']=packed(bounds);STATE['total_process_CPU_seconds']=time.process_time()
        save(output,STATE)
        print(json.dumps({k:active[k] for k in ('round','rows','stats','CPU_seconds','position_radius','angle_radius','target_reached')}),flush=True)
        if active['target_reached']: break
    for rel,digest in pins['files'].items():
        if sha(ROOT/rel)!=digest: raise ValueError('input changed during run '+rel)
    STATE['status']='PRODUCER_TARGET_REACHED_REQUIRES_SEPARATE_REVIEW' if STATE['steps'][-1]['target_reached'] else 'SIX_FURTHER_ROUNDS_COMPLETED_TARGET_NOT_REACHED'
    save(output,STATE)

if __name__=='__main__':
    if (HERE/'certificate.json').exists():
        raise SystemExit('refusing to replace an existing run, including failure telemetry')
    wall=time.time();resource.setrlimit(resource.RLIMIT_CPU,(27,29));signal.signal(signal.SIGXCPU,limited)
    error=None
    try: main()
    except BaseException as exc:
        error=traceback.format_exc();STATE['status']='BUDGET_STOP' if isinstance(exc,TimeoutError) else 'FAILED'
        STATE['error']=error
    finally:
        STATE['total_process_CPU_seconds']=time.process_time()
        STATE['wall_seconds']=time.time()-wall
        STATE['runtime_executable']=sys.executable;STATE['runtime_python']=sys.version
        save(HERE/'certificate.json',STATE)
        save(HERE/'telemetry.json',{'status':STATE['status'],'CPU_seconds':time.process_time(),
          'wall_seconds':time.time()-wall,'source_sha256':sha(Path(__file__)),
          'completed_rounds':len(STATE['steps']),'error':error})
    if error: print(error,file=sys.stderr);sys.exit(1)
