#!/usr/bin/env python3
"""G20S finite-entry root stop guards. Exact rationals, no model/LP import."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import ast,hashlib,json,time,sys,resource,traceback,signal
resource.setrlimit(resource.RLIMIT_CPU,(8,10))
START=time.process_time();WALL=time.monotonic()
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[5]
if '--snapshot'in sys.argv:ROOT=HERE/'inputs'
W=ROOT/'research/finishing-threshold-goal-20261007/current-author-20261012t'
FULL=W/'g20s-terminal-audit/full-gate'
EPS=F(501,100000);PAD=F(1,10**12)
RATIONAL={'a':(F(0),F(8,25)),'b':(-F(1,20),F(1,5)),'z':(-F(1,5),F(3,40))}
PADDED={k:(lo if k=='a'else lo-PAD,hi+PAD)for k,(lo,hi)in RATIONAL.items()}
def need(x,message):
 if not x:raise ValueError(message)
class I:
 def __init__(self,a,b=None):
  if isinstance(a,I):self.lo,self.hi=a.lo,a.hi
  else:self.lo,self.hi=F(a),F(a if b is None else b)
  need(self.lo<=self.hi,'reversed interval')
 def __add__(self,b):
  b=I(b);return I(self.lo+b.lo,self.hi+b.hi)
 __radd__=__add__
 def __neg__(self):return I(-self.hi,-self.lo)
 def __sub__(self,b):return self+-I(b)
 def __rsub__(self,b):return I(b)+-self
 def __mul__(self,b):
  b=I(b);p=[x*y for x in(self.lo,self.hi)for y in(b.lo,b.hi)];return I(min(p),max(p))
 __rmul__=__mul__
 def __truediv__(self,b):
  b=I(b);need(not b.lo<=0<=b.hi,'zero denominator');return self*I(1/b.hi,1/b.lo)
 def mag(self):return max(abs(self.lo),abs(self.hi))
 def record(self):return[str(self.lo),str(self.hi)]
def function_ast(path,name):
 nodes=[x for x in ast.parse(path.read_text()).body if isinstance(x,ast.FunctionDef)and x.name==name]
 need(len(nodes)==1,'unique function '+name);return ast.dump(nodes[0],include_attributes=False)
def load():
 deps=json.loads((HERE/'dependencies.json').read_text())
 for p,h in deps['files'].items():need(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,'changed dependency '+p)
 full=json.loads((FULL/'independent-review/MANIFEST.json').read_text())
 need(full['status']=='ACCEPTED_COMPLETE_G20S_ANALYTIC_GATE_ROOT_AND_FINITE_OPTION_COVERAGE','full gate not accepted')
 need(full['domains']['rational_sliders']=={k:list(map(str,v))for k,v in RATIONAL.items()},'wrong declared sliders')
 # The older small gate supplies identities and domain conventions only.
 # Every new-radius stop/SAT estimate is recomputed below.
 need(full['domains']['root_epsilon']=='1/5000','wrong inherited gate')
 gate=json.loads((FULL/'producer/gate-receipt.json').read_text())
 need(gate['padded_box']=={str(i):list(map(str,PADDED[k]))for k,i in [('a',2),('b',21),('z',25)]},'wrong padded root domain')
 old=ROOT/'research/uniform-capture-20261007';new=FULL/'producer/instance/research/uniform-capture-20261007'
 need((old/'root_geometry.py').read_bytes()==(new/'root_geometry.py').read_bytes(),'root core coordinate map changed')
 need(function_ast(old/'bridge.py','layout')==function_ast(new/'bridge.py','layout'),'algebraic layout changed')
 need(function_ast(old/'uniform.py','geometry')==function_ast(new/'uniform.py','geometry'),'rational geometry changed')
 rr=json.loads((FULL/'producer/inputs/accepted-gate-receipt.json').read_text())['root']
 need(rr['unique_root_in_outer_box']is True,'root existence/uniqueness dependency')
 definition=json.loads((old/'upstream-root-certificate.json').read_text())
 for iv,mid in zip(rr['intervals'],definition['box']['midpoint']):
  lo,hi=map(F,iv);r=F(definition['box']['radius']);m=F(mid)
  need(m-r<lo<hi<m+r,'root enclosure not in declared root box')
 return [I(*v)for v in rr['intervals']]
def stop_checks(root,D9=F(5,4),eps=EPS,bounds=PADDED,sum_coefficient=F(14,100)):
 need(0<=eps<=EPS,'unreviewed epsilon')
 t,beta=root;c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
 S=(6+4*t)/(1+2*t-t*t);T=c*(c+4-S)
 need(c.lo>0 and s.lo>0 and (c+s).hi<F(141,100),'common axes bound')
 need(T.lo>0,'T positivity')
 b=I(*bounds['b']);z=I(*bounds['z']);sum_new=b+z
 sum_old=I(-F(201,2500)-PAD,F(49,300)+PAD)+I(-F(41,200)-PAD,F(57,400)+PAD)
 need(sum_old.lo<=sum_new.lo<=sum_new.hi<=sum_old.hi,'new sum projection not inside old')
 rec=[]
 for pair,X,N,D,dr,cap in [((9,11),c*(1-s),1+b,D9,F(5,2),F(277,1000)),((11,13),c-s,1+T/3-b-z,F(4,3),F(2),F(129,1000))]:
  need(X.mag()<cap,'tangent cap')
  norm2=X.mag()**2+N.mag()**2;need(norm2<D*D,'norm cap fails '+str(pair))
  need(N.lo-dr*eps>0,'actual normal positivity')
  error=dr*eps+eps*(D+dr*eps)
  excluded=[];retained=[]
  for owner,axis,sgn in product(pair,('u','v'),(-1,1)):
   if axis=='v'and sgn==-1:
    retained.append({'owner':owner,'axis':axis,'sign':sgn});continue
   ref=(sgn*X)if axis=='u'else -N
   upper=ref.hi+error;need(upper<1,'SAT alternative not excluded')
   excluded.append({'owner':owner,'axis':axis,'sign':sgn,'reference_projection_interval':ref.record(),'actual_projection_upper':str(upper),'strict_gap_below_one':str(1-upper)})
  need(len(excluded)==6 and len(retained)==2,'complete owner/direction coverage')
  rec.append({'pair':list(pair),'X0':X.record(),'N0':N.record(),'D':str(D),'delta_norm_coefficient':str(dr),'norm_squared_upper':str(norm2),'norm_squared_slack':str(D*D-norm2),'actual_N_lower':str(N.lo-dr*eps),'excluded':excluded,'retained':retained})
 coefficient_b=F(141,100)+F(277,1000)+F(241,100)*EPS
 coefficient_sum=F(129,1000)+2*EPS
 need(coefficient_b<F(17,10) and coefficient_sum<sum_coefficient,'stop coefficient')
 blower=-F(17,10)*eps;sumupper=(T/3+sum_coefficient*eps).hi;zupper=sumupper-blower
 need(blower>=-F(8517,1000000),'target lower b')
 need(sumupper<F(49,2000),'target sum upper')
 need(zupper<F(33,1000),'target z upper')
 return {'status':'PASS_G20S_FINITE_ENTRY_ROOT_STOPS_REQUIRES_SEPARATE_REVIEW','rational_input_sliders':{k:list(map(str,v))for k,v in RATIONAL.items()},'exact_root_padded_sliders':{k:list(map(str,v))for k,v in bounds.items()},'epsilon':str(eps),'unscaled_slider_indices':{'a':2,'b':21,'z':25},'root_intervals':[v.record()for v in root],'c_plus_s':(c+s).record(),'T_over_3':(T/3).record(),'new_b_plus_z_projection':sum_new.record(),'old_b_plus_z_projection':sum_old.record(),'complete_stop_pairs':rec,'b_coefficient_strict_upper':str(coefficient_b),'sum_coefficient_strict_upper':str(coefficient_sum),'chosen_sum_coefficient':str(sum_coefficient),'stronger_conclusions':{'b_lower':str(blower),'b_plus_z_upper':str(sumupper),'z_upper':str(zupper)},'simple_closed_conclusions':{'b_lower':'-8517/1000000','b_plus_z_upper':'49/2000','z_upper':'33/1000'},'target_slacks':{'b_lower':str(blower+F(8517,1000000)),'b_plus_z_upper':str(F(49,2000)-sumupper),'z_upper':str(F(33,1000)-zupper)},'independent_angles':True,'both_owners_and_boundary_degeneracies_retained':True,'new_reference_transfer_or_finite_contraction_claimed':False,'optimizer_or_solver_calls':0}
def main():
 start=time.process_time();root=load();out=stop_checks(root);bad=[]
 for name,kw in [('old D=6/5',{'D9':F(6,5)}),('too large epsilon',{'eps':F(1,100)}),('D9=1',{'D9':F(1)}),('old sum coefficient 13/100',{'sum_coefficient':F(13,100)})]:
  try:stop_checks(root,**kw)
  except ValueError:bad.append(name)
  else:raise ValueError('invalid guard accepted '+name)
 # Closed targets cannot be tightened merely by display rounding.
 a=out['stronger_conclusions']
 need(F(a['b_lower'])<-F(17,2000) and F(a['b_plus_z_upper'])>F(3,125) and F(a['z_upper'])>F(1,40),'target corruption controls')
 out['negative_controls']=bad+['b>=-17/2000 not implied by displayed bound','b+z<=3/125 not implied by displayed bound','z<=1/40 not implied by displayed bound']
 out['cpu_seconds']=round(time.process_time()-start,6)
 if '--check'in sys.argv:
  old=json.loads((HERE/'receipt.json').read_text());need({k:v for k,v in old.items()if k!='cpu_seconds'}=={k:v for k,v in out.items()if k!='cpu_seconds'},'receipt mismatch')
 else:(HERE/'receipt.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'status':out['status'],'cpu_seconds':out['cpu_seconds'],'simple_closed_conclusions':out['simple_closed_conclusions'],'old_D_rejected':'old D=6/5'in bad},indent=2))
if __name__=='__main__':
 status='ERROR'
 def timeout(signum,frame):raise TimeoutError('Producer CPU cap reached')
 signal.signal(signal.SIGXCPU,timeout)
 try:main();status='PASS'
 except BaseException:
  if '--check' not in sys.argv:(HERE/'failure.txt').write_text(traceback.format_exc())
  raise
 finally:
  telemetry={'status':status,'process_CPU_seconds':time.process_time(),'calculation_CPU_seconds':time.process_time()-START,'wall_seconds':time.monotonic()-WALL,'runtime':sys.version,'solver_calls':0}
  if '--check' in sys.argv:print(json.dumps({'replay_telemetry':telemetry}))
  else:(HERE/'telemetry.json').write_text(json.dumps(telemetry,indent=2)+'\n')
