#!/usr/bin/env python3
"""Bind independently recomputed broad stop arithmetic to the frozen producer."""
from pathlib import Path
from fractions import Fraction as F
import ast,copy,hashlib,json,resource,sys,time
resource.setrlimit(resource.RLIMIT_CPU,(8,10))
H=Path(__file__).resolve().parent;P=H.parent/'root-producer';ROOT=next(p for p in H.parents if(p/'local-research/claude-20261002/results/rerun_trees_20261011/SHA256_G20S_HW.txt').is_file())
SHA='5a3aab61d2a5f5b08090fc4fc8e0ad67482007b06e370d0cbdc4db255cdf9ead'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def check_receipt(p,a):
 assert p['epsilon']==a['epsilon']=='501/100000'
 assert p['root_intervals']==a['root_intervals'] and p['T_over_3']==a['T_over_3']
 assert p['exact_root_padded_sliders']==a['padded_root_sliders']
 assert p['rational_input_sliders']=={'a':['0','8/25'],'b':['-1/20','1/5'],'z':['-1/5','3/40']}
 assert p['unscaled_slider_indices']=={'a':2,'b':21,'z':25}
 for key,ind in [('b_coefficient_strict_upper','b_coefficient_upper'),('sum_coefficient_strict_upper','tangential_coefficient_upper'),('chosen_sum_coefficient','sum_coefficient')]:assert p[key]==a[ind]
 assert p['stronger_conclusions']==a['stronger_bounds'] and p['simple_closed_conclusions']==a['simple_bounds']
 assert p['target_slacks']['b_plus_z_upper']==a['strict_slacks']['sum'] and p['target_slacks']['z_upper']==a['strict_slacks']['z']
 assert len(p['complete_stop_pairs'])==2
 for r,v in zip(p['complete_stop_pairs'],a['pairs']):
  assert r['pair']==v['pair'] and r['D']==v['D'] and r['delta_norm_coefficient']==v['dr']
  for q in('X0','N0'):assert r[q]==v[q]
  assert r['norm_squared_slack']==v['norm_squared_margin'] and r['actual_N_lower']==v['actual_N_strict_lower']
  roster={(o['owner'],o['axis'],o['sign']):o for o in v['options']}
  kept={(o['owner'],o['axis'],o['sign'])for o in r['retained']}
  gone={(o['owner'],o['axis'],o['sign'])for o in r['excluded']}
  assert len(r['retained'])==2 and len(r['excluded'])==6 and kept.isdisjoint(gone) and kept|gone==set(roster)
  for k,o in roster.items():
   assert o['retained']==(k in kept)
  for o in r['excluded']:
   k=o['owner'],o['axis'],o['sign'];q=roster[k]
   assert o['actual_projection_upper']==q['upper'] and o['strict_gap_below_one']==q['gap_to_one']
 assert p['independent_angles']is True and p['both_owners_and_boundary_degeneracies_retained']is True
 assert p['new_reference_transfer_or_finite_contraction_claimed']is False

def check_interface(i,a):
 assert i['receipt_sha256']==sha(P/'receipt.json') and i['dependencies_sha256']==sha(P/'dependencies.json')
 s=i['physical_scope'];assert s['unit_squares']==17 and s['distinct_physical_parents']is True and s['pairwise_disjoint_interiors']is True
 assert s['all45_exact_root_core_absolute_bounds']=='501/100000' and s['independent_constrained_angles']==16 and s['angle_units']=='radians' and s['unrestricted_physical_label']==4 and s['core_coordinates_normalized_by_R']is False
 assert i['input_exact_root_slider_intervals']==a['padded_root_sliders']
 assert i['unscaled_physical_slider_indices']=={'a':2,'b':21,'z':25}
 assert i['relevant_core_indices']=={'h9x':16,'h9y':17,'h11_along_u':20,'h13_along_u':24,'theta9':42,'theta11':44,'theta13':46}
 assert i['closed_necessary_linear_constraints']==[{'sense':'>=','coefficients':{'21':'1'},'rhs':'-8517/1000000'},{'sense':'<=','coefficients':{'21':'1','25':'1'},'rhs':'49/2000'},{'sense':'<=','coefficients':{'25':'1'},'rhs':'33/1000'}]
 assert i['stronger_exact_rational_conclusions']==a['stronger_bounds']
 assert i['strict_upper_target_slacks']=={'b_plus_z_upper':a['strict_slacks']['sum'],'z_upper':a['strict_slacks']['z']}
 u=i['uniform_analytic_forms'];assert u['b_lower']=='-(17/10)*epsilon' and u['b_plus_z_upper']=='T/3+(14/100)*epsilon' and u['T']=='c*(c+4-S*)' and u['epsilon_interval']==['0','501/100000'] and u['T_over_3_root_enclosure']==a['T_over_3']
 for k in('raw_coordinate_transfer_proved','finite_contraction_proved','terminal_equality_proved','capture_or_optimality_proved'):assert i[k]is False

