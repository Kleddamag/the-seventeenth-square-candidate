Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line.

# Review of `RECORD_EJPW13_v2x.md`: statement (E_JPW13, v2x), batch 5

Reviewer: a reviewer that wrote none of the record, the certificate, the checkers or the tools; 2026-10-10.
Record as reviewed: `as_reviewed/RECORD_EJPW13_v2x.md` (254 lines), sha256 7ff9ee9ceaae5474...e2e3b057d5.

## Verdict
**PROVED after corrections.** One correction, C1, in the section on use. The Statement, the corollary paragraph,
"The region in words", the status paragraph, the Evidence table and the leaf table stand as they are: I found no
wrong number in them. The statement itself (a statement about the numbers of the region file) does not depend on C1.

## Correction asked
**C1** (record lines 234 and 235; the text comes from `acceptance/usedfor_JPW13_v2x.txt`). Old text (two lines,
each with the record's two leading blanks):

      that place the loose labels 3, 4, 15, 17 in their loose slots (premise note of the region file: they apply
      because the wall column holds one centre, so no other square lies in A_Q). The factor of label 9 rests on the

New text:

      that place the loose labels 3, 4, 15, 17 in their loose slots (premise note of the region file: for y > 13/5 they
      apply, because the label-9 square is then outside A_Q and the wall column holds one centre, so no square lies in
      A_Q; at y = 13/5 itself the square is in A_Q and they are not used: the slab branch takes that position, next
      item; the region takes the end y = 13/5 closed, a superset). The factor of label 9 rests on the

Reason: the branch is named with "y >= 13/5", and the old sentence says for it that the family L statements apply. At
y = 13/5 they do not: the L files exempt "a square in [-131/250, 53/100] x [24137/10000, 13/5]" (version 1's A_Q,
closed at 13/5; `JOIN_ROOTS.md` 9.4), and there the label-9 square is that square. The region file's premise note says
"y > 13/5" and "The end y = 13/5 is taken closed (a superset)"; Codex's seal says "At y=13/5 use JPWS and its four QB
slots. The upper-wall L deductions are not used at equality." (`<author reply>`, line 3).

Not asked: "the wall case above" (lines 34, 228) can be misread as "named above"; `JOIN_ROOTS.md` says "wall above".

## The run
`proto30/out/contain/run.sh rev5_JPW13_v2x /usr/bin/python3 -B <batch5>/t_tree.py JPW13 v2x JPW13
RECORD_EJPW13_v2x.md` (absolute paths): 562.8 s wall, 560.6 s user, 534.4 MB
largest resident size (`proto30/out/contain/runs.jsonl`), exit 1 because of the one FAIL. Output
`t_JPW13_v2x.out` (sha256 b0b787d458df81de...), node data `t_JPW13_v2x_nodes.json` (c97dd50afc1a2929...).

**125 checks: 124 ok, 1 FAIL. No crash.**
The FAIL: "every one of the 342 different hash strings of the record is the hash (or its first 16 digits) of a file
named above or stands in the leaf table"; the one string left over is `b251fe25e0869879`. My judgement: **not a
defect of the record.** It is the digest of Codex's manifest that the last section quotes "as of 14:34:20", a file
the program does not know (no earlier record quoted it). The live manifest has changed since (15:02:44, sha256
49d7d8ad2ef9adf3...), so the quote cannot be recomputed from it; Codex's own reply `<author reply>`
(line 7) gives the full digest b251fe25e0869879dc28bcb3007fbbe6bed65c6604aa5fb1381aa8e35549c54a for that snapshot.

What the 124 ok lines carry (the earlier reviewers' exact rational code on the certificate's own node data):
- certificate size and both hashes; header = the statement file's (schema, labels, S_floor, window, tube, reference
  file 24e296f5...); root: parent null, no assumption, side [Sref, Sref], box = the region's in all 68 ends, arcs =
  the region's in all 51 rotations; the root contains the header window.
- shape: 255 nodes, all reached from the root, depth 12, 92 splits (43 arc, 0 box, 49 option), 163 leaves each with
  one `0` step of positive value, no terminal node; 7,133,642 terms, 6150 declarations; the eight cut sentences;
  the tree is the producer's description `JPW13.tree.jsonl` node for node.
- each of the 254 children contains its piece (assumptions, side, every box interval, every arc); the 91 split
  nodes below the root are exactly their pieces; all 43 arc cuts lie strictly inside the node's arc (my count of
  the output's lines); in each of the 49 option splits every omitted option is excluded (smallest margin 0.0194).
- place (a) fits: 159 nodes reach beyond the root, every one a leaf, none in a box interval, labels
  3, 4, 15, 17 only, largest excess 5.361e-06 rad; the list equals the facts output's (159 nodes, 354 arcs).
  Place (b) fits: label 11 is never cut and has the root's box and arc in all 255 nodes.
- both acceptance reports: PASS on the certificate on disk, the same 255 ids, lines and closure kinds, every node
  accepted; the node digest recomputed from the file equals both reports for 255 of 255; L is the same rational
  number in both reports, the assembler report and `run.json` for all 163 leaves, positive, smallest 2.900610e-04
  at `pV100w.n0.0.JPW13v2x.leaf`; all 163 rows of the record's table; the hashes of eleven files of the Evidence
  table; the log (RESULT: ACCEPTED once, exit codes 0, default options); the times and sizes of the acceptance run.

