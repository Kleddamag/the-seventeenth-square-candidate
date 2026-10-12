#!/usr/bin/env python3
"""check_comparison_records.py : tests the records of the comparison between the capture computation carried in this
edition and the earlier executions, which are NOT carried.

    python3 check_comparison_records.py          (standard library only; reads only inside the edition; writes nothing)

For each of the 98 capture statements the edition carries one comparison record
(.../rerun-clean-20261011/records/<ID>/c2/comparison_record.json) and, for all together, the summary of the final call
(.../records/_calls/k19/SUMMARY.tsv).  This script tests what can be tested without the earlier executions:

  1. the summary lists exactly the statements of the plan, each once, each with the verdict IDENTICAL, no mismatching
     row, and the row count of the plan for both checkers;
  2. every record names its statement, the verdict IDENTICAL, no problem, and for each of the two checkers as many rows
     compared and identical as the plan has, none mismatching, none missing;
  3. the NEW side of every record is the computation carried here: the SHA-256 and size of every slice output, of the
     record of every slice, of the two merged receipts and of the merge record are those of the carried files; the two
     input files have the SHA-256 the record names as new; the three manifests are the carried ones;
  4. the record names the carried comparison programs and tables by SHA-256 (compare_statement.py, compare_rows.py,
     merge_select.py, strip_inputs.py, STATEMENTS.tsv, HASH_MAP.tsv, REMOVED_KEYS.tsv, the name map), and every pair
     (stored input hash, new input hash) it reports is a line of HASH_MAP.tsv;
  5. the totals: 98 statements, 1,152 slices and 1,728,000 rows per checker.  The two numbers are fixed in this script
     (EXPECTED_SLICES, EXPECTED_ROWS); the plan must give them and the records must add up to them.
  6. the stored slice files that a record names (SHA-256 and size) are exactly the ones that the producers' own audit
     record of that statement names (audit.json, field compatibility_check): two separately made statements about the
     earlier executions agree, and the audit record says that all row fields were equal.

NOT tested, because the earlier executions are not in this edition: that the hashes on the STORED side of a record
belong to files that existed, and that the comparison program was really run on them.  A record is a statement of the
project about a comparison it made; this script shows only that the records are complete, agree with each other, and
are bound to the computation carried here.  Exit code 0 only if the last line begins "COMPARISON RECORDS RESULT: PASS".
"""
import sys, os, json, csv, hashlib
ROOT = os.path.dirname(os.path.realpath(__file__))
RUN3 = 'local-research/claude-20261002/rerun-clean-20261011/'
CAP = 'research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/'
problems = []
def bad(msg):
    problems.append(msg)
    if len(problems) <= 40: print('BAD ' + msg)
