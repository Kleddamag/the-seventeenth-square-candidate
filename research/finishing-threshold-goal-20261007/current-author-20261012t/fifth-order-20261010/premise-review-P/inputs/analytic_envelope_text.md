# Joint capture pilot — 7 October 2026

This is a working, exactly replayable **local contraction experiment**, not a new
global lower bound or a proof of optimality. Its intended contribution is a reusable
way to force a neighbourhood of packings toward the known family without splitting
it into individual angle cases.

The strongest tested mechanism combines simultaneous LP constraints, signed
second-order rotation terms, and certified bounds on differences between neighbouring
squares. Merely preserving neighbouring correlations improves the weaker model but
does not remove its plateau. The experiment therefore supports the correlation-loss
hypothesis as one contributor, not as a sufficient explanation.

## Controlled comparison

All four principal runs start from the same labelled rational packing, with each
centre coordinate within `r = 1/1024` of its reference value, every angle within
`30r` radians (about 1.679 degrees), and container side in `[Sref-1/50, Sref]`, where
`Sref = 4675530093604551/1000000000000000`.

“Position ratio” means median final coordinate width divided by its starting width,
over all 34 centre coordinates. Smaller is better. A small median does **not** assert
that every coordinate contracts; slider and rattler freedoms remain.

| Model | Position ratio after 8 rounds | Position ratio after 12 rounds |
| --- | ---: | ---: |
| First-order rows, individual bounds | 0.620116 | 0.620078 |
| First-order rows, carried correlations | 0.595148 | 0.595141 |
| Signed curvature, individual bounds | 0.000575686 | 9.408e-10 |
| Signed curvature, carried correlations | 0.00000161419 | 1.022e-9 |

The first-order plateau improves by about **4%**, but remains. At round 8, the
curvature model with correlations has a median width about **357 times smaller**
than the same curvature model without them. Both eventually reach the numerical
and rounding floor, and the correlation version does not dominate every last-round
metric. The interval-propagation control, which regenerates the same kind of rows
from its own contracted boxes, retains a median position ratio of 1 in these runs.
This is our control implementation, not a benchmark against upstream's hull kernel.

Carrying correlations requires **324 LP objectives per round**, versus 104 for
individual bounds. The result is about contraction per round, not a runtime speedup.

An explicit correlation example from the final first-order run, in radians:

| Bound on `omega9 - omega10` | Interval |
| --- | --- |
| Inferred from separately certified angles | `[-0.023155247058234, 0.018850417835159]` |
| Directly certified combined objective | `[-0.003929724595022, 0.003019676789677]` |

The second interval is about **6.04 times narrower**. Its maximum absolute value is
5.89 times smaller, reducing this pair's relative-rotation square remainder by about
35 times. That reduction does not describe the entire model's error.

The producer certifies 110 combined quantities over 19 neighbouring pairs: angle
differences, angle sums, Cartesian displacements, and displacements projected onto
the reference square axes. Duplicate directions are removed. Bounds come from the
joint LP, are checked exactly, and enter the next round both as linear constraints
and as domains for nonlinear remainder and envelope estimates.

The comparison uses the same analytic formulas with and without carried constraints.
Even the individual-only control takes the actual interval difference of the
individual angle intervals. Thus the measured benefit cannot be attributed merely
to replacing `wo + wt` with a better calculation on those same marginal intervals.

## What the strongest certificates establish

For the stated input neighbourhood, 27 of the 34 position coordinate widths fall
below `1e-10`; all angles except square 4's are confined within approximately
`1.6e-11` radians of their reference values in the combined run. Its side interval
implies the conditional bound `S >= Sref - 49/200000000000000`.

These are finite enclosures. They neither prove exact equality nor show that every
packing enters the input neighbourhood. Square 2's horizontal freedom, square 4's
rattler motions, and the translations of squares 11 and 13 remain. The individual
coordinate box necessarily represents each oblique slider with two nonzero widths;
the carried projections can retain the relation between those coordinates.

The reference is our retained [rational Bidwell packing](../../upper-packing-certificate.json).
The `interior` control moves square 4 left by `1/50`, square 11 by `-v11/50`, and
square 13 by `-v13/25`. All 136 non-overlap conditions and all vertices of that
modified reference pass an exact SAT check. Its curvature-only run also contracts
27 position widths below `1e-10`. This is a second point in the family, not uniform
coverage of all slider parameters and not upstream's centroid.

