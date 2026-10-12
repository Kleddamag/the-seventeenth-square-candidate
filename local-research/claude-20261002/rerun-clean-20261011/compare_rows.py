#!/usr/bin/env python3
"""compare_rows.py: are the rows of a NEW execution (stripped inputs) identical to the rows of a STORED execution?

    python3 compare_rows.py STORED NEW [--hash-map HASH_MAP.tsv] [--json OUT.json] [--need-all]
                            [--name-map FILE] [--statement ID] [--stored-receipts DIR] [--new-receipts DIR] [--record OUT.json]

STORED and NEW are directories, searched recursively for slice outputs of the two checkers: every file whose name ends
in  py.json  or  node.json  (for example <k>.py.json, <k>.node.json, or <attempt>/py.json, <attempt>/node.json) and
that is an object with rows / start / end_exclusive.  Files are grouped by their "implementation" field; nothing is
taken from file names.  The slices of the two sides need not have the same boundaries.

For each implementation (python exact_classes.py, node verify_classes.js):
  rows     every row of NEW must exist in STORED and be identical in EVERY field except cpu_seconds (a time), with
           identical types (an integer is not a float, true is not 1) and identical key sets.
  header   every header field of every NEW slice must be identical to the STORED side, except
             certificate_sha256, classes_sha256   expected to differ; with --hash-map they must be exactly the pair
                                                  old -> new of HASH_MAP.tsv (the same pair in every slice)
             seconds, cpu_seconds_rows, verified_utc   times
             workers                                   a run setting, reported when it differs
           and the fields that depend on the slice boundaries (status, statement, start, end_exclusive, failed_intervals,
           unrestricted_minimum_units, deficit_minimum_units, cells_default, cells_by_class), which are compared
           directly when STORED has a slice with the same boundaries and are in every case recomputed here from the
           rows of each side over the rows of the NEW slice and compared.
  --need-all   final acceptance: also require that NEW covers every row 0 .. total_intervals-1, that every one of these
           rows was compared and is identical, that NEW and STORED each hold exactly the two implementations (python
           exact_classes.py and node verify_classes.js), and that on each side the slice files of each implementation
           cover the rows exactly once (no gap, no overlap, no second file for a range).
A file whose name ends in py.json or node.json and that is no well-formed slice output is a problem on either side;
it is never skipped.  The two sides may be cut into different slices: rows are matched by row number, both partitions
are written into the record, and a merged receipt's merged_files is not compared across the sides but must equal the
number of slice files of its own side.
  --name-map FILE   lines old_class_name<TAB>new_class_name ('#' lines ignored).  Only for a rerun whose class names were
           renamed by strip_inputs.py --rename-map: the names of the STORED side are replaced before comparing, in
           classes[].name (header and rows), cells_by_class[].name, witness.class and inside the statement sentence.
  --stored-receipts DIR, --new-receipts DIR   directories with receipt_python.json and receipt_node.json (the merged
           outputs): their sha256 are recorded and they are compared field by field (same exceptions as a header).
  --record OUT.json   the comparison record (schema s17-neutral-comparison-record-v1): sha256 of this program, of the hash
           map and of the name map, old and new receipt and slice-file sha256, the allowed metadata differences, the
           header and row field names tested, row counts and mismatch counts.  Only names relative to the given
           directories are written.
Exit code 0 = identical as described, 1 = a difference or nothing to compare, 2 = bad arguments or unreadable input.
Standard library only; reads the two directories, writes only OUT.json when asked.
"""
import json, os, sys, re, hashlib

ROW_SKIP = ('cpu_seconds',)
HASHES = ('certificate_sha256', 'classes_sha256')
TIMES = ('seconds', 'cpu_seconds_rows', 'verified_utc')
SETTING = ('workers',)
PARTITION_FIELDS = ('merged_files',)      # receipts only: how many slice files a side was cut into
RANGE = ('status', 'statement', 'start', 'end_exclusive', 'failed_intervals', 'unrestricted_minimum_units', 'deficit_minimum_units',
         'cells_default', 'cells_by_class')
PASS_STATES = ('PASS_CLASSES_INTERVAL_PARTITION_ONLY', 'PASS_CLASSES_EXACT_COVER')


