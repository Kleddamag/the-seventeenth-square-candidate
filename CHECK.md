# How to check this edition

Status: candidate proof, not an established theorem. The status is stated once, in `README.md` ("Status"), and in full in `STATEMENT_STATUS.md`.

## What you need

- Python 3.9 or newer. `check.py` itself uses the standard library only.
- One level-2 check, `endpoint_upper` (the upper bound), needs **SymPy 1.14.0** (pure Python; it brings mpmath). It was tested with SymPy 1.14.0 only; other versions are untested, not known to fail. If SymPy cannot be imported, level 0 says so in one line, the check FAILS, the result is FAIL, and the last line names the cause; nothing is installed for you. Two ways to supply it: `python3 -m pip install sympy==1.14.0`, or, without touching your Python installation, `python3 -m pip install --target DIR sympy==1.14.0` and then `python3 check.py --sympy-path DIR` (DIR then holds the `sympy` and `mpmath` packages).
- Node.js is not needed for levels 0 to 2 (level 0 only says whether it is there). A full recomputation needs it.
- About 7.7 GB of disk with the large files, about 2.9 GB without.

## Where it was run

The project ran `check.py` on this edition on one platform: **macOS 27.0.1 (Darwin 27.0.0, arm64), CPython 3.9.6, Node.js v25.6.1, SymPy 1.14.0**.
On that machine every check ran to the end, and the times in this file were measured there. It is one machine; no other machine and no other operating system was tried. The full check was also run once under CPython 3.12.14 on that machine, with the same result.
Other platforms are untested: Linux, Windows, other versions of macOS, Python versions other than the two named, other SymPy versions. The wrapper that level 2 uses for the public checks builds file paths with "/" as separator; nothing in it was written for Windows. Level 0 prints the platform of your machine beside this one.

## The command

```
python3 check.py              levels 0, 1 and 2
python3 check.py --level 1    one level (the result is then PARTIAL at best)
python3 check.py --only NAME  one check of level 2 (PARTIAL at best)
python3 check.py --list       the names of the level-2 checks
python3 check.py --timeout-scale 4   the same checks, with every time limit of level 2 multiplied by 4 (for a slow machine)
```

The last line is `CHECK RESULT:` followed by one word:

