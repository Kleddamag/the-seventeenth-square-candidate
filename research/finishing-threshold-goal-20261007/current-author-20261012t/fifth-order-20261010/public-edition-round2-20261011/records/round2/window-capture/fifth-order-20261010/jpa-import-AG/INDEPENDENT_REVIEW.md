Editorial copy. Line references refer to the original; exact changes are listed in EDITED_LINES_ROUND2.json.

# Review of `bigbox/join/RECORD_EJPA_v5.md`: statement (E_JPA, v5), case T, kind A (label 9 off the wall column, above its gate)

Reviewer: independent reviewer of batch 7 (wrote none of the files under review); 2026-10-10. Record as reviewed: sha256
a147f8f8bb07f57fd3b9b90a8f454a5cb5fdac4e4e777381c4b879e7ae7773a6, 394 lines (copy in `as_reviewed/`).

## VERDICT: PROVED as it stands
No correction is required. Every number and claim of the record that I could test is right, and nothing overstates; two optional notes are in section 4. The verdict is for the statement as the record
words it: about the numbers of `JPA_exact_v5.json` (adcf0d1b...), resting on the two frozen checkers' acceptance of the certificate, NOT rerun here (section 5).

## 1. The long run: the earlier reviewers' reader
- **Changes in my copy of `t_tree.py`: none.** `t_tree.py` (sha256 3e129bd40491f0b7...) and `rjlib.py` (1ecc5cea24fa7c50...) are byte-identical copies from `batch6/` (`cmp`); one run. Command:
  `out/contain/run.sh rev7_JPA_v5 /usr/bin/python3 -B <batch7>/t_tree.py JPA v5 JPA_v5 RECORD_EJPA_v5.md`; 1099.5 s wall (1083.4 s user), largest resident size 543.4
  MB, peak memory footprint 576.5 MB; exit 1 because of the one FAIL.
- **Result: 126 checks, 125 ok, 1 FAIL.** The FAIL (line 949 of `t_JPA_v5.out`) is the expected one: "every one of the 578 different hash strings of the record is the hash (or its first 16 digits) of
  a file named above or stands in the leaf table". The only string left over (line 948) is d76878ade4f4f58c638bb76ce902373b2e7ced40140db544102cb088f362827e. Judgement: harmless, no defect of the
  record. It is the digest the record quotes for Codex's manifest, a file the program does not know. I hashed the live `THEOREM_MANIFEST.json` at 18:32: exactly this digest (file time 18:12:21,
  339,086 bytes), so the quote was made from the bytes it names. The file was rewritten at 18:34:55 (section 2, manifest).
- The 125 passed checks, from the certificate's own node data in exact rationals: size and both hashes of the certificate; header against statement file and reference file; root node = region file
  (side interval, 68 box ends, 51 rotations); shape (416 nodes: 42 arc splits, 93 option splits, 281 leaves, none terminal; depth 11) and the nine cut sentences; all 415 children contain their pieces,
  the 134 split nodes below the root are exactly their pieces; in each of the 93 option splits every omitted option is excluded on the node's store (the reader's own code); every leaf closed as
  infeasible with one round and a `0` step in both reports; node digests, kinds, line numbers and L against both acceptance and both producer reports; all 281 rows of the leaf table; the Evidence
  table's hashes and numbers; the acceptance log (hashes, RESULT: ACCEPTED once, default options); 278 nodes beyond the root (683 arcs, = the facts output's list), all leaves, by at most 5.870e-06
  rad; label 11 never cut.

## 2. Hand checks (`hand_checks.out`: 54 exact checks of my own passed; its 3 FAIL lines are faults of my script, see the end of section 3)
- **a. Statement and corollary: right.** The paragraph is the EMPTINESS COROLLARY of `SPEC_v3.0_NOTES.md` (note of 2026-10-09 18:38, from line 78) as it stands there: all conditions of section 7 and
  no terminal node give F(root) empty; its last paragraph is the step from S <= Sref to Sref. `EXPECT_JPA_v5.json` (a76bfcad...): `terminal_leaves` is the integer 0, `root_region` names the region
  file with adcf0d1b..., S_floor = Sref, its 34 box intervals are the region's `window.box`. Region file: S = [Sref, Sref], Sref = 4675530093604551/10^15; 51 unit rotations, every arc symmetric about
  its centre.
