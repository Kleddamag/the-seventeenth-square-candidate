# Reading order

Status: candidate proof, not an established theorem. The status is stated once, in `README.md` ("Status"), and in full in `STATEMENT_STATUS.md`.

All paths are relative to the root of the edition. `PKT/` stands for `research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/`, `CAP/` for `research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/`, `RC/` for `local-research/claude-20261002/review/public-edition/round5/`. "sha256" is the first 16 hex digits; the full value is in `MANIFEST.sha256`.

## 1. The proof text and what belongs to it

| Order | File | What |
|---|---|---|
| 1 | `STATEMENT.md`, `STATEMENT_STATUS.md` | the exact statement; its status |
| 2 | `PKT/revision-v7/PROOF.md` (sha256 `0d4c408d1e38a8d8`) | the proof text: 9 sections, 116 numbered paragraphs (`<!-- P001 -->` and so on). Labels in square brackets, for example `[file:OBLIGATIONS]`, are resolved by the next file. |
| 3 | `PKT/revision-v7/LABELS.tsv` | 278 rows under 95 labels: label, file, SHA-256, role. Every label of the proof text names files of this edition; some labels name several. 4 labels of the table do not occur in `PROOF.md` (`file:ENVELOPE_REVIEW`, `file:ENVELOPE_SOURCE`, `file:FINITE_ROW_KERNEL`, `file:JOINT_ROW_CONSTRUCTOR`); they occur in the companion texts of row 6. |
| 4 | `PKT/revision-v7/NOTATION.md`, `PKT/revision-v7/GLOSSARY.md` | symbols and words |
| 5 | `PKT/revision-v7/CLASS_ROW_LEMMA.md` | the lemma that turns a decided row into a statement about packings (premise CHARGE_SEMANTICS) |
| 6 | `PKT/revision-v7/ANALYTIC_ENVELOPES.md`, `PKT/revision-v7/FINITE_PARALLEL_DERIVATION.md` | two analytic derivations used in section 8 |
| 7 | `PKT/OBLIGATIONS.json` | the 210 obligations: identifier, kind, claim, what it depends on, the evidence files with their SHA-256 |
| 8 | `PKT/DEPENDENCY_GRAPH.json` | which obligation is used where |
| 9 | `PKT/EQUIVALENCE.md`, `PKT/KNOWN_LIMITS.md` | the producers' notes on the scope of their packet and of its checks, and on what they kept unchanged; read them with `KNOWN_LIMITS.md` at the top level and with `KNOWN_ISSUES.md`, which lists what is known to be wrong or missing in this version |

`PKT/EDITION.json` names the proof text, the label table and the class-row lemma with their SHA-256.

The label `file:TERMINAL_COMPOSITION` is bound to the proof text itself (it stands in paragraph P093): that step is an argument of the proof text, not a separate record.

The sections of the proof text: 1. The exact endpoint and an attained upper bound; 2. Normalization at the algebraic endpoint; 3. Class budgets and physical square counts; 4. One frame and distinct physical parents; 5. The exhaustive eleven-branch classification; 6. Selected capture implications and coarse capacity; 7. Admission and exact local trees; 8. From the G tube to physical rigidity; 9. Composition and the evidence boundary.

## 2. The 210 obligations by kind

| Kind | Number | Evidence |
|---|---|---|
| mathematical premise | 15 | listed one by one in part 3 |
| base capture or physical transfer | 50 | the capture statements under `CAP/statements/` (both exact checkers, all rows), named by `PKT/runtime/RECEIPT_ROSTER.json`; two of the rows, C_7 and C_8, are derived from another statement and have no computation of their own |
| slab capture | 1 | a capture statement |
| selected strict budget | 49 | capture statements |
| selected branch implication | 84 | each is an implication from named capture statements; the selection is checked by the public checks `selector` and `selection_binding` |
| whole local root | 11 | one tree certificate each (two more trees serve the rigidity step), with acceptance records under `research/window-extension-20261008/acceptance/` and region records among the reading copies |

## 3. The fifteen mathematical premises

For each premise: the claim, copied from `PKT/OBLIGATIONS.json` as written there (missing spaces included); the paragraphs of the proof text that carry the label `[premise:...]`; the files that `LABELS.tsv` binds to it; and the review reports. The claims use the notation of `NOTATION.md`. The premises differ much in size and kind; "files of record" shows whether a premise has a written argument of its own, a specification with programs, or tables only.

**Fifteen premises.** `OBLIGATIONS.json` has 15 rows of the kind "mathematical premise"; these are the fifteen premises of this part. `DEPENDENCY_GRAPH.json` has a field `h6_id_convention`; "H6" there is the working name of the list of obligations.

