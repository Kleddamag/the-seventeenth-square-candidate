Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line. This report reviewed the earlier executions of the capture computation, named here by neutral designations (table EARLIER_EXECUTIONS.tsv); the audit of the execution carried in this edition and the complete row comparison with the earlier ones are separate evidence.

HOLDS WITH CONDITIONS: (c1) the four FRAME rows hold only for the symmetrised classes (orbit / mirror_x); (c2) 92 executions ran on alias bytes of the pinned class file, not the pinned bytes; (c3) FRAME_MARKER's execution binds to the class literal aa8b1410..., not to the row pin marker.json 520ce3ce...; (c4) C_7 and C_8 have no execution; (c5) the receipts are internally consistent records, and I re-executed only 4 rows.

FINDINGS, most serious first

F1 (condition c1). The symmetry images are load-bearing in the four FRAME rows.
- With the unchanged checker modules and inputs, but the image list forced to identity only, rows 4500 and 4501 FAIL in both examples.
  - FRAME_MARKER: the cells that leave the class fall to the default level with least charge 941559390, below the required 998328901.
  - FRAME_0506: least default charge 875870071, below the required 999025212.
- So the certified statement is true only for "listed slots united with their D4 images" (FRAME_MARKER) or "united with their images under x -> 2*c_x - x" (FRAME_0506, FRAME_1114, FRAME_0917).
- JUDGEMENT: a consumer reading those class files as fixed regions would over-claim. The manifest wording "in this file's frame and symmetry interpretation" is sufficient if FRAME_ASSIGNMENT uses exactly that reading; I did not read FRAME_ASSIGNMENT.
- The other 94 executed rows are symmetry "fixed", with no reduction.

F2 (condition c2). 92 of 98 executions ran on class bytes whose sha256 differs from the manifest pin.
- I compared classes.json byte for byte against both claimed alias forms built from the pin file.
- 90 rows are exactly "pin without its final newline": every Q_*, PW_*, L_*, C_* that has a folder, SL11_T020, and all 47 PS/PSS/PSW37/PSSW37 rows.
- 2 rows are exactly json.dumps(parsed pin):
  - CLASS_PS_L06_T17_ENDm_H4T4: pin fea1d9752281aa0b -> classes d27d6258c5bfcb5b.
  - CLASS_PS_L06_T17_ENDp_H4T4: pin 7072785dd92ff4c2 -> classes 8c4870ddca35cac2.
- No row has any other difference.
- Six rows have classes.json byte-equal to a pin: FRAME_0506, FRAME_1114, FRAME_0917, E07A, KEY_W equal the row pin; FRAME_MARKER equals the class_literal pin (see F3).
- JUDGEMENT: both alias forms parse to the same JSON value, and both checkers act on the parsed value only, so the certified statement is the same.

F3 (condition c3). FRAME_MARKER's row pin is the old marker literal marker.json (520ce3ce...), which is not the executed file.
- The executed class file (aa8b1410906ddac7) equals class_equivalence_binding.class_literal.
- The equivalence of the two literals is a separate claim (CONVERSION.md) that I did not read.

F4 (condition c5). What the receipts can and cannot show.
- The merged receipts carry only minima and cell sums.
- A self-consistent edit of one non-extremal row figure in one slice (control A) is caught only because the Python and Node rows then disagree; an identical edit in both slice files would pass every receipt-level test.
- This matches the packet's own sentence "Merge consistency is not slice authenticity."
- My re-execution covers rows 4500 and 4501 of two folders with both checkers; all four runs equal the stored rows.

F5. Both merge routines accept overlapping slices if the duplicated rows agree (exact_classes.py lines 584-587; verify_classes_wb.js mergeSlices). I tested for overlap separately: none in any of the 98 folders.

F6. The Node receipts record the repaired checker under the key name "verify_classes.js" although the file is verify_classes_wb.js. The key is a hard-coded label and the hash is of the running file (7f6b2347...). JUDGEMENT: harmless but confusing.

F7. Python's checker_sha256() hashes the source files on disk when the header is written, not the code already imported (lines 518-519).
- The repaired Node checker hashes at load and re-checks before writing (lines 988-990, 1209).
- JUDGEMENT: a small asymmetry in binding strength, not a gap for stored receipts.

