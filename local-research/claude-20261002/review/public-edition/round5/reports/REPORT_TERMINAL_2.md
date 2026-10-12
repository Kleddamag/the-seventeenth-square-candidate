Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line.

NO GAP FOUND in the three reviewed parts of G20S_PHYSICAL (finite-row necessity and rebuild; raw stop cuts; the two raw-to-root transfers). Interface assumptions I did not re-prove are listed under (5).

FINDINGS (in order of seriousness; none is an error in the mathematics)

F1 (documentation, no numerical effect). In the files I read there is no written derivation of the remainder terms of the finite rows, in particular of the parallel-pair error `D m^2/2 + m dr + q^2/2 + q^3/6 + taumax q^3 + (D m + dr)(q + q^3)` (uniform.py line 251). independent_model.py (4d9954c7) rebuilds the rows from polynomials but uses the same three remainder formulas (its E1, E2 and the parallel error are the kernel's expressions). JUDGEMENT: its agreement therefore confirms the implementation of the kernel, not the validity of the remainders. I derived all remainders by hand (section 2) and tested them numerically against the true separation functions (section 3); they hold.

F2 (scope wording). finite-entry-stop-pruning/root-producer/PROOF.md, entry-producer/PROOF.md, PRUNING.json and rational-entry-review/REVIEW.md all state "17 actual unit squares, free 4". The sixteen-square use rests on one paragraph of the corollary THEOREM.md (634bb045, section 2). My own derivation of the cuts and transfers uses only squares 9, 11, 13 (cuts), square 2 and its right wall (a* >= 0), square 8 and the top wall (side floor), and per-label affine maps. JUDGEMENT: the sixteen-square reading is correct.

F3 (stale status strings). root-interface.json says "PRODUCER_PASS_PENDING_INDEPENDENT_REVIEW" and "raw_coordinate_transfer_proved: false"; PRUNING.json says "...PENDING_INDEPENDENT_ENTRY_REVIEW"; producer README and RESULT say "pending independent replay". Same remark as the previous reader's question 4.

F4 (harmless). finishing-continuation/model-16.json (the abandoned partial round) and proposal-timeout-retry/model-16.json are the same file (sha 7fe9ad6833f2dcf6), because both were built on the round-15 outgoing box. Only the complete round 16 of proposal-timeout-retry enters the chain.

F5 (property of the builder, not a defect). Moving the upper bound of coordinate 0 of the round-2 box by 1e-15 changes no row, because norm_upper rounds on a 1e-9 grid; 1e-6 changes 2 rows. The rows are still valid on either box.

Disclosure: I read proposal-timeout-retry-independent-review/REVIEW.md (a stored review) after finishing my hand derivation of the row types but before running my rebuild. The producer README names an <author reply> file; I did not open it.

(1) TABLE
G20S_PHYSICAL, part 1 (necessity of finite rows, rebuild) | HOLDS | hand derivation of all four row types against uniform.py lines 93-273 and pilot.py helpers; rebuild.py: 17/17 rounds, 12929 rows, kernel rows identical to saved rows, independent builder identical in every coefficient and right-hand side; box chain and 1564 dual bounds replayed, 0 mismatches.
G20S_PHYSICAL, part 2 (raw stop cuts) | HOLDS | transfer.py: own exact-interval derivation on the root domain core <= 501/100000 with the full padded slider box; raw cuts hold with margins 1.86e-5 (b), 7.05e-5 (b+z), 6.91e-5 (z).
G20S_PHYSICAL, part 3 (two raw-to-root transfers) | HOLDS | transfer.py: reference drift max 4.319e-17, angle drift <= 1.07e-60; root core <= 1/200 + 4.32e-17 < 501/100000 and <= 1/10000 + 4.32e-17 < 1/5000; a* >= 0 from the right wall of square 2.
The rest of G20S_PHYSICAL | NOT READ.

(2) RESTATEMENTS

PART 1. Given: 16 unit squares (labels 1..17 without 4) in [0,S]^2 with pairwise disjoint interiors, S <= S* < Sref = 4675530093604551/10^15. Chart (uniform.geometry): centre_i = p_i + (h_{2i}, h_{2i+1}) for ordinary i; centre_2 = p2 - a(1,0) + h3(0,1); centre_11 = p11 + h20 u11 - b v11; centre_13 = p13c + h24 u13 + z v13 with p13c = p13_file - (T0/3) v13 and T0 = c0(c0+4-Sref); square i is turned by omega_i (radians, variable 34+i) from its rational reference axes. The 100-vector x holds 29 positions, 16 angles, three zeros (6, 7, 37), a, b, z (2, 21, 25), x51 = S - Sref, and 48 true products w*omega. Required: if x lies in the incoming box B_k then every row a.x >= b of model k holds. Rows are weak inequalities and all boxes are closed.

Row types, each derived by me and compared with the code (J is the quarter turn, R(.) a rotation):
- Wall (lines 179-190). A corner is c_i + R(omega)v, and |R(omega)v - v - omega Jv| <= |v| omega^2/2 by Taylor with integral remainder. So the linearised corner plus |v| r_i^2/2 is >= 0, and the same with S - corner using a[51] = 1 and constant +Sref. Matches the code.
- Separating-axis alternatives (lines 192-218). Disjoint interiors imply that one of 8 directed alternatives holds (owner in {i,j}, axis of the owner, sign): g_v = R(omega_o)n.(c_j - c_i) - 1/2 - n.R(omega_t - omega_o)v >= 0 for all four corners v of the other square. The corner set is symmetric, so one formula serves both owners. 19 pairs give 152 alternatives.
- Linear expansion (corner_terms, error1). true g - linear = (R n - n - omega Jn).(d + delta_w) + (R n - n).delta_h - n.(R(eta)v - v - eta Jv), bounded by D r_o^2/2 + r_o dr + |v| eta_max^2/2. Here D bounds |d + delta_w| over the slider box and dr bounds |delta_h|. The term omega_o (Jn).delta_w is carried exactly by the product columns. Matches the code.
- Second-order expansions (error2). Cubic remainders D r_o^3/6 + dr r_o^2/2 + |v| eta_max^3/6. The coefficient -(n.(d+delta_w))/2 of omega^2 is replaced by its maximum over the slider box (legitimate because omega^2 >= 0). The envelope is a secant for a convex coefficient and tangents at 0 and at the midpoint for a concave one. The product omega_o * (Jn.delta_h) is bounded by the two McCormick upper planes. Each expansion is an upper bound of g_v on the box. Matches the code.
- Exclusion of alternatives. `coarse < 0` implies g < 0 at the extreme corner; I checked the bound term by term. Otherwise an alternative is dropped only if some upper expansion has maximum < 0 over the box; true_support substitutes the true products at the 8 slider-box vertices, which is exact because the form is affine in each slider. If exactly one alternative survives, its rows are necessary.
- Parallel rows (lines 227-260). The two survivors have different owners and the same n. Put mu = (omega_i+omega_j)/2, eps = (omega_j-omega_i)/2, n_m = R(mu)n, X_m = n_m.Delta, tau_m = Jn_m.Delta. Alternative A or B gives cos(eps) X_m + |sin(eps)||tau_m| >= cos^2(eps) + |sin(eps)|cos(eps). Hence X_m - 1 >= |eps|(1-|tau_m|) - eps^2/2 - |eps|^3/6 - 0.335|eps|^3|tau_m| for |eps| <= 1/10. Passing to X = n.Delta and tau' = tau0 + tauw.w costs D m^2/2 + m dr and q(D m + dr). The sum is within the code's error. Result: n.Delta - 1 + tau' mu + s eps (1-|tau'|) + error >= 0 for s = +1 and -1, which is exactly the coded row. It needs a constant sign of tau' on the box and |tau'| < 1; the code omits the pair otherwise.
- Product rows: the four McCormick inequalities, each a product of two nonnegative factors.
- Rounding (row()): coefficients are rounded to 10^-15, the loss sum |a - aq| * radius is paid, and b is floored. Valid.
- Extra row -b - z >= -49/2000 and the initial cuts: part 2.
In all 17 models: 11 pairs with one survivor, 8 parallel pairs, 0 omitted, 0 sign crossings, 27 of 152 alternatives alive. Row counts 597, 761, 761, 761, then 773 for rounds 5 to 17.
Side interval: p8_y + 1/2 - 1/200 - Sref = -1/200 - 5.2e-18 > -1/50 (exact fraction checked); S <= S* < Sref gives x51 <= 0.

