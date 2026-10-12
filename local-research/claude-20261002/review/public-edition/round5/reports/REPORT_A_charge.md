Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line.

REPORT of the reviewer of premise A: CHARGE_SEMANTICS (written 10 Oct 2026)

1. VERDICT
The premise FOLLOWS from its sources for class statements: no wrong step, and no hidden sampling gap. The bound holds for every pose because each row is a whole interval of directions with an exact cell decomposition of all centres, not a sampled pose.
Three WEAK points, all closable without new mathematics: the orbit-marker row (FRAME_MARKER) was checked by a different checker than the one the premise's proof files accept; the phrase "quarter-turn images included" is ambiguous; the argument and definitions sit one pointer away from the three pinned files.
The premise is conditional on "complete authentic receipts"; that antecedent is established elsewhere (provenance audits by the manifest author) and I did not check it beyond one header.

2. PREMISE CHARGE_SEMANTICS: FOLLOWS WITH GAPS (scope and documentation only)

Hashes: all three pinned proof files match (922bbb68..., d6fd0d89..., e2efa5bf...). The 13 frozen checker inputs match INPUT_MANIFEST.json. The live sources in local-research/claude-20261002/cert_restricted match the frozen ones (exact_classes.py 802dc62a..., verify_classes.js 72b92624...).

Findings, most serious first.

W1 (WEAK, scope). FRAME_MARKER is not a class statement.
- Place: research/.../class-snapshot-20261009-1144/marker.json is `"schema": "s17-restricted-v1" ... "symmetry": "orbit"`, k = 17. It is decided by the restricted checker (the row decision in exact_restricted.py, and verify_restricted.js).
- Why it matters: the three proof files accept "both checker implementations", meaning exact_classes.py and verify_classes.js. exact_restricted.py appears there only as an imported dependency, and verify_restricted.js is in the snapshot but not in ACCEPTED_INTERFACE.json "checkers".
- The only soundness text I found for the restricted row decision is the checker author's own RESTRICTED_CHECKER.md sections 3 to 5, which says "Argued, not machine-checked". The orbit-count review says of itself "This is **not** a full row-checker soundness audit".
- I read the orbit path myself (validate_restricted, _run_fast, exempt_set, accumulate_intervals). It uses the same primitives and correctly implements "every checked cell below Gamma lies, with the whole row interval, in one D4 image of one slot". I found no error.
- Every later step rests on the marker row. To close: name an independent review of the restricted row decision, or re-run the marker as a class file (one class, threshold 0, bound 17, symmetry orbit) through the reviewed class-checker pair.

W2 (WEAK, wording). "quarter-turn images are included" is ambiguous.
- What the source gives: the checker always adds the three quarter-turn lifts of the angle gate, because a square's side direction is only defined modulo 90 degrees (angles_meet and _angles_inside, m in {-1,0,1}). I checked that three lifts suffice, since gates lie in (-1,1) and rows in [-1,1].
- Images of the centre polygon under the container's symmetries are added only if the class file declares them. Of the 172 manifest files, 168 are `fixed` (nothing added), 3 are `mirror_x` (the 137/8 and 145/8 pair statements) and 1 is `orbit` (the marker).
- Manuscript Section 3 words it correctly ("declared symmetry images and square quarter-turn representatives"). The premise statement should say the same, so nobody reads a `fixed` statement as covering rotated copies of its regions.

W3 (WEAK, documentary). The argument is not in the three pinned files.
- ACCEPTED_INTERFACE.json and HIGH_FIRST_REVIEW.md give the interface and the score comparison only.
- The budget and row argument is in REVIEW.md ("Mathematical argument independently checked") and in inputs/RESTRICTED_CHECKER.md sections 1.3 to 1.7, 3 (R1 to R4, row lemma) and 5, plus inputs/CLASS_FORMAT.md sections 1, 3, 4.
- These are hash-bound through the review's MANIFEST.json (1ad3fe76...), not through the theorem manifest. To close: add them to the premise's proof list and to the second packet.