Pairs `(2,4), (3,5), (4,6), (9,11), (11,13)` are deliberately unused in every model.
This checks that the observed contraction does not require those incidental
rattler, corner-only, or slider-endpoint contacts. Pair labels throughout this
package follow our JSON ordering, which differs from upstream's first eight labels.

## Why the linear constraints are necessary

Write the perturbation as `z=(delta_p, omega, delta_S)` and let `J` denote rotation
by 90 degrees. The reference centres, axes and vertex offsets are rational. The
angles `omega` themselves are real radian increments; they are not replaced by
rational half-angle approximations.

For one candidate separating axis owned by square `o`, with reference normal `n`,
other square `t`, centre difference `d0 + delta_d`, and one of the other square's
vertex offsets `v`, the exact corner gap is

```
f = (R(omega_o)n) · (d0 + delta_d) - 1/2
    - n · R(omega_t - omega_o)v.
```

Non-overlap on this axis requires all four corner gaps to be nonnegative. Before
using an axis, the constructor bounds every competing separating-axis option from
above over the entire current domain. It uses a unique option only when all others
are strictly negative. Unresolved disjunctions are dropped, except for the
parallel-face case below. No option is selected because it looks likely.

Let `D >= ||d0||`, `dr >= ||delta_d||`, `wo >= |omega_o|`,
`eta >= |omega_t-omega_o|`, and `V >= ||v||`. The first-order expansion gives
the necessary inequality

```
g0 + a·z + E1 >= 0,
E1 = D*wo^2/2 + wo*dr + V*eta^2/2.
```

The second-order expansion retains the signed quadratic expression

```
Q = omega_o * (Jn · delta_d)
    - (n·d0)*omega_o^2/2
    + (n·v)*(omega_t-omega_o)^2/2,
E2 = D*wo^3/6 + dr*wo^2/2 + V*eta^3/6.
```

Thus `f <= g0 + a·z + Q + E2`. A positive multiple of a square is bounded above
by its secant on the certified interval. A negative multiple is concave and lies
below each tangent; tangents at zero and the interval midpoint are used. The
angle/displacement product is bounded above by both McCormick upper planes. For
`x in [l,u]`, `y in [L,U]`, these are `u*y + L*x - u*L` and
`l*y + U*x - l*U`. Each combination produces a necessary linear inequality.

The bounds use the elementary rotation remainders
`||R(w)-I-wJ|| <= w^2/2` and
`||R(w)-I-wJ+w^2 I/2|| <= |w|^3/6`.
Consequently, retaining curvature signs is materially stronger than assigning
every quadratic contribution an independent positive worst-case error.

For two parallel reference faces, let
`m=(omega_i+omega_j)/2`, `q=(omega_j-omega_i)/2`, and `tau=Jn·d0`.
The union of the two possible owner axes implies

```
(R(m)n)·(d0+delta_d)
  >= cos(q) + |sin(q)| - |(R(m)Jn)·(d0+delta_d)| |tan(q)|.
```

For angle radii at most 0.1, use `cos(q)>=1-q^2/2`,
`|sin(q)|>=|q|-|q|^3/6`, and `|tan(q)|<=|q|+|q|^3`.
If `M>=|m|`, `Qb>=|q|`, and `k=(1-|tau|)/2>=0`, this yields both rows

```
n·d0 - 1 + n·delta_d + tau*m +/- k*(omega_j-omega_i) >= -E,
E = D*M^2/2 + M*dr + Qb^2/2 + Qb^3/6 + |tau|*Qb^3
    + (D*M+dr)*(Qb+Qb^3).
```

Pairs with negative `k` are omitted. The absolute values create two simultaneous
necessary rows, not an unsupported choice of angular branch. This parallel-face
first-order construction builds on upstream's documented contact analysis.

Walls are checked for all four vertices of every square, with a first-order
rotation remainder. Directional centre bounds give Euclidean bounds through either
Cartesian coordinates or either square's orthonormal reference frame; taking the
minimum of these valid upper bounds is safe.

All coefficients are rounded to a `1e-15` rational grid with the entire coefficient
error paid for over the input box. Right sides round outward. No floating decision
is used to validate an accepted geometric row. The analytic derivation above is
not machine-formalized or independently reviewed.

## Exact handoff of correlations

Every LP is a relaxation `A z >= b`, with box bounds `l <= z <= u`.
For any objective vector `c`, nonnegative rational weights `lambda`, and exact
residual `d = c - A^T lambda`, weak duality gives

```
c·z >= lambda·b + sum_k d_k * (l_k if d_k >= 0 else u_k).
```

