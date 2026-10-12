Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line.

HOLDS WITH CONDITIONS: (C1) one unchanged sentence (line 72) still writes the frame-pair count in the high-first form; it is true only because q = 0, which the same paragraph states (F1). (C2) The H6 id map is a binding by name, not by content, for four ids (F2). (C3) L2-F1: the rerun logs with the pinned post-check are not yet pinned. (C4) FC-Q1,2,4 are not answered in BD / BF-BE (audit lead's coverage table). (C5) I did not read pilot.py; for the meaning of norm_upper, turn, dot and box_interval I rely on TERMINAL-2.

No changed or added line in BD or BF-BE states anything false. No change weakens a quantifier or drops a hypothesis that the selected route uses. No statement in the new text needs the high-first score.


Disclosure: I read three entries of <message file to the author>, BF, BE and BD (lines 47 to 171), only AFTER all verdicts below were formed, to check completeness. I opened no <author reply> file.

## Findings, most serious first

**F1 (TEXT, unchanged line 72 of PROOF_TEXT_CORRECTED.md, section 4).** "these two accepted pair statements give 17+m/4-(t-q)/8<137/8", with q the number of parents in both the high class and the low union.
- That is the high-first count. With the printed minimum score, a parent in both scores 7/8, so the receipt gives 17+(m-q)/4-t/8 < 137/8.
- The two forms agree exactly when q = 0. Line 62 states the strict disjointness of the high and low unions, and the last sentences of the paragraph say "The verified disjointness gives q=0".
- The sentence "each low union contains at least two parents" comes before q = 0 is stated. Without q = 0 the minimum score gives only t >= 2(m-q).
- JUDGEMENT: true as used, not a gap. It is the one place I found where the wording still has the high-first form.
- Fix: state q = 0 first, or write 17+m/4-t/8.

**F2 (record, COMPLETE_DAG.json and H6_ID_MAP.tsv).** "Each of the 210 obligations bound exactly once" is true (my script). The binding is by name.
- H6_PREMISES.json has 228 id-to-id dependency pairs: 206 are direct edges of the bound node, 2 are ancestors, 20 are NOT ancestors of the bound node.
- The 20: WALL_PARTITION (7: FRAME_ASSIGNMENT, L_3, L_15, L_17, L_4, CHARGE_SEMANTICS, COARSE_LOOSE_CAPACITY), ROOT_ADMISSION (9), SELECTOR_LOGIC (2), WALL_CONTRADICTION (1: LOCAL_JG), SL11_T020 (1: FRAME_ASSIGNMENT).
- The packet claims of WALL_PARTITION and ROOT_ADMISSION both contain "The entire coarse loose regions 3,15,17 have capacity one ... Fully gated JG therefore has no occupant of any C escape slot X". The bound nodes LEMMA_WALL_PARTITION and LEMMA_ROOT_ADMISSION are pure conditional lemmas and do not claim this. That content sits in OFFWALL_LOOSE_ROLES, JG_ESCAPE_EMPTY and the ADMIT_ nodes.
- For WALL_CONTRADICTION and SL11_T020 the users of the bound node have every dropped premise among their ancestors (script). All dropped premises are ancestors of FINAL_OPTIMALITY.
- JUDGEMENT: no gap. The new sentence at line 98 says this for coarse capacity only.
- Fix: one sentence in h6_id_convention naming the ids whose bound node is the pure part and where the applied part sits.

**F3 (citations, CLASS_ROW_LEMMA.md lines 36 and 46).** The statements are true; two source ranges are missing from SOURCES.json.
- Link 1 cites exact_classes.py 198-224 only. That is the fixed / mirror shape. For the orbit file (FRAME_MARKER) weights and budget are exact_general.py 22-29, 46-47. The proof text line 58 cites them; the lemma does not.
- Link 2 says "The validated feature potential ... invariant under the used symmetry". The validating code is check_mirror (exact_classes.py 228 ff., called at 288-289) and the orbit test of exact_general.py 32-44. Neither is in the cited ranges. REVIEW.md paragraph 13 states the fact.
- Link 3 cites RESTRICTED_CHECKER.md 279-288 for the limit step. Those lines take the core at a nearby generic centre, with no limit. The limiting-core version is REVIEW.md paragraph 17, which is also cited. Both versions are valid.
- JUDGEMENT: citation precision only.

**F4 (record, node LEMMA_CHARGE_SEMANTICS).** The new claim text no longer contains "requires stable source/input execution or the reviewed repaired worker binding" nor "the printed complete statement, literal class frame and certificate ratio must agree". It now says "validated complete authentic exact row verification" and "slice authenticity and concrete byte-alias transport remain separate premises". The worker-binding review stays in the node's files; the side and frame agreement stays in text line 52. JUDGEMENT: not weaker in substance.

**F5 (BD, note).** check_bindings.py tests the tangent guard only at e = 1/10. The inequality holds on the whole interval: 1/(1-e^2/2) <= 1+e^2 is equivalent to e^2 <= 1. The hypothesis "q <= 1/10" at line 25 is not needed by the derivation, only |eps| <= q and |eps| <= 1/10; the code enforces the latter at uniform.py line 96.

**F6 (BE, note on E-F7).** The integrality source given is the Python validation. The Node checker's own validation is not cited. Every counted row has a Python receipt on the same certificate hash, so the sentence holds.

## Item 1. Proof text

- Supplied PROOF_TEXT_BE.diff applied to a scratch copy of the BC text (dc0d6e7b) gives exactly the new text (c3d6692c). My own diff has the same added and removed lines; only one blank line in the first hunk is placed differently.
- Ten changed ranges: 1, 3, 52, 58, 64, 98, 112, 118, 194, and new 203-210. Nothing else changed.

| line | answers | verdict | basis |
|---|---|---|---|
| 1, 3 title, header | none | HOLDS | labels; packet hash quoted correctly |
| 52 | E-F6 | HOLDS | "For every packing of seventeen unit squares in the side-C square of the declared frame" is restored; "Each physical parent is counted once" added. The lemma gives it for every finite family. |
| 58 | E-F7 | HOLDS | exact_classes.py 202: `type(w) is int and w >= 0`; 207: integer coefficients > 0; 219: integer threshold; 222-224: budget equality and 2^50 bound. exact_general.py 23 and 29: integer weights >= 0; 46-47: budget = point weights plus feature capacities. Both hashes equal BE_SOURCE_PINS.json. |
| 64 | E-F4 | HOLDS | full bundle path exists; sha 7f6b2347... recomputed |
| 98 | E-F1 | HOLDS | sole user of LEMMA_COARSE_LOOSE_CAPACITY in the graph is JG_ESCAPE_EMPTY. JUDGEMENT: partition and admission use the small slots S_k (diameter below 1) and only the inclusion of S17 in coarse17; whole-region capacity is needed only for the escape slots X (line 102). See F2. |
| 112 | E-F3 | HOLDS | my census of SELECTED_ORIGINAL_MAP.json: 31 PS, 44 PSS, 7 PSW37 / PSSW37 (label 11), 2 END; no PM, no PT |
| 118 | E-F3 | HOLDS | consistent with lines 102 and 114 |
| 194 | E-F2 | HOLDS | 100 / 12 / 98 verified; edges unchanged. Not said in the sentence: two nodes gained file pins. |
| 203-210 | E-F5, E-NA, CO-c1, UX-F1, L2 | HOLDS | each sentence checked against its file (items 5 and 6 below) |

Minimum score. Read sections 3, 4 and the KEY_W paragraph in full.
- Bound 20 and 23: target and contextual lows empty, so every score is 1 or 4. Minimum score suffices.
- Frame pairs: see F1.
- 0917: 17+h/4-N(V)/8 with disjoint unions; correct for the minimum score.
- Marker: 17-N(E).

## Item 2. CLASS_ROW_LEMMA.md

JUDGEMENT: the statement is exactly what a PASS row gives, and the all-row conclusion is the one CHARGE-CORE derived, for tau instead of psi (weaker). No place is stronger than CHARGE-CORE section (2).
- Capacity: RESTRICTED_CHECKER.md 251-255 is R1 and says it. Code 198-224 read.
- Row validity: 257-266 is R2 and says it. Code 298-313: checks at both ends, margin > 0, envelope, cursor = 1 or cursor^2 + 2 cursor > 1 (beyond tan(pi/8)).
- R >= tau, my own derivation.
  - If a high class meets the closed product, R is the largest meeting high threshold, above 1, and at least every containing high threshold.
  - If none meets, no high class contains p, every accepted low contains p, so the least accepted low is at least the least containing threshold.
  - If none is accepted, R = 1 and tau <= 1.
  - Classes of threshold exactly 1 have kind 0 and fall to the default; safe.
  - Code 316-320 and 446-476 implement this order (high by decreasing threshold, then low by increasing, first claim wins, pieces must partition the slab).
  - HIGH_FIRST_REVIEW.md line 13 and REVIEW.md paragraphs 9-11 say the same.
- Strictness: line 293 `budget_units * b.denominator < b.numerator * minimum_units` is the only strict test. Line 489 is the weak cell test in integer cross-products. minimum_units is an integer > 0 (exact_restricted.py 168).
- The lemma states authenticity and exact arithmetic as hypotheses. CHARGE-CORE's conditions C2 to C4 (sampled sweep test, Node not executed, orbit shape not brute-forced) are not removed by it and it does not claim so.

## Item 3. Graph

- 328 nodes; same node set and order as BC (e8a786a7); 1537 edges identical; depends_on lists identical including order.
- Acyclic; single sink FINAL_OPTIMALITY; every node an ancestor of it; no dangling edge.
- 210 ids of H6_PREMISES.json equal H6_COVERAGE.tsv; each bound exactly once; none invented; 100 literal, 12 LEMMA_, 98 BUDGET_. Top-level map, tsv and node fields agree.
- All differences from BC: field h6_obligation_id on 210 nodes; claim of LEMMA_CHARGE_SEMANTICS (now minimum score, see F4); three file pins added to LEMMA_CHARGE_SEMANTICS (BE_SOURCE_PINS, CLASS_ROW_LEMMA, SOURCES) and three to LEMMA_ROOT_ADMISSION (ADMISSION_EVIDENCE, ARC_MARGIN_UNITS, LABEL11_EXECUTED_ARCS), all six hashes correct, none removed; six new top-level keys.
- "high-first" or "psi" now occurs only in LEMMA_CHARGE_SEMANTICS, as "does not require".

## Item 4. BD

(i) Parallel rows. Derived by me line by line.
- Owner i gives cos(e) X_m - sin(eps) tau_m >= cos^2 e + sin e cos e; owner j the same with + sin(eps). The support of the other square is (cos 2e + sin 2e)/2. So the disjunction gives BD line 33.
- Lines 38-39 follow from cos e >= 1 - e^2/2, sin e >= e - e^3/6, tan e <= e + e^3 (proved for 0 <= e <= 1).
- Line 48: Taylor on f(s) = R(s)n.d_w with |f''| <= D, plus |R(mu)n - n| <= |mu| on delta_h. Line 49 likewise.
- The sum is exactly E = uniform.py line 251.
- Expanding mu tau' + s eps (1 - sigma tau') gives omega_i: tau0/2 - s kappa0 and tauw (1 + s sigma)/2; omega_j: tau0/2 + s kappa0 and tauw (1 - s sigma)/2. These are lines 254-259 exactly, both signs.
- Guards: two survivors, different owners, same n (227); closed sign cases taulo >= 0 or tauhi <= 0, else omitted (232-238); taumax >= 1 omitted (240); e = 0 needs no division.
- D bounds |d + slider part| and dr bounds |delta_h| as maxima over the box (161-162, 197-198), m and q as radii (246-250).
- Agrees with TERMINAL-2 section (2) PART 1, which uses the sharper 0.335.