F8. The FRAME_0506 certificate carries an extra top-level key "classes" (and "source"). Neither checker restricts top-level certificate keys. JUDGEMENT: harmless, since the classes used are those of the --classes file whose sha256 is recorded.

F9. For 21 rows a second folder with a repaired-Node PASS receipt for the same class bytes exists (the second executions of those rows), not listed in the roster. For each of these rows the claimed final folder is among the folders my search found. I did not check the second folders.

(1) TABLE
"HOLDS" means every part-(I) test passed for the folder of record, including all slices and all rows of both implementations. The folders are those of the earlier executions. Columns: id | verdict | execution | symmetry | bound | rows | surplus | alias (nl = pin without final newline; dumps = json.dumps of parsed pin; "-" = bytes equal a pin).

FRAME_MARKER | CONDITION c1,c3 | first execution of FRAME_MARKER | orbit | 17 | 9000 | 13 | - (equals class_literal)
FRAME_0506 | CONDITION c1 | second execution of FRAME_0506 | mirror_x | 137/8 | 9000 | 31/2 | -
FRAME_1114 | CONDITION c1 | second execution of FRAME_1114 | mirror_x | 137/8 | 9000 | 1/2 | -
FRAME_0917 | CONDITION c1 | second execution of FRAME_0917 | mirror_x | 145/8 | 9000 | 61/4 | -
E07A | HOLDS | first execution of E07A with the repaired Node checker | fixed | 20 | 18000 | 6 | -
KEY_W | HOLDS | first execution of KEY_W | fixed | 20 | 18000 | 12 | -
C_7 | NOT READ (derived; no folder; no execution of its class file 60341809... exists under results/) | - | - | 20 | - | - | -
C_8 | NOT READ (derived; no folder; no execution of its class file exists under results/) | - | - | 20 | - | - | -

All remaining rows: HOLDS, fixed, 18000 rows, alias nl unless marked dumps.

- Q rows, bound 23, first execution of Q_nn (Q_11: first execution of Q_11 with the repaired Node checker). Surplus: Q_1 18, Q_2 17, Q_3 12, Q_4 18, Q_5 15, Q_6 1, Q_7 1, Q_8 3, Q_10 15, Q_11 11, Q_12 8, Q_13 23, Q_14 11, Q_15 13, Q_16 1, Q_17 16.
- PW rows, bound 23, first execution of PW_nn (PW_11: first execution of PW_11 with the repaired Node checker). Surplus: PW_1 4, PW_2 9, PW_5 9, PW_6 1, PW_7 7, PW_8 19, PW_10 7, PW_11 8, PW_12 14, PW_13 9, PW_14 20, PW_16 16.
- L rows, bound 20, first execution of L_nn. Surplus: L_3 8, L_4 12, L_15 8, L_17 4.
- C rows, bound 20, first execution of C_nn with the repaired Node checker for C_1, C_5, C_6, C_10, C_11, C_12, C_13, C_14; first execution of C_nn for C_2, C_16. Surplus: C_1 10, C_2 9, C_5 10, C_6 4, C_10 1, C_11 5, C_12 10, C_13 9, C_14 18, C_16 19.
- SL11_T020 (slab), bound 23, first execution of SL11_T020, surplus 12.
- CLASS_PSS_Lnn_T03, bound 23, first execution of CLASS_PSS_Lnn_T03. Surplus: L01 11, L02 15, L05 17, L06 10, L07 13, L08 4, L10 7, L12 5, L13 11, L14 9, L16 10. CLASS_PSSW37_L11_T03 (first execution of CLASS_PSSW37_L11_T03) 11.
- CLASS_PSS_Lnn_T15, bound 23, first execution of CLASS_PSS_Lnn_T15. Surplus: L01 21, L02 1, L05 12, L06 21, L07 7, L08 4, L10 14, L12 10, L13 15, L14 10, L16 7. CLASS_PSSW37_L11_T15 (first execution of CLASS_PSSW37_L11_T15) 23.
- CLASS_PS_Lnn_T09, bound 23, first execution of CLASS_PS_Lnn_T09. Surplus: L01 2, L02 12, L05 17, L06 18, L07 5, L08 17, L10 4, L12 22, L13 11, L14 15, L16 23. CLASS_PSW37_L11_T09 (first execution of CLASS_PSW37_L11_T09) 2.
- CLASS_PS_Lnn_T17, bound 23, first execution of CLASS_PS_Lnn_T17. Surplus: L01 8, L02 21, L05 17, L07 14, L08 3, L10 18, L12 15, L13 9, L14 1, L16 22. CLASS_PSW37_L11_T17 (first execution of CLASS_PSW37_L11_T17) 2.
- CLASS_PS_L06_T17_ENDm_H4T4, bound 23, first execution of CLASS_PS_L06_T17_ENDm_H4T4, surplus 1, alias dumps.
- CLASS_PS_L06_T17_ENDp_H4T4, bound 23, first execution of CLASS_PS_L06_T17_ENDp_H4T4, surplus 6, alias dumps.

