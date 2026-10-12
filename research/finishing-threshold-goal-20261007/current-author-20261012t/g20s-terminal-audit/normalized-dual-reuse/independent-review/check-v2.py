#!/usr/bin/env python3
"""Independent sparse weak-duality audit; accepted model kernel only, no solver.

Model construction is inherited from the exact source bound by the independently
accepted full gate. Residual arithmetic, initial box, simultaneous updates,
outward rounding, products, and chain validation are implemented here afresh.
"""
import copy
import hashlib
import importlib.abc
import itertools
import json
from pathlib import Path
import resource
import sys
import time
from fractions import Fraction as F

resource.setrlimit(resource.RLIMIT_CPU, (20, 22))
START = time.process_time()
HERE = Path(__file__).resolve().parent
PROD = HERE.parent / 'producer'
GATE = HERE.parents[1] / 'full-gate'
DIM = 100
CORE = tuple(i for i in range(51) if i not in (2, 6, 7, 21, 25, 37))
ANGLES = tuple(i for i in range(34, 51) if i != 37)
PRODUCTS = tuple(itertools.product((2, 21, 25), ANGLES))
OBJECTIVES = {(i, s) for i in CORE + (51,) for s in (-1, 1)}
GRID = 10**15
PAD = F(1, 10**12)

