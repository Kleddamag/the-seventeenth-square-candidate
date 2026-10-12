#!/usr/bin/env python3
"""Seal the stopped propagation and summaries without model or solver import."""
import hashlib
import json
import time
from pathlib import Path
start=time.process_time();here=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((here/'propagation-receipt.json').read_text())
assert r['status']=='THREE_ROUNDS_INCONCLUSIVE'
assert r['LP_calls']==276 and len(r['rounds'])==3
assert r['remaining_norm_faces']==[{'coordinate':44,'sign':-1}]
chain=json.loads((here/'stopped-chain.json').read_text())
for round_ in chain['rounds']:
    assert sha(here/round_['path'])==round_['sha256']
files=[]
for p in sorted(here.rglob('*')):
    if p.is_file() and p.name!='PRODUCER_MANIFEST.json' and '__pycache__' not in p.parts:
        files.append({'path':str(p.relative_to(here)),'sha256':sha(p)})
m={'status':'THREE_STOPPED_ROUNDS_INCONCLUSIVE_REQUIRES_SEPARATE_INDEPENDENT_REVIEW',
   'scope':'Valid proposed exact normalized enclosures; final core ratio1, sole face x44=-1, other44 rho=235021159590017/500000000000000; not rigidity.',
   'files':files,'LP_calls':276,'rounds':3,'calculation_exit_code':0,
   'unchanged_old_rigidity_check_called':False,
   'accepted_dependencies':{
     'full_gate_review':'a70b064bb81a55fca7f5ad9a9b19ea765c613877d8b243e041081760b9dc53dd',
     'B6_review':'b38fb735a1d3bdd84c662a68b37d7d10e806af71abf82b54c320424da79d1ad1',
     'stop_review':'e8af5453f7e97d18ee2dab652644d797218ce2382fb928b53a8cb151cee7645d'},
   'producer_CPU_cap_seconds':60,'producer_charged_CPU_seconds':5,
   'preparation_CPU_seconds':json.loads((here/'preparation.json').read_text())['CPU_seconds'],
   'calculation_CPU_seconds':r['CPU_seconds'],'seal_CPU_seconds':time.process_time()-start,
   'one_native_thread':True,'process_CPU_soft_hard':[56,59],
   'further_producer_calculation_planned':False}
(here/'PRODUCER_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({'manifest_sha256':sha(here/'PRODUCER_MANIFEST.json'),'seal_CPU_seconds':m['seal_CPU_seconds']}))
