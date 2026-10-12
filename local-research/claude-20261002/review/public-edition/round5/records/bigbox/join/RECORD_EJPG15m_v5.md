Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line.

# Record: statement (E_JPG15m, v5) for the region JPG15m v5 ("the region JPG15m v5 is empty"): ACCEPTED 2026-10-10 10:01, PROVED 10:15

Lead of the window side. Status words as in `bigbox/THEOREM_G20.md`: COMPUTED / PROVED; ACCEPTED
means: accepted by both frozen checkers in the lead's acceptance run, the record not yet reviewed.

**STATUS: PROVED (2026-10-10 10:15) as a statement about the numbers of the region file** (status words of
`bigbox/THEOREM_G20.md`): the certificate is accepted by both frozen checkers with the lead's post-check (10:01),
and this record is reviewed by a reviewer that wrote none of it, nor the certificate, nor the tools
(`reviews/join_roots/batch3/REVIEW_EJPG15m_v5.md`, sha256 77da7db7f81007c7...: 172 checks of its
own in two script runs, 132 on this certificate and 40 on the region files, none failed; its own reading of the
certificate with the earlier reviewers' program, extended; its own comparison of the root node with the region
file, child and exclusion tests; verdict: "PROVED: yes", no number, hash or claim of the record wrong; three
texts change with the status, section "Review").
Limits, as the reviewer states them: the soundness of SPEC 3.0 and of the two frozen checkers is taken from their
own reviews (`reviews/REVIEW_30*.md`), and with it the exact values L of the 39 `0` steps (the reviewer compared
them across the producer's and the acceptance reports of both programs and did not recompute them; the checkers
were not rerun); nobody but the producer has read how the leaves were made (not needed: the certificate is checked,
not the way it was made); outside label 11 the region file is the reviewed v2 file (the reviewer's exact
comparison); for label 11 the reviewer checked that the factor contains the v2 factor, the old target PB_11 and
the new target HULLW_11 (`reviews/join_roots/batch3/v_regions.out`); the v5 generator and `cmp_v5.py` are not
reviewed.
The record is written by `acceptance/mk_record.py` in the form of `RECORD_EJPG17m_v2.md` (reviewed at 01:03), with
the corrections of the review of batch 2 already in the generator; every number is taken from the files (facts
output `acceptance/JPG15m_v5_facts.out`, sha256 7a33e25381822625..., of `acceptance/region_facts.py`: all its checks ok), and
the reviewer compared every number with its own reading of the files.
**This is a statement about a region, NOT about a case of the proof:** that the capture side puts a packing into
this region needs its class statements, which are not certified.

## Statement

(E_JPG15m, v5). Let seventeen closed unit squares with pairwise disjoint interiors lie in [0, S]^2 with
S <= Sref = 4675530093604551/10^15, labelled 1 to 17, with one side direction a_i chosen for each square.
Then it is NOT the case that every xi_ik lies in the interval [lo_ik, hi_ik] and every a_i lies in the root arc of
label i, where the 34 intervals and the 17 arcs are those of

    bigbox/join/JPG15m_exact_v5.json   (entries window.box and root_arc)
    sha256 f6495dc60d07a4faead370a6af4b6f6e1c5f876c973f6dced71984b003f8aa06

In words: no packing of seventeen unit squares of side at most Sref lies in the region JPG15m v5. Coordinates xi_ik as in SPEC 3.0 section 1, from the reference file `upper-packing-certificate.json`
(sha256 24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7, the one in the certificate's header, used
by both checkers); frame (container corner at the origin): SPEC 3.0 section 0.

This is the EMPTINESS COROLLARY of SPEC 3.0 (`SPEC_v3.0_NOTES.md`, note of 2026-10-09 18:38): the certificate
satisfies all conditions of section 7 and no node is closed as terminal, so the set F(root) is empty; and a
configuration that is feasible for a side S <= Sref is feasible for the side Sref (SPEC 3.0 section 11).

