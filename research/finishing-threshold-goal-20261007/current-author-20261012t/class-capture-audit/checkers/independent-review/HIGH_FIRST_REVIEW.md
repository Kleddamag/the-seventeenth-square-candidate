# Independently reviewed high-first consequence

Reviewer: `Codex`. This is a consequence of the **frozen actual cell rule**, not merely of the published minimum-threshold `tau` statement. It is conditional on a complete authentic exact row verification with the stable-input and aggregation obligations in `REVIEW.md`. No capture certificate is verified here.

For a pose p define psi(p) as follows:

1. If some containing class has threshold greater than 1, take the maximum such threshold.
2. Otherwise, if some containing class has threshold below 1, take the minimum such threshold.
3. Otherwise take 1.

All memberships include the prescribed closed centre polygons, closed angle gates and all specified symmetry images. Counting a class counts physical parents in its union, once per parent, not the number of slot images containing that parent.

Let Q be a checked cell, I its closed parent-angle interval and R(Q,I) its implemented level. The source sorts high classes decreasingly and low classes increasingly, with high classes first. If a high class contains p in closure(Q) times I, it meets that product and the maximum meeting-high threshold is at least psi(p). If a high class merely meets the product while no high class contains p, its threshold exceeds 1 and again bounds psi(p). When there is no meeting high, each accepted low class contains the entire product in one slot image, and hence contains p. The minimum over this possibly smaller collection of low classes is at least the minimum over all low classes containing p. If no low is accepted, R=1 still bounds psi(p). Thus R(Q,I) >= psi(p) in every case, including closed boundaries and overlapping classes.

The limiting closed-core argument in `REVIEW.md` now yields one core per original physical parent with charge at least Gamma*psi(p). Symmetry-folded cores must first be unfolded into those distinct original parents. The common feature budget M gives

    sum psi(p) <= M/Gamma < beta.

This proof does not require high and low class domains to be disjoint. It is strictly stronger than the published tau assertion in general: at a high/low overlap tau takes the low threshold but psi takes the high one. Consequently a receipt whose provenance establishes only the advertised tau theorem cannot be substituted without binding this source-level strengthening.

## Count-two instance

Assume exactly seventeen parents, and exactly two nontrivial threshold classes: M with threshold 5/4 and T with threshold 7/8. Other classes of threshold exactly 1 are harmless. Put m=N(M), t=N(T), and i=N(M intersect T), all in the same declared frame, including gates if present. Direct inspection of the four membership states gives

    sum psi = 17 + (2m - t + i)/8.

The strict bound beta=137/8 therefore implies 2m-t+i<1. The numerator is an integer, hence

    t >= 2m + i.

If m>=1 and an independent geometric argument gives t<=2, then m=1, t=2 and i=0. In particular geometric disjointness of M and T is unnecessary for this conclusion: occupation of their overlap is excluded by the certified inequality and capacity premise. No claim about disjointness between different target classes follows. A common-frame assignment still requires its own cross-target distinctness/matching argument. The cap t<=2 must be proved for the full target union, with closed boundaries; it is not an automatic feature of a class file.

## Singleton instance

With M threshold 3/2, T threshold 1/2, exactly seventeen parents and beta=35/2, one similarly has

    sum psi = 17 + (m - t + i)/2,
    t >= m + i.

Thus m>=1 and independent t<=1 force m=t=1 and i=0. Again this uses the high-first code semantics, not only the minimum-threshold tau promise.

The tiny independent check `check_high_first.py` verifies all abstract cell/membership states for several high/low thresholds and all 1,140 possible four-category occupancy counts summing to seventeen, for both count formulas. These finite controls supplement the general proof above; they do not replace it or validate any real certificate.
