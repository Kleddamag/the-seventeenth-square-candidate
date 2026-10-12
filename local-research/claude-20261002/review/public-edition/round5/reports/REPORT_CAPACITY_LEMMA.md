Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line.

# Fresh-reader review: coarse-region capacity lemma (Z3 bridge / coarse-capacity-R)

**VERDICT: HOLDS for the geometric lemma (capacity at most one in each whole coarse region 3, 15, 17, every position, every pair of independent angles, every container side <= C); its use in case JG HOLDS WITH CONDITION (off-wall branch only; unique parent in L9 from FRAME_ASSIGNMENT; bound 20 of rows L3, L15, L17 with the high-first score semantics; the JG angle gates) - those imported premises were not reviewed here.**

Reviewer: fresh reader, 10 Oct 2026. I wrote none of the reviewed text. Sentences marked JUDGEMENT are my opinion; everything else is a computation of mine or a quoted line.

## 1. The lemma in my words

Hypotheses. Coordinates in unit-square sides, frame [0,U]^2 with U = 1169/250, centre (1169/500, 1169/500) (class files, field `frame`). A family of closed unit squares, pairwise interior-disjoint, arbitrary independent orientations, all inside a square container of side s <= C = 4675531/1000000 concentric with the frame. So every square lies in [delta, U-delta]^2, delta = (U-C)/2 = 469/2000000. No case assumption, no marker, no certificate.

Conclusion. At most one square of the family has its centre in each of
- region 3: x in [129/100, 2993/1500], y in [-1/2, 1411/1000] (bottom wall),
- region 15: x in [19953/10000, 26807/10000], y in [1623/500, 26/5] (top wall),
- region 17: x in [3775331/1000000, 5199531/1000000], y in [24137/10000, 29637/10000] (right wall).

Use in the wider proof (bridge steps 1-5; manifest premises WALL_PARTITION and ROOT_ADMISSION depend on COARSE_LOOSE_CAPACITY). In an off-wall branch the rows L3, L15, L17 force an occupant of the small slot S_k; S_k lies in coarse region k; capacity one makes that occupant the only parent in the whole region; in JG its angle is gated (|tau_k| < 1/20), so the two escape slots on each coarse region in the ten C files hold no parent.

The "128 closed subintervals" are subintervals of u = tan(alpha/2) in [0,1], where alpha is the direction of the separating axis. They are not side-length intervals and not sampled square angles. The "two orderings" are: which of the two squares (the owner A of the separating normal, or the other square B) is nearer the wall.

## 2. Step by step

