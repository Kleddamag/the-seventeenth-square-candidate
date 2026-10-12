Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line. This report reviewed the earlier executions of the capture computation, named here by neutral designations (table EARLIER_EXECUTIONS.tsv); the audit of the execution carried in this edition and the complete row comparison with the earlier ones are separate evidence.

HOLDS WITH CONDITIONS (C1 all six base rows are taken from their receipts: I checked statement, side, frame, coverage, budget and bindings, not the row arithmetic or the checker sources; C2 two margins are exact but thin: FRAME_1114 is strict by 1/2 unit, the wall-strip lemma by about 0.005 in H; C3 the proof records pinned for FRAME_ASSIGNMENT still name the first-run executions, the second-run receipts are bound only through the manifest rows; C4 one sentence of the proof text is literally false before clipping). No gap or wrong step found in the mathematics reviewed.

FINDINGS, most serious first

F1 (condition, thin margins).
- FRAME_1114: 137*998806500 - 8*17104561312 = 4, i.e. surplus 1/2 unit. I recomputed the budget 17104561312 from the certificate features (sum of weight * floor(coefficient mass / threshold), mask features counted once); it equals the declared value.
- Wall-strip lemma: numerically the smallest H at which two squares fit is 1.4159781 (region 3, lemma H = 1.4107655) and 1.4345837 (region 15, lemma H = 1.4297655).
- JUDGEMENT: both are exact and sufficient; neither tolerates any change of class bytes or region dimensions.

F2 (condition, record keeping).
- FRAME_L9.json (15975a65) has status "AUTHOR_BINDING_OF_ACCEPTED_DEPENDENCIES_NEW_REVIEW_PENDING" and pins the first-run receipt keys (first execution of FRAME_0506 with the plain Node checker; first execution of FRAME_1114 with the plain Node checker; first execution of FRAME_0917 with the plain Node checker).
- FRAME_L9.md and frame-premise-producer/THEOREM.md say the "original accepted charge executions ... remain the dependencies".
- The second-run receipts are bound only by manifest row -> receipt-audits/FRAME{0506,1114,0917}_wb/SAVED_PROVENANCE.json (by sha256) and RECEIPT_ROSTER.tsv rows 4, 6, 8. The H6_PREMISES rows for the three pair rows list no receipt file directly (FRAME_MARKER does).
- Those three audits name older selection manifests (b55c0d3f, f6d31ce4, b55c0d3f); only frame-direct-import/FINAL_BINDING_CHECK.json names the final 49a24436.
- JUDGEMENT: not a mathematical defect; the theorem needs only the four row statements.

F3 (wording, PROOF_TEXT line 94). "Each S_k lies in its whole coarse region" is false for the literal S17 = [19629/5000, 26/5] x [24137/10000, 7159/2500] against coarse17, whose x upper end is 5199531/1000000 < 26/5. It is true after clipping to [1000469/2000000, 8351531/2000000]^2, which is what the argument uses.

F4 (observation, reduces dependence on CHARGE_SEMANTICS). In all six base rows the high and low classes are disjoint as closed centre sets:
- BOX vs W0 ∪ E0: gap 0.737.
- HEX vs IW ∪ IE: gap 0.01344.
- The 0917 high sets vs L9 ∪ L17: gap at least 0.418.
- E07A: HEX (x >= 537/250) vs T7 (x <= 3501/5000).
- KEY_W: HEX vs L9 (x <= 4501/5000).
So the printed receipt score (least containing threshold) equals the high-first score psi on every pose. These rows do not need the high-first strengthening.

F5 (minor). On the wall column KEY_W covers no direction with tan-half in (613/2000, 30651/100000). The text says so and uses only the off-wall slot. JUDGEMENT: harmless.

(1) TABLE

