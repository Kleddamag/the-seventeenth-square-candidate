Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line.

# Record: statement (E_JPG3p, v5) for the region JPG3p v5 ("the region JPG3p v5 is empty"): ACCEPTED 2026-10-10 12:46, PROVED 13:04

Lead of the window side. Status words as in `bigbox/THEOREM_G20.md`: COMPUTED / PROVED; ACCEPTED
means: accepted by both frozen checkers in the lead's acceptance run, the record not yet reviewed.

**STATUS: PROVED (2026-10-10 13:04) as a statement about the numbers of the region file** (status words of
`bigbox/THEOREM_G20.md`): the certificate is accepted by both frozen checkers with the lead's post-check (12:46),
and this record is reviewed by a reviewer that wrote none of it, nor the certificate, nor the tools
(`reviews/join_roots/batch4/REVIEW_EJPG3p_v5.md`, sha256 9fa9013da56b4a18...: 200 checks of its
own by three programs, 131 and 15 on this certificate and 54 on the region files, none failed; its own reading of
the certificate with the earlier reviewers' program, extended; its own comparison of the root node with the region
file, child and exclusion tests; verdict: "PROVED: yes", no number, hash or claim of the record wrong; three
texts change with the status, section "Review").
Limits, as the reviewer states them: the soundness of SPEC 3.0 and of the two frozen checkers is taken from their
own reviews (`reviews/REVIEW_30*.md`), and with it the exact values L of the 22 `0` steps (the reviewer compared
them across the producer's and the acceptance reports of both programs and did not recompute them; the checkers
were not rerun; that a leaf's round uses only options its node assumes is the checkers' test too); nobody but
the producer has read how the leaves were made (not needed: the certificate is checked, not the way it was made);
outside label 11 the region file is the reviewed v2 file (the reviewer's exact comparison); for label 11 the
reviewer checked that the factor contains the v2 factor, the old target PB_11 and the new target HULLW_11
(`reviews/join_roots/batch4/v_regions.out`); the v5 generator and `cmp_v5.py` are not reviewed.
The record is written by `acceptance/mk_record.py` in the form of `RECORD_EJPG17m_v2.md` (reviewed at 01:03), with
the corrections of the review of batch 2 already in the generator; every number is taken from the files (facts
output `acceptance/JPG3p_v5_facts.out`, sha256 2a3927f403803757..., of `acceptance/region_facts.py`: all its checks ok), and
the reviewer compared every number with its own reading of the files.
**This is a statement about a region, NOT about a case of the proof:** that the capture side puts a packing into
this region needs its class statements, which are not certified.

## Statement

(E_JPG3p, v5). Let seventeen closed unit squares with pairwise disjoint interiors lie in [0, S]^2 with
S <= Sref = 4675530093604551/10^15, labelled 1 to 17, with one side direction a_i chosen for each square.
Then it is NOT the case that every xi_ik lies in the interval [lo_ik, hi_ik] and every a_i lies in the root arc of
label i, where the 34 intervals and the 17 arcs are those of

    bigbox/join/JPG3p_exact_v5.json   (entries window.box and root_arc)
    sha256 c4287958b08fe4fcd168aefc70223ac241541b4afa69995775e6c88cc60237d9

In words: no packing of seventeen unit squares of side at most Sref lies in the region JPG3p v5. Coordinates xi_ik as in SPEC 3.0 section 1, from the reference file `upper-packing-certificate.json`
(sha256 24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7, the one in the certificate's header, used
by both checkers); frame (container corner at the origin): SPEC 3.0 section 0.

This is the EMPTINESS COROLLARY of SPEC 3.0 (`SPEC_v3.0_NOTES.md`, note of 2026-10-09 18:38): the certificate
satisfies all conditions of section 7 and no node is closed as terminal, so the set F(root) is empty; and a
configuration that is feasible for a side S <= Sref is feasible for the side Sref (SPEC 3.0 section 11).

The region in words (`JOIN_ROOTS.md`, sections 1, 9.2, 9.3 and 11.1; arcs read from the region file, in rad from
each label's reference direction): case T of the join design: label 9 inside its gate [-0.099900, +0.099901], its box cut at the support end xi_(9,1) >= -9897/1000000; label 3 ABOVE its gate, [+0.099917, +0.786228]; label 17 any direction; label 15 any direction; label 4 with any direction; the loose labels 3, 4, 15, 17 in their slots; the twelve rigid labels 1, 2, 5 to 8, 10 to 14, 16 in their boxes PB_j, **label 11 in one box and one arc that contain its old target PB_11 and its new target HULLW_11** (the hull of the v2 factor and the transported new target, `JOIN_ROOTS.md` section 11.1; more than the union of the two targets; tag v5: xi_(11,1) in [-140801/1000000, 12647/62500], direction in [-0.137499811, +0.204999690]).

## Evidence

| what | value |
|---|---|
| certificate | `local-research/claude-20261002/results/assembly/JPG3p_v5/JPG3p_v5.cert.jsonl.gz`, 136,592,253 bytes, sha256 804ae79493f6733645b3d70c10edc05d5ab0c20fea416284af16c9e855c7c0ea; uncompressed stream 1a97f63c2828bd75eb355c4abb8b030d30d5183ffca06850788c719425df7c58 |
| its shape (read from the certificate) | 36 nodes, depth 7 in the Node checker's count (root = 0): 14 splits (9 arc, 0 box, 5 option) and 22 leaves closed by a `0` step; no terminal leaf; 22 steps, 988,844 terms, 832 declarations. Cuts: direction of label 15 cut 2 times (tan-half from its reference direction: -1/20, 1/20); direction of label 17 cut 7 times (tan-half from its reference direction: -1/20, 1/20, 563/2500); 3 option splits of the pair (12, 15) with 4 children; 1 option split of the pair (14, 17) with 2 children; 1 option split of the pair (8, 17) with 3 children. The description has no `recentre`: every split node has the root's centre for every label; the leaves keep their leaf files' own nodes, and 21 of the 36 nodes reach beyond the root node in some arc (list in the facts output), which SPEC 3.0 section 6 allows: a child only has to contain its piece. **Label 11 is never cut: its box and arc are the root's in every node.** |
| exact values of the `0` steps | all positive; the smallest is L = 1.927617e-03 at `pH11W37Gmppwu.n0.0.JPG3pv5.leaf`; the same rational number in both checkers' reports for each of the 22 leaves (table below) |
| producer | the audit lead: description by its `regiontree.py` (sha256 of the description 71d57dfcfa4e3f02...), certificate by the assembler `proto30/hull_tree.py` 8af834ec6ccff429... (exit 0, 1332.9 s). Its own run of both frozen checkers under `--keep-going`: 36 of 36 nodes accepted by each (`JPG3p_v5.run.json`, sha256 12cf02af3ebd9d9c...) |
| acceptance run | `locks/run_slot.sh acceptance/accept_tree30.sh JPG3p_v5 <certificate> bigbox/join/EXPECT_JPG3p_v5.json`, by the lead, 2026-10-10 12:32:38 to 12:46 on the Mac. Python checker 695.76 s (695 MB), Node checker 134.95 s (1.09 GB) |
| log | `acceptance/ACCEPT_JPG3p_v5.log`, sha256 628d831ac54b45e15cf0ae9dcd303d05ef0517910c4dc7b8373900d7c441cf80: `RESULT: ACCEPTED`, exit code of the run 0 |
| checker reports | `acceptance/JPG3p_v5_C1.json` (Python, sha256 dd8a6d6e256816b2...), `acceptance/JPG3p_v5_C2.json` (Node, sha256 810abbd1d68b1d25...) |
| frozen files | `checker/wxcheck_v30.py` cf8db52bfa1cc565..., `checker2/wxcheck2_v30.js` 97210adf74a3ebed..., `SPEC_v3.0.md` 0a6dfc2ae10ed6f3... (`acceptance/FROZEN_30.json`) |
| statement file | `bigbox/join/EXPECT_JPG3p_v5.json`, sha256 4450804df543078a20c83e71a82d505e756bfe4c1855416567cc82b8fafc6f41: 17 labels, S_floor = Sref, `terminal_leaves` 0, `root_region` = the file above |

Lines of the log that carry the statement: both checkers, started with their default options, exit 0 with PASS on
the whole file; every node accepted by both; same node ids and the same closure kind per node in both reports;
nodes 36, infeasible 22, split 14, terminal 0; the root node has parent null, an empty assumption list, the
region's side interval, the region's box in all 68 interval ends and the region's arc for every label (centre and
both end rotations).

The 22 leaves closed by a `0` step (L from the Python report; "L sha256" = sha256 of the fraction as the report
writes it; in every row the Node report has the same rational number and the audit lead's assembler
report the same fraction, `L_exact`; all placed by containment, `LEAF_FORMAT_RULING.md`):

| leaf node | leaf file sha256 | terms | L | L sha256 | options assumed |
|---|---|---|---|---|---|
| pH11W37Gmppwu.n0.0.JPG3pv5.leaf | 303ed4b44f08403c... | 46,163 | 0.0019276 | 7c7f4875f2321354... | 15:12:b:m |
| pH11W37Gpppwk2.n0.JPG3pv5.leaf | 4266fa4a87728c63... | 48,199 | 0.0023134 | 64cb8e1a06af872f... | 17:8:a:p |
| pH11W37G3ppwu.n0.JPG3pv5.leaf | a03385f3720bad47... | 42,048 | 0.0031637 | fb43cd48c3a8d59a... | none |
| pH11W37Gpmpwur.n0.JPG3pv5.leaf | 9dee2b6e53d73ed2... | 47,175 | 0.0034428 | 5e660cf32e8fea9c... | none |
| pH11W37Gpppwk3.n0.JPG3pv5.leaf | 3e56fdc4192a4e67... | 42,927 | 0.0047631 | 3fbe731c662d420d... | 17:8:b:p |
| pH11W37Gpppw.n0.0.1.0.JPG3pv5.leaf | 614796978c05bddb... | 43,306 | 0.0054892 | c6e0b8062f234712... | 8:17:b:m, 15:12:b:m |
| pH11W37Gmmpwu.n0.0.JPG3pv5.leaf | 83924e801b42094a... | 43,580 | 0.0083923 | d461bb1f6ef46791... | 15:12:b:m |
| pH11W37Gm3pwu.n0.JPG3pv5.leaf | 18dc25ac85ab1a4d... | 40,394 | 0.0102299 | 32abfcceb80e79da... | none |
| pH11W37Gpppw.n0.0.0.JPG3pv5.leaf | cfa1e855b773a7b3... | 39,827 | 0.0127295 | 218e223e68a75a51... | 8:17:b:m |
| pH11W37G3mpwu.n0.0.JPG3pv5.leaf | 99e212271565f32a... | 39,594 | 0.0131525 | 2aaac107e5d5f49c... | 14:17:a:p |
| pH11W37Gp3pwu.n0.JPG3pv5.leaf | 51b37d4698d10d9a... | 40,140 | 0.0145289 | 465f6e9201d74f32... | none |
| pH11W37Gmmpwu.n0.3.JPG3pv5.leaf | cd9d7cf4e4cefd30... | 49,750 | 0.0154877 | 78be9720017fba15... | 12:15:a:p |
| pH11W37Gmppwu.n0.3.JPG3pv5.leaf | b65f498b95b407b4... | 49,750 | 0.0167329 | 34b39e90b08a418d... | 12:15:a:p |
| pH11W37Gmppwu.n0.2.JPG3pv5.leaf | 08f0eaa794fd50d7... | 44,266 | 0.0321902 | 6b8c683640ef5e90... | 12:15:b:p |
| pH11W37Gpppw.n0.0.1.2.JPG3pv5.leaf | 825eb67c30ced1b3... | 41,080 | 0.0324404 | d35e0cce2812df70... | 8:17:b:m, 12:15:b:p |
| pH11W37G33pwu.n0.JPG3pv5.leaf | bc4c3fcc7f2da9e2... | 39,158 | 0.0335794 | 35fab11f68ddb0ff... | none |
| pH11W37Gmppwu.n0.1.JPG3pv5.leaf | 88a312a85a10f9cd... | 48,607 | 0.0498691 | 4b293d25d377e371... | 15:12:a:m |
| pH11W37Gpppw.n0.0.1.1.JPG3pv5.leaf | 31fcd074346d3ad7... | 48,282 | 17.3741450 | 76b7627c2e046708... | 8:17:b:m, 15:12:a:m |
| pH11W37Gpppw.n0.0.1.3.JPG3pv5.leaf | 3eee809252df7425... | 48,282 | 22.3624237 | 5b9aec4c2b1ee800... | 8:17:b:m, 12:15:a:p |
| pH11W37G3mpwu.n0.1.JPG3pv5.leaf | 0b7b79b56b33de94... | 46,816 | 27.2435546 | 13e1c72194276cdf... | 17:14:a:m |
| pH11W37Gmmpwu.n0.1.JPG3pv5.leaf | 90dd00d0fa00e94f... | 49,750 | 261.3445637 | 8684c331b5dd901d... | 12:15:b:p |
| pH11W37Gmmpwu.n0.2.JPG3pv5.leaf | 1be269dfed2b880c... | 49,750 | 968.9329413 | d41e47f1df0a482f... | 15:12:a:p |

## What the statement is used for, and what it does not contain

- It is the local side's statement for this branch of case T **whichever statement of label 11 certifies**: the v5
  region contains the old target PB_11 and the new target HULLW_11 (`JOIN_ROOTS.md` top table and section 11.1,
  `ADMISSION_v4.md` section 9; `cmp_v5.py`). It serves the branch if the capture side certifies, for each of the
  twelve rigid labels j, a statement with the target of this region (PT_j, PM_j, the split statements PS_j^3 or
  PSS_j^3; for label 11 also PTW37_L11 or PSW37_L11 with k = 3), together with the statements for label 9 and the
  loose labels. The composition is `JOIN_ROOTS.md` sections 3 and 9.3; it is not repeated or proved here.
- The v5 region contains the region JPG3p v2 (equal outside label 11; `cmp_v5.py` part A), so this statement
  implies (E_JPG3p, v2), which is also PROVED by a tree of its own (`RECORD_EJPG3p_v2.md`, 08:21).
- The tree consists of second-tree leaves made on the v5 root only; label 11 is not cut anywhere.
- NOT contained: that the capture side puts a packing of this branch into the region (no class statement of the
  branch is certified), and the correctness of the region file against the class files (the v5 files are checked
  by 2,552 exact self-checks and against Codex's drafts, `ADMISSION_v4.md`; the reviewer of this record compared
  the v5 file with its reviewed v2 file, equal outside label 11, and checked that the factor of label 11 contains
  the v2 factor, PB_11 and HULLW_11, `reviews/join_roots/batch4/v_regions.out`; the v5 generator and `cmp_v5.py`
  are not reviewed).

## Review

Reviewed 2026-10-10 by a reviewer that wrote none of the record, of the certificate or of the tools:
`reviews/join_roots/batch4/REVIEW_EJPG3p_v5.md` (sha256
9fa9013da56b4a184836160cae6b745e8dfe9e38136867ab7b4c27c10a7c4841); the text it read is kept as
`reviews/join_roots/batch4/as_reviewed/RECORD_EJPG3p_v5.md` (sha256 5bf850e033fa6603...); its scripts and outputs
are in `reviews/join_roots/batch4/` (`t_tree.py`, `t_JPG3p_v5.out`; `t_more.py`, `t_more_JPG3p_v5.out`;
`v_regions.py`, `v_regions.out`). **Verdict: "PROVED: yes". No number, no hash and no claim of the record is
wrong; nothing was found that touches all region trees.**
It recomputed, with its own run of the earlier reviewers' program (extended; the certificate read line by line):
every hash the record names; header and counts; the tree conditions of SPEC 3.0 section 7; the root node against
the region file (side interval, 68 box ends, 51 rotations); every cut as the record words it, each strictly
inside its node's arc; the child test of section 6 for all 35 children; the exclusion test of section 4.7 for all
5 option splits; label 11 never cut and with the root's box and arc in all 36 nodes; the final store hashes of
both acceptance reports for all 36 nodes, and the producer's two reports against them node by node; all 22 rows
of the table of leaves; the log; "the region in words" number by number. On the region file (54 checks): the v5
file against `JPG3p_exact_v2.json` (equal outside label 11; label 11 contains the v2 factor and is the same data
as in the five other v5 files; by its own transport the factor contains PB_11 and HULLW_11); JPG3p and JPG3m are
the same data in every label other than 3, whose two arcs are exact mirror images; the targets for k = 3.
What is particular to this tree (its remarks a to c, no change needed): node for node the tree has the cuts,
pairs, option lists and assumption lists of the reviewed tree on the v2 root, with the same boxes and arcs
outside label 11, and the leaves are new (no leaf file hash and no L of the v2 record recurs). The nested split:
the pair (8, 17) is split on a node that assumes nothing (five omitted options excluded with margins 0.5741 to
2.1812); under its option 8:17:b:m the direction of label 17 is cut at tan-half 563/2500 and the upper piece
splits the pair (12, 15), whose four omitted options are excluded on that node's own data with margins 0.8477 to
1.5084 (the test does not use the assumption). The three splits of the pair (12, 15) list 15:12:a:p where label
15 is below its gate and 15:12:a:m where it is above; each list passes the exclusion test, and no listed option
would be excluded.
It did not rerun the two frozen checkers or the acceptance script (the frozen checkers have run on
these bytes twice: the producer's run with `--keep-going` and my acceptance run with the default options).

The three texts that changed with the status, all in this version (13:04): the status paragraph with the limits
sentence (finding 1); the last point of "used for", which now says what this review did for the v5 file (finding
2); this section (finding 3). No correction of a number or of the Statement was asked.
Remarks of the reviewer that need no change: the 21 nodes that reach beyond the root are all leaves, 36 arcs in
all, labels 15 and 17 only, by 4.334e-6 to 5.260e-6 rad (the amounts of the reviewed v2 tree), nothing above
1e-5 rad and none in a box interval; the root arc of label 3 ends 9.3e-10 rad inside the gate, so the region is
that much larger than "ABOVE its gate" says (the safe side); the certificate file has two directory entries (a
hard link) with the size and hashes of this record.
