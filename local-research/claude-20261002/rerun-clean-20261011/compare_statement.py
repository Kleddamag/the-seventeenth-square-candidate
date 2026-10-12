#!/usr/bin/env python3
"""compare_statement.py: the old/new comparison of the merged statements, one fresh attempt per statement and call.

    python3 compare_statement.py RESULTS_DIR MERGED_DIR RECORDS_DIR --capture DIR --name-map FILE                 # FINAL GATE: all statements
    python3 compare_statement.py RESULTS_DIR MERGED_DIR RECORDS_DIR --capture DIR --name-map FILE --subset ID ... # a marked subset
    --capture DIR   REQUIRED: the capture directory whose SOURCE_MANIFEST.json, PLAN_MANIFEST.json and MERGE_MANIFEST.json
                    are the current ones (the directory merge_run.sh was run from)
    --hash-map FILE (default: HASH_MAP.tsv beside this file)

RESULTS_DIR   the slice attempts as collected: <any name>/{py.json,node.json,compare.json,provenance.json}
MERGED_DIR    output of capture/merge_run.sh: <ID>/m<n>/{receipt_python.json,receipt_node.json,merge_provenance.json}
Without --subset the statements treated are ALL statements of STATEMENTS.tsv, which must be exactly the statements of
the plan (the final gate).  With --subset only the IDs given are treated and the summary says so.

For each statement, in this order (any failure ends the statement with an explicit record of verdict INCOMPLETE):
  1. the merge that counts is taken (merge_select.py: lowest-numbered merge attempt with verdict PASS under the
     current manifests, receipts as recorded);
  2. a fresh comparison attempt directory RECORDS_DIR/<ID>/c<n> is made by one exclusive mkdir (first free number);
     nothing of an earlier attempt is read, changed or removed;
  3. every slice the merge record selects is found again in RESULTS_DIR by the content of its record (statement, slice
     id, attempt id, sha256 of provenance.json); its py.json, node.json and compare.json must have the sha256 and size
     the merge record names; the selected ranges must be the planned slices and cover the rows exactly once; the two
     output files are linked into c<n>/selected/ (symbolic links, nothing is copied);
  4. compare_rows.py is run on the stored reference execution (STATEMENTS.tsv, column input_folder) and c<n>/selected
     with --need-all, the hash map, the name map, the stored receipts and the receipts of the merge; it must end with
     return code 0 (identical) or 1 (different) and must have written its record in this attempt;
  5. the record is bound: it must name this statement, the hash map and name map of this call and compare_rows.py by
     sha256, list as new slice files exactly the selected files with the sha256 and size of the merge record (these
     are the digests of the bytes compare_rows.py parsed), as new receipts exactly the two receipts of the merge
     record, exactly the two implementations, the planned partition on the new side, and every planned row compared
     and identical for each implementation;
  6. c<n>/comparison_record.json is written atomically: the record of compare_rows.py plus a "bridge" object with
     the merge attempt and the sha256 of its record, the three manifests, every selected slice (ids, range, sha256 of
     its provenance.json, sha256 and size of py.json, node.json, compare.json), both receipts, and the sha256 of
     compare_statement.py, merge_select.py, compare_rows.py, strip_inputs.py, STATEMENTS.tsv, the hash map,
     REMOVED_KEYS.tsv and the name map.  Verdict IDENTICAL only if compare_rows.py returned 0, its record says
     IDENTICAL and step 5 holds; DIFFERENT if it returned 1 with a bound record; INCOMPLETE otherwise.
WHICH COMPARISON COUNTS for a statement: the lowest-numbered attempt c<n> with verdict IDENTICAL whose bridge names
the merge that counts (sha256 of its record) and the current tool and map digests.
The name map is REQUIRED when REMOVED_KEYS.tsv shows that class names were replaced in the inputs.
Each call writes its summary into a fresh directory RECORDS_DIR/_calls/k<n>/SUMMARY.tsv (exclusive mkdir).
Exit code 0 only if every statement treated ended IDENTICAL (final gate: all statements of the plan); 1 otherwise;
2 for bad arguments.  Reads only; writes only under RECORDS_DIR."""
import json, os, sys, subprocess, hashlib, re
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(HERE)
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)
from merge_select import counting_merge
IMPLS = ['node verify_classes.js', 'python exact_classes.py']


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def reserve(parent, letter):
    """A fresh directory parent/<letter><n>, made by an exclusive mkdir."""
    os.makedirs(parent, exist_ok=True)
    for n in range(1, 10000):
        d = os.path.join(parent, '%s%d' % (letter, n))
        try:
            os.mkdir(d); return '%s%d' % (letter, n), d
        except FileExistsError:
            continue
    raise SystemExit('no free attempt directory under ' + parent)