id | verdict | relied on
FRAME_ASSIGNMENT | HOLDS (given the four rows) | frame_geom.py on the literal class files; count algebra below
C7_C8_TRANSFER | HOLDS (given E07A) | exact fractions on E07A classes.json, C_L07.json, C_L08.json
KEY_W_ELIMINATION | HOLDS (given KEY_W and FRAME_ASSIGNMENT) | kw7_cert/classes.json slots; EXACT_ENDPOINT_AND_CASES.json branches
COARSE_LOOSE_CAPACITY | HOLDS | own derivation; capacity.py (Sturm and Bernstein, exact); strip_search.py (direct search)
FRAME_MARKER | CONDITION C1 | first execution of FRAME_MARKER: PASS, 9000/9000, side C, 17*998328901 - 16971591304 = 13; class literal equals marker.json literal
FRAME_0506 | CONDITION C1 | second execution of FRAME_0506: PASS, 9000/9000, surplus 31/2
FRAME_1114 | CONDITION C1, C2 | second execution of FRAME_1114: PASS, 9000/9000, surplus 1/2
FRAME_0917 | CONDITION C1 | second execution of FRAME_0917: PASS, 9000/9000, surplus 61/4
E07A | CONDITION C1 | first execution of E07A with the repaired Node checker: PASS, 18000/18000, surplus 6
C_7 | HOLDS as occupancy only (given E07A, marker occupied) | T7 literal equals the C_L07 target (polygon and arc)
C_8 | HOLDS as occupancy only | mirror of T7 = [19879/5000, 647/125] x [19879/5000, 26/5], inside the C_L08 target, slack 3/125
KEY_W | CONDITION C1 | first execution of KEY_W: PASS, 18000/18000, 20*999695307 - 19993906128 = 12; classes and certificate byte-equal to the kw7_cert pins
CHARGE_SEMANTICS | NOT READ beyond CLASS_FORMAT.md and PROOF_TEXT section 3 | see F4

(2) HAND-OVERS RESTATED

Rows. Each is for every family of closed unit squares with pairwise disjoint interiors in the square of side C = 4675531/1000000 concentric with F_U (centre (1169/500, 1169/500)); smaller sides follow by inclusion. Every slot arc in the four frame files is [-rho, rho], rho = 207107/500000, and rho^2 + 2 rho - 1 = 309449/250000000000 > 0, so membership is by centre only.
- FRAME_MARKER: symmetry orbit (eight D4 images), one class, threshold 0 on HEX, bound 17. HEX has vertices (537/250, y0), (316/125, y0), (316/125, y0+87/250), (297/125, y0+1/2), (23/10, y0+1/2), (537/250, y0+87/250). For 17 squares, 17 - N(E) < 17, so N(E) >= 1.
- FRAME_0506: mirror_x. M = BOX [537/250, 316/125] x [y0, y0+1/2] at 5/4; T = W0 = [-1/2, 1411/1000] x [129/100, 2993/1500] with its mirror E0 at 7/8; sum < 137/8.
- FRAME_1114: mirror_x. M = HEX at 5/4; T = pentagon IW with its mirror IE at 7/8; sum < 137/8.
- FRAME_0917: mirror_x. HEX, BONUS_1114 (= IW, IE) and BONUS_0506 (= W0, E0) at 5/4; T = L17 = [18879/5000, 26/5] x [24137/10000, 29637/10000] with its mirror L9 = [-131/250, 4501/5000] x same y at 7/8; sum < 145/8.

Derivation of FRAME_ASSIGNMENT (my own, then compared with THEOREM.md: identical).
- Some parent has its centre in g(HEX). Replace the packing by g^-1 of it; the concentric container is D4-invariant. HEX is invariant under x -> U - x (checked on the vertices), bounding-box diameter squared 493/1250 < 1, so it has exactly one occupant.
- If that occupant's side representative in [0, pi/2) exceeds pi/4, mirror the whole packing once. It then lies in the half-marker HEX x [0, rho].
- The three pair rows are universally quantified over packings, so they apply to this one image. No row needs its own image.
- 0506: HEX is inside BOX, so m >= 1; 17 + m/4 - t/8 < 137/8 gives t >= 2m >= 2, with q = 0. 1114: likewise t' >= 2.
- 0917: HEX, IW ∪ IE and W0 ∪ E0 are pairwise disjoint (gaps 0.0134, 0.911, 0.019), so h >= 5. V = L9 ∪ L17 is disjoint from all high sets, so 17 + h/4 - N(V)/8 < 145/8 gives N(V) >= 2h - 8 >= 2.
- Clipped to the physical centre box, L9 and L17 each have diameter squared 1849889604761/4000000000000 < 1 and are 2.8756 apart. Hence N(L9) = N(L17) = 1, h = 5, N(IW ∪ IE) = N(W0 ∪ E0) = 2.
- Attacks. Two labels on one square: no, HEX, L9 and L17 are pairwise disjoint closed sets. A label without occupant: no. An image chosen twice: no. A reflection relation between the L9 and L17 occupants: none is asserted, and none is used. Every one of the 173 other class files with a bound in THEOREM_MANIFEST.json has symmetry "fixed"; 160 of them have the high slot HEX x [0, rho] exactly; the twelve label-12 files use cut arcs; E07A uses [-rho, rho]. The only later whole-packing reflection is the E07A argument.

