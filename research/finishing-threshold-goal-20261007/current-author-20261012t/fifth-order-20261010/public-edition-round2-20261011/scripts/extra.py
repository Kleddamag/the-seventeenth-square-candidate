if __name__ == '__main__' and not globals().get('_S17_PUBLIC_RUNNER_ACTIVE', False):
    raise SystemExit('Use replay_public.py for this check; outputs must be redirected.')
import json, itertools
from adm import *
import run_adm
from run_adm import *
# ---------- physical centre box at side <= C in F_U
LOc=(U-C)/2+F(1,2); HIc=(U+C)/2-F(1,2)
assert (LOc,HIc)==(F(1000469,2000000),F(8351531,2000000))
def clip(poly,a,b,c):
    out=[];n=len(poly)
    for k in range(n):
        P,Q=poly[k],poly[(k+1)%n]; fp=a*P[0]+b*P[1]-c; fq=a*Q[0]+b*Q[1]-c
        if fp<=0: out.append(P)
        if (fp<0<fq) or (fq<0<fp):
            tt=fp/(fp-fq); out.append((P[0]+tt*(Q[0]-P[0]),P[1]+tt*(Q[1]-P[1])))
    return out
def phys(poly):
    for a,b,c in ((-1,0,-LOc),(1,0,HIc),(0,-1,-LOc),(0,1,HIc)):
        poly=clip(poly,F(a),F(b),c)
        if not poly: return []
    return poly
def diam2(pts): return max((P[0]-Q[0])**2+(P[1]-Q[1])**2 for P in pts for Q in pts)
def sep(pa,pb):
    for poly in (pa,pb):
        n=len(poly)
        for k in range(n):
            P,Q=poly[k],poly[(k+1)%n]; nx,ny=Q[1]-P[1],P[0]-Q[0]
            if nx==0 and ny==0: continue
            a=[nx*w[0]+ny*w[1] for w in pa]; b=[nx*w[0]+ny*w[1] for w in pb]
            if max(a)<min(b) or max(b)<min(a): return True
    return False
print("== capacity one and 136-pair disjointness of the 17 selected targets (clipped to the physical centre box at side C)")
for root in ["JQ","JPWS","JPW13","JG","JPA","JPG3m","JPG3p","JPG17m","JPG17p","JPG15m","JPG15p"]:
    s=spec(root); fp={i:phys(s[i][0]) for i in s}
    assert all(len(fp[i])>=3 for i in fp)
    dm=max((diam2(fp[i]),i) for i in fp)
    bad=[(i,k) for i,k in itertools.combinations(sorted(fp),2) if not sep(fp[i],fp[k])]
    print("  %-7s max diam^2 = %.6f (label %d) %s; non-separated pairs: %s"%(root,float(dm[0]),dm[1],"<1" if dm[0]<1 else "NOT<1",bad))
# ---------- label 12: target united with the hexagon has capacity one
print("== label 12: diam^2(hexagon U target12), per root")
for root in ["JQ","JPWS","JPW13","JG","JPA","JPG3m","JPG3p","JPG17m","JPG17p","JPG15m","JPG15p"]:
    s=spec(root)
    dL,_=loadcls(run_adm.basefile("L_3")[1]); hexg=slots(cls(dL,"M"))[0][0]
    d2=diam2(phys(hexg)+phys(s[12][0])); print("  %-7s %.6f %s"%(root,float(d2),d2<1), end=";")
print()
# ---------- trigger membership of the actual trigger parent in the selected tilted clauses
print("== triggers of the 84 selected tilted clauses")
def inpoly_rect(sub,sup):  # sub polygon (physically clipped) inside convex polygon sup
    n=len(sup); 
    for q in sub:
        sg=set()
        for k in range(n):
            o,r=sup[k],sup[(k+1)%n]; cr=(r[0]-o[0])*(q[1]-o[1])-(r[1]-o[1])*(q[0]-o[0])
            if cr!=0: sg.add(cr>0)
        if len(sg)>1: return False
    return True