The numerical solver only proposes weights. They are rounded to nonnegative
rationals; their residuals are paid for exactly. Applying this to `c` and `-c`
certifies a two-sided interval even when the proposed weights are not an exact
optimal dual solution. The same rule handles individual and combined objectives.

The checker reconstructs every row and every combined objective from the source,
checks both signs, intersects independently proved bounds, and then reconstructs
the following round. It rejects a carried relation that was not obtained from the
previous certificates. There is no circular use of newly assumed correlations.

At round 11 of the strongest run, HiGHS presolve reported infeasibility at widths
near floating-point tolerances. The exact reference `z=0` still satisfies every
row. The producer retries the identical model with presolve disabled and accepts
only exact dual bounds; it never converts a solver status into an exclusion.
There were 648 retries across the last two rounds. The late numerical floor is
distinct from the much larger plateau in the first-order model.

## Reproduction and checks

Discovery used Python 3.12, SciPy 1.18.1 and NumPy 2.5.3. Exact replay and the
controls need only the Python standard library. From the repository root:

```sh
python3 research/joint-capture-20261007/check_controls.py
python3 research/joint-capture-20261007/check_envelopes.py
```

The first command replays all six saved certificates, verifies exact feasible
motions remain inside the output bounds, and rejects six deliberate mutations.
The second runs deterministic numerical sign/remainder diagnostics; those sampled
checks are additional debugging evidence, not the analytic proof.

With SciPy installed, reproduce the four-way comparison by running:

```sh
python3 research/joint-capture-20261007/pilot.py --angular-factor 30 --iterations 12 --no-curvature --output research/joint-capture-20261007/pilot-linear-only.json
python3 research/joint-capture-20261007/pilot.py --angular-factor 30 --iterations 12 --no-curvature --carry-relations --output research/joint-capture-20261007/pilot-linear-relative.json
python3 research/joint-capture-20261007/pilot.py --angular-factor 30 --iterations 12 --output research/joint-capture-20261007/pilot-r1024-a30.json
python3 research/joint-capture-20261007/pilot.py --angular-factor 30 --iterations 12 --carry-relations --output research/joint-capture-20261007/pilot-curvature-relative.json
```

Use `--profile interior` for the second reference and omit `--angular-factor 30`
for the narrow-angle control. Certificates can differ across solver versions while
remaining valid; the exact checker is the acceptance criterion. Numerical history
and summary fields are diagnostics, not inputs to the checker.

Files: [implementation](pilot.py), [comparison](comparison.json),
[exact replay and mutation receipt](validation.json),
[numerical envelope diagnostics](envelope-diagnostics.json).

## Relation to existing work and next proof obligation

This investigation checked upstream at commit
`4261f68098bcec3923159b77dd3dec69aab734aa`. It is not a claim that nobody has
considered joint LPs, Taylor bounds, or quantitative rigidity. Those ideas already
appear in the project. Relevant primary sources are:

- [Capture review, 5 October](https://github.com/jlevy/squares/blob/4261f68098bcec3923159b77dd3dec69aab734aa/docs/project/reviews/review-2026-10-05-n17-capture-r9.md): documents stalled hull propagation and the proposed alternatives.
- [Widened projection scope](https://github.com/jlevy/squares/blob/4261f68098bcec3923159b77dd3dec69aab734aa/docs/project/reviews/review-2026-10-02-n17-widened-projection-scope.md): already proposes a wider LP-based terminal theorem.
- [First-order branch analysis](https://github.com/jlevy/squares/blob/4261f68098bcec3923159b77dd3dec69aab734aa/docs/project/reviews/review-2026-10-01-n17-first-order-branches.md): supplies the parallel-face derivative structure used here.
- [Local theorem recipe](https://github.com/jlevy/squares/blob/4261f68098bcec3923159b77dd3dec69aab734aa/docs/project/reviews/review-2026-10-02-n17-local-theorem-recipe.md): identifies the importance of moving the base point with the sliders.
- Our [fixed-angle LP package](../fixed-angle-lp/README.md) supplies the prior rational geometry and exact-dual approach.

The concrete deliverable here is the implemented free-angle contractor, its exact
correlation handoff, and the controlled ablation. The next useful proof task is to
extend it uniformly over the actual slider domain, using a moving reference, and
verify inclusion in the existing local theorem's precise coordinates. A further
global argument must still force arbitrary packings into that capture domain.
Success at the present two references does not supply either obligation.
