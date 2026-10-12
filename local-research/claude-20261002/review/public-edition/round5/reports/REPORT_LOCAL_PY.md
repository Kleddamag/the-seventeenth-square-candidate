Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line.

HOLDS WITH CONDITIONS: (1) the runs of record of G20S and HW must have used the Python checker without --packing, --expect-packing-sha256 or --no-packing-pin (I did not check their command lines); (2) control V1 could not be built as specified, because no node of HW has an unused sign assumption, and was replaced by two substitutes; (3) my reading is of the Python checker only.

FINDINGS (most serious first)

F1. No weaker test found. I read all 3,134 lines of checker/wxcheck_v30.py against SPEC_v3.0.md (885 lines, read completely first). JUDGEMENT: I found no place where the Python checker accepts something the SPEC does not allow. Details per block are in section (2).

F2. V1 does not exist as specified. scan_v1.py found 116 sign assumptions in the assume lists of HW (94 on direct children of the 47 sign splits, 22 inherited further down). All 116 are used by a round of their own node (an `asg` name or a P+ / P- declaration of that pair and class). G20S: 194 of 194 direct children use theirs (inherited ones not scanned). So a flipped sign on these trees always fails inside the node first, as LOCAL-2 saw. I ran two substitutes that reach the assume-list rule itself (V1 and V1x below). Both fail there in both checkers.

F3. Options that change what PASS means (wxcheck_v30.py 3097-3102, 3114-3115, 2932-2935). `--packing FILE` with `--no-packing-pin` or `--expect-packing-sha256 HEX` lets another reference file in (it must still have side = Sref and 17 squares, 506-511). Nothing else changes PASS: `--node` can only give exit 10, `--keep-going` cannot pass after a failure (3027-3028), `--paranoid` only adds a comparison, `--json` failing gives FAIL. No environment variable is read. JUDGEMENT: condition (1) above. The function check_certificate also takes the pin as a default argument (2887-2888), so a caller that imports the module can switch it off.

F4. Bookkeeping of the earlier reports. LOCAL-2 lists 466-478 both as read and as not read. REPORT_LOCAL_2C withdraws 2286-2326. Lines 1968-1986 are in neither LOCAL-2 list. The import reader lists 1899-1999 as read but says it did not read the par and wsup facts, whose availability tests are 1965-1981. JUDGEMENT: no longer matters, since I read all of these.

F5. Minor code notes, none weakening.
- Comment 1047-1048 speaks of "two indicator equalities"; is_equality_fact (390-394) is `circ` only.
- Docstrings 2443-2444 and 2625 still describe Ab = rho * P; the code (2458, 2648-2649) uses conj(gamma) * rho * P, which is the same under wx-cert-2.
- check_step repeats the parse tests (2295-2300).
- 2539-2540 is unreachable for a parsed node.
- A split or terminal node with an accepted `0` step keeps its kind (2581-2596); harmless, as the import reader said.

F6. The two checkers agree exactly on L at two real HW steps. For the bound step of V6b, C2's printed exact L equals C1's L as a fraction. For both V6 steps, both checkers accept value = L and reject value = L + 1e-40.

(1) OBLIGATION TABLE
LOCAL_CHECKER_SOUNDNESS (residue, Python checker) | CONDITION | whole file read; tests T1 to T4; controls V1 to V6. Conditions (1) to (3) above.

(2) BLOCKS: what the SPEC asks, what the code does, JUDGEMENT
Every "no weaker test" below is a JUDGEMENT.

