Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line.

# Record: statement (E_JPW13, v2x) for the region JPW13 v2x ("the region JPW13 v2x is empty"): ACCEPTED 2026-10-10 14:57, PROVED 15:21

Lead of the window side. Status words as in `bigbox/THEOREM_G20.md`: COMPUTED / PROVED; ACCEPTED
means: accepted by both frozen checkers in the lead's acceptance run, the record not yet reviewed.

**STATUS: PROVED (2026-10-10 15:21) as a statement about the numbers of the region file** (status words of
`bigbox/THEOREM_G20.md`): the certificate is accepted by both frozen checkers with the lead's post-check (14:57),
and this record is reviewed by a reviewer that wrote none of it, nor the certificate, nor the tools
(`reviews/join_roots/batch5/REVIEW_EJPW13_v2x.md`, sha256 2de8ae1b9d0c7ad1...: its own run of the
earlier reviewers' program on this certificate, unchanged, 125 checks, 124 ok and one FAIL that is no defect (the
program does not know the digest of Codex's manifest that the last section quotes); by hand the corollary, the
statement file, "the region in words" number by number and every claim of the section on use; a sample of six
leaves against the root; verdict: "PROVED after corrections", one correction, C1, in the section on use, made in
this version; no wrong number found in the Statement, the Evidence table or the leaf table, and the statement does
not depend on C1).
Limits, as the reviewer states them: it did not run the two checkers, so that each `0` step is valid (7,133,642
terms) and the exact values L rest on the two frozen checkers (its run ties their reports to the bytes on disk and
to each other and does not redo their arithmetic); the program it ran is the earlier reviewers', of which it read
about 140 of 961 lines; not checked: the region file against the class files, the capture side (PW_j, L_j, the
composition, the use of the wall lemma beyond its inequality), `mk_record.py` and `region_facts.py`, Codex's
manifest beyond the sixteen names quoted, and the 157 leaves outside its sample other than through the program.
As for every record of this kind, the soundness of SPEC 3.0 and of the two frozen checkers is taken from their own
reviews (`reviews/REVIEW_30*.md`), and nobody but the producer has read how the leaves were made (not needed: the
certificate is checked, not the way it was made).
The record is written by `acceptance/mk_record.py` (its branch for wall regions, first used here) in the form of
`RECORD_EJPG17m_v2.md` (reviewed at 01:03); every number is taken from the files (facts output
`acceptance/JPW13_v2x_facts.out`, sha256 134a2b48b957834f..., of `acceptance/region_facts.py`: all its checks ok), and the
reviewer compared the numbers with its own reading of the files.
**This is a statement about a region, NOT about a case of the proof:** that the capture side puts a packing into
this region needs its class statements (the wall statements and the family L statements; their state is the capture
side's bookkeeping, quoted in the last section and not checked here).

## Statement

(E_JPW13, v2x). Let seventeen closed unit squares with pairwise disjoint interiors lie in [0, S]^2 with
S <= Sref = 4675530093604551/10^15, labelled 1 to 17, with one side direction a_i chosen for each square.
Then it is NOT the case that every xi_ik lies in the interval [lo_ik, hi_ik] and every a_i lies in the root arc of
label i, where the 34 intervals and the 17 arcs are those of

    bigbox/join/JPW13_exact_v2x.json   (entries window.box and root_arc)
    sha256 e1a489e1f0d04ec0ee091ccbab9c4028a08c04ec15deeea26ff738e62b09505b

In words: no packing of seventeen unit squares of side at most Sref lies in the region JPW13 v2x. Coordinates xi_ik as in SPEC 3.0 section 1, from the reference file `upper-packing-certificate.json`
(sha256 24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7, the one in the certificate's header, used
by both checkers); frame (container corner at the origin): SPEC 3.0 section 0.

This is the EMPTINESS COROLLARY of SPEC 3.0 (`SPEC_v3.0_NOTES.md`, note of 2026-10-09 18:38): the certificate
satisfies all conditions of section 7 and no node is closed as terminal, so the set F(root) is empty; and a
configuration that is feasible for a side S <= Sref is feasible for the side Sref (SPEC 3.0 section 11).

The region in words (`JOIN_ROOTS.md`, sections 2.4, 9.3 and 9.4; arcs read from the region file, in rad from
each label's reference direction): the case "wall above" of the join design: label 9 in the wall column (class-frame x <= 53/100) with y >= 13/5, box xi_(9,1) in [-204203/1000000, -174437/1000000], xi_(9,2) in [-52219/500000, 259263/1000000], in the wall pose [-0.756708, -0.632747] (the x axis +- 2 atan(31/1000)); the loose labels 3, 4, 15, 17 in their loose slots, each with any direction; the twelve rigid labels 1, 2, 5 to 8, 10 to 14, 16 in their hull boxes HULL_j.

## Evidence

| what | value |
|---|---|
| certificate | `local-research/claude-20261002/results/assembly/JPW13/JPW13.cert.jsonl.gz`, 969,247,519 bytes, sha256 7147d7780da9006064160c6b49a4196678bcc20cd31234f1b3a0a4c54fcc050b; uncompressed stream 134a56c888a6f39ea3c364be34e21c22000f0fa49763d020bbc1e7e7efc5b6d3 |
| its shape (read from the certificate) | 255 nodes, depth 12 in the Node checker's count (root = 0): 92 splits (43 arc, 0 box, 49 option) and 163 leaves closed by a `0` step; no terminal leaf; 163 steps, 7,133,642 terms, 6150 declarations. Cuts: direction of label 3 cut 2 times (tan-half from its reference direction: -659/5000, 659/5000); direction of label 15 cut 11 times (tan-half from its reference direction: -659/5000, 659/5000, 1341/5000); direction of label 17 cut 18 times (tan-half from its reference direction: -659/5000, 659/5000); 27 option splits of the pair (14, 17) with 3 / 4 children; 17 option splits of the pair (12, 15) with 4 children; 3 option splits of the pair (9, 11) with 2 children; direction of label 4 cut 12 times (tan-half from its reference direction: -659/5000, 659/5000); 2 option splits of the pair (6, 14) with 2 children. The description has no `recentre`: every split node has the root's centre for every label; the leaves keep their leaf files' own nodes, and 159 of the 255 nodes reach beyond the root node in some arc (list in the facts output), which SPEC 3.0 section 6 allows: a child only has to contain its piece. Label 11 is never cut: its box and arc are the root's in every node. |
| exact values of the `0` steps | all positive; the smallest is L = 2.900610e-04 at `pV100w.n0.0.JPW13v2x.leaf`; the same rational number in both checkers' reports for each of the 163 leaves (table below) |
| producer | the audit lead: description by its `regiontree.py` (sha256 of the description 763aafe9fe2790cc...), certificate by the assembler `proto30/hull_tree.py` 8af834ec6ccff429... (exit 0, 7813.1 s). Its own run of both frozen checkers under `--keep-going`: 255 of 255 nodes accepted by each (`JPW13.run.json`, sha256 e73048beaa2e19db...) |
| acceptance run | `locks/run_slot.sh acceptance/accept_tree30.sh JPW13_v2x <certificate> bigbox/join/EXPECT_JPW13_v2x.json`, by the lead, 2026-10-10 13:24:48 to 14:57 on the Mac. Python checker 4591.59 s (692 MB), Node checker 927.80 s (2.40 GB) |
| log | `acceptance/ACCEPT_JPW13_v2x.log`, sha256 8465744dfb265f4b2a8c94104d564f6de6b66b5d5fcb38f6a5165fed63c94dfb: `RESULT: ACCEPTED`, exit code of the run 0 |
| checker reports | `acceptance/JPW13_v2x_C1.json` (Python, sha256 eab92bd7f2c80a24...), `acceptance/JPW13_v2x_C2.json` (Node, sha256 2fb3c2e957b02e5b...) |
| frozen files | `checker/wxcheck_v30.py` cf8db52bfa1cc565..., `checker2/wxcheck2_v30.js` 97210adf74a3ebed..., `SPEC_v3.0.md` 0a6dfc2ae10ed6f3... (`acceptance/FROZEN_30.json`) |
| statement file | `bigbox/join/EXPECT_JPW13_v2x.json`, sha256 b6a33b674b48363420afb2b2c1e1cac4c3cba86300cf048a6074b5920bd9e891: 17 labels, S_floor = Sref, `terminal_leaves` 0, `root_region` = the file above |

Lines of the log that carry the statement: both checkers, started with their default options, exit 0 with PASS on
the whole file; every node accepted by both; same node ids and the same closure kind per node in both reports;
nodes 255, infeasible 163, split 92, terminal 0; the root node has parent null, an empty assumption list, the
region's side interval, the region's box in all 68 interval ends and the region's arc for every label (centre and
both end rotations).

The 163 leaves closed by a `0` step (L from the Python report; "L sha256" = sha256 of the fraction as the report
writes it; in every row the Node report has the same rational number and the audit lead's assembler
report the same fraction, `L_exact`; all placed by containment, `LEAF_FORMAT_RULING.md`):

| leaf node | leaf file sha256 | terms | L | L sha256 | options assumed |
|---|---|---|---|---|---|
| pV100w.n0.0.JPW13v2x.leaf | 8e8fb32421511788... | 43,700 | 0.0002901 | 135b4e12d1812456... | 14:17:a:p |
| pV150w.n0.0.1.1.0.JPW13v2x.leaf | 2282b57fedd30143... | 41,484 | 0.0007988 | e55fae4204aa5bd8... | 14:17:a:p, 15:12:b:m |
| pV101w.n0.0.JPW13v2x.leaf | b9eae0dfd5c07300... | 45,785 | 0.0013917 | a74c9c506abb3f4a... | 14:17:a:p |
| pV101w.n0.2.JPW13v2x.leaf | ca386d4fce00118b... | 45,380 | 0.0014569 | 6ff807b1f61558d4... | 17:14:b:m |
| pV515w.n0.0.JPW13v2x.leaf | 2226991a3cce01e1... | 43,040 | 0.0015123 | fbbb85fdf9252249... | 14:17:a:p |
| pV515w.n0.1.JPW13v2x.leaf | ca5df6e59878c1bd... | 43,136 | 0.0015141 | 4b3b74a29bf690a9... | 17:14:a:m |
| pV115w.n0.0.JPW13v2x.leaf | 7dd7de6a82104c4d... | 44,547 | 0.0015816 | 551d87cd53f44063... | 14:17:a:p |
| pV111w.n0.0.JPW13v2x.leaf | 111059156076381c... | 44,813 | 0.0015842 | 73c95decb86e25fd... | 14:17:a:p |
| pV550wk5k2.n0.JPW13v2x.leaf | 4ab81ab292859b06... | 41,739 | 0.0020871 | a5da0a9d1e3e120b... | 17:14:a:m, 12:15:b:p |
| pV500w.n0.0.JPW13v2x.leaf | 7471a752adcd2e88... | 40,897 | 0.0020926 | 56032ed236562527... | 14:17:a:p |
| pV500w.n0.1.JPW13v2x.leaf | fced4d23a4bb3420... | 38,380 | 0.0021039 | 54fa930e48225069... | 17:14:a:m |
| pV550wk2.n0.JPW13v2x.leaf | a8e2b1d334b5a95e... | 41,439 | 0.0021524 | b004d1f711c26ad3... | 14:17:a:p, 12:15:b:p |
| pV111w.n0.2.JPW13v2x.leaf | 15270c1c12899df6... | 44,877 | 0.0025018 | 6946cc99b8b62d3c... | 17:14:b:m |
| pV115w.n0.2.JPW13v2x.leaf | 7b0028eaa731a01b... | 44,988 | 0.0026656 | 56b0098bf828be0c... | 17:14:b:m |
| pV050w.n0.0.1.1.0.JPW13v2x.leaf | b352a083227dea59... | 39,288 | 0.0032953 | b50137ffa51c40fc... | 14:17:a:p, 15:12:b:m |
| pV105w.n0.0.JPW13v2x.leaf | 7cc53063d05902fd... | 45,490 | 0.0033527 | 48028da0a3b250fa... | 14:17:a:p |
| pV501w.n0.0.JPW13v2x.leaf | a566933abc0b4abd... | 40,551 | 0.0034493 | 6119887fc8304e9d... | 14:17:a:p |
| pV511w.n0.1.JPW13v2x.leaf | a130ebbac9b540fc... | 44,266 | 0.0036185 | 6880755fc71c18e5... | 17:14:a:m |
| pV511w.n0.0.JPW13v2x.leaf | 14ffe5ce3f2b336d... | 44,149 | 0.0036686 | b9c0a74aac895c85... | 14:17:a:p |
| pV110w.n0.2.JPW13v2x.leaf | 68df8ad1bf239f64... | 46,047 | 0.0036880 | 4e3321e8a396f2a7... | 17:14:b:m |
| pV105w.n0.2.JPW13v2x.leaf | 192ed9fe88bad224... | 45,561 | 0.0037345 | f2d43ed1d954eb4a... | 17:14:b:m |
| pV501w.n0.1.JPW13v2x.leaf | 1d30b06ab7d43fc4... | 42,830 | 0.0037867 | 66534d03de6de159... | 17:14:a:m |
| pV150wk1.n0.2.JPW13v2x.leaf | 18ce0b86c856cd86... | 40,674 | 0.0039447 | 044aa21fbb039b93... | 17:14:b:m, 12:15:b:p |
| pV150w.n0.0.1.1.2.JPW13v2x.leaf | 32d24b676fcb9ab2... | 36,835 | 0.0039516 | 66b0aa3575503618... | 14:17:a:p, 12:15:b:p |
| pV555w.n0.1.0.JPW13v2x.leaf | d8235d2d4938e23e... | 42,043 | 0.0040434 | c140e6d91b1a4bcc... | 17:14:a:m, 15:12:b:m |
| pV555w.n0.0.0.JPW13v2x.leaf | 7a73bf424205a090... | 41,299 | 0.0041538 | e441226a53e6bc07... | 14:17:a:p, 15:12:b:m |
| pV050w.n0.0.2.JPW13v2x.leaf | 32ca3dc21d894135... | 42,192 | 0.0042464 | 650d1fa25e0b2871... | 14:17:a:p |
| pV050w.n0.0.1.1.3.JPW13v2x.leaf | 7c2f5f6f983745c7... | 35,744 | 0.0043754 | 163fef4f500afd44... | 14:17:a:p, 12:15:b:p |
| pV510w.n0.0.JPW13v2x.leaf | 6a79efa98716558e... | 44,358 | 0.0043981 | 4cd9605f339bae19... | 14:17:a:p |
| pV510w.n0.1.JPW13v2x.leaf | e61803def4b62a36... | 44,001 | 0.0045040 | db97baca57f0180d... | 17:14:a:m |
| pV010w.n0.1.JPW13v2x.leaf | e670fbf27de05e30... | 39,064 | 0.0048463 | b447e73fbe410cd9... | 17:14:a:m |
| pV050w.n0.1.JPW13v2x.leaf | 584fa46e6de12ece... | 38,777 | 0.0049297 | 0ccd10236c12f5bb... | 17:14:a:m |
| pV505w.n0.1.JPW13v2x.leaf | accf721833385553... | 40,698 | 0.0050313 | 18934a62f8c97c44... | 17:14:a:m |
| pV505w.n0.0.JPW13v2x.leaf | f543581eec59ad7e... | 42,591 | 0.0051153 | a59a87daccecdd44... | 14:17:a:p |
| pV550wk5.n0.1.0.JPW13v2x.leaf | 806d70a059fb9da6... | 40,437 | 0.0052176 | 43b1e7a1eb8c2cfb... | 17:14:a:m |
| pV150w.n0.0.2.JPW13v2x.leaf | 36ee152ec71cfdb1... | 42,496 | 0.0054092 | 5f88c906b5161cd8... | 14:17:a:p |
| pV550w.n0.0.1.0.JPW13v2x.leaf | a90ba8bbc8dcd5a6... | 39,396 | 0.0054278 | 880ae276aea46f42... | 14:17:a:p |
| pV000w.n0.0.JPW13v2x.leaf | 2adb96bc80252666... | 40,051 | 0.0054604 | 2b11d9ef636cace2... | 14:17:a:p |
| pV155wr.n0.0.0.JPW13v2x.leaf | 4d7a90ea8fc25679... | 42,969 | 0.0060760 | f71eda24d8b38d5b... | 14:17:a:p, 15:12:b:m |
| pV550wk5.n0.0.JPW13v2x.leaf | 653c328de4f40ca7... | 42,078 | 0.0067535 | 54d965e6cf7f69f6... | 17:14:a:m |
| pV550w.n0.0.0.JPW13v2x.leaf | 8e22ec840e054f11... | 42,687 | 0.0069152 | 0b08b0f03b362ed3... | 14:17:a:p |
| pV155wr.n0.2.0.JPW13v2x.leaf | 548236f83a1b65b6... | 42,768 | 0.0069317 | d02c639819574131... | 17:14:b:m, 15:12:b:m |
| pV551w.n0.1.0.JPW13v2x.leaf | e65451d482c00010... | 41,687 | 0.0069322 | 19ea3634a122b359... | 17:14:a:m, 15:12:b:m |
| pV551w.n0.0.0.JPW13v2x.leaf | d2f07584c9c5aec0... | 42,049 | 0.0071980 | f863f076c2aa8315... | 14:17:a:p, 15:12:b:m |
| pV150w.n0.0.1.0.JPW13v2x.leaf | d161461ee5f9b202... | 40,509 | 0.0072613 | b2c7dadf0c05b0bb... | 14:17:a:p |
| pV150wk1.n0.0.0.JPW13v2x.leaf | 5d5c87710e10fcc8... | 40,184 | 0.0072665 | 9809f9acedac157f... | 17:14:b:m, 15:12:b:m, 11:9:b:p |
| pV151w.n0.0.0.JPW13v2x.leaf | 2c1e2ef15396b96a... | 40,218 | 0.0073577 | 7ddb04cc9e0b85bc... | 14:17:a:p, 15:12:b:m |
| pV151w.n0.2.0.JPW13v2x.leaf | 6a3931197fbec8b7... | 41,909 | 0.0083250 | 08f79989ddb9ac0b... | 17:14:b:m, 15:12:b:m |
| pV100wk1.n0.JPW13v2x.leaf | d432768461135fee... | 38,904 | 0.0084527 | acd7ab972dad5787... | 17:14:b:m, 11:9:b:p |
| pV150wk1.n0.0.1.JPW13v2x.leaf | de7010c7017f108f... | 37,434 | 0.0087367 | e3e44811cddf690d... | 17:14:b:m, 15:12:b:m, 9:11:a:p |
| pV150w.n0.0.0.JPW13v2x.leaf | 297276bda2c0c8e8... | 40,732 | 0.0108091 | a5c68555bb52f99c... | 14:17:a:p |
| pV550wk4.n0.0.JPW13v2x.leaf | 0e89913dab474bf3... | 42,773 | 0.0113715 | 80bfb76da713b0b2... | 14:17:a:p, 15:12:b:m |
| pV000w.n0.1.JPW13v2x.leaf | b444a0445a16d91f... | 38,377 | 0.0125080 | c8fbcfa47df1338a... | 17:14:a:m |
| pV050w.n0.0.0.JPW13v2x.leaf | ef39d8f1c201066e... | 39,846 | 0.0127885 | 0bbd78341890db01... | 14:17:a:p |
| pV055w.n0.0.JPW13v2x.leaf | 4d5dcb86ae296afe... | 40,035 | 0.0132318 | 9e4406aa95223b13... | 14:17:a:p |
| pV550wk5k4.n0.0.JPW13v2x.leaf | 8574eefc07cbfad8... | 40,703 | 0.0136264 | c4e55e280f397fbb... | 17:14:a:m, 11:9:b:p |
| pV050w.n0.0.1.0.JPW13v2x.leaf | a5c40fdfa6c6fc3e... | 37,449 | 0.0140582 | 83386f42fc0a7875... | 14:17:a:p |
| pV110w.n0.0.0.JPW13v2x.leaf | f197dc00e244fdae... | 38,832 | 0.0152158 | b8c9bd967725af7a... | 14:17:a:p, 15:12:b:m |
| pV555w.n0.1.2.JPW13v2x.leaf | f49f2eb1a22fa6da... | 42,272 | 0.0159368 | d5616532ff7584a3... | 17:14:a:m, 12:15:b:p |
| pV555w.n0.0.2.JPW13v2x.leaf | 6cea4838ead2f2a5... | 41,541 | 0.0159564 | c09d6e567c048699... | 14:17:a:p, 12:15:b:p |
| pV010w.n0.0.0.JPW13v2x.leaf | 942638db9482080b... | 34,082 | 0.0178754 | fa1c3a119c77c486... | 14:17:a:p, 15:12:b:m |
| pV015w.n0.0.JPW13v2x.leaf | 5af737cf52bc5a8a... | 40,328 | 0.0183166 | 40467f24c26dcc48... | 14:17:a:p |
| pV155wr.n0.0.2.JPW13v2x.leaf | 303f4d6d493320e7... | 41,014 | 0.0191698 | aa4033fd4c174604... | 14:17:a:p, 12:15:b:p |
| pV550wk4.n0.3.JPW13v2x.leaf | 1a0d7d5e463b2563... | 41,718 | 0.0194904 | d3a3ab6996496b9c... | 14:17:a:p, 12:15:b:p |
| pV155wr.n0.2.2.JPW13v2x.leaf | 6adc0cbdd6aea295... | 41,733 | 0.0198055 | 5ae0f2fd11b672cc... | 17:14:b:m, 12:15:b:p |
| pV051w.n0.0.JPW13v2x.leaf | 0ea4f6e6048b40f1... | 41,209 | 0.0198113 | 8ac4cc5830a2582a... | 14:17:a:p |
| pV011w.n0.0.JPW13v2x.leaf | b7c1800b107f042b... | 41,329 | 0.0199409 | feff87e7e00f8d89... | 14:17:a:p |
| pV551w.n0.1.2.JPW13v2x.leaf | afe49ed1b2c16ead... | 42,122 | 0.0246472 | 6c13847faac68f52... | 17:14:a:m, 12:15:b:p |
| pV551w.n0.0.2.JPW13v2x.leaf | b69d82a0103db734... | 42,266 | 0.0247499 | 763ae7528cd7ccfe... | 14:17:a:p, 12:15:b:p |
| pV151w.n0.0.3.JPW13v2x.leaf | 44e9301d4c79733e... | 41,440 | 0.0266113 | 755e1f5a001224ae... | 14:17:a:p, 12:15:b:p |
| pV151w.n0.2.3.JPW13v2x.leaf | 782ec38d818c15c4... | 42,450 | 0.0270354 | ea8b78d94bd17ab0... | 17:14:b:m, 12:15:b:p |
| pV550wk5.n0.1.1.0.0.JPW13v2x.leaf | de1b17d5262fbeef... | 34,443 | 0.0302549 | 47a621590904039b... | 17:14:a:m, 15:12:b:m, 14:6:b:m |
| pV550w.n0.0.1.1.0.0.JPW13v2x.leaf | 88eda0f7a21d5604... | 32,971 | 0.0302582 | 92945e46c5d28dc3... | 14:17:a:p, 15:12:b:m, 14:6:b:m |
| pV100wk2.n0.JPW13v2x.leaf | 1759370eb26c4dc9... | 35,374 | 0.0440736 | 38518d42433ae7c6... | 17:14:b:m, 9:11:a:p |
| pV110w.n0.0.1.JPW13v2x.leaf | edfeb7e4ee1d4e0b... | 39,034 | 0.0486520 | 67c9edb204e35a4a... | 14:17:a:p, 12:15:b:p |
| pV010w.n0.0.1.JPW13v2x.leaf | 0ef58b26410f78ab... | 38,764 | 0.0497787 | 46b3a177ca3251d4... | 14:17:a:p, 12:15:b:p |
| pV550wxh.n0.JPW13v2x.leaf | 8ffe8fc643f7968a... | 34,455 | 0.0525204 | af798598964299fd... | 14:17:a:p, 15:12:b:m, 6:14:a:m |
| pV015w.n0.1.1.JPW13v2x.leaf | 6afdcc15b70fee53... | 43,880 | 0.7129455 | f4e35d30125da2a9... | 17:14:a:m |
| pV010w.n0.0.3.JPW13v2x.leaf | 1d568932d9f2b45a... | 43,880 | 0.9901882 | 2a702438ee879939... | 14:17:a:p, 12:15:a:p |
| pV550wk1.n0.JPW13v2x.leaf | beee9be877e7244e... | 43,878 | 3.7607796 | 37770a64042d0c45... | 14:17:a:p, 15:12:a:m |
| pV151w.n0.0.2.JPW13v2x.leaf | 0679c6a6a7a705f0... | 47,181 | 3.9388079 | 8298d69a00da9e0f... | 14:17:a:p, 12:15:a:p |
| pV110w.n0.0.3.JPW13v2x.leaf | 77a85d9b9bee884b... | 46,080 | 4.6662588 | fd819097741f6a10... | 14:17:a:p, 12:15:a:p |
| pV151w.n0.2.2.JPW13v2x.leaf | a4e7845daa092af1... | 47,181 | 6.5647352 | 8e3825ca15813e9d... | 17:14:b:m, 12:15:a:p |
| pV051w.n0.1.JPW13v2x.leaf | 576d4dee72413efe... | 46,082 | 6.6227296 | cbc204bb5ff3b238... | 17:14:a:m |
| pV555w.n0.1.1.JPW13v2x.leaf | 485b236f6022972c... | 46,814 | 7.3369022 | 4bfe834454185e79... | 17:14:a:m, 15:12:a:m |
| pV155wr.n0.0.3.JPW13v2x.leaf | 31ce86f2f3043b0b... | 46,814 | 8.3643910 | d6f96575370979e1... | 14:17:a:p, 12:15:a:p |
| pV555w.n0.0.3.JPW13v2x.leaf | a0b91447f7ca0428... | 46,814 | 8.3855580 | 19f47af37adc1bef... | 14:17:a:p, 12:15:a:p |
| pV151w.n0.0.1.JPW13v2x.leaf | 06beb04eabd0762f... | 47,181 | 8.7632291 | 5e10d39a16374527... | 14:17:a:p, 15:12:a:m |
| pV155wr.n0.2.3.JPW13v2x.leaf | f231919503735e27... | 46,814 | 12.0203756 | 42909dca62f687bc... | 17:14:b:m, 12:15:a:p |
| pV155wr.n0.0.1.JPW13v2x.leaf | 888cb36463a86083... | 46,814 | 12.4825445 | 7692e8656e36a985... | 14:17:a:p, 15:12:a:m |
| pV555w.n0.1.3.JPW13v2x.leaf | 91b8a3a5ce3246c8... | 46,814 | 12.7142764 | 12d8eb9aa9259e9f... | 17:14:a:m, 12:15:a:p |
| pV550wk3.n0.JPW13v2x.leaf | d61678ddf8fc5ea7... | 43,878 | 14.0921944 | 5d2a409d9aaae764... | 14:17:a:p, 12:15:a:p |
| pV551w.n0.1.3.JPW13v2x.leaf | ffc45fbe35bb41ee... | 47,181 | 15.7985406 | 43bf7fb74a1dd6e3... | 17:14:a:m, 12:15:a:p |
| pV555w.n0.0.1.JPW13v2x.leaf | 3c3c4eeeb2081f0d... | 46,814 | 16.7915852 | 70fa7faa450a3519... | 14:17:a:p, 15:12:a:m |
| pV150wk1.n0.3.JPW13v2x.leaf | 8b0c55e86a10305f... | 46,080 | 22.4105536 | 19ba4e8c8f2bcc74... | 17:14:b:m, 12:15:a:p |
| pV550wk4.n0.1.JPW13v2x.leaf | 5f12260da72bc50c... | 44,979 | 23.9975608 | a0abdfd60579ee6a... | 14:17:a:p, 15:12:a:m |
| pV050w.n0.0.1.1.2.JPW13v2x.leaf | f906e37a58bbd030... | 41,678 | 26.7283823 | e0db241f4fcf76e0... | 14:17:a:p, 12:15:a:p |
| pV155wr.n0.2.1.JPW13v2x.leaf | edab7456d97bf782... | 46,814 | 26.9598049 | cf17ff8ec8aa8bb1... | 17:14:b:m, 15:12:a:m |
| pV551w.n0.0.1.JPW13v2x.leaf | 7f21fa0a67c9454e... | 47,181 | 26.9751622 | 6f75ec99efb1e723... | 14:17:a:p, 15:12:a:m |
| pV150wk1.n0.1.JPW13v2x.leaf | 77452c0c349a22f1... | 46,080 | 28.8413114 | b0f28cf0f2643338... | 17:14:b:m, 15:12:a:m |
| pV150w.n0.0.1.1.1.JPW13v2x.leaf | ca6e9d20d4a2e80c... | 43,878 | 29.1550932 | 72eb1c957ba679c4... | 14:17:a:p, 15:12:a:m |
| pV550wk5k3.n0.JPW13v2x.leaf | 9216931ed6679963... | 43,878 | 30.4919314 | 5d90de05a2a39215... | 17:14:a:m, 12:15:a:p |
| pV015w.n0.1.2.JPW13v2x.leaf | 48ff4c602e80f2d5... | 44,614 | 34.0289356 | 8441cf48a7e92782... | 17:14:a:m |
| pV151w.n0.2.1.JPW13v2x.leaf | 2da7db4c65e1c250... | 47,181 | 38.3331837 | 8a2b104f98411516... | 17:14:b:m, 15:12:a:m |
| pV551w.n0.0.3.JPW13v2x.leaf | 68ccbfebe9b3621f... | 47,181 | 38.5378600 | 57994b5a7e8aa70c... | 14:17:a:p, 12:15:a:p |
| pV551w.n0.1.1.JPW13v2x.leaf | 4da477d6f3d551d8... | 47,181 | 40.8124478 | 26631b08eff72c12... | 17:14:a:m, 15:12:a:m |
| pV550wk5k1.n0.JPW13v2x.leaf | 801b718f65d9a0ea... | 43,878 | 48.3436081 | b2ac0fb8434c0f11... | 17:14:a:m, 15:12:a:m |
| pV010w.n0.0.2.JPW13v2x.leaf | 3bb981e470f7d904... | 43,880 | 48.8770129 | a9f32ae339962f62... | 14:17:a:p, 15:12:a:p |
| pV005w.n0.0.JPW13v2x.leaf | 4a56f07d3afa117f... | 45,715 | 56.9052894 | a6b33b9ee0819955... | 14:17:a:p |
| pV110w.n0.0.2.JPW13v2x.leaf | 4fc246973e94830e... | 46,080 | 64.1758652 | 1a9190cc2226c0c6... | 14:17:a:p, 15:12:a:p |
| pV550wk4.n0.2.JPW13v2x.leaf | 468301c4834d5a5e... | 44,979 | 66.7908832 | b0d2722cbb2af03f... | 14:17:a:p, 12:15:a:p |
| pV015w.n0.1.0.JPW13v2x.leaf | 53aecfdcddadd352... | 44,614 | 85.8937695 | 0251ab970e2134c7... | 17:14:a:m |
| pV005w.n0.1.JPW13v2x.leaf | 6784bd52ad5bd524... | 45,715 | 94.3291524 | d405427b519b2cda... | 17:14:a:m |
| pV150w.n0.0.1.1.3.JPW13v2x.leaf | 8ae0f34bb1f0e860... | 43,878 | 102.6453108 | 8849ee8640f817ee... | 14:17:a:p, 12:15:a:p |
| pV055w.n0.1.2.JPW13v2x.leaf | 32d874bf7f21a7e4... | 44,614 | 106.3951313 | 376263f6fe14d7bb... | 17:14:a:m |
| pV001w.n0.0.JPW13v2x.leaf | 69af16e712327037... | 46,082 | 119.6998461 | 4449d7f4da1ac468... | 14:17:a:p |
| pV050w.n0.0.1.1.1.JPW13v2x.leaf | 808047f130750e07... | 41,678 | 144.6143525 | 69da3fc8eed0cb8c... | 14:17:a:p, 15:12:a:m |
| pV011w.n0.1.2.JPW13v2x.leaf | 475448dd0cc2e149... | 44,981 | 194.3743627 | 01faa34b06df4032... | 17:14:a:m, 12:15:b:p |
| pV055w.n0.1.0.JPW13v2x.leaf | 2fbfdacb7aee7420... | 44,614 | 218.9427254 | 60daab95b8c94839... | 17:14:a:m |
| pV550wk5b1l.n0.JPW13v2x.leaf | 56954ace85f6363c... | 43,511 | 235.7323110 | 7218716a487bbd59... | 17:14:a:m, 15:12:b:m, 6:14:a:m |
| pV001w.n0.1.JPW13v2x.leaf | 3122ea7e9cbbf6e0... | 46,082 | 446.3118134 | 174a2a40b78ac29e... | 17:14:a:m |
| pV055w.n0.1.1.1.JPW13v2x.leaf | c2a5cc5df16d6aa2... | 43,513 | 555.5851299 | 1166bc048edddb43... | 17:14:a:m |
| pV055w.n0.1.1.0.JPW13v2x.leaf | 7d227e0da49e80e1... | 43,880 | 588.9241959 | c8140ab983d0bb10... | 17:14:a:m |
| pV011w.n0.1.0.JPW13v2x.leaf | 9330cce56ed02ab9... | 44,981 | 607.6075547 | c1fcc1a5ed27082c... | 17:14:a:m, 15:12:a:p |
| pV011w.n0.1.3.JPW13v2x.leaf | 6bfa1f2e8b920676... | 44,981 | 621.3239196 | 250c940968fdc653... | 17:14:a:m, 12:15:a:p |
| pV011w.n0.1.1.JPW13v2x.leaf | 4e130647106eb7b7... | 44,981 | 994.0842814 | 3cb53a367cf8a31a... | 17:14:a:m, 15:12:b:m |
| pV550wk5k4.n0.1.JPW13v2x.leaf | bb3b0fc44dd657b8... | 45,713 | 1610.5642720 | e76ee04ee8c9f3ab... | 17:14:a:m, 9:11:a:p |
| pV011w.n0.2.JPW13v2x.leaf | bad0d24f9e0f5fa3... | 46,082 | 10772.4806776 | b4c01ceacc9f8eba... | 17:14:b:m |
| pV001w.n0.2.JPW13v2x.leaf | f1b4a530ad0c56dc... | 46,082 | 24273.3171825 | e12716ca05066508... | 17:14:b:m |
| pV050w.n0.2.JPW13v2x.leaf | d028b08276125b65... | 44,981 | 31671.0284294 | aba1618b27b21110... | 17:14:b:m |
| pV000w.n0.2.JPW13v2x.leaf | 19e6fd4ee8b30a80... | 44,981 | 41731.5885025 | 13687b71ac898c2e... | 17:14:b:m |
| pV010w.n0.2.JPW13v2x.leaf | d787ea610bd758d1... | 44,981 | 45932.6268258 | 12be79c6389759f8... | 17:14:b:m |
| pV015w.n0.2.JPW13v2x.leaf | acca6b6ed01f8d82... | 45,715 | 47447.0999502 | 29cd83fe9004da1e... | 17:14:b:m |
| pV051w.n0.2.JPW13v2x.leaf | b986d3c2112bce12... | 46,082 | 53907.9280738 | 9e9ede54584c481f... | 17:14:b:m |
| pV005w.n0.2.JPW13v2x.leaf | 66227049f049c2ab... | 45,715 | 57834.2368983 | c598e5e20aba07d1... | 17:14:b:m |
| pV055w.n0.2.JPW13v2x.leaf | a4e88a77f4aa0a37... | 45,715 | 65515.2885791 | 5c97031f0926ae0a... | 17:14:b:m |
| pV150wk2.n0.JPW13v2x.leaf | d886a0c29ab92d7e... | 47,181 | 75440.4736246 | e031db6175c51bc8... | 14:17:b:m |
| pV111w.n0.1.JPW13v2x.leaf | 2ce0485426df0aac... | 48,282 | 95708.1566629 | 6255cc67e7a9dc8b... | 17:14:a:m |
| pV155wr.n0.1.JPW13v2x.leaf | 675c4fd517acec16... | 47,915 | 103273.0766781 | 4344c08518d758cb... | 17:14:a:m |
| pV151w.n0.1.JPW13v2x.leaf | 0908e7df1ae26c04... | 48,282 | 187569.3738442 | 761a860594b4e8f7... | 17:14:a:m |
| pV110w.n0.1.JPW13v2x.leaf | b9529af804447698... | 47,181 | 197076.4417817 | 50f49db10c86b9be... | 17:14:a:m |
| pV155wr.n0.3.JPW13v2x.leaf | 9b67c2f6fc004e53... | 47,915 | 218110.1163865 | ce38d64d86046eb9... | 14:17:b:m |
| pV105w.n0.3.JPW13v2x.leaf | 759efa983adc0665... | 47,915 | 350250.1619718 | 051210557ae88479... | 14:17:b:m |
| pV100wk3.n0.JPW13v2x.leaf | 2ab96559e786cc94... | 47,181 | 377000.7930382 | ea92594e148e8847... | 14:17:b:m |
| pV115w.n0.1.JPW13v2x.leaf | 53d4c8212b2e7fb8... | 47,915 | 412300.6920134 | 19715b17f3c8c685... | 17:14:a:m |
| pV101w.n0.3.JPW13v2x.leaf | 9434871c37408688... | 48,282 | 432729.5535730 | 88f3975ae343c767... | 14:17:b:m |
| pV501w.n0.2.JPW13v2x.leaf | c073799f0eebe51f... | 48,282 | 449073.9260764 | 723699bfd6898c13... | 14:17:b:m |
| pV515w.n0.2.JPW13v2x.leaf | 8827b753a49b6534... | 47,915 | 469901.4331830 | 976384bed99171a6... | 14:17:b:m |
| pV110w.n0.3.JPW13v2x.leaf | 3fcddc2bdff81a9c... | 47,181 | 517971.8368525 | 391a8346f3ddbbc8... | 14:17:b:m |
| pV151w.n0.3.JPW13v2x.leaf | ecf2fbaa83ca2210... | 48,282 | 630644.9112289 | b53c055923f56416... | 14:17:b:m |
| pV551w.n0.2.JPW13v2x.leaf | a038e996eb86942f... | 48,282 | 654585.8325491 | 623f73bf23e90351... | 14:17:b:m |
| pV111w.n0.3.JPW13v2x.leaf | 2921f5de6425698e... | 48,282 | 674368.8784122 | 3002337d118ea147... | 14:17:b:m |
| pV500w.n0.2.JPW13v2x.leaf | 96d1f93490c2de88... | 47,181 | 715862.0655634 | dd9426385161cfb3... | 14:17:b:m |
| pV150w.n0.1.JPW13v2x.leaf | fe92ced9d0f32d2f... | 47,181 | 848503.5243383 | 71eb595a215cf986... | 17:14:a:m |
| pV105w.n0.1.JPW13v2x.leaf | 4d83545fd89046ba... | 47,915 | 1047718.0477439 | 81640231f03cc8ad... | 17:14:a:m |
| pV555w.n0.2.JPW13v2x.leaf | d39685e73976bc56... | 47,915 | 1066507.9853750 | c6e35e9e28d79f4f... | 14:17:b:m |
| pV115w.n0.3.JPW13v2x.leaf | e48e12d122f8efa1... | 47,915 | 1207428.6519413 | 916a49e360afc0ec... | 14:17:b:m |
| pV511w.n0.2.JPW13v2x.leaf | 13622b0cc05ddde8... | 48,282 | 1287220.4104363 | 1064174e8d6613cd... | 14:17:b:m |
| pV100w.n0.1.JPW13v2x.leaf | 6e47acdf2459b21e... | 47,181 | 1660855.5181480 | 549c46d8852a2267... | 17:14:a:m |
| pV505w.n0.2.JPW13v2x.leaf | d995c77b016a81a8... | 47,915 | 2305915.9517722 | 2d312c244bbb32ee... | 14:17:b:m |
| pV101w.n0.1.JPW13v2x.leaf | 6d27e208e5c4d5fd... | 48,282 | 2397526.8429225 | 8cbf66954e6e8723... | 17:14:a:m |
| pV510w.n0.2.JPW13v2x.leaf | 0cf871d6c190e9c5... | 47,181 | 3523397.4119277 | 6bbc7daa5d02bd64... | 14:17:b:m |
| pV550wk6.n0.JPW13v2x.leaf | 47fec30b4a5bd173... | 47,181 | 7051658.4944977 | 151154d22a8bc378... | 14:17:b:m |

## What the statement is used for, and what it does not contain

- It is the local side's statement for the case "wall above", the branch "the label-9 square stands in the wall column
  (class-frame x <= 53/100) with y >= 13/5": the region file is the one of the decided design of 2026-10-09 17:47
  (`JOIN_ROOTS.md`, lower table and sections 9.3 and 9.4; it is needed under both repairs of the slab gap), reviewed
  18:34 and sealed by Codex 18:17 on the same day. It serves the branch if the capture side certifies, for each of the twelve rigid
  labels j, the wall statement PW_j with the target HULL_j (hypothesis: a square in the class W, the wall column
  from y = 129/50; or a split form of it with the same target that covers y >= 13/5), and the family L statements
  that place the loose labels 3, 4, 15, 17 in their loose slots (premise note of the region file: for y > 13/5 they
  apply, because the label-9 square is then outside A_Q and the wall column holds one centre, so no square lies in
  A_Q; at y = 13/5 itself the square is in A_Q and they are not used: the slab branch takes that position, next
  item; the region takes the end y = 13/5 closed, a superset). The factor of label 9 rests on the
  WALL LEMMA (`JOIN_ROOTS.md` section 2.4). The composition is `JOIN_ROOTS.md` sections 3 and 9.3; it is not
  repeated or proved here.
- The region lies inside `JPW_exact_v2.json` (it differs from it only in label 9's lower end of xi_2), which is not
  part of the decided design; no statement is made for JPW v2, and this statement gives nothing for the slab
  (129/50 <= y <= 13/5), whose region is `JPWS_exact_v4.json`.
- NOT contained: that the capture side puts a packing of this branch into the region. That needs its wall
  statements PW_j and the family L statements. Their state is the capture side's bookkeeping and is not checked
  here; quoted from Codex's manifest `research/finishing-threshold-goal-20261007/window-capture/second-order-20261010/theorem/THEOREM_MANIFEST.json`
  (as of 2026-10-10 14:34:20, sha256 b251fe25e0869879...; the full digest of this snapshot stands in Codex's reply
  `<author reply>`; the live file has changed since): PW_1, PW_5, PW_10, PW_11, PW_12, PW_13, PW_14, PW_16 and
  L_3, L_4, L_15, L_17 have the status COUNTED; PW_2, PW_6, PW_7 and PW_8 have the status RECEIPT OPEN.
- Also NOT contained: the correctness of the region file against the class files (reviewed with the thirteen region
  files of the tags v2 and v2x, every box end and every arc recomputed from the literal class files:
  `reviews/join_roots/REVIEW_JOIN_ROOTS_V2.md`, sha256 9ac38730...; not part of this record).

## Review

Reviewed 2026-10-10 by a reviewer that wrote none of the record, of the certificate or of the tools:
`reviews/join_roots/batch5/REVIEW_EJPW13_v2x.md` (sha256
2de8ae1b9d0c7ad1439b1ff492a40aae6e6ba00dc72a97bad15d316e13e8fa45); the text it read is kept as
`reviews/join_roots/batch5/as_reviewed/RECORD_EJPW13_v2x.md` (sha256 7ff9ee9ceaae5474...); its run and outputs are
in `reviews/join_roots/batch5/` (`t_tree.py` and `rjlib.py`, the bytes of batch 4; `t_JPW13_v2x.out`,
`t_JPW13_v2x_nodes.json`). **Verdict: "PROVED after corrections": one correction, C1, in the section on use. No
wrong number in the Statement, the corollary paragraph, "the region in words", the Evidence table or the leaf
table; the statement itself does not depend on C1.**
Its run of the earlier reviewers' program (unchanged; the certificate read line by line; 563 s, 534 MB): 125 checks,
124 ok. It carries: the certificate's size and both hashes; the header against the statement file; the root node
against the region file (side [Sref, Sref], 68 box ends, 51 rotations) and the header window; the shape (255
nodes, depth 12, 43 arc and 49 option splits, 163 leaves each with one `0` step of positive value, no terminal
node, 7,133,642 terms, 6150 declarations), the eight cut sentences and the producer's description node for node;
the child test of SPEC 3.0 section 6 for all 254 children; all 43 arc cuts strictly inside their node's arc; the
exclusion test for every omitted option of all 49 option splits (smallest margin 0.0194); the 159 nodes that reach
beyond the root: every one a leaf, none in a box interval, labels 3, 4, 15, 17 only, at most 5.361e-06 rad, the
same list as the facts output (159 nodes, 354 arcs); label 11 never cut, with the root's box and arc in all 255
nodes; the node digests of both acceptance reports for 255 of 255 nodes; L the same rational number in both
reports, the assembler report and `run.json` for all 163 leaves; all 163 rows of the table; the log.
The one FAIL is the program's test "every hash string of the record is the hash of a file named above or stands in
the leaf table": the string left over is the digest b251fe25e0869879 of Codex's manifest, quoted in the section
on use, a file the program does not know. The reviewer's judgement: not a defect (Codex's reply
`<author reply>` gives the full digest of that snapshot); the quote now says where it stands.
By hand: the corollary against `SPEC_v3.0_NOTES.md` (note of 18:38) and the statement file; "the region in words"
number by number (label 9: the four box ends; the arc's centre is conj(u_9) exactly, the x axis, its ends
rot(-31/1000) and rot(31/1000) exactly; the wall lemma's inequality in integers, 1061039/1000961 > 53/50; labels
3, 4, 15, 17: ends rot(-4147/10000), rot(4147/10000), 1.572457 rad in all, more than a quarter turn; the twelve
rigid labels from HULL_j of `classes_v2/PW_Ljj.json`, the loose ones from `classes/L_Ljj.json`); the region against
`JPW_exact_v2.json` (S, all 51 rotations and 67 of 68 box ends equal; the one difference is label 9's lower end of
xi_2, -52219/500000 against -62219/500000: inside); the sixteen quoted states of Codex's manifest (the live file
had changed, the sixteen states had not); `JOIN_ROOTS.md` and `REVIEW_JOIN_ROOTS_V2.md` where the section on use
names them. A sample of six leaves against the root (depths 5 to 12): each leaf node contains its cell, built from
the cuts on its path, in all 17 arcs, 68 box ends and S, and assumes exactly the options of its path.
It did not rerun the two frozen checkers or the acceptance script (the frozen checkers have run on
these bytes twice: the producer's run with `--keep-going` and my acceptance run with the default options).

What changed against the text the reviewer read, all in this version (15:21):
- **C1, asked.** The section on use said that the family L statements apply to the branch "y >= 13/5" because the
  wall column holds one centre. At y = 13/5 itself the label-9 square is in version 1's A_Q (closed at 13/5), where
  the L files are exempt, so they are not used there: the slab branch takes that position (Codex's seal of
  2026-10-09 18:17: "At y=13/5 use JPWS and its four QB slots. The upper-wall L deductions are not used at
  equality."), and the region takes the end y = 13/5 closed, a superset (the region file's premise note). The
  sentence now says so, in the reviewer's words.
- Not asked, taken: "the wall case above" could be read as "named above"; it now reads: the case "wall above"
  (`JOIN_ROOTS.md`), in "the region in words" and in the first point on use.
- The manifest quote names Codex's reply that carries the snapshot's full digest (the reviewer's suggestion).
- The status paragraph with the limits sentence; this section.
Remarks of the reviewer that need no change here: the record of JPWS v4 should say that the slab branch takes
y = 13/5 (it will); every later record that quotes the manifest digest gives the same FAIL in the program unless
the reviewer is told; the region file's entry `what` says "3, 15, 17 any direction" and leaves out label 4, whose
root arc is the same (a description only; the hash is pinned by Codex's contract; the record's wording is the one
that fits `root_arc`).
