from pathlib import Path
import hashlib,json,time
HERE=Path(__file__).resolve().parent;ROOT=next(p for p in HERE.parents if (p/'local-research/claude-20261002/results/rerun_trees_20261011/SHA256_G20S_HW.txt').is_file())
START=time.process_time();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def need(v,m):
 if not v:raise ValueError(m)
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
pins=load(HERE/'pins.json')
for p,h in pins['inputs'].items():need(sha(ROOT/p)==h,'input changed '+p)
r=load(HERE/'receipt.json');need(r['status']=='PASS_EXACT_FINITE_PARTIAL_CONTRACTION_TARGET_NOT_REACHED','review status')
need(r['exact_signed_bounds']==276 and len(r['controls_rejected'])==9 and not r['terminal_theorem_applied'],'scope')
tele=load(HERE/'telemetry.json');need(tele['error'] is None,'review failure')
prod=HERE.parent/'producer';diag=load(prod/'DIAGNOSTIC_MANIFEST.json')
for p,h in diag['files'].items():need(sha(prod/p)==h,'diagnostic input changed')
cost={'full_reconstruction_replay_CPU_seconds': r['CPU_seconds'], 'telemetry_process_CPU_seconds': tele['CPU_seconds'], 'source_preparation_CPU_seconds': load(HERE / 'adaptation.json')['CPU_seconds'], 'input_binding_CPU_seconds': pins['setup_CPU_seconds'], 'saved_bound_check_CPU_seconds': load(HERE / 'saved-bounds-review.json')['CPU_seconds'], 'seal_CPU_seconds_before_write': time.process_time() - START, 'conservative_total_charge_CPU_seconds': 6, 'optimizer_runs': 0, 'failed_executions': 0, 'independent_model_runs': 3, 'additional_rounds_in_this_scope': 0}
save('COSTS.json',cost)
files=['adaptation.json','independent_model.py','check.py','pins.json','receipt.json','telemetry.json','saved-bounds-review.json','REVIEW.md','COSTS.json','seal.py']
save('MANIFEST.json',{'status':'ACCEPTED_CONDITIONAL_PARTIAL_FINITE_CONTRACTION_TARGET_NOT_REACHED','reviewer':'Codex contributor 03','producer':'Codex contributor 10','producer_manifest_sha256':sha(prod/'PRODUCER_MANIFEST.json'),'certificate_sha256':sha(prod/'certificate.json'),'producer_diagnostic_manifest_sha256':sha(prod/'DIAGNOSTIC_MANIFEST.json'),'complete_rounds':3,'rows_independently_reconstructed':sum(x['rows'] for x in r['rounds']),'SAT_options_independently_checked':456,'signed_bounds_independently_replayed':276,'position_radius':'2951564640979/1000000000000000','angle_radius':'1/400','target_raw_core_radius':'1/10000','terminal_join_applied':False,'actual_side':'S <= S* < Sref; exact margin checked','physical_parent_count':17,'free_physical_label':4,'capture_or_optimality_claim':False,'cost':cost,'files':{f:sha(HERE/f) for f in files},'input_bindings':pins['inputs']})
print(sha(HERE/'MANIFEST.json'))
