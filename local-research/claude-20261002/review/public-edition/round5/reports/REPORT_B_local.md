Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line.

REPORT of the reviewer of premise B (local side), 10 Oct 2026.

R = <repository root>

## 1. Verdict

No wrong step found in any of the four premises. The rigidity theorem G20S_PHYSICAL is a real proof (two certificate trees plus a two-stage contraction), and the two analytic lemmas it stands on I re-derived by hand and found correct.
All four premises FOLLOW; three carry WEAK items of bookkeeping (dependencies not listed, one pinned file changed after the freeze, one corollary in an unpinned notes file). None is a mathematical gap.
Not replayed by me: any certificate arithmetic (tree steps, LP dual bounds, symbolic contact identities). These rest on the named reviews.

## 2. Per premise

### G20S_PHYSICAL: FOLLOWS (with two WEAK items)

Hashes: all three proof files match the manifest.

**The 45 coordinates and the three left out.** Sixteen squares have 48 coordinates: 32 positions and 16 angles. The three left out are the sliders: index 2 (a = -xi_{2,1}, square 2 along x), index 21 (b = -xi_{11,2}, square 11 along its own v axis) and index 25 (z = xi_{13,2}, square 13 along its v axis). The core is 29 positions plus 16 radian angles. Indices 6, 7, 37 (square 4) are storage placeholders with zero coefficient in every row. Source: `.../g20s-terminal-audit/sixteen-square-corollary/producer/MATHEMATICAL_INTERFACE.json`, "zero_based_core_indices". Square 8 (indices 14, 15, 41) is entirely core, so "role 8 at (L-1/2, L-1/2), axis (1,0)" does follow from core zero. `research/uniform-capture-20261007/bridge.py`, `layout`, has points[7] = (side-half, side-half), and `root_geometry.py` gives it axis (1,0).

**How rigidity is proved on a window that large: both a tree and a contraction, in five links.**
1. Tree G20S (679 nodes): the window G20S implies the tube T1 (the HW window with xi_{2,1} up to 1/100).
2. Tree HW (579 nodes): HW implies T2 (core 1/250, angles 1/500 rad, wide sliders). The hypothesis xi_{2,1} <= 0 of the window carries a configuration from T1 into HW.
3. T2 cut by xi_{2,1} <= 0 lies in the finite entry (core 1/200, angles 1/400, a in [0, 8/25], b in [-1/20, 1/5], z in [-1/5, 3/40]).
4. Finite contraction: 17 complete LP-duality rounds on necessary rows, ending at raw core below 1/10000.
5. Normalized contraction: divide the exact-root core by R = max|h_j| with sliders unscaled; 52 contact and wall rows plus 192 McCormick rows hold for every 0 < R <= 1/5000; the certified bound max|h/R| <= 0.796 < 1 contradicts the definition of R, so R = 0.

Step 3 of the chain exists twice with different numbers: the lead's instance `terminal/instances/box-wide` (ratio 0.859, in `THEOREM_G20S.md`) and Codex's sixteen-square corollary (ratio 0.796, with stop cuts). The two agree in conclusion.

**The passage from the rational chart to the exact root is proved, with error terms.**
- Centres differ by less than 1e-15 and axes by less than 1e-50.
- Raw 1/200 becomes exact-root 501/100000; raw below 1/10000 becomes below 1/10000 + 1e-15, under 1/5000.
- Sliders are padded by 1e-12, except the lower end a* >= 0, which is not padded. It is derived from square 2's right wall and S <= S*, and needs S* < p_2x + 1/2.
- That lower end is load-bearing: pair (2,6) has tangential offset tau = -a, and the parallel row uses kappa = (1 - branch*tau)/2 with branch = -1, which is valid only for a* >= 0. So "actual S <= S*, not the rational cap" is used correctly.
- The conclusion is stated for the exact-root chart only ("Zero rational-reference core is not asserted").

**Range of S.** The trees hold for every S <= Sref (SPEC section 11: same corner, same poses). The terminal theorem assumes S <= S* and concludes S = S*. The manuscript applies it at S = L only.

**Sliders and label 4.** Sliders stay free; nothing is claimed about them. No row, pair or wall involves label 4; all 19 pairs have both ends in I. The broad-tree review states that on a full packing the seventeenth square "remains present and unrestricted".