- `PASS` (exit code 0): levels 0, 1 and 2 were all run, every one of the 41 checks of level 2 ran, and nothing failed. `check.py` counts the checks it carried out and compares the number with 41 (`EXPECTED_CHECKS`); another number is a failure (`check-count`).
- `PARTIAL` (exit code 2): nothing that was run failed, but not everything was run. This is the result of `--level`, of `--only`, of a run in which checks are NOT RUN because large files are absent, and of a run in which a check is TOO-SLOW (stopped by the CPU limit that its own script sets, or by the time limit of the producers' runner; see below). **A PARTIAL result is not a PASS of the edition.**
- `FAIL` (exit code 1): at least one failure line.

`check.py` finds the root of the edition from its own location and reads only inside it. It writes under `_check_out/` in the root. One exception, which leaves no trace: the producers' runner of the public checks creates a new folder per check under `research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/public_runs/`; `check.py` moves that folder into `_check_out/` as soon as the check has ended. No listed file is changed. If a run is interrupted, such a folder may stay behind; level 1 then reports it as an unlisted file and says to remove it.

### Level 0: the environment

Python version; assertions on; the platform of your machine, beside the one platform the project ran on (information only); Node.js present (warning only); whether SymPy can be imported (if not, one plain line says which check cannot run and the two ways to supply it); the root holds the files that `check.py` needs first; the name of the root folder does not occur a second time higher up in its own path (`root-name`).
`self-test`: the function that compares two stored outputs (used by `neutral_equal`, level 2) is tried on small texts. It must treat `PASS` followed by a line `  123  unresolved constraints` as different from `PASS` alone, and must leave out exactly the 17 resource lines listed in `check.py` (`RESOURCE_LABELS`).

### Level 1: structure (it hashes about 2.9 GB, and the large files when present)

**This edition has 7,118 listed files and 22,013 pins.** `check.py` fixes both numbers, prints them in the first line of level 1 (`expected`) and counts them again in its last line.

1. `file-list`: the files on disk are exactly the files listed in `MANIFEST.sha256`, with exactly the same letters (a file under another letter case is a failure even on a disk that ignores case). No symbolic link. A file named `.DS_Store` is ignored; its content is not looked at. A top-level folder `.git` is skipped.
2. `file-count`: the manifest lists exactly 7,118 files.
3. `file-hash`: every listed file has the listed SHA-256.
4. `large-files`: each of the 12 files of `LARGE_FILES.tsv` is either absent (not a failure) or present under `_large/` with the listed size and SHA-256. The large files are not listed in the manifest; a large file put at its own path in the tree is reported as an unlisted file. A file under `_large/` that the table does not list, or a symbolic link there, is a failure.
5. `pins`: the scope, as implemented. 12 index files are read: `PKT/PART2_SHA256SUMS` (6,754); `PKT/PART2_MANIFEST.json` (6,753); `PKT/PUBLIC_ARTIFACT_ROOTS.json` (26); `PKT/PUBLIC_INPUTS.tsv` (6,748); `PKT/EDITION.json` (3); `PKT/CURRENT_BINDINGS.json` (1); `PKT/OBLIGATIONS.json` (1,288); `PKT/revision-v7/LABELS.tsv` (278); `CAP/CAPTURE_AUDIT_INPUTS.json` (101); `research/finishing-threshold-goal-20261007/clean-rerun-20261011/reseal-resume-1120/graphs/objects/4da8d938feaf76d8e85ad018ef1ed3512d95f77550401797c279226fcab9ecd6/REVIEW_HASHES.json` (29); `research/finishing-threshold-goal-20261007/clean-rerun-20261011/reseal-resume-1120/graphs/objects/cce600b80d0d7df92da5fa5642dfce1e6576de15c2093adcbf0ecf8584092afa/RECORD_HASHES.json` (20); `LARGE_FILES.tsv` (12). In a JSON file a pin is an object with a string under the key `file` and a value under the key `sha256`, at any depth; in a table it is a row with the columns `file` (or `path`) and `sha256`. The hash must be 64 lowercase hex digits; anything else is a failure. Every pin must resolve: the named file is in the edition with exactly that SHA-256 (and that size, where the table gives one), or it is one of the large files and `LARGE_FILES.tsv` lists that SHA-256 for it. There are no exceptions. Other hashes inside other files (for example `original_sha256` in the two tables, which names a file that is not in the edition, or the hashes inside receipts) are not pins and are not read here.
6. `pin-counts`: the number of pins per index file is the number fixed in `check.py`.
7. `path-neutral-table`: every file that `PATH_NEUTRAL.tsv` lists (94) has the SHA-256 that the table gives as `sha256_after`, and every file that the producers' table `PKT/PATH_NEUTRAL.tsv` names as current (68 rows) has the SHA-256 that it gives. The values `sha256_before` are not tested by `check.py`, which does not contain the replaced strings (`KNOWN_LIMITS.md`, "One substitution in carried files").
8. `fixed-hashes`: 65 files have the SHA-256 written in `check.py`: the 26 root files that the producers' `PUBLIC_ARTIFACT_ROOTS.json` names (among them their roster `PUBLIC_INPUTS.tsv`), that list itself, their manifest `PART2_MANIFEST.json` and checksum list `PART2_SHA256SUMS` of the sealed packet, the stored output of their seal check `AUTHOR_SEAL_CHECK.out`, their runbook, runner, stored replay results, table of checks, equivalence checker and three index files, the index of the capture records, the two hash tables of the reading copies, the summary of the final comparison call, `LARGE_FILES.tsv`, the two programs of this edition that level 2 runs, and every other top-level file except `check.py`, `MANIFEST.sha256` and `EDITION_BINDINGS.json`. The root files named by `PUBLIC_ARTIFACT_ROOTS.json` must be exactly the ones fixed here.
9. `proof-copy`: `PROOF.md` at the top level has the bytes of `PKT/revision-v7/PROOF.md`, and both have the SHA-256 fixed in `check.py`.
10. `bindings`: `EDITION_BINDINGS.json` gives the same hashes, counts and expected last lines in machine-readable form; `check.py` reads it and fails if a value differs from its own.

11. `rest-digest`: 344 listed files are named by no pin and no fixed hash (187 stored outputs of the second and third tree execution; 106 records, programs and tables of the comparison with the earlier executions; 39 other files carried as substituted copies at their original path, whose SHA-256 `PATH_NEUTRAL.tsv` gives (test `path-neutral-table`); 12 files of the tree work that the roster does not list). `check.py` fixes their number and one SHA-256 over the list of their hashes and paths.

**What level 1 does not catch.** Every test of it rests on `check.py`.

- Every listed file except two is bound by `check.py` itself: through a pin, a fixed hash, or the digest of the test `rest-digest`. A changed file with a changed manifest line therefore fails level 1, and so does an added file with an added manifest line (test `file-count`), unless `check.py` is changed as well.
- The two exceptions are `check.py`, which cannot fix its own hash, and `EDITION_BINDINGS.json`, which repeats the values of `check.py` and is compared with them. For these the manifest is the only binding.
- Someone who changes files, the manifest and `check.py` together can make everything pass.
- Level 1 does not look at: empty folders; anything under `_check_out/` or `.git/`; the content of a file named `.DS_Store`.
- Level 1 says nothing about what a file means.

So the last line of every run prints the SHA-256 of `MANIFEST.sha256`. **Compare it with the value in the notes of the release `large-files-v1` of the repository (github.com/Kleddamag/the-seventeenth-square-candidate/releases).** The same notes give the SHA-256 of `check.py`; compare it, and compare it with the line for `check.py` inside the manifest. That comparison is what closes the last two cases.

### Level 2: cheap exact checks (about 4 minutes on the build machine; `endpoint_upper` alone about 100 seconds)

**(a) The producers' 31 public checks** (`research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/runbook_public.json`; what each one read in the producers' own stored replay: `research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PUBLIC_REPLAY_RESULTS.json`). Each is run through the producers' runner `replay_round2.py`, unchanged, which checks the hash of the script, requires assertions, refuses cached bytecode, refuses to read files with certain names (the list is in its source), redirects every write into a new folder and allows no subprocess and no network use. `runbook_public.json` and the runner must have the hashes fixed in `check.py`, and the runbook must define exactly the 31 checks that `check.py` names. Success is exit code 0, the last line `PUBLIC CHECK <id>: PASS`, a receipt with status PASS, the status words fixed in `check.py` (below), and a set of files read that is exactly the set that the producers' stored replay of that check read. (The older table `CHECK_MAP.tsv` describes what each check tests; its column of files read differs from the stored replay for 0 of the checks and is not used.) 5 of the checks have no required output string in the runbook and pass on these conditions alone: `root_stops`, `root_stop_binding`, `entry_transfer`, `entry_binding`, `small_entry`. 6 more require only a general word somewhere in their output (`PASS`, `PASS:`, `PASS_`): `admission`, `selector`, `graph`, `loose_identities`, `bc_composition`, `finite_4`. For every check the required strings are tested by the producers' runner, not by `check.py`; `check.py` requires the conditions named above.

