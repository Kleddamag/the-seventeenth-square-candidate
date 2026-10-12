"""Independent constant/projection check; no producer imports or terminal run."""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import hashlib, json, resource, time

resource.setrlimit(resource.RLIMIT_CPU,(2,3))
start=time.process_time()
HERE=Path(__file__).resolve().parent
PRODUCER=HERE.parent/'producer'
REPO=next(p for p in HERE.parents if (p/'local-research/claude-20261002/results/rerun_trees_20261011/SHA256_G20S_HW.txt').is_file())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
producer_sha='d83b2a3290687ada0f1c36287e8fba371a7a1f3fc01ef7a1c77b906b381148e0'
assert sha(PRODUCER/'PRODUCER_MANIFEST.json')==producer_sha
manifest=load(PRODUCER/'PRODUCER_MANIFEST.json')
for name,expected in manifest['files_sha256'].items():
    assert sha(PRODUCER/name)==expected,name
for name,expected in manifest['source_files_sha256'].items():
    assert sha(REPO/name)==expected,name
OLD=REPO/'research/finishing-threshold-goal-20261007/current-author-20261012t/claude-extension-audit/terminal-producer'
gate=load(OLD/'gate-receipt.json')
raw=load(OLD/'snapshot/upper-packing-certificate.json')
saved=load(PRODUCER/'constants.json')
target=load(PRODUCER/'TARGET.json')
roles=set(range(1,18))-{4}
assert set(target['box'])=={f'{i},{k}' for i in roles for k in (1,2)}
assert set(target['alpha'])==set(map(str,roles))
assert all(F(x)==F(1,400) for x in target['alpha'].values())
special={'2,1':[-F(8,25),F(0)],'11,2':[-F(1,5),F(1,20)],'13,2':[-F(1,5),F(3,40)]}
for key,value in target['box'].items():
    assert list(map(F,value))==special.get(key,[-F(1,200),F(1,200)])

