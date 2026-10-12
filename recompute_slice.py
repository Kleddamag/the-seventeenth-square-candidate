#!/usr/bin/env python3
"""recompute_slice.py : recomputes rows START..END-1 of ONE capture statement with both exact checkers and
compares the result with each other and with the stored slices.

    python3 recompute_slice.py STATEMENT START END [--workers N] [--python EXE] [--node EXE] [--out DIR]

STATEMENT is the identifier of one of the 98 capture statements, for example Q_4; its folder in this edition is
    research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/statements/STATEMENT/
The script uses certificate.json and classes.json of that folder and the checker sources under
    research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/checker_sources/src/
and runs

    PYTHON -B .../src/exact_classes.py CERT --classes CLASSES --start START --count END-START --workers N --output OUT/py.json
    NODE   .../src/node/verify_classes_wb.js CERT --classes CLASSES --start START --count END-START --workers N --output OUT/node.json

one after the other, each in a fresh process, Python without -O and with PYTHONOPTIMIZE unset.  Then it compares
  (1) the Python rows with the Node.js rows, on the fields passed, minimum_units, cells, deficient_slabs,
      deficit_minimum_units, default, classes and, where a row has one, the witness (slab, cell, charge);
  (2) the Python rows with the stored Python rows of the same numbers (slices/*/py.json), and the Node.js rows with
      the stored Node.js rows (slices/*/node.json), on every field but the timing fields;
  (3) the SHA-256 of the certificate, the class file and the checker files with the values the stored slices name.
Needs: Python with numpy and numba for the Python checker (the stored records name the versions that were used;
give the interpreter with --python), and Node.js.  The script itself uses the standard library only.  It writes
only into OUT (default: _check_out/slice-<time>/ in the edition root) and changes no file of the edition.

One row takes about 2 CPU-seconds in the Python checker and less in Node.js; a stored slice has 1,500 rows.
A recomputed slice is not a recomputed statement: a statement is all rows 0..N-1 without gap or overlap, merged by
each checker's own --merge, with a strict integer surplus.
Last line: SLICE RESULT: EQUAL ... or SLICE RESULT: DIFFER ...   Exit code 0 only for EQUAL.
"""
import argparse, glob, hashlib, json, os, shutil, subprocess, sys, time
ROOT = os.path.dirname(os.path.realpath(__file__))
CAP = os.path.join(ROOT, *'research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/'.rstrip('/').split('/'))
CR = os.path.join(CAP, 'checker_sources', 'src')
NODE_JS = os.path.join(CR, 'node', 'verify_classes_wb.js')
PY_FILES = ('exact_classes.py', 'exact_restricted.py', 'exact_general.py', 'integer_sweep.py', 'boolean_rule.py')
ROW = ('passed', 'minimum_units', 'cells', 'deficient_slabs', 'deficit_minimum_units', 'default', 'classes')
WITNESS = ('slab', 'cell', 'charge')
T_ROW = {'cpu_seconds', 'seconds'}


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 22), b''):
            h.update(block)
    return h.hexdigest()


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser(description='Recompute one slice of one capture statement with both exact checkers.')
    ap.add_argument('statement'); ap.add_argument('start', type=int); ap.add_argument('end', type=int)
    ap.add_argument('--workers', type=int, default=1, help='processes per checker (default 1)')
    ap.add_argument('--python', default=sys.executable, help='a Python interpreter that has numpy and numba')
    ap.add_argument('--node', default=shutil.which('node') or 'node', help='the Node.js executable')
    ap.add_argument('--out', help='output folder (default: _check_out/slice-<time>/)')
    a = ap.parse_args()
    exact = os.path.join(CAP, 'statements', a.statement)
    cert, classes = os.path.join(exact, 'certificate.json'), os.path.join(exact, 'classes.json')
    for f in (cert, classes, NODE_JS) + tuple(os.path.join(CR, x) for x in PY_FILES):
        if not os.path.isfile(f):
            print('SLICE RESULT: DIFFER (missing file: %s)' % f); return 2
    if not 0 <= a.start < a.end:
        print('SLICE RESULT: DIFFER (need 0 <= START < END)'); return 2
    out = a.out or os.path.join(ROOT, '_check_out', 'slice-' + time.strftime('%Y%m%dT%H%M%S'))
    os.makedirs(out, exist_ok=True)
    for f in ('py.json', 'node.json'):
        if os.path.exists(os.path.join(out, f)):
            print('SLICE RESULT: DIFFER (%s already exists in %s; give a fresh --out)' % (f, out)); return 2
    hashes = {'certificate': sha(cert), 'classes': sha(classes), 'python': {x: sha(os.path.join(CR, x)) for x in PY_FILES}, 'node': sha(NODE_JS)}
    print('certificate sha256 %s\nclass file  sha256 %s' % (hashes['certificate'], hashes['classes']))
    env = dict(os.environ); env.pop('PYTHONOPTIMIZE', None); env['PYTHONDONTWRITEBYTECODE'] = '1'
    n = str(a.end - a.start)
    cmds = (('python', [a.python, '-B', os.path.join(CR, 'exact_classes.py'), cert, '--classes', classes, '--start', str(a.start), '--count', n,
                        '--workers', str(a.workers), '--output', os.path.join(out, 'py.json')], 'py'),
            ('node', [a.node, NODE_JS, cert, '--classes', classes, '--start', str(a.start), '--count', n,
                      '--workers', str(a.workers), '--output', os.path.join(out, 'node.json')], 'node'))
    rc = {}
    for name, cmd, short in cmds:
        t = time.time()
        with open(os.path.join(out, short + '.log'), 'w') as log:
            try:
                rc[name] = subprocess.run(cmd, cwd=out, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
            except OSError as e:
                print('SLICE RESULT: DIFFER (%s could not be started: %s)' % (name, e)); return 2
        print('%s checker: exit %d, %.0f s; log %s' % (name, rc[name], time.time() - t, os.path.join(out, short + '.log')))
        if not os.path.isfile(os.path.join(out, short + '.json')):
            print('SLICE RESULT: DIFFER (the %s checker wrote no output; read its log)' % name); return 2
    py, nd = load(os.path.join(out, 'py.json')), load(os.path.join(out, 'node.json'))
    bad = []
    want = list(range(a.start, a.end))
    prow, nrow = {r['interval']: r for r in py['rows']}, {r['interval']: r for r in nd['rows']}
    if sorted(prow) != want or sorted(nrow) != want:
        bad.append('the outputs do not hold exactly the rows %d..%d' % (a.start, a.end - 1))
    # (1) Python against Node.js
    d1 = 0
    for i in want:
        p, q = prow.get(i, {}), nrow.get(i, {})
        same = all(p.get(k) == q.get(k) for k in ROW)
        if (p.get('witness') is None) != (q.get('witness') is None):
            same = False
        elif p.get('witness') is not None:
            same &= all(p['witness'].get(k) == q['witness'].get(k) for k in WITNESS)
        if not same:
            d1 += 1
            if d1 == 1: bad.append('row %d: Python and Node.js differ' % i)
    failed = [i for i in want if not prow.get(i, {}).get('passed') or not nrow.get(i, {}).get('passed')]
    if failed:
        bad.append('%d row(s) do not pass, first %d' % (len(failed), failed[0]))
    if rc['python'] != 0 or rc['node'] != 0:
        bad.append('exit codes: python %d, node %d' % (rc['python'], rc['node']))
    # (2) against the stored slices
    stored = {'py': {}, 'node': {}}; shead = {'py': [], 'node': []}
    for kind in ('py', 'node'):
        files = sorted(glob.glob(os.path.join(exact, 'slices', '*', '%s.json' % kind)))
        for f in files:
            d = load(f)
            if d.get('end_exclusive', 0) <= a.start or d.get('start', 0) >= a.end:
                continue
            shead[kind].append(d)
            for r in d['rows']:
                if a.start <= r['interval'] < a.end:
                    stored[kind][r['interval']] = r
    d2 = {}
    for kind, mine in (('py', prow), ('node', nrow)):
        d2[kind] = 0
        if sorted(stored[kind]) != want:
            bad.append('the stored %s slices do not hold all rows %d..%d' % (kind, a.start, a.end - 1)); continue
        for i in want:
            x = {k: v for k, v in mine.get(i, {}).items() if k not in T_ROW}; y = {k: v for k, v in stored[kind][i].items() if k not in T_ROW}
            if x != y:
                d2[kind] += 1
                if d2[kind] == 1:
                    k = [k for k in sorted(set(x) | set(y)) if x.get(k, 'ABSENT') != y.get(k, 'ABSENT')][0]
                    bad.append('%s row %d field %s: recomputed %s | stored %s' % (kind, i, k, str(x.get(k, 'ABSENT'))[:100], str(y.get(k, 'ABSENT'))[:100]))
    # (3) the hashes the stored slices name
    notes = []
    for kind, new in (('py', py), ('node', nd)):
        for d in shead[kind]:
            if d.get('certificate_sha256') != hashes['certificate']: bad.append('stored %s slice names another certificate' % kind)
            if d.get('classes_sha256') != hashes['classes']: bad.append('stored %s slice names another class file' % kind)
            if d.get('checker_sha256') != new.get('checker_sha256'):
                (notes if kind == 'node' else bad).append('stored %s slice was made with other checker bytes: %s' % (kind, json.dumps(d.get('checker_sha256'))[:160]))
    if py.get('checker_sha256') != hashes['python']:
        bad.append('the Python output names other checker hashes than the files on disk have')
    json.dump({'statement': a.statement, 'rows': [a.start, a.end], 'hashes': hashes, 'python_exit': rc['python'], 'node_exit': rc['node'],
               'rows_differing_python_node': d1, 'rows_differing_from_stored': d2, 'notes': sorted(set(notes)), 'differences': bad},
              open(os.path.join(out, 'compare.json'), 'w'), indent=1)
    for x in sorted(set(notes)): print('note: ' + x)
    for x in bad: print('difference: ' + x)
    if bad:
        print('SLICE RESULT: DIFFER (%d difference(s); outputs in %s)' % (len(bad), out)); return 1
    print('SLICE RESULT: EQUAL (rows %d..%d of %s: both checkers pass every row, agree with each other and with the stored rows; outputs in %s)'
          % (a.start, a.end - 1, a.statement, out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
