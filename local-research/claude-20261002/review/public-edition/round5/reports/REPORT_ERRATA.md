Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line.

HOLDS WITH CONDITIONS: (C1) the corrected text still contradicts the BC graph in one sentence about COARSE_LOOSE_CAPACITY (F1); (C2) the minimum-score argument needs the seventeen-region profile separation and the label-12 marker-minus-target covers, which I did not recheck (other readers did); (C3) the three TERMINAL-2 parts are not judged here; (C4) B-F5, the overlap remark in R-F5 and FC-Q1,2,4 have no answer in BB/BC.

No changed hunk states anything false. No change weakens a hypothesis that the selected route uses. I found no selected application that needs the high-first score.

## Findings, most serious first

**F1 (TEXT against graph, residual).** Corrected line 98, last sentence, is unchanged from the frozen text: "WALL_PARTITION and ROOT_ADMISSION explicitly depend on this lemma [COARSE_LOOSE_CAPACITY] and all four L rows". In the BC graph, LEMMA_COARSE_LOOSE_CAPACITY has exactly one user, JG_ESCAPE_EMPTY. LEMMA_WALL_PARTITION and LEMMA_ROOT_ADMISSION depend only on LEMMA_ALGEBRAIC_ENDPOINT. The frozen H6_PREMISES lists the lemma for both. JUDGEMENT: the graph follows the new argument (roles 3 and 15 defined by the small slots) and I see no step of partition or admission that needs coarse capacity. The sentence should be corrected or the two edges restored. Not a gap: the lemma is an ancestor of FINAL_OPTIMALITY either way.

**F2 (record, graph ids).** "Every one of the 210 ids appears" is true only under renaming. 100 ids appear literally: C_7, C_8, FRAME_ASSIGNMENT, C7_C8_TRANSFER, KEY_W_ELIMINATION, 84 BRANCH, 11 LOCAL. The other 110 appear only as LEMMA_<id> (12 mathematical premises) or BUDGET_<id> (98 executed rows). No node field or sentence in BB/BC states this convention. Under the map id -> {id, LEMMA_id, BUDGET_id} all 210 are present. Node LEMMA_CHARGE_SEMANTICS still carries the high-first claim text ("sum of high-first pose scores psi"), while the BUDGET nodes carry the literal minimum statements.

**F3 (TEXT, dangling reference).** Corrected line 112 (unchanged) says "A permitted PM_j, PT_j or PS_j^k exact inequality forces its literal target by Section 3". The new Section 3 treats only bound 17, the frame pairs, bound 20 and bound 23; the PT sentence (161/8) was dropped. No PM or PT file is selected (my census: thresholds only 0, 4, 5/4, 7/8), so this is harmless. Line 118 still says "whole coarse trigger region" for k = 3, 15, where the PSS trigger is now S_k.

**F4 (TEXT precision).** Corrected line 64 names `cert_restricted/node/verify_classes_wb.js`. That file exists only at local-research/claude-20261002/cloud/bundle/local-research/claude-20261002/cert_restricted/node/ (7f6b234768f812b7, hashed by me). The directory local-research/claude-20261002/cert_restricted/node/ holds only verify_classes.js (72b92624de356507). BB note 4 and the crosswalk give the full path; the manuscript line does not.

**F5 (record, pins).** The five admission-20261011 answer files are in no hash list of BB or BC. BB STATUS_AND_SOURCE_NOTES.md cites two of them by path only, and cites "<author reply>" as the explanation. <reply pointer file> resolves that to an <author reply> file, which was outside the reader's scope and which is not a pinned source. LABEL11_EXECUTED_ARCS.json (the answer to A-Q5) is cited by no BB/BC file.

**F6 (TEXT, quantifier).** Old line 50 said "for every actual seventeen-square packing in one containing square of side C in the declared frame". New line 52 says only "for the named literal file". The quantifier now lives only in the printed receipt string. JUDGEMENT: restore it in the sentence.

