# Sixteen-square finite-entry rigidity

Producer proof; independent scope review is a separate premise. This is a
new theorem with sixteen physical squares. The previously accepted theorem
with seventeen physical squares is preserved unchanged.

Let

```
I = {1,2,3,5,6,7,8,9,10,11,12,13,14,15,16,17}.
```

Suppose sixteen **distinct actual unit squares**, labelled by I in one
common frame, are contained in the actual container `[0,S]^2` and have
pairwise disjoint interiors. Assume `S<=S*`, where S* is the algebraic root
side of the pinned `bridge.layout`; a larger rational cap does not replace
this assumption. There is no square with label4 in the hypotheses, and no
assumption that these sixteen squares can be extended to seventeen.

Use the rational reference and the exact square-by-square data in
`MATHEMATICAL_INTERFACE.json`. Its side is
`Sref=4675530093604551/10^15`. In particular the reference for13 is corrected
by `p13_file-(T0/3)*v13`, where `T0=c0*(c0+4-Sref)`. No fixed-U recentering
is implicit. The centre formulas are

```
ordinary i in I\{2,11,13}:  p_i + (h_(2i-2),h_(2i-1)),
2:                         p2 - a*(1,0) + h3*(0,1),
11:                        p11 + h20*u11 - b*v11,
13:                        p13_corrected + h24*u13 + z*v13.
```

Each square i has independent relative angle `h_(33+i)` in **radians**
about its specified reference axes, using the stated small representative
modulo a quarter turn. Require every one of the29 nonslider position
coordinates to have absolute value at most1/200 and each of the16 angles
to have absolute value at most1/400. The unscaled sliders have the full
closed ranges

```
a in [0,8/25], b in [-1/20,1/5], z in [-1/5,3/40].
```

**Conclusion.** All45 exact-root core coordinates vanish and `S=S*`.
The conclusion concerns the exact-root reference, not zero deviation from
the nearby rational file. It does not classify the surviving sliders or
assert extendability to a seventeen-square packing.

## Why the proof applies to sixteen physical squares

This is an audit of the physical premises of the inequalities and their
already independently verified arithmetic. It does not apply the earlier
seventeen-square theorem after deleting a hypothesis.

### 1. A physical sixteen-square configuration has the required model lift

The pinned rational `uniform.geometry` and exact-root
`root_geometry.geometry` omit zero-based square index3. The model's storage
entries6,7,37 are set to zero solely to embed the coordinates in the
unchanged100-variable array. No physical pose is assigned to them. All
saved rows have zero coefficients in these three columns. All48 lifted
products are a, b or z times one of the16 constrained angular coordinates;
none involves angle37. The45 core coordinates are
`{0,...,50}\{2,21,25,6,7,37}`.

Every wall inequality is containment of a named square in I. Every pair
inequality comes from one of these19 pairs:

```
(1,3),(1,5),(2,6),(3,13),(5,9),(5,11),(6,14),(7,10),(8,16),
(9,10),(10,12),(10,15),(11,12),(12,14),(12,16),(13,14),(14,17),
(15,16),(16,17).
```

All endpoints belong to I. The accepted gate checks both owners, the
relevant four physical corners, independent angles, equality boundaries
and every separating-axis alternative before using a surviving row. The
necessity argument is a fact about the two named nonoverlapping unit
squares; it uses no third square, occupancy count, contact-force premise,
or local minimality. Each product hull is valid for its actual scalar
product. Thus the same complete necessary rows hold for the physical
sixteen-square configuration.

The root-enclosure polynomials and the17-entry reference arrays define
fixed algebraic constants. Computing the unused reference point p4, or
checking its stored orientation while parsing the reference, is not a
physical-square hypothesis. No other centre formula depends on a physical
pose for4.

### 2. The side and reference-transfer guards are still physical

The accepted enclosure proves `S*<Sref`. Square8's vertical support radius
is at least1/2 at every orientation. Its raw entry therefore implies

```
S >= p8_y - 1/200 + 1/2 > Sref - 1/50.
```

Both strict comparisons are checked as exact fractions in `receipt.json`.
Consequently the finite side variable `S-Sref` belongs to `[-1/50,0]`.
This uses no area bound, certified scalar lower bound, or seventeenth
square.

The raw-to-root transfer is a separate affine calculation for each label
in I. At11 and13 it preserves the same slider when estimating the tiny
axis change, including the h-slider cross terms; at ordinary labels it
adds the reference-centre drift. Independent angle drifts are bounded
from the exact half-angle root intervals. Its only noninterval repair is

```
a* = S* - 1/2 - centre2_x >= 0,
```

which follows from square2's right wall and `S<=S*`. This likewise uses
only a physical square in I. The accepted full-entry transfer gives all45
root core coordinates below501/100000 and the padded root slider domain

