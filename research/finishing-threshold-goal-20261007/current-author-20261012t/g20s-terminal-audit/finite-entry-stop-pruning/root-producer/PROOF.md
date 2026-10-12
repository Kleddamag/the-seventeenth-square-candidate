# Physical stop pruning at exact-root radius 501/100000

This conditional geometric theorem proves necessary slider cuts on the
declared exact-root domain. This producer record does not supply independent acceptance.
It is not a contraction, terminal equality theorem, larger-window capture
result, or global lower bound. No LP, model or symbolic solver is used.

## Domain and inherited identities

Set epsilon0=501/100000 and delta=1/10^12. Use the exact algebraic root,
original labels and coordinate conventions of the accepted G20S analytic
gate. The exact-root physical sliders are allowed over the full closed box

    a∈[0,8/25+delta],
    b∈[−1/20−delta,1/5+delta],
    z∈[−1/5−delta,3/40+delta].

All45 constrained core coordinates have magnitude at most epsilon, for
0≤epsilon≤epsilon0. The sixteen constrained angle increments are independent
and measured in radians. All17 physical unit squares are present and have
disjoint interiors; physical square4 is unrestricted and unused in this
two-pair argument. The sliders are **unscaled**, at indices2,21,25. No
orientation equality, fixed owner, positive-angle assumption, or extra
slider restriction is imposed.

The intended application assumes actual S≤S*. The lemma itself uses the
exact-root centre formulas and nonoverlap; a rational-frame finite entry
must separately prove its transfer into this root box. The old analytic
gate was checked at epsilon1/5000. It supplies only unchanged reference
identities, the exact root enclosure and the padded slider conventions
here: none of its smaller-radius option exclusions is extrapolated.

Let u=(c,s), v=(−s,c), with c=(1−t²)/(1+t²), s=2t/(1+t²), and
T=c(c+4−S*). Hence c²+s²=1 exactly. The previously independently reviewed
layout identities give

    u·P9=1/2+cs+2s,        v·P9=2c+(c²−s²)/2,
    u·P11=c+2s+1/2,        v·P11=v·P9−1,
    u·P13=2c+s+1/2,        v·P13=v·P11−1−T/3.

`dependencies.json` pins the accepted root interval, unchanged layout and
coordinate-map sources, previous stop production and its separate
independent review. The executable checks those hashes and source identities
without importing numerical proof code. Every estimate at the new radius
below is freshly evaluated using exact rational intervals.

Write the actual centres as P9+h9, P11+h11*u−b*v and
P13+h13*u+z*v. Each component of h9 and the two scalar h11,h13 is bounded
by epsilon. Directed centre differences Delta=X*u−N*v obey

    (9,11):   X=c(1−s)+h11−u·h9,  N=1+b+v·h9,
    (11,13):  X=c−s+h13−h11,      N=1+T/3−b−z.       (1)

The normal core contribution in the second equation is exactly zero.

## Fresh complete SAT coverage at the larger radius

For the core-zero difference d, exact interval arithmetic over the whole
padded box establishes

    ||d9,11||<5/4,     ||d11,13||<4/3.

The corresponding displacement perturbation norms are at most
(5/2)epsilon and2epsilon. The first follows from1+sqrt(2)<5/2; the
second is the difference of two scalar displacements along u. The old
6/5 norm cap is explicitly tested and rejected on this slider box.

For either owner o and each signed reference normal ±u or±v,
the true separating normal is R(theta_o)n. Since
`||R(theta_o)n−n||≤|theta_o|≤epsilon`, its projection has the rigorous bound

    (R(theta_o)n)·Delta
       ≤ sup(n·d)+dr*epsilon+epsilon*(D+dr*epsilon).    (2)

The separating-axis theorem requires at least one of these eight directed
projections per pair to be at least the sum of the two unit-square
half-widths. That sum is at least1 because each square contains a radius1/2
disc. The verifier enumerates both owners and all four signs/axes. At
epsilon0 it strictly excludes +u,−u,+v for each owner. Thus12 alternatives
are excluded over the two pairs and both−v choices per pair remain.
Every option has its own exact reference interval, projection bound and
strict gap saved in `receipt.json`.

The same fresh calculation proves N>0 for the entire new-radius domain.
For the surviving owner, the projection is

    N*cos(theta_o)+X*sin(theta_o) ≤ N+epsilon*|X|.

Consequently nonoverlap implies `1≤N+epsilon*|X|`. Both independent owners,
either angle sign, coincident candidate directions, exact touching,
zero-angle cases and closed parameter endpoints are covered. No surviving
option is claimed to be physically realizable by a whole packing.

## The larger-radius stop constants

The accepted exact root enclosure gives strict constants

    c+s<141/100, |c(1−s)|<277/1000, |c−s|<129/1000.

For the first pair, (1) gives

    b ≥ −epsilon*[141/100+277/1000+(241/100)*epsilon].

At epsilon0 the bracket is exactly bounded above by
`16990741/10000000=1.6990741<17/10`. Therefore

    b ≥ −(17/10)*epsilon.                            (3)

For the second pair, |X|<129/1000+2epsilon. At epsilon0 this is
13902/100000<14/100. The previous coefficient13/100 fails and is retained
as a negative control. The corrected conclusion is

    b+z ≤ T/3+(14/100)*epsilon.                      (4)

At the full epsilon0 the exact root enclosure proves the closed simple cuts

    b ≥ −8517/1000000,
    b+z ≤ 49/2000,
    z ≤ 33/1000.                                   (5)

The sum and z comparisons have strict rational slack. The authoritative
stronger rational upper bounds are saved in `stronger_conclusions`:

    sum_upper = upper(T/3)+(14/100)*(501/100000),
    z_upper   = sum_upper+8517/1000000.

These stronger values, rather than only the rounded cutoffs in(5), are
exported for the separate rational-coordinate transfer to pay its drift.
The b lower cutoff in(5) is exactly the specialization of(3), so that
transfer must separately weaken it if its coordinate drift requires this.

## Interface, checks and limits

`root-interface.json` provides the exact root slider guards, maximum core
radius, angle units, all three linear inequalities and their stronger
rational slack. A consumer must bind its own actual pose-to-root map and
full guarded entry before applying them. Shared product variables in a
relaxation do not themselves establish those physical hypotheses.

The check rejects an enlarged epsilon, incorrect norm caps, the old sum
coefficient and unjustifiably stronger displayed bounds. Comparisons use
fractions only; no source floats or sampled angles enter the proof.

Read-only replay from the repository root:

```sh
/usr/bin/python3 -B research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/finite-entry-stop-pruning/root-producer/check_stops.py --snapshot --check
```

`--snapshot` selects the frozen dependency copies. Without it, the current
repository files must match exactly the same hashes. Every new-radius
SAT/norm/positivity/coefficient guard is recomputed either way. Cost and
source hashes are recorded in the manifest.