**F7 (TEXT, new word).** New line 58 says "Nonnegative integer outer weights"; the frozen text had no "integer". I checked only that required_units and budget_units are integers in all 98 Python receipts and that surplus = bound*required_units - budget_units > 0. Certificate weights were not read.

**F8 (note).** The new ENDp paragraph uses "the S17 parent", which needs L_17. The map row BRANCH_JPG17p_L06 has no extra capture premise; the graph supplies BUDGET_L_17 through OFFWALL_LOOSE_ROLES. Consistent.

## (1) Tables

### Changed hunks (old line -> new line, my own diff of b42fa167 against dc0d6e7b; 29 ranges)

The supplied PROOF_TEXT.diff and PROOF_TEXT_BC.diff have the same added and removed lines as mine; only the placement of one blank line in the first hunk differs.

| hunk | answers | verdict | basis |
|---|---|---|---|
| 1c1 title | none | HOLDS | label only |
| 2a3-4 addendum header | none | HOLDS | packet hash 99d813ec quoted correctly |
| 20c22 enclosure wording | T-F6 | HOLDS | EXACT_ENDPOINT_AND_CASES.json has isolating_box_radius 1/10^12, tight_root_intervals (width 2e-52) and L_interval. dL/dt is about -1.23, so the 1e-12 box moves L by about 1.2e-12, far more than R-L = 4.8e-17. Denominator 1+2t-t^2 is about 1.593 > 0. |
| 48c50 psi -> tau_D | SA-F1 | HOLDS; mathematical change | Score redefined as the least containing threshold. It equals the printed receipt wording in all 98 rows (script). Weaker than psi, so it follows from the same checker argument. The discovery-engine sentence is dropped (not load-bearing). |
| 50c52 receipt statement | SA-F1 | HOLDS, see F6 | C and frame centre are in all 98 statement strings. Side transfer unchanged (concentric boxes). Dropped: the explicit quantifier, "counts parents once", and the premise list (moved to new 64). |
| 52c54 cell comparison | SA-F1 | HOLDS | Re-derived: if a high class meets the cell, r > 1 and r >= every containing high threshold >= tau. If none meets, recognised lows are a subset of containing classes, so r >= tau. If none is recognised, r = 1 >= tau because no high class contains p. |
| 54c56 limiting core | SA-F1 (condensed) | HOLDS; sentences dropped | Dropped "all rows together cover square directions modulo quarter turns" and "charge at least the generic lower charge". Both belong to the imported CHARGE_SEMANTICS premise; no hypothesis changed. |
| 56c58 counting, one-unit | C-F1 | HOLDS, see F7 | Eight surplus-1 receipts found by me: Q_6, Q_7, Q_16, PW_6, C_10, PS_L14_T17, PSS_L02_T15, PS_L06_T17_ENDm. FRAME_1114 has surplus 1/2, which is 137*998806500 - 8*17104561312 = 4 after clearing q = 8. |
| 58c60 high-first not required | SA-F1, FR-F4 | HOLDS | See section (2). The old "A merged PASS" paragraph moved to new 64. |
| 60c62 frame pair scores | SA-F1, FR-F4 | HOLDS | My exact separating-axis check with mirror images: 0506 4 pairs, 1114 4 pairs, 0917 12 pairs, all strictly separated. Dropped: the identity "sum psi = 17+3N(H)-N(E outside H)" and its "occupant outside H" conclusion; no longer used. |
| 62c64 merged PASS, Node name | SA-F4, R-F6, R-F8, FC-Q3 | HOLDS, see F4 | 7f6b2347 hashed. "five-slot" removed; literal M slot counts are Q_12 6, PW_12/PS/PSS 5, C_12 4. Dropped: the PT sentence (no PT selected) and "SL11_T020 gives a B11 occupant" (content survives at lines 78, 106, 170). |
| 65a68-69 frame symmetry | R-F1 | HOLDS | Class files: FRAME_MARKER symmetry orbit, threshold 0, bound 17. 0506: mirror_x, M is the box, 5/4, side-W0 7/8, 137/8. 1114: hexagon 5/4, interior-W 7/8, 137/8. 0917: M, BONUS_1114, BONUS_0506 at 5/4, region-17 at 7/8, 145/8; mirror of region-17 is L9 = [-131/250, 4501/5000] x [24137/10000, 29637/10000]. All arcs [-rho, rho]. |
| 78c82 | SA-F1 | HOLDS | Occupancy by vacancy; distinctness by profile geometry. |
| 84c88 "high-first" -> "minimum-score" | SA-F1 | HOLDS | KEY_W has classes M (4) and E (0, 3 slots). |
| 94c98 "After clipping..." | C-F2, FR-F3 | HOLDS, see F1 | S3 = [129/100, 8751/5000] x [-1/2, 3751/5000] lies in coarse3 = [129/100, 2993/1500] x [-1/2, 1411/1000] literally. S15 = [5369/2500, 1019/400] x [19879/5000, 26/5] lies in coarse15 = [19953/10000, 26807/10000] x [1623/500, 26/5] literally. S17 = [19629/5000, 26/5] x [24137/10000, 7159/2500]; coarse17 = [3775331/10^6, 5199531/10^6] x [24137/10000, 29637/10000]. Raw inclusion fails (26/5 > 5199531/10^6); it holds after clipping x to 8351531/2000000. The three clipped diameters squared equal the printed fractions. |
| 110c114 PSS paragraph | SA-F2 | HOLDS; hypothesis changed | COARSE_LOOSE_CAPACITY removed from the PSS clauses. Checked: T3S polygon equals S3 and T15S equals S15 exactly; arms [1/20, rho] and [-rho, -1/20]; the S_k slot in L_k has arc [-rho, rho], all directions. |
| 118c122 | B-F2, T-F1, FC-Q3 | HOLDS | Map: label 6 is ENDm on JPG17m and ENDp on JPG17p; label 7 is PS_L07_T17 on both; no PSEb selected. |
| 122c126 | B-F2, T-F1 | HOLDS | See section (2). |
| 124c128 | B-F1, T-F1 | HOLDS | Hashes computed: S6_ACTIVATION 97399331, S6_ACTIVATION_AR 2db226af, REPORT_S6_join_PS06T17ENDp 25205623. The two printed statements are identical; classes_sha256 d27d6258 and 8c4870dd. |
| 125a130-131 | B-F2 | HOLDS | Map: PS_L05_T17 on JPG17p, PS_L01_T17 on JPG17m, PS_L16_T09 on JPA; "unused" list has 7 entries. Dropped: the 624-option and K-reserve paragraphs; none is selected. |
| 130c136, 131a138-139 chart | C-Q1, T-F4 | HOLDS | SPEC_v3.0.md 0a6dfc2a, lines 58-70 read: p13 = p13(file) - (T0/3) v13, T0 = u9x(u9x + 4 - Sref), frames (u_i, v_i) for 11 and 13 only. Packing hash 24e296f5 not rehashed. |
| 136c144 JG capacity | C-Q5 | HOLDS | Exact maximum over vertex pairs of the hexagon and the C12 box [20889/10000, 3111/1250] x [25971/10000, 2997/1000] is 0.3952979177669444... < 3953/10000. The PB12 union gives exactly 9437/31250. |
| 156c164 | A-F2 | HOLDS | Agrees with ADMISSION and LOCAL readers; not recomputed. |
| 162c170 | B-F3 | HOLDS | JPWS_exact_v4.json (7d32a55b): `what` has "except label 11, which is in B_11 of the slab statement"; `premise_note` has no exception. |
| 168c176 | TM-F2 | HOLDS | See "G20S composition" below. |
| 170c178 + 171a180-181 | TM-F3, T-F5 | HOLDS | Windows equal EXPECT_G20S.json and EXPECT_HW.json. The stage, transfer and ratio numbers are those of TERMINAL; not rederived. |
| 180a191-196 graph and Q7 | T-F2, T-F3 | HOLDS, see F2 | |
| 180a197-198 provenance | R-F2, R-F3, R-F7, R-F9 | HOLDS | My recount: 90 final-newline removals, 2 json.dumps, 5 identical, plus FRAME_MARKER against its class literal aa8b1410. |
| 180a199-202 JG count, chart, JPA, KEY_W | L-F3, L-Q3, L-Q4, FR-Q4 | HOLDS (JG terminal count and JPA identity not recomputed) | offwall_keyw_direction_interval is [30651/100000, 44941/100000] in the packet file. |