The runner is a guard against accidents, not a sandbox. Its own header says: "Not a sandbox for hostile code." The public checks execute Python programs of this edition with the rights of the user who starts `check.py`, and they inherit that user's environment variables (`check.py` removes `PYTHONOPTIMIZE` and sets `PYTHONDONTWRITEBYTECODE`). Read the scripts before you run them if you do not trust the source of your copy.

| id | script (last two parts of its path) | arguments | the output must contain | scope, where the runbook states one |
|---|---|---|---|---|
| `endpoint_upper` | `endpoint-feasibility/check_endpoint.py` | - | `PASS_INDEPENDENT_EXACT_S_STAR_17_SQUARE_FEASIBILITY` | Independent exact root isolation and the 17-square endpoint construction; SymPy required. |
| `partition` | `manuscript/check_case_partition.py` | - | `PASS_EXACT_GUARD_PARTITION_ON_ALL_SIGN_ATOMS` |  |
| `admission` | `scripts/entry_checks.py` | `admission` | `PASS` |  |
| `selector` | `scripts/entry_checks.py` | `selector` | `PASS` |  |
| `graph` | `scripts/entry_checks.py` | `graph` | `PASS` |  |
| `capacity` | `coarse-capacity-AP/verify_readonly.py` | - | `PASS_EXACT_CAPACITY_CURRENT_ESCAPES_FRAME_INCLUSION_AND_DERIVED_GATE` |  |
| `frame` | `reader-corrections-AQ/verify_frame.py` | - | `PASS_FIXED_FRAME_WALL_ENDS_AND_T2_ENTRY` |  |
| `wall_triggers` | `reader-corrections-AQ/verify_wall_triggers.py` | - | `PASS_ALL_29_WALL_TRIGGER_LITERALS` |  |
| `loose_identities` | `review-repair-O/check_f1.py` | - | `PASS:` |  |
| `provenance` | `scripts/provenance.py` | - | `PASS_ALL_98_NEW_CAPTURE_RECORDS_AND_EXACT_MINIMUM_DECISIONS` | Validate the new-run provenance, complete coverage and exact saved class minima for both engines. No geometric sweep or historical job dependence. |
| `bc_composition` | `scripts/composition.py` | - | `PASS:` |  |
| `bd_binding` | `scripts/finite_scope.py` | - | `exact_core_comparison` |  |
| `bfbe_pins` | `scripts/public_bindings.py` | - | `PASS_PUBLIC_BINDINGS` | Public evidence pins, forbidden-path exclusion and review-label disclosure; no history-only addendum hashes. |
| `finite_1` | `independent-review/check.py` | - | `PASS_EXACT_FINITE_PARTIAL_CONTRACTION_TARGET_NOT_REACHED` |  |
| `finite_2` | `continuation-independent-review/check.py` | - | `PASS_EXACT_FINITE_PARTIAL_CONTRACTION_TARGET_NOT_REACHED` |  |
| `finite_3` | `finishing-independent-review/check.py` | - | `PASS_EXACT_FINITE_COMPLETED_PREFIX_PARTIAL_ROUND_EXCLUDED_TARGET_NOT_REACHED` |  |
| `finite_4` | `proposal-timeout-retry-independent-review/check.py` | - | `PASS_` |  |
| `finite_join` | `proposal-timeout-retry-independent-review/check_join.py` | - | `PASS finite-entry theorem join` |  |
| `normalized_prefix` | `independent-review/check.py` | `a756cea10c4c...` | `ACCEPTED_STOPPED_PROPAGATION_INCONCLUSIVE` |  |
| `normalized_finish` | `continuation-independent-review/check.py` | `685d4d96672a...` | `ACCEPTED_` |  |
| `root_stops` | `root-review/check_root_stops.py` | `--check` | (none) |  |
| `root_stop_binding` | `root-review/check_binding.py` | `--check` | (none) |  |
| `entry_transfer` | `entry-review/check_transfer.py` | - | (none) |  |
| `entry_binding` | `entry-review/check_binding.py` | `8bcad6ad4074...` | (none) |  |
| `small_entry` | `rational-entry-review/check_corollary.py` | - | (none) |  |
| `selection_binding` | `scripts/selection.py` | `--scenario` `original` `--manifest` `research/fin...` | `ready_for_final_assembly_reader` | Metadata and readiness only, not a substitute for geometric selector review. |
| `root_chart_transfer` | `scripts/root_chart_transfer.py` | - | `PASS_INDEPENDENT_SOURCE_AND_CONDITIONAL_CONSTANT_ASSESSMENT` |  |
| `analytic_gate` | `scripts/analytic_gate.py` | - | `PASS_INDEPENDENT_COMPLETE_ROOT_ANALYTIC_GATE` |  |
| `normalized_five_rounds` | `independent-review/check-v2.py` | - | `ACCEPTED_FIVE_ROUND_OLD_WEIGHT_REUSE_INCONCLUSIVE` |  |
| `normalized_sixth_round` | `independent-review/check.py` | `6b765320f8e4...` | `ACCEPTED_SIX_NORM_FACES_ELIMINATED_ONE_REMAINS` |  |
| `endpoint_enclosure` | `public-edition-round2-20261011/check_endpoint_enclosure.py` | - | `PASS_TIGHT_ENDPOINT_ENCLOSURE` | Exact rational Banach refinement establishes both named tight root and side enclosures and matches the statement polynomials; adapted from the earlier endpoint checker, not an independent implementation. No packing feasibility or local tree replay. |

