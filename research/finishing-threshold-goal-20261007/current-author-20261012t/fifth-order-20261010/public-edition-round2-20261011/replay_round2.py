"""Run a named cheap check, preserving original bytes and redirecting receipt writes.

Not a sandbox for hostile code. The audit hook catches accidental mutation, process
launch and network use; this is intended only for the reviewed local checkers.
Run without -O. Each invocation is a separate process; never run these in parallel.
"""
import builtins, contextlib, io, json, os, pathlib, runpy, signal, sys, time, traceback, hashlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
REPO_MARKER = '/' + ROOT.name + '/'
if not __debug__:
    raise RuntimeError('Assertions are required; do not use -O or -OO.')
cfg = json.loads((HERE / 'runbook_public.json').read_text())
key = sys.argv[1]
row = next(x for x in cfg['checks'] if x['id'] == key)
destination = HERE / 'public_runs' / key
n = 1
while destination.exists():
    n += 1
    destination = HERE / 'public_runs' / (key + '-%02d' % n)
destination.mkdir(parents=True)
real_open, real_io_open, real_mkdir = builtins.open, io.open, os.mkdir
outputs, reads = {}, set()

def translated(file):
    if isinstance(file, int): return file
    s = os.fsdecode(file)
    if s.startswith('/') and REPO_MARKER in s:
        s = str(ROOT / s.split(REPO_MARKER, 1)[1])
    # The single case alias corrected by BI. Preserve original bytes.
    s = s.replace('finite-entry-stop-pruning/root-review/MANIFEST.json',
                  'finite-entry-stop-pruning/root-review/manifest.json')
    # Pure editorial path relocation; check-script bytes and mathematics are unchanged.
    legacy = str(HERE / 'revision-v4' / 'PROOF.md')
    if os.path.abspath(s) == legacy:
        s = str(HERE / 'revision-v7' / 'PROOF.md')
    return os.path.abspath(s)

def redirect(file, mode):
    p = translated(file)
    if isinstance(p, int): return p
    if any(c in str(mode) for c in 'wax+'):
        source = pathlib.Path(p)
        if not source.is_relative_to(ROOT):
            raise PermissionError('Check attempted an external write: ' + p)
        if source.is_relative_to(destination): return p
        target = destination / 'outputs' / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        outputs[p] = str(target)
        return str(target)
    return outputs.get(p, p)

def opening(original):
    def call(file, mode='r', *a, **kw):
        target = redirect(file, mode)
        # Python 3.9 pathlib supplies an opener bound to the original Path.
        # Use the redirected filename, not that bound original-path opener.
        if kw.get('opener') is not None:
            kw.pop('opener')
        return original(target, mode, *a, **kw)
    return call

def audit(event, args):
    if event == 'open':
        path, mode, flags = args
        if isinstance(path, int): return
        p = os.path.abspath(os.fsdecode(path))
        if p.endswith('.pyc'):
            raise FileNotFoundError('Replay uses source bytes, not cached bytecode')
        writing = (flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)) != 0
        if writing and not pathlib.Path(p).is_relative_to(destination):
            raise PermissionError('Unredirected write: ' + p)
        if not writing and pathlib.Path(p).is_relative_to(ROOT):
            rp=str(pathlib.Path(p).relative_to(ROOT));name=pathlib.Path(p).name
            forbidden=any(s in rp for s in ('frozen-final-original-','final-read-supplement-','final-read-errata-','package-runbook-BJ-','/sources/'))
            forbidden=forbidden or name in ('FOR_CODEX.md','STATUS.md','HANDOVER.md','worker.sh','run.sh','cvjob.sh','mkv.sh','job.txt','DONE') or name.startswith('CLAUDE_REPLY_')
            forbidden=forbidden or (name=='AGENTS.md' and rp!='AGENTS.md')
            if forbidden: raise PermissionError('Excluded public input: '+rp)
            reads.add(p)
    elif event in ('os.remove', 'os.rename', 'os.rmdir', 'os.link', 'os.symlink', 'os.chmod', 'os.truncate'):
        raise PermissionError('Mutation denied: ' + event)
    elif event == 'os.mkdir':
        if not pathlib.Path(os.path.abspath(os.fsdecode(args[0]))).is_relative_to(destination):
            raise PermissionError('mkdir outside replay outputs')
    elif event.startswith(('subprocess.', 'socket.')) or event in ('os.system', 'os.fork', 'os.posix_spawn'):
        raise PermissionError('No subprocess or network in cheap replay: ' + event)

builtins.open = opening(real_open)
io.open = opening(real_io_open)
sys.dont_write_bytecode = True
sys.addaudithook(audit)
signal.signal(signal.SIGALRM, lambda *a: (_ for _ in ()).throw(TimeoutError('570-second wall limit')))
signal.alarm(570)
script = ROOT / row['script']
assert hashlib.sha256(script.read_bytes()).hexdigest()==row['script_sha256'], 'Runbook script pin mismatch'
sys.path.insert(0, str(script.parent))
sys.argv = [str(script)] + row.get('args', [])
start, cpu = time.monotonic(), time.process_time()
captured = io.StringIO()
error = None
try:
    with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
        runpy.run_path(str(script), run_name='__main__', init_globals={'_S17_PUBLIC_RUNNER_ACTIVE': True})
except BaseException as e:
    error = repr(e)
    traceback.print_exc(file=captured)
signal.alarm(0)
out = captured.getvalue()
missing = [s for s in row.get('required_output', []) if s not in out]
passed = error is None and not missing
receipt = {'id': key, 'status': 'PASS' if passed else 'FAIL', 'error': error,
           'missing_required_output': missing, 'wall_seconds': time.monotonic()-start,
           'cpu_seconds': time.process_time()-cpu, 'python': sys.version,
           'executable': pathlib.Path(sys.executable).name,'script_sha256': row['script_sha256'], 'original_last_line': out.rstrip().split('\n')[-1],
           'inputs_read': sorted(str(pathlib.Path(p).relative_to(ROOT)) for p in reads
                                 if not pathlib.Path(p).is_relative_to(destination)),
           'redirected_outputs': {str(pathlib.Path(p).relative_to(ROOT)): str(pathlib.Path(v).relative_to(ROOT))
                                  for p,v in outputs.items()},
           'path_adaptations': ['author repository prefix', 'BI manifest.json case alias', 'round2: revision-v4/PROOF.md reads revision-v7/PROOF.md'],
           'scope': 'New execution of the named check only, not a new independent mathematical review.'}
with real_open(destination/'stdout.txt','w') as f: f.write(out)
with real_open(destination/'receipt.json','w') as f: json.dump(receipt,f,indent=2); f.write('\n')
print(json.dumps({k:receipt[k] for k in ('id','status','wall_seconds','cpu_seconds','error','missing_required_output')}))
print('PUBLIC CHECK ' + key + ': ' + receipt['status'])
sys.exit(0 if passed else 1)