**Still missing from the text.** Lines 62, 94, 118, 122, 162 and sections 1, 5, 6, 8 are all corrected. Residual: F1 (line 98), F3 (lines 112, 118), F4 (line 64), F6 (line 52).

### OPEN findings

| id | state | where and adequacy |
|---|---|---|
| A-F1 | ANSWERED | BB STATUS note 1 (pinned) names the final manifest's C_16 as authority. LITERAL row C_16 has both receipts PASS. The detail file C16_STATUS_ERRATUM.json is unpinned (F5). |
| A-F2 | ANSWERED | New line 164, BB note 8, LEAF_REUSE_SCOPE.md. |
| A-F3 | ANSWERED | Closed by T-OK; new line 22 consistent. |
| A-F4 | ANSWERED | BB note 7: both copies are a08363c6 (I hashed the packet copy). The script still has no pin. |
| A-F5 | ANSWERED | BB note 7: intentional alias. |
| A-Q5 | ANSWERED BUT INADEQUATE | True: all four executed PSW37/PSSW37 files have HULLW11 arc [1430271/5000000, 4828869/10000000] and one identical slot (my check). The answer file is unpinned and uncited (F5). |
| B-F1 | ANSWERED | New line 128, BB note 6, crosswalk signed_rows. Executed bytes equal json.dumps(proposal) for both (my check). |
| B-F2 | ANSWERED | New lines 122, 126-130. |
| B-F3 | ANSWERED | Graph nodes OCC_JPWS_*, OCC_JPW13_*, OCC_JQ_* consume SL11_T020, PW_j, Q_j; new line 170. |
| B-F4 | ANSWERED | All 84 BRANCH nodes have direct edges to CASE, FRAME_ASSIGNMENT, KEY_W_ELIMINATION, OFFWALL_LOOSE_ROLES. |
| B-F5 | NOT ANSWERED | No BB/BC sentence on the README wording. |
| B-F6 | ANSWERED | BB note 6, last sentence. |
| T-F1 | ANSWERED | ENDp argument now at new line 126. |
| T-F2 | ANSWERED | BC graph; see F2 for ids. |
| T-F3 | ANSWERED | New line 195 states the limit; Q7 is not a premise. |
| T-F4 | ANSWERED | New line 136. |
| T-F5 | ANSWERED | New lines 176-180. |
| T-F6 | ANSWERED | New line 22. |
| C-F1 | ANSWERED | New line 58, SMALL_CHECKS.json; see F7. |
| C-F2 | ANSWERED | New line 98. |
| C-F3 | ANSWERED | BB notes 1 and 3 (pinned) state the current status; crosswalk reports 84 equal rows (not recomputed). Section 9 of the text still calls the manifest tables "the status authority". |
| C-Q1 | ANSWERED | New line 136. |
| C-Q5 | ANSWERED | New line 144. |
| SA-F1 | ANSWERED | MINIMUM_SCORE_SCOPE.md, LITERAL_STATEMENTS.json, new lines 50-62. The frozen H6 CLASS rows keep the psi wording. |
| SA-F2 | ANSWERED | BB3 and new line 114: tau3 is the S3 occupant's angle. Leaves F1. |
| SA-F3 | ANSWERED | As B-F4; BRANCH PSS rows also have BUDGET_L_k directly. |
| SA-F4 | ANSWERED | New line 64, BB note 4. Review named: worker-binding-repair ACCEPTED_INTERFACE.json e2efa5bf (not opened). See F4. |
| SA-F5 | ANSWERED | BB note 2 and crosswalk: the 84 retained rows are unchanged; KEY_W amendment review 0600869f (not opened). |
| FR-F2 | ANSWERED | BC notes; SOURCE_BINDINGS pins independent-frame-review ACCEPTED_INTERFACE.json a72f5556 and FINAL_BINDING_CHECK.json 55a98218 (not opened). |
| FR-F3 | ANSWERED | New line 98. |
| FR-F4 | ANSWERED | Confirmed for the whole map; see section (2). |
| FR-Q4 | ANSWERED | New line 202, BC notes. |
| R-F1 | ANSWERED | New line 68, BC notes. |
| R-F2 | ANSWERED | New line 197, BB note 5. |
| R-F3 | ANSWERED | BC notes; REPORT_MARKER_CONVERSION.md a366444c pinned (not opened). |
| R-F4 | ANSWERED BUT INADEQUATE to close | BC notes state the scope honestly and say not all second runs are finished. Stays open until the second execution closes. |
| R-F5..F8 | PARTLY | Node name, Python header hashes (kept as an explicit provenance assumption) and embedded classes key are answered. The overlap-tolerant merge is NOT ANSWERED (none overlaps). |
| R-F9 | ANSWERED | BC notes, new line 197. |
| L-F3 | ANSWERED | New line 199: explained, not pinned. |
| L-Q3 | ANSWERED | New line 199 and the chart-origin sentence in BC notes. |
| L-Q4 | ANSWERED | RECORD_EJPA_v5.md is canonical; both pinned at e10be786. |
| TM-F1 | NOT JUDGED | Other reader; see the SOURCE_BINDINGS paragraph below. |
| TM-F2 | ANSWERED | G20S_COMPOSITION_OF_RECORD.md; box-wide 0.859 declared unused. |
| TM-F3 | ANSWERED | New lines 178-180. |
| TM-F4 | ANSWERED | Composition file names the superseding reviews 241de6ac / 91aa01be and 667b0820 / d2d07d68 (not opened). |
| FC-Q3 | ANSWERED | Lines 62, 118, 122. |
| FC-Q1,2,4 | NOT ANSWERED in BB/BC | Audit lead's coverage table. |