**The analytic lemmas, re-derived by me.**
- Parallel faces (`research/joint-capture-20261007/README.md`, "The union of the two possible owner axes implies"): with n(theta_i), n(theta_j) = cos q * n_m -/+ sin q * t_m and support 1/2 + (cos 2q + |sin 2q|)/2, the union gives X >= cos q + |sin q| - |Y||tan q|. The two rows with k = (1-|tau|)/2 and the remainder E follow. The rows are the weaker, union form, not a chosen branch.
- Unique owner: E1 = D*wo^2/2 + wo*dr + V*eta^2/2 is right, grouping (R(w)n)·d0 and (R(w)n - n)·delta_d.
- Division by R in `uniform-capture-20261007/PROOF.md` section 5 is right term by term.
- Stop cuts (`finite-entry-stop-pruning/root-producer/PROOF.md`): N + eps|X| >= 1 gives b >= -(17/10)eps and b + z <= T/3 + (14/100)eps. The form is correct.

Findings:
- **WEAK (dependency).** The manifest gives depends_on = [ALGEBRAIC_ENDPOINT] only. The premise also rests on the soundness of the tree checkers for the G20S and HW certificates. These are wx-cert-2 trees accepted by the 2.6 checkers and re-accepted under 3.0 (`acceptance/ACCEPT_G20S_v30.log` and `ACCEPT_HW_v30.log`, RESULT: ACCEPTED). To close: add LOCAL_CHECKER_SOUNDNESS, or REVIEW_26, and name the two v30 logs.
- **WEAK (who reviewed the hand lemmas).** `THEOREM_G20S.md`: "resting on Codex's analytic lemmas of the terminal proof, which are hand proofs and are taken as they stand". The joint-capture README: "not machine-formalized or independently reviewed". The later full-gate review re-derives the option exclusion and the remainder. I confirm the two lemmas above. To close: pin one reviewed text of the two envelope lemmas in the premise's proof list.
- **MINOR.** The two cited reviews (8 Oct 22:04 and 22:17) predate the PROVED status of `THEOREM_G20S.md` (23:59) and use Codex's step 3, not the lead's box-wide instance. The premise cites both routes without saying they are alternatives.

### WALL_CONTRADICTION: FOLLOWS

Hashes: all four match.

Chain as proved:
1. K is the smaller packing translated by d(1,1), d = (L-S0)/2 > 0, so K lies in [d, L-d]^2.
2. A labelling of K satisfies the JG root.
3. T_JG (a TUBE theorem with a certificate of 113 nodes and one terminal leaf) puts the sixteen squares into G20S.
4. G20S_PHYSICAL at actual side L gives core zero, so role 8 has its corner at (L, L), outside [d, L-d]^2.

Checks:
- JG root into G20S, all sixteen squares and all coordinates: the root is not inside the window by inclusion. It exceeds it in xi_{3,1}, xi_{3,2}, xi_{9,2}, xi_{17,1}, xi_{17,2} and in the arcs of the rigid labels (0.15 rad against 0.10). The tree closes those exits as infeasible. I checked exactly that the certificate's tube equals the G20S window on all sixteen labels (boxes and alpha = 1/10).
- The tube bounds the angle, not its sine: the terminal test needs |sin| <= 1/10 - 1/6000, and the cut 40/401 passes with slack 8.27e-5.
- Frames agree: T_JG and G20S both use the container corner at the origin; K lies in [0, L]^2 and L <= Sref.
- Inset argument: correct, and it uses the wall contact, not "S = S*" (which would be tautological at S = L). `ENDPOINT_CASE_G_LEMMA.md` says so itself.

Finding:
- **WEAK (dependency by name).** depends_on lists "LOCAL_JG", which is not among the fourteen global premises (it is a root obligation). The record RECORD_EJG_v2.md states that "the composition of JOIN_ROOTS.md section 3 is not proved" there; the composition is `ENDPOINT_CASE_G_LEMMA.md`. Its acceptance line reads "current note is an explicit application": the note itself has no independent review of its own. It is short and I find it correct.

### LOCAL_CERTIFICATE_IMPORT: FOLLOWS (one packet defect)

