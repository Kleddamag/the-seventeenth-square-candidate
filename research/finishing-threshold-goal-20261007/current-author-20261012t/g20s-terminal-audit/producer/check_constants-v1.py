#!/usr/bin/env python3
"""Tiny G20S source/constant assessment. No model, LP, or certificate replay."""
import hashlib
import json
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

resource.setrlimit(resource.RLIMIT_CPU, (2, 3))
START = time.process_time()
HERE = Path(__file__).resolve().parent
W = HERE.parents[1]
OLD = W / 'claude-extension-audit/terminal-producer'
SNAP = OLD / 'snapshot'
sys.path.insert(0, str(SNAP / 'research/uniform-capture-20261007'))
import uniform as u
import bridge as b

I = b.I
PAD = F(1, 10**12)
BOX = {2: (F(0), F(39,125)), 21: (-F(1,20), F(1,5)), 25: (-F(1,5), F(3,40))}
gate = json.loads((OLD / 'gate-receipt.json').read_text())
root = [I(*v) for v in gate['root']['intervals']]
Sstar, points_star, us, vs = b.layout(*root)
Sref, points, axes, corners, _, _ = u.geometry()

def dot(x, y):
    return sum((I(a)*I(v) for a,v in zip(x,y)), I(0))

# Transfer a hypothetical fully contracted rational core, not an actual new
# finite certificate. The actual future bridge still has to replay its input.
small = F(1,10000)
core = {}
param = {}
padded = {w: (lo if w == 2 else lo-PAD, hi+PAD) for w,(lo,hi) in BOX.items()}
for i in range(17):
    if i == 3:
        continue
    diff = [I(points[i][k])-points_star[i][k] for k in (0,1)]
    if i in (10,12):
        w,sign = (21,-1) if i == 10 else (25,1)
        physical_core = dot(us,diff)+I(-small,small)*dot(us,axes[i][0])+sign*I(*BOX[w])*dot(us,axes[i][1])
        physical_slider = sign*dot(vs,diff)+sign*I(-small,small)*dot(vs,axes[i][0])+I(*BOX[w])*dot(vs,axes[i][1])
        core[str(2*i)] = physical_core.absolute_upper()
        param[str(w)] = physical_slider.record()
        assert padded[w][0] <= physical_slider.lo <= physical_slider.hi <= padded[w][1]
    elif i == 1:
        core['3'] = (diff[1]+I(-small,small)).absolute_upper()
        physical_slider = I(*BOX[2])+Sstar-F(1,2)-points[1][0]
        param['2'] = [str(max(F(0),physical_slider.lo)),str(physical_slider.hi)]
        assert physical_slider.hi <= padded[2][1]
    else:
        for k in (0,1):
            core[str(2*i+k)] = (diff[k]+I(-small,small)).absolute_upper()
    drift = 2*F(gate['root']['tight_root_radius']) if i in range(8,14) or i == 15 else F(0)
    core[str(34+i)] = small+drift
assert set(map(int,core)) == set(u.CORE)
assert max(core.values()) < F(1,5000)
assert max(core.values())-small < F(1,10**15)
assert Sstar.hi < points[1][0]+F(1,2) < Sref
floor_margin = points[7][0]+F(1,2)-F(1,200)-(Sref-F(1,50))
assert floor_margin > F(149,10000)

# Exact old affine offset enclosures plus the explicit endpoint changes.
branches = {}
for row in gate['parallel_branches']:
    lo,hi = map(F,row['tau'])
    pair = tuple(map(int,row['label'].split(':')[1:3]))
    if pair == (2,6):
        lo -= F(39,125)-F(1,4)
    elif pair == (11,12):
        hi += F(1,5)-F(3,20)
    elif pair == (13,14):
        hi += F(1,5)-F(1,8)
    assert (lo >= 0 if row['branch'] == 1 else hi <= 0)
    assert max(abs(lo),abs(hi)) < 1
    branches[':'.join(map(str,pair))] = [str(lo),str(hi)]
assert F(branches['11:12'][0]) > F(3,500)
assert F(branches['13:14'][0]) > F(1,200)
assert max(max(abs(F(v)) for v in row) for row in branches.values()) < F(313,1000)

# The likely first finite-stage obstruction: owner5 +x for pair(5,11).
# First-order Taylor upper envelope, maximizing the true bilinear b*theta
# over b endpoints. This is a single necessary SAT option, not all152 audit.
def competing_upper(r, alpha):
    i,j = 4,10
    n = (F(1),F(0))
    Jn = u.p.turn(n)
    d0 = tuple(points[j][k]-points[i][k] for k in (0,1))
    movement = tuple(-v for v in axes[j][1])
    corner = max(corners[j],key=lambda v:u.p.dot(n,v))
    ndh = r*(1+abs(u.p.dot(n,axes[j][0])))
    dr = u.p.norm_upper(tuple(r*(1+abs(axes[j][0][k])) for k in (0,1)))
    dbox = [max(abs(d0[k]+q*movement[k]) for q in BOX[21]) for k in (0,1)]
    D = u.p.norm_upper(dbox)
    V = u.p.norm_upper(corner)
    values = []
    for q in BOX[21]:
        d = tuple(d0[k]+q*movement[k] for k in (0,1))
        nv = u.p.dot(n,u.p.turn(corner))
        val = u.p.dot(n,d)-F(1,2)-u.p.dot(n,corner)
        val += ndh+alpha*(abs(u.p.dot(Jn,d)+nv)+abs(nv))
        values.append(val)
    error = D*alpha**2/2+alpha*dr+V*(2*alpha)**2/2
    return {'radius':str(r),'angle':str(alpha),'upper':str(max(values)+error),'error':str(error),'D':str(D),'dr':str(dr),'upper_decimal':float(max(values)+error)}

probe = [competing_upper(F(1,200),F(1,400)),competing_upper(F(1,100),F(1,200))]
assert F(probe[0]['upper']) < 0
result = {
 'status':'CONDITIONAL_TRANSFER_AND_BRANCH_CONSTANTS_PASS_SINGLE_OPTION_ONLY',
 'no_model_solver_or_certificate_replay':True,
 'target_slider_box':{str(k):list(map(str,v)) for k,v in BOX.items()},
 'entry_radius':'1/200','entry_angle':'1/400','suggested_finite_exit_core':'1/10000',
 'padded_slider_box':{str(k):list(map(str,v)) for k,v in padded.items()},
 'old_gate_sha256':hashlib.sha256((OLD/'gate-receipt.json').read_bytes()).hexdigest(),
 'side_cap_margin':str(Sref-Sstar.hi),'rational_a_wall_margin':str(points[1][0]+F(1,2)-Sstar.hi),
 'finite_side_floor_margin':str(floor_margin),'root_transferred_core':{k:str(v) for k,v in core.items()},
 'maximum_root_transferred_core':str(max(core.values())),
 'reference_drift_above_input_core':str(max(core.values())-small),
 'root_transferred_sliders':param,'parallel_branches':branches,
 'pair5_11_owner5_x_first_order_upper':probe,
 'still_missing':['complete152 SAT option audit','exact52-label roster equality','new finite certificate','new normalized contraction certificate','full replay and independent review','actual tree terminal joins'],
 'cpu_seconds':time.process_time()-START,
}
(HERE/'constants.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('status','cpu_seconds','pair5_11_owner5_x_first_order_upper')},indent=2))