PART 2. Root chart: reference bridge.layout(t*, beta*). Identities hold identically in t; I recomputed them from the layout with intervals, residual below 3e-59: u.(P11-P9) = c(1-s), v.(P11-P9) = -1, u.(P13-P11) = c-s, v.(P13-P11) = -1 - T/3, with T = c(c+4-S*). Domain: all 45 root core coordinates <= eps0 = 501/100000 (only h9x, h9y, h20, h24 and theta9, theta11, theta13 are used); b* in [-1/20 - 1e-12, 1/5 + 1e-12], z* in [-1/5 - 1e-12, 3/40 + 1e-12]; no restriction near the root in the sliders.
c11 - c9 = X u - N v with X = c(1-s) + h11 - u.h9, N = 1 + b* + v.h9. c13 - c11 = X u - N v with X = c - s + h13 - h11, N = 1 + T/3 - b* - z*.
Non-overlap requires for some owner o and n in {+u, -u, +v, -v}: R(theta_o)n.Delta >= 1/2 + (half-width of the other square) >= 1.
Over the whole padded box at eps0:
- (9,11): N in [0.94294, 1.20706], X in [0.26436, 0.28849]; suprema of the projections: +v -0.9415, +u 0.2945, -u -0.2583.
- (11,13): N in [0.74874, 1.27374], X in [0.11803, 0.13807]; suprema: +v -0.7480, +u 0.1445, -u -0.1117.
All are below 1, so only -v survives for either owner. That gives 1 <= N cos(theta) + X sin(theta) <= N + eps|X| (N > 0), hence b* >= -eps(c+s) - eps|X|max and b* + z* <= T/3 + eps|X|max.
My exact values: b* >= -0.008501454891, b*+z* <= 0.024429483547, z* <= 0.032930938437.
Packet values (weaker, consistent): -8517/10^6, 0.024439143195, 0.032956143195. I confirmed its formulas sum = upper(T*/3) + (14/100)(501/100000) and z = sum + 8517/10^6 as exact identities, and its constants c+s < 141/100, |c(1-s)| < 277/1000, |c-s| < 129/1000, |X_1113| < 14/100, bracket < 17/10.
Raw cuts: b = b* - E_b and z = z* - E_z with E_b = -6.482e-18, E_z = +8.523e-18 (part 3). So b >= -213/25000, b+z <= 49/2000, z <= 33/1000 hold with margins 1.86e-5, 7.05e-5, 6.91e-5 from my bounds; from the packet's own bounds the margins are 3.0e-6, 6.09e-5, 4.39e-5.
Answer: the excluded part is proved empty for the WHOLE finite entry. The argument is a direct implication for every configuration in the root domain, with the full b and z ranges; that domain contains the image of the full raw entry by part 3. Nothing is localised near the root.
Same derivation at eps = 1/5000: b* >= -3.371e-4 (claimed -17/50000), b*+z* <= 0.0237634 (claimed 3/125), z* <= 0.0241005 (claimed 1/40). All hold.

