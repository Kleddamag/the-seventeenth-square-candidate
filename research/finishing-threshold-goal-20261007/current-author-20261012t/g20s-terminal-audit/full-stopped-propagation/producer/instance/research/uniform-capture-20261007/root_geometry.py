#!/usr/bin/env python3
"""Endpoint formulae and retained first derivatives, generic in t and beta."""
from fractions import Fraction as F
import itertools
import bridge
import uniform as u

# normal=(axis index, sign) in the owner's frame, in our JSON labelling.
NORMALS={
 (1,3):(0,1),(1,5):(1,1),(2,6):(1,1),(3,13):(0,1),
 (5,9):(1,1),(5,11):(0,1),(6,14):(1,1),(7,10):(1,-1),
 (8,16):(1,-1),(9,10):(0,1),(10,12):(1,-1),(10,15):(0,1),
 (11,12):(0,1),(12,14):(1,-1),(12,16):(0,1),(13,14):(0,1),
 (14,17):(0,1),(15,16):(0,1),(16,17):(0,1)}


def geometry(t,beta):
    side,points,uv,vv=bridge.layout(t,beta)
    c,s=uv;d=(1-beta*beta)/(1+beta*beta);e=2*beta/(1+beta*beta)
    us=[(F(1),F(0))]*8+[(c,s)]*6+[(F(1),F(0)),(d,-e),(F(1),F(0))]
    axes=[(v,(-v[1],v[0])) for v in us]
    corners=[tuple(tuple((a*axis[0][k]+b*axis[1][k])/2 for k in (0,1))
                   for a,b in itertools.product((-1,1),repeat=2)) for axis in axes]
    H=[[u.zero(),u.zero()] for _ in range(17)];G=[[u.zero(),u.zero()] for _ in range(17)]
    for i in range(17):
        if i==3:
            continue
        if i in (10,12):
            parameter=21 if i==10 else 25;sign=-1 if i==10 else 1
            for k in (0,1):
                H[i][k][2*i]=axes[i][0][k];G[i][k][parameter]=sign*axes[i][1][k]
        elif i==1:
            G[i][0][2]=F(-1);H[i][1][3]=F(1)
        else:
            H[i][0][2*i]=F(1);H[i][1][2*i+1]=F(1)
    return side,points,axes,corners,H,G


def row(label,data):
    side,points,axes,corners,H,G=data
    fields=label.split(':');kind=fields[0]
    if kind=='wall':
        i,c,k,sign=map(int,fields[1:]);i-=1
        a=u.scaled(H[i][k],sign);a[34+i]=sign*u.p.turn(corners[i][c])[k]
        constant=sign*(points[i][k]+corners[i][c][k])
        if sign==-1:
            a[51]=F(1);constant+=side
        return a,constant,u.scaled(G[i][k],sign),None
    left,right=map(int,fields[1:3]);i,j=left-1,right-1
    owner=int(fields[3])-1 if kind=='pair' else i
    axis,normal_sign=NORMALS[left,right];n=tuple(normal_sign*x for x in axes[owner][axis])
    d=tuple(points[j][k]-points[i][k] for k in (0,1))
    hg=[u.add_vectors(H[j][k],u.scaled(H[i][k],-1)) for k in (0,1)]
    wg=[u.add_vectors(G[j][k],u.scaled(G[i][k],-1)) for k in (0,1)]
    a=u.add_vectors(*(u.scaled(hg[k],n[k]) for k in (0,1)))
    wn=u.add_vectors(*(u.scaled(wg[k],n[k]) for k in (0,1)))
    tau=u.p.dot(u.p.turn(n),d)
    tauw=u.add_vectors(*(u.scaled(wg[k],u.p.turn(n)[k]) for k in (0,1)))
    if kind=='pair':
        c=int(fields[4]);other=j if owner==i else i;v=corners[other][c]
        a[34+owner]+=tau+u.p.dot(n,u.p.turn(v))
        a[34+other]-=u.p.dot(n,u.p.turn(v))
        for w in u.PARAMETERS:
            a[u.PRODUCTS[w,34+owner]]+=tauw[w]
        constant=u.p.dot(n,d)-F(1,2)-u.p.dot(n,v)
        extra=dict(d=d,hg=hg,wg=wg,owner=owner,other=other)
    elif kind=='parallel':
        sign=int(fields[3])
        # These three axis-parallel offsets vanish as layout identities.
        if (left,right) in ((1,3),(1,5),(2,6)):
            tau=F(0)
        branch=-1 if (left,right)==(2,6) else 1
        kappa=(1-branch*tau)/2
        a[34+i]+=tau/2-sign*kappa;a[34+j]+=tau/2+sign*kappa
        for w in u.PARAMETERS:
            a[u.PRODUCTS[w,34+i]]+=tauw[w]*(1+sign*branch)/2
            a[u.PRODUCTS[w,34+j]]+=tauw[w]*(1-sign*branch)/2
        constant=u.p.dot(n,d)-1
        extra=dict(d=d,hg=hg,wg=wg,tau=tau,tauw=tauw,branch=branch,i=i,j=j)
    else:
        raise ValueError('unsupported row label')
    return a,constant,wn,extra


def tight_labels():
    # The numeric-looking cutoff only proposes a roster; identity checking and
    # independent owner-option certification are required before proof use.
    raw=[];u.model(u.initial_bounds(F(1,1000000),1),False,row_audit=raw)
    return [label for a,g,e,label in raw if not label.startswith('product')
            and abs(g)<F(1,10**15) and all(not a[w] for w in u.PARAMETERS)]