## (2) Hand-overs restated

**ENDp clause (PS_L06_T17_ENDp_H4T4 on JPG17p).**
- Given: printed statement sum tau < 23 at side C, frame centre (1169/500, 1169/500), slots as written with quarter-turn lifts.
- Classes read from the executed bytes: M = marker hexagon with arc [0, rho], threshold 4; T17 = coarse17 rectangle with arc [1/20, rho], threshold 4; PB6 = [20379/5000, 26/5] x [14003/10000, 8001/5000] with arc [-10269/200000, 500417/10000000], threshold 0; WC = [-131/250, 53/100] x [24137/10000, 29637/10000], all directions, threshold 0.
- M, PB6 and WC are identical objects to those in PS_L05_T17, PS_L06_T09 and PSS_L06_T03. The T17 slot equals the "+" arm of the original two-arm trigger. ENDm is the same with the "-" arm.
- Branch: x9 > 53/100, label 9 gated, gate 3 holds, canonical tau_17 in [1/20, tan(pi/8)).
- Steps: rho^2 + 2 rho - 1 = 309449/250000000000 > 0, so tan(pi/8) < rho and the role-17 direction is in the arm. Clipped S17 lies in coarse17, so its centre is in the trigger polygon. The half-marker parent is in M. Hexagon x <= 316/125 and T17 x >= 3775331/10^6, so the two parents differ. WC lies in L9 with x <= 53/100, so it is empty. If PB6 were empty no parent would be in a low class; every score is 1 or 4, two are 4, sum >= 23. Contradiction with the strict bound.
- Seams: tau_17 = 1/20 is closed in the arm. theta_17 = -pi/4 belongs to branch m and ENDm.
- Agreement with SELECTOR-B: same target, arcs, hashes, activation files and argument. Its root-admission figures (xi_1 in [-0.0999650468, -4.3e-17]) were not recomputed.
- JUDGEMENT: the proof as written is correct and complete for occupancy. Admission of PB6 to the v5 factor is imported.