class NoDiscovery(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in ('numpy', 'scipy', 'sympy'):
            raise RuntimeError('Unpermitted discovery/symbolic import: ' + fullname)
sys.meta_path.insert(0, NoDiscovery())

def read(p):
    return json.loads(p.read_text())
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def strings(box):
    return [[str(x), str(y)] for x, y in box]
def expand(base):
    assert len(base) == 52
    result = list(base)
    for w, a in PRODUCTS:
        ends = [x*y for x in base[w] for y in base[a]]
        result.append((min(ends), max(ends)))
    assert len(result) == DIM
    return result
def initial():
    base = [(F(-1), F(1)) for _ in range(52)]
    for i in (6, 7, 37):
        base[i] = (F(0), F(0))
    base[51] = (F(-1), F(0))
    base[2] = (F(0), F(8, 25) + PAD)
    base[21] = (-F(1, 20) - PAD, F(1, 5) + PAD)
    base[25] = (-F(1, 5) - PAD, F(3, 40) + PAD)
    return expand(base)
def next_box(bounds, results):
    lower = {i: F(rec['bound']) for rec in results for i in [rec['coordinate']] if rec['sign'] == 1}
    upper = {i: -F(rec['bound']) for rec in results for i in [rec['coordinate']] if rec['sign'] == -1}
    base = [(max(lo, lower.get(i, lo)), min(hi, upper.get(i, hi)))
            for i, (lo, hi) in enumerate(bounds[:52])]
    assert all(lo <= hi for lo, hi in base)
    # Fraction // is floor even for negative fractions; -((-x)//1) is ceil.
    rounded = [(F((lo*GRID)//1, GRID), F(-((-hi*GRID)//1), GRID)) for lo, hi in base]
    assert all(rl <= lo <= hi <= rh for (lo, hi), (rl, rh) in zip(base, rounded))
    return expand(rounded)
def extract_old(step):
    return {(rec['coordinate'], rec['sign']): dict(rec['weights']) for rec in step['results']}
def check_roster(results):
    keys = [(x['coordinate'], x['sign']) for x in results]
    assert len(keys) == len(set(keys)) == 92 and set(keys) == OBJECTIVES
def bound(sparse, bounds, obj, weights):
    assert obj in OBJECTIVES and len(bounds) == DIM
    sums = {}
    rhs = F(0)
    for key, value in weights.items():
        assert str(int(key)) == key
        k, q = int(key), F(value)
        assert 0 <= k < len(sparse) and q >= 0
        coeff, const = sparse[k]
        rhs += q * const
        for j, a in coeff.items():
            sums[j] = sums.get(j, F(0)) + q*a
    i, s = obj
    residual = {j: (F(s) if j == i else F(0)) - sums.get(j, F(0))
                for j in set(sums) | {i}}
    residual = {j: x for j, x in residual.items() if x}
    # min residual.x over the incoming box, independent of other objectives.
    pieces = {j: min(x*bounds[j][0], x*bounds[j][1]) for j, x in residual.items()}
    floor = sum(pieces.values(), F(0))
    return rhs + floor, rhs, floor, residual
def verify_record(sparse, bounds, rec, detail):
    value, rhs, floor, residual = bound(sparse, bounds, (rec['coordinate'], rec['sign']), rec['weights'])
    assert value == F(rec['bound']) == F(detail['bound'])
    assert rhs == F(detail['weighted_rhs'])
    assert floor == F(detail['residual_box_floor'])
    assert residual == {int(j): F(x) for j, x in detail['residual'].items()}
    return value, rhs, floor, residual

manifest = read(PROD / 'PRODUCER_MANIFEST.json')
producer_manifest_sha = sha(PROD / 'PRODUCER_MANIFEST.json')
if len(sys.argv) > 1:
    assert producer_manifest_sha == sys.argv[1]
for name, digest in manifest['files_sha256'].items():
    assert sha(PROD / name) == digest
prep = read(PROD / 'preparation.json')
for rec in prep['sources']:
    p = PROD / rec['relative_path']
    assert sha(p) == rec['sha256']
    assert p.read_bytes() == (GATE / 'producer' / rec['relative_path']).read_bytes()
for name, digest in prep['inputs'].items():
    assert sha(PROD / 'inputs' / name) == digest
assert sha(GATE / 'independent-review/MANIFEST.json') == 'a70b064bb81a55fca7f5ad9a9b19ea765c613877d8b243e041081760b9dc53dd'
accepted = read(PROD / 'inputs/accepted-old-terminal-manifest.json')
assert sha(PROD / 'inputs/old-uniform-rigidity.json') == accepted['rigidity_certificate_sha256']
old = read(PROD / 'inputs/old-uniform-rigidity.json')
gate = read(PROD / 'inputs/full-gate-receipt.json')
state = read(PROD / 'reuse-receipt.json')
candidate = read(PROD / 'reuse-candidate.json')
assert len(old['steps']) == len(candidate['steps']) == len(state['rounds']) == 5
assert state['status'] == 'OLD_WEIGHTS_INCONCLUSIVE_NO_STRICT_CONTRACTION'
assert state['candidate_sha256'] == sha(PROD / 'reuse-candidate.json')
assert F(candidate['epsilon']) == F(state['epsilon']) == F(1, 5000)

# Only inherited code below is the accepted model/interval geometry kernel.
sys.path.insert(0, str(PROD / 'instance/research/uniform-capture-20261007'))
import rigidity as kernel
import root_geometry
import bridge
root = [bridge.I(*v) for v in read(PROD / 'inputs/accepted-root-gate.json')['root']['intervals']]
data = root_geometry.geometry(*root)
labels = gate['new_labels']
assert len(labels) == len(set(labels)) == 52
bounds = initial()
assert strings(bounds) == state['initial_bounds']
out = {'status': 'RUNNING', 'producer_manifest_sha256': producer_manifest_sha, 'rounds': []}
stale_old_bounds = 0
for number, (old_step, step, stated) in enumerate(zip(old['steps'], candidate['steps'], state['rounds']), 1):
    detail_path = PROD / f'round-{number:02d}-residuals.json'
    details = read(detail_path)
    assert sha(detail_path) == stated['residual_receipt_sha256']
    assert details['step'] == number and details['bounds_before'] == strings(bounds)
    rows = kernel.model(bounds, F(1, 5000), data, labels)
    assert len(rows) == 244 and all(len(row['a']) == DIM for row in rows)
    assert [row['label'] for row in rows[:52]] == labels
    digest = hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()
    assert digest == step['model_sha256'] == details['model_sha256'] == stated['model_sha256']
    if number == 1:
        assert digest == gate['normalized_model_kernel_digest']
    sparse = [({j: F(a) for j, a in enumerate(row['a']) if F(a)}, F(row['b'])) for row in rows]
    check_roster(old_step['results']); check_roster(step['results']); check_roster(details['results'])
    old_weights = extract_old(old_step)
    old_values = {(rec['coordinate'], rec['sign']): F(rec['bound']) for rec in old_step['results']}
    detail_map = {(rec['coordinate'], rec['sign']): rec for rec in details['results']}
    diagnostic = []
    for rec in step['results']:
        obj = (rec['coordinate'], rec['sign'])
        assert rec['weights'] == old_weights[obj]
        value, rhs, floor, residual = verify_record(sparse, bounds, rec, detail_map[obj])
        stale_old_bounds += value != old_values[obj]
        if obj[0] in (8, 14, 15, 41, 44, 49):
            diagnostic.append({'coordinate': obj[0], 'sign': obj[1], 'bound': str(value),
                               'weighted_rhs': str(rhs), 'residual_floor': str(floor),
                               'deficit_below_minus_one': str(-1-value),
                               'nonzero_residual_coordinates': sorted(residual)})
    next_bounds = next_box(bounds, step['results'])
    assert strings(next_bounds) == details['bounds_after']
    ratio = max(abs(v) for i in CORE for v in next_bounds[i])
    assert ratio == F(details['ratio']) == F(stated['ratio']) == 1
    worst = [{'coordinate': i, 'bounds': strings([next_bounds[i]])[0]}
             for i in CORE if max(map(abs, next_bounds[i])) == ratio]
    assert worst == stated['worst_coordinates']
    out['rounds'].append({'round': number, 'model_sha256': digest, 'objectives': 92,
                         'ratio': str(ratio), 'worst': worst, 'diagnostics': diagnostic})
    bounds = next_bounds
assert candidate['final_bounds'] == strings(bounds)
assert [x['coordinate'] for x in out['rounds'][-1]['worst']] == [8, 14, 15, 41, 44, 49]
assert bounds[8][1] == 1 and bounds[41] == (-1, 1)
assert all(bounds[i][0] == -1 for i in (14, 15, 44, 49))

controls = []
def reject(name, fn):
    try:
        fn()
    except (AssertionError, ValueError):
        controls.append({'name': name, 'status': 'REJECTED'})
    else:
        raise AssertionError('Control accepted: ' + name)
rec = copy.deepcopy(candidate['steps'][-1]['results'][0])
detail = detail_map[(rec['coordinate'], rec['sign'])]
# Bounds here are now AFTER last round; use the saved correct incoming box.
incoming = [tuple(map(F, v)) for v in details['bounds_before']]
bad = copy.deepcopy(rec); bad['bound'] = str(F(bad['bound']) + F(1, 10**12))
reject('corrupted claimed bound', lambda: verify_record(sparse, incoming, bad, detail))
bad = copy.deepcopy(rec); bad['weights']['0'] = '-1'
reject('negative weight', lambda: bound(sparse, incoming, (bad['coordinate'], bad['sign']), bad['weights']))
reject('missing objective', lambda: check_roster(step['results'][:-1]))
bad_detail = copy.deepcopy(detail); bad_detail['residual']['99'] = str(F(bad_detail['residual'].get('99', '0')) + 1)
reject('corrupted signed residual', lambda: verify_record(sparse, incoming, rec, bad_detail))
poisoned = copy.deepcopy(old['steps'][0])
poisoned['model_sha256'] = 'not consulted'
for item in poisoned['results']:
    item['bound'] = 'not consulted'
assert extract_old(poisoned) == extract_old(old['steps'][0])
controls.append({'name': 'poisoned old claimed bounds and model digest', 'status': 'IRRELEVANT_TO_EXTRACTED_WEIGHTS'})
assert stale_old_bounds > 0
assert not any(x in sys.modules for x in ('numpy', 'scipy', 'sympy'))
out.update(status='ACCEPTED_FIVE_ROUND_OLD_WEIGHT_REUSE_INCONCLUSIVE',
           objectives_verified=460, rounds_verified=5, rows_per_fresh_model=244,
           inherited_model_kernel='Source-equal accepted full-gate kernel; rebuilt at all five current boxes.',
           independent=['weak duality', 'all signed residuals', 'initial box', 'simultaneous updates',
                        'outward rounding', '48 product intervals', 'chain/final bounds'],
           changed_from_old_claimed_bounds=stale_old_bounds, controls=controls,
           conclusion='These five old-weight rounds do not prove strict contraction. No claim about fresh weights or later rounds.',
           solver_or_full_rigidity_checker_called=False, cpu_seconds=time.process_time()-START)
(HERE / 'receipt.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({k: out[k] for k in ('status', 'objectives_verified', 'changed_from_old_claimed_bounds', 'cpu_seconds')}))