Totals: 98 rows with a folder passed every test; 2 derived; 0 mismatches. All 98 surpluses equal the RECEIPT_ROSTER.tsv column.

CHARGE_SEMANTICS (only as far as part II touches it) | HOLDS for these sub-claims; the rest NOT READ.
- Single side and centre: computed for all 98 (L/A = 4675531/1000000; frame centre (1169/500, 1169/500)).
- Printed statement = class file + certificate ratio: computed for all 98 (see test 2 below).
- "Only the centre-polygon symmetries declared by the literal file are included": source reading (Python lines 313, 359-371; Node lines 606, 791-830) and the experiments in (3).
- High-first ordering: source reading (Python lines 318-319, 458-467; Node order / pieces loop).
- JUDGEMENT: the high-first score is >= the printed tau for every pose, so the printed statement follows from what is checked.

(2) HAND-OVERS RESTATED

Receipt statement (all 98).
- Given: certificate bytes (sha in receipt), class-file bytes (sha in receipt), checker sources (sha in receipt).
- Claimed: for every family of closed unit squares with pairwise disjoint interiors inside the square of side exactly 4675531/1000000, in the frame with container centre (1169/500, 1169/500), the sum of tau(pose) is strictly less than the bound.
- Class = listed slots (closed convex centre polygon x closed tan-half-angle gate, all quarter-turn lifts), united with images per the symmetry field.
- Strictness comes from one exact integer inequality, budget_units*q_b < p_b*minimum_units, and weak per-cell inequalities charge*q >= p*minimum_units.
- Surplus formula, inferred then confirmed at exact_classes.py line 526: surplus = bound*required_units - budget_units, as an exact rational. Strictly positive is equivalent to the strict budget inequality.
- The side range S <= C is NOT in the receipt; it is the separate concentric-inclusion argument of CHARGE_SEMANTICS, which I did not check.

Symmetry "orbit" (FRAME_MARKER).
- Checker requires: certificate in orbit shape; every point orbit is expanded to its full D4 orbit with one weight; every threshold orbit's listed sets must be exactly one complete D4 orbit of the first set (Python expand: "incomplete trigger orbit"; Node buildSymmetric).
- It then skips all rows beyond the folded range: rows chain from u=0 to a cursor with cursor^2+2*cursor>1 (theta from 0 to beyond pi/4), instead of u=1.
- It duplicates each slot into 8 images; reflections use the angle interval (-b, -a).

Symmetry "mirror_x" (FRAME_0506, FRAME_1114, FRAME_0917).
- Checker requires: fixed-image certificate; check_mirror / checkMirrorInvariance verify on the feature list that the mirror x -> L-x of every site of every feature is a site and that each feature's mirror image carries the same total weight (unrecognised form = refusal).
- Rows folded as for orbit; images = identity and D4[5] = x -> -x about the frame centre.
- Charge mirror and class mirror are the same axis through the container centre (LD-x in certificate units; 2*c_x-x in the frame).

