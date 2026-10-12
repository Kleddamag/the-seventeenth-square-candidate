Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line.

# Final review 1 of the frozen manuscript packet (s(17) optimality)

Reviewer: the final reviewer (fresh, had seen none of the work). Written Sat 10 Oct 2026.
Packet reviewed: `research/finishing-threshold-goal-20261007/window-capture/fifth-order-20261010/frozen-manuscript-20261010_1450/`.
`FINAL_SECTIONS.md` sha256 `a9f6efe6...3ba93` matches the value I was given. `PROOF_SKELETON.md`, `OPEN_ONE_PAGE.md` and `THEOREM_MANIFEST.json` match the hashes in the author's accompanying note.

## 1. Verdict

1. I found no step that is wrong. The upper bound (Section 1) is correct: I re-proved it exactly, independently of H256.
2. The top-level implication holds only in this form: four base budgets + 53 clauses + three root records **and fourteen imported "global premises" that the text cites but does not prove** imply the theorem. Section 8 and the core of Section 3 are citations, not proofs; they cannot be checked from the frozen text.
3. One step of Section 5 does not follow as written (the classification uses squares 3 and 15 before they are shown to exist); it closes with premises that are already COUNTED. One packet file (`OPEN_MARKER_MAP.json`) is wrong in two entries.

## 2. Findings, most serious first

### F1 — GAP (closable with existing premises): the branch classification uses parents 3 and 15 before they exist
- **Place:** Section 5, "choose canonical side directions theta_k∈[-pi/4,pi/4) for k=3,17,15" and "These comparisons form a disjoint exhaustive classification of every common-frame packing". Also `EXACT_ENDPOINT_AND_CASES.md`, "For actual parents 3,17,15".
- **Why:** Sections 4 and 5 establish a unique actual parent only for labels 9 and 17 (and the marker). Nothing before this sentence shows that an off-wall packing has exactly one parent in region 3 and in region 15. So tau3 and tau15 are not defined for "every common-frame packing".
- The exact check `check_case_partition.py` proves a partition of a coordinate domain, not that every packing has those coordinates. (I replicated it: 30870 atoms, each owned by exactly one case.)
- The manifest has the same hole: `WALL_PARTITION` depends only on `FRAME_ASSIGNMENT`.
- **What closes it:** one paragraph before the decision list.
  - Off-wall, the unique L9 parent has x9 > 53/100. The alternative AQ of the L files is the polygon [-131/250, 53/100] × [24137/10000, 13/5], which lies inside L9 (read in the hash-pinned `L_L04.json`). So AQ is empty, and L_3, L_15, L_17 (all COUNTED) each force a parent in S_k.
  - Uniqueness is the capacity-one statement for the coarse regions that Section 6 proves (wall-strip inequality for 3 and 15, diameter for 17).
  - Add L_3, L_15, L_17 and that capacity lemma as dependencies of `WALL_PARTITION` / `ROOT_ADMISSION`. No new computation is needed.

### F2 — WEAK (structural): "FINAL" sections 3, 7 and 8 rest on imported theorems the text does not prove
- **Place:**
  - Section 8, "Apply that theorem to the normalized packing at actual side L. It fixes all 45 exact-root core deviations to zero".
  - Section 3, "These are the imported checker-soundness and boundary lemmas".
  - Section 7, "This is the imported exact inference theorem".
  - Section 4, "This conditional implication is proved in ROOT_ADMISSION".
- **Why:** the manifest lists fourteen global premises, all COUNTED: ALGEBRAIC_ENDPOINT, UPPER, ENDPOINT, CHARGE_SEMANTICS, FRAME_ASSIGNMENT, C7_C8_TRANSFER, WALL_PARTITION, ROOT_ADMISSION, SELECTOR_LOGIC, LOCAL_CHECKER_SOUNDNESS, LOCAL_CERTIFICATE_IMPORT, G20S_PHYSICAL, WALL_CONTRADICTION, KEY_W_ELIMINATION. `OPEN_ONE_PAGE.md` says "no separate missing analytic argument is currently identified". That is true only if these fourteen are taken as premises.
- **Section 8** contains no geometry beyond its last line. Its whole content is G20S_PHYSICAL: a uniqueness theorem for sixteen squares in a window of half-width 1/5 and angle 1/10 rad. I could check only the trivial part: the exact layout has an axis-parallel square at (L-1/2, L-1/2), which contradicts the strict inset of Section 2. I could not check the rigidity. This is "not shown in the text", not "wrong".
- **Section 3's** bound sum psi <= M/Gamma uses "core", "site", "row", "Mobius atoms", "mask feature", "outer weights", M and Gamma without definitions. A reader cannot verify the charge argument from this text. The consequences drawn from the bound (4/4/0, 4/0, PT arithmetic) are correct.
- **What closes it:** either state in the theorem that these fourteen are hypotheses with pinned proofs elsewhere (and list them on the one page as "accepted, not re-proved here"), or include their proofs. The final assembly review must read those proofs; this packet does not let it.

