# Endpoint normalization and its exact C11/C13 position join

Producer theorem; this record does not supply its independent acceptance. The general normalization lemma
is analytic. Its application to the two literal class polygons is checked by
small rational interval arithmetic. No new capture or local closure is claimed.

## 1. Exact endpoint reduction

Fix an ambient square `[0,U]^2` and an exact target side L<=U. A packing of
seventeen unit squares in `[0,S]^2`, S<=L, consists of seventeen distinct
physical parents with pairwise disjoint interiors. Translate every square by

`d(1,1)`, where `d=(L-S)/2`.

The translated packing lies in `[0,L]^2`, with the same unit squares,
orientations and nonoverlap relations. No square is deleted, duplicated,
rescaled or replaced. The exact identity

`p+d(1,1)+(U-L)/2*(1,1)=p+(U-S)/2*(1,1)`

shows that its complete physical pose set in the concentric U frame is
identical to the original pose set. Thus every fixed-U pose predicate,
intersection or complement, occupancy count, capacity fact, common marker,
and physical-parent assignment is preserved, with all closed boundaries and
all equalities. In particular this is not an approximate transport between
similar boxes. The assertion concerns predicates on the fixed-U poses and
fixed constants; an arbitrary additional predicate explicitly involving S
need not be invariant.

Common container symmetries commute with this concentric normalization. In
centred coordinates both operations leave the same points, then apply the
same orthogonal D4 transformation. Reflected or rotated frame choices may
therefore be made before or after padding. A label assignment remains an
injective assignment of the same physical parents. This also covers a theorem
using sixteen named parents and an unrestricted seventeenth: the free parent
is still physically present and satisfies containment and nonoverlap. The
argument never substitutes the nominal label4 for an arbitrary omitted parent.

If S<L, every corner of every translated square belongs to
`[d,L-d]^2`, with d>0. Consequently no physical square touches any of the four
walls of `[0,L]^2`. This remains true after every common D4 symmetry.

It follows that the following conditional finishing mechanism is valid:

> Suppose every physical seventeen-square packing contained in `[0,L]^2`
> and satisfying the available fixed-U capture conclusions either is ruled
> out or is captured, with consistent distinct parents in one common image,
> into a local theorem that forces at least one actual wall contact at side L.
> Suppose the capture conclusions apply to all hypothetical packings under
> consideration and their padded copies. Then no such packing has side S<L.

The endpoint statement needs the entire relevant endpoint packing domain,
not just configurations that are already known to be optimal or to possess
a positive stress. It may be stronger than necessary because it can include
endpoint packings that are not padded copies of smaller ones. That strengthening
is harmless. Capturing every endpoint packing is not established here.

## 2. Use exact S*, and use the wall-contact conclusion

Apply the lemma with the exact algebraic side L=S*, whose accepted root
enclosure is copied as ROOT_GATE.json. The rational reference side
`R=4675530093604551/10^15` is strictly larger than S*. Padding to R instead
does not justify an equality theorem requiring actual side<=S*.

The accepted G20S theorem states that sixteen distinct constrained physical
parents in its window, at actual side<=S*, have all45 exact-root core
coordinates zero. H-plus supplies the same exact-core conclusion for a full
seventeen-square packing in its stated window. Their mathematical conclusions
are stronger than the bare inequality S>=S*.

In both cases, zero exact-root core puts the constrained parent labelled8 at
`(S*-1/2,S*-1/2)` with axis `(1,0)`. It has no slider. Thus it touches both
the top and right walls. This is the explicit contact used above. Under a
common reflection or rotation, the corresponding image still touches actual
container walls; no preferred physical name or wall is required. A consistent
relabelled version of either theorem has the same consequence for whichever
parent carries role8.

This wall statement is pinned by the separately accepted sixteen-square
finite-entry proof, whose final step explicitly gives that centre and axis,
and by the accepted broad G20S and H-plus composition reviews. It does not
require H's further equality-slider classification or confinement of the free
square. The rational file centre must not replace the exact-root centre here.
At side exactly S*, the conclusion S=S* alone is tautological; the core-zero
and wall-contact consequences are what rule out a padded smaller packing.

