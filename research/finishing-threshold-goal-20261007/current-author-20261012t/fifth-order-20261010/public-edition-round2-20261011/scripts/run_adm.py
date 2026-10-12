#!/usr/bin/env python3
if __name__ == '__main__' and not globals().get('_S17_PUBLIC_RUNNER_ACTIVE', False):
    raise SystemExit('Use replay_public.py for this check; outputs must be redirected.')
import sys, json, os
from adm import *
RIGID=[1,2,5,6,7,8,10,11,12,13,14,16]; LOOSE=[3,4,15,17]
sel=json.load(open(PK+"/SELECTED_ORIGINAL_MAP.json"))
SEL={}
for r in sel["rows"]:
    SEL[(r["root"],r["label"])]=r
man=json.load(open(PK+"/THEOREM_MANIFEST.json"))
BASE={r["name"]:r for r in man["base_capture_rows"]}
X0,X1,XW=F(-131,250),F(4501,5000),F(53,100)
Y0,YC,Y13,Y1=F(24137,10000),F(129,50),F(13,5),F(29637,10000)
G9LO,G9HI,KWHI=F(61301,200000),F(591183,1408817),F(44941,100000)
GT=F(1,20)
# wall lemma (own derivation): centre x < 53/100 in x>=0  =>  |theta| < 2 atan(31/1000) for the side direction in [-45,45] deg
tw=F(31,1000); assert (1+2*tw-tw*tw)*50 > 53*(1+tw*tw)
def basefile(name):
    r=BASE[name]; path=REPO+"/"+r["file"]
    assert sha(path)==r["sha256"],name
    return r["file"].split("join_design/")[-1], path
def spec(root):
    """label -> (polygon, dirspec, source)"""
    s={}
    def from_class(path,label,expect_sha=None):
        d,h=loadcls(path)
        if expect_sha: assert h==expect_sha,(path,h)
        nm,(poly,th)=target(d,label)
        return poly,th,os.path.basename(path)+":"+nm+" sha "+h[:16]
    if root=="JQ":
        for j in RIGID+LOOSE:
            poly,th,src=from_class(basefile("Q_%d"%j)[1],j); s[j]=(poly,("slot",th),src)
        s[9]=(rect(X0,XW,Y0,YC),("wall",),"L9 with x<=53/100, y<=129/50")
    elif root=="JPWS":
        for j in RIGID:
            poly,th,src=from_class(basefile("PW_%d"%j)[1],j); s[j]=(poly,("slot",th),src)
        sl=man["slab_capture"]; path=REPO+"/"+sl["file"]; assert sha(path)==sl["sha256"]
        poly,th,src=from_class(path,11); s[11]=(poly,("slot",th),src)
        for j in LOOSE:
            poly,th,src=from_class(basefile("Q_%d"%j)[1],j); s[j]=(poly,("slot",th),src)
        s[9]=(rect(X0,XW,YC,Y13),("wall",),"L9 with x<=53/100, 129/50<y<=13/5 (closure)")
    elif root=="JPW13":
        for j in RIGID:
            poly,th,src=from_class(basefile("PW_%d"%j)[1],j); s[j]=(poly,("slot",th),src)
        for j in LOOSE:
            poly,th,src=from_class(basefile("L_%d"%j)[1],j); s[j]=(poly,("slot",th),src)
        s[9]=(rect(X0,XW,Y13,Y1),("wall",),"L9 with x<=53/100, y>13/5 (closure)")
    elif root=="JG":
        for j in RIGID:
            poly,th,src=from_class(basefile("C_%d"%j)[1],j); s[j]=(poly,("slot",th),src)
        for j in (3,15,17):
            poly,th,src=from_class(basefile("L_%d"%j)[1],j); assert th==ALLDIR; s[j]=(poly,("gate",),src)
        poly,th,src=from_class(basefile("L_4")[1],4); s[4]=(poly,("slot",th),src)
        s[9]=(rect(XW,X1,Y0,Y1),("gate9",),"L9 with x>53/100 (closure), gate")
    else:
        for j in RIGID:
            r=SEL[(root,j)]; f=r["literal"]["file"]; path=f if f.startswith("/") else REPO+"/"+f
            assert REPO+"/"+r["root_binding"]["file"]==REPO+"/"+ROOTFILE[root]["file"] and r["root_binding"]["sha256"]==ROOTFILE[root]["sha256"]
            poly,th,src=from_class(path,j,r["literal"]["sha256"]); s[j]=(poly,("slot",th),src)
        d3=d17=d15=("free",)
        if root=="JPA": d9=("exit9",)
        else:
            d9=("gate9",)
            kind={"m":("below",),"p":("above",)}[root[-1]]
            if root.startswith("JPG3"): d3=kind
            elif root.startswith("JPG17"): d3=("gate",); d17=kind
            elif root.startswith("JPG15"): d3=("gate",); d17=("gate",); d15=kind
            else: raise SystemExit(root)
        for j,dk in ((3,d3),(17,d17),(15,d15)):
            poly,th,src=from_class(basefile("L_%d"%j)[1],j); assert th==ALLDIR; s[j]=(poly,dk,src)
        poly,th,src=from_class(basefile("L_4")[1],4); s[4]=(poly,("slot",th),src)
        s[9]=(rect(XW,X1,Y0,Y1),d9,"L9 with x>53/100 (closure)")
    return s
