#!/usr/bin/env python3
"""Uniform all-scales local rigidity certificate at the algebraic root.

An accepted certificate forces ||h||_infinity=0 by bounding h/||h|| strictly
inside the unit cube. The slider box is never subdivided. Exact symbolic
layout identities use SymPy; interval and LP certificate arithmetic use Fraction.
"""
import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import bridge
import root_geometry as g
import uniform as u

I=bridge.I
PAD=F(1,10**12)


def initial():
    bounds=u.initial_bounds(F(1),1)
    bounds[51]=(F(-1),F(0))
    for w in u.PARAMETERS:
        lo,hi=bounds[w];bounds[w]=(lo if w==2 else lo-PAD,hi+PAD)
    return u.refresh_products(bounds)


def interval(vector,bounds):
    return sum((I(a)*I(lo,hi) for a,(lo,hi) in zip(vector,bounds)),I(0))


def radius(vector,bounds):
    return interval(vector,bounds).absolute_upper()


def symbolic_identities(root,labels):
    import sympy as s
    t,b=s.symbols('t beta');data=g.geometry(t,b)
    polys=[sum(s.Integer(c)*t**a*b**d for a,d,c in p) for p in bridge.POLYNOMIALS]
    records=[]
    for label in labels:
        _,constant,w,_=g.row(label,data)
        num,den=s.fraction(s.cancel(constant))
        accepted=False
        for p in polys:
            quotient,remainder=s.div(num,p,t,b)
            if remainder==0:
                accepted=True;break
        if not accepted:
            raise ValueError('unproved contact identity: '+label)
        di=sum((F(str(coefficient))*root[0]**a*root[1]**d
                for (a,d),coefficient in s.Poly(den,t,b).terms()),I(0))
        if di.lo<=0<=di.hi:
            raise ValueError('layout identity denominator crosses zero')
        if any(s.cancel(w[k])!=0 for k in u.PARAMETERS):
            raise ValueError('retained row not invariant under sliders')
        records.append(dict(label=label,numerator=str(num),denominator=str(den)))
    _,points,axes,_,_,_=data
    for i,j in ((0,2),(0,4),(1,5)):
        axis,sign=g.NORMALS[i+1,j+1];n=tuple(sign*x for x in axes[i][axis])
        if s.cancel(u.p.dot(u.p.turn(n),tuple(points[j][k]-points[i][k] for k in (0,1))))!=0:
            raise ValueError('axis-face offset identity failed')
    return dict(status='PASS',identities=len(records),records=records)


def option_audit(data,epsilon,labels):
    _,points,axes,corners,H,G=data;bounds=initial();outcomes=[]
    for left,right in u.PAIRS:
        i,j=left-1,right-1
        d=tuple(points[j][k]-points[i][k] for k in (0,1))
        hg=[u.add_vectors(H[j][k],u.scaled(H[i][k],-1)) for k in (0,1)]
        wg=[u.add_vectors(G[j][k],u.scaled(G[i][k],-1)) for k in (0,1)]
        D=u.p.norm_upper(tuple((I(d[k])+interval(wg[k],bounds)).absolute_upper() for k in (0,1)))
        dr=u.p.norm_upper(tuple(radius(hg[k],bounds) for k in (0,1)))
        alive=[]
        for owner,other in ((i,j),(j,i)):
            for axis_number,axis in enumerate(axes[owner]):
                for sign in (-1,1):
                    n=tuple(sign*x for x in axis)
                    projection=u.add_vectors(*(u.scaled(wg[k],n[k]) for k in (0,1)))
                    support=max(I(u.p.dot(n,v)).lo for v in corners[other])
                    upper=(I(u.p.dot(n,d))+interval(projection,bounds)).hi+epsilon*dr-F(1,2)-support+(D+epsilon*dr)*epsilon+2*epsilon
                    if upper>=0:
                        alive.append((owner,axis_number,sign))
        pair_label=f'pair:{left}:{right}:'
        matching=[label for label in labels if label.startswith(pair_label)]
        axis,sign=g.NORMALS[left,right]
        expected=[(int(matching[0].split(':')[3])-1,axis,sign)] if matching else [(i,axis,sign),(j,axis,sign)]
        if sorted(alive)!=sorted(expected):
            raise ValueError(f'owner options not forced: {(left,right)} {alive} != {expected}')
        outcomes.append(dict(pair=[left,right],retained=alive))
    return outcomes