PART 3. Raw chart: reference from upper-packing-certificate.json (rational centres, half-angle tangents t0 for squares 9..14 and -beta0 for 16, side Sref), with p13 corrected by -(T0/3)v13. Root chart: bridge.layout at the root (t*, beta*) of the two endpoint polynomials, axes from t*, beta*.
Root enclosure (own Krawczyk test): unique root in the box of radius 1e-12 around (t0, beta0), verified radius 5.3e-61. S* in [4.675530093604550951634111270483146648767143855..., same to 60 digits]. Sref - S* = 4.837e-17 > 0.
Map, with delta_i = p_i - P_i*:
- ordinary labels: h* = h + delta_i;
- square 2: h3* = h3 + delta_2y, a* = a - delta_2x;
- labels 11 (sign -1, w = b) and 13 (sign +1, w = z): h* = u*.delta + h(u*.u) + sign w (u*.v), and w* - w = sign v*.delta + sign h (v*.u) + w (v*.v - 1), evaluated with the same raw w;
- angles: omega* = omega + 2 atan t0 - 2 atan t*, drift <= 2|t0 - t*|.
Results over the full boxes: max |delta_i| over the 16 labels = 4.319e-17; T0/3 - T*/3 = -1.2385e-17; angle drift <= 1.07e-60; E_a = a* - a = -4.319e-17, E_b = -6.482e-18, E_z = +8.523e-18. The slider-dependent terms w(u*.v), w(v*.v - 1), h(v*.u) are below 1e-60 because the raw axes use the midpoint tangent.
Transfer A: raw positions <= 1/200, angles <= 1/400, full raw sliders imply root core <= 1/200 + 4.319e-17 < 501/100000 (margin 1.0e-5); b*, z* inside the 1e-12 padded box; a* <= 8/25 + 1e-12. Blind transfer gives a* >= -4.3e-17; a* >= 0 follows instead from P2* = (S* - 1/2, 1/2): a* = S* - 1/2 - centre2_x >= S* - S >= 0 (right wall, S <= S*).
Transfer B: raw core <= 1/10000 (also checked with the actual final box, radius 64007486789/10^15, and the stopped sliders) implies root core <= 1/10000 + 4.319e-17 < 1/5000. My exact upper bound, 100000000000043193652880187769.../10^69, agrees with the packet's exact_root_core_upper_from_transfer to all printed digits.
The packet's slider errors (PRUNING.json root_transfer) agree with mine: -4.3194e-17, -6.482e-18, +8.523e-18; core_upper 1/200 + 4.319e-17.