The region in words (`JOIN_ROOTS.md`, sections 1, 9.2, 9.3 and 11.1; arcs read from the region file, in rad from
each label's reference direction): case T of the join design: label 9 inside its gate [-0.099900, +0.099901], its box cut at the support end xi_(9,1) >= -9897/1000000; label 3 inside its gate [-0.099917, +0.099917]; label 17 inside its gate [-0.099917, +0.099917]; label 15 BELOW its gate, [-0.786228, -0.099917]; label 4 with any direction; the loose labels 3, 4, 15, 17 in their slots; the twelve rigid labels 1, 2, 5 to 8, 10 to 14, 16 in their boxes PB_j, **label 11 in one box and one arc that contain its old target PB_11 and its new target HULLW_11** (the hull of the v2 factor and the transported new target, `JOIN_ROOTS.md` section 11.1; more than the union of the two targets; tag v5: xi_(11,1) in [-140801/1000000, 12647/62500], direction in [-0.137499811, +0.204999690]).

## Evidence

| what | value |
|---|---|
| certificate | `local-research/claude-20261002/results/assembly/JPG15m_v5/JPG15m_v5.cert.jsonl.gz`, 206,602,266 bytes, sha256 ed66c59b16b4b3549826311b8ba2b5be9c538e0235abab3cebb19789b9637c58; uncompressed stream d551253dcc44686ff826ac93841ae9a07ca614290c4e4d6a1a379621875648f9 |
| its shape (read from the certificate) | 61 nodes, depth 7 in the Node checker's count (root = 0): 22 splits (11 arc, 0 box, 11 option) and 39 leaves closed by a `0` step; no terminal leaf; 39 steps, 1,453,516 terms, 1443 declarations. Cuts: direction of label 15 cut 2 times (tan-half from its reference direction: -1341/5000, -659/5000); direction of label 4 cut 5 times (tan-half from its reference direction: -659/5000, 0, 659/5000); 8 option splits of the pair (12, 15) with 4 children; direction of label 14 cut 2 times (tan-half from its reference direction: 1/20); direction of label 16 cut 2 times (tan-half from its reference direction: -1/25); 3 option splits of the pair (14, 17) with 2 children. The description has no `recentre`: every split node has the root's centre for every label; the leaves keep their leaf files' own nodes, and 37 of the 61 nodes reach beyond the root node in some arc (list in the facts output), which SPEC 3.0 section 6 allows: a child only has to contain its piece. **Label 11 is never cut: its box and arc are the root's in every node.** |
| exact values of the `0` steps | all positive; the smallest is L = 2.831597e-03 at `pH11W37G323wur.n0.JPG15mv5.leaf`; the same rational number in both checkers' reports for each of the 39 leaves (table below) |
| producer | the audit lead: description by its `regiontree.py` (sha256 of the description 4d770a3b59cf2cb3...), certificate by the assembler `proto30/hull_tree.py` 8af834ec6ccff429... (exit 0, 1701.9 s). Its own run of both frozen checkers under `--keep-going`: 61 of 61 nodes accepted by each (`JPG15m_v5.run.json`, sha256 1cb536ae943c7d96...) |
| acceptance run | `locks/run_slot.sh acceptance/accept_tree30.sh JPG15m_v5 <certificate> bigbox/join/EXPECT_JPG15m_v5.json`, by the lead, 2026-10-10 09:42:46 to 10:01 on the Mac. Python checker 909.52 s (582 MB), Node checker 181.00 s (1.78 GB) |
| log | `acceptance/ACCEPT_JPG15m_v5.log`, sha256 8a730ba214eb83988c35de09aefde1a72920b0eee6b75a513d19085b757789a0: `RESULT: ACCEPTED`, exit code of the run 0 |
| checker reports | `acceptance/JPG15m_v5_C1.json` (Python, sha256 6271c6f81c542acc...), `acceptance/JPG15m_v5_C2.json` (Node, sha256 5e64d909aade8ef8...) |
| frozen files | `checker/wxcheck_v30.py` cf8db52bfa1cc565..., `checker2/wxcheck2_v30.js` 97210adf74a3ebed..., `SPEC_v3.0.md` 0a6dfc2ae10ed6f3... (`acceptance/FROZEN_30.json`) |
| statement file | `bigbox/join/EXPECT_JPG15m_v5.json`, sha256 b6b3ba8dd075a735d15a3cf31a0aee7b58ff6988129e3bc89eb0bb8cd6798d13: 17 labels, S_floor = Sref, `terminal_leaves` 0, `root_region` = the file above |

Lines of the log that carry the statement: both checkers, started with their default options, exit 0 with PASS on
the whole file; every node accepted by both; same node ids and the same closure kind per node in both reports;
nodes 61, infeasible 39, split 22, terminal 0; the root node has parent null, an empty assumption list, the
region's side interval, the region's box in all 68 interval ends and the region's arc for every label (centre and
both end rotations).

