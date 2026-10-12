#!/usr/bin/env python3
"""Independent exact polynomial reconstruction; no producer imports or optimizer.
Adapted from the accepted wider-contraction polynomial auditor. This version uses
only the 48 slider-angle lifts and the finite uniform radius-based parallel bound.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product as cartesian
from math import isqrt
import json
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'local-research/claude-20261002/results/rerun_trees_20261011/SHA256_G20S_HW.txt').is_file())
G=HERE.parents[1]
def require(x,why):
    if not x: raise ValueError(why)
PAIRS=((1,3),(1,5),(2,6),(3,13),(5,9),(5,11),(6,14),(7,10),(8,16),
       (9,10),(10,12),(10,15),(11,12),(12,14),(12,16),(13,14),(14,17),(15,16),(16,17))
SLIDERS=(2,21,25)
DUMMY=(6,7,37)
ANGLES=tuple(34+i for i in range(17) if i!=3)
CORE=tuple(i for i in range(51) if i not in SLIDERS+DUMMY)
GRID=10**15
ZERO=F(0)

# Sparse real polynomials: a sorted monomial tuple maps to a rational coefficient.
def clean(p): return {k:F(v) for k,v in p.items() if v}
def const(v): return {():F(v)} if v else {}
def var(i): return {(i,):F(1)}
def add(*ps):
    out={}
    for p in ps:
        for mon,v in p.items(): out[mon]=out.get(mon,ZERO)+v
    return clean(out)
def scale(p,v): return clean({m:c*v for m,c in p.items()})
def mul(p,q):
    out={}
    for a,x in p.items():
        for b,y in q.items():
            m=tuple(sorted(a+b));out[m]=out.get(m,ZERO)+x*y
    return clean(out)
def coredegree(mon): return sum(i not in SLIDERS for i in mon)
def trunc(p,n): return {m:c for m,c in p.items() if coredegree(m)<=n}
def dot(a,b): return sum((x*y for x,y in zip(a,b)),ZERO)
def turn(a): return (-a[1],a[0])
def pdot(a,b): return add(*(scale(v,c) for c,v in zip(a,b)))
def norm(v):
    t=dot(v,v)*10**18;k=isqrt(t.numerator//t.denominator)
    if F(k*k)<t:k+=1
    require(F(k*k)>=t,'norm enclosure')
    return F(k,10**9)
def rotate_poly(v,t):
    t2=mul(t,t)
    return tuple(add(const(v[k]),scale(t,turn(v)[k]),scale(t2,-v[k]/2)) for k in (0,1))
def pdot2(a,b): return add(*(mul(x,y) for x,y in zip(a,b)))
def dense(p):
    a=[ZERO]*DIM
    for mon,c in p.items():
        if len(mon)==1: a[mon[0]]+=c
        elif len(mon)==2: a[PRODUCTS[mon]]+=c
        elif mon: raise ValueError('unlifted monomial '+str(mon))
    return a

# Geometry is read from the pinned rational source, not the producer geometry().
raw=json.loads((G/'full-gate/producer/instance/upper-packing-certificate.json').read_text())
side=F(raw['side']);points=[];axes=[];corners=[]
for sq in raw['squares']:
    points.append((F(sq['x']),F(sq['y'])))
    t=F(sq['t']);n=((1-t*t)/(1+t*t),2*t/(1+t*t));v=turn(n)
    require(dot(n,n)==1 and dot(n,v)==0,'axes not orthonormal')
    axes.append((n,v));corners.append(tuple(tuple((a*n[k]+b*v[k])/2 for k in (0,1)) for a,b in cartesian((-1,1),repeat=2)))
c,s=axes[8][0];T=c*(c+4-side)
points[12]=tuple(points[12][k]-T*axes[12][1][k]/3 for k in (0,1))
H=[];G=[]
for i in range(17):
    if i==3:h=({},{});g=({},{})
    elif i==1:h=({},var(3));g=(scale(var(2),-1),{})
    elif i in (10,12):
        w=21 if i==10 else 25;sign=-1 if i==10 else 1
        h=tuple(scale(var(2*i),x) for x in axes[i][0]);g=tuple(scale(var(w),sign*x) for x in axes[i][1])
    else:h=(var(2*i),var(2*i+1));g=({},{})
    H.append(h);G.append(g)
PRODUCTS={k:52+j for j,k in enumerate(cartesian(SLIDERS,ANGLES))}
DIM=100
def box(p,bounds):
    lo=hi=p.get((),ZERO)
    for mon,c in p.items():
        if not mon:continue
        require(len(mon)==1,'box on nonlinear polynomial')
        l,u=bounds[mon[0]];lo+=c*(l if c>=0 else u);hi+=c*(u if c>=0 else l)
    return lo,hi
def lifted(p):
    out={}
    for m,c in p.items():
        k=(PRODUCTS[m],) if len(m)==2 else m
        require(len(k)<=1,'nonlinear polynomial after lifting')
        out[k]=out.get(k,ZERO)+c
    return clean(out)
def interval(p,bounds,relations=None):
    return box(lifted(p),bounds)
def refreshed(bounds):
    out=list(bounds[:52])+[(ZERO,ZERO)]*48
    for (a,b),i in PRODUCTS.items():
        vals=[x*y for x,y in cartesian(bounds[a],bounds[b])]
        out[i]=(min(vals),max(vals))
    return out
def initial(stopped=True):
    out=[(-F(1,200),F(1,200))]*34+[(-F(1,400),F(1,400))]*17+[(F(-1,50),ZERO)]
    for i in DUMMY: out[i]=(ZERO,ZERO)
    for i,b in zip(SLIDERS,((ZERO,F(8,25)),(F(-1,20),F(1,5)),(F(-1,5),F(3,40)))): out[i]=b
    if stopped:
        out[21]=(F(-213,25000),F(1,5));out[25]=(F(-1,5),F(33,1000))
    return refreshed(out)
def rounded_pair(pair):
    return F((pair[0]*GRID).__floor__(),GRID),F((pair[1]*GRID).__ceil__(),GRID)
def independent_model(bounds,relations=None):
    rad=[max(abs(lo),abs(hi)) for lo,hi in bounds]
    require(max(rad[i] for i in ANGLES)<=F(1,10),'angle lemma domain exceeded')
    I=lambda p:interval(p,bounds,relations)
    R=lambda p:max(abs(x) for x in I(p))
    rows=[];raw_rows=[];normals={};options=[];parallel_bounds=[]
    stats=dict(unique_pairs=0,parallel_pairs=0,omitted_pairs=0,sign_crossings=[])
    def append(p,error,label,keep=False):
        a=dense(p);aq=[F(round(v*GRID),GRID) for v in a]
        loss=sum((abs(x-y)*r for x,y,r in zip(a,aq,rad)),ZERO)
        b=F(((-p.get((),ZERO)-error-loss)*GRID).__floor__(),GRID)
        rows.append(dict(a=list(map(str,aq)),b=str(b),label=label))
        if keep:raw_rows.append((p,error,label))
    def support(p):
        # Substitute each slider vertex into the polynomial before maximizing.
        vals=[]
        for vertex in cartesian(*(bounds[w] for w in SLIDERS)):
            fixed=dict(zip(SLIDERS,vertex));reduced={}
            for mon,c in p.items():
                m=[]
                for i in mon:
                    if i in fixed:c*=fixed[i]
                    else:m.append(i)
                key=tuple(m);reduced[key]=reduced.get(key,ZERO)+c
            vals.append(I(clean(reduced))[1])
        return max(vals)
    def envelope(coefficient,p):
        lo,hi=I(p)
        if coefficient>=0:return [add(scale(p,coefficient*(lo+hi)),const(-coefficient*lo*hi))]
        return [add(scale(p,2*coefficient*t),const(-coefficient*t*t)) for t in sorted({ZERO,(lo+hi)/2})]
    def pair_parts(i,j,n):
        d=tuple(points[j][k]-points[i][k] for k in (0,1))
        h=tuple(add(H[j][k],scale(H[i][k],-1)) for k in (0,1))
        w=tuple(add(G[j][k],scale(G[i][k],-1)) for k in (0,1))
        D=norm(tuple(max(abs(d[k]+x) for x in I(w[k])) for k in (0,1)))
        dr=norm(tuple(R(p) for p in h))
        return d,h,w,D,dr
    def corner_polynomials(i,j,o,t,n,v):
        d,h,w,D,dr=pair_parts(i,j,n)
        theta=var(34+o);eta=add(var(34+t),scale(theta,-1))
        delta=tuple(add(const(d[k]),h[k],w[k]) for k in (0,1))
        exact2=trunc(add(pdot2(rotate_poly(n,theta),delta),const(F(-1,2)),scale(pdot(n,rotate_poly(v,eta)),-1)),2)
        linear=trunc(exact2,1)
        tangent=pdot(turn(n),h);wn=pdot(n,w)
        # Replace the varying coefficient of theta^2 by its whole-box supremum.
        cmax=-(dot(n,d)+I(wn)[0])/2
        shared=add(exact2,scale(mul(wn,mul(theta,theta)),F(1,2)),scale(mul(theta,theta),-I(wn)[0]/2))
        E1=D*rad[34+o]**2/2+rad[34+o]*dr+norm(v)*R(eta)**2/2
        E2=D*rad[34+o]**3/6+dr*rad[34+o]**2/2+norm(v)*R(eta)**3/6
        ans=[(linear,E1)]
        yl,yu=I(tangent);wl,wu=bounds[34+o]
        prods=[add(scale(tangent,wu),scale(theta,yl),const(-wu*yl)),add(scale(tangent,wl),scale(theta,yu),const(-wl*yu))]
        for qo,qr,qp in cartesian(envelope(cmax,theta),envelope(dot(n,v)/2,eta),prods):ans.append((add(linear,qo,qr,qp),E2))
        return ans,shared,E2
    for i in range(17):
        if i==3:continue
        for c,v in enumerate(corners[i]):
            rotated=rotate_poly(v,var(34+i))
            for k in (0,1):
                for sign in (-1,1):
                    wall=scale(add(const(points[i][k]),H[i][k],G[i][k],rotated[k]),sign)
                    if sign==-1:wall=add(wall,const(side),var(51))
                    append(trunc(wall,1),norm(v)*rad[34+i]**2/2,f'wall:{i+1}:{c}:{k}:{sign}',True)
    for left,right in PAIRS:
        i,j=left-1,right-1;alive=[]
        for o,t in ((i,j),(j,i)):
            for axis in axes[o]:
                for sign in (-1,1):
                    n=tuple(sign*x for x in axis);d,h,w,D,dr=pair_parts(i,j,n)
                    coarse=dot(n,d)+I(pdot(n,tuple(add(h[k],w[k]) for k in (0,1))))[1]-F(1,2)-max(dot(n,v) for v in corners[t])+(D+dr)*rad[34+o]+rad[34+o]+rad[34+t]
                    row=dict(pair=[left,right],owner=o+1,normal=list(map(str,n)),coarse=str(coarse))
                    if coarse<0:row['status']='excluded_coarse';options.append(row);continue
                    all_exp=[];excluded=False
                    for v in corners[t]:
                        expansions,_,_=corner_polynomials(i,j,o,t,n,v);all_exp.append(expansions)
                        upper=min(support(p)+error for p,error in expansions)
                        if upper<0:row.update(status='excluded_corner',corner_upper=str(upper));excluded=True;break
                    if not excluded:row['status']='alive';alive.append((o,t,n,all_exp))
                    options.append(row)
        if len(alive)==1:
            stats['unique_pairs']+=1;o,t,n,expansions=alive[0];normals[(left,right,o+1)]=n
            for c,alternatives in enumerate(expansions):
                for k,(p,error) in enumerate(alternatives):append(p,error,f'pair:{left}:{right}:{o+1}:{c}:{k}',True)
        elif len(alive)==2 and alive[0][0]!=alive[1][0] and alive[0][2]==alive[1][2]:
            n=alive[0][2];d,h,w,D,dr=pair_parts(i,j,n);tau=dot(turn(n),d);tauw=pdot(turn(n),w)
            taulo,tauhi=[tau+x for x in I(tauw)]
            if taulo>=0:branch=1
            elif tauhi<=0:branch=-1
            else:stats['sign_crossings'].append([left,right]);stats['omitted_pairs']+=1;continue
            taumax=max(abs(taulo),abs(tauhi))
            if taumax>=1:stats['omitted_pairs']+=1;continue
            stats['parallel_pairs']+=1;normals[left,right,0]=n
            m=scale(add(var(34+i),var(34+j)),F(1,2));q=scale(add(var(34+j),scale(var(34+i),-1)),F(1,2));M=Q=(rad[34+i]+rad[34+j])/2
            error=D*M*M/2+M*dr+Q*Q/2+Q**3/6+taumax*Q**3+(D*M+dr)*(Q+Q**3)
            for sign in (-1,1):
                p=add(const(dot(n,d)-1),pdot(n,tuple(add(h[k],w[k]) for k in (0,1))),mul(add(const(tau),tauw),m),scale(mul(add(const(1-branch*tau),scale(tauw,-branch)),q),sign))
                append(p,error,f'parallel:{left}:{right}:{sign}',True)
        else:stats['omitted_pairs']+=1
    for (x,y),index in PRODUCTS.items():
        lo,hi=bounds[x];L,U=bounds[y]
        factors=[(add(var(x),const(-lo)),add(var(y),const(-L)),f'product:{x}:{y}:1:{-L}:{-lo}'),
                 (add(const(hi),scale(var(x),-1)),add(const(U),scale(var(y),-1)),f'product:{x}:{y}:1:{-U}:{-hi}'),
                 (add(const(hi),scale(var(x),-1)),add(var(y),const(-L)),f'product:{x}:{y}:-1:{L}:{hi}'),
                 (add(var(x),const(-lo)),add(const(U),scale(var(y),-1)),f'product:{x}:{y}:-1:{U}:{lo}')]
        for a,b,label in factors: append(mul(a,b),ZERO,label)
    extra=[ZERO]*DIM;extra[21]=extra[25]=F(-1)
    rows.append(dict(a=list(map(str,extra)),b='-49/2000',label='accepted-physical-stop:minus-b-z'))
    require(len(options)==152,'all SAT directions required')
    return rows,stats,options