**Minimum score suffices.**
- Census of all 98 executed statements (statement string and class file compared, 0 differences): bound 17 with (0), 1 row; 137/8 with (5/4, 7/8), 2; 145/8 with (5/4, 7/8, 5/4, 5/4), 1; 20 with (4, 0), 2 (E07A, KEY_W); 20 with (4, 0, 0), 14 (four L, ten C); 23 with (4, 4, 0), 29 (16 Q, 12 PW, SL11_T020); 23 with (4, 4, 0, 0), 49 (CLASS).
- Marker: score is 17 - N(orbit).
- Frame pairs: high and low unions strictly disjoint, so the minimum and high-first scores coincide.
- Bound 20 and 23: each application assumes the target empty and has every other low class empty by context (AQ and WC lie in L9 at x <= 53/100; X by JG_ESCAPE_EMPTY). Then no parent is in a low class and the count closes. The argument never evaluates a pose lying in both a high and a low class.
- Label-12 seams: with target 12 assumed empty, no parent lies on a seam with the target, and the marker parent lies in a threshold-4 slot by the cover. Handled.
- What is lost: the old conclusion "the forced occupant is outside both high classes". It is replaced by the separation of the seventeen profile regions and the union capacity for label 12, both imported.

**LITERAL_STATEMENTS against receipts.** Not 12 but all 98 rows, both receipts each: statement string equal character for character, classes_sha256 equal, receipt file hash equal, PASS_CLASSES_EXACT_COVER, executed class file hash equal, source literal hash equal, bound equal. 0 mismatches. C_7 and C_8 are marked derived, with no receipt.

