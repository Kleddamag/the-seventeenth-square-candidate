Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line.

REPORT of the reviewer of premise D (ROOT_ADMISSION, SELECTOR_LOGIC), 10 Oct 2026

1. VERDICT
No wrong step found. Both premises follow geometrically: I re-derived every target-in-root inclusion, every profile separation and every trigger inclusion from the pinned files, with no failure.
Two closable GAPS sit where the manuscript uses the join, not in the proof files: (G1) the JPA line of the decision list is wider than the JPA root; (G2) case JG needs capacity one of the coarse regions 3, 15, 17, which nothing cited for JG supplies.
SELECTOR_LOGIC is sound as an OR of complete implications; its weak points are provenance and one unpinned lemma file.

2. PER PREMISE

ROOT_ADMISSION: FOLLOWS WITH GAPS

G1. GAP, closable in one sentence, no computation.
- Place: EXACT_ENDPOINT_AND_CASES.md, table row "JPA | x9 > 53/100 and 591183/1408817 <= t9 < 1"; PROOF_TEXT section 5, "the upper exit, including its endpoint, is JPA" and "The removed lower exit ... is impossible by KEY_W".
- Why: label 9's arc in JPA_exact_v5 is the absolute directions [45.52884, 84.85253] degrees. Its upper end is the reference turned by rot(4147/10000), tan-half 0.9139665. For t9 = 23/25, 19/20 and 99/100 no quarter-turn lift lies in the JPA arc; all three lie in the JPB_v5 arc.
- Cause: the reviewed admission (d-selected-roots-v2-review/check_review.py, line 203) splits label 9 by its representative about the reference direction: JPA = [gate end, ref + 45 deg], JPB = [ref - 45 deg, gate start]. The manuscript splits by theta9 in [0, pi/2). The two differ on theta9 in (84.85, 90) degrees, which the text gives to JPA and the admission gave to JPB.
- Not fatal: KEY_W's literal slot 1 is tan-half [30651/100000, 44941/100000] (34.0817 to 48.3993 degrees), so off-wall the L9 parent cannot be there. REVIEW_KEYW_AMENDMENT.md has the fact ("nearest side direction lies in [-0.0998905550, +0.1499987538]"). The manuscript and the manifest statement of KEY_W_ELIMINATION say only "cannot be below the gate".
- To close: state "off-wall, 30651/100000 <= t9 <= 44941/100000 by KEY_W"; write the JPA predicate as 591183/1408817 <= t9 <= 44941/100000; give check_case_partition.py a removed atom above 44941/100000. This is the same kind of repair as F6.

G2. GAP, closable with an existing lemma; extends F1.
- Place: PROOF_TEXT section 5, "in the fully gated off-wall case, no legacy escape predicate occurs. Identification of its occupant uses the reviewed capacity/assignment argument"; EXACT_ENDPOINT_AND_CASES.md, "subject to the independently proved actual-parent assignment".
- Why: C_j (bound 20) forces T_j only if the class X is unoccupied. X contains the COARSE regions 3, 15, 17 with direction beyond the gate. The decision list defines JG by the labelled parents (the S_k occupants) being gated. A second parent in a coarse region outside S_k, tilted, would occupy X, and nothing cited for JG excludes it.
- The diameter test fails there: coarse region 3 clipped is 0.7053 x 0.9108, squared diameter about 1.33.
- What is needed: capacity one of the coarse regions (wall-strip lemma for 3 and 15, diameter for 17). The manifest binds it only inside SELECTOR_LOGIC (pss-ruling, for PSS); ROOT_ADMISSION and WALL_PARTITION do not list it.
- The lemma's analytic step lives in standing-contract-20261009-2134/thin-splits/TRIGGER3_CAPACITY.md. That file's header says "independent review OPEN", it is not hash-pinned, and it uses 64 subintervals with H = 1411/1000 where pss-ruling uses 128 with H = 2821531/2000000.
- I checked the lemma: the oscillation bound |h(theta) - h(phi)| <= h(theta - phi) - 1/2 is correct (concavity on one period, reduction of the relative angle to [0, pi/4]) and yields the requirement a*w + b*H - b*(a+b)/2 >= 1 for an axis of either square. This also settles F4.
- To close: name the coarse-capacity lemma as a dependency of the JG paragraph and of the F1 repair, pin TRIGGER3_CAPACITY.md, record a review. Alternative: define JG as "TT unoccupied", as independent-logic-review did.
- The seven tilted branches do NOT need it: capacity of S_k by diameter is enough there.

