# Independent acceptance of the complete G20S analytic gate

Reviewer `Codex`; producer `Codex`.

**Accepted:** the complete contact-option and analytic-domain gate for the proposed terminal slider box. This is not a contraction certificate, terminal theorem or optimality proof. No solver, discovery, broad-tree computation or R17/type case was performed by this reviewer.

The rational-frame slider box is `a in[0,8/25]`, `b in[-1/20,1/5]`, `z in[-1/5,3/40]`. The root gate uses the exact-root core radius `1/5000`, zero lower a endpoint and outward `10^-12` padding on the other five slider endpoints. The finite-entry check uses the unpadded rational slider box, position radius `1/200` and sixteen independent angle radii `1/400`.

## Independent geometric result

`check.py` imports no producer geometry, row generator or checker. It reuses only this reviewer's previously sealed rational interval/layout utility, reconstructs the exact-root centres/axes and both coordinate maps, and enumerates both owners, both axes and both normal signs for every one of the nineteen retained pairs. Its interval grid is `10^-90`, distinct from the producer's `10^-80` implementation.

At the root scale all **152 alternatives** are checked. Exactly 125 have strictly negative upper gaps, each **less than `-1/60`**. The largest is approximately `-0.01682963400014499`. The remaining 27 options are exactly the expected eleven single-owner alternatives and sixteen alternatives on eight parallel pairs. These are the options not excluded by this necessary-condition audit; no surviving option is asserted feasible in a complete packing.

The independent check also covers **all 152 alternatives at the finite entry**, using an independently derived first-order corner envelope on the rational reference. Exactly the same 27 alternatives remain. Every one of the other 125 has upper gap **less than `-9/1000`**. The largest finite-entry upper bound, approximately `-0.00904525797005706`, occurs for owner 5's `+x` option against square 11. This is stronger coverage than the preceding one-option assessment. It is still not a finite contraction.

For the root enclosure, direct affine centre/core bounds prove `D<8` and `dr<3`. The upper gap is bounded by

`sup n.d(w) - 1/2 - lower_support + 3 epsilon + (8+3 epsilon)epsilon + 2 epsilon`.

The first added term pays for the core displacement; the next pays for the owner's axis rotation; the final term pays for the other square's relative support rotation. The support lower bound takes the largest lower projection among its four actual reference corners. Both independent angles and all closed boundary/degenerate cases are retained. For the second owner, central symmetry justifies the same centre-difference convention. A strict negative bound excludes the physical SAT option, without any contact-force assumption.

The finite audit expands a fixed reference corner gap directly. Its linear angle coefficients are `Jn.d+n.Jv` and `-n.Jv`; every core coordinate has its own bound. Maximizing the convex affine-plus-absolute-affine expression over all slider vertices covers the full slider box. It adds the conservative remainder `8 alpha^2/2 + 3 r alpha + (2alpha)^2/2`, using the independently checked centre/core norm envelopes and corner norm at most one. No producer finite-row decision is used in this calculation.

All eight parallel reference offsets are reconstructed independently and satisfy their designated branches, with `|tau|<321/1000`. The three axis-face zero-offset identities are inherited from the accepted algebraic proof. These are reference signs; the perturbed physical tangent offset may cross zero. The accepted parallel remainder pays for that perturbation. Therefore the review does not introduce an unstated actual-offset sign premise.

## Source, roster and symbolic identities

All producer files and source dependencies are bound by SHA256. I independently compare the isolated instance with the accepted snapshot: exactly one slider line in `uniform.py` and one padded-slider line in `bridge.py` change. All other files are byte-identical. In the producer's old-roster computation, the shared imported pilot/helper modules come from the isolated instance; their sources and packing/root data are identical to the accepted versions. The old module retains its own old initial-box function. This shared import does not silently substitute the new slider box into the old-roster calculation.

Both complete labelled rosters are saved, not merely their sizes. They agree exactly and contain 25 wall rows, eleven unique-owner rows and sixteen parallel rows: 52 distinct rows in total. The nineteen physical pair rosters and every retained owner/axis/sign also agree. This closes the dynamic-roster loophole in which a dropped unique-owner row could coexist with a printed count of nineteen audited pairs.

**Identity provenance is deliberately distinguished.** The producer freshly ran all 52 symbolic identities and saved their numerator/denominator records, together with the three axis-offset checks. This review binds those records and verifies their complete label correspondence. The reviewer does not rerun SymPy. Independently, reuse of the prior accepted identities is valid because their entire labelled roster, exact row/layout functions, root data and slider-coordinate conventions are unchanged; the two edited endpoint lines do not enter those symbolic affine identities. Their base gaps and slider coefficients vanish identically for all slider values. Their geometric necessity on this wider box is supplied by the new complete option audit above.

The normalized model's file, complete labels, dimensions and kernel hash are checked: 52 necessary geometric rows plus 192 shared McCormick rows, totaling 244 rows in 100 variables. This is model-data binding, not independent arithmetic replay of every coefficient or a dual contraction. The producer's finite necessary model records 596 rows and retains all nineteen pairs with no omitted pair or reference-sign crossing; our separate finite geometric audit validates the pair-option coverage rather than merely trusting that count.

## Controls and remaining obligations

Increasing b's upper endpoint to `1/4` makes the independent root audit detect an extra owner option for pair 5--11. Removing one retained row fails the exact roster comparison. Clean margin checks separately verify all 125 excluded options at each scale, with eight distinct owner/axis/sign records per pair. The executed reviewer checks have no failed run.

The already accepted coordinate-transfer and physical-side lemmas remain dependencies. Future tree stores allowing positive `xi_(2,1)` need the explicit actual-`S<=S*` right-wall cut before invoking `a>=0`; they are not literally included in the terminal box. The global application still retains all seventeen physical squares, with sixteen distinct constrained assignments and one unrestricted physical square. No smaller full-seventeen slider classification is inferred.

What remains is a fresh strict normalized contraction, finite contraction and actual bridge, complete independent certificate replay, and joins from actual tree terminal stores/arcs. The root cuts and common-frame injective capture remain separate obligations. The full analytic gate now passes on the complete proposed box; no box was narrowed and no contact row was dropped to obtain this result.

To replay the independent checks without overwriting accepted outputs, copy this review directory to a fresh sibling at the same depth and run `python3 check.py` followed by `python3 bind.py` in that copy. Both retain the frozen producer and prior independent geometry source as dependencies.
