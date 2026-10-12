#!/usr/bin/env python3
"""Independent exact-S* feasibility certificate for the specified 17 squares.

No producer Python is imported or executed. Root isolation, interval arithmetic,
all support sign branches, unit frames, wall inequalities and separating axes
are checked here. Input files are pinned only to identify the audited target.
"""
if not __debug__:
    raise RuntimeError('Run without -O/-OO.')
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import ast, hashlib, json, time
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
GRID = 10**70
PINNED = {
    'research/global-compensation-20261007/checks/endpoint_saturation.py':
    '931943b31aec96325bed92d2d8a3ae99c7bf83889ea6c14ad02a847ebe30010a',
    'research/uniform-capture-20261007/bridge.py':
    '8d5c2a8253f1aae97a243e907d08b337f334a8f27c66e3235e66a30fd8ae9f10',
    'research/uniform-capture-20261007/upstream-root-certificate.json':
    'ef8069b30cd1336ae01124d0f54f13b4f69741c14941f997706b7f599c23a0d9',
    'upper-packing-certificate.json':
    '24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7',
}

class I:
    def __init__(self, a, b=None):
        if isinstance(a,I):
            self.lo,self.hi=a.lo,a.hi
        else:
            self.lo,self.hi=F(a),F(a if b is None else b)
        assert self.lo<=self.hi
    @classmethod
    def out(cls,a,b):
        return cls(F((a*GRID).__floor__(),GRID),F((b*GRID).__ceil__(),GRID))
    def __add__(self,b):
        b=I(b);return I.out(self.lo+b.lo,self.hi+b.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,b):return self+-I(b)
    def __rsub__(self,b):return I(b)+-self
    def __mul__(self,b):
        b=I(b);corners=[x*y for x in (self.lo,self.hi) for y in (b.lo,b.hi)]
        return I.out(min(corners),max(corners))
    __rmul__=__mul__
    def __truediv__(self,b):
        b=I(b);assert not b.lo<=0<=b.hi
        return self*I.out(1/b.hi,1/b.lo)
    def __rtruediv__(self,b):return I(b)/self
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        result=I(1)
        for _ in range(n):result=result*self
        return result
    def record(self):return [str(self.lo),str(self.hi)]

POLYS=(
 ((0,1,1),(1,0,1),(1,1,-1),(1,2,-3),(2,0,-3),(2,2,1),(3,0,-1),(3,2,-1),(4,0,-1),(4,1,-1),(4,2,-1),(5,1,1)),
 ((0,1,-1),(0,2,4),(0,3,-1),(1,1,3),(1,2,-2),(1,3,-5),(1,4,2),(2,1,-4),(2,2,-2),(2,3,4),(2,4,2),(3,0,-2),(3,2,2),(4,0,-2),(4,1,1),(4,2,-2),(4,3,1),(5,1,1),(5,3,1)))
MID=(F(362043893314323383453621978739944164218293243036741520638379,10**60),
     F(330948674722739910429808533282915634174672003999685385633441,10**60))
OUTER_RADIUS=F(1,10**12)

def evaluate(poly,x):return sum((co*x[0]**a*x[1]**b for a,b,co in poly),0)
def derivative(poly,k):
    return [(a-int(k==0),b-int(k==1),co*(a if k==0 else b))
            for a,b,co in poly if (a if k==0 else b)>0]
def pin_inputs():
    for name,digest in PINNED.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    declared=json.loads((ROOT/'research/uniform-capture-20261007/upstream-root-certificate.json').read_text())
    assert POLYS==tuple(tuple(tuple(map(int,row)) for row in p) for p in declared['polynomials'])
    # Read a literal declaration only, without importing or executing bridge.
    bridge_tree=ast.parse((ROOT/'research/uniform-capture-20261007/bridge.py').read_text())
    declarations=[node.value for node in bridge_tree.body if isinstance(node,ast.Assign)
                  and any(isinstance(name,ast.Name) and name.id=='POLYNOMIALS' for name in node.targets)]
    assert len(declarations)==1 and ast.literal_eval(declarations[0])==POLYS
    assert MID==tuple(map(F,declared['box']['midpoint']))
    assert OUTER_RADIUS==F(declared['box']['radius'])
    raw=json.loads((ROOT/'upper-packing-certificate.json').read_text())
    assert MID==(F(raw['squares'][8]['t']),-F(raw['squares'][15]['t']))

