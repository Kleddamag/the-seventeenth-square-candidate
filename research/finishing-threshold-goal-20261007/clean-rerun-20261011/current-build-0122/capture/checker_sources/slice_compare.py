"""slice_compare.py: the output comparator of one slice (standard library only; decides nothing about the charge).

    python -B slice_compare.py PY_JSON NODE_JSON START END CERT_SHA256 CLASSES_SHA256 PY_EXIT PY_REFUSED NODE_EXIT NODE_STATE OUT_JSON

PY_JSON / NODE_JSON   the unmodified outputs of exact_classes.py and of the Node class checker for rows START..END-1
PY_EXIT / NODE_EXIT   exit codes of the two checker processes (an integer; anything else counts as "no exit code")
PY_REFUSED            yes | no    the Python checker ended by refusing the input (no output)
NODE_STATE            RUN | REFUSED | INCOMPLETE    RUN = the Node checker wrote an output
Writes OUT_JSON (atomically) and prints  "<python> <node> <agree>".
  python, node   PASS        the output exists, is for this certificate and this class file (sha256) and exactly these
                             rows, every row record is well formed and passed, and the exit code is 0
                 FAIL        a row failed (output complete, exit code 2) or the checker refused the input
                 INCOMPLETE  anything else
  agree          yes = both outputs cover the range and agree, per row, on passed, minimum_units, cells,
                 deficient_slabs, deficit_minimum_units, default and classes and on the witness (slab, cell, charge),
                 and in the header on schema, symmetry, bound, classes, total_intervals, required_units, budget_units,
                 surplus, certificate_sha256, classes_sha256 (values and JSON types);  no = a difference;
                 n/a = one of the two outputs is missing or unusable, nothing was compared
Exit code: 0 = python PASS, node PASS, agree yes;  2 = a FAIL or agree no;  3 = anything else.
OUT_JSON names the sha256 and size of the two output files it read, the range, the compared fields and the number of
differing rows.
"""
import sys, json, os, hashlib

PASS_STATES = ('PASS_CLASSES_INTERVAL_PARTITION_ONLY', 'PASS_CLASSES_EXACT_COVER')
FAIL_STATE = 'CLASSES_EXACT_COVERAGE_FAILURE'
HEADER = ('schema', 'symmetry', 'bound', 'classes', 'total_intervals', 'required_units', 'budget_units', 'surplus',
          'certificate_sha256', 'classes_sha256')
ROW = ('passed', 'minimum_units', 'cells', 'deficient_slabs', 'deficit_minimum_units', 'default', 'classes')
WITNESS = ('slab', 'cell', 'charge')


def part_ok(p):
    return (type(p) is dict and type(p.get('cells')) is int and p['cells'] >= 0
            and (p.get('minimum_units') is None or type(p['minimum_units']) is int))


def row_ok(r, names):
    """The shape both checkers' --merge ask of a row record."""
    return (type(r) is dict and type(r.get('passed')) is bool
            and type(r.get('minimum_units')) is int and type(r.get('cells')) is int
            and (r.get('deficit_minimum_units') is None or type(r['deficit_minimum_units']) is int)
            and r['passed'] == (r.get('deficit_minimum_units') is None) and r['passed'] == (r.get('witness') is None)
            and part_ok(r.get('default')) and type(r.get('classes')) is list and len(r['classes']) == len(names)
            and all(part_ok(p) and p.get('name') == n for p, n in zip(r['classes'], names))
            and r['default']['cells'] + sum(p['cells'] for p in r['classes']) == r['cells'])


