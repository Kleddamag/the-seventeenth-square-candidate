Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line.

# Review of `bigbox/join/RECORD_EJPWS_v4.md`: statement (E_JPWS, v4), the SLAB of the wall case

Reviewer: independent reviewer of batch 6 (wrote none of the files under review); 2026-10-10. Record as reviewed: sha256
38f1160bebfe98400af351484c6e3a7426fcef47d102112720ca86e197fefe3e (copy in `as_reviewed/`).

## VERDICT: PROVED as it stands

No correction is required. Every number and claim of the record that I could test is right, and nothing overstates. Three optional wording notes stand in section 3. The verdict is for the statement as
the record words it: about the numbers of the region file `JPWS_exact_v4.json` (sha256 7d32a55b...), resting on the acceptance of the certificate by the two frozen checkers, which were NOT rerun here
(section 4).

## 1. The long run: the earlier reviewers' reader, unchanged
`t_tree.py` (sha256 3e129bd40491f0b7...) and `rjlib.py` (1ecc5cea24fa7c50...) are byte-identical copies from `batch5/`: NO line was changed. Run: `out/contain/run.sh rev6_JPWS_v4 /usr/bin/python3 -B
<batch6>/t_tree.py JPWS v4 JPWS_v4 RECORD_EJPWS_v4.md`; 211.9 s wall, largest resident size 464.7 MB; exit 1 because of the one FAIL.

**Result: 123 checks, 122 ok, 1 FAIL.** The FAIL (line 360 of `t_JPWS_v4.out`) is the expected one: "every one of the 156 different hash strings of the record is the hash of a file named above or
stands in the leaf table"; left over: `ac06106efd7823b7`. Judgement: harmless, no defect of the record. It is the digest the record quotes for Codex's manifest, a file the program does not know. The
live `THEOREM_MANIFEST.json` has sha256 ac06106efd7823b7ac97a6155d099047390c03a2da37943c3c6c80535046bfc3 (file time 16:44:10, 323,113 bytes: unchanged since the snapshot the record quotes), and this
full digest stands in `<author reply>`, line 7.

The 122 passed checks, from the certificate's own node data in exact rationals: size and both hashes of the certificate; header against statement file and reference file; root node = region file (side
interval, 68 box ends, 51 rotations); shape (110 nodes: 16 arc splits, 24 option splits, 70 leaves, none terminal; depth 8); all 109 children contain their pieces and the 39 split nodes below the root
are exactly their pieces; in each of the 24 option splits every omitted option is excluded on the node's store (SPEC 4.7, own code); every leaf has one round with one `0` step; node digests, kinds,
line numbers and L against both acceptance reports and both producer reports; all 70 rows of the leaf table; the Evidence table's hashes and numbers; the acceptance log (hashes, RESULT: ACCEPTED once,
default options); 67 nodes beyond the root, all leaves, in arcs of labels 3, 15, 17 only, by at most 5.4e-6 rad; label 11 never cut and equal to the root's in all 110 nodes.

## 2. Hand checks (`hand_checks.out`: 39 exact checks of my own with Fractions, 0 FAIL)
**a. Statement and corollary.** The paragraph is the EMPTINESS COROLLARY of `SPEC_v3.0_NOTES.md` (note of 2026-10-09 18:38, from line 78) as it stands there: conditions of section 7 and no terminal
node give F(root) empty; its last paragraph is the step from S <= Sref to Sref. `EXPECT_JPWS_v4.json`: `terminal_leaves` 0, `root_region` = the region file, 7d32a55b...

**b. The region in words**, number by number against the region file:
- Label 9, box: the four ends are the file's. They are the slab x <= 53/100, 129/50 <= y <= 13/5 of the class frame carried over with the file's own constants (xi = c - delta - eta - p_9; delta = (U -
  Sref)/2 exactly, 0 <= eta < 1e-12): -0.174437108855, -0.124437108855, -0.104437108855, each rounded outward to the 1e-6 grid; the left end is the wall end (centre x >= 1/2, i.e. xi >=
  -0.204202155658; grid point below).
- Label 9, arc: centre = conj(u_9), u_9 = rot(t_9) from `upper-packing-certificate.json`: the direction is centred on the x axis exactly; ends rot(-31/1000), rot(31/1000); from the reference direction
  -0.756707744 and -0.632747442 rad = the record's [-0.756708, -0.632747]. Sanity of the wall pose: cos + sin at tan-half 31/1000 is >= 106/100, and the box keeps the centre at x <= 0.529765156 <
  53/100.
