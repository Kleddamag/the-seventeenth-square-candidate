Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line. This report reviewed the earlier executions of the capture computation, named here by neutral designations (table EARLIER_EXECUTIONS.tsv); the audit of the execution carried in this edition and the complete row comparison with the earlier ones are separate evidence.

HOLDS WITH CONDITIONS. No gap found inside the reviewed scope; every reviewed row holds given the premises of other readers listed under "Conditions" below.

Scratch folder: <reviewer scratch>/ (walk.py, walk_full.out, geom.py, geom2.py, nc/).
Sentences marked JUDGEMENT are mine; the rest are quoted lines or computations.

CONDITIONS (premises I used and did not check)
C-a. CHARGE_SEMANTICS: a complete authentic receipt implies the score inequality for every packing of side <= C in F_U.
C-b. FRAME_ASSIGNMENT: half-marker occupied in the common half frame; L9 has exactly one parent, distinct from the marker parent.
C-c. The off-wall case predicate x9 > 53/100, the wall partition, and KEY_W_ELIMINATION.
C-d. ROOT_ADMISSION for label 9 and for the chart itself. I took reference centres and axes from upper-packing-certificate.json and load_reference() in mk_join_roots_v5.py (p13 shifted by t0/3, tilted axes for labels 11 and 13 only). I did not compare that chart with SPEC 3.0.
C-e. COARSE_LOOSE_CAPACITY for regions 3 and 15. It is needed for the C rows in JG only, not for the 24 clauses.
C-f. C7_C8_TRANSFER for C_7 and C_8.
C-g. The "true" flags inside the SAVED_PROVENANCE audits (bytes match git, rows match python). I checked hashes and partitions, not the git objects.

FINDINGS, most serious first (none is a gap)
F1. Six selected receipts are strict by exactly one integer unit (B*Gamma - M = 1): Q_6, Q_7, Q_16, PW_6, C_10, PSS_L02_T15 (used by both L02 clauses). Recomputed from the receipts; strict, but with no slack against any doubt about M or Gamma.
F2. S17 is not inside coarse region 17 as literal rectangles: S17 runs to x = 26/5, coarse17 to about 5.199531. Inclusion holds only after clipping to the physical centre box [1000469/2000000, 8351531/2000000]^2 (computed). PROOF_TEXT section 5 says "Each S_k lies in its whole coarse region" without that qualifier; section 6 says "physically contained". This affects only the X-emptiness step for C rows in JG, which holds after clipping.
F3. Stale wording in the frozen manifest:
  - top-level status is "CONDITIONAL_THEOREM_WITH_OPEN_CAPTURE_AND_LOCAL_PREMISES";
  - the PSS entries carry acceptance.status "EXACT_PSS_BUDGET_STILL_REQUIRED" beside status COUNTED and a bound receipt;
  - RECEIPT_ROSTER.json pins as "selection" the historical endgame-AM/ORIGINAL_MAP.json (3219c786...), not SELECTED_ORIGINAL_MAP.json (63943cf0...). The two agree in "selected" and "literal" on all 84 rows (computed).
F4. For C_5, C_10, C_13, C_14 the H6_PREMISES row pins two saved-provenance audits: one of the historical execution (Node checker 72b92624...) and one of the repaired execution (7f6b2347...). The effective execution is the repaired one in all four.
F5. JUDGEMENT: PROOF_TEXT section 6 identifies the PSS trigger parent through coarse capacity. For the 24 T15 clauses this is not needed: the trigger polygon is literally the S slot of L_L15.json, and S15 clipped has diameter^2 = 799624844761/4000000000000 < 1. These clauses do not depend on COARSE_LOOSE_CAPACITY.
F6. JUDGEMENT plus computation: high-first scoring is not load-bearing for any reviewed row. Across all 54 literal files a threshold-0 slot meets a threshold-4 slot only in the four label-12 files (PSS_L12_T15, Q_L12, PW_L12, classes_JD/L12), and only on boundary seams with no interior overlap. Re-deriving the label-12 implication with the printed tau (minimum) gives the same occupancy conclusion.
F7. Confirmations of two exceptions stated in the text: the PW_11 target HULL11 is not inside the JPWS_v4 label-11 factor (it is inside JPW13_v2x; the slab target B_label11 is inside JPWS_v4). The raw C_12 arc [558609/2000000, 4494109/10000000] is not inside the JG_v2 label-12 arc; cut at rho = 207107/500000 it is.