- 1-115 (header, SPEC hash guard, OPTIONS, SCHEMA_V3). The only option table is {"paranoid"}. No weaker test.
- 116-308 (SPEC 10: strict JSON, numbers, labels, rotations). Floats, NaN and duplicate keys reject (141-151). Numbers must be strings matching the ASCII pattern (154-169). Labels and `eps` / `sign` / `k` are tested with `type(x) is int` or type-equal choice (225-256), so `true` and 1.0 reject. Rotations must satisfy g^2 + s^2 = 1 exactly (301). No weaker test.
- 309-333 (interval arithmetic). Exact; iv_mul takes min and max of the four products. Correct.
- 335-398 (base variables). Numbering only.
- 400-476 (polynomial helpers; SPEC 3, 5). p_add, p_scale, p_mul, p_lin are exact, with monomials as sorted tuples. sp_from_poly and sp_mul give integer-scaled forms with a positive denominator. No cached polynomial is mutated by any caller. Correct.
- 478-543 (SPEC 1, Reference). u_i from t_i, p_13 shifted by (T0/3) v_13 with T0 = u_9x (u_9x + 4 - Sref), frames (u, v) for 11 and 13. Matches.
- 545-758 (SPEC 10 names; parse_form_tokens, parse_fact_name). Unknown names reject. `sq`, `pol`, `ind` exist only under wx-cert-3 (682, 690). The tan condition G^2 + H^2 <= 1 is part of the name (714, 724). `ivl` only for Da, Db or an affine custom form (755-757). No cut on `0` (752). A custom form must be defined (644). No weaker test.
- 761-898 (parse_interval, parse_box, parse_option, parse_assumption, parse_forms, parse_base_variable, parse_qforms, parse_centre). Exact key sets through need_dict. o != t, i < j. Custom forms are nonempty, components pairwise different, not `0` and not `u:`. No weaker test.
- 901-1168 (parse_store, parse_round, parse_split, parse_close, parse_node; SPEC 10 list (W)). A store has exactly the five keys and exactly the labels of I; an arc entry with `c` rejects. At most one par declaration per (i, j, cls, kind) (1017). `kappa` is required for Pk and Ps and ignored for P+ / P- (1007-1014). A step on `0` must have sense lo (1035). 1 to 3 names per term (1044). A negative multiplier needs a `circ` fact (1049). Every name of every term is parsed whatever its multiplier (1046). Child count is 2, or the number of listed options; child ids are distinct (1107-1111). Node data: cos > 0, sin P- <= sin P+, lo <= hi, empty id rejected. No weaker test.
- 1171-1245 (SPEC 8, 10: regions and header). Schema string, packing hash, Sref by value, labels 16 or 17 as a JSON integer, 4 <= S_floor <= Sref, 0 < window alpha < 1, 0 < tube alpha <= 1, window and tube box ordered. No weaker test.
- 1249-1444 (NodeGeom; SPEC 2, 3, 4.1, 4.5, 4.6, 4.8). abar = rho * u, bbar = J abar. Da, Db, A, B, Cr, Sr as in SPEC 3. class_combo is the dictionary of 4.6 entry by entry, both axis cases of J n . d included. wall lo := X, hi := S - X. opt_poly has the sign -Sr for the pair (j, i). par_poly gives the eight polynomials of 4.6. wsup_poly is D_W - 1/2 -/+ (k/2) sigma. Test T1 confirms all of them against geometry at 40,776 values. No error found.
- 1447-1539 (initial store; effective, wsup_coefficients, ps_slopes; SPEC 4.3, 4.8, 4.6 Ps). Effective ends: only candidates with cosine > 0; larger sine on the minus side, smaller on the plus side. wsup needs V-_x > 0, V+_x > 0, V-_y <= 0 <= V+_y, with V = P * abar (not rho * P); kp, km as in the SPEC with the value 0 at a zero sine. Ps needs both effective ends, cos E > 0 strictly, sin E- <= 0 <= sin E+; kp, km with the value 1 at a zero sine. No weaker test.
- 1541-1694 (SPEC 3 store bounds, EMPTY test, 4.7). Base variables take no cut. Da and Db are the affine range capped by the cut; A and B from the capped components; Cr and Sr from the effective ends or [-1, 1]; class and custom forms by interval combination, then cap. EMPTY covers box, S, arcs, cut pairs (base variables too), pairs with a stored end, and forms with a cut. h_lo falls back to 1/2 unless all four quadrant conditions hold (1678). Exclusion is U < 1/2 + h_lo strictly (1692). Test T4 found SB containing the true value 353,520 times and 1/2 <= h_lo <= h 72,000 times. No weaker test.
- 1697-1725 (arc fact polynomials, 4.2 / 4.3). slo, shi, clo, chi, chord and tangent as in the SPEC. T4: 28,800 arc and 31,190 relative-arc values, all >= 0.
- 1728-1896 (declarations; SPEC 4.5 VALIDITY, 4.6 PRECONDITIONS, 4.10, guard rule).
  - opt: assumed, or the 7 others excluded (1752-1756).
  - par: the 6 other options excluded; cL > 0 strictly; P+ needs YU <= 1 + cL and (YL >= 0 or the assumption (i, j, K, +1)); P- is the mirror with (i, j, K, -1); Pk needs 0 <= kappa <= 1 - Ybar/(1 + cL); Ps needs that and cp >= 0, cm >= 0.
  - The sign assumption is matched with pair, class and sign (1773, 1778).
  - I re-derived Lemma P (all eight cases of P+ and P-, Pk, and the Ps chain) and the identity be - al = si Y/(1 + co). The store tests imply the lemma's hypotheses because co >= cL.
  - No weaker test.
