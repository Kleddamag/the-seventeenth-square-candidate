# Seventeen unit squares: a candidate proof that the known packing is optimal (one-page overview)

Marc Leonard Overbeck (ORCID 0009-0008-8607-8197). Contact: moverbeck@ethz.ch

Status: candidate proof, not an established theorem. The status is stated once, in `README.md` ("Status"), and in full in `STATEMENT_STATUS.md`.

**What the statement claims.** Line 9 of `STATEMENT.md` says that a packing at side L exists and that no packing has a smaller side. This is the claim that the proof text establishes under its hypotheses: the 210 obligations listed in the producers' file `OBLIGATIONS.json`, of which 15 are mathematical premises. They are the hypotheses of the theorem in the proof text (`revision-v7/PROOF.md`, lines 12 to 14: "Assume the 210 listed obligations ..."). Both files are under `research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/`. The statement is the claim of a candidate proof, not an established theorem. Uniqueness of the packing is not claimed. A premise here is a lemma that the proof text uses. For each one the edition carries the paragraphs of the proof text and the files listed in `PREMISES.md`; for some premises these files are tables and programs only, not a separate written proof. None has been verified by anyone outside the project.

![The known packing of seventeen unit squares](packing.png)

## Statement

Let L = 4.6755300936... be the algebraic number defined in `STATEMENT.md`; it is the side of the known packing (John Bidwell, 1998). The claim: seventeen closed unit squares with pairwise disjoint interiors do not fit in a closed square of side S for any S < L. Together with the packing this would give s(17) = L. The proof text derives this from 210 listed obligations; it is a candidate. Uniqueness of the packing is not claimed.

## The argument in five steps

(each step states what the candidate proof claims; the section numbers are those of the proof text)

1. **Upper bound** (section 1). The known packing is feasible at side L: 68 wall conditions and 136 pair conditions, exact.
2. **Capture** (sections 2 to 6). Take any packing of side at most C = 4.675531. The tool is a weighted counting certificate (a "charge"). Weighted points are placed in the container, and the total weight that disjoint squares can collect is bounded by a budget. A certificate names classes of positions and directions, each with a threshold. The score of a square is the smallest threshold among the classes that contain its position and direction, and 1 if no class contains it. The certificate shows that every square collects charge of at least its score, in a fixed unit, so the scores of the squares of a packing add up to less than a stated bound (`CLASS_ROW_LEMMA.md`). The score is not one fixed amount for every square: it depends on the classes the square lies in. From 98 such statements the proof concludes that the seventeen squares can be labelled so that each lies in a named window around its square in the known packing. A marker fixes the labelling. The outcome is a decision list of eleven cases.
3. **Admission** (section 7). Each of the eleven cases lies in one of eleven explicit regions (boxes for centres, arcs for directions, a range for the side).
4. **Local trees** (section 7). For ten regions a tree certificate shows that the region contains no packing of side below L. For the eleventh it shows that every packing in it lies in a small tube around the known packing. A tree splits the region; every leaf is closed by an exact inequality (linear, or a sum-of-squares identity).
5. **Rigidity** (section 8). In the tube, sixteen of the squares are rigid at the actual side: a finite exact stage (17 rounds) and then a contraction with ratio 159201934153319 / 200000000000000 < 1 force contact with a wall in a way that contradicts S < L.

## What "checked" means here

