"""Exact finite sign-atom check of the literal manuscript's case decision list.

No geometry, charge or local result is inferred. Each guard is a conjunction of
one-coordinate rational comparisons, so its truth is constant on every atom.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter
import ast,hashlib,json,time
O=Path(__file__).parent
B=O.parents[1]/'second-order-20261010/theorem'
p=B/'EXACT_ENDPOINT_AND_CASES.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
d=json.loads(p.read_text());rows=d['branches']+d['excluded_branches']
names=['x9','y9','t9','tau3','tau17','tau15']
rho=F(207107,500000)
assert (1+rho)**2>2
domain={'x9':(None,None,True,True),'y9':(None,None,True,True),'t9':(F(0),F(1),True,False),**{n:(-rho,rho,True,True) for n in names[3:]}}
ops={ast.Lt:lambda a,b:a<b,ast.LtE:lambda a,b:a<=b,ast.Gt:lambda a,b:a>b,ast.GtE:lambda a,b:a>=b}
def rational(n):
    if isinstance(n,ast.Constant) and type(n.value) is int:return F(n.value)
    if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -rational(n.operand)
    if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Div):return rational(n.left)/rational(n.right)
    raise AssertionError(ast.dump(n))
def parse(text):
    expr=ast.parse(text,mode='eval').body
    assert isinstance(expr,ast.BoolOp) and isinstance(expr.op,ast.And)
    out=[]
    for c in expr.values:
        assert isinstance(c,ast.Compare)
        for l,op,r in zip([c.left]+c.comparators[:-1],c.ops,c.comparators):
            assert type(op) in ops
            assert isinstance(l,ast.Name) != isinstance(r,ast.Name)
            name=l.id if isinstance(l,ast.Name) else r.id
            assert name in names
            out.append((name,type(op),rational(r if isinstance(l,ast.Name) else l),isinstance(l,ast.Name)))
    return out
def atoms(name,cuts):
    lo,hi,lc,hc=domain[name]
    points=set(cuts)
    if lo is not None:points.add(lo)
    if hi is not None:points.add(hi)
    points=sorted(x for x in points if (lo is None or x>=lo) and (hi is None or x<=hi))
    out=[]
    if lo is None:out.append((points[0]-1,{'lower':None,'upper':str(points[0]),'kind':'open_interval'}))
    for i,x in enumerate(points):
        if not ((lo==x and not lc) or (hi==x and not hc)):out.append((x,{'value':str(x),'kind':'singleton'}))
        if i+1<len(points):out.append(((x+points[i+1])/2,{'lower':str(x),'upper':str(points[i+1]),'kind':'open_interval'}))
    if hi is None:out.append((points[-1]+1,{'lower':str(points[-1]),'upper':None,'kind':'open_interval'}))
    return out
def check(rows):
    guards=[parse(r['predicate']) for r in rows]
    cells={n:atoms(n,{x[2] for g in guards for x in g if x[0]==n}) for n in names}
    masks={}
    for n in names:
        masks[n]=[]
        for val,_ in cells[n]:
            mask=0
            for j,g in enumerate(guards):
                if all(ops[op](val,q) if left else ops[op](q,val) for nm,op,q,left in g if nm==n):mask|=1<<j
            masks[n].append(mask)
    counts=Counter();first_bad=None
    for ix in product(*(range(len(cells[n])) for n in names)):
        mask=(1<<len(rows))-1
        for n,j in zip(names,ix):mask&=masks[n][j]
        if mask==0 or mask & (mask-1):
            first_bad={'point':{n:str(cells[n][j][0]) for n,j in zip(names,ix)},'matching':[r['root'] for k,r in enumerate(rows) if mask>>k&1]}
            break
        counts[rows[mask.bit_length()-1]['root']]+=1
    return cells,counts,first_bad
start=time.process_time()
cells,counts,bad=check(rows)
assert bad is None and len(rows)==13 and set(counts)=={r['root'] for r in rows}
assert [r['root'] for r in d['excluded_branches']]==['JPB','REMOVED_HIGH9']
# Mutations test missed and doubly owned exact endpoints, without changing source files.
mutations=[('lost_upper9_endpoint','JPA','591183/1408817 <= t9','591183/1408817 < t9'),
           ('lost_KEYW_upper_endpoint','JPA','t9 <= 44941/100000','t9 < 44941/100000'),
           ('double_owned_KEYW_upper_endpoint','REMOVED_HIGH9','44941/100000 < t9','44941/100000 <= t9'),
           ('lost_lower9_endpoint','JPB','t9 <= 61301/200000','t9 < 61301/200000'),
           ('lost_wall_seam','JPWS','y9 <= 13/5','y9 < 13/5'),
           ('double_owned_wall_seam','JPW13','y9 > 13/5','y9 >= 13/5'),
           ('lost_positive3_endpoint','JPG3p','tau3 >= 1/20','tau3 > 1/20'),
           ('double_owned_negative3_endpoint','JPG17m','-1/20 < tau3','-1/20 <= tau3')]
negative=[]
for tag,root,old,new in mutations:
    m=[dict(r) for r in rows];r=next(r for r in m if r['root']==root)
    assert old in r['predicate'];r['predicate']=r['predicate'].replace(old,new)
    _,_,failure=check(m);assert failure is not None,tag
    negative.append({'mutation':tag,'counterexample':failure})
out={'status':'PASS_EXACT_GUARD_PARTITION_ON_ALL_SIGN_ATOMS','source':{'file':str(p),'sha256':sha(p)},'reader':{'file':str(Path(__file__)),'sha256':sha(Path(__file__))},'domains':{n:[None if x is None else str(x) if isinstance(x,F) else x for x in dom] for n,dom in domain.items()},'atoms':{n:[a for _,a in v] for n,v in cells.items()},'atom_counts_by_case':dict(counts),'total_atoms':sum(counts.values()),'negative_controls':negative,'logical_justification':'Every parsed guard is an AND of comparisons between one coordinate and a rational constant. All its cut constants are atom boundaries. Each comparison, hence each guard, is constant on every product atom. Exact representative tests therefore prove disjoint exhaustiveness on the entire domain, including every singleton seam; they are not numerical sampling. JPB and REMOVED_HIGH9 are excluded only by the separately accepted KEY_W implication with both exact endpoints. Loose angle domain is a rational superset of the true canonical interval.','not_proved':'Marker/frame existence, parent assignment, any class budget, root admission, any local EMPTY/TUBE, or final optimality. Those remain named imported premises.','CPU_seconds':time.process_time()-start}
(O/'CASE_PARTITION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','total_atoms','atom_counts_by_case','CPU_seconds']}))