def isolate_root():
    box=[I(x-OUTER_RADIUS,x+OUTER_RADIUS) for x in MID]
    jac=[[evaluate(derivative(p,j),MID) for j in (0,1)] for p in POLYS]
    a,b=jac[0];c,d=jac[1];det=a*d-b*c
    assert det!=0
    inverse=((d/det,-b/det),(-c/det,a/det))
    jbox=[[evaluate(derivative(p,j),box) for j in (0,1)] for p in POLYS]
    residual=[evaluate(p,MID) for p in POLYS]
    error=[[I(int(i==j))-sum((inverse[i][k]*jbox[k][j] for k in (0,1)),I(0))
            for j in (0,1)] for i in (0,1)]
    q=max(sum(max(abs(x.lo),abs(x.hi)) for x in row) for row in error)
    eta=max(abs(sum(inverse[i][k]*residual[k] for k in (0,1))) for i in (0,1))
    assert q<1 and eta+q*OUTER_RADIUS<OUTER_RADIUS
    inner=F(1,10**50)
    assert eta/(1-q)<inner
    root=[I(x-inner,x+inner) for x in MID]
    assert all(0<x.lo<x.hi<1 for x in root)
    return root,dict(method='Independent Banach contraction for x-J(mid)^-1 F(x)',
       root_definition='Unique common zero of the two recorded polynomials in midpoint +/-10^-12',
       midpoint=list(map(str,MID)),outer_radius=str(OUTER_RADIUS),
       midpoint_jacobian_determinant=str(det),inverse_jacobian=[[str(x) for x in row] for row in inverse],
       derivative_error_matrix=[[x.record() for x in row] for row in error],
       contraction_bound=str(q),midpoint_residual_bound=str(eta),
       inner_radius=str(inner),root_intervals=[x.record() for x in root])

t,beta=sp.symbols('t beta')
ROOT_POLYS=[sp.Poly(sum(co*t**a*beta**b for a,b,co in poly),t,beta) for poly in POLYS]
root=None
interval_cache={}
denominator_checks={}
zero_cache={}

def terms(poly):
    return [[a,b,str(co)] for (a,b),co in sp.Poly(poly,t,beta).terms()]
def polynomial_interval(poly):
    return sum((F(str(co))*root[0]**a*root[1]**b
                for (a,b),co in sp.Poly(poly,t,beta).terms()),I(0))
def iv(expr):
    expr=sp.cancel(expr)
    if expr in interval_cache:return interval_cache[expr]
    num,den=sp.fraction(expr)
    dv=polynomial_interval(den)
    assert dv.lo>0 or dv.hi<0,('zero-crossing denominator',den,dv.record())
    denominator_checks[str(den)]={'terms':terms(den),'interval':dv.record()}
    result=polynomial_interval(num)/dv
    interval_cache[expr]=result
    return result
def zero(expr):
    expr=sp.cancel(expr)
    if expr in zero_cache:return zero_cache[expr]
    num,den=sp.fraction(expr)
    dv=polynomial_interval(den)
    assert dv.lo>0 or dv.hi<0
    denominator_checks[str(den)]={'terms':terms(den),'interval':dv.record()}
    if num==0:
        result={'kind':'rational_identity','denominator':str(den)}
    else:
        result=None
        for index,p in enumerate(ROOT_POLYS):
            quotient,remainder=sp.Poly(num,t,beta).div(p)
            if remainder.is_zero:
                assert sp.expand(num-quotient.as_expr()*p.as_expr())==0
                result={'kind':'root_polynomial_multiple','polynomial':index,
                        'quotient_terms':terms(quotient),'denominator':str(den)}
                break
    zero_cache[expr]=result
    return result
def certify_nonnegative(expr):
    expr=sp.cancel(expr);interval=iv(expr)
    if interval.lo>0:
        return {'kind':'strict_positive','expression':str(expr),'interval':interval.record()}
    certificate=zero(expr)
    assert certificate is not None,('failed nonnegative',str(expr),interval.record())
    return {'expression':str(expr),**certificate}
