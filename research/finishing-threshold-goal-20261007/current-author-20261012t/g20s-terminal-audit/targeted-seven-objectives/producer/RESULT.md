# Six normalized faces removed; one quantitative direction remains

The single seven-objective round gave six exact strict bounds.
The remaining objective is the negative angle of square 11, zero-based core
index 44. Its bound is exactly `-1`, so the resulting maximum core radius is
still 1. **This is not a rigidity certificate or an optimality theorem.**

The new exact box nevertheless proves a useful conditional reduction, subject
to independent review of this round. Under the accepted normalized analytic
hypotheses, let `R>0` be the maximum absolute value of the 45 exact-root core
coordinates, with `R<=1/5000`. Let `h` denote that core. Every hypothetical
physical configuration in the padded G20S slider domain must satisfy

```
h_44 = -R,
|h_j| <= (378457789018409/500000000000000) R < (757/1000) R
         for every other core coordinate j.
```

Here `h_44` is square 11's independent angular displacement from its exact-root
reference, not its rational-file angle. The other maximum is attained in the
enclosure at index 45, square 12's angle. Sliders, side, products and dummy
square-4 coordinates are not part of this normalization. There is no assertion
that the remaining direction, or any point of the enclosing box, is physically
feasible.

## Exact new bounds on one global domain

The independently accepted five-round box B5 was used unchanged for all seven
LP proposals. It has rational slider input
`a[0,8/25], b[-1/20,1/5], z[-1/5,3/40]` with the accepted root padding and
`epsilon=1/5000`. The exact 244-row global B5 model was rebuilt once and saved
as `B5-model.json`; its kernel digest is
`4469f117a953b255c88d6849aa23b08053eb9f93c02c57f0cbcb0a3fc32d58ef`.
There were **no face-specific restrictions**, parameter subdivisions or updates
between the seven proposals.

For each proposed nonnegative rational multiplier vector, the certified bound
is `sum(lambda*b)+min_B5(sign*e_i-sum(lambda*a)).x`, including the full signed
residual. Solver status and floating objective values are not premises.
`round6-residuals.json` saves every fraction and residual; rounded displays are:

| Coordinate | Minimized expression | Exact-bound decimal display | Strictly above -1? |
| --- | --- | ---: | --- |
| 8, square 5 horizontal | `-x8` | -0.555663466876 | yes |
| 14, square 8 horizontal | `x14` | -0.736025676610 | yes |
| 15, square 8 vertical | `x15` | -0.547069479724 | yes |
| 41, square 8 angle | `x41` | -0.736125676634 | yes |
| 41, square 8 angle | `-x41` | -0.547169479730 | yes |
| 44, square 11 angle | `x44` | **-1 exactly** | no |
| 49, square 16 angle | `x49` | -0.627540263517 | yes |

The other 85 objectives use empty multiplier dictionaries, giving their exact
incoming B5 box minima. The target `(44,+1)` also ended with empty row weights:
its relaxed minimizer reaches the incoming lower bound. All 92 bounds were
intersected simultaneously, rounded outward to the accepted grid, and the
shared product bounds were recomputed. The six successful targets retain
strict margins after that rounding.

The complete new B6 endpoint census has only `(44,-1)`. Moreover every other
core radius is at most the exact factor displayed above, while
`x44<=147523492924843/200000000000000<1`. Any nonzero physical core normalizes
to a vector with core infinity norm exactly one. The earlier five necessary
rounds and this global necessary round put that same vector in B6. Its only
possible norm-attaining endpoint is therefore `x44=-1`, proving the stated
direction restriction. Closed faces, simultaneous coordinate extrema and
degenerate contacts remain covered.

The six-step file retains the accepted first five steps byte-for-byte as JSON
values and appends the new model digest, all 92 exact bounds, and fresh final
intervals. `six-step-candidate.json` is an **unaccepted rigidity candidate**:
the strict final ratio condition is absent. The unchanged full rigidity checker
was consequently not run.

## Diagnostic only: the unclosed relaxation

All seven floating primal vectors and statuses are saved in
`targeted-receipt.json`. None is an exact feasible physical packing.
For `(44,+1)`, the solver reported approximately

```
a=.1674991253, b=.1470527913, z=-.04999847684,
x44=-1, normalized side=0.
```

In particular the displayed `b+z` is about `.0970543`. This suggests inspecting
the omitted physical stop pair `(11,13)`, whose small-core correlation is much
tighter. It does **not** establish that an existing stop theorem covers this
new box, that a new stop row removes every point of the remaining face, or
that another LP round succeeds. No stop model, additional round or further
optimization was attempted.

## Dependencies, physical scope and cost

The complete root/finite option and 52-identity gate is independently accepted
under SHA256 `a70b064bb81a55fca7f5ad9a9b19ea765c613877d8b243e041081760b9dc53dd`.
The accepted five-round prefix review is
`7d9db75869c3bc781ca3a08e892dd12d4c3e5f5140fae3f0577ff32ddee2a901`.
The previous seven-face corollary review is
`d98a4956589f65ff6fab859e12d9aeda6db27d04b1037625423f82863f633a60`.
All are copied and bound in this package with exact sources, root data,
packing reference, B5 and the new model.

The physical premises remain the complete accepted normalized domain, one
common frame, sixteen distinct constrained squares with independent angles,
actual `S<=S*`, and the padded slider box. In the intended seventeen-square
application the seventeenth physical square remains present without a pose
hypothesis. Actual-side wall and finite-to-root transfer premises cannot be
dropped. This reduction supplies no finite-entry proof, broad tree, common-frame
capture, original narrow equality-family classification or result on
R17/type cases.

Exactly seven SciPy/HiGHS calls were made, with native `threads=1`, the numerical
library thread environment fixed to one, and per-call time limit 2 seconds.
The script had soft/hard CPU limits 27/29 seconds.
Preparation cost `0.005790` CPU-s and the whole targeted calculation
`0.834626` CPU-s.
There were no failed attempts or retries.
Independent acceptance is recorded separately.

The source `targeted_round.py` is the replay/discovery entry point; it permits
only one seven-objective round. To preserve this frozen result, copy the
producer directory to a fresh sibling before rerunning `prepare.py` and then:

```sh
env PYTHONDONTWRITEBYTECODE=1 \
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  python3 \
  /absolute/path/to/fresh-sibling/targeted_round.py
```

That command repeats seven numerical proposals; an independent exact-only
review should instead replay the saved weights on the saved global B5 model.
No repeated proposal run is needed for the present review.