C7_C8_TRANSFER.
- E07A: symmetry fixed. M = HEX x all directions at 4; T7 = [-1/2, 3501/5000] x [19879/5000, 26/5] x tan-half [-751411/10^7, 751411/10^7] at 0; sum < 20. With N(M) = 1: 17 + 3 - N(T7) < 20, so N(T7) >= 1.
- C_7: T7 is literally the C_L07 target. This is stronger than the C file's "T or X".
- C_8: the mirrored packing is a packing in the same container with HEX occupied, in every direction. E07A applied to it and mirrored back gives an occupant of [19879/5000, 647/125] x [19879/5000, 26/5] with the same symmetric arc, inside the C_L08 target.
- The two targets are 8189/2500 apart in x, so the parents are distinct.
- The hypothesis that transfers is "all-direction hexagon occupied", not the half-marker. No budget for C_L07 or C_L08 is claimed.

KEY_W_ELIMINATION.
- KEY_W: symmetry fixed. M = HEX x [0, rho] at 4. E at 0 with slot 1 = L9 x [30651/100000, 44941/100000], slots 2 and 3 = [-131/250, 53/100] x [24137/10000, 29637/10000] x [0, 613/2000] and x [-55059/144941, 0].
- With the half-marker occupied, N(E) >= 1. Every E centre lies in L9, so the E parent is the unique L9 parent.
- If x9 > 53/100, only slot 1 is possible. For theta9 in [0, pi/2) the other lifts have tan-half < 0 or >= 1, so 30651/100000 <= t9 <= 44941/100000.
- Removed: "x9 > 53/100 and 0 <= t9 <= 61301/200000" (gap 1/200000) and "x9 > 53/100 and 44941/100000 < t9 < 1".
- The off-wall atoms [0, 61301/200000], (61301/200000, 591183/1408817), [591183/1408817, 44941/100000], (44941/100000, 1) are exhaustive and disjoint.
- The hypothesis holds on every branch; the conclusion is used only off-wall.

COARSE_LOOSE_CAPACITY.
- Core: a closed unit square contains the open disk of radius 1/2 about its centre in its interior, so two interior-disjoint squares have centre distance >= 1. A closed centre set of diameter strictly below 1 holds at most one centre; diameter exactly 1 can hold two.
- Region 17 clipped: 1851391155161/4000000000000 < 1.
- Regions 3 and 15 have clipped diameter squared about 1.33, so they need the wall-strip argument. I re-derived it: the separating axis is a side normal n of one square A, with absolute components (a, b) and d = (a+b)/2.
  - A nearer the wall: a w + b(H - d) >= 1.
  - B nearer: a w + b H >= 1/2 + f(phi), f = h_B(n) + b h_B(e_y); f is concave between the breakpoints 0, alpha, pi/2, with values d + b/2 and 1/2 + b d; the difference is (1-b)(a+b-1)/2 >= 0. Same inequality.
  - Mixed signs of n replace alpha by pi/2 - alpha, and f(phi; -alpha) = f(-phi; alpha).
- With a = (1-u^2)/(1+u^2), b = 2u/(1+u^2), failure of the inequality is P(u) = (1-w) + (1-2H)u + 4u^2 - (1+2H)u^3 + (1+w)u^4 > 0 on [0, 1]. P has no root in (0, 1] and P(0), P(1) > 0 for (529/750, 2821531/2000000) and (3427/5000, 2859531/2000000).
- Hypotheses needed: containment in one half-plane, interior-disjointness, |dx| <= w, wall distance <= H. Closed regions, strict conclusion, independent orientations, any side <= C.
- Uses checked against these hypotheses:
  - Every T_k, TT and X slot on regions 3, 15, 17 in join_design/classes*/ is exactly the lemma's rectangle.
  - Every S_k is inside its region after clipping; clipped frame L17 is inside clipped coarse17.
  - A gated occupant (|tau_k| < 1/20) is in no X slot: its other lifts have |tan-half| >= 19/21 > rho.
  - The X slots on region 9 end at 613/2000 < 61301/200000 and start at 4197/10000 > 591183/1408817, and the AQ slot needs x <= 53/100.
  - The off-wall use needs AQ empty, which follows from L9 uniqueness since AQ is inside L9.

