if __name__ == '__main__' and not globals().get('_S17_PUBLIC_RUNNER_ACTIVE', False):
    raise SystemExit('Use replay_public.py for this check; outputs must be redirected.')
from pathlib import Path
PUBLIC=Path(__file__).resolve().parent.parent
PUBLIC_ROOT=PUBLIC.parents[4]
"""Independent complete geometric SAT gate, no producer code imports/solver."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import ast, hashlib, json, resource, time

resource.setrlimit(resource.RLIMIT_CPU,(6,7))
start=time.process_time()
HERE=PUBLIC;P=PUBLIC_ROOT/'research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/full-gate/producer';BASE=PUBLIC_ROOT/'research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit'
REPO=next(x for x in HERE.parents if (x/'local-research/claude-20261002/results/rerun_trees_20261011/SHA256_G20S_HW.txt').is_file())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
producer_sha='9a7d5d0ee18167ae81c77bcbab31d07b5340d3b3faee1b24f8433162cf72a0af'
assert sha(PUBLIC/'runtime/GATE_PREPARATION.json')==producer_sha
prep=load(PUBLIC/'runtime/GATE_PREPARATION.json');rec=load(P/'gate-receipt.json')
assert rec['status']=='PASS_FULL_ROOT_ANALYTIC_GATE_NO_CONTRACTION_CLAIM'
oldroot=REPO/'research/finishing-threshold-goal-20261007/current-author-20261012t/claude-extension-audit/terminal-producer/snapshot'
changed=[]
for item in prep['sources']:
    rel=item['relative_path'];new=P/'instance'/rel;old=oldroot/rel
    assert sha(new)==item['instance_sha256'] and sha(old)==item['accepted_sha256']
    if new.read_bytes()!=old.read_bytes():
        changed.append(rel)
        a=old.read_text().splitlines();b=new.read_text().splitlines()
        assert len(a)==len(b)
        diff=[(x,y) for x,y in zip(a,b) if x!=y]
        assert len(diff)==1
        if rel.endswith('/uniform.py'):
            assert diff[0][0].strip()=='for i,interval in zip(PARAMETERS,((F(0),F(1,4)),(F(-1,20),F(3,20)),(F(-1,8),F(3,40)))):'
            assert diff[0][1].strip()=='for i,interval in zip(PARAMETERS,((F(0),F(8,25)),(F(-1,20),F(1,5)),(F(-1,5),F(3,40)))):'
        else:
            assert rel.endswith('/bridge.py')
            assert diff[0][1].strip()=="padded={'a':(F(0),F(8,25)+pad),'b':(-F(1,20)-pad,F(1,5)+pad),'z':(-F(1,5)-pad,F(3,40)+pad)}"
assert sorted(Path(x).name for x in changed)==['bridge.py','uniform.py']
for name,meta in prep['inputs'].items():assert sha(P/'inputs'/name)==meta['sha256']
gate=load(P/'inputs/accepted-gate-receipt.json')

# Reuse only this reviewer's separately frozen interval/layout implementation.
# No producer module, row generator, symbolic checker, or certificate checker
# is imported. The 90-digit interval grid differs from the producer's 80.
own=PUBLIC/'scripts'
source=(own/'root_chart_transfer.py').read_text()
assert sha(own/'root_chart_transfer.py')=='a130af5a3f8e021be4e1193a7a182f8430599ead13f9894a89f2bd943a284f95'
tree=ast.parse(source)
node=next(x for x in tree.body if isinstance(x,ast.ClassDef) and x.name=='J')
ns={'F':F,'GRID':10**90,'gate':gate}
exec(compile(ast.Module(body=[node],type_ignores=[]),'<own-J>','exec'),ns)
piece=source[source.index('t,beta=[J'):source.index('ur=(c,s);vr=(-s,c)')]
exec(compile(piece,'<own-exact-root-layout>','exec'),ns)
J=ns['J'];points=ns['rootpoints'];c,s,d,e=(ns[k] for k in ('c','s','d','e'))
axes_u=[(F(1),F(0))]*8+[(c,s)]*6+[(F(1),F(0)),(d,-e),(F(1),F(0))]
turn=lambda v:(-v[1],v[0])
axes=[(u,turn(u)) for u in axes_u]
dot=lambda a,b:sum((x*y for x,y in zip(a,b)),F(0))
EPS=F(1,5000);PAD=F(1,10**12)
box={2:(F(0),F(8,25)+PAD),21:(-F(1,20)-PAD,F(1,5)+PAD),25:(-F(1,5)-PAD,F(3,40)+PAD)}
assert rec['padded_box']=={str(k):list(map(str,v)) for k,v in box.items()}
assert F(rec['epsilon'])==EPS

def maps(ax):
    H=[];G=[]
    for i in range(17):
        if i==3:h=[{},{}];g=[{},{}]
        elif i==1:h=[{},{3:F(1)}];g=[{2:-F(1)},{}]
        elif i in (10,12):
            w,sgn=(21,-1) if i==10 else (25,1)
            h=[{2*i:ax[i][0][k]} for k in (0,1)]
            g=[{w:sgn*ax[i][1][k]} for k in (0,1)]
        else:h=[{2*i:F(1)},{2*i+1:F(1)}];g=[{},{}]
        H.append(h);G.append(g)
    return H,G
H,G=maps(axes)
def subtract(a,b):return {k:a.get(k,F(0))-b.get(k,F(0)) for k in set(a)|set(b)}
def iv(coef,bounds):return sum((J(v)*J(*bounds[k]) for k,v in coef.items()),J(0))
def pair_data(i,j,p,hh,gg,bounds):
    delta=tuple(p[j][k]-p[i][k] for k in (0,1))
    hg=[subtract(hh[j][k],hh[i][k]) for k in (0,1)]
    wg=[subtract(gg[j][k],gg[i][k]) for k in (0,1)]
    world=[J(delta[k])+iv(wg[k],bounds) for k in (0,1)]
    D2=sum(v.bound()**2 for v in world)
    dr2=sum(iv(hg[k],{x:(-F(1),F(1)) for x in hg[k]}).bound()**2 for k in (0,1))
    assert D2<64 and dr2<9
    return delta,hg,wg,D2,dr2
def corners(ax):
    return [tuple(tuple((a*u[k]+b*v[k])/2 for k in (0,1)) for a,b in product((-1,1),repeat=2)) for u,v in ax]
corner=corners(axes)
expected={tuple(item['pair']):sorted(tuple(x) for x in item['retained']) for item in gate['options']}
assert len(expected)==19
root_results=[];max_excluded=None;excluded_count=0;retained_count=0
def audit_pair(pair,bounds):
    left,right=pair;i,j=left-1,right-1
    delta,hg,wg,D2,dr2=pair_data(i,j,points,H,G,bounds)
    records=[];alive=[]
    for owner,other in ((i,j),(j,i)):
        for axis in (0,1):
            for sign in (-1,1):
                n=tuple(sign*x for x in axes[owner][axis])
                proj=dot(n,delta)
                for w in bounds:
                    coeff=sum((J(n[k])*J(wg[k].get(w,0)) for k in (0,1)),J(0))
                    proj=J(proj)+coeff*J(*bounds[w])
                lower_support=max(J(dot(n,v)).a for v in corner[other])
                upper=J(proj).b-F(1,2)-lower_support+3*EPS+(8+3*EPS)*EPS+2*EPS
                if upper>=0:alive.append((owner,axis,sign))
                records.append({'owner':owner+1,'axis':axis,'sign':sign,'upper':str(upper),'excluded':upper<0})
    return {'pair':list(pair),'D2':str(D2),'dr2':str(dr2),'retained':[list(x)for x in sorted(alive)],'options':records}
for pair,allowed in expected.items():
    row=audit_pair(pair,box)
    assert sorted(map(tuple,row['retained']))==allowed,(pair,row['retained'],allowed)
    assert len({(x['owner'],x['axis'],x['sign'])for x in row['options']})==8
    for x in row['options']:
        if x['excluded']:
            value=F(x['upper']);max_excluded=value if max_excluded is None else max(max_excluded,value);excluded_count+=1
        else:retained_count+=1
    root_results.append(row)
assert (excluded_count,retained_count)==(125,27)
assert max_excluded < -F(1,60)
assert {tuple(x['pair']):sorted(map(tuple,x['retained'])) for x in rec['options']}==expected

# Complete old/new roster/source equality; symbolic proof is inherited from
# unchanged audited row/layout functions. Bind the producer's fresh replay
# separately and do not mislabel it as our SymPy run.
oldlabels=rec['accepted_labels'];newlabels=rec['new_labels']
assert len(oldlabels)==len(set(oldlabels))==52 and sorted(oldlabels)==sorted(newlabels)
assert [sum(x.startswith(prefix) for x in newlabels)for prefix in ('wall:','pair:','parallel:')]==[25,11,16]
ident=load(P/'symbolic-identities.json')
assert sha(P/'symbolic-identities.json')==rec['identities_sha256']
assert ident['status']=='PASS' and ident['identities']==52
assert sorted(x['label']for x in ident['records'])==sorted(newlabels)
model=load(P/'normalized-model.json')
assert len(model)==244 and all(len(row['a'])==100 for row in model)
assert [x['label']for x in model[:52]]==newlabels
assert all(x['label'].startswith('product:')for x in model[52:])
assert hashlib.sha256(json.dumps(model,sort_keys=True).encode()).hexdigest()==rec['normalized_model_kernel_digest']

# Independently check reference sign branches from geometric affine offsets.
normal_data=ast.parse((P/'instance/research/uniform-capture-20261007/root_geometry.py').read_text())
normals=ast.literal_eval(next(x.value for x in normal_data.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name)and t.id=='NORMALS' for t in x.targets)))
branches={}
parallel_pairs={tuple(map(int,x.split(':')[1:3]))for x in newlabels if x.startswith('parallel:')}
for left,right in sorted(parallel_pairs):
    i,j=left-1,right-1;axis,sgn=normals[left,right];n=tuple(sgn*x for x in axes[i][axis]);jn=turn(n)
    delta,_,wg,_,_=pair_data(i,j,points,H,G,box)
    tau=J(0) if (left,right) in ((1,3),(1,5),(2,6)) else J(dot(jn,delta))
    for w in box:
        coeff=sum((J(jn[k])*J(wg[k].get(w,0)) for k in (0,1)),J(0))
        tau=tau+coeff*J(*box[w])
    if (left,right)==(2,6):assert tau.b<=0
    else:assert tau.a>=0
    assert tau.bound()<F(321,1000)
    branches[f'{left}:{right}']=tau.record()
assert len(branches)==8

# Optional independent finite-entry bound on all the same 152 alternatives.
# This uses rational raw-reference geometry and first-order corner bounds,
# not the producer's model generator or finite row decisions.
raw=load(P/'instance/upper-packing-certificate.json');pr=[];ax=[]
for sq in raw['squares']:
    t=F(sq['t']);u=((1-t*t)/(1+t*t),2*t/(1+t*t));ax.append((u,turn(u)))
    pr.append((F(sq['x']),F(sq['y'])))
c0,s0=ax[8][0];T0=c0*(c0+4-F(raw['side']))
pr[12]=tuple(pr[12][k]-T0*ax[12][1][k]/3 for k in (0,1))
hh,gg=maps(ax);cv=corners(ax)
fbox={2:(F(0),F(8,25)),21:(-F(1,20),F(1,5)),25:(-F(1,5),F(3,40))}
r=F(1,200);alpha=F(1,400);finite_results=[];finite_extras=[]
for pair,allowed in expected.items():
    i,j=pair[0]-1,pair[1]-1;delta,hg,wg,_,_=pair_data(i,j,pr,hh,gg,fbox)
    entries=[];alive=[]
    for owner,other in ((i,j),(j,i)):
        for axis in (0,1):
            for sign in (-1,1):
                n=tuple(sign*x for x in ax[owner][axis]);jn=turn(n);v=max(cv[other],key=lambda v:dot(n,v));nv=dot(n,turn(v))
                keys=set(hg[0])|set(hg[1])
                normal_displacement=r*sum(abs(sum(n[k]*hg[k].get(key,0)for k in (0,1)))for key in keys)
                vals=[]
                for ends in product(*fbox.values()):
                    values=dict(zip(fbox,ends))
                    dd=tuple(delta[k]+sum(wg[k].get(w,0)*values[w]for w in fbox)for k in (0,1))
                    vals.append(dot(n,dd)-F(1,2)-dot(n,v)+normal_displacement+alpha*(abs(dot(jn,dd)+nv)+abs(nv)))
                upper=max(vals)+8*alpha*alpha/2+3*r*alpha+(2*alpha)**2/2
                if upper>=0:alive.append((owner,axis,sign))
                entries.append({'owner':owner+1,'axis':axis,'sign':sign,'upper':str(upper),'excluded':upper<0})
    extra=sorted(set(alive)-set(allowed));finite_extras.extend([{'pair':list(pair),'option':list(x)}for x in extra])
    assert set(allowed)<=set(alive)
    finite_results.append({'pair':list(pair),'retained':[list(x)for x in sorted(alive)],'options':entries})

expanded=dict(box);expanded[21]=(box[21][0],F(1,4)+PAD)
control=audit_pair((5,11),expanded)
assert set(map(tuple,control['retained']))-set(expected[5,11])
assert sorted(newlabels[:-1])!=sorted(oldlabels)
assert len(newlabels)==52 and len(newlabels[:-1])==51
out={'status':'PASS_INDEPENDENT_COMPLETE_ROOT_ANALYTIC_GATE',
 'producer_manifest_sha256':producer_sha,'source_sha256':sha(Path(__file__)),
 'own_interval_layout_dependency_sha256':sha(own/'root_chart_transfer.py'),
 'epsilon':str(EPS),'padded_box':{str(k):list(map(str,v))for k,v in box.items()},
 'all152_root_options':root_results,'excluded':excluded_count,'retained':retained_count,
 'maximum_excluded_root_upper':str(max_excluded),'uniform_excluded_root_upper_lt':'-1/60',
 'reference_branches':branches,'exact52_source_roster_binding':True,
 'symbolic_identity_scope':'Inherited accepted52 labelled identities under exact row/layout/source and roster equality; producer fresh symbolic52 replay bound, not independently rerun.',
 'symbolic_identity_receipt_sha256':sha(P/'symbolic-identities.json'),
 'normalized244_model_scope':'File/count/label/kernel-digest binding only; no independent row arithmetic replay or contraction.',
 'finite152_options':finite_results,'finite_extra_options_from_this_bound':finite_extras,
 'finite_gate_all_expected_options_only':not finite_extras,
 'controls':['widening b to1/4 reveals extra5--11 option','omitting one inherited row rejected'],
 'solver_discovery_or_certificate_replay':False,'new_terminal_theorem':False,
 'cpu_seconds':time.process_time()-start}
(HERE/'receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'cpu_seconds':out['cpu_seconds'],'maximum_excluded_root_upper':float(max_excluded),'finite_extra_options':finite_extras}))