The 39 leaves closed by a `0` step (L from the Python report; "L sha256" = sha256 of the fraction as the report
writes it; in every row the Node report has the same rational number and the audit lead's assembler
report the same fraction, `L_exact`; all placed by containment, `LEAF_FORMAT_RULING.md`):

| leaf node | leaf file sha256 | terms | L | L sha256 | options assumed |
|---|---|---|---|---|---|
| pH11W37G323wur.n0.JPG15mv5.leaf | bcc659fcc479450e... | 41,284 | 0.0028316 | fc2a1b38aeadcc01... | none |
| pH11W37G313wk5k2.n0.0.JPG15mv5.leaf | be4fac5c5a307336... | 30,340 | 0.0041946 | 4f5fe9ee2a352817... | 15:12:b:m |
| pH11W37G313wk5k4k4r.n0.0.JPG15mv5.leaf | 06169816bc3b57dc... | 32,116 | 0.0042060 | da1cad823d74776c... | 15:12:b:m |
| pH11W37G313wk6.n0.0.0.JPG15mv5.leaf | c21c933b62bafb75... | 35,211 | 0.0044779 | 6df48760ef6bb1d9... | 15:12:b:m |
| pH11W37G313w.n0.0.0.0.JPG15mv5.leaf | c7842e5b83d51c83... | 32,585 | 0.0048845 | 36afb56d4686244f... | 15:12:b:m |
| pH11W37G313wk5k3.n0.0.JPG15mv5.leaf | 19412f55da7baa64... | 31,310 | 0.0057259 | 829cd18b521b2eb8... | 15:12:b:m |
| pH11W37G313wk5k4k5r.n0.0.JPG15mv5.leaf | 6726c68f0727302d... | 31,633 | 0.0057266 | d5340da80a73e08a... | 15:12:b:m |
| pH11W37G313wk5k4.n0.0.0.0.JPG15mv5.leaf | 28c7d19c85fb2427... | 32,295 | 0.0138529 | a8b90b386b7dfebb... | 15:12:b:m |
| pH11W37G313wk5k1.n0.0.JPG15mv5.leaf | fe4419c461b4d746... | 35,310 | 0.0138944 | 5b38df2ab76474fa... | 15:12:b:m |
| pH11W37G313wk5k5.n0.1.JPG15mv5.leaf | e919c8012a8e3dcf... | 29,749 | 0.0181770 | ed388d91edee3d83... | 14:17:a:p |
| pH11W37G313wk5k5.n0.0.JPG15mv5.leaf | 36dc3d81d00b8f16... | 30,363 | 0.0200935 | 8246f9b42fcf83a5... | 17:14:a:m |
| pH11W37G313wk6.n0.1.0.JPG15mv5.leaf | 0877d1ded2a5e1bb... | 32,635 | 0.0206920 | df5f2ca617b280a4... | 17:14:a:m |
| pH11W37G313wk4.n0.0.JPG15mv5.leaf | e5765d5e9768d64d... | 31,358 | 0.0208603 | 8ff81188499f626e... | 17:14:a:m |
| pH11W37G313wk6.n0.1.1.JPG15mv5.leaf | d60f6dc2318b4cbe... | 33,616 | 0.0221368 | b294ef4318542f39... | 14:17:a:p |
| pH11W37G313wk4.n0.1.JPG15mv5.leaf | 4214c5d430b6d99b... | 29,487 | 0.0268548 | 72eca1d300fe4567... | 14:17:a:p |
| pH11W37G313wk5k1.n0.3.JPG15mv5.leaf | 3781816ea870acd8... | 29,112 | 0.0322371 | 06b0904130b95654... | 12:15:a:p |
| pH11W37G313wk5k4k3.n0.JPG15mv5.leaf | 1f77197687488a8a... | 31,243 | 0.0322445 | 429962dbb55031d2... | 12:15:a:p |
| pH11W37G313wk6.n0.0.3.JPG15mv5.leaf | 1415c2e4e67874cd... | 37,387 | 0.0323403 | 4b0636829a99807d... | 12:15:a:p |
| pH11W37G313w.n0.0.0.3.JPG15mv5.leaf | 27fadd8b80a33b00... | 38,222 | 0.0326301 | 08da7d8afe301ce5... | 12:15:a:p |
| pH11W37G313wk5k3.n0.3.JPG15mv5.leaf | 5410d1847d768611... | 31,388 | 0.0344495 | 5a20051b7b37431a... | 12:15:a:p |
| pH11W37G313wk5k4k5r.n0.3.JPG15mv5.leaf | e7f505307c32dc61... | 32,722 | 0.0344528 | c33e59a1c13c0da3... | 12:15:a:p |
| pH11W37G313wk5k4.n0.0.0.1.JPG15mv5.leaf | c53a04fe47edf1f5... | 42,412 | 12.4945157 | 4800b03ab352f01f... | 12:15:b:p |
| pH11W37G313wk6.n0.0.1.JPG15mv5.leaf | 5b549d114b08dc89... | 43,146 | 46.9784974 | 7be6a9c25dbaf4ff... | 12:15:b:p |
| pH11W37G313wk5k2.n0.2.JPG15mv5.leaf | 909889f5e9a36431... | 42,045 | 123.7516875 | 64e686c9a6f52fa3... | 12:15:a:p |
| pH11W37G313wk5k4k4r.n0.1.JPG15mv5.leaf | c422cece4add7a43... | 42,045 | 128.3984871 | 40fbb39bdac90d59... | 12:15:b:p |
| pH11W37G313wk5k2.n0.1.JPG15mv5.leaf | 094ee7c657e8c81e... | 42,045 | 161.3298286 | d4c9a52b92a0cf57... | 12:15:b:p |
| pH11W37G313wk5k1.n0.1.JPG15mv5.leaf | 774448dfb439a90e... | 42,412 | 218.2541409 | 9ae9ee592111757f... | 12:15:b:p |
| pH11W37G313w.n0.0.0.1.JPG15mv5.leaf | 8367274fe91918b5... | 43,146 | 229.3367377 | d31555388cf31400... | 12:15:b:p |
| pH11W37G313wk5k4k4r.n0.2.JPG15mv5.leaf | 14010a856d766d6c... | 42,045 | 345.1169793 | 81e0f12b5f546351... | 12:15:a:p |
| pH11W37G313wk5k3.n0.1.JPG15mv5.leaf | c8a5fe7e8f5d62b1... | 42,412 | 567.9767797 | 6b80a3b8aec766b4... | 12:15:b:p |
| pH11W37G313wk6.n0.0.2.JPG15mv5.leaf | b549bea90fab8e03... | 43,146 | 628.3536891 | 6f2c734d10cfde04... | 15:12:a:p |
| pH11W37G313wk5k3.n0.2.JPG15mv5.leaf | 15b0a77f1549dc1e... | 42,412 | 1425.4781449 | 42f95d3a4c54727a... | 15:12:a:p |
| pH11W37G313wk5k4k4r.n0.3.JPG15mv5.leaf | 3c797535470eb817... | 42,045 | 1443.0522692 | 3c411a5dd4c7e83d... | 15:12:a:p |
| pH11W37G313wk5k1.n0.2.JPG15mv5.leaf | 509dc538b2ec3c54... | 42,412 | 1451.5648095 | 0b43371262b6857d... | 15:12:a:p |
| pH11W37G313w.n0.0.0.2.JPG15mv5.leaf | 1c6f1f00f6787f0f... | 43,146 | 1468.1788974 | 5fce192f3d11d2fc... | 15:12:a:p |
| pH11W37G313wk5k4k5r.n0.1.JPG15mv5.leaf | 2f8f2f3f4deced95... | 42,412 | 1555.0869636 | a246e371341c96d3... | 12:15:b:p |
| pH11W37G313wk5k2.n0.3.JPG15mv5.leaf | babdb91b440cb658... | 42,045 | 1587.3037927 | 5b4785a03e4ba343... | 15:12:a:p |
| pH11W37G313wk5k4k2.n0.JPG15mv5.leaf | e4829b844a00987a... | 42,412 | 2406.9720775 | 8b2e889241c030bd... | 15:12:a:p |
| pH11W37G313wk5k4k5r.n0.2.JPG15mv5.leaf | 99510f7a97c9cb71... | 42,412 | 4207.3612469 | 68fc66b88d5caaf2... | 15:12:a:p |

