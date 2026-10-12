Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line. This report reviewed the earlier executions of the capture computation, named here by neutral designations (table EARLIER_EXECUTIONS.tsv); the audit of the execution carried in this edition and the complete row comparison with the earlier ones are separate evidence.

HOLDS WITH CONDITIONS: (O1) my test of the sweep against the mathematics is a sample (7 of the 9,000 rows, 2,870 exact pose evaluations), not a proof for all rows; (O2) I did not run the Node checker; (O3) I did not check that the class literal aa8b1410 is the pinned marker (CONVERSION.md is outside this review). No gap, no error and no mismatch found for the orbit shape. Residual C4 of CHARGE-CORE is closed for the sampled rows.


FINDINGS (most serious first)
F1. Brute force, 0 mismatches. 2,870 poses in 7 rows. My direct charge (my own orbit expansion, exact Fractions) equals the checker's cell value at all 2,142 interior poses. At all 728 boundary poses no adjacent checked cell lies above the direct charge. Both level minima of every row are reached exactly (98 interior poses in the 14 minimum cells).
F2. The control (b) as worded (weight +1, budget +1) is impossible in the orbit shape. One orbit entry carries 8 images, so the loader's budget equality demands budget + 8 x capacity. The loader refuses +1 ("budget/overflow") and accepts +8 for a capacity-1 entry (17 G - budget drops from 13 to 5). For a capacity-2 entry (136 of the 953 entries) the needed +16 exceeds the surplus 13 and the loader refuses at the budget inequality. Observed exactly as predicted. This is no defect. JUDGEMENT.
F3. The symmetry images are load-bearing in two separate places, and I reproduced both. (i) Class images (R-F1): with the checker's image list forced to identity, rows 4500 and 4501 fail; class cells drop 164366688 -> 41091672 and 164367820 -> 41091955 (the figures of RECEIPTS line 162). (ii) Feature images: with my expansion cut to the first listed image, the direct charge falls below the checker's cell value at 340 of 340 poses per row.
F4. Observation. All eight images of one orbit entry can fire in a single core (7 to 9 entries have multiplicity 8 at the row-minimum cells). This is consistent with the capacity bound, because each image is its own feature with its own capacity. JUDGEMENT.
F5. Observation. The least core margin A - B(cos d + |sin d|) over the 9,000 rows is 8.28e-17 at row 6317. It is an exact positive rational and equals the slice field minimum_margin. Positive is all the argument needs. JUDGEMENT.
F6. Observation. 17 G - budget = 13 units (of 1.7e10). The inequality is strict and in integers.
F7. Observation. exact_general.geometry line 52 hard-codes L = 4613/1000; exact_restricted._head line 165 enforces c['L'] == 4613/1000, so the two agree.

