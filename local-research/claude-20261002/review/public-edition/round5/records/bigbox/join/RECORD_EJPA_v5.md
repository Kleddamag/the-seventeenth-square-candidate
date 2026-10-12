Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line.

# Record: statement (E_JPA, v5) for the region JPA v5 ("the region JPA v5 is empty"): ACCEPTED 2026-10-10 18:23, PROVED 19:00

Lead of the window side. Status words as in `bigbox/THEOREM_G20.md`: COMPUTED / PROVED; ACCEPTED
means: accepted by both frozen checkers in the lead's acceptance run, the record not yet reviewed.

**STATUS: PROVED (2026-10-10 19:00) as a statement about the numbers of the region file** (status words of
`bigbox/THEOREM_G20.md`): the certificate is accepted by both frozen checkers with the lead's post-check (18:23),
and this record is reviewed by a reviewer that wrote none of it, nor the certificate, nor the tools
(`reviews/join_roots/batch7/REVIEW_EJPA_v5.md`, sha256 623d8b32ac871925...: its own run of the
earlier reviewers' program on this certificate, unchanged, 126 checks, 125 ok and one FAIL that is no defect (the
program does not know the digest of Codex's manifest that the section on use quotes); 54 exact checks of its own
by hand: the corollary, the statement file, "the region in words" number by number, every claim of the section on
use, the arc of label 9 against the clause of the capture side's text; ALL 281 leaves against the root; verdict:
"PROVED as it stands", no correction required, nothing overstates; two optional notes, taken in this version).
Limits, as the reviewer states them: it did not run the two checkers, so the 281 `0` steps (12,439,907 terms) and
the exact values L rest on the two frozen checkers' reports (the program recomputed the node digests of both
reports from the file on disk and found the same L in both); the program it ran is the earlier reviewers', run
unchanged; not checked: the region file against the class files (PB_j, the loose slots, T9's slot and its gate
end, HULLW_11), except label 9's end x = 53/100 (exact, by the file's frame rule) and v5 against v1 = v2 (exact);
the generator of the v5 files and `cmp_v5.py`; the capture side (no class statement, certificate or receipt; of
Codex's manifest only the quoted states and the clause's sentence; the premise of amendment A, KEY_W exact, is the
capture side's); the composition (read where quoted, not re-proved); of the record's 281 table rows only what the
program compares. As for every record of this kind, the soundness of SPEC 3.0 and of the two frozen checkers is
taken from their own reviews (`reviews/REVIEW_30*.md`), and nobody but the producer has read how the leaves were
made (not needed: the certificate is checked, not the way it was made).
The record is written by `acceptance/mk_record.py` (its branch for kind A, first used here) in the form of
`RECORD_EJPG17m_v2.md` (reviewed at 01:03); every number is taken from the files (facts output
`acceptance/JPA_v5_facts.out`, sha256 05c324fdaf48e31d..., of `acceptance/region_facts.py`: all its checks ok), and the
reviewer compared the numbers with its own reading of the files.
**This is a statement about a region, NOT about a case of the proof:** that the capture side puts a packing into
this region needs its class statements (their state is the capture side's bookkeeping, quoted in the section on
use and not checked here).

## Statement

(E_JPA, v5). Let seventeen closed unit squares with pairwise disjoint interiors lie in [0, S]^2 with
S <= Sref = 4675530093604551/10^15, labelled 1 to 17, with one side direction a_i chosen for each square.
Then it is NOT the case that every xi_ik lies in the interval [lo_ik, hi_ik] and every a_i lies in the root arc of
label i, where the 34 intervals and the 17 arcs are those of

    bigbox/join/JPA_exact_v5.json   (entries window.box and root_arc)
    sha256 adcf0d1bdc02b8ea3d3f6253c6643caa2d8865427b8e6b8b91ea795f9352ff89

In words: no packing of seventeen unit squares of side at most Sref lies in the region JPA v5. Coordinates xi_ik as in SPEC 3.0 section 1, from the reference file `upper-packing-certificate.json`
(sha256 24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7, the one in the certificate's header, used
by both checkers); frame (container corner at the origin): SPEC 3.0 section 0.

This is the EMPTINESS COROLLARY of SPEC 3.0 (`SPEC_v3.0_NOTES.md`, note of 2026-10-09 18:38): the certificate
satisfies all conditions of section 7 and no node is closed as terminal, so the set F(root) is empty; and a
configuration that is feasible for a side S <= Sref is feasible for the side Sref (SPEC 3.0 section 11).

The region in words (`JOIN_ROOTS.md`, sections 1, 9.3 and 11.1; arcs read from the region file, in rad from
each label's reference direction): case T of the join design, kind A: label 9 ABOVE its gate, [+0.099901, +0.786228], in T9's rectangle off the wall column (class-frame x >= 53/100, rounded down to the grid: xi_(9,1) >= -87219/500000); label 3 any direction; label 17 any direction; label 15 any direction; label 4 with any direction; the loose labels 3, 4, 15, 17 in their slots; the twelve rigid labels 1, 2, 5 to 8, 10 to 14, 16 in their boxes PB_j, **label 11 in one box and one arc that contain its old target PB_11 and its new target HULLW_11** (the hull of the v2 factor and the transported new target, `JOIN_ROOTS.md` section 11.1; more than the union of the two targets; tag v5: xi_(11,1) in [-140801/1000000, 12647/62500], direction in [-0.137499811, +0.204999690]).

## Evidence

| what | value |
|---|---|
| certificate | `local-research/claude-20261002/results/assembly/JPA_v5/JPA_v5.cert.jsonl.gz`, 1,704,473,363 bytes, sha256 b9f9283979d2fab1f20307ac09f988e23dbd3b51abb827b9982c50c48214d2a7; uncompressed stream a935595a1f22fe641d157e7d7468316a14e40f80cdfbb4829603f6e847cc5a79 |
| its shape (read from the certificate) | 416 nodes, depth 11 in the Node checker's count (root = 0): 135 splits (42 arc, 0 box, 93 option) and 281 leaves closed by a `0` step; no terminal leaf; 281 steps, 12,439,907 terms, 10628 declarations. Cuts: direction of label 3 cut 2 times (tan-half from its reference direction: -659/5000, 659/5000); direction of label 15 cut 6 times (tan-half from its reference direction: -659/5000, 659/5000); direction of label 17 cut 18 times (tan-half from its reference direction: -659/5000, 659/5000); 27 option splits of the pair (14, 17) with 3 / 4 children; 13 option splits of the pair (9, 12) with 4 children; direction of label 9 cut 16 times (tan-half from its reference direction: 563/2500); 25 option splits of the pair (12, 15) with 4 children; 14 option splits of the pair (7, 9) with 3 children; 14 option splits of the pair (9, 11) with 3 / 4 children. The description has no `recentre`: every split node has the root's centre for every label; the leaves keep their leaf files' own nodes, and 278 of the 416 nodes reach beyond the root node in some arc (list in the facts output), which SPEC 3.0 section 6 allows: a child only has to contain its piece. **Label 11 is never cut: its box and arc are the root's in every node.** |
| exact values of the `0` steps | all positive; the smallest is L = 4.182982e-04 at `pH11W37A110wk1.n0.JPAv5.leaf`; the same rational number in both checkers' reports for each of the 281 leaves (table below) |
| producer | the audit lead: description by its `regiontree.py` (sha256 of the description 7f82aa23b94828e4...), certificate by the assembler `proto30/hull_tree.py` 8af834ec6ccff429... (exit 0, 15859.3 s). Its own run of both frozen checkers under `--keep-going`: 416 of 416 nodes accepted by each (`JPA_v5.run.json`, sha256 9805254d6a52c09f...) |
| acceptance run | `locks/run_slot.sh acceptance/accept_tree30.sh JPA_v5 <certificate> bigbox/join/EXPECT_JPA_v5.json`, by the lead, 2026-10-10 15:36:08 to 18:23 on the Mac. Python checker 8323.25 s (718 MB), Node checker 1643.09 s (4.77 GB). The run read the producer's work file in place (path in the log's first line), started in parallel with the producer's own checker run: the same bytes, sha256 equal to the named one before and after the run (`acceptance/BATCH_1536.log`) and equal to the file under `results/assembly/JPA_v5/` named in the first row, from which the facts were made |
| log | `acceptance/ACCEPT_JPA_v5.log`, sha256 7b9b9eaa427dba254237c5bd703058041884d91e5bb42a393387e0c03b89eea4: `RESULT: ACCEPTED`, exit code of the run 0 |
| checker reports | `acceptance/JPA_v5_C1.json` (Python, sha256 70adbc6f59e2ad5e...), `acceptance/JPA_v5_C2.json` (Node, sha256 8db1d58ea5211e70...) |
| frozen files | `checker/wxcheck_v30.py` cf8db52bfa1cc565..., `checker2/wxcheck2_v30.js` 97210adf74a3ebed..., `SPEC_v3.0.md` 0a6dfc2ae10ed6f3... (`acceptance/FROZEN_30.json`) |
| statement file | `bigbox/join/EXPECT_JPA_v5.json`, sha256 a76bfcad84e5279a5e66a6220b2b8990ce5dd2390da171b34da0a352036af29e: 17 labels, S_floor = Sref, `terminal_leaves` 0, `root_region` = the file above |

Lines of the log that carry the statement: both checkers, started with their default options, exit 0 with PASS on
the whole file; every node accepted by both; same node ids and the same closure kind per node in both reports;
nodes 416, infeasible 281, split 135, terminal 0; the root node has parent null, an empty assumption list, the
region's side interval, the region's box in all 68 interval ends and the region's arc for every label (centre and
both end rotations).

The 281 leaves closed by a `0` step (L from the Python report; "L sha256" = sha256 of the fraction as the report
writes it; in every row the Node report has the same rational number and the audit lead's assembler
report the same fraction, `L_exact`; all placed by containment, `LEAF_FORMAT_RULING.md`):

