Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line. This report reviewed the earlier executions of the capture computation, named here by neutral designations (table EARLIER_EXECUTIONS.tsv); the audit of the execution carried in this edition and the complete row comparison with the earlier ones are separate evidence.

HOLDS WITH CONDITIONS: (C1) CHARGE_SEMANTICS as a premise: each receipt is an authentic execution and `classes_sha256` is the hash of the class file the checker actually read; I re-ran no checker rows. (C2) FRAME_ASSIGNMENT, WALL_PARTITION, L_17: half-marker occupied in one common frame, L9 has exactly one parent, role 17 is the unique occupant of S17 and differs from the marker parent. (C3) ROOT_ADMISSION for the simultaneous seventeen-factor separation of JPG17m/p; I checked only "target inside its own factor" and "role 17 inside factor 17". (C4) The chart convention (reference poses from `upper-packing-certificate.json`, tilted axes for labels 11 and 13, the shift of p13) is taken from `mk_join_roots_v5.py` lines 245-262, not re-derived from SPEC 3.0. No gap, wrong number or wrong seam was found in the 24 clauses or in SL11_T020.

## Findings, most serious first

**F1. Sign binding of the two PS_6^17 halves rests on one hash only.** The printed statement strings of the ENDm and ENDp receipts are word-for-word identical, because the statement lists only class names, thresholds and slot counts. Only `classes_sha256` tells them apart (d27d6258… against 8c4870dd…). I reproduced both hashes from the pinned proposals (see section 3). JUDGEMENT: acceptable, but the sign of each half is carried entirely by condition C1.

**F2. PROOF_TEXT section 6 is stale against the final map.** Line 122 names four activated signed budgets (PS5/17 ENDp, PS6/17 ENDm, PS16/9 ENDa, PS1/17 ENDm). SELECTED_ORIGINAL_MAP uses only PS6/17 ENDm and PS6/17 ENDp and lists the other three as unused. PS6/17 ENDp on JPG17p appears in H6_HANDOFF (SELECTOR_LOGIC) but nowhere in PROOF_TEXT. Line 118 ("the active selector uses the admitted positive k=17 options for labels 6/7") is also stale: label 7 uses the original PS_L07_T17. JUDGEMENT: a text defect, not a logical gap, since the map and H6_PREMISES are consistent.

**F3. Nothing in the dependency graph records who consumes SL11_T020.** No row of H6_PREMISES has SL11_T020, PW_j or Q_j in `depends_on`; LOCAL_JPWS depends only on the two local-checker premises. "Label 11 of JPWS rests on SL11_T020, not PW_11" is fixed only in prose (PROOF_TEXT sections 3, 5, 7) and by geometry. The geometry is decisive: the PW_11 target HULL11 does not fit factor 11 of JPWS_v4 (its xi hull leaves the box by 0.181), so PW_11 could not place label 11 there. Also, PROOF_TEXT line 162 says the root's `premise_note` "has this explicit exception"; the literal `premise_note` of `JPWS_exact_v4.json` reads "PW_j … places the rigid labels in HULL_j" with no exception. The exception is in the file's `what` field.

**F4. Clause rows understate their premises.** Each BRANCH row has `depends_on` = [SELECTOR_LOGIC, CLASS_x] and `extra_capture_premises: []`, yet every clause uses L_17 (role 17), the unique L9 parent (WC empty) and the marker. These arrive only transitively through SELECTOR_LOGIC → ROOT_ADMISSION. JUDGEMENT: sufficient if the composition reader follows the transitive closure.

**F5. Receipt-folder READMEs name two different byte strings as "the file the run read".** The table gives the bundle file `exempt/JPS/L05T17.json` (a0d32ad9…), while job.txt names another source (the class-certificate folder named as source in the job file of the first execution of CLASS_PS_L05_T17) and the receipts bind `classes.json` 3720bdf6…. The two are equal as JSON (verified); the second is `json.dumps` of the first without the final newline. Same pattern in the first execution of CLASS_PS_L01_T17.