(ii) Scope paragraph (lines 71-75) equals TERMINAL-2 F2 and TERMINAL (c), (e): squares 9, 11, 13; square 2 and its right wall; square 8 and the top wall; per-label affine maps; no square 4. The sixteen-square THEOREM.md statement and its part "2. The side and reference-transfer guards are still physical" say the same.

(iii) Record.
- All 31 pins of BINDINGS.json match the disk.
- entry-producer/PROOF.md has "## Exact transfer" at line 52.
- PRUNING.json root_transfer.core_upper = 1/200 + 4.319e-17 < 501/100000 (exact fraction); nonnegative_root_a_uses_actual_right_wall is true.
- entry-review/REVIEW.md line 7 confirms both; check_transfer.py line 96 asserts the bound.
- The four superseding reviews open with "accepted". The stale strings quoted in BD are in the files as quoted.

## Items 5 and 6

- E-F5: the five answer files have full hashes in ADMISSION_EVIDENCE.json; all nine pins match the disk; no "<author reply>" remains in STATUS_AND_SOURCE_NOTES.md (diff against BB: 7 changed ranges, all of this kind, plus note 9).
- CO-c1: with t = 1430271/5000000 and the given reference and root end, exact fractions give the relative tan-half difference and the sine exactly as stored, for all seven roots; floats 2.573874566843636e-13 and 5.123456352621736e-13; ratio 1.99056 = 2(1+t r)/((1+t^2)(1+r^2)). Same margin in two units. The root end string is in the root file.
- UNUSED_SOURCE_SCOPE.json and UPPER-EXACT agree: same two hashes (e268531d, 1a6c91a8), same three instance folders, not load-bearing.
- L2-F1: my diff of h_report30_v1_1c01dda7.py (1c01dda7...) against h_report30.py (0314aa1f...) has the same body as H_REPORT.diff: one line replaced (the known-key set gains "root_region"), 107 lines added, nothing else removed. Without a root_region key the new code prints one line and tests nothing more. No check removed.
- L2-Q2: JQ v1 is f4d1607e..., present in PACKET.json, THEOREM_MANIFEST.json, H6_PREMISES.json and EXACT_ENDPOINT_AND_CASES.json; the v2 hash is in no packet file. The only numerical difference is label 9's box end -104437/10^6 (v1) against -124437/10^6 (v2); arcs, side and terminal equal. v2 lies in v1.
- L2-Q4: first gzip lines read by me. Header hashes b0a15298... and 8e00a16c... equal BF_CHECKS.json. JG terminal equals G20S window for all sixteen labels, every box end and alpha; Sref and packing hash equal; label 4 has JG's own root box and alpha 1.
- UX-F1: the endpoint subtree of 3417d4fa (frozen-manuscript-20261010_1450) and a08363c6 (packet) is equal. The other changes are exactly five: sources.fresh_join_review added; excluded branch REMOVED_HIGH9 added; JPA predicate t9 < 1 became t9 <= 44941/100000; offwall_keyw_direction_interval added; case_repair added. DIRECT_UPPER_IMPORT.json still carries the old pin, by design.