| leaf node | leaf file sha256 | terms | L | L sha256 | options assumed |
|---|---|---|---|---|---|
| pH11W37A110wk1.n0.JPAv5.leaf | ca530b00404ff17a... | 41,863 | 0.0004183 | 210ece27d333e494... | 14:17:a:p, 7:9:b:m |
| pH11W37A000wu.n0.0.JPAv5.leaf | 15a1adde2b0f8768... | 42,283 | 0.0007365 | 0d28feb4e224de38... | 14:17:a:p |
| pH11W37A510wuk4.n0.JPAv5.leaf | dd1c25432fe6e3d8... | 45,256 | 0.0010766 | 3e7dbc937c822be4... | 17:14:a:m |
| pH11W37A550wuk2k3.n0.1.JPAv5.leaf | e81304646c4b8b0f... | 42,725 | 0.0013329 | 2d9d09ffc076ae58... | 14:17:a:p, 12:9:a:m, 9:7:a:p, 9:11:b:m |
| pH11W37A550wuk5k2k3rk1.n0.JPAv5.leaf | e4ab6f594bab4e10... | 41,887 | 0.0013359 | 4e39af88e3014f7a... | 17:14:a:m, 12:9:a:m, 9:7:a:p, 9:11:b:m |
| pH11W37A550wuk5k1k2k1.n0.JPAv5.leaf | 114049d46d324b48... | 42,352 | 0.0013477 | 49bd6f48a3dd7f19... | 17:14:a:m, 9:12:b:m, 9:7:a:p, 9:11:b:m |
| pH11W37A151wuk2.n0.JPAv5.leaf | 3b04b0f5cb1938f1... | 43,352 | 0.0013734 | 66de4cf919d2187b... | 14:17:a:p, 9:12:b:m |
| pH11W37A155wuk6k2.n0.JPAv5.leaf | 956fb8373a931a07... | 43,917 | 0.0014205 | eb8db8ab89007f1c... | 17:14:b:m, 9:12:b:m |
| pH11W37A050wk1k3.n0.0.JPAv5.leaf | 4c113e43ee855b9b... | 40,803 | 0.0018716 | 6df63c532671006a... | 14:17:a:p, 12:9:a:m, 9:7:a:p, 9:11:b:m |
| pH11W37A550wuk5k2.n0.0.0.JPAv5.leaf | 489237d71f9b770a... | 43,248 | 0.0020745 | 5cdc6b6662ee4ea1... | 17:14:a:m, 12:9:a:m, 7:9:b:m |
| pH11W37A550wu.n0.0.0.0.JPAv5.leaf | 63c98aa5c0312a9f... | 44,198 | 0.0021091 | cf4045f1312e0cb3... | 14:17:a:p, 9:12:b:m |
| pH11W37A550wuk2.n0.0.0.JPAv5.leaf | eee5dd6717329740... | 42,762 | 0.0021112 | e510ca37b4dd8304... | 14:17:a:p, 12:9:a:m, 7:9:b:m |
| pH11W37A550wuk5k4.n0.JPAv5.leaf | 3e71527966b3d015... | 43,674 | 0.0022027 | 82952cfc40aa3714... | 17:14:a:m, 9:12:a:p |
| pH11W37A550wuk4.n0.JPAv5.leaf | 9faaa7e02bea4eb5... | 43,031 | 0.0022412 | 75992fc6a2b05932... | 14:17:a:p, 9:12:a:p |
| pH11W37A050wk1.n0.0.0.JPAv5.leaf | 8e8268980e6fc33d... | 40,002 | 0.0024041 | 6f654ad190085c51... | 14:17:a:p, 12:9:a:m, 7:9:b:m |
| pH11W37A050w.n0.0.0.0.JPAv5.leaf | da6a945411739466... | 40,914 | 0.0024057 | f6142349cb3616d0... | 14:17:a:p, 9:12:b:m |
| pH11W37A115wu.n0.2.JPAv5.leaf | 54076de3c58aeb26... | 44,797 | 0.0024505 | 42e6f4cb0108ff56... | 17:14:b:m |
| pH11W37A551wuk5k6.n0.JPAv5.leaf | c8dc567cf6c5d700... | 43,974 | 0.0025216 | 0cd6785433f15d55... | 17:14:a:m, 12:9:b:p |
| pH11W37A050wk2.n0.JPAv5.leaf | 2b5b5ea782f9a323... | 42,203 | 0.0025338 | c7c1264c1e58ecc2... | 14:17:a:p, 9:12:a:p |
| pH11W37A110wk5k6.n0.JPAv5.leaf | eb73a8c580645fe3... | 44,668 | 0.0026562 | 26259e36466517c6... | 17:14:b:m, 9:7:a:p |
| pH11W37A010wk5.n0.JPAv5.leaf | 9421eb8fb90a0dcd... | 43,001 | 0.0026871 | 1e1ab005d1f930eb... | 14:17:a:p, 9:7:b:p |
| pH11W37A151wuk4.n0.JPAv5.leaf | cf6990347d065809... | 45,403 | 0.0026916 | 596fc2d635f658ad... | 14:17:a:p, 12:9:b:p |
| pH11W37A150wuk3k3.n0.1.JPAv5.leaf | d32f6380b0f2a136... | 42,062 | 0.0027579 | 3c7fd0a6dbc89b6e... | 14:17:a:p, 12:9:a:m, 9:7:a:p, 9:11:b:m |
| pH11W37A155wuk3.n0.JPAv5.leaf | c144b198a9e2787a... | 45,316 | 0.0029150 | 23da47a971940376... | 14:17:a:p, 12:9:b:p |
| pH11W37A551wuk3.n0.JPAv5.leaf | 53c335c079852684... | 44,733 | 0.0029627 | c48de5c448957287... | 14:17:a:p, 12:9:b:p |
| pH11W37A150wu.n0.0.0.0.JPAv5.leaf | 9f4ff5d940d21934... | 41,788 | 0.0030308 | d9072feb5fad6322... | 14:17:a:p, 9:12:b:m |
| pH11W37A150wuk3k1.n0.JPAv5.leaf | 48d52f26d1daac56... | 42,571 | 0.0030402 | 4581a1ea95f31ab4... | 14:17:a:p, 12:9:a:m, 7:9:b:m |
| prH11W37A550wuk5k1k1a.n0.JPAv5.leaf | c8f5b488e090712e... | 43,786 | 0.0030499 | 3ab4fecc157db971... | 17:14:a:m, 9:12:b:m, 7:9:b:m, 15:12:b:m |
| pH11W37A110wk3.n0.JPAv5.leaf | 1a780170fedcc10f... | 45,925 | 0.0031677 | b38447f8ee7b5cac... | 14:17:a:p, 9:7:b:p |
| pH11W37A150wuk5.n0.JPAv5.leaf | 033c857d950d9b66... | 42,781 | 0.0031960 | b14bac888212d9bf... | 14:17:a:p, 9:12:a:p |
| pH11W37A010wk3.n0.JPAv5.leaf | 5e0b30703ba3b5bc... | 38,985 | 0.0032037 | a5d9a60e0bf9683d... | 14:17:a:p, 7:9:b:m |
| pH11W37A555wuk8k3.n0.JPAv5.leaf | 0841f9d38dbea24a... | 45,614 | 0.0032063 | 74be97c5aef762ed... | 17:14:a:m, 12:9:b:p |
| pH11W37A111wu.n0.2.JPAv5.leaf | f42117b5aa98f714... | 46,035 | 0.0032145 | a69e2875bb6caab7... | 17:14:b:m |
| pH11W37A555wuk6.n0.JPAv5.leaf | 9236108319077161... | 43,999 | 0.0032243 | df8949fe71055051... | 14:17:a:p, 12:9:b:p |
| pH11W37A151wuk7k3.n0.JPAv5.leaf | bd44c9124968cd46... | 45,234 | 0.0032557 | 7882e637d26a7f1a... | 17:14:b:m, 12:9:b:p |
| pH11W37A550wuk5k3.n0.JPAv5.leaf | 38f44c30b43331ed... | 45,881 | 0.0032653 | e901ecef421f8ab8... | 17:14:a:m, 12:9:b:p |
| pH11W37A511wu.n0.1.JPAv5.leaf | c940d19c40d5f3d3... | 45,736 | 0.0033645 | cb096a26459a79fd... | 17:14:a:m |
| pH11W37A150wuk7k1.n0.0.0.JPAv5.leaf | 47491e2552672881... | 41,286 | 0.0033894 | d07d1ac6d0644ccc... | 17:14:b:m, 9:12:b:m, 7:9:b:m |
| pH11W37A150wuk7k2.n0.0.0.JPAv5.leaf | d68f797a5a934ae5... | 41,654 | 0.0033912 | bb4e8bf4dd570075... | 17:14:b:m, 12:9:a:m, 7:9:b:m |
| pH11W37A515wu.n0.0.JPAv5.leaf | 0ea400db7dd45d5b... | 45,780 | 0.0034338 | db5b15b17b0fa18e... | 14:17:a:p |
| pH11W37A511wu.n0.0.JPAv5.leaf | a168d84b08b68d0d... | 46,512 | 0.0034460 | 15a919ac358f11d9... | 14:17:a:p |
| pH11W37A515wu.n0.1.JPAv5.leaf | 10f829611bdd61ad... | 46,377 | 0.0034468 | d5816b5a5e2b9b5d... | 17:14:a:m |
| pH11W37A550wuk3.n0.JPAv5.leaf | 0f259b67386614e7... | 43,785 | 0.0035130 | f3770e7865a890c0... | 14:17:a:p, 12:9:b:p |
| pH11W37A150wuk7k4.n0.JPAv5.leaf | 91909c94345f1544... | 42,865 | 0.0035651 | a1e7827c4aa08f68... | 17:14:b:m, 9:12:a:p |
| pH11W37A510wuk2.n0.JPAv5.leaf | d638843814506a36... | 43,393 | 0.0035924 | dda55a33ae3f20d3... | 14:17:a:p, 9:7:a:p |
| pH11W37A155wuk6k4.n0.JPAv5.leaf | 5b4990022f567d73... | 45,006 | 0.0037005 | ea2457da7cec97a1... | 17:14:b:m, 12:9:b:p |
| pH11W37A110wk5k7.n0.JPAv5.leaf | 886d624646c07884... | 42,964 | 0.0038614 | 49098398885d42dc... | 17:14:b:m, 9:7:b:p |
| pH11W37A510wu.n0.0.0.0.JPAv5.leaf | 69d1af66a75957b0... | 42,889 | 0.0038679 | 3994b52763cd2248... | 14:17:a:p, 7:9:b:m |
| pH11W37A115wu.n0.0.JPAv5.leaf | e2b55626afbc1f57... | 45,235 | 0.0039096 | 974b5f53c27630c1... | 14:17:a:p |
| pH11W37A100wu.n0.0.JPAv5.leaf | 649f45b6d532ae75... | 40,340 | 0.0039806 | 69cf28ed722036f0... | 14:17:a:p |
| pH11W37A100wu.n0.2.JPAv5.leaf | 5c55037f4b361e11... | 37,145 | 0.0039823 | c27ad7c30f28bc0f... | 17:14:b:m |
| pH11W37A110wk5k5.n0.JPAv5.leaf | 0590c987b4133aa0... | 41,610 | 0.0041066 | 01e927d9a6e07235... | 17:14:b:m, 7:9:b:m |
| pH11W37A510wuk1.n0.JPAv5.leaf | 42211385074f094c... | 40,519 | 0.0041640 | 89b4d9efc56f3e3c... | 14:17:a:p, 7:9:b:m |
| pH11W37A150wuk4.n0.JPAv5.leaf | b464cffe84d5b46f... | 47,175 | 0.0044010 | 9013881fe9a28e74... | 14:17:a:p, 12:9:b:p |
| pH11W37A050wk3.n0.JPAv5.leaf | d3f34be809129e76... | 45,081 | 0.0044475 | 0a3173665dbb6e08... | 14:17:a:p, 12:9:b:p |
| pH11W37A111wu.n0.0.JPAv5.leaf | d7f4e7517ca1885b... | 47,823 | 0.0049057 | 98ae725b71565a72... | 14:17:a:p |
| pH11W37A101wu.n0.0.JPAv5.leaf | e6bb93e83c9be1ae... | 42,194 | 0.0049745 | e99870007e1fdbe3... | 14:17:a:p |
| pH11W37A101wu.n0.2.JPAv5.leaf | 9fd5bf35aee0c1b7... | 41,031 | 0.0052613 | e6b9f484908be961... | 17:14:b:m |
| pH11W37A105wu.n0.0.JPAv5.leaf | ed57dfc12fc56610... | 42,559 | 0.0057613 | 60be87176098e4a4... | 14:17:a:p |
| pH11W37A050wk4.n0.JPAv5.leaf | 9b8d7640478a7c16... | 39,307 | 0.0059707 | db9b118488f71738... | 17:14:a:m |
| pH11W37A010wk6.n0.JPAv5.leaf | 35f3838c6559a175... | 38,874 | 0.0060051 | 44f511a4fdfef1b8... | 17:14:a:m |
| pH11W37A105wu.n0.2.JPAv5.leaf | 7fd7120c7e50f772... | 42,943 | 0.0064280 | 62be1dae53861389... | 17:14:b:m |
| pH11W37A500wu.n0.0.JPAv5.leaf | 730febf774ae9e62... | 40,666 | 0.0065842 | 8484c0ecc32ee1e3... | 14:17:a:p |
| pH11W37A500wu.n0.1.JPAv5.leaf | 703f48f517d6a948... | 40,984 | 0.0065858 | 65fc43547c0b45e5... | 17:14:a:m |
| pH11W37A550wuk5k1k2.n0.0.JPAv5.leaf | 9f9992ddf3605e8f... | 39,370 | 0.0067550 | 929f46c8af1792b0... | 17:14:a:m, 9:12:b:m, 9:7:a:p, 11:9:b:p |
| pH11W37A050wk1k4.n0.JPAv5.leaf | eaf9e5cdcfdbf5b5... | 39,007 | 0.0067602 | e2e7847330569553... | 14:17:a:p, 12:9:a:m, 9:7:b:p |
| pH11W37A550wuk2k3.n0.0.JPAv5.leaf | 48b1e4808267e5e9... | 39,805 | 0.0067743 | f7d8b50175036a95... | 14:17:a:p, 12:9:a:m, 9:7:a:p, 11:9:b:p |
| pH11W37A550wuk5k2k3r.n0.0.JPAv5.leaf | ea2f4a025e74d428... | 42,483 | 0.0068224 | c2908b1539d22178... | 17:14:a:m, 12:9:a:m, 9:7:a:p, 11:9:b:p |
| pH11W37A550wuk2k4.n0.JPAv5.leaf | 000118ab643d7fa8... | 42,208 | 0.0072892 | 451c815280f1449e... | 14:17:a:p, 12:9:a:m, 9:7:b:p |
| pH11W37A550wuk5k2k4.n0.JPAv5.leaf | e8caa8b4e849510b... | 42,265 | 0.0072897 | 6ad206fd7b3c3393... | 17:14:a:m, 12:9:a:m, 9:7:b:p |
| pH11W37A550wuk5k1k3.n0.JPAv5.leaf | 7d5350384953384c... | 43,166 | 0.0073421 | 9e431d2c4c9fcfa0... | 17:14:a:m, 9:12:b:m, 9:7:b:p |
| pH11W37A551wuk5k7.n0.JPAv5.leaf | f6fba81fd4c8f7cc... | 44,178 | 0.0074430 | 33a3c15aa0050b45... | 17:14:a:m, 9:12:a:p |
| pH11W37A155wuk1.n0.0.0.JPAv5.leaf | c787a248d8af3509... | 42,573 | 0.0077753 | baf353a33e857ea5... | 14:17:a:p, 9:12:b:m, 7:9:b:m |
| pH11W37A501wu.n0.1.JPAv5.leaf | 989d00cff3a070a8... | 42,505 | 0.0078468 | 43db9d4172f8d3ab... | 17:14:a:m |
| pH11W37A551wuk4.n0.JPAv5.leaf | e2b1c248dcf03bff... | 43,580 | 0.0078588 | 164bd427945189fd... | 14:17:a:p, 9:12:a:p |
| pH11W37A555wuk7.n0.JPAv5.leaf | c80545efd7a47a1f... | 43,865 | 0.0078725 | a1493cdb66af2eca... | 14:17:a:p, 9:12:a:p |
| pH11W37A151wu.n0.0.0.0.JPAv5.leaf | 202f1725e0fad9ea... | 42,011 | 0.0079295 | b4a296874d2e07b4... | 14:17:a:p, 9:12:b:m |
| pH11W37A555wuk8k4.n0.JPAv5.leaf | 0987f64ae9f9ff60... | 44,022 | 0.0079313 | ea199be7f5a61964... | 17:14:a:m, 9:12:a:p |
| pH11W37A155wuk4.n0.JPAv5.leaf | 2d99badba122dbe9... | 43,459 | 0.0081242 | 4368b48499cfbe22... | 14:17:a:p, 9:12:a:p |
| pH11W37A501wu.n0.0.JPAv5.leaf | cb60209918438f2a... | 41,543 | 0.0081518 | 9e983c88110e0afe... | 14:17:a:p |
| pH11W37A151wuk5.n0.JPAv5.leaf | 571f7f6655545d4d... | 43,855 | 0.0082994 | 7e38f49190cd6004... | 14:17:a:p, 9:12:a:p |
| pH11W37A510wuk3.n0.JPAv5.leaf | 7369634a19b075f1... | 42,701 | 0.0084519 | 044e2763dcd18f17... | 14:17:a:p, 9:7:b:p |
| pH11W37A150wuk3k4.n0.JPAv5.leaf | e3c8caff1b885e56... | 41,482 | 0.0089208 | 8db78e842db43953... | 14:17:a:p, 12:9:a:m, 9:7:b:p |
| pH11W37A155wuk6.n0.0.0.JPAv5.leaf | 8bb5194e434ecb68... | 42,861 | 0.0089330 | 4f257b5332bf866e... | 17:14:b:m, 9:12:b:m |
| pH11W37A050wk1.n0.0.1.0.JPAv5.leaf | 5ebae509e3b2bc9d... | 38,469 | 0.0090870 | 74986a4e76840fb9... | 14:17:a:p, 12:9:a:m, 7:9:b:m, 9:11:b:m |
| pH11W37A050w.n0.0.0.1.0.JPAv5.leaf | 2f50f4f5f6de959f... | 39,688 | 0.0091012 | 734437f7e33b6905... | 14:17:a:p, 9:12:b:m, 9:11:b:m |
| pH11W37A550wuk2.n0.0.1.1.JPAv5.leaf | 90ba6f28f031d8fc... | 40,792 | 0.0091618 | 9ad6d42f06b1a05a... | 14:17:a:p, 12:9:a:m, 7:9:b:m, 9:11:b:m |
| pH11W37A150wuk3k3.n0.0.JPAv5.leaf | f9f6d35fe5129acb... | 39,508 | 0.0091745 | 943e0718a8a329b3... | 14:17:a:p, 12:9:a:m, 9:7:a:p, 11:9:b:p |
| pH11W37A550wuk1.n0.1.JPAv5.leaf | ee288b96cf3c4771... | 42,099 | 0.0091812 | a160ad57f0bb5ac9... | 14:17:a:p, 9:12:b:m, 9:11:b:m |
| pH11W37A550wuk5k2k2k2r.n0.JPAv5.leaf | 0d1514a188c98c38... | 40,858 | 0.0091901 | 0ec5442e6d84f13c... | 17:14:a:m, 12:9:a:m, 7:9:b:m, 9:11:b:m |
| pH11W37A151wuk7k4.n0.JPAv5.leaf | 8c3cb666ca36ad73... | 43,399 | 0.0092236 | f11b4bd4b53a96fd... | 17:14:b:m, 9:12:a:p |
| pH11W37A155wuk6k5.n0.JPAv5.leaf | 55bf1a2984a3a855... | 42,317 | 0.0093019 | 27accf3de96877bf... | 17:14:b:m, 9:12:a:p |
| pH11W37A150wuk7k2k3.n0.0.JPAv5.leaf | cbc9b80c141417c8... | 36,932 | 0.0095739 | 0968ee92c16415e6... | 17:14:b:m, 12:9:a:m, 9:7:a:p, 15:12:b:m |
| pH11W37A150wuk7k1k2.n0.0.JPAv5.leaf | 73b83dc46637b34b... | 40,951 | 0.0096261 | 69e821a4c7a9bbc2... | 17:14:b:m, 9:12:b:m, 9:7:a:p, 15:12:b:m |
| pH11W37A150wuk7k2k4.n0.JPAv5.leaf | 419322b57998ff92... | 42,886 | 0.0098657 | 3cb83fe377a01dbe... | 17:14:b:m, 12:9:a:m, 9:7:b:p |
| pH11W37A150wuk7k1k3.n0.JPAv5.leaf | 2f0c55a51ffdae8c... | 42,190 | 0.0099204 | fe3a88405102c26c... | 17:14:b:m, 9:12:b:m, 9:7:b:p |
| pH11W37A550wuk5k2k2k3r.n0.JPAv5.leaf | a01a995fc26c41af... | 44,978 | 0.0100001 | 1845dbe3be531ad4... | 17:14:a:m, 12:9:a:m, 7:9:b:m, 9:11:a:m |
| pH11W37A550wuk5k2k3rk3.n0.JPAv5.leaf | a5a04cf1eb861521... | 45,335 | 0.0100001 | b641abec9ee07b48... | 17:14:a:m, 12:9:a:m, 9:7:a:p, 11:9:a:m |
| pH11W37A050wk1k3k3r.n0.JPAv5.leaf | 40b16ee852713f9a... | 43,195 | 0.0100001 | c7ee09b0a7807600... | 14:17:a:p, 12:9:a:m, 9:7:a:p, 11:9:a:m |
| pH11W37A555wuk9.n0.JPAv5.leaf | 1fc0ae0754c304b2... | 48,905 | 0.0100001 | 4fec1ec7cb6140c1... | 14:17:b:m |
| pH11W37A050wk1k3.n0.1.JPAv5.leaf | 188d1179a75a3927... | 36,456 | 0.0102756 | 53222b13aec38289... | 14:17:a:p, 12:9:a:m, 9:7:a:p, 11:9:b:p |
| pH11W37A000wu.n0.1.JPAv5.leaf | 17432ab18de3b21c... | 40,445 | 0.0105988 | 511090cc63347d7a... | 17:14:a:m |
| pH11W37A550wuk5k2k2.n0.0.JPAv5.leaf | 585f2a1ded42aa6c... | 39,731 | 0.0106035 | 47b6f522d273c15c... | 17:14:a:m, 12:9:a:m, 7:9:b:m, 11:9:b:p |
| pH11W37A550wu.n0.0.0.1.0.JPAv5.leaf | 2ffaa165777aca3a... | 40,468 | 0.0106194 | a3f93ba977d33e7f... | 14:17:a:p, 9:12:b:m, 11:9:b:p |
| pH11W37A550wuk2.n0.0.1.0.JPAv5.leaf | ff6371445906e6d6... | 40,594 | 0.0106380 | 4d90ce8eeb6b40be... | 14:17:a:p, 12:9:a:m, 7:9:b:m, 11:9:b:p |
| pH11W37A110wk2.n0.0.JPAv5.leaf | f84662d49d9dabc8... | 39,515 | 0.0120947 | f06e8aca34c9004a... | 14:17:a:p, 9:7:a:p, 15:12:b:m |
| pH11W37A150wuk7k3k3.n0.JPAv5.leaf | f40c1fd09b8a92c7... | 42,745 | 0.0122193 | bffc98be850490ba... | 17:14:b:m, 12:9:b:p, 9:7:b:p |
| pH11W37A150wu.n0.0.0.1.0.JPAv5.leaf | 53f3b06447202bf9... | 39,389 | 0.0128489 | 4da7fed764586cfc... | 14:17:a:p, 9:12:b:m, 11:9:b:p |
| pH11W37A150wuk3k2.n0.0.JPAv5.leaf | 5542a2042ad8f423... | 39,251 | 0.0128523 | 0c468d2f60d5cca5... | 14:17:a:p, 12:9:a:m, 7:9:b:m, 11:9:b:p |
| pH11W37A110w.n0.0.0.0.0.JPAv5.leaf | 88ace3fda1eaa710... | 38,822 | 0.0129631 | 4e04b4634d7e1bcc... | 14:17:a:p, 7:9:b:m, 15:12:b:m |
| pH11W37A505wu.n0.1.JPAv5.leaf | ad7a95c04b916587... | 43,212 | 0.0130190 | 62c8d79184226b17... | 17:14:a:m |
| pH11W37A505wu.n0.0.JPAv5.leaf | 5d3e3d08c9abd8c7... | 44,497 | 0.0132017 | 186c1337abaa243e... | 14:17:a:p |
| pH11W37A150wuk3k2.n0.1.JPAv5.leaf | 3e167d58bfc61041... | 36,782 | 0.0133575 | c39a05a33b189b81... | 14:17:a:p, 12:9:a:m, 7:9:b:m, 9:11:b:m |
| pH11W37A150wuk7k2.n0.0.1.1.JPAv5.leaf | 5ff8c24c8fa856b8... | 39,419 | 0.0134101 | cfd535da5d0cd725... | 17:14:b:m, 12:9:a:m, 7:9:b:m, 11:9:b:p |
| pH11W37A150wu.n0.0.0.1.1.JPAv5.leaf | c6eec8c6ed2ff12e... | 40,843 | 0.0134141 | b563d2aa045e9f6e... | 14:17:a:p, 9:12:b:m, 9:11:b:m |
| pH11W37A150wuk7k1k1.n0.1.JPAv5.leaf | 609ce754be45c6e9... | 39,322 | 0.0134157 | 88677854fc23bbcc... | 17:14:b:m, 9:12:b:m, 7:9:b:m, 11:9:b:p |
| pH11W37A010w.n0.0.0.0.0.JPAv5.leaf | cdc718ad7de3dd24... | 35,313 | 0.0134348 | 1280b618f245fc36... | 14:17:a:p, 7:9:b:m, 15:12:b:m |
| pH11W37A110wk5.n0.0.0.0.JPAv5.leaf | 7595725f8194e37a... | 36,732 | 0.0134390 | 4e19b0aeb7ab63d3... | 17:14:b:m, 7:9:b:m, 15:12:b:m |
| pH11W37A150wuk7k3k2.n0.JPAv5.leaf | ef4c8bc8559397a5... | 42,761 | 0.0137274 | 854e4d9856ca4f1f... | 17:14:b:m, 12:9:b:p, 9:7:a:p |
| pH11W37A150wuk7k1k1.n0.0.JPAv5.leaf | 3ab3bd506a23ad6b... | 36,246 | 0.0142368 | 9e1c2fc78b9fdd17... | 17:14:b:m, 9:12:b:m, 7:9:b:m, 9:11:b:m |
| pH11W37A150wuk7k2.n0.0.1.0.JPAv5.leaf | a05140fba5801d65... | 38,574 | 0.0142750 | 9585607fea32395e... | 17:14:b:m, 12:9:a:m, 7:9:b:m, 9:11:b:m |
| pH11W37A155wuk2k6.n0.JPAv5.leaf | b6f62c138fd044b6... | 41,813 | 0.0151607 | 2c48d87f5684f520... | 14:17:a:p, 12:9:a:m, 9:7:b:p |
| pH11W37A155wuk1k3.n0.JPAv5.leaf | cad7c618f963387c... | 42,135 | 0.0152012 | 6de72dd3e6bc0bbc... | 14:17:a:p, 9:12:b:m, 9:7:b:p |
| pH11W37A015wu.n0.0.JPAv5.leaf | 76ccb17ce2edad42... | 44,616 | 0.0154151 | 0ef0241ac115b956... | 14:17:a:p |
| pH11W37A155wuk2.n0.0.0.JPAv5.leaf | c3a3dcb0289d0234... | 42,283 | 0.0157859 | 7f41e21e1342dffd... | 14:17:a:p, 12:9:a:m, 7:9:b:m, 15:12:b:m |
| prH11W37A550wuk5k1k1c.n0.JPAv5.leaf | cc4fbcc989e87c75... | 40,922 | 0.0158487 | 8fd015483efeb23c... | 17:14:a:m, 9:12:b:m, 7:9:b:m, 12:15:b:p |
| pH11W37A010wk4k1.n0.JPAv5.leaf | 3ca11bb43e7d24bf... | 33,542 | 0.0160393 | fed0f7926cd6c133... | 14:17:a:p, 9:7:a:p, 15:12:b:m |
| pH11W37A050wk1.n0.0.1.1.JPAv5.leaf | a50c5c66819e3228... | 34,893 | 0.0166396 | 49319263fcae6e45... | 14:17:a:p, 12:9:a:m, 7:9:b:m, 11:9:b:p |
| pH11W37A050w.n0.0.0.1.1.JPAv5.leaf | 3a03ec90ed0725c6... | 38,122 | 0.0166651 | 9a99be91210da33b... | 14:17:a:p, 9:12:b:m, 11:9:b:p |
| pH11W37A151wuk3.n0.0.JPAv5.leaf | fe8fa6f3bba99af2... | 42,009 | 0.0168223 | b8e8de8bdcf23097... | 14:17:a:p, 12:9:a:m, 15:12:b:m |
| pH11W37A555wuk5.n0.0.JPAv5.leaf | ee4dda7872432779... | 42,696 | 0.0171892 | ff260cc4f93103cd... | 14:17:a:p, 12:9:a:m, 15:12:b:m |
| pH11W37A555wu.n0.0.0.0.JPAv5.leaf | e396b631c229f585... | 42,911 | 0.0171952 | 3bc1e63eb583f72b... | 14:17:a:p, 9:12:b:m, 15:12:b:m |
| pH11W37A011wu.n0.0.JPAv5.leaf | 03bc7f03392063b4... | 44,077 | 0.0172705 | 3e301e87feb346a9... | 14:17:a:p |
| pH11W37A555wuk8k1.n0.0.JPAv5.leaf | 2821fba44f7f70be... | 41,929 | 0.0173754 | 1c873d1d74225a90... | 17:14:a:m, 9:12:b:m, 15:12:b:m |
| pH11W37A555wuk8k2.n0.0.JPAv5.leaf | ed7c7951384f4907... | 42,519 | 0.0173779 | 11fbb9174bedc892... | 17:14:a:m, 12:9:a:m, 15:12:b:m |
| pH11W37A155wuk6k3.n0.0.JPAv5.leaf | 347b79c9581a67a9... | 42,341 | 0.0178266 | fc7218ccb129f9e6... | 17:14:b:m, 12:9:a:m, 15:12:b:m |
| pH11W37A551wuk2.n0.0.JPAv5.leaf | 8b9bf3c898da4409... | 41,770 | 0.0183824 | 12c54a992f332604... | 14:17:a:p, 12:9:a:m, 15:12:b:m |
| pH11W37A551wuk1.n0.0.JPAv5.leaf | a8082d8219c34aad... | 42,692 | 0.0184066 | 071ba877e3e4f1e5... | 14:17:a:p, 9:12:b:m, 15:12:b:m |
| pH11W37A551wuk5k5.n0.0.JPAv5.leaf | f62bf691daeca79b... | 42,818 | 0.0184715 | e9fbc895ecc774bf... | 17:14:a:m, 12:9:a:m, 15:12:b:m |
| pH11W37A551wuk5.n0.0.0.JPAv5.leaf | e7dadfe7178bdcda... | 43,548 | 0.0184824 | e11c3e2837790c51... | 17:14:a:m, 9:12:b:m, 15:12:b:m |
| pH11W37A151wuk7k1k1.n0.JPAv5.leaf | 73fb07441da868e8... | 42,127 | 0.0186941 | 90c2bba73adabc8d... | 17:14:b:m, 9:12:b:m, 15:12:b:m |
| pH11W37A151wuk7k2.n0.0.JPAv5.leaf | 42589c31ad14f051... | 42,453 | 0.0187004 | 77d7f8ff20cc73f2... | 17:14:b:m, 12:9:a:m, 15:12:b:m |
| pH11W37A055wu.n0.0.JPAv5.leaf | ee10e83c05bd3ffb... | 44,631 | 0.0190753 | bd85cce794f5ca9b... | 14:17:a:p |
| pH11W37A150wuk7k3k1.n0.0.JPAv5.leaf | 1e768c3149a0b28e... | 39,344 | 0.0197087 | baf4b2609e68df68... | 17:14:b:m, 12:9:b:p, 7:9:b:m, 15:12:b:m |
| pH11W37A150wuk7k1k2.n0.2.JPAv5.leaf | ffbf5bbe17491e68... | 40,794 | 0.0203069 | 09ac5dba034b6504... | 17:14:b:m, 9:12:b:m, 9:7:a:p, 12:15:b:p |
| pH11W37A150wuk7k2k3.n0.2.JPAv5.leaf | 788b44baa618ca78... | 40,698 | 0.0203131 | 53ec3b4f2a319682... | 17:14:b:m, 12:9:a:m, 9:7:a:p, 12:15:b:p |
| pH11W37A155wuk1k2.n0.0.JPAv5.leaf | fce3ea7424131079... | 41,071 | 0.0221712 | d8366c2f22996322... | 14:17:a:p, 9:12:b:m, 9:7:a:p, 15:12:b:m |
| pH11W37A155wuk2k5.n0.0.JPAv5.leaf | 486e836390e3fa2c... | 41,659 | 0.0221834 | 3dee3a067ebe066d... | 14:17:a:p, 12:9:a:m, 9:7:a:p, 15:12:b:m |
| pH11W37A155wuk1k1.n0.0.JPAv5.leaf | 179b97e05fefd9e5... | 39,539 | 0.0225780 | 5b57f5e5f1ba995e... | 14:17:a:p, 9:12:b:m, 7:9:b:m, 15:12:b:m |
| pH11W37A051wu.n0.0.JPAv5.leaf | 9d0bfdfb6721e8f2... | 43,410 | 0.0257368 | 82d20bb75e59dc22... | 14:17:a:p |
| pH11W37A155wuk2k4.n0.JPAv5.leaf | 65f4502e9fc5bfff... | 43,183 | 0.0444406 | c375ce6d7cdb4bae... | 14:17:a:p, 12:9:a:m, 7:9:b:m, 12:15:b:p |
| pH11W37A155wuk6k3.n0.2.JPAv5.leaf | 4439fa4c0961aaa1... | 42,601 | 0.0447048 | e0ad3d686c6764e7... | 17:14:b:m, 12:9:a:m, 12:15:b:p |
| pH11W37A555wuk4.n0.JPAv5.leaf | cfc33841b4670876... | 41,400 | 0.0448111 | 56b073b4af5bfd85... | 14:17:a:p, 9:12:b:m, 12:15:b:p |
| pH11W37A555wuk5k4.n0.JPAv5.leaf | 7c5623aa2e6ebf9c... | 42,039 | 0.0448289 | 84f8eae3c13e6320... | 14:17:a:p, 12:9:a:m, 12:15:b:p |
| pH11W37A555wuk8k1k4.n0.JPAv5.leaf | 21f8e106654cd348... | 41,610 | 0.0448908 | 07ec28276f4ab101... | 17:14:a:m, 9:12:b:m, 12:15:b:p |
| pH11W37A555wuk8k2k4.n0.JPAv5.leaf | 8169a49d9a75fa2f... | 42,103 | 0.0448927 | 79bb24a7d41816e5... | 17:14:a:m, 12:9:a:m, 12:15:b:p |
| pH11W37A151wuk3.n0.3.JPAv5.leaf | ae3da6bfe7b6bd45... | 40,303 | 0.0489434 | 91931d860b9d6a03... | 14:17:a:p, 12:9:a:m, 12:15:b:p |
| pH11W37A151wuk7k2.n0.2.JPAv5.leaf | 615a43ccf94e3612... | 38,003 | 0.0490814 | 4eb9875e07107d8b... | 17:14:b:m, 12:9:a:m, 12:15:b:p |
| pH11W37A151wuk7k1k3.n0.JPAv5.leaf | 46c37de02dee3c85... | 39,780 | 0.0490875 | 0b915087c9966014... | 17:14:b:m, 9:12:b:m, 12:15:b:p |
| pH11W37A551wuk1.n0.3.JPAv5.leaf | df63f38a2aa5db2b... | 39,690 | 0.0493122 | e463465920ba0e41... | 14:17:a:p, 9:12:b:m, 12:15:b:p |
| pH11W37A551wuk2.n0.3.JPAv5.leaf | d03061938d7891c2... | 40,559 | 0.0493185 | 3e667db5f3c61a99... | 14:17:a:p, 12:9:a:m, 12:15:b:p |
| pH11W37A551wuk5k5.n0.3.JPAv5.leaf | e84021591966fd51... | 40,160 | 0.0493396 | bfd6fecb73d7935e... | 17:14:a:m, 12:9:a:m, 12:15:b:p |
| pH11W37A551wuk5k4.n0.JPAv5.leaf | 77bdd2839a01c785... | 41,885 | 0.0493518 | d05504b467af4cd7... | 17:14:a:m, 9:12:b:m, 12:15:b:p |
| pH11W37A155wuk2k5.n0.2.JPAv5.leaf | f51789f286d0369b... | 41,655 | 0.0496004 | 5d94a409410f1a6e... | 14:17:a:p, 12:9:a:m, 9:7:a:p, 12:15:b:p |
| pH11W37A155wuk1k2k3.n0.JPAv5.leaf | 471c192acbadf575... | 42,967 | 0.0496366 | a7e63d1d9abe3cbb... | 14:17:a:p, 9:12:b:m, 9:7:a:p, 12:15:b:p |
| pH11W37A155wuk1k1k2.n0.JPAv5.leaf | d62da4f6c195462a... | 44,561 | 0.0499034 | 3111e73d927ecf2a... | 14:17:a:p, 9:12:b:m, 7:9:b:m, 12:15:b:p |
| pH11W37A155wuk6k3.n0.1.JPAv5.leaf | 482e38e06e792927... | 47,548 | 1.2234099 | 09bbd5daf4730ed0... | 17:14:b:m, 12:9:a:m, 15:12:a:m |
| pH11W37A150wuk7k3k1.n0.3.JPAv5.leaf | 6d89719cec8121ff... | 46,080 | 1.3315289 | 305b34b126e248e5... | 17:14:b:m, 12:9:b:p, 7:9:b:m, 12:15:b:p |
| pH11W37A110wk2.n0.3.JPAv5.leaf | 1de7d06f72c01d87... | 47,181 | 3.0118502 | 13a8e71335e3b83c... | 14:17:a:p, 9:7:a:p, 15:12:a:p |
| pH11W37A150wuk7k1k2.n0.3.JPAv5.leaf | 7347300d8be159be... | 46,080 | 5.3950004 | a673c2e4fc2fbcef... | 17:14:b:m, 9:12:b:m, 9:7:a:p, 12:15:a:p |
| pH11W37A155wuk6k3.n0.3.JPAv5.leaf | fcbf55edffb2b694... | 47,548 | 6.5937554 | a453845cb4103bc0... | 17:14:b:m, 12:9:a:m, 12:15:a:p |
| pH11W37A551wuk5.n0.0.1.JPAv5.leaf | 22c8931e6f1de92e... | 47,915 | 7.0832570 | 89ef154535bc459b... | 17:14:a:m, 9:12:b:m, 12:15:a:p |
| prH11W37A550wuk5k1k1br.n0.JPAv5.leaf | 62a8a272ebd2de16... | 46,447 | 7.5466209 | ac95b8cf1b416962... | 17:14:a:m, 9:12:b:m, 7:9:b:m, 15:12:a:m |
| pH11W37A551wuk5k5.n0.2.JPAv5.leaf | 2e94bea5faf51d25... | 47,915 | 11.4732901 | 22faaf33231b4dce... | 17:14:a:m, 12:9:a:m, 15:12:a:m |
| pH11W37A151wuk7k1k4.n0.JPAv5.leaf | cf0f0e34f2a4fce5... | 47,548 | 12.2606506 | 1a937526e9ef3ab2... | 17:14:b:m, 9:12:b:m, 12:15:a:p |
| pH11W37A151wuk7k2.n0.3.JPAv5.leaf | 3bcabc692174931b... | 47,548 | 12.3219249 | fbe4083c5ad0ee07... | 17:14:b:m, 12:9:a:m, 12:15:a:p |
| pH11W37A010wk4k3.n0.JPAv5.leaf | 63f94f40b273465e... | 45,348 | 13.6709700 | 5008362ca17fed1c... | 14:17:a:p, 9:7:a:p, 15:12:a:p |
| pH11W37A110w.n0.0.0.0.1.JPAv5.leaf | 0b4f26f909c4aa8c... | 46,447 | 14.0045625 | ed29fa0d3f190dbc... | 14:17:a:p, 7:9:b:m, 12:15:b:p |
| pH11W37A155wuk1k1k3r.n0.JPAv5.leaf | 3e1431b68060866c... | 45,713 | 17.5698573 | bee77692c00cec37... | 14:17:a:p, 9:12:b:m, 7:9:b:m, 12:15:a:p |
| pH11W37A155wuk2k5k3r.n0.JPAv5.leaf | 71afb68f7bc70da5... | 46,814 | 17.6738451 | 82f005631c67cd63... | 14:17:a:p, 12:9:a:m, 9:7:a:p, 12:15:a:p |
| pH11W37A155wuk2k5.n0.1.JPAv5.leaf | 99cf0c177bf617fa... | 46,814 | 17.8795695 | a9eafddceb777763... | 14:17:a:p, 12:9:a:m, 9:7:a:p, 15:12:a:m |
| pH11W37A551wuk2.n0.2.JPAv5.leaf | 3e1eeee146dc5faf... | 47,915 | 21.0788002 | 6c958edc4ec297a9... | 14:17:a:p, 12:9:a:m, 15:12:a:m |
| pH11W37A151wuk7k2.n0.1.JPAv5.leaf | 14046bb7c7852c1c... | 47,548 | 21.6047949 | 27831c84b8a6d546... | 17:14:b:m, 12:9:a:m, 15:12:a:m |
| pH11W37A150wuk7k1k2.n0.1.JPAv5.leaf | 2b7e9d8014312aad... | 46,080 | 23.8906373 | c8bfa44839e73457... | 17:14:b:m, 9:12:b:m, 9:7:a:p, 15:12:a:m |
| pH11W37A010w.n0.0.0.0.3.JPAv5.leaf | 999ca98d02a7bd32... | 44,614 | 26.0711104 | f6f83428f6a5652f... | 14:17:a:p, 7:9:b:m, 12:15:a:p |
| pH11W37A551wuk1.n0.2.JPAv5.leaf | 38dbe16bf6ecf3c0... | 47,915 | 27.6544827 | 4dd85df3e4cfab5b... | 14:17:a:p, 9:12:b:m, 15:12:a:m |
| pH11W37A005wu.n0.0.JPAv5.leaf | 6ac608cb88aface6... | 47,917 | 29.2017307 | 3905e3427c190bcd... | 14:17:a:p |
| pH11W37A555wuk5k2.n0.JPAv5.leaf | ac1a7b58f24d647b... | 47,915 | 34.7026425 | dbf5f6d5d74a7340... | 14:17:a:p, 12:9:a:m, 12:15:a:p |
| pH11W37A555wuk8k2k3.n0.JPAv5.leaf | aa9706095b8d3f2f... | 47,915 | 35.8536388 | b8d6c24f1114adea... | 17:14:a:m, 12:9:a:m, 15:12:a:m |
| pH11W37A110wk5k4.n0.JPAv5.leaf | ae6d7cd7494e62dd... | 46,447 | 40.2662444 | 0410c2d5d5c99e62... | 17:14:b:m, 7:9:b:m, 12:15:a:p |
| pH11W37A555wuk5k3.n0.JPAv5.leaf | 0d5498c8a4116640... | 47,915 | 41.3994154 | 14236185dbc482af... | 14:17:a:p, 12:9:a:m, 15:12:a:m |
| pH11W37A150wuk7k2k3.n0.1.JPAv5.leaf | 1e41c2645df4bd6b... | 46,080 | 43.2710195 | 2cea890708b14b0a... | 17:14:b:m, 12:9:a:m, 9:7:a:p, 15:12:a:m |
| pH11W37A150wuk7k3k1.n0.2.JPAv5.leaf | 41cd2e61cc37f68e... | 46,080 | 44.5888234 | cdf2d321650d2336... | 17:14:b:m, 12:9:b:p, 7:9:b:m, 12:15:a:p |
| pH11W37A555wuk2.n0.JPAv5.leaf | 84926cb8f296b5b1... | 47,915 | 44.9552107 | f7da03187c3cf76a... | 14:17:a:p, 9:12:b:m, 12:15:a:p |
| pH11W37A551wuk2.n0.1.JPAv5.leaf | b3dbe6a0afd943ac... | 47,915 | 45.2107626 | e76350cd2d79c0dd... | 14:17:a:p, 12:9:a:m, 12:15:a:p |
| pH11W37A155wuk1k2k4.n0.JPAv5.leaf | 5fe15ecdb7df6287... | 46,814 | 45.3921886 | 988e684338929e7a... | 14:17:a:p, 9:12:b:m, 9:7:a:p, 12:15:a:p |
| pH11W37A155wuk1k2.n0.1.JPAv5.leaf | 5aa602aa564b96c9... | 46,814 | 46.8231744 | 4fd09631a78e4c82... | 14:17:a:p, 9:12:b:m, 9:7:a:p, 15:12:a:m |
| prH11W37A550wuk5k1k1dr.n0.JPAv5.leaf | 489c86bd75e86bca... | 46,447 | 49.9065313 | 300c1ffa49b28115... | 17:14:a:m, 9:12:b:m, 7:9:b:m, 12:15:a:p |
| pH11W37A110wk5.n0.0.0.1.JPAv5.leaf | e21043d19dec617f... | 46,447 | 50.6291155 | 656b468b58ef003d... | 17:14:b:m, 7:9:b:m, 12:15:b:p |
| pH11W37A010wk4k4.n0.JPAv5.leaf | 0136b6e79e60e67f... | 45,348 | 54.7930863 | ec92eb305488ebd8... | 14:17:a:p, 9:7:a:p, 12:15:a:p |
| pH11W37A150wuk7k3k1.n0.1.JPAv5.leaf | 032e7a663f04a1c9... | 46,080 | 60.8914389 | 66efff9e24e5f117... | 17:14:b:m, 12:9:b:p, 7:9:b:m, 15:12:a:m |
| pH11W37A151wuk7k1k2.n0.JPAv5.leaf | a4a2df732b4e380f... | 47,548 | 62.0021946 | e0d27fe72d78d4b2... | 17:14:b:m, 9:12:b:m, 15:12:a:m |
| pH11W37A155wuk2k3.n0.JPAv5.leaf | 89c9f04e0c6cfb7b... | 46,814 | 62.4573826 | 4cb8117a9f3f2924... | 14:17:a:p, 12:9:a:m, 7:9:b:m, 15:12:a:m |
| pH11W37A110w.n0.0.0.0.3.JPAv5.leaf | eee49c60f5ce64da... | 46,447 | 62.6071776 | f4e1022303660272... | 14:17:a:p, 7:9:b:m, 12:15:a:p |
| pH11W37A155wuk1k1.n0.1.JPAv5.leaf | bc91516997422009... | 45,713 | 64.9618025 | 0c3a4d2c8c38ba84... | 14:17:a:p, 9:12:b:m, 7:9:b:m, 15:12:a:m |
| pH11W37A555wuk8k1k3.n0.JPAv5.leaf | c5a296c1d244f3dd... | 47,915 | 67.5003524 | 37df361f276715d4... | 17:14:a:m, 9:12:b:m, 15:12:a:m |
| pH11W37A551wuk1.n0.1.JPAv5.leaf | 5d0ec8cf232aa683... | 47,915 | 67.6991247 | 4f3783a415fcd9da... | 14:17:a:p, 9:12:b:m, 12:15:a:p |
| pH11W37A555wuk8k2.n0.1.JPAv5.leaf | e83981e56d255a56... | 47,915 | 69.7955382 | cea3338d0d4cdc6a... | 17:14:a:m, 12:9:a:m, 12:15:a:p |
| pH11W37A551wuk5k3.n0.JPAv5.leaf | 0ab1198b9a59b46f... | 47,915 | 70.3181136 | 6b6d1baa7579f640... | 17:14:a:m, 9:12:b:m, 15:12:a:m |
| pH11W37A155wuk2k2.n0.JPAv5.leaf | be4548c7caae9d8d... | 46,814 | 71.0355982 | fb4c97eab92f0948... | 14:17:a:p, 12:9:a:m, 7:9:b:m, 12:15:a:p |
| pH11W37A150wuk7k2k3.n0.3.JPAv5.leaf | fee11e45a6d6a034... | 46,080 | 75.9444556 | 3fa28a784679c2d7... | 17:14:b:m, 12:9:a:m, 9:7:a:p, 12:15:a:p |
| pH11W37A555wuk3.n0.JPAv5.leaf | 64d76b0601fcac42... | 47,915 | 87.4919474 | 09e95be297f0e8c6... | 14:17:a:p, 9:12:b:m, 15:12:a:m |
| pH11W37A151wuk3.n0.1.JPAv5.leaf | 9410a79c85cf7ed6... | 47,548 | 94.1198162 | 5ae47384b5ff4496... | 14:17:a:p, 12:9:a:m, 15:12:a:m |
| pH11W37A110wk2.n0.1.JPAv5.leaf | 8204f0a22f02c5fc... | 47,181 | 103.5205298 | 6ae7580f2c90b69e... | 14:17:a:p, 9:7:a:p, 12:15:b:p |
| pH11W37A010w.n0.0.0.0.1.JPAv5.leaf | 50d1420249616175... | 44,614 | 104.7676334 | 7fd6eb7ca45d2b9f... | 14:17:a:p, 7:9:b:m, 12:15:b:p |
| pH11W37A015wu.n0.1.JPAv5.leaf | dbdd8d1d04479802... | 47,917 | 115.1056128 | 810ab93214488b8d... | 17:14:a:m |
| pH11W37A551wuk5k5.n0.1.JPAv5.leaf | eea939a01eddb984... | 47,915 | 124.2054069 | d2a9c7b939eec64c... | 17:14:a:m, 12:9:a:m, 12:15:a:p |
| pH11W37A001wu.n0.0.JPAv5.leaf | 51bccae0777a851b... | 47,917 | 124.5125440 | bd30141bd27d01cb... | 14:17:a:p |
| pH11W37A055wu.n0.1.JPAv5.leaf | 7ddcf077a6a9f1f7... | 47,917 | 153.0724428 | 77f1cef2ef975644... | 17:14:a:m |
| pH11W37A005wu.n0.1.JPAv5.leaf | b278834875894fb0... | 47,917 | 180.6354565 | 151a85a0ab171273... | 17:14:a:m |
| pH11W37A555wuk8k1k2.n0.JPAv5.leaf | 751aa08bc1e88114... | 47,915 | 210.6443899 | 11cab554fa8b55af... | 17:14:a:m, 9:12:b:m, 12:15:a:p |
| pH11W37A110wk2.n0.2.JPAv5.leaf | 183d4d5c31b46aed... | 47,181 | 231.8137242 | 5622b88653ea8c05... | 14:17:a:p, 9:7:a:p, 12:15:a:p |
| pH11W37A151wuk3.n0.2.JPAv5.leaf | cfe763d093b530e7... | 47,548 | 251.1879988 | 9c9e3a87106c1d16... | 14:17:a:p, 12:9:a:m, 12:15:a:p |
| pH11W37A001wu.n0.1.JPAv5.leaf | b840b39c85db1666... | 47,917 | 282.2398955 | cd91efa2b0f57e5f... | 17:14:a:m |
| pH11W37A051wu.n0.1.JPAv5.leaf | 012d2a9a9bd57fbb... | 47,917 | 301.0136363 | 9c1c8082ae5f786b... | 17:14:a:m |
| pH11W37A011wu.n0.1.JPAv5.leaf | 745d4e274cbc3eb9... | 47,917 | 318.3650560 | 93fd40f081f45a60... | 17:14:a:m |
| pH11W37A110w.n0.0.0.0.2.JPAv5.leaf | 3e0650639bdda993... | 46,447 | 346.3087659 | 5c39bf4d37312448... | 14:17:a:p, 7:9:b:m, 15:12:a:p |
| pH11W37A010wk4k2.n0.JPAv5.leaf | d560c45be3230b0c... | 45,348 | 433.2800505 | 954845b3d7a25078... | 14:17:a:p, 9:7:a:p, 12:15:b:p |
| pH11W37A010w.n0.0.0.0.2.JPAv5.leaf | 14fc818e7d909c9f... | 44,614 | 715.5460749 | 48058092cce6d2df... | 14:17:a:p, 7:9:b:m, 15:12:a:p |
| pH11W37A110wk5k3.n0.JPAv5.leaf | 74d98a13c2ed138c... | 46,447 | 1425.1546851 | d0a7e76ae0e322bd... | 17:14:b:m, 7:9:b:m, 15:12:a:p |
| pH11W37A000wu.n0.2.JPAv5.leaf | e34edad9040e6364... | 47,183 | 7706.7243561 | d1cf38918d4d753f... | 17:14:b:m |
| pH11W37A001wu.n0.2.JPAv5.leaf | 696892fedcc8d6b2... | 47,917 | 14290.0829198 | d48645a3b65418b8... | 17:14:b:m |
| pH11W37A005wu.n0.2.JPAv5.leaf | 68d320cf4c4aa7e3... | 47,917 | 16060.1136714 | 367042ba9ff203f6... | 17:14:b:m |
| pH11W37A010wk7.n0.JPAv5.leaf | 8d5746c5231b08be... | 47,183 | 25378.9459938 | 045680be36146a9e... | 17:14:b:m |
| pH11W37A055wu.n0.2.JPAv5.leaf | 3a98c26a5c13bad3... | 47,917 | 26600.4236416 | 9e557d03cf6f7887... | 17:14:b:m |
| pH11W37A011wu.n0.2.JPAv5.leaf | 38471fe50c8ed7ee... | 47,917 | 40611.9479697 | 7bee19d3baafd106... | 17:14:b:m |
| pH11W37A050wk5.n0.JPAv5.leaf | c4dc931d3b9737fb... | 47,183 | 55434.6490616 | c707253b07f18d1c... | 17:14:b:m |
| pH11W37A051wu.n0.2.JPAv5.leaf | 07c6e0b3c840a6f5... | 47,917 | 75681.3472727 | 6d09a8b9da973fa2... | 17:14:b:m |
| pH11W37A111wu.n0.3.JPAv5.leaf | 62483d7950f13a4d... | 49,750 | 76798.5319901 | 476bcfdcdd2ad80a... | 14:17:b:m |
| pH11W37A155wuk5.n0.JPAv5.leaf | 048aa2f27f6cd385... | 49,750 | 121372.1463471 | 62cbf464bc288f65... | 17:14:a:m |
| prH11W37A015wua.n0.JPAv5.leaf | cf92905bd70e74bc... | 47,917 | 131267.8708155 | 0945111d37af3439... | 17:14:b:m |
| pH11W37A155wuk7.n0.JPAv5.leaf | 29addf70c1cd6151... | 49,750 | 214094.1062876 | 77f2ec6257ef0ae1... | 14:17:b:m |
| pH11W37A101wu.n0.3.JPAv5.leaf | 6004846130c9e021... | 49,750 | 215745.5209498 | 6f308c1d2703fb6d... | 14:17:b:m |
| pH11W37A151wuk8.n0.JPAv5.leaf | da034edfd988c629... | 49,750 | 219054.1992804 | ea6d373bbd9dfc68... | 14:17:b:m |
| pH11W37A050wk1k3k2r.n0.JPAv5.leaf | 381d4216db0ee2f9... | 44,247 | 266057.4601158 | 776de98615093bee... | 14:17:a:p, 12:9:a:m, 9:7:a:p, 9:11:a:m |
| pH11W37A105wu.n0.3.JPAv5.leaf | 4cd4ecb6ae4a0df2... | 49,750 | 308575.4762154 | 3c310fa5aa038a5e... | 14:17:b:m |
| pH11W37A111wu.n0.1.JPAv5.leaf | 4c7119d9314062d2... | 49,750 | 337337.8129078 | 42adb1ea87ec08ab... | 17:14:a:m |
| pH11W37A150wuk6.n0.JPAv5.leaf | c9a183e4160d4f02... | 49,016 | 418857.9579881 | f1b4d364d4805d36... | 17:14:a:m |
| pH11W37A550wuk2k3.n0.2.JPAv5.leaf | 09fc5bdf672ee53d... | 46,447 | 420443.5157031 | b60afcbf8d4b839d... | 14:17:a:p, 12:9:a:m, 9:7:a:p, 9:11:a:m |
| pH11W37A150wuk3k3.n0.2.JPAv5.leaf | ac71314ea4c7e8eb... | 46,080 | 540629.8047412 | c9f751db02c00a3c... | 14:17:a:p, 12:9:a:m, 9:7:a:p, 9:11:a:m |
| pH11W37A550wuk5k1k2k3r.n0.JPAv5.leaf | aa1f3e100a68dd96... | 46,447 | 551965.6680624 | 80947d548a941f8b... | 17:14:a:m, 9:12:b:m, 9:7:a:p, 11:9:a:m |
| pH11W37A505wu.n0.2.JPAv5.leaf | 17e1b1709fdd2f92... | 50,117 | 606313.8069614 | 1af1a58961d85f79... | 14:17:b:m |
| pH11W37A151wuk6.n0.JPAv5.leaf | 0a56ab34192d0499... | 49,750 | 649175.4716594 | ff8917e9346fcdd3... | 17:14:a:m |
| pH11W37A115wu.n0.1.JPAv5.leaf | aceabac898d7b667... | 49,750 | 693824.0674530 | ace3e5bf46953135... | 17:14:a:m |
| pH11W37A110wk4.n0.JPAv5.leaf | 5031adfa31b8204c... | 49,016 | 745627.9972961 | b7ba48a7bb68d47b... | 17:14:a:m |
| pH11W37A105wu.n0.1.JPAv5.leaf | 32b2798a3f30c836... | 49,750 | 789167.7379676 | 66b812a8c320b2f7... | 17:14:a:m |
| pH11W37A101wu.n0.1.JPAv5.leaf | 5262fcb99e18453f... | 49,750 | 846745.8321744 | 97c39b7b1bed2d67... | 17:14:a:m |
| pH11W37A100wu.n0.1.JPAv5.leaf | f78b4eb13b4863f8... | 49,016 | 846783.8891911 | 51ec5c12cd3d417c... | 17:14:a:m |
| pH11W37A550wuk5k1k2k2r.n0.JPAv5.leaf | 3787f3e08243507f... | 46,447 | 858563.5096899 | 207115080853a084... | 17:14:a:m, 9:12:b:m, 9:7:a:p, 9:11:a:m |
| pH11W37A550wuk5k2k3rk2.n0.JPAv5.leaf | cc63d726e8065977... | 46,447 | 881170.0575260 | cd28dcb78b23b5ca... | 17:14:a:m, 12:9:a:m, 9:7:a:p, 9:11:a:m |
| pH11W37A150wuk3k3.n0.3.JPAv5.leaf | cef65ffdf1d8a875... | 46,080 | 946086.8530170 | 9ae9fc631a6c7dff... | 14:17:a:p, 12:9:a:m, 9:7:a:p, 11:9:a:m |
| pH11W37A100wu.n0.3.JPAv5.leaf | 522d35222e14fd74... | 49,016 | 992160.7291431 | ca87473af0ceb13d... | 14:17:b:m |
| pH11W37A115wu.n0.3.JPAv5.leaf | 79eadb0d3ab627cd... | 49,750 | 1035354.5082357 | 8da5321ace779d85... | 14:17:b:m |
| pH11W37A110wk6.n0.JPAv5.leaf | 5402bb607b8139da... | 49,016 | 1088056.5360919 | 86f5da57f45e4730... | 14:17:b:m |
| pH11W37A511wu.n0.2.JPAv5.leaf | 24e14b8e14f972bd... | 50,117 | 1134451.0725268 | 78a6e9bd4e3bd9f1... | 14:17:b:m |
| pH11W37A501wu.n0.2.JPAv5.leaf | 8f17e45b0459c00a... | 50,117 | 1333701.4843174 | f7c64f495d5e529a... | 14:17:b:m |
| pH11W37A050w.n0.0.0.1.2.JPAv5.leaf | 99482cc6f39ed07e... | 44,614 | 1350536.9202002 | 0fc5cfa12466b2fe... | 14:17:a:p, 9:12:b:m, 9:11:a:m |
| pH11W37A150wuk8.n0.JPAv5.leaf | a2a1c21ef3231e1c... | 49,016 | 1540048.4031655 | 79925f8d3a1a998b... | 14:17:b:m |
| pH11W37A550wuk6.n0.JPAv5.leaf | b4575a8fd6dedfcc... | 49,383 | 1576461.9729014 | 134c1356ec5217c4... | 14:17:b:m |
| pH11W37A550wuk2.n0.0.1.2.JPAv5.leaf | b2d2d84092614a6a... | 46,080 | 1630177.1451479 | 6e377394a148143a... | 14:17:a:p, 12:9:a:m, 7:9:b:m, 9:11:a:m |
| pH11W37A500wu.n0.2.JPAv5.leaf | c3b25add93f74ed6... | 49,383 | 1757323.7629806 | 84371325439c25d7... | 14:17:b:m |
| pH11W37A150wuk7k2.n0.0.1.2.JPAv5.leaf | a0196ad37e3a9c0d... | 45,713 | 1946497.3780743 | 4e356c1c5326a2e8... | 17:14:b:m, 12:9:a:m, 7:9:b:m, 9:11:a:m |
| pH11W37A510wuk5.n0.JPAv5.leaf | 71e416f21b7c7282... | 49,383 | 2294445.6992149 | 28b64616e3638915... | 14:17:b:m |
| pH11W37A515wu.n0.2.JPAv5.leaf | abdbe8fdffbdd6db... | 50,117 | 2558928.2675520 | ac168fd87c33d913... | 14:17:b:m |
| pH11W37A551wuk6.n0.JPAv5.leaf | 6e01131cf3257e86... | 50,117 | 2628034.8554377 | 9156453d18cec05b... | 14:17:b:m |
| pH11W37A050wk1.n0.0.1.2.JPAv5.leaf | e009c533376cc4cf... | 43,880 | 3141054.4479646 | 2a910cc543336fa4... | 14:17:a:p, 12:9:a:m, 7:9:b:m, 9:11:a:m |
| pH11W37A550wuk2k3.n0.3.JPAv5.leaf | 5bcdc123256d6486... | 46,447 | 3361515.7338790 | 911f186424cfcc21... | 14:17:a:p, 12:9:a:m, 9:7:a:p, 11:9:a:m |
| pH11W37A550wuk1.n0.2.JPAv5.leaf | a3a517dcc2fc0035... | 46,814 | 4613193.4674176 | 405ea76a3d074be0... | 14:17:a:p, 9:12:b:m, 9:11:a:m |
| pH11W37A150wu.n0.0.0.1.2.JPAv5.leaf | 61a6f47350b25a2a... | 46,447 | 4665604.8708650 | 122ff7c93ab2d820... | 14:17:a:p, 9:12:b:m, 9:11:a:m |
| prH11W37A150wuk7k1k1a.n0.JPAv5.leaf | a7d3ac16e36564e0... | 45,713 | 4720504.5896363 | 1007c849dd76888f... | 17:14:b:m, 9:12:b:m, 7:9:b:m, 9:11:a:m |
| pH11W37A150wuk3k2.n0.2.JPAv5.leaf | 67b6c38343fca1af... | 45,713 | 7333179.4016155 | b5786ac67ee538d1... | 14:17:a:p, 12:9:a:m, 7:9:b:m, 9:11:a:m |