Validity (JUDGEMENT, my own argument).
- Every pose has angle mod pi/2 in [0, pi/4] or its mirror image does.
- The container is symmetric.
- The charge is invariant (verified by the checker, not assumed).
- The class is closed under the image set by definition: the checker tests "some image g of the cell lies in / meets a slot", and both image sets are groups, so this is the union of the slot images.
- Hence charge(p) = charge(m p) >= R(m p)*minimum >= psi(m p)*minimum = psi(p)*minimum, where the core used for p is the mirror of the core used for m p. The capacity bound does not depend on which sub-square is chosen.
- The reduction is valid for the symmetrised class and for nothing smaller (F1).

Python versus Node: same reduction — same image sets, same sign rule for the angle interval, same edge forms, same folded-range test, same refusals.
- Only difference found: Python requires the listed orbit sets to be literally in canonical order; Node canonicalises before comparing. Python is the stricter of the two.

Parser.
- Python strict_json: duplicate keys, NaN/Infinity refused; float tokens become non-numbers and are refused anywhere in the class file; rationals only as "p" or "p/q" strings (ASCII, fullmatch); exact key sets; polygons 3..64 vertices, strictly convex, counter-clockwise; -1 < lo <= hi < 1.
- Node parseJsonExact is a hand-written parser with the same rules (integers to BigInt, duplicate keys refused, trailing characters refused, anchored regexes).
- Difference: Node decodes invalid UTF-8 leniently, Python refuses. JUDGEMENT: irrelevant for stored files, which both parse.

Slice binding.
- Python: input bytes are read once, hashed and parsed from the same buffer; workers are forked after parsing and never re-read files; the slice header carries certificate sha, class sha, five checker hashes, total rows, start/end; each row carries its index.
- Python merge recomputes the header from the files on its command line and drops any slice differing in any header key, with wrong range, wrong row indices, or status inconsistent with row flags.
- Node: workers are child processes that re-read the files by path. The repair (validateWorkerSlice, 19 added lines) makes the parent refuse a child whose header (input hashes, checker hash), range, row indices, status, statement or totals differ from its own.
- I read the diff between verify_classes.js (72b92624...) and verify_classes_wb.js (7f6b2347...): it is exactly this plus the load-time checker hash.

(3) SCRIPTS, RESULTS, CONTROLS
All under <reviewer scratch>/.

check_receipts.py (my own; reads the roster and final-folder list only as the claim). Run: 40 s, 176 MB. Outputs deep.txt and deep.json.

Folder discovery: I indexed every folder under results/ holding a receipt, by classes_sha256, and matched against the manifest pin sha and its two alias shas. For all 98 rows the claimed final folder is among the folders found. C_7 and C_8: no folder anywhere runs their class file.

Tests, all passed for 98/98:
1. Both receipts exist. Status: PASS_CLASSES_EXACT_COVER in all 196 receipts, the only status met; slices are PASS_CLASSES_INTERVAL_PARTITION_ONLY. start 0, end = total = number of certificate entries; missing 0; failed []; problems [].
2. Statement contains the side and centre; the full statement string equals my reconstruction from the stored classes.json and certificate L/A, character for character; the two receipts agree on every header field.
3. bound, required_units, budget_units equal certificate.json, classes.json and the manifest bound; surplus recomputed with exact fractions equals both receipts and the roster, and is > 0.
4. sha256(certificate.json) and sha256(classes.json) equal both receipts; manifest pin files exist with the pinned sha; pin versus class bytes as in F2; roster python/node/certificate/classes sha columns equal the files.
5. Python receipts carry exactly the five frozen hashes (exact_classes.py 802dc62a..., exact_restricted.py caae39b3..., exact_general.py 89954c6c..., integer_sweep.py 3a2bfd88..., boolean_rule.py c49d38ac...). Every Node receipt of record carries 7f6b2347...; rows whose Node receipt of record is from another checker hash: none.
   - The 14 historical folders with 72b92624... (old folders of FRAME_0506/1114/0917, E07A, Q_11, PW_11, C_1, C_5, C_6, C_10, C_11, C_12, C_13, C_14) are not the folders of record.
