from pathlib import Path
import hashlib,json,time
START=time.process_time()
H=Path(__file__).resolve().parent;G=H.parents[1];P=H.parent/'continuation'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
old=H.parent/'independent-review';oldm=read(old/'MANIFEST.json')
assert sha(old/'MANIFEST.json')=='f9d879a28cf0ed98acb23672b4c2b4a923b09d48a2f6b74a52a1e500a9431941'
for name,digest in oldm['files'].items():assert sha(old/name)==digest
assert sha(P/'PRODUCER_MANIFEST.json')=='685d4d96672a5522cd44f85653907a441bf81b49ce43625f59cacc6d71870de1'
assert sha(P/'PREFIX_ACCEPTANCE_BINDING.json')=='a179e983f24c63cb4888a7f23564e06db6c9f0a7a45cf0ae6d2a93a704420746'
r=read(H/'receipt.json');assert r['status']=='ACCEPTED_STRICT_NORMALIZED_STOPPED_CONTRACTION'
cost={'new_exact_replay_cpu_seconds':r['cpu_seconds'],'new_conservative_charge_seconds':4,'prior_review_charge_seconds':5,'total_charge_seconds':9,'shared_cap_seconds':60,'remaining_seconds':51,'one_native_thread':True,'failed_review_runs':0,'solver_symbolic_or_old_checker_called':False}
(H/'COSTS.json').write_text(json.dumps(cost,indent=2)+'\n')
m={'status':'ACCEPTED_SMALL_EXACT_ROOT_RIGIDITY_AND_SIDE_EQUALITY','reviewer':'Codex contributor 07','producer':'Codex contributor 06','producer_manifest_sha256':sha(P/'PRODUCER_MANIFEST.json'),'producer_theorem_sha256':sha(P/'THEOREM.md'),'additive_prefix_acceptance_binding_sha256':sha(P/'PREFIX_ACCEPTANCE_BINDING.json'),'accepted_first_three_review_sha256':sha(old/'MANIFEST.json'),'dependencies':oldm['dependencies'],'new_rounds':2,'new_exact_objectives':184,'total_stopped_rounds':5,'total_stopped_exact_objectives':460,'rows_each_round':245,'final_core_ratio':r['final_core_ratio'],'core_coordinates':45,'physical_parents':17,'free_physical_label':4,'actual_side_hypothesis':'S <= S*','exact_root_core_radius':'1/5000','conclusion':['all 45 exact-root core coordinates zero','S = S*'],'no_finite_entry_or_capture_claim':True,'cost':cost,'files':{name:sha(H/name) for name in ['check.py','receipt.json','REVIEW.md','COSTS.json','finalize.py']},'seal_cpu_seconds':time.process_time()-START}
(H/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
print(sha(H/'MANIFEST.json'))
