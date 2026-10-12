Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line.

# Review of `RECORD_EJPG15m_v5.md`, statement (E_JPG15m, v5) (batch 3, 2026-10-10)

Reviewer: a reviewer of the window side that wrote none of the record, of the certificate, of the
checkers or of the tools. Text reviewed: the copy in
`reviews/join_roots/batch3/as_reviewed/`, sha256 473ec02ea7e28d54c03794027d9e9cb5a98fffeece122b7962ddf9d098876ace;
the record on disk still had this hash at 10:14. Paths are relative to `research/window-extension-20261008/`.

## Verdict

**PROVED: yes.** No number, no hash and no claim of the record is wrong: 172 checks in two script runs, none
failed. Three texts change together with the status (findings 1 to 3); none of them corrects a number.
Nothing was found that touches all region trees.

## Findings, sorted by weight

### 1. Status line: with PROVED it must carry the limits sentence

- The record says: "ACCEPTED ... NOT YET PROVED: this record has not been reviewed".
- I found: the limits sentence of batch 2's finding 4 for the v5 records applies unchanged, with
  `reviews/join_roots/batch3/v_regions.out` in the place of `batch2/v_regions.out`: the soundness of SPEC 3.0 and
  of the two frozen checkers is taken from their own reviews, and with it the exact values L of the 39 `0` steps
  (compared across the producer's and the acceptance reports of both programs, not recomputed); nobody but the
  producer has read how the leaves were made; it is a statement about the numbers of the region file, not about
  a case of the proof; outside label 11 the region file is the reviewed v2 file, for label 11 the factor
  contains the v2 factor, PB_11 and HULLW_11; the v5 generator and `cmp_v5.py` are not reviewed.
- Correction asked: put that sentence into the status line when the word changes.

### 2. "What the statement is used for", last point: "not reviewed by a helper" is no longer true

- I checked (`v_regions.py`, 40 checks): `JPG15m_exact_v5.json` (f6495dc6...) against `JPG15m_exact_v2.json`
  (f1d215af..., one of the thirteen region files of `reviews/join_roots/REVIEW_JOIN_ROOTS_V2.md`: the hash stands
  in the text reviewed there and that review's `recompute_v2.out` lists the region): side interval, box and arc of the sixteen labels other than 11 are equal; label 11
  of v5 contains label 11 of v2 and is the same data as in the five other v5 files; by my own transport the v5
  factor of label 11 contains the old target PB_11 (room 6.3e-7 in the box) and the new target HULLW_11 (room
  9.5e-7 in the box, 5.1e-13 rad below, 7.2e-11 rad above), and the v2 factor does not contain HULLW_11. New
  here: `JPG15m` and `JPG15p` (v2 and v5) are the same data in every label other than 15; label 15 has the same
  box in both, and its two arcs are exact mirror images.
- Correction asked: replace "not reviewed by a helper" by the words of `acceptance/usedfor_JPG15p_v5.txt`:
  "the reviewer of this record compared the v5 file with its reviewed v2 file, equal outside label 11, and
  checked that the factor of label 11 contains the v2 factor, PB_11 and HULLW_11,
  `reviews/join_roots/batch3/v_regions.out`; the v5 generator and `cmp_v5.py` are not reviewed".
  The rest of the section is, name for name, the text of the reviewed record of JPG15p v5; nothing in it is
  overstated. The targets it names for k = 15 are confirmed (PB_j the same data in PT_j, PM_j, PS_j^15, PSS_j^15
  for the twelve rigid labels; HULLW_11 the same in PTW37_L11, PSW37_L11_T15, PSSW37_L11_T15).

### 3. Section "Review": replace "NOT REVIEWED" by a pointer to this file

### 4. Remarks, no change needed

- (a) Nodes beyond the root. "37 of the 61 nodes" is right. All 37 are leaves, 85 arcs in all, by 4.673e-6 to
  7.204e-6 rad: label 4 by 5.361e-6 (6 leaves at each end); label 14 by 6.784e-6 below (16) and 5.589e-6 above
  (8); label 15 by 4.673e-6 below (32) and 6.112e-6 above (the one leaf without an option, which so reaches into
  the gate); label 16 by 6.899e-6 below (8) and 7.204e-6 above (8). Nothing exceeds 1e-5 rad; the largest is a
  little above the 6.5e-6 of the earlier trees. No node exceeds the root in a box interval. The two leaves inside
  the root are `pH11W37G313wk5k5.n0.0` and `.n0.1`. The list of the facts output equals mine (nodes, labels,
  amounts).
- (b) "label 15 BELOW its gate, [-0.786228, -0.099917]": the arc runs from exactly rot(-4147/10000) to 9.3e-10 rad
  above rot(-1/20), so it includes the gate's end (the larger side), as in the reviewed records.
- (c) "582 MB" is 611,303,424 bytes cut down, not rounded (582.98 in binary units).
- (d) The producer's two checker runs read a copy under `<scratch>/` (the file in the assembly folder is dated
  09:39, after them); both reports name the sha256 and the stream hash of the file on disk, so "the frozen
  checkers have run on these bytes twice" is right. `run.json` shows the option `--keep-going`.

## Confirmed

`t_tree.py JPG15m v5 JPG15m_v5 RECORD_EJPG15m_v5.md` (batch 2's program with additions marked "batch 3";
132 checks, output `t_JPG15m_v5.out`), the certificate read line by line (62 lines, 39 of them longer than 2 MB):
- size, sha256 and stream hash of the certificate; all 93 hash strings of the record explained (statement file,
  log, C1, C2, facts output, description, `run.json`, the three frozen files, `hull_tree.py`, leaf table);
- header: schema, 17 labels, Sref = S_floor, packing hash; header window = the statement file's;
- counts from my own reading, equal to the record, C1, C2 and the assembler report: 61 nodes, depth 7, 22 splits
  (11 arc, 0 box, 11 option), 39 leaves, no terminal node (the statement file demands 0), 39 steps, 1,453,516
  terms, 1443 declarations; every leaf has one round with one `0` step of positive value;
- tree conditions; root node = region file (side interval, 68 box ends, 51 rotations); the root contains the
  header window; the tree = the producer's description; no `recentre`;
- the cuts as the record words them, each strictly inside its node's arc: label 15 at tan-half -1341/5000 (root)
  and -659/5000; label 4 at -659/5000 (twice), 0 (once), 659/5000 (twice); label 14 at 1/20 (twice); label 16 at
  -1/25 (twice); nothing else is cut;
- the child test for all 60 edges: all pass; the 21 split nodes below the root are exactly their pieces; the 39
  leaves are larger than their pieces, in arcs only;
- the 11 option splits, each on a node with an empty assumption list (no nesting; a leaf assumes at most one
  option). Pair (12, 15), eight times: listed 12:15:a:p, 12:15:b:p, 15:12:a:p, 15:12:b:m; the four omitted
  options (12:15:a:m, 12:15:b:m, 15:12:a:m, 15:12:b:p) are excluded on the node's own data with margins 1.2002 to
  1.5197. Pair (14, 17), three times: listed 14:17:a:p, 17:14:a:m; the six omitted are excluded with margins
  0.1302 to 1.8631. The test would exclude no listed option;
- label 11 never cut, with the root's box and arc in all 61 nodes; every split node has the root's centres;
- both acceptance reports: PASS, the certificate's hashes, every node accepted, closure kinds and line numbers
  as in the file, final store hashes recomputed for 61 of 61 nodes in each program's format; the producer's two
  reports agree with them node by node (closure, store hash, evidence, L);
- the table of leaves: all 39 rows equal my rows (leaf, file hash, terms from my count, L to seven places,
  sha256 of L, option, order); L the same string in C1, C2 and the assembler report, its hash in `run.json`;
  all positive, the smallest 2.831597e-3 at `pH11W37G323wur.n0`; the terms add up; every leaf "contains";
- the log: every hash against the disk, default options, exit codes 0, RESULT: ACCEPTED once, the lines that
  carry the statement, start 09:42:46, the two times and sizes, file time 10:01:06;
- "the region in words", number by number: label 9 (arc and the end -9897/1000000), labels 3 and 17 exactly
  rot(-1/20) to rot(1/20), label 15 (remark b), label 4 exactly rot(-4147/10000) to rot(4147/10000), the numbers
  of label 11. Apart from the clause on label 15 and the corrected words on label 11 the paragraph is the one
  of the reviewed record of JPG15p v5. The corrected words on label 11 ("one box and one arc that contain ...")
  are right.

`v_regions.py` (batch 2's program; JPG15m added, part E new; 40 checks, output `v_regions.out`): finding 2.

## Limits

Not checked by me: the two frozen checkers and the acceptance script were not rerun, so the
arithmetic of the 39 `0` steps is the checkers'; the leaf files (only their hashes as the producer's reports
give them); how the leaves, the description and the certificate were made, and what "second-tree" means beyond
this: every leaf has the tag JPG15mv5 and the v5 factor of label 11; `cmp_v5.py`, the v5 generator,
`ADMISSION_v4.md` ("2,552" stands in its line 210, not recounted); nothing of the capture side or of the
composition. SPEC 3.0 was not read again: the child test, the exclusion test and the library are the earlier
reviewers' code, which I read once and ran; `mk_record.py` and `region_facts.py` were not read
again (every number of this record was compared with mine). Taken from earlier reviews: as in batch 2.

How the work was done: the run on the certificate went through
`proto30/out/contain/run.sh` with the tag `rev3_JPG15m_v5` (89 s, 424 MB), started once with explicit arguments;
standard library, exact comparisons with fractions.

    f629a449175e5a1b...  t_tree.py      c3a9d0829312bd44...  v_regions.py     1ecc5cea24fa7c50...  rjlib.py (copy)
    771d22ffbcb2e385...  t_JPG15m_v5.out                     3eec1ec5161fa91c...  v_regions.out
