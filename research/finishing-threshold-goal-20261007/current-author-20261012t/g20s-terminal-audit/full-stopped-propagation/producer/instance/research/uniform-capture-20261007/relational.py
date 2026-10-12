#!/usr/bin/env python3
"""Uniform slider contraction with exact carried linear correlations."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import uniform as u


def directions():
    _,_,axes,_,H,_=u.geometry()
    result={};seen=set()
    for left,right in u.PAIRS:
        i,j=left-1,right-1
        candidates={'angle_diff':u.add_vectors(u.unit(34+j),u.scaled(u.unit(34+i),-1)),
                    'angle_sum':u.add_vectors(u.unit(34+j),u.unit(34+i))}
        h=[u.add_vectors(H[j][k],u.scaled(H[i][k],-1)) for k in (0,1)]
        for kind,axis in (('dx',(F(1),F(0))),('dy',(F(0),F(1))),('ui',axes[i][0]),
                          ('vi',axes[i][1]),('uj',axes[j][0]),('vj',axes[j][1])):
            candidates[kind]=u.add_vectors(*(u.scaled(h[k],axis[k]) for k in (0,1)))
        for kind,vector in candidates.items():
            vector,_=u.p.canonical(vector)
            if any(vector) and vector not in seen:
                seen.add(vector);result[f'{left}:{right}:{kind}']=vector
    return result


def model(bounds,relations):
    vectors=directions();lookup={tuple(v):key for key,v in vectors.items()}
    def interval(vector):
        lo,hi=u.p.box_interval(vector,bounds)
        canonical,scale=u.p.canonical(vector)
        key=lookup.get(canonical)
        if key in relations:
            a,b=[scale*x for x in relations[key]]
            lo=max(lo,min(a,b));hi=min(hi,max(a,b))
            if lo>hi:
                raise ValueError('inconsistent certified relation')
        return lo,hi
    rows,stats=u.model(bounds,interval_provider=interval)
    for name,(lo,hi) in relations.items():
        for sign,value in ((1,lo),(-1,-hi)):
            rows.append(dict(a=[str(sign*x) for x in vectors[name]],b=str(value),label=f'relation:{name}:{sign}'))
    return rows,stats


def objectives():
    return {**{f'coordinate:{i}':u.unit(i) for i in u.CORE+(51,)},
            **{f'relation:{key}':v for key,v in directions().items()}}


def exact_bound(parsed,bounds,vector,sign,weights):
    residual=[sign*x for x in vector];value=F(0)
    for key,weight in weights.items():
        index=int(key);weight=F(weight)
        if weight<0 or not 0<=index<len(parsed):
            raise ValueError('invalid dual multiplier')
        a,b=parsed[index];value+=weight*b
        for j,coefficient in a:
            residual[j]-=weight*coefficient
    return value+u.p.box_interval(residual,bounds)[0]


def parse(rows):
    return [([(j,F(a)) for j,a in enumerate(row['a']) if F(a)],F(row['b'])) for row in rows]


def apply_results(bounds,relations,results):
    updated=list(bounds);related=dict(relations)
    vectors=directions()
    for result in results:
        name,sign,value=result['objective'],result['sign'],F(result['bound'])
        kind,key=name.split(':',1)
        if kind=='coordinate':
            index=int(key);lo,hi=updated[index]
            updated[index]=(max(lo,value),hi) if sign==1 else (lo,min(hi,-value))
        elif kind=='relation':
            lo,hi=related.get(key,u.p.box_interval(vectors[key],bounds))
            related[key]=(max(lo,value),hi) if sign==1 else (lo,min(hi,-value))
        else:
            raise ValueError('unknown objective')
    updated=u.refresh_products(u.p.outward(updated[:52]))
    related={key:u.p.outward([interval])[0] for key,interval in related.items()}
    if any(lo>hi for lo,hi in list(updated)+list(related.values())):
        raise ValueError('empty interval')
    return updated,related


def solve(bounds,relations,radius):
    import numpy as np
    from scipy.optimize import linprog
    rows,stats=model(bounds,relations);parsed=parse(rows)
    A=np.array([[float(F(x)) for x in row['a']] for row in rows])
    b=np.array([float(F(row['b'])) for row in rows])
    results=[]
    for name,vector in objectives().items():
        for sign in (1,-1):
            fit=linprog(sign*np.array([float(x) for x in vector]),A_ub=-A,b_ub=-b/float(radius),
                        bounds=[(float(lo/radius),float(hi/radius)) for lo,hi in bounds],method='highs',
                        options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
            if not fit.success:
                raise RuntimeError(f'LP proposal failed: {fit.message}')
            weights={str(i):str(F(round(max(0,-v)*u.WEIGHT_GRID),u.WEIGHT_GRID))
                     for i,v in enumerate(fit.ineqlin.marginals) if -v>1e-12}
            value=exact_bound(parsed,bounds,vector,sign,weights)
            results.append(dict(objective=name,sign=sign,weights=weights,bound=str(value)))
    new_bounds,new_relations=apply_results(bounds,relations,results)
    return new_bounds,new_relations,dict(model_sha256=hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),
                                        results=results,stats=stats,rows=len(rows))


def serialized(bounds):
    return [[str(lo),str(hi)] for lo,hi in bounds]


def check(path):
    cert=json.loads(path.read_text())
    if cert['schema']!='s17-uniform-relational-v1' or cert['source_sha256']!=hashlib.sha256(u.p.SOURCE.read_bytes()).hexdigest():
        raise ValueError('source or schema mismatch')
    radius,factor,scale=F(cert['radius']),F(cert['angle_factor']),F(cert['parameter_scale'])
    if radius<=0 or factor<=0 or scale<0 or not cert['steps']:
        raise ValueError('invalid input domain')
    bounds=u.initial_bounds(radius,factor,scale);relations={};vectors=objectives();entered=None
    for number,step in enumerate(cert['steps'],1):
        rows,stats=model(bounds,relations);parsed=parse(rows)
        if step['model_sha256']!=hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest():
            raise ValueError('model reconstruction mismatch')
        seen=set()
        for result in step['results']:
            name,sign=result['objective'],result['sign']
            if name not in vectors or sign not in (-1,1) or (name,sign) in seen:
                raise ValueError('bad or duplicate objective')
            seen.add((name,sign))
            if exact_bound(parsed,bounds,vectors[name],sign,result['weights'])!=F(result['bound']):
                raise ValueError('wrong dual bound')
        if seen!={(name,s) for name in vectors for s in (-1,1)}:
            raise ValueError('missing objective')
        bounds,relations=apply_results(bounds,relations,step['results'])
        if entered is None and max(max(abs(x) for x in bounds[i]) for i in u.CORE)<F(1,5000):
            entered=number
    if cert['final_bounds']!=serialized(bounds) or cert['final_relations']!={key:serialized([value])[0] for key,value in relations.items()}:
        raise ValueError('final interval mismatch')
    return dict(status='PASS',certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),rounds=len(cert['steps']),
                objectives=2*len(vectors)*len(cert['steps']),relations=len(relations),
                first_round_below_1_over_5000=entered,max_core_radius=str(max(max(abs(x) for x in bounds[i]) for i in u.CORE)))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--radius',default='1/512');parser.add_argument('--angle-factor',default='15')
    parser.add_argument('--parameter-scale',default='1');parser.add_argument('--rounds',type=int,default=20)
    parser.add_argument('--target-radius',default='1/10000');parser.add_argument('--output',type=Path);parser.add_argument('--check',type=Path)
    args=parser.parse_args()
    if args.check:
        print(json.dumps(check(args.check),indent=2));return
    if args.output is None:
        parser.error('--output required')
    radius,factor,scale=F(args.radius),F(args.angle_factor),F(args.parameter_scale)
    bounds=u.initial_bounds(radius,factor,scale);relations={};steps=[];history=[]
    cert=dict(schema='s17-uniform-relational-v1',radius=str(radius),angle_factor=str(factor),parameter_scale=str(scale),
              source_sha256=hashlib.sha256(u.p.SOURCE.read_bytes()).hexdigest())
    for number in range(1,args.rounds+1):
        bounds,relations,step=solve(bounds,relations,radius);steps.append(step)
        record=dict(round=number,max_core_position_radius=float(max(max(abs(x) for x in bounds[i]) for i in u.CORE if i<34)),
                    max_core_angle_radius=float(max(max(abs(x) for x in bounds[i]) for i in u.ANGLES)),side_gap=float(-bounds[51][0]),
                    **step['stats'])
        history.append(record);print(json.dumps(record),flush=True)
        cert.update(steps=steps,history=history,final_bounds=serialized(bounds),
                    final_relations={key:serialized([value])[0] for key,value in relations.items()})
        args.output.write_text(json.dumps(cert,indent=2)+'\n')
        if max(max(abs(x) for x in bounds[i]) for i in u.CORE)<F(args.target_radius):
            break


if __name__=='__main__':
    main()