- 1898-1999 (fact_poly; T4 availability). A cut needs its entry in the start store (1925). rarc needs both effective ends (1945). opt needs a valid declaration (1957). par needs a valid declaration of the same (i, j, K, kind) (1967). wsup needs the sign conditions (1978). asg needs the exact assumption (1984). No fact is built without its precondition.
- 2001-2098 (raw rule, SPEC 5). Rem = g - sum lambda * product, over a common positive denominator. Availability is tested for every term before the zero-multiplier skip (2045, then 2055). L = sum over monomials of min(R a, R b)/(D e) with D, e > 0. A monomial's interval is the repeated product of the base SB, literally, with no tightening of even powers. lower_bound_reference is the literal formula. T2: my own evaluation of L for a real HW step, without checker functions, equals the checker's L. T3: x^2 on [-1/10, 1/10] gets [-1/100, 1/100]. Correct.
- 2100-2254 (centred rule; wx-cert-3 only, not reachable for G20S or HW). The shift is expanded exactly with integer numerators; the constant term is dropped only for a zero centre; like monomials are combined; intervals are [SBlo - c, SBhi - c]. Correct as read; not tested by me.
- 2257-2434 (Certified, check_step, accept_store, run_round; SPEC 5).
  - lo: value <= L. hi: -value <= L with g = -form. `0`: L >= value and value > 0. The certified value is `value`. A `0` step gives none (2430-2431).
  - Store: S, box and arcs (cos > 0) against the old entry or the certified bound of the same form. A stored relative end needs an old R on that side, cos > 0, and the sine against the old R or the certified bound of Sr:i:j. A cut is tested against the old cut of the same name or the certified bound.
  - A fresh RoundEnv per round (2415). All declarations are tested, then all steps, then the store.
  - No weaker test, no wrong direction.
- 2437-2606 (terminal_failure, split_failure, check_node; SPEC 7, 8, 6). Rounds stop after an accepted `0` step or an EMPTY store. `infeasible` needs the `0` step or the EMPTY store. With `pair` it needs a non-EMPTY final store and all 8 options excluded. terminal and split reject an EMPTY store. Box split lo <= m <= hi; arc split cos M > 0 and sine inside; option split needs every unlisted option excluded on the final store; the sign split has no condition. _EmptyBound outside the EMPTY test becomes a rejection (2530-2531). No weaker test.
- 2609-2821 (tree pass; SPEC 6, 7, 8). child_failure: parent id; assume list equal to the parent's tuple plus the one split assumption (2691; +1 first, then -1, 2688); every box interval, with the split piece for the split coordinate; every arc by the containment test with the re-expressed centre; the side interval. Every edge is verified once. Ids are unique; the root is tested (parent null, no assumptions, S_lo <= S_floor, S_hi >= Sref, window inside). At finish: every listed child exists, no waiting child, no unverified parent, every non-root node listed once with a matching parent, every node reachable from the root. No hole found.
- 2824-3134 (driver). Every line is checked in full mode. Any exception in a node makes `failed` true and the verdict stays FAIL (2995-3001, 3027-3028). Errors of the gzip stream (truncation, bad CRC, trailing garbage) reject (2861-2863) and leave the loop as FAIL through 2910-2917. An empty line rejects (2875). PASS is set only after tree.finish() (3036-3037). Exit code 0 only for PASS in full mode (3122-3123).

The eight points. All JUDGEMENT.
(i) No float on a decision path. float() occurs only in _short (2330, messages) and round() only on the run time (2918). Every division is on Fractions or is integer `//`.
(ii) No wrong direction and no weak inequality where the SPEC is strict. I checked each comparison named above.
(iii) No fact without its precondition; see 1898-1999 and the declarations.
(iv) Zero-multiplier terms are name-checked at parse and availability-checked in evaluated rounds. T3 confirms rejection for an unavailable cut, asg, par and opt fact with multiplier 0.
(v) No tree-structure hole found.
(vi) See section (4).
(vii) See F3.
(viii) No failure becomes a pass. The one place an exception becomes evidence is empty_reason (1657-1660): an empty cap-cut intersection means the store is EMPTY, which is what SPEC 2 and 3 say.