**"Depends on".** The line copies the field `depends_on` of `OBLIGATIONS.json`. In the words of that file: "Applied dependencies are retained even when graph_binding denotes a pure lemma." So a premise may list a dependency that its pure implication does not use; the proof text says where each is used.

Working expressions inside the copied claims: "the window lead" is the AI session that produced the tree certificates and the regions; "Codex import snapshots" are copies of region files that one of the two AI systems (`CREDITS.md`) took when it first imported them; "not a fabricated exact budget" (claim of C7_C8_TRANSFER) means: no exact budget was computed for the two class files C7 and C8, which were not run; their occupancy is derived from the budget of E07A and reflection; "the lead box-wide contraction" (claim of G20S_PHYSICAL) is an alternative route with a ratio below 0.859; the claim says that it is not used as an extra step.

### 1. ALGEBRAIC_ENDPOINT

- **Claim:** There exists a unique root in the pinned rational root chart; define L=(6+4t)/(1+2t-t^2). Its accepted enclosure gives L<R<C<U. R=4675530093604551/10^15; C=4675531/10^6; U=1169/250.
- **In the proof text:** the label `[premise:ALGEBRAIC_ENDPOINT]` stands in paragraph P005.
- **Files of record for it** (label `premise:ALGEBRAIC_ENDPOINT` in `LABELS.tsv`): `research/finishing-threshold-goal-20261007/current-author-20261012t/claude-extension-audit/terminal-producer/gate-receipt.json`; `research/global-compensation-20261007/reviews/fresh-structure/endpoint-feasibility/check_endpoint.py`
- **Review reports among the reading copies:** none bound to this premise
- **Other independent reviews bound to it:** `RC/extra/research/global-compensation-20261007/reviews/fresh-structure/endpoint-feasibility/REVIEW.md`; `research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/full-gate/independent-review/MANIFEST.json`
- **Depends on:** no other obligation

### 2. UPPER

- **Claim:** Seventeen unit squares with independent specified poses fit without interior overlap in [0,L]^2. The direct independent endpoint proof checks 68 walls and 136 pairs at the identical unique algebraic root; H256 is an additional retained construction.
- **In the proof text:** the label `[premise:UPPER]` stands in paragraphs P005, P015.
- **Files of record for it** (label `premise:UPPER` in `LABELS.tsv`): `research/global-compensation-20261007/reviews/fresh-structure/endpoint-feasibility/check_endpoint.py`; `research/global-compensation-20261007/reviews/fresh-structure/endpoint-feasibility/endpoint-receipt.json`
- **Review reports among the reading copies:** `REPORT_UPPER_EXACT.md`
- **Other independent reviews bound to it:** `RC/extra/research/global-compensation-20261007/reviews/fresh-structure/endpoint-feasibility/REVIEW.md`
- **Depends on:** ALGEBRAIC_ENDPOINT

### 3. ENDPOINT

- **Claim:** For S0<L, translating by (L-S0)/2 preserves all seventeen physical parents, all fixed-U poses and their injective labels; after a common D4 image every point has positive inset from every L-wall.
- **In the proof text:** the label `[premise:ENDPOINT]` stands in paragraphs P005, P021, P112.
- **Files of record for it** (label `premise:ENDPOINT` in `LABELS.tsv`): `research/finishing-threshold-goal-20261007/current-author-20261012t/join-design-files-20261009-1525/endpoint-normalization-producer/THEOREM.md`
- **Review reports among the reading copies:** none bound to this premise
- **Other independent reviews bound to it:** `research/finishing-threshold-goal-20261007/current-author-20261012t/join-design-files-20261009-1525/independent-endpoint-normalization-review/REVIEW.md`
- **Depends on:** ALGEBRAIC_ENDPOINT

### 4. CHARGE_SEMANTICS

- **Claim:** For every finite packing of closed unit squares with pairwise disjoint interiors in the side-C square of the declared frame, validated complete authentic exact row verification gives sum of minimum containing-class scores tau <= M/Gamma < beta. The score is 1 if no class contains the pose. Closed boundaries, all required direction lifts and declared symmetries are included. The four links and strict integer comparison are in the source-bound CLASS_ROW_LEMMA. This selected route does not require the stronger high-first consequence. Smaller sides follow by concentric fixed-pose inclusion; slice authenticity and concrete byte-alias transport remain separate premises.
- **In the proof text:** the label `[premise:CHARGE_SEMANTICS]` stands in paragraph P005.
- **Files of record for it** (label `premise:CHARGE_SEMANTICS` in `LABELS.tsv`): `PKT/revision-v7/CLASS_ROW_LEMMA.md`
- **Review reports among the reading copies:** `REPORT_CHARGE_CORE.md`, `REPORT_ERRATA_2.md`, `REPORT_ORBIT.md`
- **Other independent reviews bound to it:** `research/finishing-threshold-goal-20261007/current-author-20261012t/class-capture-audit/checkers/independent-review/REVIEW.md`
- **Depends on:** no other obligation

