Editorial copy. Line references refer to the original; exact changes are listed in EDITED_LINES_ROUND2.json.

# Final bounded block: global rounds10–19

This continuation restores all100 intervals
from the accepted round9 box, review0a8aa22c9c6ba5e7e223669f4dd5891392832b0484e107570d175229016f68ed,
which in turn binds the accepted three-round prefix. The source diff changes
only prefix schema/count validation and the maximum/global round numbers.
Original physical assumptions, all accepted raw cuts, model construction,
92 signed objectives, exact dual/residual updates and native one-thread
settings remain unchanged.

Stop upon reaching all45 raw core radii<=1/10000, completing ten new rounds,
or the CPU guard. The process has a 29-CPU-second hard limit. No further
rounds, model change or split case is included. Completed and partial rounds
are saved separately. New results
must be independently replayed and joined to both frozen ancestors before a
finite-entry conclusion can be promoted.

The old uniform checker's1/5000 display is not the target. Reaching1/10000,
if achieved and reviewed, composes with the separately accepted rational small
entry theorem under actual S<=S*, common labels/frame, and the full padded
sliders. It would not certify either entire HW/G20S tree or global capture.

Run once, after source preflight:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/finite-stopped-contraction/finishing-continuation/run.py --run
```
