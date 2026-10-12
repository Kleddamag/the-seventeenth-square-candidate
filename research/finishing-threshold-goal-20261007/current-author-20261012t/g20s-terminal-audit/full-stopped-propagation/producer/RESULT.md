# Three full stopped rounds: stronger necessary bounds, no rigidity yet

All three rounds were completed, with 92 signed core/side
objectives per round and 276 LP proposals in total. Every proposed bound
was recomputed with exact nonnegative rational multipliers and a complete
signed residual. The maximum 45-core radius remains exactly 1 after each
round, so no strict contraction or local rigidity is claimed.

Unlike the preceding one-objective and four-cell tests, these rounds make
substantial progress on almost every other endpoint. They preserve one
global domain and perform no parameter subdivision. No fourth round,
additional row type or additional contact constraint was run.

## Input and necessary models

The starting point is the independently accepted global B6 enclosure. Its
only possible normalized unit norm face is x44=-1. This face is **not fixed**
in the present calculation: the entire incoming coordinate44 interval and
all other core/side/a bounds are retained.

The independently accepted physical stop theorem gives b>=-17/50000,
z<=1/40, and b+z<=3/125 on the padded exact-root G20S domain at core radius
epsilon=1/5000. The first two statements are intersected with B6. Each
round rebuilds all 52 geometric rows and 192 product rows from its current
box and appends only the necessary physical row

```
-x21-x25 >= -3/125.
```

Coordinates21 and25 are unscaled physical b and z; they are not divided by
the core radius. All48 shared product variables remain. The complete
52-label roster, all152 independent-angle option audit, exact base-gap
identities, reference geometry and normalization implications are inherited
by exact source and accepted-review binding, without a new symbolic run.

## Exact output

Let R>0 be the maximum magnitude of the 45 actual exact-root core
coordinates, with R<=1/5000, under the inherited physical hypotheses and
actual S<=S*. The accepted B6 normalization maps this packing to the present
necessary domain. If independently replayed, the new sequence implies

```
h44 = -R,
|hj| <= (235021159590017/500000000000000) R  for every other core index j.
```

The coefficient is approximately .470042319180034, strictly less than
471/1000. This strengthens the earlier other-core bound .756915578036818;
it does not exclude the remaining direction. Index44 is the angle of
physical square11, and the largest remaining other-core bound is the
negative endpoint of coordinate20, its displacement along the reference u
direction. No numerical vector is promoted to a physical motion.

The exact changes after each simultaneous outward-rounded update are:

| Round | Largest other44 magnitude | Index attaining it | x44 upper | Side lower |
|---|---|---|---|---|
| 1 | `163789735758959/250000000000000` | 41 | `23894856837441/62500000000000` | `-2423130997127/250000000000000` |
| 2 | `470100275681317/1000000000000000` | 20 | `202080217945641/1000000000000000` | `-5476258463457/1000000000000000` |
| 3 | `235021159590017/500000000000000` | 20 | `107569537112521/1000000000000000` | `-764424877619/250000000000000` |

The x44 lower endpoint remains -1 and the side upper endpoint remains0.
All45 core intervals change in every round; respectively89,89,88 core
endpoints change. Each `core-change-summary.json` gives every exact change.
The normalized side deficit falls from about.02150903 to.00969252,
.00547626, then.00305770. The per-round reductions are approximately54.94%,
43.50%,44.16%. These percentages describe these interval lengths, not a
percentage of the global proof completed.

## Exact sequence argument

Every objective in a round uses the **same incoming model and box**. For
the objective c=sign*e_i and rows A_k*x>=d_k, the saved nonnegative rational
multipliers define r=c-sum(lambda_k*A_k). Then

```
c.x >= sum(lambda_k*d_k)
       + sum_{r_j>=0} r_j lower_j + sum_{r_j<0} r_j upper_j.
```

The right-hand side is recomputed with exact fractions; its full sparse
signed residual, weighted right-hand side and residual floor are retained.
Bounds are intersected only after all92 objectives for that incoming box
have been evaluated. Endpoints are rounded outward, and all product hulls
are refreshed before the next245-row model is rebuilt. Induction therefore
preserves every normalized physical packing through the three boxes.

The final core box still reaches a unit endpoint only at x44=-1. Because
normalization of a nonzero core must attain unit magnitude somewhere, the
stated cone conclusion follows. A strict maximum below1 would contradict
normalization and prove R=0, but no such strict maximum was obtained.

The unchanged old `rigidity.check` has no schema for the additional stop
row and was not called. The new saved sequence requires its separate
independent exact reconstruction/replay. This is an additive certificate
format, not a claim that an old checker accepted an unfamiliar row.

## Saved diagnostic and interpretation

All276 HiGHS calls reported optimal status. Complete floating proposals are
saved but have no exact feasibility or physical-packing status.

The last min-x44 proposal has a approximately.1475909554,
b approximately.1476883879, z approximately-.1236883879, with x44=-1 and
side0. Its largest shared-product error is at index58=a*x41: the saved
product is approximately-.0474259849 while x41 is zero. Other large errors
are z*x41 at index90 (approximately-.0282408031) and a*x49 at index66
(approximately-.0220836200). All48 differences are recorded in
`saved-primal-diagnostic.json` using only the already saved vector.

Thus there is explicit bilinear-relaxation loss in this proposal. This
does not identify a physical obstruction or prove that any selected product
inequality will finish. The continuing contraction of the side interval
and many core coordinates supports investigating complete propagation
before concluding that three rounds reflect a limiting obstruction.
Conversely, the largest saved product defect involves a rather than only
b/z, so arbitrary b/z refinement has no special justification from this
vector. No further proposal was run under the completed scope.

## Bindings, resources and remaining scope

Accepted dependencies are:

- Full geometric gate `a70b064bb81a55fca7f5ad9a9b19ea765c613877d8b243e041081760b9dc53dd`.
- Global B6 review `b38fb735a1d3bdd84c662a68b37d7d10e806af71abf82b54c320424da79d1ad1`.
- Physical stop review `e8af5453f7e97d18ee2dab652644d797218ce2382fb928b53a8cb151cee7645d`.

All17 physical squares remain in the inherited hypotheses, with no imposed
terminal pose on the free seventeenth square. The theorem requires the
stated exact-root slider/core domain and actual S<=S*. No finite-entry
bridge, broad tree, common-frame capture, enlarged-window theorem,
full-family equality classification or global optimality claim follows
from this negative outcome.

Preparation used .006784 process CPU seconds and the complete calculation
2.527058. The process had soft/hard CPU limits56/59seconds, one native
thread, and one second per solver proposal; the resource-stop mechanism
was not used. Including saved-data summaries, source reads and sealing,
the total was at most five CPU seconds. This producer record does not
supply independent acceptance of its claims.