### 5. FRAME_ASSIGNMENT

- **Claim:** Accepted marker/pair rows allow one common D4 image with the half-marker occupied, the inherited frame counts, a unique occupant of L9 and a distinct occupant of the reflected region L17. No reflection relation between those two physical poses is asserted; all subsequent labels refer to actual distinct physical parents. No L09low substitute is used.
- **In the proof text:** the label `[premise:FRAME_ASSIGNMENT]` stands in paragraphs P005, P040, P042.
- **Files of record for it** (label `premise:FRAME_ASSIGNMENT` in `LABELS.tsv`): `research/finishing-threshold-goal-20261007/current-author-20261012t/contract-author-20261009-2110/FRAME_L9.json`; `research/finishing-threshold-goal-20261007/current-author-20261012t/contract-author-20261009-2110/FRAME_L9.md`
- **Review reports among the reading copies:** `REPORT_FRAME.md`
- **Other independent reviews bound to it:** `research/finishing-threshold-goal-20261007/current-author-20261012t/contract-author-20261009-2110/independent-frame-review/ACCEPTED_INTERFACE.json`
- **Depends on:** CHARGE_SEMANTICS, FRAME_MARKER, FRAME_0506, FRAME_1114, FRAME_0917

### 6. C7_C8_TRANSFER

- **Claim:** The E07A strict class budget and reflection imply occupancy of the literal C7 and C8 targets in the selected half frame by distinct parents. This is an occupancy transfer, not a fabricated exact budget for either unrun C file.
- **In the proof text:** the label `[premise:C7_C8_TRANSFER]` stands in paragraphs P005, P047.
- **Files of record for it** (label `premise:C7_C8_TRANSFER` in `LABELS.tsv`): `research/finishing-threshold-goal-20261007/current-author-20261012t/join-design-1702/c7-c8-inherited-producer/PROOF.md`
- **Review reports among the reading copies:** `REPORT_FRAME.md`
- **Other independent reviews bound to it:** `research/finishing-threshold-goal-20261007/current-author-20261012t/join-design-1702/c7-c8-inherited-review/RECEIPT.json`
- **Depends on:** E07A, FRAME_MARKER

### 7. WALL_PARTITION

- **Claim:** For label 9 in x<=53/100, the three disjoint branches are y<=129/50 (Q), 129/50<y<=13/5 (JPWS), and y>13/5 (JPW13). At y=13/5 the four loose QB targets, not L targets, are used. Off-wall AQ is empty by unique L9, so the accepted L3,L15,L17 budgets force unique distinct loose-role occupants before their angular gates are tested. Their clipped diameters are strictly below one; this capacity proof precedes root admission. The entire coarse loose regions 3,15,17 have capacity one; their sole occupants are the forced S_k parents. Fully gated JG therefore has no occupant of any C escape slot X. All four L rows are prerequisites in every off-wall branch, before root admission.
- **In the proof text:** the label `[premise:WALL_PARTITION]` stands in paragraph P005.
- **Files of record for it** (label `premise:WALL_PARTITION` in `LABELS.tsv`): `research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/coarse-capacity-AP/PROOF_BRIDGE_V2.md`; `research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/review-repair-O/F1_PROOF.md`; `research/finishing-threshold-goal-20261007/current-author-20261012t/join-design-1702/c-wall-v2-producer/repair-loose-only/run-01/PART3_REQUIRED_CLASS_FRAME.json`
- **Review reports among the reading copies:** `REPORT_COMPOSITION.md`, `REPORT_FRAME.md`
- **Other independent reviews bound to it:** `research/finishing-threshold-goal-20261007/current-author-20261012t/join-design-1702/loose-only-review/ACCEPTED_INTERFACE.json`
- **Depends on:** FRAME_ASSIGNMENT, L_3, L_15, L_17, CHARGE_SEMANTICS, COARSE_LOOSE_CAPACITY, L_4

### 8. ROOT_ADMISSION

