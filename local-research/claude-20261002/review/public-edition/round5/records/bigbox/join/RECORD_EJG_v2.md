Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line.

# Record: statement (T_JG, v2) for the region JG v2 ("every packing in the region JG v2 lies in the tube G20S"): ACCEPTED 2026-10-10 06:51, PROVED 08:21

Lead of the window side. Status words as in `bigbox/THEOREM_G20.md`: COMPUTED / PROVED; ACCEPTED
means: accepted by both frozen checkers in the lead's acceptance run, the record not yet reviewed.

**STATUS: PROVED (2026-10-10 08:21) as a statement about the numbers of the region file** (status words of
`bigbox/THEOREM_G20.md`): the certificate is accepted by both frozen checkers with the lead's post-check (06:51),
and this record is reviewed by a reviewer that wrote none of it, nor the certificate, nor the tools
(`reviews/join_roots/batch2/REVIEW_BATCH2.md`, sha256 25227b662a3e6211..., one review of six records:
131 checks of its own on this certificate, none failed; its own reader of the certificate, its own
comparison of the root node with the region file, its own child, exclusion and terminal tests; verdict: may be called PROVED after two corrections of wording, one of them in the Statement (the direction condition
of the tube is a bound on the angle, not on its sine); neither touches the certificate, the acceptance run or a
number of the tables; this version has them, section "Review").
Limits, as the reviewer states them: the soundness of SPEC 3.0 and of the two frozen checkers is taken from their
own reviews (`reviews/REVIEW_30*.md`), and with it the exact values L of the 56 `0` steps (the reviewer compared
them across the producer's and the acceptance reports of both programs and did not recompute them; the checkers
were not rerun); nobody but the producer has read how the leaves were made (not needed: the certificate is checked,
not the way it was made); the region file against the class files is taken from `reviews/join_roots/REVIEW_JOIN_ROOTS_V2.md`; THEOREM G20S
is taken from its own record (`bigbox/THEOREM_G20S.md`); the composition of `JOIN_ROOTS.md` section 3 is not
proved; the ruling that a leaf may be larger than the root (`LEAF_HELPERS.md`) was read and confirmed in this
review (its finding 5).
The record is written by `acceptance/mk_record.py` in the form of `RECORD_EJPG17m_v2.md` (reviewed at 01:03); the TUBE form of the Statement is new with this record and was reviewed here;
every number is taken from the files (facts output `acceptance/JG_v2_facts.out`, sha256 0c4666d35ec31704..., of
`acceptance/region_facts.py`: all its checks ok), and the reviewer compared every number with its own reading of
the files.
**This is a statement about a region, NOT about a case of the proof:** that the capture side puts a packing into
this region needs its class statements, which are not certified.

## Statement

(T_JG, v2). Let seventeen closed unit squares with pairwise disjoint interiors lie in [0, S]^2 with
S <= Sref = 4675530093604551/10^15, labelled 1 to 17, with one side direction a_i chosen for each square. If every
xi_ik lies in the interval [lo_ik, hi_ik] and every a_i lies in the root arc of label i, where the 34 intervals and
the 17 arcs are those of

    bigbox/join/JG_exact_v2.json   (entries window.box and root_arc)
    sha256 f635af684d0f81d318ad2f46f2721082e595d47ea294164062c10b6f2b941f32