1. Centres lie in [delta+1/2, U-delta-1/2]^2. HOLDS: a unit square contains its inscribed disk of radius 1/2.
2. Region 17 by diameter. HOLDS. Clipped box is [3775331/1000000, 8351531/2000000] x [24137/10000, 29637/10000]; squared diagonal 1851391155161/4000000000000 = 0.46285 < 1 (recomputed, equal). Disjoint open inscribed disks give centre distance >= 1. The clipping is needed (unclipped width 1.4242).
3. Separating axis is a side normal of one square, also for touching squares. HOLDS: standard for convex polygons with disjoint interiors (edges of the Minkowski difference are parallel to edges of A or B). The text states it without proof. JUDGEMENT: acceptable as a cited standard fact.
4. Absolute components a, b of the normal, d = (a+b)/2 as A's support against the wall. HOLDS. |n.(cA-cB)| <= a|dx| + b|dy| by the triangle inequality; A's axes are n and its perpendicular, so its support along e_y is (a+b)/2 for every sign pattern. The bridge's sentence "it does not reflect a single physical square" is obscure; the clean reason is that for mixed signs the direction of n modulo a quarter turn is pi/2 - alpha, and the two breakpoint values in step 6 are the same.
5. Ordering "A nearer": |dy| <= H - d, other support >= 1/2, hence a w + b H - b d >= 1. HOLDS.
6. Ordering "B nearer": need a w + b H >= 1/2 + f(phi), f = h_B(n) + b h_B(e_y). HOLDS. f has period pi/2 in phi, breakpoints on [0, pi/2] exactly 0, alpha, pi/2; between them it is a positive sum of sines and cosines, so f'' = -f < 0; values d + b/2 (at 0 and pi/2) and 1/2 + b d (at alpha); difference (1-b)(a+b-1)/2 >= 0 (I re-expanded it). So f >= 1/2 + b d for every independent angle of B, and inequality (1) is needed in both orderings. Ties in height are covered by either ordering.
7. Quartic. HOLDS. (1+u^2)^2 [1 - a w - b H + b(a+b)/2] = (1-w) + (1-2H)u + 4u^2 + (-1-2H)u^3 + (1+w)u^4; expanded by hand and checked exactly at 9 rational points. u in [0,1] covers alpha in [0, pi/2] including both end axes.
8. Parameters. HOLDS. w3 = 2993/1500 - 129/100 = 529/750; H3 = 1411/1000 - delta = 2821531/2000000; w15 = 3427/5000; H15 = U - delta - 1623/500 = 2859531/2000000. Rounding direction is right: H is the distance to the outermost wall position allowed by s <= C, and the failure of (1) is monotone in H and w, so smaller containers are covered. The bridge does not derive H from the regions (only check.py asserts it).
9. Cover of [0,1] by 128 closed cells [j/128, (j+1)/128]. HOLDS. Positive Bernstein coefficients give P > 0 on the closed cell; first and last coefficient are P at the cell ends; every seam value is positive and identical from both sides (checked for all 127 seams and for u = 0, 1). All arithmetic is exact; nothing is rounded.
10. Conclusion "P > 0 on [0,1] contradicts every separating axis, so two centres in the region are impossible". HOLDS.
11. Application step 2 (AQ empty off-wall; bound 20 forces an S_k occupant). HOLDS WITH CONDITION: needs the unique L9 parent with x9 > 53/100 and the row semantics; both imported, not reviewed here. AQ box [-131/250, 53/100] x [24137/10000, 13/5] read from the class files.
12. Application step 3 (S_k in coarse region). HOLDS: clipped S3, S15, S17 boxes lie in regions 3, 15, 17 (recomputed from L_L03, L_L15, L_L17; S17 only after clipping, x reaches 26/5). The clipped frame region L17 lies inside clipped coarse 17 (18879/5000 >= 3775331/1000000, same y), so the same lemma also makes the L17 occupant of FRAME_ASSIGNMENT equal to the S17 occupant; the bridge says "the identities agree" without this one line.
13. Application step 4 (gated parent is in no escape slot). HOLDS given step 11. In all ten current classes_JD files the six coarse escape slots are exactly the three regions with closed arcs [1/20, 207107/500000] and its negative. Quarter-turn images of the open gate are (19/21, 21/19) and (-21/19, -19/21), half turn |tau| > 20: all outside the arcs. 207107/500000 > tan(pi/8) (T^2+2T-1 = 309449/250000000000 > 0), so gate and arcs together cover every direction.
14. Application step 5 (two L9 angular exits). HOLDS WITH CONDITION: the gaps 1/200000 and 974949/14197000000 are right for the gate (61301/200000, 591183/1408817), and all four representatives miss both closed exits. I did not read where that label-9 gate is defined; the numbers are hard-coded in check.py.

No step is GAP or WRONG.

## 3. Replay

My own script `my_replay.py` (fractions only, 0.3 s, 13 MB) does not call the author's code. Recomputed in full, not in part:
- w, H from regions, U, C; region 17 diagonal: equal to the stated values.
- All 1280 Bernstein coefficients by a different method (Bernstein form on [0,1], then seven exact de Casteljau bisections; the author uses a Taylor shift per cell): all 1280 equal to coarse-capacity-R/RESULT.json, all positive. Minima 634043429/125829120000 (cell 52, index 2) and 43535731167/8388608000000 (cell 56, index 3), equal to Z3/RESULT.json.
- Independent certificate: exact Sturm sequence, zero real roots of P in (0,1] for both regions, P(0) = 0.2947 / 0.3146, P(1) = 0.3569 / 0.2809.
- Margins: least value of 1 - a w - b H + b d is 0.003691 (region 3, axis at 44.9 degrees) and 0.003611 (region 15, 48.3 degrees). Exact Sturm bisection: lemma 3 fails only above H = 1.415978 (used 1.410766) or w = 0.710522 (used 0.705333); lemma 15 above H = 1.434584 (used 1.429766) or w = 0.690802 (used 0.685400).
- With delta = 0 (wall on the frame edge, H = 1411/1000 and 143/100) both quartics are still root-free with positive Bernstein tables, and region 17 has squared diagonal 0.46304. So the lemma does not depend on the concentric placement, only on the container lying inside the U frame.
- `direct_sat.py` (float, sampled, evidence only): 361 x 361 independent angle pairs, all 8 extreme positions, 4 axes. Largest separating gap -0.003692 (region 3) and -0.003611 (region 15), both for parallel squares, equal to minus the exact margins; a control with H = 1.4165 gives +0.00037. So the reduction in steps 3 to 6 is sharp and loses nothing.
- `gates.py`: exact angle bookkeeping of steps 12 to 14.

Author's replay.py: run once on a copy in my scratch folder (the script overwrites its own RESULT.json, so I did not run it in place; coarse-capacity-R and second-order-20261010 were linked read-only). Outcome: exit 0, status PASS_SOURCE_TABLE_REPLAY_AND_CURRENT_C_ESCAPE_COVER, 33 pins, 1280 coefficients, same minima, same ten C files. Only differences to the stored RESULT.json: paths, CPU time, and the manifest hash (stored 02c9ecda..., current file 0216de42..., manifest rewritten 20:27). I did not run coarse-capacity-R/check.py (it rewrites INPUTS.json and RESULT.json).