- **Claim:** In the endpoint placement and one common frame, the selected capture occupancy conclusions yield all 51 pose factors in one of the eleven remaining pinned root products, with distinct parents, all orientation choices and seam ownership. Gated9 support gives xi9,1>=-9897/10^6. Seven remaining v5 factors contain both PB11 and HULLW11; JPWS_v4 uses the additional slab target. The entire coarse loose regions 3,15,17 have capacity one; their sole occupants are the forced S_k parents. Fully gated JG therefore has no occupant of any C escape slot X. All four L rows are prerequisites in every off-wall branch, before root admission. The off-wall classification is the bounded JPA angular exit, six first-ungated loose-role cases in order3,17,15, or fully gated JG; every such branch uses L3,L4,L15,L17. C12 is first identified with the half-marker occupant, so its source direction is intersected with the half-marker before admission. The JPWS slab target is checked directly and is not inferred contained in HULL11.
- **In the proof text:** the label `[premise:ROOT_ADMISSION]` stands in paragraphs P005, P043, P044, P045, P059, P060, P073, P078, P079.
- **Files of record for it** (label `premise:ROOT_ADMISSION` in `LABELS.tsv`): `research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/review-repair-O/F1_PROOF.md`; `research/finishing-threshold-goal-20261007/current-author-20261012t/standing-contract-20261009-2134/v5-root-review/ACCEPTED_INTERFACE.json`
- **Review reports among the reading copies:** `REPORT_ADMISSION.md`, `REPORT_ERRATA_2.md`
- **Other independent reviews bound to it:** none
- **Note:** The exact computation is `PKT/scripts/run_adm.py` with `adm.py` (public check `admission`). `F1_PROOF.md` is, by its title, about the loose-role identities ("F1 repair: actual off-wall loose-role identities precede angle classification"). No separate written proof of the admission geometry is bound to this premise. The reviews bound to it are the two reports named in `READING_ORDER.md`, part 3; no other independent review is. One step, a bound on the side direction of a square whose centre is near a wall, is stated only as a comment and an assertion in `run_adm.py`, lines 17 and 18, and not in the proof text. See `KNOWN_ISSUES.md`, item 1.
- **Depends on:** ENDPOINT, FRAME_ASSIGNMENT, WALL_PARTITION, KEY_W_ELIMINATION, L_3, L_15, L_17, COARSE_LOOSE_CAPACITY, L_4

### 9. SELECTOR_LOGIC

- **Claim:** For each of the 84 root/rigid-label clauses, any one listed source-bound exact class implication suffices. A PSS option also requires its listed L_k receipt; every target must fit that clause root. Different clauses may choose different options. Four further signed actual-clause alternatives are explicitly listed in S6_ACTIVATION; their common frame and off-wall premises remain required. One fifth signed alternative, PS6/T17 ENDp for JPG17p/L6, is supplied by S6_ACTIVATION_AR with its own independent geometry review and authentic budget.
- **In the proof text:** the label `[premise:SELECTOR_LOGIC]` stands in paragraphs P005, P062, P068.
- **Files of record for it** (label `premise:SELECTOR_LOGIC` in `LABELS.tsv`): `research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/endp-import-AR/S6_ACTIVATION_AR.json`; `research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/s6-import-X/S6_ACTIVATION.json`; `research/finishing-threshold-goal-20261007/current-author-20261012t/third-order-20261010/key-w-active/PER_BRANCH_CAPTURE_OPTIONS_V5_PSS_PSE_KEYW.json`
- **Review reports among the reading copies:** `REPORT_ERRATA_2.md`, `REPORT_SELECTOR_A.md`, `REPORT_SELECTOR_B.md`, `REPORT_SELECTOR_C.md`
- **Other independent reviews bound to it:** none
- **Depends on:** CHARGE_SEMANTICS, ROOT_ADMISSION, KEY_W_ELIMINATION

### 10. LOCAL_CHECKER_SOUNDNESS

- **Claim:** SPEC3 exact geometry and polynomial certificate rules, exhaustive child coverage and terminal tests imply the whole-root EMPTY/TUBE theorem; the frozen Python and Node algorithms implement that specification in their accepted complete modes. For root-region EMPTY, use the cited notes corollary: root node equals the named region and terminal leaf count is zero. These statement bindings are enforced by acceptance/h_report30.py, not inferred from a bare checker PASS.
- **In the proof text:** the label `[premise:LOCAL_CHECKER_SOUNDNESS]` stands in paragraphs P005, P088.
- **Files of record for it** (label `premise:LOCAL_CHECKER_SOUNDNESS` in `LABELS.tsv`): `research/window-extension-20261008/SPEC_v3.0.md`; `research/window-extension-20261008/checker/wxcheck_v30.py`; `research/window-extension-20261008/checker2/wxcheck2_v30.js`
- **Review reports among the reading copies:** `REPORT_LOCAL_2C.md`, `REPORT_LOCAL_PY.md`
- **Other independent reviews bound to it:** `RC/extra/research/window-extension-20261008/reviews/REVIEW_30_JS.md`; `RC/extra/research/window-extension-20261008/reviews/REVIEW_30_PY.md`; `RC/records/reviews/REVIEW_30.md`; `RC/records/reviews/REVIEW_30_ACCEPT.md`
- **Depends on:** no other obligation

