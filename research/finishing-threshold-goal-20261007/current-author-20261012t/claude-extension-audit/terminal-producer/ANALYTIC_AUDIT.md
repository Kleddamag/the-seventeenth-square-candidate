# Independent terminal audit: box-relaxed

Reviewer: Codex reviewer `Codex`, 2026-10-08. This is an
independent review of Claude's changed instance. The reviewer helped produce the
original terminal method and the separate practical padded terminal, but did not
produce this instance or its certificates. The review does not replace the
separate audits of the WX engine, its checkers, or its window certificates.

## Scope and replay

The source is `research/window-extension-20261008/terminal/instances/box-relaxed/`.
No source there was executed. The 19-file snapshot in this directory
contains the pinned sources, inputs, two certificates, interface and replay
metadata. `snapshot-receipt.json` records SHA-256 values and the exact two changed
source lines. Every declared unchanged file was compared with our original.

The replay wrapper uses a 115-second soft/118-second hard process CPU limit. No LP is invoked.
The independent domain gate took 6.049840 CPU-seconds, and snapshot creation and
hash comparison took 0.015356. Final measured replay cost is in
`replay-receipt.json`; `verify.py` writes its receipt only inside our snapshot.

## Precise result under review

Use the packing-file labels, origin-aligned container, rational axes, and corrected
rational centre of square 13 from `uniform.geometry`. Every square has its own
independent quarter-turn angle lift. Assume a feasible configuration of the
sixteen labels other than 4, actual side `S <= S*`, the 29 rational core position
coordinates bounded by `1/100`, the 16 angle increments bounded by `1/200`, and

```
a in [0,1/4], b in [-1/20,3/20], z in [-1/8,3/40].
```

The intended conclusion is `S=S*` and **all 45 exact-root core deviations vanish**.
The same statement follows for the constrained squares of a physical packing of
17 squares. It neither asserts feasibility of the whole slider box nor assumes
anything about the rattler, positive contact forces, local minimality, an occupancy
mask, a global lower bound, or the stop pairs.

## Required wording correction

The extension's top-level `THEOREM.md` §1 defines core coordinates relative to the
rational packing file, defines its family by those coordinates being zero, and
§3/§4 then says they vanish. This is not the result of the terminal proof. Its
instance README correctly says **exact-root** core deviations vanish after the
bridge. The top-level theorem and corresponding shorthand in `SPEC.md` §11 must
make this distinction explicit.

This is substantive even though the displacement is tiny. With all rational core
coordinates zero, square 8 is unrotated at its rational centre. Its right reach
exceeds the certified upper enclosure for `S*` by the positive rational

```
172774611520751077003947028629799873599009499147027426104376477
/4000000000000000000000000000000000000000000000000000000000000000000000000000000
```

(approximately `4.319365288e-17`). Thus literal rational-core-zero and `S<=S*`
are incompatible. This wording error does not invalidate the correctly stated
instance theorem or its intended optimality consequence.

## Changed constants and finite envelope coverage

Exactly one line changes in `uniform.initial_bounds` and one in `bridge.run`.
They replace the original slider intervals by the box above and its `10^-12`
padding. The finite certificate header is exactly radius `1/100`, angle factor
`1/2`, parameter scale `1`, and the pinned packing digest. All other proof sources
are byte-identical to the original accepted libraries.

The slider box enters every relevant computation through current bounds: reference
centre difference `d(w)`, its norm bound `D`, the tangent offset, shared products,
option exclusion supports, and McCormick endpoints. There is no separate hardcoded
old `b` or `z` endpoint in those engines. `root_geometry.NORMALS` is only a proposed
roster: it is accepted only after the complete option audit and exact identities.

For a fixed owner and corner, the exact signed gap is

```
f = R(omega_o)n . (d(w)+dh) - 1/2 - n . R(omega_t-omega_o)v.
```

This also represents the other owner after reversing its outward normal; central
symmetry of the other square replaces its corner set by its negative. Thus using
one direction `d=p_j-p_i` for both owner enumerations retains all eight SAT axes.