## What the statement is used for, and what it does not contain

- It is the local side's statement for the branch "kind A" of case T, "the label-9 square stands off the wall
  column (class-frame x > 53/100) with its nearest side direction above its gate" (`JOIN_ROOTS.md` sections 1, 3
  and 9.3), **whichever statement of label 11 certifies**: the v5 region contains the old target PB_11 and the new
  target HULLW_11 (`JOIN_ROOTS.md` top table and section 11.1, `ADMISSION_v4.md` section 9; `cmp_v5.py`). It serves
  the branch if the capture side certifies, for each of the twelve rigid labels j, a statement with the target of
  this region (PT_j, PM_j or the split statement PS_j^9; for label 11 also PTW37_L11 or PSW37_L11 with k = 9; for
  label 16 also the form "PS_16^9 ENDa", which the capture side joined to this root on 2026-10-10: its join review
  of 17:32 found the target inside this root with least margin 1.9e-7, as stated by the audit lead,
  not checked here),
  together with the statements for the loose labels; label 9's own factor is T9's slot off the wall column and
  rests on nothing beyond the class file (table of section 9.3). The composition is `JOIN_ROOTS.md` sections 3 and
  9.3; it is not repeated or proved here.
- The two seams of label 9. Position, x = 53/100: a square ON that line lies in the wall column, the statements
  PT_j and PM_j say nothing about it and the wall cases take it (`JOIN_ROOTS.md` section 9.3, item (c)); the region
  takes the end closed (xi_(9,1) from -87219/500000, the grid point below), a superset. Direction, the gate's upper
  end: the slots of a class file are closed sets (`cloud/analysis/CLASS_FORMAT.md`), so a direction exactly at the
  end of T9's interval is in T9 and THIS branch takes it; the region's arc starts 1.4e-9 rad below that end.
