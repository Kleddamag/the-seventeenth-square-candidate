Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line.

# Review of tags v2 and v2x (`JOIN_ROOTS.md` section 9, G1 to G6) and of `RECORD_EJQ_v1.md` (G7)

Independent reviewer (the same reviewer as `REVIEW_JOIN_ROOTS.md`), 2026-10-09.
Texts as reviewed are kept here: `JOIN_ROOTS_as_reviewed_v2.md` (state 18:04:45, sha256 fffc0bd1...; the live file
got three more lines at 18:07, so its lines after 36 are 3 higher) and `RECORD_EJQ_v1_as_reviewed.md` (f91a5b81...).
Line numbers below refer to these copies.

**VERDICT: SOUND WITH CORRECTIONS.** No MUST finding. The thirteen region files are what section 9 says they
are: every box end and every arc recomputed from the literal class files with my own code (5,122 exact
conditions, 0 failures, 9 deliberate mutations all detected). The support lemma is true, its minimum is taken
correctly and the end is rounded in the safe direction. The cover of 9.3 and every cell of the table of 9.4
hold against the literal hypotheses of the class files. `RECORD_EJQ_v1.md`: every number confirmed; my own
acceptance run gives the same result; the statement is correct and may be called PROVED with one wording
correction (S2).

## Findings

### MUST
None.

### SHOULD

**S1. Section 9.5 item 4 (lines 549 to 552) is not the decided design.** It tells the float side to describe
the wall cells (s9 from y = 129/50, loose labels in the loose slots) on `JPW_exact_v2.json`, with JPW13 only as
an alternative, and does not name JPWS. The table at the top (lines 11, 12, 24) and 9.4 say: slab on JPWS,
above 13/5 on JPW13, JPW v2 not part of the design. A complete tree on JPW v2 would give the statement for JPW13
(containment, verified), but it must also close "slab with the loose labels in their loose slots", which no
case hands over, and it gives nothing for JPWS (JPWS is not inside JPW v2 in labels 3, 15, 17: xi_{3,1} to
0.495099 against 0.249966). Fix: rewrite item 4 as two descriptions, JPW13 and JPWS.

