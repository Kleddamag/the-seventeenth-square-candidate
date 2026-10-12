Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line. This report reviewed the earlier executions of the capture computation, named here by neutral designations (table EARLIER_EXECUTIONS.tsv); the audit of the execution carried in this edition and the complete row comparison with the earlier ones are separate evidence.

HOLDS WITH CONDITIONS: every one of the 210 obligations has a verdict from at least two readers and none is GAP, WRONG or NOT READ by all; but four blocks are not covered at the needed level by any final reader (K1 capture-checker core, K2 authenticity of the stored executions, K3 residue of the region checkers, K4 tree arithmetic), and the errata scope (E) is pending.

Included: the "earlier read" column, and REPORT_TERMINAL_2.md as delivered. Only ERRATA is treated as PENDING. The filled table is saved as `<reviewer scratch>/COVERAGE_FILLED.tsv` (sha256 8db8fa8225179e7d), produced by `mk_cov.py` (693d1ef38120c06b).

Codes used below.
- Readers, with the line of the report file after the colon: ADM = REPORT_ADMISSION, TXT = REPORT_TEXT, SA / SB / SC = REPORT_SELECTOR_A / B / C, FR = REPORT_FRAME, RC = REPORT_RECEIPTS, LO = REPORT_LOCAL, TM = REPORT_TERMINAL, T2 = REPORT_TERMINAL_2, FC = REPORT_FRESH_CODEX_copy_d70d668e.
- Earlier reads in premise-review-20261010: EA = REPORT_A_charge, EC = REPORT_CHARGE_SEMANTICS, EL = REPORT_LOCAL_CHECKERS_IMPORT, ECAP = REPORT_CAPACITY_LEMMA, EM = REPORT_MARKER_CONVERSION, ECF = REPORT_C_frame, ES6 = REPORT_S6_*.
- Open conditions: K1 to K4 as in the verdict line; E = waits for ERRATA (text, dependency graph or record).

## (b) NOT COVERED AT THE NEEDED LEVEL

**1. K1, the core of CHARGE_SEMANTICS: no final reader at M.**
- Not read in this round: row validity (core strictly inside every parent of the row interval, centre envelope), the limiting-core / boundary-of-cell step, the capacity bound (sum of charges <= M), and the sweep and cell arithmetic.
- The readers say so themselves: RC:186, FR:45 and FR:124, SA:102, SB:160, SC:138, FC:14 and FC:295.
- What final readers did cover at M:
  - side and centre of all 98 executions, the printed statement, the declared-symmetry rule, the orbit / mirror_x reduction with its validity argument, high-first order, parser, alias rule and slice binding (RC:74-79, RC:91-121);
  - S <= C by concentric inclusion (TXT:62, FC:253);
  - the budget recomputed from the certificate features for 6 of 98 certificates only (FR:7, FR:100).
- Earlier reads supply M for the Python side; both reports are themselves pinned in the CHARGE_SEMANTICS row (fdc92d4c, 89e5b821).
  - EC (packet 11ef58b1): chain (i) to (v), item-by-item source reading, 28 corruptions. Bytes confirmed: its five module hashes and 7f6b2347 equal the frozen hashes in every receipt of record (RC:135) and exact_classes.py 802dc62a is in RECEIPT_ROSTER.json. Its limit: exact_restricted.py only at lines 163-180, 455-520, 588-665 (EC:61).
  - EA (packet of 14:50): full reading of exact_general.py, integer_sweep.py, boolean_rule.py, exact_classes.py and the geometry and decision parts of exact_restricted.py; budget lemma, row validity (re-run on all 18,000 KEY_W rows), boundary centres, a toy test of geometry(). Bytes confirmed only for exact_classes.py (802dc62a); the other four modules' hashes are not in its text, so NOT confirmed.
- Covered by nobody at M, earlier reads included:
  - the Node sweep source (lines 752-905), buildFixed and ruleOf (RC:186; EC:61; EA "only its row loop and order");
  - the helpers _ints, slab_minima, _first_below, _merge / _intersect / _complement of exact_restricted.py (EC:61; EA unclear);
  - the budget from features for the other 92 certificates;
  - the row-validity inequalities on any real certificate other than KEY_W.
- JUDGEMENT: the Python = Node agreement on all 1,728,000 rows (RC:140) checks the two sweeps against each other, not against the mathematics.

**2. K2, authenticity of the stored executions: nobody.**
- Receipt-level tests cannot show it (RC:28-32, FC:295).
- Evidence held: 4 rows re-executed (RC:32); about 60 runs of 1 to 3 rows (EC:60, earlier packet); slice 9 of PS_1^17, 1,500 rows, Mac equal to cloud in both checkers (SB:25).
- Saved-provenance audits were checked for fields, hashes and partitions only: SA (25), SC (58), FR (6); the git objects by nobody (SA:102, SB:161, SC:138).
- The second execution (ledger X3) is still running, and the 21 folders of second executions are unchecked (RC:44).
- All 191 capture-side obligations carry K1 and K2.

**3. K3, residue of LOCAL_CHECKER_SOUNDNESS.**
- At M in this round (LO:17): SPEC 4.6, 4.8, class forms, centred rule, 4.7 exclusion, split and child containment, in both checkers.
- At M by the earlier reader EL (bytes confirmed: SPEC 0a6dfc2a, wxcheck_v30.py cf8db52b, wxcheck2_v30.js 97210adf, h_report30 0314aa1f, all equal to the final pins): Python leaf / store / pair closure / terminal / splits / tree / root logic.
- Read by nobody:
  - Node checker: Validator (960-1620), acceptStore, terminalTest, checkNode beyond the split tests, checkRoot, CertChecker, the 2.6 lowerBound path, _fact3, mulHot, hotOf (LO:167; EL:98 "did not read the Node checker's source at all");
  - Python: Reference class, parse_round, parse_fact_name, most of the parsing sections A and E (EL:98, LO:166);
  - SPEC sections 9 to 12 (LO:165) and sections 3 to 5 and 10 line by line (EL:101).
- Read but not tested: arc and relative-arc facts 4.2, 4.3 and the indicator machinery 4.10 (LO:168; EL:100 "no control on a relative-arc store entry, a cut, an ind declaration or a sign split").

**4. K4, tree arithmetic: no reader replayed the tree arithmetic of any of the eleven roots in this round, with one partial exception.**
- The evidence is the two frozen checkers' saved acceptance runs: logs concordant (LO:65-69); C1 and C2 agree on 1,130 nodes and 719 zero-step values (FC:300).
- Exception in this round: JPG15p_v5, 21 of 23 nodes re-verified by the frozen Python checker on corrupted copies (LO:29, LO:61).
- Earlier: the whole JQ v1 certificate re-run through both frozen checkers on a copy by EL (EL:59; certificate 0b2a8ff8, same bytes as the final pin).
- No replay of any kind for JG, JPA, JPWS, JPW13, JPG3m, JPG3p, JPG17m, JPG17p, JPG15m.
- Child-link containment was recomputed with own code for eight trees, 753 links (LO:123), but not for JG and JPW13 (LO:172).
- The terminal test of JG's one terminal leaf was checked by no reader (ADM:51, LO:20).
- G20S tree (679 nodes) and HW tree (579 nodes): arithmetic by no reader, headers and v3.0 logs only (TM:2 C2, TM:33, FC:22). No report states that these two logs carry the frozen checker hashes.

