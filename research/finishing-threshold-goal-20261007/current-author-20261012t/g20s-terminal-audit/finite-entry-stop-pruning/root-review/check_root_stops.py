#!/usr/bin/env python3
"""Fresh broad-radius stop arithmetic using this reviewer's sealed interval/poly primitives.
No producer imports, LP, model construction, SymPy, or root-proof rerun.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import importlib.util,hashlib,json,resource,time,sys
resource.setrlimit(resource.RLIMIT_CPU,(8,10))
HERE=Path(__file__).resolve().parent
G=HERE.parents[1]
OLD=G/'stop-coupled-finish/stop-review'
P=HERE.parent/'root-producer'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
EXPECTED_OLD='e8af5453f7e97d18ee2dab652644d797218ce2382fb928b53a8cb151cee7645d'
EPS=F(501,100000);PAD=F(1,10**12)

def arithmetic(I,root,eps=EPS,sumcoef=F(14,100),D9=F(5,4)):
 assert eps>0
 t=I(*root[0]);c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
 side=(6+4*t)/(1+2*t-t*t);T=c*(c+4-side)
 assert c.lo>0 and s.lo>0 and (c+s).hi<F(141,100) and T.lo>0
 b=I(-F(1,20)-PAD,F(1,5)+PAD);z=I(-F(1,5)-PAD,F(3,40)+PAD)
 records=[]
 for pair,X,N,D,dr,cap in [((9,11),c*(1-s),1+b,D9,F(5,2),F(277,1000)),
                             ((11,13),c-s,1+T/3-b-z,F(4,3),F(2),F(129,1000))]:
  assert X.mag()<cap and X.mag()**2+N.mag()**2<D**2
  actual_N_lo=N.lo-dr*eps;assert actual_N_lo>0
  roster=[]
  for owner,axis,sgn in product(pair,('u','v'),(-1,1)):
   if axis=='v' and sgn==-1:
    roster.append({'owner':owner,'axis':axis,'sign':sgn,'retained':True});continue
   p=sgn*X if axis=='u' else -N
   upper=p.hi+dr*eps+eps*(D+dr*eps)
   assert upper<1
   roster.append({'owner':owner,'axis':axis,'sign':sgn,'retained':False,'upper':str(upper),'gap_to_one':str(1-upper)})
  assert len(roster)==8 and sum(r['retained']for r in roster)==2
  records.append({'pair':list(pair),'D':str(D),'dr':str(dr),'X0':X.record(),'N0':N.record(),
                  'actual_N_strict_lower':str(actual_N_lo),'norm_squared_margin':str(D**2-X.mag()**2-N.mag()**2),'options':roster})
 assert F(2)<F(3,2)**2
 bcoef=F(141,100)+F(277,1000)+F(241,100)*eps
 tang=F(129,1000)+2*eps
 assert bcoef<F(17,10) and tang<sumcoef
 blo=-F(17,10)*eps;sm=(T/3).hi+sumcoef*eps;zu=sm-blo
 assert blo==-F(8517,1000000) and sm<F(49,2000) and zu<F(33,1000)
 return {'epsilon':str(eps),'padded_root_sliders':{'a':['0',str(F(8,25)+PAD)],'b':b.record(),'z':z.record()},
  'pairs':records,'root_intervals':root,'T_over_3':(T/3).record(),
  'b_coefficient_upper':str(bcoef),'b_coefficient_slack_to_17_over_10':str(F(17,10)-bcoef),
  'tangential_coefficient_upper':str(tang),'sum_coefficient':'7/50','tangential_slack_to_14_over_100':str(sumcoef-tang),
  'stronger_bounds':{'b_lower':str(blo),'b_plus_z_upper':str(sm),'z_upper':str(zu)},
  'parametric_bounds':{'b_lower':'-(17/10)*epsilon','b_plus_z_upper':'T/3+(7/50)*epsilon','z_upper':'T/3+(46/25)*epsilon'},
  'simple_bounds':{'b_lower':'-8517/1000000','b_plus_z_upper':'49/2000','z_upper':'33/1000'},
  'strict_slacks':{'sum':str(F(49,2000)-sm),'z':str(F(33,1000)-zu)},
  'decimal_display':{'sum_upper':float(sm),'z_upper':float(zu),'sum_slack':float(F(49,2000)-sm),'z_slack':float(F(33,1000)-zu)}}

def main():
 start=time.process_time();assert sha(OLD/'manifest.json')==EXPECTED_OLD
 old=json.loads((OLD/'manifest.json').read_text())
 for f in old['files']:assert sha(OLD/f['path'])==f['sha256']
 spec=importlib.util.spec_from_file_location('own_accepted_stop_primitives',OLD/'check.py')
 own=importlib.util.module_from_spec(spec);spec.loader.exec_module(own)
 assert own.identities()==4
 oldrec=json.loads((G/'stop-coupled-finish/stop-producer/receipt.json').read_text())
 assert sha(G/'stop-coupled-finish/stop-producer/receipt.json')=='e4e7a631108bdea1bcbd368c99af5e6d504dc3f3b20c6d566b54061b637c1f9b'
 result=arithmetic(own.Iv,oldrec['root_intervals'])
 controls=[]
 for name,kwargs in [('old_13_over_100',{'sumcoef':F(13,100)}),('old_norm_6_over_5',{'D9':F(6,5)}),('radius_1_over_100',{'eps':F(1,100)})]:
  try:arithmetic(own.Iv,oldrec['root_intervals'],**kwargs)
  except AssertionError:controls.append(name)
  else:raise AssertionError('accepted bad claim '+name)
 result.update(status='INDEPENDENT_BROAD_ROOT_STOP_ARITHMETIC_PASS_PRODUCER_BINDING_SEPARATE_OBLIGATION',
  reference_independent_review_sha256=EXPECTED_OLD,reference_own_source_sha256=sha(OLD/'check.py'),
  independent_projection_identities=4,all_SAT_options=16,strictly_excluded=12,retained_negative_v_owners=4,
  corruption_controls_rejected=controls,producer_code_imported=False,
  no_new_finite_entry_or_rigidity_claim=True,new_LP_or_model_calls=0,CPU_seconds=time.process_time()-start)
 path=HERE/'arithmetic-receipt.json'
 if '--check' in sys.argv:
  saved=json.loads(path.read_text());assert {k:v for k,v in saved.items()if k!='CPU_seconds'}=={k:v for k,v in result.items()if k!='CPU_seconds'}
 else:path.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k]for k in ('status','b_coefficient_upper','tangential_coefficient_upper','decimal_display','CPU_seconds')}))
if __name__=='__main__':main()
