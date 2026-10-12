#!/bin/bash
# slice_run.sh: one slice attempt of the exact check of one capture statement, with a neutral provenance record.
#
#   slice_run.sh NAME slice STATEMENT_ID START END          example:  slice_run.sh Q_11-00-a1 slice Q_11 0 1500
#
# NAME must be  <STATEMENT_ID>-<SLICE_ID>-<ATTEMPT_ID>:  SLICE_ID is the two-digit number of the planned slice
# [START, END) in PLAN_MANIFEST.json, ATTEMPT_ID is a1, a2, ...  A retry is a new attempt with the next attempt id.
# The result directory of an attempt is created by this script, by one exclusive mkdir, before anything is written:
# if a directory (or anything else) of that name exists, complete, incomplete or empty, the script writes nothing
# and ends with exit code 94.  Of two invocations with the same NAME at most one gets past this point.
# Everything it needs lies beside it (this directory is called the capture directory):
#   SOURCE_MANIFEST.json   roles -> files, sha256, bytes (the five Python files, the Node checker, this wrapper,
#                          the comparator)
#   PLAN_MANIFEST.json     run id; per statement: rows, input sha256, checker, planned slices
#   src/                   exact_classes.py exact_restricted.py exact_general.py integer_sweep.py boolean_rule.py
#                          node/verify_classes_wb.js
#   slice_compare.py       the output comparator
#   inputs/<STATEMENT_ID>/certificate.json, classes.json
# It stages inputs and sources into a fresh run root (read-only copies), measures their sha256 before and after, runs
#   python -B src/exact_classes.py inputs/certificate.json --classes inputs/classes.json --start S --count N --workers W --output out/py.json
#   node src/node/verify_classes_wb.js inputs/certificate.json --classes inputs/classes.json --start S --count N --workers W --output out/node.json
#   python -B src/slice_compare.py out/py.json out/node.json S E <certificate sha256> <classes sha256> <python exit> <refused> <node exit> <node state> out/compare.json
# with the run root as working directory (PYTHONOPTIMIZE unset), and writes into  <parent of the capture directory>/results/NAME/
#   py.json  node.json  compare.json     the three outputs, unmodified
#   provenance.json                      schema s17-neutral-slice-provenance-v1, written last, atomically
#   DONE, diag/                          a one-line end marker and the console logs: diagnostics, not part of the record
# Both checkers are mandatory.  No Node executable, a time limit, a crash, a changed input or source: INCOMPLETE.
# Verdict PASS only if all three processes ran and exited 0, inputs and sources are those of the manifests before and
# after, and the outputs are for these inputs, these sources and exactly these rows and agree.
# Exit code: 0 PASS, 2 FAIL, 3 INCOMPLETE, 91 bad arguments, 94 the attempt directory exists already (nothing written),
# 1 the driver part ended on an error it did not foresee (no record is written; the attempt name stays used).
# A range that is no planned slice of the plan is refused before any checker starts (INCOMPLETE).
# Variables read by this script:
#   SLICE_PYTHON  interpreter that has numpy and numba: runs the Python checker, the comparator and one version
#                 question (default: python3 as found on PATH)
#   SLICE_NODE    node executable (default: node or nodejs on PATH, else the last match in a list of usual places,
#                 some of them under HOME)
#   SLICE_PROCESSES, SLICE_NODE_PROCESSES   value of --workers for the two checkers (default 4)
#   SLICE_TIMEOUT, SLICE_NODE_TIMEOUT       seconds (default 10800)
#   SLICE_OUT     parent of the result directory (default: results beside the capture directory)
#   SLICE_TMP     parent of the run root (default: the system's temporary directory: TMPDIR, TEMP or TMP)
#   PATH (python3, node), HOME (node lookup), TMPDIR / TEMP / TMP (temporary files)
# Programs started: the python3 found on PATH (SLICE_PYTHON if there is none), which reads the driver part of this
# file in isolated mode (neither the current directory nor any PYTHON variable enters its module search); one version
# question to SLICE_PYTHON and one to node; the Python checker; the Node checker; the comparator.  The checkers, the
# comparator and the Python version question inherit the environment of this script with PYTHONOPTIMIZE removed; the
# record lists, by NAME only, the variables set in it that can change how they run (environment_names_set).  The
# Python checker sets defaults for the thread-count variables itself.
# A time limit ends the checker concerned (its whole process group).  If this script itself is ended from outside
# while a checker runs, that checker is NOT ended with it: it runs on until it finishes, no record is written, the
# run root stays, and the attempt name stays used (exit code 94 for the same NAME).
# The wrapper named in the record is the file that was started (hashed before and after); a file whose bytes are not
# those of the manifest's launch wrapper ends INCOMPLETE whatever its name.
# This script sends and fetches nothing.
NAME=$1; MODE=$2; SID=$3; START=$4; END=$5
CAP=$(cd "$(dirname "$0")" && pwd)
ROOT=$(dirname "$CAP")
case "$NAME" in ""|.*|*[!A-Za-z0-9._-]*) echo "usage: slice_run.sh NAME slice STATEMENT_ID START END" >&2; exit 91 ;; esac
[ "$MODE" = slice ] || { echo "slice_run.sh: second word must be slice" >&2; exit 91; }
case "$SID" in ""|.*|*[!A-Za-z0-9._-]*) echo "slice_run.sh: bad statement id" >&2; exit 91 ;; esac
case "$START$END" in ""|*[!0-9]*) echo "slice_run.sh: bad row range" >&2; exit 91 ;; esac
[ -n "$START" ] && [ -n "$END" ] && [ "$START" -lt "$END" ] || { echo "slice_run.sh: bad row range" >&2; exit 91; }
# ---- the attempt directory: its parent may exist, the directory itself must be made here and now
P=${SLICE_OUT:-$ROOT/results}
mkdir -p "$P" || exit 91
R=$P/$NAME
if ! mkdir "$R" 2> /dev/null; then
  echo "slice_run.sh: $NAME exists already; nothing written; a retry needs a new attempt id" >&2; exit 94
