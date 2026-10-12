#!/usr/bin/env python3
# Independent admission check (reader ADMISSION). Exact rationals only.
if __name__ == '__main__' and not globals().get('_S17_PUBLIC_RUNNER_ACTIVE', False):
    raise SystemExit('Use replay_public.py for this check; outputs must be redirected.')
import json, hashlib, sys, os
from fractions import Fraction as F
from pathlib import Path
PUBLIC=Path(__file__).resolve().parent.parent
REPO=str(PUBLIC.parents[4])
PK=str(PUBLIC/"runtime")
CL=REPO+"/local-research/claude-20261002/cloud/analysis/join_design"
JOIN=os.environ.get("JOINDIR", REPO+"/research/window-extension-20261008/bigbox/join")
U=F(1169,250); Rr=F(4675530093604551,10**15); C=F(4675531,10**6)
def sha(p): return hashlib.sha256(open(p,"rb").read()).hexdigest()
def rot(t): t=F(t); return (F(1-t*t,1+t*t), F(2*t,1+t*t))
def mul(p,q): return (p[0]*q[0]-p[1]*q[1], p[0]*q[1]+p[1]*q[0])
def conj(p): return (p[0],-p[1])
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
Jq=(F(0),F(1))
# ---- reference chart (SPEC 3.0 section 1)
pk=json.load(open(REPO+"/upper-packing-certificate.json"))
assert sha(REPO+"/upper-packing-certificate.json")=="24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7"
assert F(pk["side"])==Rr
p={};t={};u={};v={}
for k,s in enumerate(pk["squares"]):
    i=k+1; p[i]=(F(s["x"]),F(s["y"])); t[i]=F(s["t"]); u[i]=rot(t[i]); v[i]=(-u[i][1],u[i][0])
T0=u[9][0]*(u[9][0]+4-Rr)
p[13]=(p[13][0]-T0/3*v[13][0], p[13][1]-T0/3*v[13][1])
e={i:((u[i],v[i]) if i in (11,13) else ((F(1),F(0)),(F(0),F(1)))) for i in p}
# ---- L enclosure from the packet
ec=json.load(open(PK+"/EXACT_ENDPOINT_AND_CASES.json"))
Llo,Lhi=[F(x) for x in ec["endpoint"]["L_interval"]]
assert Llo<Lhi<Rr<C<U
ROOTFILE={r["root"]:r["root_pin"] for r in ec["branches"]}
RHO=F(207107,500000)
assert (1+RHO)**2>2      # rho > tan(pi/8)
ALLDIR=(-RHO,RHO)
def loadcls(path):
    if not path.startswith("/"): path=CL+"/"+path
    d=json.load(open(path))
    assert d["schema"]=="s17-classes-v1" and d["symmetry"]=="fixed"
    assert [F(x) for x in d["frame"]["center"]]==[U/2,U/2], path
    return d,sha(path)
def cls(d,prefix):
    cs=[c for c in d["classes"] if c["name"].startswith(prefix)]
    assert len(cs)==1,(prefix,[c["name"] for c in d["classes"]])
    return cs[0]
def slots(c):
    return [([(F(a),F(b)) for a,b in s["centre"]["polygon"]],(F(s["angle_tan_half"][0]),F(s["angle_tan_half"][1]))) for s in c["slots"]]
def target(d,label):
    """the unique threshold-0 class that is the label's target"""
    cs=[c for c in d["classes"] if F(c["threshold"])==0 and any(c["name"].startswith(pre+"label%d_"%label) for pre in ("PB_","HULLW_","QB_","HULL_","B_","T_","S_"))]
    assert len(cs)==1,[c["name"] for c in d["classes"]]
    s=slots(cs[0]); assert len(s)==1
    return cs[0]["name"],s[0]
def rect(x0,x1,y0,y1): return [(F(x0),F(y0)),(F(x1),F(y0)),(F(x1),F(y1)),(F(x0),F(y1))]
# ---- transport of a class-frame polygon into chart coordinates of label i, all L in [Llo,Lhi]
def transport(i,poly,clip=True):
    out=[]
    for k in (0,1):
        vals=[]
        for c in poly:
            for L in (Llo,Lhi):
                q=(c[0]-(U-L)/2-p[i][0], c[1]-(U-L)/2-p[i][1])
                vals.append(dot(e[i][k],q))
        lo,hi=min(vals),max(vals)
        if clip and i not in (11,13):
            # physical: centre in [1/2, L-1/2] in the endpoint frame, any orientation
            lo=max(lo,F(1,2)-p[i][k]); hi=min(hi,Lhi-F(1,2)-p[i][k])
        out.append((lo,hi))
    return out
def loadroot(name,fn=None):
    pin=ROOTFILE[name]
    path=fn or (REPO+"/"+pin["file"])
    if fn is None: assert sha(path)==pin["sha256"],name
    else: path=fn
    d=json.load(open(path))
    assert F(d["Sref"])==Rr and F(d["S_floor"])==Rr and [F(x) for x in d["S"]]==[Rr,Rr] and d["labels"]==17
    box={int(i):[(F(a),F(b)) for a,b in bb] for i,bb in d["window"]["box"].items()}
    arc={}
    for i,a in d["root_arc"].items():
        c=tuple(F(x) for x in a["c"]); lo=tuple(F(x) for x in a["lo"]); hi=tuple(F(x) for x in a["hi"])
        for g in (c,lo,hi): assert g[0]**2+g[1]**2==1
        assert lo[0]>0 and hi[0]>0 and lo[1]<=hi[1]
        A=mul(u[int(i)],mul(c,lo)); B=mul(u[int(i)],mul(c,hi))
        arc[int(i)]=(A,B)
    return d,box,arc
def in_arc(D,arc):
    A,B=arc
    return cross(A,D)>=0 and cross(D,B)>=0
def arc_margin(D,arc):
    """sines of the angular distances from D to the two ends (positive inside)"""
    A,B=arc
    return cross(A,D),cross(D,B)
def interval_in_arc(a_lo,a_hi,arc):
    """absolute tan-half interval [a_lo,a_hi] of ONE side direction; some quarter-turn lift must lie in the root arc.
    returns (k, margin_lo_sine, margin_hi_sine) or None"""
    best=None
    for k in range(4):
        D1,D2=rot(a_lo),rot(a_hi)
        for _ in range(k): D1,D2=mul(D1,Jq),mul(D2,Jq)
        assert cross(D1,D2)>=0  # CCW, shorter than a half turn
        if in_arc(D1,arc) and in_arc(D2,arc):
            m=(k,cross(arc[0],D1),cross(D2,arc[1]))
            assert best is None
            best=m
    return best
