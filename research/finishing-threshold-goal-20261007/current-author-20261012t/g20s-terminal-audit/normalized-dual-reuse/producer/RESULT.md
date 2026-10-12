# Old normalized dual weights are inconclusive on G20S

All five accepted box-relaxed weight rounds were reevaluated on the widened
G20S normalized model. The maximum normalized core bound remains **exactly 1
after every round**. This does not prove a counterexample, failure of the
normalized relaxation, or impossibility of a fresh certificate. It establishes
only that this prescribed five-round weight reuse does not give the strict
contraction needed for the terminal proof.

No solver, new weight search, finite contraction, full finite-chain replay,
broad tree or capture work was performed. The independent full analytic gate
continues to pass and is bound as a dependency.

## Exact experiment

The rational slider box is `a[0,8/25]`, `b[-1/20,1/5]`, `z[-1/5,3/40]`;
the root model uses the accepted `10^-12` padding, unpadded lower a endpoint,
and `epsilon=1/5000`. Source files are exact copies of the complete analytic
gate's two-constant instance. The first rebuilt model digest matches that
gate: `94fe0122926d379f084f32ae0d2a2c8d75665d40778ffea1da4f60d8fc1708a7`.

The only input reused from each old objective was its coordinate, sign and
nonnegative multiplier dictionary. The weight-source certificate SHA256 is
`73894585ed9ac8caa50ee1020c9589ea983b3b5413566385b7336eb179f6b7a0`.
No old claimed bound, model digest or final interval was used to compute a new
bound. Model row indices need not retain the same interpretation for the
weak-duality calculation to remain sound: every new row is necessary and each
weight is nonnegative. All weight indices were checked against the new row
count.

At each of five rounds, the 244-row model was rebuilt from that round's current
widened intervals. For every one of its 92 objectives the saved exact bound is

```
sum_k lambda_k b_k
 + min_{x in current box} (sign*e_i - sum_k lambda_k a_k) . x.
```

The unchanged `exact_dual` value was compared with a separate sparse residual
computation. Each round records all 92 residual vectors, weighted RHS sums,
residual box contributions and resulting bounds. Bounds were updated
simultaneously, rounded only outward, and all shared product intervals were
recomputed before constructing the next model. Thus **460 new exact bounds**
were evaluated. Nothing from a previous old output box was silently carried.

`reuse-candidate.json` uses the existing certificate schema but is explicitly
an **unaccepted candidate**, since its final ratio is 1.
The unchanged `rigidity.check` was not run:
its required strict-contraction condition is absent. The per-round exact data
are `round-01-residuals.json` through `round-05-residuals.json`.

## What remains loose

After round 5, these core coordinates retain at least one unit-cube endpoint:

| Index | Physical coordinate | Unremoved endpoint |
| --- | --- | --- |
| 8 | square 5 horizontal core | +1 |
| 14 | square 8 horizontal core | -1 |
| 15 | square 8 vertical core | -1 |
| 41 | square 8 angle | both -1 and +1 |
| 44 | square 11 angle | -1 |
| 49 | square 16 angle | -1 |

These are enclosure bounds, **not simultaneously feasible values or a primal
witness**. They identify where this reused dual sequence fails to force the
normalization contradiction. Further reuse rounds, LP work or parameter
subdivision were outside this experiment and were not attempted.

## Cost, preservation and replay

Preparation took `0.008217` CPU-s. The five rounds completed in approximately
2.57 CPU-s; the exact total is in `reuse-receipt.json`.
There were no failed processes or numerical retries.
One process used soft/hard CPU limits 55/58 seconds and one native thread.

The accepted analytic gate, old certificate, exact source files, candidates,
residuals and this failure account are preserved and hash-bound by
`PRODUCER_MANIFEST.json`.
The independent review of this negative result is separate from the already
accepted analytic gate.

For a nondestructive replay, first copy this producer directory to a fresh
sibling at the same directory depth and run its `prepare.py`, then:

```sh
env PYTHONDONTWRITEBYTECODE=1 \
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  python3 \
  /absolute/path/to/fresh-sibling/reuse_weights.py
```

The script contains an unchanged-checker branch that would run only after a
strict contraction and before its resource limit. That branch was
not taken in this result. A future successful G20S normalized certificate would
still prove only all-scale exact-root rigidity; finite entry and tree capture
would remain separate obligations.
