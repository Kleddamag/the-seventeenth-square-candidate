"""Small exact Banach enclosure check. Standard library; stdout only; no solver.

The map x -> x - J(mid)^(-1) F(x) is a contraction of the closed
midpoint +/- 10^-12 box.  Its unique fixed point is the same common root
as in the endpoint definition.  The residual bound then proves a radius
10^-58 enclosure, and monotonic rational evaluation encloses its side.
The Banach construction adapts check_endpoint.py; this is a tight-enclosure
refinement, not an independently implemented second endpoint proof.
"""
from fractions import Fraction as Q
from pathlib import Path
import ast, hashlib, json, re

if not __debug__:
    raise RuntimeError('Assertions required')
ROOT = Path(__file__).resolve().parents[5]
PINS = {
    'research/uniform-capture-20261007/upstream-root-certificate.json':
    'ef8069b30cd1336ae01124d0f54f13b4f69741c14941f997706b7f599c23a0d9',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/second-order-20261010/theorem/EXACT_ENDPOINT_AND_CASES.json':
    'ea0c3739f00d7513f4adf2c18ce7ebc133141dd12b827229a1f13f461d890e3b',
    'research/global-compensation-20261007/reviews/fresh-structure/endpoint-feasibility/endpoint-receipt.json':
    'f75bb799888eee7fbe68cd8ed2a2be4a93e5cff6b164ac61d698a8cc378636b5',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/claude-extension-audit/terminal-producer/gate-receipt.json':
    '7dee354d5582d3104a6972eb81efc988d9284ede0751906faf0ed9a10b25c8d5',
    'upper-packing-certificate.json':
    '24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7',
}
STATEMENT = str(Path(__file__).resolve().parent.relative_to(ROOT) / 'ENDPOINT_STATEMENT.md')
PINS[STATEMENT] = 'dd73365b0681f0efb00e351f89a1dcb1f80a8e758d44563b1e5e81f851521870'

class IV:
    def __init__(self, lo, hi=None):
        if isinstance(lo, IV): self.lo, self.hi = lo.lo, lo.hi
        else: self.lo, self.hi = Q(lo), Q(lo if hi is None else hi)
        assert self.lo <= self.hi
    def __add__(self, o):
        o = IV(o); return IV(self.lo+o.lo, self.hi+o.hi)
    __radd__ = __add__
    def __neg__(self): return IV(-self.hi, -self.lo)
    def __sub__(self, o): return self + -IV(o)
    def __rsub__(self, o): return IV(o) + -self
    def __mul__(self, o):
        o = IV(o); c = [a*b for a in (self.lo,self.hi) for b in (o.lo,o.hi)]
        return IV(min(c),max(c))
    __rmul__ = __mul__
    def __pow__(self, n):
        assert isinstance(n,int) and n >= 0
        a = IV(1)
        for _ in range(n): a = a*self
        return a
    def norm(self): return max(abs(self.lo),abs(self.hi))

POLYS = (
 ((0,1,1),(1,0,1),(1,1,-1),(1,2,-3),(2,0,-3),(2,2,1),(3,0,-1),(3,2,-1),(4,0,-1),(4,1,-1),(4,2,-1),(5,1,1)),
 ((0,1,-1),(0,2,4),(0,3,-1),(1,1,3),(1,2,-2),(1,3,-5),(1,4,2),(2,1,-4),(2,2,-2),(2,3,4),(2,4,2),(3,0,-2),(3,2,2),(4,0,-2),(4,1,1),(4,2,-2),(4,3,1),(5,1,1),(5,3,1)))
MID = (Q(362043893314323383453621978739944164218293243036741520638379,10**60),
       Q(330948674722739910429808533282915634174672003999685385633441,10**60))

def evaluate(p, x): return sum(c*x[0]**a*x[1]**b for a,b,c in p)
def derivative(p, i):
    return [(a-(i==0),b-(i==1),c*(a if i==0 else b))
            for a,b,c in p if (a if i==0 else b)]