def dot(a,b):return sum(x*y for x,y in zip(a,b))

def endpoint_layout():
    # Direct endpoint coordinates; no imported bridge and no slide assumption.
    c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
    d=(1-beta*beta)/(1+beta*beta);e=2*beta/(1+beta*beta)
    S=(6+4*t)/(1+2*t-t*t);h=(c+s)/2;half=sp.Rational(1,2)
    x15=half+(2+c*s+3*s-s*S)/c
    y17=3*half+(2+3*c-c*S)/s
    A=d*(x15+half)-e*(S-1)+half
    B=(d+e)*(S-1)-half
    U10=3*half+c*s+2*s;V10=c*(S-1)-s-half
    U11=c+2*s+half;V11=2*c+(c*c-s*s)/2-1;U13=2*c+s+half
    R=lambda U,V:(c*U-s*V,s*U+c*V)
    P=[(half,half),(S-half,half),(3*half,half),(S-3*half,half),
       (half,3*half),(S-half,3*half),(half,S-half),(S-half,S-half),
       (h,2+h),R(U10,V10),R(U11,V11),R(U11+1,V10-1),
       R(U13,V11-1),R(U13+1,V10-2),(x15,S-half),
       (d*A+e*B,-e*A+d*B),(S-half,y17)]
    frames=[((1,0),(0,1)),((c,s),(-s,c)),((d,-e),(e,d))]
    roster=[0]*8+[1]*6+[0,2,0]
    # The target's specified restoration of bridge square13 is exactly this
    # direct endpoint coordinate: R(U13,V11-1-tau/3)+tau*v/3.
    tau=c*(c+4-S);old13=R(U13,V11-1-tau/3)
    restoration=[sp.cancel(P[12][k]-old13[k]-tau*frames[1][1][k]/3) for k in (0,1)]
    assert restoration==[0,0]
    return S,P,frames,roster,(c,s,d,e),restoration

