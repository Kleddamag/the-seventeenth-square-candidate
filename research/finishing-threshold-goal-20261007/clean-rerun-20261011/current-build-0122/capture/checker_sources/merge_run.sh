#!/bin/bash
# merge_run.sh: one merge attempt for one capture statement: the selected slice attempts are merged with both
# checkers' own --merge, with a neutral provenance record.
#
#   merge_run.sh STATEMENT_ID RESULTS_DIR DEST_DIR [MERGE_ATTEMPT_ID]
#
# RESULTS_DIR holds one directory per slice attempt (any names), each with py.json, node.json, compare.json and
# provenance.json as slice_run.sh wrote them.  Attempts are identified by the CONTENT of provenance.json, never by a
# directory name.
# The merge attempt gets its own directory DEST_DIR/STATEMENT_ID/MERGE_ATTEMPT_ID (m1, m2, ...), made by one exclusive
# mkdir before anything is written.  With an id given: if that directory exists in any state, nothing is written
# (exit code 94).  Without an id: the first free number is taken.  An attempt directory is never written twice.
# WHICH MERGE COUNTS for a statement: the lowest-numbered attempt whose merge_provenance.json says verdict PASS and
# names the current SOURCE_MANIFEST.json, PLAN_MANIFEST.json and MERGE_MANIFEST.json.  Other attempts stay as they are.
#
# Selection.  For every planned slice of PLAN_MANIFEST.json exactly one slice attempt is selected: the lowest attempt
# number among the attempts that pass ALL of the following, checked here from the files themselves (the verdict
# word of a record is not taken on trust):
#   record     schema, run, statement, planned slice and its exact range, attempt id; verdict PASS; python, node and
#              compare each started, exit code the integer 0, no signal, no time limit; wrapper exit code 0; the three
#              argv lists exactly those of the planned slice; optimisation level 0; every check of the record ok;
#              inputs before and after = plan; sources before and after = SOURCE_MANIFEST.json; the record names the
#              current SOURCE_MANIFEST.json and PLAN_MANIFEST.json
#   files      py.json, node.json, compare.json have the sha256 and size the record names
#   outputs    each of py.json and node.json: implementation, schema, exact range, total, input sha256, checker
#              sha256, pass status, no failed row, exactly the rows of the slice in order (integers), every row
#              well formed and passed; the two outputs agree in the header and in every row
#   compare    compare.json: PASS, PASS, agree yes, the range, all rows compared, none differing, and the sha256 and
#              size of the two outputs it read are those of the files
# Attempts that fail a test are listed as not selected with the reasons and never enter the merge.  The selected
# ranges must cover [0, total_intervals) exactly once.  The bytes that were checked are the bytes that are merged:
# they are written read-only into a fresh run root (sha256 measured before and after), where
#   python -B src/exact_classes.py inputs/certificate.json --classes inputs/classes.json --output out/receipt_python.json --merge slices/<id>.py.json ...
#   node src/node/verify_classes_wb.js inputs/certificate.json --classes inputs/classes.json --output out/receipt_node.json --merge slices/<id>.node.json ...
# run with the run root as working directory.  Written into the attempt directory:
#   receipt_python.json  receipt_node.json     the two merged outputs, unmodified
#   merge_provenance.json                      schema s17-neutral-merge-provenance-v1, written last, atomically
#   diag/                                      console logs: diagnostics, not part of the record
# The sources this script runs are those of MERGE_MANIFEST.json (this wrapper, the five Python files, the Node
# checker; the checker files must be the ones SOURCE_MANIFEST.json names).
# Verdict PASS only if both merges ran and exited 0, both receipts say PASS_CLASSES_EXACT_COVER for rows 0..total with
# no problem, no missing and no failed row, count as merged files exactly the selected slices, are for the plan's
# inputs and the manifest's sources, agree with each other on status, statement, header, coverage, minima and cell
# counts, and carry the minima and cell counts recomputed here from the selected rows.
# Exit code: 0 PASS, 2 FAIL (a failed row), 3 INCOMPLETE, 91 bad arguments, 94 the attempt directory exists already
# (nothing written), 1 the driver part ended on an error it did not foresee (no record; the attempt id stays used).
# Variables read by this script:
#   MERGE_PYTHON   interpreter that has numpy and numba: runs the Python merge and one version question (default:
#                  python3 as found on PATH)
#   MERGE_NODE     node executable (default: node on PATH)
#   MERGE_TIMEOUT  seconds per merge (default 3600)
#   MERGE_TMP      parent of the run root (default: the system's temporary directory: TMPDIR, TEMP or TMP)
#   PATH (python3, node), TMPDIR / TEMP / TMP (temporary files)
# Programs started: the python3 found on PATH (MERGE_PYTHON if there is none), which reads the driver part of this
# file in isolated mode; one version question to MERGE_PYTHON and one to node; the Python merge; the Node merge.  The
# merges and the Python version question inherit the environment of this script with PYTHONOPTIMIZE removed; the
# record lists, by NAME only, the variables set in it that can change how they run (environment_names_set).
# A time limit ends the merge concerned (its whole process group).  If this script itself is ended from outside while
# a merge runs, that merge is NOT ended with it, no record is written, the run root stays and the attempt id stays
# used.  This script sends and fetches nothing.
SID=$1; RESULTS=$2; DEST=$3; MID=${4:-}
CAP=$(cd "$(dirname "$0")" && pwd)
U="usage: merge_run.sh STATEMENT_ID RESULTS_DIR DEST_DIR [MERGE_ATTEMPT_ID]"
case "$SID" in ""|.*|*[!A-Za-z0-9._-]*) echo "$U" >&2; exit 91 ;; esac
[ -d "$RESULTS" ] && [ -n "$DEST" ] && [ $# -le 4 ] || { echo "$U" >&2; exit 91; }
case "$MID" in ""|m[1-9]|m[1-9][0-9]|m[1-9][0-9][0-9]) ;; *) echo "$U (attempt id: m1 ... m999)" >&2; exit 91 ;; esac
# ---- the attempt directory: the statement's folder may exist, the attempt's directory must be made here and now
mkdir -p "$DEST/$SID" || exit 91
if [ -n "$MID" ]; then
  if ! mkdir "$DEST/$SID/$MID" 2> /dev/null; then
    echo "merge_run.sh: $SID $MID exists already; nothing written; another merge needs a new attempt id" >&2; exit 94
  fi