### F3 — PACKET DEFECT: `OPEN_MARKER_MAP.json` binds two markers to the wrong obligations
- **Place:** the entries for line 140 and for the second marker of line 152, token `[OPEN: LOCAL_JPA, LOCAL_JPWS, LOCAL_JPW13]`.
- **Why:** both have `kind: wall_capture` and `remaining_ids: [PW_2, PW_6, PW_7, PW_8]`. They should name LOCAL_JPA, LOCAL_JPWS, LOCAL_JPW13. The accompanying note says the "exact mapping of every OPEN occurrence" was verified; for these two entries it is not exact.
- **The count is right.** The skeleton has ten bracketed `[OPEN` strings. One is the legend `[OPEN: ids]` on line 3; nine are real (lines 7, 68, 90 twice, 92, 140, 152 three times). The map has nine entries.
- No obligation is lost: the local obligations still appear under line 7, under the third marker of line 152, and on the one page.
- **What closes it:** regenerate the two entries and record it as a revision of the packet.

### F4 — WEAK: the wall-strip capacity inequality is asserted, not derived
- **Place:** Section 6, "a separating axis with absolute components a,b would require a*w+b*H-b*(a+b)/2>=1".
- **Why:** the bound uses |dy| <= H - (a+b)/2. That is immediate only when the square that owns the axis is the one nearer the wall. When the other square (direction phi, arbitrary) is nearer, one needs h_j(n) + b·h_j(e_y) >= 1/2 + b(a+b)/2 for all phi.
- **It is true.** The left side is concave in phi between the break points phi = 0 and phi = direction of n. Its values there are (a+b)/2 + b/2 and 1/2 + b(a+b)/2, and the difference is (1-b)(a+b-1)/2 >= 0. So the stated inequality is the right necessary condition, with both squares parallel as the worst case. The text should say so.
- **Verified exactly:**
  - The quartic coefficients [1-w, 1-2H, 4, -1-2H, 1+w] follow from the substitution.
  - All Bernstein coefficients on 128 subintervals are positive (least 0.005039 for k=3, 0.005190 for k=15).
  - H = 1411/1000 - (U-C)/2 and 143/100 - (U-C)/2, so the wall used is that of the C box, which is the safe side.
- The margin is thin: 1 - (a·w + b·H - b(a+b)/2) >= 0.0037 for k=3 and 0.0036 for k=15.

### F5 — WEAK: "forces an E occupant" does not by itself give a new parent
- **Place:** Section 3, "A strict bound of 23 therefore forces an E occupant". Section 6, "forces its literal target by Section 3. The reviewed target geometry identifies the occupant".
- **Why:** the deduction is correct, but the occupant may lie in E∩H; that is, it may be the marker parent or the trigger parent itself. psi is high-first, so such a parent scores 4, and the contrapositive only excludes "no parent in E at all".
- The text treats this for label 12 only ("marker-minus-target construction"). For the other eleven labels, "a parent with a new label" needs target ∩ (marker ∪ trigger region) to be empty, boundaries included.
- The text says the 136 cross-label pairs of targets are disjoint. It does not say that the branch's trigger slot and the half-marker are among the seventeen regions of each profile. I could not check this from the packet: not shown, not known to be wrong.
- **What closes it:** one sentence naming, per branch, the trigger region and marker as members of the separated family.

### F6 — WEAK: the endpoint of the removed lower exit is not shown in the text
- **Place:** Section 5, "The removed lower exit includes its gate endpoint and is impossible by KEY_W".
- **Why:** class sets are closed and the exit is closed, so the claim needs KEY_W's low arc to start strictly above 61301/200000. The text never gives that number.
- In the hash-pinned KEY_W file the gate arc is [30651/100000, 44941/100000], and 30651/100000 - 61301/200000 = 1/200000 > 0. So the claim is true.
- Wording also differs: the text says "below the current T9 gate"; the manifest (`KEY_W_ELIMINATION`) says "below the old T9 gate".
- **What closes it:** quote the endpoint and use one word.

### F7 — WEAK: the C7/C8 transfer by reflection is legitimate, but the text does not say why
- **Place:** Section 4, "The accepted E07A pair implication and common reflection already yield the C7/C8 target consequences".
- **Why:** the frame was fixed by a reflection that puts the marker occupant's direction in [0, pi/4]; a second reflection leaves that half frame. The step is valid only because E07A's high class is the all-direction hexagon (mirror-symmetric about x = 1169/500), so the budget applies to the mirror image of any packing with the marker occupied. I confirmed this in the pinned E07A file.
- The text should state it. It also calls E07A a "pair implication", while the file calls itself a one-sided statement for label 7.