PART 1. RESTATEMENT (my words) AND JUDGEMENT
Load path: exact_classes.load -> parse_classes -> validate_classes (lines 266-321). For symmetry "orbit" it demands point_orbits and threshold_orbits, forbids sites / features, runs _strict_symmetric, then exact_general.expand (lines 19-48).
Sites. A row [x, y, w] of point_orbits is an integer point of [0, LD]^2, LD = L x D = 46,130,000,000. It stands for its orbit under the eight symmetries of that square: swap x and y, x -> LD - x, y -> LD - y. The orbit is sorted and appended to one global list; this fixes the indices used later. Each image is a one-site feature of weight w. In this file: 5,287 orbits (5,285 of size 8, 2 of size 4), 42,288 sites, all point weights 0.
Features. An entry of threshold_orbits has 'sets' (index tuples), weight w >= 0, threshold k, coefficients c (positive, descending), or winning_masks. A threshold feature fires on a captured set T iff the sum of c_j over its sites in T is >= k. A mask feature fires iff all sites of one mask are in T; masks must pairwise intersect. Thresholds, coefficients and masks are carried unchanged to every image, position by position.
How images are generated. The file lists the images itself. expand lines 32-44 recompute the eight images of sets[0] and demand that the listed set equals them exactly, each once ("incomplete trigger orbit" otherwise). For threshold features the tuple must be in canonical order (by coefficient descending, then index). Each listed image gets weight w.
Budget. Sum of point weights over all site images, plus for every listed image w x capacity; capacity = floor(sum c / k) for a threshold feature and 1 for a mask feature (line 46). It must equal budget_units (line 47).
Charge. chi(K) of a closed set K = sum of the weights of all expanded features that fire on the sites lying in K. For a pose in row [a, b, t, B] the core is the closed square of side B, direction 2 atan t, centred at the pose centre in certificate coordinates q = L/2 + A(e - c), c = (1169/500, 1169/500).
Class. One class, threshold 0: the hexagon x gate [-207107/500000, 207107/500000], united with its eight images about c; rotations keep the angle interval, reflections negate it (exact_classes.py 359-371). The gate covers every row angle. The hexagon is mirror-symmetric, so there are four distinct images.
JUDGEMENT 1a. The expanded feature set equals the closure of the first listed image of each entry under the eight symmetries. Computed with my own code: 953 entries, 7,624 listed images, 7,624 images in my closure, every closure of size 8, no entry differs, no image listed twice, no feature in two entries. My expanded multiset is invariant under each of the eight symmetries. It equals the multiset the loader hands to the sweep (sites identical, 7,624 features identical with weights).
JUDGEMENT 1b. The budget bounds the total charge of any family of pairwise disjoint cores. A site lies in at most one core. For a threshold feature the firing cores take disjoint site subsets each of coefficient sum >= k, so at most floor(sum c / k) fire. For a mask feature two firing cores would both contain the common site of their masks, so at most 1 fires; my brute-force set packing gives capacity 1 for all 16 mask images. Weights are >= 0. Each image counts with its own capacity, so the argument is unchanged for the expanded set.
JUDGEMENT 1c. The folded row range is sound. Rows cover u in [0, 207107/500000] without gap, beyond tan(pi/8). A square of negative angle is mirrored; the charge is invariant (tested: 600 direct evaluations at 75 centres, 0 asymmetric) and the class is a union over a group.
Budget recomputed: mine 16,971,591,304 = certificate budget_units = receipt_python = receipt_node. G = 998,328,901. 17 G - budget = 13 = receipt surplus. Capacities: 6,536 images of capacity 1, 1,088 of capacity 2.

PART 2. BRUTE FORCE (t2_brute.py; direct side = myorbit.py, no checker function)
Rows: 0; 7820 = stored global-minimum row (789710848, first of 7820-7824); 8965 = tightest level (default minimum 999999994, first of 8965-8970); 4500; 4501; 8058 and 5678 = first two draws of random.Random(20261011).randrange(9000).
Poses per row, 410: 110 uniform in the legal centre square, 4 corners and 16 edge points of it, 128 in the class regions (all 8 images: inside, the 6 vertices, edge midpoints, just outside), 112 on corners / edges / midpoints of random cells (8 cells per row taken in class pieces), 30 in and on the least cell of each level, 10 least cells of the ten lowest slabs.
row | poses | legal | interior, equal | boundary, equal to least adjacent, above | mismatch | uncovered legal | unsound level | statement fails | level minima reached (class, default) | s
0 | 410 | 410 | 306, 306 | 104, 88, 16 | 0 | 0 | 0 | 0 | 979514434 7/7, 1001832462 7/7 | 38.0
7820 | 410 | 399 | 306, 306 | 104, 86, 18 | 0 | 0 | 0 | 0 | 789710848 7/7, 1001832469 7/7 | 37.7
8965 | 410 | 396 | 306, 306 | 104, 87, 17 | 0 | 0 | 0 | 0 | 799777012 7/7, 999999994 7/7 | 37.4
4500 | 410 | 410 | 306, 306 | 104, 83, 21 | 0 | 0 | 0 | 0 | 941559390 7/7, 1001832469 7/7 | 37.2
4501 | 410 | 410 | 306, 306 | 104, 90, 14 | 0 | 0 | 0 | 0 | 941559390 7/7, 1001832469 7/7 | 39.0
8058 | 410 | 404 | 306, 306 | 104, 86, 18 | 0 | 0 | 0 | 0 | 792509618 7/7, 1001832470 7/7 | 38.6
5678 | 410 | 410 | 306, 306 | 104, 80, 24 | 0 | 0 | 0 | 0 | 935653065 7/7, 1001832472 7/7 | 37.5
total | 2,870 | 2,839 | 2,142, 2,142 | 728, 600, 128 | 0 | 0 | 0 | 0 | 98/98 | 265
Meaning of the columns. "Unsound level": a cell the checker gives the class level while my own orbit class says tau = 1 for an angle of the row (1,148 class-level cells met, 0 unsound). "Statement fails": direct charge < tau(pose) x G with my tau (1,222 class poses, 1,648 default poses, 0 failures). 31 poses lie in checked cells just outside the legal square; they were compared too. The checker's cell values are plain sums over the rectangle list of exact_general.geometry; the cell levels are the partition check_row itself hands to its sweep (captured). Before sampling, each row was recomputed and found equal to the stored row, and my plain-array sweep gave the stored cell counts and minima per level.

