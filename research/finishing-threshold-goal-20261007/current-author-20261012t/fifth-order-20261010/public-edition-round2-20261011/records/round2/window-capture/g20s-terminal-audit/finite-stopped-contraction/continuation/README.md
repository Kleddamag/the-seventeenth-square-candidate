Editorial copy. Line references refer to the original; exact changes are listed in EDITED_LINES_ROUND2.json.

# Six-round bounded continuation

This continuation restores
all100 final intervals of the independently accepted three-round prefix
(review65ba63fc416b50daf3c179901b059d9e2da6b340c3b70604983aa52931fa86ec).
It checks the complete registry, source bindings, domain inclusion and exact
48-product refresh before running. It does not repeat the prefix.

The source diff shows only prefix restoration, schema and round-limit changes.
All physical assumptions, the original raw entry, accepted stop cuts, model
construction, native one-thread readback and exact nonnegative-dual/residual
arithmetic are unchanged. Local round names are global4..9. At most six full
rounds run, with early stop if all45 raw core radii are<=1/10000; no extra
objectives, domain split or adaptive extension is permitted.

The process has a 29-CPU-second hard limit and a 27-CPU-second soft limit.
All models, weights, incoming/outgoing boxes and any partial round are saved.
Independent review replays only this continuation and joins the accepted prefix.

Run once from repository root, after the independent source preflight:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/finite-stopped-contraction/continuation/run.py --run
```

A target-reaching producer result still needs independent model/arithmetic
replay and the accepted raw-entry theorem join. It would finish this finite
entry only, not the HW/G20S trees or common-frame global capture.
