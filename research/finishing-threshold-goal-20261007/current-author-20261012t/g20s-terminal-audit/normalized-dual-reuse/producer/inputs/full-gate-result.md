# G20S full analytic gate passes; contraction remains open

This additive check discharges the roster, root option coverage, symbolic
tightness and model-validity prerequisites for the proposed G20S terminal.
It is **not a new terminal theorem**: no solver, contraction certificate,
broad tree or capture calculation was run.

The exact rational input sliders are
`a in[0,8/25]`, `b in[-1/20,1/5]`, `z in[-1/5,3/40]`.
For the all-scale argument the lower a endpoint remains zero and the other
five endpoints receive `10^-12` outward padding. The root core radius is
`epsilon=1/5000`. The optional finite entry is position radius `1/200` and
independent angle radius `1/400` in the accepted rational reference frames.
The previous independently accepted assessment supplies its full coordinate
contract, actual-side wall repair, floor and conditional reference transfer.

| Exact check | Result |
| --- | --- |
| Old and widened tight-label sets | Identical, with all 52 labels recorded |
| Row types | 25 wall, 11 unique-owner, 16 parallel rows on 8 pairs |
| Complete root SAT roster | All 152 owner/axis/sign possibilities covered |
| Excluded root options | 125, every upper gap `<-1/60` |
| Possibly surviving root options | 27: one on each of 11 pairs, two on each of 8 pairs |
| Symbolic base gaps and slider coefficients | All 52 freshly checked; three zero-offset identities also checked |
| Root reference parallel signs | All eight branches valid with `abs(tau)<1` |
| Normalized necessary-row model | 244 rows, assembled without any solve |
| Finite entry pair coverage | All 19 pairs retained: 11 unique-owner, 8 parallel; no omissions or sign crossings in the reference offsets |
| Finite necessary-row model | 596 rows, assembled without any solve |

The largest excluded root upper bound is approximately
`-0.016829634000145`, with its exact fraction in `gate-receipt.json`.
“Surviving” means the gate has not excluded that axis; it does not assert
feasibility of an entire packing or arbitrary slider combination.

## Scope of the geometric proof

For each pair, the physical centre difference is
`d(w)+R dh`, with `0<R<=epsilon`, while each angle is independently
bounded in absolute value by `R`. The separate coarse audit proves
`||d(w)||<8` and `||dh||<3` over the complete padded slider box and
normalized core cube. The recorded upper bound for a reference unit normal n is

```
sup_w n.d(w) + 3 epsilon - 1/2 - lower_support(n, other_square)
    + (8+3 epsilon) epsilon + 2 epsilon.
```

The first `3 epsilon` pays for the core displacement. The next term bounds
rotation of the owner's axis against the full displaced centre difference.
The final `2 epsilon` bounds the other square's support change under the
relative rotation, using corner norm at most one. `lower_support` is the
maximum of the four exact-interval lower corner projections. Hence a strictly
negative result excludes the physical separating option throughout the closed
domain, without assuming a contact point or correlated angles.

Both owners, both axes and both normal signs are enumerated. For the second
owner the common direction `p_j-p_i` remains valid by central symmetry of
the other square; its four corners are all included. This is the same accepted
SAT convention, independently evaluated here with deliberately larger norm
constants. Every pair has exactly the expected remaining options. The unchanged
kernel's sharper option audit was also executed and agreed.

For parallel pairs, the checked sign is that of the **reference** tangential
offset `tau(w)`. The perturbed physical offset may change sign. The accepted
two-owner inequality bounds its absolute value by `|tau|+D|m|+dr` and pays
the last two terms in the remainder. This distinction applies equally to the
finite model. No force, local-minimum or positive-contact hypothesis occurs.

The exact old and new tight-label sets were each generated using the pinned
respective sources and then compared as sets and cardinalities. Their complete
arrays are saved. This closes the dynamic-roster loophole: reporting 19 pairs
or 52 counts alone would not have sufficed. Fresh symbolic checking shows for
every named row that its base-gap numerator is divisible by an accepted root
polynomial, its denominator excludes zero on the accepted root enclosure,
and every slider coefficient vanishes identically. The records are saved in
`symbolic-identities.json`; the identities are valid independently of slider
endpoints. The accepted root enclosure itself is inherited, not recomputed.

The 244 normalized rows consist of these 52 necessary geometric inequalities
and 192 shared McCormick inequalities. The existing hand proof justifies their
Taylor remainders at every positive `R<=epsilon`. Fresh model assembly rebuilt
all box-dependent coefficients and errors; its kernel digest is
`94fe0122926d379f084f32ae0d2a2c8d75665d40778ffea1da4f60d8fc1708a7`.
This hash is not a contraction result. The finite model uses the accepted
first/second-order option exclusions and remainders; its retained-pair roster
is separately saved, with kernel digest
`87c322abfb9a5529396997cc19da6d410c90d787f653f574eb2ac5821407a041`.

## Dependencies and remaining work

`instance/` preserves the accepted source layout and packing/root reference.
`SOURCE.diff` changes exactly two slider-constant lines: `uniform.initial_bounds`
and `bridge.run`'s padded box. The other kernel sources are byte-identical.
`preparation.json` binds every old/new source digest to the accepted terminal
manifest.

The intended consequence, once the missing certificates exist, remains:
sixteen **distinct** constrained squares satisfying the declared input at
actual `S<=S*` have `S=S*` and zero **exact-root** core. A seventeenth physical
square may have arbitrary pose; it remains in the complete packing. No old
narrow slider classification for seventeen squares is inferred. A future
tree terminal that permits positive `xi_(2,1)` must use the physical
`S<=S*` right-wall repair to obtain `a>=0`; replacing that side bound by
`S<=Sref` is invalid.

The conclusion of this source alone requires normalized strict contraction,
finite contraction and its bridge, the broad trees, complete independent
replays, and terminal-store/arc joins. Root cuts, a common frame and an
injective capture assignment are separate premises.

## Replay and cost

Preparation used `0.010928` CPU-s. The guarded calculation used
`8.291733` CPU-s: roster at 1.284461, root options at 1.898885, fresh symbolic
identities at 6.752240, normalized model at 7.132486 and finite model at
8.289812 cumulative CPU-seconds. There were no failed attempts.
There was one calculation process with soft/hard CPU
limits 11/12 seconds and one native thread.

To reproduce without changing this frozen package, copy `producer/` to a
fresh sibling directory at the same depth, then run the copied `prepare.py`
and `check_gate.py`. The latter never calls a solver; its receipt is regenerated
inside that fresh copy. The runtime invocation used was:

```sh
env PYTHONDONTWRITEBYTECODE=1 \
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  python3 \
  /absolute/path/to/fresh-sibling/check_gate.py
```

This gate establishes the analytic prerequisite only. Terminal certificate
discovery and replay are separate proof steps.
