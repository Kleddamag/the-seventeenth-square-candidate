# Independent enlarged-radius physical stop review

Independently accepted on 2026-10-08 over the entire padded exact-root G20S slider
box at core radius `501/100000`. Acceptance binds producer manifest
`5a3aab61d2a5f5b08090fc4fc8e0ad67482007b06e370d0cbdc4db255cdf9ead`
through the separate manifest and producer-binding receipt in this folder. This is a necessary
geometric pruning theorem, not a larger-radius rigidity or finite-contraction
theorem.

## Exact statement

Set `epsilon0=501/100000`, `delta=1/10^12`. In the same exact-root coordinate
map and physical labels as the accepted G20S gate, allow all 45 core coordinates
and each of the sixteen independent physical radian angle deviations to have
absolute value at most epsilon, for any `0<=epsilon<=epsilon0`. The full closed
slider intervals are

```
a in [0, 8/25+delta],
b in [-1/20-delta, 1/5+delta],
z in [-1/5-delta, 3/40+delta].
```

Every physical nonoverlapping configuration in this domain satisfies

```
b >= -(17/10)*epsilon,
b+z <= T/3+(7/50)*epsilon,
z <= T/3+(46/25)*epsilon,
```

where `T=c(c+4-S*)` at the accepted algebraic root. Therefore at epsilon0,

```
b >= -8517/1000000,
b+z <= 49/2000,
z <= 33/1000.
```

The exact stronger rational upper bounds, before rounding to the latter two
cutoffs, are retained in `arithmetic-receipt.json`. In particular, the additive
terms are `3507/5000000` for b+z and `46092/5000000` for z. These stronger
bounds are the appropriate inputs to a reference-transfer proof: the already
rounded upper cutoff has no budget assigned to a subsequent coordinate error.
The physical sliders remain unscaled, with indices a=2, b=21, z=25.

Square 4 remains physical and unrestricted, but is unused by these two pairs.
The full a interval is preserved. This statement directly assumes the specified
exact-root coordinate domain; no transfer into it is inferred. An actual-side
hypothesis such as `S<=S*` must be supplied wherever the surrounding coordinate
transfer uses it, notably to repair the lower a bound from a wall.

## Fresh full-domain coverage

The review reuses its own previously sealed rational-interval and sparse
polynomial primitives, pinned through independent stop review
`e8af5453f7e97d18ee2dab652644d797218ce2382fb928b53a8cb151cee7645d`.
It imports no producer checker. All four Cartesian projection identities are
rechecked by exact polynomial reduction modulo `c^2+s^2=1`. At the accepted root,
`u=(c,s)`, `v=(-s,c)`, and the physical pair differences are `Delta=X*u-N*v` with

```
(9,11):  X=c(1-s)+h11-u.h9,  N=1+b+v.h9;
(11,13): X=c-s+h13-h11,      N=1+T/3-b-z.
```

The reference norms over the whole padded slider intervals satisfy `D=5/4`
and `D=4/3`, respectively. The core-displacement norms are at most
`dr*epsilon`, with `dr=5/2` and `dr=2`. These norm bounds and actual N positivity
are recomputed at the larger radius. The old 6/5 reference cap fails for (9,11)
and is rejected as a control.

There are eight possible directed separating owner axes for each pair. Every
unit square contains a radius-1/2 disc, so a separating projection must be at
least 1. For either independent owner angle theta,

```
R(theta)n . Delta <= sup(n.d)+dr*epsilon0
                   +epsilon0*(D+dr*epsilon0).
```

The independent receipt lists all sixteen alternatives. Each owner's `+u`,
`-u` and `+v` choices are strictly below 1. Both negative-v owners are retained
in each pair. Thus the proof covers their union, without choosing one owner or
asserting both simultaneously. The bounds are uniform over the entire closed
box: no sign split, endpoint omission, equal-angle assumption, or subdivision
is needed. Zero angles, coincident owner axes, degeneracies and exact touching
are included.

For whichever remaining owner separates, positive N gives

```
1 <= N*cos(theta)+X*sin(theta) <= N+epsilon*abs(X).
```

The exact root enclosure establishes `c+s<141/100`,
`abs(c(1-s))<277/1000` and `abs(c-s)<129/1000`. At epsilon0 the two relevant
coefficient bounds are

```
141/100+277/1000+(241/100)*epsilon0
    =16990741/10000000 <17/10,
129/1000+2*epsilon0
    =6951/50000 <7/50.
```

Their positive slacks are `9259/10000000` and `49/50000`. The old sum
coefficient 13/100 is too small for this estimate and is explicitly rejected.
For smaller epsilon the same inequalities follow by monotonicity. The normal
core displacement in pair(11,13) is exactly zero; it is not bounded by a
spurious independent error. Substitution proves the stated parametric stops.

## Quantitative slack and limits

The exact interval computation yields, as decimal displays only,

```
b+z upper: 0.02443914319540521,
z upper:   0.03295614319540521.
```

The strict remaining margins below 49/2000 and 33/1000 are greater than
`0.00006085680459479` and `0.00004385680459479`, respectively. Full rational
margins are recorded; no proof decision uses those decimal displays.

This directly enlarges the radius on which physical stop pruning is available.
It does not assert that every slider tuple remaining after pruning is feasible,
restore older slider endpoints, contract a finite entry to radius1/5000, or
extend the local rigidity theorem itself to radius501/100000. The proposed raw
rational entry and its three raw-coordinate cuts require the distinct transfer
producer and independent reviewer. A new global capture or optimality result
does not follow from this audit.

## Replay and independence

The arithmetic script rederives norms, all owner-axis tests, coefficients and
rational slacks. Its three negative controls reject the old coefficient, old
norm cap and an undeclared larger radius. The binding checker separately
compares every producer alternative and value, exact input domain, source
hashes, proof interface, and four additional corruption controls.
Producer source is inspected and replayed read-only, never imported by the
independent arithmetic. The accepted algebraic-root existence/uniqueness proof
is an explicit dependency and is not rerun. Full cost and replay records are
bound by the review manifest. No optimizer, model or tree is run.

Read-only independent arithmetic replay:

```
python3 -B research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/finite-entry-stop-pruning/root-review/check_root_stops.py --check
```

Read-only producer-binding replay:

```
python3 -B research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/finite-entry-stop-pruning/root-review/check_binding.py --check
```

Recorded arithmetic and replay CPU totals 0.050461 seconds. A fail-closed
pre-freeze manifest mismatch is preserved in `PREFREEZE_BINDING_FAILURE.md`;
it did not change any mathematical input or accept a stale source.
