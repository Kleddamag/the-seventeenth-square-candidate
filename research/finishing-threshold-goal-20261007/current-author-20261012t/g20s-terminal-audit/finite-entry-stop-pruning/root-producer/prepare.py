#!/usr/bin/env python3
"""Freeze exact source dependencies for larger-radius physical stop guards."""
import hashlib,json,shutil,time
from pathlib import Path
START=time.process_time()
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'local-research/claude-20261002/results/rerun_trees_20261011/SHA256_G20S_HW.txt').exists())
G=HERE.parents[1]
OLD=G/'stop-coupled-finish/stop-producer'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(OLD/'manifest.json')=='ebcb669d46ea8230bf840c98ff7fb7b0d6980bcce1ea11315a9b9508b9a7c03d'
deps=json.loads((OLD/'dependencies.json').read_text())['files'].copy()
extra={
 G/'stop-coupled-finish/stop-review/manifest.json':'e8af5453f7e97d18ee2dab652644d797218ce2382fb928b53a8cb151cee7645d',
 G/'stop-coupled-finish/stop-review/REVIEW.md':'7623f5b2290f22c49be71ee5ebeebc218d313b565de829a3829b4e67ac30e169',
 OLD/'manifest.json':'ebcb669d46ea8230bf840c98ff7fb7b0d6980bcce1ea11315a9b9508b9a7c03d',
}
# The accepted old manifest binds its checker; extract the exact digest from it.
oldmanifest=json.loads((OLD/'manifest.json').read_text())
items=oldmanifest['files']
if isinstance(items,dict): oldcheck=items['check_stops.py']; oldcheck=oldcheck['sha256'] if isinstance(oldcheck,dict) else oldcheck
else: oldcheck=next(item['sha256'] for item in items if item['path']=='check_stops.py')
extra[OLD/'check_stops.py']=oldcheck
for source,digest in extra.items():deps[str(source.relative_to(ROOT))]=digest
for name,digest in deps.items():
 source=ROOT/name
 assert sha(source)==digest
 target=HERE/'inputs'/name;target.parent.mkdir(parents=True,exist_ok=True)
 shutil.copyfile(source,target)
 assert sha(target)==digest
data={'status':'FROZEN_DEPENDENCIES_FOR_RADIUS_501_OVER_100000_STOP_GUARDS',
      'inherited_small_gate_radius':'1/5000',
      'inherited_scope':'Exact reference identities, root enclosure, slider conventions, previous proof structure only; all new-radius guards recomputed.',
      'files':deps,'process_CPU_seconds':time.process_time(),'preparation_CPU_seconds':time.process_time()-START}
(HERE/'dependencies.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'copied_dependencies':len(deps),'process_CPU_seconds':time.process_time()}))
