# Conditional local optimality without a slider partition

This is a computer-assisted **local theorem**. The global packing problem remains
open. The exact arithmetic checks below have passed; the elementary geometric and
analytic lemmas are given here as hand proofs, not a proof-assistant formalization.

## Theorem and input domain

Use the labels, rational moving reference `p(w)`, normal-coordinate map `H`, and
three parameters of [README.md](README.md). Let a physical packing of 17 unit
squares have side `S<=S*`, where `S*` is the side at the specified algebraic root.
Suppose, after one fixed rigid placement and labelling, it has

- every one of the 29 core position coordinates within `1/100` of the rational family;
- every one of the 16 non-rattler angle increments within `1/200` radians;
- `a in [0,1/4]`, `b in [-1/2500,1/12]`, `z in [-1/8,1/16]`.

Square 4 is unrestricted except that it participates in the physical packing.
The packing's container has its lower-left corner at the reference origin.
Then **`S=S*`**, and all sixteen squares other than square 4 belong exactly to the
endpoint family at the same algebraic root. There is no occupancy-state premise.

The theorem does not assert that every packing admits this placement and labelling.
In particular, the three input slider bounds remain hypotheses, not conclusions.

## 1. Root and layout

`bridge.root_enclosure` reconstructs the two endpoint polynomials, verifies them
against the pinned input, and takes the rational midpoint of the retained root
certificate. With `C=J(midpoint)^-1`, define `T(x)=x-C F(x)`. All arithmetic is exact
rational interval arithmetic. On the closed infinity-norm box of radius `10^-12`,
the checker establishes

```
q = sup ||I-C J(x)||_infinity < 1
eta = ||C F(midpoint)||_infinity
eta + q*10^-12 < 10^-12.
```

The mean-value bound makes `T` a contraction mapping of this box into itself.
Banach's theorem gives its unique fixed point; since `C` is invertible this is a
root of `F`. Its distance from the midpoint is at most `eta/(1-q)`. The checker
rounds this enclosure outward and evaluates the endpoint layout by rational
functions. Every interval operation rounds outward at a `10^-80` rational grid.

`root_geometry.py` gives centres, axes and vertex offsets at this root. The axes
use `(1-t^2,2t)/(1+t^2)` and the corresponding negative-beta orientation, so they
are exactly orthonormal. The small input box selects unambiguous angle lifts.

## 2. The finite capture and frame transfer

`uniform-relational-projection.json` contains 11 rounds, each with 312 signed
objectives: 92 individual-coordinate objectives and 220 objectives for 110
combined quantities. `relational.check` reconstructs all necessary rows and
replays all 3,432 rational dual bounds. The individual and combined quantities
used in a round depend only on previously certified intervals.

The exact geometric envelope derivation is in [README.md](README.md). The
relaxation treats the full slider box at once. In particular, `w*omega` is shared
across constraints, and the small-displacement Taylor remainder excludes the
motion of the moving reference.

The contractor assumes `S>=Sref-1/50`. This follows from the stated input domain
without any global lower-bound theorem: square 8's horizontal reach is at least
`1/2` at every orientation, and its centre's input lower bound gives
`S >= p8_x + 1/2 - 1/100`. The checker verifies that this exceeds its required floor.
The root enclosure also proves `S*<=Sref`.

The final core bounds are transferred to the exact-root frame by interval
arithmetic. For an ordinary centre coordinate, add its reference-coordinate drift.
For squares 11 and 13, project onto `u*`; the drift includes the entire allowed
slider motion projected against the difference between the two frames. For angle
increments use `|2 atan(t)-2 atan(t*)|<=2|t-t*|`.

The largest transferred core radius is less than `5.518e-5`, hence less than
`epsilon=1/5000`. This is a finite inclusion, not yet an equality argument.

The bridge also transfers the parameters. If `d` is the reference-position
difference, a slider centre has the form

```
p_rat + h*u_rat + sign*w*v_rat,
```

with sign -1 for 11 and +1 for 13. Its exact-root parameter is
`sign*v*·d + sign*(v*·u_rat)h + (v*·v_rat)w`.
For square 2 it is `a*=S*-1/2-p2_x+a`. Physical containment in `S<=S*` implies
`a*>=0`, since its horizontal reach is at least `1/2`.
The checker proves that all three exact parameters lie in

```
B+ = [0, 1/4+10^-12]
     × [-1/2500-10^-12, 1/12+10^-12]
     × [-1/8-10^-12, 1/16+10^-12].
```

This small explicit padding resolves parameter-boundary transfer without using
H-268 or its occupancy assumption.

## 3. Exact rows at the moving algebraic family

The final local argument retains 52 first-order contact and wall rows over `B+`.
For each row, `rigidity.symbolic_identities` reconstructs its base gap as a rational
function of `t,beta`. It checks that the numerator is identically zero or exactly
divisible by one of the two root polynomials. Its denominator is nonzero on the
proved root enclosure. It also checks that the coefficient of each slider's
translation in the base gap vanishes identically. Thus the base gap is **exactly
zero at every point of the moving family**, not merely small in a root interval.

The three axis-parallel reference tangential offsets used as zero are separately
checked as symbolic identities. All remaining derivative coefficients are evaluated
by outward intervals at the algebraic root; their uncertainty is paid in each row.

