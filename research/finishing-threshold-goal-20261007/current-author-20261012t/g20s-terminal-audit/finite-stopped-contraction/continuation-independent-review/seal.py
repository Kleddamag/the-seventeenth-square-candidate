from pathlib import Path
import hashlib,json,time
HERE=Path(__file__).resolve().parent;ROOT=next(p for p in HERE.parents if (p/'local-research/claude-20261002/results/rerun_trees_20261011/SHA256_G20S_HW.txt').is_file());START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def need(x,m):
 if not x:raise ValueError(m)
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
pins=load(HERE/'pins.json')
for p,h in pins['inputs'].items():need(sha(ROOT/p)==h,'input changed '+p)
r=load(HERE/'receipt.json');need(r['status']=='PASS_EXACT_FINITE_PARTIAL_CONTRACTION_TARGET_NOT_REACHED' and r['exact_signed_bounds']==552 and len(r['controls_rejected'])==9,'review scope')
need(not r['terminal_theorem_applied'] and [x['round'] for x in r['rounds']]==list(range(4,10)),'round/terminal scope')
t=load(HERE/'telemetry.json');need(t['error'] is None,'failure')
old=HERE.parent/'independent-review';prod=HERE.parent/'continuation'
need(sha(HERE/'independent_model.py')==sha(old/'independent_model.py'),'unchanged independent polynomial implementation')
cost={'full_new_replay_CPU_seconds': r['CPU_seconds'], 'telemetry_process_CPU_seconds': t['CPU_seconds'], 'source_preparation_CPU_seconds': load(HERE / 'PREPARATION.json')['CPU_seconds'], 'input_binding_CPU_seconds': pins['setup_CPU_seconds'], 'saved_bound_check_CPU_seconds': load(HERE / 'saved-bounds-review.json')['CPU_seconds'], 'seal_CPU_seconds_before_write': time.process_time() - START, 'conservative_total_charge_CPU_seconds': 11, 'prefix_rounds_replayed': 0, 'new_model_reconstructions': 6, 'failed_executions': 0, 'optimizer_runs': 0}
save('COSTS.json',cost)
files=['PREPARATION.json','independent_model.py','check.py','pins.json','receipt.json','telemetry.json','saved-bounds-review.json','REVIEW.md','COSTS.json','seal.py']
save('MANIFEST.json',{'status':'ACCEPTED_SIX_FURTHER_CONDITIONAL_PARTIAL_FINITE_ROUNDS_TARGET_NOT_REACHED','reviewer':'Codex contributor 03','producer':'Codex contributor 10','producer_manifest_sha256':sha(prod/'PRODUCER_MANIFEST.json'),'certificate_sha256':sha(prod/'certificate.json'),'prefix_independent_review_sha256':sha(old/'MANIFEST.json'),'new_complete_rounds':6,'total_rounds_with_accepted_prefix':9,'new_rows_independently_reconstructed':sum(x['rows'] for x in r['rounds']),'new_SAT_options_checked':912,'new_signed_bounds_replayed':552,'position_radius':'7336628287/6250000000000','angle_radius':'1/400','target_raw_core_radius':'1/10000','terminal_join_applied':False,'physical_scope':'Seventeen physical squares, free4; one common frame/injective roles; actual S<=S*; original guarded raw entry and accepted stop cuts.','capture_or_optimality_claim':False,'cost':cost,'files':{f:sha(HERE/f) for f in files},'input_bindings':pins['inputs']})
print(sha(HERE/'MANIFEST.json'))
