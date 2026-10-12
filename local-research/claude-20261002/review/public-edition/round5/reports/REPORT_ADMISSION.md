Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line.

HOLDS WITH CONDITIONS (C1: the L enclosure upper end and eps, since the smallest admission margin is R - L_hi - eps = 4.319e-17; C2: the upstream premises FRAME_ASSIGNMENT, KEY_W_ELIMINATION, COARSE_LOOSE_CAPACITY, L_3/L_4/L_15/L_17 and every capture occupancy, none re-proved here; C3: the stale "C_16 RECEIPT OPEN" entry inside the packet must be reconciled; C4: the reviewers' own admission script was not run, so its verdict is not what I rely on)

FINDINGS, most serious first

F1 (record inconsistency inside the frozen packet). EXACT_ENDPOINT_AND_CASES.json, block C_legacy_exemption_absence.source_files[11], says C_16: "status: RECEIPT OPEN", "accepted_by: None", "needed: Matching strict exact class budget...". THEOREM_MANIFEST.json base_capture_rows and MANIFEST_TABLES.md line 61 say C_16 COUNTED. C_16's class T_label16 is the label-16 factor of root JG in my admission. JUDGEMENT: probably a stale copy in an expository file, but a packet file contradicts the status authority on a row that JG admission consumes; it needs a one-line reconciliation by the authors.

F2 ("a new region contains the one it replaces" is false for JPWS, and is not needed there). Computed: JPWS v4 is strictly inside JPWS v2x (v2x contains v4: True; v4 contains v2x: False). The replacement is justified only by the new capture statement SL11_T020 (target B_label11). My admission for JPWS used B_11 directly and passes. For the seven case-T roots the rule holds: v5 contains v4 and v5 contains v2, all 17 labels, boxes and arcs, exact (JPA, JPG3m/p, JPG17m/p, JPG15m/p). v5 does NOT contain v1 for the six JPG roots (v2 introduced the label-9 support cut). JUDGEMENT: harmless provided no v1-root tree or leaf, and no JPWS-v2x label-11 leaf, is used by the final trees; I did not check leaf provenance (that is LOCAL_CERTIFICATE_IMPORT).

F3 (smallest margin is 4.3e-17 and rests on another premise). In all eleven roots the smallest position margin is R - L_hi - eps = 172774611520751077003947028629799873599009499147027426104376477/(4*10^78) = 4.319365e-17, at the flush right/top wall ends whose root end is 0 (label 2 xi_1 hi; same value at 6 xi_1 hi, 7 xi_2 hi, 8 both, 15 xi_2 hi, 17 xi_1 hi). It is positive only because L <= L_hi < R - eps (eps = R - (p_2x + 1/2) = 5.172236e-18). This is exactly the ALGEBRAIC_ENDPOINT enclosure; I did not re-prove the enclosure.

F4 (authors' partition script does not read the packet copy). check_case_partition.py reads second-order-20261010/theorem/EXACT_ENDPOINT_AND_CASES.json. Computed: its 13 predicates and 11 root pins are identical to the packet copy. No defect, but the binding is by content equality, not by a pinned hash in the script.

F5 (note). H6_HANDOFF lists one sha256 (bf7771724f6229cc...) for both coarse-capacity-AP/PURE_LEMMA_SCOPE_V2.json and ACCEPTED_INTERFACE_V2.json. On disk both files do have that hash, so they are byte-identical. Not my obligation; reported for the COARSE_LOOSE_CAPACITY reader.

No gap or error found in the partition or in the admission numerics.

(1) TABLE

WALL_PARTITION | CONDITION (C2) | Own atom-wise check part.py on the packet's 13 literal predicates: 15000 product atoms (singleton endpoints and open intervals), exactly one predicate true on each; seams (x9=53/100, y9=129/50) -> JQ, y9=13/5 -> JPWS, y9=13/5+10^-30 -> JPW13. Own literal check of 29 wall triggers and 4 L exemptions (last.py). Authors' check_case_partition.py run on scratch copy: PASS, 41160 atoms; 4 scratch mutations rejected. Capacity/uniqueness inputs (L9 unique parent, coarse capacity, L budgets) NOT re-proved.

ROOT_ADMISSION | CONDITION (C1, C2, C3, C4) | Own exact-fraction derivation run_adm.py for all eleven roots, 17 labels each (34 box ends + arc per label): no failure. Root file sha256 = packet root_pin for all eleven; certificate root node (box, arc, S, assume=[], parent=null) and header (packing sha, Sref, S_floor, window, terminal) equal the root file for all eleven, certificate gz sha256 = manifest value for all eleven (bind.py). 136-pair disjointness and capacity one of the 17 selected targets for all eleven (extra.py).

(2) RESTATEMENT OF THE HAND-OVERS

Frame and units (computed/asserted for every file used): every class file has schema s17-classes-v1, symmetry "fixed", frame centre (1169/500, 1169/500). Every root has Sref = S_floor = R = 4675530093604551/10^15, S = [R, R], 17 labels. Chart (SPEC_v3.0.md section 1, lines 58-70): xi_ik = e_ik . (q_i - p_i), p_i from upper-packing-certificate.json, p_13 shifted by -(T0/3) v_13, axes (u_i, v_i) for labels 11 and 13, Cartesian otherwise. A class-frame point c is q = c - (U - L)/2 (1,1), U = 1169/250, L in [L_lo, L_hi] of the packet (same two rationals as composition.out). C = 4675531/10^6 enters only through the physical centre clip used in the capacity check.

Given: a packing at side S0 < L, placed concentrically in [0, L]^2, one common frame; a unique parent in L9 = [-131/250, 4501/5000] x [24137/10000, 29637/10000]; the half-marker occupant with side representative in [0, pi/4]; each selected class statement's target occupied. Required: for the branch that the decision list assigns, every label's parent has xi in the closed root box and one side direction in the closed root arc.

What I derived per label (all weak inequalities, closed sets):
- Position: extrema of xi over polygon vertices times {L_lo, L_hi}; for Cartesian labels intersected with the physical bound 1/2 - p <= xi <= L_hi - 1/2 - p (centre in [1/2, L - 1/2]^2 for any orientation); labels 11, 13 unclipped.
- Direction: a slot means "some side direction has tan-half in the closed interval"; I require a quarter-turn lift of the whole interval inside the root arc (exact cross-product test; lift 3 for label 16, 0 otherwise). All-direction slots: root arc at least a quarter turn (cos of its length <= 0).
- Label 12: interval cut at rho = 207107/500000, justified because target-12 and the marker have one parent (diam^2 of hexagon united with target = 0.301984 = 9437/31250 in ten roots, 0.395298 in JG, both < 1) and only the marker's own representative can lie in a slot with lower end > -rho and upper end < 1.
- Label 9, wall roots: rectangle x in [-131/250, 53/100], y in [24137/10000, 129/50] (JQ), [129/50, 13/5] (JPWS), [13/5, 29637/10000] (JPW13, closure); direction x axis +- 2 atan(31/1000) by my own wall lemma (cos + sin increasing on [0, pi/4]; (1 + 2 tau - tau^2)/(1 + tau^2) > 53/50 at tau = 31/1000).
- Label 9, off-wall: rectangle [53/100, 4501/5000] x [24137/10000, 29637/10000]; JPA: t9 in [591183/1408817, 44941/100000]; JG and six JPG: closed gate [61301/200000, 591183/1408817] plus the support bound q_x >= (cos + sin)/2 evaluated at both gate ends. Root end -9897/10^6 has margin 4.299e-07.
- Loose 3, 17, 15: slot S_k; gate = +-rot(1/20) closed; "m" = from the -45 degree direction to rot(-1/20); "p" = mirror; free otherwise. Label 4: S_4 or QB_4, free.

Targets used: JQ: QB_j of the sixteen Q16 files. JPWS: HULL_j of PW_j (j != 11), B_label11 of SL_L11_T020_DH, QB of loose Q_3,4,15,17. JPW13: HULL_j of all twelve PW_j, S_j of L_3,4,15,17. JG: T_j of the twelve C rows, S_j of L files. Seven tilted roots: the target of each of the 84 files in SELECTED_ORIGINAL_MAP.json (file sha256 checked against the map; root_binding checked against the packet root pin), S_j of L files.

Smallest margins found (position / smallest nonzero arc margin as a sine / ends with exact equality):
- JQ: 4.319e-17 at label 2 xi_1 hi / 1.561e-10 label 5 upper arc end / equality at labels 1, 2, 8, 9.
- JPWS: 4.319e-17 at label 2 xi_1 hi / 7.228e-11 label 11 upper arc end / equality at 1, 2, 7, 8, 9. Label 11 (B_11): box margins 9.812e-07, 9.925e-07, 9.630e-07, 9.644e-07; arc 3.731e-10 and 7.228e-11. Label 9 at the seam y = 13/5: xi_2 hi margin 1.089e-07. Smallest non-wall position margin seen: label 13 xi_2 hi, 3.588e-09.
- JPW13: 4.319e-17 at label 2 xi_1 hi / 7.228e-11 label 11 upper arc end / equality at 1, 2, 7, 8, 9. Label 9 xi_2 lo (y = 13/5, closed superset) 8.911e-07; label 11 xi_1 lo 4.420e-08.
- JG: 4.319e-17 at label 2 xi_1 hi / 1.2e-10 label 14 lower arc end / equality at 1, 2, 3, 5, 6, 7, 8, 15, 17. Label 9 arc 7.928e-10 and 9.236e-10.
- JPA v5: 4.319e-17 / 5.123e-13 label 11 lower arc end / equality at 1, 2, 7, 8. Label 9 lower arc end 1.398e-09.
- JPG3m, JPG3p, JPG17m, JPG17p, JPG15m, JPG15p (v5): 4.319e-17 / 5.123e-13 label 11 lower arc end / equality at 1, 2, 7, 8 and at the gate ends +-1/20 of the gated or tilted loose labels. JPG17m: label 13 xi_1 hi 9.201e-09; label 11 box 1.044e-06, 9.873e-07, 9.843e-07, 9.501e-07.
JUDGEMENT: equality at closed ends is admissible because targets, roots and SPEC arcs are all closed.

Root identity: sha256 of each of the eleven root files equals the packet root_pin and the manifest root_obligations entry. Each certificate's root node equals window.box, root_arc and S of that file with an empty assumption list.

Tube bounds the angle: SPEC_v3.0.md section 8 (lines 601-633) defines membership by |phi_i| <= alpha_i and proves it from cos Ab > 0 and |sin Ab| <= alpha - alpha^3/6. JG root: terminal alpha 1/10 for sixteen labels and 1 for label 4; terminal box xi_(2,1) in [-39/125, 0], xi_(13,2) in [-1/5, 28/125]; statement "TUBE ... sixteen squares other than 4". The certificate header's terminal equals the file's. I did not check the leaves' terminal tests.

Partition and seams (WALL_PARTITION):
- x9 = 53/100 belongs to the wall case. AQ, W, SLAB are closed at 53/100 and contain it. Off-wall is strict, which is what makes the closed WC and the L-file AQ empty (any occupant lies in L9, hence is the unique L9 parent).
- y9 = 129/50 belongs to JQ: the twelve rigid Q triggers are [24137/10000, 129/50] closed.
- y9 = 13/5 belongs to JPWS: loose Q triggers [24137/10000, 13/5], PW triggers [129/50, 29637/10000], SLAB [129/50, 13/5], all closed, thresholds 4, bound 23, every direction (rho > tan(pi/8)). JPW13 needs y9 > 13/5 strictly because the L-file exemption AQ is closed at 13/5; the predicate is strict. The JPW13 root is closed at 13/5 (superset only).
- For label 11 at the seam: the admitted target in JPWS is B_11 of SL11_T020, not HULL_11 of PW_11.
- t9: 61301/200000 is owned by the removed lower exit; 591183/1408817 and 44941/100000 by JPA. T9's literal lower end -408817/1000000 is exactly the quarter-turn image of 591183/1408817. KEY_W's literal low slot is [30651/100000, 44941/100000] on all of L9 (file read, hash matches manifest); its budget was not checked.
- tau_k = +-1/20 belong to the m/p branches; trigger slots are closed there.
- Signs and mirrors: both signs are separate roots, each admitted separately; no file used has a symmetry other than "fixed". The only reflection I met is the E07A to label-8 transfer (C7_C8_TRANSFER): the E07A target lies in T_7 and its x -> U - x image lies in T_8 (computed).
- JG exemption X of the twelve C files: slots 1, 2 miss the open gate by 1/200000 and by 974949/14197000000 (back-lift chart; 974949/14088170000 in the forward chart); slot 3 lies in the wall column; slots 4-9 are the coarse regions 3, 15, 17 beyond +-1/20 and contain S_k. Emptiness of slots 4-9 needs COARSE_LOOSE_CAPACITY, not re-proved.
- 84 tilted clauses: each file has exactly M, one trigger, one target and WC = [-131/250, 53/100] x [24137/10000, 29637/10000]; 15 + thr(M) + thr(trigger) = bound 23; the trigger contains the branch's trigger pose set in all 84 (JPA: T9 with the quarter-turn image of [591183/1408817, 44941/100000]; JPG k m/p: S_k with the correct sign, including the one-ended ENDm / ENDp files for label 6); every PSS clause names L_k as extra premise.
- Distinct parents: per root the 17 targets, clipped to [1000469/2000000, 8351531/2000000]^2, have diam^2 < 1 (largest 0.463497, label 3, JQ and JPWS; 0.439548, label 9, off-wall roots; 0.332827, label 13, JPW13) and all 136 pairs are strictly separated by an edge normal.

(3) SCRIPTS (all under <reviewer scratch>/)
- adm.py, run_adm.py: admission, eleven roots, FAILS: none.
- neg.py: 14 scratch root variants. 13 rejected: JPWS label 11 xi_2 hi -2e-6; JPWS label 9 y-top -2e-7 (seam 13/5); JPWS label 11 arc; JPW13 label 9 y-bottom +1e-6 (seam 13/5); JPW13 label 9 arc; JPG17m label 11 lower arc end turned by tan-half 1e-11; JPG17m label 17 gate end; JG label 9 support end +2e-6; JG label 12 arc; JPA label 9 exit end; JQ label 2 wall end -1e-16; JPG3p label 3 gate end; JPG15m label 13 xi_2 hi -1e-6. One accepted: JPG17m label 11 xi_1 lo +1e-6, because the true margin is 1.044e-06 (v5 box is the union with the old PB_11 box); shrinking by 2e-6 is rejected.
- bind.py --hash: eleven roots, "ALL EQUAL", gz sha True. No separate negative control; it is a plain equality test.
- extra.py: capacity, 136 pairs, label-12 union, 84 triggers, version containments.
- part.py: 15000 atoms, 0 bad. Negative controls on scratch copies: "y9 <= 13/5" to "<" (gap), "y9 > 13/5" to ">=" (double owner JPWS and JPW13), "y9 <= 129/50" to "<" (gap), JPWS "x9 <= 53/100" to "<" (gap): all detected.
- Authors' check_case_partition.py, copied to scratch (in place it would write CASE_PARTITION.json): PASS on the packet copy; the same four mutated inputs each end in AssertionError.
- last.py: wall triggers, L exemptions, C exemptions, E07A containment, KEY_W literal.
- NOT RUN: d-selected-roots-v2-review/check_review.py (reviewers' admission script; bound to a producer directory and writes beside itself) and anything in v5-root-review.

(4) SHA256 (first 16 hex)
PACKET.json 99d813ec5d1ffd1a; PROOF_TEXT.md b42fa1670b11643a; EXACT_ENDPOINT_AND_CASES.json a08363c6a5f4ebb2; SELECTED_ORIGINAL_MAP.json 63943cf07fd93323; THEOREM_MANIFEST.json 49a2443699a03620; H6_PREMISES.json 6741793e2af90717; H6_HANDOFF.md d229a1629e5596e7; SPEC_v3.0.md 0a6dfc2ae10ed6f3; upper-packing-certificate.json 24e296f5995abc94; composition.out 53ea429530b116f5; mk_join_roots_v5.py (read for conventions only) 1c57f1adf7051d64; check_case_partition.py 97ef83686bdd79a3; check_review.py (not run) cfd49942bcba624d; d-selected-roots-v2-review/ACCEPTED_INTERFACE.json 033302490f21463e; RECORD_EJPWS_v4.md (first 60 lines read) af742507a1553a11; SL_L11_T020_DH.json afde932909082930.
Roots: JQ_exact_v1 f4d1607eb4378487; JG_exact_v2 f635af684d0f81d3; JPA_exact_v5 adcf0d1bdc02b8ea; JPWS_exact_v4 7d32a55bc2b08005; JPW13_exact_v2x e1a489e1f0d04ec0; JPG3m_v5 1e2a3b429193a69f; JPG3p_v5 c4287958b08fe4fc; JPG17m_v5 18550e414d3f5057; JPG17p_v5 11b68ec1eb4aa790; JPG15m_v5 f6495dc60d07a4fa; JPG15p_v5 6c9ad4887e868fe0.
Certificates (full gz hash equal to manifest): JQ 0b2a8ff8a3f9e12d; JG e7587199a38d4772; JPA_v5 b9f9283979d2fab1; JPWS_v4 538a6a512a10b72d; JPW13 7147d7780da90060; JPG3m_v5 7535735021ff18c4; JPG3p_v5 804ae79493f67336; JPG17m_v5 68613d8407cb5a9f; JPG17p_v5 f392b6ba42c9abc3; JPG15m_v5 ed66c59b16b4b354; JPG15p_v5 1adb38643a3a28a1.
Class files: every Q, PW, L, C, E07A, KEY_W file was checked against the sha256 in THEOREM_MANIFEST base_capture_rows, and each of the 84 selected files against SELECTED_ORIGINAL_MAP, by assertion inside the scripts.

(5) NOT READ / NOT CHECKED
- REVIEW.md and INPUTS.json of d-selected-roots-v2-review; all of v5-root-review; morning-contract selector files; REVIEW_KEYW_AMENDMENT.md; F1_PROOF.md, LOOSE_IDENTITIES.json, check_f1.py; all coarse-capacity-R and -AP files; loose-only-review; PART3_REQUIRED_CLASS_FRAME.json; REPORT.md, REPORT_C_frame.md, REPORT_D_join.md; WALL_TRIGGERS.json and verify_wall_triggers.py (I checked the literals myself instead); FRAME_CHECK.json; jpa-import-AG/AUDIT.json; ADMISSION_v4.md; JOIN_ROOTS.md; all RECORD files except the first 60 lines of RECORD_EJPWS_v4.md; SPEC_v3.0_NOTES.md (root-region corollary). So I cannot say where I agree or disagree with the earlier reviews beyond the numbers the proof text quotes (9437/31250, 1/200000, 974949/14197000000, -9897/10^6, 110 nodes: the first four reproduced, the last not checked).
- No tree content beyond header and root node: zero terminal leaves, child coverage, leaf arithmetic, acceptance logs, h_report30 post-check.
- No capture budget or receipt; no charge semantics; FRAME_ASSIGNMENT, the KEY_W budget, coarse capacity, the L budgets.
- The root-end uniqueness of the L enclosure; G20S / HW; the terminal test of JG's leaves.
- Whether the class checker's slot semantics is "some side direction in the closed interval" as I assumed from PROOF_TEXT section 3 (CHARGE_SEMANTICS).
- The reflection used for the half-marker and the E07A transfer beyond the two containments stated.

(6) QUESTIONS TO THE AUTHORS
1. Why does the packet's EXACT_ENDPOINT_AND_CASES.json carry C_16 as RECEIPT OPEN while the manifest says COUNTED? Which is authoritative for the frozen packet, and is the file to be regenerated?
2. Does any leaf or subtree of the accepted JPWS_v4 certificate come from a JPWS v2x run whose label-11 hypothesis was HULL_11, and does any accepted v5 certificate reuse a leaf made on a v1 root (no support cut for label 9)? The region containments I verified cover v2 and v4 only.
3. PURE_LEMMA_SCOPE_V2.json and ACCEPTED_INTERFACE_V2.json are byte-identical. Intended?
4. check_case_partition.py reads the second-order copy of the decision list. Should the script, or its output CASE_PARTITION.json, pin the packet copy's sha256 (a08363c6...)?
5. The seven v5 roots have a label-11 lower arc margin of 5.123e-13 (sine) against HULLW_11. Is the absolute tan-half lower end 1430271/5000000 of HULLW_11 the literal of every PSW37 / PSSW37 file that was actually executed? I compared only the files named in SELECTED_ORIGINAL_MAP.json by hash.