- With Codex's amendment A (class statement KEY_W; my review `reviews/join_roots/keyw_amendment/REVIEW_KEYW_AMENDMENT.md`)
  this is the only region for "label 9 off the wall column with its direction outside its gate": the region JPB
  (below the gate) is not needed. Under KEY_W the branch needs label 9's direction only up to +0.15 rad: the
  clause of the capture side's text reads "x9 > 53/100 and 591183/1408817 <= t9 <= 44941/100000" (t9 = tan-half of
  label 9's absolute direction; as stated by the audit lead). That interval is [+0.0999006241,
  +0.1499987538] rad from label 9's reference direction; the root file's arc is [+0.0999006227, +0.7862284215] rad
  and contains it (exact comparison of the tan-half values: 1.4e-9 rad of room below, 0.636 rad above). So the root
  covers MORE directions than the clause uses.
- The v5 region contains the regions JPA v1 and JPA v2 (one region; equal to v5 outside label 11, `cmp_v5.py` part
  A), on which no tree was accepted: this statement implies the statement for them.
- The tree cuts the directions of labels 3, 15 and 17 at tan-half -659/5000 and 659/5000 only and the direction of
  label 9 at tan-half 563/2500 only (each from its label's reference direction; not every cell is cut at every
  value), and closes every piece; labels 4 and 11 are not cut anywhere (label 11 has the root's box and arc in all
  416 nodes).
