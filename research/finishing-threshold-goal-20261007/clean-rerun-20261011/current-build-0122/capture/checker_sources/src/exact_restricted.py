"""Exact checker for RESTRICTED charge certificates (schema s17-restricted-v1).

Statement checked (see cloud/analysis/RESTRICTED_CHECKER.md):
  in every family of closed unit squares with disjoint interiors inside the square
  container of side S = L/A, at most k-1 squares have a pose outside E*,
where E is the exempt pose set stored in the certificate and E* is
  "orbit": the union of the 8 D4 images of E        (D4-invariant charge, folded rows),
  "core" : the intersection of the 8 images         (D4-invariant charge, folded rows),
  "fixed": E itself, nothing symmetrised            (charge image by image, rows on the
                                                     whole range u = tan(phi/2) in [0,1]).
With E empty and k = 17 the symmetric modes give the published statement.

The files boolean_rule.py, integer_sweep.py and exact_general.py next to this file
are byte-identical copies of bounds/4.6601/global_src; the rectangles, the sweep
geometry and the tree arithmetic are computed by them, unchanged, in every mode.
This file adds
  * the row validation of exact_general.validate with 17 replaced by k, and its
    fixed-image variant (sites/features image by image, rows up to u = 1),
  * the exact decision which sweep cells are CERTAINLY exempt,
  * the sweep over the cells that are not exempt.
All decisions use Python integers / Fractions; int64 only inside the sweep tree
(same 2^50 bound as published).

Two engines decide the same per-cell rule:
  "reference": lists every cell below the threshold and tests rectangles one by one
               (the 08:37 code; needed for disc regions),
  "fast"     : per slab, the exempt cells are index intervals found with exact integer
               arithmetic; the sweep is repeated with the exempt intervals left out.
--audit runs both and demands the same verdict, the same witness and, cell by cell,
the same exemption on the listed cells.
"""
if not __debug__:
    raise SystemExit("Run without -O/-OO and unset PYTHONOPTIMIZE.")
import os
for _k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMBA_NUM_THREADS'):
    os.environ.setdefault(_k, '1')            # before numpy: a fork pool must not meet a threaded BLAS
from fractions import Fraction as F
from math import lcm
from pathlib import Path
from bisect import bisect_left, bisect_right
import sys, json, time, hashlib
import numpy as np
from numba import njit
from integer_sweep import accumulate, add, query, trig, need
from exact_general import expand, geometry
from boolean_rule import expansion

SCHEMA = 's17-restricted-v1'
# the eight symmetries of the container as matrices acting on centred coordinates;
# the first four are rotations (pose angle unchanged mod pi/2), the last four are
# reflections (pose angle negated mod pi/2)
D4 = (((1, 0), (0, 1)), ((0, -1), (1, 0)), ((-1, 0), (0, -1)), ((0, 1), (-1, 0)),
      ((1, 0), (0, -1)), ((-1, 0), (0, 1)), ((0, 1), (1, 0)), ((0, -1), (-1, 0)))
MAX_RUNS = 1 << 24
AUDIT_CELLS = 20000                # --audit compares the two engines cell by cell on up to this many cells per row
HERE = Path(__file__).resolve().parent
SOURCES = ('exact_restricted.py', 'exact_general.py', 'integer_sweep.py', 'boolean_rule.py')


# ----------------------------------------------------------------- parsing
def rat(x):
    need(type(x) is int or type(x) is str, 'rational must be an integer or a string p/q (no floats)')
    try:
        return F(x)
    except (ValueError, ZeroDivisionError):
        raise ValueError('bad rational ' + repr(x))


def keys(obj, required, optional=()):
    need(type(obj) is dict, 'object expected')
    need(set(required) <= set(obj) and set(obj) <= set(required) | set(optional),
         'unknown or missing keys: ' + repr(sorted(obj)))


def point(p):
    need(type(p) is list and len(p) == 2, 'point')
    return (rat(p[0]), rat(p[1]))


def polygon(raw):
    """Closed convex polygon = convex hull of its vertices; vertices must be listed
    counter-clockwise, strictly convex.  Returns the vertex list."""
    need(type(raw) is list and 3 <= len(raw) <= 64, 'polygon needs 3..64 vertices')
    v = [point(p) for p in raw]
    n = len(v)
    for i in range(n):
        (x0, y0), (x1, y1), (x2, y2) = v[i], v[(i + 1) % n], v[(i + 2) % n]
        need((x1 - x0) * (y2 - y1) - (y1 - y0) * (x2 - x1) > 0, 'polygon not strictly convex counter-clockwise')
        # every vertex on the closed left side of every edge: then the intersection of
        # the edge half-planes equals the convex hull of the vertices (winding once)
        for (x, y) in v:
            need((x1 - x0) * (y - y0) - (y1 - y0) * (x - x0) >= 0, 'polygon not convex')
    # winding number one: the edge directions turn left by less than a full extra turn;
    # with all vertices left of all edges a double cover would repeat a vertex
    need(len(set(v)) == n, 'repeated polygon vertex')
    return v


def _slots(raw):
    need(type(raw) is list and 1 <= len(raw) <= 4096, 'slots')
    out = []
    for s in raw:
        keys(s, ('centre',), ('angle_tan_half', 'label'))
        cr = s['centre']
        need(type(cr) is dict and len(cr) == 1, 'slot centre region')
        if 'polygon' in cr:
            region = ('polygon', polygon(cr['polygon']))
        elif 'disc' in cr:
            keys(cr['disc'], ('center', 'radius'))
            rho = rat(cr['disc']['radius'])
            need(rho > 0, 'disc radius')
            region = ('disc', point(cr['disc']['center']), rho)
        else:
            raise ValueError('unknown centre region')
        ang = None
        if 'angle_tan_half' in s:
            a = s['angle_tan_half']
            need(type(a) is list and len(a) == 2, 'angle_tan_half')
            lo, hi = rat(a[0]), rat(a[1])
            need(-1 < lo <= hi < 1, 'angle_tan_half needs -1 < lo <= hi < 1')
            ang = (lo, hi)
        out.append((region, ang))
    return out


def _cells(raw):
    need(type(raw) is list and 1 <= len(raw) <= 4096, 'cells')
    return [polygon(p) for p in raw]