### 11. LOCAL_CERTIFICATE_IMPORT

- **Claim:** Every imported region result has matching pinned root/header, complete frozen-checker acceptance, and an independent record review. The accepted S_floor=R singleton-side trees apply at every actual S<=R by fixed-pose containment monotonicity: root and terminal charts are side-independent. Physical G20S is subsequently applied at actual L, never at the larger R. A leaf PASS or a count of cells is not a whole-root proof. Complete checker acceptance means the window lead's saved complete runs, not a polynomial-arithmetic replay by the import audit. Old JPG17m_v2/JPG3p_v2 records with PB11-only scope close no selected v5 root. For JPWS_v4, JPW13_v2x, JPG3p_v5 and JPG15m_v5 the final lead records and independent batch3–6 reviews are explicitly supplied alongside the early Codex import snapshots; exact statement/evidence comparisons preserve the same root conclusions.
- **In the proof text:** the label `[premise:LOCAL_CERTIFICATE_IMPORT]` stands in paragraphs P005, P089.
- **Files of record for it** (label `premise:LOCAL_CERTIFICATE_IMPORT` in `LABELS.tsv`): `research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/final-records-AV/FINAL_RECORDS.json`; `research/finishing-threshold-goal-20261007/current-author-20261012t/third-order-20261010/manuscript/SIDE_CAP_TRANSFER.json`
- **Review reports among the reading copies:** `REPORT_LOCAL.md`, `REPORT_MACTREES_FINAL.md`, `REPORT_RECORDS.md`
- **Other independent reviews bound to it:** none
- **Depends on:** LOCAL_CHECKER_SOUNDNESS

### 12. G20S_PHYSICAL

- **Claim:** Sixteen distinct actual unit squares other than label 4 in G20S, at actual S<=L, have all 45 exact-root core deviations zero. The input position/angle chart is rational-reference based; the zero-core conclusion is exact-root based. Sliders remain in the accepted wide domains. The G20S/HW trees also have complete v3.0 acceptance runs. This route uses the independently reviewed sixteen-square stopped contraction (ratio 159201934153319/200000000000000 < 1); the lead box-wide contraction (below 0.859) is an alternative, not a combined extra step. The G20S -> T1 -> HW -> T2 -> stopped-sixteen-square finite-entry chain preserves xi_(2,1)<=0 at both handovers. Zero exact-root core gives role 8 physical right/top corner contact at actual S<=L.
- **In the proof text:** the label `[premise:G20S_PHYSICAL]` stands in paragraphs P005, P092, P112.
- **Files of record for it** (label `premise:G20S_PHYSICAL` in `LABELS.tsv`): `research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/sixteen-square-corollary/producer/THEOREM.md`
- **Review reports among the reading copies:** `REPORT_ERRATA_2.md`, `REPORT_TERMINAL_2.md`
- **Other independent reviews bound to it:** `research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/sixteen-square-corollary/independent-review/REVIEW.md`
- **Depends on:** ALGEBRAIC_ENDPOINT, LOCAL_CHECKER_SOUNDNESS

### 13. WALL_CONTRADICTION

- **Claim:** An endpoint-normalized strictly smaller packing cannot satisfy the JG root: JG implies G20S, physical rigidity at actual L fixes role 8 at (L-1/2,L-1/2), axis(1,0), so it touches two L-walls, contradicting positive inset.
- **In the proof text:** the label `[premise:WALL_CONTRADICTION]` stands in paragraphs P005, P111, P112.
- **Files of record for it** (label `premise:WALL_CONTRADICTION` in `LABELS.tsv`): `research/finishing-threshold-goal-20261007/current-author-20261012t/join-design-files-20261009-1525/endpoint-normalization-producer/THEOREM.md`; `research/finishing-threshold-goal-20261007/current-author-20261012t/second-order-20261010/theorem/ENDPOINT_CASE_G_LEMMA.md`
- **Review reports among the reading copies:** `REPORT_COMPOSITION.md`
- **Other independent reviews bound to it:** `research/finishing-threshold-goal-20261007/current-author-20261012t/join-design-files-20261009-1525/independent-endpoint-normalization-review/REVIEW.md`
- **Depends on:** ENDPOINT, LOCAL_JG, G20S_PHYSICAL

### 14. KEY_W_ELIMINATION