## Item 7. RC-Q1

The JG tube statement is made in the chart of SPEC_v3.0 sections 0 and 1.
- Container [0,S]^2 with a corner at the origin; rational reference centres of the packing file 24e296f5 with p13 corrected; xi_ik = e_ik.(q_i - p_i).
- The packing handed over is the normalized one: translated by ((L-S0)/2, (L-S0)/2) into [0,L]^2 (text section 2).
- JG is proved with side interval [R,R]. It applies to these poses by enlarging the box from [0,L]^2 to [0,R]^2 with the poses fixed (SPEC section 11, text lines 158-160). There is no translation.
- The tube constrains the same unchanged poses. G20S, HW and the sixteen-square theorem are stated in the same chart with actual container [0,S]^2, S = L (composition "Statement"; THEOREM.md: "No fixed-U recentering is implicit").

The capture and admission side uses a different chart, F_U, concentric at (U/2, U/2).
- The two differ by the single fixed translation (U-L)/2 in both coordinates.
- It is stated three times: section 2 (p + (L-S0)/2 + (U-L)/2 = p + (U-S0)/2), section 7 (xi = e.(c - (U-L)(1,1)/2 - p_i), and "The capture-to-root chart remains c-(U-L)(1,1)/2 with no additional shift"), and the frame field of every root file ("A class-frame point c corresponds to c - (U - S*)/2").