(3) SCRIPTS (<reviewer scratch>/)

- receipt_meta.py: for the six receipt folders checks side L/A = C, frame, hash binding of classes and certificate, status, slices partitioning [0, N), every row passed, per-row class minima against threshold * Gamma, Python and Node rows equal, strict budget. Result: all six OK; the Node checker hash in all six is 7f6b2347 (verify_classes_wb.js). cmp: the three pair classes.json are byte-equal to the snapshot pins.
- receipt_neg.py, on scratch copies of the 0506 folder: untouched copy passes; rejected: one row set to failed, one row removed, class threshold edited, budget +16, side changed, a class row minimum lowered below 5/4 Gamma.
- frame_geom.py: results as in (2). Built-in controls: HEX against BOX (overlapping) and IW against IE (touching at (1169/500, 1169/500)) are reported not separated.
- budget.py, budget2.py: budgets recomputed for all six certificates and equal to the declared values; winning masks pairwise intersecting in all six. Control: one weight +5 in the 1114 certificate gives a mismatch and loses strictness.
- capacity.py: Sturm count 0 for both quartics; least Bernstein coefficients over 128 cells are 634043429/125829120000 and 43535731167/8388608000000, equal to the text. Controls, all rejected: H + 1/100, w + 1/100 (region 3), H + 1/100 (region 15), H = 3/2.
- strip_search.py: direct search over both angles and offset with the four side normals, no use of the reduction; no counterexample, minima as in F1, attained with both squares parallel near 45 degrees. Controls: w = 1 gives 0.5, w = 0 gives 1.5.
- region_scan.py: slot scan of join_design/classes*/, results in (2).
- Six SAVED_PROVENANCE audits (three FRAME pair rows, FRAME_MARKER_CLASS, L07_onesided_wb, KEY_W): their receipt, class and certificate hashes equal the files in the folders of record.

(4) SHA256, first 16 hex

Packet: PACKET.json 99d813ec5d1ffd1a; PROOF_TEXT.md b42fa1670b11643a; H6_HANDOFF.md d229a1629e5596e7; H6_PREMISES.json 6741793e2af90717; THEOREM_MANIFEST.json 49a2443699a03620; RECEIPT_ROSTER.tsv b8dbc710126b066e; MANIFEST_TABLES.md f5b95301204998f8; EXACT_ENDPOINT_AND_CASES.json a08363c6a5f4ebb2.
Classes: marker.json 520ce3cea70663d9; pair05_06.json 0dc3b61bfe065089; pair11_14.json 5df8270c46e8d059; pair09_17.json 5cc1503d61201b98; FRAME_MARKER_CLASS.json aa8b1410906ddac7; E07A classes.json eb730b1bbf04e8dd; C_L07.json 60341809dba3593a; C_L08.json bb345831da943357; kw7_cert/classes.json bc9af7eacc5de952; L_L03 654dcdb2bd7dc627; L_L04 036302c5ecfec8c4; L_L15 cfc5a6498b9d76be; L_L17 f23a24dafacf1f3a.
Receipts (python / node / certificate):
- 0506: 958d49cbbd99bcfa / c0cbb71154d6ef8a / f1bcf8c5e8c9bae3
- 1114: 1d90faad499b78c2 / 92f1593bb5c9f7c7 / 9fb534b0c528391b
- 0917: fe522dc6dd78289e / bc71d631221accb9 / 2997c8fbdf46c377
- marker: 9fa412114086b18b / 0943e2ea4e1169bc / 4f6fd3419ed52352
- E07A: a33ab6adeab98611 / 6a7ed7422306fd05 / 0df07ad4202b4afb
- KEY_W: 1875676f6fad1277 / dc3804f47e2a7dc1 / d822e0ea6dcf8fb3
Audits: FRAME0506_wb 4fb3537d6318b91d; FRAME1114_wb a180061da47e37ad; FRAME0917_wb 51b5663707e5f60f; FRAME_MARKER_CLASS c729f758b2946039; L07_onesided_wb 6a2eb4edcc1f2ae3; KEY_W 842e3a45a5d1a940; FRAME0506_COMPARISON 87538e9124012 3c1 (read: head only) -> 87538e91240123c1; FRAME1114_COMPARISON f8a1f52d9413dd2a and FRAME0917_COMPARISON bddc01e5967dbf00 (hash only); frame-direct-import/IMPORT.json 8f259a339f468d3c.
Proof sources: FRAME_L9.json 15975a656870d9f9; FRAME_L9.md 20fc49dea2b00fe3; frame-premise-producer/THEOREM.md fb5cde9c4e50feb8; CLASS_FORMAT.md a445043af2da8887; c7-c8 PROOF.md c35d48ab808fd23c; case-repair-S/PROOF.md f63251b65b5c5a0d; ACTIVATION.json 60c13d920adbdfb8; PROOF_BRIDGE_V2.md 198b70376f3687c0.
Read after my verdict: REPORT_C_frame.md 113f6fa4df01a0f8 (agrees on all four premises; its open item on X-emptiness is what COARSE_LOOSE_CAPACITY now closes); REPORT_CAPACITY_LEMMA.md d9b883c5c42dc024 (first third and its verdict lines; agrees).
The other files of join_design/classes*/ used by region_scan.py were not hashed one by one.