def same(a, b):
    """Equality with exact types, recursively."""
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return set(a) == set(b) and all(same(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def rename(v, nm):
    """The class names of a stored output replaced by the name map (new objects; nothing else is touched)."""
    if not nm or type(v) is not dict:
        return v
    def nlist(l):
        return [dict(c, name=nm.get(c['name'], c['name'])) if type(c) is dict and type(c.get('name')) is str else c for c in l] if type(l) is list else l
    v = dict(v)
    for k in ('classes', 'cells_by_class'):
        if k in v:
            v[k] = nlist(v[k])
    if type(v.get('statement')) is str:
        v['statement'] = re.sub(r'(?<![A-Za-z0-9_.+-])(%s)(?![A-Za-z0-9_.+-])' % '|'.join(re.escape(o) for o in sorted(nm, key=len, reverse=True)),
                                lambda m: nm[m.group(1)], v['statement'])
    if type(v.get('rows')) is list:
        rows = []
        for r in v['rows']:
            if type(r) is dict:
                r = dict(r)
                if 'classes' in r:
                    r['classes'] = nlist(r['classes'])
                if type(r.get('witness')) is dict and r['witness'].get('class') in nm:
                    r['witness'] = dict(r['witness'], **{'class': nm[r['witness']['class']]})
            rows.append(r)
        v['rows'] = rows
    return v


def file_facts(p, root):
    if p in FACTS:
        return dict(FACTS[p])
    raw = open(p, 'rb').read()
    return dict(file=os.path.relpath(p, root), sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))


FACTS = {}        # path -> sha256 and size of the bytes that were parsed
IMPLS = ['node verify_classes.js', 'python exact_classes.py']


def find(root, nm, problems, tag):
    """Every file below root whose name ends in py.json or node.json MUST be a slice output of one of the two
    implementations: an object with integer start < end_exclusive and exactly the rows start .. end_exclusive-1 with
    integer row numbers.  Anything else is a problem (never skipped silently)."""
    out = []
    for d, _, files in os.walk(root, followlinks=True):
        for f in sorted(files):
            if f.endswith('py.json') or f.endswith('node.json'):
                p = os.path.join(d, f); rel = os.path.relpath(p, root)
                try:
                    raw = open(p, 'rb').read(); v = json.loads(raw.decode('utf-8'))
                except Exception as e:
                    problems.append('%s: %s is unreadable (%s)' % (tag, rel, type(e).__name__)); continue
                FACTS[p] = dict(file=rel, sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
                ok = (type(v) is dict and type(v.get('rows')) is list and type(v.get('start')) is int and type(v.get('end_exclusive')) is int
                      and 0 <= v['start'] < v['end_exclusive'] and type(v.get('total_intervals')) is int and v['end_exclusive'] <= v['total_intervals']
                      and v.get('implementation') in IMPLS and len(v['rows']) == v['end_exclusive'] - v['start']
                      and all(type(r) is dict and type(r.get('interval')) is int and r['interval'] == v['start'] + i for i, r in enumerate(v['rows'])))
                if not ok:
                    problems.append('%s: %s is no well-formed slice output' % (tag, rel)); continue
                out.append((p, rename(v, nm)))
    return out


def partition(files, impl):
    """The ranges of the slice files of one implementation, sorted; and whether they cover [0, total) exactly once."""
    rs = sorted((v['start'], v['end_exclusive']) for _, v in files if v['implementation'] == impl)
    totals_ = {v['total_intervals'] for _, v in files if v['implementation'] == impl}
    exact = (len(totals_) == 1 and bool(rs) and rs[0][0] == 0 and rs[-1][1] == next(iter(totals_)) and all(a[1] == b[0] for a, b in zip(rs, rs[1:])))
    return [list(r) for r in rs], exact


def join(parts):
    mins = [p['minimum_units'] for p in parts if p['minimum_units'] is not None]
    return dict(cells=sum(p['cells'] for p in parts), minimum_units=min(mins) if mins else None)


def totals(rows, names):
    deficits = [r['deficit_minimum_units'] for r in rows if r['deficit_minimum_units'] is not None]
    return dict(unrestricted_minimum_units=min(r['minimum_units'] for r in rows), deficit_minimum_units=min(deficits) if deficits else None,
                cells_default=join([r['default'] for r in rows]),
                cells_by_class=[dict(name=n, **join([r['classes'][i] for r in rows])) for i, n in enumerate(names)],
                failed_intervals=[r['interval'] for r in rows if not r['passed']])


def strip_row(r):
    return {k: v for k, v in r.items() if k not in ROW_SKIP}


def side(files, impl, problems, tag):
    """rows by interval and the list of headers of one implementation on one side."""
    rows = {}; heads = []
    for p, v in files:
        if v['implementation'] != impl:
            continue
        heads.append((p, {k: x for k, x in v.items() if k != 'rows'}))
        for r in v['rows']:
            i = r['interval']
            if i in rows and not same(strip_row(rows[i]), strip_row(r)):
                problems.append('%s: row %d differs between two files of the same side (%s)' % (tag, i, p))
            rows.setdefault(i, r)
    return rows, heads


def main(argv):
    args = [a for a in argv if not a.startswith('--')]
    opt = {}
    it = iter(argv)
    for a in it:
        if a in ('--hash-map', '--json', '--name-map', '--statement', '--stored-receipts', '--new-receipts', '--record'):
            opt[a] = next(it, None); args = [x for x in args if x != opt[a]]
        elif a == '--need-all':
            opt[a] = True
    if len(args) != 2 or not all(os.path.isdir(a) for a in args):
        print(__doc__); return 2
    stored_dir, new_dir = args
    hmap = None
    if opt.get('--hash-map'):
        hmap = {}
        for l in list(open(opt['--hash-map']))[1:]:
            w = l.rstrip('\n').split('\t'); hmap[w[2]] = w[3]
    nm = {}
    if opt.get('--name-map'):
        for l in open(opt['--name-map']):
            w = l.rstrip('\n').split('\t')
            if l.strip() and not l.startswith('#'):
                if len(w) != 2 or not w[0] or not w[1]:
                    print('bad line in the name map: %r' % l); return 2
                nm[w[0]] = w[1]
    problems = []; report = dict(stored=stored_dir, new=new_dir, implementations={})
    S = find(stored_dir, nm, problems, 'STORED'); N = find(new_dir, None, problems, 'NEW')
    impls = sorted({v['implementation'] for _, v in N})
    if not impls:
        problems.append('no slice output found in NEW')
    for impl in impls:
        srows, sheads = side(S, impl, problems, 'STORED'); nrows, nheads = side(N, impl, problems, 'NEW')
        rep = dict(new_files=len(nheads), stored_files=len(sheads), rows_new=len(nrows), rows_stored=len(srows), rows_compared=0, rows_identical=0,
                   rows_differing=0, rows_missing_in_stored=0, first_differences=[], header_fields_identical=[], header_fields_differing={},
                   hashes=[], workers={}, fields_excluded_per_row=list(ROW_SKIP), header_fields_excluded=list(TIMES),
                   row_fields_tested=sorted({k for r in nrows.values() for k in r if k not in ROW_SKIP}),
                   stored_slice_files=[file_facts(p, stored_dir) for p, v in S if v['implementation'] == impl],
                   new_slice_files=[file_facts(p, new_dir) for p, v in N if v['implementation'] == impl])
        report['implementations'][impl] = rep
        if not sheads:
            problems.append('%s: no slice output of this implementation in STORED' % impl); continue
        for i in sorted(nrows):
            if i not in srows:
                rep['rows_missing_in_stored'] += 1; continue
            rep['rows_compared'] += 1
            a = strip_row(srows[i]); b = strip_row(nrows[i])
            if same(a, b) and list(srows[i]) == list(nrows[i]):
                rep['rows_identical'] += 1
            else:
                rep['rows_differing'] += 1
                if len(rep['first_differences']) < 20:
                    bad = sorted(k for k in set(a) | set(b) if k not in a or k not in b or not same(a[k], b[k])) or ['key order']
                    rep['first_differences'].append(dict(interval=i, fields=bad, stored={k: a.get(k) for k in bad}, new={k: b.get(k) for k in bad}))
        if rep['rows_missing_in_stored']:
            problems.append('%s: %d rows of NEW are not in STORED' % (impl, rep['rows_missing_in_stored']))
        if rep['rows_differing']:
            problems.append('%s: %d rows differ' % (impl, rep['rows_differing']))
        if not rep['rows_compared']:
            problems.append('%s: no row compared' % impl)
        # headers
        by_range = {(h['start'], h['end_exclusive']): h for _, h in sheads}
        ident = None; differing = {}
        for p, h in nheads:
            ref = sheads[0][1]                      # range-independent fields: every stored header must agree among themselves
            free = [k for k in set(ref) | set(h) if k not in HASHES + TIMES + SETTING + RANGE]
            for _, sh in sheads:
                for k in free:
                    if k not in sh or k not in ref or not same(sh[k], ref[k]):
                        problems.append('%s: STORED headers disagree among themselves in %s' % (impl, k))
            ok = []
            for k in sorted(free):
                if k in ref and k in h and same(ref[k], h[k]):
                    ok.append(k)
                else:
                    differing.setdefault(k, dict(stored=ref.get(k), new=h.get(k), file=os.path.relpath(p, new_dir)))
            lo, hi = h['start'], h['end_exclusive']
            names = [c['name'] for c in h['classes']]
            rng = [nrows[i] for i in range(lo, hi)]
            tn = totals(rng, names)
            for k, v in tn.items():
                if not same(h.get(k), v):
                    differing.setdefault(k + ' (NEW header against NEW rows)', dict(header=h.get(k), from_rows=v, file=os.path.relpath(p, new_dir)))
            want_status = None if tn['failed_intervals'] else ('PASS_CLASSES_EXACT_COVER' if lo == 0 and hi == h.get('total_intervals') else 'PASS_CLASSES_INTERVAL_PARTITION_ONLY')
            if h.get('status') != want_status:
                differing.setdefault('status (NEW)', dict(new=h.get('status'), expected=want_status, file=os.path.relpath(p, new_dir)))
            if all(i in srows for i in range(lo, hi)):
                ts = totals([srows[i] for i in range(lo, hi)], names)
                for k in tn:
                    if not same(tn[k], ts[k]):
                        differing.setdefault(k + ' (recomputed from rows, STORED against NEW)', dict(stored=ts[k], new=tn[k], file=os.path.relpath(p, new_dir)))
                    else:
                        ok.append(k + ' (recomputed from the rows of both sides)')
            if (lo, hi) in by_range:
                sh = by_range[(lo, hi)]
                for k in RANGE:
                    if k in sh and k in h and same(sh[k], h[k]):
                        ok.append(k)
                    else:
                        differing.setdefault(k, dict(stored=sh.get(k), new=h.get(k), file=os.path.relpath(p, new_dir)))
            pair = tuple((k, ref.get(k), h.get(k)) for k in HASHES)
            if pair not in rep['hashes']:
                rep['hashes'].append(pair)
            for k, old, new in pair:
                if hmap is not None and hmap.get(old) != new:
                    msg = '%s: %s of NEW (%s) is not the stripped image of the stored one (%s) in the hash map' % (impl, k, new, old)
                    if msg not in problems:
                        problems.append(msg)
                if hmap is None and old == new:
                    rep.setdefault('note', []).append('%s is the same on both sides' % k)
            for k in SETTING:
                rep['workers'][os.path.relpath(p, new_dir)] = dict(stored=ref.get(k), new=h.get(k))
            ident = set(ok) if ident is None else ident & set(ok)
        rep['header_fields_identical'] = sorted(ident or [])
        rep['header_fields_differing'] = differing
        if differing:
            problems.append('%s: header fields differ: %s' % (impl, ', '.join(sorted(differing))))
        if len(rep['hashes']) != 1:
            problems.append('%s: more than one pair of input hashes among the slices' % impl)
        rep['partition'] = {}
        for tag, files in (('stored', S), ('new', N)):
            rs, ex = partition(files, impl)
            rep['partition'][tag] = dict(slice_files=len(rs), ranges=rs, covers_all_rows_exactly_once=ex)
        if opt.get('--need-all'):
            total = nheads[0][1].get('total_intervals')
            if sorted(nrows) != list(range(total)):
                problems.append('%s: NEW does not cover all %s rows (%d present)' % (impl, total, len(nrows)))
            if rep['rows_compared'] != total or rep['rows_identical'] != total:
                problems.append('%s: %d of %s rows compared, %d identical' % (impl, rep['rows_compared'], total, rep['rows_identical']))
            for tag in ('stored', 'new'):
                if not rep['partition'][tag]['covers_all_rows_exactly_once']:
                    problems.append('%s: the %s slice files do not cover the rows exactly once: %r' % (impl, tag, rep['partition'][tag]['ranges'][:30]))
        rep['hashes'] = [dict(field=k, stored=o, new=n, in_hash_map=(None if hmap is None else hmap.get(o) == n)) for pr in rep['hashes'] for k, o, n in pr]
    if len(impls) < 2:
        report['note'] = 'only %d implementation(s) found in NEW' % len(impls)
    if opt.get('--need-all'):
        both = ['node verify_classes.js', 'python exact_classes.py']
        if impls != both:
            problems.append('final acceptance needs exactly the two implementations in NEW; found %r' % impls)
        if sorted({v['implementation'] for _, v in S}) != both:
            problems.append('final acceptance needs exactly the two implementations in STORED')
    # the merged receipts, when given
    receipts = None
    if opt.get('--stored-receipts') or opt.get('--new-receipts'):
        receipts = {}
        if not (opt.get('--stored-receipts') and opt.get('--new-receipts')):
            problems.append('receipts: both --stored-receipts and --new-receipts are needed')
        else:
            for name in ('receipt_python.json', 'receipt_node.json'):
                po = os.path.join(opt['--stored-receipts'], name); pn = os.path.join(opt['--new-receipts'], name)
                try:
                    rawo = open(po, 'rb').read(); rawn = open(pn, 'rb').read()
                    FACTS[po] = dict(file=name, sha256=hashlib.sha256(rawo).hexdigest(), bytes=len(rawo))
                    FACTS[pn] = dict(file=name, sha256=hashlib.sha256(rawn).hexdigest(), bytes=len(rawn))
                    a = rename(json.loads(rawo.decode('utf-8')), nm); b = json.loads(rawn.decode('utf-8'))
                    if type(a) is not dict or type(b) is not dict:
                        raise ValueError('not an object')
                except Exception as e:
                    problems.append('%s: unreadable (%s)' % (name, type(e).__name__)); continue
                keys = sorted(set(a) | set(b)); skip = HASHES + TIMES + SETTING + PARTITION_FIELDS
                # merged_files counts the slice files of ITS OWN side: the two sides may be cut differently
                impl = 'python exact_classes.py' if name == 'receipt_python.json' else 'node verify_classes.js'
                pm = {}
                for tag, d_, files in (('stored', a, S), ('new', b, N)):
                    rs, ex = partition(files, impl)
                    pm[tag] = dict(merged_files=d_.get('merged_files'), slice_files=len(rs), covers_all_rows_exactly_once=ex,
                                   equal=type(d_.get('merged_files')) is int and d_['merged_files'] == len(rs) and ex)
                    if not pm[tag]['equal']:
                        problems.append('%s: merged_files of the %s receipt (%r) is not the number of %s slice files covering the rows exactly once (%d)'
                                        % (name, tag, d_.get('merged_files'), tag, len(rs)))
                bad = [k for k in keys if k not in skip and (k not in a or k not in b or not same(a[k], b[k]))]
                pairs = [(k, a.get(k), b.get(k)) for k in HASHES]
                for k, old, new in pairs:
                    if hmap is not None and hmap.get(old) != new:
                        problems.append('%s: %s of the new receipt is not the stripped image of the stored one in the hash map' % (name, k))
                if a.get('status') != 'PASS_CLASSES_EXACT_COVER' or b.get('status') != 'PASS_CLASSES_EXACT_COVER':
                    problems.append('%s: a receipt is not PASS_CLASSES_EXACT_COVER' % name)
                if bad:
                    problems.append('%s: fields differ: %s' % (name, ', '.join(bad)))
                receipts[name] = dict(stored=file_facts(po, opt['--stored-receipts']), new=file_facts(pn, opt['--new-receipts']),
                                      fields_tested=[k for k in keys if k not in skip], fields_differing=bad,
                                      partition_fields_not_required_equal=list(PARTITION_FIELDS), merged_files_each_against_its_own_slice_files=pm,
                                      input_hashes=[dict(field=k, stored=o, new=n) for k, o, n in pairs])
        report['receipts'] = receipts
    report['problems'] = problems
    report['verdict'] = 'IDENTICAL' if not problems else 'DIFFERENT'
    for impl, rep in report['implementations'].items():
        print('%s' % impl)
        print('  files: stored %d, new %d;  rows compared %d: identical %d, differing %d, not in stored %d' %
              (rep['stored_files'], rep['new_files'], rep['rows_compared'], rep['rows_identical'], rep['rows_differing'], rep['rows_missing_in_stored']))
        print('  row fields excluded: %s' % ', '.join(ROW_SKIP))
        print('  header fields identical: %s' % ', '.join(rep['header_fields_identical']))
        print('  header fields differing: %s' % (json.dumps(rep['header_fields_differing']) if rep['header_fields_differing'] else 'none'))
        for hh in rep['hashes']:
            print('  %s: %s -> %s%s' % (hh['field'], hh['stored'], hh['new'], '' if hh['in_hash_map'] is None else '  (pair in the hash map: %s)' % ('yes' if hh['in_hash_map'] else 'NO')))
        w = {(v['stored'], v['new']) for v in rep['workers'].values()}
        print('  workers (stored, new): %s;  times not compared: %s' % (sorted(w), ', '.join(TIMES)))
        for d in rep['first_differences'][:5]:
            print('  DIFFERENCE row %d: %s' % (d['interval'], json.dumps(d)[:400]))
    for p in problems:
        print('PROBLEM: ' + p)
    print('VERDICT: ' + report['verdict'])
    if opt.get('--json'):
        open(opt['--json'], 'w').write(json.dumps(report, indent=1) + '\n')
    if opt.get('--record'):
        def digest(path):
            return hashlib.sha256(open(path, 'rb').read()).hexdigest() if path else None
        rec = dict(schema='s17-neutral-comparison-record-v1', statement_id=opt.get('--statement'),
                   comparison_program=dict(file='compare_rows.py', sha256=digest(os.path.abspath(__file__))),
                   hash_map_sha256=digest(opt.get('--hash-map')), name_map_sha256=digest(opt.get('--name-map')), name_map=nm,
                   allowed_metadata_differences=dict(
                       row_fields_not_compared=list(ROW_SKIP),
                       header_fields_expected_to_differ={k: 'must be the pair old -> new of the hash map' for k in HASHES},
                       header_fields_not_compared=list(TIMES), header_fields_reported_only=list(SETTING),
                       receipt_fields_not_required_equal={k: 'each side must equal the number of its own slice files, which must cover the rows exactly once' for k in PARTITION_FIELDS},
                       class_names='replaced on the stored side by the name map' if nm else 'none: names must be identical'),
                   implementations={}, receipts=receipts, problems=problems, verdict=report['verdict'])
        for impl, rep in report['implementations'].items():
            rec['implementations'][impl] = dict(
                rows_new=rep['rows_new'], rows_stored=rep['rows_stored'], rows_compared=rep['rows_compared'], rows_identical=rep['rows_identical'],
                rows_mismatching=rep['rows_differing'], rows_missing_in_stored=rep['rows_missing_in_stored'],
                row_fields_tested=rep['row_fields_tested'], header_fields_tested=rep['header_fields_identical'] + sorted(rep['header_fields_differing']),
                header_fields_mismatching=sorted(rep['header_fields_differing']), input_hashes=rep['hashes'], workers=sorted({(v['stored'], v['new']) for v in rep['workers'].values()}),
                stored_slice_files=rep['stored_slice_files'], new_slice_files=rep['new_slice_files'], first_differences=rep['first_differences'],
                partition=rep.get('partition'))
        open(opt['--record'], 'w').write(json.dumps(rec, indent=1) + '\n')
    return 0 if not problems else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