**Graph.** 328 nodes, acyclic, single sink FINAL_OPTIMALITY, every node reaches it, no dangling dependency.
- C_7 and C_8 depend on C7_C8_TRANSFER, which depends on FRAME_ASSIGNMENT, BUDGET_E07A, BUDGET_FRAME_MARKER, LEMMA_C7_C8_TRANSFER; PROFILE_JG consumes both.
- ADMIT_JPWS has BUDGET_SL11_T020, eleven PW (not PW_11) and Q_3, 4, 15, 17 as ancestors. ADMIT_JPW13 has twelve PW and four L. ADMIT_JQ has sixteen Q.
- Every ADMIT depends on its PROFILE (the occupancies) and LEMMA_ROOT_ADMISSION.
- No capture-side node (281 checked) has LOCAL_*, TREE_*, EXCLUDE_* or the terminal lemmas as an ancestor.

**G20S composition.** Every arrow is stated.
- G20S window: 29 positions in [-1/5, 1/5], angles 1/10, xi_(2,1) in [-39/125, 0], xi_(11,2) in [-1/5, 1/5], xi_(13,2) in [-1/5, 28/125].
- T1: 3/20, 101/1000, [-8/25, 1/100], [-1/5, 2/25], [-1/5, 1/10]; cut xi_(2,1) <= 0.
- HW window, read from EXPECT_HW.json: T1 with upper end 0. The composition file asserts the containment but does not print these numbers.
- T2: 1/250, 1/500, [-8/25, 1/250], [-1/5, 1/20], [-1/5, 3/40]; cut again.
- Entry: 1/200, 1/400, a in [0, 8/25], b in [-1/20, 1/5], z in [-1/5, 3/40]. S >= 4 from area 16.
- All equal TERMINAL's report, hand-over (b), and the two EXPECT files end for end.