(5) NOT READ

- Checker sources (exact_classes.py, verify_classes_wb.js and the other Python modules), any row arithmetic, the Git objects and execution authenticity behind the audits, the checker's implementation of "orbit", "mirror_x" and quarter-turn lifts.
- REVIEW_KEYW_AMENDMENT.md (0600869f, hash only), check_keyw.py, CONDITIONAL_AMENDMENT.json.
- coarse-capacity-R/PROOF.md (bae93844), INPUTS.json, RESULT.json, both scope and interface files, REPLAY.json, verify_readonly.py: hash only. About 2,400 characters in the middle of PROOF_BRIDGE_V2.md (application steps) were not read.
- c7-c8 RECEIPT.json (16a97f33) and accepted.json (43ef993f): hash only.
- independent-frame-review REVIEW.md; marker-class-Q CONVERSION.md beyond one line, REQUEST.json, REPORT_MARKER_CONVERSION.md, marker-import-AD files; REPORT_A_charge.md, REPORT_D_join.md, REPORT_CHARGE_SEMANTICS.md; F1_PROOF.md, LOOSE_IDENTITIES.json, check_f1.py; GLOSSARY.md; SELECTED_ORIGINAL_MAP.json content.
- The first-run folders.
- ROOT_ADMISSION and SELECTOR_LOGIC: the seventeen-factor separations, root arcs, JPA admission of [591183/1408817, 44941/100000], the label-12 argument, and the PSS and PSE uses beyond the fact that their trigger polygons equal the coarse regions.

(6) QUESTIONS TO THE AUTHORS

1. Will FRAME_L9.json (status "NEW_REVIEW_PENDING", first-run receipt keys) get a note or successor naming the second-run receipts, and should the H6_PREMISES rows FRAME_0506, FRAME_1114, FRAME_0917 pin receipt_python.json and receipt_node.json directly, as FRAME_MARKER does?
2. PROOF_TEXT line 94: replace "Each S_k lies in its whole coarse region" by the clipped statement for k = 17?
3. The Python receipt of FRAME_1114 differs between first and second run (6dc053db against 1d90faad), while those of FRAME_0506 and FRAME_0917 are byte-identical across runs. What differs? I did not open the first-run folder.
4. The KEY_W class comment says "MEASURING file ... numbers not agreed with the local side". Please confirm that the endpoints 30651/100000 and 44941/100000 are the ones the JPA and JG admissions were checked against; I verified only the case partition.
5. The three FRAME_wb audits cite selection manifests b55c0d3f and f6d31ce4. Is FINAL_BINDING_CHECK.json (manifest 49a24436) the intended sole link to the final manifest?