(3) LINE RANGES (ranges.py, output in ranges_out.txt)
| reader | lines claimed read |
| LOCAL-2 (995 lines) | 116-308, 374-398, 466-545, 598-615, 673-760, 921-1248, 1466-1504, 1701-1727, 1842-1898, 2261-2400 |
| LOCAL (337) | 487, 887-898, 1282-1310, 1386-1411, 1414-1420, 1423-1444, 1455-1463, 1505-1518, 1521-1539, 1760-1797, 1975-1986, 2149-2182, 2184-2199, 2201-2228, 2309-2315, 2534-2538, 2613-2621, 2667-2709, 2727-2731, 3115 |
| import reader (714) | 141-151, 158-169, 296-303, 326-328, 1107-1111, 1118, 1211-1212, 1230-1237, 1266-1270, 1367, 1370-1383, 1631-1661, 1664-1680, 1682-1694, 1701-1725, 1880-1896, 1899-1999, 2002-2011, 2038-2059, 2061-2079, 2277-2283, 2286-2324, 2327-2330, 2333-2400, 2415-2432, 2441-2463, 2472-2488, 2551-2596, 2613-2621, 2624-2654, 2677-2680, 2685-2688, 2691, 2693-2706, 2737-2821, 3027-3037, 3097-3102, 3122-3123 |
| LOCAL-2B, LOCAL-2C | none |
Union as claimed: 1,787 lines. 1,535 of them are claimed by exactly one reader.
Complement as claimed (1,347 lines): 1-115, 309-325, 329-373, 399-465, 546-597, 616-672, 761-886, 899-920, 1249-1265, 1271-1281, 1311-1366, 1368-1369, 1384-1385, 1412-1413, 1421-1422, 1445-1454, 1464-1465, 1519-1520, 1540-1630, 1662-1663, 1681, 1695-1700, 1728-1759, 1798-1841, 2000-2001, 2012-2037, 2060, 2080-2148, 2183, 2200, 2229-2260, 2401-2414, 2433-2440, 2464-2471, 2489-2533, 2539-2550, 2597-2612, 2622-2623, 2655-2666, 2710-2726, 2732-2736, 2822-3026, 3038-3096, 3103-3114, 3116-3121, 3124-3134.
If LOCAL-2 is counted only where it does not contradict itself, the complement has 1,362 lines: the above plus 466-478 and 2325-2326.
LOCAL-PY read 1-3134, the complement and everything else. Unread in wxcheck_v30.py after me: none.

(4) SCHEMA BRANCHES (every use of SCHEMA_V3; the flag is set at 1210 and 1217)
- 682: `sq:` and `pol:` names are parsed only under wx-cert-3. Under wx-cert-2 they fall through to "unknown fact name".
- 690: `ind:` names likewise.
- 975 and 996: mode "ind" is a declaration only under wx-cert-3. Under wx-cert-2 the mode choice is ("opt", "par") and "ind" rejects.
- 1030 and 1032: `centre` is an allowed step key only under wx-cert-3. Under wx-cert-2 it is an unknown key, and step.centre is None for every step.
- 1146: `q:` keys of `forms` are taken out only under wx-cert-3. Under wx-cert-2 parse_forms rejects them by the name pattern, and qforms is empty.
- 1180 and 1182: `centre` of window and tube only under wx-cert-3. Under wx-cert-2 it is an unknown key and the centres are the identity.
- 2958-2961: report keys only.
Nothing else branches on the schema. Fact polynomials, SB, exclusion, store acceptance, closures and the tree pass are one code path for both. Data-driven consequences under wx-cert-2: 2305 always takes the raw rule; ind_index is empty, so the guard rule (1889-1896) and the second half of 1957 never act; 2458 and 2648-2649 multiply by the identity. JUDGEMENT: a wx-cert-2 certificate is checked by the 2.6 rules, as the SCHEMA RULE asks.

