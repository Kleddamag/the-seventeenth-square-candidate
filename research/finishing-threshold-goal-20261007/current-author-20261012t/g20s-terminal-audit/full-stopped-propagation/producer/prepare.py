#!/usr/bin/env python3
"""Prepare the fixed global stopped-domain experiment without computation."""
import hashlib
import json
import shutil
import time
from pathlib import Path
start=time.process_time();here=Path(__file__).resolve().parent
src=here.parents[1]/'four-cell-slider-cover/producer'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(src/'PRODUCER_MANIFEST.json')=='286f332c768d9985300cce48487b20bbaeb35f707b6336bad7b467eb6b80e7cd'
manifest=json.loads((src/'PRODUCER_MANIFEST.json').read_text())
pins={r['path']:r['sha256'] for r in manifest['files']}
for name in sorted(pins):
    if name.startswith(('instance/','inputs/')) or name=='stop-review-binding.json':
        assert sha(src/name)==pins[name]
        out=here/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src/name,out)
prep=json.loads((src/'preparation.json').read_text())
assert sha(here/'inputs/accepted-targeted-review-manifest.json')=='b38fb735a1d3bdd84c662a68b37d7d10e806af71abf82b54c320424da79d1ad1'
assert sha(here/'inputs/full-gate-review-manifest.json')=='a70b064bb81a55fca7f5ad9a9b19ea765c613877d8b243e041081760b9dc53dd'
assert sha(here/'inputs/stop-review/manifest.json')=='e8af5453f7e97d18ee2dab652644d797218ce2382fb928b53a8cb151cee7645d'
plan={
 'status':'PREPARED_GLOBAL_STOPPED_PROPAGATION',
 'sources':prep['sources'],'inputs':prep['inputs'],
 'stop_review_binding_sha256':sha(here/'stop-review-binding.json'),
 'base':'Accepted global B6; all incoming core/side/a bounds retained',
 'epsilon':'1/5000','physical_cuts':{'b_lower':'-17/50000','z_upper':'1/40','b_plus_z_upper':'3/125'},
 'model':'52 geometric rows +192 product rows +1 physical stop row',
 'maximum_rounds':3,'objectives_per_round':92,'maximum_LP_calls':276,
 'updates':'simultaneous intersection, exact outward rounding, refreshed product hulls',
 'no_subdivision':True,'no_fixed_norm_face':True,'no_new_contact_rows':True,
 'unchanged_rigidity_checker_not_applicable':True,
 'producer_CPU_cap_seconds':60,'native_threads':1,
 'CPU_seconds':time.process_time()-start}
(here/'preparation.json').write_text(json.dumps(plan,indent=2)+'\n')
print(json.dumps({'status':plan['status'],'CPU_seconds':plan['CPU_seconds']}))