6. Slices, for ALL 98 folders rather than a sample: 12 Python + 12 Node slices each (6 + 6 for the three second executions of FRAME_0506, FRAME_1114 and FRAME_0917); merged_files equals that count.
   - Ranges partition [0, total) with no gap and no overlap; row indices contiguous; every slice header equals the merged receipt in all 11 header fields.
   - Every row is re-decided by me from its own figures with exact integers (default: least charge >= required; class with threshold p/q: least*q >= p*required; cells add up; row minimum = least over parts).
   - Minimum over rows, default cells/minimum and per-class cells/minimum are recomputed and equal the merged receipt; Python rows equal Node rows field for field; every compare file says agree "yes".
   - Rows covered: 1,728,000 per implementation. This includes the first execution of CLASS_PS_L05_T17, the first execution of CLASS_PS_L01_T17 and the three second executions of FRAME_0506, FRAME_1114 and FRAME_0917. The only stray files are the marker file and the job file of the slice 9 of the first execution of CLASS_PS_L01_T17, computed on the build machine.

bind_check.py: for all 98 rows, some proof file pinned in the manifest row (sha verified) contains the sha256 of the folder-of-record's receipt_python.json and of receipt_node.json. My lookup into H6_PREMISES.json did not match the file's shape, so that file was not checked.

Negative controls for check_receipts.py, on scratch copies of the second execution of FRAME_1114:
- clean copy: 0 mismatches.
- A, one row's minimum_units +1 in one Python slice (self-consistent): flagged "python and node rows differ at 1 rows (first [4000])".
- B, last hex digit of certificate_sha256 in receipt_node.json changed: flagged (receipts differ; not the stored certificate; 6 Node slices differ in header).
- C, one slice pair removed: flagged (rows [4500,6000) MISSING; merged minimum 876496763 versus recomputed 876496780; cell totals differ).
- D, a slice duplicated under another name: flagged OVERLAPS.
- E, row 100 set below the requirement in both slices: flagged "row 100 does not pass my re-decision" plus merged default minimum mismatch.

Checker experiments: checker copies in scratch chk/ with hashes verified equal to the bundle; Python from local-research/claude-20261002/.venv; rows 4500 and 4501.
- M0 / P0, unchanged inputs: Python and Node rows equal the stored rows of record for the first execution of FRAME_MARKER and the second execution of FRAME_0506.
- M1 orbit -> fixed and M2 orbit -> mirror_x: both checkers refuse ("needs the fixed-image shape (no point_orbits / threshold_orbits)").
- P1 mirror_x -> fixed: both refuse ("rows of a fixed-image certificate must end exactly at u = 1").
- P2 mirror_x -> orbit: both refuse ("needs the symmetric shape (no sites / features)").
- M3 (marker slot replaced by its quarter-turn image), M4 (by its mirror image, gate negated), P3 (both P0506 slots replaced by mirror images): all row figures identical to the stored rows in both checkers. The checker treats the class as the symmetrised set.
- P4, one feature weight +1 with budget adjusted: both refuse with the mirror-invariance message for feature 0.
- M5, one of 8 sets removed from a threshold orbit with budget adjusted: Python "incomplete trigger orbit"; Node "sets are not one complete D4 orbit".
- Identity-only images (my driver driver_images.py on the unchanged Python modules, and a one-line patched scratch copy of the Node file named PATCHED_identity_only.js): both rows fail in both examples, with identical figures in Python and Node.
  - Marker class cells drop from 164366688 to 41091672 in row 4500 (exactly one quarter: the slot is mirror-symmetric, so 4 distinct images).
  - P0506 class T_side-W0 cells drop from 157904833 to 75657225; deficit 875870071.