(1) TABLE
BRANCH_JPG15m_L01, 02, 05, 06, 07, 08, 10, 13, 14, 16 | HOLDS under C-a to C-d | PSS_Lxx_T15 + L_15; walk.py 0 mismatches; geom.py G2 (trigger = S15, arms, marker/trigger separation, target inside JPG15m_v5 box and arc)
BRANCH_JPG15p_L01, 02, 05, 06, 07, 08, 10, 13, 14, 16 | HOLDS under C-a to C-d | same files, plus-arm, JPG15p_v5
BRANCH_JPG15m_L11, BRANCH_JPG15p_L11 | HOLDS under C-a to C-d | PSSW37_L11_T15 + L_15; HULLW11 inside the v5 label-11 factor (smallest arc margin 2.57e-13, exact, positive)
BRANCH_JPG15m_L12, BRANCH_JPG15p_L12 | HOLDS under C-a to C-d | PSS_L12_T15 + L_15; half-marker inside M(5 slots) union PB12 exactly; diam^2(hexagon union PB12) = 9437/31250
Q_1..Q_8, Q_10..Q_17 (16 rows) | HOLDS under C-a, C-b | walk.py; geom.py G3, G5; geom2.py H1 (each QB_j inside JQ_exact_v1 factor j), H4
PW_1, 2, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16 | HOLDS under C-a, C-b | walk.py; geom2.py H2 (inside JPW13; all but 11 inside JPWS), H4
L_3, L_4, L_15, L_17 | HOLDS under C-a, C-b, C-c | walk.py; geom.py G3; geom2.py H2, H3
C_1, 2, 5, 6, 10, 11, 12, 13, 14, 16 | HOLDS under C-a, C-b, C-c, C-e | walk.py; geom.py G3, G4 (X empty when fully gated); geom2.py H3
C_7, C_8 | NOT READ as premises | dependency on E07A and FRAME_MARKER through C7_C8_TRANSFER noted. Roster rows have no execution and derived_from [E07A, FRAME_MARKER]. Their literal targets (classes/C_L07.json, C_L08.json) do lie inside JG_v2 factors 7 and 8 (computed).
Budgets used by the clauses: CLASS_PSS_Lxx_T15 (11), CLASS_PSSW37_L11_T15, L_15 | receipts verified | walk.py

(2) HAND-OVERS RESTATED

Form of a branch clause (root JPG15m or JPG15p, rigid label j).
Given:
  - a 17-square packing of side <= C, concentric in F_U, in the common half frame;
  - a parent in the half-marker M (centre in the hexagon, side direction tan-half in [0, rho] modulo quarter turns);
  - off-wall: the unique L9 parent has x9 > 53/100, so the column WC = [-131/250, 53/100] x [24137/10000, 29637/10000] and AQ inside it hold no centre;
  - L_15: sum < 20 with thresholds M 4, S15 0, AQ 0;
  - the branch: role 15 is the S15 occupant, with canonical theta15 in [-pi/4, pi/4) and tau15 <= -1/20 (m) or tau15 >= 1/20 (p).
Steps:
  1. L_15 with one M parent gives a parent in (S15 union AQ) outside M; AQ is empty, so S15 is occupied. S15 has capacity one, so that parent is role 15.
  2. Role 15 lies in T15S = S15 x ([1/20, rho] union [-rho, -1/20]). The seams tau = ±1/20 and theta = -pi/4 are inside the closed arms, since rho^2 + 2*rho - 1 > 0.
  3. The marker parent and role 15 are different parents: the hexagon and S15 are separated in y by about 0.9288.
  4. PSS_j^15: sum < 23 with thresholds 4 / 4 / 0 / 0. So 17 + 3N(H) - N(E outside H) < 23 with N(H) >= 2 forces N(E outside H) >= 1. WC is empty, so a parent lies in the target (PB_j, or HULLW11 for j = 11) and is neither the marker nor the trigger parent.
Required: that target, as a closed centre polygon times a closed arc, lies in factor j of the literal v5 root after the chart xi = e·(c - (U-L)/2 - p_j), with L in the root file's enclosure. This holds for all 12 labels in both roots. Box margins at flush right/top walls are 4.32e-17 = (R - L) - eps > 0; arc ends for labels 1, 2, 7, 8 coincide exactly with the root arc ends.
Label 12: M is the half-marker minus the target (5 slots). Either the marker parent lies in PB12, or it lies in M and step 4 applies. PB12 is occupied either way; union capacity makes the occupant the marker parent.
Strictness: the receipt inequality is strict (M*q < p*Gamma in integers); the gate is open and the arms closed. Both signs use the same file; the other arm is simply unused.
Nothing UNUSED is relied on: every selected name is PSS_Lxx_T15 or PSSW37_L11_T15, is among the manifest's OR options, has activation EXISTING_REVIEWED_OPTION and no extra class premises (script-checked).
JUDGEMENT: the seventeen JPG15 regions (12 selected targets, S3, S4, S15, S17, L9 with x >= 53/100) are pairwise strictly separated after clipping, so seventeen occupancies give seventeen distinct parents with no further capacity argument.

