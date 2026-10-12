from pathlib import Path
import hashlib,json,time
H=Path(__file__).resolve().parent;start=time.process_time()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((H/'receipt.json').read_text());assert r['status']=='ACCEPTED_RATIONAL_SMALL_ENTRY_COROLLARY'
cost={'measured_check_cpu_seconds':r['cpu_seconds'],'additional_conservative_charge_seconds':1,'prior_shared_charge_seconds':9,'total_shared_charge_seconds':10,'original_cap_seconds':60,'remaining_seconds':50,'single_native_thread':True,'failed_runs':0,'new_optimizer_or_model_or_certificate_replay':False}
(H/'COSTS.json').write_text(json.dumps(cost,indent=2)+'\n')
m={'status':'ACCEPTED_RATIONAL_SMALL_ENTRY_COROLLARY_AND_MATHEMATICAL_INTERFACE','reviewer':'Codex contributor 07','dependencies':{'accepted_transfer_review':'ab96060dce2f0e5b17006b52a9a8c0d7b70f6a94897c9dd0f013d9911cfbdd12','accepted_exact_root_rigidity_review':'e5b0819966146f51aef3fae61feaaed0985e70379ed6eb180e6931c8e1f41570'},'raw_core_radius':'1/10000','root_core_radius':'1/5000','independent_radian_angle_count':16,'position_core_count':29,'physical_parent_count':17,'free_physical_label':4,'actual_side_premise':'S <= algebraic S*','conclusion':['All45 exact-root core coordinates zero','S=S*'],'larger_entry_1_200_position_1_400_angle_accepted':False,'interface_kind':'Mathematical interface only; no new WX certificate-type claim','cost':cost,'files':{n:sha(H/n) for n in ['check_corollary.py','receipt.json','MATHEMATICAL_INTERFACE.json','REVIEW.md','COSTS.json','seal.py']},'seal_cpu_seconds':time.process_time()-start}
(H/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n');print(sha(H/'MANIFEST.json'))