**Limits inside the public checks.** 15 of the 31 public checks run a script of the producers that sets a CPU limit for itself (`resource.setrlimit(RLIMIT_CPU, ...)`), and the producers' runner sets an alarm of 570 seconds of wall time around the script of every check. These limits stand in files that hashes bind; `check.py` cannot change them, and `--timeout-scale` does not reach them. On a slow machine a check can use up its limit before it has finished. `check.py` then reports that check as `TOO-SLOW`, names the limit that stopped it, and ends `PARTIAL`: the check was not carried out on that machine, and no inequality failed. On the build machine every check stayed inside its limit; a slower machine may not. The table gives, for each of these checks, the CPU limit of its script. Wall times on the build machine are not given here: they were not measured on the present scripts.

| check | CPU limit of its script (s) |
|---|---|
| `finite_1` | 150 |
| `finite_2` | 150 |
| `finite_3` | 150 |
| `finite_4` | 150 |
| `normalized_prefix` | 45 |
| `normalized_finish` | 35 |
| `root_stops` | 8 |
| `root_stop_binding` | 8 |
| `entry_transfer` | 3 |
| `entry_binding` | 3 |
| `small_entry` | 2 |
| `root_chart_transfer` | 2 |
| `analytic_gate` | 6 |
| `normalized_five_rounds` | 20 |
| `normalized_sixth_round` | 15 |

Wall time is not CPU time: a check can wait for the disk and stay inside its CPU limit.

**Status words that read like a failure.** `check.py` fixes, for each public check, the status words that its output must contain (`EXPECTED_STATUS`: every word that begins `PASS_`, `ACCEPTED_`, `FAIL_`, `REJECTED_` or `INCONCLUSIVE_`); they are the words of the producers' stored output of the same check, and any other set of words fails. For 6 checks a required word reads like a failure or an unfinished stage. It is the expected outcome of that check; the producers say why, one sentence per check (`PKT/EXPECTED_INTERMEDIATE_STATUSES.json`; their words):

- `finite_1`, `PASS_EXACT_FINITE_PARTIAL_CONTRACTION_TARGET_NOT_REACHED`: "Rounds 1–3 validate finite bounds without yet reaching the small-entry radius; finite_4 reaches it at round 17 and finite_join checks the transfer to small_entry."
- `finite_2`, `PASS_EXACT_FINITE_PARTIAL_CONTRACTION_TARGET_NOT_REACHED`: "Rounds 4–9 validate the continuation without yet reaching the small-entry radius; finite_4 reaches it at round 17 and finite_join checks the transfer to small_entry."
- `finite_3`, `PASS_EXACT_FINITE_COMPLETED_PREFIX_PARTIAL_ROUND_EXCLUDED_TARGET_NOT_REACHED`: "Rounds 10–15 are complete and the old partial round 16 is deliberately excluded; finite_4 supplies complete rounds 16–17 and finite_join checks their small_entry transfer."
- `normalized_prefix`, `ACCEPTED_STOPPED_PROPAGATION_INCONCLUSIVE`: "The first three stopped normalized rounds leave one norm face at radius 1; normalized_finish verifies rounds 4–5 and the strict ratio 159201934153319/200000000000000 < 1."
- `normalized_five_rounds`, `ACCEPTED_FIVE_ROUND_OLD_WEIGHT_REUSE_INCONCLUSIVE`: "The five rounds with reused weights correctly give no strict contraction; normalized_sixth_round removes six remaining norm faces, then the stopped chain normalized_prefix and normalized_finish closes the final face."
- `normalized_sixth_round`, `ACCEPTED_SIX_NORM_FACES_ELIMINATED_ONE_REMAINS`: "The targeted round eliminates six norm faces but leaves one; the full-domain stopped chain normalized_prefix and normalized_finish supplies strict contraction for that remaining obstruction."