(3) SCRIPTS (all in <reviewer scratch>/, run with python3 -B)
- rebuild.py. For each of the 17 rounds: model file sha equals the certificate's; rows rebuilt with uniform.model on the saved incoming box plus the extra row and compared for full equality (a, b, label): equal 17/17. Rows rebuilt with independent_model.independent_model (called directly, stored verdict not used): equal in a and b for all rows and in labels for all geometric rows, 17/17. Round-1 incoming box equals the box I built from the theorem text plus the three cuts. Incoming box of round k+1 equals the outgoing box I recomputed for round k (exact_dual over the saved rows, outward rounding, product refresh). 1564 bounds, 0 mismatches; 92 objectives per round; final max core 64007486789/10^15 < 1/10000. Total 12929 rows. Log: rebuild_all.log.
- controls1.py, controls1b.py (negative controls of the rebuild). Round-2 box perturbed: b lower bound back to -1/20 gives 50 rows differing; coordinate 34 +1e-15 gives 6; coordinate 40 +1e-12 gives 38; coordinate 15 +1e-9 gives 12; a upper +1e-9 gives 34; z upper +1e-9 gives 38; coordinate 0 +1e-6 gives 2. Both builders give the same counts. Coordinate 0 +1e-15 and the side bound give 0 (F5; the side enters no remainder). Saved rows perturbed: row 300 right-hand side +1e-15, one coefficient of row 10 +1e-15, row 500 deleted; each is detected as a mismatch.
- controls1.py (numerical falsification, floats). For rounds 1, 2, 17, 1500 points of the incoming box each (vertices, uniform, mixed) with true products: every saved row value minus the true quantity (wall slack; g_v for pair rows; max(gA,gB)/cos(eps) for parallel rows; 0 for product rows). 0 violations at tolerance 1e-13. Minimum margins, round 1: wall 8.9e-9, pair 7.7e-8, parallel 4.5e-5. Round 17: wall 2.6e-15, pair 2.0e-15, parallel 7.5e-13. JUDGEMENT: the round-17 margins are at float resolution, so that round is a weak test; rounds 1 and 2 are the meaningful ones.
- controls1c.py (control of that test). Right-hand sides of three round-1 rows raised by 1e-7 (wall), 1e-6 (pair), 1e-4 (parallel): exactly those three rows are flagged.
- transfer.py (parts 2 and 3; own interval class; layout retyped and compared with bridge.layout at a rational point; polynomials compared with bridge.POLYNOMIALS). Output as in section 2. My root box overlaps the pinned bridge.root_enclosure box (radius 1e-55).
- Controls of transfer.py. eps = 51/10000: the b and z cuts fail (margins -1.35e-4 and -9.8e-5). eps = 1/100: all three cuts and the constants 17/10 and 14/100 fail. Raw position radius 501/100000: "root core < 501/100000" fails by 4.3e-17. Without the T0/3 correction of p13 (transfer_nocorr.py): E_z becomes 0.0237 and the reference drift 1.8e-2, so z* leaves the padded box and the transfer is invalid; the correction is therefore load-bearing and it is present in uniform.geometry (lines 50-52).