fi
mkdir "$R/diag" || exit 91

# ---- a node executable: only looks; installs nothing
find_node() {
  local n g
  if [ -n "${SLICE_NODE:-}" ]; then
    n=$(command -v "$SLICE_NODE" 2> /dev/null) && [ -n "$n" ] && [ -x "$n" ] && { echo "$n"; return 0; }
    return 1
  fi
  n=$(command -v node 2> /dev/null) && [ -n "$n" ] && { echo "$n"; return 0; }
  n=$(command -v nodejs 2> /dev/null) && [ -n "$n" ] && { echo "$n"; return 0; }
  for g in /usr/local/bin/node /usr/bin/node /usr/bin/nodejs /opt/node/bin/node /snap/bin/node \
           "$HOME/.local/bin/node" "$HOME/.volta/bin/node" \
           "$HOME"/.nvm/versions/node/*/bin/node /opt/nvm/versions/node/*/bin/node \
           /usr/local/nvm/versions/node/*/bin/node /usr/local/share/nvm/versions/node/*/bin/node \
           /opt/node*/bin/node /usr/local/lib/nodejs/*/bin/node; do
    [ -f "$g" ] && [ -x "$g" ] && n=$g
  done
  case "$n" in /*) echo "$n"; return 0 ;; esac
  return 1
}
NODE=$(find_node)

# ---- the interpreter for the Python checker and the comparator, and the one that reads the driver below
PY=${SLICE_PYTHON:-python3}
DRV=$(command -v python3 2> /dev/null); [ -n "$DRV" ] || DRV=$PY

exec "$DRV" -I -B - "$CAP/$(basename "$0")" "$CAP" "$R" "$NAME" "$SID" "$START" "$END" "$PY" "${NODE:-}" \
  "${SLICE_PROCESSES:-4}" "${SLICE_NODE_PROCESSES:-4}" "${SLICE_TIMEOUT:-10800}" "${SLICE_NODE_TIMEOUT:-10800}" <<'DRIVER_EOF'
# The driver (Python, standard library only), read from this file by the interpreter started above; it is part of the
# wrapper and of its sha256.
import sys, os, json, hashlib, shutil, subprocess, time, signal, re, datetime, tempfile

(WRAPPER, CAP, RES, NAME, SID, START, END, PY, NODE, WK, NW, PT, NT) = sys.argv[1:14]
START = int(START); END = int(END); N = END - START
def posint(x, default):
    return int(x) if re.fullmatch(r'[1-9][0-9]{0,8}', x or '') else default
WK = posint(WK, 4); NW = min(posint(NW, 4), N); PT = posint(PT, 10800); NT = posint(NT, 10800)
SCHEMA = 's17-neutral-slice-provenance-v1'
PY_ROLES = ('python_checker_main', 'python_checker_restricted', 'python_checker_general', 'python_checker_sweep', 'python_checker_rule')
ALL_ROLES = PY_ROLES + ('node_checker', 'launch_wrapper', 'output_comparator')


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def sha_file(p):
    try:
        with open(p, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None


def atomic(path, text):
    tmp = path + '.tmp'
    with open(tmp, 'w') as f:
        f.write(text); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)


NOT_RUN = dict(started=False, exit_code=None, signal=None, timed_out=False)
prov = dict(schema=SCHEMA, run_id=None, statement_id=SID, slice_id=None, attempt_id=None, planned=None,
            rows=dict(start=START, end_exclusive=END, total_intervals=None),
            source_manifest_sha256=None, plan_manifest_sha256=None,
            input_sha256_before=None, input_sha256_after=None, source_sha256_before=None, source_sha256_after=None,
            invocation=dict(python=None, node=None, compare=None), runtime=None,
            started_utc=utc(), finished_utc=None,
            exits=dict(python=dict(NOT_RUN), node=dict(NOT_RUN), compare=dict(NOT_RUN), wrapper=dict(exit_code=None)),
            outputs=dict(python=None, node=None, compare=None), checks=[], verdict='INCOMPLETE', detail=[],
            environment_names_set=sorted(k for k in os.environ if k != 'PYTHONOPTIMIZE' and re.fullmatch(
                r'PYTHON.*|NUMBA_.*|NODE_.*|.*_NUM_THREADS|LD_PRELOAD|LD_LIBRARY_PATH|DYLD_.*|BASH_ENV|CDPATH', k)))
RUNROOT = None


def finish(verdict):
    code = {'PASS': 0, 'FAIL': 2}.get(verdict, 3)
    prov['verdict'] = verdict; prov['finished_utc'] = utc(); prov['exits']['wrapper']['exit_code'] = code
    atomic(os.path.join(RES, 'provenance.json'), json.dumps(prov, indent=1) + '\n')
    e = prov['exits']
    atomic(os.path.join(RES, 'DONE'), 'exit=%d end=%s verdict=%s statement=%s rows=%d-%d python_exit=%s node_exit=%s compare_exit=%s%s\n'
           % (code, prov['finished_utc'], verdict, SID, START, END, e['python']['exit_code'], e['node']['exit_code'], e['compare']['exit_code'],
              (' detail=' + ','.join(prov['detail'])) if prov['detail'] else ''))
    if RUNROOT:
        for d, _, fs in os.walk(RUNROOT):
            os.chmod(d, 0o700)
        shutil.rmtree(RUNROOT, ignore_errors=True)
    sys.exit(code)


def stop(word):
    prov['detail'].append(word); finish('INCOMPLETE')


def run(role, real, argv, timeout, log):
    """Runs real + argv[1:] in the run root.  Records what happened under exits[role]."""
    ex = prov['exits'][role]
    env = dict(os.environ); env.pop('PYTHONOPTIMIZE', None)
    with open(log, 'wb') as lf:
        try:
            p = subprocess.Popen([real] + argv[1:], cwd=RUNROOT, stdin=subprocess.DEVNULL, stdout=lf, stderr=subprocess.STDOUT, env=env, start_new_session=True)
        except OSError as e:
            prov['detail'].append('%s_not_started:%s' % (role, type(e).__name__)); return
        ex['started'] = True
        try:
            rc = p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            ex['timed_out'] = True
            for sig, grace in ((signal.SIGTERM, 60), (signal.SIGKILL, None)):
                try:
                    os.killpg(p.pid, sig)
                except ProcessLookupError:
                    pass
                try:
                    rc = p.wait(timeout=grace); break
                except subprocess.TimeoutExpired:
                    continue
        if rc < 0:
            ex['signal'] = -rc
        else:
            ex['exit_code'] = rc


def last_line(path):
    try:
        lines = [l for l in open(path, errors='replace').read().splitlines() if l.strip()]
        return lines[-1] if lines else ''
    except OSError:
        return ''


# ---- the manifests and the plan
try:
    sm_raw = open(os.path.join(CAP, 'SOURCE_MANIFEST.json'), 'rb').read(); SM = json.loads(sm_raw)
    pm_raw = open(os.path.join(CAP, 'PLAN_MANIFEST.json'), 'rb').read(); PM = json.loads(pm_raw)
except (OSError, ValueError):
    stop('manifest_unreadable')
prov['source_manifest_sha256'] = hashlib.sha256(sm_raw).hexdigest(); prov['plan_manifest_sha256'] = hashlib.sha256(pm_raw).hexdigest()
prov['run_id'] = PM.get('run_id')
roles = SM.get('roles', {})
if set(roles) != set(ALL_ROLES):
    stop('source_manifest_roles')
st = [s for s in PM.get('statements', []) if s.get('statement_id') == SID]
if len(st) != 1:
    stop('statement_not_in_plan')
st = st[0]; TOTAL = st['total_intervals']; prov['rows']['total_intervals'] = TOTAL
if st.get('checker_variant') != 'wb' or st.get('node_checker_sha256') != roles['node_checker']['sha256']:
    stop('checker_variant_of_plan_is_not_the_manifest_node_checker')
if END > TOTAL:
    stop('range_beyond_the_rows')
planned = [s['slice_id'] for s in st['slices'] if s['start'] == START and s['end_exclusive'] == END]
if len(planned) != 1:
    stop('range_is_no_planned_slice')
prov['slice_id'] = planned[0]; prov['planned'] = True
m = re.fullmatch(re.escape(SID + '-' + prov['slice_id'] + '-') + r'(a[1-9][0-9]{0,2})', NAME)
if not m:
    stop('name_is_not_statement-slice-attempt')
prov['attempt_id'] = m.group(1)

# ---- staging: a fresh run root with read-only copies
base = os.environ.get('SLICE_TMP') or None
if base:
    os.makedirs(base, exist_ok=True)
RUNROOT = tempfile.mkdtemp(prefix='slice_', dir=base)
os.makedirs(os.path.join(RUNROOT, 'out')); os.makedirs(os.path.join(RUNROOT, 'inputs'))
staged = {}          # role -> path of the bytes that are executed
for role in ALL_ROLES:
    rel = roles[role]['file']
    if role == 'launch_wrapper':
        staged[role] = WRAPPER; continue
    dst = os.path.join(RUNROOT, rel if rel.startswith('src/') else 'src/' + rel)
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


def measure():
    return {k: sha_file(p) for k, p in inputs.items()}, {r: sha_file(staged[r]) for r in ALL_ROLES}


prov['input_sha256_before'], prov['source_sha256_before'] = measure()
ib = prov['input_sha256_before']; sb = prov['source_sha256_before']
if ib != dict(certificate=st['certificate_sha256'], classes=st['classes_sha256']):
    stop('staged_inputs_are_not_those_of_the_plan')
if sb != {r: roles[r]['sha256'] for r in ALL_ROLES}:
    stop('staged_sources_are_not_those_of_the_manifest')

# ---- the argv lists (first token = the role's program; paths relative to the run root)
a_py = ['python', '-B', 'src/exact_classes.py', 'inputs/certificate.json', '--classes', 'inputs/classes.json',
        '--start', str(START), '--count', str(N), '--workers', str(WK), '--output', 'out/py.json']
a_node = ['node', 'src/node/verify_classes_wb.js', 'inputs/certificate.json', '--classes', 'inputs/classes.json',
          '--start', str(START), '--count', str(N), '--workers', str(NW), '--output', 'out/node.json']
note = 'argv[0] names the program, its path is not recorded; working directory = run root; PYTHONOPTIMIZE unset'
prov['invocation']['python'] = dict(argv=a_py, workers=WK, timeout_seconds=PT, note=note)
prov['invocation']['node'] = dict(argv=a_node, workers=NW, timeout_seconds=NT, note=note)

# ---- runtime (version questions only; nothing is computed)
rt = dict(python_implementation=None, python_version=None, python_optimization_level=None, numpy_version=None, numba_version=None,
          node_version=None, platform_system=None, platform_architecture=None)
prov['runtime'] = rt
probe = ('import sys, json, platform, numpy, numba; print(json.dumps(dict(python_implementation=platform.python_implementation(), '
         'python_version=platform.python_version(), python_optimization_level=sys.flags.optimize, numpy_version=numpy.__version__, '
         'numba_version=numba.__version__, platform_system=platform.system(), platform_architecture=platform.machine())))')
env0 = dict(os.environ); env0.pop('PYTHONOPTIMIZE', None)
try:
    r = subprocess.run([PY, '-B', '-c', probe], cwd=RUNROOT, stdin=subprocess.DEVNULL, capture_output=True, env=env0, timeout=600)
    rt.update(json.loads(r.stdout.decode().strip().splitlines()[-1]))
except Exception:
    stop('python_with_numpy_and_numba_not_available')
if rt['python_optimization_level'] != 0:
    stop('python_optimization_level_is_not_0')
if not NODE:
    stop('no_node_executable')
try:
    r = subprocess.run([NODE, '--version'], stdin=subprocess.DEVNULL, capture_output=True, timeout=120)
    v = r.stdout.decode().strip().splitlines()[0]
    rt['node_version'] = v if re.fullmatch(r'[A-Za-z0-9._-]{1,40}', v) else None
except Exception:
    pass
if rt['node_version'] is None:
    stop('no_node_executable')

# ---- stage 1 and stage 2
run('python', PY, a_py, PT, os.path.join(RES, 'diag', 'py.log'))
run('node', NODE, a_node, NT, os.path.join(RES, 'diag', 'node.log'))
ep = prov['exits']['python']; en = prov['exits']['node']
have_py = os.path.isfile(os.path.join(RUNROOT, 'out/py.json')) and os.path.getsize(os.path.join(RUNROOT, 'out/py.json')) > 0
have_node = os.path.isfile(os.path.join(RUNROOT, 'out/node.json')) and os.path.getsize(os.path.join(RUNROOT, 'out/node.json')) > 0
py_refused = ep['exit_code'] == 1 and not have_py and last_line(os.path.join(RES, 'diag', 'py.log')).startswith('ValueError: ')
node_refused = en['exit_code'] == 1 and not have_node and any(l.startswith('REFUSED: ') for l in open(os.path.join(RES, 'diag', 'node.log'), errors='replace'))
node_state = 'REFUSED' if node_refused else 'RUN' if (have_node and en['exit_code'] in (0, 2)) else 'INCOMPLETE'
if py_refused: prov['detail'].append('python_refused')
if node_refused: prov['detail'].append('node_refused')

# ---- stage 3: the comparator
a_cmp = ['python', '-B', 'src/slice_compare.py', 'out/py.json', 'out/node.json', str(START), str(END), ib['certificate'], ib['classes'],
         str(ep['exit_code']), 'yes' if py_refused else 'no', str(en['exit_code']), node_state, 'out/compare.json']
prov['invocation']['compare'] = dict(argv=a_cmp, timeout_seconds=1800, note=note)
run('compare', PY, a_cmp, 1800, os.path.join(RES, 'diag', 'compare.log'))
ec = prov['exits']['compare']

# ---- after: the same measurements again, then the outputs
prov['input_sha256_after'], prov['source_sha256_after'] = measure()
for role, name in (('python', 'py.json'), ('node', 'node.json'), ('compare', 'compare.json')):
    src = os.path.join(RUNROOT, 'out', name)
    if os.path.isfile(src) and os.path.getsize(src) > 0:
        dst = os.path.join(RES, name)
        shutil.copyfile(src, dst + '.tmp'); os.replace(dst + '.tmp', dst)
        raw = open(dst, 'rb').read()
        if hashlib.sha256(raw).hexdigest() != sha_file(src):
            os.remove(dst); prov['detail'].append('output_copy_differs:' + role); continue
        prov['outputs'][role] = dict(file=name, sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))

# ---- the verdict, from the exit states and the outputs
checks = prov['checks']


def check(name, ok):
    checks.append(dict(check=name, ok=bool(ok))); return bool(ok)


def exact(x, v):
    """x is the integer v: a JSON integer, neither a float nor true / false."""
    return type(x) is int and x == v


stable = check('inputs: before == after == plan', prov['input_sha256_after'] == ib)
stable &= check('sources: before == after == manifest', prov['source_sha256_after'] == sb)
ran = check('python, node, compare started, exited, no signal, no time limit',
            all(e['started'] and not e['timed_out'] and e['signal'] is None and e['exit_code'] is not None for e in (ep, en, ec)))
zero = check('python, node, compare exit code 0', all(e['exit_code'] == 0 for e in (ep, en, ec)))
outs = check('py.json, node.json, compare.json present', all(prov['outputs'][k] for k in ('python', 'node', 'compare')))
good = False; cmp_fail = False
if outs:
    try:
        dp = json.load(open(os.path.join(RES, 'py.json'))); dn = json.load(open(os.path.join(RES, 'node.json'))); dc = json.load(open(os.path.join(RES, 'compare.json')))
        want_py = {os.path.basename(roles[r]['file']): sb[r] for r in PY_ROLES}
        g = True
        for tag, d, want in (('python', dp, want_py), ('node', dn, {'verify_classes.js': sb['node_checker']})):
            g &= check(tag + ' output: range, total_intervals, input sha256, row sequence',
                       exact(d.get('start'), START) and exact(d.get('end_exclusive'), END) and exact(d.get('total_intervals'), TOTAL)
                       and d.get('certificate_sha256') == ib['certificate'] and d.get('classes_sha256') == ib['classes']
                       and type(d.get('rows')) is list and len(d['rows']) == N
                       and all(type(r) is dict and exact(r.get('interval'), START + i) for i, r in enumerate(d['rows'])))
            g &= check(tag + ' output: checker_sha256 = staged sources', d.get('checker_sha256') == want)
            g &= check(tag + ' output: every row passed, no failed interval',
                       d.get('failed_intervals') == [] and all(r.get('passed') is True for r in d['rows'])
                       and d.get('status') in ('PASS_CLASSES_INTERVAL_PARTITION_ONLY', 'PASS_CLASSES_EXACT_COVER'))
        g &= check('compare.json: python PASS, node PASS, agree yes, all rows compared, none differing',
                   dc.get('python') == 'PASS' and dc.get('node') == 'PASS' and dc.get('agree') == 'yes'
                   and type(dc.get('rows')) is list and len(dc['rows']) == 2 and exact(dc['rows'][0], START) and exact(dc['rows'][1], END)
                   and exact(dc.get('rows_compared'), N) and exact(dc.get('rows_differing'), 0) and dc.get('differences') == [])
        g &= check('compare.json names the two outputs it read',
                   dc.get('python_output_sha256') == prov['outputs']['python']['sha256'] and dc.get('node_output_sha256') == prov['outputs']['node']['sha256'])
        good = g
        cmp_fail = (dc.get('python') == 'FAIL' or dc.get('node') == 'FAIL' or dc.get('agree') == 'no')
    except Exception as e:
        prov['detail'].append('outputs_unreadable:' + type(e).__name__)
elif prov['outputs']['compare']:
    try:
        dc = json.load(open(os.path.join(RES, 'compare.json')))
        cmp_fail = (dc.get('python') == 'FAIL' or dc.get('node') == 'FAIL' or dc.get('agree') == 'no')
    except Exception:
        pass
if stable and ran and zero and outs and good:
    finish('PASS')
if stable and ec['started'] and ec['exit_code'] == 2 and cmp_fail and not any(e['timed_out'] or e['signal'] is not None for e in (ep, en, ec)):
    finish('FAIL')
finish('INCOMPLETE')
DRIVER_EOF
