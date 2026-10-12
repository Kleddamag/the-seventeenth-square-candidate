#!/usr/bin/env python3
"""Export exact necessary root constraints, without asserting raw-frame transfer."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,sys,time
START=time.process_time();HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((HERE/'receipt.json').read_text())
assert r['status']=='PASS_G20S_FINITE_ENTRY_ROOT_STOPS_REQUIRES_SEPARATE_REVIEW'
assert r['epsilon']=='501/100000'
assert F(r['target_slacks']['b_plus_z_upper'])>0 and F(r['target_slacks']['z_upper'])>0
out={'schema':'s17-finite-entry-root-stop-constraints-v1','status':'PRODUCER_PASS_REQUIRES_SEPARATE_INDEPENDENT_REVIEW',
 'receipt_sha256':sha(HERE/'receipt.json'),'dependencies_sha256':sha(HERE/'dependencies.json'),
 'physical_scope':{'unit_squares':17,'distinct_physical_parents':True,'pairwise_disjoint_interiors':True,
   'original_labels_and_reference':'accepted exact-root G20S geometry',
   'intended_actual_side_hypothesis':'S <= S*; no replacement by Sref',
   'all45_exact_root_core_absolute_bounds':'501/100000','independent_constrained_angles':16,
   'core_position_units':'unit-square side lengths; Cartesian except the declared along-u slider charts',
   'core_coordinates_normalized_by_R':False,
   'angle_units':'radians','unrestricted_physical_label':4},
 'input_exact_root_slider_intervals':r['exact_root_padded_sliders'],
 'unscaled_physical_slider_indices':r['unscaled_slider_indices'],
 'relevant_core_indices':{'h9x':16,'h9y':17,'h11_along_u':20,'h13_along_u':24,'theta9':42,'theta11':44,'theta13':46},
 'closed_necessary_linear_constraints':[
   {'sense':'>=','coefficients':{'21':'1'},'rhs':'-8517/1000000'},
   {'sense':'<=','coefficients':{'21':'1','25':'1'},'rhs':'49/2000'},
   {'sense':'<=','coefficients':{'25':'1'},'rhs':'33/1000'}],
 'stronger_exact_rational_conclusions':r['stronger_conclusions'],
 'strict_upper_target_slacks':{k:r['target_slacks'][k] for k in ('b_plus_z_upper','z_upper')},
 'uniform_analytic_forms':{'b_lower':'-(17/10)*epsilon','b_plus_z_upper':'T/3+(14/100)*epsilon',
  'T':'c*(c+4-S*)','epsilon_interval':['0','501/100000'],'T_over_3_root_enclosure':r['T_over_3']},
 'root_SAT_options':16,'strictly_excluded_options':12,'retained_owner_options':4,
 'raw_coordinate_transfer_proved':False,'finite_contraction_proved':False,'terminal_equality_proved':False,
 'capture_or_optimality_proved':False,
 'guard_before_use':'Independent acceptance plus actual physical pose-to-root domain transfer; never infer guards from relaxed numerical points.'}
if '--check' in sys.argv:assert out==json.loads((HERE/'root-interface.json').read_text())
else:(HERE/'root-interface.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'process_CPU_seconds':time.process_time()}))