- The proof is a list of **210 obligations** (`OBLIGATIONS.json`): 15 mathematical premises, 50 base capture rows, 1 slab statement, 49 strict budgets, 84 branch implications, 11 local roots. The proof text composes them; it says itself that it is a conditional composition (section 9).
- The deciding arithmetic is on integers and rationals. In the Python capture checker they are Python integers and Fractions, with 64-bit integers inside its sweep tree under the bound 2^50. In the Node.js capture checker the decisions use BigInt, and the sweep tree stores its integers in binary64 (Float64Array) and compares them there; the source refuses a certificate unless the sum of absolute weights is below 2^50 and tests the values it reads with Number.isSafeInteger, so every operation on them is exact. Floating-point solvers only propose certificates; the specification of the tree certificates has the checkers work on rationals. (`KNOWN_LIMITS.md`, table row e.)
- Capture: 98 numeric statements, 1,728,000 rows for each of the two checkers. The edition carries one fresh computation by each checker (Python and Node.js) on inputs without free text, in 1,152 slices. Before release the project compared it row by row with stored earlier executions, through a published hash map and name map: 1,728,000 rows per checker, 0 mismatching. The earlier executions are not carried; the records of that comparison are. The merge of the slices is structural and does not recompute the charge inequalities; the producers' public check `provenance` decides every stored row again from the numbers recorded in it.
- Tree certificates: 13 trees, accepted by two independently written exact checkers (written by separate sessions of the same AI system from one specification) against that frozen specification. They were executed again on 11 October 2026: 26 of 26 checker runs PASS, 13 of 13 post-checks ACCEPTED; and a third time in a neutral folder, with outputs equal to the second apart from paths and times.
- Reading: in the audit of the sealed record every one of the 210 obligations was read by at least two independent readers (separate AI sessions) who had not written it (`AUDIT.md`; this number comes from that record, which is not in the edition). 29 of their reports are in this edition as reading copies. For 2 of the 15 premises no report among the reading copies is bound to the premise (ALGEBRAIC_ENDPOINT, ENDPOINT); `READING_ORDER.md`, part 3, lists what is bound to each. The reports were written about the project's sealed record and about the earlier executions of the capture computation, not about the files reissued for this edition (`KNOWN_LIMITS.md`).
- All of this is an **internal** audit, and it was made on the sealed record before the revision that this edition carries (`STATEMENT_STATUS.md`). Every system of the project that produced or read the work was an AI system. See `AUDIT.md`; for the one outside review so far, `README.md` and `KNOWN_LIMITS.md`.

## What it rests on that this project did not make

The charge method, the exact side and the local recipe of Joshua Levy's squares project; the proof shape of the n = 11 proof by Manasseh Ahmed (github.com/Queuingtheorydotcom), 11SquaresOptimal (github.com/Queuingtheorydotcom/11SquaresOptimal); the frames and checkers of Mira and Guzhou0806. See `CREDITS.md`.

## How to check it yourself

One command: `python3 check.py` (about 4 minutes; one check needs SymPy 1.14.0, see `README.md`; run by the project on one platform only, see `CHECK.md`). It verifies the SHA-256 of every file, resolves every pin of the form {"file", "sha256"} in the index files it lists, runs the producers' 31 public checks (the upper bound, the tight enclosure of L, the case logic, the dependency graph, the rigidity arithmetic, the decision of every stored capture row, the bindings), their equivalence check, an independent program for the enclosure of L, the test of the comparison records, and reads the stored outputs of the tree executions. It does **not** recompute the capture rows or the tree certificates; that takes many machine-hours and is described in `CHECK.md`.

## What would break it

A wrong lemma among the 15 premises; a specification that says less than the proof needs; an error common to both implementations of a checker; or a stored execution that did not run what its record says. Readers are asked to look there first. The premises are of very different size and kind. Some are an argument of a page or less; some bundle long geometric arguments; one is a specification with two checkers; some are computer-assisted; and some have no written argument of their own outside the proof text and tables. `check.py` does not establish them; it replays exact computations on which some of them rest. `PREMISES.md` is a table of them; `READING_ORDER.md`, part 3, lists the files of each. `README.md` names the three places that deserve the hardest look and says how to report a problem.

## Next step

A formalization in Lean is planned: a checker whose soundness is proved in Lean, and the certificates of this edition run through it as compiled code. It has not been started. Until it exists and others have checked it, the result is a candidate.