## What the statement is used for, and what it does not contain

- It is the local side's statement for this branch of case T **whichever statement of label 11 certifies**: the v5
  region contains the old target PB_11 and the new target HULLW_11 (`JOIN_ROOTS.md` top table and section 11.1,
  `ADMISSION_v4.md` section 9; `cmp_v5.py`). It serves the branch if the capture side certifies, for each of the
  twelve rigid labels j, a statement with the target of this region (PT_j, PM_j, the split statements PS_j^15 or
  PSS_j^15; for label 11 also PTW37_L11 or PSW37_L11 with k = 15), together with the statements for label 9 and the
  loose labels. The composition is `JOIN_ROOTS.md` sections 3 and 9.3; it is not repeated or proved here.
- The v5 region contains the region JPG15m v2 (equal outside label 11; `cmp_v5.py` part A), so this statement
  implies (E_JPG15m, v2).
- The tree consists of second-tree leaves made on the v5 root only; label 11 is not cut anywhere.
- NOT contained: that the capture side puts a packing of this branch into the region (no class statement of the
  branch is certified), and the correctness of the region file against the class files (the v5 files are checked
  by 2,552 exact self-checks and against Codex's drafts, `ADMISSION_v4.md`; the reviewer of this record compared
  the v5 file with its reviewed v2 file, equal outside label 11, and checked that the factor of label 11 contains
  the v2 factor, PB_11 and HULLW_11, `reviews/join_roots/batch3/v_regions.out`; the v5 generator and `cmp_v5.py`
  are not reviewed).

