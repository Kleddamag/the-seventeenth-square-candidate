# Independent sixteen-square physical-scope review

The separate sixteen-square corollary is accepted subject to the exact
producer/source bindings in this review's manifest. The existing
seventeen-square theorem and its frozen interface remain unchanged.

The new statement concerns sixteen distinct physical unit squares carrying
labels

`I={1,2,3,5,6,7,8,9,10,11,12,13,14,15,16,17}`.

They must all be contained in the actual square `[0,S]^2`, have pairwise
disjoint interiors, and use one common reference frame and the injective
label assignment in the producer's mathematical interface. Assume actual
`S<=S*`, the algebraic candidate side. Use the same corrected rational
reference, 29 position coordinates of absolute value at most `1/200`,
16 independent radian angles of absolute value at most `1/400`, and the
closed unscaled slider ranges

`a∈[0,8/25], b∈[-1/20,1/5], z∈[-1/5,3/40]`.

Then all 45 exact-root core coordinates vanish and `S=S*`. This does not
assert that the rational-reference core vanishes. Physical square 4 is
absent from the assumptions; extension to a seventeen-square packing is
neither assumed nor concluded.

## Why deleting a physical square is justified here

I independently read the finite and normalized geometry, root layout,
reference-transfer code, both physical-stop proofs, the full gate review,
the complete B6 ancestry, the stopped root proof and the accepted finite
entry proof. The following is a fresh dependency argument on sixteen
physical squares. It does not apply the old seventeen-square theorem as a
black box to an object outside that theorem's hypotheses.

1. **The coordinate lift exists without a seventeenth square.** Storage
   columns 6, 7 and 37 can be set to zero as algebraic placeholders. Neither
   of the coordinate maps constructs a physical square at those entries.
   The 45 core columns and all 48 slider-angle products omit them. The
   algebraic layout's unused reference point 4 is just a constant in a
   parsed reference array; no other point depends on a physical pose for 4.
   Every audited row has zero coefficients in these three columns.

2. **Every geometric premise is available from the sixteen squares.** All
   wall rows name a label in I. The nineteen contact-pair labels are exactly
   the explicit roster in `THEOREM.md` and in the independently checked
   `PAIRS` and `NORMALS` source literals. No endpoint or separating owner is
   4. The accepted all-option geometric argument remains a necessary
   condition on two actual nonoverlapping unit squares: it includes both
   owners, independent orientations, actual corner supports and equality
   cases. Pair nonoverlap follows directly from the new sixteen-square
   packing hypothesis. There is no force-positivity, local-minimum, area,
   charge-count or missing-square premise to replace. The product rows are
   valid for the actual scalar products in the lift.

3. **The reference and side guards also survive independently.** The
   accepted root enclosure gives `S*<Sref`. Square 8 alone, its vertical
   half-width at least `1/2`, and its raw vertical displacement at least
   `-1/200` imply `S>Sref-1/50`. Thus the finite side coordinate belongs to
   `[-1/50,0]` without a scalar lower bound for seventeen squares. The
   affine/axis transfer is labelwise on I; the square-11 and square-13
   slider correlations are retained in that calculation. The only physical
   endpoint repair is `a*>=0`, obtained from square 2's right wall and
   actual `S<=S*`. A larger rational cap would not suffice for this repair.

4. **The stop cuts require only named pairs in I.** Both the enlarged
   `501/100000` root stop lemma and the small `1/5000` lemma use only
   nonoverlap of 9/11 and 11/13. Their sixteen separating alternatives,
   independent owner angles, norm estimates, subdivisions and strict
   slack were already independently proved on the whole padded slider
   domain. No hypothesis in their derivations uses square 4. Applying the
   enlarged lemma and the same reference-error payment therefore derives
   the raw cuts `b>=-213/25000`, `b+z<=49/2000`, `z<=33/1000` for the
   sixteen-square configuration. These remain derived necessities, not
   extra assumptions added to the new theorem.