def p(rel): return os.path.join(ROOT, *rel.split('/'))
def sha(rel):
    h = hashlib.sha256()
    with open(p(rel), 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()
def pin_ok(rel, want_sha, want_bytes=None):
    return os.path.isfile(p(rel)) and (want_bytes is None or os.path.getsize(p(rel)) == want_bytes) and sha(rel) == want_sha
def main():
    plan = json.load(open(p(CAP + 'checker_sources/PLAN_MANIFEST.json'), encoding='utf-8'))
    plans = {s['statement_id']: s for s in plan['statements']}
    man = {k: sha(CAP + 'checker_sources/' + n) for k, n in (('source_manifest_sha256', 'SOURCE_MANIFEST.json'), ('plan_manifest_sha256', 'PLAN_MANIFEST.json'), ('merge_manifest_sha256', 'MERGE_MANIFEST.json'))}
    tools = {'compare_statement': 'compare_statement.py', 'merge_select': 'merge_select.py', 'compare_rows': 'compare_rows.py', 'strip_inputs': 'strip_inputs.py',
             'statements_table': 'STATEMENTS.tsv', 'hash_map': 'HASH_MAP.tsv', 'removed_keys_table': 'REMOVED_KEYS.tsv', 'name_map': 'RENAME_MAP.proposed.tsv'}
    tool_sha = {k: sha(RUN3 + n) for k, n in tools.items()}
    with open(p(RUN3 + 'HASH_MAP.tsv'), encoding='utf-8') as f:
        hm = list(csv.reader(f, delimiter='\t'))[1:]
    pairs = {(r[0], r[1]): (r[2], r[3], int(r[5])) for r in hm}
    with open(p(RUN3 + 'STATEMENTS.tsv'), encoding='utf-8') as f:
        st = list(csv.DictReader(f, delimiter='\t'))
    if [r['id'] for r in st] != [s['statement_id'] for s in plan['statements']]: bad('STATEMENTS.tsv does not list the statements of the plan in the plan order')
    if len(pairs) != 2 * len(plans): bad('HASH_MAP.tsv does not have two lines per statement')
    # 1. the summary of the final call
    lines = open(p(RUN3 + 'records/_calls/k19/SUMMARY.tsv'), encoding='utf-8').read().rstrip('\n').split('\n')
    head = [l for l in lines if l.startswith('#')]; body = [l.split('\t') for l in lines if not l.startswith('#')]
    if head != ['# scope: ALL %d statements of the plan (final gate)' % len(plans), '# identical: %d of %d' % (len(plans), len(plans))]: bad('summary: head lines are %r' % head)
    cols = body[0]; rows = [dict(zip(cols, r)) for r in body[1:]]
    if sorted(r['statement'] for r in rows) != sorted(plans): bad('summary: does not list exactly the statements of the plan, each once')
    for r in rows:
        sid = r['statement']; total = plans.get(sid, {}).get('total_intervals')
        if not (r['verdict'] == 'IDENTICAL' and r['mismatching_rows'] == '0' and r['reason'] == '' and r['rows_python'] == r['rows_node'] == str(total) and r['record'] == '%s/%s/comparison_record.json' % (sid, r['comparison_attempt'])):
            bad('summary line of %s: %r' % (sid, r))
    # 2. to 4. every record
    n_slices = 0; n_rows = 0; n_files = 0
    for r in rows:
        sid = r['statement']; rel = RUN3 + 'records/' + r['record']; folder = CAP + 'statements/' + sid + '/'
        try:
            d = json.load(open(p(rel), encoding='utf-8'))
        except Exception as e:
            bad('%s: record cannot be read: %s' % (sid, e)); continue
        total = plans[sid]['total_intervals']; sl = plans[sid]['slices']
        def need(cond, what):
            if not cond: bad('%s: %s' % (sid, what))
        need(d.get('schema') == 's17-neutral-comparison-record-v1' and d.get('statement_id') == sid and d.get('comparison_attempt_id') == r['comparison_attempt'], 'identity of the record')
        need(d.get('verdict') == 'IDENTICAL' and d.get('verdict_of_compare_rows') == 'IDENTICAL' and d.get('problems') == [] and d.get('reason') == '', 'verdict')
        b = d.get('bridge', {})
        need(b.get('merge_attempt_id') == r['merge_attempt'] and b.get('compare_rows_return_code') == 0 and b.get('compare_rows_verdict') == 'IDENTICAL', 'bridge verdict')
        need(isinstance(b.get('binding_tests'), dict) and len(b['binding_tests']) == 8 and all(v is True for v in b['binding_tests'].values()), 'binding tests of the record')
        need(b.get('manifests') == man, 'the three manifests are not the carried ones')
        need(b.get('source_sha256') == tool_sha, 'programs and tables named by the record are not the carried ones')
        need(d.get('hash_map_sha256') == tool_sha['hash_map'] and d.get('name_map_sha256') == tool_sha['name_map'] and d.get('comparison_program', {}).get('sha256') == tool_sha['compare_rows'], 'hash map, name map or comparison program')
        need(pin_ok(folder + 'merge_provenance.json', b.get('merge_provenance_sha256')), 'merge record is not the carried one')
        sel = b.get('selected_slices', [])
        need([(x['slice_id'], x['start'], x['end_exclusive']) for x in sel] == [(x['slice_id'], x['start'], x['end_exclusive']) for x in sl], 'selected slices are not the planned slices')
        for x in sel:
            sf = folder + 'slices/%s-%s/' % (x['slice_id'], x['attempt_id'])
            need(pin_ok(sf + 'provenance.json', x['provenance_sha256']), 'record of slice %s' % x['slice_id'])
            for role, name in (('python', 'py.json'), ('node', 'node.json'), ('compare', 'compare.json')):
                need(pin_ok(sf + name, x[role]['sha256'], x[role]['bytes']), 'slice %s %s is not the carried file' % (x['slice_id'], name)); n_files += 1
        n_slices += len(sel)
        for role, name in (('python', 'receipt_python.json'), ('node', 'receipt_node.json')):
            br = b.get('receipts', {}).get(role, {})
            need(pin_ok(folder + name, br.get('sha256'), br.get('bytes')), name + ' is not the carried file')
            rr = d.get('receipts', {}).get(name, {})
            need(rr.get('new', {}).get('sha256') == br.get('sha256') and rr.get('fields_differing') == [], name + ': new side or differing fields')
        new_in = {'classes_sha256': sha(folder + 'classes.json'), 'certificate_sha256': sha(folder + 'certificate.json')}
        need(set(d.get('implementations', {})) == {'node verify_classes.js', 'python exact_classes.py'}, 'not exactly the two checkers')
        for impl, ext, role in (('python exact_classes.py', 'py', 'python'), ('node verify_classes.js', 'node', 'node')):
            im = d.get('implementations', {}).get(impl, {})
            need(im.get('rows_new') == im.get('rows_stored') == im.get('rows_compared') == im.get('rows_identical') == total and im.get('rows_mismatching') == 0 and im.get('rows_missing_in_stored') == 0
                 and im.get('header_fields_mismatching') == [] and im.get('first_differences') == [], impl + ': row counts')
            need([(f['sha256'], f['bytes']) for f in sorted(im.get('new_slice_files', []), key=lambda f: f['file'])] == [(x[role]['sha256'], x[role]['bytes']) for x in sel], impl + ': new slice files are not the selected files')
            need(im.get('partition', {}).get('new', {}).get('covers_all_rows_exactly_once') is True and im.get('partition', {}).get('stored', {}).get('covers_all_rows_exactly_once') is True, impl + ': partition')
            for h in im.get('input_hashes', []):
                kind = 'classes.json' if h['field'] == 'classes_sha256' else 'certificate.json'
                need(h.get('in_hash_map') is True and h['new'] == new_in[h['field']] and pairs.get((sid, kind), ('', '', 0))[:2] == (h['stored'], h['new']), impl + ': input hash pair of ' + kind)
            need(len(im.get('input_hashes', [])) == 2, impl + ': two input hashes')
        need(pairs.get((sid, 'classes.json'), ('', '', -1))[2] == os.path.getsize(p(folder + 'classes.json')) and pairs.get((sid, 'certificate.json'), ('', '', -1))[2] == os.path.getsize(p(folder + 'certificate.json')), 'sizes of the inputs in HASH_MAP.tsv')
        try:
            au = json.load(open(p(folder + 'audit.json'), encoding='utf-8'))
            s1 = {(x['sha256'], x['bytes']) for x in au['compatibility_check']['stored_slice_bytes']}
            s2 = {(x['sha256'], x['bytes']) for im in d['implementations'].values() for x in im['stored_slice_files']}
            need(s1 == s2 and au.get('old_new_comparison', '').startswith('ALL_ROW_FIELDS_EQUAL'), 'stored slice files differ from the ones the audit record of the producers names')
        except Exception as e:
            bad('%s: audit record cannot be compared: %s' % (sid, e))
        n_rows += total
    want_slices = sum(len(s['slices']) for s in plan['statements']); want_rows = sum(s['total_intervals'] for s in plan['statements'])
    if (want_slices, want_rows) != (EXPECTED_SLICES, EXPECTED_ROWS): bad('the plan has %d slices and %d rows; this script fixes %d and %d' % (want_slices, want_rows, EXPECTED_SLICES, EXPECTED_ROWS))
    if (n_slices, n_rows) != (EXPECTED_SLICES, EXPECTED_ROWS): bad('totals: %d slices, %d rows; this script fixes %d and %d' % (n_slices, n_rows, EXPECTED_SLICES, EXPECTED_ROWS))
    print('records read: %d; slices bound: %d (%d output files with SHA-256 and size); rows per checker reported identical: %d' % (len(rows), n_slices, n_files, n_rows))
    print('COMPARISON RECORDS RESULT: %s' % ('PASS (%d statements, each IDENTICAL in its record; the stored side is not in this edition and is not tested)' % len(rows) if not problems else 'FAIL (%d problems)' % len(problems)))
    return 0 if not problems else 1
EXPECTED_SLICES = 1152        # slices of the capture computation, all statements together
EXPECTED_ROWS = 1728000       # rows per checker, all statements together


if __name__ == '__main__':
    sys.exit(main())