**Changes in my copy of `t_tree.py`: none.** It (3e129bd40491f0b7...) and `rjlib.py` (1ecc5cea24fa7c50...) are batch
4's bytes. Its blocks for JPG15m and JPG3p did not run: "The region in words" is not checked by it, I did that by hand.

## Checks by hand (short one-off python with `rjlib`, and reading)
- Corollary: `SPEC_v3.0_NOTES.md`, note of 2026-10-09 18:38 (line 78), says what the record says. Statement file
  b6a33b67...: 17 labels, S_floor = Sref, `terminal_leaves` 0, `root_region` = the region file e1a489e1...
- Label 9, box: the four ends of the record are the file's. By the file's own `info_floats["9"]` the upper end of
  xi_1 is class-frame x = 53/100, the lower end of xi_2 is y = 13/5, the upper end of xi_2 is y = 29637/10000 (the
  top of the wall column; in the record as a number only), the lower end of xi_1 is the wall end (floats only).
- Label 9, arc: centre = conj(u_9) exactly (u_9 = rot(t_9), `squares[8].t` of the reference file), so the centre
  is the x axis exactly; ends rot(-31/1000), rot(31/1000) exactly; from the reference direction -0.7567077436 and
  -0.6327474420 rad, the record's [-0.756708, -0.632747]. Wall lemma's inequality, in integers:
  (1 + 2 tau - tau^2)/(1 + tau^2) = 1061039/1000961 > 53/50 at tau = 31/1000.
- Labels 3, 4, 15, 17: centre the reference direction, ends rot(-4147/10000), rot(4147/10000) exactly: -0.786228
  to +0.786228 rad, 1.572457 in total, more than a quarter turn (1.570796), so "any direction" is right.
- The twelve rigid labels have `position_source` HULL_j of `classes_v2/PW_Ljj.json`, the four loose ones S_j of
  `classes/L_Ljj.json`; `what` and `premise_note` agree with the record. `JOIN_ROOTS.md`: row "wall above" of the
  lower table (line 84, same hash), WALL LEMMA in 2.4, the table and item (b) of 9.3, "DECIDED 17:47" and "JPW13
  is needed under both" in 9.4, lines 101 to 104 for 18:34 and 18:17; Codex's contract holds the region's hash.
- `JPW13_exact_v2x.json` against `JPW_exact_v2.json` (8151e371...): S equal, all 51 arc rotations equal, 67 of the
  68 box ends equal; the one difference is label 9, xi_2, lower end, -52219/500000 against -62219/500000: inside.
- Codex's manifest, live file: the sixteen names have exactly the quoted states (PW_1, 5, 10, 11, 12, 13, 14, 16 and
  L_3, 4, 15, 17 COUNTED; PW_2, 6, 7, 8 RECEIPT OPEN). The file changed after the quote; that is not a defect.
- `REVIEW_JOIN_ROOTS_V2.md` is 9ac387300a880a0f...; its lines 8, 9, 91 and 99 cover the thirteen files and JPW13.
- Overstatement: none besides C1. Status paragraph, Statement and last section say that this is a statement about
  the region's numbers, and that neither capture nor the region file against the class files is checked here.

## Sample of six leaves against the root (step 5)
Leaves pV100w.n0.0, pV550wk5.n0.1.1.0.0, pV155wr.n0.2.3, pV511w.n0.1, pV050w.n0.0.1.1.2, pV550wxh.n0. For each I
followed root -> leaf in `JPW13.tree.jsonl` (depths 6, 12, 7, 5, 11, 12), built the cell (root arcs of 3, 4, 15, 17
cut at the tan-half values of the path; all other arcs, the box and S the root's) and tested with `arc_contains`: all
six leaf nodes contain their cell in all 17 arcs, all 68 box ends and S; every cut lies strictly inside the cell it
cuts; the leaf's assumption list is exactly the list of options on its path, in path order, and the record's row shows
these options. Smallest slack over the four loose labels: 4.63e-06 (sine) in the three leaves of depth 11 and 12, 0 in
the other three.

## Not checked (limits)
- I did not run the two checkers. That each `0` step is valid (7,133,642 terms) and the exact values L rest on
  the two frozen checkers, as recorded in the reports of the lead's acceptance run and of the producer's run; the
  run above ties those reports to the bytes on disk and to each other, it does not redo their arithmetic.
- `t_tree.py` is the earlier reviewers' program. I ran it unchanged and read about 140 of its 961 lines; what its
  ok lines mean rests on its text and on the reviews of batches 3 and 4.
- The region file against the class files; the capture side (PW_j, L_j, the composition of `JOIN_ROOTS.md`
  sections 3 and 9.3, the use of the wall lemma beyond its inequality); `mk_record.py`, `region_facts.py`; the
  manifest beyond the sixteen names; the 157 leaves outside the sample other than through the program.

## What touches other trees or records
- Every record that quotes the manifest digest in its last section (the next wall record, JPWS v4, and others of
  this generator) will give this same FAIL in `t_tree.py` unless the program is told of the snapshot; the quote
  could name Codex's reply that carries the full digest.
- The seam y = 13/5: the record of JPWS v4 should say that the slab branch takes y = 13/5 (C1's other half).
- The region file's entry `what` (and that of `JPW_exact_v2.json`) says "3, 15, 17 any direction" and leaves out
  label 4, whose root arc is the same; a description only, the record's wording is the one that fits `root_arc`.
  The file's hash is pinned by Codex's contract, so I do not ask for a change.