Base rows.
Q_j, bound 23: classes M 4, AQ 4, QB_j 0. AQ = [-131/250, 53/100] x [24137/10000, 129/50] for the twelve rigid j and x [24137/10000, 13/5] for j = 3, 4, 15, 17, every direction. Marker and wall parent are distinct (L9 is disjoint from the hexagon), so a parent lies in QB_j. Use: JQ (y9 <= 129/50, closed) takes all 16; JPWS (129/50 < y9 <= 13/5) takes the four loose ones.
PW_j, bound 23: classes M 4, W 4, HULL_j 0, with W = [-131/250, 53/100] x [129/50, 29637/10000]. Use: JPW13 takes all 12; JPWS takes the 11 with j != 11.
L_k, bound 20: classes M 4, S_k 0, AQ(13/5) 0. Use wherever AQ is empty: off-wall, and JPW13 (y9 > 13/5). The seam y9 = 13/5 has AQ occupied and belongs to JPWS, where loose Q rows are used instead. Clipped diam^2 of S3, S4, S15, S17: 1097067164761, 1249531044761, 799624844761, 1059571044761, each over 4*10^12.
C_j, bound 20: classes M 4, T_j 0, X 0. X has the same 9 slots in all ten files. Use: JG only. X is empty there because:
  - the two region-9 slots miss the closed gate hull (gaps 1/200000 below and 974949/14197000000 above, reproduced);
  - the AQ slot has x <= 53/100;
  - the six coarse 3/15/17 arms hold only the gated S_k parent, by coarse capacity. Widths and far-edge distances equal the lemma's (w, H) = (529/750, 2821531/2000000) and (3427/5000, 2859531/2000000); coarse17 clipped has diam^2 = 1851391155161/4*10^12.
Absent numbers:
  - Q_9, PW_9, C_9: label 9 is the trigger or gated parent itself.
  - PW_3, 4, 15, 17: replaced by loose Q_3, 4, 15, 17 in JPWS and by L_3, 4, 15, 17 in JPW13.
  - PW_11 in JPWS: replaced by SL11_T020.
  - C_3, 4, 15, 17: replaced by L_3, 4, 15, 17 (S_k times the closed gate fits JG; S4 in any direction).
  - C_7, C_8: C7_C8_TRANSFER.
Every use I found in PROOF_TEXT sections 5 and 6 is covered by a row that exists and is COUNTED.

(3) SCRIPTS AND CONTROLS

walk.py (sha 81d7a5d7fe45b7ff; output c13631646d452882): 14794 checks, 0 mismatches, over 24 clauses, 12 clause budgets, L_15 and 42 base rows (64 executions). Per statement it checks:
  - manifest pin = H6_PREMISES = map = sha256 of the literal on disk;
  - roster JSON = TSV;
  - both merged receipts PASS_CLASSES_EXACT_COVER, rows 0..N, nothing missing or failed;
  - side text "4675531/1000000" and centre (1169/500, 1169/500) in both statements; certificate L/A = normalized_target = C;
  - bound, strict integer inequality and recomputed surplus;
  - certificate.json sha, M and Gamma equal to the receipt;
  - class alias: all 64 receipt class files equal json.dumps(literal) with the trailing newline removed, regenerated and hashed;
  - Node checker: every effective execution has 7f6b2347...; the 10 historical ones have 72b92624...;
  - slices: each row covered exactly once and passed, in Python and in Node;
  - slice file hashes equal the job receipt hashes in the saved-provenance audits (58 audits), whose job ranges partition the rows.
Negative controls on scratch copies of the first execution of CLASS_PSS_L01_T15, all rejected: one row flipped to failed; budget raised to 23*Gamma; one slice triplet removed; side text altered; class coordinate 1/20 changed to 1/21; an extra newline in the literal. An unmodified copy passes.

geom.py (13d1e2a7facfcd25): 372 exact checks, 0 fails. Controls --break 1..4, all rejected: a trigger arm narrowed; one M slot of the label-12 file dropped; the wrong cut for Q_3; gate end moved to 613/2000.

geom2.py (e915c24f04a55071): 70 further checks, 0 fails. Covers the frame marker literal (same hexagon), every base target against its root, 17-region separation for JQ, JPWS, JPW13, JG and JPG15, and the low/high overlap census.

Hand checks: branch implications L01, L11, L12 (and the other nine mechanically); base uses Q_1 in JQ, C_1 and C_12 in JG, PW_11 in JPW13 versus JPWS.