Taylor's norm bounds give a first-order upper remainder
`D Wo^2/2 + Wo dr + V Eta^2/2`. The second-order terms are
`omega_o Jn.dh -(n.d(w))omega_o^2/2 +(n.v)eta^2/2`, with upper remainder
`D Wo^3/6 + dr Wo^2/2 + V Eta^3/6`. Replacing the first square's coefficient by
its interval supremum is valid because the square is nonnegative; positive
quadratics use an upper secant, negative quadratics an upper tangent. The mixed
angle/displacement term uses either McCormick upper plane. All these operations
remain valid on the enlarged slider box.

For option exclusion, substituting true products `q=w*omega` leaves an expression
multiaffine in the three sliders. Its maximum over their box is attained at one of
eight vertices. The carried relational bounds concern core variables and angles,
not slider choices, so they remain valid when evaluating each vertex support.
Unavailable axes are removed only by strict negative upper bounds. A unique owner
is used only when all seven alternatives have been excluded; otherwise the model
uses the proven parallel union or omits the pair. Dropping a pair cannot exclude
a physical packing. This covers independent orientations and degenerate contact
points without a force or transversality assumption.

The exact replay reconstructs every finite row and every carried relation. Its
weak-duality check includes the full signed residual against current box bounds;
weights are nonnegative rationals, and coefficient/RHS rounding is outward with
the full rounding loss paid. Solver statuses and history tables are not evidence.

## Root transfer, side floor, and slider boundaries

`check_gate.py` uses the original audited
root/geometry libraries, writes the changed box explicitly, and independently
projects the final rational pose intervals into the root frames. All 45 core
coordinates and all three slider intervals are covered. The maximum transferred
core bound is less than `1/5000`; the exact number is in `gate-receipt.json`.

For squares 11 and 13 the direct projection includes the entire slider motion,
the transverse displacement, both reference-axis changes and the reference-centre
change. For angles, `|2 atan t - 2 atan t*| <= 2|t-t*|` controls the lift change.
The corresponding padded root box is

```
a in [0,250000000001/10^12],
b in [-50000000001/10^12,150000000001/10^12],
z in [-125000000001/10^12,75000000001/10^12].
```

The unpadded lower end `a*>=0` is a physical wall consequence:
`x2+1/2<=S<=S*`, hence `a*=S*-1/2-x2>=0`. In the rational frame,
`p2x+1/2>S*` is verified exactly, so `a=p2x-x2>0` as well. This latter fact is
needed to receive a WX tube that allows positive `xi_(2,1)`; it cannot be replaced
by the slightly larger hypothesis `S<=Sref`.

No certified scalar lower bound is needed. Square 8 has horizontal reach at least
`1/2` at every orientation, so the input centre interval gives
`S>=p8x+1/2-1/100>=Sref-1/50`. All side margins are explicitly recorded in the
independent gate receipt and reproduced in the composition replay.

## Full root option coverage and sign guards

The independent gate reconstructs all 152 owner/axis/sign possibilities for the
19 retained pairs. It intentionally uses the coarser universal estimates
`||d(w)||<8` and normalized core centre difference `<3`, rather than the
producer's sharper norms. The excluded options still have strictly negative upper
gap bounds; the largest is below `-0.04883844`. Exactly the declared eleven
unique-owner and eight parallel pairs survive.

The gate rechecks all 52 symbolic tight identities and slider invariances and
all three zero tangential-offset identities. It independently rebuilds the first
244-row normalized model using the original library and the new box; its digest
equals the instance certificate's first model digest.

The closest fixed-sign parallel offsets remain safely inside their required
branches throughout the padded root box:

| Pair | Enclosing interval, rounded here for display |
| --- | --- |
| (11,12) | [0.0068386968692873, 0.2068386968712874] |
| (13,14) | [0.0055764400646925, 0.2055764400666926] |
| (2,6) | [-0.250000000001, 0] |

Exact rational intervals for every parallel row are in the gate receipt. No stop
lemma is needed to restore these signs: the entry box already imposes the needed
`b` and `z` ends. The standalone stop remarks in the instance README are not
dependencies of this audited chain and are not accepted by this review.

