# The internal audit

**This was an internal audit. It is not an outside check.**

Status: candidate proof, not an established theorem. The status is stated once, in `README.md` ("Status"), and in full in `STATEMENT_STATUS.md`.

## What was checked, and how

"The producers" are the AI systems that wrote the proof files and the certificates. "The readers" are separate AI sessions that had not written what they read and were given the files, not the producers' conclusions. "Independent" in this edition means such a separate session; in several places a session of one AI system reviewed work of another session of the same system.

1. **Reading.** The proof was frozen as a list of 210 obligations, 15 of them mathematical premises. Every obligation was read by at least two independent readers, in two rounds. The second round covered the parts that the first had not read at the needed depth: the core of the capture checker, the upper bound (with a reader's own exact code), the tree checkers and the region records (with negative controls on altered certificates).
2. **Corrections.** The producers answered the findings in seven addenda. Four were read again by fresh readers; two were compared line by line with their predecessors; of the seventh, the index of stored runs was checked against the files.
3. **Capture.** During the audit every capture computation existed in two stored executions on different machines, compared row by row in both checkers; the readers' reports speak of those. For this edition the computation was made once more by each checker on inputs without free text (1,152 slices) and compared row by row with the stored earlier executions: 1,728,000 rows per checker, 0 mismatching. The edition carries this last computation and the records of the comparison, not the earlier executions.
4. **Trees, second execution.** All 13 tree certificates were run again in both frozen checkers: 26 of 26 runs PASS and equal to the first record line by line and node by node; 13 of 13 post-checks ACCEPTED. The outputs are under `local-research/claude-20261002/results/rerun_trees_20261011/`. A third execution was made in a neutral folder; its outputs are under `local-research/claude-20261002/results/trees_neutral_20261011/` and equal the second apart from paths and times.
5. **Closing.** The findings list has 153 lines: 114 closed, 23 results, 16 noted, none open. The coverage table has 210 rows, none with anything open.

## What is in this edition

- 29 of the readers' reports and 20 records of the tree work, as reading copies (`local-research/claude-20261002/review/public-edition/round5/`; `READING_ORDER.md`, part 4).
- The capture computation of item 3 and the stored outputs of item 4.
- Not here: the findings list, the coverage table, the addenda and the rest of the audit trail. They belong to the sealed record (`KNOWN_LIMITS.md`). The numbers in items 1, 2 and 5 are taken from that record; the files from which they were counted are not in this edition.

## What the audit was not

- Every system of the project that produced, read or checked the work was an AI system. Within the project no human has read the mathematics.
- It was not an outside review. Since then Guzhou0806 (N17 project) read the fifteen premises in an earlier state of this work and ran a checker of his own on two of the thirteen trees (JQ and JPG15p_v5). His report is not part of this edition. This is not a refereed review, and nobody outside the project has verified the whole (`KNOWN_LIMITS.md`).
- **The audit covered the sealed record as it stood before the revision that this edition carries.** Against the producers' preceding edition 203 of the 210 claims are word for word the same, 6 differ in wording only and 1 was corrected (the ratio in the claim of G20S_PHYSICAL; `CHECK.md`, level 2 (b)). The revised proof text, the reissued check scripts and the new capture computation have had the checks of this file and of `CHECK.md`, but no independent review of the final bytes; the producers' own files say so (`STATEMENT_STATUS.md`).
- The audit read the sealed record. The proof text of this edition was written afterwards from that record, and the producers' check scripts were reissued for this edition; the readers' reports are not reviews of the reissued files (`KNOWN_LIMITS.md`).
- After the audit closed, the outside reader raised points that this edition answers: the tight endpoint check and an independent program for it, the decision of every stored row from its recorded numbers (the public check `provenance`), and the producers' note on index sizes (`CHECK.md`).
- The proof rests on 15 mathematical premises, on two exact capture checkers agreeing, on two exact tree checkers agreeing, and on the stored runs having executed what their records say.
- Uniqueness of the packing is not claimed.