Surpluses (B*Gamma - M) for the clause budgets: L01 21, L02 1, L05 12, L06 21, L07 7, L08 4, L10 14, L11 23, L12 10, L13 15, L14 10, L16 7; L_15 8.

(4) SHA256, first 16 hex digits
PACKET.json 99d813ec5d1ffd1a
THEOREM_MANIFEST.json 49a2443699a03620
SELECTED_ORIGINAL_MAP.json 63943cf07fd93323
H6_PREMISES.json 6741793e2af90717
PROOF_TEXT.md b42fa1670b11643a
H6_HANDOFF.md d229a1629e5596e7
H6_COVERAGE.tsv 9e9884091d5f8bed
RECEIPT_ROSTER.tsv b8dbc710126b066e
RECEIPT_ROSTER.json c031c9afc47c7ddb
JPG15m_exact_v5 f6495dc60d07a4fa
JPG15p_exact_v5 6c9ad4887e868fe0
JQ_exact_v1 f4d1607eb4378487
JPWS_exact_v4 7d32a55bc2b08005
JPW13_exact_v2x e1a489e1f0d04ec0
JG_exact_v2 f635af684d0f81d3
upper-packing-certificate.json 24e296f5995abc94
mk_join_roots_v5.py 1c57f1adf7051d64 (chart formulas only)
CLASS_FORMAT.md a445043af2da8887
marker.json 520ce3cea70663d9
L_L15 cfc5a6498b9d76be
PSS_L01_T15 7dce6c116b54beeb
PSS_L12_T15 f3faf1759bb6fc44
PSSW37_L11_T15 721d1ab8cdb957f7
Q_L01 2631b5aeba0c3e23
PW_L11 8a4b05525575d22d
classes_JD/L01 e7291cc33c302b88
classes_JD/L12 133ddb28b6227353
L_L03 654dcdb2bd7dc627
L_L04 036302c5ecfec8c4
L_L17 f23a24dafacf1f3a
C_L07 60341809dba3593a
C_L08 bb345831da943357
SL_L11_T020_DH afde932909082930
pss-ruling/ACCEPTED_INTERFACE.json c2a5a5359975aa6b
endgame-AM/ORIGINAL_MAP.json 3219c78600158729
The remaining class literals, receipts, certificates and saved-provenance files were each hashed against their pins by walk.py.

(5) NOT READ
  - checker sources (exact_classes.py, verify_classes_wb.js) and the worker-binding repair; the git objects behind the saved-provenance audits; no receipt row was recomputed;
  - CHARGE_SEMANTICS, FRAME_ASSIGNMENT, C7_C8_TRANSFER, KEY_W, COARSE_LOOSE_CAPACITY proofs (only the (w, H) and diameter inputs were reproduced);
  - ROOT_ADMISSION reviews, label-9 admission, SPEC 3.0 chart definition;
  - local trees LOCAL_JPG15m/p;
  - PER_BRANCH_CAPTURE_OPTIONS files, S6 activations, WALL_TRIGGERS.json (literals recomputed instead), EXACT_ENDPOINT_AND_CASES.json, MANIFEST_TABLES.md, PROOF_SKELETON.md, GLOSSARY.md;
  - the earlier reports REPORT_D_join, REPORT_C_frame, REPORT_A_charge, final-review REPORT.
Of the pinned earlier reviews I opened only pss-ruling/ACCEPTED_INTERFACE.json, after my own verdict. It says "requires_L_k": true and excludes only the PSSW25_L13 files; I agree on both. It points to an <author reply> file, which I did not open.

(6) QUESTIONS TO THE AUTHORS
Q1. Is the chart of the v5 roots exactly load_reference() of mk_join_roots_v5.py (p13 shifted by t0/3 along v13, tilted axes for 11 and 13 only)? The root files do not list p_i. Which pinned file states the chart independently of the generator?
Q2. Should PROOF_TEXT section 5 say "each clipped S_k lies in its coarse region"? S17 exceeds coarse17 in x before clipping.
Q3. Are the manifest fields in F3 intended to stay as historical wording in a frozen packet whose rows are all COUNTED?
Q4. For the six receipts with surplus exactly 1: is the integer rounding of the weights (weight_denominator 10^9) the only source of M and Gamma, so that the one-unit strictness is exact and needs no interval argument?
Q5. For C_12 in JG the cut at rho needs "T12 occupant = marker parent". Is the capacity of the union of the hexagon with the C_12 box [20889/10000, 3111/1250] x [25971/10000, 2997/1000] pinned anywhere? By my bounding-box computation its diam^2 is at most 0.4428 < 1; the 9437/31250 figure in the text is for the PB12 box of the wall and tilted profiles.