def main():
    global root
    start=time.monotonic();pin_inputs();root,root_receipt=isolate_root()
    S,P,frames,roster,(c,s,d,e),restoration=endpoint_layout()
    unit=[]
    for index,(a,b) in enumerate(frames):
        identities=[dot(a,a)-1,dot(b,b)-1,dot(a,b),a[0]*b[1]-a[1]*b[0]-1]
        assert all(sp.cancel(expr)==0 for expr in identities)
        for axis in (a,b):
            for coord in axis:iv(coord)
        unit.append({'class':index,'squares':[j+1 for j,k in enumerate(roster) if k==index],
                     'identities':'|a|^2=|b|^2=1, a dot b=0, det(a,b)=1, exact rational identities'})
    strict_branches={name:certify_nonnegative(expr) for name,expr in
         [('c',c),('s',s),('d',d),('e',e),('cos_theta_plus_beta',c*d-s*e),
          ('sin_theta_plus_beta',c*e+s*d)]}
    assert all(row['kind']=='strict_positive' for row in strict_branches.values())
    all_axes=[axis for frame in frames for axis in frame]
    signs=[];supports={}
    for owner_class in range(3):
        for normal_axis in (0,1):
            for sign in (-1,1):
                n=tuple(sign*x for x in frames[owner_class][normal_axis])
                for square_class,frame in enumerate(frames):
                    total=0
                    for body_axis,axis in enumerate(frame):
                        expr=sp.cancel(dot(axis,n));bound=iv(expr)
                        if expr==0:
                            branch=0
                        elif bound.lo>0:
                            branch=1
                        elif bound.hi<0:
                            branch=-1
                        else:
                            raise AssertionError(('unresolved support sign',expr,bound.record()))
                        total+=branch*expr
                        signs.append({'body_class':square_class,'body_axis':body_axis,
                                      'normal_class':owner_class,'normal_axis':normal_axis,
                                      'normal_sign':sign,'dot_product':str(expr),
                                      'sign':branch,'interval':bound.record()})
                    supports[square_class,owner_class,normal_axis,sign]=sp.cancel(total/2)
    assert len(signs)==72
    def support(label,owner,axis,sign):return supports[roster[label-1],roster[owner-1],axis,sign]
    walls=[]
    for i,(x,y) in enumerate(P,1):
        for name,axis,sign,coord in [('left',0,-1,x),('right',0,1,S-x),
                                    ('bottom',1,-1,y),('top',1,1,S-y)]:
            gap=coord-support(i,1,axis,sign)
            walls.append({'square':i,'wall':name,'certificate':certify_nonnegative(gap)})
    pairs=[];contacts=[]
    for i in range(1,18):
        for j in range(i+1,18):
            options=[]
            delta=tuple(P[j-1][k]-P[i-1][k] for k in (0,1))
            for owner in (i,j):
                for axis in (0,1):
                    for sign in (-1,1):
                        n=tuple(sign*x for x in frames[roster[owner-1]][axis])
                        gap=sp.cancel(dot(n,delta)-support(i,owner,axis,sign)-support(j,owner,axis,sign))
                        options.append((iv(gap).lo,owner,axis,sign,gap))
            _,owner,axis,sign,gap=max(options,key=lambda row:row[0])
            certificate=certify_nonnegative(gap)
            pair={'pair':[i,j],'owner':owner,'axis':axis,'sign':sign,'certificate':certificate}
            if certificate['kind']!='strict_positive':
                # Additionally establish actual touching, not just a tight
                # selected row: every SAT gap is nonpositive and one is zero.
                all_nonpositive=[]
                for _,ow,ax,sg,other in options:
                    bound=iv(other)
                    if bound.hi<0:rec={'kind':'strict_negative','interval':bound.record()}
                    else:
                        rec=zero(other)
                        assert rec is not None,('contact has positive alternative',i,j,ow,ax,sg)
                    all_nonpositive.append({'owner':ow,'axis':ax,'sign':sg,'certificate':rec})
                pair['contact_all_axes_nonpositive']=all_nonpositive
                contacts.append([i,j])
            pairs.append(pair)
        print(json.dumps({'completed_square':i,'pair_rows':len(pairs),'seconds':time.monotonic()-start}),flush=True)
    assert len(P)==17 and len(roster)==17 and len(walls)==68 and len(pairs)==136
    assert {tuple(x['pair']) for x in pairs}=={(i,j) for i in range(1,18) for j in range(i+1,18)}
    # Every center and side denominator is checked independently of which
    # separating row happened to be chosen for a pair.
    coordinates=[{'square':i,'class':roster[i-1],
                  'center':[str(sp.cancel(x)) for x in point],
                  'center_intervals':[iv(x).record() for x in point]}
                 for i,point in enumerate(P,1)]
    side_interval=iv(S)
    assert side_interval.lo>0
    pin_inputs()
    out={'status':'PASS_INDEPENDENT_EXACT_S_STAR_17_SQUARE_FEASIBILITY',
         'scope':'Explicit endpoint packing only; proves side S* is feasible, not global optimality. No rational-U or resource-charge premise.',
         'independence':'No producer Python imported or executed. Fresh rational interval implementation, root contraction, support branches, and SAT checks.',
         'target_construction':'bridge.layout(t,beta), followed by P13 += tau*v/3 and P4=(S*-3/2,1/2); reconstructed directly here.',
         'root_polynomials':[terms(p) for p in ROOT_POLYS],'root_receipt':root_receipt,
         'side_expression':str(S),'side_interval':side_interval.record(),
         'unit_frame_checks':unit,'frames':[[[str(sp.cancel(x)) for x in axis] for axis in frame] for frame in frames],
         'orientation_roster':roster,'square13_restoration_identities':list(map(str,restoration)),
         'strict_support_generators':strict_branches,'all_72_support_sign_branches':signs,
         'coordinates':coordinates,'walls':walls,'pairs':pairs,'touching_pairs':contacts,
         'wall_certificate_counts':dict(Counter(r['certificate']['kind'] for r in walls)),
         'pair_certificate_counts':dict(Counter(r['certificate']['kind'] for r in pairs)),
         'all_denominator_checks':denominator_checks,'seconds':time.monotonic()-start,
         'source_hashes':PINNED,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'endpoint-receipt.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','wall_certificate_counts','pair_certificate_counts','touching_pairs','seconds']},indent=2))

if __name__=='__main__':main()
