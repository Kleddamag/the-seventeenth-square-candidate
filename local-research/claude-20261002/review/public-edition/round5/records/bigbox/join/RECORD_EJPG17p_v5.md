Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line.

# Record: statement (E_JPG17p, v5) for the region JPG17p v5 ("the region JPG17p v5 is empty"): ACCEPTED 2026-10-10 07:19, PROVED 08:21

Lead of the window side. Status words as in `bigbox/THEOREM_G20.md`: COMPUTED / PROVED; ACCEPTED
means: accepted by both frozen checkers in the lead's acceptance run, the record not yet reviewed.

**STATUS: PROVED (2026-10-10 08:21) as a statement about the numbers of the region file** (status words of
`bigbox/THEOREM_G20.md`): the certificate is accepted by both frozen checkers with the lead's post-check (07:19),
and this record is reviewed by a reviewer that wrote none of it, nor the certificate, nor the tools
(`reviews/join_roots/batch2/REVIEW_BATCH2.md`, sha256 25227b662a3e6211..., one review of six records:
117 checks of its own on this certificate and 45 on the region files of the five regions (`v_regions.out`), none failed; its own reader of the certificate, its own
comparison of the root node with the region file, its own child and exclusion tests; verdict: may be called PROVED after one correction of wording (label 11 lies in the hull of its two targets, not in
their union), which touches neither the Statement, nor the certificate, nor the acceptance run, nor a number of
the tables; this version has it, section "Review").
Limits, as the reviewer states them: the soundness of SPEC 3.0 and of the two frozen checkers is taken from their
own reviews (`reviews/REVIEW_30*.md`), and with it the exact values L of the 32 `0` steps (the reviewer compared
them across the producer's and the acceptance reports of both programs and did not recompute them; the checkers
were not rerun); nobody but the producer has read how the leaves were made (not needed: the certificate is checked,
not the way it was made); outside label 11 the region file is the reviewed v2 file (the reviewer's exact comparison); for label 11 the
reviewer checked that the factor contains the v2 factor, the old target PB_11 and the new target HULLW_11
(`reviews/join_roots/batch2/v_regions.out`); the v5 generator and `cmp_v5.py` are not reviewed.
The record is written by `acceptance/mk_record.py` in the form of `RECORD_EJPG17m_v2.md` (reviewed at 01:03);
every number is taken from the files (facts output `acceptance/JPG17p_v5_facts.out`, sha256 74c3dca64372c630..., of
`acceptance/region_facts.py`: all its checks ok), and the reviewer compared every number with its own reading of
the files.
**This is a statement about a region, NOT about a case of the proof:** that the capture side puts a packing into
this region needs its class statements, which are not certified.

## Statement

(E_JPG17p, v5). Let seventeen closed unit squares with pairwise disjoint interiors lie in [0, S]^2 with
S <= Sref = 4675530093604551/10^15, labelled 1 to 17, with one side direction a_i chosen for each square.
Then it is NOT the case that every xi_ik lies in the interval [lo_ik, hi_ik] and every a_i lies in the root arc of
label i, where the 34 intervals and the 17 arcs are those of

    bigbox/join/JPG17p_exact_v5.json   (entries window.box and root_arc)
    sha256 11b68ec1eb4aa790612e865da1983db23cde7cffe50aa59a84621f6fe2d39c12

In words: no packing of seventeen unit squares of side at most Sref lies in the region JPG17p v5. Coordinates xi_ik as in SPEC 3.0 section 1, from the reference file `upper-packing-certificate.json`
(sha256 24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7, the one in the certificate's header, used
by both checkers); frame (container corner at the origin): SPEC 3.0 section 0.

This is the EMPTINESS COROLLARY of SPEC 3.0 (`SPEC_v3.0_NOTES.md`, note of 2026-10-09 18:38): the certificate
satisfies all conditions of section 7 and no node is closed as terminal, so the set F(root) is empty; and a
configuration that is feasible for a side S <= Sref is feasible for the side Sref (SPEC 3.0 section 11).

The region in words (`JOIN_ROOTS.md`, sections 1, 9.2, 9.3 and 11.1; arcs read from the region file, in rad from
each label's reference direction): case T of the join design: label 9 inside its gate [-0.099900, +0.099901], its box cut at the support end xi_(9,1) >= -9897/1000000; label 3 inside its gate [-0.099917, +0.099917]; label 17 ABOVE its gate, [+0.099917, +0.786228]; label 15 any direction; label 4 with any direction; the loose labels 3, 4, 15, 17 in their slots; the twelve rigid labels 1, 2, 5 to 8, 10 to 14, 16 in their boxes PB_j, **label 11 in one box and one arc that contain its old target PB_11 and its new target HULLW_11** (the hull of the v2 factor and the transported new target, `JOIN_ROOTS.md` section 11.1; more than the union of the two targets; tag v5: xi_(11,1) in [-140801/1000000, 12647/62500], direction in [-0.137499811, +0.204999690]).

## Evidence

| what | value |
|---|---|
| certificate | `local-research/claude-20261002/results/assembly/JPG17p_v5/JPG17p_v5.cert.jsonl.gz`, 166,879,611 bytes, sha256 f392b6ba42c9abc3a60957cceeb70078dd72b200c2ef032ebdb8a0c6a7044b97; uncompressed stream a95e49f35370d4ded9a441800ad174848ec567c7d3b35c69bdcfd61ec8eaaee2 |
| its shape (read from the certificate) | 48 nodes, depth 9 in the Node checker's count (root = 0): 16 splits (9 arc, 0 box, 7 option) and 32 leaves closed by a `0` step; no terminal leaf; 32 steps, 1,176,714 terms, 1192 declarations. Cuts: direction of label 15 cut 4 times (tan-half from its reference direction: -659/5000, -1/20, 1/20, 659/5000); direction of label 17 cut 5 times (tan-half from its reference direction: 659/5000); 1 option split of the pair (4, 14) with 5 children; 4 option splits of the pair (12, 15) with 4 children; 1 option split of the pair (4, 6) with 4 children; 1 option split of the pair (3, 4) with 4 children. The description has no `recentre`: every split node has the root's centre for every label; the leaves keep their leaf files' own nodes, and 32 of the 48 nodes reach beyond the root node in some arc (list in the facts output), which SPEC 3.0 section 6 allows: a child only has to contain its piece. **Label 11 is never cut: its box and arc are the root's in every node.** |
| exact values of the `0` steps | all positive; the smallest is L = 1.472960e-03 at `pH11W37G453wuk3k2.n0.JPG17pv5.leaf`; the same rational number in both checkers' reports for each of the 32 leaves (table below) |
| producer | the audit lead: description by its `regiontree.py` (sha256 of the description 393b551525831749...), certificate by the assembler `proto30/hull_tree.py` 8af834ec6ccff429... (exit 0, 1567.3 s). Its own run of both frozen checkers under `--keep-going`: 48 of 48 nodes accepted by each (`JPG17p_v5.run.json`, sha256 af382fd136cc694b...) |
| acceptance run | `locks/run_slot.sh acceptance/accept_tree30.sh JPG17p_v5 <certificate> bigbox/join/EXPECT_JPG17p_v5.json`, by the lead, 2026-10-10 07:02:38 to 07:19 on the Mac. Python checker 825.48 s (632 MB), Node checker 162.38 s (1.48 GB) |
| log | `acceptance/ACCEPT_JPG17p_v5.log`, sha256 a86ef2c14fd9090fa0e3bc4c86aaf748a6dbf9fddc39dbf702e2b6489e767228: `RESULT: ACCEPTED`, exit code of the run 0 |
| checker reports | `acceptance/JPG17p_v5_C1.json` (Python, sha256 d3bf3fd968349ed7...), `acceptance/JPG17p_v5_C2.json` (Node, sha256 797cc0fb56db5a94...) |
| frozen files | `checker/wxcheck_v30.py` cf8db52bfa1cc565..., `checker2/wxcheck2_v30.js` 97210adf74a3ebed..., `SPEC_v3.0.md` 0a6dfc2ae10ed6f3... (`acceptance/FROZEN_30.json`) |
| statement file | `bigbox/join/EXPECT_JPG17p_v5.json`, sha256 c8000b864d207c0c6f7823370818c82bffcec89bd4731422be5176621db2dac9: 17 labels, S_floor = Sref, `terminal_leaves` 0, `root_region` = the file above |

Lines of the log that carry the statement: both checkers, started with their default options, exit 0 with PASS on
the whole file; every node accepted by both; same node ids and the same closure kind per node in both reports;
nodes 48, infeasible 32, split 16, terminal 0; the root node has parent null, an empty assumption list, the
region's side interval, the region's box in all 68 interval ends and the region's arc for every label (centre and
both end rotations).

The 32 leaves closed by a `0` step (L from the Python report; "L sha256" = sha256 of the fraction as the report
writes it; in every row the Node report has the same rational number and the audit lead's assembler
report the same fraction, `L_exact`; all placed by containment, `LEAF_FORMAT_RULING.md`):

| leaf node | leaf file sha256 | terms | L | L sha256 | options assumed |
|---|---|---|---|---|---|
| pH11W37G453wuk3k2.n0.JPG17pv5.leaf | 236ca3e6e75a18a7... | 36,477 | 0.0014730 | 4b818ef4b7b556c3... | 14:4:a:m, 6:4:a:m, 4:3:a:m |
| pH11W37G453wuk3k5.n0.JPG17pv5.leaf | 8c32ba48a3777b02... | 36,605 | 0.0015361 | 040ada56ea72ae86... | 14:4:a:m, 4:6:a:p |
| pH11W37G553wu.n0.0.JPG17pv5.leaf | 585f4513f5715d47... | 43,772 | 0.0017123 | 7b11e307c534cba6... | 15:12:b:m |
| pH11W37G453wuk3k6.n0.JPG17pv5.leaf | a001bedd8b1d26ef... | 36,393 | 0.0021320 | 6e6e6823b3e91c39... | 14:4:a:m, 4:6:b:p |
| pH11W37G453wuk4.n0.JPG17pv5.leaf | 4342ec809ed58a3b... | 39,408 | 0.0023866 | 279c0d5b6d2f5561... | 4:14:a:p |
| pH11W37G413wu.n0.JPG17pv5.leaf | de62dd7379e6a0c8... | 40,493 | 0.0024295 | 022d57ae2bc049fe... | none |
| pH11W37G513wu.n0.JPG17pv5.leaf | 14e1be99ad80e3e4... | 43,016 | 0.0042531 | da0c4d28f17b9b56... | none |
| pH11W37G453wuk3k3.n0.JPG17pv5.leaf | 78d8ebb5601c89bf... | 41,557 | 0.0076470 | a459a8828a4d90b9... | 14:4:a:m, 6:4:a:m, 4:3:b:m |
| pH11W37G453wuk2.n0.0.JPG17pv5.leaf | ad93ecabada3fc92... | 32,396 | 0.0092527 | 34cbbb2f2612405e... | 14:4:b:m, 15:12:b:m |
| pH11W37G453wuk1.n0.0.JPG17pv5.leaf | 64fe994afa52baa9... | 31,820 | 0.0092546 | 114ba7615383f31a... | 4:14:b:p, 15:12:b:m |
| pH11W37G453wuk3k7.n0.JPG17pv5.leaf | 1e3b57b0f634c8c2... | 36,699 | 0.0108589 | 939bf85918c85505... | 14:4:a:m, 6:4:b:m |
| pH11W37G553wu.n0.2.JPG17pv5.leaf | 8707a6ae8da9504b... | 41,722 | 0.0157087 | 84e37d63d3fdad80... | 12:15:b:p |
| pH11W37G433wu.n0.JPG17pv5.leaf | 7f9f6665e3bbdee5... | 38,600 | 0.0161389 | d34e7dfd72f0b8a0... | none |
| pH11W37G453wuk3k1.n0.0.JPG17pv5.leaf | 19c297cf027324ae... | 32,661 | 0.0165086 | 7b656d91940595ba... | 14:4:a:m, 6:4:a:m, 3:4:a:p, 15:12:b:m |
| pH11W37G453wuk1.n0.2.JPG17pv5.leaf | 1d3e596d954d7dfb... | 35,049 | 0.0181346 | 21b1a7f6a595bde3... | 4:14:b:p, 12:15:b:p |
| pH11W37G453wuk2.n0.2.JPG17pv5.leaf | 8c71d48bec7a5cad... | 35,496 | 0.0183924 | 0144c48c8072bf12... | 14:4:b:m, 12:15:b:p |
| pH11W37G533wu.n0.JPG17pv5.leaf | 6cbe66775a63afd1... | 34,470 | 0.0195612 | cf1737a88e35c9a5... | none |
| pH11W37G423wu.n0.JPG17pv5.leaf | 078e835fa64a0777... | 35,103 | 0.0290571 | 321f9a4eafc3891c... | none |
| pH11W37G443wu.n0.JPG17pv5.leaf | af845e157e77fca2... | 37,898 | 0.0303385 | 95b2ea96015ebaac... | none |
| pH11W37G543wu.n0.JPG17pv5.leaf | 27d6963fbeab4d2b... | 33,025 | 0.0324075 | 50c9984c94ccc311... | none |
| pH11W37G453wuk3k1.n0.2.JPG17pv5.leaf | 3ccd7706fa5973f9... | 32,956 | 0.0358211 | f9e098b5a5badf14... | 14:4:a:m, 6:4:a:m, 3:4:a:p, 12:15:b:p |
| pH11W37G523wu.n0.JPG17pv5.leaf | b4240c3c678a0747... | 30,089 | 0.0412417 | 801193b9e8516087... | none |
| pH11W37G453wuk1.n0.3.JPG17pv5.leaf | 138cf94f860a894f... | 34,543 | 0.0442809 | dcfc71e0fc8d3b0a... | 4:14:b:p, 15:12:a:m |
| pH11W37G453wuk2.n0.3.JPG17pv5.leaf | df2ce69df129cbe2... | 34,115 | 0.0442824 | ee05bc58e2c879d7... | 14:4:b:m, 15:12:a:m |
| pH11W37G453wuk1.n0.1.JPG17pv5.leaf | fac02adc7fff8e94... | 31,291 | 0.0444045 | 3fc9f1ec95f7cac8... | 4:14:b:p, 12:15:a:p |
| pH11W37G453wuk2.n0.1.JPG17pv5.leaf | 5d9ef6c922762cb4... | 30,376 | 0.0444053 | 1adbef0a00cf5ec2... | 14:4:b:m, 12:15:a:p |
| pH11W37G453wuk3k1.n0.1.JPG17pv5.leaf | 65a35ff28b0cafec... | 30,053 | 0.0444490 | 395409f4a029280e... | 14:4:a:m, 6:4:a:m, 3:4:a:p, 15:12:a:m |
| pH11W37G453wuk3k1.n0.3.JPG17pv5.leaf | 5d527a8e2df2f986... | 27,775 | 0.0445603 | 98a9e5fbb5ae3940... | 14:4:a:m, 6:4:a:m, 3:4:a:p, 12:15:a:p |
| pH11W37G453wuk5.n0.JPG17pv5.leaf | 6c090a2dbfb19907... | 44,614 | 16.1639018 | 4ac7410553339557... | 4:14:a:m |
| pH11W37G553wu.n0.1.JPG17pv5.leaf | f79937ef12d1fd8d... | 47,915 | 64.9626735 | bb38b4068566fc42... | 15:12:a:m |
| pH11W37G553wu.n0.3.JPG17pv5.leaf | 975093a20abd61ad... | 47,915 | 124.7188140 | 570934d43eabe348... | 12:15:a:p |
| pH11W37G453wuk3k4.n0.JPG17pv5.leaf | 9ad2a9f48b64b496... | 42,412 | 5218.7982943 | 733d5dcd06c476c0... | 14:4:a:m, 6:4:a:m, 4:3:b:p |

## What the statement is used for, and what it does not contain

- It is the local side's statement for this branch of case T **whichever statement of label 11 certifies**: the v5
  region contains the old target PB_11 and the new target HULLW_11 (`JOIN_ROOTS.md` top table and section 11.1,
  `ADMISSION_v4.md` section 9; `cmp_v5.py`). It serves the branch if the capture side certifies, for each of the
  twelve rigid labels j, a statement with the target of this region (PT_j, PM_j, the split statements PS_j^17 or
  PSS_j^17; for label 11 also PTW37_L11 or PSW37_L11 with k = 17), together with the statements for label 9 and the
  loose labels. The composition is `JOIN_ROOTS.md` sections 3 and 9.3; it is not repeated or proved here.
- The v5 region contains the region JPG17p v2 (equal outside label 11; `cmp_v5.py` part A), so this statement
  implies (E_JPG17p, v2).
- The tree consists of second-tree leaves made on the v5 root only; label 11 is not cut anywhere.
- NOT contained: that the capture side puts a packing of this branch into the region (no class statement of the
  branch is certified), and the correctness of the region file against the class files (the v5 files are checked
  by 2,552 exact self-checks and against Codex's drafts, `ADMISSION_v4.md`; the reviewer of this record compared
  the v5 file with its reviewed v2 file, equal outside label 11, and checked that the factor of label 11 contains
  the v2 factor, PB_11 and HULLW_11, `reviews/join_roots/batch2/v_regions.out`; the v5 generator and `cmp_v5.py`
  are not reviewed).

## Review

Reviewed 2026-10-10 by a reviewer that wrote none of the record, of the certificate or of the tools,
in one batch with five other records: `reviews/join_roots/batch2/REVIEW_BATCH2.md` (sha256
25227b662a3e6211cc35fa09492e716c5e0e4001ca3d339b7623146a0f958905); the text it read is kept as
`reviews/join_roots/batch2/as_reviewed/RECORD_EJPG17p_v5.md` (sha256 274ec4fea50876e1...); its scripts and outputs are in
`reviews/join_roots/batch2/` (`t_tree.py`, output `t_JPG17p_v5.out`; `v_regions.py`, `v_regions.out`). **Verdict: the statement may be called PROVED after the listed correction, a correction of wording.**
It recomputed, with its own code (the earlier reviewer's scripts made into one program and extended): every hash
the record names; the certificate line by line (header, counts, the tree conditions of SPEC 3.0 section 7, the
root node against the region file in the side interval, 68 box ends and 51 rotations, every cut as the record
words it); the child test of section 6 for all 47 children; the exclusion test of section 4.7 for
all 7 option splits (the nested ones too: the pairs (4, 14) with five children, (4, 6), (3, 4), (12, 15)); the final store hashes of both acceptance reports from the node data, and the producer's two reports against
them node by node; every row of the table of leaves; the log.
On the region file (`v_regions.out`, 45 checks for the five regions): the v5 file against its v2 file (equal
outside label 11; label 11 of v5 contains label 11 of v2 and is larger by 46247/1000000 in xi_(11,1) and by
3.749992e-2 rad at the lower arc end), "the region in words" number by number, label 11 never cut and with the
root's box and arc in every node, the targets (the class PB_j is the same data in PT_j, PM_j, PS_j^k and PSS_j^k
for all twelve rigid labels; HULLW_11 the same in PTW37_L11, PSW37_L11_Tkk and PSSW37_L11_Tkk), and the reviewer's
own transport of the two targets: the factor of label 11 contains PB_11 and HULLW_11. This is the v5 record the
reviewer took in depth.
It did not rerun the two frozen checkers or the acceptance script (the frozen checkers have run on
these bytes twice: the producer's run with `--keep-going` and my acceptance run with the default options).

The correction, made in this version (08:21):
1. "The region in words" said "label 11 in the union of its old target PB_11 and its new target HULLW_11". The
   factor of label 11 is one box and one arc, the hull of the v2 factor and the transported new target
   (`JOIN_ROOTS.md` section 11.1, `ADMISSION_v4.md` section 9); it contains both targets and is more than their
   union. The numbers were right; the words described a smaller region than the one that is proved empty (the safe
   side; the Statement names the file and was not affected). The same text is corrected in
   `acceptance/mk_record.py`.
Also taken up: the limits sentence in the status paragraph (finding 4); the last point of "used for" now says what
this review did for the v5 file (remark 6d). Remarks of the reviewer that need no change: the root arc of label 17
ends 9.3e-10 rad inside the gate, so the region is that much larger than "ABOVE its gate" says (the safe side, as in
the reviewed record of JPG17m v2); the sizes of the acceptance row are in binary units.