**5. LOCAL_CERTIFICATE_IMPORT, the part "independent record review": R only.**
- The eleven RECORD_E*.md files and the batch reviews were read in full by nobody (LO:170; FC:302 read lines 1-75 and 1-85 of the JPWS pair; ADM:82 the first 60 lines of one).
- The h_report30.py source was not read in this round (LO:169); EL read its lines 338-342 and 395-446.

**6. UPPER: M only through the authors' script.**
- TXT:36 read check_endpoint.py in full and reran it with two negative controls; its own independent check is float. FC:12 imported it.
- No reader recomputed the 68 walls and 136 pairs exactly with code of their own.

**7. G20S_PHYSICAL after TERMINAL-2.**
- The rigidity chain is M: normalized stage TM:18 and TM:52-56; finite rows, stop cuts and transfers T2:19-21; hand-overs TM:19-21.
- Left: the two trees (K4); no pinned text derives the finite-row remainders (T2:6: the reader derived them, and the "independent" builder shares the formula); the file of record proves step 3 by the other route (TM:8); relational.py and verify.py were read by nobody (TM:71, T2:93). JUDGEMENT: I do not know whether these two files are load-bearing.

**8. Files of record read by no final reader, claim re-derived independently.** JUDGEMENT: these are not gaps, since the claims were re-derived.
- ENDPOINT producer THEOREM.md 892de6a5 and its review (TXT:37, TXT:115).
- REVIEW_KEYW_AMENDMENT.md 0600869f (FR:125, ADM:82, SA:102).
- v5-root-review and d-selected-roots-v2-review (ADM:73, ADM:82).
- c7-c8 RECEIPT.json and accepted.json (FR:127).
- coarse-capacity-R files (FR:126; ECAP read them, bytes confirmed).
- The contents of S6_ACTIVATION and S6_ACTIVATION_AR beyond the two selected rows (SB:85, SA:102).

**9. Dependency rows that do not carry their use (E).**
- 150 rows are consumed by no other row (my closure of H6_PREMISES depends_on): the 40 Q / PW / C rows, SL11_T020, C7_C8_TRANSFER, the 84 BRANCH rows, UPPER, the ten EMPTY roots, WALL_CONTRADICTION.
- C_7, C_8, Q_j, PW_j and the CLASS_PS rows have empty depends_on.
- BRANCH rows reach FRAME_ASSIGNMENT, KEY_W_ELIMINATION and L_4 / L_15 / L_17 only through SELECTOR_LOGIC -> ROOT_ADMISSION, and never reach their own LOCAL root.
- The use is covered at M from the text by ADM:38 (targets per root), SC:60-74, SB:76-83 and FC:250-262, and the per-root label count closes (17 in each of the eleven roots, my count). The graph itself is the ERRATA reader's scope.

**10. PENDING (ERRATA).**
- PROOF_TEXT lines 62, 94, 118, 122, the section 1 and section 8 wording, and the ENDp argument that is absent from the manuscript (TXT:6-12, SB:8, FC:314).
- The stale C_16 "RECEIPT OPEN" entry (ADM:6; the receipt of record exists, RC:63).
- FRAME_L9.json status and first-run keys (FR:11-16); stale statuses (TM:12, T2:10, SC:19-22).
- Which definition of role 3 is meant (SA:10).
- Whether the 84-clause selector file has a recorded acceptance (SA:16).

## Condition chains

Closed, with the report that closes them:
- ADM C1 (L enclosure): TXT:35, R - L - eps = 4.31937e-17 > 0; also T2:55, TM:35.
- ADM C2, SA C2 / C3 / C5, SB C2, SC C-b / C-c / C-e / C-f: FRAME_ASSIGNMENT (FR:33, FC:15), KEY_W_ELIMINATION (FR:35, FC:24), COARSE_LOOSE_CAPACITY (FR:36, FC:25), C7_C8_TRANSFER (FR:34, FC:16), WALL_PARTITION (ADM:20, FC:17), L_k (RC:62; use SC:35). All end in K1, K2.
- SA C4, SB C3 / C4, SC C-d: ROOT_ADMISSION for all eleven roots with the 136-pair separation (ADM:22, ADM:63; FC:270). The chart equals SPEC 3.0 section 1 for sixteen labels (TM:41) and was taken from SPEC lines 58-70 for all seventeen (ADM:26). JUDGEMENT: label 4's reference pose is covered only by ADM and FC.
- SA C6 (the other 48 clauses): SB:31-44, SC:29-32.
- FR C1 (row arithmetic): RC:139, every row re-decided from stored figures; ends in K1, K2.
- RC c1 (symmetrised reading): FR:50-53 uses exactly the united classes.
- RC c2 (alias): RC:22, SA:52, SB:95, SC:85, FC:293.
- RC c3 (the two marker literals): FC:293, FR:37, SC:93, and EM (bytes confirmed: 520ce3ce, aa8b1410, 4f6fd341, 9fa41211, 0943e2ea). Slots, gate, frame, symmetry and the count inequality are the same.
- RC c4 (C_7, C_8 have no execution): FR:42-43, FC:67-68.
- LO C1 (four large certificates not rehashed): ADM:22, ADM:68 and ADM:78 hashed all eleven gz files itself, the four large ones included, equal to the manifest; TM:62 hashed JG. An independent reader therefore closes it, not only the audit lead's rehash.
- TXT (a), TM C1: T2:19-21.
- T2 "not re-proved" items: S* = L (TXT:35, TM:35); entry into the finite stage (TM:19-20).
- FC C1: TXT:35-36.

Not closed:
- K1, K2, K3, K4 as above.
- LO C2 only as far as EL reaches; LO C3; LO C4 (records).
- TM C2 (trees); TM C3 and ADM C3 (E).
- SB F1: the sign of the two PS_6^17 halves is bound by classes_sha256 alone. Both hashes were reproduced by SB:129-130 and RC:18-19, and FC:282 rejected the swapped file. JUDGEMENT: sufficient.

Candidates examined:
- Full proof of CHARGE_SEMANTICS: item 1.
- Authenticity: item 2.
- Tree arithmetic: item 4.
- Three sub-parts of G20S_PHYSICAL: closed by T2.
- ENDPOINT's producer theorem: file unread, claim M (item 8).
- Marker literals: closed.
- C7_C8_TRANSFER: M by FR and FC; consumed by no row (item 9).
- KEY_W: R by RC:54 and FR:44, budget recomputed from features (FR:100), use M at FR:35. The stale class comment (FR:137) agrees with the ends ADM:35 and ADM:58 used.

