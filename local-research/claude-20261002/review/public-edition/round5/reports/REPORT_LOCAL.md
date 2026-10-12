Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line.

HOLDS WITH CONDITIONS (C1: the four certificates above 300 MB, JG, JPA_v5, JPWS_v4, JPW13, were not rehashed by me; C2: the checker parts I did not read rest on the earlier reader; C3: the leaf arithmetic of record was not replayed by me except most of JPG15p_v5; C4: I did not read the records in full, the batch reviews or h_report30.py's source). No gap and no wrong statement found in what I read or ran.

FINDINGS, most serious first

F1. The acceptance runs of JPWS_v4 and JPA_v5 were made on working copies, not on the paths the packet pins. ACCEPT_JPWS_v4.log line 1 names `<producer work folder>/assembly_slab5/work/JPWS_v4/JPWS_v4.cert.jsonl.gz`; ACCEPT_JPA_v5.log names `<producer work folder>/assembly/work/JPA_v5/JPA_v5.cert.jsonl.gz`. The packet pins `local-research/claude-20261002/results/assembly/<ROOT>/...` with the same sha256 (538a6a51..., b9f92839...). Identity therefore rests on the hash alone, and these are two of the four files I did not rehash. PACKET's own list `large_existing_pins_not_rehashed` contains all ten assembly certificates. My leafprov.py did read both pinned-path files to the end (gzip decoded without error; 110 nodes / 70 leaves and 416 / 281, as in the logs); that is not a hash. JUDGEMENT: one sequential `shasum -a 256` of the four large files closes this.

F2. My Node-checker coverage is by reading only. I ran no corruption control with wxcheck2_v30.js. For the points of part 1 its source matches the SPEC line by line (below).

F3. EXPECT_JG_v2.json has `terminal_leaves: null`, so the acceptance report does not pin the number of terminal leaves of JG (the log lists one, 'td0f7ae2afe'). JUDGEMENT: harmless for a tube statement, since any number of terminal leaves proves the same thing.

F4. No defect found in SPEC 4.6, 4.8, the class forms or the centred rule, nor in either checker's implementation of them.

(1) TABLE

id | status | relied on
LOCAL_CHECKER_SOUNDNESS | CONDITION | 4.6, 4.8, class forms, centred rule, 4.7 exclusion, split and child-containment tests: re-derived by hand (JUDGEMENT), tested exactly (facts_test.py), read in both checkers. Sections 5 (store update), 7, 8, 10 code and all parsing/validation: NOT READ (earlier reader).
LOCAL_CERTIFICATE_IMPORT | CONDITION | 99 pinned files of the LOCAL rows rehashed, 0 mismatches; eleven logs; record, root and certificate hashes concordant; side transfer restated. Conditions C1, C4.
LOCAL_JQ | CONDITION | ACCEPT_JQ_v1_jQTwn0.log: 1 node, 1 infeasible, 0 terminal; cert 0b2a8ff8 rehashed; root f4d1607e. Arithmetic not replayed.
LOCAL_JG | CONDITION | ACCEPT_JG_v2.log: 113 nodes, 56 infeasible, 1 terminal, 56 split. Tube of EXPECT_JG_v2 equals the window of EXPECT_G20S (core, boxes, radius 1/10) on the sixteen labels; label 4 keeps its root box and radius 1. Cert e7587199 NOT rehashed; tree not streamed by me.
LOCAL_JPA | CONDITION | log 416/281/0/135; leafprov.py 415 child links, 0 containment failures; cert b9f92839 NOT rehashed (F1).
LOCAL_JPWS | CONDITION | log 110/70/0/40; leafprov.py 109 links, 0 failures; cert 538a6a51 NOT rehashed (F1).
LOCAL_JPW13 | CONDITION | log 255/163/0/92; cert 7147d778 NOT rehashed; tree not streamed by me.
LOCAL_JPG3m | CONDITION | log 36/22/0/14; cert 75357350 rehashed; leafprov.py 35 links, 0 failures.
LOCAL_JPG3p | CONDITION | log 36/22/0/14; cert 804ae794 rehashed; 35 links, 0 failures.
LOCAL_JPG17m | CONDITION | log 31/18/0/13; cert 68613d84 rehashed; 30 links, 0 failures.
LOCAL_JPG17p | CONDITION | log 48/32/0/16; cert f392b6ba rehashed; 47 links, 0 failures.
LOCAL_JPG15m | CONDITION | log 61/39/0/22; cert ed66c59b rehashed; 60 links, 0 failures.
LOCAL_JPG15p | CONDITION | log 23/15/0/8; cert 1adb3864 rehashed; 22 links, 0 failures; my own frozen-Python run on the K1 copy accepted 14 of its 15 leaves and 7 of 8 splits (the eighth is the one I corrupted).
For all eleven rows "CONDITION" means: holds given LOCAL_CHECKER_SOUNDNESS and that the saved complete runs are what the logs say. I found nothing against either.

PART 1. Parallel-class facts, wall-support facts, class forms, centred rule

Mathematics (JUDGEMENT throughout, backed by the exact tests in (3)):
- 4.6 options. O_i = (i,j,axis_i,eps_i) holds iff al >= (1+|co|+|si|)/2; O_j = (j,i,axis_j,-eps_j) holds iff be >= the same. Checked against the direct four-corner test in 59,880 exact cases. The sign "-eps_j" is essential: with +eps_j, 709 of 709 control cases violate the P+ facts.
- Identity (be - al)(1+co) = si*Y: re-derived from n_j = co n_i + si J n_i, J n_j = co J n_i - si n_i; exact in all cases.
- Lemma P (P+, P-, Pk): the eight cases of the SPEC proof are correct. It needs only co > -1; the checker demands cL > 0, which is stronger.
- Kind Ps: the counter-clockwise arc from E^- to E^+ has length angle(R^+) - angle(R^-) in [0, pi). With cos E^± > 0 and sin E^- <= 0 <= sin E^+ it is the arc through 0 inside (-pi/2, pi/2). g(s) = sqrt(1-s^2)+s-1 is concave with g(0)=0, which gives co+|si|-1 >= k|si|. The "else 1" case is safe because cp, cm >= 0 are required.
- 4.8: (F1) for a wall is D_W >= (|cos t|+|sin t|)/2; with the arc containing the x-direction the same secant bound applies; "else 0" gives D_W >= 1/2, which is true.
- Class forms: all five dictionary entries re-derived (al, be, co, si, Y, including both axis cases of J n . d).
- Centred rule: Rem(c+y) is the same polynomial function; each y_v lies in [SBlo - c_v, SBhi - c_v]; the monomial-wise interval bound is a lower bound. Indicator variables keep c = 0 and [0,1].

Implementation, Python (wxcheck_v30.py):
- class_combo 1282-1310; par_poly 1386-1411; class_frame 1414-1420; wsup_poly 1423-1444; wsup_coefficients 1505-1518; ps_slopes 1521-1539.
- par_failure 1760-1797: six other options excluded, cL > 0 strict, YU <= 1+cL, YL >= 0 or the sign assumption with the same (i,j,K), 0 <= kappa <= 1 - Ybar/(1+cL); for Ps additionally both effective ends, sign conditions, cp >= 0, cm >= 0.
- asg at 1982-1986 requires the exact assumption (i,j,K,sign); wsup at 1975-1981 rejects when the sign conditions fail.
- Centred rule: centred_remainder 2149-2182, centred_interval 2184-2199, lower_bound_centred 2201-2228; `centre` accepts base variables only (parse_centre 887-898).
- Each test is exactly the SPEC's, none weaker.

Implementation, Node (wxcheck2_v30.js), read in source:
- classBar 1733-1740; _classForm 1742-1768; parPoly 1808-1826; parPsPoly 1855-1862; wsupPoly 1868-1881.
- SB of class forms 2065-2085; _declarePar 2253-2315 (same preconditions, same strictness; kappa < 0 rejected at 2289).
- wsup availability and slopes 2444-2461; asg 2463-2466.
- Centred rule: _shift3 2753-2849 (binomial expansion with exact denominators), _bound3 2863-2917, lowerBound3 2670-2737; stepCentre 1339-1349 accepts base variables only.
- Fact caches are keyed with the store-dependent coefficient (`name|k`, `name|cp`), so a cached polynomial cannot be reused with another slope.
- No weaker test found.

PART 2. Corruption controls on a real tree
Tree: JPG15p_v5 (23 nodes, 72 MB, pinned, rehashed 1adb3864...). Frozen Python checker cf8db52b..., venv python 3.9.6, `python -I -B wxcheck_v30.py CERT --json J`.
- K2 (default options, exactly the acceptance command): at interior node 'n5a39232273' (child 2 of the arc split of label 4 at 'nfd3c319ee4') I moved the lower arc end of label 4 from sine -0.259099127 to -0.259049086, leaving a gap of 5.0e-5 uncovered. Result: FAIL, "node 'n5a39232273' (child 2 of 'nfd3c319ee4'): its arc of square 4 does not contain the required arc", after 120 s; the 8 nodes before it were accepted.
- K1 (--keep-going, so every other node is still checked): at interior node 'n8289a454e8' I removed option (12,15,a,+1) and its child from the option split and deleted that leaf's line. Result: FAIL, "option split of the pair 12-15 omits option (12, 15, 'a', 1), which is not excluded"; nodes=22, accepted=21, 14 zero steps; 333 s. The only node not accepted is the corrupted one.
- No subtree restriction was needed. The line "exit K2: 0" in my run.log is the exit code of my output pipe, not of the checker; the verdicts come from the first output line and from K2_C1.json / K1_C1.json ('verdict': 'FAIL').

PART 3. Packing pin and frozen hashes in the acceptance runs
- accept_tree30.sh (0cd4ff06...) starts the checkers as `python -I -B wxcheck_v30.py CERT --json J1 $REFOPT` and `node --max-old-space-size=12000 wxcheck2_v30.js CERT --json J2 $REFOPT`.
- REFOPT is empty or `--packing FILE --expect-packing-sha256 SHA`. The script cannot pass --no-packing-pin, --node or --keep-going.
- All eleven logs show "options: default" for C1 and C2 and no "REFERENCE FILE" line.
- All eleven logs record the frozen hashes: checker cf8db52b..., checker2 97210adf..., SPEC 0a6dfc2a..., packing 24e296f5..., driver 0cd4ff06..., h_report30 0314aa1f..., FROZEN_30 6d65a070....
- Both checker reports name packing 24e296f5...; modes are 'full' and 'certificate'; exit codes 0, 0, 0; first lines PASS, PASS; last lines "RESULT: ACCEPTED" and "FIRST LINES: both PASS"; 50 "ok" lines (49 for JG), no FAIL line.
- The Python default pin is PINNED_PACKING_SHA256 = 24e296f5... (line 487); it is removed only by --no-packing-pin (line 3115).

PART 4. LOCAL_CERTIFICATE_IMPORT, all eleven
- Final record pinned. For every root the file `bigbox/join/RECORD_E<root>.md` on disk has the hash named in the table of JOIN_ROOTS.md (lines 108-118), and that hash is pinned in the root's packet row. For JPA it is pinned as the byte-identical copy jpa-import-AG/LEAD_RECORD.md, e10be786.... For JPWS, JPW13, JPG3p, JPG15m the row pins the early snapshot and also the final record and its batch 6, 5, 4, 3 review.
- Certificate hash: the same in the record, the acceptance log and the packet row, for all eleven. Rehashed by me: JQ, JPG3m, JPG3p, JPG17m, JPG17p, JPG15m, JPG15p. Not rehashed: JG, JPA_v5, JPWS_v4, JPW13.
- Root region hash: the same in the record, the log line "root region file ... has the stated SHA-256" and the packet row; all eleven root files rehashed.
- Admission premise: the two admission interfaces of ROOT_ADMISSION carry the same eleven root hashes, once each. JQ, JG, JPW13 are in join-design-1702/d-selected-roots-v2-review/ACCEPTED_INTERFACE.json; the eight v4/v5 roots are in standing-contract-20261009-2134/v5-root-review/ACCEPTED_INTERFACE.json. I grepped these two files and did not rehash them.
- Both checkers ACCEPT with the post-check; nodes, infeasible, terminal, split, steps and terms are equal between C1 and C2 in all eleven logs.
- The log lines "root node: box = the region's box, all 68 interval ends", "every arc ... = the region's root arc" and "side interval = the region's" are present with "ok" in the logs I read in full (JPG15p) or extracted (the other ten).
- Sanity check of my own: the reference point (xi = 0, directions u_i up to quarter turns) lies outside each of the ten EMPTY roots and inside JG, the only root with a terminal leaf.

(2) HAND-OVERS RESTATED

Checker theorem to whole root.
- Given: a certificate whose root node equals the region file (S = [R,R], box, arcs, 17 labels), every node closed, every child containing its piece.
- Then F(root) lies in the tube; with zero terminal leaves F(root) is empty.
- F(root) is all configurations with S = R exactly, every corner in [0,R]^2 (closed), pairwise disjoint interiors (touching allowed), xi in the closed box, a_i in the closed arc.
- The statement is for one labelling and one choice of side direction per square.

Side transfer (R to S0).
- Given a packing in [0,S0]^2 with S0 <= R. In the proof S0 < L < R; I did not verify L < R, which belongs to ALGEBRAIC_ENDPOINT.
- Keep every centre and direction and take S = R. Corners lie in [0,S0]^2, a subset of [0,R]^2 with the same corner at the origin, so (F1) holds at R; (F2) does not involve S.
- The coordinates xi_ik = e_ik.(q_i - p_i) and the arcs do not contain S (p_i, e_ik, u_i come from the packing file; p_13 uses the constant Sref).
- So a pose in the root at side S0 is the same point of F(root) at side R.
- Direction: emptiness at the larger side implies emptiness at every smaller side. The facts that contain S (wall hi, wsup xhi/yhi, side) are evaluated at S = R and are true for the embedded configuration.
- JUDGEMENT: no inequality goes the wrong way.
- Required of the admission premise, not checked by me: the poses it places in a root are measured with the container corner at the origin of this chart, and far-wall squares are admitted with the padding R - S0.

JG to G20S.
- The terminal leaf's store lies in the tube of EXPECT_JG_v2, which equals the G20S window on the sixteen labels (compared: core, the two box overrides, radius 1/10).
- The conclusion is coordinate-only, hence valid at the actual side.
- The G20S tree was accepted with 16 labels and S_floor = 4 (ACCEPT_G20S_v30.log), so it covers 4 <= S <= Sref, which includes L.
- I did not read G20S_PHYSICAL.

LEAF PROVENANCE

Reuse. Yes, by the records' own words and by the data.
- The records say the leaves are "all placed by containment, LEAF_FORMAT_RULING.md" (RECORD_EJPWS_v4.md line 76, RECORD_EJPG17m_v5.md line 71, RECORD_EJPA_v5.md line 77).
- In all eight certificates named in the question, every leaf's own box and arcs are strictly larger than the piece of the parent it closes: 15/15, 18/18, 22/22, 22/22, 32/32, 39/39, 70/70, 281/281.
- So the leaves were made on regions of their own. Whether a given leaf was first made for a v1, v2 or v2x root I did not establish. JUDGEMENT: it does not matter, for the following reason.

How each checker handles it. Neither checker reads any external leaf file or trusts a stored result. A leaf is an ordinary node line of the certificate with its own S, box, arcs and assumptions, and two things are checked.
(a) The leaf's certificate is verified against the leaf line's own data.
- Python: `_check_node` builds `initial_store(node)` from that line (wxcheck_v30.py 2534-2538, 1455-1463), rebuilds every fact from it and requires the `0` step with L >= value > 0 (2309-2315).
- Node: `checkNode` does the same (wxcheck2_v30.js 3136-3137, initialStore 1928-1936; the step test at 3010-3013).
- This proves F(leaf) is empty for the leaf's own, larger region.
(b) Containment of the parent's piece in the leaf is tested for every child link, leaf or not.
- Python: `child_failure` 2667-2709 (assumption list equal to the parent's plus the split assumption, every box interval, every arc by `arc_contains` 2613-2621 with re-expression of the centre, side interval), called from `TreeChecker._verify` 2727-2731.
- Node: `checkChild` 3289-3330 with `arcContainment` 3271-3279, called from `_pair` 3461-3466.
So provenance is irrelevant to soundness: (piece of N) is contained in F(leaf), and F(leaf) is empty.

What I checked myself.
- Control K2 shows the Python containment test rejecting a 5e-5 gap on a real tree.
- leafprov.py recomputed the containment of every child link of the eight certificates with code of my own (exact fractions, re-expressed centres): 753 links in all, 0 failures; 24 to 683 child arcs per tree have a centre different from the parent's, so the re-expression path is exercised.
- No split node has rounds, so the parent's final store is its node data and my test is the SPEC's test.
- No leaf box leaves its root box.

Not checked: the leaf arithmetic itself (apart from JPG15p_v5 above), the Node checker's rejection of a containment gap by a run, and the origin of each leaf file. A leaf's assumption list must equal the path's list exactly (both checkers), so a leaf made under other option assumptions cannot be hung in.

(3) SCRIPTS (all in <reviewer scratch>/)

- facts_test.py, exact fractions, imports the frozen Python checker read-only.
  A: 42,560 equalities of the checker's polynomials (al, be, co, si, Y for all 16 classes; opt corners; walls; wsup) against direct geometry, including the framed labels 11 and 13; all exact.
  B: Lemma P and Ps on touching and separated pairs: P+ 8,658, P- 8,770, Pk 17,428, Ps 8,524 cases, no violation; 3,098 and 1,699 cases tight (value exactly 0).
  Controls for B: P+ used outside its Y range, 38,213 violations; slope from a narrower arc, 3,251 violations; wrong sign of O_j, 709 of 709 violate.
  C: wall support, 97,651 cases hold, 80,615 tight; control with a narrower arc, 42,402 violations.
  D: `wsup_coefficients` and `ps_slopes` equal the SPEC formulas in 24,000 cases.
- logs_table.py: the eleven acceptance logs to one table (results under part 3 and 4).
- Hash script (inline): 99 pinned files of the 13 LOCAL rows rehashed, 0 mismatches, 4 skipped above 300 MB.
- scan.py, corrupt.py and the two checker runs K2, K1 (part 2).
- leafprov.py: 143 s, results above.
- h_report30.py on JPG15p_v5:
  positive with the files of record: 50 ok, RESULT: ACCEPTED;
  control a (EXPECT of JPG15m_v5): NOT ACCEPTED, "header window = expected window" FAIL and "root node: every arc ... (labels that differ: [15])" FAIL;
  control b (C1 report of my K1 run): exit 1 with six FAIL lines;
  control c (my K2 file with the reports of record): NOT ACCEPTED, "C1 checked this file" and "C2 checked this file" FAIL.
- Reference-point check of the eleven root files (inline; result under part 4).

(4) SHA-256, first 16 hex digits

Rehashed by me:
- PACKET.json 99d813ec5d1ffd1a; SPEC_v3.0.md 0a6dfc2ae10ed6f3; wxcheck_v30.py cf8db52bfa1cc565; wxcheck2_v30.js 97210adf74a3ebed.
- accept_tree30.sh 0cd4ff06497209cb; h_report30.py 0314aa1f8f742cd7; FROZEN_30.json 6d65a0705c039bbf; upper-packing-certificate.json 24e296f5995abc94.
- EXPECT_JG_v2.json 363ff3a6f97f872c; EXPECT_G20S.json 1447c955c52f5a52.
- Logs: JQ d04fa0f0f18576a9; JPWS 78f713f7ebb4263e; JPW13 8465744dfb265f4b; JPA 7b9b9eaa427dba25; JPG3m c0f07aba317e86e5; JPG3p 628d831ac54b45e1; JPG17m 88c670b3ca7d8641; JPG17p a86ef2c14fd9090f; JPG15m 8a730ba214eb8398; JPG15p fa0c177cb8d9e93f; JG 4a00565164511b55.
- Roots: JQ f4d1607eb4378487; JG f635af684d0f81d3; JPA adcf0d1bdc02b8ea; JPWS 7d32a55bc2b08005; JPW13 e1a489e1f0d04ec0; JPG3m 1e2a3b429193a69f; JPG3p c4287958b08fe4fc; JPG17m 18550e414d3f5057; JPG17p 11b68ec1eb4aa790; JPG15m f6495dc60d07a4fa; JPG15p 6c9ad4887e868fe0.
- Records: JQ d27d6d9b24f52eed; JG 947f9ffbb609e78c; JPA e10be7862229bd33; JPWS af742507a1553a11; JPW13 0f7d2cb3f0cb3d10; JPG3m 493e912222a6a8e6; JPG3p 16226ebd1dca325b; JPG17m ae527a87116bd338; JPG17p 0054d9b1f67d013b; JPG15m 33b20db1bc7f344e; JPG15p 8ce55c186f982223.
- Certificates: JQ 0b2a8ff8a3f9e12d; JPG3m 7535735021ff18c4; JPG3p 804ae79493f67336; JPG17m 68613d8407cb5a9f; JPG17p f392b6ba42c9abc3; JPG15m ed66c59b16b4b354; JPG15p 1adb38643a3a28a1.
- The C1/C2 JSON reports, batch reviews, SIDE_CAP_TRANSFER.json (03bd024468419832), ACCEPTED_REGIONS.json and the other files of the LOCAL rows are among the 99 that matched their pins.

Read but not rehashed: JG e7587199a38d4772; JPA_v5 b9f9283979d2fab1; JPWS_v4 538a6a512a10b72d; JPW13 7147d7780da90060 (hashes as in logs and packet); H6_PREMISES.json, H6_HANDOFF.md, H6_COVERAGE.tsv, PROOF_TEXT.md, JOIN_ROOTS.md; the two admission interfaces (pinned 033302490f21463e, 346a7e8501522232).

Scratch copies: K1_optionhole 6cc401cf144b34f5; K2_arcgap cc8ed9c80c84962f.

(5) NOT READ
- SPEC sections 9 to 12 (certificate format, what the application must add); section 8 was read, not tested.
- Python checker: sections A and E (strict JSON, parsing, well-formedness), run_round and accept_store (2333-2440), terminal_failure, root_failure, TreeChecker.add from line 2760 and finish, the main loop.
- Node checker: the Validator (960-1620), acceptStore, terminalTest, checkNode beyond the split tests, checkRoot, CertChecker, the 2.6 lowerBound path beyond one reading, _fact3, mulHot, hotOf.
- Arc and relative-arc facts 4.2, 4.3 and the indicator machinery 4.10: read in the SPEC, not tested.
- h_report30.py source, mk_table.py, FROZEN_30.json content.
- The eleven records beyond grep; all batch reviews; LEAF_FORMAT_RULING.md; SPEC_v3.0_NOTES.md (the 18:38 emptiness corollary: I argued it myself).
- REVIEW_30*.md, fresh_local_review.md, local_spec_notes.md, REPORT_LOCAL_CHECKERS_IMPORT.md: not read, so I can state no agreement or disagreement with them.
- The trees JG, JPW13 and JQ were not streamed by leafprov.py. The Node checker was run on nothing. No leaf arithmetic of record was replayed except in the two control runs on JPG15p_v5.
- Whether each root region equals what the admission premise needs mathematically (only the hash identity was checked); L < R; G20S_PHYSICAL.

(6) QUESTIONS TO THE AUTHORS
1. Will someone rehash JG, JPA_v5, JPWS_v4 and JPW13 at the pinned assembly paths in one sequential pass, and state for JPWS_v4 and JPA_v5 that the work files of the acceptance runs were those bytes?
2. Why is `terminal_leaves` null in EXPECT_JG_v2.json while the ten EMPTY expectations pin 0? Should the one terminal leaf 'td0f7ae2afe' be pinned?
3. Does the admission premise state explicitly that poses are taken with the container corner at the origin of the SPEC chart and that squares at the far walls are admitted at S0 < R with the shift R - S0 inside the root boxes? The side transfer needs exactly this and nothing else.
4. The packet row LOCAL_JPA pins the record as jpa-import-AG/LEAD_RECORD.md and not under its name in bigbox/join. They are byte-identical today (e10be786...). Is the join copy the file of record?

