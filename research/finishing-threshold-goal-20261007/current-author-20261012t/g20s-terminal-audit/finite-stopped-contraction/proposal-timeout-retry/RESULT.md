# Producer reaches the finite-entry target at round17

The narrow retry completed rounds16 and17, then stopped early on the exact
target. It did not run round18. All45 raw core intervals are contained in
[-64007486789/10^15,64007486789/10^15], strictly inside[-1/10000,1/10000].
The exact target slack is35992513211/10^15. Maximum position radius is
30394903479/10^15; maximum angle radius is64007486789/10^15.

| global round | rows | maximum position | maximum angle | CPU seconds |
|---|---:|---:|---:|---:|
|16|773|.00005583725376|.000117599804877|2.248132|
|17|773|.000030394903479|.000064007486789|2.114671|

Both models retain11 unique pairs,8 parallel pairs, no omitted pair and no
sign crossing. All184 new signed bounds, both full models and every incoming/
outgoing interval are saved. The old partial16 data were not used. Sources,
all accepted ancestors and the rational small-entry theorem are bound.

check_target_join.py independently of model generation compares the final
data with the accepted small theorem: identical rational reference and
coordinate-map source bytes, same45-core registry/common physical labels,
all three sliders inside that theorem's raw ranges, and all core bounds
<=1/10000. TARGET_JOIN.json records exact containment. It is a data join,
not an independent proof of the new finite bounds; that replay is a separate proof obligation.

Subject to independent finite replay, this supplies the missing local link
from the guarded .005-position/.0025-radian finite entry to exact-root core
zero and S=S*. It does not establish common-frame capture or independently
accept either entire HW/G20S tree. Raw rational-reference core zero is not
claimed, since the terminal conclusion uses the algebraic reference.

Run cost4.556524CPU-s, wall4.524506s.

Fresh native clocks read0 at the start of each round and about.175451 and
.163902seconds after their92 proposals. Per-proposal records show accumulation
on each instance. This documents the timer behavior without re-running
the previous timeout artifact. No further retry or solver run remains.
