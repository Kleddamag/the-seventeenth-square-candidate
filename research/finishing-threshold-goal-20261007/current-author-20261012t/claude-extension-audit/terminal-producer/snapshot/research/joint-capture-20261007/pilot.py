#!/usr/bin/env python3
"""Research pilot: necessary Taylor rows, joint LP, and exact dual replay.

No new global packing bound is asserted. Angles are increments in radians.
Discovery needs scipy; --check uses only the Python standard library.
"""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'upper-packing-certificate.json'
GRID = 10**15
DUAL_GRID = 10**10
N = 52
PROFILE = 'boundary'
CURVATURE = True
CARRY_RELATIONS = False
# These contacts involve the rattler, corner-only contact, or slider endpoints.
# Omit them to test the rigid mechanism without endpoint-specific assistance.
OMITTED_PAIRS = {(2, 4), (3, 5), (4, 6), (9, 11), (11, 13)}


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def turn(v):
    return (-v[1], v[0])


def norm_upper(v):
    """Rational Euclidean norm upper bound on a 1e-9 grid."""
    s = dot(v, v) * 10**18
    k = isqrt(s.numerator // s.denominator)
    if F(k*k) < s:
        k += 1
    return F(k, 10**9)


def reference():
    raw = json.loads(SOURCE.read_text())
    points, axes, corners = [], [], []
    for sq in raw['squares']:
        points.append((F(sq['x']), F(sq['y'])))
        t = F(sq['t'])
        u = ((1-t*t)/(1+t*t), 2*t/(1+t*t))
        v = turn(u)
        axes.append((u, v))
        corners.append(tuple(tuple((a*u[k]+b*v[k])/2 for k in range(2))
                             for a in (-1, 1) for b in (-1, 1)))
    if PROFILE == 'interior':
        # Move the rattler and the two sliders away from incidental contacts.
        points[3] = (points[3][0]-F(1,50), points[3][1])
        for i, amount in ((10,F(1,50)), (12,F(1,25))):
            points[i] = tuple(points[i][k]-amount*axes[i][1][k] for k in (0,1))
    return F(raw['side']), points, axes, corners


def canonical(vector):
    scale = next((x for x in vector if x), F(1))
    return tuple(x/scale for x in vector), scale


def box_interval(vector, bounds):
    return (sum((x*(lo if x>=0 else hi) for x,(lo,hi) in zip(vector,bounds)), F(0)),
            sum((x*(hi if x>=0 else lo) for x,(lo,hi) in zip(vector,bounds)), F(0)))


def pair_vector(i, j, kind, axes):
    vector = [F(0)]*N
    if kind == 'angle_diff':
        vector[34+i], vector[34+j] = F(-1), F(1)
    elif kind == 'angle_sum':
        vector[34+i], vector[34+j] = F(1), F(1)
    else:
        axis = {'dx':(F(1),F(0)), 'dy':(F(0),F(1)),
                'u_i':axes[i][0], 'v_i':axes[i][1],
                'u_j':axes[j][0], 'v_j':axes[j][1]}[kind]
        for k in (0,1):
            vector[2*i+k], vector[2*j+k] = -axis[k], axis[k]
    return vector


def relation_directions():
    """A fixed, reconstructible selection of quantities for near neighbours."""
    _, p, axes, corners = reference()
    directions, seen = {}, set()
    for i in range(17):
        for j in range(i+1,17):
            if (i+1,j+1) in OMITTED_PAIRS:
                continue
            d = tuple(p[j][k]-p[i][k] for k in (0,1))
            gaps = []
            for owner, other in ((i,j),(j,i)):
                for axis in axes[owner]:
                    for sign in (-1,1):
                        n = tuple(sign*x for x in axis)
                        gaps.append(dot(n,d)-F(1,2)-max(dot(n,v) for v in corners[other]))
            if max(gaps) > F(1,100):
                continue
            for kind in ('angle_diff','angle_sum','dx','dy','u_i','v_i','u_j','v_j'):
                vector, _ = canonical(pair_vector(i,j,kind,axes))
                if vector not in seen:
                    directions[f'{i+1}:{j+1}:{kind}'] = vector
                    seen.add(vector)
    return directions


def build_model(bounds, relations=None, directions=None):
    """Derive necessary linear inequalities A*z >= b on the supplied box.

    All arithmetic constructing the rows is exact. Unsupported SAT
    disjunctions are dropped (a relaxation), never selected heuristically.
    """
    S, p, axes, corners = reference()
    relations, directions = relations or {}, directions or {}
    lookup = {tuple(vector): name for name,vector in directions.items()}
    rad = [max(abs(a), abs(b)) for a, b in bounds]
    if max(rad[34:51]) > F(1, 10):
        raise ValueError('parallel-face remainder requires angle radii <= 0.1')
    rows, stats = [], dict(unique_pairs=0, parallel_pairs=0, omitted_pairs=0)

    def linear_interval(vector):
        lo, hi = box_interval(vector,bounds)
        key, scale = canonical(vector)
        name = lookup.get(key)
        if name in relations:
            left, right = (scale*x for x in relations[name])
            lo, hi = max(lo,min(left,right)), min(hi,max(left,right))
        if lo > hi:
            raise ValueError('inconsistent relational enclosure')
        return lo, hi

    def pair_radius(i,j,kind):
        return max(abs(x) for x in linear_interval(pair_vector(i,j,kind,axes)))

    def sat_row(i, j, owner, other, n, v, d, D, dr):
        wo, wt = rad[34+owner], rad[34+other]
        a = [F(0)]*N
        for k in (0, 1):
            a[2*i+k] = -n[k]
            a[2*j+k] = n[k]
        a[34+owner] = dot(turn(n), d)+dot(n, turn(v))
        a[34+other] = -dot(n, turn(v))
        g0 = dot(n, d)-F(1, 2)-dot(n, v)
        relative_radius = pair_radius(owner,other,'angle_diff')
        err = D*wo*wo/2+wo*dr+norm_upper(v)*relative_radius**2/2
        return a, g0, err

    def add(a, g0, error, label):
        # Round coefficients, paying for their entire possible box error.
        aq = [F(round(x*GRID), GRID) for x in a]
        loss = sum((abs(x-y)*r for x, y, r in zip(a, aq, rad)), F(0))
        exact_b = -g0-error-loss
        b = F((exact_b*GRID).__floor__(), GRID)
        rows.append({'a': [str(x) for x in aq], 'b': str(b), 'label': label})

    def quadratic_upper(coefficient, vector):
        """Affine upper envelopes of coefficient*(vector.z)^2."""
        lo, hi = linear_interval(vector)
        if coefficient >= 0:
            return [([coefficient*(lo+hi)*x for x in vector], -coefficient*lo*hi)]
        # A concave quadratic lies below every tangent.
        return [([2*coefficient*t*x for x in vector], -coefficient*t*t)
                for t in set((F(0), (lo+hi)/2))]

    def add_second_order(i,j,owner,other,n,v,d,D,dr,label):
        """Keep curvature signs and centre/angle products in affine envelopes."""
        a, g0, _ = sat_row(i,j,owner,other,n,v,d,D,dr)
        wo, wt = rad[34+owner], rad[34+other]
        angular, relative, tangent = [F(0)]*N, [F(0)]*N, [F(0)]*N
        angular[34+owner] = F(1)
        relative[34+other], relative[34+owner] = F(1), F(-1)
        for k in (0,1):
            tangent[2*i+k], tangent[2*j+k] = -turn(n)[k], turn(n)[k]
        yl, yu = linear_interval(tangent)
        wl, wu = bounds[34+owner]
        # Both McCormick upper planes bound omega*(Jn.delta_d).
        products = [([wu*y+yl*w for y,w in zip(tangent,angular)], -wu*yl),
                    ([wl*y+yu*w for y,w in zip(tangent,angular)], -wl*yu)]
        qown = quadratic_upper(-dot(n,d)/2, angular)
        qrelative = quadratic_upper(dot(n,v)/2, relative)
        relative_radius = max(abs(x) for x in linear_interval(relative))
        error = D*wo**3/6+dr*wo*wo/2+norm_upper(v)*relative_radius**3/6
        count = 0
        for pa, pc in products:
            for qa, qc in qown:
                for ra, rc in qrelative:
                    add([x+y+z+w for x,y,z,w in zip(a,pa,qa,ra)],
                        g0+pc+qc+rc, error, f'{label}:{count}')
                    count += 1

    for i in range(17):
        w = rad[34+i]
        for c, v in enumerate(corners[i]):
            for k in (0, 1):
                for sign in (-1, 1):
                    a = [F(0)]*N
                    a[2*i+k] = F(sign)
                    a[34+i] = sign*turn(v)[k]
                    g0 = sign*(p[i][k]+v[k])
                    if sign == -1:
                        a[51] = F(1)
                        g0 += S
                    add(a, g0, norm_upper(v)*w*w/2,
                        f'wall:{i+1}:{c}:{k}:{sign}')

    for i in range(17):
        for j in range(i+1, 17):
            if (i+1, j+1) in OMITTED_PAIRS:
                stats['omitted_pairs'] += 1
                continue
            d = tuple(p[j][k]-p[i][k] for k in (0, 1))
            D = norm_upper(d)
            dr = min(norm_upper((pair_radius(i,j,a),pair_radius(i,j,b)))
                     for a,b in (('dx','dy'),('u_i','v_i'),('u_j','v_j')))
            alive = []
            for owner, other in ((i, j), (j, i)):
                wo, wt = rad[34+owner], rad[34+other]
                for axis in axes[owner]:
                    for sign in (-1, 1):
                        n = tuple(sign*x for x in axis)
                        support = max(dot(n, v) for v in corners[other])
                        g0 = dot(n, d)-F(1, 2)-support
                        # |R(w)-I| <= |w|; corner norm <= 1.
                        change = D*wo+dr+pair_radius(owner,other,'angle_diff')
                        if g0+change < 0:
                            continue
                        excluded = False
                        for v in corners[other]:
                            a, corner_gap, err = sat_row(i,j,owner,other,n,v,d,D,dr)
                            upper = corner_gap+err+box_interval(a,bounds)[1]
                            if upper < 0:
                                excluded = True
                                break
                        if not excluded:
                            alive.append((owner, other, n, g0))
            if len(alive) == 1:
                stats['unique_pairs'] += 1
                owner, other, n, _ = alive[0]
                for c, v in enumerate(corners[other]):
                    a, g0, err = sat_row(i,j,owner,other,n,v,d,D,dr)
                    add(a, g0, err, f'unique:{i+1}:{j+1}:{owner+1}:{c}')
                    if CURVATURE:
                        add_second_order(i,j,owner,other,n,v,d,D,dr,
                                         f'curvature:{i+1}:{j+1}:{owner+1}:{c}')
            elif (len(alive) == 2 and alive[0][0] != alive[1][0]
                  and alive[0][2] == alive[1][2]):
                stats['parallel_pairs'] += 1
                n = alive[0][2]
                tau = dot(turn(n), d)
                # Bound mean and relative angle separately, optionally by
                # quantities certified by the previous joint LP.
                m = pair_radius(i,j,'angle_sum')/2
                q = pair_radius(i,j,'angle_diff')/2
                kappa = (1-abs(tau))/2
                if kappa < 0:
                    stats['omitted_pairs'] += 1
                    stats['parallel_pairs'] -= 1
                    continue
                # cos q>=1-q²/2; |sin q|>=|q|-|q|³/6;
                # |tan q|<=|q|+|q|³ for |q|<=0.1.
                err = (D*m*m/2+m*dr+q*q/2+q**3/6+abs(tau)*q**3
                       +(D*m+dr)*(q+q**3))
                for sign in (-1, 1):
                    a = [F(0)]*N
                    for k in (0, 1):
                        a[2*i+k] = -n[k]
                        a[2*j+k] = n[k]
                    a[34+i] = tau/2-sign*kappa
                    a[34+j] = tau/2+sign*kappa
                    add(a, dot(n, d)-1, err, f'parallel:{i+1}:{j+1}:{sign}')
            else:
                stats['omitted_pairs'] += 1
    for name,(lo,hi) in sorted(relations.items()):
        vector = directions[name]
        add(vector,-lo,F(0),f'carried:{name}:lower')
        add([-x for x in vector],hi,F(0),f'carried:{name}:upper')
    return rows, stats


def parse_rows(rows):
    return [[F(x) for x in row['a']] for row in rows], [F(row['b']) for row in rows]


def dual_bound(A, b, bounds, coordinate, sign, weights, vector=None):
    """Exact weak duality, including every dual residual via the input box."""
    if (vector is None and not 0 <= coordinate < N) or sign not in (-1, 1):
        raise ValueError('invalid objective')
    if vector is not None and len(vector) != N:
        raise ValueError('invalid objective vector')
    residual = ([sign*x for x in vector] if vector is not None
                else [F(sign if j == coordinate else 0) for j in range(N)])
    value = F(0)
    for key, weight in weights.items():
        row = int(key)
        w = F(weight)
        if w < 0 or not 0 <= row < len(A):
            raise ValueError('invalid dual multiplier')
        value += w*b[row]
        for j, a in enumerate(A[row]):
            residual[j] -= w*a
    for d, (lo, hi) in zip(residual, bounds):
        value += d*(lo if d >= 0 else hi)
    return value


def interval_propagate(A, b, bounds, max_rounds=1000):
    """Floating baseline only; not used in the proof certificates."""
    import numpy as np
    lo, hi = np.array(bounds, dtype=float).T.copy()
    sparse = [(np.flatnonzero(row), row[row != 0], rhs) for row, rhs in zip(A, b)]
    for iteration in range(max_rounds):
        old_lo, old_hi = lo.copy(), hi.copy()
        for indices, values, rhs in sparse:
            contributions = values*np.where(values > 0, hi[indices], lo[indices])
            total = contributions.sum()
            for index, a, contribution in zip(indices, values, contributions):
                bound = (rhs-total+contribution)/a
                if a > 0:
                    lo[index] = max(lo[index], bound)
                else:
                    hi[index] = min(hi[index], bound)
        if max(np.max(abs(lo-old_lo)), np.max(abs(hi-old_hi))) < 1e-13:
            break
    return list(zip(lo, hi)), iteration+1


def solve_box(bounds, radius, relations=None, directions=None):
    import numpy as np
    from scipy.optimize import linprog
    relations, directions = relations or {}, directions or {}
    rows, stats = build_model(bounds,relations,directions)
    A, b = parse_rows(rows)
    zero_in_domain = all(lo<=0<=hi for lo,hi in bounds) and all(lo<=0<=hi for lo,hi in relations.values())
    if zero_in_domain and any(rhs > 0 for rhs in b):
        raise ValueError('model excluded the exactly feasible reference packing')
    stats['solver_retries'] = 0
    Af, bf = np.array(A, dtype=float), np.array(b, dtype=float)
    baseline, rounds = interval_propagate(Af, bf, bounds)
    results, contracted = [], []
    def certify(vector, sign):
        c = sign*np.array(vector,dtype=float)
        # Scale variables, not rows, to keep small boxes well resolved.
        fit = linprog(c, A_ub=-Af, b_ub=-bf/float(radius),
                      bounds=[(float(a/radius), float(z/radius)) for a, z in bounds],
                      method='highs', options={'dual_feasibility_tolerance': 1e-9,
                                               'primal_feasibility_tolerance': 1e-9})
        if not fit.success and zero_in_domain:
            # At near-roundoff box widths, HiGHS presolve can report numerical
            # infeasibility even though z=0 is exactly feasible. Retry the same
            # model without presolve; never accept an exclusion from this status.
            stats['solver_retries'] += 1
            fit = linprog(c,A_ub=-Af,b_ub=-bf/float(radius),
                          bounds=[(float(a/radius),float(z/radius)) for a,z in bounds],
                          method='highs',options={'presolve':False,
                            'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
        if not fit.success:
            raise RuntimeError(f'LP failed: {fit.message}')
        weights = {str(i): str(F(round(max(0, -v)*DUAL_GRID), DUAL_GRID))
                   for i, v in enumerate(fit.ineqlin.marginals) if -v > 1e-12}
        certified = dual_bound(A,b,bounds,None,sign,weights,vector)
        return certified, weights

    for coordinate in range(N):
        endpoints = []
        vector = [F(int(j == coordinate)) for j in range(N)]
        for sign in (1, -1):
            certified, weights = certify(vector,sign)
            results.append(dict(coordinate=coordinate, sign=sign, weights=weights,
                                lower_bound=str(certified)))
            endpoints.append(certified if sign == 1 else -certified)
        contracted.append((max(bounds[coordinate][0], endpoints[0]),
                           min(bounds[coordinate][1], endpoints[1])))
    relative_results, next_relations = [], {}
    relative_gains = {}
    for name,vector in directions.items():
        endpoints = []
        for sign in (1,-1):
            certified, weights = certify(vector,sign)
            relative_results.append(dict(direction=name,sign=sign,weights=weights,
                                         lower_bound=str(certified)))
            endpoints.append(certified if sign == 1 else -certified)
        lo, hi = box_interval(vector,contracted)
        if name in relations:
            lo, hi = max(lo,relations[name][0]), min(hi,relations[name][1])
        next_relations[name] = outward([(max(lo,endpoints[0]),min(hi,endpoints[1]))])[0]
        plain_lo, plain_hi = box_interval(vector,contracted)
        if plain_hi > plain_lo:
            relative_gains[name] = float((next_relations[name][1]-next_relations[name][0])/(plain_hi-plain_lo))
    def reduction(box, indices):
        return [float((box[i][1]-box[i][0])/(bounds[i][1]-bounds[i][0])) for i in indices]
    report = dict(rows=len(rows), **stats,
                  interval_rounds=rounds,
                  interval_center_width_ratios=reduction(baseline, range(34)),
                  lp_center_width_ratios=reduction(contracted, range(34)),
                  interval_angle_width_ratios=reduction(baseline, range(34, 51)),
                  lp_angle_width_ratios=reduction(contracted, range(34, 51)),
                  side_interval=[str(x) for x in contracted[51]])
    return dict(bounds=[[str(a), str(b)] for a, b in bounds],
                relations={name:[str(x) for x in interval] for name,interval in relations.items()},
                rows_sha256=hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest(),
                results=results, relative_results=relative_results, relative_gains=relative_gains,
                report=report), contracted, next_relations


def outward(box):
    """Keep later boxes small in bit length, rounding only outward."""
    return [(F((a*GRID).__floor__(), GRID), F((b*GRID).__ceil__(), GRID)) for a, b in box]


def initial_box(radius, angular_factor):
    return [(-radius, radius)]*34+[(-angular_factor*radius, angular_factor*radius)]*17+[(F(-1,50), F(0))]


def solve(radius, angular_factor, iterations):
    import numpy as np
    bounds = initial_box(radius, angular_factor)
    initial = bounds.copy()
    baseline = bounds.copy()
    directions = relation_directions() if CARRY_RELATIONS else {}
    relations = {}
    steps, history = [], []
    for iteration in range(iterations):
        step, contracted, relations = solve_box(bounds, radius, relations, directions)
        steps.append(step)
        # Baseline receives its own updated domains and regenerated rows.
        base_rows, _ = build_model(baseline)
        A, b = parse_rows(base_rows)
        base, _ = interval_propagate(np.array(A, dtype=float), np.array(b, dtype=float), baseline)
        baseline = [(F(str(a)), F(str(b))) for a, b in base]
        bounds = outward(contracted)
        ratios = lambda box, inds: [float((box[i][1]-box[i][0])/(initial[i][1]-initial[i][0])) for i in inds]
        record = dict(iteration=iteration+1,
                      lp_center_width_ratios=ratios(bounds, range(34)),
                      interval_center_width_ratios=ratios(baseline, range(34)),
                      lp_angle_width_ratios=ratios(bounds, range(34,51)),
                      interval_angle_width_ratios=ratios(baseline, range(34,51)),
                      side_lower=float(bounds[51][0]))
        history.append(record)
        print(json.dumps(dict(iteration=iteration+1,
                              lp_median_center_ratio=float(np.median(record['lp_center_width_ratios'])),
                              interval_median_center_ratio=float(np.median(record['interval_center_width_ratios'])),
                              lp_angle_ratios=record['lp_angle_width_ratios'])), flush=True)
    return dict(schema='s17-joint-capture-pilot-v3',
                source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                profile=PROFILE, curvature=CURVATURE, carry_relations=CARRY_RELATIONS,
                radius=str(radius), angular_factor=angular_factor, steps=steps,
                final_box=[[str(a), str(b)] for a,b in bounds], history=history,
                final_relations={name:[str(x) for x in interval] for name,interval in relations.items()})


def check(path):
    global PROFILE, CURVATURE, CARRY_RELATIONS
    cert = json.loads(path.read_text())
    if cert['schema'] != 's17-joint-capture-pilot-v3':
        raise ValueError('unsupported certificate schema')
    if cert['source_sha256'] != hashlib.sha256(SOURCE.read_bytes()).hexdigest():
        raise ValueError('source hash mismatch')
    if (cert['profile'] not in ('boundary', 'interior') or type(cert['curvature']) is not bool
        or type(cert['carry_relations']) is not bool):
        raise ValueError('invalid model configuration')
    PROFILE, CURVATURE = cert['profile'], cert['curvature']
    CARRY_RELATIONS = cert['carry_relations']
    radius, factor = F(cert['radius']), F(cert['angular_factor'])
    if radius <= 0 or factor <= 0:
        raise ValueError('positive box sizes required')
    bounds = initial_box(radius, factor)
    directions = relation_directions() if CARRY_RELATIONS else {}
    relations = {}
    if not cert['steps']:
        raise ValueError('empty certificate chain')
    objectives = 0
    for step in cert['steps']:
        if bounds != [(F(a),F(b)) for a,b in step['bounds']]:
            raise ValueError('unexpected input box in certificate chain')
        if {name:[str(x) for x in interval] for name,interval in relations.items()} != step['relations']:
            raise ValueError('uncertified relation in certificate chain')
        rows, _ = build_model(bounds,relations,directions)
        if hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest() != step['rows_sha256']:
            raise ValueError('geometry rows do not match reconstruction')
        A, b = parse_rows(rows)
        seen, next_box = set(), [list(pair) for pair in bounds]
        for result in step['results']:
            key = (result['coordinate'], result['sign'])
            if key in seen:
                raise ValueError('duplicate objective')
            seen.add(key)
            bound = dual_bound(A, b, bounds, *key, result['weights'])
            if bound != F(result['lower_bound']):
                raise ValueError('dual bound mismatch')
            i, sign = key
            if sign == 1:
                next_box[i][0] = max(next_box[i][0], bound)
            else:
                next_box[i][1] = min(next_box[i][1], -bound)
        if seen != {(i, s) for i in range(N) for s in (-1, 1)}:
            raise ValueError('missing objective')
        objectives += len(seen)
        relative_seen, endpoints = set(), {}
        for result in step['relative_results']:
            name, sign = result['direction'], result['sign']
            if name not in directions or (name,sign) in relative_seen:
                raise ValueError('invalid relative objective')
            relative_seen.add((name,sign))
            bound = dual_bound(A,b,bounds,None,sign,result['weights'],directions[name])
            if bound != F(result['lower_bound']):
                raise ValueError('relative dual bound mismatch')
            endpoints[(name,sign)] = bound if sign == 1 else -bound
        if relative_seen != {(name,s) for name in directions for s in (-1,1)}:
            raise ValueError('missing relative objective')
        next_relations = {}
        for name,vector in directions.items():
            lo, hi = box_interval(vector,next_box)
            if name in relations:
                lo, hi = max(lo,relations[name][0]), min(hi,relations[name][1])
            next_relations[name] = outward([(max(lo,endpoints[(name,1)]),min(hi,endpoints[(name,-1)]))])[0]
            if next_relations[name][0] > next_relations[name][1]:
                raise ValueError('empty relative enclosure')
        relations = next_relations
        objectives += len(relative_seen)
        bounds = outward(next_box)
        if any(a > b for a,b in bounds):
            raise ValueError('unexpected empty box')
    if [[str(a),str(b)] for a,b in bounds] != cert['final_box']:
        raise ValueError('final box mismatch')
    if {name:[str(x) for x in interval] for name,interval in relations.items()} != cert['final_relations']:
        raise ValueError('final relations mismatch')
    return dict(status='PASS', certificate=str(path), steps=len(cert['steps']), objectives=objectives)


def main():
    global PROFILE, CURVATURE, CARRY_RELATIONS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--radius', default='1/1024')
    parser.add_argument('--angular-factor', type=int, default=1)
    parser.add_argument('--iterations', type=int, default=1)
    parser.add_argument('--profile', choices=('boundary','interior'), default='boundary')
    parser.add_argument('--no-curvature', action='store_true')
    parser.add_argument('--carry-relations', action='store_true')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    if args.check:
        print(json.dumps(check(args.check), indent=2))
        return
    if args.output is None:
        parser.error('--output is required for discovery')
    if args.iterations <= 0:
        parser.error('positive --iterations is required')
    PROFILE, CURVATURE = args.profile, not args.no_curvature
    CARRY_RELATIONS = args.carry_relations
    cert = solve(F(args.radius), args.angular_factor, args.iterations)
    args.output.write_text(json.dumps(cert, indent=2)+'\n')


if __name__ == '__main__':
    main()
