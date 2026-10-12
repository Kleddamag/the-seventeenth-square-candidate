# Guarded finite stopped contraction pilot

This producer performs at most three rounds. It does not
call the old checker's terminal acceptance.

The physical assumptions are the exact accepted PRUNING.json guards bound
by INPUTS.json:17 actual unit squares in one actual container/common frame,
injective labels, actual S<=S*,29 raw position coordinates bounded by1/200,
16 independent radian angle coordinates bounded by1/400, full stated raw
sliders. Physical4 is omitted only from this necessary relaxation. The
accepted cuts initialize b>=-213/25000,z<=33/1000 and add -b-z>=-49/2000 to
every model. All100 intervals, the exact100-column row arrays, all92 signed
coordinate objectives, nonnegative rounded dual weights and simultaneous
outward updates are saved. Product intervals are recomputed after updates.

The initial side interval is [-1/50,0] for S-Sref. Its lower end follows
already from the top wall at square8: y8>=p8y-1/200 and vertical half-support
is at least1/2, so S-Sref>=p8y-1/200+1/2-Sref>-1/50. The exact rational
comparison and source point are saved. The upper end uses actual S<=S*<Sref.

The floating LP uses y=x/(1/200), with rows A*y>=b/(1/200); this changes
neither the recovered row multipliers nor the unscaled exact weak-dual
bound. Native row duals for these lower rows have nonnegative sign. The
integer-grid nonnegative multipliers are merely proposals; exact residual
interval arithmetic certifies the resulting bound on the incoming box.

Limits: max3 full rounds,29CPU-s hard process limit plus1CPU-s preparation
reserve, soft27 and a2-second final-write reserve. At most one native solver
thread, verified by readback. No split cases, extra objectives, adaptive
rounds or repeated baseline. Any incomplete round remains separately marked
and does not alter the last completed box. Solver failure/timeout implies no
physical infeasibility claim. This production record does not itself establish independent replay.

Target: all45 raw core intervals lie in[-1/10000,1/10000]. Only this target
and the original slider/frame assumptions can invoke the bound new rational
small-entry theorem. Reaching an old1/5000 display threshold does not suffice.
Even a successful local entry does not establish arbitrary global capture.

Run once from repository root:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/finite-stopped-contraction/producer/run.py --run
```

Read-only replay is provided separately by the independent reviewer; the
producer does not claim its own exact arithmetic constitutes that review.