(5) CONTROLS (controls.py; results in controls_results.txt; full-certificate runs except V6b0 and V6z0)
C1 = `python -I -B wxcheck_v30.py FILE` with the venv python; C2 = `node --max-old-space-size=6000 wxcheck2_v30.js FILE`.
| control | node (line) | change | C1 | C2 | as expected |
| V1 (HW, substitute) | sign split root.1.1.1.2.2.2.1.1 (295); fails at child root.1.1.1.2.2.2.1.1.2 (296) | the two ids of its children list swapped; no other line changed | FAIL: assume list is not the parent's list followed by the split assumption | FAIL: assumption 1 is ysign (5, 11, a+a+, -1), expected +1 | yes |
| V1x (HW, extra) | root.1.1.1.1.1.1.1.1.1.1 (244) | one extra sign assumption (1, 2, a+a+, +1), used by no round, appended | FAIL: same assume-list rule | FAIL: list has 1 items, expected 0, extra assumption | yes |
| V2 (HW) | same node (244) | par declaration (1, 3, a+a+, Ps) removed, name par:1:3:a+a+:Ps:1 kept | FAIL at round 1 step 4: no valid par declaration | FAIL at steps[4].terms[5]: fact not available | yes |
| V3 (HW) | same node (244) | kappa of that Ps declaration set to 0 | FAIL at pairs[1]: cp >= 0 and cm >= 0 fails | FAIL at pairs[1]: cp >= 0 fails, cp = -0.1015 | yes |
| V4 (HW) | root.1.1.1.2.2.2.1.1.2 (296) | stored rarc[1-3].hi turned back by the rotation of t = 1e-12, sine 1.3e-12 below the certified value | FAIL at round 1 store: St^+ of the pair 1-3 is not implied | FAIL at store.rarc[1-3].hi: tighter than certified | yes |
| V5 (G20S) | root.1.1.1.1.1.1.1.1.1.1 (244) | cut A:10:11:lo set to its certified bound + 1e-18 | FAIL at round 1 store: cut not implied | FAIL at store.cuts: not implied | yes |
| V6b (HW) | root.1.1.1.1.1.1.1.1.1.1 (244), step 0, S lo | value set to L + 1e-40 | FAIL at step 0: claim not accepted | FAIL at steps[0]; its exact L equals C1's | yes |
| V6z (HW) | root.1.1.2.1.2.2.1.1.2 (322), step 0, form 0 | value set to L + 1e-40 | FAIL at step 0: needs L >= value > 0 | FAIL at steps[0]: `0` step not accepted | yes |
| V6b0, V6z0 (HW, --node mode) | the same two steps | value set to L exactly | node accepted, exit 10 | NODE-OK, exit 3 | yes |
V3: no HW control existed for a Ps-specific precondition; Ps declarations do exist (19,246 in HW). V5 uses the lower side of a cut; LOCAL-2's W1 used the upper side.

(6) SCRIPTS (all in <reviewer scratch>/) AND TESTS
- scan_targets.py: one pass over HW and G20S; picks the earliest nodes per control. Counts: HW 579 nodes (289 split, 289 infeasible, 1 terminal), 47 sign splits, 1,776 rounds. G20S 679 nodes (339 split, 302 infeasible, 38 terminal), 97 sign splits, 3,006 rounds.
- scan_v1.py: the count for F2.
- v6_L.py: exact L of the two V6 steps with the frozen checker imported read-only; fast path equals literal path.
- controls.py: the controls. Its first start stopped on a slip of mine in matching the node line, before any checker ran. A later start of V1x stopped on my own assertion. I fixed the script.
- ranges.py: section (3).
- poly_tests.py: T1, T2, T3 as cited above. T3 also: rarc is available at cosine 7/25 and rejected at -7/25; wsup availability equals my own sign test for all 16 labels.
- sample_tests.py: T4 as cited above; also the Ps slope inequality 5,235 times and the wsup slope inequality 1,008 times.
T3 first failed through an error in my own test (I had listed an available rarc fact as unavailable); I corrected the test.

(7) HASHES (first 16 hex)
SPEC_v3.0.md 0a6dfc2ae10ed6f3; wxcheck_v30.py cf8db52bfa1cc565; wxcheck2_v30.js 97210adf74a3ebed; G20S_tree.jsonl.gz 3275f52aca2e23e1; HW_tree.jsonl.gz c974a9c5dce91e7d; upper-packing-certificate.json 24e296f5995abc94; LOCAL-2/hw_controls.py 5f813ffdaa11244e; controls_results.txt aa1c0892dddaca56. The first five agree with the values given for the review.

(8) NOT DONE
- I did not read the Node checker or h_report30.py.
- I did not run the unchanged certificates.
- No flip of an unused sign assumption on a real node (F2).
- One control only on G20S.
- The two acceptances at value = L were made in one-node mode, not as full runs.
- The centred rule was read, not tested.
- The stored-end branch of `effective` was tested only through V4 and LOCAL-2's W2, not in T4.
- I did not check the command lines of the G20S and HW acceptance runs.

(9) QUESTIONS TO THE AUTHORS
1. Do the acceptance logs of G20S and HW show "options: default" for C1, so that the pinned packing file was required?
2. Should the proof text say that on wx-cert-2 trees of this chain every sign assumption is used by its node? It is not needed for soundness.

