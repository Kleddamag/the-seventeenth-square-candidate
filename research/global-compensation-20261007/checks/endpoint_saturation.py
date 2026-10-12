#!/usr/bin/env python3
"""Replay the earlier exact endpoint member and resource saturation check."""
import os
from pathlib import Path
os.chdir(Path(__file__).resolve().parents[3])
import sys,json,math
from fractions import Fraction as F
import sympy as sp
sys.path.insert(0,'research/uniform-capture-20261007')
import bridge
root,_=bridge.root_enclosure()
t,b=sp.symbols('t b')
S,P,u,v=bridge.layout(t,b);c,s=u;d=(1-b*b)/(1+b*b);e=2*b/(1+b*b);T=c*(c+4-S)
P[12]=tuple(P[12][k]+T*v[k]/3 for k in (0,1))
P[3]=(S-sp.Rational(3,2),sp.Rational(1,2))
classes=[0]*8+[1]*6+[0,2,0];axes=[[(1,0),(0,1)],[(c,s),(-s,c)],[(d,-e),(e,d)]]
polys=[sum(sp.Integer(co)*t**a*b**bb for a,bb,co in poly) for poly in bridge.POLYNOMIALS]
cache={}
def interval(expr):
 expr=sp.cancel(expr)
 if expr in cache:return cache[expr]
 num,den=sp.fraction(expr)
 def ev(p):
  return sum((F(str(co))*root[0]**a*root[1]**bb for (a,bb),co in sp.Poly(p,t,b).terms()),bridge.I(0))
 z=ev(num)/ev(den);cache[expr]=z;return z
def zero(expr):
 num,den=sp.fraction(sp.cancel(expr))
 return any(sp.div(num,poly,t,b)[1]==0 for poly in polys)
def support(i,owner):
 a,bclass=classes[i],classes[owner]
 if a==bclass:return sp.Rational(1,2)
 return {(0,1):(c+s)/2,(0,2):(d+e)/2,(1,2):(c*d-s*e+c*e+s*d)/2}[tuple(sorted((a,bclass)))]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
positive=identities=0
for i in range(17):
 h=support(i,0)
 for z in [P[i][0]-h,S-P[i][0]-h,P[i][1]-h,S-P[i][1]-h]:
  val=interval(z)
  if val.lo>0:positive+=1
  else:assert zero(z);identities+=1
contacts=[]
for i in range(17):
 for j in range(i+1,17):
  options=[]
  for owner in [i,j]:
   for n in axes[classes[owner]]:
    for sign in [-1,1]:
     z=sign*dot(n,[P[j][k]-P[i][k] for k in [0,1]])-support(i,owner)-support(j,owner)
     bound=interval(z);options.append((bound.lo,z))
  lb,expr=max(options,key=lambda v:v[0])
  if lb>0:positive+=1
  else:assert zero(expr),(i,j,lb);identities+=1;contacts.append([i+1,j+1])
print('EXACT_ROOT_MEMBER_FEASIBLE','positive',positive,'zero identities',identities,'contacts',contacts,flush=True)
D=json.load(open('upper-packing-certificate.json'));U=F(D['side'])
pose_err=max((interval(P[i][k])-F(D['squares'][i][['x','y'][k]])).absolute_upper() for i in range(17) for k in [0,1])
side_err=(interval(S)-U).absolute_upper()
axis_err=F(0)
for i in range(17):
 tt=F(D['squares'][i]['t']);actual=((1-tt*tt)/(1+tt*tt),2*tt/(1+tt*tt))
 axis_err=max(axis_err,*[(interval(axes[classes[i]][0][k])-actual[k]).absolute_upper() for k in [0,1]])
assert pose_err<F(1,10**15) and side_err<F(1,10**15) and axis_err<F(1,10**50)
print('root/source errors',float(pose_err),float(side_err),float(axis_err),flush=True)
C=json.load(open('bounds/4.6601/certificate.json'));CD=C['coordinate_denominator'];LD=4613*CD//1000
pts=[]
for x,y,_ in C['point_orbits']:pts+=sorted({(a,b) for u,v in [(x,y),(y,x)] for a in [u,LD-u] for b in [v,LD-v]})
pf=U.numerator*1000;pd=U.denominator*CD*4613
hit=[];minmargin=F(1)
for square in D['squares']:
 x,y,t=map(F,[square['x'],square['y'],square['t']]);cm=math.lcm(x.denominator,y.denominator)
 dx0=x.numerator*pd*(cm//x.denominator);dy0=y.numerator*pd*(cm//y.denominator)
 aa=t.denominator*t.denominator-t.numerator*t.numerator;bb=2*t.numerator*t.denominator;dd=t.denominator*t.denominator+t.numerator*t.numerator
 den=dd*pd*cm;row=[]
 for xx,yy in pts:
  dx=xx*pf*cm-dx0;dy=yy*pf*cm-dy0
  a=2*abs(aa*dx+bb*dy);bval=2*abs(-bb*dx+aa*dy)
  gap=min(abs(den-a),abs(den-bval))
  assert gap*10**9>2*den
  row.append(a<den and bval<den)
 hit.append(row)
features=[];saturated=[];fixed=[]
for ri,r in enumerate(C['threshold_orbits']):
 for ii,ids in enumerate(r['sets']):
  owners=[]
  for i,row in enumerate(hit):
   if r.get('winning_masks'):
    mask=sum(1<<j for j,k in enumerate(ids) if row[k]);win=any(mask&m==m for m in r['winning_masks'])
   else:win=sum(co for k,co in zip(ids,r.get('coefficients',[1]*len(ids))) if row[k])>=r['threshold']
   if win:owners.append(i+1)
  assert len(owners)<=1
  if owners:saturated.append((ri,ii,owners[0]))
  if owners and owners[0] not in [2,4,11,13]:fixed.append((ri,ii,owners[0]))
print('EXACT_SATURATION','resources',sum(len(r['sets']) for r in C['threshold_orbits']),'saturated',len(saturated),'fixed-owner',len(fixed),'all site boundary distances >1e-9; root transfer error <1e-14')