**SOURCE_BINDINGS and the three TERMINAL-2 parts.**
- Raw stop cuts: named (finite-entry-stop-pruning PRUNING.json 0bbb358a, RESULT.md, entry-review REVIEW.md and MANIFEST 86c21cac, root-review REVIEW.md).
- Two raw-to-root transfers: named (entry-review check_transfer.py and check_binding.py for 501/100000; full-stopped-propagation/rational-entry-review REVIEW.md and MATHEMATICAL_INTERFACE.json for 1/10000 to 1/5000).
- Necessity of the finite rows: named only as the four stage reviews, independent_model.py (4d9954c7) and the scope review 241de6ac. No single proof text of row necessity is pinned; the composition file says so itself.

## (3) Scripts and controls (all in <reviewer scratch>/)

- lit.py, lit2.py: 98 rows against both receipts and class files, 0 mismatches. Control: one statement changed ("23" to "22") and one class hash zeroed in a scratch copy; 4 mismatches flagged.
- framesep.py: exact strict separation, all pairs pass. Control: low polygons shifted by 3/4; the 1114 file is reported not separated. The 0506 and 0917 files stay separated under that shift, as their geometry requires.
- geom.py, geom2.py, geom3.py: slots, coarse regions, END files, JG capacity. Control: C12 box shifted by 2/5 gives 0.9066, reported not below 3953/10000.
- Surplus recomputation for 98 receipts: all equal the printed surplus, all positive.
- dag.py, dag2.py, dag3.py. Controls:
  - deleting C_7, C_8 -> C7_C8_TRANSFER: noticed (three nodes no longer reach the final node);
  - deleting OCC_JPWS_SL11_T020 -> BUDGET_SL11_T020: noticed;
  - deleting JG_ESCAPE_EMPTY -> LEMMA_COARSE_LOOSE_CAPACITY: noticed;
  - adding BUDGET_Q_1 -> LOCAL_JQ: noticed as a back edge;
  - adding a cycle: noticed;
  - deleting BRANCH_JPA_L01 -> KEY_W_ELIMINATION: NOT noticed, because that node stays an ancestor through CASE_JPA; my check is on ancestors, not direct edges.
- I did not run the authors' scripts (check_literal_statements.py, check_small.py, check_crosswalk.py, check_sources.py, build_dag.py).

## (4) sha256 prefixes

