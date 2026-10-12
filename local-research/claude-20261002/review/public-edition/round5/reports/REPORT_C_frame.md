Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line.

REPORT of the reviewer of premise C (frame and case partition), packet frozen-manuscript-20261010_1450, written 10 Oct 2026

## 1. Verdict

All four reviewed premises follow from what their proof files show, taking CHARGE_SEMANTICS and the exact receipts as given; I found no wrong step.
F1 is confirmed as a real gap of the 1450 packet, and it is closable: the proposed closure is correct and I verified the wall-strip inequality independently.
One piece of F1 survives Codex's O1 repair: defining roles 3, 15, 17 by their small slots S_k does not by itself make the C-family exemption X empty in case JG.

All nine proof files named by the four premises match their sha256. So do the files pinned inside FRAME_L9.json, the four frame class files, the KEY_W class and certificate, and the E07A inputs.

## 2. Per premise

### FRAME_ASSIGNMENT: FOLLOWS

**The argument, reconstructed from the class files:**
- **Marker.** marker.json is an orbit restriction (k = 17, bound 17, exempt = the hexagon M in all directions), so some parent lies in one of the eight D4 images of M. Apply the inverse image to the whole packing.
- **Half-marker.** M is invariant under x -> U - x (checked on the six vertices). If the M parent's direction in [0, pi/2) exceeds pi/4, mirror the whole packing once; the direction becomes pi/2 - theta. Since r^2 + 2r - 1 = 309449/250000000000 > 0 for r = 207107/500000, [0, pi/4] lies inside the half-marker gate.
- **One common image for everything: proved.** The three pair statements are universally quantified over all packings in the frame and have mirror_x symmetry, so they hold in the image just chosen. L9 is exactly the mirror of the file's L17 rectangle. No property needs its own image.
- **The counting, in the manuscript's notation.**
  - For pair05_06 and pair11_14: m = parents in the file's marker class (threshold 5/4), t = parents in its low union (slot plus mirror, threshold 7/8), q = parents in both.
  - High-first sum = 17 + m/4 - (t-q)/8 < 137/8 gives t - q >= 2m. The occupied hexagon is the 1114 marker and lies in the 0506 marker box, so m >= 1 and each low union holds at least two parents.
  - Those two low unions are byte-for-byte the classes BONUS_1114 and BONUS_0506 of pair09_17 (polygon and gate compared).
  - M, the two bonus unions and V = L9 ∪ L17 are pairwise disjoint as closed sets, so h >= 1 + 2 + 2 = 5 distinct high parents.
  - 17 + h/4 - N(V)/8 < 145/8 gives N(V) > 2h - 9 >= 1, so N(V) >= 2.
- **Uniqueness and distinctness.**
  - M: squared bounding-box diameter 493/1250 < 1.
  - L9 and L17, clipped to the centre box [1/2, U - 1/2]^2: width 2001/5000, height 11/20, squared diameter 11566501/25000000 < 1.
  - The two rectangles are disjoint and each has capacity one, so with N(V) >= 2 each holds exactly one parent. Both are disjoint from M.
- **Is the "five distinct high parents" argument complete? Yes.** Two remarks that the text could add:
  - q = 0 necessarily, because both targets are disjoint from their marker.
  - h = 5 exactly, because h = 6 would force N(V) >= 4, above the capacity of V.
  - The two mirror pieces of the 1114 bonus touch at (U/2, U/2); the source counts them as one union, which is right.

**Findings:**
- **MINOR.** The manifest pins FRAME_L9.json, which is only a binding and still carries the status string "AUTHOR_BINDING_OF_ACCEPTED_DEPENDENCIES_NEW_REVIEW_PENDING". The argument lives in FRAME_L9.md and join-design-files-20261009-1525/frame-premise-producer/THEOREM.md, pinned only inside that binding. The manuscript's "in the notation of FRAME_L9" refers to m, t, q, which are defined only in THEOREM.md. Fix: pin both files in the premise and define m, t, q, h, N(V) in Section 4.
- **MINOR.** The strict margins are a few integer units: marker 13, pair05_06 31/2, pair11_14 1/2, pair09_17 61/4 (recomputed from the recorded Gamma and budget). pair11_14 rests on half a unit in 1.7e10 and on "saved one-worker Node inputs". The inequality is exact, but the premise stands or falls with the integer exactness of that one receipt, which I did not check.

