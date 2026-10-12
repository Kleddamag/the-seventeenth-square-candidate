#!/usr/bin/env python3
"""Exact closed-entry reference transfer; no model, LP, tree or SymPy call."""
import hashlib,json,resource,sys,time
from fractions import Fraction as F
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(7,8))
start=time.process_time();here=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
prep=json.loads((here/'preparation.json').read_text())
for v in prep['files']:assert sha(here/v['path'])==v['sha256']
sys.path.insert(0,str(here/'instance/research/uniform-capture-20261007'))
import bridge as bridge
I=bridge.I
raw=json.loads((here/'inputs/raw-reference-interface.json').read_text())
raw_review=json.loads((here/'inputs/raw-reference-review.json').read_text())
assert sha(here/'inputs/raw-reference-interface.json')==raw_review['files']['MATHEMATICAL_INTERFACE.json']
gate=json.loads((here/'inputs/accepted-root-gate.json').read_text())
root=[I(*v) for v in gate['root']['intervals']]
Sstar,pstar,us,vs=bridge.layout(*root)
rows=raw['rational_entry_scope']['squares']
points={v['label']:tuple(map(F,v['reference_centre'])) for v in rows}
axes={v['label']:(tuple(map(F,v['reference_u'])),tuple(map(F,v['reference_v']))) for v in rows}
Sref=F(raw['rational_entry_scope']['reference_side'])
core_indices=set(raw['common_hypotheses']['zero_based_core_indices'])
box={int(k):tuple(map(F,v)) for k,v in prep['raw_slider_box'].items()}
pad=F(1,10**12);padded={w:(lo if w==2 else lo-pad,hi+pad) for w,(lo,hi) in box.items()}
r=F(1,200);alpha=F(1,400);eps=F(501,100000)
def dot(x,y):return sum((I(a)*I(b) for a,b in zip(x,y)),I(0))
core={};sliders={};errors={};matrix_records={}
for label in sorted(points):
    i=label-1;diff=tuple(I(points[label][k])-pstar[i][k] for k in (0,1))
    if label in (11,13):
        w,sign=(21,-1) if label==11 else (25,1)
        uu=dot(us,axes[label][0]);uv=dot(us,axes[label][1])
        vu=dot(vs,axes[label][0]);vv=dot(vs,axes[label][1])
        hp=dot(us,diff)+I(-r,r)*uu+sign*I(*box[w])*uv
        # Preserve the same raw slider when bounding its transfer error.
        err=sign*dot(vs,diff)+sign*I(-r,r)*vu+I(*box[w])*(vv-1)
        wp=I(*box[w])+err
        core[str(2*i)]=hp.absolute_upper();sliders[str(w)]=wp.record();errors[str(w)]=err.record()
        matrix_records[str(label)]={'reference_delta':[v.record() for v in diff],
          'u_star_dot_u_raw':uu.record(),'u_star_dot_v_raw':uv.record(),
          'v_star_dot_u_raw':vu.record(),'v_star_dot_v_raw':vv.record(),
          'core_interval':hp.record(),'slider_error':err.record()}
        assert padded[w][0]<=wp.lo<=wp.hi<=padded[w][1]
    elif label==2:
        core['3']=(diff[1]+I(-r,r)).absolute_upper()
        err=Sstar-F(1,2)-points[2][0]
        wp=I(*box[2])+err
        # The lower endpoint0 uses the actual right wall and S<=S*, not rounding.
        sliders['2']=[str(max(F(0),wp.lo)),str(wp.hi)];errors['2']=err.record()
        assert wp.hi<=padded[2][1]
    else:
        for k in (0,1):core[str(2*i+k)]=(diff[k]+I(-r,r)).absolute_upper()
    drift=2*F(gate['root']['tight_root_radius']) if 9<=label<=14 or label==16 else F(0)
    core[str(34+i)]=alpha+drift
assert set(map(int,core))==core_indices and len(core)==45
assert all(v<eps for v in core.values())
assert all(max(abs(F(v)) for v in e)<F(1,10**15) for e in errors.values())
assert Sstar.hi<points[2][0]+F(1,2)<Sref
floor_margin=points[8][0]+F(1,2)-r-(Sref-F(1,50))
assert floor_margin>F(149,10000)

# These comparisons are conditional arithmetic until the new physical stop
# proof at eps is independently accepted and bound by export.py.
c,s=us;T=c*(c+4-Sstar)
root_b_lower=-F(17,10)*eps
strict_sum_upper=T.hi/3+F(14,100)*eps
strict_z_upper=strict_sum_upper-root_b_lower
eb=I(*errors['21']);ez=I(*errors['25'])
raw_b_lower=root_b_lower-eb.hi
raw_sum_upper=strict_sum_upper-(eb+ez).lo
raw_z_upper=strict_z_upper-ez.lo
slacks={'b':raw_b_lower-(-F(213,25000)),
        'sum':F(49,2000)-raw_sum_upper,'z':F(33,1000)-raw_z_upper}
assert all(v>0 for v in slacks.values())
out={'status':'EXACT_TRANSFER_PASS_CUT_COMPOSITION_REQUIRES_SEPARATE_ROOT_STOP_ACCEPTANCE',
 'raw_entry':{'position_radius':str(r),'independent_angle_radius':str(alpha),
              'sliders':{str(k):list(map(str,v)) for k,v in box.items()}},
 'root_epsilon':str(eps),'root_core_bounds':{k:str(v) for k,v in core.items()},
 'maximum_root_core_bound':str(max(core.values())),
 'root_core_margin':str(eps-max(core.values())),
 'root_slider_intervals':sliders,'root_slider_error_intervals':errors,
 'slider_error_uniform_abs_bound':'1/1000000000000000',
 'root_slider_pads':{str(k):list(map(str,v)) for k,v in padded.items()},
 'matrix_records':matrix_records,'a_root_lower_uses_actual_right_wall':True,
 'a_raw_wall_margin':str(points[2][0]+F(1,2)-Sstar.hi),
 'finite_side_floor_margin':str(floor_margin),
 'conditional_root_bounds':{'b_lower':str(root_b_lower),'strict_sum_upper':str(strict_sum_upper),
                            'strict_z_upper':str(strict_z_upper)},
 'raw_necessary_bounds':{'b_lower':str(raw_b_lower),'sum_upper':str(raw_sum_upper),'z_upper':str(raw_z_upper)},
 'exported_cutoffs':{'b_lower':'-213/25000','sum_upper':'49/2000','z_upper':'33/1000'},
 'strict_export_slacks':{k:str(v) for k,v in slacks.items()},
 'no_finite_contraction_or_terminal_reach_claim':True,'no_model_optimizer_tree_symbolic_call':True,
 'CPU_seconds':time.process_time()-start}
(here/'transfer-receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'CPU_seconds':out['CPU_seconds'],
 'maximum_root_core_bound_decimal':float(max(core.values())),
 'slider_error_abs_decimal':{k:max(abs(float(F(v))) for v in e) for k,e in errors.items()},
 'strict_export_slacks_decimal':{k:float(v) for k,v in slacks.items()}},indent=2))