For each of the 19 retained pairs, the checker bounds all eight separating-axis
options over the entire root enclosure, `B+`, and the full core cube of radius
epsilon. It proves exactly the declared alternatives remain: eleven unique owners
and eight pairs of parallel reference normals. Unavailable options have a strictly
negative gap upper bound. All parallel offsets stay in their stated sign branch,
with absolute value less than one. No floating choice selects an owner or sign.

The argument uses necessary conditions only. Dropping the rattler and all other
pairs enlarges the feasible set and cannot remove a physical packing.

## 4. Normalize by the actual largest deviation

Let `h` be the 45 exact-root core coordinates, and suppose
`R=||h||_infinity>0`. The bridge gives `R<=epsilon`. Put

```
x=h/R,       s=(S-S*)/R,       q[k,i]=w[k]*x_angle[i].
```

Then `||x||_infinity=1`. The parameters stay unscaled in `B+`, and the 48 product
variables satisfy the four McCormick inequalities with the current normalized
angle bounds. Exactly the same product variable occurs in every relevant row.

The side coordinate satisfies `-1<=s<=0`. The upper bound is the theorem's side
hypothesis. For the lower bound, square 8's reference x-coordinate is `S*-1/2`,
its x-displacement is at least `-R`, and its horizontal reach is at least `1/2`.
Consequently `S>=S*-R`.

These facts put every hypothetical nonzero physical deviation in the initial
100-variable normalized box. The three rattler placeholders are zero and unused.

## 5. Necessary inequalities valid at every scale

For a unique owner, write `d(w)` for the moving-reference centre difference,
`dh` for the normalized core displacement, `omega_o=R*x_o`, and
`eta_actual=R*(x_t-x_o)`. First-order expansion of the exact corner gap, using
its zero base gap, gives after division by `R`

```
f/R <= A(w)·x + epsilon*(D*Wo^2/2 + Wo*dr + V*Eta^2/2),
```

where `D>=||d(w)||`, `dr>=||dh||`, `Wo>=|x_o|`, `Eta>=|x_t-x_o|`, and `V<=1`.
The inequality follows from `||R(theta)-I-theta J||<=theta^2/2` and
`0<R<=epsilon`. The `w*x_o` terms of `A(w)·x` are the shared product variables.
For walls the corresponding normalized remainder is `epsilon*Wo^2/2`.

For a pair of parallel faces, set normalized
`m=(x_i+x_j)/2`, `q=(x_j-x_i)/2`, and `tau(w)=Jn·d(w)`.
The separating-axis union and elementary sine, cosine and tangent bounds give
both first-order rows with error bounded by

```
E/R <= epsilon*(D*M^2/2 + M*dr + Q^2/2)
       + epsilon^2*(Q^3/6 + |tau|*Q^3)
       + (D*M+dr)*(epsilon*Q + epsilon^3*Q^3),
```

where `M>=|m|`, `Q>=|q|`. This is obtained by substituting physical angles
`R*m,R*q` and core displacement `R*dh` into the parallel-face remainder in the
point-pilot proof, dividing by `R`, then bounding each remaining nonnegative power
of `R` by the corresponding power of epsilon. The angle bounds are far inside
that lemma's `0.1`-radian range.

The root-dependent derivative coefficient interval `a_j in [L_j,U_j]` is replaced
by a rational coefficient `a0_j`, paying
`max(|a0_j-L_j|,|a0_j-U_j|)*max(|lo_j|,|hi_j|)` on the normalized box. This is
proportional to the normalized variable, **not a constant root-gap error divided
by R**. Exact base tightness in section 3 is what makes the all-scale argument work.

Every row thus holds for every physical `0<R<=epsilon`. There is no limiting
argument based on a sequence of numerically smaller boxes.

## 6. Four uniform rounds force a contradiction

`uniform-rigidity.json` stores four rounds of 92 signed objectives. Each round
reconstructs the all-scale necessary inequalities on the previous normalized box
and applies exact residual-corrected weak duality. The three slider intervals are never narrowed or subdivided; outward grid
rounding can enlarge an endpoint by less than `10^-15`. The four bounds on the largest normalized core coordinate are

| Round | Maximum absolute normalized core coordinate |
| --- | ---: |
| 1 | 1 |
| 2 | 1 |
| 3 | 0.976096442707191 |
| 4 | `105112045749639/250000000000000` = 0.420448182998556 |

All 368 dual objectives pass rational replay. The final bound is strictly less
than one, contradicting the defining equality `||x||_infinity=1`. Therefore
`R=0`: all 45 exact-root core deviations vanish.

With core deviations zero, square 8 reaches the family's right wall, so physical
containment gives `S>=S*`. Combined with `S<=S*`, this proves equality. The sixteen
non-rattler squares have exactly the family centres and orientations at their
remaining slider values; square 4 may occupy any position where it physically fits.

## Validation and scope

The complete chain is replayed by `verify.py`; its output binds the capture,
bridge, and rigidity certificate digests, verifies coordinate and parameter-domain
inclusion, and records the source digests. Exact positive and mutation controls
are separate receipts. The independent numerical diagnostics check the nonlinear
rows at three physical scales; they are debugging evidence, not the all-scale proof.

The algebraic endpoint formulae and polynomial definition come from the cited
upstream work. This proof reconstructs their root enclosure and the retained
contact identities. It does not need a fresh replay of the upstream H-261/H-268
local theorem, and it does not reuse the upstream partition of the slider box.

**Still missing:** a global argument that forces every potentially better packing
into the stated neighbourhood and slider box, allowing for labellings, orientations,
and other contact arrangements. Nothing in this local proof supplies that argument.