Agrees with REPORT_TEXT lines 61-65 and REPORT_TERMINAL (a), (c), (d). JUDGEMENT: I found no step that needs a translation not stated. The only other chart change is the raw-to-root reference change inside the sixteen-square theorem, which is the stated "Exact transfer".

## One line per item

- E-F1: CLOSED (sentence corrected; see F2).
- E-F2: CLOSED (see F2, F4).
- E-F3: CLOSED.
- E-F4: CLOSED.
- E-F5: CLOSED.
- E-F6: CLOSED.
- E-F7: CLOSED (see F6).
- E-NA: B-F5 CLOSED (two README addenda pinned and cited); R-F5 overlap CLOSED (RECEIPTS F5: none in 98 folders); FC-Q1,2,4 STILL OPEN (not in BD / BF-BE; coverage table).
- TM2-F1: CLOSED.
- TM2-F2: CLOSED.
- TM2-F3: CLOSED.
- CC-F2: CLOSED (see F3).
- UX-F1: CLOSED.
- L2-F1: file identified, CLOSED; STILL OPEN for the pin of the rerun logs (author: "not yet handed over"; <message file to the author> has a newer entry BG at 07:18 that I did not read).
- L2-Q2: CLOSED.
- L2-Q4: CLOSED.
- CO-c1: CLOSED.
- RC-Q1: CLOSED (item 7).

