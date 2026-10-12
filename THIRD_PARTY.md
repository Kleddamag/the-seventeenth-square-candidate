# Third-party material in this edition

This file lists every file of the edition that is a copy of a file of another project, or was made from one. General credits (whose ideas and methods the work stands on) are in `CREDITS.md`; this file is only about files.

## How the list was made

- The comparison was made on the project's internal package of 11 October 2026. That package is an earlier collection of the files of the project; it is not this edition and it is not published. Every file of it was compared, by its git blob hash, with every file of the squares project at its commit `ef79288a498b5469e6b944f7b150d83aeeab5f94` (6 Oct 2026; 15,658 files, of which 6,823 are under `packing/resources/`). The files found there were then looked for in this edition by their SHA-256.
- What this cannot find: a file that was copied and then edited, a copy of another revision than the one compared, and code adapted by hand. Where the project's own files say such a thing, it is listed below.

## 1. Copies of files of the squares project

Source: **Joshua Levy, the squares project (https://github.com/jlevy/squares)**. Its licence file (`LICENSE` at the commit above) gives three grants: code under the MIT License; everything else (documentation, research reports, frontier and campaign records, data, figures) under Creative Commons Attribution 4.0 International (CC BY 4.0), with attribution; and no grant for the third-party material under `packing/resources/`.

| File | Their file | Kind | Licence | How established | Copies in this edition |
|---|---|---|---|---|---|
| `H256.md` | `packing/campaign/hypotheses/H-256-n17-exact-endpoint-feasibility.md` | campaign record | CC BY 4.0 | byte-identical at the commit above | 1 |
| `H256_CERTIFICATE.json` | `packing/campaign/series/series-000-smoke-and-calibration/results/exp-238-n17-endpoint-feasibility/run-001/certificate.json` | data | CC BY 4.0 | byte-identical at the commit above | 1 |
| `H256_CHECKER.py` | `packing/devtools/check_n17_endpoint_feasibility.py` | code | MIT | byte-identical at the commit above | 1 |
| `upstream-root-certificate.json` | `packing/campaign/series/series-000-smoke-and-calibration/results/exp-237-n17-polynomial-root/run-001/certificate.json` | data | CC BY 4.0 | not byte-identical: the same JSON content written out in another layout | 9 |

None of these comes from `packing/resources/`. Changes made by this project: the files were renamed on copying; the root certificate was written out again with the same content. Nothing else was changed. Not in this edition (they are in the internal package named above): `cover-receipt.json`.

The copies:

- `H256.md`:
  - `research/finishing-threshold-goal-20261007/current-author-20261012t/contract-stage-20261009-1252/reflection-closed/chirality-coupling/exact-root-extension/producer/inputs/H256.md`
- `H256_CERTIFICATE.json`:
  - `research/finishing-threshold-goal-20261007/current-author-20261012t/contract-stage-20261009-1252/reflection-closed/chirality-coupling/exact-root-extension/producer/inputs/H256_CERTIFICATE.json`
- `H256_CHECKER.py`:
  - `research/finishing-threshold-goal-20261007/current-author-20261012t/contract-stage-20261009-1252/reflection-closed/chirality-coupling/exact-root-extension/producer/inputs/H256_CHECKER.py`
- `upstream-root-certificate.json`:
  - `research/finishing-threshold-goal-20261007/current-author-20261012t/claude-extension-audit/terminal-producer/snapshot/research/uniform-capture-20261007/upstream-root-certificate.json`
  - `research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/finite-entry-stop-pruning/entry-producer/instance/research/uniform-capture-20261007/upstream-root-certificate.json`
  - `research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/finite-entry-stop-pruning/root-producer/inputs/research/uniform-capture-20261007/upstream-root-certificate.json`
  - `research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/full-gate/producer/instance/research/uniform-capture-20261007/upstream-root-certificate.json`
  - `research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/full-stopped-propagation/continuation/instance/research/uniform-capture-20261007/upstream-root-certificate.json`
  - `research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/full-stopped-propagation/producer/instance/research/uniform-capture-20261007/upstream-root-certificate.json`
  - `research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/normalized-dual-reuse/producer/instance/research/uniform-capture-20261007/upstream-root-certificate.json`
  - `research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/targeted-seven-objectives/producer/instance/research/uniform-capture-20261007/upstream-root-certificate.json`
  - `research/uniform-capture-20261007/upstream-root-certificate.json`

`H256.md` is upstream text carried byte for byte. It is a working sheet of the squares project: besides the mathematics it holds that project's own planning fields and rules of work, and the name of an AI system that reviewed for that project (`KNOWN_LIMITS.md`). None of that text is this project's.

The MIT notice of the squares project, which covers `H256_CHECKER.py`:

```
Copyright (c) 2026 Joshua Levy

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

For the CC BY 4.0 files the attribution, in the wording that their licence file asks for, is: "Joshua Levy, the squares project (https://github.com/jlevy/squares)". Licence text: https://creativecommons.org/licenses/by/4.0/legalcode.

## 2. Files of this project that the squares project has archived (not third-party)

The comparison found files of this edition whose bytes occur in the squares project only under `packing/resources/web/`, in folders that archive this project's own public releases. They are this project's files:

- `research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/checker_sources/src/integer_sweep.py`
- `research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/checker_sources/src/boolean_rule.py`
- `research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/checker_sources/src/exact_general.py`
- `research/finishing-threshold-goal-20261007/current-author-20261012t/claude-extension-audit/terminal-producer/snapshot/upper-packing-certificate.json` and 7 more byte copies

## Lineage that is not a copy of a file

- **Mira-acc/17squares and Guzhou0806/n17-square-packing.** The frames and checkers of this work follow the design of theirs (`CREDITS.md`). No file of theirs was found in the edition, within the limits stated at the top.
- **Manasseh Ahmed (github.com/Queuingtheorydotcom), 11SquaresOptimal (github.com/Queuingtheorydotcom/11SquaresOptimal).** No file of it was found. There is no copy of that project on the build machine to compare bytes with.

## Licence not established

Listed here and not guessed:

- `upper-packing-certificate.json` (top level, and 7 byte copies inside the evidence folders). Its own header says: "Rational reconstruction of John Bidwell's 1998 packing", with a drawing of the packing in David Ellsworth's catalogue as source. The numbers were reconstructed from that drawing. No licence for that source was identified.
- **Mira-acc/17squares:** no licence file at its root; the attribution file of its 4.613 certificate package makes the derived certificate data available under CC BY 4.0 with attribution; no grant of its own was found for its 4.614153 package. **Guzhou0806/n17-square-packing:** no general licence grant was found.
- No file of the edition comes from the squares project's `packing/resources/`, except the files of this project listed in the section "Files of this project that the squares project has archived".