O1 (observation, the antecedent; NOT CHECKED beyond one case). No real statement is one complete run.
- Each is 12 slices of 1,500 rows on each of two implementations.
- "Complete and authentic" is asserted by the SAVED_PROVENANCE.json audits, whose scope line is "stored metadata and source provenance only; no checker rows executed", accepted by Codex, the manifest's own author.
- For Q_1 I checked: the checker hashes are the reviewed ones (Python 802dc62a..., Node 7f6b2347..., the accepted worker-binding repair); the slices tile 0 to 18,000; the class pin differs from the checked bytes only by a declared final line feed.
- The premise is silent without this; a fresh reviewer should take the receipt audits as a separate task.

O2 (note). Margins are exact but razor thin.
- Q_1: Gamma 999,905,254, M 22,997,820,824, surplus 18 units, so M/Gamma = 23 minus 1.8e-8.
- KEY_W: surplus 12 units; least strict-core margin over 18,000 rows is 8.3e-17, positive in exact rationals.
- Strictness is all the proof needs, but nothing is robust to an arithmetic slip. The safeguard is the row-by-row agreement of the Python and Node receipts.

O3 (minor). The KEY_W certificate.json has an embedded top-level `classes` key. The checker ignores unknown top-level keys; the statement is about the --classes file whose hash is in the receipt. Harmless, but a reader may take the embedded one for the checked one.

O4 (minor). Both checkers and the test oracle have one author. The independent reviewer read the code and ran 10,888 small cases plus 352 abstract states. Independence between Python and Node is of implementation, not authorship.

No scope widening found in the manuscript's use. Section 3 claims the bound for seventeen-square packings at side at most C in the declared frame; the source proves it for any family of interior-disjoint unit squares in a square of side at most C placed concentrically. Section 2's shift p + (U - S0)/2 is exactly that concentric placement, and every class file has frame centre (1169/500, 1169/500).

3. THE FIVE QUESTIONS

(1) The mathematics.
- Setting: a certificate container [0, 4613/1000]^2, with unit squares scaled to side A = (4613/1000)/C. In the KEY_W certificate I recomputed L/A = 4675531/1000000.
- Sites and features: sites are finitely many grid points. A feature is at most 20 sites with positive integer coefficients and a threshold k (or a list of pairwise-intersecting "winning masks"), and an integer weight w >= 0. It fires on a closed set K if the sites in K carry coefficient sum >= k (or contain a mask). The charge chi(K) is the sum of weights of firing features.
- Budget lemma (R1), proved and elementary: on pairwise disjoint sets a feature fires at most floor(sum a / k) times (once for masks), so the charges sum to at most M = sum of w times capacity. The checker recomputes M and demands equality with budget_units. Gamma is minimum_units. No LP duality theorem is used; this one line is the whole "weak duality".
- A row is not a sampled pose. A row [a, b, t, B] says: for every square whose side direction has tan-half u in [a, b], and every centre, use as core the concentric closed square of side B < A with fixed direction 2 atan(t).
- Row validity: two exact endpoint inequalities (core strictly inside the open parent; centre envelope), extended to the whole interval by monotonicity of cos d + |sin d| on |d| <= 45 degrees and concavity of cos + sin. I re-derived both and re-ran them on all 18,000 KEY_W rows.
- Row cover: rows form a gapless chain from u = 0 to exactly u = 1 (`fixed`), or to beyond tan(22.5 degrees) with a verified mirror or D4 symmetry of charge and classes (`mirror_x`, `orbit`).
- Centres: for a fixed core shape, the centres whose core contains a given site set form a closed rectangle. The charge is a signed sum of rectangle indicators (Mobius expansion of the Boolean rule), hence constant on the open cells of the arrangement of all rectangle edges. Every cell meeting the envelope of possible centres is tested.
- So the continuum is handled by an exact cell decomposition in the centre and an interval cover in the angle. There is no Lipschitz or sampling step.
- Boundary centres: take a nearby generic centre in an adjacent checked cell; the core is still inside the open parent because containment is strict.
- Conclusion: cores of different squares lie in disjoint open parents, so Gamma times sum psi <= sum of charges <= M < beta times Gamma.
- Where written: RESTRICTED_CHECKER.md sections 3 and 5, CLASS_FORMAT.md section 1, REVIEW.md, HIGH_FIRST_REVIEW.md.
- On "18,000 rows": these are 18,000 direction intervals, each with about 4.4e8 cells. The "sampled rows" of the search engine play no part in the proof.

