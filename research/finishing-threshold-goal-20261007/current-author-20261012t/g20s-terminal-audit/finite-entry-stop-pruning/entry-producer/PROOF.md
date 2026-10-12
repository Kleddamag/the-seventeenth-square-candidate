# Guarded raw-coordinate stop pruning

For the declared rational entry, the exact coordinate transfer passes.
After the separate larger-root stop theorem is independently accepted and
bound, the following necessary raw-coordinate cuts follow:

```
b >= -213/25000,
b+z <= 49/2000,
z <= 33/1000.
```

This is pruning on a guarded finite entry. It is not a finite contraction,
terminal-reach, enlarged-window rigidity, or optimality theorem.

## Complete input scope

There are seventeen actual unit squares, all contained in `[0,S]^2` and
pairwise interior-disjoint. Sixteen distinct physical squares have labels
`1,2,3,5,6,7,8,9,10,11,12,13,14,15,16,17` in one common frame; physical
square4 remains present with unrestricted pose. One physical square cannot
serve two constrained labels. The actual side satisfies `S<=S*`, the
accepted algebraic side, not merely the slightly larger rational cap.

Use precisely the rational reference centres and orthonormal axes exported
in the pinned accepted mathematical interface. Square13's reference is
`p13_file-(T0/3)*v13`, with `T0=c0*(c0+4-Sref)`; it is not the uncorrected
file centre. The reference side is `4675530093604551/10^15` and no fixed-U
translation is silently applied.

Every one of the29 nonslider position coordinates has absolute value at
most1/200. Every one of the16 independent relative rotation angles has
absolute value at most1/400 **radians**. The raw sliders satisfy
`a in[0,8/25]`, `b in[-1/20,1/5]`, `z in[-1/5,3/40]`. For ordinary labels,
the position coordinates are world-coordinate displacements. The three
exceptions are

```
centre2  = p2  - a*(1,0) + h3*(0,1),
centre11 = p11 + h20*u11 - b*v11,
centre13 = p13_corrected + h24*u13 + z*v13.
```

Angles are independent small representatives modulo a quarter turn. A
half-angle tangent bound1/400 is not the asserted radian bound1/400.
Consumers using such charts must prove their arc lies in this physical
angle range. The sufficient rational bound `|t_relative|<=1/800` implies
`|2 atan(t_relative)|<=1/400` only when t is explicitly the relative
half-angle tangent about this same reference orientation. This is a
mathematical implication, not an engine-schema assertion.

## Exact transfer

Let starred centres and axes be the exact algebraic-root reference and
`delta_i=p_i-p_i*`. For a moving square with raw centre
`p_i+h*u_i+sign*w*v_i`, where `(i,sign,w)=(11,-1,b)` or `(13,+1,z)`, the
exact root coordinates are

```
h* = u* dot delta_i + h*(u* dot u_i) + sign*w*(u* dot v_i),
w* = w + sign*(v* dot delta_i) + sign*h*(v* dot u_i)
       + w*(v* dot v_i-1).
```

The same raw slider w is retained when bounding its error; subtracting two
independent wide slider intervals would destroy this cancellation. The
saved interval calculation evaluates these formulas on the entire closed
entry box, not sampled poses. Ordinary centres transfer by adding delta_i.
Angle drift is bounded by twice the accepted half-angle root enclosure
radius, using the derivative bound `|(2 atan t)'|<=2`.

The full roster of45 root-core bounds is saved. Its maximum is about
`.0050000000000000435`, strictly less than `501/100000=.00501`. The exact
fractions, not this decimal, establish the comparison. The absolute slider
transfer errors are below1e-15 (actual interval bounds are about4.32e-17
for a,6.49e-18 for b and8.53e-18 for z). Thus all upper and lower root
parameter endpoints fit the existing1e-12 padded box, except that the
nonnegative a* lower endpoint uses the actual physical wall:

```
a* = S*-1/2-centre2_x >= 0,
```

because a unit square's horizontal half-width is at least1/2 and its right
wall is at actual S<=S*. This lower bound is not inferred by rounding a
slightly negative transferred interval. Square8 separately gives the
finite side floor `S>=Sref-1/50` with margin greater than149/10000. The
global certified lower bound4.673 is not needed for this implication.

## Composition with the larger-root stop lemma

The new root theorem must cover the full same padded slider box with all
root-core positions and independent angles bounded by501/100000. It gives

```
b* >= -(17/10)*(501/100000) = -8517/1000000,
b*+z* <= T*/3 + (14/100)*(501/100000).
```

Retain the second expression's exact upper enclosure U before rounding to
49/2000. It also gives `z*<=U+8517/1000000`. Let E_b,E_z be the saved signed
intervals for `b*-b` and `z*-z`. Then

```
b   >= -8517/1000000 - upper(E_b),
b+z <= U - lower(E_b+E_z),
z   <= U+8517/1000000 - lower(E_z).
```

The exact comparisons leave strict positive margins to the exported raw
cutoffs: approximately3.0e-6,6.08568e-5 and4.38568e-5 respectively. Paying
the raw-reference errors from only the already rounded root upper49/2000
would not justify keeping that same raw cutoff. The stronger root bound
is an essential dependency of the export.

## Displacement-coordinate sign map

In the stated local orthonormal coordinates,
`xi_(11,2)=-b`, `xi_(13,2)=z`, and `xi_(2,1)=-a`. Therefore the cuts are
equivalently

```
xi_(11,2) <= 213/25000,
xi_(13,2)-xi_(11,2) <= 49/2000,
xi_(13,2) <= 33/1000.
```

The machine export includes both these exact named-coordinate equations
and the unscaled slider rows. They are mathematical necessities on the
complete stated domain. No claim is made that a WX checker already
recognizes a new pruning-step type or that an arbitrary wider root or
tangent interval satisfies these guards.
