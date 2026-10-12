#!/usr/bin/env python3
"""Pin the source-only G20S assessment and exact tiny-check dependencies."""
import hashlib
import json
import time
from pathlib import Path

t0=time.process_time()
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'local-research/claude-20261002/results/rerun_trees_20261011/SHA256_G20S_HW.txt').is_file())
W=HERE.parents[1]
OLD=W/'claude-extension-audit/terminal-producer'
SNAP=OLD/'snapshot'
WX=W/'coarse-capture/new-leaf-import/hplus015-import/inputs'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs=HERE/'inputs'
inputs.mkdir(exist_ok=True)
documents={'TERMINAL_NOTES.md': ROOT / 'research/window-extension-20261008/terminal/TERMINAL_NOTES.md', 'G20S_PLAN.md': ROOT / 'research/window-extension-20261008/bigbox/G20S_PLAN.md'}
for name,p in documents.items():
    (inputs/name).write_bytes(p.read_bytes())
target=json.loads((SNAP/'INTERFACE-tube.json').read_text())
target['status']='PROPOSED_G20S_TERMINAL_NOT_PROVED'
target['box']={k:['-1/200','1/200'] for k in target['box']}
target['box'].update({'2,1':['-8/25','0'],'11,2':['-1/5','1/20'],'13,2':['-1/5','3/40']})
target['alpha']={k:'1/400' for k in target['alpha']}
target['note']='One common frame and injective16-label assignment; square4 has no pose hypothesis. A tree may allow xi2,1<=r only with the actual S<=S* wall repair. No scalar lower bound required.'
target['conclusion_if_new_chain_passes']='S=S* and45exact-root core deviations vanish; no original17-family slider-range claim.'
(HERE/'TARGET.json').write_text(json.dumps(target,indent=2)+'\n')
sources=[OLD/'MANIFEST.json',OLD/'ANALYTIC_AUDIT.md',OLD/'gate-receipt.json',OLD/'RESULT.md',
 SNAP/'upper-packing-certificate.json',SNAP/'INTERFACE-tube.json',
 SNAP/'research/joint-capture-20261007/pilot.py',WX/'SPEC.md',WX/'wxcheck_v251.py',WX/'wxcheck2_v251.js']
sources += [SNAP/'research/uniform-capture-20261007'/s for s in
 ('uniform.py','bridge.py','rigidity.py','relational.py','root_geometry.py','verify.py','upstream-root-certificate.json')]
old_manifest=json.loads((OLD/'MANIFEST.json').read_text())
for p in sources:
    if p.is_relative_to(OLD) and p!=OLD/'MANIFEST.json':
        rel=str(p.relative_to(OLD))
        assert old_manifest['files_sha256'][rel]==sha(p), rel
manifest={'status': 'SOURCE_AND_CONSTANT_ASSESSMENT_ONLY_REQUIRES_SEPARATE_INDEPENDENT_REVIEW', 'producer': 'Codex contributor 06', 'target_a_upper': '8/25', 'superseded_target_a_upper': '39/125', 'no_solver_or_new_model_or_certificate_replay': True, 'source_files_sha256': {str(p.relative_to(ROOT)): sha(p) for p in sources}, 'document_snapshots': {name: {'source': str(p.relative_to(ROOT)), 'sha256': sha(inputs / name)} for (name, p) in documents.items()}, 'cpu_seconds_tiny_checks': sum((json.loads((HERE / f).read_text())['cpu_seconds'] for f in ('constants-v1.json', 'constants.json'))), 'producer_cpu_charged_seconds': 2, 'files_sha256': {}, 'freeze_cpu_seconds': time.process_time() - t0}
manifest['files_sha256']={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='PRODUCER_MANIFEST.json'}
(HERE/'PRODUCER_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'manifest_sha256':sha(HERE/'PRODUCER_MANIFEST.json'),'freeze_cpu_seconds':time.process_time()-t0,'tiny_checks_cpu_seconds':manifest['cpu_seconds_tiny_checks']}))
