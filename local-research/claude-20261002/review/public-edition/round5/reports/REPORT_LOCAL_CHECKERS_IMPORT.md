Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line.

REPORT of a fresh reader (local half: checker soundness, certificate import, side transfer), 10 Oct 2026.

VERDICT: no acceptance of a wrong object found; all three premises hold, with one condition (the EMPTY statement needs the post-check, not a bare PASS) and one bookkeeping mismatch in the import (four regions: the packet pins different record and review files than JOIN_ROOTS names).

PACKET.json sha256 begins 11ef58b1 (11ef58b16e72988a): as expected. Checkers found by name: wxcheck_v30.py cf8db52bfa1cc565, wxcheck2_v30.js 97210adf74a3ebed; the packet's copies in proof_sources have the same hashes.

## 1. What a tree file is (my words)
- A tree file is JSON lines: a header (reference-packing hash, Sref, root id, window, tube, optional `labels` and `S_floor`), then one node per line.
- A node is a rational cell: a box for every chart coordinate xi_ik, an arc per square (centre rotation and two end rotations with positive cosine), a side interval and a list of assumptions. F(N) is the set of feasible configurations in that cell.
- A leaf asserts one of two things. INFEASIBLE means F(N) is empty; TERMINAL means the final store lies in the tube.
- INFEASIBLE has three forms: an accepted `0` step (exact identity 0 = Rem + sum lambda_k * product of at most 3 facts, with the interval lower bound L of Rem satisfying L >= value > 0); an EMPTY store (contradictory bounds); or all 8 separating options of one pair excluded.
- At a split the checker verifies that the split point lies in the parent's final interval or arc, that every unlisted option is excluded (option split), and that each child's box, arcs and side interval contain the parent's final store (the split coordinate: the closed half).
- Tree conditions: unique ids, each non-root node in exactly one children list, parent fields agree, all nodes reachable, all nodes closed.
- Root conditions: parent null, no assumptions, S_lo <= S_floor, S_hi >= Sref, root contains the header window.
- Accepted statement, SPEC section 7: "THEOREM. If all conditions hold, every feasible configuration with S_floor <= S <= Sref in the window lies in the tube."
- The root-region form the proof uses, notes of 18:38: "If a certificate satisfies all conditions of section 7 and NO node of it is closed as TERMINAL ... then F(root) is empty" and "NO feasible configuration with S <= Sref has its positions and directions in the root's box and arcs (it would be feasible for the side Sref, hence in F(root))."