**S2. The record's emptiness step is not literally the root-region corollary.** `SPEC_v3.0_NOTES.md` lines 36 to
45 conclude "every configuration of F(root) lies in the tube". The record (lines 22 to 24) needs "F(root) is
empty". That is true and short: SPEC 3.0 section 5 (line 515: an accepted `0` step proves F(N) empty), closing
condition 7 (a), the root conditions and section 2 for what F(root) is, section 11 for S <= Sref; with several
nodes, the induction of the THEOREM's proof with (a) and (c) only. But it is an argument of its own, used by
twelve of the thirteen statements, and I find it written in none of `SPEC_v3.0.md`, `SPEC_v3.0_NOTES.md`,
`reviews/REVIEW_30_ACCEPT.md` (section 3 of JOIN_ROOTS only says "`terminal_leaves` = 0"). Fix: add a two-line
EMPTINESS COROLLARY to the notes ("all conditions of section 7 and no node closed as TERMINAL: F(root) is
empty") and cite it; in the record replace "closes case Q" (line 51) by "is the local side's statement for
case Q" (it is conditional on (i) and (ii) of the same section).

**S3. The composition for the decided design uses more than "the one addition" named in 9.3 (line 491).** All
of the following hold (exact checks), but none is written where the cases are stated: (a) L9 holds one centre
(feasible part: diameter squared 11566501/25000000 < 1), so in cases T and G the exempt class WC of PT_j / PM_j
and the exempt A_Q of L_j are empty; without it PT_j gives "PB_j or the wall column" only. (b) The wall column
holds one centre (1517/5000), used for JPW13. (c) A square ON the line x = 53/100 lies in WC, so PT_j / PM_j say
nothing about it; the wall cases take it (their statements apply, the wall lemma applies in K because the
shift is positive). (d) Case G still needs "X empty": X of the C files is version 1's TT united with A_Q(v1);
with s9 gated and off the wall column it is empty. (e) The support lemma. Fix: one paragraph in 9.3, or the
theorem text of open point 6, before a tree on these regions is counted.

### NOTE

N1. **Support end and Codex's seal (lines 462 to 469).** Codex sealed xi_{9,1} >= -99/10000. The regions end at
-9897/1000000, which is 3e-6 TIGHTER; it does not follow from the sealed statement but from the exact value
-0.0098965702325, which I recomputed and which equals Codex's `support_minus_reference` as a rational number.
A final text must quote the lemma with -9897/1000000 (or the exact value), not the sealed number.

N2. **"Cross-check of the PW files" (lines 427 to 433).** Boxes: exact for the ten labels, as claimed. Arcs:
exact for eight; for labels 10 and 16 (one end from PB_j, the other from QB_j, so a new centre and a new
rounding) JPW's root-arc ends differ from JPA's / JQ's by 1.1e-10 to 1.6e-9 rad; the class-file intervals are
exactly the hull. For 11 and 13 "one end each is 1e-6 short" is what remains after rounding to the grid: as
polygons HULL_11 and HULL_13 are short of the tilted hull of PB_j u QB_j at SEVEN of eight ends (1.2e-7 to
8.7e-7; only HULL_13's lower xi_1 end is beyond it, by 3.1e-8). No region uses the containment.

N3. **9.5 item 3, "no cut is made".** Rule 1's tolerance (1e-5) is the lead's rule, not the tool's:
`eff/sdp3/mk_chain_tree.py` (Chain.box, lines 86 to 92, file of 16:19) cuts whenever a cell end is strictly
inside the root's. A cell that starts label 9 at Codex's -0.0098966 would be cut 4.3e-7 inside the root and
leave an open sliver (shown by `hull_node.py check`; no soundness issue). `p3tools/rootcheck.py` of item 5 is not
in that folder on this Mac; not seen.

N4. **9.5 item 3, the fallback.** The node identity is right (G5 below). But the piece below the cut,
xi_{9,1} in [-0.204203, -0.009897] with gated directions, is empty only by 4.3e-7 at the gate's lower end: its
"one further leaf" would have to prove the support lemma numerically to that margin. Treat the lemma as part
of the theorem text; it is elementary and checked here.

N5. Wall ends: 15 per region, 14 in JPA and JPB (as in v1). In JG v2 and the six JPG v2 label 9's entry is the
support end. `info_floats["9"].arc.tau_centre` is a text, not a number, in JQ, JPW, JPW13, JPWS (v1 report N2).

N6. `JQ_exact_v2.json` lists the version 2 loose Q files as inputs (the lead's bookkeeping point). I recomputed
JQ v2 from the sixteen files of record (`classes_v2_Q16/`, byte-identical to their sources, hashes checked):
the same region in all 68 ends and 17 arcs.

N7. In the two checker reports `final_store_sha256` differs (0a802b6b... and 1a945429...). This is by
construction (two different serialisations: `store_digest`, wxcheck_v30.py line 2510; `storeDigest`,
wxcheck2_v30.js line 3257); the acceptance report does not compare them. Not a discrepancy.

## Results

**G1 (exact, own code: `recompute_v2.py`, `recompute_v2.out`).** Thirteen regions, 221 (region, label) entries.
My mapping: JQ: A_Q(v2), QB_j of record; JPW: W, HULL_j, loose slots; JPW13: W with y >= 13/5; JPWS: slab,
HULL_j, QB_3/4/15/17 of `classes/`; JPA, JPB: T9 of the PT files, PB_j of PT; JG, JPG: L9 with the support end,
E_j resp. PB_j. Every transported polygon lies in its box for every S* of the enclosure; every non-wall end is
within 1e-6 of the hull; wall ends valid; 156 slot arcs, lift -1 for label 16 in all thirteen, 0 otherwise,
excess at most 3.106e-9 rad; gates, "above / below", "any", wall pose, header radii, lo = conj(hi), ROOT
CONTAINS WINDOW: all true. Table of 9.1 (`case_logic_v2.out` section 7): JQ: ONE end (label 9's upper xi_2,
-0.124437 against -0.104437), v2 inside v1; JG and six JPG: ONE end (label 9's lower xi_1, -0.009897 against
-0.204203), all other fields equal; JPA, JPB: all 68 ends and 17 arcs equal; JPW v2 differs from v1 exactly in
labels 1, 5, 9, 10, 11, 12, 13, 14, 16; JPW13 = JPW v2 with ONE end (-0.104438, v1's), inside JPW v2; JPWS
differs from JPW v2 exactly in 3, 4, 9, 15, 17 and has 3, 4, 15, 17 as JQ. JG v2: 7 + 20 exits recounted. The
eight decimal rows of 9.1 agree with the file. I RAN (not imported) both generators into `regen_v2/`: the
thirteen region files and both tables are byte-identical; the EXPECT files differ in the folder name only.

**G2 (exact).** The lemma is true as stated: for ANY unit side direction (g, s) of the square, c - u/2 + v/2 is a
corner with x = c_x - (g + s)/2. Root arc of label 9 (the same in JG and the six JPG, v1 and v2): absolute
angles 0.594827896 to 0.794628218 rad, both ends in the open first quadrant, lower end first; (g + s)/2 =
0.6943055854250 at the lower and 0.7070766608065 at the upper end; concave on the quadrant, so the minimum is the
lower end value (also: 2,001 exact directions across the arc, none below). Minimum - p_9x = -0.0098965702325;
the end -9897/1000000 is BELOW it by 4.29767e-7: safe direction. At the gate's own lower end the value is
60762587399/87515625202 (confirmed); the arc's outward rounding lowers it by 1.06e-10. Premises (a) and (b)
are all that is used, with the frame of 2.1 (left wall x = 0 in K and for the checkers; xi_{9,1} = c_x - p_9x,
label 9 Cartesian). Nothing handed over is lost: K lies in x >= 0 and a gated direction lies in the root arc.
0.6943 > 53/100: a gated square is off the wall column. Codex's three rationals in
`d-join-roots-producer/RESULT.json` equal mine exactly (margin to -99/10000: 3.42977e-6).

**G3 (exact, `case_logic_v2.out` sections 2 and 6; float sampling of my own, `sample_cover_v2.out`).** Class
frame: L9 = wall column u T9's rectangle; wall column = A_Q(v2) u slab u {y >= 13/5}. In K the label-9 boxes
overlap at every seam: JQ v2 ends at -0.124437, JPWS starts at -0.124438; JPWS ends at -0.104437, JPW13 starts
at -0.104438; the wall factors end at -0.174437, JPA / JPB start at -0.174438. Directions: JPA starts 2.3e-9
rad below the gate arc's upper end, JPB ends 3.2e-9 rad above its lower end; JPA's top and JPB's bottom plus a
quarter turn overlap by 1.6605e-3 rad. The five wall arcs are the x axis +- rot(31/1000) exactly. Wall lemma:
1061039/1000961 > 53/50 and 31/1000 < sqrt2 - 1; class-frame x <= 53/100 is x < 53/100 in K. The only poses in
no factor are those the two lemmas exclude. Sampling: 300,000 feasible poses, dense at the seams, none outside
its factor; smallest gated xi_{9,1} = -0.009876766.

**G4 (exact for the files, reading for the logic).** L_j exempt [-131/250, 53/100] x [24137/10000, 13/5]
(four files); the sixteen version 1 Q files have that A_Q, the sixteen `classes_v2` Q files end at 129/50;
W = [.., 53/100] x [129/50, 29637/10000]; PW has twelve files, none for a loose label: the gap is real. Every
cell of the table follows. JPW13 has no open premise under either repair: for y > 13/5 the square is in W and
not in A_Q(v1), the wall column holds one centre, so L_j gives the loose slots; y = 13/5 itself is taken by JQ
v1 (repair 1) or JPWS (repair 2). JPWS is the right region for repair (2). "JQ v1 counts under both", "JPW v2
contains JPW13", "JPW v2 is no substitute for JPWS": confirmed. In each case (JQ, JPWS, JPW13, JPW v2, T, G)
the seventeen position sets are pairwise disjoint (exact separating-axis test) and every feasible part has
diameter < 1 (largest 0.6809); label 12: diam(hexagon u HULL_12 box) = 0.549531, and HULL_12 leaves the
hexagon (true for PW only), M = half-marker minus target in PW, PT, PM, Q.

**G5 (exact numbers, reading of the rules).** -9897/1000000 lies strictly inside [-204203/1000000,
195763/1000000]; `HULL_TREE_FORMAT.md` lines 46 to 48 and `hull_node.py` lines 431 to 445 give the second child
[at, hi] with the same side interval, other intervals, arcs and assumption list; SPEC 3.0 section 6 (line
552) admits it. JG v1 and v2 (and each JPG) agree in everything else, so that child is the v2 root node. Leaves
then fit if the v1 description keeps the ids (hull_tree.py lines 115 to 118 compare id and parent). JPA, JPB:
the same regions; their EXPECT files differ in `name` and `root_region` only.

**G6.** See N2. Nominal rectangles of Log 17:28: the region equals them in 6 of 8 ends and is 1e-6 inside in
the two named. `SHA256SUMS_v1`: 22 of 22 match at 18:32 (no file of tag v1 changed); `SHA256SUMS_v2` 22 of 22, `_v2x` 4 of 4; the hashes
printed in 9.1 and the thirteen rows of the top table are the files'; inputs_sha256 (108 per region) match the
disk; `classes_v2/SHA256SUMS` 100 of 100. Root tests: I re-ran BOTH frozen checkers on the thirteen stored test
certificates and the control (`rerun_checkers_v2/`): each certificate carries the region's node, the root is
accepted, the only failure is the missing child; the control is refused by both. `sample_check_v2.py` re-run:
the numbers of 9.6 reproduce (it tests tag v2 only).

**G7 (`record_check.py`, `record_check.out`; own acceptance run).** Hashes recomputed and equal to the record:
certificate .gz 0b2a8ff8..., uncompressed 3d4606d1..., second copy byte-identical, log d04fa0f0..., reports
3ccc8233... and b8128b2a..., EXPECT cbd56dcb..., region f4d1607e..., the three frozen files. My own comparison
of the certificate with `JQ_exact_v1.json`: 2 lines, ONE node = the root, parent null, empty assumption list,
side [Sref, Sref], box equal in all 68 ends, arcs equal in centre and both ends for 17 labels, header window
and tube equal to the file's; closure "infeasible", one round, one step of the form `0`, sense lo, declared
value 3455339/552809052, 48,209 terms. Both reports: whole-file PASS (modes "full" and "certificate"), 1 node,
infeasible 1, terminal 0; `zero_step_L` the same 3,761-character string, sha256 32f5ba22..., value
0.006945012101 > 0; the cloud run's two reports record that same hash. My run
(`acceptance/ACCEPT_REVIEW_JR_JQ_v1_jQTwn0.log`, 18:23): RESULT: ACCEPTED, both reports equal the lead's except
the time, the two logs agree line for line except date, times and memory.
Is the statement right: yes; it is the statement of the notes' corollary with "empty" in the place of "in the
tube", see S2. Is the last section overstated: only "closes" (S2); its two "NOT contained" items are the right
ones (for (i): JQ v1 and JQ v2 are confirmed against the class files in my two reports).
**May (E_JQ, v1) be called PROVED** as a statement about the numbers of `JQ_exact_v1.json`: yes, in the sense
of `bigbox/THEOREM_G20.md` (accepted by both frozen checkers; specification and checkers reviewed at their
freeze; this record reviewed by a reviewer that wrote none of it), once S2's wording is in. Limits: the
soundness of SPEC 3.0 and of the two frozen checkers is taken from `reviews/REVIEW_30*.md`, not from me; I did
not re-derive L from the 48,209 terms (two checkers did, three times). Nothing here says that case Q is empty:
that needs the sixteen Q_j certificates, which do not exist.

## How each part was verified
- Exact computation with my own code: G1; the numbers of G2; the seams, rectangles, capacities and disjointness
  of G3 / G4; all region-to-region comparisons; G6; the certificate-against-region comparison and all hashes of G7.
- Re-execution of the lead's programs with output into my folder (or under my NAME): both generators, both frozen
  checkers on fourteen test certificates, the acceptance script on the JQ certificate, `sample_check_v2.py`.
- Reading only: the case logic of 9.3 / 9.4 as an argument, the tool code quoted, SPEC 3.0 sections 5 to 7 and
  11, the notes' corollary, three replies of Codex.

## NOT checked
- Any capture statement (no class certificate exists); the truth of the twelve other region statements (no trees).
- The generators' code beyond the support part and what they write (their outputs were recomputed instead).
- SPEC 3.0, the two frozen checkers, `h_report30.py`: not re-reviewed. The export chain and the cloud job.
- Codex's audits beyond the three rationals; the float cells, the strip "xi_{9,1} in [-0.204203, -0.1753]",
  `rootcheck.py`, prices and manifests.
- Whether "loose only" is the best design, and Codex's pending seal of it.

Files of this part (all in this folder): `recompute_v2.py`, `recompute_v2.out`, `case_logic_v2.py`,
`case_logic_v2.out`, `sample_cover_v2.py`, `sample_cover_v2.out`, `sample_check_v2.rerun.out`,
`rerun_checkers_v2.sh`, `rerun_checkers_v2/`, `regen_v2/`, `record_check.py`, `record_check.out`,
`accept_rerun.stdout`, the two "as reviewed" copies. Outside this folder:
`acceptance/ACCEPT_REVIEW_JR_JQ_v1_jQTwn0.log`, `acceptance/REVIEW_JR_JQ_v1_jQTwn0_C1.json`, `_C2.json`.
