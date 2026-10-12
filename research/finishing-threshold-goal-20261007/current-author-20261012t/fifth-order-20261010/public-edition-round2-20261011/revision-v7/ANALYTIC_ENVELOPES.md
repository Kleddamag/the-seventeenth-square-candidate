# Separating-axis envelope lemmas

Write the perturbation as `z=(delta_p, omega, delta_S)` and let `J` denote rotation
by 90 degrees. The reference centres, axes and vertex offsets are rational. The
angles `omega` themselves are real radian increments; they are not replaced by
rational half-angle approximations.

For one candidate separating axis owned by square `o`, with reference normal `n`,
other square `t`, centre difference `d0 + delta_d`, and one of the other square's
vertex offsets `v`, the exact corner gap is

```
f = (R(omega_o)n) · (d0 + delta_d) - 1/2
    - n · R(omega_t - omega_o)v.
```

Non-overlap on this axis requires all four corner gaps to be nonnegative. Before
using an axis, the separating-axis row constructor in [file:JOINT_ROW_CONSTRUCTOR] bounds every competing separating-axis option from
above over the entire current domain. It uses a unique option only when all others
are strictly negative. Unresolved disjunctions are dropped, except for the
parallel-face case below. No option is selected because it looks likely.

Here `g0 = n·d0 − 1/2 − n·v` and the linear form is
`a·z = n·delta_d + omega_o (Jn·d0) − (omega_t−omega_o) n·Jv`.
Thus `g0 + a·z` is precisely the constant-plus-linear Taylor part of the displayed corner gap. The vector `a` here is a row coefficient vector, not the physical slider named a elsewhere.

Let `D >= ||d0||`, `dr >= ||delta_d||`, `wo >= |omega_o|`,
`eta >= |omega_t-omega_o|`, and `V >= ||v||`. The first-order expansion gives
the necessary inequality

```
g0 + a·z + E1 >= 0,
E1 = D*wo^2/2 + wo*dr + V*eta^2/2.
```

The second-order expansion retains the signed quadratic expression

```
Q = omega_o * (Jn · delta_d)
    - (n·d0)*omega_o^2/2
    + (n·v)*(omega_t-omega_o)^2/2,
E2 = D*wo^3/6 + dr*wo^2/2 + V*eta^3/6.
```

Thus `f <= g0 + a·z + Q + E2`. A positive multiple of a square is bounded above
by its secant on the certified interval. A negative multiple is concave and lies
below each tangent; tangents at zero and the interval midpoint are used. The
angle/displacement product is bounded above by both McCormick upper planes. For
`x in [l,u]`, `y in [L,U]`, these are `u*y + L*x - u*L` and
`l*y + U*x - l*U`. Each combination produces a necessary linear inequality.

The bounds use the elementary rotation remainders
`||R(w)-I-wJ|| <= w^2/2` and
`||R(w)-I-wJ+w^2 I/2|| <= |w|^3/6`.
Consequently, retaining curvature signs is materially stronger than assigning
every quadratic contribution an independent positive worst-case error.

For two parallel reference faces, let
`m=(omega_i+omega_j)/2`, `q=(omega_j-omega_i)/2`, and `tau=Jn·d0`.
The union of the two possible owner axes implies

```
(R(m)n)·(d0+delta_d)
  >= cos(q) + |sin(q)| - |(R(m)Jn)·(d0+delta_d)| |tan(q)|.
```

For angle radii at most 0.1, use `cos(q)>=1-q^2/2`,
`|sin(q)|>=|q|-|q|^3/6`, and `|tan(q)|<=|q|+|q|^3`.
If `M>=|m|`, `Qb>=|q|`, and `k=(1-|tau|)/2>=0`, this yields both rows

```
n·d0 - 1 + n·delta_d + tau*m +/- k*(omega_j-omega_i) >= -E,
E = D*M^2/2 + M*dr + Qb^2/2 + Qb^3/6 + |tau|*Qb^3
    + (D*M+dr)*(Qb+Qb^3).
```

Pairs with negative `k` are omitted. The absolute values create two simultaneous
necessary rows, not an unsupported choice of angular branch. This parallel-face
first-order construction builds on Joshua Levy’s squares project (github.com/jlevy/squares), specifically its first-order branch analysis at commit 4261f68098bcec3923159b77dd3dec69aab734aa, `docs/project/reviews/review-2026-10-01-n17-first-order-branches.md`.

Walls are checked for all four vertices of every square, with a first-order
rotation remainder. Directional centre bounds give Euclidean bounds through either
Cartesian coordinates or either square's orthonormal reference frame; taking the
minimum of these valid upper bounds is safe.

These are analytic arguments, not machine-formalized proofs. The independent local-premise review [file:ENVELOPE_REVIEW] rederived both envelope lemmas by hand; its stated certificate-replay limits remain in force. The finite-row derivation is separately assessed in [file:FINITE_ROW_DERIVATION], section (2). Source of the extracted mathematical section: [file:ENVELOPE_SOURCE], lines 92–169; the source’s unreviewed-pilot status does not describe those later independent assessments.
