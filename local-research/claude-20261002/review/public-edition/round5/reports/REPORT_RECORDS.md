Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line.

HOLDS WITH CONDITIONS. Each of the eleven records derives its claim from one accepted single-file tree on its own root, plus SPEC 3.0 and the two frozen checkers. No record rests on a carried tree, a containment, a symmetry or a lemma of its own. Conditions: (C1) soundness of SPEC 3.0 and of the checkers cf8db52b / 97210adf, which I read only in sections 2, 6, 7, 8, 11 and the two corollary notes; (C2) the saved checker runs themselves, which I did not rerun (another reviewer does); (C3) for JG only, the step from "in the tube G20S" to "S = S*" is THEOREM G20S plus a frame step of the composition, outside the record.

All eleven records were read in full by eye, except the leaf-table rows of JPW13 (163 rows, lines 76 to 243) and JPA (281 rows, lines 81 to 361). Those I read by script only, with only the first and last rows by eye.

FINDINGS, most serious first

1. No finding of class (iii). JUDGEMENT: no sentence in any of the eleven records leaves a condition open for the record's own claim.

2. LOW, wording, RECORD_EJPWS_v4.md line 52: "label 11 in B_11 of the slab statement (a rectangle inside HULL_11's positions, HULL_11's arc)". For the region boxes this is true: label 11's box of JPWS v4 lies inside its box of JPWS v2x (exact, my regions.py). PROOF_TEXT.md of the packet says the literal class polygon B11 of SL_L11_T020_DH has one rounded vertex about 3.7e-8 outside HULL11 and that no inclusion in HULL11 is used. JUDGEMENT: the parenthesis is loose for the class polygons and harmless for the record's claim, which names the file. I did not check the class files.

3. LOW, stale wording in every record: "its class statements, which are not certified" (for example RECORD_EJPG17m_v5.md lines 25-26, RECORD_EJG_v2.md lines 26-27 and 167-168, RECORD_EJQ_v1.md lines 13-14 "the sixteen class certificates Q_j ... which do not exist"). True at the time of writing, class (i). RECEIPT_ROSTER.tsv of the packet has 114 rows, all COUNTED.

4. NOTE, RECORD_EJPWS_v4.md line 62 and RECORD_EJPA_v5.md line 63: the acceptance run read the producer's work file under a scratch path, not the file of record. Identity rests on sha256. I confirmed that the file of record on disk has the compressed hash and the uncompressed-stream hash the log names, for both. JUDGEMENT: no gap.

5. NOTE: for JPWS v4, JPW13 v2x, JPG3p v5 and JPG15m v5 the packet (H6_PREMISES rows 202, 203, 205, 208) pins both an early LEAD_RECORD_SNAPSHOT and the final record. The snapshot hashes (38f1160b, 7ff9ee9c, 5bf850e0, 473ec02e) are the "as_reviewed" texts the records name. The final record hashes are the eleven of record. I did not compare snapshot against final text.

(1) TABLE (ids as in H6_PREMISES.json rows 199 to 209)

| id | verdict | relied on |
|---|---|---|
| LOCAL_JQ | CONDITION (C1, C2) | RECORD_EJQ_v1.md whole; rec_check.py |
| LOCAL_JG | CONDITION (C1, C2, C3) | RECORD_EJG_v2.md whole; rec_check.py, leaf_tables.py, regions.py |
| LOCAL_JPA | CONDITION (C1, C2) | RECORD_EJPA_v5.md, table rows by script; all four scripts |
| LOCAL_JPWS | CONDITION (C1, C2) | RECORD_EJPWS_v4.md whole; scripts |
| LOCAL_JPW13 | CONDITION (C1, C2) | RECORD_EJPW13_v2x.md, table rows by script; scripts |
| LOCAL_JPG3m, JPG3p, JPG17m, JPG17p, JPG15m, JPG15p | CONDITION (C1, C2) | each v5 record whole; scripts |

(2) RESTATEMENT AND CHECKS, common to all eleven

