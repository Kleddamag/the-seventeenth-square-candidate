#!/usr/bin/env python3
"""Independent exact stop proof: polynomial projections and complete SAT roster.

No producer imports, floating arithmetic, model, solver, or root proof replay.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import ast,copy,hashlib,json,resource,time,sys
resource.setrlimit(resource.RLIMIT_CPU,(8,10))
HERE=Path(__file__).resolve().parent
P=HERE.parent/'stop-producer'
ROOT=next(p for p in HERE.parents if (p/'local-research/claude-20261002/results/rerun_trees_20261011/SHA256_G20S_HW.txt').is_file())
W=ROOT/'research/finishing-threshold-goal-20261007/current-author-20261012t'
G=W/'g20s-terminal-audit'
EPS=F(1,5000); PAD=F(1,10**12)
PRODUCER='ebcb669d46ea8230bf840c98ff7fb7b0d6980bcce1ea11315a9b9508b9a7c03d'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

# Polynomial ring in c,s,T,h9x,h9y,h11,h13,b,z, modulo c^2+s^2-1.
ZERO=(0,)*9
class Poly:
 def __init__(self,d):self.d={k:F(v) for k,v in d.items() if v}
 @staticmethod
 def cast(x):return x if isinstance(x,Poly) else Poly({ZERO:F(x)})
 def __add__(self,y):
  y=Poly.cast(y);d=dict(self.d)
  for k,v in y.d.items():d[k]=d.get(k,F(0))+v
  return Poly(d)
 __radd__=__add__
 def __neg__(self):return Poly({k:-v for k,v in self.d.items()})
 def __sub__(self,y):return self+-Poly.cast(y)
 def __rsub__(self,y):return Poly.cast(y)+-self
 def __mul__(self,y):
  y=Poly.cast(y);d={}
  for a,x in self.d.items():
   for b,z in y.d.items():
    k=tuple(i+j for i,j in zip(a,b));d[k]=d.get(k,F(0))+x*z
  return Poly(d)
 __rmul__=__mul__
 def __truediv__(self,y):return self*F(1,y)
 def reduced(self):
  d=dict(self.d)
  while any(k[0]>=2 for k in d):
   k=next(k for k in d if k[0]>=2);v=d.pop(k)
   a=list(k);a[0]-=2;a=tuple(a)
   b=list(a);b[1]+=2;b=tuple(b)
   d[a]=d.get(a,F(0))+v;d[b]=d.get(b,F(0))-v
  return {k:v for k,v in d.items() if v}
def variable(i):
 k=list(ZERO);k[i]=1;return Poly({tuple(k):F(1)})
def dot(a,b):return sum((x*y for x,y in zip(a,b)),0)
def identities():
 c,s,T,hx,hy,h11,h13,b,z=[variable(i) for i in range(9)]
 u=(c,s);v=(-s,c);h=(c+s)/2
 U11=c+2*s+F(1,2);V11=2*c+(c*c-s*s)/2-1;U13=2*c+s+F(1,2)
 def R(U,V):return(c*U-s*V,s*U+c*V)
 p9=(h+hx,2+h+hy)
 p11=tuple(R(U11,V11)[k]+h11*u[k]-b*v[k] for k in (0,1))
 p13=tuple(R(U13,V11-1-T/3)[k]+h13*u[k]+z*v[k] for k in (0,1))
 targets=[(p9,p11,c*(1-s)+h11-c*hx-s*hy,1+b-s*hx+c*hy),
          (p11,p13,c-s+h13-h11,1+T/3-b-z)]
 for left,right,X,N in targets:
  delta=tuple(right[k]-left[k] for k in(0,1))
  assert not (dot(u,delta)-X).reduced()
  assert not (-dot(v,delta)-N).reduced()
 return 4

class Iv:
 def __init__(self,a,b=None):
  if isinstance(a,Iv):self.lo,self.hi=a.lo,a.hi
  else:self.lo,self.hi=F(a),F(a if b is None else b)
  assert self.lo<=self.hi
 def __add__(self,b):
  b=Iv(b);return Iv(self.lo+b.lo,self.hi+b.hi)
 __radd__=__add__
 def __neg__(self):return Iv(-self.hi,-self.lo)
 def __sub__(self,b):return self+-Iv(b)
 def __rsub__(self,b):return Iv(b)+-self
 def __mul__(self,b):
  b=Iv(b);x=[p*q for p in (self.lo,self.hi) for q in (b.lo,b.hi)]
  return Iv(min(x),max(x))
 __rmul__=__mul__
 def __truediv__(self,b):
  b=Iv(b);assert b.lo*b.hi>0
  return self*Iv(1/b.hi,1/b.lo)
 def mag(self):return max(abs(self.lo),abs(self.hi))
 def record(self):return[str(self.lo),str(self.hi)]
def func(path,name):
 xs=[x for x in ast.parse(path.read_text()).body if isinstance(x,ast.FunctionDef) and x.name==name]
 assert len(xs)==1
 return ast.dump(xs[0],include_attributes=False)

def arithmetic(rec,D9=F(5,4)):
 expected={'a':['0',str(F(8,25)+PAD)],'b':[str(-F(1,20)-PAD),str(F(1,5)+PAD)],
           'z':[str(-F(1,5)-PAD),str(F(3,40)+PAD)]}
 assert rec['exact_root_padded_sliders']==expected and F(rec['epsilon'])==EPS
 t,beta=[Iv(*p) for p in rec['root_intervals']]
 c=(1-t*t)/(1+t*t);s=2*t/(1+t*t);side=(6+4*t)/(1+2*t-t*t);T=c*(c+4-side)
 assert c.lo>0 and s.lo>0 and (c+s).hi<F(141,100) and T.lo>0
 b,z=Iv(*expected['b']),Iv(*expected['z'])
 oldsum=Iv(-F(201,2500)-PAD,F(49,300)+PAD)+Iv(-F(41,200)-PAD,F(57,400)+PAD)
 newsum=b+z;assert oldsum.lo<=newsum.lo<=newsum.hi<=oldsum.hi
 assert rec['new_b_plus_z_projection']==newsum.record()
 assert rec['old_b_plus_z_projection']==oldsum.record()
 assert rec['T_over_3']==(T/3).record()
 data=[((9,11),c*(1-s),1+b,D9,F(5,2),F(277,1000)),
       ((11,13),c-s,1+T/3-b-z,F(4,3),F(2),F(129,1000))]
 assert [tuple(r['pair'])for r in rec['complete_stop_pairs']]==[d[0]for d in data]
 summaries=[]
 for saved,(pair,X,N,D,dr,cap) in zip(rec['complete_stop_pairs'],data):
  assert X.mag()<cap
  assert X.mag()**2+N.mag()**2<D*D
  assert N.lo-dr*EPS>0
  assert saved['X0']==X.record() and saved['N0']==N.record()
  assert F(saved['D'])==D and F(saved['delta_norm_coefficient'])==dr
  assert F(saved['norm_squared_upper'])==X.mag()**2+N.mag()**2
  assert F(saved['norm_squared_slack'])==D*D-X.mag()**2-N.mag()**2
  assert F(saved['actual_N_lower'])==N.lo-dr*EPS
  allopts=set(product(pair,('u','v'),(-1,1)))
  retained={(o,'v',-1)for o in pair};excluded=allopts-retained
  actual_retained={(r['owner'],r['axis'],r['sign'])for r in saved['retained']}
  actual_excluded={(r['owner'],r['axis'],r['sign'])for r in saved['excluded']}
  assert len(saved['retained'])==2 and actual_retained==retained
  assert len(saved['excluded'])==6 and actual_excluded==excluded
  maxima=[]
  for r in saved['excluded']:
   ref=r['sign']*X if r['axis']=='u' else -N
   upper=ref.hi+dr*EPS+EPS*(D+dr*EPS)
   assert upper<1 and r['reference_projection_interval']==ref.record()
   assert F(r['actual_projection_upper'])==upper and F(r['strict_gap_below_one'])==1-upper
   maxima.append(upper)
  summaries.append({'pair':list(pair),'all8_options':8,'retained_negative_v_owners':list(pair),
    'max_discarded_projection_lt':str(F(7,25) if pair==(9,11) else F(13,100)),
    'actual_max_discarded_projection':str(max(maxima)), 'norm_squared_margin':str(D*D-X.mag()**2-N.mag()**2)})
  assert max(maxima)<(F(7,25) if pair==(9,11) else F(13,100))
 assert (c*(1-s)).lo**2+F(6,5)**2>F(6,5)**2 # old D fails at b=1/5
 assert F(2)<F(3,2)**2  # ||delta9,11|| <= (1+sqrt(2))*epsilon <2.5epsilon
 bcoef=F(141,100)+F(277,1000)+F(241,100)*EPS
 sumcoef=F(129,1000)+2*EPS
 assert bcoef<F(17,10) and sumcoef<F(13,100)
 assert F(rec['b_coefficient_strict_upper'])==bcoef and F(rec['sum_coefficient_strict_upper'])==sumcoef
 blower=-F(17,10)*EPS;sumupper=(T/3).hi+F(13,100)*EPS;zupper=sumupper-blower
 assert rec['stronger_conclusions']=={'b_lower':str(blower),'b_plus_z_upper':str(sumupper),'z_upper':str(zupper)}
 assert blower>=-F(17,50000) and sumupper<F(3,125) and zupper<F(1,40)
 assert rec['simple_closed_conclusions']=={'b_lower':'-17/50000','b_plus_z_upper':'3/125','z_upper':'1/40'}
 return {'pairs':summaries,'b_lower':str(blower),'b_plus_z_upper_below':'3/125','z_upper_below':'1/40',
         'sum_margin':str(F(3,125)-sumupper),'z_margin':str(F(1,40)-zupper),
         'old_6_over_5_norm_cap_invalid':True,'b_coefficient':str(bcoef),'sum_coefficient':str(sumcoef)}

def main():
 start=time.process_time();assert sha(P/'manifest.json')==PRODUCER
 manifest=json.loads((P/'manifest.json').read_text())
 for r in manifest['files']:assert sha(P/r['path'])==r['sha256']
 dep=json.loads((P/'dependencies.json').read_text())
 for path,digest in dep['files'].items():assert sha(ROOT/path)==digest
 full=G/'full-gate'
 gate=json.loads((full/'independent-review/MANIFEST.json').read_text())
 assert gate['status']=='ACCEPTED_COMPLETE_G20S_ANALYTIC_GATE_ROOT_AND_FINITE_OPTION_COVERAGE'
 assert gate['domains']['rational_sliders']=={'a':['0','8/25'],'b':['-1/20','1/5'],'z':['-1/5','3/40']}
 assert gate['domains']['root_epsilon']=='1/5000'
 old=ROOT/'research/uniform-capture-20261007';new=full/'producer/instance/research/uniform-capture-20261007'
 assert (old/'root_geometry.py').read_bytes()==(new/'root_geometry.py').read_bytes()
 assert func(old/'bridge.py','layout')==func(new/'bridge.py','layout')
 assert func(old/'uniform.py','geometry')==func(new/'uniform.py','geometry')
 rec=json.loads((P/'receipt.json').read_text())
 interface=json.loads((P/'terminal-interface.json').read_text())
 assert interface['independent_angle_units']=='radians'
 assert interface['maximum_exact_root_core_radius']=='1/5000'
 assert interface['input_root_slider_intervals']==rec['exact_root_padded_sliders']
 assert interface['unscaled_physical_slider_indices']=={'a':2,'b':21,'z':25}
 assert interface['relevant_core_coordinate_indices']=={'h9x':16,'h9y':17,'h11_along_u':20,'h13_along_u':24,'theta9':42,'theta11':44,'theta13':46}
 assert interface['closed_necessary_linear_constraints']==[
  {'sense':'>=','coefficients':{'21':'1'},'rhs':'-17/50000'},
  {'sense':'<=','coefficients':{'21':'1','25':'1'},'rhs':'3/125'},
  {'sense':'<=','coefficients':{'25':'1'},'rhs':'1/40'}]
 assert interface['stop_sum_stronger_exact_rational_rhs']==rec['stronger_conclusions']['b_plus_z_upper']
 assert interface['LP_exclusion_or_terminal_equality_proved']is False
 root=json.loads((full/'producer/inputs/accepted-gate-receipt.json').read_text())['root']
 assert root['unique_root_in_outer_box']is True and root['intervals']==rec['root_intervals']
 assert rec['unscaled_slider_indices']=={'a':2,'b':21,'z':25}
 symbolic=identities();result=arithmetic(rec)
 rejected=[]
 for name in ('old norm cap','missing owner','changed slider domain','false strict sum target','wrong normal sign','extra epsilon'):
  r=copy.deepcopy(rec);D=F(5,4)
  if name=='old norm cap':D=F(6,5)
  elif name=='missing owner':r['complete_stop_pairs'][0]['retained'].pop()
  elif name=='changed slider domain':r['exact_root_padded_sliders']['b'][1]='49/300'
  elif name=='false strict sum target':r['simple_closed_conclusions']['b_plus_z_upper']='1/50'
  elif name=='wrong normal sign':r['complete_stop_pairs'][1]['excluded'][0]['sign']=1
  else:r['epsilon']='1/100'
  try:arithmetic(r,D)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('accepted corruption '+name)
 result.update(status='ACCEPTED_G20S_PADDED_ROOT_STOP_EXTENSION',producer_manifest_sha256=PRODUCER,
  independent_symbolic_projection_identities=symbolic,corruptions_rejected=rejected,
  whole_closed_box_no_subdivision_or_angle_sign_restriction=True,producer_code_imported=False,
  unscaled_terminal_interface_checked=True,
  new_finite_contraction_or_reference_transfer=False,normalized_dual_or_finishing_theorem=False,
  new_solver_calls=0,cpu_seconds=time.process_time()-start)
 if '--check' in sys.argv:
  saved=json.loads((HERE/'receipt.json').read_text())
  assert {k:v for k,v in saved.items() if k!='cpu_seconds'}=={k:v for k,v in result.items() if k!='cpu_seconds'}
 else:
  (HERE/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items()if k!='pairs'}))
if __name__=='__main__':main()
