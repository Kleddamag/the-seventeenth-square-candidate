# Independent review: complete padded G20S physical stops

Accepted on 2026-10-08. Reviewer: `Codex`; producer:
`Codex`. This independently accepts the geometric theorem
and its unscaled terminal interface, not an LP result or a finishing theorem.
The frozen producer manifest is
`ebcb669d46ea8230bf840c98ff7fb7b0d6980bcce1ea11315a9b9508b9a7c03d`.

## Exact accepted statement

Use the exact-root geometry, physical labels and core parametrization bound by
the accepted full G20S analytic gate (review manifest
`a70b064bb81a55fca7f5ad9a9b19ea765c613877d8b243e041081760b9dc53dd`).
Let `delta=1/10^12` and `0<=epsilon<=1/5000`. All 45 exact-root core coordinates
have absolute value at most epsilon; the sixteen constrained angle deviations
are independent physical angles in radians with that same bound. The entire
input slider box is

```
a in [0, 8/25+delta]
b in [-1/20-delta, 1/5+delta]
z in [-1/5-delta, 3/40+delta].
```

For physical nonoverlapping unit squares in that parametrization, necessarily

```
b >= -(17/10) epsilon,
b+z <= T/3+(13/100) epsilon,
```

where `T=c(c+4-S*)` is the accepted exact-root reference quantity. Consequently

```
b >= -17/50000,
b+z <= 3/125,
z <= 1/40.
```

The last two closed bounds have strict rational slack. Square 4 remains a
physical square but is unrestricted and unused in this two-pair implication.
The slider a is unused, so its full padded input interval remains allowed.

This is a direct theorem on the padded exact-root domain. It does not establish
finite-window contraction or a new rational-reference transfer. An application
must supply that domain and its core radius independently. In the intended
terminal application the side premise is the actual `S<=S*`; a larger rational
cap does not replace it in any subsequent equality argument.

## Independent analytic reconstruction

Write `u=(c,s)`, `v=(-s,c)`, with
`c=(1-t^2)/(1+t^2)` and `s=2t/(1+t^2)` at the accepted root. Our checker defines
a sparse polynomial ring and proves all four projection identities directly
from the Cartesian reference centres, reducing modulo `c^2+s^2-1`. It imports
neither the producer checker nor an existing symbolic proof module.

The actual centre formulas are `P9+h9`, `P11+h11*u-b*v`, and
`P13+h13*u+z*v`. For the directed differences `Delta=X*u-N*v` the identities are

```
(9,11):  X=c(1-s)+h11-u.h9,  N=1+b+v.h9;
(11,13): X=c-s+h13-h11,      N=1+T/3-b-z.
```

The independent code also verifies the exact source identity of `bridge.layout`
and `uniform.geometry` between the old accepted geometry and the G20S full-gate
instance, and byte identity of `root_geometry.py`. The root interval is checked
against the accepted gate receipt, not inferred from floating evaluations.
This inherits the accepted root existence/uniqueness theorem; it does not rerun
that theorem.

### Complete separating-axis coverage

Every nonoverlapping pair of unit squares has a separating projection along
one of eight directed owner axes: either owner's two orthogonal axes, in either
sign. The sum of half supports along every unit axis is at least 1 because each
square contains its radius-1/2 incircle.

For the zero-core difference d the whole padded input box satisfies
`||d||<5/4` for (9,11) and `||d||<4/3` for (11,13). Core changes have norms at most
`(5/2)epsilon` and `2epsilon`, respectively. The first follows from
`1+sqrt(2)<5/2`; the second change lies entirely along u. For each owner's
independent theta, `||R(theta)n-n||<=|theta|<=epsilon`, so

```
R(theta)n . Delta <= sup(n.d)+dr*epsilon+epsilon*(D+dr*epsilon).
```

We independently enumerate all eight options per pair. For each of the two
owners, `+u`, `-u` and `+v` have projection strictly below 1; in fact the largest
excluded projection is below 7/25 for (9,11), and below 13/100 for (11,13).
Exactly both `-v` owner alternatives remain in each pair. The argument uses the
union of those alternatives, never an assumed common owner or their intersection.

The calculation is uniform over the entire closed box. No angle equality,
angle-sign condition, or subdivision is needed. It includes zero angles,
coincident owner axes, slider endpoints and exact touching. Each strict
exclusion only removes an axis unable to provide separation.

Both actual N values are strictly positive throughout the box. Whichever
remaining owner supplies separation therefore satisfies

```
1 <= N*cos(theta)+X*sin(theta) <= N+epsilon*abs(X).
```

The root bounds give `c+s<141/100`, `abs(c(1-s))<277/1000`,
`abs(c-s)<129/1000` and `T>0`. Thus the worst coefficient in the first stop is

```
141/100+277/1000+(241/100)*(1/5000)
=843741/500000 <17/10.
```

For (11,13), the normal core change is exactly zero, and the tangential bound
is `129/1000+2/5000=647/5000<13/100`. These establish the two epsilon-dependent
bounds. Independent rational arithmetic establishes

```
T/3+13/500000 <3/125,
T/3+183/500000 <1/40.
```

The exact gaps are saved in `receipt.json`; they are approximately
0.0002362568046 and 0.0008962568046, respectively.

### The widened domain is genuinely checked

The old norm cap 6/5 for (9,11) is invalid at the new endpoint b=1/5: there
`N=6/5` at zero core while `X=c(1-s)>0`, so the norm is strictly greater than
6/5. Our independent control rejects that cap. The replacement 5/4 is checked
on the full new padded b interval, rather than transferred from the old bound
`b<=49/300`. Both pair estimates are recomputed on the new box. Containment of
the new b+z interval in the old reviewed interval is additionally checked but
is not used as a substitute for those calculations.

## Interface and verification

The exact interface keeps the physical sliders unscaled: a index 2, b index 21,
z index 25. Relevant core indices are h9x/h9y=16/17, h11=20, h13=24, and
angles 9/11/13=42/44/46. We compare these indices, the root-domain bounds, and
all three linear rows against the producer's `terminal-interface.json`.
A normalized model may use these rows only after verifying its own map into
this same physical domain. In particular `b+z` must not acquire a normalization
factor.

Six independent corruption controls reject an old norm cap, an omitted owner,
a replaced slider endpoint, an unjustified stronger sum target, a changed
normal sign, and an enlarged epsilon. The independent script uses only exact
standard-library rational arithmetic. Producer replay was separately performed
in read-only snapshot mode and passed. No solver, new model, LP, R17
instance, or stress job was run.

Read-only independent replay from the repository root:

```
python3 -B research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/stop-coupled-finish/stop-review/check.py --check
```

Read-only producer replay:

```
python3 -B research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/stop-coupled-finish/stop-producer/check_stops.py --snapshot --check
```

Measured arithmetic/replay CPU totals 0.095293 seconds, including two independent
construction checks, the final read-only independent check, and the producer
snapshot replay. Exact components are in
`resources.json`.

## What is not proved here

These are necessary physical restrictions. They do not restore the old a upper,
b upper or z lower bounds, prove attainability of any retained slider tuple,
validate a normalized dual, eliminate a norm face, prove terminal equality,
establish finite capture, or prove global optimality. Those composition and
coverage obligations remain with their separate producers and reviewers.
