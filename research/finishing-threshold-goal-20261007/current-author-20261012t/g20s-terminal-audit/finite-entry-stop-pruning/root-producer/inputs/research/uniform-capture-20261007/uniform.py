#!/usr/bin/env python3
"""Uniform slider-box experiment with shared angle-times-slide variables.

The base geometry is rational; this is not the algebraic endpoint theorem.
"""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('capture_pilot', HERE.parent/'joint-capture-20261007/pilot.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

PAIRS = ((1,3),(1,5),(2,6),(3,13),(5,9),(5,11),(6,14),(7,10),(8,16),
         (9,10),(10,12),(10,15),(11,12),(12,14),(12,16),(13,14),(14,17),(15,16),(16,17))
PARAMETERS = (2,21,25)  # a, b, z in the upstream moving-family convention
DUMMY = (6,7,37)       # Square 4 is entirely dropped, including its walls.
ANGLES = tuple(34+i for i in range(17) if i != 3)
PRODUCTS = {(w,angle):52+k for k,(w,angle) in enumerate(itertools.product(PARAMETERS,ANGLES))}
DIMENSION = 52+len(PRODUCTS)
CORE = tuple(i for i in range(51) if i not in PARAMETERS+DUMMY)
GRID = 10**15
WEIGHT_GRID = 10**10


def zero():
    return [F(0)]*DIMENSION


def unit(i):
    v=zero();v[i]=F(1);return v


def add_vectors(*vectors):
    return [sum(values,F(0)) for values in zip(*vectors)]


def scaled(v,a):
    return [a*x for x in v]


def geometry():
    p.PROFILE='boundary'
    side,points,axes,corners=p.reference()
    c,s=axes[8][0]
    T=c*(c+4-side)
    points[12]=tuple(points[12][k]-T*axes[12][1][k]/3 for k in (0,1))
    # Physical centre = reference + H*h + G*w. Parameter motion is kept
    # out of h and hence out of the small-displacement Taylor remainder.
    H=[[zero(),zero()] for _ in range(17)]
    G=[[zero(),zero()] for _ in range(17)]
    for i in range(17):
        if i==3:
            continue
        if i in (10,12):
            core_index=2*i
            parameter=21 if i==10 else 25
            sign=-1 if i==10 else 1
            for k in (0,1):
                H[i][k][core_index]=axes[i][0][k]
                G[i][k][parameter]=sign*axes[i][1][k]
        elif i==1:
            G[i][0][2]=F(-1)
            H[i][1][3]=F(1)
        else:
            H[i][0][2*i]=F(1)
            H[i][1][2*i+1]=F(1)
    return side,points,axes,corners,H,G


def initial_bounds(radius, angle_factor, parameter_scale=F(1)):
    bounds=[(-radius,radius)]*34+[(-angle_factor*radius,angle_factor*radius)]*17+[(F(-1,50),F(0))]
    for i in DUMMY:
        bounds[i]=(F(0),F(0))
    for i,interval in zip(PARAMETERS,((F(0),F(1,4)),(F(-1,2500),F(1,12)),(F(-1,8),F(1,16)))):
        bounds[i]=tuple(parameter_scale*x for x in interval)
    return refresh_products(bounds)


def refresh_products(bounds):
    result=list(bounds[:52])+[(F(0),F(0))]*len(PRODUCTS)
    for (w,angle),index in PRODUCTS.items():
        values=[x*y for x,y in itertools.product(result[w],result[angle])]
        result[index]=(min(values),max(values))
    return result


def model(bounds, curvature=True, shared=True, audit=None, interval_provider=None, row_audit=None):
    side,points,axes,corners,H,G=geometry()
    radii=[max(abs(a),abs(b)) for a,b in bounds]
    if max(radii[i] for i in ANGLES)>F(1,10):
        raise ValueError('angle radius too large')
    vertices=list(itertools.product(*(bounds[w] for w in PARAMETERS)))
    stats=dict(unique_pairs=0,parallel_pairs=0,omitted_pairs=0,sign_crossings=[])
    rows=[]

    def interval(v):
        return (interval_provider(v) if interval_provider is not None
                else p.box_interval(v,bounds))

    def radius(v):
        return max(abs(x) for x in interval(v))

    def true_support(a):
        # A is linear in the lifted variables. Substitution q=w*omega is
        # multi-affine: its maximum is attained at parameter-box vertices,
        # with all remaining scalar variables at appropriate endpoints.
        maxima=[]
        for vertex in vertices:
            reduced=list(a)
            fixed=F(0)
            for w,value in zip(PARAMETERS,vertex):
                fixed+=reduced[w]*value
                reduced[w]=F(0)
                for angle in ANGLES:
                    index=PRODUCTS[w,angle]
                    reduced[angle]+=reduced[index]*value
                    reduced[index]=F(0)
            maxima.append(fixed+interval(reduced)[1])
        return max(maxima)

    def row(a,g0,error,label):
        if row_audit is not None:
            row_audit.append((a,g0,error,label))
        aq=[F(round(x*GRID),GRID) for x in a]
        loss=sum((abs(x-y)*r for x,y,r in zip(a,aq,radii)),F(0))
        b=F(((-g0-error-loss)*GRID).__floor__(),GRID)
        rows.append(dict(a=[str(x) for x in aq],b=str(b),label=label))

    def with_product(a,coefficient,w,angle):
        a[PRODUCTS[w,angle]]+=coefficient

    def quadratic(coefficient,v):
        lo,hi=interval(v)
        if coefficient>=0:
            return [(scaled(v,coefficient*(lo+hi)),-coefficient*lo*hi)]
        return [(scaled(v,2*coefficient*t),-coefficient*t*t)
                for t in sorted(set((F(0),(lo+hi)/2)))]

    def corner_terms(i,j,owner,other,n,v):
        d=tuple(points[j][k]-points[i][k] for k in (0,1))
        hg=[add_vectors(H[j][k],scaled(H[i][k],-1)) for k in (0,1)]
        wg=[add_vectors(G[j][k],scaled(G[i][k],-1)) for k in (0,1)]
        dn=add_vectors(*(scaled(hg[k],n[k]) for k in (0,1)))
        wn=add_vectors(*(scaled(wg[k],n[k]) for k in (0,1)))
        tangent=add_vectors(*(scaled(hg[k],p.turn(n)[k]) for k in (0,1)))
        wtangent=add_vectors(*(scaled(wg[k],p.turn(n)[k]) for k in (0,1)))
        own,other_angle=34+owner,34+other
        eta=add_vectors(unit(other_angle),scaled(unit(own),-1))
        a=add_vectors(dn,wn)
        a[own]+=p.dot(p.turn(n),d)+p.dot(n,p.turn(v))
        a[other_angle]-=p.dot(n,p.turn(v))
        for w in PARAMETERS:
            with_product(a,wtangent[w],w,own)
        g0=p.dot(n,d)-F(1,2)-p.dot(n,v)
        dr=p.norm_upper((radius(hg[0]),radius(hg[1])))
        D=p.norm_upper(tuple(max(abs(d[k]+x) for x in interval(wg[k])) for k in (0,1)))
        wo=radii[own];eta_radius=radius(eta);V=p.norm_upper(v)
        error1=D*wo*wo/2+wo*dr+V*eta_radius**2/2
        expansions=[(a,g0,error1)]
        if curvature:
            # c(w)*omega^2 <= max_w c(w)*omega^2.
            cmax=-(p.dot(n,d)+interval(wn)[0])/2
            qo=quadratic(cmax,unit(own))
            qr=quadratic(p.dot(n,v)/2,eta)
            yl,yu=interval(tangent);wl,wu=bounds[own]
            products=[(add_vectors(scaled(tangent,wu),scaled(unit(own),yl)),-wu*yl),
                      (add_vectors(scaled(tangent,wl),scaled(unit(own),yu)),-wl*yu)]
            error2=D*wo**3/6+dr*wo*wo/2+V*eta_radius**3/6
            for (qa,qc),(ra,rc),(pa,pc) in itertools.product(qo,qr,products):
                expansions.append((add_vectors(a,qa,ra,pa),g0+qc+rc+pc,error2))
        return expansions

    for i in range(17):
        if i==3:
            continue
        for c,v in enumerate(corners[i]):
            for k in (0,1):
                for sign in (-1,1):
                    a=scaled(add_vectors(H[i][k],G[i][k]),sign)
                    a[34+i]=sign*p.turn(v)[k]
                    g0=sign*(points[i][k]+v[k])
                    if sign==-1:
                        a[51]=F(1);g0+=side
                    row(a,g0,p.norm_upper(v)*radii[34+i]**2/2,f'wall:{i+1}:{c}:{k}:{sign}')

    for left,right in PAIRS:
        i,j=left-1,right-1
        d=tuple(points[j][k]-points[i][k] for k in (0,1))
        hg=[add_vectors(H[j][k],scaled(H[i][k],-1)) for k in (0,1)]
        wg=[add_vectors(G[j][k],scaled(G[i][k],-1)) for k in (0,1)]
        dr=p.norm_upper((radius(hg[0]),radius(hg[1])))
        D=p.norm_upper(tuple(max(abs(d[k]+x) for x in interval(wg[k])) for k in (0,1)))
        alive=[]
        for owner,other in ((i,j),(j,i)):
            for axis in axes[owner]:
                for sign in (-1,1):
                    n=tuple(sign*x for x in axis)
                    projection=add_vectors(*(scaled(add_vectors(hg[k],wg[k]),n[k]) for k in (0,1)))
                    coarse=(p.dot(n,d)+interval(projection)[1]-F(1,2)
                            -max(p.dot(n,v) for v in corners[other])
                            +(D+dr)*radii[34+owner]+radii[34+owner]+radii[34+other])
                    if coarse<0:
                        continue
                    excluded=False
                    all_expansions=[]
                    for v in corners[other]:
                        expansions=corner_terms(i,j,owner,other,n,v)
                        all_expansions.append(expansions)
                        if min(g0+error+true_support(a) for a,g0,error in expansions)<0:
                            excluded=True;break
                    if not excluded:
                        alive.append((owner,other,n,all_expansions))
        if len(alive)==1:
            stats['unique_pairs']+=1
            owner,other,n,expansions=alive[0]
            if audit is not None:
                audit[(left,right,owner+1)]=n
            for c,alternatives in enumerate(expansions):
                for k,(a,g0,error) in enumerate(alternatives):
                    row(a,g0,error,f'pair:{left}:{right}:{owner+1}:{c}:{k}')
        elif len(alive)==2 and alive[0][0]!=alive[1][0] and alive[0][2]==alive[1][2]:
            n=alive[0][2]
            tau0=p.dot(p.turn(n),d)
            tauw=add_vectors(*(scaled(wg[k],p.turn(n)[k]) for k in (0,1)))
            taulo,tauhi=(tau0+x for x in interval(tauw))
            if taulo>=0:
                branch=1
            elif tauhi<=0:
                branch=-1
            else:
                stats['sign_crossings'].append([left,right])
                stats['omitted_pairs']+=1;continue
            taumax=max(abs(taulo),abs(tauhi))
            if taumax>=1:
                stats['omitted_pairs']+=1;continue
            stats['parallel_pairs']+=1
            if audit is not None:
                audit[(left,right,0)]=n
            if interval_provider is None:
                m=(radii[34+i]+radii[34+j])/2
                q=m
            else:
                m=radius(add_vectors(unit(34+i),unit(34+j)))/2
                q=radius(add_vectors(unit(34+j),scaled(unit(34+i),-1)))/2
            error=(D*m*m/2+m*dr+q*q/2+q**3/6+taumax*q**3+(D*m+dr)*(q+q**3))
            for sign in (-1,1):
                a=add_vectors(*(scaled(add_vectors(hg[k],wg[k]),n[k]) for k in (0,1)))
                kappa0=(1-branch*tau0)/2
                a[34+i]+=tau0/2-sign*kappa0
                a[34+j]+=tau0/2+sign*kappa0
                for w in PARAMETERS:
                    with_product(a,tauw[w]*(1+sign*branch)/2,w,34+i)
                    with_product(a,tauw[w]*(1-sign*branch)/2,w,34+j)
                row(a,p.dot(n,d)-1,error,f'parallel:{left}:{right}:{sign}')
        else:
            stats['omitted_pairs']+=1

    if shared:
        for (w,angle),index in PRODUCTS.items():
            l,u=bounds[w];L,U=bounds[angle]
            # Four McCormick inequalities for the same lifted product across
            # all geometry rows. No equality q=w*omega is asserted by the LP.
            for wa,aa,qa,c in ((-L,-l,1,l*L),(-U,-u,1,u*U),
                               (L,u,-1,-u*L),(U,l,-1,-l*U)):
                a=zero();a[w]=wa;a[angle]=aa;a[index]=F(qa)
                row(a,c,F(0),f'product:{w}:{angle}:{qa}:{wa}:{aa}')
    return rows,stats


def parse_exact_rows(rows):
    return [([(j,F(a)) for j,a in enumerate(row['a']) if F(a)],F(row['b']))
            for row in rows]


def exact_dual(rows,bounds,coordinate,sign,weights,parsed=None):
    if coordinate not in CORE+(51,) or sign not in (-1,1):
        raise ValueError('invalid objective')
    residual=[F(sign if j==coordinate else 0) for j in range(DIMENSION)]
    value=F(0)
    if parsed is None:
        parsed=parse_exact_rows(rows)
    for key,value_str in weights.items():
        weight=F(value_str);index=int(key)
        if weight<0 or not 0<=index<len(rows):
            raise ValueError('invalid multiplier')
        a,b=parsed[index]
        value+=weight*b
        for j,coefficient in a:
            residual[j]-=weight*coefficient
    return value+sum((v*(lo if v>=0 else hi) for v,(lo,hi) in zip(residual,bounds)),F(0))


def solve_round(bounds,radius,curvature=True,shared=True):
    import numpy as np
    from scipy.optimize import linprog
    rows,stats=model(bounds,curvature,shared)
    parsed=parse_exact_rows(rows)
    A=np.array([[float(F(x)) for x in r['a']] for r in rows]);b=np.array([float(F(r['b'])) for r in rows])
    results=[];output=list(bounds)
    for coordinate in CORE+(51,):
        for sign in (1,-1):
            c=np.zeros(DIMENSION);c[coordinate]=sign
            fit=linprog(c,A_ub=-A,b_ub=-b/float(radius),
                        bounds=[(float(lo/radius),float(hi/radius)) for lo,hi in bounds],
                        method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
            if not fit.success:
                raise RuntimeError(f'LP failure: {fit.message}; stats={stats}')
            weights={str(i):str(F(round(max(0,-v)*WEIGHT_GRID),WEIGHT_GRID))
                     for i,v in enumerate(fit.ineqlin.marginals) if -v>1e-12}
            bound=exact_dual(rows,bounds,coordinate,sign,weights,parsed)
            results.append(dict(coordinate=coordinate,sign=sign,weights=weights,bound=str(bound)))
            lo,hi=output[coordinate]
            output[coordinate]=(max(lo,bound),hi) if sign==1 else (lo,min(hi,-bound))
    output=p.outward(output[:52]);output=refresh_products(output)
    return output,dict(model_sha256=hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),
                       results=results,stats=stats,rows=len(rows))


def check(path):
    cert=json.loads(path.read_text())
    if cert['schema']!='s17-uniform-capture-v1':
        raise ValueError('unexpected schema')
    if cert['source_sha256']!=hashlib.sha256(p.SOURCE.read_bytes()).hexdigest():
        raise ValueError('source mismatch')
    if any(type(cert[key]) is not bool for key in ('curvature','shared_products')):
        raise ValueError('invalid model flags')
    radius,scale=F(cert['radius']),F(cert['parameter_scale'])
    factor=F(cert['angle_factor'])
    if radius<=0 or scale<0 or factor<=0 or not cert['steps']:
        raise ValueError('invalid domain or empty chain')
    bounds=initial_bounds(radius,factor,scale)
    entered=None
    for number,step in enumerate(cert['steps'],1):
        rows,stats=model(bounds,cert['curvature'],cert['shared_products'])
        parsed=parse_exact_rows(rows)
        if hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()!=step['model_sha256']:
            raise ValueError('model reconstruction mismatch')
        seen=set();updated=list(bounds)
        for result in step['results']:
            coordinate,sign=result['coordinate'],result['sign']
            if (coordinate,sign) in seen:
                raise ValueError('duplicate objective')
            seen.add((coordinate,sign))
            bound=exact_dual(rows,bounds,coordinate,sign,result['weights'],parsed)
            if bound!=F(result['bound']):
                raise ValueError('dual bound mismatch')
            lo,hi=updated[coordinate]
            updated[coordinate]=(max(lo,bound),hi) if sign==1 else (lo,min(hi,-bound))
        if seen!={(i,s) for i in CORE+(51,) for s in (-1,1)}:
            raise ValueError('missing objective')
        bounds=refresh_products(p.outward(updated[:52]))
        if any(lo>hi for lo,hi in bounds):
            raise ValueError('unexpected empty domain')
        if entered is None and max(max(abs(x) for x in bounds[i]) for i in CORE)<F(1,5000):
            entered=number
    if [[str(lo),str(hi)] for lo,hi in bounds]!=cert['final_bounds']:
        raise ValueError('final bounds mismatch')
    return dict(status='PASS',rounds=len(cert['steps']),objectives=92*len(cert['steps']),
                certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                first_round_below_1_over_5000=entered,
                max_core_radius=str(max(max(abs(x) for x in bounds[i]) for i in CORE)),
                scope='Uniform over the declared parameter box at the rational reference; algebraic composition is separate.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--radius',default='1/1024')
    parser.add_argument('--angle-factor',type=int,default=30)
    parser.add_argument('--parameter-scale',default='1')
    parser.add_argument('--rounds',type=int,default=10)
    parser.add_argument('--no-curvature',action='store_true')
    parser.add_argument('--no-shared-products',action='store_true')
    parser.add_argument('--target-radius')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--check',type=Path)
    args=parser.parse_args()
    if args.check:
        print(json.dumps(check(args.check),indent=2));return
    if args.output is None:
        parser.error('--output is required for discovery')
    radius=F(args.radius)
    bounds=initial_bounds(radius,args.angle_factor,F(args.parameter_scale))
    history=[];steps=[]
    result=dict(schema='s17-uniform-capture-v1',radius=str(radius),angle_factor=args.angle_factor,
                parameter_scale=args.parameter_scale,curvature=not args.no_curvature,
                shared_products=not args.no_shared_products,
                source_sha256=hashlib.sha256(p.SOURCE.read_bytes()).hexdigest())
    for iteration in range(args.rounds):
        bounds,step=solve_round(bounds,radius,not args.no_curvature,not args.no_shared_products)
        steps.append(step)
        record=dict(round=iteration+1,
                    max_core_position_radius=float(max(max(abs(x) for x in bounds[i]) for i in CORE if i<34)),
                    max_core_angle_radius=float(max(max(abs(x) for x in bounds[i]) for i in ANGLES)),
                    side_gap=float(-bounds[51][0]),**step['stats'])
        history.append(record);print(json.dumps(record),flush=True)
        result.update(steps=steps,history=history,final_bounds=[[str(lo),str(hi)] for lo,hi in bounds])
        args.output.write_text(json.dumps(result,indent=2)+'\n')
        if args.target_radius is not None and max(max(abs(x) for x in bounds[i]) for i in CORE)<F(args.target_radius):
            break


if __name__=='__main__':
    main()