**F6. Path style differs.** The two END rows of SELECTED_ORIGINAL_MAP give the literal as an absolute path; H6_PREMISES gives it relative. Same file, same hash.

**F7. Thin but exact margins (information).**
- Flush right walls, labels 2, 6, 7, 8: slack 4.32e-17, which is R − s_hi − eps > 0.
- Arc slack exactly 0 for labels 1, 2, 7, 8: root arc ends equal slot ends ±500417/10000000; closed inclusion.
- Label 11 arc slack 2.6e-13.
- Root arc 17 passes the seam ±1/20 by 4.66e-10.
- Receipt surpluses of 1 unit: PS_L14_T17 and PS_L06_T17_ENDm; 2 units: PSW37_L11_T17.

**F8. PS_1^17 slice 9 (Mac execution): acceptable.** JUDGEMENT, on these facts: the README states it openly; job.txt shows the same checker hashes, certificate c20657b8… and class bytes 3b2a7a5a…; the audit binds the Mac files by hash and records `all_saved_bytes_match_git: false` and names the slice 9 of the first execution of CLASS_PS_L01_T17, computed on the build machine, as a local slice instead of hiding it. I compared the Mac slice with the later cloud run of slice 9 of the first execution of CLASS_PS_L01_T17 myself: Python and Node, all 1,500 rows identical in every field except `cpu_seconds`; headers differ only in timing, worker count and `verified_utc`. Residual: the merged receipt contains the Mac slice; the later cloud run of slice 9 of the first execution of CLASS_PS_L01_T17 is stored but not merged.

## (1) Table

| id | verdict | relied on |
|---|---|---|
| BRANCH_JPG17m_L01, BRANCH_JPG17p_L01 | CONDITION (C1–C4) | geom.py: PS_L01_T17 target in factor 1, position slack 9.5e-7, arc slack 0; walk.py receipt surplus 8; F8 |
| BRANCH_JPG17m_L02, _p_L02 | CONDITION | geom.py slack 4.3e-17, arc 0; surplus 21 |
| BRANCH_JPG17m_L05 | CONDITION | original two-arc PS_L05_T17, first execution of CLASS_PS_L05_T17, surplus 17 = 23·998849323 − 22973534412; by hand in (2) |
| BRANCH_JPG17p_L05 | CONDITION | same file and receipt; arc [1/20, ρ] present; root arc 17 lower end ≤ 1/20 |
| BRANCH_JPG17m_L06 | CONDITION (and F1) | PS_L06_T17_ENDm_H4T4, only arc [−ρ, −1/20]; surplus 1; M, target, WC identical to original 070c7c9b… |
| BRANCH_JPG17p_L06 | CONDITION (and F1) | PS_L06_T17_ENDp_H4T4, only arc [1/20, ρ]; surplus 6; by hand in (2) |
| BRANCH_JPG17m_L07, _p_L07 | CONDITION | PS_L07_T17, surplus 14; slack 4.3e-17 |
| BRANCH_JPG17m_L08, _p_L08 | CONDITION | PS_L08_T17, surplus 3 |
| BRANCH_JPG17m_L10, _p_L10 | CONDITION | PS_L10_T17, surplus 18; slack 3.9e-7 |
| BRANCH_JPG17m_L11, _p_L11 | CONDITION | PSW37_L11_T17 (target HULLW11), surplus 2; position slack 9.5e-7, arc slack 2.6e-13 |
| BRANCH_JPG17m_L12, _p_L12 | CONDITION | PS_L12_T17, surplus 15; five-slot M covers half-marker minus target (9-cell cut); diam²(hexagon ∪ box) = 9437/31250 |
| BRANCH_JPG17m_L13, _p_L13 | CONDITION | PS_L13_T17, surplus 9; slack 9.2e-9 |
| BRANCH_JPG17m_L14, _p_L14 | CONDITION | PS_L14_T17, surplus 1; slack 2.2e-7 |
| BRANCH_JPG17m_L16, _p_L16 | CONDITION | PS_L16_T17, surplus 22; arc fits after 3 quarter turns |
| SL11_T020 | CONDITION (C1, C2, C3; F3) | receipt surplus 12; B11 in JPWS_v4 factor 11 (slack 9.6e-7), arc fits; factor 11 strictly separated from the other 16 factor boxes |
| the 13 CLASS rows used above (CLASS_PS_L{01,02,05,07,08,10,12,13,14,16}_T17, CLASS_PSW37_L11_T17, CLASS_PS_L06_T17_ENDm_H4T4, _ENDp_H4T4) | CONDITION (C1) | walk.py: both receipts PASS, 18,000 rows, side, frame, bound, strict surplus, hashes, slices |
| the other 36 selected strict budget rows (T09, T03, T15 families) | receipt level HOLDS under C1; geometry NOT READ | walk_all.py: 0 mismatches |
| L_17, FRAME_MARKER (base rows used) | receipt level only; their proofs NOT READ | walk.py; L_17 surplus 4 (bound 20), FRAME_MARKER surplus 13 (bound 17) |

