#!/usr/bin/env python3
"""Freeze accepted B5 and exact source for one seven-objective round."""
import hashlib
import json
import time
from pathlib import Path
t0=time.process_time()
HERE=Path(__file__).resolve().parent
G=HERE.parents[1]
W=HERE.parents[2]
P=G/'normalized-dual-reuse/producer'
R=G/'normalized-dual-reuse/independent-review'
F=G/'full-gate/independent-review'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(R/'MANIFEST.json')=='7d9db75869c3bc781ca3a08e892dd12d4c3e5f5140fae3f0577ff32ddee2a901'
assert sha(R/'SEVEN_FACE_REVIEW_MANIFEST.json')=='d98a4956589f65ff6fab859e12d9aeda6db27d04b1037625423f82863f633a60'
assert sha(F/'MANIFEST.json')=='a70b064bb81a55fca7f5ad9a9b19ea765c613877d8b243e041081760b9dc53dd'
pm=json.loads((P/'PRODUCER_MANIFEST.json').read_text())
sources=[]
for src in sorted((P/'instance').rglob('*')):
    if not src.is_file():continue
    rel=str(src.relative_to(P))
    assert sha(src)==pm['files_sha256'][rel]
    dst=HERE/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(src.read_bytes())
    sources.append({'path':rel,'sha256':sha(dst)})
inputs=HERE/'inputs';inputs.mkdir(exist_ok=True)
paths={
 'accepted-prefix.json':P/'reuse-candidate.json',
 'accepted-prefix-producer-manifest.json':P/'PRODUCER_MANIFEST.json',
 'accepted-prefix-review-manifest.json':R/'MANIFEST.json',
 'accepted-prefix-review-receipt.json':R/'receipt.json',
 'seven-face-review-manifest.json':R/'SEVEN_FACE_REVIEW_MANIFEST.json',
 'seven-face-review.md':R/'SEVEN_FACE_REVIEW.md',
 'full-gate-review-manifest.json':F/'MANIFEST.json',
 'full-gate-receipt.json':P/'inputs/full-gate-receipt.json',
 'accepted-root-gate.json':P/'inputs/accepted-root-gate.json',
}
for name,src in paths.items():(inputs/name).write_bytes(src.read_bytes())
assert sha(inputs/'accepted-prefix.json')==pm['files_sha256']['reuse-candidate.json']
out={'status':'PREPARED_ONE_GLOBAL_B5_SEVEN_OBJECTIVE_ROUND','sources':sources,
 'inputs':{name:sha(inputs/name) for name in paths},'cpu_seconds':time.process_time()-t0,
 'target_objectives':[[8,-1],[14,1],[15,1],[41,1],[41,-1],[44,1],[49,1]],
 'maximum_lp_proposals':7,'producer_cpu_cap_seconds':30,'no_face_intersections':True}
(HERE/'preparation.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'cpu_seconds':out['cpu_seconds']}))
