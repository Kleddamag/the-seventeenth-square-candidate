# Public admission entry point

From the repository root, run:

```
python3 -B research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/replay_round2.py admission
```

The import chain is `scripts/entry_checks.py` → `scripts/run_adm.py` → `scripts/adm.py`. The check performs exact root admission and has no solver or `hull_node.py` dependency. The replay runner records actual reads and redirects writes to its own new result folder. `ADMISSION_DEPENDENCIES.json` binds the current run and its observed dependencies; it does not identify an earlier run as a new execution.

Names of generating or formerly reviewed programs in historical records identify earlier sources. They are not public commands or additional runtime requirements. Verification uses the exact pinned root JSON and the separate EXPECT-region comparison. In particular, historical mentions of `audit_v5_roots.py`, `check_review.py` and `mk_join_roots_v2.py` do not instruct the reader to run those programs. `LEGACY_REFERENCES.json` identifies remaining occurrences and their historical role.

Recorded execution, exact admission arithmetic, and independent mathematical review are separate evidence. A successful command establishes only its stated checks.
