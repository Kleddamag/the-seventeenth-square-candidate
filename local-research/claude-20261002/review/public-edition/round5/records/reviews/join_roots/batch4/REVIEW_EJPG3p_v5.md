Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line.

# Review of `RECORD_EJPG3p_v5.md`, statement (E_JPG3p, v5) (batch 4, 2026-10-10)

Reviewer: a reviewer of the window side that wrote none of the record, of the certificate, of the
checkers or of the earlier tools. Text reviewed: the copy in
`reviews/join_roots/batch4/as_reviewed/`, sha256 5bf850e033fa6603e1884e2dcfe2299c0c205d6cd08e67de3ba1dd358d4fe4a1;
the record on disk still had this hash at 13:02. Paths are relative to `research/window-extension-20261008/`.

## Verdict

**PROVED: yes.** No number, no hash and no claim of the record is wrong: 200 checks by three programs
(131 + 15 + 54), none failed. Three texts change together with the status (findings 1 to 3); none of them
corrects a number. Nothing was found that touches all region trees.

## Findings, sorted by weight

### 1. Status line: with PROVED it must carry the limits sentence

- The record says: "ACCEPTED ... NOT YET PROVED: this record has not been reviewed".
- I found: the limits sentence of the v5 records (batch 3, finding 1) applies unchanged, with
  `reviews/join_roots/batch4/v_regions.out` as the file and 22 as the number of `0` steps: the soundness of
  SPEC 3.0 and of the two frozen checkers is taken from their own reviews, and with it the exact values L of the
  22 `0` steps (compared across the producer's and the acceptance reports of both programs, not recomputed);
  nobody but the producer has read how the leaves were made; it is a statement about the numbers of the region
  file, not about a case of the proof; outside label 11 the region file is the reviewed v2 file, for label 11 the
  factor contains the v2 factor, PB_11 and HULLW_11; the v5 generator and `cmp_v5.py` are not reviewed.
- Correction asked: put that sentence into the status line when the word changes.

### 2. "What the statement is used for", last point: "not reviewed by a helper" is no longer true

- I checked (`v_regions.py`, 54 checks): `JPG3p_exact_v5.json` (c4287958...) against `JPG3p_exact_v2.json`
  (230da863..., the file of the reviewed v2 record and of the tree batch 2 read; the hash stands in the text
  reviewed in `reviews/join_roots/REVIEW_JOIN_ROOTS_V2.md`): side interval, box and arc of the sixteen labels
  other than 11 are equal; label 11 of v5 contains label 11 of v2 (upper end of xi_1 from 31221/200000 to
  12647/62500, lower arc end from -0.099999886 to -0.137499811, the four other ends are the v2 numbers) and is the
  same data as in the five other v5 files; by my own transport the v5 factor of label 11 contains the old target
  PB_11 (room 6.3e-7 in the box) and the new target HULLW_11 (room 9.5e-7 in the box, 5.1e-13 rad below, 7.2e-11
  rad above), and the v2 factor does not contain HULLW_11. `JPG3p` and `JPG3m` (v2 and v5) are the same data in
  every label other than 3; label 3 has the same box in both, and its two arcs are exact mirror images.
- Correction asked: replace "not reviewed by a helper" by the words of `acceptance/usedfor_JPG15p_v5.txt`:
  "the reviewer of this record compared the v5 file with its reviewed v2 file, equal outside label 11, and
  checked that the factor of label 11 contains the v2 factor, PB_11 and HULLW_11,
  `reviews/join_roots/batch4/v_regions.out`; the v5 generator and `cmp_v5.py` are not reviewed".
- Nothing else in the section is overstated. It is `acceptance/usedfor_JPG3p_v5.txt` character for character,
  and apart from the names and one new clause it is the section of the reviewed record of JPG3m v5. The new
  clause of the second point is right: `bigbox/join/RECORD_EJPG3p_v2.md` (0bd5fa4e..., file time 08:21) has the
  one status line "STATUS: PROVED (2026-10-10 08:21) as a statement about the numbers of the region file" and
  the title "... ACCEPTED 2026-10-10 03:06, PROVED 08:21". The targets named for k = 3 are confirmed (PB_j the
  same data in PT_j, PM_j, PS_j^3, PSS_j^3 for the twelve rigid labels; HULLW_11 the same in PTW37_L11,
  PSW37_L11_T03, PSSW37_L11_T03). Third point: every leaf has the tag JPG3pv5 and the v5 factor of label 11.

### 3. Section "Review": replace "NOT REVIEWED" by a pointer to this file

### 4. What is particular to this tree: remarks, no change needed

- (a) The same tree as on the v2 root. Node for node (36) the v5 tree has the closure kind, the cut (label and
  tan-half), the pair, the list of options in the same order and the assumption list of the reviewed v2 tree
  (batch 2's node data of `JPG3p.cert.jsonl.gz`). The 14 split nodes and the 22 leaf nodes have, outside label
  11, exactly the box and arcs of their partners; label 11 of every node contains its partner's. The leaves are
  new: no file hash and no L of the v2 record's table recurs; 15 of 22 have another number of terms.
- (b) The nested split. `n5aad634dc2` (assumes nothing) splits the pair (8, 17) into 8:17:b:m, 17:8:a:p,
  17:8:b:p; the five omitted options are excluded with margins 0.5741 to 2.1812. Its child for 8:17:b:m,
  `n7f09731f47`, cuts the direction of label 17 at tan-half 563/2500, strictly inside its arc; the lower piece is
  a leaf, the upper piece `n968c694e5b` splits the pair (12, 15). All three assume exactly [8:17:b:m]; the four
  children of the split assume [8:17:b:m, their option]. The four omitted options (12:15:a:m, 12:15:b:m,
  15:12:a:p, 15:12:b:p) are excluded on that node's own box and arcs of the labels 12 and 15 with margins 0.8477
  to 1.5084; the test does not use the assumption (labels 8 and 17 do not occur in it), so it holds with it all
  the more. The node has no round, and both checkers' final store hash of it is the hash of its own S, box and
  arcs with no cut and no relative arc (recomputed). No node assumes two options of one pair.
- (c) The pair (12, 15), three times. Where label 15 is below its gate (`n4bc180a2b1`) the list is 12:15:a:p,
  12:15:b:p, 15:12:a:p, 15:12:b:m; in the two cells where label 15 is above its gate (`nec47cfa3e4`, nested
  `n968c694e5b`) it has 15:12:a:m for 15:12:a:p. Each list passes the test: the omitted 15:12:a:m is excluded
  with margin 0.7508 in the first cell, the omitted 15:12:a:p with 0.8477 in the others, the other omitted
  options with 1.36 to 1.58. Pair (14, 17): listed 14:17:a:p, 17:14:a:m; the six omitted are excluded with
  0.1302 to 1.8631. No listed option would be excluded; all values are those of the v2 tree. A float sampling of
  the five nodes (64 corners, 3000 points each) finds no point at which an omitted option holds.
- (d) Nodes beyond the root. "21 of the 36 nodes" is right. All 21 are leaves, 36 arcs in all, labels 15 and 17
  only: label 15 by 4.334e-6 rad (7 leaves below, 12 above); label 17 by 4.334e-6 (9 below, 4 above) and by
  5.260e-6 above (the four leaves under the nested split). Nothing exceeds 1e-5 rad; these are the amounts of
  the reviewed v2 tree. No node exceeds the root in a box interval; every leaf has the root's box. The one leaf
  inside the root is `pH11W37G33pwu.n0`. The list of the facts output equals mine (nodes, labels, amounts).
- (e) "label 3 ABOVE its gate, [+0.099917, +0.786228]": the arc runs from 9.3e-10 rad below rot(1/20) to exactly
  rot(4147/10000), so it includes the gate's end (the larger side), as in the reviewed records. Labels 4, 15 and
  17 are exactly rot(-4147/10000) to rot(4147/10000), a quarter turn and more.
- (f) The certificate file has two directory entries (a hard link); the bytes read at 12:56 have the size and
  hashes of the record, and the producer's runs (`run.json`: `--keep-going`) and both acceptance reports name them.

## Confirmed

`t_tree.py JPG3p v5 JPG3p_v5 RECORD_EJPG3p_v5.md` (batch 3's program; one line changed, additions marked
"batch 4"; 131 checks, output `t_JPG3p_v5.out`), the certificate read line by line (37 lines, 22 over 2 MB):
- size, sha256 and stream hash of the certificate; all 59 different hash strings of the record explained
  (statement file, log, C1, C2, facts output, description, `run.json`, the three frozen files, `hull_tree.py`,
  44 in the leaf table); header: schema, 17 labels, Sref = S_floor, packing hash, window = the statement file's;
- counts from my own reading, equal to the record, C1, C2 and the assembler report: 36 nodes, depth 7, 14 splits
  (9 arc, 0 box, 5 option), 22 leaves, no terminal node (the statement file demands 0), 22 steps, 988,844 terms,
  832 declarations; every leaf has one round with one `0` step of positive value;
- tree conditions; root node = region file (side interval, 68 box ends, 51 rotations); the root contains the
  header window; the tree = the producer's description; no `recentre`; every split node has the root's centres;
- the cuts as the record words them, each strictly inside its node's arc: label 15 at tan-half -1/20 (root) and
  1/20; label 17 at -1/20 and 1/20 (3 times each) and 563/2500 (once); nothing else is cut; label 11 never cut,
  with the root's box and arc in all 36 nodes;
- the child test for all 35 edges; the 13 split nodes below the root are exactly their pieces; the 22 leaves
  are larger than their pieces, in the arcs of the labels 15 and 17 only;
- both acceptance reports: PASS, the certificate's hashes, every node accepted, closure kinds and line numbers
  as in the file, final store hashes recomputed for 36 of 36 nodes in each program's format; the producer's two
  reports agree with them node by node (closure, store hash, evidence, L);
- the table of leaves: all 22 rows equal my rows (leaf, file hash, terms from my count, L to seven places,
  sha256 of L, options in the node's order); L the same string in C1, C2 and the assembler report, its hash in
  `run.json`; all positive, the smallest 1.927617e-3 at `pH11W37Gmppwu.n0.0`; every leaf "contains";
- the log: every hash against the disk, default options, exit codes 0 of both checkers and of the report,
  RESULT: ACCEPTED once, the lines that carry the statement, start 12:32:38, both times and sizes, file time
  12:46:36; "the region in words", number by number (labels 9, 3, 17, 15, 4, 11).

`t_more.py JPG3p v5` (new, 15 checks, output `t_more_JPG3p_v5.out`; works from the node data the run above wrote;
tried first on batch 2's v2 node data): remarks a to c. `v_regions.py` (batch 3's program; C and D for k = 3 and
the JPG3p files, E on JPG3m and JPG3p, part F new; 54 checks, output `v_regions.out`): finding 2 and remark e.

## Limits

Not checked by me: the two frozen checkers and the acceptance script were not rerun, so the
arithmetic of the 22 `0` steps is the checkers', and so is the test that a leaf's round uses only options its
node assumes (832 declarations, counted only); the leaf files (only their hashes as the producer's reports give
them); how the leaves, the description and the certificate were made, and what "second-tree" means beyond the
tag and the factor of label 11; `cmp_v5.py`, the v5 generator, `ADMISSION_v4.md`; the capture side and the
composition; the exit code of the acceptance run itself (the log has those of the checkers and of the report).
SPEC 3.0, `mk_record.py` and `region_facts.py` were not read: the child test, the exclusion test and the library
are the earlier reviewers' code, which I read once and ran; my float sampling uses the same frame, so it is a
second look at the bounds, not at the conventions. The v2 tree is batch 2's file `t_JPG3p_v2_nodes.json`
(fa123a6d...), not read again from its certificate. Taken from earlier reviews: as in batch 2.

How the work was done: one run on the certificate, through
`proto30/out/contain/run.sh` with the tag `rev4_JPG3p_v5` (60 s, 345 MB) and explicit arguments; standard library,
exact comparisons with fractions.

    3e129bd40491f0b7...  t_tree.py     8153d01a3b55854e...  t_more.py     385815cb88a3ea0d...  v_regions.py
    1ecc5cea24fa7c50...  rjlib.py (copy)                    18e26dc7d0f90354...  t_JPG3p_v5.out
    0bc3dcf4fd2f39b1...  t_more_JPG3p_v5.out                bd4cbf65e0cc40ac...  v_regions.out
