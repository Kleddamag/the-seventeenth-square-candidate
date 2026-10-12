#!/usr/bin/env python3
"""Independent stdlib exact stop-pair arithmetic; no producer imports or LP."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
FAMILY = HERE.parent
WINDOW = FAMILY.parent
ROOT = WINDOW.parents[2]
REFERENCE = ROOT / 'research/global-compensation-20261007/reviews/wider-contraction-portable-1007/evidence/snapshot/upper-packing-certificate.json'
THEOREM = REFERENCE.parents[2] / 'THEOREM.md'
SREF = F(4675530093604551, 10**15)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


class Interval:
    """Unrounded rational endpoint arithmetic, independent of bridge.I."""
    def __init__(self, lo, hi=None):
        if isinstance(lo, Interval):
            self.lo, self.hi = lo.lo, lo.hi
        else:
            self.lo, self.hi = F(lo), F(lo if hi is None else hi)
        need(self.lo <= self.hi, 'reversed interval')

    def __add__(self, other):
        other = Interval(other)
        return Interval(self.lo+other.lo, self.hi+other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self+-Interval(other)

    def __rsub__(self, other):
        return Interval(other)+-self

    def __mul__(self, other):
        other = Interval(other)
        values = [a*b for a, b in product((self.lo, self.hi), (other.lo, other.hi))]
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Interval(other)
        need(not other.lo <= 0 <= other.hi, 'division across zero')
        return self*Interval(1/other.hi, 1/other.lo)

    def magnitude(self):
        return max(abs(self.lo), abs(self.hi))


def compute():
    raw = json.loads(REFERENCE.read_text())
    saved = json.loads((FAMILY / 'stopping-pair-constants.json').read_text())['result']
    points = [tuple(F(square[k]) for k in ('x', 'y')) for square in raw['squares']]
    ts = [F(square['t']) for square in raw['squares']]
    need(ts[8] == ts[10] == ts[12], 'stop reference axes differ')
    t = ts[8]
    u = ((1-t*t)/(1+t*t), 2*t/(1+t*t))
    v = (-u[1], u[0])
    c, s = u
    need(dot(u, u) == dot(v, v) == 1 and dot(u, v) == 0 and min(u) > 0, 'invalid common axes')
    T = c*(c+4-SREF)
    points[12] = tuple(points[12][k]-T*v[k]/3 for k in (0, 1))
    for name, vector in (('u', u), ('v', v)):
        need(tuple(map(F, saved['reference_axes'][name])) == vector, 'reference axis mismatch')
    base = {}
    for i, j in ((9, 11), (11, 13)):
        difference = tuple(points[j-1][k]-points[i-1][k] for k in (0, 1))
        base[f'{i},{j}'] = (dot(u, difference), -dot(v, difference))
        need(base[f'{i},{j}'] == tuple(F(saved['base'][f'{i},{j}'][key]) for key in ('X0', 'K')), 'base projection mismatch')
    alpha = F(3, 100)
    summaries = []
    for case, radius in zip(saved['cases'], (F(2, 25), F(3, 20), F(1, 4))):
        need(F(case['radius']) == radius and F(case['angle']) == alpha, 'wrong radius or angle')
        a = (F(0), F(1, 4)+radius)
        b = (-F(1, 2500)-radius, F(1, 12)+radius)
        z = (-F(1, 8)-radius, F(1, 16)+radius)
        for key, bounds in (('a', a), ('b', b), ('z', z)):
            need(tuple(map(F, case['sliders'][key])) == bounds, 'wrong padded slider range')
        records = {}
        for pair in ('9,11', '11,13'):
            x_values, n_values = [], []
            # World-coordinate vertices, rather than the producer's formulas.
            if pair == '9,11':
                for hx, hy, transverse, slide in product((-radius, radius), (-radius, radius), (-radius, radius), b):
                    first = (points[8][0]+hx, points[8][1]+hy)
                    second = tuple(points[10][k]+transverse*u[k]-slide*v[k] for k in (0, 1))
                    difference = tuple(second[k]-first[k] for k in (0, 1))
                    x_values.append(dot(u, difference)); n_values.append(-dot(v, difference))
            else:
                for left, right, bs, zs in product((-radius, radius), (-radius, radius), b, z):
                    first = tuple(points[10][k]+left*u[k]-bs*v[k] for k in (0, 1))
                    second = tuple(points[12][k]+right*u[k]+zs*v[k] for k in (0, 1))
                    difference = tuple(second[k]-first[k] for k in (0, 1))
                    x_values.append(dot(u, difference)); n_values.append(-dot(v, difference))
            xlo, xhi = min(x_values), max(x_values)
            nlo, nhi = min(n_values), max(n_values)
            L = max(abs(xlo), abs(xhi))
            C = 1-L
            E = alpha**2+F(2, 3)*alpha**3+L*alpha**3/6
            u_upper = L+alpha*nhi
            v_upper = alpha*L-nlo*(1-alpha**2/2)
            need(nlo > 0 and C > 0 and max(u_upper, v_upper) < 1, 'incomplete SAT exclusion')
            row = case['pairs'][pair]
            for key, exact in (('L', L), ('C', C), ('E', E), ('eliminated_u_upper', u_upper), ('eliminated_positive_v_upper', v_upper)):
                need(F(row[key]) == exact, 'wrong '+key)
            need(tuple(map(F, row['X'])) == (xlo, xhi) and tuple(map(F, row['N'])) == (nlo, nhi), 'wrong coordinate enclosure')
            i, j = pair.split(',')
            excluded = {f'owner={owner},axis={axis},sign={sign}' for owner, axis, sign in product((i, j), ('u', 'v'), (-1, 1)) if axis == 'u' or sign == 1}
            retained = {f'owner={owner},axis=v,sign=-1' for owner in (i, j)}
            need(len(row['eliminated_options']) == 6 and set(row['eliminated_options']) == excluded, 'lost excluded owner/direction')
            need(len(row['retained_options']) == 2 and set(row['retained_options']) == retained, 'lost retained owner')
            k = base[pair][1]
            simple = 1-k-(c+s)*radius-alpha*L if pair == '9,11' else k-1+alpha*L
            need(F(row['uniform_simple_bound']['exact']) == simple, 'wrong uniform slider consequence')
            records[pair] = dict(N_positive=str(nlo), L=str(L), C=str(C), E=str(E),
                                 u_guard_margin=str(1-u_upper), positive_v_guard_margin=str(1-v_upper),
                                 slider_bound=str(simple))
        summaries.append(dict(radius=str(radius), pairs=records))
    need(len(saved['cases']) == 3, 'unexpected finite case roster')
    # Independently certify the claimed first sufficient guard to fail along
    # this one-parameter family of padded domains, not just the three samples.
    x9, k9 = base['9,11']
    limit = (1-x9-alpha*(k9+F(1, 12)))/((1+c+s)*(1+alpha))
    need(F(saved['first_u_guard_radius_limit_at_angle_003']['exact']) == limit, 'wrong limiting radius')
    guards_at_limit = {}
    for pair, (x0, k) in base.items():
        if pair == '9,11':
            L = x0+(1+c+s)*limit
            nlo, nhi = k-F(1, 2500)-(1+c+s)*limit, k+F(1, 12)+(1+c+s)*limit
        else:
            L = x0+2*limit
            nlo, nhi = k-F(1, 12)-F(1, 16)-2*limit, k+F(1, 2500)+F(1, 8)+2*limit
        ug = L+alpha*nhi
        vg = alpha*L-nlo*(1-alpha**2/2)
        need(x0 > 0 and nlo > 0 and L < 1 and vg < 1, 'another guard fails before the proposed limit')
        need(ug == 1 if pair == '9,11' else ug < 1, 'wrong first u guard')
        guards_at_limit[pair] = dict(N_lower=str(nlo), L=str(L), u_upper=str(ug), positive_v_upper=str(vg))
    # Root lemma: use the already proved outer root box, without importing
    # producer interval/root code or relying on rounded display constants.
    tr = Interval(t-F(1, 10**12), t+F(1, 10**12))
    cr = (1-tr*tr)/(1+tr*tr)
    sr = 2*tr/(1+tr*tr)
    side = (6+4*tr)/(1+2*tr-tr*tr)
    root_T = cr*(cr+4-side)
    eps, pad = F(1, 5000), F(1, 10**12)
    broad_b = Interval(-F(201, 2500)-pad, F(49, 300)+pad)
    broad_z = Interval(-F(41, 200)-pad, F(57, 400)+pad)
    need((cr+sr).hi < F(141, 100), 'c+s bound failed')
    need(root_T.lo > 0 and (root_T/3+F(183, 100)*eps).hi < F(1, 40), 'stopped z bound failed')
    root_records = []
    for pair, X, N, D, dr, xmax in (
        ('9,11', cr*(1-sr), 1+broad_b, F(6, 5), F(5, 2), F(277, 1000)),
        ('11,13', cr-sr, 1+root_T/3-broad_b-broad_z, F(4, 3), F(2), F(129, 1000))):
        need(X.magnitude() < xmax and N.lo-dr*eps > 0, 'root coordinate guard failed')
        need(X.magnitude()**2+N.magnitude()**2 < D*D, 'root norm bound failed')
        option_bounds = []
        for reference_projection in (X, -X, -N):
            upper = reference_projection.hi+dr*eps+eps*(D+dr*eps)
            need(upper < 1, 'root SAT alternative survives')
            option_bounds.append(str(upper))
        root_records.append(dict(pair=pair, D=str(D), dr=str(dr),
                                 N_lower_after_core=str(N.lo-dr*eps), six_option_upper_bounds=option_bounds))
    need(F(141, 100)+F(277, 1000)+F(241, 100)*eps < F(17, 10), 'b stop coefficient failed')
    need(F(129, 1000)+2*eps < F(13, 100), 'sum stop coefficient failed')
    need(-F(17, 10)*eps >= -F(1, 2500), 'old lower b stop not recovered')
    v10 = cr*(side-1)-sr-F(1, 2)
    v11 = 2*cr+(cr*cr-sr*sr)/2-1
    tau11 = v10-1-v11+Interval(-F(17, 10)*eps, broad_b.hi)
    tau13 = v10-v11-1+root_T/3-Interval(broad_z.lo, F(1, 40))
    need(0 < tau11.lo <= tau11.hi < 1 and 0 < tau13.lo <= tau13.hi < 1, 'stopped parallel sign not restored')
    need(saved['packing_exclusions'] == 0 and not saved['capture_proved'], 'unproved global conclusion')
    for relative, digest in saved['dependencies'].items():
        need(sha(ROOT/relative) == digest, 'changed producer dependency')
    need(saved['source_sha256'] == sha(FAMILY/'check_stops.py'), 'changed producer source')
    return dict(finite_cases=summaries, first_guard_radius=str(limit), first_guard_radius_display=float(limit),
                guards_at_limit=guards_at_limit, root_stop_checks=root_records,
                root_terminal_consequences=['b >= -(17/10)*epsilon', 'b+z <= T/3+(13/100)*epsilon',
                                            'at epsilon<=1/5000: b >= -1/2500 and z < 1/40'],
                positive_parallel_offset_intervals={
                    '11,12':[str(tau11.lo), str(tau11.hi)], '13,14':[str(tau13.lo), str(tau13.hi)]},
                finite_contraction_proved=False, padded_rigidity_proved=False, capture_proved=False,
                root_transfer_replayed_here=False, remaining_terminal_model_replayed_here=False)


def main():
    cpu, wall = time.process_time(), time.monotonic()
    proof = compute()
    sources = [Path(__file__), REFERENCE, THEOREM, FAMILY/'check_stops.py', FAMILY/'stopping-pair-constants.json',
               FAMILY/'STOPPING_PAIRS.md', WINDOW/'padded-terminal/check_stops.py', WINDOW/'padded-terminal/PROPOSAL.md',
               ROOT/'research/uniform-capture-20261007/bridge.py', ROOT/'research/uniform-capture-20261007/root_geometry.py']
    result = dict(status='PASS_INDEPENDENT_STOP_PAIR_ARITHMETIC_AND_ANALYTIC_COVERAGE',
                  reviewer='Codex contributor 05', producer_code_imported=False,
                  checked=proof, input_sha256={str(p.relative_to(ROOT)):sha(p) for p in sources},
                  cpu_seconds=time.process_time()-cpu, wall_seconds=time.monotonic()-wall)
    target = HERE/'arithmetic-receipt.json'
    if not target.exists():
        target.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status', 'cpu_seconds', 'wall_seconds')}, indent=2))


if __name__ == '__main__':
    main()