- **Claim:** The literal KEY_W budget and occupied half-marker force the unique L9 parent into its gate-or-wall union. Off-wall its canonical tan-half direction satisfies 30651/100000<=t9<=44941/100000. Thus the old lower JPB predicate and the high atom 44941/100000<t9<1 are impossible. The retained JPA predicate is 591183/1408817<=t9<=44941/100000; all other case predicates remain unchanged. This eliminates actual cases, not every point of a padded JPB root.
- **In the proof text:** the label `[premise:KEY_W_ELIMINATION]` stands in paragraphs P005, P049.
- **Files of record for it** (label `premise:KEY_W_ELIMINATION` in `LABELS.tsv`): `research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/case-repair-S/PROOF.md`
- **Review reports among the reading copies:** `REPORT_COMPOSITION.md`
- **Other independent reviews bound to it:** `RC/records/reviews/join_roots/keyw_amendment/REVIEW_KEYW_AMENDMENT.md`
- **Depends on:** KEY_W, FRAME_ASSIGNMENT

### 15. COARSE_LOOSE_CAPACITY

- **Claim:** For any family of closed unit squares with pairwise disjoint interiors, contained in a square container of side s<=C=4675531/1000000 concentric with F_U=[0,1169/250]^2, each whole coarse centre region 3,15,17 specified exactly in PROOF_BRIDGE_V2.md has capacity at most one, with arbitrary independent orientations.
- **In the proof text:** the label `[premise:COARSE_LOOSE_CAPACITY]` stands in paragraphs P005, P055, P066.
- **Files of record for it** (label `premise:COARSE_LOOSE_CAPACITY` in `LABELS.tsv`): `research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/coarse-capacity-AP/PROOF_BRIDGE_V2.md`; `research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/coarse-capacity-R/PROOF.md`
- **Review reports among the reading copies:** `REPORT_CAPACITY_LEMMA.md`, `REPORT_FRAME.md`
- **Other independent reviews bound to it:** `research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/coarse-capacity-AP/ACCEPTED_INTERFACE_V2.json`
- **Depends on:** no other obligation

## 4. The independent review reports and the records of the tree work

The 29 reports under `RC/reports/` are reading copies: lines about the organisation of the work were removed or replaced, a note was added at the head of each, and names of the earlier executions were replaced by neutral designations. `EDITED_LINES.tsv` lists every edit (297 in all: 90 lines removed, 178 replaced, 29 added). For each it gives the file, the line number in the original, the action, the SHA-256 of the original line, the new text and a reason. **It does not give the text of a removed or replaced line.** `edit_list.json` holds the same fields, and `REVIEW_HASHES.json` gives the SHA-256 of each copy and of its original. The originals are not in this edition. A reader can therefore see where a copy was edited, what stands there now and why, but cannot see what a removed or replaced line said, and cannot rebuild an original. **Line numbers that a report cites about itself or about another report refer to the originals.** `EARLIER_EXECUTIONS.tsv` maps each neutral designation to the name the earlier execution had.

The two hash tables name each copy at the path where this edition carries it.

**Further extracts.** `RC/extra/` holds 11 files: 8 tables named `<file>.EDITS.tsv` and 3 extracts. Each table lists the lines that were replaced or removed in one further review or record, in the same way as in the reading copies: the path of the file it replaces, the SHA-256 of that file and of the copy, the line number, the action, the SHA-256 of the original line and the new text (76 rows in all; no row gives the text of an original line). For 3 of the tables the extract stands beside the table and has the SHA-256 that the table gives for the copy: `REVIEW.md`, `REVIEW_30_JS.md`, `REVIEW_30_PY.md`. For the other 5 (`extra/fifth-order-20261010/jpa-import-AG/LEAD_RECORD.md.EDITS.tsv`, `jpa-import-AG/INDEPENDENT_REVIEW.md.EDITS.tsv`, `window-capture/fifth-order-20261010/jpa-import-AG/LEAD_RECORD.md.EDITS.tsv`, `JPW13_v2x/LEAD_RECORD_SNAPSHOT.md.EDITS.tsv`, `JPWS_v4/LEAD_RECORD_SNAPSHOT.md.EDITS.tsv`) no file of the edition has the SHA-256 that the table gives for the copy. For these the table shows which lines were edited, not the bytes that are carried. The files that the tables name under `replaces` are not in the edition.