- Labels 3, 4, 15, 17: each arc is rot(-4147/10000) to rot(4147/10000) about the reference direction (+-0.786228 rad), and (1 + 4147/10000)^2 >= 2: more than a quarter turn, so "any direction" is
  right. Their boxes and arcs are those of `JQ_exact_v1.json` (the Q-boxes); the eleven other rigid labels have the boxes and arcs of `JPW13_exact_v2x.json`.
- Label 11: box [0.040576, 0.202352] x [-0.153576, -0.002132], inside its box in `JPWS_exact_v2x.json` ([-0.1408, 0.202352] x [-0.153576, 0.140769]) and smaller; its arc is that file's (centre and
  both ends).
- The file's `what` and `info_floats["9"]` (box, arc offsets, tau_half 31/1000, source "the slab of the wall column") agree with the record; for `premise_note` see note N3.

**c. "What the statement is used for".**
- v4 against v2x entry by entry: S, `terminal`, window.alpha, window.centre and root_arc are equal; window.box differs in label 11 only, where v4 lies inside. The folder has no record for v2x ("for
  which no statement is made").
- The seam: `JOIN_ROOTS.md` 9.3 and 9.4 (decided 17:47, repair (2); table: slab -> JPWS, y >= 13/5 -> JPW13) and line 3 of Codex's reply of 9 Oct 18:17 ("At y=13/5 use JPWS and its four QB slots. The
  upper-wall L deductions are not used at equality.") say what the record says. Numbers: JPW13 starts at -52219/500000 = -104438/1000000, 1e-6 below JPWS's upper end, and both boxes hold y = 13/5; at
  the lower seam `JQ_exact_v1.json` reaches -104437/1000000 and holds JPWS's lower end; the three files have the same xi_(9,1) interval and the same arc of label 9.
- Hypotheses: "W from y = 129/50" (PW_j) and "A_Q up to y = 13/5" (loose Q files) are the region file's `premise_note`; "version 1" and "files of record" are `JOIN_ROOTS.md` 9.4 (`classes_v2_Q16/`).
- Dates and files: region file written 9 Oct 22:06:14; `ADMISSION_v4.md` has "made 22:06", the hash 7d32a55b..., the statement file a0ddbc0f..., "Codex sealed the nine v4 hashes at 22:09", the 2,429
  self-checks (= the file's `self_check.count`), `cmp_v4.py`, and Codex's draft "same region end for end".
- Manifest (live file = the snapshot quoted): PW_1, 5, 7, 8, 10, 12, 13, 14, 16 and Q_3, Q_4, Q_15, Q_17 COUNTED; PW_2, PW_6 RECEIPT OPEN; `slab_capture`: id SL11_T020, status COUNTED, root = this
  region file's hash. The sha256 of each of these rows and of the slab file is among the region file's `inputs_sha256`: the states are those of the region's own inputs.
- Acceptance run: the log's first line names the producer's work file (a path in the producer's work folder); `BATCH_1609.log`: sha256 equal to the named one before the run and 538a6a51... after it; exit 0 at 16:46:55.

**d. The replacement leaf** `pUslabs20c945wb1m.n0.JPWSv4.leaf`: its node has S = [Sref, Sref], as have all 110 nodes and the stores of all 70 rounds; it assumes exactly 17:14:a:m and 12:15:b:p; its
table row has L = 1658.4611507. The sentence "a solver setting and not part of the certificate" is right: SPEC 3.0 asks S_lo <= S_floor and S_hi >= Sref at the root and that a child's side interval
contains its piece's (line 564); the `0` step is checked on the node as written.

**Step 5, for all 70 leaves instead of six.** From the producer's description `JPWS_v4.tree.jsonl` alone I walked root -> leaf (every cut strictly inside its node's piece; arc splits: label 3 twice,
15 five times, 17 nine times, only at -659/5000 and 659/5000; option splits: 17 of (14, 17) with 3 or 4 children, 5 of (6, 14) with 2, 2 of (12, 15) with 4), built each cell from the ROOT's data and
tested the leaf's node of the certificate against it: all 70 contain their cell in 17 arcs, 68 box ends and S and assume exactly the options on their path; 67 reach beyond the root (labels 3, 15, 17),
none in a box. Six of the leaves are printed one by one in `hand_checks.out`.

**e. Overstatement:** none. Status line, statement and both "NOT contained" items say that this is a statement about the region's numbers, for the whole root as the file stands, and not about the
capture side or the class files.

## 3. Optional notes (wording only; none changes the statement, none is asked as a correction)
- N1. Status paragraph, "quoted in the last section": the quote stands in the section on use; the last one is "Review".
- N2. "(three pieces per label)" is true of the cut values; a cell need not be cut at both (the cell of the c945 leaves has label 15 in tan-half [-4147/10000, 659/5000] and label 17 uncut). All 70
  cells are closed all the same.
- N3. The record names a hypothesis for PW_j and for the loose Q files, none for the slab statement of label 11; and the region file's `premise_note` does not mention label 11's exception ("PW_j ...
  places the rigid labels in HULL_j"; the file's `what`, `design` and `status` do say B_11). If wanted: "with the target B_11, and for the loose labels" -> "with the target B_11 (hypothesis: a square
  in the slab of the wall column, 129/50 <= y <= 13/5), and for the loose labels". I only READ that field: class `SLAB_label9_wall_column_slab` of `SL_L11_T020_DH.json` (sha256 afde9329..., the
  manifest's) is the polygon [-131/250, 53/100] x [129/50, 13/5], every direction, so the seam y = 13/5 lies in it. Codex's seal of 18:17 is older than tag v4 (it names JPWS v2x); the seam rule itself
  did not change.

## 4. Not checked (limits)
- The two frozen checkers were not rerun. That each of the 70 `0` steps holds on its node (L > 0 exactly; 2,982,299 terms), the closing condition of every leaf, rests on the two checkers'
  acceptance alone: I compared their reports and the log by content and hash and recomputed no step.
- `t_tree.py` and `rjlib.py` are the earlier reviewers' code, run unchanged; I read the header and the functions I used (`arc_contains`, the rotation helpers), not the whole program. The exclusion
  test of the option splits is its, not mine.
- SPEC 3.0, its theorem and the proof of the corollary: read against the record's wording, not reviewed.
- The region file against the class files: not reviewed (the record says so too). My comparisons with JQ v1, JPW13 v2x, JPWS v2x and the class-frame slab are consistency checks. The class statements
  and their states: checked as quotes only.
- The wall lemma and the composition (`JOIN_ROOTS.md` 2.4, 3, 9.3): read, not reviewed.
- The audit lead's account of the replacement leaf (the float solve's interval): not looked up beyond the audit lead's log (line 7986) ("node uncut on a shorter
  side interval: the cell of leaf pUslabs20c945wb1m (+0.01)"). It does not bear on the statement.
- The acceptance run read the producer's work file in the producer's scratch folder, not the file under `results/assembly/JPWS_v4/`; that the bytes are the same rests on sha256 (log line 2, both
  reports, `BATCH_1609.log`, and the file on disk hashed in my run, stream hash included).

## 5. What touches other trees or records
- This statement does not serve a branch that rests on PW_11 with the target HULL_11 (the record says so). The manifest lists PW_11 as COUNTED beside `slab_capture`: the composition must take
  SL11_T020 for label 11 in the slab. The region file's `premise_note`, read alone, suggests PW_11 (N3); the file's hash is sealed, so the remedy is wording elsewhere.
- Seams: the numbers agree with the regions of `RECORD_EJPW13_v2x.md` and `RECORD_EJQ_v1.md`; nothing here changes them.
- Manifest: three of its 50 base rows are RECEIPT OPEN: PW_2 and PW_6 (named by the record) and FRAME_MARKER (not named; whether this branch needs it is the capture side's matter).
- No finding concerns `t_tree.py`, the checkers or another tree.

## Files (in `reviews/join_roots/batch6/`)
`REVIEW_EJPWS_v4.md`; `as_reviewed/` (record and its sha256); `t_tree.py`, `rjlib.py` (copies, unchanged); `t_JPWS_v4.out`, `t_JPWS_v4_nodes.json` (the long run); `hand_checks.out` (output of the
one-off exact checks; their code was not kept as a file); `SHA256SUMS_review.txt`. Outside the folder only what the runner writes (`proto30/out/contain/rev6_JPWS_v4.stdout`,
`.stderr`, one line of `runs.jsonl`).