(4) SHA256 (first 16 hex)
019ce089aa4d531f uniform.py (full-gate/producer/instance/research/uniform-capture-20261007)
0870bec5b2243e7a pilot.py (joint-capture-20261007, same instance)
24e296f5995abc94 upper-packing-certificate.json
a3b496ca0422b481 bridge.py; 8d31d7547394117f root_geometry.py (read only); ef8069b30cd1336a upstream-root-certificate.json (comparison only)
4d9954c7e8539435 independent_model.py (identical in all four review folders)
6ac1dd6924225e60 finite-stopped-contraction/producer/run.py; 32354f36e94ca483 producer/README.md
Models 1..17: b76c209a3b56d7f1, 8f97eca45ddc2b57, 68b196608d399209, d8f6b7d2a8aa3813, e52a4efc4d0e6116, 360cf5d51c072349, 1e21c617c7cdca61, 166e26749faca86a, 05821612401b4e07, e66e3cfdf1448cef, eb8ebda9d108564a, 89ec874925ecd5a2, e8db3f3e54b7e873, 9560264bb7bb88c1, 6f9f86fc1ebf45eb, 7fe9ad6833f2dcf6, dd3871979f6f9ff3. All 17 hashes, the four certificates, uniform.py, pilot.py, the reference file, bridge.py, PRUNING.json and the rational-entry interface occur in the sixteen-square corollary's receipt and manifest files.
Certificates: 2e1fe0586b161e87 (producer), 31ed99eeafff5fe6 (continuation), 573103065292ad04 (finishing-continuation), a98263696c3aebef (proposal-timeout-retry)
634bb04591d597bd sixteen-square-corollary/producer/THEOREM.md; 91aa01bea5eb6246 its independent-review/MANIFEST.json
a2ff41d2090adbd0 finite-entry-stop-pruning/root-producer/PROOF.md; cf079be5b0824087 entry-producer/PROOF.md
86487b6c108365fd root-interface.json (not bound directly in the corollary receipt; bound through the root-review manifest 5df4e5b559ff071f); 0bbb358ac5b9860e PRUNING.json
ae34d7be2525232a rational-entry-review/MATHEMATICAL_INTERFACE.json; efb79df77e26703d its REVIEW.md; 537811d96b2f53c6 its MANIFEST.json
848e6d2bbb08f7b5 proposal-timeout-retry-independent-review/REVIEW.md
99d813ec5d1ffd1a PACKET.json (matches)

(5) NOT READ / NOT DONE
- The packet's own checkers were not run: the four finite check.py, check_join.py, root-producer/check_stops.py, root-review/check_root_stops.py, both check_transfer.py, check_corollary.py, sixteen-square audit.py and check.py. I replaced them by my own scripts; I give no verdict on those tools.
- entry-review/REVIEW.md, root-review/REVIEW.md, the "original exact reference-transfer lemma" text (review seal 986e95c5...), the other finite REVIEW.md files, the body of the sixteen-square REVIEW.md, analytic_envelope_text.md, normalized_division_text.md, full_gate_analytic_review.md, fresh_local_review.md.
- relational.py, verify.py, rigidity.py; pilot.py beyond lines 1-190 and the function outward.
- The floating LP proposals were not rerun (they are not proof premises).
- Interface assumptions not re-proved: that the root of the two polynomials in the 1e-12 box, with bridge.layout, is the S* = L of the claim and the chart of the normalized stage (ALGEBRAIC_ENDPOINT and the previous reader's part); I only confirmed existence and uniqueness in the box and S* = 4.67553009360455095163.... That a physical configuration actually enters the finite entry (tree side) is not in my scope.

(6) QUESTIONS TO THE AUTHORS
1. Which pinned text contains the derivation of the finite-row remainders, in particular the parallel-pair error of uniform.py line 251? If none, a half-page lemma (the mean-frame argument in section 2) should be pinned; the "independent" builder shares the formula.
2. Please restate the scope of finite-entry-stop-pruning and rational-entry-review for sixteen squares, or pin one sentence saying that only squares 9, 11, 13, 2 and 8 and their walls are used.
3. Answer to the previous reader's question 3, for confirmation: the statement "the entry tube lies in the root domain core <= 501/100000" is entry-producer/PROOF.md, section "Exact transfer", with the number in PRUNING.json root_transfer.core_upper; its independent check is entry-review/check_transfer.py. Is that the intended file of record?
4. Stale "pending review" status fields (F3).