- NOT contained: that the capture side puts a packing of this branch into the region. That needs the class
  statements named above. Their state is the capture side's bookkeeping and is not checked here; quoted from
  Codex's manifest
  `research/finishing-threshold-goal-20261007/window-capture/second-order-20261010/theorem/THEOREM_MANIFEST.json`
  (as of 2026-10-10 18:34:55, sha256 5e51cbea3a65ffa022bd59c34aec99454e0f2cc80be697c7888c70adadb111ba, the state
  the reviewer of this record read; in the snapshot of 18:12:21, d76878ade4f4f58c..., FRAME_MARKER was still RECEIPT
  OPEN): the twelve branch clauses of this root, BRANCH_JPA_L01 to BRANCH_JPA_L16 (labels 1, 2, 5, 6, 7, 8, 10, 11,
  12, 13, 14, 16), and the base rows L_3, L_4, L_15, L_17, KEY_W and FRAME_MARKER have the status COUNTED; the root
  obligation of JPA itself is RECEIPT OPEN there (it waits for this record).
- Also NOT contained: the correctness of the region file against the class files (the v5 files are checked by 2,552
  exact self-checks and against Codex's drafts, `ADMISSION_v4.md`; the v5 generator and `cmp_v5.py` are not
  reviewed by a reviewer).