## 3. Actual class files at the exact endpoint

The frozen44-file join snapshot is
`e48bb1b912f4d419c9e18ab1389acfa33e16357068754f1cb13addb06a19a182`.
Its class reference is `q_i=p_f,i+(U-R)/2*(1,1)`, where p_f is the rational
file reference, corrected at13 by
`p_f,13=p_file,13-(T0/3)*v_f,13`, with `T0=c_f*(c_f+4-R)`.
The actual C11/C13 polygons are read from the rational class files, not their
floating summary or a reconstructed nominal square.

Let z be a class centre in one of these polygons and let `(u_f,v_f)` be its
rational orthonormal local basis. At the normalized endpoint its physical
centre is `z-(U-S*)/2*(1,1)`. Therefore its rational-reference local vector is

`xi_f(S*)=xi_f(R)+(S*-R)/2*(u_fx+u_fy,v_fx+v_fy)`.

This is a single fixed tiny shift, not the drift over all S in[4.674,R].
The accepted side enclosure gives

`S*-R approximately -4.8365888729516855e-17`.

The rational interval calculation proves each coordinate of that shift has
absolute value<10^-16. It evaluates every polygon corner with outward
rational rounding. The resulting C11 and C13 local coordinate hulls both
lie strictly in `[-199951/1000000,199951/1000000]^2`. In particular both
fit the radius1/5 position box with margin strictly greater than49/10^6.
For11 this also supplies the slider bound `|b|<1/5`; for13 it supplies
`-1/5<z<1/5<28/125`, the relevant G20S slider cuts.

The previously recorded actual-side hull extending to approximately-.201028
was correct for that wider range of side values. Endpoint normalization
removes its use in this finishing formulation; it does not assert that the
untranslated smaller packing already belonged to the radius.2 window.

## 4. Rational reference versus exact-root reference

The local input windows above are stated in the rational file reference and
bases. The local theorem's output instead has zero deviation from the exact
algebraic reference. These are distinct statements.

To bind the distinction explicitly, the checker uses the accepted algebraic
root interval for t and exact relations

`c=(1-t^2)/(1+t^2)`, `s=2t/(1+t^2)`, `u*=(c,s)`, `v*=(-s,c)`.

The exact-root centres for11/13 are reconstructed from the pinned bridge
identities:

`u11=c+2s+1/2`, `v11=2c+(c^2-s^2)/2-1`,

`u13=2c+s+1/2`, `T=c(c+4-S*)`,

`p*11=Rot(u11,v11)`, `p*13=Rot(u13,v11-1-T/3)`.

Here `Rot(a,b)=(ca-sb,sa+cb)`. Direct interval projection of the physical
endpoint corners relative to these exact centres and axes independently
fits the same radius199951/1000000 box. The file/exact centre discrepancies
are below10^-15 (computed maxima about2.19e-17 and2.43e-17); each axis
component discrepancy is below10^-50. No drift is rounded to zero.

The radius.2 margins are approximately:

| Polygon | Rational local coordinates | Exact-root local coordinates |
|---|---:|---:|
| C11 | .0000495598345941047 | .0000495598345940784 |
| C13 | .0000494646651118299 | .0000494646651118576 |

All exact endpoints and margins are in RECEIPT.json. Its interval operations
round outward to a rational grid of denominator10^65. The accepted root
existence/enclosure proof is inherited by hash, not replayed or re-solved.

## 5. What is and is not reduced

This supplies a concrete positional join for the actual C11/C13 polygons
after exact endpoint normalization. It also proves the general finishing
reduction from endpoint capture plus a wall-rigid local conclusion to global
exclusion of smaller packings. Neither statement assumes minimality,
nondegenerate contacts, or any stress pattern.

The remaining angle premises, other position/slider factors, loose-role gates,
common assignment, exact charge certificates, case coverage and local exit
closures must still be proved. No overall endpoint capture, G20S admission
of the full C profile, or global optimality theorem follows from these two
position calculations alone. In particular the broad C11/C13 angle arcs
are preserved literally in the receipt and are not declared G20S-admissible.