### F8 — MINOR: status tables
- `MANIFEST_TABLES.md` lists C_7 and C_8 as "Bound 20, COUNTED" with literal class hashes, in the same table as budget receipts. They are derived occupancy consequences without a budget receipt (the text says so). The column should differ.
- The preface's "independently accepted" conditional composition refers to manifest `820402a6...` (11:20), not to the frozen `b251fe25...` (14:34). Nothing reviewed the composition of the frozen manifest.
- The base table has 51 rows because the slab SL11_T020 is printed with the 50 base rows. "46 of 50" is right.

### F9 — MINOR: overloaded or undefined terms
- **"marker"** means both the all-direction hexagon (orbit bound, pair files, E07A) and the half-marker with directions in [0, pi/4] (L, C, KEY_W, P files). Sections 3 and 6 say "the marker is occupied" for both.
- **"core"** means a closed set inside a square (Section 3) and the rigid part of the layout (Section 8). "45 exact-root core deviations" is never defined: sixteen parents have 48 coordinates, and the text does not say which three are left out.
- **Two charts in Section 8.** The window G20S is in the rational-reference chart xi; the conclusion "deviations zero" is relative to the exact root. The manifest says this; the text does not.
- **"label" and "role"** are used for the same thing ("role 8", "role9").
- **Label map missing.** Capture labels differ from the construction labels of Section 1 and no table gives the map. From the pinned files: capture 2 = construction 5, 3 = construction 2, 4 = construction 6, 7 = construction 4; 8, 9, 12, 13, 15, 17 agree.
- **Letters with several meanings:** L (side; statements L_k; regions L9, L17), R (cap; R0), C (cap; statements C_j), T (slack; trigger), t (root coordinate; count in "(t-q)"; t9), H (union M∪T; wall distance; H0), Q (cell; family; JQ), S (side; slot S_k), E (low union; E07A).
- **"(t-q)", m, h, N(V)** in Section 4 are "in the notation of FRAME_L9", which the packet does not contain.
- **Three angle conventions:** theta9 in [0, pi/2), theta_k in [-pi/4, pi/4), marker in [0, pi/4]. Gates are in tan-half (1/20, i.e. 0.09992 rad), the tube in radians (1/10), file comments say "0.0999". They are compatible; the text should say so once.
- **Undefined in the frozen text:** WC, A_Q, S_k, TT, "4/4/0", PM/PT/PS/PSS/PSE/PW/PB/HULLW, "slab factor".
- **For the audit lead, not a manuscript defect:** L = 4.675530093604550951634..., so "S* = 4.675530093604551..." is the rounded-up cap R, not a truncation. R - L = 4.84e-17.

### No finding on these points
- **(i) Symmetry and seams.** The marker orbit has four images (the hexagon is symmetric about x = 1169/500). A quarter turn and then one reflection fix the frame; nothing later uses a per-square reflection. x9 = 53/100 and y9 = 129/50 belong to closed sets on the side that owns them. y9 = 13/5 belongs to AQ (closed), so the L rows give nothing there and the middle profile is the right owner. Subject to F1.
- **(ii) Quantifiers.** Every class statement is universal over packings of side <= C in the fixed frame; hypotheses enter only through occupancy. A clause alternative is a universally valid implication, so the choice per clause is free. The same class file serves the m and p clause of a branch pair (checked in the manifest).
- **(iii) Strictness.** sum psi <= M/Gamma < B is strict and the lower counts are >= B, so the deductions hold. They hold at side L because L < C. I checked the arithmetic of 137/8, 145/8, 20, 161/8 and 23.
- **(iv) Side transfer.** No gap. The argument never uses 4.674. A packing of any side S0 < L has F_U poses p + (U-S0)/2. Admission uses c - (U-L)/2, the corner chart of the normalized packing in [0,L]², which lies in [0,R]² with the same poses. So every side below L is covered at once; there is no interface with the lower bound to check.
- **(v) Section 8.** The final deduction is valid given G20S_PHYSICAL and the JG record. See F2 for what I could not check.

## 3. What I verified myself, and how

All scripts and their `.out` files are in the review folder. Standard library only; the longest run is 14 s.

1. **Upper bound, exactly** (`check_upper.py`, `check_upper.out`), written from `UPPER_FORMULAS.md` only.
   - Method: I eliminate b from F and G by pseudo-remainder (eliminant of degree 40, squarefree part 26). The eliminant is strictly monotone with a sign change on [t0 - 1e-12, t0 + 1e-12]. I then work in Q[x]/(m), with m the degree-18 factor that vanishes at t*. Zero tests are exact (gcd with m); signs come from a rational enclosure of radius 1e-140.
   - Root: F(t*,b*) = G(t*,b*) = 0 exactly; the root is unique in the box; |t*-t0| <= 3.8e-61, |b*-b0| <= 4.9e-61.
   - Side: L = 4.6755300936045509516341112704831466487671...; L < R < C < U; s, c, d, e, T > 0; both tilted bases are orthonormal.
   - Walls: 15 exact contacts, 53 strict, 0 violations.
   - Pairs (four edge-normal axes per pair): 21 exact contacts, 115 strict, 0 overlaps; least strict gap 0.0237377 = T/3.
   - These are the counts the text gives for H256. **The layout is a valid packing of 17 unit squares in [0,L]².**