def parse_restriction(c):
    need(type(c) is dict and 'restriction' in c, 'no restriction object: use the published checker')
    r = c['restriction']
    keys(r, ('schema', 'k', 'symmetry', 'frame', 'exempt'), ('comment',))
    need(r['schema'] == SCHEMA, 'unknown restriction schema')
    k = r['k']
    need(type(k) is int and k >= 1, 'k must be a positive integer')
    need(type(r['symmetry']) is str and r['symmetry'] in ('orbit', 'core', 'fixed'),
         "symmetry must be 'orbit', 'core' (D4-symmetric charge) or 'fixed' (fixed-image charge)")
    keys(r['frame'], ('unit', 'center'))
    need(r['frame']['unit'] == 'unit_square', "frame.unit must be 'unit_square'")
    centre = point(r['frame']['center'])
    e = r['exempt']
    need(type(e) is dict and 'kind' in e and type(e['kind']) is str, 'exempt.kind')
    out = dict(k=k, mode=r['symmetry'], centre=centre, kind=e['kind'], slots=[], cells=[])
    if e['kind'] == 'empty':
        keys(e, ('kind',))
    elif e['kind'] == 'slots':
        keys(e, ('kind', 'slots'))
        out['slots'] = _slots(e['slots'])
    elif e['kind'] == 'outside_cells':
        keys(e, ('kind', 'cells'))
        out['cells'] = _cells(e['cells'])
    elif e['kind'] == 'mixed':
        keys(e, ('kind', 'slots', 'cells'))
        out['slots'] = _slots(e['slots'])
        out['cells'] = _cells(e['cells'])
    else:
        raise ValueError('unknown exempt.kind')
    return out


def _head(c):
    L = F(c['L']); A = F(c['A'])
    need(L == F(4613, 1000) and 0 < A < L, 'wrong container/parent')
    need('normalized_target' in c and F(c['normalized_target']) == L / A, 'normalized target')
    den = c.get('weight_denominator'); need(type(den) is int and den > 0, 'denominator')
    need(type(c.get('minimum_units')) is int and c['minimum_units'] > 0 and type(c.get('budget_units')) is int, 'units')
    return L, A


def validate_restricted(c):
    """Returns (data, jobs, spans, minimum margin, R).  Symmetric shape: exact_general.validate
    with the counting constant 17 replaced by restriction.k.  Fixed-image shape: see validate_fixed."""
    R = parse_restriction(c)
    if R['mode'] == 'fixed':
        return validate_fixed(c, R)
    need('sites' not in c and 'features' not in c, "'sites'/'features' belong to symmetry 'fixed'")
    L, A = _head(c)
    data = expand(c); jobs = []; margins = []; spans = []; cursor = F(0)
    for row in c['entries']:
        a, b, t, B = map(F, row); need(a == cursor and 0 <= a < b < 1 and 0 <= t < 1 and 0 < B < A, 'catalogue coverage')
        cc, ss = trig(t); f = []; g = []
        for u in (a, b):
            c0, s0 = trig(u); dot = cc * c0 + ss * s0; cross = abs(cc * s0 - ss * c0)
            need(dot > 0 and dot >= cross, 'angle range'); f.append(c0 + s0); g.append(dot + cross)
        margin = A - B * max(g); need(margin > 0, 'core not strict'); margins.append(margin); r = A * min(f) / 2
        need(B * (cc + ss) / 2 <= r < L / 2, 'parent envelope'); jobs.append((t, B, L / 2 - r)); spans.append((a, b)); cursor = b
    need(cursor * cursor + 2 * cursor > 1, 'angle gap')
    need(R['k'] * c['minimum_units'] > c['budget_units'], 'counting budget')
    R['A'] = A
    return data, jobs, spans, min(margins), R


