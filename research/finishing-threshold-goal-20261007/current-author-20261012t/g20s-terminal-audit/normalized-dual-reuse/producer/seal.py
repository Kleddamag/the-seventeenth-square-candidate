#!/usr/bin/env python3
"""Seal the G20S old-weight reuse failure without claiming contraction."""
import hashlib
import json
import time
from pathlib import Path
t0=time.process_time()
HERE=Path(__file__).resolve().parent
G=HERE.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
review=G/'full-gate/independent-review/MANIFEST.json'
assert sha(review)=='a70b064bb81a55fca7f5ad9a9b19ea765c613877d8b243e041081760b9dc53dd'
(HERE/'inputs/full-gate-review-manifest.json').write_bytes(review.read_bytes())
r=json.loads((HERE/'reuse-receipt.json').read_text())
assert r['status']=='OLD_WEIGHTS_INCONCLUSIVE_NO_STRICT_CONTRACTION'
assert len(r['rounds'])==5 and all(x['ratio']=='1' for x in r['rounds'])
candidate=json.loads((HERE/'reuse-candidate.json').read_text())
assert len(candidate['steps'])==5 and all(len(x['results'])==92 for x in candidate['steps'])
manifest={'status': 'OLD_WEIGHTS_INCONCLUSIVE_REQUIRES_SEPARATE_INDEPENDENT_NEGATIVE_RESULT_REVIEW', 'producer': 'Codex contributor 06', 'rounds': 5, 'exact_objectives': 460, 'final_ratio': '1', 'old_certificate_sha256': r['old_certificate_sha256'], 'no_new_weights_solver_finite_certificate_or_tree': True, 'unchanged_rigidity_checker_run': False, 'accepted_full_gate_review_sha256': sha(review), 'cpu_seconds_preparation': json.loads((HERE / 'preparation.json').read_text())['cpu_seconds'], 'cpu_seconds_reuse': r['cpu_seconds'], 'producer_cpu_charged_seconds': 4, 'not_implied': ['counterexample', 'failure of fresh normalized contraction', 'new terminal theorem', 'capture', 'optimality'], 'files_sha256': {str(p.relative_to(HERE)): sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name != 'PRODUCER_MANIFEST.json'}, 'seal_cpu_seconds': time.process_time() - t0}
(HERE/'PRODUCER_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'manifest_sha256':sha(HERE/'PRODUCER_MANIFEST.json'),'reuse_cpu_seconds':r['cpu_seconds'],'seal_cpu_seconds':time.process_time()-t0}))
