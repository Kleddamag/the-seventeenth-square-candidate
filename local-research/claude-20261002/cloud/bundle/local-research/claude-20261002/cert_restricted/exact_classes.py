"""Exact checker for CLASS certificates (schema s17-classes-v1, cloud/analysis/CLASS_FORMAT.md).

Input: a charge certificate in the published shape (no restriction object) and a class file:
pose classes C_1..C_r with rational thresholds t_c >= 0 and a rational bound b.  With
  tau(p) = min { t_c : p in C_c },  tau(p) = 1 if p lies in no class,
the statement checked is: for every family of closed unit squares with pairwise disjoint
interiors inside the square container of side S = L/A (frame of the file),
  sum over the squares of tau(pose)  <  b.
A class is the union of its slots (closed convex polygon of centres x closed tan-half-angle
interval, all quarter-turn lifts), united with their images under the symmetry of the file:
  "fixed"   : nothing added     (fixed-image charge, rows on the whole range u in [0, 1]),
  "mirror_x": the mirror x -> 2 c_x - x  (fixed-image charge whose invariance under the mirror is
              verified on the feature list, rows on the folded range as for "orbit"),
  "orbit"   : all eight D4 images       (D4-symmetric charge, rows on the folded range).

Checked, all exactly (Python integers / Fractions; int64 only inside the sweep tree, under the
published 2^50 bound):
  1. structure, capacities and budget of the certificate (as exact_restricted.py),
  2. budget_units * q_b < p_b * minimum_units for b = p_b / q_b,
  3. for every row and every checked cell of the published arrangement:
       charge * q >= p * minimum_units,   p / q = R(cell),
     R(cell) = the largest threshold among the classes with t_c > 1 that the closed cell x closed
     row interval MEETS in one of their slot images; if there is none, the least threshold among
     the classes with t_c < 1 that contain the whole closed cell x closed row interval in ONE slot
     image; if there is none, 1.

The rectangles, the sweep geometry and the tree arithmetic are those of exact_general.py /
integer_sweep.py (unchanged); the integer edge forms, the "all four corners inside" and the
"rectangle meets polygon" index intervals are those of exact_restricted.py (imported, unchanged).

    python exact_classes.py CERT.json --classes CLASSES.json --output OUT.json [--start i] [--count n] [--workers w]
    python exact_classes.py CERT.json --classes CLASSES.json --output ALL.json --merge OUT1.json OUT2.json ...

Exit code 0 = no row of the range failed, 2 = some row failed, 3 = merge incomplete; a refused
certificate or class file ends with a ValueError (exit code 1).
"""
if not __debug__:
    raise SystemExit("Run without -O/-OO and unset PYTHONOPTIMIZE.")
import exact_restricted as xr            # first: it sets the thread limits before numpy is loaded
from exact_restricted import need, D4, SlabExemption, slab_minima, _first_below, _merge, _intersect, _complement
from fractions import Fraction as F
from pathlib import Path
from bisect import bisect_left, bisect_right
import sys, json, time, hashlib, re
import numpy as np
from numba import njit
from integer_sweep import add, query, trig
from exact_general import expand, geometry
from boolean_rule import expansion

SCHEMA = 's17-classes-v1'
HERE = Path(__file__).resolve().parent
SOURCES = ('exact_classes.py', 'exact_restricted.py', 'exact_general.py', 'integer_sweep.py', 'boolean_rule.py')
MAX_CLASSES = 256
MAX_SLOTS = 4096
PASS, PARTIAL = 'PASS_CLASSES_EXACT_COVER', 'PASS_CLASSES_INTERVAL_PARTITION_ONLY'
FAILURE, INCOMPLETE = 'CLASSES_EXACT_COVERAGE_FAILURE', 'MERGE_INCOMPLETE'
BIG = 2 ** 59                      # above every charge (charges are below 2^50 in absolute value)


# ----------------------------------------------------------------- strict JSON and numbers
class JsonFloat:
    """A float token of the JSON text.  It is never a number for this checker."""
    def __init__(self, text):
        self.text = text


def _pairs(pairs):
    out = {}
    for k, v in pairs:
        need(k not in out, 'JSON: duplicate key ' + repr(k))
        out[k] = v
    return out


def _constant(text):
    raise ValueError('JSON: %s is not allowed' % text)


