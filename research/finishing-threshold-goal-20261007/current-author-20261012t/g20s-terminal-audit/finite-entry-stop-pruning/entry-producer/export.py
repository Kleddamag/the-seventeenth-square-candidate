#!/usr/bin/env python3
"""Compose exact transfer with a pinned accepted root-stop theorem; no model."""
import hashlib,json,shutil,sys,time
from fractions import Fraction as F
from pathlib import Path
start=time.process_time();here=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert len(sys.argv)==2 and len(sys.argv[1])==64
expected_review=sys.argv[1]
rootdir=here.parent/'root-producer';reviewdir=here.parent/'root-review'
assert sha(reviewdir/'manifest.json')==expected_review
review=json.loads((reviewdir/'manifest.json').read_text())
assert review['status'].startswith('ACCEPTED')
assert sha(rootdir/'manifest.json')=='5a3aab61d2a5f5b08090fc4fc8e0ad67482007b06e370d0cbdc4db255cdf9ead'
producer=json.loads((rootdir/'manifest.json').read_text())
records=producer['files']
pins=records if isinstance(records,dict) else {v['path']:v['sha256'] for v in records}
for name in ('root-interface.json','receipt.json','PROOF.md'):
    assert sha(rootdir/name)==pins[name]
root=json.loads((rootdir/'root-interface.json').read_text())
rr=json.loads((rootdir/'receipt.json').read_text())
tr=json.loads((here/'transfer-receipt.json').read_text())
assert root['physical_scope']['all45_exact_root_core_absolute_bounds']==tr['root_epsilon']=='501/100000'
assert root['unscaled_physical_slider_indices']=={'a':2,'b':21,'z':25}
for name,index in (('a','2'),('b','21'),('z','25')):
    assert root['input_exact_root_slider_intervals'][name]==tr['root_slider_pads'][index]
gate=json.loads((here/'inputs/accepted-root-gate.json').read_text())
for small,large in zip(gate['root']['intervals'],rr['root_intervals']):
    assert F(large[0])<=F(small[0])<=F(small[1])<=F(large[1])
strong=root['stronger_exact_rational_conclusions']
L=F(strong['b_lower']);U=F(strong['b_plus_z_upper']);Z=F(strong['z_upper'])
assert L==-F(8517,1000000) and Z==U-L
eb=list(map(F,tr['root_slider_error_intervals']['21']))
ez=list(map(F,tr['root_slider_error_intervals']['25']))
actual={'b_lower':L-eb[1],'sum_upper':U-eb[0]-ez[0],'z_upper':Z-ez[0]}
slacks={'b':actual['b_lower']+F(213,25000),
        'sum':F(49,2000)-actual['sum_upper'],'z':F(33,1000)-actual['z_upper']}
assert all(v>0 for v in slacks.values())
frozen=[]
for source,prefix,names in ((rootdir,'root-proof',['manifest.json','root-interface.json','receipt.json','PROOF.md']),
                           (reviewdir,'root-review',['manifest.json'])):
    for name in names:
        out=here/'inputs'/prefix/name;out.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source/name,out)
        frozen.append({'path':str(out.relative_to(here)),'sha256':sha(out)})
raw=json.loads((here/'inputs/raw-reference-interface.json').read_text())
squares=raw['rational_entry_scope']['squares']
for square in squares:
    square['independent_angle_radius_radians']='1/400'
    square['nonslider_position_coordinate_radius']='1/200'
