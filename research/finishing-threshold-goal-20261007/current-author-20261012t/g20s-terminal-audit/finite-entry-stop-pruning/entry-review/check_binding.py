"""Independent scope/export/source audit after independent coordinate arithmetic."""
import copy,hashlib,json,resource,sys,time
from pathlib import Path
from fractions import Fraction as F
resource.setrlimit(resource.RLIMIT_CPU,(3,4))
start=time.process_time();H=Path(__file__).resolve().parent;G=H.parents[1];P=H.parent/'entry-producer';RR=H.parent/'root-review'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
assert sha(P/'PRODUCER_MANIFEST.json')==sys.argv[1]
pm=load(P/'PRODUCER_MANIFEST.json')
items=pm.get('files_sha256',pm.get('files'))
if isinstance(items,dict):items=[{'path':k,'sha256':v if isinstance(v,str) else v['sha256']} for k,v in items.items()]
for v in items:assert sha(P/v['path'])==v['sha256']
assert sha(RR/'manifest.json')=='907071a795d42b92890da0a1894b3a9765635908caf2812044ade6d65d76056e'
r=load(RR/'manifest.json')
for v in r['files']:assert sha(RR/v['path'])==v['sha256']
assert r['status']=='ACCEPTED_G20S_BROAD_ROOT_STOP_THEOREM'
assert (P/'inputs/root-review/manifest.json').read_bytes()==(RR/'manifest.json').read_bytes()
root=load(P/'inputs/root-proof/root-interface.json')
assert sha(P/'inputs/root-proof/root-interface.json')==r['root_interface_sha256']
assert r['uniform_bounds']=={'b_lower':'-(17/10)*epsilon','b_plus_z_upper':'T/3+(7/50)*epsilon','z_upper':'T/3+(46/25)*epsilon'}
assert root['unscaled_physical_slider_indices']==r['unscaled_slider_indices']=={'a':2,'b':21,'z':25}
assert root['physical_scope']['all45_exact_root_core_absolute_bounds']==r['input_domain']['core_epsilon_max']=='501/100000'
raw=load(P/'inputs/raw-reference-interface.json');x=load(P/'PRUNING.json')
assert sha(P/'inputs/raw-reference-interface.json')=='d1aead18ef637439b696c303e050c63afeb9782e326703e7e9c7bd9b70939ff4'
assert sha(P/'inputs/raw-reference-review.json')=='5a70b980bdf8c519d1bcb19a6f710737e41073e782286f849e9ac62915f3b3cc'
tr=load(P/'transfer-receipt.json');own=load(H/'transfer-receipt.json')
assert tr['root_epsilon']==own['root_epsilon']=='501/100000'
assert set(tr['root_core_bounds'])==set(own['all45_root_core_bounds']) and len(tr['root_core_bounds'])==45
for j,v in tr['root_core_bounds'].items():assert F(own['all45_root_core_bounds'][j])<=F(v)<F(501,100000)
for j,v in tr['root_slider_error_intervals'].items():
    lo,hi=map(F,v);a,b=map(F,own['root_minus_raw_slider_errors'][j]);assert lo<=a<=b<=hi
    assert max(abs(lo),abs(hi))<F(1,10**15)
for name,j in r['unscaled_slider_indices'].items():
    lo,hi=map(F,r['input_domain']['exact_root_sliders'][name]);a,b=map(F,tr['root_slider_intervals'][str(j)])
    assert lo<=a<=b<=hi
    assert root['input_exact_root_slider_intervals'][name]==tr['root_slider_pads'][str(j)]