## (c) Disagreements between reports

1. Label-11 lower arc margin of the v5 roots: ADM:45-46 gives 5.123e-13 "as a sine"; SA:20 and SB:21 give 2.6e-13; SC:31 gives 2.57e-13. The ratio is 1.99. JUDGEMENT: same quantity in two measures (sine of the angle against tan-half difference, factor 2/(1+tau^2)); I did not recompute it. The upper end shows the same pattern (ADM:42 7.228e-11, SA:60 3.7e-11). FINDINGS A-Q5 quotes the sine value without the unit.
2. bridge.py: TXT:99 gives 8d5c2a8253f1aae9; TM:65 and T2:78 give a3b496ca0422b481. These are two different files of the same name: the first hash occurs in the packet's endpoint audit-manifest and receipt, the second in the sixteen-square MANIFEST 91aa01be (my grep). Not a contradiction; the reports give no paths.
3. Role 3 and the PSS clauses: SA:10 and SC:24 say the T03 / T15 clauses need no coarse-capacity step; SA:10 explicitly disagrees with the pinned earlier review D item S3. PROOF_TEXT sections 5 and 6 differ; open for the authors.
4. Scope of sign-off on the region checkers: EL:3 "all three premises hold"; LO:2 and FC:343 keep CONDITION. A difference of scope, not of a lemma.
5. Verdict words for E07A and KEY_W: RC:53-54 HOLDS, FR:41 and FR:44 CONDITION C1, FC:30 and FC:75 CONDITION C2. Same facts, different scope.
6. Count of one-unit surpluses: SC:17 lists six, RC:60-69 shows eight among the 98 (adds PS_L14_T17 and PS_L06_T17_ENDm, which SB:23 reports). Consistent as a union.
7. Label-12 marker slots: SA:50, SB:72, SC:32 say five (PS / PSS files); FC:284 says Q12 six, PW12 five, C12 four. Different files, no conflict; PROOF_TEXT:62 is imprecise.

Everything else that two readers computed agrees:
- Smallest admission margin 4.319e-17 (ADM:10, TXT:35, SA:20, SB:19, SC:54, T2:61); R - L = 4.8366e-17 (TXT:35, TM:35, T2:55); eps 5.17e-18 (ADM:10, TM:35); L to 39 digits (TXT:35, T2:55).
- All surpluses of the 98 executions between RC and SA:66, SB:31-48, SC:97, FR:37-44; five of them recomputed by me from the quoted Gamma and M (FRAME_MARKER 13, FRAME_1114 4/8, KEY_W 12, SL11 12, CLASS_PS_L05_T17 17).
- diam^2 values: 9437/31250 (ADM:33, SA:50, SB:41, SC:32); S3 and S17 (SA:10, SB:102, SC:63); coarse-17 (SB:102, SC:67, FR:81, ECAP:23); C_12 in JG 0.395298 against the bound 0.4428 (ADM:33, SC:151).
- Bernstein minima (FR:101, FC:280, ECAP:43).
- Gate ends 61301/200000 and 591183/1408817 with gaps 1/200000 and 974949/14197000000 (ADM:35, ADM:61, SA:44, SC:66, FR:92, ECAP:35); KEY_W ends 30651/100000 and 44941/100000 (ADM:58, FR:72, SA:2, FC:255).
- Root-file hashes (ADM:77, LO:155, SA:73, SB:119-121, SC:109-114) and certificate hashes (ADM:78, LO:157, LO:160, TM:62).
- Class and receipt hashes wherever two reports list them (L_L03 / 04 / 15 / 17, SL11, marker, C_L07 / 08, the END pair, the frame receipts).
- Node counts: the sum of LO:19-29 is 1,130 nodes and 719 infeasible leaves, equal to FC:300; 1,728,000 rows (RC:141) and 1,998,000 (FC:291) both follow from 94 / 4 and 108 / 7 executions.
- Finite stage: 1,564 bounds and final core 64007486789/10^15 (TM:56, T2:67).

JUDGEMENT, from the union of SA:8, SB:56, SC:25 and FR:20-26: the printed minimum score suffices for all 98 executed statements, so the high-first upgrade of CHARGE_SEMANTICS is load-bearing for none of them.

## (d) Counts

| Group | Count | Coverage |
|---|---|---|
| Branch implications | 84 | M, each by one selector reader and by FC |
| Selected budgets | 49 | R by RC, SB and FC plus the family reader; use M |
| Base rows with an execution | 48 | R by RC and FC (+ SC 42, FR 6); use M |
| Derived base rows C_7, C_8 | 2 | no receipt exists; M by FR and FC |
| Slab row | 1 | R (RC, SB, FC); use M (SB, ADM, FC) |
| Premises, whole content at M | 11 | UPPER with the qualifier of item 6 |
| Premises, partial | 4 | CHARGE_SEMANTICS, LOCAL_CHECKER_SOUNDNESS, LOCAL_CERTIFICATE_IMPORT, G20S_PHYSICAL |
| Whole local roots | 11 | R; no complete arithmetic replay in this round |

Open conditions: K1 K2 on 191 obligations, K3 / K4 on 15, none on 4 (ALGEBRAIC_ENDPOINT, UPPER, ENDPOINT, COARSE_LOOSE_CAPACITY). Rows waiting for ERRATA in the table: 8. Rows with GAP, WRONG, or NOT READ by all readers: 0.

## (1), (2), (5), (6)

- Table: section (a) below.
- Hand-overs: none restated; mine is a bookkeeping read.
- Scripts: `mk_cov.py` builds the table; the check script confirmed 210 ids in H6 order, 7 columns, and every FC line reference and FC verdict against the Codex report (0 mismatches). Negative control: two ids swapped is detected by both tests.
- sha256 (first 16) of files relied on:
  - REPORT_ADMISSION 34a889bffd776b1d; FRAME f97019c656ee33d9; FRESH_CODEX copy d70d668e4e463cd8 (byte-identical to its original); LOCAL 022131e8adc45830; RECEIPTS ab18158a320996ec; SELECTOR_A 32f283bfe5b33ca6; SELECTOR_B 1c2003f5afdca974; SELECTOR_C 783a47f8871db75f; TERMINAL 04695c4a184f43e9; TERMINAL_2 d95c56521d9224c7; TEXT 393e6ef1af43f2fe.
  - COVERAGE_PLAN f29cca8380c1b674; FINDINGS b1e22970add8e591.
  - PACKET.json 99d813ec5d1ffd1a; H6_COVERAGE.tsv 9e9884091d5f8bed; H6_PREMISES.json 6741793e2af90717; RECEIPT_ROSTER.json c031c9afc47c7ddb.
  - Earlier reads: EC 89e5b8211283ab83, EA fdc92d4c02cb9f54, EL 7216ed6a50f96c7d, ECAP d9b883c5c42dc024, EM a366444cd16397ab, all pinned in H6_PREMISES. REPORT_SKELETON_EARLY_READ 00372cf794472a99 is not pinned and adds no level.