positions=raw['common_hypotheses']['core_position_indices']
angles=raw['common_hypotheses']['core_angle_indices']
coordinate_bounds={str(i):['-1/200','1/200'] for i in positions}
coordinate_bounds.update({str(i):['-1/400','1/400'] for i in angles})
coordinate_bounds.update(tr['raw_entry']['sliders'])
export={
 'schema':'s17-guarded-raw-stop-pruning-v1',
 'status':'PRODUCER_PASS_WITH_ACCEPTED_ROOT_THEOREM_REQUIRES_SEPARATE_INDEPENDENT_ENTRY_REVIEW',
 'kind':'Mathematical guarded linear necessities; not a newly recognized WX certificate step',
 'guards':{
   **raw['common_hypotheses'],
   'all17_squares_physically_contained_and_interior_disjoint':True,
   'frame':'Actual physical [0,S]^2 in the one stated common reference frame; no automatic fixed-U recentering',
   'reference_side':raw['rational_entry_scope']['reference_side'],
   'reference_p13_correction':raw['rational_entry_scope']['reference_p13_correction'],
   'closed_zero_based_raw_coordinate_bounds':coordinate_bounds,
   'squares':squares,
   'angles_are_radians_not_half_angle_tangents':True,
   'consumer_half_angle_arc_must_imply_radian_guard':True,
   'sufficient_relative_half_angle_tangent_bound':'1/800, only relative to the same stated reference orientation',
   'no_dummy_coordinate_constraint_on_physical4':True,
 },
 'unscaled_raw_slider_rows':[
   {'coefficients':{'b':'1'},'sense':'>=','rhs':'-213/25000'},
   {'coefficients':{'b':'1','z':'1'},'sense':'<=','rhs':'49/2000'},
   {'coefficients':{'z':'1'},'sense':'<=','rhs':'33/1000'}],
 'raw_slider_index_rows':[
   {'coefficients':{'21':'1'},'sense':'>=','rhs':'-213/25000'},
   {'coefficients':{'21':'1','25':'1'},'sense':'<=','rhs':'49/2000'},
   {'coefficients':{'25':'1'},'sense':'<=','rhs':'33/1000'}],
 'mathematical_local_displacement_sign_map':{'xi_11_2':'-b','xi_13_2':'z','xi_2_1':'-a'},
 'equivalent_local_displacement_rows':[
   {'coefficients':{'xi_11_2':'1'},'sense':'<=','rhs':'213/25000'},
   {'coefficients':{'xi_13_2':'1','xi_11_2':'-1'},'sense':'<=','rhs':'49/2000'},
   {'coefficients':{'xi_13_2':'1'},'sense':'<=','rhs':'33/1000'}],
 'root_transfer':{'epsilon':tr['root_epsilon'],'core_upper':tr['maximum_root_core_bound'],
   'slider_errors':tr['root_slider_error_intervals'],'nonnegative_root_a_uses_actual_right_wall':True},
 'stronger_root_bounds_used':strong,
 'exact_composed_raw_bounds':{k:str(v) for k,v in actual.items()},
 'strict_export_slacks':{k:str(v) for k,v in slacks.items()},
 'dependencies':{'root_producer_manifest_sha256':sha(rootdir/'manifest.json'),
   'accepted_root_review_sha256':expected_review,
   'raw_reference_review_sha256':sha(here/'inputs/raw-reference-review.json'),
   'raw_reference_interface_sha256':sha(here/'inputs/raw-reference-interface.json'),
   'packing_reference_sha256':sha(here/'instance/upper-packing-certificate.json'),
   'root_bridge_source_sha256':sha(here/'instance/research/uniform-capture-20261007/bridge.py'),
   'raw_coordinate_source_sha256':sha(here/'instance/research/uniform-capture-20261007/uniform.py'),
   'accepted_root_gate_sha256':sha(here/'inputs/accepted-root-gate.json'),
   'transfer_receipt_sha256':sha(here/'transfer-receipt.json')},
 'not_conclusions':{'finite_contraction':True,'terminal_reach':True,'WX_step_schema_acceptance':True,
                    'larger_window_rigidity':True,'global_capture_or_optimality':True}}
(here/'PRUNING.json').write_text(json.dumps(export,indent=2)+'\n')
receipt={'status':'ACCEPTED_ROOT_COMPOSED_EXACTLY_ENTRY_REVIEW_SEPARATE_OBLIGATION','root_review_sha256':expected_review,
 'files':frozen,'export_sha256':sha(here/'PRUNING.json'),
 'strict_export_slacks':export['strict_export_slacks'],'CPU_seconds':time.process_time()-start}
(here/'export-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'CPU_seconds':receipt['CPU_seconds'],
 'export_sha256':receipt['export_sha256'],'slacks_decimal':{k:float(v) for k,v in slacks.items()}},indent=2))
