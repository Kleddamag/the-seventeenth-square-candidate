# Padded-slider terminal bridge — 8 October 2026

Status: the stop lemma and uniform coordinate transfer below have exact arithmetic
receipts and await separate review. The new all-scale rigidity certificate is NOT
proved: reusing the four old rounds' dual weights gives maximum normalized core
radius exactly one. No finite contraction of padded tube A has yet been proved.
No optimization was run for this investigation.

## Scope and input

Use the exact-root coordinates and labels of the accepted local theorem. All 16
non-rattler angles remain independent. Square 4 is physically present but unused
by this necessary relaxation. Actual side satisfies S <= S*. The rational-frame
padded ranges requested here are

    a in [0,33/100], b in [-201/2500,49/300], z in [-41/200,57/400].

The exact-root transfer permits a further 10^-12 on every endpoint except the
physical lower wall a >= 0. This extra padding is included in every check below.
Assume all 45 exact-root core coordinates have absolute value <= epsilon, where
0 < epsilon <= 1/5000. These are terminal assumptions; they do not follow just
from membership in a position-radius 0.08 window.

## Complete stop-pair lemma

Let u=(c,s), v=(-s,c) be the common exact-root axes of squares 9, 11, and 13.
Write relative centre vectors as d+delta and let n=-v. Algebraic identities give

    n.d(9,11) = 1+b,
    n.d(11,13) = 1+T/3-b-z,
    T=c(c+4-S*).

Every square contains a disc of radius 1/2. Hence separation along any unit
axis requires projected centre difference at least 1. At either stop pair,
check_stops.py excludes both signs of u and the positive-v normal for BOTH
owners, on the whole padded slider box and all independent angles. It does so
by the safe upper bound

    reference projection + dr*epsilon + epsilon*(D+dr*epsilon) < 1.

Here D bounds ||d||, and dr*epsilon bounds ||delta||. The checked choices are
D=6/5, dr=5/2 for (9,11), and D=4/3, dr=2 for (11,13). Thus every non-overlapping
physical pair uses n rotated by one of its two owner angles. Boundaries and
coincident owner directions are retained; a strict inequality is used only to
exclude the other six alternatives.

Write N=n.(d+delta) and X=u.(d+delta). The script checks N>0 on the whole
padded box. If the surviving owner angle is theta, separation and disc support
imply

    1 <= N*cos(theta)+X*sin(theta) <= N+epsilon*|X|.

For (9,11), |n.delta| <= (c+s)*epsilon and
|X| <= |u.d|+(1+c+s)*epsilon. Exact enclosures give

    c+s < 141/100, |u.d| < 277/1000,
    141/100 + 277/1000 + (241/100)/5000 < 17/10.

Therefore b >= -(17/10)*epsilon. For (11,13), n.delta=0 exactly because
both core displacements are along u, and |X| <= 129/1000+2*epsilon < 13/100.
Therefore

    b+z <= T/3+(13/100)*epsilon.

At epsilon=1/5000 these give b >= -17/50000 = -0.00034 (which is already
inside the OLD lower b stop), and z <= T/3+183/500000 < 1/40. The pairwise
constraint b+z is stronger than the box consequence and may be retained by a
future normalized model. No claim that the full rectangular slider box is
physically feasible is made.

## Exact stopped terminal domain

A convenient containing box for the next all-scale proof is

    a in [0,33/100+10^-12],
    b in [-17/50000,49/300+10^-12],
    z in [-41/200-10^-12,1/40].

The exact arithmetic check accepts all 19 original separating-option rosters
and all 52 tight-row/model guards over this domain. In particular, it restores
BOTH fixed-sign parallel offsets (11,12) and (13,14). Both cross zero on the
full padded domain; considering only (11,12) would leave a second gap.

The algebraic tight-row identities are unchanged by the slider box because
their base gaps vanish identically in every slider. Their interval derivative
coefficients and remainders must nevertheless be recomputed on the new box.
The checker currently reconstructs those 244 rows. This is guard validity,
not a proof that the resulting relaxation strictly contracts.