def strict_json(raw):
    """JSON with integers as Python integers, float tokens as JsonFloat objects (refused wherever a
    number is expected), duplicate keys and NaN / Infinity refused."""
    try:
        return json.loads(raw.decode('utf-8'), parse_float=JsonFloat, parse_constant=_constant, object_pairs_hook=_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as e:
        raise ValueError('JSON: ' + str(e))


def has_float(v):
    if type(v) is JsonFloat:
        return True
    if type(v) is list:
        return any(has_float(x) for x in v)
    if type(v) is dict:
        return any(has_float(x) for x in v.values())
    return False


_RAT = re.compile(r'(-?[0-9]+)(?:/([0-9]+))?')
_NAME = re.compile(r'[A-Za-z0-9_.+-]{1,64}')


def srat(x, what):
    """A rational written as a string "p" or "p/q" (ASCII digits, q > 0).  Nothing else."""
    need(type(x) is str, what + ': rational expected as a string "p" or "p/q"')
    m = _RAT.fullmatch(x)
    need(m is not None, what + ': not a rational "p" or "p/q"')
    q = 1 if m.group(2) is None else int(m.group(2))
    need(q > 0, what + ': zero denominator')
    return F(int(m.group(1)), q)


def crat(x, what):
    """A rational of the certificate: a JSON integer or a string "p" / "p/q"."""
    if type(x) is int:
        return F(x)
    return srat(x, what)


def exact_keys(obj, required, optional, what):
    need(type(obj) is dict, what + ': object expected')
    need(set(required) <= set(obj) and set(obj) <= set(required) | set(optional), what + ': unknown or missing keys ' + repr(sorted(obj)))


# ----------------------------------------------------------------- the class file
def _point(p, what):
    need(type(p) is list and len(p) == 2, what + ': point [x, y] expected')
    return (srat(p[0], what), srat(p[1], what))


def _polygon(raw, what):
    """Closed convex polygon: 3..64 vertices, counter-clockwise, strictly convex, none repeated."""
    need(type(raw) is list and 3 <= len(raw) <= 64, what + ': polygon needs 3..64 vertices')
    v = [_point(p, what) for p in raw]
    n = len(v)
    need(len(set(v)) == n, what + ': repeated polygon vertex')
    for i in range(n):
        (x0, y0), (x1, y1), (x2, y2) = v[i], v[(i + 1) % n], v[(i + 2) % n]
        need((x1 - x0) * (y2 - y1) - (y1 - y0) * (x2 - x1) > 0, what + ': polygon not strictly convex counter-clockwise')
        for (x, y) in v:
            need((x1 - x0) * (y - y0) - (y1 - y0) * (x - x0) >= 0, what + ': polygon not convex')
    return v


def parse_classes(o):
    """Strict reading of a class file.  Returns dict(symmetry, centre, bound, classes) with
    classes = [dict(name, threshold, kind, slots=[(vertices, (lo, hi)), ...])]; kind is the sign
    of threshold - 1."""
    need(type(o) is dict, 'class file: JSON object expected')
    need(not has_float(o), 'class file: float number tokens are not allowed anywhere in the file')
    exact_keys(o, ('schema', 'symmetry', 'frame', 'bound', 'classes'), ('comment',), 'class file')
    need(type(o['schema']) is str and o['schema'] == SCHEMA, 'class file: schema must be ' + SCHEMA)
    need(type(o['symmetry']) is str and o['symmetry'] in ('fixed', 'mirror_x', 'orbit'), "class file: symmetry must be 'fixed', 'mirror_x' or 'orbit'")
    exact_keys(o['frame'], ('unit', 'center'), (), 'class file: frame')
    need(type(o['frame']['unit']) is str and o['frame']['unit'] == 'unit_square', "class file: frame.unit must be 'unit_square'")
    centre = _point(o['frame']['center'], 'class file: frame.center')
    bound = srat(o['bound'], 'class file: bound')
    need(bound > 0, 'class file: bound must be positive')
    raw = o['classes']
    need(type(raw) is list and 1 <= len(raw) <= MAX_CLASSES, 'class file: classes must be a list of 1..%d classes' % MAX_CLASSES)
    classes = []; names = set()
    for ci, c in enumerate(raw):
        what = 'classes[%d]' % ci
        exact_keys(c, ('name', 'threshold', 'slots'), (), what)
        need(type(c['name']) is str and _NAME.fullmatch(c['name']) is not None, what + ': name must be 1..64 characters of A-Z a-z 0-9 _ . + -')
        need(c['name'] not in names, what + ': name used twice'); names.add(c['name'])
        t = srat(c['threshold'], what + '.threshold')
        need(t >= 0, what + ': threshold must be >= 0')
        need(type(c['slots']) is list and 1 <= len(c['slots']) <= MAX_SLOTS, what + ': slots must be a list of 1..%d slots' % MAX_SLOTS)
        slots = []
        for si, s in enumerate(c['slots']):
            w = '%s.slots[%d]' % (what, si)
            exact_keys(s, ('centre', 'angle_tan_half'), ('label',), w)
            exact_keys(s['centre'], ('polygon',), (), w + '.centre')
            verts = _polygon(s['centre']['polygon'], w + '.polygon')
            g = s['angle_tan_half']
            need(type(g) is list and len(g) == 2, w + ': angle_tan_half [lo, hi] expected')
            lo, hi = srat(g[0], w + '.angle_tan_half'), srat(g[1], w + '.angle_tan_half')
            need(-1 < lo <= hi < 1, w + ': angle_tan_half needs -1 < lo <= hi < 1')
            slots.append((verts, (lo, hi)))
        classes.append(dict(name=c['name'], threshold=t, kind=(t > 1) - (t < 1), slots=slots))
    return dict(symmetry=o['symmetry'], centre=centre, bound=bound, classes=classes)


# ----------------------------------------------------------------- the certificate
def _fixed_charge(c, LD):
    """Fixed-image shape (RESTRICTED_CHECKER.md 1.4): sites and features image by image.  The
    checks are those of exact_restricted.validate_fixed."""
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
        xr.keys(f, ('sites', 'weight'), ('threshold', 'coefficients', 'winning_masks'))
        idx = f['sites']; w = f['weight']
        need(type(w) is int and w >= 0, 'invalid feature weight')
        need(type(idx) is list and 1 <= len(idx) <= 20 and all(type(i) is int and 0 <= i < len(sites) for i in idx)
             and len(set(idx)) == len(idx), 'invalid feature sites')
        n = len(idx)
        coeff = f.get('coefficients', [1] * n)
        need(type(coeff) is list and len(coeff) == n and all(type(v) is int and v > 0 for v in coeff)
             and coeff == sorted(coeff, reverse=True), 'invalid site coefficients')
        coeff = tuple(coeff)
        rules = f.get('winning_masks', [])
        need(type(rules) is list, 'winning_masks')
        if rules:
            need(n <= 12 and all(type(v) is int and 0 < v < 2 ** n for v in rules) and len(set(rules)) == len(rules)
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
    return sites, triggers, tw


def check_mirror(sites, triggers, tw, LD):
    """symmetry 'mirror_x': the charge must be invariant under the mirror x -> L - x of the
    container, verified on the feature list itself.  A feature image is identified by its rule and
    its sites (threshold rule: threshold and the multiset of (coefficient, site); mask rule: the
    set of masks and the sites in their order); repeated features add their weights.  Required:
    the mirror image of every site of every feature (also of weight 0) is a site, and the total
    weight listed for the mirror image of a feature equals the total weight listed for the feature.
    A mirror image written in a form that is not recognised is a refusal."""
    index = {p: i for i, p in enumerate(sites)}

    def ident(idx, k, coeff, rules):
        if rules:
            return ('masks', tuple(sorted(rules)), tuple(idx))
        return ('threshold', k, tuple(sorted(zip(coeff, idx), key=lambda z: (-z[0], z[1]))))
    total = {}
    for (idx, k, coeff, rules), w in zip(triggers, tw):
        key = ident(idx, k, coeff, rules)
        total[key] = total.get(key, 0) + w
    for n, (idx, k, coeff, rules) in enumerate(triggers):
        image = [index.get((LD - sites[i][0], sites[i][1])) for i in idx]
        need(all(j is not None for j in image), 'mirror_x: the mirror image of a site of feature %d is not a site' % n)
        need(total.get(ident(image, k, coeff, rules)) == total[ident(idx, k, coeff, rules)],
             'mirror_x: the mirror image of feature %d is not listed with the same weight, coefficients and masks' % n)


def _strict_symmetric(c):
    """Shape checks before exact_general.expand, which takes several things for granted."""
    po = c['point_orbits']; to = c['threshold_orbits']
    need(type(po) is list and all(type(r) is list and len(r) == 3 for r in po), 'point_orbits: rows [x, y, w] expected')
    need(type(to) is list, 'threshold_orbits: list expected')
    for e in to:
        need(type(e) is dict and {'sets', 'weight'} <= set(e) <= {'sets', 'weight', 'threshold', 'coefficients', 'winning_masks'},
             'threshold orbit: unknown or missing keys')
        need(type(e['sets']) is list and len(e['sets']) >= 1 and all(type(s) is list and 1 <= len(s) <= 20 for s in e['sets']), 'threshold orbit: sets')
        need('coefficients' not in e or type(e['coefficients']) is list, 'threshold orbit: coefficients')
        need('winning_masks' not in e or (type(e['winning_masks']) is list and len(e['winning_masks']) >= 1), 'threshold orbit: winning_masks must be a non-empty list')


def validate_classes(c, CL):
    """Whole-file validation.  Returns (data, jobs, spans, minimum margin); data is what
    exact_general.geometry takes.  CL (from parse_classes) receives A and the list of images."""
    need(type(c) is dict, 'certificate must be a JSON object')
    need('restriction' not in c, 'the certificate carries a restriction object; a class check needs a certificate without one')
    for key in ('L', 'A', 'normalized_target', 'coordinate_denominator', 'weight_denominator', 'budget_units', 'minimum_units', 'entries'):
        need(key in c, 'certificate: key %s is missing' % key)
    for key in ('L', 'A', 'normalized_target'):
        crat(c[key], key)
    L, A = xr._head(c)
    D = c['coordinate_denominator']
    need(type(D) is int and D > 0 and (L * D).denominator == 1, 'invalid coordinate scale'); LD = int(L * D)
    mode = CL['symmetry']
    if mode == 'orbit':
        need('sites' not in c and 'features' not in c, "symmetry 'orbit' needs the symmetric shape (no sites / features)")
        need('point_orbits' in c and 'threshold_orbits' in c, "symmetry 'orbit' needs point_orbits and threshold_orbits")
        _strict_symmetric(c)
        data = expand(c)
    else:
        need('point_orbits' not in c and 'threshold_orbits' not in c, "symmetry '%s' needs the fixed-image shape (no point_orbits / threshold_orbits)" % mode)
        need('sites' in c and 'features' in c, "symmetry '%s' needs top-level sites and features" % mode)
        sites, triggers, tw = _fixed_charge(c, LD)
        if mode == 'mirror_x':
            check_mirror(sites, triggers, tw, LD)
        data = (sites, [0] * len(sites), triggers, tw, D)
    need(c['budget_units'] > 0, 'budget_units must be positive (no feature of positive weight)')
    b = CL['bound']
    need(c['budget_units'] * b.denominator < b.numerator * c['minimum_units'], 'budget inequality budget_units * q_b < p_b * minimum_units fails')
    rows = c['entries']
    need(type(rows) is list and len(rows) >= 1, 'entries')
    full = mode == 'fixed'                 # rows up to u = 1; otherwise the folded range of the symmetric shape
    jobs = []; margins = []; spans = []; cursor = F(0)
    for i, row in enumerate(rows):
        need(type(row) is list and len(row) == 4, 'row')
        a, b_, t, B = (crat(x, 'entries[%d]' % i) for x in row)
        need(a == cursor and 0 <= a < b_ and (b_ <= 1 if full else b_ < 1) and 0 <= t < 1 and 0 < B < A, 'catalogue coverage')
        cc, ss = trig(t); f = []; g = []
        for u in (a, b_):
            c0, s0 = trig(u); dot = cc * c0 + ss * s0; cross = abs(cc * s0 - ss * c0)
            need(dot > 0 and dot >= cross, 'angle range'); f.append(c0 + s0); g.append(dot + cross)
        margin = A - B * max(g); need(margin > 0, 'core not strict'); margins.append(margin); r = A * min(f) / 2
        need(B * (cc + ss) / 2 <= r < L / 2, 'parent envelope'); jobs.append((t, B, L / 2 - r)); spans.append((a, b_)); cursor = b_
    if full:
        need(cursor == 1, 'angle gap: rows of a fixed-image certificate must end exactly at u = 1')
    else:
        need(cursor * cursor + 2 * cursor > 1, 'angle gap: the rows must reach beyond tan(pi/8)')
    CL['A'] = A; CL['S'] = L / A
    CL['images'] = {'fixed': D4[:1], 'mirror_x': (D4[0], D4[5]), 'orbit': D4}[mode]
    need(D4[5] == ((-1, 0), (0, 1)), 'mirror matrix')
    cls = CL['classes']
    # the order in which the classes claim the cells: above 1 by decreasing threshold, then below 1
    # by increasing threshold; equal thresholds in file order
    CL['order'] = (sorted((i for i, k in enumerate(cls) if k['kind'] > 0), key=lambda i: (-cls[i]['threshold'], i))
                   + sorted((i for i, k in enumerate(cls) if k['kind'] < 0), key=lambda i: (cls[i]['threshold'], i)))
    CL['levels'] = [k['threshold'] for k in cls] + [F(1)]          # one level per class, then the default level
    return data, jobs, spans, min(margins)


def load(cert_path, class_path):
    raw = Path(cert_path).read_bytes(); craw = Path(class_path).read_bytes()
    try:
        c = strict_json(raw)
        CL = parse_classes(strict_json(craw))
        data, jobs, spans, margin = validate_classes(c, CL)
    except (TypeError, KeyError, IndexError, AttributeError) as e:      # malformed input that a test above did not name
        raise ValueError('malformed input (%s: %s)' % (type(e).__name__, e))
    return c, CL, data, jobs, spans, margin, hashlib.sha256(raw).hexdigest(), hashlib.sha256(craw).hexdigest()


# ----------------------------------------------------------------- one row
def angles_meet(I, J):
    """The closed interval I has a point in common with J + m*pi/2 for some integer m.  All
    numbers are tan(angle/2) of angles in (-pi, pi), where tan(x/2) is increasing.  I lies in
    [-1, 1] (angles in [-pi/2, pi/2]) and J in (-1, 1), so only m in {-1, 0, 1} can succeed."""
    lo, hi = J
    need(-1 < lo <= hi < 1 and -1 <= I[0] <= I[1] <= 1, 'angle chart')
    lifts = ((lo, hi), ((1 + lo) / (1 - lo), (1 + hi) / (1 - hi)), ((lo - 1) / (lo + 1), (hi - 1) / (hi + 1)))
    return any(l2 <= I[1] and I[0] <= h2 for l2, h2 in lifts)


class ClassRow(SlabExemption):
    """The slot images of every class that can matter in one row (angle interval [a, b]), in the
    integer sweep coordinates of the row.  The forms, boxes and the two index-interval routines are
    inherited unchanged from exact_restricted: _slot_interval = y-cells whose closed rectangle lies
    in the polygon, _blocked_interval = y-cells whose closed rectangle meets the polygon."""

    def __init__(self, CL, meta, a, b):
        C, S, RR, scale = meta['C'], meta['S'], meta['R'], meta['scale']
        need(C * C + S * S == RR * RR and RR > 0 and scale > 0, 'rotation')
        self.xe = meta['xe']; self.ye = meta['ye']; self.nv = len(self.ye) - 1
        K = CL['A'] * scale * RR * RR
        cx, cy = CL['centre']
        self.regs = [[] for _ in CL['classes']]
        for M in CL['images']:
            N = ((M[0][0] * C + M[0][1] * S, -M[0][0] * S + M[0][1] * C),
                 (M[1][0] * C + M[1][1] * S, -M[1][0] * S + M[1][1] * C))
            det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
            need(N[0][0] * N[1][1] - N[0][1] * N[1][0] == det * RR * RR and det in (1, -1), 'similarity')
            I = (a, b) if det == 1 else (-b, -a)
            for ci, cl in enumerate(CL['classes']):
                for verts, gate in cl['slots']:
                    if cl['kind'] < 0 and self._angles_inside(I, gate):
                        self.regs[ci].append(('polygon', self._forms(verts, N, K, cx, cy), self._box(verts, N, CL['A'] * scale, cx, cy)))
                    elif cl['kind'] > 0 and angles_meet(I, gate):
                        box, den, pts = self._box(verts, N, CL['A'] * scale, cx, cy)
                        self.regs[ci].append((box, den, None, pts))
        self.active = any(self.regs)

    def slabs_of(self, reg, high):
        """A range of slab indices that contains every slab the region can touch (generous by one
        slab on each side; the interval routines decide exactly)."""
        (umin, umax, _, _), den = (reg[0], reg[1]) if high else (reg[2][0], reg[2][1])
        k0 = bisect_left(self.xe, -((-umin) // den)) - 2
        k1 = bisect_right(self.xe, umax // den) + 1
        return max(0, k0), min(len(self.xe) - 1, k1)

    def interval(self, reg, high, u0, u1):
        return self._blocked_interval(reg, u0, u1) if high else self._slot_interval(reg, u0, u1)


@njit
def accumulate_levels(nv, evindex, atomindex, sign, ylo, yhi, weights, first, last, flag, ptr, ivlo, ivhi, ivlevel, needs):
    """The published sweep in which every checked slab is queried completely: a slab with flag 0 as
    one range of the last level (the default level), a slab with flag 1 as the listed ranges
    ivlo[i]..ivhi[i]-1, ptr[k] <= i < ptr[k+1] (a partition of [first, last) in increasing order),
    each with its level ivlevel[i].  Returns per level the number of cells and the least value, the
    least minimum among the ranges that are below the need of their level, and the first cell in
    sweep order below the need of its level: slab, y-cell, level, value (or -1)."""
    n = 1
    while n < nv:
        n *= 2
    mn = np.zeros(2 * n, np.int64); lazy = np.zeros(2 * n, np.int64)
    nl = len(needs)
    cnt = np.zeros(nl, np.int64); low = np.full(nl, 2 ** 60, np.int64)
    p = 0; deficit = np.int64(2 ** 60)
    wk = np.int64(-1); wj = np.int64(-1); wl = np.int64(-1); wz = np.int64(0)
    for k in range(len(first)):
        while p < len(evindex) and evindex[p] == k:
            j = atomindex[p]; w = sign[p] * weights[j]
            add(mn, lazy, 1, 0, n, ylo[j], yhi[j], w)
            p += 1
        if first[k] >= 0:
            if flag[k] == 0:
                i0 = 0; i1 = 1
            else:
                i0 = ptr[k]; i1 = ptr[k + 1]
            for i in range(i0, i1):
                if flag[k] == 0:
                    lo = first[k]; hi = last[k]; lev = nl - 1
                else:
                    lo = ivlo[i]; hi = ivhi[i]; lev = ivlevel[i]
                z = query(mn, lazy, 1, 0, n, lo, hi)
                cnt[lev] += hi - lo
                if z < low[lev]:
                    low[lev] = z
                if z < needs[lev]:
                    if z < deficit:
                        deficit = z
                    if wk < 0:
                        wk = k; wl = lev
                        wj = _first_below(mn, lazy, 1, 0, n, lo, hi, np.int64(0), needs[lev])
                        wz = query(mn, lazy, 1, 0, n, wj, wj + 1)
    return cnt, low, deficit, wk, wj, wl, wz


def check_row(data, job, span, CL, minimum):
    """One row.  'passed' is True only if every checked cell has charge * q >= p * minimum for its
    required threshold p/q (rule 3 of the module text)."""
    a, b = span
    arrays, meta = geometry(*data, *job, meta=True)
    first, last = arrays[7], arrays[8]
    z, cells, zs = slab_minima(*arrays)
    z = int(z); cells = int(cells)
    cls = CL['classes']; nc = len(cls); levels = CL['levels']
    rec = dict(minimum_units=z, cells=cells, deficient_slabs=int(np.count_nonzero((first >= 0) & (zs < min(minimum, BIG)))))
    nslab = len(first)
    flag = np.zeros(nslab, np.int64); count = np.zeros(nslab + 1, np.int64); lo = []; hi = []; lev = []
    tester = ClassRow(CL, meta, a, b)
    if tester.active:
        touch = {}                                  # slab -> {class -> regions that may touch it}
        for ci in CL['order']:
            high = cls[ci]['kind'] > 0
            for reg in tester.regs[ci]:
                k0, k1 = tester.slabs_of(reg, high)
                for k in range(k0, k1):
                    if first[k] >= 0:
                        touch.setdefault(k, {}).setdefault(ci, []).append(reg)
        xe = meta['xe']
        for k in sorted(touch):
            f0, l0 = int(first[k]), int(last[k]); u0, u1 = xe[k], xe[k + 1]
            need(u0 < u1 and f0 < l0, 'degenerate slab')
            remaining = [(f0, l0)]; pieces = []
            for ci in CL['order']:
                if ci not in touch[k] or not remaining:
                    continue
                high = cls[ci]['kind'] > 0
                found = [iv for iv in (tester.interval(reg, high, u0, u1) for reg in touch[k][ci]) if iv is not None]
                X = _intersect(_merge(found), [(f0, l0)])
                if not X:
                    continue
                pieces += [(j0, j1, ci) for j0, j1 in _intersect(remaining, X)]
                remaining = _intersect(remaining, _complement(X, f0, l0))
            if not pieces:
                continue                            # the whole slab is of the default level
            pieces += [(j0, j1, nc) for j0, j1 in remaining]
            pieces.sort()
            need(pieces[0][0] == f0 and pieces[-1][1] == l0 and all(x[1] == y[0] for x, y in zip(pieces, pieces[1:]))
                 and all(x[0] < x[1] for x in pieces), 'the pieces do not partition the slab')
            flag[k] = 1; count[k + 1] = len(pieces)
            for j0, j1, level in pieces:
                lo.append(j0); hi.append(j1); lev.append(level)
    ptr = np.cumsum(count)
    needs = [min(BIG, -((-t.numerator * minimum) // t.denominator)) for t in levels]        # ceil(t * minimum)
    if not lo and z >= needs[nc]:
        # no slab is divided and the least charge of the row meets the default threshold: every
        # checked cell is of the default level and the first sweep has decided the row
        cnt = [0] * nc + [cells]; low = [2 ** 60] * nc + [z]; deficit = 2 ** 60; wk = wj = wl = -1; wz = 0
    else:
        cnt, low, deficit, wk, wj, wl, wz = accumulate_levels(*arrays, flag, ptr, np.array(lo, np.int64), np.array(hi, np.int64),
                                                              np.array(lev, np.int64), np.array(needs, np.int64))
        cnt = [int(x) for x in cnt]; low = [int(x) for x in low]; wk = int(wk); wj = int(wj); wl = int(wl); wz = int(wz); deficit = int(deficit)
    need(sum(cnt) == cells and min(low) == z, 'level sweep disagrees with the published sweep')
    # the decision, in exact rationals, from the least charge of every level
    failing = [i for i, t in enumerate(levels) if cnt[i] and low[i] * t.denominator < t.numerator * minimum]
    need(bool(failing) == (wk >= 0) and (not failing or (wl in failing and wj >= 0 and deficit == min(low[i] for i in failing))), 'witness inconsistent')
    part = lambda i: dict(cells=cnt[i], minimum_units=low[i] if cnt[i] else None)
    rec.update(passed=not failing, deficit_minimum_units=deficit if failing else None, default=part(nc),
               classes=[dict(name=k['name'], **part(i)) for i, k in enumerate(cls)], witness=None)
    if failing:
        t = levels[wl]
        need(wz * t.denominator < t.numerator * minimum, 'witness charge')
        xe, ye = meta['xe'], meta['ye']
        K = CL['A'] * meta['scale'] * meta['R'] ** 2; C, S = meta['C'], meta['S']; cx, cy = CL['centre']
        rec['witness'] = {'slab': wk, 'cell': wj, 'charge': wz, 'required_threshold': str(t), 'class': cls[wl]['name'] if wl < nc else None,
                          'frame_corners': [[str(cx + (C * u - S * v) / K), str(cy + (S * u + C * v) / K)]
                                            for u, v in ((xe[wk], ye[wj]), (xe[wk + 1], ye[wj]), (xe[wk + 1], ye[wj + 1]), (xe[wk], ye[wj + 1]))]}
    return rec


# ----------------------------------------------------------------- results
def statement(CL):
    which = {'orbit': 'the listed slots united with their eight D4 images',
             'mirror_x': 'the listed slots united with their images under the mirror x -> 2 c_x - x',
             'fixed': 'the listed slots exactly as written'}[CL['symmetry']]
    return ('For every family of closed unit squares with pairwise disjoint interiors inside a square of side %s, '
            'read in the frame with the container centre at (%s, %s), the sum of tau(pose) over the squares is less than %s, '
            'where tau(pose) is the least threshold among the classes that contain the pose and 1 if no class contains it. '
            'A class is %s (angle gates with all quarter-turn lifts). Classes: %s.'
            % (CL['S'], CL['centre'][0], CL['centre'][1], CL['bound'], which,
               '; '.join('%s threshold %s (%d slots)' % (k['name'], k['threshold'], len(k['slots'])) for k in CL['classes'])))


def checker_sha256():
    return {n: hashlib.sha256((HERE / n).read_bytes()).hexdigest() for n in SOURCES}


def header(c, CL, total, csha, clsha):
    return dict(implementation='python exact_classes.py', schema=SCHEMA, symmetry=CL['symmetry'], bound=str(CL['bound']),
                classes=[dict(name=k['name'], threshold=str(k['threshold']), slots=len(k['slots'])) for k in CL['classes']],
                total_intervals=total, required_units=str(c['minimum_units']), budget_units=str(c['budget_units']),
                surplus=str(CL['bound'] * c['minimum_units'] - c['budget_units']),
                certificate_sha256=csha, classes_sha256=clsha, checker_sha256=checker_sha256())


def totals(CL, rows):
    """Cells decided by each class and the least charge among them, over a list of row records."""
    def join(parts):
        mins = [p['minimum_units'] for p in parts if p['minimum_units'] is not None]
        return dict(cells=sum(p['cells'] for p in parts), minimum_units=min(mins) if mins else None)
    deficits = [r['deficit_minimum_units'] for r in rows if r['deficit_minimum_units'] is not None]
    return dict(unrestricted_minimum_units=min(r['minimum_units'] for r in rows) if rows else None,
                deficit_minimum_units=min(deficits) if deficits else None,
                cells_default=join([r['default'] for r in rows]),
                cells_by_class=[dict(name=k['name'], **join([r['classes'][i] for r in rows])) for i, k in enumerate(CL['classes'])])


def _row_ok(CL, r):
    def part(p):
        return (type(p) is dict and type(p.get('cells')) is int and p['cells'] >= 0
                and (p.get('minimum_units') is None or type(p['minimum_units']) is int))
    return (type(r) is dict and type(r.get('interval')) is int and type(r.get('passed')) is bool
            and type(r.get('minimum_units')) is int and type(r.get('cells')) is int
            and (r.get('deficit_minimum_units') is None or type(r['deficit_minimum_units']) is int)
            and r['passed'] == (r.get('deficit_minimum_units') is None) and r['passed'] == (r.get('witness') is None)
            and part(r.get('default')) and type(r.get('classes')) is list and len(r['classes']) == len(CL['classes'])
            and all(part(p) and p.get('name') == k['name'] for p, k in zip(r['classes'], CL['classes']))
            and r['default']['cells'] + sum(p['cells'] for p in r['classes']) == r['cells'])


def merge(c, CL, total, csha, clsha, paths):
    """Aggregates slice results of THIS checker.  The complete statement is given only if every
    row 0..total-1 is present, every record of it passed, and all slices are for this certificate,
    this class file and these checker sources."""
    head = header(c, CL, total, csha, clsha); problems = []; kept = {}; failed = set()
    same = ('passed', 'minimum_units', 'cells', 'deficient_slabs', 'deficit_minimum_units', 'default', 'classes')
    for path in paths:
        try:
            d = json.loads(Path(path).read_text())
        except (OSError, ValueError):
            problems.append('%s: unreadable' % path); continue
        if type(d) is not dict:
            problems.append('%s: not a slice' % path); continue
        bad = [key for key in head if d.get(key) != head[key]]
        if bad:
            problems.append('%s: differs in %s' % (path, ', '.join(bad))); continue
        rows = d.get('rows'); s = d.get('start'); e = d.get('end_exclusive')
        if type(rows) is not list or type(s) is not int or type(e) is not int or not (0 <= s and e <= total) or len(rows) != e - s:
            problems.append('%s: malformed slice' % path); continue
        if not all(_row_ok(CL, r) and r['interval'] == s + n for n, r in enumerate(rows)):
            problems.append('%s: malformed rows' % path); continue
        bad_rows = [r['interval'] for r in rows if not r['passed']]
        st = d.get('status')
        if st not in (PASS, PARTIAL, FAILURE) or (st == FAILURE) != bool(bad_rows) or d.get('failed_intervals') != bad_rows:
            problems.append('%s: status and row flags are inconsistent' % path); continue
        for r in rows:
            i = r['interval']
            if not r['passed']:
                failed.add(i)
            if i not in kept:
                kept[i] = r
            elif any(kept[i].get(key) != r.get(key) for key in same):
                problems.append('%s: row %d differs from the same row in an earlier slice' % (path, i))
    missing = [i for i in range(total) if i not in kept]
    status = FAILURE if failed else INCOMPLETE if problems or missing else PASS
    out = dict(status=status, statement=statement(CL) if status == PASS else None)
    out.update(head)
    out.update(start=0, end_exclusive=total, merged_files=len(paths), problems=problems, missing_intervals=len(missing),
               first_missing_intervals=missing[:20], failed_intervals=sorted(failed))
    out.update(totals(CL, [kept[i] for i in sorted(kept)]))
    return out


# ----------------------------------------------------------------- command line
_JOB = None


def _work(i):
    data, jobs, spans, CL, minimum = _JOB
    t0 = time.process_time()
    rec = check_row(data, jobs[i], spans[i], CL, minimum)
    out = dict(interval=i); out.update(rec); out['cpu_seconds'] = round(time.process_time() - t0, 4)
    return out


def _warm():
    """Compile every numba routine in this process (before a pool is forked)."""
    ev = np.array([[0, 0, 1], [1, 0, -1]], np.int64)      # column slices are strided, as in geometry()
    one = np.ones(1, np.int64); zero = np.zeros(1, np.int64)
    arrays = (1, ev[:, 0], ev[:, 1], ev[:, 2], zero, one, np.array([5], np.int64), np.array([0, 0], np.int64), np.array([1, 1], np.int64))
    need(int(slab_minima(*arrays)[0]) == 0, 'warm-up sweep')
    r = accumulate_levels(*arrays, np.array([1, 0], np.int64), np.array([0, 1, 1], np.int64), np.array([0], np.int64), np.array([1], np.int64),
                          np.array([0], np.int64), np.array([5, 1], np.int64))
    need([int(x) for x in r[0]] == [1, 1] and [int(x) for x in r[1]] == [5, 0] and int(r[2]) == 0
         and (int(r[3]), int(r[4]), int(r[5]), int(r[6])) == (1, 0, 1, 0), 'warm-up level sweep')


def main(argv=None):
    import argparse

    class Parser(argparse.ArgumentParser):
        def error(self, message):             # argparse would exit with code 2, which means "a row failed" here
            raise ValueError('command line: ' + message)
    ap = Parser()
    ap.add_argument('certificate'); ap.add_argument('--output', required=True)
    ap.add_argument('--classes', required=True, help='the class file (schema s17-classes-v1)')
    ap.add_argument('--start', type=int, default=0); ap.add_argument('--count', type=int, default=None)
    ap.add_argument('--workers', type=int, default=1, help='forked worker processes for the rows of the range')
    ap.add_argument('--merge', nargs='+', default=None, metavar='SLICE.json', help='aggregate slice results instead of checking rows')
    args = ap.parse_args(argv)
    c, CL, data, jobs, spans, margin, csha, clsha = load(args.certificate, args.classes)
    total = len(jobs)
    if args.merge is not None:
        result = merge(c, CL, total, csha, clsha, args.merge)
        Path(args.output).write_text(json.dumps(result, indent=1) + '\n'); print(json.dumps(result, indent=1))
        return {PASS: 0, FAILURE: 2}.get(result['status'], 3)
    lo = args.start; hi = total if args.count is None else min(total, lo + args.count)
    need(0 <= lo < hi, 'row range'); need(args.workers >= 1, 'workers'); rows = []; start = time.monotonic()
    global _JOB
    _JOB = (data, jobs, spans, CL, c['minimum_units'])
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
        if n % 100 == 0 or not rec['passed']:
            print(rec['interval'], rec['minimum_units'], rec['deficient_slabs'], rec['passed'], round(time.monotonic() - start, 1), flush=True)
    if pool is not None:
        pool.close(); pool.join()
    failed = [r['interval'] for r in rows if not r['passed']]; complete = lo == 0 and hi == total
    status = FAILURE if failed else PASS if complete else PARTIAL
    result = dict(status=status, statement=statement(CL) if status == PASS else None)
    result.update(header(c, CL, total, csha, clsha))
    result.update(start=lo, end_exclusive=hi, failed_intervals=failed)
    result.update(totals(CL, rows))
    result.update(minimum_margin=str(margin), workers=args.workers, seconds=time.monotonic() - start,
                  cpu_seconds_rows=round(sum(r['cpu_seconds'] for r in rows), 2), rows=rows)
    Path(args.output).write_text(json.dumps(result, indent=1) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('rows', 'checker_sha256')}, indent=1))
    return 2 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