def read_slice(path, lo, hi, sha, csha):
    """(state, rows by interval or None, header, note, file facts): state COMPLETE_PASS, COMPLETE_FAIL or INCOMPLETE."""
    try:
        raw = open(path, 'rb').read()
    except OSError as e:
        return 'INCOMPLETE', None, None, 'no readable output (%s)' % type(e).__name__, None
    facts = dict(sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
    try:
        d = json.loads(raw.decode('utf-8'))
    except Exception as e:
        return 'INCOMPLETE', None, None, 'no readable output (%s)' % type(e).__name__, facts
    if type(d) is not dict:
        return 'INCOMPLETE', None, None, 'output is not an object', facts
    rows = d.get('rows')
    if (type(rows) is not list or type(d.get('start')) is not int or type(d.get('end_exclusive')) is not int
            or d['start'] != lo or d['end_exclusive'] != hi):
        return 'INCOMPLETE', None, d, 'output is not for rows %d-%d' % (lo, hi), facts
    if len(rows) != hi - lo or not all(type(r) is dict and type(r.get('interval')) is int and r['interval'] == lo + i for i, r in enumerate(rows)):
        return 'INCOMPLETE', None, d, 'row records do not match the range', facts
    if d.get('certificate_sha256') != sha:
        return 'INCOMPLETE', None, d, 'output is for another certificate', facts
    if d.get('classes_sha256') != csha:
        return 'INCOMPLETE', None, d, 'output is for another class file', facts
    cls = d.get('classes')
    if type(cls) is not list or not all(type(k) is dict and type(k.get('name')) is str for k in cls):
        return 'INCOMPLETE', None, d, 'no class list in the header', facts
    names = [k['name'] for k in cls]
    if not all(row_ok(r, names) for r in rows):
        return 'INCOMPLETE', None, d, 'malformed row records', facts
    bad = [r['interval'] for r in rows if r['passed'] is not True]
    status = d.get('status'); failed = d.get('failed_intervals')
    if not bad and status in PASS_STATES and failed == []:
        return 'COMPLETE_PASS', {r['interval']: r for r in rows}, d, 'every row passes', facts
    if bad and status == FAIL_STATE and failed == bad:
        return 'COMPLETE_FAIL', {r['interval']: r for r in rows}, d, 'failed rows: %r' % bad[:20], facts
    return 'INCOMPLETE', None, d, 'status %r and row flags are inconsistent (rows not passing: %r)' % (status, bad[:20]), facts


def join(parts):
    mins = [p['minimum_units'] for p in parts if p['minimum_units'] is not None]
    return dict(cells=sum(p['cells'] for p in parts), minimum_units=min(mins) if mins else None)


def same(a, b):
    """Equal values of equal JSON types, at every depth."""
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return set(a) == set(b) and all(same(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def compare(pyf, nodef, lo, hi, sha, csha, py_rc, py_refused, node_rc, node_state_in, out):
    ps, prow, pd, pnote, pfacts = read_slice(pyf, lo, hi, sha, csha)
    if ps == 'COMPLETE_PASS' and py_rc == 0:
        PYS = 'PASS'
    elif ps == 'COMPLETE_FAIL' and py_rc == 2:
        PYS = 'FAIL'
    elif ps == 'INCOMPLETE' and prow is None and py_refused and not os.path.exists(pyf):
        PYS = 'FAIL'; pnote = 'the checker refused the input'
    else:
        PYS = 'INCOMPLETE'
        if ps != 'INCOMPLETE':
            pnote += '; exit code %r does not fit' % (py_rc,); prow = None
    nrow = None; nd = None; nfacts = None
    if node_state_in == 'RUN':
        ns, nrow, nd, nnote, nfacts = read_slice(nodef, lo, hi, sha, csha)
        if ns == 'COMPLETE_PASS' and node_rc == 0:
            NS = 'PASS'
        elif ns == 'COMPLETE_FAIL' and node_rc == 2:
            NS = 'FAIL'
        else:
            NS = 'INCOMPLETE'
            if ns != 'INCOMPLETE':
                nnote += '; exit code %r does not fit' % (node_rc,); nrow = None
    elif node_state_in == 'REFUSED':
        NS = 'FAIL'; nnote = 'the checker refused the input'
    else:
        NS = 'INCOMPLETE'; nnote = 'the Node checker did not deliver its rows'
    diffs = []; nd_count = 0; compared = 0; witnesses = 0
    if prow is not None and nrow is not None:
        for key in HEADER:
            if key not in pd or key not in nd or not same(pd[key], nd[key]):
                diffs.append(dict(header=key, python=pd.get(key), node=nd.get(key)))
        for i in range(lo, hi):
            p = prow[i]; n = nrow[i]; compared += 1
            bad = [k for k in ROW if k not in p or k not in n or not same(p[k], n[k])]
            pw = p.get('witness'); nw = n.get('witness')
            if pw is not None and nw is not None:
                witnesses += 1
                if type(pw) is not dict or type(nw) is not dict or any(k not in pw or k not in nw or not same(pw[k], nw[k]) for k in WITNESS):
                    bad.append('witness')
            elif pw is not None or nw is not None:
                bad.append('witness')
            if bad:
                nd_count += 1
                if len(diffs) < 40:
                    diffs.append(dict(interval=i, fields=bad, python={k: p.get(k) for k in bad}, node={k: n.get(k) for k in bad}))
        AGREE = 'no' if diffs else 'yes'
    else:
        AGREE = 'n/a'
    res = dict(rows=[lo, hi], certificate_sha256=sha, classes_sha256=csha,
               python_output_sha256=pfacts['sha256'] if pfacts else None, python_output_bytes=pfacts['bytes'] if pfacts else None,
               node_output_sha256=nfacts['sha256'] if nfacts else None, node_output_bytes=nfacts['bytes'] if nfacts else None,
               python=PYS, python_note=pnote, python_exit=py_rc,
               node=NS, node_note=nnote, node_exit=node_rc, agree=AGREE, rows_compared=compared, rows_differing=nd_count,
               header_fields_differing=len([d for d in diffs if 'header' in d]),
               rows_with_witness_compared=witnesses, compared_per_row=list(ROW) + ['witness: ' + ', '.join(WITNESS)],
               compared_in_header=list(HEADER), differences=diffs)
    for tag, rows_, d in (('python', prow, pd), ('node', nrow, nd)):
        if rows_ is None:
            continue
        rs = [rows_[i] for i in range(lo, hi)]
        res[tag + '_minimum_units_of_slice'] = min(r['minimum_units'] for r in rs)
        res[tag + '_cells_of_slice'] = sum(r['cells'] for r in rs)
        res[tag + '_cells_default'] = join([r['default'] for r in rs])
        res[tag + '_cells_by_class'] = [dict(name=k['name'], threshold=k.get('threshold'), **join([r['classes'][j] for r in rs]))
                                        for j, k in enumerate(d['classes'])]
        res[tag + '_checker_sha256'] = d.get('checker_sha256')
    tmp = out + '.tmp'
    with open(tmp, 'w') as f:
        f.write(json.dumps(res, indent=1) + '\n')
    os.replace(tmp, out)
    print(PYS, NS, AGREE)
    if PYS == 'PASS' and NS == 'PASS' and AGREE == 'yes':
        return 0
    if PYS == 'FAIL' or NS == 'FAIL' or AGREE == 'no':
        return 2
    return 3


def number(x):
    try:
        return int(x)
    except ValueError:
        return None


if __name__ == '__main__':
    a = sys.argv
    if len(a) != 12 or a[8] not in ('yes', 'no') or a[10] not in ('RUN', 'REFUSED', 'INCOMPLETE'):
        sys.stderr.write(__doc__); sys.exit(91)
    sys.exit(compare(a[1], a[2], int(a[3]), int(a[4]), a[5], a[6], number(a[7]), a[8] == 'yes', number(a[9]), a[10], a[11]))