### WALL_PARTITION: FOLLOWS as stated; F1 confirmed and closable, one piece left

**The statement itself (label 9 in x <= 53/100):**
- **Triggers, read from the pinned class files (all 32 hashes equal the manifest rows and the disk).**
  - Twelve rigid Q files: trigger x <= 53/100, y <= 129/50, closed, every direction.
  - Loose Q_3, Q_4, Q_15, Q_17: trigger through y <= 13/5.
  - PW: trigger y >= 129/50.
  - L_3, L_4, L_15, L_17: low alternative AQ = [-131/250, 53/100] x [24137/10000, 13/5], closed, every direction.
- **The three branches.**
  - y9 <= 129/50: both Q triggers hold, giving sixteen QB targets.
  - 129/50 < y9 <= 13/5: W and the loose-Q trigger hold, giving twelve HULL and four QB.
  - y9 > 13/5: W holds; AQ lies inside L9 and its only possible occupant is the L9 parent, which is above it, so AQ is empty and L forces S_3, S_4, S_15, S_17.
- **Seams.** At y9 = 13/5 the L9 parent is in closed AQ, so L gives nothing and loose Q must be used, exactly as the premise says. x9 = 53/100 belongs to the wall.
- **Profiles recomputed.** For each of Q, W_lower, W_upper in PART3_REQUIRED_CLASS_FRAME.json: seventeen clipped regions with squared diameter below 1 (largest 0.4635, label 3), all 136 pairs strictly separated, and only target 12 meets the marker hexagon, with union squared diameter 9437/31250.

**F1 at the source:**
- **Confirmed.** In the 1450 packet no premise proves that parents 3, 15, 17 exist and are unique before tau_3, tau_17, tau_15 are used. WALL_PARTITION's own statement is about the wall column only.
- **The proposed closure checks out against the files.**
  - AQ is identical in L_L03, L_L04, L_L15, L_L17 and lies inside L9 (53/100 < 4501/5000, 13/5 < 29637/10000).
  - Off-wall the unique L9 parent has x9 > 53/100, so AQ is empty, boundary included.
  - Each L file has M at threshold 4, S and AQ at 0, bound 20, so S_k is occupied.
  - S_k alone has capacity one by diameter: clipped squared diameters 1097067164761/4000000000000 (3), 799624844761/4000000000000 (15), 1059571044761/4000000000000 (17).
- **The wall-strip capacity inequality is right.**
  - With w the width along the wall and H the largest wall distance, two interior-disjoint unit squares would need an axis (a, b) with a*w + b*H - b*(a+b)/2 >= 1. F4's concavity argument for the case where the nearer square does not own the axis is correct.
  - The source proof (standing-contract-20261009-2134/thin-splits/TRIGGER3_CAPACITY.md) already treats both cases, through |h(theta) - h(phi)| <= h(theta - phi) - 1/2. Only the manuscript omitted the second case.
  - The quartic [1-w, 1-2H, 4, -1-2H, 1+w] has all Bernstein coefficients positive on 128 subintervals: least 0.005039 for (529/750, 2821531/2000000), 0.005190 for (3427/5000, 2859531/2000000).
  - A brute-force scan over both orientations independently (quarter-degree grid, all four candidate axes) gives worst slack -0.00369 (k = 3) and -0.00361 (k = 15), attained with the squares parallel.
  - The diameter test fails on these coarse regions (clipped squared diameter 1.327 and 1.334), so the lemma is needed there.