def model(bounds,epsilon,data,labels):
    rows=[];radii=[max(abs(lo),abs(hi)) for lo,hi in bounds]
    def append(a,error,label):
        aq=[];loss=F(0)
        for value,r in zip(a,radii):
            enclosure=I(value);middle=F(round((enclosure.lo+enclosure.hi)*u.GRID/2),u.GRID)
            aq.append(middle);loss+=max(abs(middle-enclosure.lo),abs(middle-enclosure.hi))*r
        b=F(((-error-loss)*u.GRID).__floor__(),u.GRID)
        rows.append(dict(a=list(map(str,aq)),b=str(b),label=label))
    for label in labels:
        a,_,_,extra=g.row(label,data)
        if label.startswith('wall'):
            angle=34+int(label.split(':')[1])-1
            error=epsilon*radii[angle]**2/2
        else:
            d,hg,wg=extra['d'],extra['hg'],extra['wg']
            D=u.p.norm_upper(tuple((I(d[k])+interval(wg[k],bounds)).absolute_upper() for k in (0,1)))
            dr=u.p.norm_upper(tuple(radius(hg[k],bounds) for k in (0,1)))
            if label.startswith('pair'):
                own,other=34+extra['owner'],34+extra['other']
                wo=radii[own];eta=radii[own]+radii[other]
                error=epsilon*(D*wo*wo/2+wo*dr+eta*eta/2)
            else:
                i,j=extra['i'],extra['j'];M=(radii[34+i]+radii[34+j])/2;Q=M
                tau=I(extra['tau'])+interval(extra['tauw'],bounds)
                if (extra['branch']==1 and tau.lo<0) or (extra['branch']==-1 and tau.hi>0) or tau.absolute_upper()>=1:
                    raise ValueError('parallel offset leaves its branch')
                error=(epsilon*(D*M*M/2+M*dr+Q*Q/2)
                       +epsilon**2*(Q**3/6+tau.absolute_upper()*Q**3)
                       +(D*M+dr)*(epsilon*Q+epsilon**3*Q**3))
        append(a,error,label)
    # These rows use the normalized angle and product coordinates directly.
    for (w,angle),index in u.PRODUCTS.items():
        l,h=bounds[w];L,U=bounds[angle]
        for wa,aa,qa,c in ((-L,-l,1,l*L),(-U,-h,1,h*U),(L,h,-1,-h*L),(U,l,-1,-l*U)):
            a=u.zero();a[w]=wa;a[angle]=aa;a[index]=F(qa)
            append(a,c,f'product:{w}:{angle}:{qa}:{wa}:{aa}')
    return rows


def solve_round(bounds,epsilon,data,labels):
    import numpy as np
    from scipy.optimize import linprog
    rows=model(bounds,epsilon,data,labels);parsed=u.parse_exact_rows(rows)
    A=np.array([[float(F(a)) for a in row['a']] for row in rows]);b=np.array([float(F(row['b'])) for row in rows])
    output=list(bounds);results=[]
    for coordinate in u.CORE+(51,):
        for sign in (-1,1):
            c=np.zeros(u.DIMENSION);c[coordinate]=sign
            fit=linprog(c,A_ub=-A,b_ub=-b,bounds=[(float(lo),float(hi)) for lo,hi in bounds],method='highs')
            if not fit.success:
                raise RuntimeError(f'LP proposal failed: {fit.message}')
            weights={str(i):str(F(round(max(0,-v)*u.WEIGHT_GRID),u.WEIGHT_GRID)) for i,v in enumerate(fit.ineqlin.marginals) if -v>1e-12}
            value=u.exact_dual(rows,bounds,coordinate,sign,weights,parsed)
            results.append(dict(coordinate=coordinate,sign=sign,weights=weights,bound=str(value)))
            lo,hi=output[coordinate];output[coordinate]=(max(lo,value),hi) if sign==1 else (lo,min(hi,-value))
    return u.refresh_products(u.p.outward(output[:52])),dict(model_sha256=hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),results=results)