- Packet: PACKET.json 99d813ec5d1ffd1a; PROOF_TEXT.md b42fa1670b11643a; SELECTED_ORIGINAL_MAP.json 63943cf07fd93323; H6_COVERAGE.tsv 9e9884091d5f8bed; H6_PREMISES.json 6741793e2af90717; EXACT_ENDPOINT_AND_CASES.json a08363c6a5f4ebb2.
- BB: ADDENDUM 65605d09a3e41129; PROOF_TEXT_CORRECTED b5ebdceaa1c9fd9a; PROOF_TEXT.diff b3e9c8df70035709; LITERAL_STATEMENTS.json 20c0f22bd67b0e8f; MINIMUM_SCORE_SCOPE.md a25ef9a3ceb2812d; STATUS_AND_SOURCE_NOTES.md 64275fe1e472a02d; STATUS_SOURCE_CROSSWALK.json e398029138d7cab7; SMALL_CHECKS.json 4b05623206ff9dc2; COMPLETE_DAG.json a8f0ba159dadc5d1 (not analysed).
- BC: ADDENDUM 4d55d63ac865178e; PROOF_TEXT_CORRECTED dc0d6e7b5bd8aab8; PROOF_TEXT_BC.diff ac94a3c54d8e2799; COMPLETE_DAG.json e8a786a77aaa9884; G20S_COMPOSITION_OF_RECORD.md 92bb48dd36d7b82b; SOURCE_BINDINGS.json 560b232adad72e8f; SOURCE_AND_EXECUTION_NOTES.md c2ae8fad644543fd; PREPARATION_NOTES.md 26534907649b1893.
- Admission answers: C16_STATUS_ERRATUM c64a95946e6c9acb; CASE_SOURCE_BINDING ce8b1c86f3d17b56; CHILD_CONTROLS ac0a15507aa740ac; LABEL11_EXECUTED_ARCS 255e2dd786db71cd; LEAF_REUSE_SCOPE.json 65a1913bb4782ef3, .md 2c07f1de36770826.
- Others: SPEC_v3.0.md 0a6dfc2ae10ed6f3; EXPECT_G20S.json 1447c955c52f5a52; EXPECT_HW.json 5f63bf97bf6e39f6; JPWS_exact_v4.json 7d32a55bc2b08005; S6_ACTIVATION.json 973993319a656c8e; S6_ACTIVATION_AR.json 2db226af512d9dcc; REPORT_S6_join_PS06T17ENDp.md 252056233c814a75; verify_classes_wb.js (bundle) 7f6b234768f812b7; verify_classes.js 72b92624de356507; ENDm classes d27d6258c5bfcb5b; ENDp classes 8c4870ddca35cac2.
- All 98 executed class files, 196 receipts and 98 source literals: hashed by lit.py against the values in LITERAL_STATEMENTS.json, all equal.
- Readers' material: FINDINGS.md b1e22970add8e591; REPORT_SELECTOR_B.md 1c2003f5afdca974; REPORT_TERMINAL.md 04695c4a184f43e9.

## (5) Not read

- The other eight reader reports beyond grep hits in SELECTOR_B, TERMINAL and FRESH_CODEX.
- BB COMPLETE_DAG.json and the .tsv companions.
- Bodies of the authors' five BB scripts and two BC scripts (only a grep in build_dag.py).
- Every review file that the addenda cite by hash: worker-binding ACCEPTED_INTERFACE, REVIEW_KEYW_AMENDMENT, REPORT_MARKER_CONVERSION, independent-frame-review ACCEPTED_INTERFACE, FINAL_BINDING_CHECK, the stage, scope and transfer reviews, REPORT_S6_joins.
- The sixteen-square THEOREM.md, THEOREM_G20S.md, acceptance logs and certificate headers.
- Root files other than the two note fields of JPWS_exact_v4.json.
- The seventeen-region separations, the label-12 covers and all root admissions.
- Certificate weights; any row arithmetic.
- <author reply> (outside scope).
- The files of the graph nodes' "files" fields.
- LEAF_REUSE_SCOPE.md beyond its first paragraphs.

## (6) Questions to the authors

1. Line 98, last sentence: do WALL_PARTITION and ROOT_ADMISSION depend on COARSE_LOOSE_CAPACITY or not? Correct the sentence or add the two edges.
2. Will the graph state the id convention (LEMMA_<id>, BUDGET_<id>), or carry the H6 id in a field of each node?
3. Will BC pin the five admission-20261011 files, and replace the reference to "<author reply>" by pinned evidence?
4. Line 112: delete "PM_j, PT_j" or say that Section 3 does not treat them because none is selected.
5. Line 52: restore "for every packing of seventeen unit squares in the side-C square of the declared frame".
6. Line 58: is "integer" for the outer weights literal (weights scaled by 10^9), and which pinned file says so?
7. Line 64: give the full bundle path of verify_classes_wb.js.
8. Should LEMMA_CHARGE_SEMANTICS in the graph state the minimum form, since nothing downstream uses psi?
9. Which pinned text proves necessity of the saved finite rows (for TERMINAL-2)?
10. B-F5 (README wording) and the overlap-tolerant merge in R-F5: one sentence each in an addendum?