5. **The finite arithmetic is cardinality-independent.** For any valid
   lifted point satisfying `A x>=d`, a saved nonnegative multiplier vector
   proves

   `c·x >= λ·d + min_{y∈B}(c-λA)·y`.

   The accepted seventeen complete finite rounds establish this algebraic
   implication with all signed residuals retained, simultaneous outward
   updates and all 48 products refreshed. Since every initial row has just
   been justified on sixteen physical squares, induction preserves their
   lift through every round. The old abandoned partial round 16 is not used.
   The accepted final maximum raw core radius
   `64007486789/10^15` is strictly below `1/10000`. The same labelwise
   transfer consequently gives exact-root core radius below `1/5000` and
   the padded slider box, without constructing any square 4.

6. **The entire small-root proof applies, rather than just its conclusion.**
   If `R=max|h_j|>0`, divide the 45 root core coordinates by R and leave the
   sliders unscaled. Square 8's right wall yields `S>=S*+h14>=S*-R`, so
   the normalized side is in `[-1,0]`. The initial 52 geometric rows and
   192 product rows now hold for the sixteen-square lift. The first five
   B6-ancestry rounds imported only old nonnegative weight dictionaries,
   while rebuilding the current whole-domain rows and recomputing bounds.
   The sixth round used the entire global B5 box; it did not impose the
   separately derived possible norm face. All these implications are
   algebraic and retain the sixteen-square point. The small physical stops
   justify intersecting B6 with `b*>=-17/50000`, `z*<=1/40` and appending
   `-b*-z*>=-3/125`. The five accepted stopped rounds imply

   `max|h_j/R| <= 159201934153319/200000000000000 < 1`,

   contradicting the definition of R. Therefore R is zero. Square 8 is then
   axis-parallel with centre `(S*-1/2,S*-1/2)`; its wall gives `S>=S*`,
   and the assumed opposite inequality gives equality.

This audit of the entire necessity chain is the extra mathematical step.
The historic review documents state seventeen-square hypotheses, but their
proved row, transfer and arithmetic lemmas have the smaller dependencies
listed above. The new result reuses those lemmas, not an unjustified
weakening of the historic theorem's logical statement.

## Independent checks and cost

`check.py` imports only Python standard-library modules, not any producer
checker, model, solver or geometry module. It independently checks the
literal pair/normal/dummy rosters, all 12,929 saved finite rows and all
1,564 objective identities, seven saved normalized/B5/stopped model files,
the exact five-round-to-B6 inheritance, the accepted review hashes, and
the two exact physical-side comparisons. All row dummy coefficients are
zero and every product angle belongs to I. This is a metadata/dependency
check, not a new geometric proof or another arithmetic replay of those
certificates.

Six controls independently reject a wall for 4, a pair involving 4, owner
4, angle 37 in a product, a nonzero dummy coefficient and an unrecognized
seventeen-square count row. A separate interface check binds the frozen
producer output and verifies that the new guards require sixteen contained,
pairwise interior-disjoint physical squares with no extension assumption;
it also compares all numerical pose data with the unchanged accepted
seventeen-square interface.

The metadata pass took 0.171208 CPU seconds. The final manifest records the
separate interface check and conservative total CPU time. No optimizer, model construction, symbolic identity
replay or full tree run occurred. 

Safe metadata replay from the repository root uses a new output pathname:

```sh
python3 -B research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/sixteen-square-corollary/independent-review/check.py --output /tmp/sixteen-scope-NEW.json
```

The checker creates output exclusively and refuses to replace an existing
file. Without `--output` it prints to stdout. The independent interface
checker has the same output discipline. Do not regenerate frozen receipts
in place.

## Remaining limitations

This is a local conditional theorem; sixteen squares can of course be
packed differently outside this window. It proves neither a global
sixteen-square optimum nor capture into the window. It does not classify
the expanded equality sliders, supply a seventeenth square, validate any
WX fact extension or accept an HW/G20S tree. Such uses still require their
own complete geometric/root/terminal joins. The actual-side hypothesis,
common frame, distinct physical labels, full unit-square containment,
pairwise interior-disjointness, corrected reference and independent radian
angle conventions cannot be omitted.