## Parallel inequality and validity at every positive scale

For the two parallel reference-owner axes put
`m=(omega_i+omega_j)/2`, `q=(omega_j-omega_i)/2`, and
`A=R(m)n.d_actual`, `B=R(m)Jn.d_actual`. Either owner option implies

```
A cos q + |B sin q| >= cos(q)^2 + |sin q| cos q.
```

Here `cos q>0`; therefore
`A >= cos q + |sin q| - |B| |tan q|`. With reference tangent offset
`tau=Jn.d(w)`, one has `|B|<=|tau|+D|m|+dr`.
For `|q|<=0.1`, use `cos q>=1-q^2/2`,
`|sin q|>=|q|-|q|^3/6`, and `|tan q|<=|q|+|q|^3`.
The last follows by integrating `tan^2 x <= x^2/(1-.1^2/2)^2 <3x^2`.
An upper expansion for `A` then gives both simultaneous first-order rows
with coefficient `(1-|tau|)/2` on the signed angle difference and error

```
E = D M^2/2 + M dr + Q^2/2 + Q^3/6 + |tau| Q^3
    + (D M + dr)(Q+Q^3).
```

The fixed-sign guard represents `|tau|` exactly as `branch*tau`; it does not
assume the perturbed physical tangent offset has that sign. The guard `|tau|<1`
makes both signed rows necessary. This derivation covers the two-owner union and
zero relative angle, without choosing an angular branch.

Let `R` be the largest of the 45 exact-root core deviations and assume `R>0`.
Normalize them as `x=h/R`, leave the sliders unscaled, and set
`s=(S-S*)/R`, `q_(k,i)=w_k*x_angle_i`. The bridge gives `R<=epsilon=1/5000`.
Square 8 gives `S>=S*-R`; actual `S<=S*` gives `-1<=s<=0`. Thus the normalized
point starts in the full declared box and has `||x||_infinity=1`.

Substituting physical angles `R m,R q` and displacement `R dh` into the parallel
error, then dividing by `R`, gives

```
R (D M^2/2+M dr+Q^2/2)
+ R^2 (Q^3/6+|tau|Q^3)
+ (D M+dr)(R Q+R^3 Q^3).
```

Replacing each nonnegative power of `R` by the same power of epsilon is exactly
the all-scale remainder in `rigidity.model`. The unique-owner and wall bounds
normalize in the same way. Exact symbolic base tightness removes the constant
gap before dividing; there is no uncertain root residual divided by an arbitrarily
small `R`. Interval error in a derivative coefficient is instead paid against
the normalized variable's radius.

All 48 products are shared across rows and obey the four necessary McCormick
inequalities; the physical point satisfies exact product equality even though
the relaxation does not enforce it. Every accepted round encloses the same
normalized physical point. A final maximum core bound below one contradicts
its definition, so `R=0`. Square 8 then reaches the exact wall `S*`; together
with `S<=S*`, this yields equality. The proof does not assume every slider choice
is physically realizable.

## WX interface binding and remaining obligations

The five currently supplied headers A-pad, B-pad, T-plus, T-plus-r012 and
T-plus-r015 all explicitly deliver `b>=-1/20`, `b<=3/20`, `z>=-1/8`, `z<=3/40`,
the 29 core position bounds and all 16 angle bounds. The gate pins their full
certificate hashes and header hashes. Their only relaxed terminal endpoint is
`xi_(2,1)<=1/100`, which the actual `S<=S*` wall argument tightens to `<0`.
The other bound `xi_(2,1)>=-1/4` already gives `a<=1/4`.

Reading these headers is not a replay or review of the WX proof. The sibling
reviewers must independently accept its analytic facts, checkers, complete trees,
root coverage and every terminal store. Subject to those approvals, the terminal
join uses no extra stop theorem or scalar lower bound. All statements remain for
one fixed frame/labelling; capture must still provide such a placement and labels,
including the relevant square-container symmetries. No global capture or full
optimality theorem is claimed by this terminal audit alone.