def function(p,n):
 a=[x for x in ast.parse(p.read_text()).body if isinstance(x,ast.FunctionDef)and x.name==n];assert len(a)==1;return ast.dump(a[0],include_attributes=False)
def main():
 st=time.process_time();assert sha(P/'manifest.json')==SHA
 for file,digest in {'PROOF.md':'62a0c88675cb34b427087793cac3af27d4f2ac62b6ba720bd09ac2debab719a4','check_stops.py':'2b39c67e67568c68c2fc24310050976949268cfc6e66110633daba340168972f','dependencies.json':'4b2a990bc565ba455546dc4871461d58f54a2c6312fd1d54b4d4b0e9ae5b3347','receipt.json':'980aec13f9ea60c72fbd0dff0443240c4adef6590fa236af252c4de4f96ad10a','root-interface.json':'c0a2e20edd832648f44edef6e0ee83507a7e6acd91e83785c0ccd10a3958bc0e'}.items():assert sha(P/file)==digest
 m=load(P/'manifest.json')
 for f in m['files']:assert sha(P/f['path'])==f['sha256']
 deps=load(P/'dependencies.json')
 for name,digest in deps['files'].items():assert sha(ROOT/name)==sha(P/'inputs'/name)==digest
 a=load(H/'arithmetic-receipt.json');p=load(P/'receipt.json');i=load(P/'root-interface.json')
 check_receipt(p,a);check_interface(i,a)
 full=ROOT/'research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/full-gate'
 assert load(full/'producer/inputs/accepted-gate-receipt.json')['root']['intervals']==a['root_intervals']
 old=ROOT/'research/uniform-capture-20261007';new=full/'producer/instance/research/uniform-capture-20261007'
 assert function(old/'bridge.py','layout')==function(new/'bridge.py','layout')
 assert function(old/'uniform.py','geometry')==function(new/'uniform.py','geometry')
 assert (old/'root_geometry.py').read_bytes()==(new/'root_geometry.py').read_bytes()
 rejected=[]
 for name in('missing_owner','changed_normal_sign','old_coefficient_interface','scaled_slider_index'):
  badp=copy.deepcopy(p);badi=copy.deepcopy(i)
  if name=='missing_owner':badp['complete_stop_pairs'][0]['retained'].pop()
  elif name=='changed_normal_sign':badp['complete_stop_pairs'][0]['retained'][0]['sign']=1
  elif name=='old_coefficient_interface':badi['uniform_analytic_forms']['b_plus_z_upper']='T/3+(13/100)*epsilon'
  else:badi['unscaled_physical_slider_indices']['b']=20
  try:check_receipt(badp,a);check_interface(badi,a)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('accepted corruption '+name)
 out={'status':'ACCEPTED_G20S_BROAD_ROOT_STOP_THEOREM','producer_manifest_sha256':SHA,
  'arithmetic_receipt_sha256':sha(H/'arithmetic-receipt.json'),'root_interface_sha256':sha(P/'root-interface.json'),
  'checked_all16_SAT_options':True,'both_retained_owners_each_pair':True,'full_closed_padded_domain':True,
  'new_radius':'501/100000','parametric_sum_coefficient':'7/50','stronger_rational_bounds_bound':True,
  'source_geometry_layout_and_core_map_unchanged':True,'unscaled_slider_indices_checked':True,
  'negative_binding_controls_rejected':rejected,'producer_source_imported':False,
  'raw_reference_transfer_accepted':False,'larger_radius_rigidity_claimed':False,'finite_contraction_or_global_capture_claimed':False,
  'new_LP_or_model_calls':0,'CPU_seconds':time.process_time()-st}
 f=H/'binding-receipt.json'
 if '--check'in sys.argv:
  old=load(f);assert {k:v for k,v in old.items()if k!='CPU_seconds'}=={k:v for k,v in out.items()if k!='CPU_seconds'}
 else:f.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