```
a* in [0, 8/25+10^-12],
b* in [-1/20-10^-12, 1/5+10^-12],
z* in [-1/5-10^-12, 3/40+10^-12].
```

The larger-radius stop proof uses only pairs9/11 and11/13. Their full16
SAT options and both independent owners were rechecked on this domain.
Its stronger exact sum bound, followed by the accepted reference-error
payment, proves the raw necessary cuts

```
b >= -213/25000, b+z <= 49/2000, z <= 33/1000.
```

No square4 premise is hidden in this transfer or stop argument. The cuts
are derived necessities, not additional entry assumptions.

### 3. The accepted finite contraction is an arithmetic implication

Start with the closed raw entry, its physical side interval and these raw
stop cuts. Embed the actual coordinates and all true slider-angle products
in the100-variable box. All17 **complete arithmetic rounds** use only
the necessary rows identified in step1, together with the unscaled row
`-b-z>=-49/2000`. The number17 here counts rounds, not physical squares.

For a row system `A x>=d`, any saved nonnegative rational weights lambda
prove the exact bound

```
c.x >= lambda.d + min_{x in B} (c-lambda.A).x.
```

The exact signed residual minimum, simultaneous closed-box intersection,
outward rounding and product refresh preserve every physical lift. These
operations depend only on the necessary row system and the incoming box,
not on a packing's cardinality. The separate accepted reviews cover all
1564 signed bounds in the17 complete models. The abandoned partial old
round16 contributes nothing to the induction.

The accepted final box has maximum raw core absolute value
`64007486789/10^15<1/10000`. The accepted small-reference transfer, audited
in step2 for its actual dependencies, consequently puts all45 exact-root
core coordinates below1/5000 in the same padded slider domain.

### 4. The complete normalized ancestry also needs only I

Write the exact-root core as h and let `R=max |h_j|` over its45 coordinates.
If R>0, normalize the core by R, keep a*,b*,z* **unscaled**, and lift their
products with the normalized16 angles. The core attains absolute value1.
Square8's exact-root centre is `(S*-1/2+h14,S*-1/2+h15)`. Its right wall
and support at least1/2 imply `S>=S*+h14>=S*-R`. Hence the normalized side
`eta=(S-S*)/R` lies in `[-1,0]`; again there is no area or count premise.

The accepted full padded gate gives52 necessary geometric rows for every
`0<R<=1/5000`. Each is one of the wall/pair implications of step1. Together
with192 valid product-hull rows they give the244-row necessary system.
The entire global B6 ancestry is accounted for:

* The first five rounds rebuild this same244-row kernel on each incoming
  box. Older certificates supplied only numerical nonnegative weights and
  objective identities. No old physical domain, old bound or old final
  box is imported. Their460 exact bounds were independently replayed.
* The sixth round uses the **global B5 box**, not a restriction to a norm
  face. Its92 bounds were independently checked;85 have empty weight
  lists, as does one selected objective. Its entire resulting B6 is valid.
  The separately discussed sole possible norm face is a consequence, not
  an assumption in any bound used here.

The smaller-radius physical stops are again solely the two-pair argument
on9/11 and11/13. They give `b*>=-17/50000`, `z*<=1/40`, and
`b*+z*<=3/125` on the full padded root box. Intersect B6 with the first two
cuts, refresh products, and append the unscaled row
`-b*-z*>=-3/125`. The five accepted stopped rounds use245 rows and the
same exact weak-duality induction. No face is fixed in these models.
Their independent reviews establish

```
max |h_j/R| <= 159201934153319/200000000000000 < 1.
```

This contradicts the definition of R, so the exact-root core is zero.
When it is zero, square8 is axis parallel at `(S*-1/2,S*-1/2)`. Its right
wall forces `S>=S*`, completing the equality claim.

## Dependencies, validation and scope

`receipt.json` binds the frozen reference/model sources and every accepted
review used above. Its read-only metadata check verifies all12929 saved
finite rows, the52-label normalized roster, B5 and the five stopped model
arrays, the dummy/product rosters, exact B5-prefix/B6 inheritance, and the
physical side comparisons. It does not reconstruct models or replay old
dual arithmetic. Those arithmetic implications are inherited only from
the separately hashed independent reviews; the new physical-scope audit
above is the additional proof obligation.

The theorem has closed position/slider boundaries and independent angular
representatives. It assumes all16 physical unit squares are contained and
pairwise interior-disjoint in the same frame. It makes no assertion that
an arbitrary sixteen-square packing enters the tube, that a seventeenth
square can be added, that the widened equality family has already been
classified, or that any HW/G20S tree or new checker rule has been accepted.

Read-only metadata replay from the repository root:

```sh
python3 -B research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/sixteen-square-corollary/producer/audit.py --check
```

Only Python's standard library is used. No solver, numerical model build,
symbolic identity replay or tree job was run for this corollary.
