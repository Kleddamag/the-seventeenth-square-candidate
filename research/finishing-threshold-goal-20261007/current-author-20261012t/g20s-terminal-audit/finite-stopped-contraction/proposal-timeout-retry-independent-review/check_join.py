#!/usr/bin/env python3
"""Exact data and hypothesis composition only; no model/replay/optimizer."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,time,copy
HERE=Path(__file__).resolve().parent;ROOT=next(p for p in HERE.parents if (p/'local-research/claude-20261002/results/rerun_trees_20261011/SHA256_G20S_HW.txt').is_file());G=HERE.parents[1]
START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def need(x,m):
 if not x:raise ValueError(m)
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
import independent_model as m
r=load(HERE/'receipt.json');need(r['status']=='PASS_EXACT_FINITE_ENTRY_TO_ACCEPTED_RATIONAL_THEOREM','new exact replay')
need(r['terminal_theorem_applied'] and r['target_all45_rawcore_abs_le_1_10000'] and r['excluded_partial_round'] is None,'target and whole rounds')
need([x['round'] for x in r['rounds']]==[16,17] and r['exact_signed_bounds']==184,'new round scope')
small=G/'full-stopped-propagation/rational-entry-review';man=small/'MANIFEST.json'
need(sha(man)=='5a70b980bdf8c519d1bcb19a6f710737e41073e782286f849e9ac62915f3b3cc','accepted rational theorem')
accepted=load(man);need(accepted['status']=='ACCEPTED_RATIONAL_SMALL_ENTRY_COROLLARY_AND_MATHEMATICAL_INTERFACE','accepted theorem status')
for name,h in accepted['files'].items():need(sha(small/name)==h,'accepted rational review file '+name)
i=load(small/'MATHEMATICAL_INTERFACE.json');need(sha(small/'MATHEMATICAL_INTERFACE.json')=='d1aead18ef637439b696c303e050c63afeb9782e326703e7e9c7bd9b70939ff4','accepted interface')
need(i['common_hypotheses']['zero_based_core_indices']==list(m.CORE),'all45 core names')
need(i['common_hypotheses']['core_position_indices']==[k for k in m.CORE if k<34],'29 position names')
need(i['common_hypotheses']['core_angle_indices']==list(m.ANGLES),'16 independent radian angles')
need(i['common_hypotheses']['actual_unit_squares']==17 and i['common_hypotheses']['unrestricted_physical_label']==4,'full17/free4')
rs=i['rational_entry_scope'];need(F(rs['reference_side'])==m.side and rs['all45_core_abs_upper']=='1/10000','raw side and target')
need(rs['conclusion']==['All45 exact-root core coordinates equal zero','S = S*'],'exact-root conclusion only')
need(rs['raw_core_zero_not_claimed'] is True,'raw zero forbidden')
coords=rs['squares'];labels=[j for j in range(1,18) if j!=4]
need([q['label'] for q in coords]==labels,'complete injective constrained role roster')
for q in coords:
 j=q['label']-1
 need(tuple(map(F,q['reference_centre']))==m.points[j],'reference centre '+str(j+1))
 need(tuple(map(F,q['reference_u']))==m.axes[j][0] and tuple(map(F,q['reference_v']))==m.axes[j][1],'reference axes '+str(j+1))
 need(q['angle_coordinate']==34+j and q['independent_angle_radius_radians']=='1/10000','old angle convention')
 if j==1:need(m.H[j]==({},m.var(3)) and m.G[j]==(m.scale(m.var(2),-1),{}),'a formula')
 elif j in (10,12):
  w=21 if j==10 else 25;sgn=-1 if j==10 else 1
  need(m.H[j]==tuple(m.scale(m.var(2*j),x) for x in m.axes[j][0]),'local tangent formula')
  need(m.G[j]==tuple(m.scale(m.var(w),sgn*x) for x in m.axes[j][1]),'local slider formula')
 else:need(m.H[j]==(m.var(2*j),m.var(2*j+1)) and m.G[j]==({},{}),'world coordinate formula')
b=[tuple(map(F,x)) for x in r['final_bounds']];target=F(1,10000)
need(all(max(map(abs,b[j]))<=target for j in m.CORE),'all45 endpoint inclusion')
for j,x in rs['slider_bounds'].items():
 lo,hi=map(F,x);need(lo<=b[int(j)][0]<=b[int(j)][1]<=hi,'raw slider inclusion')
maxcore=max(max(map(abs,b[j])) for j in m.CORE);need(maxcore==F(64007486789,10**15),'exact achieved radius')
# The accepted physical pruning input supplies these cuts from the original entry.
pr=G/'finite-entry-stop-pruning/entry-review/MANIFEST.json'
need(sha(pr)=='1f53aada94731e6d9189efd5833ebf3911b02d311a2616cc5bf1a35ab3cb3f18','raw stop acceptance')
pruning=G/'finite-entry-stop-pruning/entry-producer/PRUNING.json'
need(sha(pruning)=='0a2655c65353b67cfd22ba05b9e84208e9c03c6664c3900ff3f771326ae9eb34','raw stop interface')
ancestry=[]
for folder,digest,rounds in [('independent-review','65ba63fc416b50daf3c179901b059d9e2da6b340c3b70604983aa52931fa86ec',[1,2,3]),('continuation-independent-review','0a8aa22c9c6ba5e7e223669f4dd5891392832b0484e107570d175229016f68ed',list(range(4,10))),('finishing-independent-review','7766e022697c707fb576b9108f7323c99f47dd5e658e6603fa68b22a28857c9f',list(range(10,16)))]:
 p=HERE.parent/folder/'MANIFEST.json';need(sha(p)==digest,'ancestor acceptance')
 ancestry.append({'path':str(p.relative_to(ROOT)),'sha256':digest,'complete_rounds':rounds})
pg=load(pruning)['guards']
need(pg['all17_squares_physically_contained_and_interior_disjoint'] is True and pg['actual_unit_squares']==17,'accepted full17 packing guard')
original=m.initial(False)
need(set(map(int,pg['closed_zero_based_raw_coordinate_bounds']))==set(m.CORE+m.SLIDERS),'full original raw guard roster')
for j,pair in pg['closed_zero_based_raw_coordinate_bounds'].items():need(tuple(map(F,pair))==original[int(j)],'original raw guard endpoint '+j)
common=copy.deepcopy(i['common_hypotheses'])
common.update({'all17_squares_physically_contained_and_interior_disjoint':True,'all17_squares_physically_contained_in_actual_container':True,'all17_squares_pairwise_interior_disjoint':True,'actual_physical_container':'[0,S]^2','frame':pg['frame']})
packing_keys=('all17_squares_physically_contained_and_interior_disjoint','all17_squares_physically_contained_in_actual_container','all17_squares_pairwise_interior_disjoint')
def validate_full_packing_guard(g):
    need(g.get('actual_unit_squares')==17 and g.get('actual_physical_container')=='[0,S]^2','physical parent count/container')
    for key in packing_keys:need(g.get(key) is True,'required full packing guard '+key)
validate_full_packing_guard(common)
guard_controls=[]
for key in packing_keys:
    bad=copy.deepcopy(common);del bad[key]
    try:validate_full_packing_guard(bad)
    except ValueError:guard_controls.append('missing:'+key)
    else:raise ValueError('missing packing guard accepted')
newcoords=copy.deepcopy(coords)
for q in newcoords:q['independent_angle_radius_radians']='1/400';q['core_position_abs_upper']='1/200'
export={'schema':'s17-accepted-finite-entry-mathematical-interface-v1','status':'INDEPENDENTLY_CHECKED_FINITE_ENTRY_TO_EXACT_ROOT_RIGIDITY','kind':'Mathematical theorem interface; not a new WX checker fact or whole-tree receipt','common_hypotheses':common,'reference_sources':i['sources'],'finite_entry':{'frame':'Actual physical [0,S]^2; no implicit fixed-U translation','reference_side':str(m.side),'core_position_abs_upper':'1/200','independent_radian_angle_abs_upper':'1/400','sliders':rs['slider_bounds'],'squares':newcoords,'free_physical_square4_pose_unrestricted':True,'all_boundaries_closed':True,'stop_cuts_are_derived_not_extra_input_hypotheses':True},'verified_finite_output':{'maximum_all45_raw_core_abs':str(maxcore),'maximum_raw_position_abs':'30394903479/1000000000000000','maximum_raw_radian_angle_abs':str(maxcore),'required_small_theorem_radius':'1/10000','strict_radius_slack':str(target-maxcore),'completed_rounds':17,'discarded_old_partial16_used':False},'conclusion':['All45 exact-root core coordinates equal zero','S = S*'],'raw_reference_core_zero_claimed':False,'proof_bindings':{'accepted_raw_stop_review':{'path':str(pr.relative_to(ROOT)),'sha256':sha(pr)},'raw_stop_interface':{'path':str(pruning.relative_to(ROOT)),'sha256':sha(pruning)},'accepted_ancestors':ancestry,'new_exact_replay_receipt_sha256':sha(HERE/'receipt.json'),'new_producer_certificate_sha256':sha(HERE.parent/'proposal-timeout-retry/certificate.json'),'accepted_rational_small_theorem':{'path':str(man.relative_to(ROOT)),'sha256':sha(man)},'accepted_rational_interface':{'path':str((small/'MATHEMATICAL_INTERFACE.json').relative_to(ROOT)),'sha256':sha(small/'MATHEMATICAL_INTERFACE.json')}},'not_claimed':{'HW_or_G20S_tree_arithmetic_or_coverage':True,'global_capture':True,'global_optimality':True,'classification_of_expanded_slider_equality_family':True,'new_WX_fact_rule':True}}
save('MATHEMATICAL_INTERFACE.json',export)
save('join-receipt.json',{'status':'PASS_COMPLETE_FINITE_ENTRY_TO_ACCEPTED_EXACT_ROOT_THEOREM','coordinate_centres_checked':16,'orthonormal_reference_axis_pairs_checked':16,'position_core_count':29,'independent_radian_angle_count':16,'all45_exact_endpoint_inclusions':True,'all3_slider_inclusions':True,'actual_side_premise_preserved':True,'full17_free4_premise_preserved':True,'explicit_all17_containment_and_interior_disjointness_checked':True,'omitted_packing_guard_controls_rejected':guard_controls,'raw_core_zero_not_claimed':True,'maximum_final_core':str(maxcore),'slack_to_small_theorem':str(target-maxcore),'accepted_ancestor_rounds':15,'new_completed_rounds':2,'partial_old16_used':False,'interface_sha256':sha(HERE/'MATHEMATICAL_INTERFACE.json'),'CPU_seconds':time.process_time()-START})
print('PASS finite-entry theorem join; CPU',time.process_time()-START)
