#!/usr/bin/env python3
"""Exact light checks for padded-slider terminal stop lemma; no optimization."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,sys,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'research/uniform-capture-20261007'))
import uniform as u,bridge,root_geometry as g,rigidity as r
I=bridge.I
PAD=F(1,10**12);EPS=F(1,5000)
INPUT={2:(F(0),F(33,100)),21:(-F(201,2500),F(49,300)),25:(-F(41,200),F(57,400))}
BROAD={k:(lo if k==2 else lo-PAD,hi+PAD)for k,(lo,hi)in INPUT.items()}
STOPPED={2:BROAD[2],21:(-F(17,10)*EPS,BROAD[21][1]),25:(BROAD[25][0],F(1,40))}
def dot(a,b):return sum((x*y for x,y in zip(a,b)),I(0))
def initial(params):
 bs=u.initial_bounds(F(1),1);bs[51]=(F(-1),F(0))
 for k,v in params.items():bs[k]=v
 return u.refresh_products(bs)
def main():
 start=time.process_time();root,rr=bridge.root_enclosure();data=g.geometry(*root)
 S,ps,axes,corners,H,G=data;c,s=axes[8][0];T=c*(c+4-S)
 import sympy as sy
 t,be=sy.symbols('t beta');sd=g.geometry(t,be);Ss,sp,sa,_,_,_=sd;cs,ss=sa[8][0];Ts=cs*(cs+4-Ss)
 identities=[]
 for i,j,wanted in [(8,10,-1),(10,12,-1-Ts/3)]:
  result=sy.cancel(sum(sa[8][1][k]*(sp[j][k]-sp[i][k])for k in(0,1))-wanted)
  assert result==0
  identities.append({'pair':[i+1,j+1],'v_projection':str(wanted),'symbolic_difference':str(result)})
 assert (c+s).hi<F(141,100)
 assert T.lo>0 and (T/3+F(183,100)*EPS).hi<F(1,40)
 bounds=initial(BROAD);stop_records=[]
 for i,j,D,dr in [(8,10,F(6,5),F(5,2)),(10,12,F(4,3),F(2))]:
  d=[ps[j][k]-ps[i][k]+r.interval(u.add_vectors(G[j][k],u.scaled(G[i][k],-1)),bounds)for k in(0,1)]
  # The common u,v frame eliminates interval dependency of rotations.
  du=dot(axes[i][0],[ps[j][k]-ps[i][k]for k in(0,1)])
  if i==8:dv=-1-I(*BROAD[21])
  else:dv=-1-T/3+I(*BROAD[21])+I(*BROAD[25])
  assert (-dv).lo-dr*EPS>0
  assert du.absolute_upper()<(F(277,1000) if i==8 else F(129,1000))
  maxnorm2=du.absolute_upper()**2+dv.absolute_upper()**2
  assert maxnorm2<D*D
  excluded=[]
  for an,sgn in [(0,-1),(0,1),(1,1)]:
   proj=sgn*(du if an==0 else dv)
   # Every owner differs from its common reference by <= EPS.
   upper=proj.hi+dr*EPS+EPS*(D+dr*EPS)
   assert upper<1
   excluded.append({'axis':an,'sign':sgn,'owners':[i+1,j+1],'gap_upper':str(upper-1)})
  stop_records.append({'pair':[i+1,j+1],'u_projection':du.record(),'v_projection':dv.record(),'D':str(D),'dr':str(dr),'norm_squared_upper':str(maxnorm2),'six_excluded_options':excluded})
 assert F(141,100)+F(277,1000)+(1+F(141,100))*EPS<F(17,10)
 assert F(129,1000)+2*EPS<F(13,100)
 # Uniform rational-to-root map at rational core radius 1/6000.
 ref,p,ra,*_=u.geometry();max_core_drift=F(0);param_drift={}
 for i in range(17):
  if i==3:continue
  dd=[I(p[i][k])-ps[i][k]for k in(0,1)]
  if i in(10,12):
   w=21 if i==10 else 25;sgn=-1 if i==10 else 1
   cross=dot(axes[i][0],ra[i][1]).absolute_upper()
   err=dot(axes[i][0],dd).absolute_upper()+max(map(abs,INPUT[w]))*cross
   max_core_drift=max(max_core_drift,err)
   off=sgn*dot(axes[i][1],dd)
   cross2=sgn*dot(axes[i][1],ra[i][0])*I(-F(1,6000),F(1,6000))
   along=dot(axes[i][1],ra[i][1])-1
   drift=off+cross2+along*I(*INPUT[w]);param_drift[str(w)]=drift.record();assert drift.absolute_upper()<PAD
  else:max_core_drift=max(max_core_drift,*(x.absolute_upper()for x in dd))
 a_drift=S-F(1,2)-p[1][0];param_drift['2']=a_drift.record();assert a_drift.absolute_upper()<PAD
 max_core_drift=max(max_core_drift,2*F(rr['tight_root_radius']))
 assert F(1,6000)+max_core_drift<EPS
 # Existing root terminal choices and remainder guards over stopped broad box.
 labels=g.tight_labels();saved=r.initial;r.initial=lambda:initial(STOPPED)
 options=r.option_audit(data,EPS,labels);rows=r.model(r.initial(),EPS,data,labels)
 branch=[]
 for lab in labels:
  if not lab.startswith('parallel:'):continue
  _,_,_,ex=g.row(lab,data);tau=I(ex['tau'])+r.interval(ex['tauw'],r.initial())
  branch.append({'label':lab,'tau':tau.record(),'branch':ex['branch']})
 r.initial=saved
 out={'schema':'s17-padded-terminal-stops-v1','status':'PASS','claim':'Stop, root-transfer and terminal model guards only; no rigidity dual or finite contraction claim','epsilon':str(EPS),'rational_core_input':'1/6000','input_parameters':{str(k):list(map(str,v))for k,v in INPUT.items()},'broad_root_parameters':{str(k):list(map(str,v))for k,v in BROAD.items()},'stopped_root_parameters':{str(k):list(map(str,v))for k,v in STOPPED.items()},'identities':identities,'T_over_3':(T/3).record(),'c_plus_s':(c+s).record(),'stop_checks':stop_records,'stop_conclusions':['b >= -(17/10) epsilon','b+z <= T/3 + (13/100) epsilon'],'root_parameter_drift':param_drift,'maximum_core_reference_drift':str(max_core_drift),'terminal_model':{'labels':len(labels),'pairs':len(options),'rows':len(rows),'row_sha256':hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),'branches':branch},'cpu_seconds':time.process_time()-start,'dependencies':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in[Path(u.__file__),Path(bridge.__file__),Path(g.__file__),Path(r.__file__),u.p.SOURCE,Path(__file__)]}}
 (HERE/'stop-receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in['status','cpu_seconds','maximum_core_reference_drift']},indent=2))
if __name__=='__main__':main()