PART 3. DIRECT ROWS (unmodified copy of DIRECT's driver.py, sha 1bbecabe0b311527; it supports the orbit shape as it stands; nothing changed)
row | direct mode | s | tree mode | s
0 | EQUAL | 2.1 | EQUAL | 3.0
7820 | EQUAL | 2.3 | EQUAL | 1.4
8965 | EQUAL | 2.3 | EQUAL | 1.5
4500 | EQUAL | 2.3 | EQUAL | 1.4
4501 | EQUAL | 2.5 | EQUAL | 1.5
8058 | EQUAL | 2.6 | EQUAL | 1.4
5678 | EQUAL | 2.5 | EQUAL | 1.4
Fields compared: minimum_units, cells, deficient_slabs, passed, deficit_minimum_units, default, classes, witness, against exact/slices/*.py.json. Direct mode compiled no numba routine. Separately: the 9,000 python rows and the 9,000 node rows of the slices agree in minimum, cells, passed, default, classes (0 differences); their sums equal the merged receipt.

PART 4. NEGATIVE CONTROLS (scratch only)
(a) images forced to identity (t4a_identity.py, 340 poses per row: 30 in each of the 8 class images, 100 uniform)
row | checker, full images | checker, identity only | witness | my direct charge at the witness | (a1) my class = listed slot only: statement fails | (a2) my features = first image only: below required level / below cell value | s
4500 | passed | FAILS, class cells 164366688 -> 41091672 | cell (14215, 28073), charge 998206027 < G | 998206027; tau full 0 through group elements 3 and 7; tau identity 1 | 8 poses; example frame centre (1.992604764, 2.347831338), charge 956866231 < G 998328901 | 88 / 340 of 340 | 66
4501 | passed | FAILS, class cells 164367820 -> 41091955 | cell (14192, 28085), charge 998296688 < G | 998296688; tau full 0 through 3 and 7; tau identity 1 | 4 poses; example (2.314146274, 1.994748729), charge 964609372 | 88 / 340 of 340 | 63
With the full orbit the statement holds at all 680 poses.
(b) weight of one orbit entry +1, budget +8 (t4b_weight.py; the prediction is printed before the altered file is loaded; it comes from my own evaluation of the entry's 8 images at every cell that could undercut)
row | entry chosen at | entry | images firing there | predicted: chosen cell, row minimum, level minima | observed (check_row tree, plain sweep, my direct charge) | result
7820 | row-minimum cell | 97 | 8 | 789710856, 789710856, [789710856, 1001832469] | same | CONFIRMED
4500 | row-minimum cell | 97 | 8 | 941559398, 941559398, [941559398, 1001832469] | same | CONFIRMED
7820 | row-minimum cell | 123 | 3 | 789710851, 789710851, [789710851, 1001832469] | same | CONFIRMED
4500 | row-minimum cell | 6 | 3 | 941559393, 941559393, [941559393, 1001832471] | same | CONFIRMED
8965 | default-minimum cell | 12 | 1 | 999999995, row min unchanged 799777012, [799777012, 999999995] | same | CONFIRMED
4501 | default-minimum cell | 27 | 1 | 1001832470, row min unchanged 941559390, [941559390, 1001832470] | same | CONFIRMED
8965 | default-minimum cell | 16 | 2 | 999999996, row min unchanged, [799777012, 999999996] | same | CONFIRMED
Each case about 10 s. In every case weight +1 with budget +1 was REFUSED ("budget/overflow"), as predicted.
(c) capacity-2 entry 39, weight +1 (t4c_cap2.py): budget +1 REFUSED, +8 REFUSED (equality), +16 REFUSED (budget inequality, 17 G - budget = -3). As predicted.

PART 5. THE RECEIPT IN MINIMUM-SCORE FORM
The stored receipt (PASS_CLASSES_EXACT_COVER, python and node) asserts: for every family of closed unit squares with pairwise disjoint interiors in a square of side 4675531/1000000, read with the container centre at (1169/500, 1169/500), the sum of tau(pose) is < 17, where tau = 0 on the class (the hexagon with every angle, united with its eight D4 images) and tau = 1 elsewhere. So at most 16 squares lie outside the class; among 17 squares at least one lies in it.
Nothing in my reading or tests depends on a high-first reading. The class file has one class of threshold 0. The checker holds kind -1, order [0], levels [0, 1]; its regions for the row are 8 polygons of the "contained" kind; the "meets" branch (classes above 1) is never entered. The sweep used the needs [0, 998328901] only. For this file the code's score and the printed tau are the same function. JUDGEMENT.

HASHES VERIFIED (sha256, first 16)
exact_classes.py 802dc62aa4f2a9e1; exact_restricted.py caae39b30cfcde51; exact_general.py 89954c6c44e1368b; integer_sweep.py 3a2bfd8892a9693b; boolean_rule.py c49d38ac96027b34 (equal to the receipts and to every slice header).
certificate.json 4f6fd3419ed52352; classes.json aa8b1410906ddac7; receipt_python.json 9fa412114086b18b; receipt_node.json 0943e2ea4e1169bc.
DIRECT driver.py 1bbecabe0b311527 (my copy identical); CHARGE-CORE brute.py 98e06be2f64353f1 (read for the method; its feature expansion not reused).

SCRIPTS (all in <reviewer scratch>/; logs and JSON in out/, altered certificates in control/)
myorbit.py 380679860eee6687 (my expansion, budget, direct charge, orbit class; imports no project code)
rowkit.py 9abb02565eb2594f (the checker's cells, values and levels, read from the unmodified modules)
t1_budget.py 0f7aeb34117501bc; t2_brute.py 534211454cb53e9f; t4a_identity.py 4cb867bf50b30aef; t4b_weight.py 03ee395a74ee12c4; t4c_cap2.py cfa081bdf90feaed; t5_sym.py 8519508357ba8085; driver.py 1bbecabe0b311527 (unmodified copy)
Records used: the first execution of FRAME_MARKER (certificate.json, classes.json, receipts, slices) and .../cert_restricted/.

AGREEMENT WITH EARLIER READERS (read after my own results)
CHARGE-CORE: I agree with its capacity argument and its budget for this folder; its residual C4 is now tested. RECEIPTS R-F1: reproduced with identical cell figures, and explained from the mathematics side (poses of charge below G that are in the class only through a non-identity image). DIRECT: same result for this certificate with its own driver.

WHAT I DID NOT DO
- No brute force on the other 8,993 rows; the all-row statement rests on the two receipts.
- No run of the Node checker; I only compared the stored node rows with the stored python rows.
- No reading of CONVERSION.md; whether the hexagon class is the pinned marker's exempt set, and whether the frame of the class file is the frame of the marker, is not judged here.
- No check of the provenance of the slices (job files, branches) or of REQUEST.json.
- No separate brute force of poses with negative angle beyond the 600-evaluation symmetry test.
- The boundary limit was tested on 728 boundary poses, not proved by me; I rely on the monotone-feature argument (closed capture at a boundary point contains the capture in each adjacent open cell). JUDGEMENT.
- The CLI of exact_classes.py was not run on the altered files; I called load and check_row directly.

QUESTIONS TO THE AUTHORS
Q1. None on the orbit shape. One note for the record text: a weight change of 1 in an orbit entry moves the budget by 8 or 16, so the surplus of 13 leaves room for exactly one such unit on a capacity-1 entry and none on a capacity-2 entry.

