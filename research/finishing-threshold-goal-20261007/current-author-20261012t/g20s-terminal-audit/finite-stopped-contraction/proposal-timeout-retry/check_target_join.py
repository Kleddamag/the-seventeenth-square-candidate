#!/usr/bin/env python3
"""Exact data join only; finite-bound validity requires the independent replay."""
import hashlib,json,sys
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'local-research/claude-20261002/results/rerun_trees_20261011/SHA256_G20S_HW.txt').is_file())
G=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check():
    cp=HERE/'certificate.json';c=json.loads(cp.read_text())
    inputs=json.loads((HERE/'INPUTS.json').read_text())
    for rel,digest in inputs['files'].items():assert sha(ROOT/rel)==digest
    ip=G/'full-stopped-propagation/rational-entry-review/MATHEMATICAL_INTERFACE.json'
    rp=G/'full-stopped-propagation/rational-entry-review/MANIFEST.json'
    pp=G/'finite-entry-stop-pruning/entry-producer/PRUNING.json'
    interface=json.loads(ip.read_text());pruning=json.loads(pp.read_text())
    assert c['status']=='PRODUCER_TARGET_REACHED_REQUIRES_SEPARATE_REVIEW'
    assert len(c['steps'])==2 and [s['round'] for s in c['steps']]==[16,17]
    assert 'partial_round' not in c
    assert c['final_bounds']==c['steps'][-1]['outgoing_bounds']
    bounds=[tuple(map(F,x)) for x in c['final_bounds']]
    common=interface['common_hypotheses'];entry=interface['rational_entry_scope']
    keys=('actual_unit_squares','distinct_constrained_physical_labels',
      'unrestricted_physical_label','one_common_frame_and_one_injective_label_assignment',
      'zero_based_core_indices','core_position_indices','core_angle_indices',
      'sliders_not_normalized_core')
    for key in keys:assert common[key]==pruning['guards'][key]
    assert c['registry']['core']==common['zero_based_core_indices']
    assert F(entry['all45_core_abs_upper'])==F(1,10000)
    maxcore=max(max(map(abs,bounds[k])) for k in c['registry']['core'])
    assert maxcore<=F(1,10000)
    for key,(lo,hi) in entry['slider_bounds'].items():
        a,b=bounds[int(key)];assert F(lo)<=a<=b<=F(hi)
    assert sha(ROOT/inputs['uniform_path'])==interface['sources']['rational_coordinate_map']['sha256']
    ref=G/'full-gate/producer/instance/upper-packing-certificate.json'
    assert sha(ref)==interface['sources']['rational_reference_file']['sha256']
    return {'status':'EXACT_TARGET_AND_TERMINAL_INTERFACE_JOIN_REQUIRES_SEPARATE_NEW_FINITE_REPLAY',
      'certificate_sha256':sha(cp),'accepted_rational_entry_review_sha256':sha(rp),
      'mathematical_interface_sha256':sha(ip),'accepted_raw_stop_export_sha256':sha(pp),
      'all45_raw_core_radius':str(maxcore),'target':'1/10000',
      'positive_target_slack':str(F(1,10000)-maxcore),
      'same_reference_and_coordinate_map_bytes':True,'same_common_labels_and_physical_guards':True,
      'all_three_raw_slider_intervals_in_terminal_domain':True,
      'conclusion_if_new_finite_replay_accepts':['All45 exact-root core coordinates equal zero','actual S=S*'],
      'hypotheses_still_required':'All17 physical unit squares; same common frame/injective labels; actual S<=S*; accepted original finite entry',
      'not_claimed':['raw core coordinates equal zero','arbitrary capture','entire HW/G20S tree accepted','global optimality']}
if __name__=='__main__':
    result=check();path=HERE/'TARGET_JOIN.json'
    if sys.argv[1:]==['--check']:
        assert json.loads(path.read_text())==result
        print('PASS exact saved-bound terminal join; finite replay remains separate')
    elif not sys.argv[1:]:
        path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'])
    else:raise SystemExit('use no arguments to create or --check for read-only replay')