W1. WEAK, scope. The off-wall eight-way split is in no premise statement.
- WALL_PARTITION covers only x9 <= 53/100. The off-wall split is carried by one sentence of d-selected-roots-v2-review/REVIEW.md: "Off-wall, the role-9 angular split and the first-ungated order 3,17,15 exhaust the alternatives".
- It needs L_3, L_15, L_17 and L_4 to define the labelled parents and to give S_k. These are base rows, all COUNTED, but absent from ROOT_ADMISSION.depends_on.
- With "label k := the unique occupant of S_k" the split is exhaustive and every seam is owned. I checked: closed TT and T9 ends against open gates; 53/100 to the wall; 129/50 to Q; 13/5 to JPWS; tau = +-tan(pi/8) inside the arcs of both sign roots.

W2. WEAK, answers F5 (distinct parents).
- "136 separations" and "seventeen capacities" mean: per profile, the 17 label regions, clipped to the physical centre box at cap C, are pairwise strictly disjoint closed polygons, each of squared diameter below 1. All targets occupied then gives 17 different squares, one per label, exhausting the packing.
- I re-verified this for all eleven current roots with the UNION over all listed options per label: 136 of 136 pairs separated in each; largest squared diameter 0.4635.
- The coarse trigger region is not itself a member of that family (S_k is; for trigger 9 the T9 polygon is exactly label 9's off-wall factor). It does not matter, for two reasons.
  - psi = 1 + 3*1_H - 1_(E outside H) forces an occupant of E OUTSIDE H, so never the marker parent's or the trigger parent's pose. The text should say "an occupant of E outside H".
  - Exact check over all 121 selectable files, the Q, PW, C, L base files and the slab file: no trigger slot polygon meets its own file's target (530 comparisons, 0 meeting); no target of a label other than 12 meets the hexagon; every trigger is centre-disjoint from the hexagon; hexagon united with target 12 has squared diameter below 1 in all twelve label-12 files.

W3. WEAK, unstated dependency. C_12's arc reaches tan-half 4494109/10000000 (48.4 degrees). It fits JG's label-12 arc only after the cut at the half-marker end 207107/500000; my control without the cut fails. The cut is valid (target-12 occupant = marker parent, whose representative lies in [0, pi/4]) and is in check_review.py, but section 7 does not mention it. Q_12 and PW_12 need no cut.

W4. WEAK, provenance.
- The first proof file accepts the superseded tags (twelve roots: JPA and JPB v1, JPG v2, JPWS v2x). The current JPA v5, six JPG v5 and JPWS v4 are covered by v5-root-review for label 11 only, with "other sixteen labels ... unchanged" asserted. My direct check of all 17 labels on the current files removes the doubt.
- JPWS_exact_v4 does NOT contain the full HULL_11: for label 11 it rests on SL11_T020 alone. This is consistent with the manifest.

(d) Chart: exact and the same in both halves.
- Capture: class-frame centre c = K + (U - L)/2 = P + (U - S0)/2.
- Local: xi = e.(c - (U - L)/2 - p_i), corner at the origin, no recentring from L to R.
- p_i and the axes: SPEC_v3.0 section 1 and check_review.py agree, including p_13 = p_13^file - (T0/3) v_13 and tilted axes for 11 and 13 only.
- L enters through an enclosure of width 2.1e-54; the dependence is affine, so vertices times the two ends suffice.

SELECTOR_LOGIC: FOLLOWS (weak points only)

- "Any one suffices" holds for every option. In each of the 352 (clause, option) pairs:
  - thresholds give marker + trigger + 15 = bound exactly (23, 161/8, or 20 for PM);
  - the alternative WC is the whole wall column, empty off-wall;
  - the branch's trigger pose set lies in the option's trigger class (S_k clipped inside the slot polygon, branch arc inside a quarter-turn lift of the slot interval; for JPA, [gate end, KEY_W end] inside T9's lift; PSEp only in the plus root);
  - the target fits the clause root.
- Mixing is consistent: each option is a universally valid implication on its branch, and the union-of-options profile stays separated.
- Coverage is exact: 7 roots x 12 rigid labels = 84. The key-w selector file has 84 rows whose candidates, hashes, bounds and extra premises equal the manifest clauses (0 differences); all 121 selectable statements are used. Labels 3, 4, 15, 17 come from the L rows and label 9 from FRAME plus KEY_W, so no label of any root lacks a source.

S1. WEAK. "A PSS option also requires its listed L_k receipt" understates: L_3, L_15, L_17 (and L_4) are needed in EVERY off-wall branch, for the branch definition and for the loose root factors. PSS is then no special case. All 18 PSS-type files list L_k with the base row's hash and status COUNTED.

S2. WEAK, provenance. accepted_by names an audit by Codex: the selector was assembled and audited by the same party. Its own ACCEPTED_INTERFACE has status "REVIEWED_CONDITIONAL_SELECTOR_NOT_FULL_PROOF" and covers the 96-clause file; the 84-clause file is covered by the KEY_W amendment review. The only review of the composition by another party is the conditional composition review of the 11:20 manifest.

S3. Same as G2: the PSS identification p = q rests on TRIGGER3_CAPACITY.md (unpinned, "review OPEN").

3. WHAT I VERIFIED MYSELF
Scripts in <reviewer scratch>/: adm.py, adm2.py, adm3.py, strip.py, strip2.py. Fractions only, 1.2 s, pinned files only.
- SHA-256 of all 11 proof files of the two premises, 11 root files, 121 selectable class files, the base class files used and the slab file: all match the manifest.
- 455 (root, label, source) admissions on the eleven CURRENT roots, each with both position intervals (all polygon vertices times both ends of the L enclosure, physical clip, tilted axes for 11 and 13) and the direction arc with all quarter-turn lifts: 0 failures.
  - This includes the 352 option targets, C_j into JG, Q / PW / L / slab into the wall roots, the loose labels with their branch arcs, and label 9 (gate; support cut -9897/10^6; wall bound 31/1000).
  - Least position margin 4.3e-17, at flush right-wall ends.
- Six negative controls all behave: HULLW_11 into a v2 root fails; PB_11 into v2 passes; C_12 without the cut fails; a wrong label fails; HULL_11 into JPWS_v4 fails; QB_3 into JPW13 fails.
- Profiles, triggers, marker classes, selector equality: as stated above.
- Replay of check_review.py to a scratch output: PASS.
- Wall-strip capacity, by float scan over both orientations (not a proof): largest separating gap -0.00369 (region 3) and -0.00361 (region 15), both at parallel squares; a control with H = 1.45 gives a positive gap.

4. NOT CHECKED
- Any charge receipt, including KEY_W's.
- FRAME_L9 and its review; C7_C8_TRANSFER; ENDPOINT; the L enclosure itself.
- The local trees, and that both checkers' code implements the SPEC section 1 chart (I compared the SPEC text with check_review.py only).
- The exact Bernstein tables of pss-ruling.
- audit_v5_roots.py, not rerun because it writes into the repository.
- The internals of psv-audit and pse-review (replaced by my own check).
- The 624 fallback options and the ten reserve cuts (seal K): they are not among the 84 clauses' listed options.