`check.py` reads that file as well: where it names a check, the status words of that check must be the word it gives and also the words fixed in `check.py`; if the file and `check.py` differ, no public check is run.

**The check `provenance` is the one that decides the capture rows again.** It runs the producers' `scripts/new_capture_check.py` over all 98 statements. For every stored row of both checkers it derives the decision from the numbers recorded in the row (a level with cells fails if and only if its minimum is below threshold times the required units), compares it with the recorded flag, and refuses a failing row, an empty row, or a row on which the two checkers differ. It also tests the coverage of the rows by the planned slices, the header of every slice and receipt against the inputs, the literal statement, the record of every slice run and of every merge, and the hashes of the checker sources. It does not run a geometric sweep and cannot show that a recorded run took place. Its own description is the header of that file.

Two notes of the producers belong beside these commands. `research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PUBLIC_ENTRYPOINTS.md`: the supported public command, and the statement that names of older programs inside retained records are historical and not required at run time. `research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/INDEX_SAFETY.md`: the bounds on array indices of the Node.js capture checker for the 98 selected certificates; read the numbers there, they are bounds and not measured maxima.

The runner adapts paths in three ways, and names the three in every receipt it writes (`path_adaptations`). (1) A path that contains the name of the root folder between two slashes is read at the same place under the root of the edition; the test goes by the folder name of the root, so it applies only when the root folder of the edition has the name that the repository folder had on the build machine (the last part of `OLD`, below); otherwise the wrapper of `check.py` does this mapping. The runner splits a path at the first occurrence of that folder name; if the name occurs a second time higher up in the path of the edition (for example `.../edition/work/edition/`), it would build wrong paths and every public check would fail with "No such file". `check.py` tests this at level 0 and before the checks of level 2 (`root-name`), and reports a failure with a message that says which name occurs twice. (2) One file name is read under another letter case: `finite-entry-stop-pruning/root-review/MANIFEST.json` as `manifest.json`. (3) `revision-v4/PROOF.md` under the packet is read as `revision-v7/PROOF.md`: an unchanged check names the proof text by an older path, and the runner opens the current proof text instead (`research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PUBLIC_PATH_ALIASES.json` declares this one). `check.py` applies the alias of (3) when it compares the files a check read with the list of the stored replay.

What `check.py` itself maps, and why. Some carried files contain the absolute path of the repository on the build machine (`/Users/builder/Developer/07-math-research/17-squares-certified-bound`, the constant `OLD` in `check.py`; `builder` stands there for the name of the build account). `check.py` therefore starts each of these checks through a small wrapper, `shim.py`, which it writes into `_check_out/`. The wrapper replaces six functions for the script it runs: `os.stat`, `os.lstat`, `os.listdir`, `os.scandir`, `open` and `io.open`. Each of them maps its path argument in two ways: a path that begins with `OLD` is read at the same place under the root of the edition, whatever the root folder is called; and a large file that is not in the tree is read from `_large/`. The two `open` functions also drop an `opener=` argument, as the producers' runner does. The wrapper also replaces `pathlib.PurePath.relative_to`, so that a path under `OLD` counts as a path under the root. No file is edited, and nothing else is changed. Checks that need large files are reported as NOT RUN when those are absent: `bc_composition` (2), `bfbe_pins` (12) and `equivalence` (12).

**(b) `equivalence`**: the producers' `check_equivalence.py`. It checks the SHA-256 and size of the 6,748 files of their roster; that the 210 claims stand to those of their preceding edition as their table `CLAIM_EQUIVALENCE.json` says (word for word, or one of the declared changes; see below), with the same dependencies and kinds; 2 signed restrictions; 11 data projections; the 98 capture audit records against the class files, receipts and literal statements (100 literal statements, two of them derived); and that the stored outputs of their own runs of the 31 checks name exactly the files those runs read. Its output must equal the stored file `AUTHOR_SEAL_CHECK.out`, the output of the producers' seal check. In their words it does not show that English statements mean the same, does not reconstruct comparisons with objects that are not carried, and does not authenticate a run. Of the 210 claims, 203 are word for word those of the producers' preceding edition, 6 differ from it in wording only (WALL_PARTITION, ROOT_ADMISSION, LOCAL_CHECKER_SOUNDNESS, WALL_CONTRADICTION, KEY_W_ELIMINATION, COARSE_LOOSE_CAPACITY), and 1 was corrected: the claim of G20S_PHYSICAL said "ratio below 0.796", which was false; the ratio of record is 159201934153319 / 200000000000000 = 0.79600967..., and the claim now gives that fraction. The proof uses only that the ratio is below 1. The classification is the producers' own (`PKT/CLAIM_EQUIVALENCE.json`, `PKT/REVISION_SCOPE.json`); all 7 changed claims are claims of premises.

