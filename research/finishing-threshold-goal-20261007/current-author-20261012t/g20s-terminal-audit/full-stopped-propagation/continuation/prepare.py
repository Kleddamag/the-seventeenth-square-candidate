#!/usr/bin/env python3
'Bind the frozen first three rounds and prepare the continuation.'
import difflib
import hashlib
import json
import shutil
import time
from pathlib import Path
start=time.process_time();here=Path(__file__).resolve().parent;src=here.parent/'producer'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
prefix_sha='a756cea10c4cbc60dd686bb7bc9c10ed83ae4853122f91e77803f3e0a7b58a2a'
assert sha(src/'PRODUCER_MANIFEST.json')==prefix_sha
m=json.loads((src/'PRODUCER_MANIFEST.json').read_text())
pins={v['path']:v['sha256'] for v in m['files']}
for name in sorted(pins):
    if name.startswith(('instance/','inputs/')) or name=='stop-review-binding.json':
        assert sha(src/name)==pins[name]
        dest=here/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src/name,dest)
prefix_files=['PRODUCER_MANIFEST.json','stopped-chain.json','propagation-receipt.json','propagate.py','RESULT.md']
prefix_files += [f'round-{i:02d}/{name}' for i in (1,2,3) for name in ('round.json','model.json')]
for name in prefix_files:
    if name!='PRODUCER_MANIFEST.json':assert sha(src/name)==pins[name]
    dest=here/'prefix'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src/name,dest)
old=(src/'propagate.py').read_text();new=old
changes=[
 ('At most three full simultaneous stopped-model rounds, exact residual bounds.',
  'At most twelve additional simultaneous rounds after the frozen three-round prefix.'),
 ('resource.setrlimit(resource.RLIMIT_CPU,(56,59))','resource.setrlimit(resource.RLIMIT_CPU,(50,53))'),
 ("'maximum_LP_calls':276","'maximum_LP_calls':1104"),
 ("for name,digest in prep['inputs'].items():assert sha(HERE/'inputs'/name)==digest", "for name,digest in prep['inputs'].items():assert sha(HERE/'inputs'/name)==digest\n    for item in prep['prefix_files']:assert sha(HERE/item['path'])==item['sha256']"),
 ("bounds=u.refresh_products(bounds)\n    gate=", "bounds=u.refresh_products(bounds)\n    assert sha(HERE/'prefix/PRODUCER_MANIFEST.json')=='"+prefix_sha+"'\n    prefix=json.loads((HERE/'prefix/stopped-chain.json').read_text())\n    assert len(prefix['rounds'])==3 and prefix['final_core_ratio']=='1'\n    bounds=[tuple(map(F,v)) for v in prefix['final_bounds']]\n    assert u.refresh_products(bounds)==bounds\n    assert bounds[21][0]>=-F(17,50000) and bounds[25][1]<=F(1,40)\n    gate="),
 ("'initial_bounds':[list(map(str,v)) for v in bounds],'extra_row':extra,", "'initial_bounds':[list(map(str,v)) for v in bounds],'extra_row':extra,\n      'prefix_manifest_sha256':sha(HERE/'prefix/PRODUCER_MANIFEST.json'),\n      'prefix_chain_sha256':sha(HERE/'prefix/stopped-chain.json'),"),
 ('for iteration in range(1,4):','for iteration in range(4,16):'),
 ('time.process_time()-START>=50','time.process_time()-START>=44'),
 ("STATE['LP_calls']<=276","STATE['LP_calls']<=1104"),
 ("STATE['status']='THREE_ROUNDS_INCONCLUSIVE'","STATE['status']='TWELVE_ADDITIONAL_ROUNDS_INCONCLUSIVE'"),
]
for a,b in changes:
    assert new.count(a)==1,(a,new.count(a))
    new=new.replace(a,b)
(here/'propagate.py').write_text(new)
(here/'SOURCE.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='frozen-prefix/propagate.py',tofile='continuation/propagate.py')))
prep=json.loads((src/'preparation.json').read_text())
prep.update({'status': 'PREPARED_CONTINUATION_FROM_FROZEN_THREE_ROUNDS', 'base': 'Exact final box from frozen stopped round3; same245 necessary rows', 'maximum_rounds': 12, 'round_numbers': [4, 15], 'maximum_LP_calls': 1104, 'shared_original_producer_CPU_cap_seconds': 60, 'prefix_conservative_CPU_charge': 5, 'new_process_CPU_soft_hard': [50, 53], 'prefix_manifest_sha256': prefix_sha, 'prefix_files': [{'path': 'prefix/' + name, 'sha256': sha(here / 'prefix' / name)} for name in prefix_files], 'source_diff_sha256': sha(here / 'SOURCE.diff'), 'continuation_source_sha256': sha(here / 'propagate.py'), 'CPU_seconds': time.process_time() - start})
(here/'preparation.json').write_text(json.dumps(prep,indent=2)+'\n')
print(json.dumps({'status':prep['status'],'CPU_seconds':prep['CPU_seconds'],'source_sha256':prep['continuation_source_sha256']}))
