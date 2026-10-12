#!/usr/bin/env python3
"""Freeze the larger-radius physical stop package; no geometry search."""
import difflib,hashlib,json,time
from pathlib import Path
START=time.process_time();HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'local-research/claude-20261002/results/rerun_trees_20261011/SHA256_G20S_HW.txt').exists())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
r=load(HERE/'receipt.json');deps=load(HERE/'dependencies.json')
assert r['status']=='PASS_G20S_FINITE_ENTRY_ROOT_STOPS_REQUIRES_SEPARATE_REVIEW'
assert r['simple_closed_conclusions']=={'b_lower':'-8517/1000000','b_plus_z_upper':'49/2000','z_upper':'33/1000'}
assert len(r['complete_stop_pairs'])==2
assert sum(len(v['excluded']) for v in r['complete_stop_pairs'])==12
assert sum(len(v['retained']) for v in r['complete_stop_pairs'])==4
for path,digest in deps['files'].items():assert sha(HERE/'inputs'/path)==digest
previous=HERE.parents[1]/'stop-coupled-finish/stop-producer/check_stops.py'
patch=''.join(difflib.unified_diff(previous.read_text().splitlines(True),(HERE/'check_stops.py').read_text().splitlines(True),
                                 fromfile='accepted-small-radius-check_stops.py',tofile='larger-radius-check_stops.py'))
(HERE/'SOURCE.diff').write_text(patch)
replay=json.loads((HERE/'replay-output.jsonl').read_text().splitlines()[-1])['replay_telemetry']
cost={'preparation_process_CPU_seconds':deps['process_CPU_seconds'],
      'guard_calculation_process_CPU_seconds':load(HERE/'telemetry.json')['process_CPU_seconds'],
      'interface_process_CPU_seconds':load(HERE/'interface-telemetry.json')['process_CPU_seconds'],
      'read_only_replay_process_CPU_seconds':replay['process_CPU_seconds'],
      'additional_interface_metadata_process_CPU_seconds':0.038026,
      'conservative_producer_CPU_charge_seconds':2,'producer_CPU_cap_seconds':10,
      'one_core':True,'new_model_LP_SymPy_calls':0,'failed_numerical_runs':0,
      'unmeasured_shell_source_read_and_seal_overhead':'Included in conservative two-second charge'}
cost['measured_process_CPU_seconds']=sum(v for k,v in cost.items() if k.endswith('process_CPU_seconds'))
assert cost['measured_process_CPU_seconds']<2
(HERE/'COSTS.json').write_text(json.dumps(cost,indent=2)+'\n')
files=[p for p in HERE.rglob('*') if p.is_file() and p!=HERE/'manifest.json']
manifest={'schema':'s17-g20s-finite-entry-exact-root-stop-v1',
 'status':'PRODUCER_PASS_REQUIRES_SEPARATE_INDEPENDENT_REVIEW','producer':'Codex contributor 10',
 'exact_root_epsilon_max':'501/100000','exact_root_slider_domain':r['exact_root_padded_sliders'],
 'claims':r['simple_closed_conclusions'],'stronger_rational_rhs_in':'root-interface.json',
 'SAT_options':16,'strictly_excluded':12,'retained_both_owner_choices':4,
 'independent_angles':True,'physical_parents':17,'unrestricted_physical_label':4,
 'unscaled_slider_indices':r['unscaled_slider_indices'],
 'full_gate_review_sha256':'a70b064bb81a55fca7f5ad9a9b19ea765c613877d8b243e041081760b9dc53dd',
 'prior_stop_review_sha256':'e8af5453f7e97d18ee2dab652644d797218ce2382fb928b53a8cb151cee7645d',
 'new_radius_guards_all_recomputed':True,'old_sum_coefficient13_over100_rejected':True,
 'raw_coordinate_transfer_proved':False,'finite_contraction_or_terminal_proved':False,
 'capture_or_global_optimality_proved':False,'negative_controls':7,
 'files':[{'path':str(p.relative_to(HERE)),'sha256':sha(p)} for p in sorted(files)],
 'CPU_charge_seconds':2,'CPU_cap_seconds':10,
 'replay':'/usr/bin/python3 -B research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/finite-entry-stop-pruning/root-producer/check_stops.py --snapshot --check',
 'seal_CPU_seconds':time.process_time()-START}
(HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'status':manifest['status'],'manifest_sha256':sha(HERE/'manifest.json'),
                  'measured_process_CPU_seconds':cost['measured_process_CPU_seconds'],'conservative_CPU_seconds':2}))