def upward(q, digits=80):
    d=10**digits; return Q(-((-q*d).numerator//(-q*d).denominator),d)
def side(t): return (6+4*t)/(1+2*t-t*t)

def parse_polynomial(expression):
    """Parse this statement's polynomial syntax; no eval or symbolic package."""
    assert re.fullmatch(r'[0-9tb()+\-^]+', expression)
    expression = re.sub(r'(?<=[0-9tb)])(?=[tb(])', '*', expression).replace('^', '**')
    def add(p, q, sign=1):
        out = dict(p)
        for k, c in q.items(): out[k] = out.get(k, 0) + sign*c
        return {k: c for k, c in out.items() if c}
    def multiply(p, q):
        out = {}
        for (a,b), c in p.items():
            for (d,e), f in q.items():
                k = (a+d,b+e); out[k] = out.get(k,0) + c*f
        return {k: c for k,c in out.items() if c}
    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return {(0,0): node.value} if node.value else {}
        if isinstance(node, ast.Name):
            assert node.id in ('t','b')
            return {(1,0) if node.id=='t' else (0,1): 1}
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return {k: -c for k,c in visit(node.operand).items()}
        assert isinstance(node, ast.BinOp)
        p = visit(node.left)
        if isinstance(node.op, ast.Pow):
            assert isinstance(node.right, ast.Constant) and type(node.right.value) is int
            n = node.right.value; assert 0 <= n <= 10
            out = {(0,0): 1}
            for _ in range(n): out = multiply(out,p)
            return out
        q = visit(node.right)
        if isinstance(node.op, ast.Add): return add(p,q)
        if isinstance(node.op, ast.Sub): return add(p,q,-1)
        assert isinstance(node.op, ast.Mult)
        return multiply(p,q)
    p = visit(ast.parse(expression, mode='eval').body)
    return tuple((a,b,c) for (a,b),c in sorted(p.items()))

def main():
    data = {}
    for p,h in PINS.items():
        raw = (ROOT/p).read_bytes(); assert hashlib.sha256(raw).hexdigest()==h,p
        data[p] = raw.decode('utf-8') if p==STATEMENT else json.loads(raw)
    definition, cases, old, gate, reference = [data[p] for p in PINS if p!=STATEMENT]
    ep=cases['endpoint']
    assert tuple(tuple(tuple(map(int,v)) for v in p) for p in definition['polynomials'])==POLYS
    for name, polynomial in zip(('F','G'), POLYS):
        definitions = re.findall(r'Define \$'+name+r'\(t,b\)=(.*?)\$\.', data[STATEMENT])
        assert len(definitions)==1
        assert parse_polynomial(definitions[0])==polynomial, name
    assert tuple(map(Q,definition['box']['midpoint']))==MID
    assert tuple(map(Q,ep['isolating_box_midpoint']))==MID
    radius=Q(1,10**12)
    assert Q(definition['box']['radius'])==Q(ep['isolating_box_radius'])==radius
    outer=[IV(m-radius,m+radius) for m in MID]
    assert 0<outer[0].lo<outer[0].hi<1
    assert 1+2*outer[0].lo-outer[0].hi**2>0
    a,b=[evaluate(derivative(POLYS[0],k),MID) for k in (0,1)]
    c,d=[evaluate(derivative(POLYS[1],k),MID) for k in (0,1)]
    det=a*d-b*c; assert det!=0
    inverse=((d/det,-b/det),(-c/det,a/det))
    jac=[[evaluate(derivative(p,k),outer) for k in (0,1)] for p in POLYS]
    err=[[IV(int(i==j))-sum(inverse[i][k]*jac[k][j] for k in (0,1))
          for j in (0,1)] for i in (0,1)]
    q=max(sum(v.norm() for v in row) for row in err)
    f=[evaluate(p,MID) for p in POLYS]
    eta=max(abs(sum(inverse[i][k]*f[k] for k in (0,1))) for i in (0,1))
    assert q<1 and eta+q*radius<radius
    inner=Q(1,10**58)
    assert eta/(1-q)<inner
    roots=[(m-inner,m+inner) for m in MID]
    for small, claimed, terminal in zip(roots,ep['tight_root_intervals'],gate['root']['intervals']):
        assert Q(claimed[0])<small[0]<small[1]<Q(claimed[1])
        assert Q(terminal[0])<small[0]<small[1]<Q(terminal[1])
    # side'(t)=4*(t^2+3*t-2)/(1+2*t-t^2)^2, strictly negative here.
    lo,hi=roots[0]
    assert 0<lo<hi<1 and hi*hi+3*hi-2<0
    denominator_lower = 1+2*lo-hi*hi
    assert denominator_lower>0  # Lower bound for every t in [lo,hi].
    assert 1+2*lo-lo*lo>0 and 1+2*hi-hi*hi>0
    exact=(side(hi),side(lo))
    tight=tuple(map(Q,ep['L_interval'])); wide=tuple(map(Q,old['side_interval']))
    assert tight[0]<exact[0]<exact[1]<tight[1]
    terminal_side=tuple(map(Q,gate['side_interval']))
    assert terminal_side[0]<exact[0]<exact[1]<terminal_side[1]
    assert wide[0]<tight[0]<tight[1]<wide[1]
    R=Q(reference['side']); C=Q(4675531,10**6); U=Q(1169,250)
    eps=Q(reference['squares'][0]['x'])-Q(1,2)
    assert eps>0
    assert wide[0]>4 and wide[1]<R<C<U and R-wide[1]-2*eps>0
    assert R-wide[1]-eps>0
    out={'status':'PASS_TIGHT_ENDPOINT_ENCLOSURE',
         'method':'Exact rational Banach map on radius 10^-12; residual refinement to radius 10^-58; monotonic rational side evaluation',
         'implementation_provenance':'Banach construction adapted from check_endpoint.py; not an independent implementation',
         'scope':'Root existence/uniqueness and both packet tight enclosures; not packing feasibility or downstream replay',
         'statement_polynomials_equal_certificate':True,
         'denominator_lower':str(denominator_lower),'eps':str(eps),
         'inputs':PINS,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'contraction_upper':str(upward(q)),'residual_upper':str(upward(eta)),
         'root_distance_upper':str(upward(eta/(1-q))),
         'new_radius':str(inner),'new_root_intervals':[[str(v) for v in r] for r in roots],
         'new_L_interval':[str(v) for v in exact],
         'packet_tight_L_interval':[str(v) for v in tight],
         'terminal_gate_L_interval':[str(v) for v in terminal_side],
         'old_replay_wide_L_interval':[str(v) for v in wide],
         'wide_suffices':{'L_gt_4':True,'L_lt_R_lt_C_lt_U':True,
           'P087_R_minus_Lhi_minus_eps':str(R-wide[1]-eps),
           'stronger_R_minus_Lhi_minus_2eps':str(R-wide[1]-2*eps)}}
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