else
  n=1
  while ! mkdir "$DEST/$SID/m$n" 2> /dev/null; do
    [ -e "$DEST/$SID/m$n" ] || [ -L "$DEST/$SID/m$n" ] || exit 91
    n=$((n + 1)); [ "$n" -le 999 ] || exit 91
  done
  MID=m$n
fi
OUT=$DEST/$SID/$MID
mkdir "$OUT/diag" || exit 91
PY=${MERGE_PYTHON:-python3}
NODE=${MERGE_NODE:-$(command -v node 2> /dev/null)}
DRV=$(command -v python3 2> /dev/null); [ -n "$DRV" ] || DRV=$PY
exec "$DRV" -I -B - "$CAP/$(basename "$0")" "$CAP" "$RESULTS" "$OUT" "$SID" "$MID" "$PY" "${NODE:-}" "${MERGE_TIMEOUT:-3600}" <<'DRIVER_EOF'
# The driver (Python, standard library only), read from this file by the interpreter started above; it is part of the
# wrapper and of its sha256.
import sys, os, json, hashlib, shutil, subprocess, signal, re, datetime, tempfile

(WRAPPER, CAP, RESULTS, OUT, SID, MID, PY, NODE, TMO) = sys.argv[1:10]
TMO = int(TMO) if re.fullmatch(r'[1-9][0-9]{0,6}', TMO) else 3600
SCHEMA = 's17-neutral-merge-provenance-v1'; SLICE_SCHEMA = 's17-neutral-slice-provenance-v1'
PY_ROLES = ('python_checker_main', 'python_checker_restricted', 'python_checker_general', 'python_checker_sweep', 'python_checker_rule')
SLICE_ROLES = PY_ROLES + ('node_checker', 'launch_wrapper', 'output_comparator')
MERGE_ROLES = PY_ROLES + ('node_checker', 'merge_wrapper')
HEADER = ('schema', 'symmetry', 'bound', 'classes', 'total_intervals', 'required_units', 'budget_units', 'surplus', 'certificate_sha256', 'classes_sha256')
ROW = ('passed', 'minimum_units', 'cells', 'deficient_slabs', 'deficit_minimum_units', 'default', 'classes')
AGREE = ('status', 'statement', 'schema', 'symmetry', 'bound', 'classes', 'total_intervals', 'required_units', 'budget_units', 'surplus',
         'certificate_sha256', 'classes_sha256', 'start', 'end_exclusive', 'merged_files', 'problems', 'missing_intervals', 'first_missing_intervals',
         'failed_intervals', 'unrestricted_minimum_units', 'deficit_minimum_units', 'cells_default', 'cells_by_class')