S={j:slots(cls(loadcls(run_adm.basefile("L_%d"%j)[1])[0],"S_label%d_"%j))[0] for j in (3,15,17)}
T9rect=rect(XW,X1,Y0,Y1)
bad=[];cnt=0
for (root,j),r in sorted(run_adm.SEL.items()):
    f=r["literal"]["file"]; d,_=loadcls(f if f.startswith("/") else REPO+"/"+f)
    names=[c["name"] for c in d["classes"]]
    thr={c["name"]:F(c["threshold"]) for c in d["classes"]}
    trig=[c for c in d["classes"] if c["name"].startswith("T") and not c["name"].startswith("T_label")]
    assert len(trig)==1 and F(trig[0]["threshold"])>1 and F(d["bound"])==23, names
    # every threshold-0 class is the target or WC (empty off-wall); M is high
    zero=[n for n in names if thr[n]==0]; assert len(zero)==2 and any(n.startswith("WC_") for n in zero), zero
    wc=slots(cls(d,"WC_")); assert len(wc)==1 and wc[0][0]==rect(X0,XW,Y0,Y1)
    assert F(15)+thr["M"]+F(trig[0]["threshold"])==F(d["bound"])
    tsl=slots(trig[0]); ok=False
    if root=="JPA":
        # x9>53/100 in L9, quarter-turn representative of [G9HI,KWHI] is [(t-1)/(t+1)]
        qb=lambda x:(x-1)/(x+1)
        ok=any(inpoly_rect(phys(T9rect),P) and th[0]<=qb(G9HI) and qb(KWHI)<=th[1] for P,th in tsl)
    else:
        k=int(root[3:-1]); sign=root[-1]
        want=(-RHO,-GT) if sign=="m" else (GT,RHO)   # canonical tau in [-tan(pi/8),-1/20] resp. [1/20,tan(pi/8)), rho>tan(pi/8)
        ok=any(inpoly_rect(phys(S[k][0]),P) and th[0]<=want[0] and want[1]<=th[1] for P,th in tsl)
        assert trig[0]["name"].startswith("T%d"%k), (root,j,trig[0]["name"])
    cnt+=1
    if not ok: bad.append((root,j,trig[0]["name"]))
    # extra premises: PSS (cut trigger = loose slot) must name L_k
    if "PSS" in r["selected"]: assert [x["name"] for x in r["extra_capture_premises"]]==["L_%d"%int(root[3:-1])]
print("  clauses:",cnt,"trigger does not contain the branch's trigger pose set:",bad)
# ---------- v5 contains v4 and v2 (all labels; box and arcs)
print("== v5 region contains the regions of tags v4 and v2")
def region(fn):
    d=json.load(open(fn)); box={int(i):[(F(a),F(b)) for a,b in bb] for i,bb in d["window"]["box"].items()}
    arc={}
    for i,a in d["root_arc"].items():
        c,lo,hi=[tuple(F(x) for x in a[k]) for k in ("c","lo","hi")]
        arc[int(i)]=(mul(u[int(i)],mul(c,lo)),mul(u[int(i)],mul(c,hi)))
    return box,arc
def contains(big,small):
    bb,ba=big; sb,sa=small; worst=None
    for i in range(1,18):
        for k in (0,1):
            for m in (sb[i][k][0]-bb[i][k][0], bb[i][k][1]-sb[i][k][1]):
                worst=m if worst is None or m<worst else worst
        if not (in_arc(sa[i][0],ba[i]) and in_arc(sa[i][1],ba[i]) and cross(sa[i][0],sa[i][1])>=0): return False,i
    return worst>=0, worst
J=REPO+"/research/window-extension-20261008/bigbox/join/"
for root in ["JPA","JPG3m","JPG3p","JPG17m","JPG17p","JPG15m","JPG15p"]:
    r5=region(J+"%s_exact_v5.json"%root)
    print("  %-7s v5>=v4: %s   v5>=v2: %s   v5>=v1: %s"%(root,contains(r5,region(J+"%s_exact_v4.json"%root))[0],contains(r5,region(J+"%s_exact_v2.json"%root))[0],contains(r5,region(J+"%s_exact_v1.json"%root))[0]))
print("  JPWS: v2x>=v4:",contains(region(J+"JPWS_exact_v2x.json"),region(J+"JPWS_exact_v4.json"))[0]," v4>=v2x:",contains(region(J+"JPWS_exact_v4.json"),region(J+"JPWS_exact_v2x.json"))[0])