- NOT READ:
  - PROOF_TEXT, H6_HANDOFF.md, SELECTED_ORIGINAL_MAP.json, any proof source or scratch output of the readers;
  - REPORT_B_local, C_frame, D_join, SKELETON and the S6 reports beyond heads and grep lines, so "ECF" in the table is by its headline only;
  - INPUT_MANIFEST.json, which could confirm EA's other module bytes.
  - No authors' working notes were opened.
- Questions to the authors:
  1. Will the capture-checker core (K1) get a reader of its own, so that it does not rest on two earlier-packet reads?
  2. Which G20S / HW log lines carry the frozen checker hashes?
  3. Are relational.py and verify.py load-bearing?
  4. State the unit of the label-11 margin.

## (a) TSV

Columns: id, kind, readers (report:line, verdict as written), level, verdict, earlier read, open condition.

```
ALGEBRAIC_ENDPOINT	prem	TXT:35 HOLDS; T2:55; TM:35; FC:11 CONDITION C1	M	HOLDS	-	-
UPPER	prem	TXT:36 HOLDS; FC:12 CONDITION C1	M (authors' exact script read in full and rerun; own check float only)	HOLDS	-	-
ENDPOINT	prem	TXT:37 HOLDS; FC:13 HOLDS	M	HOLDS	-	-
CHARGE_SEMANTICS	prem	RC:74 HOLDS for sub-claims, rest NOT READ; FR:45 NOT READ; TXT:62; FC:14 CONDITION C2	M in part; core N	CONDITION	EA (bytes: exact_classes.py confirmed, other modules NOT confirmed); EC (bytes confirmed): M for the Python core	K1 K2
FRAME_ASSIGNMENT	prem	FR:33 HOLDS given the four rows; FC:15 HOLDS; RC:10	M	HOLDS given rows	ECF (earlier packet, bytes not compared)	K1 K2
C7_C8_TRANSFER	prem	FR:34 HOLDS given E07A; FC:16 HOLDS; ADM:60	M	HOLDS given E07A	ECF (earlier packet, bytes not compared)	K1 K2; E
WALL_PARTITION	prem	ADM:20 CONDITION C2; FC:17 HOLDS	M	CONDITION (C2 closed by FR:33, FR:36, SC:35)	-	K1 K2
ROOT_ADMISSION	prem	ADM:22 CONDITION C1-C4; FC:18 HOLDS	M	CONDITION (C1 closed by TXT:35; C2 by FR:33-36; C3 open)	-	K1 K2; E
SELECTOR_LOGIC	prem	SA:23 CONDITION (36 clauses); SB:31-44 (24); SC:29-32 (24); FC:19 HOLDS (84)	M	HOLDS as union of the three parts	ES6 (pinned, read by SB after verdict)	K1 K2; E
LOCAL_CHECKER_SOUNDNESS	prem	LO:17 CONDITION; FC:20 CONDITION C3	M in part	CONDITION	EL (bytes confirmed): M for Python main logic	K3
LOCAL_CERTIFICATE_IMPORT	prem	LO:18 CONDITION; ADM:22; TXT:63; FC:21 CONDITION C3	R (import) + M (side transfer)	CONDITION	EL (bytes confirmed)	K3 K4; records N
G20S_PHYSICAL	prem	TXT:38 CONDITION; TM:18 CONDITION; T2:19-21 HOLDS (three parts); FC:22 CONDITION C4	M (rigidity chain) + R (G20S, HW trees)	CONDITION	-	K3 K4; E
WALL_CONTRADICTION	prem	TXT:39 HOLDS given G20S_PHYSICAL, LOCAL_JG; TM:21 HOLDS; FC:23 HOLDS	M	HOLDS given premises	-	K3 K4
KEY_W_ELIMINATION	prem	FR:35 HOLDS given KEY_W, FRAME_ASSIGNMENT; FC:24 HOLDS; ADM:58	M	HOLDS given rows	ECF (earlier packet, bytes not compared)	K1 K2
COARSE_LOOSE_CAPACITY	prem	FR:36 HOLDS; FC:25 HOLDS	M	HOLDS	ECAP (coarse-capacity-R bytes confirmed; bridge text NOT the same bytes)	-
FRAME_MARKER	base	FR:37 CONDITION C1; RC:49 CONDITION c1,c3; SB:48; FC:26 CONDITION C2	R (use M: FR:33)	CONDITION	EM (bytes confirmed)	K1 K2
FRAME_0506	base	FR:38 CONDITION C1; RC:50 CONDITION c1; FC:27 CONDITION C2	R (use M: FR:33)	CONDITION	-	K1 K2
FRAME_1114	base	FR:39 CONDITION C1,C2; RC:51 CONDITION c1; FC:28 CONDITION C2	R (use M: FR:33)	CONDITION	-	K1 K2
FRAME_0917	base	FR:40 CONDITION C1; RC:52 CONDITION c1; FC:29 CONDITION C2	R (use M: FR:33)	CONDITION	-	K1 K2
E07A	base	FR:41 CONDITION C1; RC:53 HOLDS; FC:30 CONDITION C2	R (use M: FR:34)	CONDITION	-	K1 K2
Q_1	base	SC:33 HOLDS under C-a,C-b; RC:60 HOLDS; FC:31 CONDITION C2	R (use M: SC:33, ADM:38)	CONDITION	-	K1 K2
Q_2	base	SC:33 HOLDS under C-a,C-b; RC:60 HOLDS; FC:32 CONDITION C2	R (use M: SC:33, ADM:38)	CONDITION	-	K1 K2
Q_3	base	SC:33 HOLDS under C-a,C-b; RC:60 HOLDS; FC:33 CONDITION C2	R (use M: SC:33, ADM:38)	CONDITION	-	K1 K2
Q_4	base	SC:33 HOLDS under C-a,C-b; RC:60 HOLDS; FC:34 CONDITION C2	R (use M: SC:33, ADM:38)	CONDITION	-	K1 K2
Q_5	base	SC:33 HOLDS under C-a,C-b; RC:60 HOLDS; FC:35 CONDITION C2	R (use M: SC:33, ADM:38)	CONDITION	-	K1 K2
Q_6	base	SC:33 HOLDS under C-a,C-b; RC:60 HOLDS; FC:36 CONDITION C2	R (use M: SC:33, ADM:38)	CONDITION	-	K1 K2
Q_7	base	SC:33 HOLDS under C-a,C-b; RC:60 HOLDS; FC:37 CONDITION C2	R (use M: SC:33, ADM:38)	CONDITION	-	K1 K2
Q_8	base	SC:33 HOLDS under C-a,C-b; RC:60 HOLDS; FC:38 CONDITION C2	R (use M: SC:33, ADM:38)	CONDITION	-	K1 K2
Q_10	base	SC:33 HOLDS under C-a,C-b; RC:60 HOLDS; FC:39 CONDITION C2	R (use M: SC:33, ADM:38)	CONDITION	-	K1 K2
Q_11	base	SC:33 HOLDS under C-a,C-b; RC:60 HOLDS; FC:40 CONDITION C2	R (use M: SC:33, ADM:38)	CONDITION	-	K1 K2
Q_12	base	SC:33 HOLDS under C-a,C-b; RC:60 HOLDS; FC:41 CONDITION C2	R (use M: SC:33, ADM:38)	CONDITION	-	K1 K2
Q_13	base	SC:33 HOLDS under C-a,C-b; RC:60 HOLDS; FC:42 CONDITION C2	R (use M: SC:33, ADM:38)	CONDITION	-	K1 K2
Q_14	base	SC:33 HOLDS under C-a,C-b; RC:60 HOLDS; FC:43 CONDITION C2	R (use M: SC:33, ADM:38)	CONDITION	-	K1 K2
Q_15	base	SC:33 HOLDS under C-a,C-b; RC:60 HOLDS; FC:44 CONDITION C2	R (use M: SC:33, ADM:38)	CONDITION	-	K1 K2
Q_16	base	SC:33 HOLDS under C-a,C-b; RC:60 HOLDS; FC:45 CONDITION C2	R (use M: SC:33, ADM:38)	CONDITION	-	K1 K2
Q_17	base	SC:33 HOLDS under C-a,C-b; RC:60 HOLDS; FC:46 CONDITION C2	R (use M: SC:33, ADM:38)	CONDITION	-	K1 K2
PW_1	base	SC:34 HOLDS under C-a,C-b; RC:61 HOLDS; FC:47 CONDITION C2	R (use M: SC:34, ADM:38)	CONDITION	-	K1 K2
PW_2	base	SC:34 HOLDS under C-a,C-b; RC:61 HOLDS; FC:48 CONDITION C2	R (use M: SC:34, ADM:38)	CONDITION	-	K1 K2
PW_5	base	SC:34 HOLDS under C-a,C-b; RC:61 HOLDS; FC:49 CONDITION C2	R (use M: SC:34, ADM:38)	CONDITION	-	K1 K2
PW_6	base	SC:34 HOLDS under C-a,C-b; RC:61 HOLDS; FC:50 CONDITION C2	R (use M: SC:34, ADM:38)	CONDITION	-	K1 K2
PW_7	base	SC:34 HOLDS under C-a,C-b; RC:61 HOLDS; FC:51 CONDITION C2	R (use M: SC:34, ADM:38)	CONDITION	-	K1 K2
PW_8	base	SC:34 HOLDS under C-a,C-b; RC:61 HOLDS; FC:52 CONDITION C2	R (use M: SC:34, ADM:38)	CONDITION	-	K1 K2
PW_10	base	SC:34 HOLDS under C-a,C-b; RC:61 HOLDS; FC:53 CONDITION C2	R (use M: SC:34, ADM:38)	CONDITION	-	K1 K2
PW_11	base	SC:34 HOLDS under C-a,C-b; RC:61 HOLDS; FC:54 CONDITION C2	R (use M: SC:34, ADM:38)	CONDITION	-	K1 K2
PW_12	base	SC:34 HOLDS under C-a,C-b; RC:61 HOLDS; FC:55 CONDITION C2	R (use M: SC:34, ADM:38)	CONDITION	-	K1 K2
PW_13	base	SC:34 HOLDS under C-a,C-b; RC:61 HOLDS; FC:56 CONDITION C2	R (use M: SC:34, ADM:38)	CONDITION	-	K1 K2
PW_14	base	SC:34 HOLDS under C-a,C-b; RC:61 HOLDS; FC:57 CONDITION C2	R (use M: SC:34, ADM:38)	CONDITION	-	K1 K2
PW_16	base	SC:34 HOLDS under C-a,C-b; RC:61 HOLDS; FC:58 CONDITION C2	R (use M: SC:34, ADM:38)	CONDITION	-	K1 K2
L_3	base	SC:35 HOLDS under C-a,C-b,C-c; SA:37 CONDITION; RC:62 HOLDS; FC:59 CONDITION C2	R (use M: SC:35)	CONDITION	-	K1 K2
L_4	base	SC:35 HOLDS under C-a,C-b,C-c; RC:62 HOLDS; FC:60 CONDITION C2	R (use M: SC:35)	CONDITION	-	K1 K2
L_15	base	SC:35 HOLDS under C-a,C-b,C-c; RC:62 HOLDS; FC:61 CONDITION C2	R (use M: SC:35)	CONDITION	-	K1 K2
L_17	base	SC:35 HOLDS under C-a,C-b,C-c; SB:48; RC:62 HOLDS; FC:62 CONDITION C2	R (use M: SC:35)	CONDITION	-	K1 K2
C_1	base	SC:36 HOLDS under C-a,C-b,C-c,C-e; RC:63 HOLDS; FC:63 CONDITION C2	R (use M: SC:36, ADM:61)	CONDITION	-	K1 K2
C_2	base	SC:36 HOLDS under C-a,C-b,C-c,C-e; RC:63 HOLDS; FC:64 CONDITION C2	R (use M: SC:36, ADM:61)	CONDITION	-	K1 K2
C_5	base	SC:36 HOLDS under C-a,C-b,C-c,C-e; RC:63 HOLDS; FC:65 CONDITION C2	R (use M: SC:36, ADM:61)	CONDITION	-	K1 K2
C_6	base	SC:36 HOLDS under C-a,C-b,C-c,C-e; RC:63 HOLDS; FC:66 CONDITION C2	R (use M: SC:36, ADM:61)	CONDITION	-	K1 K2
C_7	base	FR:42 HOLDS as occupancy; FC:67 HOLDS; SC:37 NOT READ; RC:55 NOT READ	M (derived row, no execution exists)	HOLDS given E07A	-	K1 K2 through E07A; E
C_8	base	FR:43 HOLDS as occupancy; FC:68 HOLDS; SC:37 NOT READ; RC:56 NOT READ	M (derived row, no execution exists)	HOLDS given E07A	-	K1 K2 through E07A; E
C_10	base	SC:36 HOLDS under C-a,C-b,C-c,C-e; RC:63 HOLDS; FC:69 CONDITION C2	R (use M: SC:36, ADM:61)	CONDITION	-	K1 K2
C_11	base	SC:36 HOLDS under C-a,C-b,C-c,C-e; RC:63 HOLDS; FC:70 CONDITION C2	R (use M: SC:36, ADM:61)	CONDITION	-	K1 K2
C_12	base	SC:36 HOLDS under C-a,C-b,C-c,C-e; RC:63 HOLDS; FC:71 CONDITION C2	R (use M: SC:36, ADM:61)	CONDITION	-	K1 K2
C_13	base	SC:36 HOLDS under C-a,C-b,C-c,C-e; RC:63 HOLDS; FC:72 CONDITION C2	R (use M: SC:36, ADM:61)	CONDITION	-	K1 K2
C_14	base	SC:36 HOLDS under C-a,C-b,C-c,C-e; RC:63 HOLDS; FC:73 CONDITION C2	R (use M: SC:36, ADM:61)	CONDITION	-	K1 K2
C_16	base	SC:36 HOLDS under C-a,C-b,C-c,C-e; RC:63 HOLDS; FC:74 CONDITION C2	R (use M: SC:36, ADM:61)	CONDITION	-	K1 K2
KEY_W	base	FR:44 CONDITION C1; RC:54 HOLDS; FC:75 CONDITION C2	R (use M: FR:35)	CONDITION	EA (KEY_W certificate rows; bytes not compared)	K1 K2
SL11_T020	slab	SB:45 CONDITION C1-C3; RC:64 HOLDS; ADM:42; FC:76 CONDITION C2	R (use M: SB:45, FC:76)	CONDITION	EC section 3 (bytes confirmed)	K1 K2; E
CLASS_PSSW37_L11_T03	budget	SA:36 CONDITION C1; SB:47; RC:65 HOLDS; FC:77 CONDITION C2	R (use M: SA:27-32)	CONDITION	-	K1 K2
CLASS_PSSW37_L11_T15	budget	SC:38; SB:47; RC:66 HOLDS; FC:78 CONDITION C2	R (use M: SC:29-32)	CONDITION	-	K1 K2
CLASS_PSS_L01_T03	budget	SA:35 CONDITION C1; SB:47; RC:65 HOLDS; FC:79 CONDITION C2	R (use M: SA:27-32)	CONDITION	-	K1 K2
CLASS_PSS_L01_T15	budget	SC:38; SB:47; RC:66 HOLDS; FC:80 CONDITION C2	R (use M: SC:29-32)	CONDITION	-	K1 K2
CLASS_PSS_L02_T03	budget	SA:35 CONDITION C1; SB:47; RC:65 HOLDS; FC:81 CONDITION C2	R (use M: SA:27-32)	CONDITION	-	K1 K2
CLASS_PSS_L02_T15	budget	SC:38; SB:47; RC:66 HOLDS; FC:82 CONDITION C2	R (use M: SC:29-32)	CONDITION	-	K1 K2
CLASS_PSS_L05_T03	budget	SA:35 CONDITION C1; SB:47; RC:65 HOLDS; FC:83 CONDITION C2	R (use M: SA:27-32)	CONDITION	-	K1 K2
CLASS_PSS_L05_T15	budget	SC:38; SB:47; RC:66 HOLDS; FC:84 CONDITION C2	R (use M: SC:29-32)	CONDITION	-	K1 K2
CLASS_PSS_L06_T03	budget	SA:35 CONDITION C1; SB:47; RC:65 HOLDS; FC:85 CONDITION C2	R (use M: SA:27-32)	CONDITION	-	K1 K2
CLASS_PSS_L06_T15	budget	SC:38; SB:47; RC:66 HOLDS; FC:86 CONDITION C2	R (use M: SC:29-32)	CONDITION	-	K1 K2
CLASS_PSS_L07_T03	budget	SA:35 CONDITION C1; SB:47; RC:65 HOLDS; FC:87 CONDITION C2	R (use M: SA:27-32)	CONDITION	-	K1 K2
CLASS_PSS_L07_T15	budget	SC:38; SB:47; RC:66 HOLDS; FC:88 CONDITION C2	R (use M: SC:29-32)	CONDITION	-	K1 K2
CLASS_PSS_L08_T03	budget	SA:35 CONDITION C1; SB:47; RC:65 HOLDS; FC:89 CONDITION C2	R (use M: SA:27-32)	CONDITION	-	K1 K2
CLASS_PSS_L08_T15	budget	SC:38; SB:47; RC:66 HOLDS; FC:90 CONDITION C2	R (use M: SC:29-32)	CONDITION	-	K1 K2
CLASS_PSS_L10_T03	budget	SA:35 CONDITION C1; SB:47; RC:65 HOLDS; FC:91 CONDITION C2	R (use M: SA:27-32)	CONDITION	-	K1 K2
CLASS_PSS_L10_T15	budget	SC:38; SB:47; RC:66 HOLDS; FC:92 CONDITION C2	R (use M: SC:29-32)	CONDITION	-	K1 K2
CLASS_PSS_L12_T03	budget	SA:35 CONDITION C1; SB:47; RC:65 HOLDS; FC:93 CONDITION C2	R (use M: SA:27-32)	CONDITION	-	K1 K2
CLASS_PSS_L12_T15	budget	SC:38; SB:47; RC:66 HOLDS; FC:94 CONDITION C2	R (use M: SC:29-32)	CONDITION	-	K1 K2
CLASS_PSS_L13_T03	budget	SA:35 CONDITION C1; SB:47; RC:65 HOLDS; FC:95 CONDITION C2	R (use M: SA:27-32)	CONDITION	-	K1 K2
CLASS_PSS_L13_T15	budget	SC:38; SB:47; RC:66 HOLDS; FC:96 CONDITION C2	R (use M: SC:29-32)	CONDITION	-	K1 K2
CLASS_PSS_L14_T03	budget	SA:35 CONDITION C1; SB:47; RC:65 HOLDS; FC:97 CONDITION C2	R (use M: SA:27-32)	CONDITION	-	K1 K2
CLASS_PSS_L14_T15	budget	SC:38; SB:47; RC:66 HOLDS; FC:98 CONDITION C2	R (use M: SC:29-32)	CONDITION	-	K1 K2
CLASS_PSS_L16_T03	budget	SA:35 CONDITION C1; SB:47; RC:65 HOLDS; FC:99 CONDITION C2	R (use M: SA:27-32)	CONDITION	-	K1 K2
CLASS_PSS_L16_T15	budget	SC:38; SB:47; RC:66 HOLDS; FC:100 CONDITION C2	R (use M: SC:29-32)	CONDITION	-	K1 K2
CLASS_PSW37_L11_T09	budget	SA:34 CONDITION C1; SB:47; RC:67 HOLDS; FC:101 CONDITION C2	R (use M: SA:24-26)	CONDITION	-	K1 K2
CLASS_PSW37_L11_T17	budget	SB:46 CONDITION C1; RC:68 HOLDS; FC:102 CONDITION C2	R (use M: SB:31-44)	CONDITION	-	K1 K2
CLASS_PS_L01_T09	budget	SA:33 CONDITION C1; SB:47; RC:67 HOLDS; FC:103 CONDITION C2	R (use M: SA:24-26)	CONDITION	-	K1 K2
CLASS_PS_L01_T17	budget	SB:46 CONDITION C1; RC:68 HOLDS; FC:104 CONDITION C2	R (use M: SB:31-44)	CONDITION	-	K1 K2
CLASS_PS_L02_T09	budget	SA:33 CONDITION C1; SB:47; RC:67 HOLDS; FC:105 CONDITION C2	R (use M: SA:24-26)	CONDITION	-	K1 K2
CLASS_PS_L02_T17	budget	SB:46 CONDITION C1; RC:68 HOLDS; FC:106 CONDITION C2	R (use M: SB:31-44)	CONDITION	-	K1 K2
CLASS_PS_L05_T09	budget	SA:33 CONDITION C1; SB:47; RC:67 HOLDS; FC:107 CONDITION C2	R (use M: SA:24-26)	CONDITION	-	K1 K2
CLASS_PS_L05_T17	budget	SB:46 CONDITION C1; RC:68 HOLDS; FC:108 CONDITION C2	R (use M: SB:31-44)	CONDITION	-	K1 K2
CLASS_PS_L06_T09	budget	SA:33 CONDITION C1; SB:47; RC:67 HOLDS; FC:109 CONDITION C2	R (use M: SA:24-26)	CONDITION	-	K1 K2
CLASS_PS_L06_T17_ENDm_H4T4	budget	SB:46 CONDITION C1; RC:69 HOLDS; FC:110 CONDITION C2	R (use M: SB:35)	CONDITION	-	K1 K2
CLASS_PS_L06_T17_ENDp_H4T4	budget	SB:46 CONDITION C1; RC:70 HOLDS; FC:111 CONDITION C2	R (use M: SB:36)	CONDITION	-	K1 K2
CLASS_PS_L07_T09	budget	SA:33 CONDITION C1; SB:47; RC:67 HOLDS; FC:112 CONDITION C2	R (use M: SA:24-26)	CONDITION	-	K1 K2
CLASS_PS_L07_T17	budget	SB:46 CONDITION C1; RC:68 HOLDS; FC:113 CONDITION C2	R (use M: SB:31-44)	CONDITION	-	K1 K2
CLASS_PS_L08_T09	budget	SA:33 CONDITION C1; SB:47; RC:67 HOLDS; FC:114 CONDITION C2	R (use M: SA:24-26)	CONDITION	-	K1 K2
CLASS_PS_L08_T17	budget	SB:46 CONDITION C1; RC:68 HOLDS; FC:115 CONDITION C2	R (use M: SB:31-44)	CONDITION	-	K1 K2
CLASS_PS_L10_T09	budget	SA:33 CONDITION C1; SB:47; RC:67 HOLDS; FC:116 CONDITION C2	R (use M: SA:24-26)	CONDITION	-	K1 K2
CLASS_PS_L10_T17	budget	SB:46 CONDITION C1; RC:68 HOLDS; FC:117 CONDITION C2	R (use M: SB:31-44)	CONDITION	-	K1 K2
CLASS_PS_L12_T09	budget	SA:33 CONDITION C1; SB:47; RC:67 HOLDS; FC:118 CONDITION C2	R (use M: SA:24-26)	CONDITION	-	K1 K2
CLASS_PS_L12_T17	budget	SB:46 CONDITION C1; RC:68 HOLDS; FC:119 CONDITION C2	R (use M: SB:31-44)	CONDITION	-	K1 K2
CLASS_PS_L13_T09	budget	SA:33 CONDITION C1; SB:47; RC:67 HOLDS; FC:120 CONDITION C2	R (use M: SA:24-26)	CONDITION	-	K1 K2
CLASS_PS_L13_T17	budget	SB:46 CONDITION C1; RC:68 HOLDS; FC:121 CONDITION C2	R (use M: SB:31-44)	CONDITION	-	K1 K2
CLASS_PS_L14_T09	budget	SA:33 CONDITION C1; SB:47; RC:67 HOLDS; FC:122 CONDITION C2	R (use M: SA:24-26)	CONDITION	-	K1 K2
CLASS_PS_L14_T17	budget	SB:46 CONDITION C1; RC:68 HOLDS; FC:123 CONDITION C2	R (use M: SB:31-44)	CONDITION	-	K1 K2
CLASS_PS_L16_T09	budget	SA:33 CONDITION C1; SB:47; RC:67 HOLDS; FC:124 CONDITION C2	R (use M: SA:24-26)	CONDITION	-	K1 K2
CLASS_PS_L16_T17	budget	SB:46 CONDITION C1; RC:68 HOLDS; FC:125 CONDITION C2	R (use M: SB:31-44)	CONDITION	-	K1 K2
BRANCH_JPA_L01	branch	SA:24 HOLDS given C1-C5; FC:126 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPA_L02	branch	SA:24 HOLDS given C1-C5; FC:127 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPA_L05	branch	SA:24 HOLDS given C1-C5; FC:128 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPA_L06	branch	SA:24 HOLDS given C1-C5; FC:129 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPA_L07	branch	SA:24 HOLDS given C1-C5; FC:130 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPA_L08	branch	SA:24 HOLDS given C1-C5; FC:131 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPA_L10	branch	SA:24 HOLDS given C1-C5; FC:132 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPA_L11	branch	SA:25 HOLDS given C1-C5; FC:133 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPA_L12	branch	SA:26 HOLDS given C1-C5; FC:134 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPA_L13	branch	SA:24 HOLDS given C1-C5; FC:135 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPA_L14	branch	SA:24 HOLDS given C1-C5; FC:136 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPA_L16	branch	SA:24 HOLDS given C1-C5; FC:137 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3m_L01	branch	SA:27 HOLDS given C1-C5; FC:138 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3p_L01	branch	SA:30 HOLDS given C1-C5; FC:139 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3m_L02	branch	SA:27 HOLDS given C1-C5; FC:140 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3p_L02	branch	SA:30 HOLDS given C1-C5; FC:141 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3m_L05	branch	SA:27 HOLDS given C1-C5; FC:142 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3p_L05	branch	SA:30 HOLDS given C1-C5; FC:143 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3m_L06	branch	SA:27 HOLDS given C1-C5; FC:144 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3p_L06	branch	SA:30 HOLDS given C1-C5; FC:145 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3m_L07	branch	SA:27 HOLDS given C1-C5; FC:146 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3p_L07	branch	SA:30 HOLDS given C1-C5; FC:147 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3m_L08	branch	SA:27 HOLDS given C1-C5; FC:148 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3p_L08	branch	SA:30 HOLDS given C1-C5; FC:149 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3m_L10	branch	SA:27 HOLDS given C1-C5; FC:150 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3p_L10	branch	SA:30 HOLDS given C1-C5; FC:151 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3m_L11	branch	SA:28 HOLDS given C1-C5; FC:152 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3p_L11	branch	SA:31 HOLDS given C1-C5; FC:153 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3m_L12	branch	SA:29 HOLDS given C1-C5; FC:154 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3p_L12	branch	SA:32 HOLDS given C1-C5; FC:155 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3m_L13	branch	SA:27 HOLDS given C1-C5; FC:156 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3p_L13	branch	SA:30 HOLDS given C1-C5; FC:157 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3m_L14	branch	SA:27 HOLDS given C1-C5; FC:158 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3p_L14	branch	SA:30 HOLDS given C1-C5; FC:159 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3m_L16	branch	SA:27 HOLDS given C1-C5; FC:160 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG3p_L16	branch	SA:30 HOLDS given C1-C5; FC:161 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17m_L01	branch	SB:31 CONDITION C1-C4; FC:162 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17p_L01	branch	SB:31 CONDITION C1-C4; FC:163 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17m_L02	branch	SB:32 CONDITION C1-C4; FC:164 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17p_L02	branch	SB:32 CONDITION C1-C4; FC:165 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17m_L05	branch	SB:33 CONDITION C1-C4; FC:166 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17p_L05	branch	SB:34 CONDITION C1-C4; FC:167 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17m_L06	branch	SB:35 CONDITION C1-C4; FC:168 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17p_L06	branch	SB:36 CONDITION C1-C4; FC:169 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17m_L07	branch	SB:37 CONDITION C1-C4; FC:170 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17p_L07	branch	SB:37 CONDITION C1-C4; FC:171 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17m_L08	branch	SB:38 CONDITION C1-C4; FC:172 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17p_L08	branch	SB:38 CONDITION C1-C4; FC:173 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17m_L10	branch	SB:39 CONDITION C1-C4; FC:174 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17p_L10	branch	SB:39 CONDITION C1-C4; FC:175 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17m_L11	branch	SB:40 CONDITION C1-C4; FC:176 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17p_L11	branch	SB:40 CONDITION C1-C4; FC:177 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17m_L12	branch	SB:41 CONDITION C1-C4; FC:178 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17p_L12	branch	SB:41 CONDITION C1-C4; FC:179 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17m_L13	branch	SB:42 CONDITION C1-C4; FC:180 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17p_L13	branch	SB:42 CONDITION C1-C4; FC:181 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17m_L14	branch	SB:43 CONDITION C1-C4; FC:182 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17p_L14	branch	SB:43 CONDITION C1-C4; FC:183 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17m_L16	branch	SB:44 CONDITION C1-C4; FC:184 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG17p_L16	branch	SB:44 CONDITION C1-C4; FC:185 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15m_L01	branch	SC:29 HOLDS under C-a to C-d; FC:186 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15p_L01	branch	SC:30 HOLDS under C-a to C-d; FC:187 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15m_L02	branch	SC:29 HOLDS under C-a to C-d; FC:188 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15p_L02	branch	SC:30 HOLDS under C-a to C-d; FC:189 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15m_L05	branch	SC:29 HOLDS under C-a to C-d; FC:190 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15p_L05	branch	SC:30 HOLDS under C-a to C-d; FC:191 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15m_L06	branch	SC:29 HOLDS under C-a to C-d; FC:192 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15p_L06	branch	SC:30 HOLDS under C-a to C-d; FC:193 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15m_L07	branch	SC:29 HOLDS under C-a to C-d; FC:194 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15p_L07	branch	SC:30 HOLDS under C-a to C-d; FC:195 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15m_L08	branch	SC:29 HOLDS under C-a to C-d; FC:196 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15p_L08	branch	SC:30 HOLDS under C-a to C-d; FC:197 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15m_L10	branch	SC:29 HOLDS under C-a to C-d; FC:198 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15p_L10	branch	SC:30 HOLDS under C-a to C-d; FC:199 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15m_L11	branch	SC:31 HOLDS under C-a to C-d; FC:200 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15p_L11	branch	SC:31 HOLDS under C-a to C-d; FC:201 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15m_L12	branch	SC:32 HOLDS under C-a to C-d; FC:202 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15p_L12	branch	SC:32 HOLDS under C-a to C-d; FC:203 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15m_L13	branch	SC:29 HOLDS under C-a to C-d; FC:204 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15p_L13	branch	SC:30 HOLDS under C-a to C-d; FC:205 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15m_L14	branch	SC:29 HOLDS under C-a to C-d; FC:206 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15p_L14	branch	SC:30 HOLDS under C-a to C-d; FC:207 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15m_L16	branch	SC:29 HOLDS under C-a to C-d; FC:208 HOLDS	M	HOLDS given premises	-	K1 K2
BRANCH_JPG15p_L16	branch	SC:30 HOLDS under C-a to C-d; FC:209 HOLDS	M	HOLDS given premises	-	K1 K2
LOCAL_JQ	root	LO:19 CONDITION; ADM:22; FC:210 CONDITION C3	R; checker M in part; tree arithmetic N in this round	CONDITION	EL: whole certificate rerun, both frozen checkers (bytes confirmed)	K3 K4
LOCAL_JG	root	LO:20 CONDITION; ADM:22; FC:211 CONDITION C3	R; checker M in part; tree arithmetic N	CONDITION	-	K3 K4
LOCAL_JPA	root	LO:21 CONDITION; ADM:22; FC:212 CONDITION C3	R; checker M in part; tree arithmetic N	CONDITION	-	K3 K4
LOCAL_JPWS	root	LO:22 CONDITION; ADM:22; FC:213 CONDITION C3	R; checker M in part; tree arithmetic N	CONDITION	-	K3 K4
LOCAL_JPW13	root	LO:23 CONDITION; ADM:22; FC:214 CONDITION C3	R; checker M in part; tree arithmetic N	CONDITION	-	K3 K4
LOCAL_JPG3m	root	LO:24 CONDITION; ADM:22; FC:215 CONDITION C3	R; checker M in part; tree arithmetic N	CONDITION	-	K3 K4
LOCAL_JPG3p	root	LO:25 CONDITION; ADM:22; FC:216 CONDITION C3	R; checker M in part; tree arithmetic N	CONDITION	-	K3 K4
LOCAL_JPG17m	root	LO:26 CONDITION; ADM:22; FC:217 CONDITION C3	R; checker M in part; tree arithmetic N	CONDITION	-	K3 K4
LOCAL_JPG17p	root	LO:27 CONDITION; ADM:22; FC:218 CONDITION C3	R; checker M in part; tree arithmetic N	CONDITION	-	K3 K4
LOCAL_JPG15m	root	LO:28 CONDITION; ADM:22; FC:219 CONDITION C3	R; checker M in part; tree arithmetic N	CONDITION	-	K3 K4
LOCAL_JPG15p	root	LO:29 CONDITION; ADM:22; FC:220 CONDITION C3	R; checker M in part; tree arithmetic: 21 of 23 nodes rerun (LO:29), else N	CONDITION	-	K3 K4
```