assert tr['a_root_lower_uses_actual_right_wall']
small=load(P/'inputs/accepted-root-gate.json')['root']['intervals'];large=load(RR/'arithmetic-receipt.json')['root_intervals']
assert len(small)==len(large)==2
for a,b in zip(small,large):assert F(b[0])<=F(a[0])<=F(a[1])<=F(b[1])
strong=r['stronger_exact_bounds'];assert strong==root['stronger_exact_rational_conclusions']==x['stronger_root_bounds_used']
L,U,Z=map(F,(strong['b_lower'],strong['b_plus_z_upper'],strong['z_upper']))
assert L==-F(8517,1000000) and Z==U-L
err=tr['root_slider_error_intervals'];eb=list(map(F,err['21']));ez=list(map(F,err['25']))
actual={'b_lower':L-eb[1],'sum_upper':U-eb[0]-ez[0],'z_upper':Z-ez[0]}
slacks={'b':actual['b_lower']+F(213,25000),'sum':F(49,2000)-actual['sum_upper'],'z':F(33,1000)-actual['z_upper']}
assert {k:str(v) for k,v in actual.items()}==x['exact_composed_raw_bounds']
assert {k:str(v) for k,v in slacks.items()}==x['strict_export_slacks'] and min(slacks.values())>0
# Independent tighter coordinate errors also imply the same cutoffs using the
# ROOT REVIEW'S exact upper, not our independently computed narrower T interval.
oeb=list(map(F,own['root_minus_raw_slider_errors']['21']));oez=list(map(F,own['root_minus_raw_slider_errors']['25']))
assert L-oeb[1]>-F(213,25000) and U-oeb[0]-oez[0]<F(49,2000) and Z-oez[0]<F(33,1000)

named=[{'coefficients':{'b':'1'},'sense':'>=','rhs':'-213/25000'},{'coefficients':{'b':'1','z':'1'},'sense':'<=','rhs':'49/2000'},{'coefficients':{'z':'1'},'sense':'<=','rhs':'33/1000'}]
indexrows=[{**row,'coefficients':{str({'b':21,'z':25}[k]):v for k,v in row['coefficients'].items()}} for row in named]
wx=[{'coefficients':{'xi_11_2':'1'},'sense':'<=','rhs':'213/25000'},{'coefficients':{'xi_13_2':'1','xi_11_2':'-1'},'sense':'<=','rhs':'49/2000'},{'coefficients':{'xi_13_2':'1'},'sense':'<=','rhs':'33/1000'}]
common=raw['common_hypotheses'];rawscope=raw['rational_entry_scope']
expectedbounds={str(j):['-1/200','1/200'] for j in common['core_position_indices']}
expectedbounds.update({str(j):['-1/400','1/400'] for j in common['core_angle_indices']})
expectedbounds.update(rawscope['slider_bounds'])
expectedsquares=copy.deepcopy(rawscope['squares'])
for q in expectedsquares:q['independent_angle_radius_radians']='1/400';q['nonslider_position_coordinate_radius']='1/200'
def validate_export(v):
    q=v['guards']
    for k,val in common.items():assert q[k]==val
    assert q['closed_zero_based_raw_coordinate_bounds']==expectedbounds
    assert q['squares']==expectedsquares
    assert q['frame']=='Actual physical [0,S]^2 in the one stated common reference frame; no automatic fixed-U recentering'
    assert q['reference_side']==rawscope['reference_side'] and q['reference_p13_correction']==rawscope['reference_p13_correction']
    assert q['all17_squares_physically_contained_and_interior_disjoint']
    assert q['angles_are_radians_not_half_angle_tangents'] and q['consumer_half_angle_arc_must_imply_radian_guard']
    assert q['sufficient_relative_half_angle_tangent_bound']=='1/800, only relative to the same stated reference orientation'
    assert q['no_dummy_coordinate_constraint_on_physical4']
    assert v['unscaled_raw_slider_rows']==named and v['raw_slider_index_rows']==indexrows
    assert v['mathematical_local_displacement_sign_map']=={'xi_11_2':'-b','xi_13_2':'z','xi_2_1':'-a'}
    assert v['equivalent_local_displacement_rows']==wx
    assert v['root_transfer']['nonnegative_root_a_uses_actual_right_wall']
    assert v['not_conclusions']=={'finite_contraction':True,'terminal_reach':True,'WX_step_schema_acceptance':True,'larger_window_rigidity':True,'global_capture_or_optimality':True}
