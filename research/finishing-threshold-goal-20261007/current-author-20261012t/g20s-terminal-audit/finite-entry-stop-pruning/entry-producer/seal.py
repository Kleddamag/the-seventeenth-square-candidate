#!/usr/bin/env python3
"""Seal exact guarded pruning; no model, solver, or transfer rerun."""
import hashlib,json,time
from pathlib import Path
start=time.process_time();here=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((here/'export-receipt.json').read_text())
assert r['root_review_sha256']=='907071a795d42b92890da0a1894b3a9765635908caf2812044ade6d65d76056e'
assert sha(here/'PRUNING.json')==r['export_sha256']
files=[]
for p in sorted(here.rglob('*')):
    if p.is_file() and p.name!='PRODUCER_MANIFEST.json' and '__pycache__' not in p.parts:
        files.append({'path':str(p.relative_to(here)),'sha256':sha(p)})
m={'status':'EXACT_RAW_PRUNING_PASS_REQUIRES_SEPARATE_INDEPENDENT_ENTRY_REVIEW',
 'files':files,'scope':'Necessary guarded raw cuts on positions1/200/radianangles1/400; no finite contraction or terminal-reach claim.',
 'accepted_root_stop_review_sha256':r['root_review_sha256'],
 'pruning_export_sha256':r['export_sha256'],
 'raw_reference_review_sha256':'5a70b980bdf8c519d1bcb19a6f710737e41073e782286f849e9ac62915f3b3cc',
 'producer_CPU_cap_seconds':10,'producer_conservative_CPU_charge_seconds':3,
 'preparation_CPU_seconds':.004026,'first_transfer_CPU_seconds':.022188,
 'final_transfer_CPU_seconds':json.loads((here/'transfer-receipt.json').read_text())['CPU_seconds'],
 'export_CPU_seconds':r['CPU_seconds'],'seal_CPU_seconds':time.process_time()-start,
 'model_optimizer_symbolic_tree_calls':0,'physical_parent_count':17,'free_physical_label':4,
 'actual_side_premise':'S<=algebraic S*','WX_schema_acceptance_claimed':False,
 'further_calculation_planned':False}
(here/'PRODUCER_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({'manifest_sha256':sha(here/'PRODUCER_MANIFEST.json'),'seal_CPU_seconds':m['seal_CPU_seconds']}))
