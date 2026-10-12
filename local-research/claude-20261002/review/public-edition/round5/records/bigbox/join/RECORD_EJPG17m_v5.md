Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line.

# Record: statement (E_JPG17m, v5) for the region JPG17m v5 ("the region JPG17m v5 is empty"): ACCEPTED 2026-10-10 07:02, PROVED 08:21

Lead of the window side. Status words as in `bigbox/THEOREM_G20.md`: COMPUTED / PROVED; ACCEPTED
means: accepted by both frozen checkers in the lead's acceptance run, the record not yet reviewed.

**STATUS: PROVED (2026-10-10 08:21) as a statement about the numbers of the region file** (status words of
`bigbox/THEOREM_G20.md`): the certificate is accepted by both frozen checkers with the lead's post-check (07:02),
and this record is reviewed by a reviewer that wrote none of it, nor the certificate, nor the tools
(`reviews/join_roots/batch2/REVIEW_BATCH2.md`, sha256 25227b662a3e6211..., one review of six records:
115 checks of its own on this certificate and 45 on the region files of the five regions (`v_regions.out`), none failed; its own reader of the certificate, its own
comparison of the root node with the region file, its own child and exclusion tests; verdict: may be called PROVED after one correction of wording (label 11 lies in the hull of its two targets, not in
their union), which touches neither the Statement, nor the certificate, nor the acceptance run, nor a number of
the tables; this version has it, section "Review").
Limits, as the reviewer states them: the soundness of SPEC 3.0 and of the two frozen checkers is taken from their
own reviews (`reviews/REVIEW_30*.md`), and with it the exact values L of the 18 `0` steps (the reviewer compared
them across the producer's and the acceptance reports of both programs and did not recompute them; the checkers
were not rerun); nobody but the producer has read how the leaves were made (not needed: the certificate is checked,
not the way it was made); outside label 11 the region file is the reviewed v2 file (the reviewer's exact comparison); for label 11 the
reviewer checked that the factor contains the v2 factor, the old target PB_11 and the new target HULLW_11
(`reviews/join_roots/batch2/v_regions.out`); the v5 generator and `cmp_v5.py` are not reviewed.
The record is written by `acceptance/mk_record.py` in the form of `RECORD_EJPG17m_v2.md` (reviewed at 01:03);
every number is taken from the files (facts output `acceptance/JPG17m_v5_facts.out`, sha256 9d720b79b51255c6..., of
`acceptance/region_facts.py`: all its checks ok), and the reviewer compared every number with its own reading of
the files.
**This is a statement about a region, NOT about a case of the proof:** that the capture side puts a packing into
this region needs its class statements, which are not certified.

## Statement

(E_JPG17m, v5). Let seventeen closed unit squares with pairwise disjoint interiors lie in [0, S]^2 with
S <= Sref = 4675530093604551/10^15, labelled 1 to 17, with one side direction a_i chosen for each square.
Then it is NOT the case that every xi_ik lies in the interval [lo_ik, hi_ik] and every a_i lies in the root arc of
label i, where the 34 intervals and the 17 arcs are those of

    bigbox/join/JPG17m_exact_v5.json   (entries window.box and root_arc)
    sha256 18550e414d3f50577234684d54ceb4b0e44b45bbce6cd4b5efff9596e7f72272

In words: no packing of seventeen unit squares of side at most Sref lies in the region JPG17m v5. Coordinates xi_ik as in SPEC 3.0 section 1, from the reference file `upper-packing-certificate.json`
(sha256 24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7, the one in the certificate's header, used
by both checkers); frame (container corner at the origin): SPEC 3.0 section 0.

This is the EMPTINESS COROLLARY of SPEC 3.0 (`SPEC_v3.0_NOTES.md`, note of 2026-10-09 18:38): the certificate
satisfies all conditions of section 7 and no node is closed as terminal, so the set F(root) is empty; and a
configuration that is feasible for a side S <= Sref is feasible for the side Sref (SPEC 3.0 section 11).

The region in words (`JOIN_ROOTS.md`, sections 1, 9.2, 9.3 and 11.1; arcs read from the region file, in rad from
each label's reference direction): case T of the join design: label 9 inside its gate [-0.099900, +0.099901], its box cut at the support end xi_(9,1) >= -9897/1000000; label 3 inside its gate [-0.099917, +0.099917]; label 17 BELOW its gate, [-0.786228, -0.099917]; label 15 any direction; label 4 with any direction; the loose labels 3, 4, 15, 17 in their slots; the twelve rigid labels 1, 2, 5 to 8, 10 to 14, 16 in their boxes PB_j, **label 11 in one box and one arc that contain its old target PB_11 and its new target HULLW_11** (the hull of the v2 factor and the transported new target, `JOIN_ROOTS.md` section 11.1; more than the union of the two targets; tag v5: xi_(11,1) in [-140801/1000000, 12647/62500], direction in [-0.137499811, +0.204999690]).

## Evidence

| what | value |
|---|---|
| certificate | `local-research/claude-20261002/results/assembly/JPG17m_v5/JPG17m_v5.cert.jsonl.gz`, 106,187,146 bytes, sha256 68613d8407cb5a9f8fdb7142641b3d4237f36f002ba856f6498bff7a66aa1751; uncompressed stream 2d0940073082b0773193e4231beaadf83f2a9a57082cb99b72183fe22aa030c4 |
| its shape (read from the certificate) | 31 nodes, depth 8 in the Node checker's count (root = 0): 13 splits (11 arc, 0 box, 2 option) and 18 leaves closed by a `0` step; no terminal leaf; 18 steps, 748,232 terms, 679 declarations. Cuts: direction of label 15 cut 4 times (tan-half from its reference direction: -659/5000, -1/20, 1/20, 659/5000); direction of label 17 cut 5 times (tan-half from its reference direction: -659/5000); 2 option splits of the pair (12, 15) with 4 children; direction of label 4 cut 2 times (tan-half from its reference direction: -659/5000, 659/5000). The description has no `recentre`: every split node has the root's centre for every label; the leaves keep their leaf files' own nodes, and 18 of the 31 nodes reach beyond the root node in some arc (list in the facts output), which SPEC 3.0 section 6 allows: a child only has to contain its piece. **Label 11 is never cut: its box and arc are the root's in every node.** |
| exact values of the `0` steps | all positive; the smallest is L = 1.769578e-03 at `pH11W37G153w.n0.0.JPG17mv5.leaf`; the same rational number in both checkers' reports for each of the 18 leaves (table below) |
| producer | the audit lead: description by its `regiontree.py` (sha256 of the description 3a2ee8200cfd6422...), certificate by the assembler `proto30/hull_tree.py` 8af834ec6ccff429... (exit 0, 954.6 s). Its own run of both frozen checkers under `--keep-going`: 31 of 31 nodes accepted by each (`JPG17m_v5.run.json`, sha256 27442dde4e9e2489...) |
| acceptance run | `locks/run_slot.sh acceptance/accept_tree30.sh JPG17m_v5 <certificate> bigbox/join/EXPECT_JPG17m_v5.json`, by the lead, 2026-10-10 06:51:59 to 07:02 on the Mac. Python checker 518.19 s (645 MB), Node checker 106.26 s (1.08 GB) |
| log | `acceptance/ACCEPT_JPG17m_v5.log`, sha256 88c670b3ca7d8641ceb32b36045620b079b1795e3060dd53c9f61f22f804724f: `RESULT: ACCEPTED`, exit code of the run 0 |
| checker reports | `acceptance/JPG17m_v5_C1.json` (Python, sha256 def972a2e80e2d53...), `acceptance/JPG17m_v5_C2.json` (Node, sha256 def2d4907e7006c6...) |
| frozen files | `checker/wxcheck_v30.py` cf8db52bfa1cc565..., `checker2/wxcheck2_v30.js` 97210adf74a3ebed..., `SPEC_v3.0.md` 0a6dfc2ae10ed6f3... (`acceptance/FROZEN_30.json`) |
| statement file | `bigbox/join/EXPECT_JPG17m_v5.json`, sha256 9c202c8eb04502072e327f0333054f56ca814f005d8812a2daccaf9aa20147be: 17 labels, S_floor = Sref, `terminal_leaves` 0, `root_region` = the file above |

Lines of the log that carry the statement: both checkers, started with their default options, exit 0 with PASS on
the whole file; every node accepted by both; same node ids and the same closure kind per node in both reports;
nodes 31, infeasible 18, split 13, terminal 0; the root node has parent null, an empty assumption list, the
region's side interval, the region's box in all 68 interval ends and the region's arc for every label (centre and
both end rotations).

The 18 leaves closed by a `0` step (L from the Python report; "L sha256" = sha256 of the fraction as the report
writes it; in every row the Node report has the same rational number and the audit lead's assembler
report the same fraction, `L_exact`; all placed by containment, `LEAF_FORMAT_RULING.md`):

| leaf node | leaf file sha256 | terms | L | L sha256 | options assumed |
|---|---|---|---|---|---|
| pH11W37G153w.n0.0.JPG17mv5.leaf | 42ca9cc13520cc0d... | 44,595 | 0.0017696 | 2d530dcac44341ac... | 15:12:b:m |
| pH11W37G253wu.n0.JPG17mv5.leaf | a3b28da840a0dcfc... | 39,335 | 0.0026082 | 6df8e5bbb8c8424c... | none |
| pH11W37G213wu.n0.JPG17mv5.leaf | 65590d9ba88179c0... | 42,344 | 0.0038142 | c1624b384fe76e28... | none |
| pH11W37G133wu.n0.JPG17mv5.leaf | de73d7fd1033d9e4... | 37,093 | 0.0093308 | 1eb66a4a6670d960... | none |
| pH11W37G113wu.n0.0.JPG17mv5.leaf | 0da533b446d9ec72... | 37,257 | 0.0136923 | 74c8c2f714612dd7... | 15:12:b:m |
| pH11W37G153w.n0.2.JPG17mv5.leaf | d3242eb8d8360b8c... | 42,514 | 0.0157050 | 3920bd0f66cc9a06... | 12:15:b:p |
| pH11W37G233wu.n0.JPG17mv5.leaf | 838c01eeb468a003... | 35,380 | 0.0238523 | 098b4b113a72756a... | none |
| pH11W37G123wu.n0.JPG17mv5.leaf | 7bee5ac90644b009... | 32,589 | 0.0282176 | 48dfe3120163b150... | none |
| pH11W37G143wu.n0.JPG17mv5.leaf | 2c8dfd03de090c0a... | 34,243 | 0.0296192 | cb257f93631db958... | none |
| pH11W37G223wu.n0.JPG17mv5.leaf | 398c4aabed10efed... | 35,475 | 0.0314684 | a1ef36fd0f55ed25... | none |
| pH11W37G243wu.n0.JPG17mv5.leaf | f0234ac49e38a6d5... | 36,039 | 0.0367209 | 41ece83071bb3d2c... | none |
| pH11W37G153w.n0.1.0.JPG17mv5.leaf | 26131e36978c0f7b... | 46,814 | 8.2073772 | 5ddad665c26389f3... | 15:12:a:m |
| pH11W37G153w.n0.1.2.JPG17mv5.leaf | 0c92062041cbd52c... | 46,814 | 14.1996160 | 865d88129e161493... | 15:12:a:m |
| pH11W37G153w.n0.3.JPG17mv5.leaf | 38331558466f005f... | 47,915 | 20.9879962 | 4f335e928988fac0... | 12:15:a:p |
| pH11W37G153w.n0.1.1.JPG17mv5.leaf | 01adf32da5410831... | 46,080 | 26.9778932 | 91afc43ff4f2067e... | 15:12:a:m |
| pH11W37G113wu.n0.2.JPG17mv5.leaf | 0a5bd8ec17141a71... | 47,915 | 65.1076819 | a8129fe42774780a... | 12:15:a:p |
| pH11W37G113wu.n0.3.JPG17mv5.leaf | 02f226f73ca6d52e... | 47,915 | 251.7714290 | daeaece1ba5eb7bc... | 15:12:a:p |
| pH11W37G113wu.n0.1.JPG17mv5.leaf | 315747b99ba9bee1... | 47,915 | 1564.2689538 | 99d84d086d8990b1... | 12:15:b:p |

## What the statement is used for, and what it does not contain

- It is the local side's statement for this branch of case T **whichever statement of label 11 certifies**: the v5
  region contains the old target PB_11 and the new target HULLW_11 (`JOIN_ROOTS.md` top table and section 11.1,
  `ADMISSION_v4.md` section 9; `cmp_v5.py`). It serves the branch if the capture side certifies, for each of the
  twelve rigid labels j, a statement with the target of this region (PT_j, PM_j, the split statements PS_j^17 or
  PSS_j^17; for label 11 also PTW37_L11 or PSW37_L11 with k = 17), together with the statements for label 9 and the
  loose labels. The composition is `JOIN_ROOTS.md` sections 3 and 9.3; it is not repeated or proved here.
- The v5 region contains the region JPG17m v2 (equal outside label 11; `cmp_v5.py` part A), so this statement
  implies (E_JPG17m, v2), which was proved separately from the first tree at 01:06.
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
`reviews/join_roots/batch2/as_reviewed/RECORD_EJPG17m_v5.md` (sha256 946e380abe9e0bd7...); its scripts and outputs are in
`reviews/join_roots/batch2/` (`t_tree.py`, output `t_JPG17m_v5.out`; `v_regions.py`, `v_regions.out`). **Verdict: the statement may be called PROVED after the listed correction, a correction of wording.**
It recomputed, with its own code (the earlier reviewer's scripts made into one program and extended): every hash
the record names; the certificate line by line (header, counts, the tree conditions of SPEC 3.0 section 7, the
root node against the region file in the side interval, 68 box ends and 51 rotations, every cut as the record
words it); the child test of section 6 for all 30 children; the exclusion test of section 4.7 for
both option splits; the final store hashes of both acceptance reports from the node data, and the producer's two reports against
them node by node; every row of the table of leaves; the log.
On the region file (`v_regions.out`, 45 checks for the five regions): the v5 file against its v2 file (equal
outside label 11; label 11 of v5 contains label 11 of v2 and is larger by 46247/1000000 in xi_(11,1) and by
3.749992e-2 rad at the lower arc end), "the region in words" number by number, label 11 never cut and with the
root's box and arc in every node, the targets (the class PB_j is the same data in PT_j, PM_j, PS_j^k and PSS_j^k
for all twelve rigid labels; HULLW_11 the same in PTW37_L11, PSW37_L11_Tkk and PSSW37_L11_Tkk), and the reviewer's
own transport of the two targets: the factor of label 11 contains PB_11 and HULLW_11. This record was read
as differences from `RECORD_EJPG17p_v5.md`, the v5 record the reviewer took in depth; its tree had the full script.
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
ends 9.3e-10 rad inside the gate, so the region is that much larger than "BELOW its gate" says (the safe side, as in
the reviewed record of JPG17m v2); the sizes of the acceptance row are in binary units.