## (2) Hand-overs restated

**Logical form of a clause (JPG17σ, rigid label j).**
- Given: a packing of side S ≤ C read in the frame with centre (1169/500, 1169/500); a marker parent p_M with centre in the hexagon and a side representative in [0, π/4]; exactly one parent in L9, with x9 > 53/100; role 17 = the unique occupant of S17, canonical θ17 ∈ [−π/4, π/4), τ17 = tan(θ17/2), with τ17 ≤ −1/20 (m) or τ17 ≥ 1/20 (p). The seams ±1/20 belong to the tilted branches.
- Statement used: Σ score < 23, strict, for the literal file with classes M (4), T17 (4), target (0), WC (0).
- Argument: WC ⊂ L9 ∩ {x ≤ 53/100} is empty. If no parent lay in the target, no parent would be in a low class; p_M ∈ M and p_17 ∈ T17 are different parents (hexagon and T17 rectangle are disjoint); the sum would be ≥ 4 + 4 + 15 = 23. Hence the target is occupied.
- JUDGEMENT: this form holds whether the score is read "least threshold" (the receipts' printed wording) or high-first, because under the hypothesis no parent is in a low class.
- Required afterwards: target inside root factor j (positions and arc). For j ≠ 12 the target polygon is disjoint from the hexagon, the T17 rectangle and WC, so its occupant is a third parent. For j = 12 the occupant is p_M by capacity of hexagon ∪ box.

**Trigger coverage, all 24 (computed).**
- T17 rectangle = [3775331/10^6, 5199531/10^6] × [24137/10^4, 29637/10^4]; it contains S17 clipped to centres feasible at side C.
- Arcs [−ρ, −1/20] and [1/20, ρ], ρ = 207107/500000, ρ² + 2ρ − 1 > 0 so ρ > tan(π/8); closed at ±1/20.
- The two halves of PS_6^17: ENDm serves only JPG17m, ENDp only JPG17p. Between them lies the open gate (−1/20, 1/20), which belongs to JPG15m/p and JG, so there is no gap at either seam. θ17 = −π/4 belongs to m and is inside ENDm.
- Root arc 17: JPG17m [−4147/10000, −0.04999999953], JPG17p [0.04999999953, 4147/10000]; both contain their seam.

**JPG17m label 5 (exact).** Target PB5 = [−1/2, 3001/5000] × [14003/10000, 8001/5000], arc [−500417/10^7, 10269/200000]. Reference p5 = (1/2 + eps, 3/2 + …), direction (1,0). Clipped to feasible centres: x ≥ 0.5002349532.
- xi_1 ∈ [−5e-18, 0.0999650468] inside [−1/10^6, 49983/500000].
- xi_2 ∈ [−0.0999349532, 0.0999650468] inside [−19987/200000, 49983/500000]; least slack 4.68e-8.
- Arc slack 1.4e-10 and 8.0e-10.

**JPG17p label 6 (ENDp).** Target [20379/5000, 26/5] × [14003/10000, 8001/5000]; xi_1 ∈ [−0.0999650468, −4.3e-17] inside [−49983/500000, 0]; xi_2 as for label 5. Arc slack 8.0e-10 and 1.4e-10.

**JPG17m label 12.** Box [21889/10000, 3011/1250] × [26971/10000, 2897/1000], arc [1532251/5000000, ρ]. The hexagon cut along the four box lines gives 9 cells: the central one lies in the box, each of the other 8 lies in a full-arc M slot, and the fifth M slot covers the hexagon for directions [0, 1532251/5000000]. So half-marker ⊂ M ∪ target. Position slacks 1.0e-7 to 9.0e-7; the arc fits without cutting at tan(π/8).

**JPG17p label 11.** HULLW11 slacks about 1e-6; arc slack 2.6e-13.

**SL11_T020.**
- Given: branch JPWS, x9 ≤ 53/100 and 129/50 < y9 ≤ 13/5, role 9 the unique L9 parent, marker parent distinct (hexagon disjoint from L9).
- File: M (4), SLAB = [−131/250, 53/100] × [129/50, 13/5] every direction (4), B_label11 (0); bound 23 strict; receipt surplus 12.
- The slab is closed at y = 13/5, so that seam is the slab's. The AQ slot of the L files is closed at 13/5 as well, so the L rows cannot serve there; this agrees with the text.
- Conclusion: B11 is occupied, by the same 4 + 4 + 15 argument (no other low class). The occupant is neither the marker nor role 9, since B11 is disjoint from the hexagon and from L9.
- Uniqueness: diam²(B11) = 0.0491 < 1.
- Identification with label 11 downstream: B11 lies in factor 11 of JPWS_v4 (position slack 9.6e-7, arc fits). I mapped the whole factor-11 box back to the class frame; it has diameter² < 1 and is strictly separated from each of the other 16 factor boxes. JUDGEMENT: once all 17 factors are occupied, the B11 occupant is the one and only square the root calls label 11. That all the other factors are occupied is ROOT_ADMISSION and the other rows, not this row.
- B11 is not inside HULL11 (consistent with the text, which uses no such inclusion).

**UNUSED material.** None of RM12, RMSC, RME, AL, RMD, AC1, AC2, AL6 or an unselected END file appears in the 24 clause rows, their class rows or their proof lists (token scan in walk.py plus reading the rows). L01, L05 and L16 use the whole originals, not PS1 ENDm, PS5 ENDp or PS16 ENDp. The 22 original selections are listed candidates in the reviewed selector file with the same hash, bound 23 and no extra premise; the two END selections are in S6_ACTIVATION and S6_ACTIVATION_AR.

**Agreement with pinned reviews (read after my verdict).** REPORT_S6_joins.md and REPORT_S6_join_PS06T17ENDp.md give the same least margins (4.7e-8, 4.3e-17) and the same observations as my F4 and F5. Their condition "FRAME_MARKER receipt open" no longer applies: the receipt exists and passes my walk.

## (3) Scripts and controls

All in `<reviewer scratch>/`.

**walk.py** (clause → map row → H6 row → roster row → folder → both receipts → stored class bytes → certificate header → slices). Result: 24 clauses, SL11_T020, L_17, FRAME_MARKER: 0 mismatches.
- Every receipt: PASS_CLASSES_EXACT_COVER, rows 0..18000 (FRAME_MARKER 9000), missing 0, failed none, problems none, side 4675531/1000000 and frame (1169/500, 1169/500) in both statement strings, certificate L/A = normalized_target = C, bound·Γ − M equal to the stated surplus and > 0, 12 slices forming a gap-free partition.
- Class bytes: for the classes_v2 files the receipt hash is sha256 of `json.dumps(pin)` and the pin is exactly those bytes plus one final LF. For the two END proposals the pin is formatted differently; `json.dumps(json.loads(pin))` reproduces the receipt hash; no duplicate keys.
- Controls, all rejected: budget +17 units in both receipts; one failed interval plus altered side in the Node receipt; slice 7 removed; trigger arc 1/20 → 1/19 in the literal; the folder of CLASS_PS_L05_T09 offered for CLASS_PS_L05_T17; ENDp folder offered for ENDm (caught by hashes and surplus only, see F1).

**walk_all.py**: all 49 selected strict budget rows at receipt level: 0 mismatches; every one of the 84 clauses selects one of the 49.

**geom.py** (fractions only): 457 checks, 0 failed.
- Controls, all rejected: root box of label 5 narrowed by 1e-6; JPG17p root offered for JPG17m; ENDp literal offered for ENDm; the "above" slot removed from M of PS_L12_T17; gate end −1/20 → −51/1000; B11 shifted by 1/1000.
- Reproduced manuscript constants: 9437/31250; S17 diam² 1059571044761/4·10^12; coarse-17 diam² 1851391155161/4·10^12.

**Slice 9 comparison** (inline script): see F8.

## (4) sha256 prefixes of files relied on

Packet:
- PACKET.json 99d813ec5d1ffd1a
- PROOF_TEXT.md b42fa1670b11643a
- H6_HANDOFF.md d229a1629e5596e7
- H6_PREMISES.json 6741793e2af90717
- SELECTED_ORIGINAL_MAP.json 63943cf07fd93323
- RECEIPT_ROSTER.tsv b8dbc710126b066e
- EXACT_ENDPOINT_AND_CASES.json a08363c6a5f4ebb2
- THEOREM_MANIFEST.json 49a2443699a03620

Roots and chart:
- JPG17m_exact_v5 18550e414d3f5057
- JPG17p_exact_v5 11b68ec1eb4aa790
- JPWS_exact_v4 7d32a55bc2b08005
- upper-packing-certificate.json 24e296f5995abc94
- mk_join_roots_v5.py 1c57f1adf7051d64

Literals (pin / receipt class hash):
- PS_L01_T17 e103e79134f71481 / 3b2a7a5a7a40327c
- PS_L02_T17 2522523b1a481037 / f4776e1b44924128
- PS_L05_T17 a0d32ad9bccaa845 / 3720bdf64d7590b7
- PS_L06_T17_ENDm fea1d9752281aa0b / d27d6258c5bfcb5b
- PS_L06_T17_ENDp 7072785dd92ff4c2 / 8c4870ddca35cac2
- PS_L07_T17 ad6ba9389c28ddce / 8f552de7c0571541
- PS_L08_T17 5771bb501dc9cacd / 9ece4ccc2f082f63
- PS_L10_T17 6957b484e8fa3977 / 688c9683f7ad05e2
- PSW37_L11_T17 1cb191363af205fd / 7aab51a5e0b7e0cb
- PS_L12_T17 02088c87415cb244 / 903523c8439c05c4
- PS_L13_T17 0d529b9fa8fd0977 / aac19823f719d2ca
- PS_L14_T17 0b823b2a3326e556 / 48528ec98880fbf4
- PS_L16_T17 78653fbb5a0f429b / 9aada1e841617ced
- SL_L11_T020_DH afde932909082930 / 4a8380f457f347dd
- L_L17 f23a24dafacf1f3a / 650585f9e4e1ccaa
- FRAME_MARKER_CLASS aa8b1410906ddac7 (bytes)
- PS_L06_T17 original 070c7c9bd9f81bb5
- PW_L11 8a4b05525575d22d

Receipts and audits:
- first execution of CLASS_PS_L05_T17: python 005e9f1546dfcdb2, node f9b17eeaad35c281, certificate 0f68ece8bdc212b1, SAVED_PROVENANCE 583bb7b90f41460a
- first execution of CLASS_PS_L01_T17: python 597f869432d5d644, node 463ef53ac9f4e9be, certificate c20657b847698ec9, SAVED_PROVENANCE 435447f37ee15597
- Slice 9 of the first execution of CLASS_PS_L01_T17: mac py 43b6141ed654de0c, mac node c2f29683335af023, later cloud run py 438db52cbbdc5d0a, later cloud run node 3a721bb776a320a3
- The remaining receipt and certificate hashes equal the RECEIPT_ROSTER.tsv columns (verified by walk.py).

Other:
- Selector PER_BRANCH_CAPTURE_OPTIONS_V5_PSS_PSE_KEYW 4521655d218f635c
- S6_ACTIVATION 973993319a656c8e; S6_ACTIVATION_AR 2db226af512d9dcc
- REPORT_S6_joins 5bf2f5b613368ee7; REPORT_S6_join_PS06T17ENDp 252056233c814a75
- README of the first execution of CLASS_PS_L01_T17 76bc572092870b02; README of the first execution of CLASS_PS_L05_T17 8e76e932682299d3
- My scripts: walk.py b2ddd267d72dbf07; geom.py 2505854278762854

## (5) Not read

- The checker sources (exact_classes.py, verify_classes_wb.js); no checker row was re-executed; quarter-turn lifting and high-first order inside the checker.
- Git commits and branches behind the audits; the audit scripts; the `objects/` folders; SAVED_PROVENANCE files other than those of CLASS_PS_L05_T17 and CLASS_PS_L01_T17 (the others only hash-checked against their pins).
- ALIAS_CONTROLS.json, PS06P_GEOMETRY.json, `pss-ruling`, `psv-audit`, `pse-review`, `selector/ACCEPTED_INTERFACE.json`, REPORT_D_join.md, REVIEW_KEYW_AMENDMENT.md, the reports of the reviewers of premises C and D on B11 (hash-pinned sources of SELECTOR_LOGIC that I did not open).
- Proofs of FRAME_ASSIGNMENT, WALL_PARTITION, L_17 (receipt level only), KEY_W, COARSE_LOOSE_CAPACITY.
- The 16 × 16 pairwise separation of targets in JPG17m/p; root factors of labels 3, 4, 9, 15; the local trees.
- Geometry of the 60 clauses on JPA, JPG3m/p, JPG15m/p, and the L_k joins of the PSS rows.
- SPEC 3.0 (chart convention, C4); MANIFEST_TABLES.md beyond a grep; PROOF_SKELETON.md; RECEIPT_ROSTER.json.

## (6) Questions to the authors

1. Will PROOF_TEXT section 6 (lines 118 and 122) be brought in line with the final map: only PS6/17 ENDm and ENDp active, and PS6/17 ENDp named?
2. Which obligation id consumes SL11_T020, the PW_j (j ≠ 11) and Q_3, Q_4, Q_15, Q_17 for JPWS? Should ROOT_ADMISSION or a wall-branch row list them in `depends_on`?
3. PROOF_TEXT line 162 against the literal `premise_note` of JPWS_exact_v4.json: is the `what` field meant?
4. For the END receipts, is there any binding of the sign other than `classes_sha256`? The statement strings are identical.
5. The READMEs call the bundle file "the file the run read" while job.txt names `classcerts/<name>/classes.json`. Which bytes did the checker open?
6. Should the merged PS_1^17 receipt be rebuilt with the later cloud run of slice 9 of the first execution of CLASS_PS_L01_T17, so that no Mac slice remains in a receipt of record, or is the documented equality enough for you?