(2) High-first.
- Proved for psi, including overlaps and boundaries. In check_row the classes above 1 claim, by decreasing threshold, every cell whose closed rectangle times closed row interval meets one of their slot images. Then classes below 1 claim, by increasing threshold, cells wholly inside one slot image. The rest get 1.
- Hence R(cell, row) >= psi(p) for every p in the closed product, and the test is charge times q >= p times Gamma in exact integers.
- I checked the two interval routines (_blocked_interval, _slot_interval) line by line: closed, touching counts for high, all four corners for low. The Node twin has the same order and a BigInt comparison.

(3) Symmetry. See W2: gate lifts by the checker always; centre images only as declared by the file. For reflected images the row interval is tested as [-b, -a] against the gate, which is the correct pairing.

(4) What PASS means.
- Each run validates the whole certificate first: structure, budget recomputed, strict budget inequality, row chain. Then each row passes only if every level's least charge meets its threshold.
- Arithmetic: Python integers and Fractions; int64 only in the sweep tree under an enforced 2^50 bound on the absolute weight sum; Node BigInt, with safe-integer checks.
- The status with the statement is issued only for all rows in one run or by --merge. Merge trusts the slice flags, so the real statements rest on O1.
- The known false-PASS defect of the old Node worker driver is real. It is closed for the receipts I looked at, which use the repaired file 7f6b2347.... I verified that the repaired and original Node files are byte-identical up to and beyond the end of checkRow, and that the prefix hash d40a1aa6... is reproduced at byte 46,907.

(5) Scope in the side. All sides <= C are covered: a smaller container placed concentrically lies inside the certificate container, and the statement quantifies over all families inside it. Nothing uses a lower bound on the side.

4. F2 AND F5 OF THE FIRST REVIEWER
F2 is answered by the sources, but not by the three pinned files. Core, site, row, feature, mask feature, outer weight, M and Gamma are defined in RESTRICTED_CHECKER.md sections 1.3 to 1.5 and 3; the Mobius atoms are boolean_rule.expansion; the proof is as under (1). The second packet should carry those files (W3).
F5 is answered, and in the stronger direction. With thresholds 4/4/0 and seventeen squares, sum psi = 17 + 3 N(H) - N(E outside H). So a strict bound 23 with N(H) >= 2 gives N(E outside H) >= 3 N(H) - 5 >= 1. A parent in E and H scores 4 and does not help the inequality, so the forced occupant has a pose outside the marker and trigger classes and is a different physical square from both. No disjointness of target and trigger region is needed. HIGH_FIRST_REVIEW.md has the same overlap term ("t >= 2m + i") for the count-two case. The manuscript sentence should read "forces an occupant of E outside H". This holds provided the marker parent and the trigger parent do lie in the high classes as written in that file; that is the stated hypothesis, and label 12 is treated separately.

5. WHAT I VERIFIED MYSELF
- Hashes as above.
- Full reading of exact_general.py, integer_sweep.py, boolean_rule.py, exact_classes.py and the geometry and decision parts of exact_restricted.py. I re-derived the sweep coordinates, frame map, edge forms, bounding boxes, both index-interval rules, checked-cell cover of the envelope, class order and exact decision.
- KEY_W certificate, by my own script (<reviewer scratch>/chk_cert.py): side, budget recomputed from 14,122 features, strict inequality, the 18,000-row chain ending at 1, all row inequalities in exact rationals, plus a float check of the two interval lemmas at interior angles.
- Toy test without numba (<reviewer scratch>/toy.py): on 120 random small instances with coefficient and mask features, the frozen geometry() rectangle sums equal the directly evaluated charge of the closed core at random interior points of all 11,566 checked cells. 36,000 random envelope centres all fall in checked cells.
- Survey of the 172 manifest class files: hashes, schema, symmetry, frame centre, threshold patterns.
- Arithmetic of the 4/4/0, 4/0, 161/8 and 137/8 score formulas.

6. WHAT I DID NOT CHECK
- Any real row; any receipt beyond the Q_1 audit header.
- The Node checker line by line (only its row loop and order).
- verify_restricted.js.
- The check_mirror logic on a real mirror_x certificate.
- The independent reviewer's test scripts (not rerun).
- The worker-binding repair beyond the prefix identity.
- Whether each row's class regions mean what the manuscript says they mean; that belongs to FRAME_ASSIGNMENT and ROOT_ADMISSION.

