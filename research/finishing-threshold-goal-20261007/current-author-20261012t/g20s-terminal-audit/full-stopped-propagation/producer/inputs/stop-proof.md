# Physical stops on the complete padded G20S terminal domain

This is a conditional geometric theorem; independent acceptance is a separate premise.
It proves necessary slider restrictions for actual nonoverlapping unit
squares. It neither contracts a finite window nor proves a normalized LP
bound, terminal equality, capture, or global optimality.

## Exact domain and coordinate convention

Use the exact-root geometry and original labels of the accepted G20S full
analytic gate. Write epsilon0=1/5000 and delta=10^-12. The declared rational
input sliders are

    a in[0,8/25], b in[-1/20,1/5], z in[-1/5,3/40].

The theorem proved here directly allows the larger **exact-root** ranges

    a in[0,8/25+delta],
    b in[-1/20-delta,1/5+delta],
    z in[-1/5-delta,3/40+delta].

These are exactly the padded ranges bound by the accepted full-gate receipt.
The sliders are unscaled physical coordinates, indices2,21,25, respectively;
in particular b+z is not multiplied by the normalization radius. All45
exact-root core coordinates have absolute value at most epsilon, where
0<=epsilon<=epsilon0. Each of the sixteen constrained physical angles is
independent with absolute value at most epsilon. Physical square4 remains
present but is unused by this two-pair implication. Its pose is unrestricted.

The usual application assumes actual S<=S*, but no rational cap substitutes
for S* here. The argument uses the exact-root centre parametrization directly.
A finite/rational-frame application must separately supply its accepted
transfer into this padded root domain and core bound. No new transfer is
claimed. The slider a does not occur in either stop pair, so its full padded
range is retained without an extra restriction.

## Exact reference identities

Let u=(c,s), v=(-s,c), c=(1-t^2)/(1+t^2), s=2t/(1+t^2), where t is the
accepted algebraic root coordinate, and T=c(c+4-S*). Then u,v are exactly
orthonormal. From the unchanged `bridge.layout`, in these coordinates:

    u.P9 = 1/2+cs+2s,       v.P9 = 2c+(c^2-s^2)/2;
    u.P11=c+2s+1/2,         v.P11=v.P9-1;
    u.P13=2c+s+1/2,         v.P13=v.P11-1-T/3.

The P9 formulas follow by substituting P9=((c+s)/2,2+(c+s)/2)
and using c^2+s^2=1. P11/P13 are the displayed rotated coordinates in the
source. These are the previously independently reviewed identities, whose
source/analytic hashes are explicitly bound. `check_stops.py` checks that the
full-gate layout function, reference geometry and exact-root core map remain
identical to these accepted sources; it imports none of their numerical code.

Actual centres are P9+h9, P11+h11*u-b*v and P13+h13*u+z*v, with both
world-coordinate components of h9 and scalars h11,h13 bounded by epsilon.
Writing each directed difference from the first label to the second as
Delta=X*u-N*v gives the exact formulas

    (9,11):  X=c(1-s)+h11-u.h9,  N=1+b+v.h9;
    (11,13): X=c-s+h13-h11,      N=1+T/3-b-z.             (1)

For the reference difference d (core set to zero), the new norm bounds are
||d||<5/4 for(9,11), and ||d||<4/3 for(11,13). The core displacement norms
are at most(5/2)epsilon and2epsilon: the first uses
1+sqrt(2)<5/2, and the second is a single u-direction difference.
The verifier checks the reference norm bounds using exact rational root
enclosures and the **entire padded slider intervals**. The old6/5 bound for
(9,11) fails and is retained as a negative control. The new b+z interval is
also checked to lie inside the old reviewed interval, but the arithmetic
for both new-domain pair guards is recomputed rather than inferred solely
from that inclusion.

## All eight separating alternatives per pair

For either owner o in{i,j}, the four directed normal choices are
R(theta_o)u, -R(theta_o)u, R(theta_o)v, -R(theta_o)v. The separating-axis
theorem ensures that at least one of these eight projections of Delta is at
least the sum of the two square half-widths. Every unit square contains a
radius1/2 disc, so that sum is at least1 on every unit normal.

For a reference unit normal n and Delta=d+dh, the exact rotation norm bound
||R(theta_o)n-n||<=|theta_o| yields

    n_rotated.Delta
      <= sup(n.d)+dr*epsilon+epsilon*(D+dr*epsilon),      (2)

where D and dr are the pair constants above. The script enumerates and
strictly bounds below1 the following six options for each pair:

    owner=i or j, normal=+u,-u,+v.

Both negative-v owner choices are retained. Thus all16 directed alternatives
across the two pairs are accounted for: twelve excluded, four retained.
Angles are never equated or given a common sign. Closed parameter boundaries,
zero angles, coincident owner directions, and exact touching separations are
included. Strict inequalities only exclude options that genuinely cannot
separate. A retained option is not asserted to be attained by a whole packing.

The same exact check proves N>0 on both full padded domains. For the retained
owner o, the projection is N*cos(theta_o)+X*sin(theta_o). Since N>0,
cos(theta_o)<=1 and |sin(theta_o)|<=epsilon imply

    1 <= N*cos(theta_o)+X*sin(theta_o) <= N+epsilon*|X|. (3)

This applies to whichever owner supplies separation; no owner-selection
assumption is needed.

## Uniform stop consequences

The root enclosure proves the strict constants

    c+s<141/100,  |c(1-s)|<277/1000,  |c-s|<129/1000.

For pair(9,11), (1) gives |v.h9|<=(c+s)epsilon and
|X|<277/1000+(241/100)epsilon. Equation(3) therefore gives

    b >= -epsilon*[141/100+277/1000+(241/100)epsilon]
      >= -(17/10)epsilon,

because the bracket is less than17/10 even at epsilon0. For(11,13), the
normal core displacement is **exactly zero**, and
|X|<129/1000+2epsilon<13/100. Hence

    b+z <= T/3+(13/100)epsilon.                         (4)

At epsilon<=1/5000, the exact rational interval checks yield the requested
closed consequences

    b >= -17/50000,
    b+z <= 3/125,
    z <= 1/40.                                        (5)

In fact the last two displayed upper bounds have strict rational slack:
T/3+13/500000<3/125 and T/3+183/500000<1/40.
These are necessary restrictions on complete hypothetical packings, not an
assertion that every slider tuple in the resulting box is feasible. They do
not restore the old a upper, b upper or z lower endpoints.

## Composition and verification scope

The independently accepted full G20S gate supplies the same input/root
conventions and exact source identities. The prior stop review supplies the
already audited general physical argument; this package explicitly rechecks
the new domain and owner coverage, increasing only the deficient norm cap.
All dependency hashes appear in `dependencies.json` and the frozen manifest.

A normalized model that uses b/z as unscaled indices21/25 can add the first
and third bounds in(5), or the stronger correlated bound(4), after its own
physical-to-model map is checked. This proof does not validate a solver result
or claim that adding these bounds excludes the remaining norm face. That is
a separate exact-dual/composition obligation.

Read-only replay from the repository root:

```sh
/usr/bin/python3 -B research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/stop-coupled-finish/stop-producer/check_stops.py --snapshot --check
```

The `--snapshot` flag selects the hash-identical dependency copies under
`inputs/`; without that flag, current repository files must match the same
hashes. The checker uses only Python standard-library rational arithmetic, without
floating inputs, imports of numerical proof engines, native solver calls or
new row/model assembly. Negative controls include the failed old norm cap,
an enlarged epsilon, a still smaller norm cap and three unjustifiably tighter
display bounds. No additional geometric exclusion is asserted.