# Different outward grid from the producer; exact rational operations only.
GRID=10**90
class J:
    def __init__(self,a,b=None):
        if isinstance(a,J): self.a,self.b=a.a,a.b
        else: self.a,self.b=F(a),F(a if b is None else b)
        assert self.a<=self.b
    @staticmethod
    def outward(a,b):
        return J(F((a*GRID).__floor__(),GRID),F((b*GRID).__ceil__(),GRID))
    def __add__(self,o):
        o=J(o); return J.outward(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self): return J(-self.b,-self.a)
    def __sub__(self,o): return self+-J(o)
    def __rsub__(self,o): return J(o)+-self
    def __mul__(self,o):
        o=J(o); v=[x*y for x in (self.a,self.b) for y in (o.a,o.b)]
        return J.outward(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=J(o); assert not o.a<=0<=o.b
        return self*J.outward(1/o.b,1/o.a)
    def __rtruediv__(self,o): return J(o)/self
    def bound(self): return max(abs(self.a),abs(self.b))
    def record(self): return [str(self.a),str(self.b)]

dot=lambda x,y:sum((a*b for a,b in zip(x,y)),F(0))
turn=lambda v:(-v[1],v[0])
axes=[];points=[]
for sq in raw['squares']:
    t=F(sq['t']); u=((1-t*t)/(1+t*t),2*t/(1+t*t))
    axes.append((u,turn(u)));points.append((F(sq['x']),F(sq['y'])))
Sref=F(raw['side']);c0,s0=axes[8][0];T0=c0*(c0+4-Sref)
points[12]=tuple(points[12][k]-T0*axes[12][1][k]/3 for k in (0,1))

# Reconstruct the exact-root endpoint layout from its accepted enclosure,
# not by importing bridge.py or rerunning its root proof.
t,beta=[J(*x) for x in gate['root']['intervals']]
c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
d=(1-beta*beta)/(1+beta*beta);e=2*beta/(1+beta*beta)
S=(6+4*t)/(1+2*t-t*t)
half=F(1,2);h=(c+s)/2
x=half+(2+c*s+3*s-s*S)/c
y=3*half+(2+3*c-c*S)/s
aa=d*(x+half)-e*(S-1)+half;bb=(d+e)*(S-1)-half
u10=3*half+c*s+2*s;v10=c*(S-1)-s-half
u11=c+2*s+half;v11=2*c+(c*c-s*s)/2-1
u13=2*c+s+half;T=c*(c+4-S)
rot=lambda a,b:(c*a-s*b,s*a+c*b)
rootpoints=[(half,half),(S-half,half),(3*half,half),
            (S-3*half-T/(3*s),half),(half,3*half),(S-half,3*half),
            (half,S-half),(S-half,S-half),(h,2+h),rot(u10,v10),rot(u11,v11),
            rot(u11+1,v10-1),rot(u13,v11-1-T/3),rot(u13+1,v10-2),
            (x,S-half),(d*aa+e*bb,-e*aa+d*bb),(S-half,y)]
ur=(c,s);vr=(-s,c);eps=F(1,10000);pad=F(1,10**12)
box={2:(F(0),F(8,25)),21:(-F(1,20),F(1,5)),25:(-F(1,5),F(3,40))}
core={};slides={}
for i in range(17):
    if i==3: continue
    delta=tuple(J(points[i][k])-rootpoints[i][k] for k in (0,1))
    if i in (10,12):
        w,sign=(21,-1) if i==10 else (25,1)
        base_u=dot(ur,delta);base_v=dot(vr,delta)
        Muu=dot(ur,axes[i][0]);Muv=dot(ur,axes[i][1])
        Mvu=dot(vr,axes[i][0]);Mvv=dot(vr,axes[i][1])
        core[2*i]=(base_u+Muu*J(-eps,eps)+sign*Muv*J(*box[w])).bound()
        slides[w]=sign*base_v+sign*Mvu*J(-eps,eps)+Mvv*J(*box[w])
    elif i==1:
        core[3]=(delta[1]+J(-eps,eps)).bound()
        a=J(*box[2])+S-half-points[1][0]
        slides[2]=J(max(F(0),a.a),a.b)
    else:
        for k in (0,1):core[2*i+k]=(delta[k]+J(-eps,eps)).bound()
    drift=2*F(gate['root']['tight_root_radius']) if i in range(8,14) or i==15 else F(0)
    core[34+i]=eps+drift
expected_core=set(range(51))-{2,6,7,21,25,37}
assert set(core)==expected_core and len(core)==45
assert max(core.values()) < eps+F(1,10**15) < F(1,5000)
for w,(lo,hi) in box.items():
    assert (lo if w==2 else lo-pad)<=slides[w].a<=slides[w].b<=hi+pad
assert S.b<points[1][0]+half<Sref
floor_margin=points[7][0]+half-F(1,200)-(Sref-F(1,50))
assert floor_margin>F(149,10000)

# The exact affine coefficients are -a, +b and -z. Old fraction-valued
# enclosures include the same 1e-12 padding; shift just the changed extremes.
branches={}
for entry in gate['parallel_branches']:
    key=':'.join(entry['label'].split(':')[1:3]);lo,hi=map(F,entry['tau'])
    if key=='2:6':lo-=F(8,25)-F(1,4)
    if key=='11:12':hi+=F(1,5)-F(3,20)
    if key=='13:14':hi+=F(1,5)-F(1,8)
    assert (lo>=0 if entry['branch']==1 else hi<=0)
    assert max(abs(lo),abs(hi))<F(321,1000)
    if key in branches:assert branches[key]==[str(lo),str(hi)]
    branches[key]=[str(lo),str(hi)]
assert len(branches)==8 and branches==saved['parallel_branches']
assert F(branches['11:12'][0])>F(3,500)
assert F(branches['13:14'][0])>F(1,200)

# Independently derived one-corner SAT envelope, with a finer norm grid.
def norm(v):
    q=sum(x*x for x in v)*10**24;k=isqrt(q.numerator//q.denominator)
    if F(k*k)<q:k+=1
    return F(k,10**12)
v=max((tuple((a*axes[10][0][k]+b*axes[10][1][k])/2 for k in (0,1))
       for a in (-1,1) for b in (-1,1)),key=lambda x:x[0])
base=tuple(points[10][k]-points[4][k] for k in (0,1))
motion=tuple(-x for x in axes[10][1]);nv=-v[1]
def bound(r,alpha):
    delta_radius=tuple(r*(1+abs(axes[10][0][k])) for k in (0,1))
    D=norm(tuple(max(abs(base[k]+q*motion[k]) for q in box[21]) for k in (0,1)))
    linear=[]
    for q in box[21]:
        dx,dy=(base[k]+q*motion[k] for k in (0,1))
        linear.append(dx-half-v[0]+delta_radius[0]+alpha*(abs(dy+nv)+abs(nv)))
    return max(linear)+D*alpha*alpha/2+alpha*norm(delta_radius)+norm(v)*(2*alpha)**2/2
small_option=bound(F(1,200),F(1,400));larger_option=bound(F(1,100),F(1,200))
assert small_option < -F(9,1000)
assert small_option<=F(saved['pair5_11_owner5_x_first_order_upper'][0]['upper'])
assert larger_option>0

controls={
 'obsolete_39_125_terminal_rejected':special['2,1'][0] != -F(39,125),
 'rational_cap_cannot_supply_a_nonnegative':not(Sref<points[1][0]+half),
 'uncontracted_1_4000_not_inside_1_5000':F(1,4000)>F(1,5000),
 'obsolete_313_1000_offset_bound_rejected':abs(F(branches['2:6'][0]))>F(313,1000),
}
assert all(controls.values())
out={'status':'PASS_INDEPENDENT_SOURCE_AND_CONDITIONAL_CONSTANT_ASSESSMENT',
 'producer_manifest_sha256':producer_sha,'source_sha256':sha(Path(__file__)),
 'target_a_upper':'8/25','terminal_angle':'1/400','terminal_position':'1/200',
 'maximum_exact_root_core_from_1_10000':str(max(core.values())),
 'exact_root_slider_enclosures':{str(k):v.record() for k,v in slides.items()},
 'finite_side_floor_margin':str(floor_margin),'parallel_branches':branches,
 'single_5_11_competing_option_upper':str(small_option),
 'larger_tube_bound_positive_not_a_witness':str(larger_option),
 'corruption_controls':controls,'full_roster_or_152_options_checked':False,
 'new_rigidity_or_finite_certificate_checked':False,
 'actual_pose_matching_or_R17_work':False,'model_solver_or_checker_run':False,
 'cpu_seconds':time.process_time()-start}
(HERE/'receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'cpu_seconds':out['cpu_seconds'],
                  'single_option_upper_decimal':float(small_option)}))