- Given: 17 closed unit squares, pairwise disjoint interiors, in [0,S]^2 with S <= Sref = 4675530093604551/10^15, container corner at the origin, any labelling 1 to 17, one of the four side directions a_i chosen per square. Coordinates xi_ik from upper-packing-certificate.json (24e296f5...).
- Claim (ten records): NOT (every xi_ik in the closed interval of the region file's window.box and every a_i in the closed root_arc). Claim (JG): if in the region, then in the tube.
- Region files: each record names the file and hash of the JOIN_ROOTS.md table (lines 106 to 118); I rehashed all eleven. Each region file has S = [Sref, Sref]. Its `statement_if_a_complete_tree_is_accepted` reads "EMPTY: no feasible configuration (seventeen squares, side Sref) lies in the root region" for ten and "TUBE: ... sixteen squares other than 4 in the window G20S" for JG.
- Side range: the tree proves the statement for S = Sref; the record extends it to S <= Sref by SPEC 3.0 section 11 (squares in [0,S]^2 lie in [0,Sref]^2; box and arcs do not mention S). JUDGEMENT: correct.
- Frame: the region files' `frame` entry speaks of the endpoint frame; the records state the claim for any configuration with the corner at the origin. JUDGEMENT: the record's form is the stronger one; reading a packing in the endpoint frame is the composition's matter.
- Derivation: emptiness corollary (SPEC_v3.0_NOTES.md lines 80 to 97) or root-region corollary (lines 36 to 49). I read both proofs against SPEC sections 2, 6, 7. JUDGEMENT: both are correct as induction over the tree, given the checker enforces sections 5 to 7.
- Root node against region file, my own exact comparison for all eleven: parent null, empty assumption list, S equal, 68 box ends equal, 51 rotations (centre and both ends, both components) equal. Header window box and alpha, and header terminal, equal the region file's.
- Counts, from my own streaming read of each certificate (no step evaluated): node count, leaf count, terminal count and split counts by type equal the record and the log for all eleven. Ids are unique, there is one parentless node (the header's root), every children list equals the set of nodes naming that parent, all nodes are reachable, and every node has S = [Sref, Sref].
- Logs: each has exactly one "RESULT: ACCEPTED", no line starting with FAIL, no "not ok". Each has the lines "root node: parent is null", "empty assumption list", side, box and arc equal to the region's, and "the statement of this record is made for the ROOT REGION of '<file of record>'". The ten emptiness logs have "ok number of terminal leaves is 0 (expected 0)"; JG has "number of terminal leaves: 1 (not fixed by the statement)". Each log names cf8db52bfa1cc565, 97210adf74a3ebed, h_report30.py 0314aa1f8f742cd7 and both certificate hashes. Log hashes equal the records'.
- Leaf tables, all eleven by script: row ids equal the certificate's infeasible node ids; "options assumed" equals the node's assumption list in order; L equals zero_step_L of the Python report to the printed digits; "L sha256" is the hash of that fraction string; L is the same rational in both reports and positive. Every node is accepted in both reports, with the same ids and closure kinds as in the certificate file. Smallest L equals the record's in each.
- Assembly (point 5): every certificate of record is one .jsonl.gz file with one hash, and that file is what both checkers accepted node by node. JUDGEMENT: the assembly needs no trust. Leaf files, helper files and the assembler are not premises.

PER RECORD

JQ v1 (d27d6d9b). Statement: JQ_exact_v1.json (f4d1607e) is empty for S <= Sref. Premises: one-node certificate 0b2a8ff8, log d04fa0f0, EXPECT cbd56dcb, SPEC and checkers. (c)-items: none for the claim. Lines 62-64 say the design hands JQ v2, which lies in JQ v1; I checked this exactly (only label 9's upper end of xi_2 differs, -124437/1000000 against -104437/1000000, v2 inside). The packet pins JQ v1. Open wording: lines 13-14 and 65-69, class (i), capture side. Counts 1 / 1 / 0: yes.

JG v2 (947f9ffb). Statement: every configuration in JG_exact_v2.json (f635af68) has, for the sixteen labels other than 4, xi in [-1/5, 1/5] (xi_21 in [-39/125, 0], xi_13,2 in [-1/5, 28/125]) and |phi_i| <= 1/10 rad. This equals THEOREM_G20S.md section 2 (read by me) and the region file's `terminal`. Label 4's tube factor is its root box with radius 1, no condition (root arc 0.786228 rad < 1; tube box of 4 equals root box, exact). Premises: certificate e7587199 with 113 nodes, 56 leaves, 1 terminal leaf td0f7ae2afe; log 4a005651; SPEC section 8 terminal test (599/6000 = 1/10 - 1/6000, exact).
(c)-item: two leaves made on a helper window reach 2.006e-2 rad below the root in label 13 (lines 155 to 166; LEAF_HELPERS.md 6c0775b4, read lines 1 to 60). Argument: SPEC section 6 asks of a child only that it contains its piece, and F(child) is defined by its own data. JUDGEMENT: complete and correct; a leaf on a larger node proves more. The helper file is not a premise: the certificate is one file, both helper leaves are children of ne99e545db0 in it and accepted by both reports. I did not recompute the child test for them.
Open wording: lines 19-20 "the composition ... is not proved" and 152-154 "S0 = S* is a further step of the composition ... not proved here", class (i); the packet's LOCAL_CERTIFICATE_IMPORT says "Physical G20S is subsequently applied at actual L", not followed by me. Lines 167-170, class (i). Counts: yes.

JPG17m v5 (ae527a87), JPG17p v5 (0054d9b1), JPG3m v5 (493e9122), JPG3p v5 (16226ebd), JPG15p v5 (8ce55c18), JPG15m v5 (33b20db1). Statement: JPG<x>_exact_v5.json (18550e41, 11b68ec1, 1e2a3b42, c4287958, 6c9ad488, f6495dc6) is empty for S <= Sref. Premises: certificates 68613d84 (31/18), f392b6ba (48/32), 75357350 (36/22), 804ae794 (36/22), 1adb3864 (23/15), ed66c59b (61/39), their logs, SPEC and checkers.
(c)-items: none load-bearing. No carried tree: each record says "The tree consists of second-tree leaves made on the v5 root only", every leaf id ends in "...v5.leaf", and the v5 root differs from the v2 file in label 11 (control 3). The old records RECORD_EJPG17m_v2.md and RECORD_EJPG3p_v2.md are named for form only; I did not read them. "The v5 region contains the region v2" is a side remark; I checked it exactly for all six: equal outside label 11, and label 11 of v5 (xi_1 in [-140801/1000000, 12647/62500], arc [-0.137499811, +0.204999690] rad) contains v2's.
"The region in words": the gates, the "above" and "below" arcs, label 9's support end -9897/1000000 and the "any direction" arcs match the files (tan-half 4147/10000, (tau+1)^2 >= 2 exact).
Open wording: "It serves the branch if the capture side certifies ..." (for example JPG17m lines 98-101) and "NOT contained" (lines 105-110), class (i). "the v5 generator and cmp_v5.py are not reviewed" (line 20), class (i): region file against class files. Counts: yes for all six.

JPWS v4 (af742507). Statement: JPWS_exact_v4.json (7d32a55b) is empty for S <= Sref. Premises: certificate 538a6a51 (110/70), log 78f713f7, SPEC and checkers.
(c)-items: none load-bearing. Replacement leaf (lines 170-175): "a solver setting and not part of the certificate"; all 110 nodes have S = [Sref, Sref] (my read) and the leaf is accepted in both reports; JUDGEMENT correct. "The region lies inside JPWS_exact_v2x.json" (line 176): exact, only label 11's box differs, v4 inside.
Open wording: line 184 "PW_2 and PW_6 have the status RECEIPT OPEN", class (i), both COUNTED in the roster. Line 241 FRAME_MARKER, class (i), COUNTED in the roster. Line 238 "THE COMPOSITION MUST TAKE SL11_T020 FOR LABEL 11 IN THE SLAB", class (ii): PROOF_TEXT.md says SL11_T020 gives the B11 occupant in the middle wall branch and that the reviewer of premise D checks its direct admission to JPWS_v4; the roster has SL11_T020 COUNTED. Lines 185-187 "not reviewed by a helper", class (i). Counts: yes.

JPW13 v2x (0f7d2cb3). Statement: JPW13_exact_v2x.json (e1a489e1) is empty for S <= Sref. Premises: certificate 7147d778 (255/163), log 8465744d, SPEC and checkers.
(c)-items: none load-bearing. "The region lies inside JPW_exact_v2.json" (line 258): exact, one end differs. The seam sentence (lines 252-255) concerns which capture statement applies at y = 13/5; the region takes the end closed (label 9 xi_2 from -52219/500000 = -104438/1000000, and JPWS ends at -104437/1000000, so the two overlap).
Open wording: line 266 "PW_2, PW_6, PW_7 and PW_8 have the status RECEIPT OPEN", class (i), all four COUNTED in the roster. Counts: yes.

JPA v5 (e10be786). Statement: JPA_exact_v5.json (adcf0d1b) is empty for S <= Sref. Premises: certificate b9f92839 (416/281), log 7b9b9eaa, SPEC and checkers.
(c)-items: none load-bearing. Lines 384-389, the clause 591183/1408817 <= t9 <= 44941/100000 lies in the root's arc of label 9: I recomputed exactly from the region file and the packing file. The absolute tan-half of the root arc is [0.419630795796869, 0.913966453374868]; the clause is inside, with room 8.2185e-10 below and 0.464556 above. Relative to the reference the arc is [+0.0999006227, +0.7862284215] rad; xi_(9,1) starts at -87219/500000. v5 contains JPA v1 = v2 (exact, only label 11 differs).
Open wording: lines 371-373, label 16 "PS_16^9 ENDa ... not checked here", class (i): PROOF_TEXT.md says PS16/9 ENDa on JPA is activated through the independent S6 review; not verified by me. Lines 401-402 FRAME_MARKER, class (i), COUNTED. Line 404 "the root obligation of JPA itself is RECEIPT OPEN there (it waits for this record)", class (ii): H6_PREMISES row 201 LOCAL_JPA is COUNTED with this record's hash. Line 459, class (i). Lines 462-463, label 9 below its gate is in no proved region and is excluded by KEY_W alone: class (i), KEY_W is COUNTED in the roster; the use is the composition's. Counts: yes.

(3) SCRIPTS (in <reviewer scratch>/) and controls

- rec_check.py: hashes, logs, one streaming pass per certificate, root against region. Outputs rec_check_*.out, run_all.stdout, nodes_<name>.json.
- leaf_tables.py: leaf tables against certificate nodes and both reports. No problems in any of the eleven.
- regions.py: exact containments and the quoted region numbers.
- neg_controls.py: all on scratch copies in memory. A region copy with one box end moved by 1e-6 is flagged; with one arc end replaced is flagged; the v5 certificate root against the v2 region file is flagged in label 11; a record row with one L digit and one option changed is flagged in both.
- I ran no checker, so I have no control of the checkers themselves.

(4) SHA256 (first 16) of files relied on

Records, region files, certificates and logs: as listed per record above; all rehashed by me and equal to the records, the JOIN_ROOTS table and H6_PREMISES rows 199 to 209. Certificates were also checked by uncompressed stream. Others: SPEC_v3.0.md 0a6dfc2ae10ed6f3; SPEC_v3.0_NOTES.md 4f8d1e8fa5d20bea; LEAF_HELPERS.md 6c0775b4d48198f0; THEOREM_G20S.md ed64ff7ec8aef6ed; EXPECT files cbd56dcb (JQ), 363ff3a6 (JG), a76bfcad (JPA), 4450804d, 8d4ac066, cbf1d4e9, b6b3ba8d, c8000b86, 9c202c8e, a0ddbc0f (JPWS), b6a33b67 (JPW13). The C1 / C2 reports were read, not hashed by me.

(5) NOT READ

- SPEC 3.0 outside sections 2, 6, 7, 8 and the opening of 11; both checkers' code; h_report30.py; accept_tree30.sh.
- Any `0` step or polynomial arithmetic; the child and exclusion tests were not recomputed.
- REVIEW_JOIN_ROOTS_V2.md and the batch reviews 2 to 7 (no (c)-item needed them).
- LEAF_FORMAT_RULING.md; LEAF_HELPERS.md after line 60.
- RECORD_EJPG17m_v2.md, RECORD_EJPG3p_v2.md, the as_reviewed snapshots, ADMISSION_v4.md, cmp_v5.py.
- The region files against the class files; the support end of label 9; the wall lemma; KEY_W; the composition.
- JOIN_ROOTS.md beyond line 164.
- THEOREM_G20S.md beyond section 3.
- In the packet: only H6_PREMISES rows 10 and 199 to 209, the roster rows named, and two sentences of PROOF_TEXT.

(6) QUESTIONS TO THE AUTHORS

1. JG: THEOREM G20S speaks of "the frame and labelling above" (THEOREM.md section 1), and SPEC_v3.0_NOTES lines 61 to 76 require a translation by (eps, eps) for a tube clipped at xi_{2,1} <= 0. Which final premise carries the frame in which (T_JG) hands a packing to G20S at the actual side L?
2. JPWS: should line 52's "a rectangle inside HULL_11's positions" be read as a statement about the region boxes only, given the 3.7e-8 remark in PROOF_TEXT?
3. For the four roots with two pinned record texts, is the final record (af742507, 0f7d2cb3, 16226ebd, 33b20db1) the one the proof cites?

