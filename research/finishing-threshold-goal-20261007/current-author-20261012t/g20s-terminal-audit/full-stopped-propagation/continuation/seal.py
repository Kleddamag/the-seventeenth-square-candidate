#!/usr/bin/env python3
"""Freeze the successful continuation without model or solver import."""
import hashlib
import json
import time
from fractions import Fraction as F
from pathlib import Path
start=time.process_time();here=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((here/'propagation-receipt.json').read_text())
assert r['status']=='STRICT_CONTRACTION_REQUIRES_SEPARATE_INDEPENDENT_EXACT_REVIEW'
assert r['LP_calls']==184 and [x['round'] for x in r['rounds']]==[4,5]
assert F(r['final_core_ratio'])==F(159201934153319,200000000000000)<1
chain=json.loads((here/'stopped-chain.json').read_text())
for item in chain['rounds']:assert sha(here/item['path'])==item['sha256']
files=[]
for p in sorted(here.rglob('*')):
    if p.is_file() and p.name!='PRODUCER_MANIFEST.json' and '__pycache__' not in p.parts:
        files.append({'path':str(p.relative_to(here)),'sha256':sha(p)})
m={'status':'STRICT_STOPPED_CONTRACTION_REQUIRES_SEPARATE_INDEPENDENT_REVIEW',
   'scope':'Small exact-root rigidity on full padded G20S domain, conditional on combined exact replay and physical join; no finite-entry/capture theorem.',
   'files':files,'LP_calls':184,'rounds':[4,5],'calculation_exit_code':0,
   'combined_stopped_rounds':5,'combined_LP_calls':460,
   'exact_core_ratio':r['final_core_ratio'],'old_rigidity_check_called':False,
   'prefix_manifest_sha256':'a756cea10c4cbc60dd686bb7bc9c10ed83ae4853122f91e77803f3e0a7b58a2a',
   'accepted_dependencies':{
     'full_gate_review':'a70b064bb81a55fca7f5ad9a9b19ea765c613877d8b243e041081760b9dc53dd',
     'B6_review':'b38fb735a1d3bdd84c662a68b37d7d10e806af71abf82b54c320424da79d1ad1',
     'stop_review':'e8af5453f7e97d18ee2dab652644d797218ce2382fb928b53a8cb151cee7645d'},
   'shared_original_producer_CPU_cap_seconds':60,
   'prefix_charged_CPU_seconds':5,'continuation_charged_CPU_seconds':4,'combined_charged_CPU_seconds':9,
   'first_preparation_CPU_seconds':0.015031,
   'final_preparation_CPU_seconds':json.loads((here/'preparation.json').read_text())['CPU_seconds'],
   'calculation_CPU_seconds':r['CPU_seconds'],'seal_CPU_seconds':time.process_time()-start,
   'process_CPU_soft_hard':[50,53],'one_native_thread':True,
   'further_calculation_planned':False}
(here/'PRODUCER_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({'manifest_sha256':sha(here/'PRODUCER_MANIFEST.json'),'seal_CPU_seconds':m['seal_CPU_seconds']}))