**The tables of the reading copies are carried apart from the copies.** The copies are under `RC/`. Their 7 tables are carried in folders named by a SHA-256, under `research/finishing-threshold-goal-20261007/clean-rerun-20261011/reseal-resume-1120/graphs/objects/`: `REVIEW_HASHES.json` in `4da8d938feaf.../`; `RECORD_HASHES.json` in `cce600b80d0d.../`; `EDITED_LINES_RECORDS.tsv` in `d349189dfc4e.../`; `edit_list.json` in `126c9e391fc2.../`; `record_edit_list.json` in `631d325a92f8.../`; `EARLIER_EXECUTIONS.tsv` in `e57f088880ce.../`; and under `research/finishing-threshold-goal-20261007/clean-rerun-20261011/reseal-t-1420/grapht/objects/`: `EDITED_LINES.tsv` in `b0092f4edbd1.../`. The producers' roster lists each table at that path with its SHA-256. A folder name is not always the SHA-256 of the file inside (it is for 2 of the 7; for the others the name is the SHA-256 of another version of the table), so go by the roster and by `MANIFEST.sha256`, not by the folder name.

The last two columns say how a report is tied to the proof. "Obligations" is the number of obligations that list the report among their evidence files in `OBLIGATIONS.json`. "Labels" are the labels of `LABELS.tsv` that name it. A report with 0 and no label is not named by an obligation; it is carried because it belongs to the reading of the audit (`AUDIT.md`), for example a review of the composition or of a checker. The number says nothing about what the report found.

| Report | sha256 | Obligations | Labels |
|---|---|---|---|
| `REPORT.md` | `b81f450e63c4adf9` | 3 | none |
| `REPORT_ADMISSION.md` | `dd31cfa4c8545bab` | 0 | `premise:ROOT_ADMISSION` |
| `REPORT_A_charge.md` | `f8be3116ef169002` | 2 | none |
| `REPORT_B_local.md` | `7136815b33bb7a2b` | 4 | `file:ENVELOPE_REVIEW` |
| `REPORT_CAPACITY_LEMMA.md` | `0fd99f5564807e83` | 1 | `premise:COARSE_LOOSE_CAPACITY` |
| `REPORT_CHARGE_CORE.md` | `1f1c43851adbf68f` | 0 | `file:CHARGE_CORE_DERIVATION`, `premise:CHARGE_SEMANTICS` |
| `REPORT_CHARGE_SEMANTICS.md` | `de635a114810b989` | 1 | none |
| `REPORT_COMPOSITION.md` | `6a44fd31f4feb4fd` | 0 | `premise:KEY_W_ELIMINATION`, `premise:WALL_CONTRADICTION`, `premise:WALL_PARTITION` |
| `REPORT_C_frame.md` | `23d8b55034786178` | 5 | none |
| `REPORT_D_join.md` | `24308f7432236952` | 5 | none |
| `REPORT_ERRATA.md` | `f76391d5b5f76858` | 0 | none |
| `REPORT_ERRATA_2.md` | `505bd3aac850454c` | 0 | `premise:CHARGE_SEMANTICS`, `premise:G20S_PHYSICAL`, `premise:ROOT_ADMISSION`, `premise:SELECTOR_LOGIC` |
| `REPORT_FRAME.md` | `6b7ba895f64ea1ae` | 0 | `premise:C7_C8_TRANSFER`, `premise:COARSE_LOOSE_CAPACITY`, `premise:FRAME_ASSIGNMENT`, `premise:WALL_PARTITION` |
| `REPORT_LOCAL.md` | `6794992f414b5480` | 0 | `premise:LOCAL_CERTIFICATE_IMPORT` |
| `REPORT_LOCAL_2C.md` | `4f24555af2eb75b1` | 0 | `premise:LOCAL_CHECKER_SOUNDNESS` |
| `REPORT_LOCAL_CHECKERS_IMPORT.md` | `75b8855faf6a6ae9` | 2 | none |
| `REPORT_LOCAL_PY.md` | `ecbbfd3dcb86d81e` | 0 | `premise:LOCAL_CHECKER_SOUNDNESS` |
| `REPORT_MACTREES_FINAL.md` | `e9e4de08810f4aa3` | 0 | `premise:LOCAL_CERTIFICATE_IMPORT` |
| `REPORT_MARKER_CONVERSION.md` | `e1ead69908beb73d` | 1 | none |
| `REPORT_ORBIT.md` | `57bc90c7698a7589` | 0 | `premise:CHARGE_SEMANTICS` |
| `REPORT_RECEIPTS.md` | `5fbb4925c4ff10c9` | 0 | `file:RECEIPT_ASSESSMENT` |
| `REPORT_RECORDS.md` | `3c2caee059c4fd54` | 0 | `premise:LOCAL_CERTIFICATE_IMPORT` |
| `REPORT_S6_join_PS06T17ENDp.md` | `389c8a00f0f22bad` | 3 | none |
| `REPORT_S6_joins.md` | `c6add8582d6f2c63` | 3 | none |
| `REPORT_SELECTOR_A.md` | `af475de7dc09e10f` | 0 | `premise:SELECTOR_LOGIC` |
| `REPORT_SELECTOR_B.md` | `a9ed6821e298a86e` | 0 | `premise:SELECTOR_LOGIC` |
| `REPORT_SELECTOR_C.md` | `3765c2320e8cfb81` | 0 | `premise:SELECTOR_LOGIC` |
| `REPORT_TERMINAL_2.md` | `db59fe0da7d13dda` | 0 | `file:FINITE_ROW_DERIVATION`, `premise:G20S_PHYSICAL` |
| `REPORT_UPPER_EXACT.md` | `506d6c8288828d58` | 0 | `premise:UPPER` |

