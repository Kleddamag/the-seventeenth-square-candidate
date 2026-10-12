Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line.

# Review of Codex's conditional amendment "KEY_W exact => root JPB and its twelve selector rows are not needed"

Lead of the window side (author of the root files), 2026-10-10 09:05.
I wrote none of the amendment, of the class files or of the class checkers. Reviewed texts:
`research/finishing-threshold-goal-20261007/<author reply>` (sha256 352273f9a2ae1207...) and
`.../window-capture/second-order-20261010/key-w/CONDITIONAL_AMENDMENT.json` (sha256 4253c8a936c81470...).
My exact check: `check_keyw.py` (e4d0e8998481e31f...), output `check_keyw.out` (aaf060aa74c8d7f9...): 55 checks,
none failed; exact fractions, every file read from the disk at its pinned hash.

## Verdict

**COUNTED, as an implication.** The literal numbers of the class file KEY_W suffice: if KEY_W is exact, no
packing in the capture frame has the label-9 square off the wall column with its direction below its gate, so
the root `JPB_exact_v5.json` (2e6b8572...) carries no obligation and its twelve selector rows (labels 1, 2, 5, 6,
7, 8, 10, 11, 12, 13, 14, 16; 96 rows become 84) can go. The JPB root as I defined it does NOT reach anywhere
this gate fails to exclude, except into the wall column, which is the wall branch's obligation and not JPB's
(point 5). Nothing is missing in the argument. Whether the premise holds (the receipts) is Codex's audit, not mine.

## The chain, each link checked against the literal files

1. **Statement of KEY_W** (`cloud/analysis/CLASS_FORMAT.md` section 1, the receipts' own text): for every family of
   unit squares in the container of side 4675531/1000000 (> Sref), frame centre (1169/500, 1169/500), the sum of
   tau is less than 20; tau = 4 on M, 0 on E, 1 elsewhere. M and E are disjoint (least x of the hexagon 537/250,
   largest x of E 4501/5000). Seventeen squares with one in M and none in E give 4 + 16 = 20. So: M occupied
   implies a square in E.
2. **M is the selected half-marker**: equal as JSON to the class M of the pinned `PS_L01_T09.json` and of ten
   more PS_j^9 files (label 12's file has its own M, "half-marker minus target", `JOIN_ROOTS.md` 2.4); same frame, symmetry `fixed`; the
   hexagon is that of the marker object of `FRAME_L9.json`, the interval its `half_marker_tan_interval`.
3. **The occupant is the label-9 square**: every E slot has its centres in L9 = [-131/250, 4501/5000] x
   [24137/10000, 29637/10000] (slot 1 is L9 exactly, slots 2 and 3 are L9 cut at x <= 53/100), and the frame
   lemma has exactly one occupant of L9 in the one D4 image in which the half-marker is occupied (`FRAME_L9.md`
   points 1 to 3: "AQ and T9 predicates contained in it refer to that one physical parent"; so does E). Taken
   from Codex's `FRAME_L9.json` and its independent review (pinned hashes verified, texts not reviewed by me);
   the join design rests on the same statement already (`JOIN_ROOTS.md` section 3).
4. **Off the wall column only slot 1 remains**: tan-half in [30651/100000, 44941/100000] for one side direction.
   T9's direction interval is [-408817/1000000, 61301/200000], and 30651/100000 - 61301/200000 = 1/200000 > 0.
   With ALL quarter-turn lifts: only the lift by minus a quarter turn meets T9, and only in the piece from T9's
   lower end to -55059/144941, which is the component ABOVE the gate. Relative to label 9's reference direction
   (my own transport; equal to Codex's `relative_t_interval` exactly): gate (-0.0998996962, +0.0999006241),
   E slot 1 [-0.0998905550, +0.1499987538]; the upper end is below +3/20 rad (exact bound).
5. **Against the root files**: label 9's arc in `JPB_exact_v5.json` (and v1, v2) is
   [rot(-4147/10000), gate's lower end + 2.41e-9 rad]; its upper end is strictly below E slot 1's lower end, gap
   9.1388e-6 rad, and NO quarter-turn lift of E slot 1's interval meets the arc. So a configuration whose label-9
   square is off the wall column and in E does not lie in the region JPB at all, whichever side direction is
   chosen. What KEY_W does not exclude inside the region JPB: label-9 centres with class-frame x <= 53/100 (the
   root's box reaches 8.9e-7 below 53/100 by its outward rounding; E slots 2 and 3 hold such poses). They are in
   the wall column, where the composition takes the wall branch first (`JOIN_ROOTS.md` 9.3: x <= 53/100, roots JQ,
   JPWS, JPW13, untouched). So they are no obligation of JPB.
6. **The rest of E slot 1 is covered by what stays**: the gate part lies in label 9's gate arc of JG v2 and of
   the six JPG regions (v2 and v5), the part above the gate in the arc of `JPA_exact_v5.json`
   ([gate's upper end - padding, rot(4147/10000)]), and such a pose is in T9, so the JPA rows apply.
7. **Selector**: 96 rows = 8 roots x 12 labels; exactly twelve name JPB, each with roots = [JPB] alone and trigger
   9; they equal the amendment's `removed_clauses` as JSON; the files used by those rows only are the five PSEb
   files it lists.

## Limits and what the contract must carry

- NOT checked by me: the two receipts (seen: both `PASS_CLASSES_EXACT_COVER`, 18,000 intervals, none missing or
  failed, budget 19993906128 < 20 x 999695307, the pinned certificate and class hashes; the audit is Codex's);
  the class checkers; `FRAME_L9.json` and its review; the frame of step 2. The local side proves nothing here.
- KEY_W becomes a BASE PREMISE of the composition: twelve rows go, one exact premise comes (class bc9af7ea...,
  certificate d822e0ea..., both receipts, and the dependency on the unique occupant of L9). The case split then
  reads: label-9 square in the wall column: wall branch; off it: by KEY_W its nearest side direction lies in
  [-0.0998905550, +0.1499987538], so inside its gate (JG, six JPG) or above it (JPA); never below.
- JPA stays, with its rows; so do the six JPG, JG and the three wall roots. (E_JPB, v5) need not be proved; if its
  tree completes all the same it is a true statement that the composition does not use.
- Optional: under KEY_W the branch JPA needs label 9's direction only up to +0.1499987538 rad, not
  up to rot(4147/10000) = +0.786228. A cut root for JPA would be a new region file and a new seal
  (worth it only if open JPA cells lie beyond +0.15).
- The class file's comment says "numbers not agreed with the local side". This review is that agreement for the
  use made here: the wall column x <= 53/100 is the design's own, and the lower end 30651/100000 lies inside the
  gate by 9.14e-6 rad. The upper end +0.15 is beyond the gate, so KEY_W does not make label 9 gated.
