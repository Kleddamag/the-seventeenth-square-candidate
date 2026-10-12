#!/usr/bin/env python3
"""Prepare isolated sources and old weights for bounded G20S reuse only."""
import hashlib
import json
import shutil
import time
from pathlib import Path
t0=time.process_time()
HERE=Path(__file__).resolve().parent
G=HERE.parents[1]
W=HERE.parents[2]
FULL=G/'full-gate/producer'
OLD=W/'claude-extension-audit/terminal-producer'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
fm=json.loads((FULL/'PRODUCER_MANIFEST.json').read_text())
om=json.loads((OLD/'MANIFEST.json').read_text())
sources=[]
for p in sorted((FULL/'instance').rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(FULL)
    assert sha(p)==fm['files_sha256'][str(rel)]
    dest=HERE/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes())
    sources.append({'relative_path':str(rel),'sha256':sha(dest)})
inputs=HERE/'inputs';inputs.mkdir(exist_ok=True)
paths={
 'old-uniform-rigidity.json':OLD/'snapshot/research/uniform-capture-20261007/uniform-rigidity.json',
 'accepted-old-terminal-manifest.json':OLD/'MANIFEST.json',
 'accepted-root-gate.json':OLD/'gate-receipt.json',
 'full-gate-producer-manifest.json':FULL/'PRODUCER_MANIFEST.json',
 'full-gate-receipt.json':FULL/'gate-receipt.json',
 'full-gate-result.md':FULL/'RESULT.md',
}
for name,p in paths.items():
    if p.is_relative_to(OLD) and p!=OLD/'MANIFEST.json':
        assert sha(p)==om['files_sha256'][str(p.relative_to(OLD))]
    (inputs/name).write_bytes(p.read_bytes())
old=json.loads((inputs/'old-uniform-rigidity.json').read_text())
assert old['schema']=='s17-uniform-rigidity-v1' and old['epsilon']=='1/5000'
assert len(old['steps'])==5 and all(len(x['results'])==92 for x in old['steps'])
out={'status':'PREPARED_WEIGHTS_ONLY_REUSE','old_steps':5,'old_objectives_per_step':92,
 'sources':sources,'inputs':{name:sha(inputs/name) for name in paths},
 'source_directory':str(FULL/'instance'),'cpu_seconds':time.process_time()-t0,
 'no_models_or_solver_run':True}
(HERE/'preparation.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'cpu_seconds':out['cpu_seconds']}))