## Rational-frame handoff

check_stops.py independently performs the root-enclosure/coordinate formulas
on the ENTIRE rational padded slider box at core radius 1/6000. It proves:

* all exact-root core coordinates lie below 1/5000;
* every slider changes by less than 10^-12;
* a*>=0 follows from actual containment and S<=S*, not from approximate side;
* all stop-lemma inequalities and stopped-box model guards apply.

The largest coordinate reference drift is below 4.32e-17. A finite contractor
that proves rational core <=1/6000 on the declared padded slider input may
therefore use this terminal domain without first restoring the old slider box.
This receipt does NOT certify any finite contractor output or root ancestry.

## Exact old-dual reuse and outcome

reuse_duals.py reconstructs the stopped model, applies the old four rounds'
nonnegative rational weights with full residual payment against the NEW bounds,
and records the newly justified bounds and model hashes. Production used
2.684203 CPU seconds, no LP. The maximum core radius remains exactly one in
all four rounds. The generated reused-rigidity.json is valid bound data but
NOT a strict contraction certificate. No equality theorem follows.

This tests the old weights, not mathematical impossibility of the enlarged
terminal theorem. A new optimizer may exploit changed coefficients or the
correlated stop halfplane. It must yield independently replayable rational duals.

## Stronger model if needed

Retain the necessary slider inequality b+z <= T_upper/3+13*epsilon/100, using
an exact rational upper enclosure of T. It holds for all physical points.
For each normalized angle x, the existing shared lifts q_b=b*x and q_z=z*x
permit McCormick rows for y=b+z and q_y=q_b+q_z. These are necessary pointwise
identities and need no extra product variable. Use a complete lower and upper
bound on y and the already-certified interval for x. This preserves the
correlation which the stopped containing box drops. All rows require a new
independent coefficient audit and rational replay.

Alternatively subdivide the two-dimensional (b,z) polygon. Its vertices suffice
for affine coefficient extrema, but NOT by themselves for an LP contraction:
normalized angles and slider-angle products remain jointly constrained. Each
leaf needs its own valid relaxation and replay; testing only vertex LPs is not
a sound cover theorem without an additional convex-hull argument.

## Costed next steps (not launched)

1. Fresh 100-variable normalized rigidity proposals on the stopped box, up to
   eight rounds and 120 CPU-seconds, one native solver thread. The earlier
   smaller hybrid domain took 7.57 seconds for three rounds, but the widened
   domain could stall. Stop after eight rounds or the cap, preserving all duals.
2. Independent symbolic/interval/weak-dual replay: budget 60 CPU-seconds. The
   historical comparable exact replay took 6.56 seconds. Add a further 60 seconds
   only if auditing new correlation rows is needed; no automatic heavy campaign.
3. If still stalled, analyze which objectives remain at radius one before any
   new subdivision plan. This note supplies no many-leaf computation.


## Why the sixteen-square relaxation cannot restore the old upper stops

check_skeleton.py certifies the exact-root family at

    a=33/100, b=1/10, z=-1/5,

with square 4 removed. It checks all 256 containment inequalities for the 64
vertices of the remaining squares and all 120 pair separations. Each selected
separating axis has all 16 corner-sum gap inequalities checked. Positive gaps
use exact rational root intervals; zero gaps use symbolic identities or exact
divisibility by a root polynomial, with the denominator certified nonzero.
The check took 9.911804 CPU seconds. Independent acceptance is a separate premise from this producer result.

This packing violates a<=1/4, b<=1/12, and z>=-1/8 simultaneously. It satisfies
all stop-pair constraints because it is an actual packing of those 16 squares.
Consequently no argument using only containment and mutual non-overlap of this
skeleton can recover those three original endpoints. This is NOT a seventeen-
square packing; the existence of a compatible rattler has not been claimed or
checked. The witness supports enlarging the all-scale theorem, rather than
trying to force the old slider box solely through the 16-square relaxation.