- **b. "The region in words": right, number by number against the region file.** Label 9: the ends c*lo, c*hi lie at tan-half 567946313691858184003/11360767759702735510000 and 4147/10000 from the
  reference, that is +0.0999006227 and +0.7862284215 rad: "[+0.099901, +0.786228]" (decimals rounded to nearest, not outward). Its box: the lower end of xi_(9,1) is -87219/500000; by the file's frame
  rule (xi = x - (U - S*)/2 - p_9x, U = 1169/250) class-frame x = 53/100 is xi = -0.1744371088552421, and the box end lies below it by less than 1e-6 at both ends of the S* enclosure (exact); the
  other three ends: by the floats of `info_floats` only. Labels 3, 17, 15, 4: centre = reference, ends exactly rot(-4147/10000) and rot(4147/10000), half arc 0.786228422 rad > pi/4 ((1 + t)^2 > 2):
  more than a quarter turn, so "any direction". Label 11: xi_(11,1) in [-140801/1000000, 12647/62500]; direction ends -0.137499810503 and +0.204999690253 rad, the record's nine decimals; by
  `info_floats` its box and arc are the hull of the old root and the new slot, as `JOIN_ROOTS.md` section 11.1 describes it.
- **c. Which arc of label 9 the root file itself covers.** With u_9 = rot(t_9), t_9 = squares[8].t = 0.3620438933... (reference direction at 0.6947275928 rad), the
  ends of `root_arc["9"]` are u_9*c*lo and u_9*c*hi. As tan-half of the ABSOLUTE direction the root covers [0.419630795796869..., 0.913966453374868...] (both exact fractions are in `hand_checks.out`);
  in rad from the reference direction [+0.0999006227, +0.7862284215]; absolute [0.7946282155, 1.4809560144] rad, no wrap.
- **The clause 591183/1408817 <= t9 <= 44941/100000, that is [0.419630796618723..., 0.44941], LIES INSIDE this arc:** both comparisons of the tan-half values hold exactly. Room below: 8.2185e-10 in
  tan-half = 1.3976e-9 rad. Room above: 0.464556 in tan-half = 0.636229668 rad. The record's numbers in its third point on use are right: clause [+0.0999006241, +0.1499987538] rad, root
  [+0.0999006227, +0.7862284215] rad, "1.4e-9 rad of room below, 0.636 rad above". The room below equals the file's own `excess_beyond_the_required_arc_rad` (1.3976e-09), so the clause's lower end is
  the gate end the root file was made from; the clause stands in these words in the manifest (line 971 of the 18:12:21 file). For the books: the root's arc ends at absolute tan-half 0.913966 (0.00083
  rad beyond pi/4 above the reference), not at 1; a clause "t9 < 1" would not lie inside this root, the retained clause does. The record claims only the latter.