## Hashes at the start and at the end of the review (first 16 hex)

No file changed. One file is new: BF-BE/ADDENDUM.json 20874fb2a7bd9be9 (07:06). Its 28 pins match the disk, and its file list equals what I read.

| file | start = end |
|---|---|
| BD/ADDENDUM.json | 2e05c2e9b1581b27 |
| BD/BINDINGS.json | 4ddb7c670170e377 |
| BD/FINITE_REMAINDERS_AND_SCOPE.md | 189f47f7d9a512f7 |
| BD/check_bindings.py | 32f3ef643a1882cd |
| BF-BE/ADMISSION_EVIDENCE.json | feaa578ea65777e2 |
| BF-BE/ARC_MARGIN_UNITS.json | 7b38bcc4551bc429 |
| BF-BE/BE_ANSWERS.md | b86aa2e23686270c |
| BF-BE/BE_CHECKS.json | 4bdd7a0964186c7a |
| BF-BE/BE_SOURCE_PINS.json | 5689c90c0deb6a07 |
| BF-BE/BF_ANSWERS.md | 6dee18a3a680b670 |
| BF-BE/BF_CHECKS.json | 4565e7259095c282 |
| BF-BE/CLASS_ROW_LEMMA.md | 533e04f47193d8de |
| BF-BE/COMPLETE_DAG.json | 4b13c86fdc6ce65e |
| BF-BE/ENDPOINT_DEFINITION.diff | c67cee9239ed35e7 |
| BF-BE/H6_ID_MAP.tsv | e72ba377d6891359 |
| BF-BE/H_REPORT.diff | ea7e6b648e5c2aee |
| BF-BE/PACKAGE_CHECK.json | 18af54bd2e5cb456 |
| BF-BE/PREPARATION_NOTES.md | 5f6209bca4602acb |
| BF-BE/PROOF_TEXT_BE.diff | e8c4b25f116ff0e7 |
| BF-BE/PROOF_TEXT_CORRECTED.md | c3d6692c358eb0ce |
| BF-BE/<reply pointer file> | db20cb2e6eac084f |
| BF-BE/SOURCES.json | b5f6064b0e7069fc |
| BF-BE/STATUS_AND_SOURCE_NOTES.md | 60846b0c465e4c88 |
| BF-BE/UNUSED_SOURCE_SCOPE.json | d52bbee60bb423d0 |
| BF-BE/build_be.py | c6b8284c487792de |
| BF-BE/check_bf.py | 509123794a379451 |
| BF-BE/check_package.py | f5a58e24b892ae94 |

