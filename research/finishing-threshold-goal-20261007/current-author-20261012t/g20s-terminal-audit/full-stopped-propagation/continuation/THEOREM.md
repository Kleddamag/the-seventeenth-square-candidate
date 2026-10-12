# G20S padded exact-root terminal: producer theorem and replay obligation

The saved continuation gives the exact strict normalized bound

```
rho = 159201934153319/200000000000000 = .796009670766595 < 1.
```

The assertion below becomes an accepted theorem only after independent
replay of the frozen three-round prefix and both continuation rounds, with
the stated accepted geometric and physical-stop dependencies. No enlarged
finite-entry or broad-window theorem is asserted here.

## Precise physical domain

Let `(t*,beta*)` be the unique root in the already accepted root enclosure
of the two polynomials in the pinned `bridge.py`. Define the exact root
side, centres and reference orientation axes by the pinned functions
`bridge.layout(t*,beta*)` and `root_geometry.geometry(t*,beta*)`. In
particular

```
S* = (6+4t*)/(1+2t*-(t*)^2),
p8 = (S*-1/2,S*-1/2).
```

The exact p13 is the corrected layout centre already used in that source,
including the `-T/3` term. These are exact-root reference poses, not the
nearby printed rational file poses. Let `(u,v)` be the orthonormal root
axes of squares9 through14.

Consider a packing of seventeen unit squares in `[0,S]^2` with actual
`S<=S*`. Sixteen distinct physical squares have the labels
`{1,2,3,5,6,7,8,9,10,11,12,13,14,15,16,17}` in one common frame. Physical
square4 remains present with arbitrary pose. No square may supply two
labels. Suppose their centres and independent orientations have the
following exact-root representation (array indices are zero based):

- For `i` other than2,4,11,13, centre `p_i+(h_(2i-2),h_(2i-1))`.
- Square2 has centre `p2-a*(1,0)+h3*(0,1)`.
- Square11 has centre `p11+h20*u-b*v`.
- Square13 has centre `p13+h24*u+z*v`.
- Each constrained square i is rotated by the independent angle
  `theta_i=h_(33+i)` from its reference axes, in radians. Square orientation
  is understood modulo a quarter turn, with these specified small
  representatives.

The core index set is

```
C = {0,...,50} \ {2,21,25,6,7,37}.
```

The unscaled slider values occupy coordinates2,21,25, while6,7,37 are dummy
entries for the unrestricted square4 and do not belong to the core. Require

```
max_{j in C} |h_j| <= 1/5000,
a in [0, 320000000001/1000000000000],
b in [-50000000001/1000000000000, 200000000001/1000000000000],
z in [-200000000001/1000000000000, 75000000001/1000000000000].
```

These are the full G20S rational sliders a<=8/25, b in[-1/20,1/5],
z in[-1/5,3/40], padded by10^-12 on all endpoints except a's lower0.
There is no positivity assumption on active contact forces, no
local-minimality assumption, and no assumption that the full slider box
itself consists of feasible packings.

**Conclusion:** all45 exact-root core coordinates are zero and `S=S*`.
The conclusion does not tighten the surviving sliders to the old narrow
seventeen-square family intervals. Such a classification would need its
own argument using the full physical packing.

## Proof and certificate composition

Let `R=max_{j in C}|h_j|`. Suppose first R>0. Normalize each core coordinate
by R, keep a,b,z unscaled, and introduce each shared product
`q_(w,i)=w*x_i` for the three sliders and sixteen normalized angles. The
normalized core lies in the unit cube and attains absolute value1.

Let `eta=(S-S*)/R`. Square8's horizontal half-width is at least1/2 for
every orientation, so its actual right-wall inequality gives
`S>=S*+h14>=S*-R`. Together with the actual cap `S<=S*`, this proves
`-1<=eta<=0`. This uses no global scalar lower-bound assumption.

The accepted complete52-row/152-option gate proves that the pinned
normalized52 geometric inequalities are necessary throughout the full
padded slider domain for every `0<R<=1/5000`. It includes all owners,
physical corners, independent angles, reference branch signs and exact
root base-gap identities. The 192 product hull inequalities are necessary
for the actual products. The accepted six-step B6 enclosure, whose exact
model sources and input domain are bound here, therefore contains this
normalized physical packing.

The separately accepted physical stop theorem on this same full padded
domain proves

```
b>=-17/50000,  z<=1/40,  b+z<=3/125.
```

Intersect the first two cuts with B6 and append the exact row
`-x21-x25>=-3/125`. These slider inequalities remain unscaled; dividing
them by R would be incorrect. No new contact assumption is inserted.

The frozen prefix performs three rounds of92 signed core/side objective
bounds. The continuation performs two additional rounds, stopping at the
first strict core radius. Every bound follows from nonnegative rational
linear combinations of the current245 necessary rows plus an exact signed
box residual. Every round uses one incoming model for all92 objectives,
then simultaneously intersects the bounds, rounds outwards and refreshes
all48 product hulls before the next model is built. Induction preserves the
normalized physical packing at every step. The separate independent replay
must reconstruct all five models and all460 new exact residual bounds;
the earlier accepted B6 ancestry remains a distinct dependency.

The final box has

```
max_{j in C}|x_j| <= 159201934153319/200000000000000 < 1,
```

contradicting the definition of R. Hence R=0.

When R=0, square8 is axis parallel with centre
`(S*-1/2,S*-1/2)`. Its right wall requires S>=S*. The assumed actual
S<=S* therefore gives S=S*. No rational cap slightly above S* can replace
the actual cap in this equality step.

## Proof boundary

This is a small exact-root terminal theorem. It does not yet show that a
finite-entry rational tube, the HW tree, or the G20S tree reaches this
domain. Those need their own finite contraction, exact rational-to-root
bridge, slider containment, actual-side floor/wall handling and complete
tree coverage with matched labels and angle charts. Common-frame capture
and global optimality remain separate. The R17/type/seam work is not
instantiated.

The unchanged old `rigidity.check` cannot accept the additional physical
stop row and was not run. The new independent certificate replay and its
source are required; solver status is only a proposal aid.