- **d. "What the statement is used for": right, each claim against the file it names.** (1) v1 / v2: `JPA_exact_v1.json` and `JPA_exact_v2.json` are one region (S, `window.box`, `root_arc` equal entry
  by entry); v5 equals them in S and in the boxes and arcs of the 16 labels other than 11, and its box and arc of label 11 contain the old ones (4 ends; `arc_contains`, slack 3.7e-2 in sine below, 0
  above). `acceptance/` and `bigbox/join/` hold no acceptance log or record of JPA v1, v2 or v4. (2) The two seams: `JOIN_ROOTS.md` 9.3 item (c) reads as quoted (a square ON x = 53/100 lies in WC,
  PT_j / PM_j say nothing about it, the wall cases take it); its table has for JPA "x >= 53/100, the slot of T9 in the PT files | above / below the gate | nothing beyond the class file".
  `CLASS_FORMAT.md` lines 48, 49, 81: a slot is a closed polygon x a closed tan-half interval, "Closed sets throughout". The 1.4e-9 rad: see c. (3) Amendment A (`JOIN_ROOTS.md` line 29): "REGION JPB
  IS NOT NEEDED; eleven regions remain", KEY_W with [-0.0998905550, +0.1499987538] rad; line 39: JPA needs label 9's direction only up to +0.15 rad. `REVIEW_KEYW_AMENDMENT.md` is the lead's review of
  09:05, verdict "COUNTED, as an implication". (4) "PS_16^9 ENDa ... least margin 1.9e-7": the row stands in the audit lead's `<message file to the author>` (line 233, "FOLLOWS ... | 1.9e-7"). (5)
  `ADMISSION_v4.md`: section 9 is "Tag v5 for case T"; line 210 "Generator: 2,552 exact self-checks, all true"; the region file's own `self_check`: count 2552, all ok. (6) `BATCH_1536.log`: the work
  file's sha256 before and after the run is the named one (1,704,473,363 bytes); acceptance exit 0 at 18:23:44.
- **Codex's manifest**, read at 18:32 from the bytes with the quoted digest d76878ad... (`as_of` 2026-10-10T18:12:21): exactly twelve clauses with roots == ["JPA"], BRANCH_JPA_L01 to L16 for labels 1,
  2, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16, all COUNTED; options PT_j, PS_j_T09, PM_j, for L11 also PTW37_L11 and PSW37_L11_T09, for L16 also CLASS_PS_L16_T09_ENDa_H4T4; base rows L_3, L_4, L_15, L_17,
  KEY_W COUNTED, FRAME_MARKER RECEIPT OPEN; root obligation JPA: RECEIPT OPEN with sha256 adcf0d1b... All as quoted. THE LIVE FILE HAS CHANGED SINCE (not a defect): at 18:34:55 it became
  5e51cbea3a65ffa0... (345,744 bytes); there the twelve clauses, the four L rows and KEY_W are still COUNTED, FRAME_MARKER is now COUNTED, and the root obligation of JPA is still RECEIPT OPEN
  (accepted_by null, read 18:50).
- **e. Overstatement: none found.** Status paragraph, statement and both "NOT contained" points claim a statement about the region's numbers only; the record says itself that the capture side's
  placing of packings and the region file's correctness against the class files are no part of it.

## 3. Step 4: every leaf against the root (my own exact code on `t_JPA_v5_nodes.json`, the reader's dump of the certificate's nodes, and on the producer's description)
- (i) All 416 nodes have the side interval [Sref, Sref]. The root node equals the region file (51 rotations, 68 box ends, no assumption).
- Description = certificate in ids and parents: 135 splits + 281 leaves. Cuts: label 3 at -659/5000 and 659/5000 (1 + 1), label 15 (3 + 3), label 17 (9 + 9), label 9 at 563/2500 (16); no box cut.
  Option splits: (14, 17) 27 (18 with 3 children, 9 with 4), (9, 12) 13, (12, 15) 25, (7, 9) 14, (9, 11) 14 (9 with 3, 5 with 4). Labels 4 and 11 are never cut. All as in the record.
- (ii) For ALL 281 leaves I followed root -> leaf and built the cell: the root's arcs cut at the tan-half values on the path (every cut lies strictly inside the piece it cuts), all else the root's.
  Each leaf node contains its cell in all 17 arcs (`arc_contains`), all 68 box ends and S, and its assumption list is exactly the options on its path, in path order (1 / 2 / 3 / 4 options: 73 / 43 /
  95 / 70 leaves; never two options of one pair). The 135 split nodes have the root's centres and are exactly their cells (34 arc ends, 68 box ends); largest depth 11.
