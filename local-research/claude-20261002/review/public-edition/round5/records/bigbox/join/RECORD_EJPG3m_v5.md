Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line.

# Record: statement (E_JPG3m, v5) for the region JPG3m v5 ("the region JPG3m v5 is empty"): ACCEPTED 2026-10-10 07:33, PROVED 08:21

Lead of the window side. Status words as in `bigbox/THEOREM_G20.md`: COMPUTED / PROVED; ACCEPTED
means: accepted by both frozen checkers in the lead's acceptance run, the record not yet reviewed.

**STATUS: PROVED (2026-10-10 08:21) as a statement about the numbers of the region file** (status words of
`bigbox/THEOREM_G20.md`): the certificate is accepted by both frozen checkers with the lead's post-check (07:33),
and this record is reviewed by a reviewer that wrote none of it, nor the certificate, nor the tools
(`reviews/join_roots/batch2/REVIEW_BATCH2.md`, sha256 25227b662a3e6211..., one review of six records:
116 checks of its own on this certificate and 45 on the region files of the five regions (`v_regions.out`), none failed; its own reader of the certificate, its own
comparison of the root node with the region file, its own child and exclusion tests; verdict: may be called PROVED after one correction of wording (label 11 lies in the hull of its two targets, not in
their union), which touches neither the Statement, nor the certificate, nor the acceptance run, nor a number of
the tables; this version has it, section "Review").
Limits, as the reviewer states them: the soundness of SPEC 3.0 and of the two frozen checkers is taken from their
own reviews (`reviews/REVIEW_30*.md`), and with it the exact values L of the 22 `0` steps (the reviewer compared
them across the producer's and the acceptance reports of both programs and did not recompute them; the checkers
were not rerun); nobody but the producer has read how the leaves were made (not needed: the certificate is checked,
not the way it was made); outside label 11 the region file is the reviewed v2 file (the reviewer's exact comparison); for label 11 the
reviewer checked that the factor contains the v2 factor, the old target PB_11 and the new target HULLW_11
(`reviews/join_roots/batch2/v_regions.out`); the v5 generator and `cmp_v5.py` are not reviewed.
The record is written by `acceptance/mk_record.py` in the form of `RECORD_EJPG17m_v2.md` (reviewed at 01:03);
every number is taken from the files (facts output `acceptance/JPG3m_v5_facts.out`, sha256 10badce5c6043713..., of
`acceptance/region_facts.py`: all its checks ok), and the reviewer compared every number with its own reading of
the files.
**This is a statement about a region, NOT about a case of the proof:** that the capture side puts a packing into
this region needs its class statements, which are not certified.

## Statement

(E_JPG3m, v5). Let seventeen closed unit squares with pairwise disjoint interiors lie in [0, S]^2 with
S <= Sref = 4675530093604551/10^15, labelled 1 to 17, with one side direction a_i chosen for each square.
Then it is NOT the case that every xi_ik lies in the interval [lo_ik, hi_ik] and every a_i lies in the root arc of
label i, where the 34 intervals and the 17 arcs are those of

    bigbox/join/JPG3m_exact_v5.json   (entries window.box and root_arc)
    sha256 1e2a3b429193a69f9426e4966b8dbacb85e960b0301b926b8c645e191f6a867e

In words: no packing of seventeen unit squares of side at most Sref lies in the region JPG3m v5. Coordinates xi_ik as in SPEC 3.0 section 1, from the reference file `upper-packing-certificate.json`
(sha256 24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7, the one in the certificate's header, used
by both checkers); frame (container corner at the origin): SPEC 3.0 section 0.

This is the EMPTINESS COROLLARY of SPEC 3.0 (`SPEC_v3.0_NOTES.md`, note of 2026-10-09 18:38): the certificate
satisfies all conditions of section 7 and no node is closed as terminal, so the set F(root) is empty; and a
configuration that is feasible for a side S <= Sref is feasible for the side Sref (SPEC 3.0 section 11).

The region in words (`JOIN_ROOTS.md`, sections 1, 9.2, 9.3 and 11.1; arcs read from the region file, in rad from
each label's reference direction): case T of the join design: label 9 inside its gate [-0.099900, +0.099901], its box cut at the support end xi_(9,1) >= -9897/1000000; label 3 BELOW its gate, [-0.786228, -0.099917]; label 17 any direction; label 15 any direction; label 4 with any direction; the loose labels 3, 4, 15, 17 in their slots; the twelve rigid labels 1, 2, 5 to 8, 10 to 14, 16 in their boxes PB_j, **label 11 in one box and one arc that contain its old target PB_11 and its new target HULLW_11** (the hull of the v2 factor and the transported new target, `JOIN_ROOTS.md` section 11.1; more than the union of the two targets; tag v5: xi_(11,1) in [-140801/1000000, 12647/62500], direction in [-0.137499811, +0.204999690]).

## Evidence

| what | value |
|---|---|
| certificate | `local-research/claude-20261002/results/assembly/JPG3m_v5/JPG3m_v5.cert.jsonl.gz`, 137,008,711 bytes, sha256 7535735021ff18c43e84956180d0389e423ff863e5dd2e2cf661e227f0a94fd4; uncompressed stream 704cfc8cdb015c104599541fea55b214817b81b79c2ef357347eefd598319ab8 |
| its shape (read from the certificate) | 36 nodes, depth 7 in the Node checker's count (root = 0): 14 splits (9 arc, 0 box, 5 option) and 22 leaves closed by a `0` step; no terminal leaf; 22 steps, 993,869 terms, 832 declarations. Cuts: direction of label 15 cut 2 times (tan-half from its reference direction: -1/20, 1/20); direction of label 17 cut 7 times (tan-half from its reference direction: -1/20, 1/20, 563/2500); 3 option splits of the pair (12, 15) with 4 children; 1 option split of the pair (14, 17) with 2 children; 1 option split of the pair (8, 17) with 3 children. The description has no `recentre`: every split node has the root's centre for every label; the leaves keep their leaf files' own nodes, and 21 of the 36 nodes reach beyond the root node in some arc (list in the facts output), which SPEC 3.0 section 6 allows: a child only has to contain its piece. **Label 11 is never cut: its box and arc are the root's in every node.** |
| exact values of the `0` steps | all positive; the smallest is L = 2.922766e-03 at `pH11W37Gppmwuk5.n0.JPG3mv5.leaf`; the same rational number in both checkers' reports for each of the 22 leaves (table below) |
| producer | the audit lead: description by its `regiontree.py` (sha256 of the description e736aadb10aa1787...), certificate by the assembler `proto30/hull_tree.py` 8af834ec6ccff429... (exit 0, 1305.8 s). Its own run of both frozen checkers under `--keep-going`: 36 of 36 nodes accepted by each (`JPG3m_v5.run.json`, sha256 4bcbdb534314cfb0...) |
| acceptance run | `locks/run_slot.sh acceptance/accept_tree30.sh JPG3m_v5 <certificate> bigbox/join/EXPECT_JPG3m_v5.json`, by the lead, 2026-10-10 07:19:25 to 07:33 on the Mac. Python checker 692.41 s (698 MB), Node checker 133.09 s (1.29 GB) |
| log | `acceptance/ACCEPT_JPG3m_v5.log`, sha256 c0f07aba317e86e5a8d35c41e8150b0c0687d63096f21a368510c399ad14eb4f: `RESULT: ACCEPTED`, exit code of the run 0 |
| checker reports | `acceptance/JPG3m_v5_C1.json` (Python, sha256 6551c829b3afe0a2...), `acceptance/JPG3m_v5_C2.json` (Node, sha256 314cdc247edca8d4...) |
| frozen files | `checker/wxcheck_v30.py` cf8db52bfa1cc565..., `checker2/wxcheck2_v30.js` 97210adf74a3ebed..., `SPEC_v3.0.md` 0a6dfc2ae10ed6f3... (`acceptance/FROZEN_30.json`) |
| statement file | `bigbox/join/EXPECT_JPG3m_v5.json`, sha256 8d4ac066206f1538636e858fe828e066ac7a4f67df28cdf973f6b4bc858cf8b5: 17 labels, S_floor = Sref, `terminal_leaves` 0, `root_region` = the file above |

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
| pH11W37Gppmwuk5.n0.JPG3mv5.leaf | b1f2b29d937dcc52... | 48,504 | 0.0029228 | 66253b99969d80d8... | 17:8:a:p |
| pH11W37Gmpmwu.n0.0.JPG3mv5.leaf | a714469c238b379a... | 46,469 | 0.0030146 | 59404212a7f7016d... | 15:12:b:m |
| pH11W37G3pmwu.n0.JPG3mv5.leaf | 1f772f11749e9765... | 42,053 | 0.0031559 | fe7048f2d943f6fc... | none |
| pH11W37Gpmmwu.n0.JPG3mv5.leaf | ce96470f4dbdc0d7... | 46,303 | 0.0033566 | f1c02a493ac2bb55... | none |
| pH11W37Gppmwu.n0.0.1.0.JPG3mv5.leaf | 8418f32da91c3bf4... | 43,097 | 0.0063925 | 553431b687bb7885... | 8:17:b:m, 15:12:b:m |
| pH11W37Gppmwuk6.n0.JPG3mv5.leaf | dee05e82c8679940... | 43,427 | 0.0073248 | a83b75b9854d28f1... | 17:8:b:p |
| pH11W37Gmmmwu.n0.0.JPG3mv5.leaf | 395906970e3163b1... | 42,673 | 0.0074128 | d15a3580abb346f8... | 15:12:b:m |
| pH11W37Gm3mwu.n0.JPG3mv5.leaf | 3bdf385bf09a710d... | 40,076 | 0.0097808 | dcec42c50ac4f42e... | none |
| pH11W37Gppmwu.n0.0.0.JPG3mv5.leaf | ab1e6dfed497c36c... | 41,288 | 0.0148492 | 65cf1056ac4456cb... | 8:17:b:m |
| pH11W37Gp3mwu.n0.JPG3mv5.leaf | d7bc580590ceec7e... | 42,173 | 0.0150441 | 32fcc7ab915d285b... | none |
| pH11W37G3mmwu.n0.0.JPG3mv5.leaf | fab7511ab4d139a7... | 41,508 | 0.0167196 | 715d802d36e56e2e... | 14:17:a:p |
| pH11W37Gmpmwuk3.n0.JPG3mv5.leaf | deacda7b4eac3357... | 44,786 | 0.0363789 | 929530122d3d9941... | 12:15:b:p |
| pH11W37Gppmwuk4.n0.JPG3mv5.leaf | ad6a878cc9d03f7e... | 42,293 | 0.0366996 | c33f5a4916027860... | 8:17:b:m, 12:15:b:p |
| pH11W37Gmpmwuk4.n0.JPG3mv5.leaf | 2cf4df79a843c383... | 49,747 | 0.0370716 | 8607a07535f98720... | 12:15:a:p |
| pH11W37G33mwu.n0.JPG3mv5.leaf | 53c61d7d26fd67e8... | 39,016 | 0.0375721 | c2ed35ace875ed18... | none |
| pH11W37Gmmmwu.n0.3.JPG3mv5.leaf | 485e815dcb1a0f54... | 49,745 | 0.0393297 | 9dc3653a750644f4... | 12:15:a:p |
| pH11W37Gmpmwuk2.n0.JPG3mv5.leaf | 56c8611055607c15... | 47,831 | 0.0498670 | d4fe1b02818ae391... | 15:12:a:m |
| pH11W37Gppmwu.n0.0.1.1.JPG3mv5.leaf | 18a13fe5149f55fb... | 48,282 | 29.4979356 | 2a8423214987a84a... | 8:17:b:m, 15:12:a:m |
| pH11W37G3mmwu.n0.1.JPG3mv5.leaf | cf522dc5aceeb41c... | 46,816 | 66.0259372 | 3dece86208e84294... | 17:14:a:m |
| pH11W37Gppmwu.n0.0.1.2.JPG3mv5.leaf | d32d4aa0e690d177... | 48,282 | 158.3280916 | 2ca624e0942e2491... | 8:17:b:m, 12:15:a:p |
| pH11W37Gmmmwu.n0.1.JPG3mv5.leaf | 512ba1988ef0d147... | 49,750 | 226.2398383 | 1e2f4d211b5ea091... | 12:15:b:p |
| pH11W37Gmmmwu.n0.2.JPG3mv5.leaf | 702947d5863d80ed... | 49,750 | 449.1724283 | 43e216bc7dc305a1... | 15:12:a:p |

## What the statement is used for, and what it does not contain

- It is the local side's statement for this branch of case T **whichever statement of label 11 certifies**: the v5
  region contains the old target PB_11 and the new target HULLW_11 (`JOIN_ROOTS.md` top table and section 11.1,
  `ADMISSION_v4.md` section 9; `cmp_v5.py`). It serves the branch if the capture side certifies, for each of the
  twelve rigid labels j, a statement with the target of this region (PT_j, PM_j, the split statements PS_j^3 or
  PSS_j^3; for label 11 also PTW37_L11 or PSW37_L11 with k = 3), together with the statements for label 9 and the
  loose labels. The composition is `JOIN_ROOTS.md` sections 3 and 9.3; it is not repeated or proved here.
- The v5 region contains the region JPG3m v2 (equal outside label 11; `cmp_v5.py` part A), so this statement
  implies (E_JPG3m, v2).
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
`reviews/join_roots/batch2/as_reviewed/RECORD_EJPG3m_v5.md` (sha256 2add0b2f61345b59...); its scripts and outputs are in
`reviews/join_roots/batch2/` (`t_tree.py`, output `t_JPG3m_v5.out`; `v_regions.py`, `v_regions.out`). **Verdict: the statement may be called PROVED after the listed correction, a correction of wording.**
It recomputed, with its own code (the earlier reviewer's scripts made into one program and extended): every hash
the record names; the certificate line by line (header, counts, the tree conditions of SPEC 3.0 section 7, the
root node against the region file in the side interval, 68 box ends and 51 rotations, every cut as the record
words it); the child test of section 6 for all 35 children; the exclusion test of section 4.7 for
all 5 option splits; the final store hashes of both acceptance reports from the node data, and the producer's two reports against
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
this review did for the v5 file (remark 6d). Remarks of the reviewer that need no change: the root arc of label 3
ends 9.3e-10 rad inside the gate, so the region is that much larger than "BELOW its gate" says (the safe side, as in
the reviewed record of JPG17m v2); the sizes of the acceptance row are in binary units.