def atomic(path, text):
    tmp = path + '.tmp'
    with open(tmp, 'w') as f:
        f.write(text); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)


def main(argv):
    opt = {'--name-map': None, '--capture': None, '--hash-map': os.path.join(HERE, 'HASH_MAP.tsv')}
    pos = []; subset = None; i = 0
    while i < len(argv):
        a = argv[i]
        if a in opt:
            if i + 1 >= len(argv):
                print(__doc__); return 2
            opt[a] = argv[i + 1]; i += 2
        elif a == '--subset':
            subset = argv[i + 1:]; break
        elif a.startswith('--'):
            print(__doc__); return 2
        else:
            pos.append(a); i += 1
    if len(pos) != 3 or (subset is not None and not subset) or not opt['--capture']:
        print(__doc__); return 2
    RES, MER, REC = pos; nm = opt['--name-map']; HM = opt['--hash-map']; CAP = opt['--capture']
    renamed = any(int(x) > 0 for l in open(os.path.join(HERE, 'REMOVED_KEYS.tsv')) for x in re.findall(r'renamed=(\d+)', l))
    if renamed and not nm:
        print('REFUSED: the inputs carry replaced class names (REMOVED_KEYS.tsv); --name-map FILE is required'); return 2
    for f in [HM] + ([nm] if nm else []) + [os.path.join(CAP, x) for x in ('SOURCE_MANIFEST.json', 'PLAN_MANIFEST.json', 'MERGE_MANIFEST.json')]:
        if not os.path.isfile(f):
            print('REFUSED: no such file: %s' % f); return 2
    rows = [l.rstrip('\n').split('\t') for l in open(os.path.join(HERE, 'STATEMENTS.tsv'))]
    sts = [dict(zip(rows[0], r)) for r in rows[1:]]
    plan = {s['statement_id']: s for s in json.load(open(os.path.join(CAP, 'PLAN_MANIFEST.json')))['statements']}
    if subset is None:
        if sorted(s['id'] for s in sts) != sorted(plan) or len(sts) != len(plan):
            print('REFUSED: the statements of STATEMENTS.tsv are not exactly the statements of the plan'); return 2
        treat = [s['id'] for s in sts]
    else:
        unknown = [x for x in subset if x not in plan or x not in {s['id'] for s in sts}]
        if unknown or len(set(subset)) != len(subset):
            print('REFUSED: unknown or repeated statement: %s' % ' '.join(unknown)); return 2
        treat = list(subset)
    folder = {s['id']: s['input_folder'] for s in sts}
    recs = {}
    for name in sorted(os.listdir(RES)):
        p = os.path.join(RES, name, 'provenance.json')
        if os.path.isfile(p):
            try:
                raw = open(p, 'rb').read(); r = json.loads(raw.decode('utf-8'))
                key = (r.get('statement_id'), r.get('slice_id'), r.get('attempt_id'), hashlib.sha256(raw).hexdigest())
                recs.setdefault(key, []).append(os.path.join(RES, name))
            except (ValueError, UnicodeDecodeError, AttributeError):
                pass
    pins = dict(compare_statement=sha(os.path.abspath(__file__)), merge_select=sha(os.path.join(HERE, 'merge_select.py')), compare_rows=sha(os.path.join(HERE, 'compare_rows.py')),
                strip_inputs=sha(os.path.join(HERE, 'strip_inputs.py')), statements_table=sha(os.path.join(HERE, 'STATEMENTS.tsv')), hash_map=sha(HM),
                removed_keys_table=sha(os.path.join(HERE, 'REMOVED_KEYS.tsv')), name_map=sha(nm) if nm else None)
    manifests = dict(source_manifest_sha256=sha(os.path.join(CAP, 'SOURCE_MANIFEST.json')), plan_manifest_sha256=sha(os.path.join(CAP, 'PLAN_MANIFEST.json')),
                     merge_manifest_sha256=sha(os.path.join(CAP, 'MERGE_MANIFEST.json')))
    os.makedirs(REC, exist_ok=True)
    call_id, call_dir = reserve(os.path.join(REC, '_calls'), 'k')
    summary = [['statement', 'merge_attempt', 'comparison_attempt', 'verdict', 'rows_python', 'rows_node', 'mismatching_rows', 'reason', 'record']]
    for sid in treat:
        cm = counting_merge(MER, sid, CAP)
        cid, d = reserve(os.path.join(REC, sid), 'c')
        out = os.path.join(d, 'comparison_record.json')
        base = dict(schema='s17-neutral-comparison-record-v1', statement_id=sid, comparison_attempt_id=cid)

        def end(verdict, reason, extra=None, counts=('', '', '')):
            rec = dict(base); rec.update(extra or {}); rec['verdict'] = verdict; rec['reason'] = reason
            atomic(out, json.dumps(rec, indent=1) + '\n')
            summary.append([sid, cm['attempt_id'] if cm else '', cid, verdict, counts[0], counts[1], counts[2], reason, os.path.relpath(out, REC)])
            print(' '.join(str(x) for x in summary[-1][:8]))

        if cm is None:
            end('INCOMPLETE', 'no merge attempt of this statement counts (none with verdict PASS under the current manifests and with its receipts as recorded)'); continue
        m = cm['record']; total = plan[sid]['total_intervals']
        psl = sorted(plan[sid]['slices'], key=lambda s: s['start'])
        sel_ = m.get('selected_slices') if type(m.get('selected_slices')) is list else []
        if [(s.get('slice_id'), s.get('start'), s.get('end_exclusive')) for s in sel_] != [(s['slice_id'], s['start'], s['end_exclusive']) for s in psl]:
            end('INCOMPLETE', 'the merge record does not select exactly the planned slices in order'); continue
        sel = os.path.join(d, 'selected'); os.mkdir(sel)
        want = {}; bridge_slices = []; problem = None
        for s in sel_:
            cands = recs.get((sid, s['slice_id'], s['attempt_id'], s['provenance_sha256']), [])
            if len(cands) != 1:
                problem = 'slice %s attempt %s: %d directories in RESULTS_DIR hold the selected record' % (s['slice_id'], s['attempt_id'], len(cands)); break
            a = cands[0]; b = dict(slice_id=s['slice_id'], attempt_id=s['attempt_id'], start=s['start'], end_exclusive=s['end_exclusive'], provenance_sha256=s['provenance_sha256'])
            for role, fn, ext in (('python', 'py.json', 'py'), ('node', 'node.json', 'node'), ('compare', 'compare.json', 'compare')):
                src = os.path.abspath(os.path.join(a, fn)); o = s.get(role) if type(s.get(role)) is dict else {}
                if not os.path.isfile(src) or sha(src) != o.get('sha256') or os.path.getsize(src) != o.get('bytes'):
                    problem = 'slice %s: %s is not the file the merge record names' % (s['slice_id'], fn); break
                b[role] = dict(sha256=o['sha256'], bytes=o['bytes'])
                if role != 'compare':
                    name = '%s.%s.json' % (s['slice_id'], ext); os.symlink(src, os.path.join(sel, name)); want[name] = (o['sha256'], o['bytes'])
            if problem:
                break
            bridge_slices.append(b)
        if problem:
            end('INCOMPLETE', problem); continue
        ex = os.path.join(W, 'results', folder[sid], 'exact'); child = os.path.join(d, 'compare_rows_record.json'); txt = os.path.join(d, 'compare_rows.txt')
        cmd = [sys.executable, '-B', os.path.join(HERE, 'compare_rows.py'), os.path.join(ex, 'slices'), sel, '--hash-map', HM, '--need-all',
               '--statement', sid, '--stored-receipts', ex, '--new-receipts', cm['dir'], '--record', child] + (['--name-map', nm] if nm else [])
        r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        open(txt, 'w').write(r.stdout)
        if r.returncode not in (0, 1) or not os.path.isfile(child):
            end('INCOMPLETE', 'compare_rows.py ended with return code %d%s' % (r.returncode, '' if os.path.isfile(child) else ' and wrote no record')); continue
        try:
            c = json.load(open(child))
        except ValueError:
            end('INCOMPLETE', 'the record of compare_rows.py is unreadable'); continue
        im = c.get('implementations') if type(c.get('implementations')) is dict else {}
        rc = c.get('receipts') if type(c.get('receipts')) is dict else {}
        tests = {
            'statement': c.get('statement_id') == sid,
            'hash map, name map and compare_rows.py by sha256': c.get('hash_map_sha256') == pins['hash_map'] and c.get('name_map_sha256') == pins['name_map']
            and (c.get('comparison_program') or {}).get('sha256') == pins['compare_rows'],
            'exactly the two implementations': sorted(im) == IMPLS,
            'new slice files = the selected files (sha256 and size of the parsed bytes)': all(
                {x['file']: (x['sha256'], x['bytes']) for x in v.get('new_slice_files', [])} == {k: w for k, w in want.items() if k.endswith(('.py.json' if i == 'python exact_classes.py' else '.node.json'))}
                for i, v in im.items()) and bool(im),
            'new partition = the planned slices': all(((v.get('partition') or {}).get('new') or {}).get('ranges') == [[s['start'], s['end_exclusive']] for s in psl] for v in im.values()) and bool(im),
            'stored partition covers the rows exactly once': all(((v.get('partition') or {}).get('stored') or {}).get('covers_all_rows_exactly_once') is True for v in im.values()) and bool(im),
            'every planned row compared for each implementation': all(v.get('rows_compared') == total and v.get('rows_new') == total for v in im.values()) and bool(im),
            'new receipts = the receipts of the merge record': all(
                type((rc.get(n) or {}).get('new')) is dict and rc[n]['new'].get('sha256') == m['outputs'][role]['sha256'] and rc[n]['new'].get('bytes') == m['outputs'][role]['bytes']
                for n, role in (('receipt_python.json', 'python'), ('receipt_node.json', 'node'))),
        }
        bound = all(tests.values())
        ident = (bound and r.returncode == 0 and c.get('verdict') == 'IDENTICAL' and c.get('problems') == []
                 and all(v.get('rows_identical') == total and v.get('rows_mismatching') == 0 and not v.get('header_fields_mismatching') for v in im.values()))
        if ident:
            verdict, reason = 'IDENTICAL', ''
        elif bound and r.returncode == 1 and c.get('verdict') == 'DIFFERENT':
            verdict, reason = 'DIFFERENT', '; '.join(str(p) for p in (c.get('problems') or [])[:3])[:300]
        else:
            verdict, reason = 'INCOMPLETE', 'record not bound or inconsistent: ' + ', '.join(k for k, v in tests.items() if not v)[:300]
        crv = c.pop('verdict', None); c['verdict_of_compare_rows'] = crv
        bridge = dict(merge_attempt_id=cm['attempt_id'], merge_provenance_sha256=cm['record_sha256'], manifests=manifests, selected_slices=bridge_slices,
                      receipts={role: dict(m['outputs'][role]) for role in ('python', 'node')}, source_sha256=pins, binding_tests=tests,
                      compare_rows_return_code=r.returncode, compare_rows_verdict=crv)
        end(verdict, reason, extra=dict(c, comparison_attempt_id=cid, bridge=bridge),
            counts=(str(im.get('python exact_classes.py', {}).get('rows_compared', '')), str(im.get('node verify_classes.js', {}).get('rows_compared', '')),
                    str(sum(x.get('rows_mismatching', 0) for x in im.values()))))
    good = sum(1 for l in summary[1:] if l[3] == 'IDENTICAL')
    scope = ('ALL %d statements of the plan (final gate)' % len(treat)) if subset is None else ('SUBSET of %d statements (not the final gate)' % len(treat))
    atomic(os.path.join(call_dir, 'SUMMARY.tsv'), '# scope: %s\n# identical: %d of %d\n' % (scope, good, len(treat)) + '\n'.join('\t'.join(l) for l in summary) + '\n')
    print('%s: scope %s; IDENTICAL %d of %d; summary %s' % (call_id, scope, good, len(treat), os.path.relpath(os.path.join(call_dir, 'SUMMARY.tsv'), REC)))
    return 0 if treat and good == len(treat) else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
