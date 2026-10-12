# Narrow numerical-proposal retry

This stage restores only the complete round15 box accepted by review
7766e022697c707fb576b9108f7323c99f47dd5e658e6603fa68b22a28857c9f.
Ignore the entire old partial round16, including its one valid-looking bound.
At most global rounds16–18; stop on all45 raw core coordinates<=1/10000.
Geometry, physical premises, stop cuts, rational row construction and92
signed objectives are identical to the previous stages.

The only numerical engineering change is a fresh HiGHS instance for each
round and a native time_limit setting up to3seconds. Each proposal records
native getRunTime before and after; failed objective identity is preserved.
The timer may accumulate across calls on one instance, so these are native
clock settings, not a claim of independent per-objective wall-clock budgets.
The prior timeout's exact cause is not assumed. A fresh-clock API preflight
used0.266416CPU-s and no model/solve.

The process has an 11-CPU-second hard limit and a 9-CPU-second soft signal
for final telemetry. Explicit checks retain a 2-second writing reserve.
This stage contains no further retry or model change.

Run once after independent source preflight:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/finite-stopped-contraction/proposal-timeout-retry/run.py --run
```

Acceptance of the producer target requires independent replay of every new completed
round and the accepted rational-entry theorem join. No whole-tree or common-
frame capture result is obtained merely by this numerical retry.