**Findings:**
- **GAP (closable, no computation): what the S_k-only repair leaves.**
  - The triggers T_k in the PS/PT files and the exemption X in the C files ("X_some_loose_label_not_gated_exempt") are written on the coarse regions, not on S_k: region-3 = [129/100, 2993/1500] x [-1/2, 1411/1000], region-15 = [19953/10000, 26807/10000] x [1623/500, 26/5], region-17 = [3775331/1000000, 5199531/1000000] x [24137/10000, 29637/10000].
  - If role k is defined as the S_k occupant (as F1_PROOF.md in review-repair-O and Section 5 of the 15:31 O1 packet do), then "all tau_k gated" does not exclude a second parent in region-k outside S_k turned beyond the gate. That parent would occupy X, and the ten direct C rows would give nothing in case JG.
  - The accepted source split (c-wall-v2-producer/V2_PROOF.md section 2 and its review) is by trigger occupancy ("WC empty and TT2 occupied / TT2 empty", with X inside TT2 ∪ WC). The manuscript's decision list by role angles equals it only if each coarse region has capacity one.
  - To close: state "region-k holds exactly one parent, the S_k occupant" using the wall-strip lemma for 3 and 15 and the diameter 1851391155161/4000000000000 < 1 for 17 (checked; S_17 lies in both the frame L17 and the file's region-17 after clipping). Invoke it explicitly for X-emptiness in JG, and add the lemma to the dependencies of WALL_PARTITION and ROOT_ADMISSION. The O1 manifest adds L_3, L_15, L_17 but not this lemma.
  - The first reviewer's wording (capacity of the Section 6 regions) closes F1 fully; the S_k-diameter version does not.
- **WEAK: the lemma has never been independently accepted at source.** TRIGGER3_CAPACITY.md says "New analytic argument by Codex; independent review OPEN". The later pss-ruling that quotes it names Codex as reviewer. The first reviewer's replication and mine are, as far as the files show, its only outside checks. It should get its own pin and acceptance record, because it is load-bearing for JG and its margin is thin (about 0.0037).
- **MINOR: slab target is not literally inside HULL11.** The manuscript's JPWS uses B_11 of SL_L11_T020_DH.json for label 11; the premise's proof file has HULL_11 in the slab profile. B_11's vertex (4216149/2500000, 10105833/5000000) lies 3.7e-8 outside HULL_11 (rounding on the shared edge). I checked the slab profile with B_11 directly: capacity one and all 136 pairs separated, so nothing breaks, but no step may infer B_11's properties from HULL_11 by inclusion.
- **MINOR: the file's region-17 is the frame's L17 shifted by 469/1000000 in x.** The identification of "role 17" across the two goes through S_17 and both capacities, which hold; the text should say the two rectangles differ.

### C7_C8_TRANSFER: FOLLOWS

- **The E07A file** (inputs/classes.json, eb730b1b...) is a one-sided, symmetry-fixed statement: M = hexagon with gate [-r, r] (every direction) at threshold 4; T = [-1/2, 3501/5000] x [19879/5000, 26/5] with gate ±751411/10000000 at threshold 0; bound 20. Recorded surplus 6 = 20*997821631 - 19956432614.
- **C7.** M occupied forces T occupied, and T equals the C_L07 target exactly (box and gate).
- **C8.** Mirror the whole packing about x = U/2; it is again a packing in the frame and M is still occupied. Apply E07A and mirror back: the occupant lies in [19879/5000, 647/125] x [19879/5000, 26/5], inside the C_L08 target with slack 3/125; the gate is symmetric.
- **F7 confirmed.** The second application is legitimate only because E07A's high class is the mirror-invariant all-direction hexagon. With the half-marker [0, r] the mirrored marker parent would leave the class except at 0 and 45 degrees.
- **Distinctness.** The two targets are separated in x by 8189/2500; both are far from M.
- **Scope.** The manifest rows C_7 and C_8 claim occupancy only, with no literal score bound; that matches what is proved.
- **MINOR.** The manuscript's "E07A pair implication" should read "one-sided statement for label 7". The E07A row's only proof pin is the C7/C8 reviewer's RECEIPT.json; the budget acceptance itself (accepted.json, 43ef993f..., hash verified) is one level further and not pinned in the manifest.

### KEY_W_ELIMINATION: FOLLOWS

- **The KEY_W file** (kw7_cert/classes.json, bc9af7ea...): M = half-marker at threshold 4; E at threshold 0 with three slots:
  - slot 1: all of L9, tan-half in [30651/100000, 44941/100000];
  - slots 2 and 3: the wall column x <= 53/100, tan-half in [0, 613/2000] and [-55059/144941, 0].
  - Bound 20, symmetry fixed; recorded surplus 12.
- **Chain.** The occupied half-marker forces a parent in E. Every E centre lies in L9, so it is the unique L9 parent. Off-wall (x9 > 53/100) only slot 1 is possible. For the canonical theta9 in [0, pi/2) the only quarter-turn lift that can meet [34.08°, 48.40°] is the identity, so t9 >= 30651/100000.
- **F6 confirmed.** 30651/100000 - 61301/200000 = 1/200000 > 0.
- **Exhaustiveness after removal.** The removed predicate is exactly "x9 > 53/100 and 0 <= t9 <= 61301/200000" (EXACT_ENDPOINT_AND_CASES.json, excluded_branches), endpoint included, and it is empty. The other eleven predicates are untouched, so the list stays exhaustive and disjoint, subject to the F1 item above. JPA is correctly kept: slot 1 reaches 44941/100000, above the gate's upper end 591183/1408817.
- **MINOR.** The class comment and the phrase "gated or stands on the wall" overstate slots 2 and 3. On the wall column the directions with tan-half in (613/2000, 30651/100000), width 1/100000, are in no E slot. This is harmless here because the wall case is decided by x9 alone and only the off-wall contrapositive is used; the literal "gate-or-wall union" of the premise is correct.
- **MINOR.** "old T9 gate" (manifest) and "current T9 gate" (text) are the same number, 61301/200000.

## 3. What I verified myself

Exact rationals with python fractions; scripts frame.py, strip.py, profiles.py, show.py in <reviewer scratch>/.
- **Hashes:** every file listed above.
- **Frame geometry:** mirror invariance of the hexagon, identity of the hexagon across marker, 1114 and 0917, identity of the bonus slots, the eighteen strict separations, the diameters 493/1250 and 11566501/25000000, the count algebra, the four surpluses.
- **Wall profiles:** capacity and 136 separations for three profiles plus the slab variant with B_11; the label 12 union diameter.
- **L files:** AQ inside L9; clipped diameters of S_3, S_4, S_15, S_17, of the coarse regions and of WC.
- **Wall-strip lemma:** derivation of the quartic, exact Bernstein positivity, brute-force scan over independent orientations, and a reading of the source proof.
- **KEY_W:** slot geometry, the endpoint gap, the quarter-turn images, the JPB predicate, the legacy C arcs against the gate (613/2000 < 61301/200000; upper gap 974949/14197000000 > 0).
- **E07A:** target equality with C7, mirrored inclusion in C8, the separation.

## 4. What I did not check

- Any charge receipt or row, and the checker's reading of "orbit", "mirror_x" and quarter-turn lifts; I took CHARGE_SEMANTICS and the COUNTED rows as given. The KEY_W acceptance is a provenance audit ("no checker rows executed"), and the amendment review says it did not check the receipts.
- ROOT_ADMISSION: off-wall profile separations, how the JPG roots define their factors for labels 3, 15, 17, root inclusions.
- SELECTOR_LOGIC, the PSS/PSE options, the fallback catalog.
- The 15:31 O1 packet beyond its F1 paragraph and the dependency lists of WALL_PARTITION and ROOT_ADMISSION.
- I did not run the reviewers' own scripts (review.py, check_keyw.py); I recomputed instead.