## Review

Reviewed 2026-10-10 by a reviewer that wrote none of the record, of the certificate or of the tools:
`reviews/join_roots/batch7/REVIEW_EJPA_v5.md` (sha256
623d8b32ac8719250616ed0f9927fd071e3ac8f3835751ff2bf70859aeeb122b); the text it read is kept as
`reviews/join_roots/batch7/as_reviewed/RECORD_EJPA_v5.md` (sha256 a147f8f8bb07f57f...); its run and outputs are in
`reviews/join_roots/batch7/` (`t_tree.py` and `rjlib.py`, the bytes of batches 4 to 6; `t_JPA_v5.out`,
`t_JPA_v5_nodes.json`, `hand_checks.out`). **Verdict: "PROVED as it stands". No correction is required: every
number and claim it could test is right, and nothing overstates.**
Its run of the earlier reviewers' program (unchanged; the certificate read line by line; 1100 s, 543 MB): 126
checks, 125 ok. It carries: the certificate's size and both hashes; the header against the statement file and the
reference file; the root node against the region file (side interval, 68 box ends, 51 rotations); the shape (416
nodes, depth 11, 42 arc and 93 option splits, 281 leaves, none terminal) and the nine cut sentences; the child
test of SPEC 3.0 section 6 for all 415 children; the exclusion of every omitted option in each of the 93 option
splits; every leaf closed as infeasible with one round and a `0` step in both reports; the node digests, kinds and
L against both acceptance reports and both of the producer's reports; all 281 rows of the table; the hashes and
numbers of the Evidence table; the log; the 278 nodes beyond the root (683 arcs, the facts output's list), all
leaves, by at most 5.870e-06 rad; label 11 never cut.
The one FAIL is the program's test "every hash string of the record is the hash of a file named above or stands in
the leaf table": the string left over is the digest d76878ade4f4f58c... of Codex's manifest, a file the program
does not know; the reviewer hashed the live manifest at 18:32 and found exactly this digest. Its judgement:
harmless, no defect of the record.
By hand, 54 exact checks (three more FAIL lines of its first script are faults of that script, redone and ok):
the corollary against `SPEC_v3.0_NOTES.md` and the statement file; "the region in words" number by number (label
9's arc ends at tan-half 567946313691858184003/11360767759702735510000 and 4147/10000 from its reference, that is
+0.0999006227 and +0.7862284215 rad; the end x = 53/100 by the file's frame rule, the box end below it by less than
1e-6; labels 3, 17, 15, 4 more than a quarter turn; label 11's box and arc); v5 against `JPA_exact_v1.json` and
`JPA_exact_v2.json` (one region; v5 equal to it outside label 11 and containing it in label 11); the two seams
against `JOIN_ROOTS.md` section 9.3 and `CLASS_FORMAT.md`; amendment A; the quoted states of Codex's manifest; the
acceptance run's work file by its sha256.
**The arc of label 9 covered by the root file itself:** as tan-half of the
absolute direction [0.419630795796869..., 0.913966453374868...], that is [+0.0999006227, +0.7862284215] rad from
label 9's reference direction (absolute 0.7946282155 to 1.4809560144 rad, no wrap). The clause 591183/1408817 <=
t9 <= 44941/100000 lies inside it, both comparisons exact: room below 8.2185e-10 in tan-half (1.3976e-9 rad, the
file's own excess beyond the required arc), room above 0.464556 in tan-half (0.636229668 rad). The root ends at
tan-half 0.913966, not at 1: a clause "t9 < 1" would NOT lie inside this root; the retained clause does.
ALL 281 leaves against the root, with its own code on the certificate's node data and the producer's description:
all 416 nodes have the side interval [Sref, Sref]; each leaf node contains its cell (17 arcs, 68 box ends, S) and
assumes exactly the options of its path, in path order; the 135 split nodes are exactly their cells; beyond the
root 278 nodes, all leaves, none in a box interval; label 9: 25 leaves below the root arc by 5.870e-06 rad each,
37 above by 5.260e-06 rad each; labels 3, 15, 17 by at most 5.361e-06 rad; label 4's arc and label 11's box and
arc are the root's in all 416 nodes.
It did not rerun the two frozen checkers or the acceptance script (each of the two frozen checkers
has run on these bytes twice: in the producer's run with `--keep-going` and in my acceptance run with the default
options).

What changed against the text the reviewer read, all in this version (19:00), none of it asked as a correction:
- Note 1: "the region in words" now says that the end of xi_(9,1) is class-frame x = 53/100 ROUNDED DOWN to the
  grid (a superset), as the second point on use says.
- Note 2: the manifest quote is brought to the state of 18:34:55 that the reviewer read (FRAME_MARKER went from
  RECEIPT OPEN to COUNTED 22 minutes after the snapshot I had quoted; nothing else that is quoted changed). A quote
  of the manifest is right for the digest it names only.
- The status paragraph with the limits sentence; this section.
Remark of the reviewer for the proof as a whole, no change here: label 9's directions BELOW its gate are in no
proved region (JPB has no tree); they are excluded by the capture side's KEY_W alone (amendment A).