Others relied on:
- BC PROOF_TEXT_CORRECTED dc0d6e7b5bd8aab8; BC COMPLETE_DAG e8a786a77aaa9884; packet PROOF_TEXT b42fa1670b11643a.
- RESTRICTED_CHECKER.md 31ce8b7943a69ed1; HIGH_FIRST_REVIEW.md d6fd0d89c38734e6; REVIEW.md 63602be907da319d; exact_classes.py 802dc62aa4f2a9e1; exact_general.py 89954c6c44e1368b; REPORT_CHARGE_CORE.md 6f8f7e897cd754db.
- uniform.py 019ce089aa4d531f; REPORT_TERMINAL_2.md d95c56521d9224c7; SPEC_v3.0.md 0a6dfc2ae10ed6f3.
- h_report30_v1 1c01dda73b9ff581; h_report30.py 0314aa1f8f742cd7.

## Scripts (<reviewer scratch>/)

- dagcheck.py (ecc34744): graph comparison, ancestry, id binding. Six controls, all flagged: edge removed, back edge, h6 field dropped, id duplicated, id invented, orphan node.
- pins.py (868e0ef8): every file / sha256 / bytes triple in ADMISSION_EVIDENCE, BE_SOURCE_PINS, SOURCES, UNUSED_SOURCE_SCOPE, ARC_MARGIN_UNITS, BF_CHECKS, BE_CHECKS, BD BINDINGS, both ADDENDUM files: 0 bad. Control: last hex digit changed, every pin flagged.
- arc.py (ed7ddae1): CO-c1 exact. Control: root end moved by 1e-20, both stored values rejected.
- bfcheck.py (9a4d9f97): endpoint subtree and JQ v1 / v2. Control: one endpoint value changed, inequality reported.
- hdr.py (a5160d1e): header against header. Control: label 13 replaced by label 12, flagged.
- parallel.py (b1278f6d): exact grid test of the tangent polynomial on [0, 1/10], with a control at e = 11/10. Float falsification of the parallel row with the full E on about 150,000 feasible random samples: least row value +1.9e-5, no violation. Controls: dropping q^2/2 or the term (Dm+dr)(q+q^3) gives violations (-3.6e-3, -9.5e-4). Dropping D m^2/2 or m dr gave none in this sample, so the test is weak for those two terms; they rest on my hand derivation.
- patch of the supplied text diff on a scratch copy; diff of the two post-check scripts.
- I ran none of the author's scripts.

## Not read

- Every <author reply> file; <message file to the author> outside lines 47-171.
- BB and BC apart from the BC text as diff base, the BC graph, lines 1-40 of G20S_COMPOSITION_OF_RECORD.md and a diff of the BB status notes.
- build_be.py, check_bf.py, check_package.py; contents of PACKAGE_CHECK.json and BE_CHECKS.json beyond their pins.
- Graph node texts other than the changed node and nine nodes printed for F2.
- Contents of C16_STATUS_ERRATUM, CASE_SOURCE_BINDING, LEAF_REUSE_SCOPE, CHILD_CONTROLS, PROVENANCE_INDEX, PER_JOB_RECORDS (hashes only); LABEL11_EXECUTED_ARCS beyond its four row headers.
- pilot.py; uniform.py outside lines 50-275; exact_classes.py outside 160-230, 255-326, 440-492; exact_general.py after line 60; the Node checker; boolean_rule.py; integer_sweep.py.
- The sixteen-square THEOREM.md after its part 2; entry-producer/PROOF.md after the first lines of "Exact transfer"; check_transfer.py and check_binding.py beyond a grep; the four review texts beyond their opening lines.
- REPORT_TERMINAL_2 sections (4) to (6); REPORT_UPPER_EXACT, REPORT_RECEIPTS, REPORT_TEXT and REPORT_TERMINAL beyond the lines quoted.
- SPEC_v3.0 outside sections 0, 1, 11; SPEC_v3.0_NOTES.
- New text lines 4-22 and 185-202 apart from the changed lines.
- Any certificate body, any tree stream beyond the first line, any computation rerun.