def check_root(root,fn=None,verbose=True):
    d,box,arc=loadroot(root,fn)
    s=spec(root)
    worst=None; fails=[]
    rows=[]
    for i in range(1,18):
        poly,dk,src=s[i]
        tr=transport(i,poly)
        if i==9 and dk[0]=="gate9":
            # support bound, own derivation: q_x >= (g+s)/2 for the side direction in the first quadrant, gate closed
            smin=min(sum(rot(G9LO)),sum(rot(G9HI)))/2
            assert rot(G9LO)[0]>0 and rot(G9LO)[1]>0 and rot(G9HI)[0]>0 and rot(G9HI)[1]>0
            tr[0]=(max(tr[0][0], smin-p[9][0]), tr[0][1])
        ms={}
        for k in (0,1):
            assert tr[k][0]<=tr[k][1],(root,i,k,"empty target?")
            ms["xi%d.lo"%(k+1)]=tr[k][0]-box[i][k][0]
            ms["xi%d.hi"%(k+1)]=box[i][k][1]-tr[k][1]
        A,B=arc[i]
        if dk[0]=="slot":
            a_lo,a_hi=dk[1]
            if (a_lo,a_hi)==ALLDIR: dk=("free",)
            else:
                if i==12:
                    assert a_lo>-RHO and a_hi<1   # only the marker's own representative in [0,45deg] can lie in the slot
                    a_hi=min(a_hi,RHO)
                m=interval_in_arc(a_lo,a_hi,(A,B))
                if m is None: ms["arc"]=F(-1)
                else: ms["arc.lo(sin)"]=m[1]; ms["arc.hi(sin)"]=m[2]; ms["_lift"]=m[0]
        if dk[0]=="free":
            ms["arc.free(-cos of length)"]=-dot(A,B)     # >= 0 iff the arc is at least a quarter turn
        elif dk[0]=="gate":
            D1,D2=rot(-GT),rot(GT); ms["arc.lo(sin)"]=cross(A,D1); ms["arc.hi(sin)"]=cross(D2,B)
            if not(in_arc(D1,(A,B)) and in_arc(D2,(A,B))): ms["arc"]=F(-1)
        elif dk[0]=="below":
            D1,D2=(F(1),F(-1)),rot(-GT); ms["arc.lo(unnorm)"]=cross(A,D1); ms["arc.hi(sin)"]=cross(D2,B)
            if not(in_arc(D1,(A,B)) and in_arc(D2,(A,B))): ms["arc"]=F(-1)
        elif dk[0]=="above":
            D1,D2=rot(GT),(F(1),F(1)); ms["arc.lo(sin)"]=cross(A,D1); ms["arc.hi(unnorm)"]=cross(D2,B)
            if not(in_arc(D1,(A,B)) and in_arc(D2,(A,B))): ms["arc"]=F(-1)
        elif dk[0]=="wall":
            D1,D2=rot(-tw),rot(tw); ms["arc.lo(sin)"]=cross(A,D1); ms["arc.hi(sin)"]=cross(D2,B)
            if not(in_arc(D1,(A,B)) and in_arc(D2,(A,B))): ms["arc"]=F(-1)
        elif dk[0] in ("gate9","exit9"):
            lo,hi=(G9LO,G9HI) if dk[0]=="gate9" else (G9HI,KWHI)
            m=interval_in_arc(lo,hi,(A,B))
            if m is None or m[0]!=0: ms["arc"]=F(-1)
            else: ms["arc.lo(sin)"]=m[1]; ms["arc.hi(sin)"]=m[2]
        for k,vv in ms.items():
            if k.startswith("_"): continue
            if vv<0: fails.append((i,k,float(vv),src))
            if worst is None or vv<worst[0]: worst=(vv,i,k)
        rows.append((i,src,ms))
    if verbose:
        for i,src,ms in rows:
            print("  %2d %-58s "%(i,src[:58])+" ".join("%s=%.3e"%(k.replace("(sin)","").replace("(unnorm)","*"),float(vv)) for k,vv in ms.items()))
    return worst,fails
if __name__=="__main__":
    roots=sys.argv[1:] or ["JQ","JPWS","JPW13","JG","JPA","JPG3m","JPG3p","JPG17m","JPG17p","JPG15m","JPG15p"]
    for r in roots:
        print("=====",r,ROOTFILE[r]["sha256"][:16])
        w,f=check_root(r)
        print("  smallest margin: %s = %.6e at label %d, %s"%(w[0],float(w[0]),w[1],w[2]))
        print("  FAILS:",f if f else "none")
