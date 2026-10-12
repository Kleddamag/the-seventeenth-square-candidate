#!/usr/bin/env python3
"""Pin existing reference geometry; no model or solver is evaluated."""
import hashlib,json,shutil,time
from pathlib import Path
start=time.process_time();here=Path(__file__).resolve().parent;G=here.parents[1]
src=G/'full-stopped-propagation/continuation'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(src/'PRODUCER_MANIFEST.json')=='685d4d96672a5522cd44f85653907a441bf81b49ce43625f59cacc6d71870de1'
prep=json.loads((src/'preparation.json').read_text());files=[]
for v in prep['sources']:
    p=src/v['path'];assert sha(p)==v['sha256']
    out=here/v['path'];out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,out)
    files.append({'path':v['path'],'sha256':sha(out)})
extras={
 'inputs/accepted-root-gate.json':src/'inputs/accepted-root-gate.json',
 'inputs/raw-reference-interface.json':G/'full-stopped-propagation/rational-entry-review/MATHEMATICAL_INTERFACE.json',
 'inputs/raw-reference-review.json':G/'full-stopped-propagation/rational-entry-review/MANIFEST.json',
 'inputs/accepted-transfer-review.json':G/'independent-review/MANIFEST.json',
}
assert sha(extras['inputs/raw-reference-review.json'])=='5a70b980bdf8c519d1bcb19a6f710737e41073e782286f849e9ac62915f3b3cc'
assert sha(extras['inputs/accepted-transfer-review.json'])=='ab96060dce2f0e5b17006b52a9a8c0d7b70f6a94897c9dd0f013d9911cfbdd12'
for name,p in extras.items():
    out=here/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,out)
    files.append({'path':name,'sha256':sha(out)})
record={'status':'PREPARED_REFERENCE_DATA_ONLY','files':files,
 'raw_position_radius':'1/200','raw_angle_radius':'1/400','root_epsilon':'501/100000',
 'raw_slider_box':{'2':['0','8/25'],'21':['-1/20','1/5'],'25':['-1/5','3/40']},
 'CPU_seconds':time.process_time()-start}
(here/'preparation.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':record['status'],'CPU_seconds':record['CPU_seconds']}))
