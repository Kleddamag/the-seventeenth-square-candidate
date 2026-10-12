# Independent G20S terminal assessment

Reviewer `Codex`, producer `Codex`.

**Accepted as an analytic reuse assessment and a collection of conditional exact constant lemmas. No new terminal theorem is established.** The current target is the plan's terminal/HW upper bound `a<=8/25`; the final G20S root instead has `a<=39/125`. The producer retained its superseded 39/125 calculation separately. The independent review performed no solver, model assembly, symbolic identity audit, certificate replay, actual packing search or R17 work.

The target has twenty-nine core position coordinates bounded by `1/200`, sixteen independent angle increments bounded by `1/400`, and sliders

`a in [0,8/25], b in [-1/20,1/5], z in [-1/5,3/40]`.

The common-frame assignment must use sixteen distinct actual physical squares, with the accepted corrected reference, own-reference axes for labels 11/13, and their slider signs. For a seventeen-square application, the remaining physical square is unrestricted in pose but remains physically contained and nonoverlapping. Dummy coordinates in the sixteen-square relaxation impose no condition on that square. A successful terminal would give side equality and zero **exact-root** core, without automatically tightening the three sliders to the previously established smaller full-seventeen family. Such tightening is a separate equality-scope problem.

## Independently checked constants

`check.py` imports no producer module. It binds all frozen source/dependency hashes, parses the rational reference and accepted root enclosure, reconstructs the endpoint formulae, and uses a separate interval implementation on a `10^-90` outward grid. It verifies the complete target roster and these statements:

- All forty-five rational core coordinates bounded by `1/10000` transfer into the exact-root core cube of radius `1/5000`, with additional reference error less than `10^-15`. All three transferred sliders fit the declared padded box, retaining the physical lower bound `a*>=0`. This is conditional on a future finite certificate reaching that raw core cube.
- All eight parallel-pair **reference** offset branches remain valid. Their magnitudes are below `321/1000`; the positive lower bounds of pairs 11--12 and 13--14 exceed `3/500` and `1/200`. The independent calculation uses the accepted exact fraction bounds and the exact affine changes `-a`, `+b`, `-z`; it does not use rounded roster logs.
- The accepted root/ref data give `S*<p2x+1/2<Sref`. Under actual `S<=S*`, the physical right wall therefore implies rational `a>0` and exact-root `a*>=0`. Square 8 gives the finite side floor `S>Sref-1/50` from the proposed input, with margin greater than `149/10000`. No scalar lower-bound assumption is needed.
- The one competing SAT option for pair 5--11, owned by square 5 with reference normal `+x`, is rigorously excluded on the complete proposed entry and slider box. A separately derived necessary corner-gap upper bound is approximately `-0.00907704651879`, strictly below `-9/1000`. For the larger entry `(position1/100, angle1/200)` this same sufficient bound is positive, which proves neither feasibility nor failure of another bound.

For the last check I expanded the selected corner gap directly. The independent angles give linear coefficients `Jn.d+n.Jv` and `-n.Jv`; the centre contribution is bounded separately. The dependence on b is an affine function plus an absolute affine function, hence its maximum on the interval occurs at an endpoint. The remainder `D alpha^2/2 + alpha dr + ||v|| (2alpha)^2/2` follows from the rotation remainder bound. A fixed corner suffices because an actual separating owner axis must separate every corner. This proves exactly one option's exclusion, not the complete 152-option audit.

Four exact controls reject the obsolete terminal a endpoint, use of Sref for the physical a-wall repair, an insufficient raw contraction radius, and the obsolete `313/1000` offset bound. Measured independent computation: 0.010303 CPU seconds; no failed execution.

## Source and analytic reuse obligations

The two slider constants in `uniform.initial_bounds` and `bridge.run` must change together. `rigidity.initial` derives its padded box from the first, and `verify.py` checks the bridge's box against it. The bridge's core/parameter projections, exact-root drift and lower-side implication must be bound to the new finite certificate rather than substituted by this hypothetical constant calculation.

The old symbolic base-gap identities are affine in the sliders with identically zero slope, so their algebra does not depend on the old slider endpoints. Their usefulness as necessary physical inequalities does depend on owner-option coverage. The dynamic `tight_labels()` roster can lose a unique-owner row, and `option_audit` may still report nineteen pairs. Thus an exact comparison to all fifty-two old row labels, including eleven unique-owner pairs and eight parallel pairs, is required. Counts alone cannot discharge it. No new roster comparison or complete option audit has been performed here.

The parallel reference-sign proof concerns tau(w), not the actual perturbed tangent offset. The accepted two-owner lemma bounds the latter by `|tau|+D|m|+dr` and pays the additional terms. The wider interval must still be used when rebuilding every norm bound, product interval, coefficient supremum, McCormick row and all-scale error. Old dual multipliers require residual recomputation on the new model. A new strict normalized contraction ratio below one is essential; successful separate endpoint probes do not imply the combined box contracts.

The final all-scale normalization and side equality retain actual `S<=S*`. Square 8 gives the normalized side coordinate in `[-1,0]`; after zero exact-root core it reaches the exact-root right wall. A nearby rational side cap does not replace the actual-side premise. Neither numerical closeness nor unproved force/contact assumptions are used.

## Explicit physical cut at a tree-terminal join

The planned HW/G20S terminal stores allow a positive upper endpoint for `xi_(2,1)` (r or 0.01). Those stored boxes are **not literally contained** in the terminal's `xi_(2,1)<=0` box. On the actual physical subdomain with `S<=S*`, the right-wall inequality and the verified `S*<p2x+1/2` imply

`xi_(2,1) <= S* - p2x - 1/2 < 0`.

This is a valid separately stated semantic cut before invoking the terminal. Future composition must record the wall and exact-side hypotheses explicitly; it must not silently tighten a stored tree box or claim literal inclusion. Similarly, actual arc endpoints and their compositions, not nominal angle labels alone, must pass the terminal gate tests. Every remaining coordinate/sliding endpoint needs its own valid inclusion.

The root cuts `b<=1/5`, `z>=-1/5` and `a<=39/125` remain input/capture or broad-tree obligations. The wider terminal does not establish them from a position-only window. No future capture-region data has been imported or tested by this review.

## What remains

The missing work is the new complete roster/option/identity audit, a fresh combined-box all-scale contraction, finite contraction into the checked small core, full exact replay and independent composition, then actual joins from the HW and G20S trees. A wider full-seventeen equality-family claim would require additional geometry. This review does not supply those additional certificates or their independent acceptance.

The accepted scope is therefore meaningful but limited: the target passes exact reference-branch, coordinate-transfer and one important option checks, and the existing analytic method has a precise reuse contract. The optimality implication remains conditional on the missing complete certificates and global capture.