**(c) `comparison_records`**: `check_comparison_records.py` (its header says exactly what is tested and what is not). The earlier executions of the capture computation are not in this edition, so the comparison with them cannot be run again here. The edition carries its records: one per statement and the summary of the final call. The check shows that the records are complete, say IDENTICAL for every statement and both checkers, name the carried programs and tables by SHA-256, name as the new side exactly the slices, receipts and inputs carried here (SHA-256 and size), and name as the stored side the same slice files as the producers' own audit records. Expected last line: `COMPARISON RECORDS RESULT: PASS (98 statements, each IDENTICAL in its record; the stored side is not in this edition and is not tested)`.

**(c2) `independent_endpoint`**: the program `independent/endpoint_enclosure/own_endpoint_enclosure.py`, written by an independent reader (standard library, exact rationals; its header describes the method). It must end with `RESULT: PROVED ...` after 39 lines `[ok]`, and its control run (`--control`: one coefficient of F changed by 1) must end `RESULT: NOT PROVED` with exit code 1. The public check `endpoint_enclosure` of part (a) is the producers' own exact check of the same tight enclosure; in the producers' words it adapts their earlier endpoint checker and is not an independent implementation. `independent/endpoint_enclosure/README.md` lists the path lines that were changed for this edition.

**(d) The stored outputs of the tree executions.** `trees_first_lines` (26 checker outputs of the second execution, first line `PASS`), `trees_post_checks` (13 post-check reports, last line `RESULT: ACCEPTED`), `trees_sha256_all` (`SHA256_ALL.txt`, the hash list written when the second execution ended, names exactly the 71 expected files of that folder, each once; 16 of them are files of this edition with the listed SHA-256; 55 are carried as substituted copies, so that the list names the SHA-256 they had before the substitution and `PATH_NEUTRAL.tsv` gives both values (the number 55 is fixed in `check.py` as `EXPECTED_BEFORE_IN_SHA256_ALL`; any other number fails)), `trees_certificates` (each pair of machine reports names the certificate of this edition by the SHA-256 that the producers' roster gives, and this packing file and this specification). `neutral_first_lines` and `neutral_post_checks`: the same two tests on the third execution. `neutral_equal`: each of the 65 output files of the third execution (26 checker outputs, 26 machine reports with every node, 13 post-check reports) equals the file of the second after the following, and nothing else, is taken out of both: path prefixes (everything before `local-research/`, `research/` or the name of the packing file in an absolute path, and the part `_large/`); every time of the form "N s"; a number that follows the word "seconds", "elapsed" or "time"; in the machine reports the four fields `seconds`, `cpu_seconds`, `wall_seconds` and `elapsed`; every line that begins with "real", "user" or "sys"; and the lines that the time command appended to the outputs of the second execution. Those appended lines are the line with "real", "user" and "sys" and 17 lines of the form "<integer>  <label>"; `check.py` lists the 17 labels (`RESOURCE_LABELS`: average shared memory size, average unshared data size, average unshared stack size, block input operations, block output operations, cycles elapsed, instructions retired, involuntary context switches, maximum resident set size, messages received, messages sent, page faults, page reclaims, peak memory footprint, signals received, swaps, voluntary context switches) and leaves out a line only if its label is one of them. Every other line is compared.

## What you should see

```
L0 PASS    python                     Python 3.x.y (3.9 or newer is needed)
...
L1 INFO    expected                   this edition has 7118 listed files and 22013 pins in 12 index files; ...
L1 PASS    file-list                  7118 files listed, 7118 present, none missing, none unlisted, no symbolic link, letter case exact
...
L2 PASS    graph                      PUBLIC CHECK graph: PASS [read exactly the N files that the producers' stored replay read] (0.1 s)
...
CHECK RESULT: PASS (levels 0-2; 7118 files, 22013 pins, 41 checks); sha256 of MANIFEST.sha256: <64 hex digits>
```

Without the large files the last line reads `CHECK RESULT: PARTIAL (levels 0-2; ..., 41 checks, of which NOT RUN for absent large files: ...; nothing that was run failed, but N check(s) NOT RUN: this is not a PASS of the edition); sha256 of MANIFEST.sha256: ...`, and the exit code is 2. With `--level 1` it reads `CHECK RESULT: PARTIAL (level 1 ONLY; ...)`.

If a check is stopped by a limit the line reads `L2 TOO-SLOW <check>  stopped by the script's own N-second CPU limit (...); the check was not carried out on this machine`, and the last line is `CHECK RESULT: PARTIAL (...; of which TOO SLOW ON THIS MACHINE (stopped by the CPU limit of their own script or by the time limit of the runner): ...)`. `check.py` decides this by the cause, never by an amount of time alone: the producers' runner must name its own time limit in its receipt; or the script's handler for its CPU limit must have raised its error (4 of the 15 scripts install such a handler (`finite_1`, `finite_2`, `finite_3`, `finite_4`); each of them catches the error itself, prints it and ends, so the receipt then says `SystemExit(1)`, and `check.py` requires that the last error the script printed is the `TimeoutError` of its handler, with the message that stands in the script, and that the process used at least the limit of CPU seconds); or, for a script without such a handler, the process must have been ended by the signal of the CPU limit (SIGXCPU). A check that fails for another reason is a FAIL, however long it ran. Where the system gives no CPU time for a process (no `resource` module), a stop of the first kind of script is reported as FAIL.

Status words of the single lines: PASS, FAIL, TOO-SLOW (a check stopped by the CPU limit of its own script or by the time limit of the producers' runner; the result is then PARTIAL), WARN (level 0: Node.js missing, or a SymPy version other than the tested one; a WARN does not change the result), MISSING (level 0: SymPy cannot be imported; the level-2 check that needs it will fail), NOT-RUN (a check that needs an absent large file; the result is then PARTIAL), INFO.

On failure every failed line is repeated, then the last line is `CHECK RESULT: FAIL (...; N failure line(s) in: <names of the failed checks>); sha256 of MANIFEST.sha256: ...`, and the exit code is 1. A check that cannot be carried out (for example because a stored output is missing) is a FAIL line. `check.py` itself does not end in a Python traceback; where a script of the producers stops with an error, the FAIL line quotes the last line of that error.

## What a PASS means, and what it does not

- It means: you hold the files that the manifest lists; the index files point at files of this edition; the cheap exact checks give the recorded results on your machine; every stored capture row's recorded decision follows from its recorded numbers, in both checkers, and the two agree; the comparison records are complete and bound to the computation carried here; the stored tree outputs say PASS and ACCEPTED and name the certificates of this edition.
- It does not mean that the theorem is established. It does not recompute the capture rows or the trees, it does not read the mathematics, it cannot rerun the comparison with the earlier executions, and it cannot show that a stored execution ran what its record says. `KNOWN_LIMITS.md` has the table.
- Things `check.py` never looks at: anything under `_check_out/` or `.git/`, files named `.DS_Store`, and empty folders. It tests its own hash only through the manifest.
- It was run by the project on one platform only (above). A PASS on your machine is a statement about your machine.
- Scripts of the edition other than the ones `check.py` runs are carried as sources of the record. Some of them read files that are not carried and cannot run from this edition as they stand (`KNOWN_LIMITS.md`). The supported run is `check.py`.

## Full recomputation, by hand

`check.py` does not run this. **Write the outputs outside the edition, or under `_check_out/`**, so that level 1 still passes afterwards.

### One tree certificate (13 in all; up to 7 GB of memory for the largest)

The two checkers: `research/window-extension-20261008/checker/wxcheck_v30.py` (Python, standard library only) and `research/window-extension-20261008/checker2/wxcheck2_v30.js` (Node.js). The specification they implement: `research/window-extension-20261008/SPEC_v3.0.md`. From the root of the edition, with `CERT` the certificate, `EXPECT` its expectation file and `OUT` an output folder:

```
(cd research/window-extension-20261008/checker  && python3 -I -B wxcheck_v30.py "$CERT" --json "$OUT/T_C1.json" > "$OUT/T_C1.out"; echo $? > "$OUT/T_C1.rc")
(cd research/window-extension-20261008/checker2 && node --max-old-space-size=12000 wxcheck2_v30.js "$CERT" --json "$OUT/T_C2.json" > "$OUT/T_C2.out"; echo $? > "$OUT/T_C2.rc")
python3 -I -B research/window-extension-20261008/acceptance/h_report30.py "$CERT" "$OUT/T_C1.json" "$OUT/T_C2.json" "$(cat $OUT/T_C1.rc)" "$(cat $OUT/T_C2.rc)" "$EXPECT" research/window-extension-20261008/acceptance/FROZEN_30.json
```

`CERT` and `EXPECT` must be absolute paths. Success: both checkers exit 0 and print `PASS` as first line; the post-check `h_report30.py` ends with `RESULT: ACCEPTED`. Compare with the stored outputs in `local-research/claude-20261002/results/rerun_trees_20261011/` (`<tree>_C1.out`, `<tree>_C2.out`, `<tree>_report.out`); they differ from yours only in path prefixes and times.

| Tree | Certificate | EXPECT file (under `research/window-extension-20261008/`) | Time of the second execution, Python / Node.js (from `results.tsv` there) |
|---|---|---|---|
| JQ | `local-research/claude-20261002/cloud/analysis/part3_exact/certs/JQ_v1/jQTw.n0.JQ.cert.jsonl.gz` | `bigbox/join/EXPECT_JQ_v1.json` | 30 s / 10 s |
| JPG15p_v5 | `local-research/claude-20261002/results/assembly/JPG15p_v5/JPG15p_v5.cert.jsonl.gz` | `bigbox/join/EXPECT_JPG15p_v5.json` | 371 s / 75 s |
| JPG17m_v5 | `local-research/claude-20261002/results/assembly/JPG17m_v5/JPG17m_v5.cert.jsonl.gz` (large: under `_large/`) | `bigbox/join/EXPECT_JPG17m_v5.json` | 531 s / 110 s |
| JPG3m_v5 | `local-research/claude-20261002/results/assembly/JPG3m_v5/JPG3m_v5.cert.jsonl.gz` (large: under `_large/`) | `bigbox/join/EXPECT_JPG3m_v5.json` | 711 s / 140 s |
| JPG3p_v5 | `local-research/claude-20261002/results/assembly/JPG3p_v5/JPG3p_v5.cert.jsonl.gz` (large: under `_large/`) | `bigbox/join/EXPECT_JPG3p_v5.json` | 752 s / 140 s |
| JPG17p_v5 | `local-research/claude-20261002/results/assembly/JPG17p_v5/JPG17p_v5.cert.jsonl.gz` (large: under `_large/`) | `bigbox/join/EXPECT_JPG17p_v5.json` | 888 s / 180 s |
| JPG15m_v5 | `local-research/claude-20261002/results/assembly/JPG15m_v5/JPG15m_v5.cert.jsonl.gz` (large: under `_large/`) | `bigbox/join/EXPECT_JPG15m_v5.json` | 1007 s / 195 s |
| G20S | `research/window-extension-20261008/bigbox/gen17/G20S_tree.jsonl.gz` (large: under `_large/`) | `acceptance/EXPECT_G20S.json` | 626 s / 301 s |
| HW | `research/window-extension-20261008/bigbox/gen17/HW_tree.jsonl.gz` (large: under `_large/`) | `acceptance/EXPECT_HW.json` | 461 s / 210 s |
| JG | `local-research/claude-20261002/results/assembly/JG/JG.cert.jsonl.gz` (large: under `_large/`) | `bigbox/join/EXPECT_JG_v2.json` | 1594 s / 336 s |
| JPWS_v4 | `local-research/claude-20261002/results/assembly/JPWS_v4/JPWS_v4.cert.jsonl.gz` (large: under `_large/`) | `bigbox/join/EXPECT_JPWS_v4.json` | 1975 s / 401 s |
| JPW13 | `local-research/claude-20261002/results/assembly/JPW13/JPW13.cert.jsonl.gz` (large: under `_large/`) | `bigbox/join/EXPECT_JPW13_v2x.json` | 4655 s / 957 s |
| JPA_v5 | `local-research/claude-20261002/results/assembly/JPA_v5/JPA_v5.cert.jsonl.gz` (large: under `_large/`) | `bigbox/join/EXPECT_JPA_v5.json` | 8449 s / 1674 s |

Start with JQ: it is small and takes under a minute.

### One slice of one capture statement

A capture statement has 18,000 rows (4 of them 9,000). It was computed in slices of 1,500 rows, each by the Python checker and by the Node.js checker; then each checker merged its slices into one receipt. The recorded durations of the 1,152 selected slice runs add up to about 601 hours on machines with four workers (both checkers together). `recompute_slice.py` recomputes any range of rows of any statement with both checkers and compares the result with the stored rows:

```
python3 recompute_slice.py Q_4 0 1500 --python /path/to/python-with-numpy-and-numba --workers 4
```

Needs Python with numpy and numba (the stored records name numpy 2.0.2, numba 0.60.0) and Node.js. One row takes about 2 CPU-seconds in the Python checker, so a full slice takes about 45 CPU-minutes there. The script prints the two commands it runs; its header describes what is compared. Expected last line: `SLICE RESULT: EQUAL (...)`. On the build machine (another platform than the stored runs) it was tested on rows 0 to 2 of the statement Q_4 and on rows 1498 to 1501 of CLASS_PS_L05_T17, across a slice boundary (result: EQUAL both times), not on a full slice.
A recomputed slice is not a recomputed statement: a statement is all rows without gap or overlap, each checker's own merge, a strict integer surplus, and unchanged source bytes during the run. The launcher that the stored runs used is `research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/checker_sources/slice_run.sh`, the merge script `merge_run.sh` beside it.
Which Node.js checker is which: the checker of record is the file `research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/checker_sources/src/node/verify_classes_wb.js` (SHA-256 `7f6b234768f812b7acf515c28cc4ced0e5b7fb5bcd4c0ba03114733975087d40`). Every stored slice and receipt names its implementation as "node verify_classes.js"; that string is printed by this file and is not the name of another file. The stored records name the file by its SHA-256.