Not recomputed or read: charge arithmetic, FRAME_ASSIGNMENT, reports C and D, F1_PROOF.md, the JG local tree, the source of the label-9 gate.

## 4. What a reader must be told that the text does not say

1. The 128 cells subdivide the direction of the separating axis (u = tan of half its angle). Positions and the second square's angle are removed analytically. Nothing is sampled.
2. Coordinate convention: origin at the frame corner, walls at delta and U - delta; H is "region edge minus delta" (3) and "U minus delta minus region edge" (15). The bridge gives w and H as bare numbers.
3. The margin is thin: about 0.005 in H and in w for regions 3 and 15. Any later enlargement of either region by 0.005 in width or towards the interior breaks the lemma. Region 17 has a wide margin (0.46 against 1).
4. The regions reach outside the container (y from -1/2, y to 26/5, x to 5.1995); only region 17 needs the clipping.
5. Coarse 17 is the mirror image of L9 with constant C instead of U (x0 = C - 4501/5000, x1 = C + 131/250), hence the shift by 469/1000000 = 2 delta against the frame region L17. JUDGEMENT: harmless for capacity, but a reader should know it is not the reflection of the frame.
6. The application covers the off-wall branch only (x9 > 53/100). The bridge does not say where the wall branch gets its identification.
7. Status disagreement: the bridge (18:02) says "FRAME_MARKER remains open until its current literal receipt/conversion is imported"; the manifest of 20:27 lists FRAME_MARKER and FRAME_ASSIGNMENT as COUNTED. One of the two is out of date. JUDGEMENT: the audit lead should decide which and record it.
8. The bridge is not a file of record: the manifest pins the five coarse-capacity-R files for COARSE_LOOSE_CAPACITY and never mentions coarse-capacity-Z3. Z3/RESULT.json records an older manifest hash.
9. coarse-capacity-R/RESULT.json field `C_escape_files_equal` was computed on the old classes/C_L*.json; the ten current classes_JD files are covered only by the Z3 replay (and by my check above).
10. Both author scripts rewrite pinned result files on every run (CPU time changes the hash). Replays must be run on a copy.
11. ACCEPTED_INTERFACE.json and PURE_LEMMA_SCOPE.json state the lemma differently ("seventeen-square packing" plus an off-wall clause against "any family"). The proof gives the stronger "any family" form.

## 5. Files relied on (sha256)

- coarse-capacity-Z3/PROOF_BRIDGE.md 5eea194353cd9897c1552722852f4da045b11a38e327af5c35a9f5eeac065c51 (begins 5eea1943 as expected)
- coarse-capacity-Z3/RESULT.json 8b60cefac86d03dd9dcf6fc555e3d6794638ed568a0f12216da793e9e59c3cb0
- coarse-capacity-Z3/replay.py ef9c83fba7bed00f326def4c8ba85ce58a4083bd3de1121c1e0b6cd3ee8281f2
- coarse-capacity-R/PROOF.md bae9384411086b31ea5a547e40409409e3fd50b514da13078e0c189c3c227a28
- coarse-capacity-R/RESULT.json 5a466b6e51c3d1b55d66713af225873d15214d842cea9a02b99c647dc73fb41e
- coarse-capacity-R/check.py 14fcd438bbfabd0f0cb4e4f7b034af481413c9baf952d35727576dbe41271845 (read, not run)
- coarse-capacity-R/INPUTS.json 1dcf00c457bf60cb633c994033b70120b797c2ab5f26c19c19e160cc445aaa02
- coarse-capacity-R/ACCEPTED_INTERFACE.json 7e2693de02576eb955f641b386e4aafc44bcc3c349d864096078180842e1cf98
- coarse-capacity-R/PURE_LEMMA_SCOPE.json bc677b6953be297b6c4613be8cad3ef748a79c0a69c74da7da74488cdf7cb43d
- join_design/classes/L_L03.json 654dcdb2bd7dc627..., L_L15.json cfc5a6498b9d76be..., L_L17.json f23a24dafacf1f3a... (first 16 hex; equal to INPUTS.json)
- join_design/classes_JD/ L01 e7291cc33c302b88, L02 492e553c499ea6f4, L05 815b43670f11bc4b, L06 45f029fde9069021, L10 4d40cfef77ce2c2f, L11 3e73123004d95e35, L12 133ddb28b6227353, L13 26193ca8ba97a21d, L14 c9d349363302b8de, L16 ccf832baee001f61 (first 16 hex)
- second-order-20261010/theorem/THEOREM_MANIFEST.json 0216de42e6608665... (as of 2026-10-10T20:27:16; only premise entries and statuses read)
- my scripts in <reviewer scratch>/: my_replay.py 4756b6e299952553, direct_sat.py a0d29d58b0ab9ad8, gates.py 13f9789266496169; the copy run of the author's script is in <reviewer scratch>/authorrun/