PART = 'PASS_CLASSES_INTERVAL_PARTITION_ONLY'; WHOLE = 'PASS_CLASSES_EXACT_COVER'
SLICE_CHECKS = 13          # the number of checks a slice record of verdict PASS carries
UTC = r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z'
HEX = r'[0-9a-f]{64}'


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def sha_file(p):
    try:
        with open(p, 'rb') as f:
            return sha(f.read())
    except OSError:
        return None


def read(p):
    try:
        with open(p, 'rb') as f:
            return f.read()
    except OSError:
        return None


def atomic(path, text):
    tmp = path + '.tmp'
    with open(tmp, 'w') as f:
        f.write(text); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)


def exact(x, v):
    """x is the integer v: a JSON integer, neither a float nor true / false."""
    return type(x) is int and x == v


def same(a, b):
    """Equal values of equal JSON types, at every depth."""
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return set(a) == set(b) and all(same(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


NOT_RUN = dict(started=False, exit_code=None, signal=None, timed_out=False)
prov = dict(schema=SCHEMA, run_id=None, statement_id=SID, merge_attempt_id=MID, rows=dict(start=0, end_exclusive=None, total_intervals=None),
            source_manifest_sha256=None, plan_manifest_sha256=None, merge_manifest_sha256=None,
            selection_rule='per planned slice: the lowest attempt number among the attempts that pass every test of merge_run.sh (record, files, outputs, compare)',
            counting_rule='the merge that counts for a statement is the lowest-numbered merge attempt with verdict PASS that names the current source, plan and merge manifests',
            selected_slices=[], not_selected=[], planned_slices_without_a_selected_attempt=[],
            input_sha256_before=None, input_sha256_after=None, source_sha256_before=None, source_sha256_after=None,
            slice_files_unchanged=None, invocation=dict(python=None, node=None), runtime=None, started_utc=utc(), finished_utc=None,
            exits=dict(python=dict(NOT_RUN), node=dict(NOT_RUN), wrapper=dict(exit_code=None)),
            outputs=dict(python=None, node=None), checks=[], verdict='INCOMPLETE', detail=[],
            environment_names_set=sorted(k for k in os.environ if k != 'PYTHONOPTIMIZE' and re.fullmatch(
                r'PYTHON.*|NUMBA_.*|NODE_.*|.*_NUM_THREADS|LD_PRELOAD|LD_LIBRARY_PATH|DYLD_.*|BASH_ENV|CDPATH', k)))
RUNROOT = None


def finish(verdict):
    code = {'PASS': 0, 'FAIL': 2}.get(verdict, 3)
    prov['verdict'] = verdict; prov['finished_utc'] = utc(); prov['exits']['wrapper']['exit_code'] = code
    atomic(os.path.join(OUT, 'merge_provenance.json'), json.dumps(prov, indent=1) + '\n')
    if RUNROOT:
        for d, _, fs in os.walk(RUNROOT):
            os.chmod(d, 0o700)
        shutil.rmtree(RUNROOT, ignore_errors=True)
    print('%s %s %s selected %d not selected %d%s' % (SID, MID, verdict, len(prov['selected_slices']), len(prov['not_selected']),
                                                    (' detail=' + ','.join(prov['detail'])) if prov['detail'] else ''))
    sys.exit(code)


def stop(word):
    prov['detail'].append(word); finish('INCOMPLETE')


def run(role, real, argv, log):
    ex = prov['exits'][role]
    env = dict(os.environ); env.pop('PYTHONOPTIMIZE', None)
    with open(log, 'wb') as lf:
        try:
            p = subprocess.Popen([real] + argv[1:], cwd=RUNROOT, stdin=subprocess.DEVNULL, stdout=lf, stderr=subprocess.STDOUT, env=env, start_new_session=True)
        except OSError as e:
            prov['detail'].append('%s_not_started:%s' % (role, type(e).__name__)); return
        ex['started'] = True
        try:
            rc = p.wait(timeout=TMO)
        except subprocess.TimeoutExpired:
            ex['timed_out'] = True
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            rc = p.wait()
        if rc < 0:
            ex['signal'] = -rc
        else:
            ex['exit_code'] = rc


# ---- the manifests and the plan
try:
    sm_raw = open(os.path.join(CAP, 'SOURCE_MANIFEST.json'), 'rb').read(); SM = json.loads(sm_raw)
    mm_raw = open(os.path.join(CAP, 'MERGE_MANIFEST.json'), 'rb').read(); MM = json.loads(mm_raw)
    pm_raw = open(os.path.join(CAP, 'PLAN_MANIFEST.json'), 'rb').read(); PM = json.loads(pm_raw)
except (OSError, ValueError):
    stop('manifest_unreadable')
prov['source_manifest_sha256'] = sha(sm_raw); prov['plan_manifest_sha256'] = sha(pm_raw); prov['merge_manifest_sha256'] = sha(mm_raw)
prov['run_id'] = PM.get('run_id')
slice_roles = SM.get('roles', {})          # the sources the slice records must name
roles = MM.get('roles', {})                # the sources this merge runs
if set(slice_roles) != set(SLICE_ROLES) or set(roles) != set(MERGE_ROLES):
    stop('manifest_roles')
if any(roles[r] != slice_roles[r] for r in PY_ROLES + ('node_checker',)):
    stop('merge_manifest_names_other_checkers_than_the_slice_manifest')
st = [s for s in PM.get('statements', []) if s.get('statement_id') == SID]
if len(st) != 1:
    stop('statement_not_in_plan')
st = st[0]; TOTAL = st['total_intervals']
if type(TOTAL) is not int or TOTAL < 1:
    stop('plan_total')
prov['rows'].update(end_exclusive=TOTAL, total_intervals=TOTAL)
plan = sorted(st['slices'], key=lambda s: s['start'])
if not (plan and all(type(s.get('start')) is int and type(s.get('end_exclusive')) is int and type(s.get('slice_id')) is str for s in plan)
        and plan[0]['start'] == 0 and plan[-1]['end_exclusive'] == TOTAL and all(a['end_exclusive'] == b['start'] for a, b in zip(plan, plan[1:]))
        and all(a['start'] < a['end_exclusive'] for a in plan) and len({s['slice_id'] for s in plan}) == len(plan)):
    stop('planned_slices_do_not_cover_the_rows_exactly_once')
want_inputs = dict(certificate=st['certificate_sha256'], classes=st['classes_sha256'])
want_sources = {r: slice_roles[r]['sha256'] for r in SLICE_ROLES}
WANT_CHECKER = {'python': {os.path.basename(slice_roles[r]['file']): slice_roles[r]['sha256'] for r in PY_ROLES},
                'node': {'verify_classes.js': slice_roles['node_checker']['sha256']}}
IMPL = {'python': 'python exact_classes.py', 'node': 'node verify_classes.js'}


# ---- the tests of one slice attempt
def part_ok(p):
    return (type(p) is dict and type(p.get('cells')) is int and p['cells'] >= 0
            and (p.get('minimum_units') is None or type(p['minimum_units']) is int))


def row_ok(r, names):
    return (type(r.get('passed')) is bool and type(r.get('minimum_units')) is int and type(r.get('cells')) is int
            and type(r.get('deficient_slabs')) is int
            and (r.get('deficit_minimum_units') is None or type(r['deficit_minimum_units']) is int)
            and r['passed'] == (r.get('deficit_minimum_units') is None) and r['passed'] == (r.get('witness') is None)
            and part_ok(r.get('default')) and type(r.get('classes')) is list and len(r['classes']) == len(names)
            and all(part_ok(p) and p.get('name') == n for p, n in zip(r['classes'], names))
            and r['default']['cells'] + sum(p['cells'] for p in r['classes']) == r['cells'])


def test_output(raw, role, s, e, why):
    """The parsed output, or None; reasons are appended to why."""
    tag = 'py.json' if role == 'python' else 'node.json'
    try:
        d = json.loads(raw.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        why.append(tag + ' unreadable'); return None
    if type(d) is not dict:
        why.append(tag + ' is no object'); return None
    bad = []
    if d.get('implementation') != IMPL[role] or d.get('schema') != 's17-classes-v1': bad.append('implementation or schema')
    if not (exact(d.get('start'), s) and exact(d.get('end_exclusive'), e) and exact(d.get('total_intervals'), TOTAL)): bad.append('range')
    if d.get('certificate_sha256') != want_inputs['certificate'] or d.get('classes_sha256') != want_inputs['classes']: bad.append('input sha256')
    if d.get('checker_sha256') != WANT_CHECKER[role]: bad.append('checker sha256')
    if d.get('status') != (WHOLE if (s == 0 and e == TOTAL) else PART) or d.get('failed_intervals') != []: bad.append('status')
    cls = d.get('classes'); rows = d.get('rows')
    if not (type(cls) is list and cls and all(type(k) is dict and type(k.get('name')) is str for k in cls)):
        bad.append('class list')
    elif not (type(rows) is list and len(rows) == e - s and all(type(r) is dict and exact(r.get('interval'), s + i) for i, r in enumerate(rows))):
        bad.append('row sequence')
    elif not all(row_ok(r, [k['name'] for k in cls]) and r['passed'] is True for r in rows):
        bad.append('row records')
    if bad:
        why.append('%s: %s' % (tag, ', '.join(bad))); return None
    return d


def test_attempt(d, praw, r):
    """(slice of the plan or None, attempt number, files, reasons).  files: role -> (facts, bytes)."""
    why = []; files = {}
    rows = r.get('rows') if type(r.get('rows')) is dict else {}
    sl = [s for s in plan if s['slice_id'] == r.get('slice_id') and exact(rows.get('start'), s['start']) and exact(rows.get('end_exclusive'), s['end_exclusive'])]
    sl = sl[0] if len(sl) == 1 and exact(rows.get('total_intervals'), TOTAL) and r.get('planned') is True else None
    if sl is None: why.append('rows are no planned slice')
    m = re.fullmatch(r'a([1-9][0-9]{0,2})', r.get('attempt_id') if type(r.get('attempt_id')) is str else '')
    if not m: why.append('attempt id')
    if r.get('verdict') != 'PASS': why.append('verdict ' + str(r.get('verdict')))
    ex = r.get('exits') if type(r.get('exits')) is dict else {}
    for k in ('python', 'node', 'compare'):
        e = ex.get(k) if type(ex.get(k)) is dict else {}
        if not (e.get('started') is True and exact(e.get('exit_code'), 0) and e.get('signal') is None and e.get('timed_out') is False):
            why.append('process state of ' + k)
    if not (type(ex.get('wrapper')) is dict and exact(ex['wrapper'].get('exit_code'), 0)): why.append('wrapper exit code')
    if r.get('input_sha256_before') != want_inputs or r.get('input_sha256_after') != want_inputs: why.append('inputs are not those of the plan')
    if r.get('source_sha256_before') != want_sources or r.get('source_sha256_after') != want_sources: why.append('sources are not those of the manifest')
    if r.get('source_manifest_sha256') != prov['source_manifest_sha256'] or r.get('plan_manifest_sha256') != prov['plan_manifest_sha256']: why.append('another manifest')
    ck = r.get('checks')
    if not (type(ck) is list and len(ck) == SLICE_CHECKS and all(type(c) is dict and type(c.get('check')) is str and c.get('ok') is True for c in ck)): why.append('checks of the record')
    if r.get('detail') != []: why.append('detail of the record')
    rt = r.get('runtime') if type(r.get('runtime')) is dict else {}
    if not (exact(rt.get('python_optimization_level'), 0) and all(type(rt.get(k)) is str and rt[k] for k in (
            'python_implementation', 'python_version', 'numpy_version', 'numba_version', 'node_version', 'platform_system', 'platform_architecture'))): why.append('runtime')
    if not (type(r.get('started_utc')) is str and re.fullmatch(UTC, r['started_utc']) and type(r.get('finished_utc')) is str and re.fullmatch(UTC, r['finished_utc'])
            and r['started_utc'] <= r['finished_utc']): why.append('time stamps')
    en = r.get('environment_names_set')
    if not (type(en) is list and all(type(x) is str for x in en)): why.append('environment names')
    for role, fn in (('python', 'py.json'), ('node', 'node.json'), ('compare', 'compare.json')):
        o = r.get('outputs', {}).get(role) if type(r.get('outputs')) is dict else None
        raw = read(os.path.join(d, fn))
        if not (type(o) is dict and o.get('file') == fn and type(o.get('sha256')) is str and re.fullmatch(HEX, o['sha256']) and raw is not None
                and sha(raw) == o['sha256'] and exact(o.get('bytes'), len(raw))):
            why.append('%s is not the file of the record' % fn)
        else:
            files[role] = (dict(file=fn, sha256=o['sha256'], bytes=o['bytes']), raw)
    if sl is not None and len(files) == 3:
        s, e = sl['start'], sl['end_exclusive']; n = e - s
        inv = r.get('invocation') if type(r.get('invocation')) is dict else {}
        ip, inn, ic = (inv.get(k) if type(inv.get(k)) is dict else {} for k in ('python', 'node', 'compare'))
        wp, wn = ip.get('workers'), inn.get('workers')
        okinv = (type(wp) is int and wp >= 1 and type(wn) is int and 1 <= wn <= n
                 and all(type(x.get('timeout_seconds')) is int and x['timeout_seconds'] >= 1 for x in (ip, inn, ic)))
        if okinv:
            okinv = (ip.get('argv') == ['python', '-B', 'src/exact_classes.py', 'inputs/certificate.json', '--classes', 'inputs/classes.json',
                                        '--start', str(s), '--count', str(n), '--workers', str(wp), '--output', 'out/py.json']
                     and inn.get('argv') == ['node', 'src/node/verify_classes_wb.js', 'inputs/certificate.json', '--classes', 'inputs/classes.json',
                                             '--start', str(s), '--count', str(n), '--workers', str(wn), '--output', 'out/node.json']
                     and ic.get('argv') == ['python', '-B', 'src/slice_compare.py', 'out/py.json', 'out/node.json', str(s), str(e), want_inputs['certificate'],
                                            want_inputs['classes'], '0', 'no', '0', 'RUN', 'out/compare.json'])
        if not okinv: why.append('invocations are not those of the planned slice')
        dp = test_output(files['python'][1], 'python', s, e, why); dn = test_output(files['node'][1], 'node', s, e, why)
        if dp is not None and dn is not None:
            if not all(k in dp and k in dn and same(dp[k], dn[k]) for k in HEADER): why.append('the two outputs differ in the header')
            elif not all(same(p[k], q[k]) for p, q in zip(dp['rows'], dn['rows']) for k in ROW): why.append('the two outputs differ in a row')
        try:
            dc = json.loads(files['compare'][1].decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            dc = None
        if not (type(dc) is dict and dc.get('python') == 'PASS' and dc.get('node') == 'PASS' and dc.get('agree') == 'yes'
                and type(dc.get('rows')) is list and len(dc['rows']) == 2 and exact(dc['rows'][0], s) and exact(dc['rows'][1], e)
                and exact(dc.get('rows_compared'), n) and exact(dc.get('rows_differing'), 0) and exact(dc.get('header_fields_differing'), 0)
                and dc.get('differences') == [] and exact(dc.get('python_exit'), 0) and exact(dc.get('node_exit'), 0)
                and dc.get('certificate_sha256') == want_inputs['certificate'] and dc.get('classes_sha256') == want_inputs['classes']
                and dc.get('python_output_sha256') == files['python'][0]['sha256'] and exact(dc.get('python_output_bytes'), files['python'][0]['bytes'])
                and dc.get('node_output_sha256') == files['node'][0]['sha256'] and exact(dc.get('node_output_bytes'), files['node'][0]['bytes'])):
            why.append('compare.json does not show a full agreement of these two files')
    return sl, int(m.group(1)) if m else 0, files, why


# ---- the attempts found, by the content of their records
found = {}; other = []
for name in sorted(os.listdir(RESULTS)):
    d = os.path.join(RESULTS, name); praw = read(os.path.join(d, 'provenance.json'))
    if praw is None:
        continue
    try:
        r = json.loads(praw.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        continue
    if type(r) is not dict or r.get('schema') != SLICE_SCHEMA or r.get('statement_id') != SID or r.get('run_id') != prov['run_id']:
        continue
    sl, n, files, why = test_attempt(d, praw, r)
    rec = dict(slice_id=r.get('slice_id') if type(r.get('slice_id')) is str else None, attempt_id=r.get('attempt_id') if type(r.get('attempt_id')) is str else None,
               verdict=r.get('verdict') if type(r.get('verdict')) is str else None, provenance_sha256=sha(praw), files=files, n=n, why=why, sl=sl)
    if sl is None:
        other.append(rec)
    else:
        found.setdefault(sl['slice_id'], []).append(rec)
selected = []
for s in plan:
    cands = sorted(found.get(s['slice_id'], []), key=lambda z: z['n'])
    if len({c['attempt_id'] for c in cands}) != len(cands):
        stop('two_records_with_the_same_attempt_id:' + s['slice_id'])
    ok = [c for c in cands if not c['why']]
    if ok:
        c = ok[0]; selected.append(c)
        prov['selected_slices'].append(dict(slice_id=s['slice_id'], attempt_id=c['attempt_id'], start=s['start'], end_exclusive=s['end_exclusive'],
                                            provenance_sha256=c['provenance_sha256'], python=c['files']['python'][0], node=c['files']['node'][0], compare=c['files']['compare'][0]))
    else:
        prov['planned_slices_without_a_selected_attempt'].append(s['slice_id'])
    for c in cands:
        if not ok or c is not ok[0]:
            prov['not_selected'].append(dict(slice_id=c['slice_id'], attempt_id=c['attempt_id'], verdict=c['verdict'], provenance_sha256=c['provenance_sha256'],
                                             reason='; '.join(c['why']) or 'a lower attempt number that passes every test was selected'))
        if not ok or c is not ok[0]:
            c['files'] = {}                 # bytes of attempts that are not merged are dropped
for c in other:
    prov['not_selected'].append(dict(slice_id=c['slice_id'], attempt_id=c['attempt_id'], verdict=c['verdict'], provenance_sha256=c['provenance_sha256'], reason='; '.join(c['why'])))
if prov['planned_slices_without_a_selected_attempt']:
    stop('planned_slices_without_a_completed_attempt')
cover = [(c['sl']['start'], c['sl']['end_exclusive']) for c in selected]
if not (len(selected) == len(plan) and cover[0][0] == 0 and cover[-1][1] == TOTAL and all(a[1] == b[0] for a, b in zip(cover, cover[1:]))):
    stop('selected_slices_do_not_cover_the_rows_exactly_once')

# ---- staging: the checked bytes, read-only, in a fresh run root
base = os.environ.get('MERGE_TMP') or None
if base:
    os.makedirs(base, exist_ok=True)
RUNROOT = tempfile.mkdtemp(prefix='merge_', dir=base)
for sub in ('out', 'inputs', 'slices'):
    os.makedirs(os.path.join(RUNROOT, sub))
staged = {}
for role in MERGE_ROLES:
    rel = roles[role]['file']
    if role == 'merge_wrapper':
        staged[role] = WRAPPER; continue
    dst = os.path.join(RUNROOT, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    try:
        shutil.copyfile(os.path.join(CAP, rel), dst); os.chmod(dst, 0o444)
    except OSError:
        stop('source_missing:' + role)
    staged[role] = dst
inputs = {}
for key, name in (('certificate', 'certificate.json'), ('classes', 'classes.json')):
    dst = os.path.join(RUNROOT, 'inputs', name)
    try:
        shutil.copyfile(os.path.join(CAP, 'inputs', SID, name), dst); os.chmod(dst, 0o444)
    except OSError:
        stop('input_missing:' + key)
    inputs[key] = dst
slice_paths = []
for c in selected:
    for role, ext in (('python', 'py'), ('node', 'node')):
        dst = os.path.join(RUNROOT, 'slices/%s.%s.json' % (c['slice_id'], ext))
        with open(dst, 'wb') as f:
            f.write(c['files'][role][1])
        os.chmod(dst, 0o444)
        slice_paths.append((dst, c['files'][role][0]['sha256']))


def measure():
    return {k: sha_file(p) for k, p in inputs.items()}, {r: sha_file(staged[r]) for r in MERGE_ROLES}, all(sha_file(p) == h for p, h in slice_paths)


prov['input_sha256_before'], prov['source_sha256_before'], slices_ok = measure()
if prov['input_sha256_before'] != want_inputs:
    stop('staged_inputs_are_not_those_of_the_plan')
if prov['source_sha256_before'] != {r: roles[r]['sha256'] for r in MERGE_ROLES}:
    stop('staged_sources_are_not_those_of_the_manifest')
if not slices_ok:
    stop('staged_slice_files_differ_from_their_records')

note = 'argv[0] names the program, its path is not recorded; working directory = run root; PYTHONOPTIMIZE unset'
a_py = ['python', '-B', 'src/exact_classes.py', 'inputs/certificate.json', '--classes', 'inputs/classes.json', '--output', 'out/receipt_python.json',
        '--merge'] + ['slices/%s.py.json' % c['slice_id'] for c in selected]
a_node = ['node', 'src/node/verify_classes_wb.js', 'inputs/certificate.json', '--classes', 'inputs/classes.json', '--output', 'out/receipt_node.json',
          '--merge'] + ['slices/%s.node.json' % c['slice_id'] for c in selected]
prov['invocation'] = dict(python=dict(argv=a_py, timeout_seconds=TMO, note=note), node=dict(argv=a_node, timeout_seconds=TMO, note=note))
rt = dict(python_implementation=None, python_version=None, python_optimization_level=None, numpy_version=None, numba_version=None,
          node_version=None, platform_system=None, platform_architecture=None)
prov['runtime'] = rt
probe = ('import sys, json, platform, numpy, numba; print(json.dumps(dict(python_implementation=platform.python_implementation(), '
         'python_version=platform.python_version(), python_optimization_level=sys.flags.optimize, numpy_version=numpy.__version__, '
         'numba_version=numba.__version__, platform_system=platform.system(), platform_architecture=platform.machine())))')
env0 = dict(os.environ); env0.pop('PYTHONOPTIMIZE', None)
try:
    r = subprocess.run([PY, '-B', '-c', probe], cwd=RUNROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env0, timeout=600)
    rt.update(json.loads(r.stdout.decode().strip().splitlines()[-1]))
except Exception:
    stop('python_with_numpy_and_numba_not_available')
if rt['python_optimization_level'] != 0:
    stop('python_optimization_level_is_not_0')
try:
    r = subprocess.run([NODE, '--version'], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    v = r.stdout.decode().strip().splitlines()[0]
    rt['node_version'] = v if re.fullmatch(r'[A-Za-z0-9._-]{1,40}', v) else None
except Exception:
    pass
if rt['node_version'] is None:
    stop('no_node_executable')

run('python', PY, a_py, os.path.join(OUT, 'diag', 'merge_python.log'))
run('node', NODE, a_node, os.path.join(OUT, 'diag', 'merge_node.log'))
prov['input_sha256_after'], prov['source_sha256_after'], prov['slice_files_unchanged'] = measure()
receipts = {}
for role, name in (('python', 'receipt_python.json'), ('node', 'receipt_node.json')):
    raw = read(os.path.join(RUNROOT, 'out', name))
    if raw:
        dst = os.path.join(OUT, name)
        with open(dst + '.tmp', 'wb') as f:
            f.write(raw); f.flush(); os.fsync(f.fileno())
        os.replace(dst + '.tmp', dst)
        if read(dst) != raw:
            os.remove(dst); prov['detail'].append('receipt_copy_differs:' + role); continue
        prov['outputs'][role] = dict(file=name, sha256=sha(raw), bytes=len(raw)); receipts[role] = raw

checks = prov['checks']


def check(name, ok):
    checks.append(dict(check=name, ok=bool(ok))); return bool(ok)


def join(parts):
    mins = [p['minimum_units'] for p in parts if p['minimum_units'] is not None]
    return dict(cells=sum(p['cells'] for p in parts), minimum_units=min(mins) if mins else None)


ep = prov['exits']['python']; en = prov['exits']['node']
g = check('inputs: before == after == plan', prov['input_sha256_after'] == want_inputs)
g &= check('sources: before == after == merge manifest', prov['source_sha256_after'] == prov['source_sha256_before'])
g &= check('slice files unchanged during the merges', prov['slice_files_unchanged'] is True)
g &= check('both merges started, exited, no signal, no time limit', all(e['started'] and not e['timed_out'] and e['signal'] is None and e['exit_code'] is not None for e in (ep, en)))
integrity = g
g &= check('both merges exit code 0', ep['exit_code'] == 0 and en['exit_code'] == 0)
g &= check('both receipts present', len(receipts) == 2)
failed_row = False
if len(receipts) == 2:
    try:
        dp = json.loads(receipts['python'].decode('utf-8')); dn = json.loads(receipts['node'].decode('utf-8'))
        sb = prov['source_sha256_before']
        for tag, d, role in (('python', dp, 'python'), ('node', dn, 'node')):
            g &= check(tag + ' receipt: PASS_CLASSES_EXACT_COVER for rows 0..total, merged files = the selected slices, no problem, none missing, none failed',
                       d.get('status') == WHOLE and d.get('implementation') == IMPL[role] and exact(d.get('start'), 0) and exact(d.get('end_exclusive'), TOTAL)
                       and exact(d.get('total_intervals'), TOTAL) and exact(d.get('merged_files'), len(selected)) and d.get('problems') == []
                       and exact(d.get('missing_intervals'), 0) and d.get('first_missing_intervals') == [] and d.get('failed_intervals') == []
                       and type(d.get('statement')) is str)
            g &= check(tag + ' receipt: input sha256 = plan, checker_sha256 = staged sources',
                       d.get('certificate_sha256') == want_inputs['certificate'] and d.get('classes_sha256') == want_inputs['classes'] and d.get('checker_sha256') == WANT_CHECKER[role])
            rows = [r for c in selected for r in json.loads(c['files'][role][1].decode('utf-8'))['rows']]
            names = [k['name'] for k in d['classes']]
            g &= check(tag + ' receipt: minima and cell counts = those recomputed from the %d selected rows' % len(rows),
                       len(rows) == TOTAL and exact(d.get('unrestricted_minimum_units'), min(r['minimum_units'] for r in rows)) and d.get('deficit_minimum_units') is None
                       and same(d.get('cells_default'), join([r['default'] for r in rows]))
                       and same(d.get('cells_by_class'), [dict(name=n, **join([r['classes'][i] for r in rows])) for i, n in enumerate(names)]))
            failed_row |= d.get('status') == 'CLASSES_EXACT_COVERAGE_FAILURE'
        bad = [k for k in AGREE if k not in dp or k not in dn or not same(dp[k], dn[k])]
        prov['receipts_compared_on'] = list(AGREE); prov['receipts_differ_in'] = bad
        g &= check('the two receipts agree on status, statement, header, coverage, minima and cell counts', not bad)
    except Exception as e:
        prov['detail'].append('receipts_unreadable:' + type(e).__name__); g = False
if g:
    finish('PASS')
if integrity and failed_row and 2 in (ep['exit_code'], en['exit_code']):
    finish('FAIL')
finish('INCOMPLETE')
DRIVER_EOF