def validate_fixed(c, R=None):
    """Fixed-image shape: sites and features image by image (no orbit closure, no tied weights),
    rows a gapless chain in u = tan(phi/2) from 0 to exactly 1 (all side directions in [0, pi/2]).
    Returns data in the form exact_general.geometry takes: all site weights 0, one trigger per
    feature image with its own weight."""
    if R is None:
        R = parse_restriction(c)
    need(R['mode'] == 'fixed', 'not a fixed-image restriction')
    need('point_orbits' not in c and 'threshold_orbits' not in c, "'point_orbits'/'threshold_orbits' belong to the symmetric modes")
    need(type(c.get('L')) in (int, str) and type(c.get('A')) in (int, str) and type(c.get('normalized_target')) in (int, str),
         'L, A, normalized_target must be rationals')
    L, A = _head(c)
    D = c.get('coordinate_denominator')
    need(type(D) is int and D > 0 and (L * D).denominator == 1, 'invalid coordinate scale'); LD = int(L * D)
    raw = c.get('sites')
    need(type(raw) is list and len(raw) >= 1, 'sites')
    sites = []
    for p in raw:
        need(type(p) is list and len(p) == 2 and type(p[0]) is int and type(p[1]) is int and 0 <= p[0] <= LD and 0 <= p[1] <= LD, 'invalid site')
        sites.append((p[0], p[1]))
    need(len(set(sites)) == len(sites), 'duplicate site')
    feats = c.get('features')
    need(type(feats) is list, 'features')
    triggers = []; tw = []; budget = 0; absolute = 0
    for f in feats:
        keys(f, ('sites', 'weight'), ('threshold', 'coefficients', 'winning_masks'))
        idx = f['sites']; w = f['weight']
        need(type(w) is int and w >= 0, 'invalid feature weight')
        need(type(idx) is list and 1 <= len(idx) <= 20 and len(set(idx)) == len(idx)
             and all(type(i) is int and 0 <= i < len(sites) for i in idx), 'invalid feature sites')
        n = len(idx)
        coeff = f.get('coefficients', [1] * n)
        need(type(coeff) is list and len(coeff) == n and all(type(v) is int and v > 0 for v in coeff)
             and coeff == sorted(coeff, reverse=True), 'invalid site coefficients')
        coeff = tuple(coeff)
        rules = f.get('winning_masks', [])
        need(type(rules) is list, 'winning_masks')
        if rules:
            need(n <= 12 and len(set(rules)) == len(rules) and all(type(v) is int and 0 < v < 2 ** n for v in rules)
                 and all(a & b for a in rules for b in rules), 'invalid intersecting rule')
        else:
            need('winning_masks' not in f, 'empty winning_masks')
            need('threshold' in f, 'threshold missing')
        k = f.get('threshold', 1)
        need(type(k) is int and 1 <= k <= sum(coeff), 'invalid threshold')
        rules = tuple(rules)
        triggers.append((tuple(idx), k, coeff, rules)); tw.append(w)
        budget += (1 if rules else sum(coeff) // k) * w
        absolute += w * sum(abs(a) for _, a in expansion(coeff, k, rules))
    need(budget == c['budget_units'] and absolute < 2 ** 50, 'budget/overflow')
    need(any(tw), 'no feature with positive weight')
    data = (sites, [0] * len(sites), triggers, tw, D)
    rows = c.get('entries')
    need(type(rows) is list and len(rows) >= 1, 'entries')
    jobs = []; margins = []; spans = []; cursor = F(0)
    for row in rows:
        need(type(row) is list and len(row) == 4, 'row')
        a, b, t, B = map(rat, row)
        need(a == cursor and 0 <= a < b <= 1 and 0 <= t < 1 and 0 < B < A, 'catalogue coverage')
        cc, ss = trig(t); f = []; g = []
        for u in (a, b):
            c0, s0 = trig(u); dot = cc * c0 + ss * s0; cross = abs(cc * s0 - ss * c0)
            need(dot > 0 and dot >= cross, 'angle range'); f.append(c0 + s0); g.append(dot + cross)
        margin = A - B * max(g); need(margin > 0, 'core not strict'); margins.append(margin); r = A * min(f) / 2
        need(B * (cc + ss) / 2 <= r < L / 2, 'parent envelope'); jobs.append((t, B, L / 2 - r)); spans.append((a, b)); cursor = b
    need(cursor == 1, 'angle gap: fixed-image rows must end exactly at u = 1 (side direction pi/2)')
    need(R['k'] * c['minimum_units'] > c['budget_units'], 'counting budget')
    R['A'] = A
    return data, jobs, spans, min(margins), R


# ----------------------------------------------------------------- deficient cells (reference engine)
@njit
def _collect(mn, lazy, k, a, b, lo, hi, acc, thr, slab, out, cnt):
    """Append to out every leaf (y-cell) of [lo,hi) whose value is < thr, as maximal runs
    (slab, j0, j1, minimum) in increasing j.  Returns the new run count (may exceed the
    capacity; then the caller must retry with a larger buffer)."""
    if hi <= a or b <= lo:
        return cnt
    v = mn[k] + acc
    if v >= thr:
        return cnt
    if b - a == 1:
        cap = out.shape[0]
        if cnt > 0 and cnt <= cap and out[cnt - 1, 0] == slab and out[cnt - 1, 2] == a:
            out[cnt - 1, 2] = a + 1
            if v < out[cnt - 1, 3]:
                out[cnt - 1, 3] = v
            return cnt
        if cnt < cap:
            out[cnt, 0] = slab; out[cnt, 1] = a; out[cnt, 2] = a + 1; out[cnt, 3] = v
        return cnt + 1
    mid = (a + b) // 2
    acc2 = acc + lazy[k]
    cnt = _collect(mn, lazy, 2 * k, a, mid, lo, hi, acc2, thr, slab, out, cnt)
    cnt = _collect(mn, lazy, 2 * k + 1, mid, b, lo, hi, acc2, thr, slab, out, cnt)
    return cnt


@njit
def accumulate_restricted(nv, evindex, atomindex, sign, ylo, yhi, weights, first, last, thr, out):
    """The published sweep (integer_sweep.accumulate, tree mode) that additionally lists
    every checked cell with charge < thr."""
    n = 1
    while n < nv:
        n *= 2
    mn = np.zeros(2 * n, np.int64); lazy = np.zeros(2 * n, np.int64)
    p = 0; best = np.int64(2 ** 60); cells = np.int64(0); cnt = np.int64(0)
    for k in range(len(first)):
        while p < len(evindex) and evindex[p] == k:
            j = atomindex[p]; w = sign[p] * weights[j]
            add(mn, lazy, 1, 0, n, ylo[j], yhi[j], w)
            p += 1
        if first[k] >= 0:
            z = query(mn, lazy, 1, 0, n, first[k], last[k])
            if z < best:
                best = z
            cells += last[k] - first[k]
            if z < thr:
                cnt = _collect(mn, lazy, 1, 0, n, first[k], last[k], np.int64(0), np.int64(thr), np.int64(k), out, cnt)
    return best, cells, cnt


def deficient_direct(arrays, thr):
    """Slow independent enumeration (numpy difference arrays, no tree) of the deficient
    cells; used by the tests to audit accumulate_restricted."""
    nv, evindex, atomindex, sign, ylo, yhi, weights, first, last = arrays
    masses = np.zeros(nv, np.int64); p = 0; found = set()
    for k in range(len(first)):
        while p < len(evindex) and evindex[p] == k:
            j = atomindex[p]; masses[ylo[j]:yhi[j]] += sign[p] * weights[j]; p += 1
        if first[k] >= 0:
            for j in np.nonzero(masses[first[k]:last[k]] < thr)[0]:
                found.add((k, int(first[k] + j)))
    return found


# ----------------------------------------------------------------- sweeps of the fast engine
@njit
def slab_minima(nv, evindex, atomindex, sign, ylo, yhi, weights, first, last):
    """The published sweep, additionally returning the minimum of every checked slab."""
    n = 1
    while n < nv:
        n *= 2
    mn = np.zeros(2 * n, np.int64); lazy = np.zeros(2 * n, np.int64)
    out = np.full(len(first), 2 ** 60, np.int64)
    p = 0; best = np.int64(2 ** 60); cells = np.int64(0)
    for k in range(len(first)):
        while p < len(evindex) and evindex[p] == k:
            j = atomindex[p]; w = sign[p] * weights[j]
            add(mn, lazy, 1, 0, n, ylo[j], yhi[j], w)
            p += 1
        if first[k] >= 0:
            z = query(mn, lazy, 1, 0, n, first[k], last[k])
            out[k] = z
            if z < best:
                best = z
            cells += last[k] - first[k]
    return best, cells, out


@njit
def _first_below(mn, lazy, k, a, b, lo, hi, acc, thr):
    """Index of the first leaf of [lo,hi) with value < thr, or -1."""
    if hi <= a or b <= lo:
        return -1
    v = mn[k] + acc
    if v >= thr:
        return -1
    if b - a == 1:
        return a
    mid = (a + b) // 2
    acc2 = acc + lazy[k]
    r = _first_below(mn, lazy, 2 * k, a, mid, lo, hi, acc2, thr)
    if r >= 0:
        return r
    return _first_below(mn, lazy, 2 * k + 1, mid, b, lo, hi, acc2, thr)


@njit
def accumulate_intervals(nv, evindex, atomindex, sign, ylo, yhi, weights, first, last, flag, ptr, ivlo, ivhi, thr):
    """The published sweep in which, for the slabs with flag 1, the query range [first,last) is
    replaced by the listed index intervals ivlo[i]..ivhi[i]-1, ptr[k] <= i < ptr[k+1] (the cells of
    the slab that are NOT exempt).  Slabs with flag 0 are queried on their whole range.  Returns the
    minimum over everything queried and the first cell (slab, y-cell) below thr, or -1, -1."""
    n = 1
    while n < nv:
        n *= 2
    mn = np.zeros(2 * n, np.int64); lazy = np.zeros(2 * n, np.int64)
    p = 0; best = np.int64(2 ** 60); wk = np.int64(-1); wj = np.int64(-1); queried = np.int64(0)
    for k in range(len(first)):
        while p < len(evindex) and evindex[p] == k:
            j = atomindex[p]; w = sign[p] * weights[j]
            add(mn, lazy, 1, 0, n, ylo[j], yhi[j], w)
            p += 1
        if first[k] >= 0:
            if flag[k] == 0:
                z = query(mn, lazy, 1, 0, n, first[k], last[k])
                queried += last[k] - first[k]
                if z < best:
                    best = z
                if z < thr and wk < 0:
                    wk = k; wj = _first_below(mn, lazy, 1, 0, n, first[k], last[k], np.int64(0), thr)
            else:
                for i in range(ptr[k], ptr[k + 1]):
                    z = query(mn, lazy, 1, 0, n, ivlo[i], ivhi[i])
                    queried += ivhi[i] - ivlo[i]
                    if z < best:
                        best = z
                    if z < thr and wk < 0:
                        wk = k; wj = _first_below(mn, lazy, 1, 0, n, ivlo[i], ivhi[i], np.int64(0), thr)
    return best, wk, wj, queried


# ----------------------------------------------------------------- exemption test
def _ints(*vals):
    m = 1
    for v in vals:
        m = lcm(m, F(v).denominator)
    return [int(F(v) * m) for v in vals], m


class RowExemption:
    """Reference engine.  Decides, for one row (angle interval [a,b] in tan-half-angle, core
    angle t), whether a closed sweep rectangle [u0,u1]x[v0,v1] (integer sweep coordinates) times
    the closed angle interval is certainly inside E* .

    Sweep coordinates: u = scale*(C x' + S y'), v = scale*(-S x' + C y') with (x',y') the
    centre in certificate units relative to the container centre and C,S,R integers,
    C^2+S^2=R^2.  Hence (x',y') = W(u,v)/(scale R^2), W=[[C,-S],[S,C]].  The frame point of
    the image of this centre under the symmetry M is e = centre_F + M (x',y')/A, i.e.
    e = centre_F + N(u,v)/K with N = M W (integer) and K = A*scale*R^2 > 0.

    Modes 'orbit' / 'core': the eight images M in D4 (one / all must succeed).  Mode 'fixed':
    the identity only, i.e. E exactly as written."""

    def __init__(self, R, meta, a, b):
        self.kind = R['kind']; self.mode = R['mode']; self.tests = 0
        C, S, RR, scale = meta['C'], meta['S'], meta['R'], meta['scale']
        need(C * C + S * S == RR * RR and RR > 0 and scale > 0, 'rotation')
        K = R['A'] * scale * RR * RR
        cx, cy = R['centre']
        self.images = []
        for M in (D4[:1] if self.mode == 'fixed' else D4):
            N = ((M[0][0] * C + M[0][1] * S, -M[0][0] * S + M[0][1] * C),
                 (M[1][0] * C + M[1][1] * S, -M[1][0] * S + M[1][1] * C))
            det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
            need(N[0][0] * N[1][1] - N[0][1] * N[1][0] == det * RR * RR, 'similarity')
            I = (a, b) if det == 1 else (-b, -a)
            regs = []
            for region, ang in R['slots']:
                if ang is not None and not self._angles_inside(I, ang):
                    continue
                if region[0] == 'polygon':
                    regs.append(('polygon', self._forms(region[1], N, K, cx, cy), self._box(region[1], N, R['A'] * scale, cx, cy)))
                else:
                    (px, py), rho = region[1], region[2]
                    (ox, oy), den = _ints(K * (cx - px), K * (cy - py))
                    rhs = (den * K * rho) ** 2
                    regs.append(('disc', N, den, ox, oy, rhs.numerator, rhs.denominator))
            polys = []
            for v in R['cells']:
                box, den, verts = self._box(v, N, R['A'] * scale, cx, cy)
                polys.append((box, den, self._forms(v, N, K, cx, cy), verts))
            self.images.append((regs, polys))

    @staticmethod
    def _angles_inside(I, J):
        """[I] subset of [J] + m*pi/2 for one integer m.  All quantities are tan(angle/2) of
        angles in (-pi,pi), where tan(x/2) is increasing; the quarter-turn shift is the
        Mobius map t -> (1+t)/(1-t) (and its inverse t -> (t-1)/(t+1)).  I lies in [-1,1]
        (angles in [-pi/2,pi/2]), J in (-1,1); then only m in {-1,0,1} can succeed."""
        lo, hi = J
        need(-1 < lo <= hi < 1 and -1 <= I[0] <= I[1] <= 1, 'angle chart')
        for m in (-1, 0, 1):
            if m == 0:
                l2, h2 = lo, hi
            elif m == 1:
                l2, h2 = (1 + lo) / (1 - lo), (1 + hi) / (1 - hi)
            else:
                l2, h2 = (lo - 1) / (lo + 1), (hi - 1) / (hi + 1)
            if l2 <= I[0] and I[1] <= h2:
                return True
        return False

    @staticmethod
    def _forms(v, N, K, cx, cy):
        """For every edge p1->p2 of the counter-clockwise polygon an integer form (a,b,c) with
        a*u+b*v+c of the same sign as n.(e-p1), n the inward (left) normal of the edge."""
        forms = []; n = len(v)
        for i in range(n):
            (x1, y1), (x2, y2) = v[i], v[(i + 1) % n]
            n0, n1 = -(y2 - y1), (x2 - x1)
            (a, b, c), _ = _ints(n0 * N[0][0] + n1 * N[1][0], n0 * N[0][1] + n1 * N[1][1],
                                 K * (n0 * (cx - x1) + n1 * (cy - y1)))
            forms.append((a, b, c))
        return forms

    @staticmethod
    def _box(v, N, As, cx, cy):
        """Sweep coordinates of the polygon vertices (the pre-image of the frame polygon under
        (u,v) -> centre_F + N(u,v)/K), as integers over a common denominator den, with the
        bounding values: ((umin, umax, vmin, vmax), den, [(U_i, V_i)])."""
        us = [(N[0][0] * (x - cx) + N[1][0] * (y - cy)) * As for x, y in v]
        vs = [(N[0][1] * (x - cx) + N[1][1] * (y - cy)) * As for x, y in v]
        vals, den = _ints(*(us + vs))
        n = len(v); U = vals[:n]; V = vals[n:]
        return (min(U), max(U), min(V), max(V)), den, list(zip(U, V))

    # --- rectangle tests (closed rectangle, integer corners) ---
    @staticmethod
    def _inside_polygon(forms, u0, u1, v0, v1):
        return all(c + min(a * u0, a * u1) + min(b * v0, b * v1) >= 0 for a, b, c in forms)

    @staticmethod
    def _inside_disc(reg, u0, u1, v0, v1):
        _, N, den, ox, oy, num, dd = reg
        for u in (u0, u1):
            for v in (v0, v1):
                X = den * (N[0][0] * u + N[0][1] * v) + ox; Y = den * (N[1][0] * u + N[1][1] * v) + oy
                if (X * X + Y * Y) * dd > num:
                    return False
        return True

    @staticmethod
    def _separated(poly, u0, u1, v0, v1):
        (umin, umax, vmin, vmax), den, forms = poly[0], poly[1], poly[2]
        if u1 * den < umin or u0 * den > umax or v1 * den < vmin or v0 * den > vmax:
            return True
        return any(c + max(a * u0, a * u1) + max(b * v0, b * v1) < 0 for a, b, c in forms)

    def _image_ok(self, image, u0, u1, v0, v1):
        regs, polys = image
        for reg in regs:
            if reg[0] == 'polygon':
                if self._inside_polygon(reg[1], u0, u1, v0, v1):
                    return True
            elif self._inside_disc(reg, u0, u1, v0, v1):
                return True
        return bool(polys) and all(self._separated(p, u0, u1, v0, v1) for p in polys)

    def exempt(self, u0, u1, v0, v1):
        need(u0 < u1 and v0 < v1, 'degenerate cell')
        self.tests += 1
        if self.kind == 'empty':
            return False
        results = (self._image_ok(image, u0, u1, v0, v1) for image in self.images)
        return all(results) if self.mode == 'core' else any(results)


# --- index-interval sets: sorted lists of disjoint, non-adjacent half-open pairs (j0, j1) ---
def _merge(iv):
    out = []
    for lo, hi in sorted(iv):
        if lo >= hi:
            continue
        if out and lo <= out[-1][1]:
            if hi > out[-1][1]:
                out[-1] = (out[-1][0], hi)
        else:
            out.append((lo, hi))
    return out


def _intersect(X, Y):
    out = []; i = j = 0
    while i < len(X) and j < len(Y):
        lo = max(X[i][0], Y[j][0]); hi = min(X[i][1], Y[j][1])
        if lo < hi:
            out.append((lo, hi))
        if X[i][1] < Y[j][1]:
            i += 1
        else:
            j += 1
    return out


def _complement(X, lo, hi):
    """[lo, hi) minus the merged set X."""
    out = []; cur = lo
    for a, b in X:
        if b <= cur:
            continue
        if a >= hi:
            break
        if a > cur:
            out.append((cur, a))
        cur = max(cur, b)
    if cur < hi:
        out.append((cur, hi))
    return out


class SlabExemption(RowExemption):
    """Fast engine: the same per-cell rule as RowExemption.exempt, evaluated per slab.  For a slab
    [u0,u1] and a convex region the y-cells whose closed rectangle lies in the region form one
    index interval; for a convex polygon the y-cells whose closed rectangle meets it form one
    index interval.  Both are found with integer arithmetic on the same forms / vertices."""

    def __init__(self, R, meta, a, b):
        RowExemption.__init__(self, R, meta, a, b)
        need(all(reg[0] == 'polygon' for regs, _ in self.images for reg in regs), 'the fast engine has no disc regions')
        self.xe = meta['xe']; self.ye = meta['ye']; self.nv = len(self.ye) - 1; self.slab_tests = 0

    def _slot_interval(self, reg, u0, u1):
        """y-cells j with [u0,u1] x [ye_j, ye_j+1] inside the polygon: all four corners satisfy
        every form, i.e. for b > 0: ye_j >= ceil(-m/b), for b < 0: ye_j+1 <= floor(m/-b),
        for b = 0: m >= 0, with m = c + min(a u0, a u1)."""
        (umin, umax, _, _), den, _ = reg[2]
        if u0 * den < umin or u1 * den > umax:
            return None
        LO = None; HI = None
        for a, b, c in reg[1]:
            m = c + min(a * u0, a * u1)
            if b > 0:
                x = -(m // b)
                if LO is None or x > LO:
                    LO = x
            elif b < 0:
                x = m // (-b)
                if HI is None or x < HI:
                    HI = x
            elif m < 0:
                return None
        jl = 0 if LO is None else bisect_left(self.ye, LO)
        jh = self.nv if HI is None else bisect_right(self.ye, HI) - 1
        return (jl, jh) if jl < jh else None

    def _blocked_interval(self, poly, u0, u1):
        """y-cells j whose closed rectangle [u0,u1] x [ye_j, ye_j+1] meets the closed polygon:
        those meeting the exact v-range of (polygon intersected with the slab)."""
        (umin, umax, _, _), den, _, verts = poly
        a0 = u0 * den; a1 = u1 * den
        if a1 < umin or a0 > umax:
            return None
        lo = hi = None
        n = len(verts)
        for i in range(n):
            U1, V1 = verts[i]; U2, V2 = verts[(i + 1) % n]
            cand = []
            if a0 <= U1 <= a1:
                cand.append(F(V1))
            if U1 != U2:
                for x in (a0, a1):
                    if min(U1, U2) <= x <= max(U1, U2):
                        cand.append(V1 + F((V2 - V1) * (x - U1), U2 - U1))
            for y in cand:
                if lo is None or y < lo:
                    lo = y
                if hi is None or y > hi:
                    hi = y
        if lo is None:
            return None
        # cell j meets [lo, hi]/den  iff  ye_j+1 >= ceil(lo/den)  and  ye_j <= floor(hi/den)
        pmin = -((-lo.numerator) // (lo.denominator * den)); pmax = hi.numerator // (hi.denominator * den)
        j0 = max(0, bisect_left(self.ye, pmin) - 1); j1 = min(self.nv, bisect_right(self.ye, pmax))
        return (j0, j1) if j0 < j1 else None

    def _image_set(self, image, u0, u1):
        regs, polys = image
        out = []
        for reg in regs:
            iv = self._slot_interval(reg, u0, u1)
            if iv is not None:
                out.append(iv)
        if polys:
            blocked = []
            for p in polys:
                iv = self._blocked_interval(p, u0, u1)
                if iv is not None:
                    blocked.append(iv)
            out += _complement(_merge(blocked), 0, self.nv)
        self.slab_tests += len(regs) + len(polys)
        return _merge(out)

    def exempt_set(self, k):
        """The exempt y-cells of slab k as a merged interval set."""
        if self.kind == 'empty':
            return []
        u0, u1 = self.xe[k], self.xe[k + 1]
        need(u0 < u1, 'degenerate slab')
        sets = [self._image_set(image, u0, u1) for image in self.images]
        if self.mode == 'core':
            X = sets[0]
            for Y in sets[1:]:
                X = _intersect(X, Y)
            return X
        return _merge([iv for X in sets for iv in X])


# ----------------------------------------------------------------- one row
def _witness(R, meta, k, j):
    xe, ye = meta['xe'], meta['ye']
    K = R['A'] * meta['scale'] * meta['R'] ** 2; C, S = meta['C'], meta['S']; cx, cy = R['centre']
    return dict(slab=k, ycell=j, frame_corners=[[str(cx + (C * u - S * v) / K), str(cy + (S * u + C * v) / K)]
                                                for u in (xe[k], xe[k + 1]) for v in (ye[j], ye[j + 1])])


def _run_reference(arrays, meta, R, a, b, minimum, z, cells, audit, rec):
    cap = 1 << 16
    while True:
        out = np.zeros((cap, 4), np.int64)
        z2, cells2, cnt = accumulate_restricted(*arrays, np.int64(minimum), out)
        cnt = int(cnt)
        if cnt <= cap:
            break
        need(cnt <= MAX_RUNS, 'too many deficient runs')
        cap = 1 << (cnt - 1).bit_length()
    need(int(z2) == z and int(cells2) == cells and cnt > 0, 'restricted sweep disagrees with published sweep')
    runs = out[:cnt]
    need(int(runs[:, 3].min()) == z and bool(np.all(runs[:, 2] > runs[:, 1])), 'deficient list inconsistent')
    rec['deficient_runs'] = cnt; rec['deficient_cells'] = int((runs[:, 2] - runs[:, 1]).sum())
    direct = None
    if audit:
        listed = {(int(k), j) for k, j0, j1, _ in runs for j in range(int(j0), int(j1))}
        direct = deficient_direct(arrays, minimum)
        need(listed == direct, 'audit: direct enumeration disagrees')
    xe, ye = meta['xe'], meta['ye']
    tester = RowExemption(R, meta, a, b)
    witness = None
    stack = [(int(k), int(j0), int(j1)) for k, j0, j1, _ in runs[::-1]]
    while stack:
        k, j0, j1 = stack.pop()
        if tester.exempt(xe[k], xe[k + 1], ye[j0], ye[j1]):
            continue
        if j1 - j0 == 1:
            witness = (k, j0)
            break
        mid = (j0 + j1) // 2
        stack.append((k, mid, j1)); stack.append((k, j0, mid))
    rec['exemption_tests'] = tester.tests
    return witness, direct


def _run_fast(arrays, meta, R, a, b, minimum, z, cells, rec):
    first, last = arrays[7], arrays[8]
    zb, cellsb, zs = slab_minima(*arrays)
    need(int(zb) == z and int(cellsb) == cells, 'slab sweep disagrees with published sweep')
    deficient = np.nonzero((first >= 0) & (zs < minimum))[0]
    need(len(deficient) > 0, 'no deficient slab below the row minimum')
    tester = SlabExemption(R, meta, a, b)
    nslab = len(first)
    flag = np.zeros(nslab, np.int64); count = np.zeros(nslab + 1, np.int64); lo = []; hi = []; sets = {}
    for k in deficient:
        k = int(k)
        X = tester.exempt_set(k)
        sets[k] = X
        must = _complement(X, int(first[k]), int(last[k]))
        flag[k] = 1; count[k + 1] = len(must)
        for j0, j1 in must:
            need(first[k] <= j0 < j1 <= last[k], 'interval outside the checked range')
            lo.append(j0); hi.append(j1)
    ptr = np.cumsum(count)
    best, wk, wj, queried = accumulate_intervals(*arrays, flag, ptr, np.array(lo, np.int64), np.array(hi, np.int64), np.int64(minimum))
    best = int(best); wk = int(wk); wj = int(wj)
    rec['deficient_slabs'] = int(len(deficient)); rec['slab_tests'] = tester.slab_tests; rec['cells_required'] = int(queried)
    need((best < minimum) == (wk >= 0) and (wk < 0 or wj >= 0), 'witness inconsistent')
    rec['deficit_minimum_units'] = best if best < minimum else None
    witness = None
    if wk >= 0:
        witness = (wk, wj)
        # the failing cell must also fail the reference rule (one rectangle test)
        xe, ye = meta['xe'], meta['ye']
        if not any(reg[0] == 'disc' for regs, _ in tester.images for reg in regs):
            need(not RowExemption(R, meta, a, b).exempt(xe[wk], xe[wk + 1], ye[wj], ye[wj + 1]), 'fast engine: witness cell is exempt by the reference rule')
    return witness, sets


def check_row(data, job, span, R, minimum, audit=False, engine=None):
    """Returns a dict; 'passed' is True only if every checked sweep cell has charge
    >= minimum or is certainly exempt.  engine: 'fast', 'reference' or None (fast unless the
    exempt set has a disc region).  audit: both engines and the direct enumeration, compared."""
    a, b = span
    arrays, meta = geometry(*data, *job, meta=True)
    z, cells, _ = accumulate(*arrays)
    z = int(z); cells = int(cells)
    rec = dict(minimum_units=z, cells=cells, deficient_cells=0, deficient_runs=0, deficient_slabs=0, exemption_tests=0,
               slab_tests=0, deficit_minimum_units=None, engine='none', passed=z >= minimum)
    if z >= minimum:
        if audit:
            need(not deficient_direct(arrays, minimum), 'audit: direct enumeration disagrees')
        return rec
    has_disc = any(region[0] == 'disc' for region, _ in R['slots'])
    if engine is None:           # E empty: every deficient cell is a failure; the reference engine counts them as before
        engine = 'reference' if has_disc or R['kind'] == 'empty' else 'fast'
    need(engine in ('fast', 'reference'), 'unknown engine')
    need(not (engine == 'fast' and has_disc), 'disc regions need the reference engine')
    use_ref = engine == 'reference' or audit
    use_fast = engine == 'fast' or (audit and not has_disc)
    rec['engine'] = '+'.join(n for n, on in (('fast', use_fast), ('reference', use_ref)) if on)
    wr = wf = None
    if use_ref:
        wr, direct = _run_reference(arrays, meta, R, a, b, minimum, z, cells, audit, rec)
    else:
        rec['deficient_cells'] = rec['deficient_runs'] = None        # not enumerated by the fast engine
    if use_fast:
        wf, sets = _run_fast(arrays, meta, R, a, b, minimum, z, cells, rec)
    if use_ref and use_fast:
        need(wr == wf, 'audit: the two engines disagree (%r, %r)' % (wr, wf))
        if audit and len(direct) <= AUDIT_CELLS:
            xe, ye = meta['xe'], meta['ye']; ref = RowExemption(R, meta, a, b); low = None
            for k, j in sorted(direct):
                inside = any(j0 <= j < j1 for j0, j1 in sets[k])
                need(ref.exempt(xe[k], xe[k + 1], ye[j], ye[j + 1]) == inside, 'audit: exemption of cell (%d,%d) differs between the engines' % (k, j))
            rec['audit_cells'] = len(direct)
    witness = wf if use_fast else wr
    rec['passed'] = witness is None
    if witness is not None:
        rec['witness'] = _witness(R, meta, *witness)
    return rec


def statement(c, R):
    S = F(c['L']) / F(c['A']); kk = R['k']
    what = {'empty': 'any pose',
            'slots': 'a pose outside E* (E = union of the listed slots)',
            'outside_cells': 'a pose outside E* (E = poses whose centre is outside the union of the listed cells)',
            'mixed': 'a pose outside E* (E = union of the listed slots and of the poses whose centre is outside the union of the listed cells)'}[R['kind']]
    star = '' if R['kind'] == 'empty' else {'orbit': ' E* = union of the eight D4 images of E.',
                                             'core': ' E* = intersection of the eight D4 images of E (a subset of E).',
                                             'fixed': ' E* = E exactly as stored (fixed image, nothing symmetrised).'}[R['mode']]
    return ('In every family of closed unit squares with disjoint interiors inside a square of side %s, '
            'at most %d squares have %s.%s' % (S, kk - 1, what, star))


# ----------------------------------------------------------------- D4 images of an exempt set (lemma L3)
def image_exempt(exempt, centre, g):
    """The JSON exempt object of the image E^G, G = D4[g] acting about `centre` (frame point of
    the container centre): polygons and disc centres are mapped, reflected polygons are re-listed
    counter-clockwise, and a gate [lo,hi] becomes [-hi,-lo] under a reflection."""
    M = D4[g]; det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    cx, cy = point(centre)

    def pt(p):
        x, y = point(p); dx, dy = x - cx, y - cy
        return [str(cx + M[0][0] * dx + M[0][1] * dy), str(cy + M[1][0] * dx + M[1][1] * dy)]

    def poly(v):
        w = [pt(p) for p in v]
        return w if det == 1 else [w[0]] + w[:0:-1]
    out = dict(kind=exempt['kind'])
    if 'slots' in exempt:
        out['slots'] = []
        for s in exempt['slots']:
            t = dict(s)
            if 'polygon' in s['centre']:
                t['centre'] = dict(polygon=poly(s['centre']['polygon']))
            else:
                t['centre'] = dict(disc=dict(center=pt(s['centre']['disc']['center']), radius=s['centre']['disc']['radius']))
            if 'angle_tan_half' in s and det == -1:
                lo, hi = map(rat, s['angle_tan_half']); t['angle_tan_half'] = [str(-hi), str(-lo)]
            out['slots'].append(t)
    if 'cells' in exempt:
        out['cells'] = [poly(v) for v in exempt['cells']]
    return out


# ----------------------------------------------------------------- command line
def checker_sha256():
    return {n: hashlib.sha256((HERE / n).read_bytes()).hexdigest() for n in SOURCES}


def load(path, restriction=None):
    """Reads a certificate; with `restriction` (a path) the restriction object is taken from that
    file.  Returns (certificate dict, sha256 of the certificate file, sha256 of the restriction file or None)."""
    raw = Path(path).read_bytes(); c = json.loads(raw); rsha = None
    need(type(c) is dict, 'certificate must be a JSON object')
    if restriction is not None:
        need('restriction' not in c, 'the certificate already has a restriction object')
        rraw = Path(restriction).read_bytes(); r = json.loads(rraw); rsha = hashlib.sha256(rraw).hexdigest()
        if type(r) is dict and type(r.get('restriction')) is dict:      # a wrapper file (e.g. exempt/<entry>/C01.json)
            r = r['restriction']
        c['restriction'] = r
    return c, hashlib.sha256(raw).hexdigest(), rsha


_JOB = None


def _work(i):
    data, jobs, spans, R, minimum, audit, engine = _JOB
    t0 = time.process_time()
    rec = check_row(data, jobs[i], spans[i], R, minimum, audit=audit, engine=engine)
    rec['interval'] = i; rec['cpu_seconds'] = round(time.process_time() - t0, 4)
    return rec


def _warm():
    """Compile every numba routine in this process (before a pool is forked)."""
    ev = np.array([[0, 0, 1], [1, 0, -1]], np.int64)      # column slices are strided, as in geometry()
    one = np.ones(1, np.int64); zero = np.zeros(1, np.int64)
    arrays = (1, ev[:, 0], ev[:, 1], ev[:, 2], zero, one, np.array([5], np.int64), np.array([0, 0], np.int64), np.array([1, 1], np.int64))
    need(int(accumulate(*arrays)[0]) == 0 and int(slab_minima(*arrays)[0]) == 0, 'warm-up sweep')
    out = np.zeros((4, 4), np.int64)
    need(int(accumulate_restricted(*arrays, np.int64(1), out)[2]) == 1 and int(out[0, 0]) == 1, 'warm-up listing')
    r = accumulate_intervals(*arrays, np.array([1, 1], np.int64), np.array([0, 1, 2], np.int64), np.array([0, 0], np.int64),
                             np.array([1, 1], np.int64), np.int64(1))
    need(int(r[0]) == 0 and int(r[1]) == 1 and int(r[2]) == 0, 'warm-up interval sweep')


def merge(c, csha, rsha, R, total, paths):
    """Aggregates slice results.  The complete statement is given only if every row 0..total-1
    is present, every record of it passed, and all slices are for this certificate, this
    restriction, this checker."""
    sha = checker_sha256(); problems = []; seen = {}; failed = set(); names = []
    for path in paths:
        d = json.loads(Path(path).read_text()); names.append(str(path))
        for key, want in (('certificate_sha256', csha), ('restriction_sha256', rsha), ('checker_sha256', sha), ('schema', SCHEMA),
                          ('k', R['k']), ('symmetry', R['mode']), ('exempt_kind', R['kind']), ('total_intervals', total),
                          ('required_units', c['minimum_units']), ('budget_units', c['budget_units'])):
            if d.get(key) != want:
                problems.append('%s: %s differs' % (path, key))
        rows = d.get('rows')
        if type(rows) is not list or [r.get('interval') for r in rows] != list(range(d.get('start', -1), d.get('end_exclusive', -1))):
            problems.append('%s: rows do not match start/end_exclusive' % path); continue
        for r in rows:
            i = r['interval']
            ok = r.get('passed') is True and type(r.get('minimum_units')) is int and r.get('deficit_minimum_units') is None
            if not ok or (r['minimum_units'] < c['minimum_units'] and r.get('engine', 'none') == 'none'):
                failed.add(i)
            seen[i] = seen.get(i, 0) + 1
    missing = [i for i in range(total) if i not in seen]
    extra = sorted(i for i in seen if not (type(i) is int and 0 <= i < total))
    if extra:
        problems.append('rows outside the certificate: %r' % extra[:10])
    status = ('RESTRICTED_EXACT_COVERAGE_FAILURE' if failed else 'MERGE_INCOMPLETE' if problems or missing else 'PASS_RESTRICTED_EXACT_COVER')
    return dict(status=status, statement=statement(c, R) if status == 'PASS_RESTRICTED_EXACT_COVER' else None, schema=SCHEMA, k=R['k'],
                symmetry=R['mode'], exempt_kind=R['kind'], start=0, end_exclusive=total, total_intervals=total,
                required_units=c['minimum_units'], budget_units=c['budget_units'], surplus=R['k'] * c['minimum_units'] - c['budget_units'],
                failed_intervals=sorted(failed), missing_intervals=len(missing), first_missing=missing[:10], problems=problems,
                certificate_sha256=csha, restriction_sha256=rsha, checker_sha256=sha, merged_from=names)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('certificate'); ap.add_argument('--output', required=True)
    ap.add_argument('--start', type=int, default=0); ap.add_argument('--count', type=int, default=None)
    ap.add_argument('--audit', action='store_true', help='both engines and a direct enumeration of the deficient cells (slow)')
    ap.add_argument('--engine', choices=['fast', 'reference'], default=None, help='default: fast, reference if the exempt set has a disc')
    ap.add_argument('--workers', type=int, default=1, help='forked worker processes for the rows of the range')
    ap.add_argument('--restriction', default=None, help='take the restriction object from this JSON file')
    ap.add_argument('--merge', nargs='+', default=None, metavar='SLICE.json', help='aggregate slice results instead of checking rows')
    args = ap.parse_args()
    c, csha, rsha = load(args.certificate, args.restriction)
    data, jobs, spans, margin, R = validate_restricted(c)
    if args.merge is not None:
        result = merge(c, csha, rsha, R, len(jobs), args.merge)
        Path(args.output).write_text(json.dumps(result, indent=1) + '\n'); print(json.dumps(result, indent=1))
        sys.exit({'PASS_RESTRICTED_EXACT_COVER': 0, 'RESTRICTED_EXACT_COVERAGE_FAILURE': 2}.get(result['status'], 3))
    lo = args.start; hi = len(jobs) if args.count is None else min(len(jobs), lo + args.count)
    need(0 <= lo < hi, 'row range'); need(args.workers >= 1, 'workers'); rows = []; start = time.monotonic()
    global _JOB
    _JOB = (data, jobs, spans, R, c['minimum_units'], args.audit, args.engine)
    pool = None
    if args.workers > 1:
        import multiprocessing as mp
        _warm()
        pool = mp.get_context('fork').Pool(args.workers)
        it = pool.imap(_work, range(lo, hi), chunksize=1)
    else:
        it = map(_work, range(lo, hi))
    for n, rec in enumerate(it):
        rows.append(rec)
        if n % 100 == 0:
            print(rec['interval'], rec['minimum_units'], rec['deficient_slabs'], rec['passed'], round(time.monotonic() - start, 1), flush=True)
    if pool is not None:
        pool.close(); pool.join()
    failed = [r for r in rows if not r['passed']]; complete = lo == 0 and hi == len(jobs)
    known = [r['deficient_cells'] for r in rows if r['deficient_cells'] is not None]
    status = ('RESTRICTED_EXACT_COVERAGE_FAILURE' if failed else
              'PASS_RESTRICTED_EXACT_COVER' if complete else 'PASS_RESTRICTED_INTERVAL_PARTITION_ONLY')
    result = dict(status=status, statement=statement(c, R) if complete and not failed else None, schema=SCHEMA,
                  k=R['k'], symmetry=R['mode'], exempt_kind=R['kind'], start=lo, end_exclusive=hi, total_intervals=len(jobs),
                  required_units=c['minimum_units'], budget_units=c['budget_units'], surplus=R['k'] * c['minimum_units'] - c['budget_units'],
                  unrestricted_minimum_units=min(r['minimum_units'] for r in rows),
                  deficient_cells=sum(known) if len(known) == len(rows) else None, deficient_slabs=sum(r['deficient_slabs'] for r in rows),
                  failed_intervals=[r['interval'] for r in failed], minimum_margin=str(margin),
                  certificate_sha256=csha, restriction_sha256=rsha, checker_sha256=checker_sha256(), workers=args.workers,
                  seconds=time.monotonic() - start, cpu_seconds_rows=round(sum(r['cpu_seconds'] for r in rows), 2), rows=rows)
    Path(args.output).write_text(json.dumps(result, indent=1) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('rows', 'checker_sha256')}, indent=1))
    sys.exit(2 if failed else 0)


if __name__ == '__main__':
    main()