The 20 records of the tree work (9 reviews of the tree checkers and the regions, 11 region records) are reading copies in the same sense, under `RC/records/`: `EDITED_LINES_RECORDS.tsv` lists every edit (253 in all: 229 lines replaced, 20 added, 4 removed) with the same columns, again without the text of the original line; `record_edit_list.json` holds the same fields; `RECORD_HASHES.json` gives the SHA-256 of each copy and of its original. **Hashes and line numbers that these records cite, also for each other, are those of the sealed originals.** Statements of status inside a record describe the day of the record.

| Record | sha256 |
|---|---|
| `bigbox/join/RECORD_EJG_v2.md` | `aa4931c5246af907` |
| `bigbox/join/RECORD_EJPA_v5.md` | `24a7a4d625b6b2e1` |
| `bigbox/join/RECORD_EJPG15m_v5.md` | `2ba460f0695bcea4` |
| `bigbox/join/RECORD_EJPG15p_v5.md` | `6fabbcd875b57f36` |
| `bigbox/join/RECORD_EJPG17m_v5.md` | `f26d995fb9017fb2` |
| `bigbox/join/RECORD_EJPG17p_v5.md` | `7e6750bceefeab9d` |
| `bigbox/join/RECORD_EJPG3m_v5.md` | `2fca7b5b1a05e65d` |
| `bigbox/join/RECORD_EJPG3p_v5.md` | `0e66116336814bc2` |
| `bigbox/join/RECORD_EJPW13_v2x.md` | `3ca62dd1396b61ea` |
| `bigbox/join/RECORD_EJPWS_v4.md` | `8ece74d148f51994` |
| `bigbox/join/RECORD_EJQ_v1.md` | `fb74f216cfbf016d` |
| `reviews/REVIEW_30.md` | `85ad0498b2ae47cb` |
| `reviews/REVIEW_30_ACCEPT.md` | `c64708f23a3eab19` |
| `reviews/join_roots/REVIEW_JOIN_ROOTS_V2.md` | `f267ae76954bf1f7` |
| `reviews/join_roots/batch2/REVIEW_BATCH2.md` | `e34abbf4ab5c94d4` |
| `reviews/join_roots/batch3/REVIEW_EJPG15m_v5.md` | `80a84fb8a869ecff` |
| `reviews/join_roots/batch4/REVIEW_EJPG3p_v5.md` | `7e2d1935775ae8c9` |
| `reviews/join_roots/batch5/REVIEW_EJPW13_v2x.md` | `c617776554d5b04e` |
| `reviews/join_roots/batch6/REVIEW_EJPWS_v4.md` | `53c70a667c0e6bf5` |
| `reviews/join_roots/keyw_amendment/REVIEW_KEYW_AMENDMENT.md` | `8bd94339f25c8b41` |

## 5. The computations

- Capture: `CAP/CAPTURE_AUDIT_INPUTS.json` names the audit record of each statement; `CAP/statements/<ID>/audit.json` names its inputs, receipts and selected slices; `PKT/runtime/RECEIPT_ROSTER.json` gives the same per statement of the proof. The checkers, the launcher and the plan are under `CAP/checker_sources/`. `recompute_slice.py` recomputes any range of rows. The comparison with the earlier executions: `local-research/claude-20261002/rerun-clean-20261011/records/` and `check_comparison_records.py`.
- Trees: the specification is `research/window-extension-20261008/SPEC_v3.0.md` with `SPEC_v3.0_NOTES.md`; the checkers are `research/window-extension-20261008/checker/wxcheck_v30.py` and `research/window-extension-20261008/checker2/wxcheck2_v30.js`. `CHECK.md` lists the 13 certificates.
- The 31 public checks: `PKT/runbook_public.json`; what each read in the producers' stored replay: `PKT/PUBLIC_REPLAY_RESULTS.json`; the supported entry point: `PKT/PUBLIC_ENTRYPOINTS.md`.