Hashes: `ACCEPTED_REGIONS.json` and `SIDE_CAP_TRANSFER.json` match. **`third-order-20261010/local-region-audits/ACCEPTED_UPDATES.json` differs**: pinned 1196787f..., on disk 9ee54fbf..., modified 15:02, after the freeze of 14:47. A JPW13_v2x entry (COUNTED, EMPTY) was added. The pinned bytes survive as `local-region-audits/JPW13_v2x/PRE_IMPORT_ACCEPTED_UPDATES.json` (hash 1196787f..., checked).

The monotonicity argument is written and correct. It is SPEC 3.0 section 11, first paragraph, and the corollary in `SPEC_v3.0_NOTES.md` (06:22): a configuration feasible for side S <= Sref is feasible for Sref because (F1) only weakens, (F2) does not mention S, and neither root box, arcs nor tube mention S.

Which translation: none at this step. Both containers share the corner at the origin, so [0, L]^2 lies in [0, Sref]^2 and the pose boxes survive unchanged. The only translation is the endpoint normalization by (L-S0)/2, done earlier, and the regions are stated in that endpoint frame.

I checked all nine root files (JQ_v1, JG_v2, JPG17m/17p/3m/3p/15p/15m v5, JPW13_v2x):
- Frame "ENDPOINT FRAME", S fixed at [Sref, Sref], 17 labels.
- No lower box end at 0. Left and bottom wall ends are at -1/1000000, so the flush position xi = -eps = -5.17e-18 is inside.
- Upper ends at 0 only for the right and top wall coordinates of labels 2, 6, 8, 17 (x) and 7, 8, 15 (y). That loses nothing: a square in [0, L]^2 has centre <= L - 1/2 < p, because the upper end of the S* enclosure is below Sref - eps (checked exactly).

Findings:
- **PACKET DEFECT.** As above. To close: re-pin, or point the manifest at the pre-import copy.
- **WEAK (scope of the import audit).** `ACCEPTED_REGIONS.json`, verification_scope: "No fresh polynomial-term or whole-tree arithmetic replay". The import checks hashes, headers, root nodes, saved PASS reports and record reviews. The premise claims no more, but "complete frozen-checker acceptance" means the lead's acceptance runs, not a rerun.
- **NOTE.** JPG17m_v2 and JPG3p_v2 are COUNTED but carry "Old PB_11 target only; does not cover selected v5 enlarged label-11 factor". They close no selected root and must not be cited for one.
- **NOTE.** Eight selected roots are closed in the pinned files (JQ, JG, six v5 regions). JPW13 is closed only in the post-freeze file. Two of the eleven (JPA, JPWS) have no entry.

### LOCAL_CHECKER_SOUNDNESS: FOLLOWS (one WEAK item)

Hashes: all seven match.

I read SPEC 3.0 sections 0 to 9 and 11 as mathematics. A tree that passes all rules proves that every configuration of F(root) lies in the tube, and that F(root) is empty if no leaf is terminal. What I checked:

- **Non-overlap constraints, valid for all packings in the cell.**
  - SAT lemma (4.5), by the Minkowski difference: correct.
  - Corner facts of an option are facts only if the node assumes the option or the seven others are excluded on the round's start store.
  - The exclusion test (4.7) is strict (U < 1/2 + h_lo). I checked the quadrant test for h_lo, including the boundary cases of points on the axes.
  - Option split: every unlisted option must be excluded on the parent's final store.
  - Parallel classes (4.6): I verified the identity be - al = si*Y/(1+co) and all eight cases of Lemma P.
  - Indicators (4.10): the lifted point picks the smallest index of an option that holds; guard rule (T3); TERM LEMMA correct. So no separating option is ever chosen without proof.
