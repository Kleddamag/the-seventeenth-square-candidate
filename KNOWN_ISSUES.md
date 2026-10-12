# Known issues in version 1

This file lists what is known to be missing, unclear or badly presented in version 1 of this edition. No item
changes a number that a check tests, and `check.py` passes with all of them present. They are to be fixed in
version 1.1; its changelog will say which were. Reports of further problems are welcome (`README.md`, "How to
report a problem").

`PKT/` stands for
`research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/`.
The top-level `PROOF.md` is a byte copy of `PKT/revision-v7/PROOF.md`; line numbers below are the same in both.

## 1. Arguments and evidence

1. **Root admission (premise ROOT_ADMISSION) has no separate written proof of its geometry.** The edition
   carries the paragraphs of the proof text and the exact computation (`PKT/scripts/run_adm.py` with `adm.py`,
   public check `admission`). The reviews bound to this premise are the two reports named in `READING_ORDER.md`,
   part 3 (`REPORT_ADMISSION.md`, `REPORT_ERRATA_2.md`); they are reviews by sessions of the same AI systems, and
   the second ends with points marked open (item 6 below). The file `F1_PROOF.md` that is listed for
   this premise covers the loose-role identities only; its fifth line speaks of a "high-first counting
   implication", while the proof text says that the high-first rule is not used, and the two have not been
   reconciled. One step of the admission is stated only as a comment in `run_adm.py`, lines 17 and 18, and not in
   the proof text: a unit square inside the half-plane x >= 0 whose centre has x < 53/100 has its side direction
   within 2 atan(31/1000) of the wall direction. The argument, as intended: for a side direction theta in
   [-45, 45] degrees the half-extent of a unit square along x is (cos|theta| + sin|theta|)/2, which increases
   with |theta| on that range; the square lies in x >= 0, so this half-extent is at most the centre's x, hence
   cos|theta| + sin|theta| < 53/50. With t = tan(|theta|/2) one has cos|theta| + sin|theta| = (1 + 2t - t^2)/(1 + t^2),
   and at t = 31/1000 this exceeds 53/50 (the script asserts (1 + 2t - t^2) 50 > 53 (1 + t^2) in exact arithmetic);
   so |theta| < 2 atan(31/1000). This paragraph has not been reviewed. Version 1.1 is to carry the step in the proof
   text and a written argument for the admission geometry.
2. **The class-row lemma is a statement with pointers, not one written proof.** It is the step from a passed
   row of a counting certificate to a statement about real packings (premise CHARGE_SEMANTICS), and the first of
   the three places that `README.md` names for the hardest look. `PKT/revision-v7/CLASS_ROW_LEMMA.md` states it
   and points to line ranges of five other files; no single file writes the proof out whole, and the report
   on its derivation among the reading copies (`REPORT_CHARGE_CORE.md`, line 3) says so itself and describes how
   small the reviewer's own test of the rows was. Version 1.1 is to carry the lemma written out in one place.
3. **The composition of the final stages is an argument of the proof text only.** The label
   `file:TERMINAL_COMPOSITION` is bound to the proof text itself, so the paragraph that composes the stages of
   the rigidity part cites no separate record.
4. **"Two independently written exact checkers"** (`OVERVIEW.md`): the two programs were written by separate
   sessions of the same AI system from one specification. Agreement between them guards against slips of
   programming, not against an error in the specification.
5. **Producer and reviewer are often the same AI system.** Several carried reviews say so in their own words (for
   example "Reviewer `Codex`; producer `Codex`"). `AUDIT.md` states this in general; it is repeated here because
   it limits what "independent" means throughout the edition.
6. **Status words in carried records describe the day of the record.** Files that the proof binds carry words such
   as `CONDITIONAL_THEOREM_WITH_OPEN_CAPTURE_AND_LOCAL_PREMISES`, "final review NOT STARTED", "RECEIPT OPEN",
   "NOT YET PROVED", "Still missing", "STILL OPEN" (for example
   `Q/second-order-20261010/theorem/THEOREM_MANIFEST.json`, where `Q/` is the folder above `fifth-order-20261010`;
   the last report of the reading copies, `REPORT_ERRATA_2.md`, lines 139 and 145). Some of the records that
   later closed these points are not carried, so the edition does not show, file by file, how each was closed.
   `AUDIT.md` says "none open" of the project's own list of findings, which is not carried either. A reader
   should treat every such point as open until the files of the edition settle it.
7. **Numbers that readers reported as differing between carried files; they have not been examined yet:** the count of guard
   atoms (30870 in one report and one interface file, 41160 in the admission report and in the output of the
   partition check); the number of nodes of the tree JG (113 and 110); two hash values quoted for one packet file
   in the reports; two pairs of hash values that disagree inside the records of the rigidity part
   (`entry-producer/REPLAY.md` line 20; `finite-stopped-contraction/continuation/RESULT.md` line 47). Which
   value is the one of record in each case is to be stated in version 1.1. The rigidity part also
   has two routes with different constants (ratio 0.859 with radius 8.735e-5 in `PKT/records/THEOREM_G20S.md`;
   ratio 159201934153319/200000000000000 with radius 6.4007e-5 in the proof text); the proof text uses the second.
8. **Two numbers of the proof text are in no stored output.** The admission margins quoted in the proof text
   (paragraph P080) are computed by `run_adm.py`, but the stored output bound for the admission is one line
   ("PASS 11 exact root admissions, 17 labels each"). The "93 option splits" of the tree JPA_v5 (paragraph P090)
   are in no machine report; the stored report gives 416 nodes, 281 infeasible leaves and 135 splits.

## 2. The proof text: numbers written without a space

In about 55 places of `PROOF.md` a number stands directly after the word before it. No number is wrong. The
places where the reading could be mistaken, with the reading that is meant:

| Line | As printed | Meant |
|---|---|---|
| 125 | threshold0 and bound17 | threshold 0 and bound 17 |
| 125 | BOX threshold5/4, W0/E0 threshold7/8 and bound137/8 | BOX threshold 5/4, W0/E0 threshold 7/8 and bound 137/8 |
| 125 | HEX threshold5/4, IW/IE threshold7/8 and bound137/8 | HEX threshold 5/4, IW/IE threshold 7/8 and bound 137/8 |
| 125 | the three threshold5/4 high unions ... the threshold7/8 L9/L17 union, at bound145/8 | the three threshold 5/4 high unions ... the threshold 7/8 L9/L17 union, at bound 145/8 |
| 131 | Its inequality17+h/4-N(V)/8<145/8 | Its inequality 17 + h/4 - N(V)/8 < 145/8 |
| 146 | middle-wall factor129/50≤y≤13/5 | middle-wall factor 129/50 ≤ y ≤ 13/5 |
| 146 | upper-wall factor13/5≤y≤29637/10000 | upper-wall factor 13/5 ≤ y ≤ 29637/10000 |
| 179 | a whole coarse region3,15 or17 | a whole coarse region 3, 15 or 17 |
| 200 | squared diameter1851391155161/4000000000000<1 | squared diameter 1851391155161/4000000000000 < 1 |
| 206 | breakpoints0,alpha,pi/2 | breakpoints 0, alpha, pi/2 |
| 206 | d+b/2 at0 andpi/2, and1/2+bd atalpha | d + b/2 at 0 and pi/2, and 1/2 + bd at alpha |

The remaining places are plain: "role9", "role11", "role3", "role15", "role17", "target12", "label12", "Label12"
(read "role 9", "target 12", "label 12" and so on); "Section1", "Section3", "Section5", "Section11"; "pair05_06",
"pair09_17", "pair11_14" (identifiers, correct as printed); "ordinary4/4/0" (ordinary 4/4/0); "all29 literals";
"high9 atom"; "bound23"; "coarse17"; "all17 scores"; "are32", "leaving29", "include16", "the45", "all45" in line
343 (read "are 32", "leaving 29", "include 16", "the 45", "all 45"). `GLOSSARY.md` and `NOTATION.md` beside the
proof text have about ten such places each, and a few of the producers' files join a hash value to the word
before it.

## 3. The check program and platforms

1. **One platform, two Python versions.** The checks were run on macOS on one machine, under CPython 3.9.6 and,
   once and in full, under CPython 3.12.14 (the capture computation ran on Linux machines, as its records say).
   `check.py` has not been run on Linux or Windows.
2. **Folder name twice in the path.** If the name of the edition's root folder occurs a second time higher up in
   its own path, the producers' runner builds wrong paths; `check.py` stops with a message that says so. Rename
   one of the two folders.
3. **Environment of the caller.** `check.py` starts its checks with the caller's Python environment
   (`PYTHONPATH`, user site packages). Run it in a clean environment if that matters to you.
4. **One output differs between machines by design.** The fresh output of the check `small_entry` contains the
   hash of a regenerated file that holds absolute paths, so that one value differs from the stored one on every
   machine; the verdict does not depend on it.
5. `recompute_slice.py` needs NumPy and Numba, which the main check does not need.

## 4. Wording and disclosure

1. **The reading copies of the reviews** open with a note that passages about the logistics of the review "were
   removed". The note means the lines listed in the tables of edited lines. The copies still contain the
   reviewers' first person, placeholders such as `<author reply>`, sections "QUESTIONS TO THE AUTHORS" whose
   answers are not carried, clock times, and remarks about how a review was run.
2. **Counts in `KNOWN_LIMITS.md`** of working words, clock times and remarks about how the work was run were
   made with word patterns and are lower bounds. For example a plain search for clock times of the form HH:MM
   finds about 270 in about 50 text files, more than the dated times counted there.
3. **A sentence in two of the producers' files is not accurate:** `PKT/PATH_NEUTRAL_POLICY.json` and
   `PKT/KNOWN_LIMITS.md` say that no string length or digest commitment of the replaced account name is
   published. `PATH_NEUTRAL.tsv` gives the size of each file before and after the replacement, which shows the
   length of the name, and the hash before the replacement, with which a guess can be confirmed. The name is not
   a secret (`KNOWN_LIMITS.md`).
4. **Labels that are not explained anywhere:** the two-letter labels BB to BG in the reports, "ledger X3", "O1
   packet", `capture-run-3`, MACTREES, cvMKQ, rev26, r30py and r30js are names of steps, records and sessions of
   the work. They identify things and carry no mathematical meaning.
5. **Words inside the 210 claims** that read oddly without context: "the lead box-wide contraction", "the window
   lead's saved complete runs", "batch3-6 reviews", "not a fabricated exact budget" (`READING_ORDER.md` explains
   some of them). The claims are bound by hashes and are printed as they are.