- (iii) Beyond the root: 278 nodes, all leaves, none in a box interval (all 281 leaves have the root's 68 box ends). Nodes per label: 3: 139, 9: 62, 15: 251, 17: 231 (683 arcs); largest excess
  5.870e-06 rad. Label 9: 25 leaves reach below the root arc, each by 5.870e-06 rad, and 37 above, each by 5.260e-06 rad: the lead's facts. Labels 3, 15, 17: at most 5.361e-06 rad. Label 4's arc and
  label 11's box and arc are the root's in all 416 nodes. Leaves larger than the root are admissible (`LEAF_HELPERS.md`, "Added 2026-10-10 08:22: the ruling is reviewed").
- My own slips: part 2 of `hand_checks.out` has three FAIL lines that are faults of MY one-off script, not of the record. Two compared the certificate's option objects {kind, o, t, axis, eps} with the
  description's strings "opt:o:t:axis:p|m" untranslated; a typo in a print stopped the script before its last checks. Part 3 repeats them with eps = +1 / -1 read as p / m (as the reader's `optname`
  does): all ok.

## 4. Optional wording notes (not needed for the verdict)
1. Region in words, to agree with the second point on use (the end is the grid point below, a superset):
   old: `(class-frame x >= 53/100: xi_(9,1) >= -87219/500000)`
   new: `(class-frame x >= 53/100, rounded down to the grid: xi_(9,1) >= -87219/500000)`
2. The manifest quote is right for the snapshot it names and may stay as it is. Only if the lead wants the live state of 18:34:55 instead:
   old: `(as of 2026-10-10 18:12:21, sha256 d76878ade4f4f58c638bb76ce902373b2e7ced40140db544102cb088f362827e)`
   new: `(as of 2026-10-10 18:34:55, sha256 5e51cbea3a65ffa022bd59c34aec99454e0f2cc80be697c7888c70adadb111ba)`
   old (two lines of the record): `L_17 and KEY_W have the status COUNTED; the base row FRAME_MARKER has the` / `status RECEIPT OPEN; the root obligation`
   new: `L_17, KEY_W and FRAME_MARKER have the status COUNTED; the root obligation`

## 5. What I did NOT check (limits)
- The two frozen checkers were not rerun (each has run twice on these bytes). So the 281 `0` steps (12,439,907 terms) and the exact L values rest on their two reports; the reader recomputed the node
  digests of both reports from the file on disk and found the same L in both.
- The region file against the class files (PB_j, the loose slots, T9's slot and its gate end, HULLW_11): outside the record's claim and not checked, except label 9's x end (exact, by the file's frame
  rule) and v5 against v1 = v2. `mk_join_roots_v5.py` and `cmp_v5.py` were not read.
- The capture side: no class statement, certificate or receipt was looked at; of the manifest only the quoted states and the clause's sentence. The audit lead's statement and the join review of 17:32 were
  not read beyond the line named in 2d. The premise of amendment A (KEY_W exact) is the capture side's. The composition (`JOIN_ROOTS.md` sections 3 and 9.3) was read where quoted, not re-proved.
- Of the record I read lines 1 to 48 and 344 to 394; its 281 table rows were compared by the reader only. The certificate was read by the reader's run only (not copied).

## 6. What touches other trees or records
- The manifest is rewritten while records quote it: a quote of its states is right for the digest it names only (here FRAME_MARKER went from RECEIPT OPEN to COUNTED 22 minutes after the snapshot).
- Label 9's directions below its gate are in no proved region (JPB has no tree); they are excluded by the capture side's KEY_W alone (amendment A). This root's own arc ends at absolute tan-half
  0.913966, so it covers nothing above that.
- I looked at no other record or tree.

## 7. Files (all in `reviews/join_roots/batch7/`)
`REVIEW_EJPA_v5.md` (this report), `SHA256SUMS_review.txt`; `as_reviewed/RECORD_EJPA_v5.md` and `as_reviewed/SHA256SUMS_as_reviewed.txt`; `t_tree.py`, `rjlib.py` (copies); `t_JPA_v5.out` (1008 lines),
`t_JPA_v5_nodes.json`; `hand_checks.out`; `run_times.txt`. The runner wrote `proto30/out/contain/rev7_JPA_v5.stdout` and `.stderr`.
