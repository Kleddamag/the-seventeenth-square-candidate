# Box-relaxed terminal: independent review accepted

**PASS for the intended exact-root theorem.** The instance's precise README
statement is accepted. The extension's top-level theorem must replace its literal
claim that rational-reference core coordinates vanish by the conclusion that
exact-root core deviations vanish after the bridge. See `ANALYTIC_AUDIT.md` for
the proof and an exact positive margin demonstrating the distinction.

For a feasible configuration of the sixteen constrained squares, actual
`S<=S*`, rational core position radius `1/100`, independent angle radius `1/200`,
and rational slider box

```
a [0,1/4], b [-1/20,3/20], z [-1/8,3/40],
```

the conclusion is `S=S*` and all 45 exact-root core deviations are zero. This
also applies to the constrained squares of a packing of 17. No global lower
bound, occupancy hypothesis, rattler restriction, or separate stop lemma is used.

The independent analytic gate used the original root/geometry libraries and an
explicit reconstruction of the changed box.
It checked all 45 frame transfers, all 152 SAT options with deliberately looser
norm constants, 52 exact identities, all parallel sign guards and the first
244-row normalized model. The hand audit establishes the finite Taylor envelopes,
the full two-owner parallel inequality, shared products, residual weak duality,
and their all-scale normalization. A dual PASS alone was not taken as geometric
coverage evidence.

The snapshot replay independently reproduced:

| Stage | Exact result |
| --- | --- |
| Finite contraction | 14 rounds, 4,368 signed bounds, 110 relations |
| Rational maximum core | `22715168151/500000000000000` |
| Frame transfer | Every exact-root core is `<1/5000`; padded sliders match rigidity input |
| Rigidity | 5 rounds, 460 signed bounds; 52 identities and 19 pair audits |
| Final normalized ratio | `135416159726711/250000000000000 = 0.541664638906844 < 1` |
| Composition | Coordinate identity, exact side cap, square-2 wall, square-8 floor all PASS |

The finite certificate hash is
`6ec03fea30e82afe30e3c3160a6d76155023f3b85fabf7f04c122043d76b4819`.
The rigidity certificate hash is
`73894585ed9ac8caa50ee1020c9589ea983b3b5413566385b7336eb179f6b7a0`.
The freshly written full proof receipt hash is
`55cc6955e7c3b2289ab25978c66597758a005f104befdd64ea0b380d6bfcb853`.

Measured CPU: snapshot/hashes 0.015356 s; independent gate 6.049840 s; complete
exact replay and composition 46.680195 s. Total of these metered jobs:
52.745391 s. Small source/header read commands took less than one second of
additional wall time. There were no failed numerical attempts or LP calls.

The gate pins and checks the terminal headers of A-pad, B-pad, T-plus,
T-plus-r012 and T-plus-r015. All supply the required b/z endpoints explicitly.
The only join adjustment is the WX tube's positive upper allowance for
`xi_(2,1)`: physical containment at actual `S<=S*` implies `a>0` in the rational
frame. Thus neither the unverified stop remark nor a new scalar bound is needed
at this join. Full WX certificate/checker acceptance remains a separate review.

This local result still requires capture into the certified window with the
correct labels and container symmetry before it can prove global optimality.

Replay (writes only in this audit snapshot):

```sh
env PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 research/finishing-threshold-goal-20261007/current-author-20261012t/claude-extension-audit/terminal-producer/check_gate.py
env PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 research/finishing-threshold-goal-20261007/current-author-20261012t/claude-extension-audit/terminal-producer/replay_snapshot.py
```

Receipts are frozen for this audit; a future replay should first copy this audit
directory to a new destination if the original timings/receipt bytes must remain
unchanged. `MANIFEST.json` binds the accepted files and dependency hashes.