def check(path):
    cert=json.loads(path.read_text());epsilon=F(cert['epsilon'])
    if cert['schema']!='s17-uniform-rigidity-v1' or not 0<epsilon<=F(1,1000) or not cert['steps']:
        raise ValueError('invalid rigidity certificate')
    root,root_receipt=bridge.root_enclosure();labels=g.tight_labels();identities=symbolic_identities(root,labels)
    data=g.geometry(*root);options=option_audit(data,epsilon,labels);bounds=initial()
    for step in cert['steps']:
        rows=model(bounds,epsilon,data,labels);parsed=u.parse_exact_rows(rows)
        if step['model_sha256']!=hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest():
            raise ValueError('model mismatch')
        seen=set();updated=list(bounds)
        for result in step['results']:
            i,sign=result['coordinate'],result['sign']
            if (i,sign) in seen:
                raise ValueError('duplicate objective')
            seen.add((i,sign));value=u.exact_dual(rows,bounds,i,sign,result['weights'],parsed)
            if value!=F(result['bound']):
                raise ValueError('wrong dual bound')
            lo,hi=updated[i];updated[i]=(max(lo,value),hi) if sign==1 else (lo,min(hi,-value))
        if seen!={(i,s) for i in u.CORE+(51,) for s in (-1,1)}:
            raise ValueError('missing objective')
        bounds=u.refresh_products(u.p.outward(updated[:52]))
        if any(lo>hi for lo,hi in bounds):
            raise ValueError('empty interval')
    if cert['final_bounds']!=[[str(lo),str(hi)] for lo,hi in bounds]:
        raise ValueError('final bounds mismatch')
    ratio=max(max(abs(x) for x in bounds[i]) for i in u.CORE)
    if ratio>=1:
        raise ValueError('strict contraction not established')
    return dict(status='PASS',certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),epsilon=str(epsilon),
                rounds=len(cert['steps']),objectives=92*len(cert['steps']),ratio=str(ratio),ratio_decimal=float(ratio),
                identities=identities['identities'],pairs=len(options),
                conclusion='Uniform local rigidity on the declared padded slider box, assuming the analytic normalized remainder derivation.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--epsilon',default='1/5000');parser.add_argument('--rounds',type=int,default=15)
    parser.add_argument('--output',type=Path);parser.add_argument('--check',type=Path)
    args=parser.parse_args()
    if args.check:
        print(json.dumps(check(args.check),indent=2));return
    if args.output is None:
        parser.error('--output required')
    epsilon=F(args.epsilon);root,_=bridge.root_enclosure();labels=g.tight_labels()
    identities=symbolic_identities(root,labels);data=g.geometry(*root);options=option_audit(data,epsilon,labels)
    bounds=initial();steps=[];history=[]
    for number in range(1,args.rounds+1):
        bounds,step=solve_round(bounds,epsilon,data,labels);steps.append(step)
        ratio=max(max(abs(x) for x in bounds[i]) for i in u.CORE)
        record=dict(round=number,ratio=float(ratio));history.append(record);print(json.dumps(record),flush=True)
        cert=dict(schema='s17-uniform-rigidity-v1',epsilon=str(epsilon),steps=steps,history=history,
                  final_bounds=[[str(lo),str(hi)] for lo,hi in bounds])
        args.output.write_text(json.dumps(cert,indent=2)+'\n')
        if ratio<F(9,10):
            break


if __name__=='__main__':
    main()
