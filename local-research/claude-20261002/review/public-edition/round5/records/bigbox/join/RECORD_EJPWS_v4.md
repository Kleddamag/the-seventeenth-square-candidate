Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line.

# Record: statement (E_JPWS, v4) for the region JPWS v4 ("the region JPWS v4 is empty"): ACCEPTED 2026-10-10 16:46, PROVED 17:11

Lead of the window side. Status words as in `bigbox/THEOREM_G20.md`: COMPUTED / PROVED; ACCEPTED
means: accepted by both frozen checkers in the lead's acceptance run, the record not yet reviewed.

**STATUS: PROVED (2026-10-10 17:11) as a statement about the numbers of the region file** (status words of
`bigbox/THEOREM_G20.md`): the certificate is accepted by both frozen checkers with the lead's post-check (16:46),
and this record is reviewed by a reviewer that wrote none of it, nor the certificate, nor the tools
(`reviews/join_roots/batch6/REVIEW_EJPWS_v4.md`, sha256 0a094486675bef10...: its own run of the
earlier reviewers' program on this certificate, unchanged, 123 checks, 122 ok and one FAIL that is no defect (the
program does not know the digest of Codex's manifest that the section on use quotes); 39 exact checks of its own
by hand, none failed: the corollary, the statement file, "the region in words" number by number, every claim of
the section on use, the replacement leaf; ALL 70 leaves against the root; verdict: "PROVED as it stands", no
correction asked; three optional notes of wording, taken in this version).
Limits, as the reviewer states them: it did not run the two checkers, so that each of the 70 `0` steps holds on
its node (L > 0 exactly; 2,982,299 terms) rests on the two frozen checkers' acceptance alone; the program it ran
is the earlier reviewers', run unchanged and not read whole (the exclusion test of the option splits is that
program's); not reviewed: SPEC 3.0 and the proof of the corollary (read against the record's wording only), the
region file against the class files, the class statements (their states are checked as quotes only), the wall
lemma and the composition; the acceptance run read the producer's work file, and that it has the bytes of the
file of record rests on sha256 (log, both reports, `acceptance/BATCH_1609.log`, the file on disk hashed in the
reviewer's run). As for every record of this kind, the soundness of SPEC 3.0 and of the two frozen checkers is
taken from their own reviews (`reviews/REVIEW_30*.md`), and nobody but the producer has read how the leaves were
made (not needed: the certificate is checked, not the way it was made).
The record is written by `acceptance/mk_record.py` (its branch for wall regions) in the form of
`RECORD_EJPG17m_v2.md` (reviewed at 01:03); every number is taken from the files (facts output
`acceptance/JPWS_v4_facts.out`, sha256 56a6557634855ae1..., of `acceptance/region_facts.py`: all its checks ok), and the
reviewer compared the numbers with its own reading of the files.
**This is a statement about a region, NOT about a case of the proof:** that the capture side puts a packing into
this region needs its class statements (the wall statements, the slab statement of label 11 and the loose Q statements; their state is the capture
side's bookkeeping, quoted in the section on use and not checked here).

## Statement

(E_JPWS, v4). Let seventeen closed unit squares with pairwise disjoint interiors lie in [0, S]^2 with
S <= Sref = 4675530093604551/10^15, labelled 1 to 17, with one side direction a_i chosen for each square.
Then it is NOT the case that every xi_ik lies in the interval [lo_ik, hi_ik] and every a_i lies in the root arc of
label i, where the 34 intervals and the 17 arcs are those of

    bigbox/join/JPWS_exact_v4.json   (entries window.box and root_arc)
    sha256 7d32a55bc2b080056d267dd10d38abb003ff84a649cd22aabb05899ec2a8be1f

In words: no packing of seventeen unit squares of side at most Sref lies in the region JPWS v4. Coordinates xi_ik as in SPEC 3.0 section 1, from the reference file `upper-packing-certificate.json`
(sha256 24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7, the one in the certificate's header, used
by both checkers); frame (container corner at the origin): SPEC 3.0 section 0.

This is the EMPTINESS COROLLARY of SPEC 3.0 (`SPEC_v3.0_NOTES.md`, note of 2026-10-09 18:38): the certificate
satisfies all conditions of section 7 and no node is closed as terminal, so the set F(root) is empty; and a
configuration that is feasible for a side S <= Sref is feasible for the side Sref (SPEC 3.0 section 11).

The region in words (`JOIN_ROOTS.md`, sections 2.4, 9.3, 9.4 and 11; arcs read from the region file, in rad from
each label's reference direction): the slab of the wall case: label 9 in the wall column (class-frame x <= 53/100) with 129/50 <= y <= 13/5, box xi_(9,1) in [-204203/1000000, -174437/1000000], xi_(9,2) in [-62219/500000, -104437/1000000], in the wall pose [-0.756708, -0.632747] (the x axis +- 2 atan(31/1000)); the loose labels 3, 4, 15, 17 in their version 1 Q-boxes QB_j, each with any direction; the rigid labels 1, 2, 5 to 8, 10, 12 to 14, 16 in their hull boxes HULL_j and label 11 in B_11 of the slab statement (a rectangle inside HULL_11's positions, HULL_11's arc).

## Evidence

| what | value |
|---|---|
| certificate | `local-research/claude-20261002/results/assembly/JPWS_v4/JPWS_v4.cert.jsonl.gz`, 402,763,192 bytes, sha256 538a6a512a10b72dd59f7a4eeec710c6bddb12411c6728745c7bbcf9cb333cf4; uncompressed stream fa745f412c202f2957840444faefa2185ef98688d88080987049848239c7691c |
| its shape (read from the certificate) | 110 nodes, depth 8 in the Node checker's count (root = 0): 40 splits (16 arc, 0 box, 24 option) and 70 leaves closed by a `0` step; no terminal leaf; 70 steps, 2,982,299 terms, 2520 declarations. Cuts: direction of label 3 cut 2 times (tan-half from its reference direction: -659/5000, 659/5000); direction of label 15 cut 5 times (tan-half from its reference direction: -659/5000, 659/5000); 17 option splits of the pair (14, 17) with 3 / 4 children; direction of label 17 cut 9 times (tan-half from its reference direction: -659/5000, 659/5000); 5 option splits of the pair (6, 14) with 2 children; 2 option splits of the pair (12, 15) with 4 children. The description has no `recentre`: every split node has the root's centre for every label; the leaves keep their leaf files' own nodes, and 67 of the 110 nodes reach beyond the root node in some arc (list in the facts output), which SPEC 3.0 section 6 allows: a child only has to contain its piece. Label 11 is never cut: its box and arc are the root's in every node. |
| exact values of the `0` steps | all positive; the smallest is L = 1.609870e-03 at `pUslabs20c945w.n0.2.JPWSv4.leaf`; the same rational number in both checkers' reports for each of the 70 leaves (table below) |
| producer | the audit lead: description by its `regiontree.py` (sha256 of the description d8d8001929c41c2b...), certificate by the assembler `proto30/hull_tree.py` 8af834ec6ccff429... (exit 0, 3621.3 s). Its own run of both frozen checkers under `--keep-going`: 110 of 110 nodes accepted by each (`JPWS_v4.run.json`, sha256 70317eaee35e3eda...) |
| acceptance run | `locks/run_slot.sh acceptance/accept_tree30.sh JPWS_v4 <certificate> bigbox/join/EXPECT_JPWS_v4.json`, by the lead, 2026-10-10 16:07:20 to 16:46 on the Mac. Python checker 1952.51 s (622 MB), Node checker 401.60 s (1.27 GB). The run read the producer's work file in place (path in the log's first line), started in parallel with the producer's own checker run: the same bytes, sha256 equal to the named one before and after the run (`acceptance/BATCH_1609.log`) and equal to the file under `results/assembly/JPWS_v4/` named in the first row, from which the facts were made |
| log | `acceptance/ACCEPT_JPWS_v4.log`, sha256 78f713f7ebb4263e538f153161b865ed39ab709160018086a26ddc6b3286efec: `RESULT: ACCEPTED`, exit code of the run 0 |
| checker reports | `acceptance/JPWS_v4_C1.json` (Python, sha256 564bce18c8902d6b...), `acceptance/JPWS_v4_C2.json` (Node, sha256 125e472d12dee5e7...) |
| frozen files | `checker/wxcheck_v30.py` cf8db52bfa1cc565..., `checker2/wxcheck2_v30.js` 97210adf74a3ebed..., `SPEC_v3.0.md` 0a6dfc2ae10ed6f3... (`acceptance/FROZEN_30.json`) |
| statement file | `bigbox/join/EXPECT_JPWS_v4.json`, sha256 a0ddbc0faaed59c2bb17a76fb3ec88d5968401828eced75f58e51b0f1733945d: 17 labels, S_floor = Sref, `terminal_leaves` 0, `root_region` = the file above |

Lines of the log that carry the statement: both checkers, started with their default options, exit 0 with PASS on
the whole file; every node accepted by both; same node ids and the same closure kind per node in both reports;
nodes 110, infeasible 70, split 40, terminal 0; the root node has parent null, an empty assumption list, the
region's side interval, the region's box in all 68 interval ends and the region's arc for every label (centre and
both end rotations).

The 70 leaves closed by a `0` step (L from the Python report; "L sha256" = sha256 of the fraction as the report
writes it; in every row the Node report has the same rational number and the audit lead's assembler
report the same fraction, `L_exact`; all placed by containment, `LEAF_FORMAT_RULING.md`):

| leaf node | leaf file sha256 | terms | L | L sha256 | options assumed |
|---|---|---|---|---|---|
| pUslabs20c945w.n0.2.JPWSv4.leaf | 67a1b1b9fbb32f1b... | 44,926 | 0.0016099 | c736c3d054727ada... | 17:14:b:m |
| pUslabs20c500w.n0.1.JPWSv4.leaf | a2993738055605dd... | 40,183 | 0.0020638 | 0a7c0ffe4cd02845... | 17:14:a:m |
| pUslabs20c500w.n0.0.JPWSv4.leaf | a6ed1e0424f24a5f... | 41,564 | 0.0021045 | 598a9dd699c2dd96... | 14:17:a:p |
| pUslabs20c555w.n0.1.JPWSv4.leaf | f842106dc757ca6b... | 43,466 | 0.0043495 | b8436706172b0a05... | 17:14:a:m |
| pUslabs20c555w.n0.0.JPWSv4.leaf | 0235a16b6a03be87... | 43,183 | 0.0044195 | dde958868682da1d... | 14:17:a:p |
| pUslabs20c945w.n0.1.0.JPWSv4.leaf | ba3926af8fc4d17f... | 44,061 | 0.0051718 | 1b9f063db7caab86... | 17:14:a:m, 15:12:b:m |
| pUslabs20c945w.n0.0.0.JPWSv4.leaf | 0d8a15a38c1eabd4... | 41,975 | 0.0057488 | 77080357bdbb14b4... | 14:17:a:p, 15:12:b:m |
| pUslabs20c100w.n0.0.JPWSv4.leaf | 05d999beec4394b7... | 39,934 | 0.0057849 | ae0c19698c9d15c2... | 14:17:a:p |
| pUslabs20c100w.n0.2.JPWSv4.leaf | dadd13f6c7e6db9c... | 42,536 | 0.0060419 | 647e2d24b2cdc46b... | 17:14:b:m |
| pUslabs20c451w.n0.0.JPWSv4.leaf | 9c55931b7799774e... | 41,841 | 0.0068209 | c7a142abcd49774b... | 14:17:a:p |
| pUslabs20c551w.n0.1.JPWSv4.leaf | 04262fd0f7676c9a... | 38,631 | 0.0073178 | 47daedb4df6ac51d... | 17:14:a:m |
| pUslabs20c551w.n0.0.JPWSv4.leaf | 0b8ef2431bfd4885... | 38,309 | 0.0075211 | cddd6192e585b381... | 14:17:a:p |
| pUslabs20c155wr.n0.0.JPWSv4.leaf | 2c55be69c27c043b... | 42,006 | 0.0075813 | bb8bd62e54582d36... | 14:17:a:p |
| pUslabs20c155wr.n0.2.JPWSv4.leaf | 18c1a5a8553d7270... | 39,763 | 0.0077676 | c36c5d0dc04b4f7d... | 17:14:b:m |
| pUslabs20c550w.n0.1.0.JPWSv4.leaf | b41750a9f9cdfd37... | 37,055 | 0.0079836 | 16df52f4329891a5... | 17:14:a:m, 14:6:b:m |
| pUslabs20c550w.n0.0.0.JPWSv4.leaf | c7533afe6861fc44... | 38,825 | 0.0080620 | 054e0049aa040731... | 14:17:a:p, 14:6:b:m |
| pUslabs20c501w.n0.1.JPWSv4.leaf | 1011dd09b88ada47... | 42,155 | 0.0090069 | 92e73b8070a7a411... | 17:14:a:m |
| pUslabs20c451w.n0.2.JPWSv4.leaf | d41a56a16bda2e67... | 40,818 | 0.0092544 | 15c193d6a1ef4f33... | 17:14:b:m |
| pUslabs20c150w.n0.0.0.JPWSv4.leaf | be88e83cb9c4a8ab... | 38,263 | 0.0095434 | 69429e0debed13b0... | 14:17:a:p, 14:6:b:m |
| pUslabs20c150w.n0.2.0.JPWSv4.leaf | 56d679bed9224d57... | 38,419 | 0.0101239 | 5c8bbf992b6059e7... | 17:14:b:m, 14:6:b:m |
| pUslabs20c050w.n0.0.0.JPWSv4.leaf | 8ec2f9baa406ac92... | 39,233 | 0.0118630 | db3e31dd35e19870... | 14:17:a:p, 14:6:b:m |
| pUslabs20c501w.n0.0.JPWSv4.leaf | 79df935fe739a857... | 43,686 | 0.0123115 | e0956dcc12196cd1... | 14:17:a:p |
| pUslabs20c101w.n0.2.JPWSv4.leaf | ec346c661cc2b940... | 42,686 | 0.0124238 | 5c11dbe99c24cc0a... | 17:14:b:m |
| pUslabs20c000w.n0.0.JPWSv4.leaf | b753275908679d94... | 41,721 | 0.0126518 | 69ed48d5d32c90bc... | 14:17:a:p |
| pUslabs20c101w.n0.0.JPWSv4.leaf | bc931c1eb06c29f8... | 43,961 | 0.0144338 | a712b31e2e1cbaa0... | 14:17:a:p |
| pUslabs20c050w.n0.1.JPWSv4.leaf | 952226e4a062518c... | 36,845 | 0.0145471 | 5ce9ea2e2f7a2b75... | 17:14:a:m |
| pUslabs20c055w.n0.0.JPWSv4.leaf | f0578158585ec579... | 41,966 | 0.0198220 | b3c7471c81d9e8e1... | 14:17:a:p |
| pUslabs20c000w.n0.1.JPWSv4.leaf | 2ffe1c4cd3b68af5... | 39,140 | 0.0251320 | 893998e7f64473be... | 17:14:a:m |
| pUslabs20c910w.n0.0.JPWSv4.leaf | e8d6b25f84c9cc3a... | 37,816 | 0.0275609 | 0ab8ef083decc035... | 14:17:a:p |
| pUslabs20c910w.n0.1.JPWSv4.leaf | d2d72b953e137787... | 38,765 | 0.0276692 | 867f1e96ad38d783... | 17:14:a:m |
| pUslabs20c910w.n0.2.JPWSv4.leaf | 73ea553cd3aa9469... | 39,325 | 0.0282900 | 834d45963ac9a109... | 17:14:b:m |
| pUslabs20c911w.n0.0.JPWSv4.leaf | 4f37a2f8b14752c0... | 39,534 | 0.0360613 | dff621d742a0ae2b... | 14:17:a:p |
| pUslabs20c911w.n0.1.JPWSv4.leaf | 6d5dbb4f251a640f... | 41,876 | 0.0361407 | b9afbb94af10eabb... | 17:14:a:m |
| pUslabs20c911w.n0.2.JPWSv4.leaf | e4f40dea50d2bd38... | 40,269 | 0.0364696 | b59cdae24107bd6b... | 17:14:b:m |
| pUslabs20c050w.n0.0.1.JPWSv4.leaf | 01ac57e9effd38ec... | 35,581 | 0.0375272 | 89b1140e5b52cba8... | 14:17:a:p, 6:14:a:m |
| pUslabs20c550w.n0.0.1.JPWSv4.leaf | fc6e3861d542810b... | 38,572 | 0.0384176 | cba049bf8d5a75a5... | 14:17:a:p, 6:14:a:m |
| pUslabs20c550w.n0.1.1.JPWSv4.leaf | de7400eb246f6940... | 38,599 | 0.0384269 | fd5e24a84931b8a0... | 17:14:a:m, 6:14:a:m |
| pUslabs20c150w.n0.0.1.JPWSv4.leaf | 09dd9648211c3a10... | 39,143 | 0.0389912 | c95c1e24b81185c7... | 14:17:a:p, 6:14:a:m |
| pUslabs20c150w.n0.2.1.JPWSv4.leaf | ffead7dee294d24b... | 39,451 | 0.0394296 | 09efc9b7d96a5306... | 17:14:b:m, 6:14:a:m |
| pUslabs20c945w.n0.0.1.JPWSv4.leaf | 0127aa2357a453ef... | 46,084 | 1.2744931 | 5bae90168fa196f7... | 14:17:a:p, 12:15:b:p |
| pUslabs20c945w.n0.0.2.JPWSv4.leaf | a2d873636345a4e7... | 46,084 | 20.7270273 | e150c88f3d3613b4... | 14:17:a:p, 15:12:a:p |
| pUslabs20c945w.n0.1.2.JPWSv4.leaf | 0ea0d40da45668da... | 46,084 | 21.4114379 | ae1392adc894ec54... | 17:14:a:m, 15:12:a:p |
| pUslabs20c001w.n0.0.JPWSv4.leaf | 8ff404d092bc1e84... | 44,616 | 72.8817144 | 6d19c2604bbeb21c... | 14:17:a:p |
| pUslabs20c055w.n0.1.JPWSv4.leaf | 9ea90481fcfb2661... | 44,616 | 168.0716478 | 637fc386a24c4000... | 17:14:a:m |
| pUslabs20c050w.n0.2.JPWSv4.leaf | 89b9d35cb76ea6ca... | 43,515 | 388.8464938 | fc2f32e8125de420... | 17:14:b:m |
| pUslabs20c451w.n0.1.JPWSv4.leaf | 5cb7d42ec3398f86... | 46,084 | 520.4142140 | 015a85b8ef05c4bd... | 17:14:a:m |
| pUslabs20c001w.n0.1.JPWSv4.leaf | cf6f5705e0dc28f3... | 44,616 | 665.7103457 | 8a59d74396258fae... | 17:14:a:m |
| pUslabs20c001w.n0.2.JPWSv4.leaf | 1792bec367d77b94... | 44,616 | 1310.1816714 | 26082f9e1c2397d0... | 17:14:b:m |
| pUslabs20c945wb1m.n0.JPWSv4.leaf | 886ef16feacbdbb6... | 46,084 | 1658.4611507 | 9f57bbeca7a75d0d... | 17:14:a:m, 12:15:b:p |
| pUslabs20c000w.n0.2.JPWSv4.leaf | 14f0724303b1b458... | 43,515 | 5065.2578707 | b01809751d37e54b... | 17:14:b:m |
| pUslabs20c055w.n0.2.JPWSv4.leaf | 4613c11656a43fcc... | 44,616 | 8992.0582431 | 947b2d2b5d6ad7da... | 17:14:b:m |
| pUslabs20c100w.n0.1.JPWSv4.leaf | 3c6bd463fdb18cfb... | 44,616 | 117424.9779281 | 8ed638639638a8f7... | 17:14:a:m |
| pUslabs20c101w.n0.1.JPWSv4.leaf | e84ce482fafcc68b... | 45,717 | 374512.9602529 | b32de07744223f95... | 17:14:a:m |
| pUslabs20c100w.n0.3.JPWSv4.leaf | 4a7bbdd0a936842f... | 44,616 | 395757.3839174 | 6834643a90a04fca... | 14:17:b:m |
| pUslabs20c101w.n0.3.JPWSv4.leaf | e46a40a4a3937c50... | 45,717 | 419487.0056391 | 9f7f854aac8cde25... | 14:17:b:m |
| pUslabs20c150w.n0.1.JPWSv4.leaf | 444289dee896c39f... | 44,616 | 443829.8490511 | 1b2caa55a5dbfb84... | 17:14:a:m |
| pUslabs20c150w.n0.3.JPWSv4.leaf | 23bdd73ced96e5a0... | 44,616 | 475401.8933033 | d9cf54338aa852d3... | 14:17:b:m |
| pUslabs20c945w.n0.3.JPWSv4.leaf | a84fa715b9449738... | 47,185 | 546765.8688471 | 2b5bbd9c2c4d34da... | 14:17:b:m |
| pUslabs20c550w.n0.2.JPWSv4.leaf | 52335cf1221bfad3... | 44,616 | 550656.8523573 | 9f1c6ef111238801... | 14:17:b:m |
| pUslabs20c945w.n0.0.3.JPWSv4.leaf | fce642b802fedfdb... | 46,084 | 555483.3751437 | 5577875e66a22eda... | 14:17:a:p, 12:15:a:p |
| pUslabs20c155wr.n0.1.JPWSv4.leaf | 027d01c0430db9d0... | 45,717 | 573833.2743682 | d62c1410eb844069... | 17:14:a:m |
| pUslabs20c451w.n0.3.JPWSv4.leaf | 3904cb4862ced1ec... | 46,084 | 768028.2276563 | 366c8f74b6650e4d... | 14:17:b:m |
| pUslabs20c155wr.n0.3.JPWSv4.leaf | db68d06720f47dc7... | 45,717 | 928978.5298018 | 47c431bbaf935913... | 14:17:b:m |
| pUslabs20c551w.n0.2.JPWSv4.leaf | fd3fb6e30a071843... | 45,717 | 958056.5078953 | b2aafc9c983afe47... | 14:17:b:m |
| pUslabs20c945w.n0.1.3.JPWSv4.leaf | 4d9c5c1fbd6553dc... | 46,084 | 999412.5079724 | 6c85bdce78978534... | 17:14:a:m, 12:15:a:p |
| pUslabs20c911w.n0.3.JPWSv4.leaf | d532ed4cd6fd3277... | 46,818 | 1120342.3534075 | 5544ff6b74c3445b... | 14:17:b:m |
| pUslabs20c500w.n0.2.JPWSv4.leaf | 6402e1e9f0e10881... | 44,616 | 1431297.5497825 | d898f909dbfd495f... | 14:17:b:m |
| pUslabs20c555w.n0.2.JPWSv4.leaf | 5d57a40c6d22f21b... | 45,717 | 1781117.7156725 | 569bc87b6d7a94f8... | 14:17:b:m |
| pUslabs20c501w.n0.2.JPWSv4.leaf | 0e156d033d87f1c1... | 45,717 | 2004748.5215810 | 0f33e6581e1a0a64... | 14:17:b:m |
| pUslabs20c910w.n0.3.JPWSv4.leaf | cce54054a4bbc67d... | 45,717 | 4754375.1848575 | ad8725393756f605... | 14:17:b:m |

## What the statement is used for, and what it does not contain

- It is the local side's statement for the SLAB of the wall case, the branch "the label-9 square stands in the wall
  column (class-frame x <= 53/100) with 129/50 <= y <= 13/5" (decided design of 2026-10-09 17:47, repair (2):
  `JOIN_ROOTS.md`, lower table and sections 9.3 and 9.4; the region file is the one of tag v4, made 22:06 on that
  day with label 11's tighter target, section 11 and `ADMISSION_v4.md`; Codex sealed its hash at 22:09). It serves
  the branch if the capture side certifies: for the eleven rigid labels j other than 11 the wall statement PW_j
  with the target HULL_j (hypothesis: a square in the class W, the wall column from y = 129/50), for label 11 the
  slab statement SL_L11_T020_DH with the target B_11 (hypothesis: a square in the slab of the wall column,
  129/50 <= y <= 13/5; NOT PW_11, whose target is HULL_11), and for the loose labels 3, 4, 15, 17 the loose Q files of
  record Q_3, Q_4, Q_15, Q_17 with the targets QB_j (hypothesis: a square in version 1's A_Q, the wall column up to
  y = 13/5; premise note of the region file). The factor of label 9 rests on the WALL LEMMA (`JOIN_ROOTS.md`
  section 2.4). The composition is `JOIN_ROOTS.md` sections 3 and 9.3; it is not repeated or proved here.
- The seam y = 13/5 belongs to THIS branch: there the label-9 square is in version 1's A_Q, the loose Q files
  apply, and the family L statements of the branch "wall above" are not used (Codex's seal of 2026-10-09 18:17;
  `RECORD_EJPW13_v2x.md`, section on use). The regions overlap at both seams (the box of label 9 is rounded
  outward: xi_(9,2) from -62219/500000 to -104437/1000000; JPW13 starts at -52219/500000 = -104438/1000000).
- The statement is for the WHOLE root as the file stands: the loose labels in their Q-boxes with ANY direction.
- The tree cuts the directions of labels 3, 15 and 17 at tan-half -659/5000 and 659/5000 only (not every cell is
  cut at both values) and closes every piece; labels 4 and 11 are not cut anywhere. One of the 70 leaves,
  `pUslabs20c945wb1m.n0.JPWSv4.leaf` (L = 1658.46, options 17:14:a:m and 12:15:b:p), replaces a leaf whose exact
  solve had failed twice (the audit lead's account). Its float solve
  used the side interval [Sref - 0.10, Sref + 0.01] instead of the usual [Sref - 0.10, Sref + 0.05]; that is a
  solver setting and not part of the certificate: this leaf's node has the side interval [Sref, Sref] like all 110
  nodes (read from the certificate), and both frozen checkers accept its `0` step on that node.
- The region lies inside `JPWS_exact_v2x.json` (label 11 in HULL_11 there; `ADMISSION_v4.md`), for which no
  statement is made: this statement does not serve a branch that rests on PW_11 with the target HULL_11.
- NOT contained: that the capture side puts a packing of this branch into the region. That needs the class
  statements named above. Their state is the capture side's bookkeeping and is not checked here; quoted from
  Codex's manifest
  `research/finishing-threshold-goal-20261007/window-capture/second-order-20261010/theorem/THEOREM_MANIFEST.json`
  (as of 2026-10-10 16:44:10, sha256 ac06106efd7823b7...; the full digest of this snapshot stands in Codex's reply
  `<author reply>`): PW_1, PW_5, PW_7, PW_8, PW_10, PW_12, PW_13, PW_14, PW_16, the slab statement
  SL11_T020 and Q_3, Q_4, Q_15, Q_17 have the status COUNTED; PW_2 and PW_6 have the status RECEIPT OPEN.
- Also NOT contained: the correctness of the region file against the class files (tag v4: 2,429 exact self-checks
  of the generator, `cmp_v4.py`, and Codex's independently made draft is the same region end for end,
  `ADMISSION_v4.md`; not reviewed by a reviewer).

## Review

Reviewed 2026-10-10 by a reviewer that wrote none of the record, of the certificate or of the tools:
`reviews/join_roots/batch6/REVIEW_EJPWS_v4.md` (sha256
0a094486675bef106080299862c52968d6256de1c4499b1a4fd27bd339c4bcf6); the text it read is kept as
`reviews/join_roots/batch6/as_reviewed/RECORD_EJPWS_v4.md` (sha256 38f1160bebfe9840...); its run and outputs are in
`reviews/join_roots/batch6/` (`t_tree.py` and `rjlib.py`, the bytes of batches 4 and 5; `t_JPWS_v4.out`,
`t_JPWS_v4_nodes.json`, `hand_checks.out`). **Verdict: "PROVED as it stands". No correction is required: every
number and claim it could test is right, and nothing overstates.**
Its run of the earlier reviewers' program (unchanged; the certificate read line by line; 212 s, 465 MB): 123 checks,
122 ok. It carries: the certificate's size and both hashes; the header against the statement file and the reference
file; the root node against the region file (side interval, 68 box ends, 51 rotations); the shape (110 nodes, depth
8, 16 arc and 24 option splits, 70 leaves each with one `0` step, none terminal); the child test of SPEC 3.0
section 6 for all 109 children; the exclusion of every omitted option in each of the 24 option splits; the node
digests, kinds and L against both acceptance reports and both of the producer's reports; all 70 rows of the table;
the hashes and numbers of the Evidence table; the log; the 67 nodes beyond the root: all leaves, in arcs of labels
3, 15, 17 only, by at most 5.4e-6 rad; label 11 never cut, the root's in all 110 nodes.
The one FAIL is the program's test "every hash string of the record is the hash of a file named above or stands in
the leaf table": the string left over is the digest ac06106efd7823b7 of Codex's manifest, a file the program does
not know; the reviewer found the live file unchanged since the snapshot quoted and the full digest in Codex's reply
`<author reply>`. Its judgement: harmless, no defect of the record.
By hand, 39 exact checks, none failed: the corollary against `SPEC_v3.0_NOTES.md` and the statement file; label 9's
box (the slab x <= 53/100, 129/50 <= y <= 13/5 of the class frame carried over with the file's own constants and
rounded outward; the left end is the wall end) and arc (centre conj(u_9) exactly, ends rot(-31/1000), rot(31/1000));
labels 3, 4, 15, 17 more than a quarter turn, with the boxes and arcs of `JQ_exact_v1.json` (the Q-boxes); the
eleven rigid labels other than 11 with the boxes and arcs of `JPW13_exact_v2x.json`; label 11's box inside its box
of `JPWS_exact_v2x.json`, with that file's arc; v4 against v2x entry by entry (only label 11's box differs, v4
inside); both seams (JPW13 starts 1e-6 below this region's upper end and both hold y = 13/5; `JQ_exact_v1.json`
holds the lower end; the three files have the same xi_(9,1) interval and the same arc of label 9); the dates and
files of the section on use; the quoted states of Codex's manifest, and that each quoted row's file is among the
region file's own inputs; the acceptance run's work file by its sha256. The replacement leaf: its node has
S = [Sref, Sref], as have all 110 nodes and the stores of all 70 rounds, and it assumes exactly 17:14:a:m and
12:15:b:p; the sentence "a solver setting and not part of the certificate" is right by SPEC 3.0 (root conditions;
a child's side interval contains its piece's). ALL 70 leaves against the root: from the producer's description
alone, each leaf node contains its cell (17 arcs, 68 box ends, S) and assumes exactly the options of its path.
It did not rerun the two frozen checkers or the acceptance script (each of the two frozen checkers
has run on these bytes twice: in the producer's run with `--keep-going` and in my acceptance run with the default
options).

What changed against the text the reviewer read, all in this version (17:11), none of it asked as a correction:
- N1: the status paragraph said that the states of the capture statements are quoted "in the last section"; they
  are quoted in the section on use.
- N2: "(three pieces per label)" was true of the cut values only; a cell need not be cut at both (the cell of the
  c945 leaves has label 15 in tan-half [-4147/10000, 659/5000] and label 17 uncut). The sentence now says so.
- N3: the section on use now names the hypothesis of the slab statement of label 11 (a square in the slab of the
  wall column; the reviewer read this field of `SL_L11_T020_DH.json`, sha256 afde9329..., the polygon
  [-131/250, 53/100] x [129/50, 13/5] with every direction, so the seam y = 13/5 lies in it) and says that it is
  not PW_11. The region file's `premise_note`, read alone, suggests PW_11 for label 11 ("PW_j places the rigid
  labels in HULL_j"); its entries `what`, `design` and `status` say B_11. The file's hash is sealed, so the remedy
  is this wording: THE COMPOSITION MUST TAKE SL11_T020 FOR LABEL 11 IN THE SLAB.
- The status paragraph with the limits sentence; this section.
Remarks of the reviewer that need no change here: Codex's seal of 2026-10-09 18:17 is older than tag v4 (it names
JPWS v2x); the seam rule itself did not change. Codex's manifest has a third base row with the status RECEIPT OPEN,
FRAME_MARKER, which this record does not name (whether this branch needs it is the capture side's matter).
