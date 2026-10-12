"""Independent wider rational entry transfer; no producer code imported."""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import hashlib,json,resource,time
resource.setrlimit(resource.RLIMIT_CPU,(3,4))
start=time.process_time()
HERE=Path(__file__).resolve().parent;G=HERE.parents[1]
P=G/'full-stopped-propagation/continuation'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
assert sha(G/'full-stopped-propagation/rational-entry-review/MANIFEST.json')=='5a70b980bdf8c519d1bcb19a6f710737e41073e782286f849e9ac62915f3b3cc'
assert sha(P/'instance/upper-packing-certificate.json')=='24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7'
assert sha(P/'inputs/accepted-root-gate.json')=='7dee354d5582d3104a6972eb81efc988d9284ede0751906faf0ed9a10b25c8d5'
gate=load(P/'inputs/accepted-root-gate.json');raw=load(P/'instance/upper-packing-certificate.json')
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
ur=(c,s);vr=(-s,c);eps=F(1,200);angle=F(1,400);target=F(501,100000);pad=F(1,10**12)
box={2:(F(0),F(8,25)),21:(-F(1,20),F(1,5)),25:(-F(1,5),F(3,40))}
core={};slides={};slider_errors={}
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
        slider_errors[w]=sign*base_v+sign*Mvu*J(-eps,eps)+(Mvv-1)*J(*box[w])
    elif i==1:
        core[3]=(delta[1]+J(-eps,eps)).bound()
        a=J(*box[2])+S-half-points[1][0]
        slides[2]=J(max(F(0),a.a),a.b)
        slider_errors[2]=S-half-points[1][0]
    else:
        for k in (0,1):core[2*i+k]=(delta[k]+J(-eps,eps)).bound()
    drift=2*F(gate['root']['tight_root_radius']) if i in range(8,14) or i==15 else F(0)
    core[34+i]=angle+drift
expected_core=set(range(51))-{2,6,7,21,25,37}
assert set(core)==expected_core and len(core)==45
assert max(core.values()) < eps+F(1,10**15) < target
assert max(core[34+i] for i in range(17) if i!=3)<angle+F(1,10**15)<target
for w,(lo,hi) in box.items():
    assert (lo if w==2 else lo-pad)<=slides[w].a<=slides[w].b<=hi+pad
assert S.b<points[1][0]+half<Sref
floor_margin=points[7][0]+half-F(1,200)-(Sref-F(1,50))
assert floor_margin>F(149,10000)


# Keep root-to-raw errors rather than passing rounded stop cutoffs unchanged.
assert set(slider_errors)=={2,21,25}
assert all(v.bound()<F(1,10**15) for v in slider_errors.values())
root_b_lower=-F(17,10)*target
root_sum_upper=T.b/3+F(14,100)*target
root_z_upper=T.b/3+(F(17,10)+F(14,100))*target
raw_b_lower=root_b_lower-slider_errors[21].b
raw_sum_upper=root_sum_upper-slider_errors[21].a-slider_errors[25].a
raw_z_upper=root_z_upper-slider_errors[25].a
assert raw_b_lower>-F(213,25000)
assert raw_sum_upper<F(49,2000)
assert raw_z_upper<F(33,1000)
controls={'wrong_larger_position_radius_not_covered':F(1,100)>target,
 'wrong_halfangle_interpretation_not_covered':2*F(1,400)>F(1,400)+F(1,10**15),
 'rational_cap_does_not_supply_a_wall_repair':not(Sref<points[1][0]+F(1,2)),
 'no_rigidity_from_root_entry':target>F(1,5000),
 'rounded_sum_cut_has_no_automatic_transport_margin':F(49,2000)-F(2,10**15)<F(49,2000)}
assert all(controls.values())
out={'status':'EXACT_TRANSFER_AND_RAW_SLACK_PASS_REQUIRES_SEPARATE_STOP_THEOREM_BINDING',
 'raw_position_radius':'1/200','raw_angle_radius_radians':'1/400','root_epsilon':'501/100000',
 'core_indices':sorted(core),'all45_root_core_bounds':{str(i):str(v) for i,v in core.items()},
 'maximum_root_core':str(max(core.values())),
 'raw_slider_box':{str(w):list(map(str,v)) for w,v in box.items()},
 'root_slider_enclosures':{str(w):v.record() for w,v in slides.items()},
 'root_minus_raw_slider_errors':{str(w):v.record() for w,v in slider_errors.items()},
 'T_interval':T.record(),'algebraic_side_interval':S.record(),'rational_p2x_plus_half':str(points[1][0]+F(1,2)),
 'stronger_root_bounds':{'b_lower':str(root_b_lower),'b_plus_z_upper':str(root_sum_upper),'z_upper':str(root_z_upper)},
 'raw_bounds':{'b_lower':str(raw_b_lower),'b_plus_z_upper':str(raw_sum_upper),'z_upper':str(raw_z_upper)},
 'raw_cutoffs':{'b_lower':'-213/25000','b_plus_z_upper':'49/2000','z_upper':'33/1000'},
 'strict_raw_slacks':{'b_lower':str(raw_b_lower+F(213,25000)),
 'b_plus_z_upper':str(F(49,2000)-raw_sum_upper),'z_upper':str(F(33,1000)-raw_z_upper)},
 'controls':controls,'no_optimizer_model_or_symbolic_import':True,'cpu_seconds':time.process_time()-start}
(HERE/'transfer-receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'cpu_seconds':out['cpu_seconds'],'raw_cutoffs':out['raw_cutoffs'],
 'strict_raw_slacks_decimal':{k:float(F(v)) for k,v in out['strict_raw_slacks'].items()}}))