## Review

Reviewed 2026-10-10 by a reviewer that wrote none of the record, of the certificate or of the tools:
`reviews/join_roots/batch3/REVIEW_EJPG15m_v5.md` (sha256
77da7db7f81007c7765dc852b9aeec672c4ea4e4579cd5d587d0c40c43be722a); the text it read is kept as
`reviews/join_roots/batch3/as_reviewed/RECORD_EJPG15m_v5.md` (sha256 473ec02ea7e28d54...); its scripts and outputs
are in `reviews/join_roots/batch3/` (`t_tree.py`, output `t_JPG15m_v5.out`; `v_regions.py`, `v_regions.out`).
**Verdict: "PROVED: yes". No number, no hash and no claim of the record is wrong; nothing was found that touches
all region trees.**
It recomputed, with its own run of the earlier reviewers' program (extended; 132 checks on the certificate, read
line by line): every hash the record names; header and counts; the tree conditions of SPEC 3.0 section 7; the
root node against the region file (side interval, 68 box ends, 51 rotations); every cut as the record words it,
each strictly inside its node's arc; the child test of section 6 for all 60 children; the exclusion test of
section 4.7 for all 11 option splits (each on a node with an empty assumption list; the four omitted options of
the pair (12, 15) excluded with margins 1.2002 to 1.5197, the six of the pair (14, 17) with 0.1302 to 1.8631);
label 11 never cut and with the root's box and arc in all 61 nodes; the final store hashes of both acceptance
reports for all 61 nodes, and the producer's two reports against them node by node; all 39 rows of the table of
leaves; the log; "the region in words" number by number. On the region file (40 checks): the v5 file against
`JPG15m_exact_v2.json` (equal outside label 11; label 11 contains the v2 factor and is the same data as in the
five other v5 files; by its own transport the factor contains PB_11 and HULLW_11); JPG15m and JPG15p are the same
data in every label other than 15, whose two arcs are exact mirror images; the targets for k = 15.
It did not rerun the two frozen checkers or the acceptance script (the frozen checkers have run on
these bytes twice: the producer's run with `--keep-going` and my acceptance run with the default options).

The three texts that changed with the status, all in this version (10:15): the status paragraph with the limits
sentence (finding 1); the last point of "used for", which now says what this review did for the v5 file (finding
2); this section (finding 3). No correction of a number or of the Statement was asked.
Remarks of the reviewer that need no change: the 37 nodes that reach beyond the root are all leaves, 85 arcs in
all, by 4.673e-6 to 7.204e-6 rad (labels 4, 14, 15, 16; the largest at label 16, a little above the 6.5e-6 of the
earlier trees), nothing above 1e-5 rad and none in a box interval; the root arc of label 15 ends 9.3e-10 rad
inside the gate, so the region is that much larger than "BELOW its gate" says (the safe side); the sizes of the
acceptance row are in binary units and cut down, not rounded (582 MB is 611,303,424 bytes); the producer's two
checker runs read a copy of the certificate with the same sha256 and stream hash as the file on disk.