## 2. Python checker source, per item (line numbers of wxcheck_v30.py)
- Leaf by `0` step: HOLDS WITH CONDITION. Lines 2286-2324 (sense must be "lo", L >= value > 0 at 2309-2315; negative multiplier only with a circ fact, 2295; 1 to 3 facts, 2297; pol only with circ, 2299; guard rule 1880-1896). L is exact: integer-scaled remainder 2038-2059, sum of min(r*lo, r*hi) 2061-2079, monomial intervals 2002-2011, interval product 326-328. Fact polynomials I read have the right sign: box, side, cut, circ, arc, tangent, wall (lo := X, hi := S - X, line 1367), option corner (1370-1383), sq, pol, ind (1899-1999, 1701-1725). Condition: I did not read the parallel-class facts (4.6), wall-support facts (4.8), class forms, form_poly, or the centred bounding rule (2149-2260); the JQ leaf uses the centred rule, and both checkers gave the same L on it (0.006945012101), which is a cross-check, not a reading.
- Leaf by EMPTY store: HOLDS. 1631-1661, 2551-2553, 2562-2563. A new store entry is accepted only if weaker than the old one or implied by a certified value of this round (2333-2400, 2277-2283); steps of a round use the store at its start (2415-2432).
- Leaf by pair closure: HOLDS. 2567-2580. Exclusion is strict, U < 1/2 + h_lo (1682-1694); h_lo falls back to 1/2 (1664-1680), the safe side.
- Terminal leaf: HOLDS. 2441-2463, 2582-2590: tlo <= lo and hi <= thi; cosine > 0; |sin| <= aT - aT^3/6; an EMPTY store may not be closed as terminal or split.
- Box split: HOLDS. lo <= m <= hi (2472-2476); child 1 must contain [lo, m], child 2 [m, hi] (2677-2680, 2693-2699). Both halves are closed and share m, so no sliver is lost.
- Arc split: HOLDS. cos M > 0, sin P^- <= sin M <= sin P^+ (2477-2483); containment after re-centring with both cosines > 0 (2613-2621, 2700-2705).
- Option split: HOLDS. Every unlisted option excluded on the final store (2484-2488); child l assumes Lst[l] (2685-2686, 2691).
- Sign split: HOLDS. +1 then -1, both closed (2687-2688).
- Child side interval contains the parent's (2706); child count and distinct ids (1107-1111); tree conditions (2737-2821): HOLDS.
- Root: HOLDS for the header-window theorem (2624-2654). HOLDS WITH CONDITION for the root-region statements: "root node = named region" and "terminal leaves = 0" are checked by acceptance/h_report30.py lines 395-446 and 338-342 (0314aa1f8f742cd7, the same bytes as the packet's local_acceptance_postcheck.py), not by the checker. PROOF_TEXT section 7 says this correctly.
- Can the file weaken the check: HOLDS (nothing found). Unknown keys reject (1118, 1211-1212); the header has only `labels` (16 or 17) and `S_floor` (4 <= S_floor <= Sref) as options (1230-1237); no floats, no duplicate keys (141-151); numbers are exact fractions (158-169); every rotation must satisfy g^2 + s^2 = 1 exactly (296-303). A step's `centre` only selects the second bounding rule.
- Rounding: none in the paths I read; floats appear only in messages (2327-2330).
- Command line (not the file): HOLDS WITH CONDITION. PASS comes only from a full run (3027-3037, 3122-3123); `--node` and `--keep-going` cannot give PASS. `--packing` with `--no-packing-pin` (3097-3102) would let another reference file in, so the runs of record must use the pinned file. I counted hash occurrences in the eleven logs but did not read their command lines.
- JUDGEMENT: a split or terminal node whose rounds contain an accepted `0` step keeps its declared kind (2552-2596). Harmless: the node is empty anyway.

## 3. Side transfer S <= R
- Carrying sentence, SPEC section 11: "a configuration that is feasible for a side S <= Sref is feasible for the side Sref (condition (F1) only gets weaker, (F2) does not mention S), and neither the window nor the tube nor the reference data mention S."
- PROOF_TEXT section 7: "Keep all squares fixed in the corner-at-origin chart and enlarge only the containing box from [0,S]^2 to [0,R]^2. Pair separations are unchanged, and the right/top wall constraints become weaker. All reference positions, root intervals and arcs are fixed data independent of S."
- JUDGEMENT: HOLDS, the argument is complete. It does not need each leaf fact to be monotone in S: the tree is a statement about configurations feasible at side exactly Sref, and the only step is "feasible at S implies feasible at Sref with the same poses". That is true from (F1) and (F2): the left and bottom walls are x >= 0, y >= 0 with no S, the right and top walls only relax.
- JUDGEMENT: the chart is S-free in the code too: q_i = p_i + xi_i1 e_i1 + xi_i2 e_i2 with p, e from the reference file (1266-1270); S enters only as a variable in side facts and in the right/top wall facts.
- Checked: all eleven region files and EXPECT files have S = [Sref, Sref], S_floor = Sref, labels 17. The checker enforces S_lo <= S_floor (control K7), so the step from "S = Sref" to "S <= Sref" is made by the SPEC text, not by a program. That is where it belongs.
- JUDGEMENT, limit of the transfer: it says nothing about whether a packing of side L has its poses in a root. A square flush at the right wall of [0,L]^2 has xi = L - Sref + eps, which the roots allow only because L < Sref - eps. That belongs to ROOT_ADMISSION and the frame note of 08:51; I did not re-verify the wall ends of the eleven files (the earlier reviewer did for nine).

## 4. Import
- Root (region file) hashes: all eleven rows of "Whole-root obligations" in MANIFEST_TABLES.md agree with JOIN_ROOTS.md and with the files on disk (full 64 hex computed). No mismatch.
- Certificate hashes: all eleven from JOIN_ROOTS occur in the packet. All eleven acceptance logs contain the certificate hash, both frozen checker hashes, "RESULT: ACCEPTED", the ROOT REGION line and no FAIL. The ten EMPTY logs have "number of terminal leaves is 0 (expected 0)"; EXPECT_JG_v2 has no terminal count, consistent with JG being a tube statement.
- MISMATCH (bookkeeping, four regions): for JPWS_v4, JPW13_v2x, JPG3p_v5 and JPG15m_v5 the record and review hashes of JOIN_ROOTS occur NOWHERE in the packet. The packet (proof_sources/e903ba53..._ACCEPTED_UPDATES_20261010_1712.json) pins other files: third-order-20261010/local-region-audits/<region>/LEAD_RECORD_SNAPSHOT.md and Codex's own REVIEW.md.

| region | JOIN_ROOTS record / review | packet record / review |
|---|---|---|
| JPWS_v4 | af742507a1553a11 / 0a094486675bef10 | 38f1160bebfe / 6166f1da0e71 |
| JPW13_v2x | 0f7d2cb3f0cb3d10 / 2de8ae1b9d0c7ad1 | 7ff9ee9ceaae / bb99271434d4 |
| JPG3p_v5 | 16226ebd1dca325b / 9fa9013da56b4a18 | 5bf850e033fa / c2da862e1f57 |
| JPG15m_v5 | 33b20db1bc7f344e / 77da7db7f81007c7 | 473ec02ea7e2 / 509dad5c0bd2 |

  The snapshots are dated minutes after acceptance and before the PROVED time of JOIN_ROOTS (JPG15m 10:10 against 10:15; JPG3p 12:48 against 13:04; JPW13 15:00 against 15:21; JPWS 17:09 against 17:11). Root, EXPECT, certificate and acceptance-log hashes of these four agree with disk.
- JUDGEMENT: not a mathematical gap, but the premise's "independent record review" for these four is Codex's import review of an early snapshot, not the lead-side reviews of batches 3 to 6 that JOIN_ROOTS calls the reviews of record. To close: add the four final RECORD_E*.md and the four batch reviews to the packet's proof list.
- For JQ, JPA, JPG3m, JPG17m, JPG17p, JPG15p and JG the JOIN_ROOTS record and review hashes do occur in the packet.

## 5. Negative controls
Object: the JQ v1 certificate (one node, one leaf, 48,209 terms, centred `0` step, value 0.0062505, L 0.0069450), copied to scratch; 6.5 MB compressed, 26.8 MB plain. The frozen Python checker on the copy: PASS in 30.6 s, 427 MB, certificate hash 0b2a8ff8... reproduced. The Node checker on the copy: PASS in 6.4 s, 729 MB. Reference file: a scratch copy of upper-packing-certificate.json (24e296f5995abc94), pin left on.

Python, each on its own copy:
| id | corruption | result |
|---|---|---|
| B0 | re-serialised, unchanged content | PASS |
| K1 | one multiplier (term 100, fact box:5:2:hi, 9.9e-7) times 3 | ACCEPTED, see below |
| K1b | the same multiplier times 10^6 | REJECT: L = -0.1646 |
| K2 | root box upper end of xi:1:1 wider by 2e-6 | REJECT: "new upper end of xi:1:1 is not implied" |
| K2b | the same end wider by 1/10 | REJECT: L = -5.18 |
| K3 | leaf kind swapped to terminal | REJECT: "store interval of xi:1:1 is not inside the tube" |
| K4 | sense of the `0` step set to "hi" | REJECT |
| K5 | claimed value set to 1 | REJECT: needs L >= value |
| K6 | one multiplier negated, no circ fact | REJECT |
| K7 | header S_floor set to 4, root stays [Sref, Sref] | REJECT: "the root needs S_lo <= 4" |
| K8 | header window box 2e-6 beyond the root | REJECT: root box does not contain the window |
| K9 | header window radius of label 1 from 1873/25000 to 1874/25000 (root arc sine 0.0749295) | REJECT: root arc does not contain the window arc |
| K10 | extra key "trusted": true in the node | REJECT: unknown key |

Split controls on a tree I built from the same leaf (root "R" with no rounds, box split of xi:1:1 at 1/10, two children that are copies of the leaf):
| id | corruption | result |
|---|---|---|
| T0 | none | PASS, 3 nodes |
| T1 | one child of the split deleted | REJECT: "lists the child 'c2', which does not exist" |
| T2 | parent 2e-9 wider than child 2 at the top (a sliver) | REJECT: child interval does not contain the required interval |
| T3 | option split of pair 7-10 listing one wrong option | REJECT: "omits option (10, 7, 'b', 1), which is not excluded" |
| T4 | box split with one child id | REJECT: needs 2 children |
| T5 | arc split of square 1, parent's upper arc end 2e-7 beyond child 2 | REJECT: child arc does not contain the required arc |

Node checker repeats: B0 PASS, original gz copy PASS, K1 PASS; K5, T1, T2, T3, T5 all FAIL with the matching reason (K5: "claimed value 1 > L = 0.006945012100770656").

K1, the one accepted corruption, exactly: tripling that multiplier leaves L exactly unchanged (difference of the two exact fractions is 0), and both checkers accept. JUDGEMENT: not a defect. The corrupted file is another valid certificate: the multiplier is still nonnegative and the checker recomputed L >= value. L does not move because the remainder's coefficient on that coordinate is negative, so the bound is taken at the end where the fact hi - xi vanishes. K1b shows the arithmetic does react.

JUDGEMENT on K2: the rejection came from the round's proposed store, not from the leaf's inequality. A wider root with a consistently rewritten store might pass if the slack allows; that would be a true statement about a larger region and is why the root-region post-check, not the PASS, binds the statement.

## Files relied on (sha256, first 16 hex)
PACKET.json 11ef58b16e72988a; GLOBAL_PREMISES.json b45518bb2cb0fabf; PROOF_TEXT.md 61be63e55ba24491; MANIFEST_TABLES.md 5747ad78779f1217; local_spec_notes 4f8d1e8fa5d20bea; SIDE_CAP_TRANSFER 03bd024468419832; fresh_local_review cf54d5dc37c004e5; SPEC_v3.0.md 0a6dfc2ae10ed6f3; wxcheck_v30.py cf8db52bfa1cc565; wxcheck2_v30.js 97210adf74a3ebed; h_report30.py 0314aa1f8f742cd7; JOIN_ROOTS.md e8261fd666c4a39b; ACCEPTED_UPDATES_20261010_1712.json e903ba53b99cee2d; JQ certificate 0b2a8ff8a3f9e12d (plain stream 3d4606d12b2305b8); EXPECT_JQ_v1.json cbd56dcb45a945f4; ACCEPT_JQ_v1_jQTwn0.log d04fa0f0f18576a9; upper-packing-certificate.json 24e296f5995abc94; region files JQ f4d1607eb4378487, JPWS 7d32a55bc2b08005, JPW13 e1a489e1f0d04ec0, JPA adcf0d1bdc02b8ea, JPG3m 1e2a3b429193a69f, JPG3p c4287958b08fe4fc, JPG17m 18550e414d3f5057, JPG17p 11b68ec1eb4aa790, JPG15m f6495dc60d07a4fa, JPG15p 6c9ad4887e868fe0, JG f635af684d0f81d3.

## What I did not do
- Did not read in the Python checker: parallel-class facts and their preconditions (4.6), wall-support facts (4.8), class and custom forms, form_poly, the centred bounding rule, the Reference class, parse_round and parse_fact_name. Did not read the Node checker's source at all; it was only run.
- Did not run any of the ten larger certificates (all above 50 MB or not located), so no control on a real multi-node tree; the split controls use my synthetic three-node tree.
- No control on a relative-arc store entry, a cut, an `ind` declaration (the JQ leaf has none) or a sign split.
- Did not read SPEC sections 3 to 5 and 10 line by line, the reviews REVIEW_30*.md, the eleven records or their reviews; did not check the acceptance logs' command lines or accept_tree30.sh.
- Did not re-verify the wall ends of the eleven root files or anything of ROOT_ADMISSION.

Scratch folder <reviewer scratch>/ holds the gz copy of the JQ certificate, the two checker copies, pack.json, the four generator scripts mk1.py to mk4.py and seven small report files.