then the configuration lies in the TUBE of the certificate's header (entries terminal.box and terminal.alpha, equal
to the statement file's `tube`): for every label i other than 4, xi_i1 and xi_i2 lie in [-1/5, 1/5] (label 2:
xi_21 in [-39/125, 0]; label 13: xi_13,2 in [-1/5, 28/125]) and the angle phi_i from the reference direction u_i
of label i to a_i (a_i = R(phi_i) u_i, SPEC 3.0 section 8) satisfies |phi_i| <= 1/10 rad. This is the window G20S
of `bigbox/THEOREM_G20S.md` (section 2) for the sixteen labels; for label 4 the tube is its root box with radius 1,
that is no condition beyond the hypothesis (the root arc of label 4 lies within 0.786228 rad of its reference
direction, and the box is the root's).

In words: every packing of seventeen unit squares of side at most Sref that lies in the region JG v2 has its
sixteen squares other than 4 in the window G20S. Coordinates xi_ik as in SPEC 3.0 section 1, from the reference file `upper-packing-certificate.json`
(sha256 24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7, the one in the certificate's header, used
by both checkers); frame (container corner at the origin): SPEC 3.0 section 0.

This is the COROLLARY (root region) of SPEC 3.0 (`SPEC_v3.0_NOTES.md`, note of 2026-10-09 06:22, from the proof of
the THEOREM of section 7): the certificate satisfies all conditions of section 7, so every configuration of F(root)
lies in the tube; and a configuration that is feasible for a side S <= Sref is feasible for the side Sref (SPEC 3.0
section 11). With THEOREM G20S this is the local side's statement for case G; the composition is `JOIN_ROOTS.md`
section 3 and is not repeated or proved here.

The region in words (`JOIN_ROOTS.md`, sections 1, 9.2, 9.3 and 11.1; arcs read from the region file, in rad from
each label's reference direction): case G of the join design: label 9 inside its gate [-0.099900, +0.099901], its box cut at the support end xi_(9,1) >= -9897/1000000; label 3 inside its gate [-0.099917, +0.099917]; label 17 inside its gate [-0.099917, +0.099917]; label 15 inside its gate [-0.099917, +0.099917]; label 4 with any direction; the loose labels 3, 4, 15, 17 in their slots; the twelve rigid labels 1, 2, 5 to 8, 10 to 14, 16 in their boxes E_j.

## Evidence

| what | value |
|---|---|
| certificate | `local-research/claude-20261002/results/assembly/JG/JG.cert.jsonl.gz`, 371,866,669 bytes, sha256 e7587199a38d4772394c1284b0abe4b90e8f98f7dc3845c639e5dc08839ac7b5; uncompressed stream a5f5adfa9d14307c067866f05db40e48f451daa0779e7be2f87aae938dadeac0 |
| its shape (read from the certificate) | 113 nodes, depth 29 in the Node checker's count (root = 0): 56 splits (21 arc, 7 box, 28 option) and 56 leaves closed by a `0` step; 1 terminal leaf (`td0f7ae2afe`: the piece that is left when every exit is cut off; both checkers accept it as terminal, that is: its node lies in the tube); 56 steps, 2,670,577 terms, 2222 declarations. Cuts: direction of label 1 cut 2 times (tan-half from its reference direction: -1/20, 1/20); 28 option splits of the pair (14, 17) with 2 children; direction of label 2 cut 2 times (tan-half from its reference direction: -1/20, 1/20); direction of label 5 cut 2 times (tan-half from its reference direction: -1/20, 1/20); direction of label 6 cut 2 times (tan-half from its reference direction: -1/20, 1/20); direction of label 7 cut 2 times (tan-half from its reference direction: -1/20, 1/20); direction of label 8 cut 2 times (tan-half from its reference direction: -1/20, 1/20); direction of label 10 cut 2 times (tan-half from its reference direction: -1/20, 1/20); direction of label 11 cut 2 times (tan-half from its reference direction: -1/20, 1/20); direction of label 12 cut 1 times (tan-half from its reference direction: -1/20); direction of label 13 cut 2 times (tan-half from its reference direction: -1/20, 1/20); direction of label 14 cut 1 times (tan-half from its reference direction: 1/20); direction of label 16 cut 1 times (tan-half from its reference direction: -1/20); xi_(3,1) cut at -1/5, 1/5; xi_(3,2) cut at 1/5; xi_(9,2) cut at -1/5, 1/5; xi_(17,1) cut at -1/5; xi_(17,2) cut at 1/5. The description has no `recentre`: every split node has the root's centre for every label; the leaves keep their leaf files' own nodes, and 56 of the 113 nodes reach beyond the root node in some arc (list in the facts output), which SPEC 3.0 section 6 allows: a child only has to contain its piece. Label 11 is cut in this tree. |
| exact values of the `0` steps | all positive; the smallest is L = 9.718258e-03 at `gX16a.n0.JGv2.leaf`; the same rational number in both checkers' reports for each of the 56 leaves (table below) |
| producer | the audit lead: description by its `regiontree.py` (sha256 of the description 436855a8f05ef000...), certificate by the assembler `proto30/hull_tree.py` 8af834ec6ccff429... (exit 0, 1329.8 s). Its own run of both frozen checkers under `--keep-going`: 113 of 113 nodes accepted by each (`JG.run.json`, sha256 41a3a63199460276...) |
| acceptance run | `locks/run_slot.sh acceptance/accept_tree30.sh JG_v2 <certificate> bigbox/join/EXPECT_JG_v2.json`, by the lead, 2026-10-10 06:20:22 to 06:51 on the Mac. Python checker 1523.33 s (753 MB), Node checker 332.65 s (1.45 GB) |
| log | `acceptance/ACCEPT_JG_v2.log`, sha256 4a00565164511b55761d8c69bc8d9c875d261f966dda022b227b818af3ccc0c9: `RESULT: ACCEPTED`, exit code of the run 0 |
| checker reports | `acceptance/JG_v2_C1.json` (Python, sha256 dd1f9471f4804f85...), `acceptance/JG_v2_C2.json` (Node, sha256 356b83ab846543e8...) |
| frozen files | `checker/wxcheck_v30.py` cf8db52bfa1cc565..., `checker2/wxcheck2_v30.js` 97210adf74a3ebed..., `SPEC_v3.0.md` 0a6dfc2ae10ed6f3... (`acceptance/FROZEN_30.json`) |
| statement file | `bigbox/join/EXPECT_JG_v2.json`, sha256 363ff3a6f97f872cbd0afff90d110d33d41cb87553e6ab8978be995ece76616e: 17 labels, S_floor = Sref, `terminal_leaves` not fixed (TUBE statement), `root_region` = the file above |

Lines of the log that carry the statement: both checkers, started with their default options, exit 0 with PASS on
the whole file; every node accepted by both; same node ids and the same closure kind per node in both reports;
nodes 113, infeasible 56, split 56, terminal 1; the root node has parent null, an empty assumption list, the
region's side interval, the region's box in all 68 interval ends and the region's arc for every label (centre and
both end rotations).

The 56 leaves closed by a `0` step (L from the Python report; "L sha256" = sha256 of the fraction as the report
writes it; in every row the Node report has the same rational number and the audit lead's assembler
report the same fraction, `L_exact`; all placed by containment, `LEAF_FORMAT_RULING.md`):

| leaf node | leaf file sha256 | terms | L | L sha256 | options assumed |
|---|---|---|---|---|---|
| gX16a.n0.JGv2.leaf | 9de530ce8e203e26... | 44,921 | 0.0097183 | 75d1dfc12ed72c07... | 14:17:a:p |
| gF11.n0.0.JGv2.leaf | 670f4c90e1993b06... | 44,939 | 0.0111502 | f7ab6d7c1bb19053... | 14:17:a:p |
| gF15.n0.0.JGv2.leaf | cb5815bfcbdbfd01... | 48,021 | 0.0132510 | c06843667718658a... | 14:17:a:p |
| gF14.n0.0.JGv2.leaf | 59e3b37340eed597... | 45,829 | 0.0132791 | a8b40f9c56b4b8ee... | 14:17:a:p |
| gF7.n0.0.JGv2.leaf | 1c449ac0748cf06f... | 48,341 | 0.0141989 | d5874e4d29517e4b... | 14:17:a:p |
| gX3.n0.0.JGv2.leaf | 0a49b9f923a6b00c... | 48,526 | 0.0143468 | aacc8c6ac8c9a454... | 14:17:a:p |
| gF12.n0.0.JGv2.leaf | e33d839ca742b837... | 47,960 | 0.0147121 | 3a0dea004668cc3b... | 14:17:a:p |
| gF4.n0.0.JGv2.leaf | d28be6a60076c8c2... | 48,250 | 0.0157047 | f4d7c98185d69f6d... | 14:17:a:p |
| gF10.n0.0.JGv2.leaf | 41a37361e62b48f1... | 47,756 | 0.0164047 | df9acebe364c8c91... | 14:17:a:p |
| gX16b.n0.JGv2.leaf | 147ff2855daa5155... | 41,941 | 0.0166843 | 730ecbe842c9151e... | 17:14:a:m |
| gX21.n0.0.JGv2.leaf | 87c2cf861024d078... | 41,841 | 0.0167464 | c765dc1d6c534ca3... | 14:17:a:p |
| gF11.n0.1.JGv2.leaf | 3d74f03e97c60acb... | 46,454 | 0.0167931 | df6ddb5e5552056c... | 17:14:a:m |
| gF12.n0.1.JGv2.leaf | 673628af8842b6bd... | 45,765 | 0.0169917 | f35a48faeb3ffe6e... | 17:14:a:m |
| gF14.n0.1.JGv2.leaf | 7b4e739d09a172b8... | 46,099 | 0.0180776 | 27063ea8eb355ab6... | 17:14:a:m |
| gX19b.n0.JGv2.leaf | 894ccaaafa4b122a... | 42,612 | 0.0184393 | 5df73ee5146fcddb... | 17:14:a:m |
| gX21.n0.1.JGv2.leaf | 7024229888100da4... | 38,773 | 0.0186984 | 45c155fc558f46e2... | 17:14:a:m |
| gF9.n0.0.JGv2.leaf | 620d321415e08687... | 47,095 | 0.0190338 | b7a7ff44953fa458... | 14:17:a:p |
| gF8.n0.0.JGv2.leaf | 33af6a2d8d4a939e... | 49,581 | 0.0201526 | 38646fea967bbc16... | 14:17:a:p |
| gX20.n0.1.JGv2.leaf | 9674d28efc4754aa... | 39,383 | 0.0206917 | fc3be530f83e3180... | 17:14:a:m |
| gF4.n0.1.JGv2.leaf | 9b0b7762e24b7f6f... | 47,143 | 0.0207600 | bfdd1477e008b8b9... | 17:14:a:m |
| gF8.n0.1.JGv2.leaf | fc421d9a19e934d4... | 46,400 | 0.0208188 | cb4547f154477717... | 17:14:a:m |
| gF5.n0.1.JGv2.leaf | bac8a4552a0b8b50... | 46,881 | 0.0212288 | 9faa44f257179f59... | 17:14:a:m |
| gF7.n0.1.JGv2.leaf | a61342fd2a020924... | 47,716 | 0.0227310 | a124e6f85ffb8fe7... | 17:14:a:m |
| gF6.n0.1.JGv2.leaf | 5cb138e328119f61... | 47,495 | 0.0260659 | ca0e93a78482e688... | 17:14:a:m |
| gX19a.n0.JGv2.leaf | e169c54956385fc6... | 42,630 | 0.0282724 | 191cd31d03e749d4... | 14:17:a:p |
| gX3.n0.1.JGv2.leaf | c356d31cb1c16212... | 49,407 | 0.0299800 | bf5dadc57458a344... | 17:14:a:m |
| gX20.n0.0.JGv2.leaf | 129a27cef46db860... | 39,748 | 0.0337449 | 58aba040768bef13... | 14:17:a:p |
| gF15.n0.1.JGv2.leaf | 2a79217b1fdf5135... | 43,671 | 0.0348656 | f163a68805d24628... | 17:14:a:m |
| gF9.n0.1.JGv2.leaf | 2d70bd4a9a3ec8fd... | 45,662 | 0.0430950 | ca89ecfd2d369540... | 17:14:a:m |
| gF10.n0.1.JGv2.leaf | 17e5f1e735c5cc16... | 44,093 | 0.0431963 | 31b39f4db45e3f17... | 17:14:a:m |
| gF5.n0.0.JGv2.leaf | bd66fe8470d60cd6... | 50,196 | 0.0459257 | 93fe87ff9aab9f6a... | 14:17:a:p |
| gF13b.n0.JGv2.leaf | 46233ac760387a22... | 53,047 | 9.1918010 | 55f131022f4cf7be... | 14:17:a:p |
| gF6a.n0.JGv2.leaf | 3b5549f10ee491da... | 54,148 | 30.7879848 | c25f226d621da4e8... | 14:17:a:p |
| pNGF18fat0.n0.JGH13low.leaf | b83b691f34c74513... | 49,748 | 87.7058072 | b8806b95515a7412... | 14:17:a:p |
| gF13.n0.1.JGv2.leaf | f3ba9fd4ae17cad7... | 53,047 | 129.9591184 | bb20f7946ae0930b... | 17:14:a:m |
| gX1.n0.0.JGv2.leaf | 58f07349d90be0e2... | 54,882 | 207.7028048 | bef4596b3d4e1516... | 14:17:a:p |
| gF2.n0.1.JGv2.leaf | ca9b2f95f6ff7648... | 54,882 | 216.4553259 | 31052024dc5b57c3... | 17:14:a:m |
| gX17.n0.0.JGv2.leaf | e53ff0de3442f9af... | 51,214 | 374.4308673 | f60bdfe7ebbc045d... | 14:17:a:p |
| gF2.n0.0.JGv2.leaf | 92826c688f31e221... | 54,882 | 383.0480924 | 2a068c37e32491ae... | 14:17:a:p |
| gX1.n0.1.JGv2.leaf | d56da166712d298f... | 54,882 | 464.4153326 | a26b658f890687e0... | 17:14:a:m |
| gF24.n0.0.JGv2.leaf | 9f55510e19619e61... | 48,282 | 535.1911520 | 7b9e67a2b9dc75a3... | 14:17:a:p |
| gX17.n0.1.JGv2.leaf | 66add33f922c7145... | 51,214 | 624.1854503 | 906a897aad32db27... | 17:14:a:m |
| gF23.n0.0.JGv2.leaf | 33d43b9a9c5b07fd... | 48,282 | 898.1220315 | 0517a1884bc5675f... | 14:17:a:p |
| pNGF18fat1.n0.JGH13low.leaf | b2bb7c5b00702cfa... | 49,748 | 1595.7964498 | 3278730c9f2b8040... | 17:14:a:m |
| gF29.n0.1.JGv2.leaf | 7278dacf6519862e... | 48,282 | 2266.4005275 | 8e5db33c2746b9bd... | 17:14:a:m |
| gF24.n0.1.JGv2.leaf | 73262b2449bdba7e... | 48,282 | 3502.9985735 | cca2d13a74cd1bd9... | 17:14:a:m |
| gF29.n0.0.JGv2.leaf | b667bf5149d0abb7... | 48,282 | 3639.6643589 | a6b6348aeaa6bcae... | 14:17:a:p |
| gF27.n0.1.JGv2.leaf | c09011a15cbbca2f... | 48,282 | 4425.2387323 | 1673776d1d6f4f5b... | 17:14:a:m |
| gF27.n0.0.JGv2.leaf | 8a1cf5bec3b092b5... | 48,282 | 10273.1333648 | a4c2432f720476f0... | 14:17:a:p |
| gF28.n0.0.JGv2.leaf | 0f87387d8239d685... | 48,282 | 29608.2824163 | 79ebb0b0b078055b... | 14:17:a:p |
| gF28.n0.1.JGv2.leaf | fcd8e4e51b185ef2... | 48,282 | 32194.7117723 | 7c467dcf8e926f78... | 17:14:a:m |
| gF23.n0.1.JGv2.leaf | aa1ff01acc5b039f... | 48,282 | 35664.2270887 | fe40d734714d0c1d... | 17:14:a:m |
| gF22.n0.1.JGv2.leaf | 52c5d6ae54d6a20d... | 48,651 | 98963.9745374 | 5fffa6b2ab3b060f... | 17:14:a:m |
| gF22.n0.0.JGv2.leaf | 2f76e90e9b16004e... | 48,651 | 142302.1973224 | fe804bc45b42911c... | 14:17:a:p |
| gX33.n0.0.JGv2.leaf | 6507f17e10a5837c... | 46,816 | 460861.5524884 | 6bc3eb25b93b43b4... | 14:17:a:p |
| gX33.n0.1.JGv2.leaf | 6338e0ceec448ff9... | 46,816 | 1083946.4007702 | d5f61e22ec7ef757... | 17:14:a:m |

## What the statement is used for, and what it does not contain

- It is the local side's statement for case G of the decided design (all of 9, 3, 15, 17 inside their gates): the
  region file is the one of the lower table of `JOIN_ROOTS.md`, reviewed 18:34 and sealed by Codex 18:17. With
  THEOREM G20S (`bigbox/THEOREM_G20S.md`, section 3) it gives the case-G line of the LOCAL THEOREM (form) of
  `JOIN_ROOTS.md` section 3: seventeen squares in [0, S*]^2 (the endpoint placement K of its section 2.1) that lie
  in the region JG v2 have their sixteen squares other than 4 on the three-slider family. For a packing of side
  S <= S* read with its own container corner at the origin (the frame of the Statement above), (T_JG, v2) and
  THEOREM G20S give S = S* as well, directly. In the endpoint frame of the join design, S0 = S* is a further step
  of the composition (section 3, case G: on the family label 8 touches two walls, a statement of Codex), which is
  not proved here.
- **The two leaves made on a helper window are admissible in a tree of the root `JG_exact_v2.json`.** Exit F18,
  the sliver "label 13 below" (node `ne99e545db0`, an option split of the pair (14, 17) with the options 14:17:a:p
  and 17:14:a:m), is closed by `pNGF18fat0.n0.JGH13low.leaf` and `pNGF18fat1.n0.JGH13low.leaf`, exported on
  `LEAFHELPER_JG_13low_v1.json`. Their nodes have label 13's direction in [-0.120062903, -0.099911074] and so reach
  2.006e-2 rad below the root's lower end -0.099999888 (and 6.5e-6 rad above the root's upper end of label 12, the
  exporter's widening). Why this is admissible: SPEC 3.0 section 6 demands of a child only that it CONTAINS its
  piece, its F is defined by its own data, and nothing bounds a node other than the root from above; the leaf then
  proves the emptiness of its own, larger node. Both frozen checkers accepted these two nodes in this run, a
  whole-file PASS with default options. They are not different in kind from the other leaves: all 56 leaf nodes of
  this tree reach beyond the root node in some arc (the exporter's widening of a few 1e-6 rad), as do 21 leaves of
  the accepted tree JPG3p v2. Ruling and rules of use: `LEAF_HELPERS.md`. The helper file itself is no part of the
  proof: no statement is made for it, and the certificate does not name it.
- NOT contained: that the capture side puts a packing of case G into the region (its statements of families C and
  L and for label 9, none certified), and the correctness of the region file against the class files (reviewed,
  `reviews/join_roots/REVIEW_JOIN_ROOTS_V2.md`; the support end of label 9 is a lemma of the text, `JOIN_ROOTS.md`
  section 9.2).

## Review

Reviewed 2026-10-10 by a reviewer that wrote none of the record, of the certificate or of the tools,
in one batch with five other records: `reviews/join_roots/batch2/REVIEW_BATCH2.md` (sha256
25227b662a3e6211cc35fa09492e716c5e0e4001ca3d339b7623146a0f958905); the text it read is kept as
`reviews/join_roots/batch2/as_reviewed/RECORD_EJG_v2.md` (sha256 63dcdcf63cea7d2e...); its scripts and outputs are in
`reviews/join_roots/batch2/` (`t_tree.py`, output `t_JG_v2.out`; `w_helper.out`). **Verdict: the statement may be called PROVED after the listed corrections; both are corrections of wording.**
It recomputed, with its own code (the earlier reviewer's scripts made into one program and extended): every hash
the record names; the certificate line by line (header, counts, the tree conditions of SPEC 3.0 section 7, the
root node against the region file in the side interval, 68 box ends and 51 rotations, every cut as the record
words it); the child test of section 6 for all 112 children; the exclusion test of section 4.7 for
all 28 option splits; the final store hashes of both acceptance reports from the node data, and the producer's two reports against
them node by node; every row of the table of leaves; the log.
In addition for this record: the terminal node `td0f7ae2afe` (line 72 of the certificate, depth 28, first child of
the box split of xi_(17,2) at 1/5, no assumption, no round) passes the reviewer's own terminal test of SPEC 3.0
section 8 (box inside the tube's box in all 68 ends; smallest slack in sine 8.27e-5), and every arc end of the
sixteen labels is within 0.099916791 rad of the reference direction by exact enclosure of the angle; the header's
tube equals the region file's `terminal` and the statement file's `tube` and was compared with `THEOREM_G20S.md`
section 2 by reading; leaving `terminal_leaves` open in the statement file is right for a tube statement (the
corollary does not depend on how many nodes are closed as terminal). The two helper-window leaves and the helper
file (review finding 5, not a condition): `LEAF_HELPERS.md` and this record's paragraph are right and complete; no
condition in SPEC 3.0, in the two corollaries or in either checker bounds a node other than the root (the header
window is used only in `root_failure` / `checkRoot`); all 56 leaf nodes reach beyond the root by 4.257e-6 to
6.498e-6 rad in arcs, only the two helper leaves go further (2.0063e-2 rad, label 13), and no node exceeds the root
in a box interval; the six omitted options of the split `ne99e545db0` are excluded (margins 0.0506 to 1.7834).
It did not rerun the two frozen checkers or the acceptance script (the frozen checkers have run on
these bytes twice: the producer's run with `--keep-going` and my acceptance run with the default options).

The two corrections, both made in this version (08:21):
1. Statement, the direction condition of the tube. It read "the sine of the angle of a_i from the reference
   direction of label i is at most 1/10 in absolute value". The tube of SPEC 3.0 section 8 and the window G20S of
   `THEOREM_G20S.md` section 2 bound the ANGLE: |phi_i| <= 1/10 rad. The sine form describes a larger set (angles
   up to asin(1/10) = 0.100167 rad), so the sentence was true but weaker than what is proved, it was not the
   window G20S, and with it the hypothesis of THEOREM G20S would not have been met. Now the angle form. The
   certificate proves the angle form: the terminal test demands |sin| <= alpha - alpha^3/6 = 599/6000, which
   implies |angle| <= alpha = 1/10 (SPEC 3.0 section 8), and the reviewer's exact enclosure puts every arc end of
   the terminal node within 0.099916791 rad of the reference direction. My own check before the change: SPEC 3.0
   section 8 ("every a_i = R(phi_i) gamma_i u_i with |phi_i| <= alpha_i") and `THEOREM_G20S.md` section 2
   ("|phi_i| <= 1/10 for all sixteen"). The same text is corrected in `acceptance/mk_record.py`.
2. "What the statement is used for", first point. The sentence with THEOREM G20S named the LOCAL THEOREM of
   `JOIN_ROOTS.md` section 3 as the source of "has side S*" and named no frame. The LOCAL THEOREM is about seventeen
   squares in [0, S*]^2 and concludes only that the sixteen squares other than 4 lie on the family; "S = S*" comes
   directly from THEOREM G20S for a packing read with its own container corner at the origin, and in the endpoint
   frame of the join design it is a step of the composition, which is not proved. Reworded with the frame and the
   source (the reviewer's proposal).
Also taken up: the limits sentence in the status paragraph (finding 4); the status paragraph now says that the TUBE
form of the Statement is new with this record (remark 6e). Remarks of the reviewer that need no change: the sizes
of the acceptance row are in binary units (753 MB is 790,085,632 bytes, 1.45 GB is 1,554,497,536 bytes); "inside
its gate" is exactly rot(-1/20) to rot(1/20) for the labels 3, 15, 17, and "any direction" is exactly
rot(-4147/10000) to rot(4147/10000). The reviewer's own slip, noted in its report: four starts of the slot wrapper
with a wrong tag (exit 1, no output but a usage error; lines in `proto30/out/contain/runs.jsonl`).