(4) SHA256, first 16 hex digits
- PACKET.json 99d813ec5d1ffd1a
- THEOREM_MANIFEST.json 49a2443699a03620 (equals the pin inside SELECTED_ORIGINAL_MAP.json)
- SELECTED_ORIGINAL_MAP.json 63943cf07fd93323
- H6_COVERAGE.tsv 9e9884091d5f8bed
- RECEIPT_ROSTER.tsv b8dbc710126b066e
- FINAL_EXECUTION_FOLDERS.txt 841a6ef2e1d0e3cb
- The five files above have their full sha present in PACKET.json.
- PROOF_TEXT.md b42fa1670b11643a; H6_HANDOFF.md d229a1629e5596e7 (only the CHARGE_SEMANTICS paragraph and one line of PROOF_TEXT read)
- Bundle cert_restricted: exact_classes.py 802dc62aa4f2a9e1; exact_restricted.py caae39b30cfcde51; exact_general.py 89954c6c44e1368b; integer_sweep.py 3a2bfd8892a9693b; boolean_rule.py c49d38ac96027b34; node/verify_classes_wb.js 7f6b234768f812b7; node/verify_classes.js 72b92624de356507 (diff only)
- first execution of FRAME_MARKER: certificate.json 4f6fd3419ed52352; classes.json aa8b1410906ddac7
- second execution of FRAME_0506: certificate.json f1bcf8c5e8c9bae3; classes.json 0dc3b61bfe065089
- second execution of FRAME_1114 (control source): receipt_python.json 1d90faad499b78c2; receipt_node.json 92f1593bb5c9f7c7
- Per-row receipt, certificate and class hashes: computed by the script and equal to the RECEIPT_ROSTER.tsv columns for all 98 final rows.
- check_receipts.py as run for the final result: 8ce09572d0a3a182

(5) NOT READ / NOT DONE
- Whether the slice rows were really produced by the checkers, beyond 2 rows x 2 folders x 2 checkers; no SAVED_PROVENANCE audit content was read (only searched for hashes).
- The equivalence marker.json <-> FRAME_MARKER_CLASS.json; the C7/C8 transfer; FRAME_ASSIGNMENT's use of the symmetric statements.
- CHARGE_SEMANTICS beyond the points listed: side range S <= C; the capacity and core argument (only as far as needed for the symmetry argument); row validation inequalities ("core not strict", "parent envelope"); the sweep and tree arithmetic in geometry() / integer_sweep.py; accumulate_levels and the Node sweep (lines 752-905 not read line by line); _slot_interval / _blocked_interval correctness (read, not tested independently); Node buildFixed and ruleOf (lines 270-361, 429-460).
- The 14 historical folders and the 21 folders of second executions (indexed only).
- H6_PREMISES.json per-row pins; RECEIPT_ROSTER.json; MANIFEST_TABLES.md; the review reports pinned under CHARGE_SEMANTICS (REPORT_A_charge.md, REPORT_CHARGE_SEMANTICS.md, HIGH_FIRST_REVIEW.md, the worker-binding review), so I state no agreement or disagreement with them.
- No race test of the Node worker binding (code reading only).
- The three COUNTED but unselected statements (CLASS_PS_L01_T17_ENDm_H4T4, CLASS_PS_L05_T17_ENDp_H4T4, CLASS_PS_L16_T09_ENDa_H4T4) are not among the 100 and were not checked.

(6) QUESTIONS TO THE AUTHORS
1. FRAME_0506 / FRAME_1114 / FRAME_0917: does FRAME_ASSIGNMENT use the classes as "slots united with their mirror images" (e.g. T_side-W0 = west strip and its east mirror image, threshold 7/8)? The identity-only run shows the fixed reading is not certified.
2. FRAME_MARKER: the row pin is marker.json 520ce3ce... but the execution is for aa8b1410.... Is the row's exact_statement ("this file's ... symmetry interpretation") meant for marker.json or for the class literal? Which review carries the equivalence?
3. Why do 90 executions use the pin without its final newline and 2 use json.dumps of it, instead of the pinned bytes? Is the alias rule stated once in the packet as a premise (parsed-value equality), or only audited per row?
4. Are the 21 folders of second executions meant as independent replications? They are not in the roster; should they be, or should the packet say they are unused?
5. The Node receipts name the checker "verify_classes.js" with the hash of verify_classes_wb.js. Is there a packet sentence that fixes this naming, so that a reader does not look for 7f6b2347... under the wrong filename?
6. Python records checker hashes from disk at header time rather than from the loaded modules. Was any Python slice produced while the sources on that machine could change? The Node repair closes this; Python has no equivalent.