- **Exactness of the positivity certificate.** It is not a Gram-matrix sum of squares. Each step is the exact polynomial identity g = Rem + sum of lambda_k times products of at most three facts, with lambda_k >= 0 (either sign only with the identically-zero `circ`). Rem is bounded below monomial by monomial with exact rational interval products over the store bounds. Squares `sq:NAME` enter only as facts. A `0` step needs L >= value > 0 and sense "lo". The CLAIM g(x) >= L is proved correctly for the raw and the centred rule.
- **Cover rule.** Children are closed cells sharing the face ([lo, m] and [m, hi]; arc halves sharing M; sign split Y >= 0 and Y <= 0). Each child must contain the parent's final store in every other interval, arc and the side. A child inherits only assumptions, no cuts. Shared faces are covered twice, never missed.
- **Store updates.** The arc and relative-arc endpoint rules are right, including the case omega >= pi/2 in 4.3.
- **Root and terminal tests** (section 8): correct. sin Ab >= alpha gives angle >= alpha; |sin| <= alpha - alpha^3/6 gives |angle| <= alpha.
- **Modes.** REVIEW_30_PY: `--keep-going` keeps FAIL; `--node` never prints PASS; the frozen file cf8db52b... has neither `--allow-extra-keys` nor the partial mode ("Freeze cf8db52b... as it stands", part P9). The JG acceptance ran with default options.

Findings:
- **WEAK (unpinned corollary).** The premise says the rules "imply the whole-root EMPTY/TUBE theorem". The THEOREM of section 7 is about the header window. The root-region TUBE corollary is worded in REVIEW_30_ACCEPT.md R.4 (pinned). The EMPTINESS corollary exists only in `SPEC_v3.0_NOTES.md` (note of 18:38), which is not in the proof list. It also needs "number of terminal leaves = 0" and "root node = region file", which the acceptance post-check enforces, not the checkers. Both corollaries are correct (induction with closures (a) and (c) only). To close: pin the notes file and name the post-check in the premise.
- **NOTE (independence, as the reviews state it).** REVIEW_30_ACCEPT: "The 3.0 part of C1 and the certificate come from the same helper ... so the independence that counts for this certificate is that of C2". The two code reviews and the acceptance review are by one reviewer; the text audit is by another. Interpreters are taken as given.
- **NOTE.** REVIEW_30 found one unsound literal reading in the audited candidate (a `0` step with sense "hi", MUST-1). The frozen text has the fix (section 5, "allowed with the sense 'lo' only"; section 10 line 792).

## 3. What I verified myself

- sha256 of all proof files of the four premises, plus ALGEBRAIC_ENDPOINT and ENDPOINT: one mismatch, reported above.
- Exact recomputation (python fractions) from `upper-packing-certificate.json` (24e296f5...): SPEC section 1 reference centres and axes, including the corrected p_13 with T0, equal the 16 entries of the sixteen-square MATHEMATICAL_INTERFACE.json, centre and both axes, for all labels. So the tree chart and the terminal theorem's chart are the same.
- Exact: JG tube equals the G20S window on 16 labels; 40/401 <= 1/10 - 1/6000; (1 + 4147/10000)^2 >= 2; T2 cut by xi_{2,1} <= 0 lies in the finite entry; the S* enclosure (width 2.1e-54) has upper end below Sref - 2 eps; Sref - S* = 4.8366e-17.
- By hand: the parallel-face union inequality and its remainder, the unique-owner remainder, the division by R, the code coefficients of the parallel row in `root_geometry.py` (tau/2 -/+ sign*kappa and the slider product shares), the form of the stop cuts, the identities and the eight cases of SPEC Lemma P, the 4.7 quadrant test, the TERM LEMMA and CLAIM, the covering proof, and both root-region corollaries.
- Frame and wall ends of the nine root region files.

## 4. What I did not check

- Any arithmetic replay: the G20S, HW, JG and other trees; the 17 + 11 rounds of LP dual bounds (1,564 and 552 objective identities); the 52 symbolic contact identities; the 152-option gate intervals; the root enclosure.
- The checker source code (`wxcheck_v30.py`, `wxcheck2_v30.js`): read only through their reviews. SPEC section 10 (format rules) was skimmed, not read.
- The seven Ps and wsup concavity bounds in SPEC 4.6 and 4.8: read, not re-derived line by line.
- The lead's `terminal/instances/box-wide` files and REVIEW_26 parts R5 and R6; the HW import review; the 2.6 errata.
- The region records other than JG, and whether each region file equals the capture classes (that is ROOT_ADMISSION).
- The reviews of ENDPOINT (REVIEW.md and ACCEPTED_INTERFACE.json of the endpoint normalization): hashes only; I read the producer theorem and the case-G lemma.