2. **Section 2.** The identity p + (L-S0)/2 + (U-L)/2 = p + (U-S0)/2 and the strict inset. No generality is lost: any S0 < L is treated and no minimizer is assumed.
3. **Small exact checks** (`small_checks.py`).
   - (1+rho)² > 2; marker diameter² = 493/1250; the quarter turn of 591183/1408817 is -408817/10^6.
   - Gaps 1/200000 and 974949/14197000000; clipped L9 diameter² = 0.4627.
   - Both wall-strip quartics.
   - The decision list is a partition (30870 atoms, the number in `CASE_PARTITION.json`).
4. **Open list against the manifest** (`manifest_queries.py`).
   - Base rows: 46/50 COUNTED; open are exactly PW_2, 6, 7, 8.
   - Clauses: 31/84 COUNTED, 53 open. Roots: 8/11; open are JPA, JPWS, JPW13.
   - The 30 budgets named on the one page all exist in the manifest and all have bound 23. Every one of the 53 open clauses has at least one of them as an option.
   - Their extra premises are L_3 (8 budgets), L_15 (8) and none (14); L_3 and L_15 are COUNTED.
   - No COUNTED clause lacks a COUNTED option.
   - `OPEN_ONE_PAGE.md` is complete against the text, apart from F2.
5. **The known packing against every class statement** (`optimum_vs_classes.py`, `optimum_controls.py`).
   - Idea: a statement "sum psi < bound for every packing of side <= C" must hold for the packing of side L.
   - Scope: I evaluated psi (Section 3) for all 172 hash-pinned class files of the manifest (50 base, 1 slab, 121 selectable; every hash matched).
   - Members: nine members of the optimal family — sliders at their ends, the pocket square (capture label 4) turned by +7.0° and -5.8° and lifted, and the south-east corner square slid left by the whole play. All nine are valid packings (float separation check).
   - Result: **no statement is violated.** Scores are 16 to 20 against bounds 17 to 23, and no pose is within 1e-7 of a slot boundary.
   - Controls: the evaluator reports a violation when I turn square 9 to 0 (KEY_W) or displace capture label 3 (L_3).
   - Two facts worth knowing: the pocket square can turn by about 7.4°, more than the 5.72° gate, which is harmless because label 4 is direction-free in L_4 and in the JG root; and the south-east corner square is a third slider.
   - This step read files outside the packet. All were hash-pinned by the frozen manifest and I checked each hash.
6. **Packet consistency.** Every line of `FINAL_SECTIONS.md` after its header is verbatim in `PROOF_TEXT.md`, except the Section 4 paragraph with the omitted OPEN sentence. `PROOF_SKELETON.md` is `PROOF_TEXT.md` plus the status snapshot.
7. **From the pinned JG root file.** The label 9 support end before rounding is -0.0098965702, above the cut -9897/10^6 by 4.3e-7. Label 4's root arc covers every direction. Both agree with Section 7.

## 4. What I did not check

- Any exact receipt: no class budget, no local tree, no leaf, no checker run. COUNTED statuses are taken as given.
- The charge argument behind sum psi <= M/Gamma (F2), and the checker that implements it.
- G20S_PHYSICAL (the rigidity theorem) and the JG contraction. I did not test rigidity of the corner square numerically.
- ROOT_ADMISSION: the 136 separations per profile, the seventeen capacities, the label 12 union, the root inclusions of targets, the quarter-turn comparisons.
- FRAME_L9's notation and the "five distinct high parents" separation in Section 4; I checked only the arithmetic.
- The Q and PW trigger geometry in the three wall cases, JQ EMPTY, and its relation to the "second optimum" that the L files mention in a slot label.
- The fallback catalog (624 options), the PSE alternatives, the reserve seal K. The algebra of Score_D = max(Score_D1, Score_D2) in Section 6 is correct as stated.
- The H256 checker and the "endpoint-feasibility" member; I re-proved the H256 member from the formulas instead.
- `OPEN_DEPENDENCIES.json`, `REMAINING_CAPTURE.json`, `BRANCH_DEPENDENCIES.json`, `CANDIDATES.tsv`, `PACKET.json`, beyond what the queries above touch.
- Check 5 is a float evaluation on nine packings. It can find a false statement; it cannot prove one true.