validate_export(x)
# Verify algebraic sign substitution at every row, independently of display.
for source,target in zip(named,wx):
    coeff={('xi_11_2' if k=='b' else 'xi_13_2'):F(v)*(-1 if k=='b' else 1) for k,v in source['coefficients'].items()}
    rhs=F(source['rhs']);sense=source['sense']
    if sense=='>=':coeff={k:-v for k,v in coeff.items()};rhs=-rhs;sense='<='
    assert coeff=={k:F(v) for k,v in target['coefficients'].items()} and rhs==F(target['rhs']) and sense==target['sense']
deps=x['dependencies'];expecteddeps={'accepted_root_review_sha256':sha(RR/'manifest.json'),'raw_reference_review_sha256':sha(P/'inputs/raw-reference-review.json'),'raw_reference_interface_sha256':sha(P/'inputs/raw-reference-interface.json'),'root_producer_manifest_sha256':sha(P/'inputs/root-proof/manifest.json'),'packing_reference_sha256':sha(P/'instance/upper-packing-certificate.json'),'root_bridge_source_sha256':sha(P/'instance/research/uniform-capture-20261007/bridge.py'),'raw_coordinate_source_sha256':sha(P/'instance/research/uniform-capture-20261007/uniform.py'),'accepted_root_gate_sha256':sha(P/'inputs/accepted-root-gate.json'),'transfer_receipt_sha256':sha(P/'transfer-receipt.json')}
assert deps==expecteddeps
controls=[]
def reject(name,mutate):
    v=copy.deepcopy(x);mutate(v)
    try:validate_export(v)
    except AssertionError:controls.append(name)
    else:raise AssertionError('Accepted bad guard: '+name)
reject('widen position guard',lambda v:v['guards']['closed_zero_based_raw_coordinate_bounds']['0'].__setitem__(1,'1/100'))
reject('interpret angle as tan-half',lambda v:v['guards'].__setitem__('angle_units','tan-half'))
reject('duplicate physical role',lambda v:v['guards']['distinct_constrained_physical_labels'].__setitem__(0,2))
reject('replace actual algebraic cap by Sref',lambda v:v['guards'].__setitem__('actual_side_hypothesis','S <= Sref'))
reject('flip WX b sign',lambda v:v['mathematical_local_displacement_sign_map'].__setitem__('xi_11_2','b'))
reject('claim finite contraction',lambda v:v['not_conclusions'].__setitem__('finite_contraction',False))
reject('strengthen b cutoff',lambda v:v['unscaled_raw_slider_rows'][0].__setitem__('rhs','-1/125'))
reject('drop one closed coordinate',lambda v:v['guards']['closed_zero_based_raw_coordinate_bounds'].pop('50'))
out={'status':'ACCEPTED_GUARDED_RAW_ENTRY_STOP_PRUNING','entry_producer_manifest_sha256':sha(P/'PRODUCER_MANIFEST.json'),'root_stop_review_sha256':sha(RR/'manifest.json'),'export_sha256':sha(P/'PRUNING.json'),'complete_core_coordinate_count':45,'position_coordinates':29,'independent_radian_angle_coordinates':16,'physical_squares':17,'free_physical_label':4,'actual_S_le_Sstar_and_a_wall_retained':True,'stronger_root_upper_used_with_signed_transfer_error':True,'WX_algebraic_sign_substitution_checked':True,'WX_engine_acceptance_claimed':False,'closed_raw_bounds_and_all_labels_verified':True,'strict_export_slacks':{k:str(v) for k,v in slacks.items()},'guard_corruption_controls_rejected':controls,'CPU_seconds':time.process_time()-start}
(H/'binding-receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'CPU_seconds':out['CPU_seconds'],'controls':len(controls)}))
