"""Compose accepted exact transfer and strict rigidity; no optimization."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,resource,time
resource.setrlimit(resource.RLIMIT_CPU,(2,3))
start=time.process_time()
H=Path(__file__).resolve().parent;G=H.parents[1];P=H.parent/'continuation'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
def accepted(directory,digest):
    assert sha(directory/'MANIFEST.json')==digest
    m=load(directory/'MANIFEST.json')
    for name,v in m['files'].items():
        assert sha(directory/name)==(v if isinstance(v,str) else v['sha256'])
    return m
transfer=G/'independent-review'
accepted(transfer,'ab96060dce2f0e5b17006b52a9a8c0d7b70f6a94897c9dd0f013d9911cfbdd12')
rigidity=H.parent/'continuation-independent-review'
accepted(rigidity,'e5b0819966146f51aef3fae61feaaed0985e70379ed6eb180e6931c8e1f41570')
assert sha(P/'PRODUCER_MANIFEST.json')=='685d4d96672a5522cd44f85653907a441bf81b49ce43625f59cacc6d71870de1'
rec=load(transfer/'receipt.json')
rawradius=F(1,10000);rootradius=F(1,5000);pad=F(1,10**12)
assert F(rec['maximum_exact_root_core_from_1_10000'])<rawradius+F(1,10**15)<rootradius
rawbox={2:(F(0),F(8,25)),21:(-F(1,20),F(1,5)),25:(-F(1,5),F(3,40))}
rootbox={w:(lo if w==2 else lo-pad,hi+pad) for w,(lo,hi) in rawbox.items()}
assert set(rec['exact_root_slider_enclosures'])==set(map(str,rawbox))
for w,(lo,hi) in rootbox.items():
    l,h=map(F,rec['exact_root_slider_enclosures'][str(w)]);assert lo<=l<=h<=hi
roles=tuple(i for i in range(1,18) if i!=4)
core=tuple(i for i in range(51) if i not in (2,6,7,21,25,37))
angles=tuple(33+i for i in roles)
positions=tuple(i for i in core if i not in angles)
assert len(core)==45 and len(angles)==16 and len(positions)==29
old=G.parent/'claude-extension-audit/terminal-producer'
assert (old/'snapshot/upper-packing-certificate.json').read_bytes()==(P/'instance/upper-packing-certificate.json').read_bytes()
assert load(old/'gate-receipt.json')['root']==load(P/'inputs/accepted-root-gate.json')['root']
raw=load(P/'instance/upper-packing-certificate.json');side=F(raw['side'])
poses=[]
for i,sq in enumerate(raw['squares'],1):
    t=F(sq['t']);u=((1-t*t)/(1+t*t),2*t/(1+t*t));v=(-u[1],u[0])
    poses.append({'label':i,'point':(F(sq['x']),F(sq['y'])),'u':u,'v':v,'t':t})
c,s=poses[8]['u'];T=c*(c+4-side)
poses[12]['point']=tuple(poses[12]['point'][k]-T*poses[12]['v'][k]/3 for k in (0,1))
entries=[]
for i in roles:
    q=poses[i-1];item={'label':i,'reference_centre':list(map(str,q['point'])),'reference_u':list(map(str,q['u'])),'reference_v':list(map(str,q['v'])),'angle_coordinate':33+i,'independent_angle_radius_radians':'1/10000'}
    if i==2:
        item.update(position_formula='p2 - a*(1,0) + h3*(0,1)',core_position_indices=[3],slider_index=2)
    elif i==11:
        item.update(position_formula='p11 + h20*u11 - b*v11',core_position_indices=[20],slider_index=21)
    elif i==13:
        item.update(position_formula='p13_corrected + h24*u13 + z*v13',core_position_indices=[24],slider_index=25)
    else:item.update(position_formula=f'p{i} + (h{2*i-2},h{2*i-1})',core_position_indices=[2*i-2,2*i-1])
    entries.append(item)
assert sorted(j for v in entries for j in v['core_position_indices'])==list(positions)
sourcepaths={'rational_reference_file':P/'instance/upper-packing-certificate.json','rational_coordinate_map':P/'instance/research/uniform-capture-20261007/uniform.py','exact_root_layout':P/'instance/research/uniform-capture-20261007/bridge.py','exact_root_geometry':P/'instance/research/uniform-capture-20261007/root_geometry.py','accepted_root_enclosure':P/'inputs/accepted-root-gate.json'}
sources={k:{'path':str(v.resolve()),'sha256':sha(v)} for k,v in sourcepaths.items()}
assert sources['rational_reference_file']['sha256']=='24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7'
assert sources['rational_coordinate_map']['sha256']=='019ce089aa4d531fc292d332585360a2087428a770d5a66b8a8e1cf04fca921d'
assert sources['exact_root_layout']['sha256']=='a3b496ca0422b4818651d2d59d9652e925eb12af79200bcdd27b47843d0a56cc'
assert sources['exact_root_geometry']['sha256']=='8d31d7547394117f8fa4be7eb20beff85908f56409f5a0a3f57d4ffb08e1b38a'
common={'actual_unit_squares':17,'distinct_constrained_physical_labels':list(roles),'unrestricted_physical_label':4,'unrestricted_square_still_physically_contained_and_nonoverlapping':True,'one_common_frame_and_one_injective_label_assignment':True,'actual_side_hypothesis':'S <= S* (the algebraic root side, not a larger rational cap)','angle_units':'radians, independent physical rotations modulo pi/2 with stated small representatives','zero_based_core_indices':list(core),'core_position_indices':list(positions),'core_angle_indices':list(angles),'sliders_not_normalized_core':{'a':2,'b':21,'z':25},'dummy_indices_not_physical_constraints':[6,7,37]}
interface={'schema':'s17-mathematical-local-interface-v1','status':'ACCEPTED_MATHEMATICAL_INTERFACE_NOT_A_WX_CERTIFICATE_TYPE','common_hypotheses':common,'sources':sources,'exact_root_scope':{'reference':'bridge.layout(t*,beta*) and root_geometry.geometry(t*,beta*) at the accepted algebraic root','all45_core_abs_upper':'1/5000','slider_bounds':{str(w):list(map(str,b)) for w,b in rootbox.items()},'physical_pose_formulas':'Same coordinate formulas as raw entries, with exact-root reference centres and axes','conclusion':['All45 exact-root core coordinates equal zero','S = S*']},'rational_entry_scope':{'reference_side':str(side),'frame':'Actual physical [0,S]^2; no fixed-U centring translation is silently applied','all45_core_abs_upper':'1/10000','slider_bounds':{str(w):list(map(str,b)) for w,b in rawbox.items()},'reference_p13_correction':'p13_file - T0*v13/3, T0=c0*(c0+4-Sref), (c0,s0)=u9','squares':entries,'exact_root_core_upper_from_transfer':rec['maximum_exact_root_core_from_1_10000'],'parameter_transfer_requires_physical_right_wall_for_a_nonnegative':True,'conclusion':['All45 exact-root core coordinates equal zero','S = S*'],'raw_core_zero_not_claimed':True},'proof_dependencies':{'transfer_review_sha256':sha(transfer/'MANIFEST.json'),'strict_rigidity_review_sha256':sha(rigidity/'MANIFEST.json')},'not_proved_here':{'entry_from_position_1_200_angle_1_400':True,'HW_or_G20S_tree_join':True,'arbitrary_capture':True,'global_optimality':True,'expanded_slider_equality_family_classification':True,'WX_certificate_type_compatibility':True}}
(H/'MATHEMATICAL_INTERFACE.json').write_text(json.dumps(interface,indent=2)+'\n')
controls={'radius_1_4000_is_not_accepted_raw_tube':F(1,4000)>rootradius,'raw_slider_not_in_core':all(w not in core for w in rawbox),'dummy_free4_not_in_core':all(i not in core for i in (6,7,37)),'larger_finite_position_not_in_raw_cube':F(1,200)>rawradius,'larger_finite_angle_not_in_raw_cube':F(1,400)>rawradius,'actual_side_cap_not_replaced':rec['corruption_controls']['rational_cap_cannot_supply_a_nonnegative']}
assert all(controls.values())
out={'status':'ACCEPTED_RATIONAL_SMALL_ENTRY_COROLLARY','transfer_inherited_not_replayed':True,'new_model_solver_symbolic_or_arithmetic_chain_replay':False,'common_physical_domain':common,'raw_core_radius':'1/10000','exact_root_core_bound':rec['maximum_exact_root_core_from_1_10000'],'strictly_below_root_radius':'1/5000','exact_root_parameter_containment':True,'physical_wall_repair_required':True,'source_root_and_reference_equalities_checked':True,'controls':controls,'interface_sha256':sha(H/'MATHEMATICAL_INTERFACE.json'),'cpu_seconds':time.process_time()-start}
(H/'receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'cpu_seconds':out['cpu_seconds'],'interface_sha256':out['interface_sha256']}))
