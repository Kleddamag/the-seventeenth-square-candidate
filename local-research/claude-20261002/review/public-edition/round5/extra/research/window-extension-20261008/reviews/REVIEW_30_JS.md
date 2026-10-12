# REVIEW 30 (Node): the draft checker `checker2/wxcheck2_v30.js` for specification version 3.0

Reviewer: an independent reviewer session (the reviewer of the frozen 2.6 checkers, `reviews/REVIEW_26.md`, and of the Python candidate for
3.0, `reviews/REVIEW_30_PY.md`). Started 9 October 2026. I wrote none of the reviewed
files and had not seen this file, its diff or its author's notes before. The notes were read only for part J6,
after J1 to J5.
What I wrote: this file and the folder `reviews/r30js/` (scripts, test certificates, outputs, logs).

Reviewed state (SHA-256, verified at the start):

| file | SHA-256 |
|---|---|
| `checker2/wxcheck2_v30.js` as given to me (the DRAFT; 3,784 lines) | 8aa489f4cf88a9af33737d2d89627a16f1d496decc229f244eb0dae5759e0927 |
| `checker2/wxcheck2_v26.js` (frozen 2.6 Node checker; 2,966 lines) | a725c230b4454462ccaad0ef7c92271cc1c3ac3a2ef19e0b5054db332a723968 |
| `SPEC_v3.0.md` = `proto30/SPEC_v3.0_final.md` (the final text; 885 lines) | 0a6dfc2ae10ed6f30a21ebe357a6e73dd7355223c521cc67a3f2bdab9549aba0 |
| `checker2/wxcheck2_v30.js` as FROZEN by its author at 03:10 (3,818 lines; parts J8, J5, J7) | 97210adf74a3ebed7cde021a3cb1ff6ea6380d8d2d55540a2a2a1cb17dc27542 |

The draft was replaced by its author at 02:42, while I was reading (the last pass that the lead announced). To have
a fixed object I rebuilt the draft from my own diff (`patch` of the frozen file with
`r30js/CODE_v26_to_v30_js.diff`; the result has the hash above) and keep it read-only as
`r30js/wxcheck2_v30_draft_8aa489f4.js`. **Parts J1 to J6 are about that file; its line numbers are used
throughout.** The last pass is reviewed as a diff in part J8.

The parts are written as they are finished. The status of each part is in its first line.

**Verdict (part J7, at the end): the frozen file 97210adf... is SOUND AS FAR AS REVIEWED: KEEP FROZEN. No MUST.**
One finding on the way, fixed before the freeze: the help option of the draft (and of both frozen 2.6 checkers)
ended with exit code 0 without checking anything (J4).

## J1. The diff against the frozen 2.6 file, hunk by hunk

Status: DONE (reading); the regression runs that confirm it are in J5.

`diff checker2/wxcheck2_v26.js checker2/wxcheck2_v30.js` (mine, kept as `r30js/CODE_v26_to_v30_js.diff`): 64 hunks,
848 lines added, 30 lines of the frozen file replaced, none removed without replacement. The author's own diff file
`checker2/v30/diff_v26_v30.txt` has the same 64 hunks; I used mine. I read every hunk and then the whole draft once
from top to bottom.

The gate is the module variable `SCHEMA3` (469), set by `useSchema` (471-474), which is called in two places:
`Validator.header` (1118), as soon as the schema string has been tested and before anything else of the header is
read, and `CertChecker.checkNodeText` (3393), before every node. "Effect under wx-cert-2" = can the hunk change the
verdict, the reason or the report for a certificate whose header says "wx-cert-2", with the default options.

| # | lines (draft) | what the hunk does | passage of the final text | effect under wx-cert-2 |
|---|---|---|---|---|
| 1 | 4 | comment: two schema strings | - | none |
| 2 | 6-7 | comment: name, version and SHA-256 of the specification. The hash is that of the audited candidate (2cec6f72...), not of the final text | - | none (see J8) |
| 3 | 10-37 | comment: what version 3.0 adds, where it is implemented | - | none |
| 4 | 457-475 | `SCHEMA3` (false when the file is loaded) and `useSchema(true or false)`; any other argument is an internal error | THE TWO SCHEMAS; section 10, SCHEMA RULE | none: under wx-cert-2 the flag is false |
| 5 | 491-493 | `varName`: text `z#n` for a variable number >= NVAR (messages only) | section 3, INDICATOR VARIABLES | none (no such variable exists) |
| 6 | 636-662 | `squareHot` (square of an integer coefficient array) and `binomBig` (binomial coefficient as BigInt) | 4.9; 5 CENTRED RULE | none (not called) |
| 7 | 664 | end marker of the block | - | none |
| 8 | 917-936 | `parseFactName`: `sq:NAME`, `pol:NAME` (NAME matches `[A-Za-z0-9_]+`, exactly two parts), `ind:i:j:k` (four parts; labels of I without leading zero; i < j; k one digit 1 to 8). Each case begins with `if (!SCHEMA3) return bad` | section 10, FACT names; (W) "the index of an ind name is one digit 1 to 8" | none: the three cases return the string of the default case, so the rejection and its words are those of the frozen file |
| 9 | 958-964 | `Validator` constructor: `strictKeys` is gone; the map `unknownKeys` is kept and stays empty | section 10, KEYS | none with default options (the removed option `--ignore-unknown-keys` was off by default) |
| 10 | 966 | end marker | - | none |
| 11 | 970-973 | `Validator` gets `qforms` and `assumeOptPairs` (both set again for every node, hunk 31) | section 3; 4.10 (R3) | none |
| 12 | 980-981 | `obj()`: a key that is neither required nor optional always rejects | KEYS | none with default options |
| 13 | 1082-1085 | `region()` (window, tube): optional key list `SCHEMA3 ? ['centre'] : []` | section 10, header `centre`; KEYS | none: the call is the frozen call; `centre` is an unknown key |
| 14 | 1096-1107 | `region()`: `if (SCHEMA3 && v.has('centre'))` read the map (exactly the labels of I, every value a unit rotation), else `centre = null`; the result gets the field `centre` | sections 8, 10 | none: the read is gated at the point of use; `centre` is null |
| 15 | 1113-1119 | `header()`: `schema` must be the string "wx-cert-2" or "wx-cert-3"; then `useSchema` | section 10, first item | a header with "wx-cert-3" is no longer rejected (the frozen file's test `F36`). For a third string the rejection stays, with other words ("... or "wx-cert-3"") |
| 16 | 1153-1154 | the header object returns `schema` and `schema3` | - | none |
| 17 | 1214-1225 | `factRef()`: a parsed name of kind sq, pol or ind under wx-cert-2 is an internal error; for sq and pol the form `q:NAME` must be in the node's `qforms`, else reject | 4.9 last sentence; (W) | none (the kinds cannot occur) |
| 18 | 1246-1251 | `forms()`: `if (SCHEMA3 && name.startsWith('q:'))` the key goes to `qform` | section 10, `forms` | none: a key `q:X` reaches the frozen test and is rejected ("must match [A-Za-z0-9_]+") |
| 19 | 1272-1325 | new: `baseVarNumber` (the name of a base variable, parsed like a form name), `qform` (nonempty list; entries of exactly two elements; a number; a list of 0 to 2 base variable names; monomials pairwise different as multisets; coefficient 0 allowed) | section 3 POLYNOMIAL FORMS; section 10 | none (not called; `qform` begins with an internal error under wx-cert-2) |
| 20 | 1327 | `qforms.set(NAME, ...)` (last line of `qform`) | - | none |
| 21 | 1329-1346 | new: `stepCentre` (a JSON object; every key a base variable name; every value a number) | section 10, step `centre` | none (not called; internal error under wx-cert-2) |
| 22 | 1388 | `indSeen` (pairs with an `ind` declaration in this round) | 4.10 (R1) | none |
| 23 | 1421-1453 | `round()`: the mode "ind" under `SCHEMA3`: exactly the keys i, j, mode, options; i < j labels; 1 to 8 options, each with exactly o, t, axis, eps, {o,t} = {i,j}, pairwise different; (R1); (R3); the message for an unknown mode names three modes under wx-cert-3 | 4.10 DECLARATION, (R1), (R3); section 10 | none: `SCHEMA3 && mode === 'ind'` is false, and the last `else` is the frozen rejection with the frozen words |
| 24 | 1455-1462 | (R2), after all declarations of the round are read | 4.10 (R2) | none (`indSeen` is empty) |
| 25 | 1469-1471 | a step may have the key `centre`: `SCHEMA3 ? ['centre'] : []` | section 10; KEYS | none: the frozen call |
| 26-28 | 1492, 1497, 1500 | the flag `pol` of a term; a comment at the sign rule | (T1), (T2) | none |
| 29 | 1502-1504 | (T2): a term with a `pol` name and no `circ` name rejects, in every round | (T2); (W) | none (no `pol` name exists) |
| 30 | 1507-1512 | `if (SCHEMA3 && s.has('centre'))` read the centre; the step object gets the field `centre` (null without the key) | section 5; section 10 | none: gated at the point of use; `centre` is null |
| 31 | 1591-1597 | `node()`: `qforms` and `assumeOptPairs` are made new for the node, before its `forms` and rounds are read; the pairs with an option assumption are collected | section 3 ("not inherited by children"); (R3) | none |
| 32 | 1603 | the node object returns `qforms` | - | none |
| 33 | 1869-1901 | `NodeCtx`: `qDen`, `qHot`, `qSPoly` (a polynomial form as integer arrays over the lcm of its denominators, and as a rational polynomial) | section 3 | none (not called) |
| 34 | 2180-2186 | `RoundCtx` gets `indDecl`, `indListed`, `nz` | section 3 ("They belong to the round") | none (stay empty) |
| 35 | 2204-2231 | `declare()`: the `ind` declaration: every option of the pair that is not listed must be excluded on the start store; the pair gets the m - 1 variable numbers from NVAR + nz on; `indListed` maps the k-th listed option to (i, j, k) | 4.10 PRECONDITION, INDICATORS; section 10 | none: unreachable (and an internal error under wx-cert-2) |
| 36 | 2304-2305 | `fact()`: names of kind sq, pol, ind go to `_fact3` | (T4) | none |
| 37 | 2313-2347 | `_fact3`: `ind:i:j:k` needs a declaration of the pair in this round and k <= m; its polynomial is the variable for k < m and 1 minus the others for k = m (the constant 1 for m = 1); sq and pol entries carry the form and the denominator | 4.10 NAME, INDICATORS; (T4) | none |
| 38 | 2349-2363 | `_hot3`, `_poly3`: the arrays of an entry, built when a term is expanded | 4.9 | none |
| 39 | 2408-2419 | `_factPoly`, case opt: available iff OPT-AVAILABLE or (under `SCHEMA3`) IND-LISTED | (T4), 4.5 | none: `!(SCHEMA3 && ...)` is true, the condition and the message are the frozen ones |
| 40 | 2616-2617 | marker | - | none |
| 41 | 2619-2957 | new: `_guardRule` (T3), `lowerBound3` (Rem as one integer map over one denominator), `_shift3` (the substitution v = c + y), `_bound3` (the interval sum), `lowerBoundReference3` (the same number by plain rational arithmetic, for `--paranoid`) | (T3); section 5 STEP, RAW RULE, CENTRED RULE | none (not called, see hunks 42-44) |
| 42 | 2970-2972 | `checkStep`: `if (SCHEMA3 && this.indListed.size !== 0) this._guardRule(...)` after the names of the term have been made available | (T3); (E) | none |
| 43 | 2977-2983 | `checkStep`: L by `lowerBound3` under wx-cert-3, by the frozen `lowerBound` under wx-cert-2; a step with a centre under wx-cert-2 is an internal error | section 5 | none: the frozen function is called with the frozen arguments |
| 44 | 2986 | `--paranoid`: the reference evaluation follows the same choice | - | none |
| 45 | 2989 | marker | - | none |
| 46 | 2998 | an accepted `0` step also returns its L (in lowest terms) | report only | none for the verdict; see hunks 55, 56 |
| 47 | 3093-3103 | `terminalTest`: with a tube centre under wx-cert-3 the endpoint is `conj(gammaT) * rho * P`, else `rho * P`; a tube with centres under wx-cert-2 is an internal error | section 8, TERMINAL TEST | none: `gamma` is null, `rel` is `rho` |
| 48 | 3105-3107 | the two tests use `rel`; the messages say "absolute arc endpoint" without a centre (the frozen words) | section 8 | none |
| 49 | 3109 | marker | - | none |
| 50-52 | 3127, 3141, 3213-3217 | `checkNode` remembers the L of the first accepted `0` step and returns it as `zeroStepL` if the node is closed as infeasible by that step | report only | none for the verdict |
| 53 | 3338-3355 | `checkRoot`: with a window centre under wx-cert-3 the endpoints are `conj(gamma) * rho * P`; an extra message for a non-positive cosine in that case; the schema of the header must be the schema in force, else internal error; the three frozen tests follow unchanged | section 8, ROOT CONTAINS WINDOW | none |
| 54 | 3391-3393 | `checkNodeText`: `useSchema(this.header.schema3)` before every node | SCHEMA RULE | none |
| 55, 56 | 3411-3413, 3594-3595 | the node entry of the `--json` report gets the key `zero_step_L` when the node is closed as infeasible by a `0` step | report only | **the report changes**: the key appears under wx-cert-2 too |
| 57, 58 | 3653, 3672-3673 | the option `--ignore-unknown-keys` is removed from the usage text and from `main`; the word is now an unknown option (usage error, exit code 2) | KEYS | only for a caller that gave the option |
| 59-61 | 3705-3711, 3714, 3718 | report: `spec` is "SPEC.md version 3.0"; new keys `schema`, `window_centres`, `tube_centres` | report only | **the report changes**: `spec` differs and the three keys are written under wx-cert-2 too ("wx-cert-2", false, false) |
| 62 | 3741-3743 | one more output line, `schema=...`, after the line `labels=... S_floor=...` | output only | **the output changes** by this line (the first line, the verdict, is unchanged) |
| 63 | 3753 | the output line "unknown keys ignored ..." is gone with the option | - | none with default options |
| 64 | 3769-3770 | exports for tests: `SCHEMA3` (getter), `useSchema`, `squareHot`, `binomBig`, `hotOf`, `mulHot` | - | none for the command line |

**Claim.** For a certificate with the schema "wx-cert-2" and the default options the draft returns the verdict of
the frozen file, with the same reason, the same exit code and the same node entries (closure, evidence, digest of
the final store), and it differs from the frozen file in the report and the output only by: the value of `spec`;
the three keys `schema`, `window_centres`, `tube_centres`; the key `zero_step_L` in the entry of a node closed by a
`0` step; the output line `schema=wx-cert-2`.

**Proof by reading.** `SCHEMA3` is false from the header on (1118) and is set to false again before every node
(3393). Go through the table: hunks 8, 13, 14, 18, 23, 25, 30, 39, 42, 43, 44, 47, 53 test the flag at the place
where the new behaviour would begin and take the frozen path; hunks 17, 19, 21, 35, 37 and the gates in 43, 47, 53
turn an impossible arrival of a new element into an internal error, which the driver reports as FAIL; hunks 24, 29,
31, 34 work on sets that stay empty. Hunk 12 makes unconditional what the frozen file did with its default option.
Hunk 15 changes the test of the schema string, which a wx-cert-2 certificate passes in both files. The remaining
hunks are comments, new functions that are not called, and the report. The frozen function `lowerBound` (2511-2598)
has no hunk and is the one called. The two things the lead named, the empty id and the name and hash of the
specification, are not in the draft; they are the last pass (J8).

Unlike the Python candidate, whose report under wx-cert-2 has exactly the keys of its frozen file, this draft
writes its new report keys under both schemas. That is a choice, not a defect; a program that compares 3.0
reports of the two checkers must know it (the keys are `schema`, `window_centres`, `tube_centres` on both sides;
`zero_step_L` exists only here).

**Confirmation by runs** (J5): 586 wx-cert-2 files of the two 2.6 corpora, frozen file against draft, whole
reports compared apart from the listed keys.

## J2. Every new rule of the final text against the code; the lists (W) and (E)

Status: DONE. Direction of the question: can the code accept what the text rejects. **Result: in the draft I
found no input that the final text rejects and the draft accepts, except the empty node id** (final text, section
7: "a node id is a non-empty JSON string"; the draft accepts it, as the frozen 2.6 Node file does; it is the
announced change of the last pass, J8).

Test files: my 477 files of the Python review (`r30py/certs/attack`, `p8`, `p6`, `excl`, `excl2`), run again on
the draft WITH the reasons (`r30js/j_run.py mine`, `out/mine_results.json`): 475 as I derive them from the text,
every rejection for the planted reason; the two others are the empty-id files (on the frozen file: 477 of 477, J5). Names of files below are those of
`r30py/certs/attack/` unless a folder is given; "un" = the item stands in a round that is not evaluated, "ev" = in
an evaluated one.

### J2.1 The new rules

| rule of the final text | where in the draft | my files | result |
|---|---|---|---|
| (T1) lambda >= 0 unless the term has a `circ` name; whole file; whatever the names | `Validator.round` 1499-1501 (while the round is read) | `R01` (un), `R20` (a guarded corner with a negative multiplier), `X01`, `X07` (circ, either sign: accepted) | as the text |
| (T2) `pol:NAME` only in a term with a `circ` name; whole file; also with the multiplier 0 | 1492-1504 | `R02` (un), `p8/c03d` (multiplier 0; ev and un) | as the text |
| (T3) GUARD RULE: a corner name of an IND-LISTED option O_k needs `ind:i:j:k` with THAT k in the same term; also in a `circ` term; also with the multiplier 0; evaluated rounds only | `_guardRule` 2626-2640, called for every term in `checkStep` 2972, before any multiplier is looked at | `R14`, `R21` (multiplier 0), `R22` (indicator of another pair), `R24` (two options, one guard), `R25` (circ and pol, no guard), `R31` (m = 1); `R23` (two corners of one option, one guard: accepted); `R03` (un: accepted) | as the text |
| (T4) availability of every name of every term, also with the multiplier 0; evaluated rounds only | `fact` 2303-2313, called for every name of every term in `checkStep` 2969; `_fact3` 2323-2348; `_factPoly` 2374-2473 | `R26`, `R27`, `R32`; `p8/c03a`-`c03g2` (multiplier 0); `R04a`, `R04b` (un: accepted); `p6/a1`-`a4`, `a6`, `a9` (un accepted, ev rejected) | as the text |
| a corner name is available iff its option is OPT-AVAILABLE or IND-LISTED | `_factPoly`, case opt, 2414-2418 | `p8/c03a`, `R26` | as the text |
| `ind:i:j:k` available iff the pair has an `ind` declaration in THIS round and k <= m | `_fact3` 2326-2328 | `R27`, `R32`, `p8/c03g`, `c03g2` | as the text |
| (R1) one `ind` declaration per pair and round | 1447-1448 | `R07` (un) | as the text |
| (R2) no `opt` and `ind` declaration of one pair in a round | 1455-1461 | `R08` (un); `R29` (opt in round 1, ind in round 2: accepted) | as the text |
| (R3) no `ind` declaration for a pair with an option assumption of the node, in any round | 1449 with 1594-1596 | `R09` (un); `R30` (a SIGN assumption: accepted) | as the text |
| shape of an `ind` declaration: exactly the keys i, j, mode, options; 1 to 8 options, each exactly o, t, axis, eps, of the pair, pairwise different | 1429-1450 | `R12` (un), `S13`-`S17`, `S10` | as the text |
| PRECONDITION: every option NOT in the list is excluded (4.7) on the store at the START of the round; a failing declaration rejects, used or not; evaluated rounds only; a listed option may be excluded | `declare` 2212-2221 with `view.excluded` 2121-2132 of the `StoreView` of the round's start store (`checkNode` 3134-3135) | `P01`-`P05`, `R33`; `R10` (un: accepted); `excl2/X1`-`X7` (the exclusion depends on a CUT of the start store); `X11`, `P03` (an excluded option in the list) | as the text |
| the indicator variables belong to the round | `RoundCtx` is made new for every round (3134); `indDecl`, `indListed`, `nz` 2183-2185; the numbers NVAR + nz are given in `declare` 2224-2225 | `X13a`, `X13b` (lists of 2 and 3 for one pair in two rounds, exact L in round 2) | as the text |
| ind_k = z_k for k < m, ind_m = 1 - z_1 - ... - z_(m-1); m = 1: the constant 1 | `_fact3` 2330-2342 | `X08` (the two indicators of a list of 2 add up to the constant), `X09`, `X11`, `X12` (the list in the other order), `X15`, `K05` (m = 1) | exact L as the text |
| SB of an indicator variable is [0, 1] | `_bound3` 2853 (`lowerBoundReference3` 2944) | all `X` pairs with indicators | exact L |
| q forms: key `q:NAME`; nonempty; entries [number, list of 0 to 2 base variable names]; monomials pairwise different as multisets; coefficient 0 allowed; of the node, not inherited | `forms` 1250; `qform` 1301-1328; reset per node 1594 | `Q01`, `Q05`-`Q08`, `Q10`, `Q11`, `Q03` (child), `Q15` (the same name in two nodes, exact L), `Q09` (zero form) | as the text |
| `sq:NAME`, `pol:NAME` need `q:NAME` in the node's `forms`; whole file | `factRef` 1220-1224 | `R05`, `R06` (un), `Q04`, `Q12` | as the text |
| `q:NAME` is not a form NAME (no objective, no cut, no component of a custom form) | `formRef` 1193-1206 through `parseFormParts` 748-790 (no case `q`) | `Q13`, `Q14`; the referee's `r30/d/A_P3`-`A_P8` in the lead's cross-run | as the text |
| `centre` of a step: an object; keys base variable names; values numbers; whole file | 1510 and `stepCentre` 1335-1345 | `C01`-`C08`, `R11` (un) | as the text |
| RAW RULE / CENTRED RULE, exactly | `lowerBound3` 2655-2722, `_shift3` 2738-2834, `_bound3` 2848-2902 | 18 pairs `X01`-`X17` (claim at L accepted, at L + 10^-30 rejected), `Q15`; J3 and J5 for the stress set | exact |
| a step WITH the field, also `{}`, is centred; a value for a variable that does not occur has no effect | 2715-2721; `_shift3` 2758 (`moved === 0`) | `X02` (empty centre), `X06` | exact |
| header centres: exactly the labels of I, unit rotations, window and tube independent | `region` 1100-1105 | `D04`, `D06`, `D12`, `D08`, `D09` | as the text |
| ROOT CONTAINS WINDOW with centres: Ab = conj(gamma) * rho * P | `checkRoot` 3347-3358 | `D02`, `D09`; `D07` (half turn everywhere: accepted) | as the text |
| TERMINAL TEST with centres | `terminalTest` 3100-3108 | `D03`, `D08`, `D10` (accepted by 6.7e-10), `D11` (rejected by 3.3e-10) | as the text |
| SCHEMA RULE: under wx-cert-2 every new element rejects where it occurs | the gates of J1 (hunks 8, 13, 14, 18, 23, 25, 30) | `S01`-`S06` (five of them un), `S07a`-`S08` (other schema strings) | as the text, with the words of the frozen file |
| KEYS | `obj` 975-984 and its 18 callers; a term has exactly two elements 1483 | `S09`-`S13`, `C09`, `D05`, `D13` | as the text |

### J2.2 List (W), WHOLE FILE, clause by clause

Everything below is tested inside `Validator.node` (1574-1604), which reads all rounds of the node in a loop
(1600-1601) before the node is checked; so each test is made for every node and every round.

| clause of (W) | where | my files (all "un") |
|---|---|---|
| KEYS | `obj` 975-984 | `p6` (the referee's rows), `S04` |
| numbers, labels and pairs | `parseNum` 351-359; `label` 1000-1005 (a number token of at most two digits, no leading zero); `nameLabel` 731-735; `pairIJ` 1157-1161; `optionFields` 1169-1173; `pmInt` 1007-1010; `k12` 1012-1015 | `p8/c08` (25 files), `p6/a5`, `h1`-`h12` |
| node data (lo <= hi, S_lo <= S_hi, cos > 0, sin P- <= sin P+, unit rotations) | `node` 1582-1585; `boxMap` 1054; `arcMap` 1066-1072; `rot` 1025-1030 | 2.6 corpus |
| 1 to 3 names per term | 1489 | `p8/c02c` |
| G^2 + H^2 <= 1 in a `tan` name | `parseFactName` 843, 858 | `p8/c01b`, `c01d` |
| `ivl:FORM` only for Da, Db or an affine custom form | `factRef` 1233-1234 | `p8/c02d` |
| no `cut` name and no key of `cuts` for the form `0` | 1230; `store` 1376 | `p8/c02e`, `c04` |
| `u:NAME` defined: objective, fact name, key of `cuts` | `formRef` 1199-1203, called from 1472, 1227, 1375 | `p8/c02b` (4 files) |
| `q:NAME` of a `sq` or `pol` name defined | 1220-1224 | `R05`, `R06` |
| the index of an `ind` name is one digit 1 to 8 | 933 | `R13a` |
| (T1) and (T2) for every term whatever its multiplier | 1501, 1504 | `R01`, `R02`, `p8/c03d` |
| a step on the form `0` has the sense "lo" | 1477 | `p8/c02f` |
| the shape of every declaration, with `kappa` for Pk and Ps; `kappa` on P+/P-, if present, a number | 1396-1420 (1411, 1412) | `p6/a7`, `p8/c07g` |
| at most one `par` declaration per (i, j, cls, kind) | 1416 | `p8/c02a` |
| the shape of every `ind` declaration and (R1) to (R3) | 1429-1461 | `R07`, `R08`, `R09`, `R12` |
| the shape of every `centre` | 1335-1345 | `R11` |
| the FORMAT of every proposed store | `store` 1347-1383 | `p6/b3` (rotation not unit), `p8/c02b`, `c04` |

### J2.3 List (E), EVALUATED ROUNDS ONLY, clause by clause

Everything below is inside the loop over the rounds of `checkNode` (3130-3157), which leaves the loop after the
first round with an accepted `0` step or with an EMPTY new store (3155-3156). Nothing of it is called anywhere
else, so none of these tests can reject in a round that is not evaluated.

| clause of (E) | where | my files (un: accepted; ev: rejected) |
|---|---|---|
| the EMPTY test | `emptyReason` 2086-2117, on the initial store (3124) and on the store after every evaluated round (3152) | 2.6 corpus |
| precondition of every declaration, used or not: `opt` | `declare` 2193-2203 | `excl2/Y1`-`Y5` |
| ... `par`, including 0 <= kappa | `_declarePar` 2239-2301 (2275) | `p6/a8` un, ev |
| ... `ind` | 2212-2221 | `R10` un; `P05` ev (unused) |
| (T4): a `cut` name has its cut in the start store | 2459-2463 | `p6/a4`; `p8/c03b` |
| an `opt` name: `opt` declaration of its option in the round, or its option in the list of an `ind` declaration of the round | 2414-2418 | `p6/a2`; `p8/c03a`, `c03h` |
| a `par` name: its `par` declaration in the round | 2422-2423 | `p6/a3`; `p8/c03c` |
| an `asg` name: its sign assumption | 2451 | `p6/a1` un, ev |
| a `wsup` name: the sign conditions of 4.8 | 2436-2441 | `p6/a9` un, ev |
| a `rarc` name: an effective relative arc | 2401-2402 | `p6/a6` un, ev |
| `ind:i:j:k`: declaration of the pair in the round and k <= m | 2326-2328 | `R04a`, `R04b` un; `R27`, `R32` ev |
| (T3) | 2972, 2626-2640 | `R03` un; `R14` ev |
| acceptance of every step, also value > 0 of a `0` step | `checkStep` 2990-3003 (2996) | `p6/b4`, `b5` un, ev |
| acceptance of every entry of the proposed store, also cos > 0 of a proposed endpoint | `acceptStore` 3011-3071 (3035-3036, 3048, 3053) | `p6/b1`, `b2` un, ev |
| an evaluated round is evaluated COMPLETELY (steps after an accepted `0` step, its store) | the loop over the steps has no exit (3138-3147); `acceptStore` 3149 and the EMPTY test 3152 come before the two `break` | `R15`, `R16` |
| the final store is the store after the last evaluated round; the closure reads it | 3149-3156, 3160-3212 | 2.6 corpus |

Order of events in an evaluated round (final text, end of section 5): (1) the start store is not EMPTY (3124 for
the first round; for a later round the loop was left at 3155 otherwise); (2) every declaration (3135); (3) every
step (3138-3147); (4) every entry of the proposed store (3149); (5) the EMPTY test on the new store (3152). It is
the order of the text.

Two remarks. (a) (T3) is tested after (T4) within one term, and term by term; so of several defects the first in
this order is reported; the verdict does not depend on it. (b) In `lowerBound3` a term with the multiplier 0 is
left out of Rem (2684, 2705), which is right ("contributes nothing"); its names have been through `fact` and
`_guardRule` before, at 2969-2972, so (T3) and (T4) are still tested for it (`R21`, `p8/c03a`-`c03g2`).

## J3. Exactness; caches; state of the module

Status: DONE (reading); the runs that test it are in J5.

**Result: every number that enters an acceptance decision is a BigInt or a fraction of BigInts (class `Q`,
261-328: always reduced, denominator > 0). I found no place where a JavaScript Number takes part in arithmetic on
a value of the certificate, and none where a Number can reach 2^53.** The language helps: an expression that
mixes a BigInt and a Number (`1n + 1`) throws a TypeError, which the driver reports as FAIL; only comparisons mix
silently, and I searched for those (below).

### J3.1 Every place where a Number occurs

| where | what is a Number there | why it cannot lose precision or overflow |
|---|---|---|
| JSON reader `parseJsonStrict` (106-236) | positions in the line, character codes; `parseInt(hex, 16)` (146) on exactly four hexadecimal digits | values below 65,536. A JSON number token is NOT converted: it is kept as its text (`JNum`, 97-99) |
| number strings (`parseNumString` 343-350) | none: the pattern `^-?[0-9]+(?:\/[0-9]+)?$`, then `BigInt(text)`; denominator 0 rejects | - |
| JSON integers of the format | `label` (1000-1005): the token must match `^[1-9][0-9]*$` and have at most TWO characters before `Number(v.raw)`; `pmInt` (1007-1010) and `k12` (1012-1015) compare the token text with '1', '-1', '2'; `labels` (1134-1137) with '16', '17' | at most 99; the text comparison makes 1.0, 1e0, 01, -0 and a 20-digit token impossible |
| labels inside names and keys (`nameLabel` 731-735) | at most two characters, same pattern, then `Number` | at most 99 |
| the index of `ind:i:j:k` (933-934) | one character 1 to 8, then `Number` | at most 8 |
| variable numbers | 0 to NVAR - 1 = 68 for base variables (435); NVAR + nz - 1 for the indicator variables of a round (2224-2225), nz <= 7 per declared pair | at most 68 + 7 * 136. A monomial is the sorted string of the characters with the codes 48 + number (477-489); the codes stay below 1,100, far from the surrogate range, so a character is one code unit and `charCodeAt(i) - 48` (2765, 2791, 2871, 2926, 2942) gives the number back |
| `v >> 1`, `v & 1` (495, 1940, 1994) | a variable number below 2 * NL | - |
| `i * 32 + j` (1954), `v * 64 + e` (2776) | keys of two small caches: labels at most 17; e < 64 is tested one line before (2775) | below 2^17 |
| exponents in the centred rule | `e` = the length of a run of equal characters in a monomial (2806-2810); `binomBig(e, k)` (659-663) multiplies and divides BigInts; `cn[v] ** BigInt(e - k)`, `cd[v] ** BigInt(k)` (2780) are BigInt powers | a term has at most three names, a name a polynomial of degree at most 4 (`sq` of a form of degree 2), so no exponent exceeds 12; an exponent of 64 or more is an internal error (2775), i.e. FAIL |
| `Int32Array` `cls`, `T`, `t` (2741, 2760) | the class number of a variable (fewer than NVAR classes) and sums of exponents | at most 12 |
| lengths that decide something | 1 to 3 names (1489), exactly two elements of a term (1483), 1 to 8 options (1433), 0 to 2 variables of an entry (1315), nonempty lists (1255, 1307, 1548), number of children (1567), `pf.k > dcl.m` (2328) | small counts |
| counters | line numbers, statistics, tree depth, numbers of occurrences in `children` lists (compared with 0 and 1) | below the number of lines |
| signs | `Q.sign()` (272) returns -1, 0, 1 from a BigInt comparison; `Em.g.sign() * Ep.g.sign() >= 0` (2154) | exact |
| small constants | `Q.int(k)` (271) is called with 2, 3, 4, 6 and with +-1 from `eps` (695, 696, 1143, 1147, 1730, 1786, 1844, 2060-2069, 3091) | `BigInt` of a small integer |
| floating point | `ratioToNumber` (330-339), `Q.toNumber` (323), `SPoly.evalFloat` (591-606), `out.seconds` (3623) | used only inside the TEXT of messages (2287, 2295, 2296, 2994, 3001, 3002, 3107, 3261, 3262, 3357, 3358), in tests and for the time; `toNumber()` occurs nowhere outside a template string, and no branch reads one |

Comparisons that could mix the two types: I searched for a field `.n`, `.d`, `den`, `num` compared with a
literal that is not a BigInt literal: none. The decisions themselves: `lhs <= rhs` in `checkStep` (2997, 3000)
compares two BigInts (value * den(L) against num(L) * den(value), both denominators positive); every other
decision goes through `Q.cmp` (309-313) or `Q.sign`.

### J3.2 "One integer coefficient map over one common denominator" (`lowerBound3`, 2655-2722)

Every polynomial of a name is an integer polynomial over a positive denominator. B := lcm of the denominators of
ALL multipliers (2657-2661); D := lcm of the denominator of g and of the product denominators of all terms with a
non-zero multiplier (2689-2690; the denominator of a product is the product of the denominators of its factors,
2664-2681). A term enters with the integer factor `-(lam.n * (B / lam.d)) * (D / td.den)` (2707-2709), g with
`+-B * (D / gh.den)` (2701): both divisions are exact because B and D are common multiples by construction. So R_m
= B * D * r_m is an integer for every monomial, also with indicator variables (their polynomials have the
denominator 1, 2333-2340) and with squares of polynomial forms (denominator den^2, 2346-2347 and 2354-2355).

Centre (`_shift3`, 2738-2834). For a moved variable v with c_v = n_v/d_v: a run v^e becomes sum_k C(e,k)
n_v^(e-k) d_v^k y_v^k (2780) over d_v^e. The denominators of the centre are grouped by VALUE; T_delta is the
largest total exponent of the variables with the denominator delta in one monomial (2761-2767), Dc := prod
delta^T_delta (2769-2771), and a monomial is multiplied by prod delta^(T_delta - t_delta(m)) (2793-2799), which
is the integer Dc / prod_v d_v^(e_v). So Y_m / (B * D * Dc) is exactly the coefficient of the substituted
polynomial, whatever the denominators of the centre are and whether or not they share factors with those of the
store; a centre of 0, a variable without a value and every indicator variable are not moved (2747, 2811-2813);
if nothing is moved the map is returned unchanged (2758).

Bound (`_bound3`, 2848-2902). The interval of a variable is written [a/q, b/q] with integers (2853-2863; for a
base variable SB(v) or SB(v) - c_v with rational subtraction first, for an indicator variable [0, 1]); the
interval of a monomial is built one variable at a time from the interval of the monomial without its last
variable (2867-2884), min and max of the four integer products, denominator the product of the q; the sum is
taken per denominator and brought to the lcm at the end (2886-2900). The comparison `va > vb` (2864) guards
against an improper interval.

I checked each of these formulas by hand and found no error; what a reading cannot give, the runs give: J5
(stress set: 40 random steps with exponent 12, 65 centre values with different large denominators, up to 31
indicator variables; three programs, L equal as rationals).

### J3.3 Caches and their keys

| where | lifetime | key | complete? |
|---|---|---|---|
| `Validator.custom`, `formCache`, `factCache`, `qforms`, `assumeOptPairs` (967-973) | one node: made new in `node()` (1588-1596) BEFORE the node's `forms` and rounds are read | name string | yes. A parsed name carries the node's own definition (`pf.def` 1202, `pf.qdef` 1223). Test: `Q15` (the same `q:f` in two nodes with different definitions, exact L), `Q03` |
| `pf.rc`, `pf.entry` on a parsed fact name (1237-1238, 2306-2311) | one round: the entry is used only if `pf.rc === this` (the `RoundCtx` of the round) | the object identity of the round | yes; a new `RoundCtx` is made for every round (3134). Not used for sq, pol, ind |
| `RoundCtx.indDecl[pair].entries[k]` (2224, 2329-2342) | one round | pair, k | yes: the polynomial of `ind:i:j:k` depends on m and on the variable numbers of THIS round. Test: `X13a`, `X13b` |
| `RoundCtx.denIds`, `denVals`, `monB`, `optOK`, `parOK`, `psOK`, `indListed`, `nz` (2172-2185) | one round | - | yes |
| `NodeCtx.fp`, `sfp` (1635-1636; named forms and store-independent facts) | one node (3121) | form name; fact name, with kappa, cp/cm or k appended where the polynomial depends on it (1795, 1842, 1855) | yes. The corner polynomial of an option is the same whether the option is opt-declared or ind-listed |
| `qDen` on a form definition (1871-1878) | one node | - | yes |
| `StoreView._sb`, `_eff`, `_ex`, `_hlo`, `_base` (1928-1932) | one store (a new view for the store after every round, 3150) | form name; pair; option; variable | yes; a store object is never changed after it is built |
| `cache`, `va`, `vb`, `vq` in `_bound3`; `wCache`, `cofCache` in `_shift3` | one call, i.e. one step | monomial; variable; (variable, exponent) | yes: they depend on the centre of the step |
| `hotOf(sp)._hot` (615-622) | with its polynomial | - | the arrays are never written after they are made |

### J3.4 State of the module; two certificates in one process

Module-level variables: the label set (`LABELS`, `NL`, `LIDX`, `LABEL_KEYS`, `LABEL_KEY_SET`, `LABEL_TEXT`, `NVAR`,
`V_S`, `V_C0`, `V_SN0`; 442-443) and `SCHEMA3` (469). Nothing else: no cache lives at module level (the only
other top-level containers are constants: `LABEL_SETS`, `ARC_SUBS`).

Both selections are made in `Validator.header` (1118, 1139) and made again at the start of
`CertChecker.checkNodeText` (3390, 3393), from the header that this `CertChecker` accepted. Everything that
depends on them for a node (`Validator.node`, `checkNode`, `checkRoot`, `checkChild` through `feedNode` 3399-3445)
runs synchronously after that; `finish()` (3456-3502) uses neither. The driver gives control away only between
lines (`for await`, 3570). So if two certificates are checked in one process, in any interleaving of their
lines, every node is read and checked under the label set and the schema of its own header, and all caches hang
on objects of one `CertChecker`. `checkRoot` tests in addition that the schema in force is the schema of the
header it was given (3347). What the code allows and what it does not: calling `checkNode`, `terminalTest` or a
`Validator` method directly, without `checkNodeText`, uses whatever selection was made last; the command line
never does that (one file per process). Tested: J5, interleaving.

## J4. Options, modes, environment, exit codes, words printed

Status: DONE. (Line numbers of the draft; the two lines that the last pass changed are named.)

| option | effect | can it give PASS / exit 0 where the text rejects, or without the whole certificate having been checked? |
|---|---|---|
| `--packing FILE`, `--expect-packing-sha256 H`, `--no-packing-pin` | another reference file; the pin (3565-3568) | they change the REFERENCE FILE, not what is checked: the header's `packing_sha256` must equal the hash of the file read (1121), the report carries that hash, and the acceptance script must compare it with 24e296f5... (as for 2.6 and as for the Python checker) |
| `--node ID` | one node alone | no: the result is NODE-OK, exit code 3, never PASS (3731-3732, 3758) |
| `--json OUT` | report; written BEFORE the verdict is printed; if it cannot be written the verdict becomes FAIL (3722-3727) | no |
| `--dump-stores` | more text in the report | no |
| `--paranoid` | second, literal evaluation of every L; a difference is an internal error = FAIL (2985-2988) | no |
| `--keep-going` | continues after a failure; the first reason stays, `pass` stays false (3551-3559) | no |
| `--quiet` | prints only the verdict line | no |
| `--help`, `-h` | prints the usage text | **in the draft: YES for the exit code.** `process.exit(0)` (3676) without anything having been read; the usage text contains "0 = PASS" in its second line, its first line is "usage: ...". The frozen 2.6 file has the same line. Reported to the lead; **fixed in the last pass** (J8): `process.exit(2)` |
| any other word that begins with `--` | usage error, exit 2 (3677) | no. In the draft a word that begins with ONE dash (`-x`) is taken as the certificate's file name; the last pass makes every word that begins with `-` a usage error |
| removed: `--ignore-unknown-keys` | now an unknown option, exit 2 | - |

**Environment.** The program reads no environment variable (no `process.env`) and loads four built-in modules
(`fs`, `path`, `crypto`, `zlib`; 79-82), which a file in the folder or `NODE_PATH` cannot replace (built-in
modules win). What CAN change its behaviour from outside is Node itself: `NODE_OPTIONS` (for example `--require
FILE` runs any code first). Advice for the acceptance script, not for the checker: start it with `NODE_OPTIONS`
unset, as the Python checkers are started with `-I`. My runs do so.

**Exit codes and words.** `PASS` is printed in one place (3732), only if `res.pass` and not `--node`; exit code 0
is set in one place (3758: `res.pass ? (nodeOnly ? 3 : 0) : 1`) and, in the draft, by the help option. `res.pass`
is `out.reason === null` at the end of `checkLines` (3618), which needs: the packing pin (3565-3568); a first
line that `Validator.header` accepts; every further line accepted by `feedNode`, no empty line (3577); at least
one line; `finish()` without rejection (3611-3613: the root exists, every child exists with the right parent,
every node but the root in exactly one `children` list, everything reachable). An error of the stream (a file
that cannot be read, invalid UTF-8, a damaged or truncated gzip stream) is thrown inside the `for await` and
caught at 3615: FAIL. An exception that escapes `main` prints FAIL and sets exit code 1 (3779-3783). `process.exit`
is called with 2 in four places (3664, 3677, 3679, 3681) and with 0 in one (3676, the help option).
**So, apart from the help option of the draft, no path prints PASS or ends with 0 unless every line of the
certificate was read and accepted and the tree conditions hold.**

Three observations that are not defects of the checking:

1. gzip is recognised by the file NAME (`file.endsWith('.gz')`, 3509); the Python checker looks at the first two
   bytes. So a gzip file without the ending `.gz` and a plain file with it are rejected here and accepted by the
   Python checker (J5, `g02`, `g03`). The text says only that a checker "may read the same lines from a
   gzip-compressed file". The acceptance script should name compressed certificates `*.gz`.
2. For a `.gz` certificate the report key `certificate_sha256` is the SHA-256 of the DECOMPRESSED bytes (the hash
   is fed from the stream after gunzip, 3523), while the Python report gives the hash of the file on disk under
   that key and the hash of the lines under `certificate_uncompressed_sha256`. For the real certificate: here
   f678f75a..., there 989e9738... . A script that compares the two reports must compare this key with the
   Python key `certificate_uncompressed_sha256`.
3. Under "wx-cert-2" the report has the new keys too (J1).

## J5. Runs

Status: DONE. Node v25.6.1,
`NODE_OPTIONS` unset; Python programs started with `-I -B`. Scripts and results are in `r30js/` (`j_run.py`,
`j_stress.py`, `j_misc.py`, `j_interleave.js`, `j_big.py`; `job_*.sh`). **Every suite was run twice: on the draft
8aa489f4... (results in `r30js/out/`) and, after the freeze, on the FROZEN file 97210adf... (results in
`r30js/out_frozen/`).** Where two programs are compared the Python side is `proto30/wxproto30b.py` (55a74437...)
in the first round and the file to be frozen, `proto30/wxcheck_v30_candidate.py` (cf8db52b...), in the second.
(In the result files the program under test is called "draft" in both rounds; the first line of every output
gives its SHA-256.)

| run | files | draft 8aa489f4 | frozen 97210adf |
|---|---|---|---|
| wx-cert-2 corpora `checker2/v26/inputs` (228) and `checker/v26/testcerts` (358), the frozen 2.6 Node file against the 3.0 file: exit code, first output line and the whole report apart from `spec`, `seconds`, `certificate` and the new keys (`j_run.py regress`) | 586 | identical in **585**; the one difference is `fail/F36.jsonl` (2.6: FAIL at the header; 3.0: PASS), as expected. 2.6: 87 PASS, 499 FAIL | the same: **585**, F36 |
| the same files with only the schema string changed to "wx-cert-3", against the 2.6 file's report on the original (`j_run.py swap`; every L is then computed by `lowerBound3`) | 574 (12 cannot be swapped: gzip, or the string is not in the header) | identical in **574**, including reasons, counts of monomials and the digests of all final stores | the same: **574** |
| my 477 files of the Python review, with reasons (`j_run.py mine`) | 477 | 475 as I derive them from the text; the two others are the empty-id files (accepted) | **477** (141 PASS, 336 FAIL); the empty id is rejected |
| `--paranoid` against default on the wx-cert-3 files of mine and the author's 72 of `proto30/testcerts30` (`j_run.py paranoid`) | 386 | same verdict and report in 386 | same verdict and report in 386 (107 PASS, 279 FAIL) |
| exactness under stress (`j_stress.py`), see below | 40 cases, 80 files | all as expected; L equal in three programs in 40 | the same: 40 of 40 |
| the file, the JSON reader, names, two `0` steps (`j_misc.py`), see below | 82 | (not run: the set was finished after the freeze) | all 82 verdicts as expected |
| command line (`j_misc.py options`) | 29 / 35 cases | exit 0 for the help option (J4) | 35 as expected; exit code 0 in six, each a full-run PASS |
| several certificates in one process (`j_interleave.js`), see below | 11 certificates, 190 arrangements | - | no certificate ended otherwise than alone |
| the real certificate `proto30/out/tree3/c01/G20S_v3_c01.jsonl.gz`, ONCE, `--json` | 1 | - (the lead's and the author's runs) | **PASS**, exit 0, 132.6 s, 1.24 GB |

**The real certificate with the frozen file** (`job_big_node.sh`, `j_big.py`; report kept as
`r30js/out_frozen/G20S_v3_c01.<reviewer>.node.report.json`): PASS; 153 nodes (81 infeasible, 1 terminal, 71 split),
2,673 declarations, 81 steps, 1,614,692 terms, 1,414,746 monomials, tree depth 71; `spec_sha256` 0a6dfc2a...aba0;
`certificate_sha256` f678f75a...da58 = the Python report's `certificate_uncompressed_sha256`. Against my Python
report of the same file (P9): the same 153 ids with the same closure, rounds, evaluated rounds and line;
`zero_step_L` in the same 81 entries, **equal as rationals and as strings in all 81**. Against the report the
lead named (`checker2/v30/out/c2_big_first.json`, made with the draft): the whole report is equal apart from
`seconds`, `certificate`, `spec`, `spec_sha256`.

**Exactness under stress** (`certs/stress/`, built by `j_stress.py` with my own evaluator of the Python review,
`r30py/r30_eval.py`, which was written from the text). 40 random nodes closed by one step on the form `0`: 9 to
31 terms of twelve shapes (`sq` alone, with a fact, with another `sq`; `sq:S2` three times with S2 = S * S, i.e.
S^12, in 30 of the 40; `circ` with one or two `pol` names and either sign; indicator products up to the third
power; guarded corners, also inside a `circ` term; repeated names; multipliers 0), 2 to 5 `ind` declarations (the
pair 1-3 with a list of 2 or of 3 in changing order, other pairs with all 8 options; 8 to 30 indicator
variables), and a centre: none (6 cases), empty (11), 1 to 40 values (17), a value for every one of the 65 base
variables (6), with denominators that are primes, squares of primes, powers of ten and numbers of up to 40
digits, some values far outside the store interval, some for variables that do not occur. For each case my
evaluator computes L (denominators of 125 to 1,528 digits) and two files are written: the claim exactly L and
the claim L + 10^-40. Result on the frozen file: **40 of 40 accepted at L, 40 of 40 rejected at L + 10^-40, by
the Node checker and by the Python checker; and the three numbers L (mine, the Node report's `zero_step_L`, the
Python report's `zero_step_L`) are the same string in all 40.** The same held for the draft against
`wxproto30b.py --proto-report`.

**The file and the JSON reader** (`certs/misc/`; both programs on every file).

| group | cases | result (Node frozen; Python cf8db52b) |
|---|---|---|
| gzip: a truncated file (by 20 bytes; by 1 byte), a wrong CRC, a wrong length field, a zlib stream, zero bytes of content | 6 | rejected by both |
| gzip: a valid certificate followed by a line that must reject, the FILE CUT exactly where the valid lines end (a full flush stands there, so everything that can be decompressed is a valid certificate) | 1 (`g09`) | **rejected by both** ("unexpected end of file"); control `g08` (the complete file): rejected at the bad line |
| gzip: header with the optional fields FEXTRA, FNAME, FCOMMENT; a second, empty member | 2 | accepted by both |
| gzip by name or by content: plain text named `.gz`; gzip content not named `.gz` | 2 (`g02`, `g03`) | **the two programs differ**: Node rejects both (it decides by the name), Python accepts both (it decides by the first two bytes). J4, observation 1 |
| byte order mark before a node; a raw control character or tab in a string; bad escapes; single quotes; a comment; NaN, -Infinity; trailing commas; 01, 1., .5, +1, 0x10, 1_0; tru, True, nul | 21 | rejected by both |
| UTF-8: an encoded surrogate, an overlong encoding | 2 | rejected by both |
| `eps` written as 1E0, 1e+0, 10e-1, -0, 1.0, 1e0, 01, 9007199254740993, 1e999999999, true, "1", [1], null | 13 | rejected by both; `1` followed by a blank: accepted by both |
| form feed, vertical tab, no-break space, U+2028, NUL between two tokens | 5 | rejected by both |
| 200,000 nested arrays | 1 (`j11`) | rejected by both: FAIL, exit code 1 (here: the stack overflow of the recursive reader is caught and reported as an internal error = FAIL) |
| three million blanks after a node; an escaped NUL in an id | 2 | accepted by both |
| a label key twice, once written with an escape; a node twice; a node inside an array; a node cut short; the header twice; carriage returns alone as line ends; a node id with the raw byte 7F while the header names the id without it | 7 | rejected by both |
| names that are properties of every JavaScript object: `__proto__`, `constructor`, `toString`, `hasOwnProperty`, `valueOf`, `prototype`, `length`, each as the node id, as a custom form and as a polynomial form at once; a step with `sq` and `pol` of that form claiming exactly my L, and L + 10^-30 | 14 | accepted at L, rejected at L + 10^-30, by both (all tables keyed by names from the certificate are `Map`s) |
| two accepted `0` steps with different L in one round, a third in a round that is not evaluated, in both orders | 2 | accepted by both; `zero_step_L` is the L of the FIRST step in both reports |

**Several certificates in one process** (`j_interleave.js` loads the frozen file as a module). Eleven
certificates (wx-cert-2 and wx-cert-3; sixteen and seventeen labels; with header centres; one, three, four, five
and eleven nodes; eight that pass and three that fail), each with its own `CertChecker`, their lines fed in 60
shuffled round-robin orders, in all 110 nestings "header of A, all of B, rest of A", and in 20 orders "all
headers first": 190 arrangements, and in every one every certificate ended exactly as it ends alone (verdict,
reason, node entries with digests and `zero_step_L`). Test of the test: in a copy of the file from which I
removed the two lines of `checkNodeText` that select the label set and the schema again, the same 190
arrangements give 609 wrong endings, none of them an acceptance of a certificate that fails alone (the gates of
`checkRoot` and `terminalTest` and the label tests turn them into FAIL). So the re-selection is what protects,
and it is there.

Known from the lead, not from me: the lead's cross-run of 1,841 test certificates through both drafts (the same verdict
in all but the four empty-id files, the same L on 278 closing steps), and a cross-run of all corpora through the
two frozen files, which was running when this was written.

## J6. After reading the author's notes

Status: DONE. Read after J1 to J4 were written and the scripts of J5 existed: `checker2/CHECKER2_NOTES.md`,
section "10. Version 3.0" (lines 1488 to 2030: 10.1 to 10.11; the two long tables 10.12 and 10.13, which list
every input of the author's tests, I did not read line by line). SHA-256 of the file when read: b49dda06...f4f5.

**The author's readings against the final text.** Section 10.6 of the notes lists ten questions that the lead decided
(Q1 to Q10), eleven readings of the four additions (N1 to N11) and thirteen earlier readings that were stricter
than the words of the audited candidate. I compared each with the final text and with the code:

| the author's reading | final text | my finding |
|---|---|---|
| Q1 to Q10 (tan length, the lists of the last item, multiplier 0, cut under `0`, empty custom form, header ranges, `kappa` on P+/P-, JSON integers, repeated options, the hash as a string) | each is now stated (4.2; 10 WHERE EACH TEST IS MADE; 5 TERM RULES; 10 `store`; 3; 10 Header ranges; 10 `pairs`; 10 labels; 6; 10 first item) | the code does what the final text says in all ten (J2; my `p8` files) |
| N1: (R1), (R2) are per round | 4.10 "a round" | the same (`R29`) |
| N2: (R3) reads the node's own `assume` list | 4.10 (R3), 10 | the same (`R09`, `R30`) |
| N3: one `ind:i:j:k` guards every corner name of O_k in the term, in any order | (T3) "the term also contains the name" | the same (`R23`) |
| N4: the multiplier "-0" is 0 and not negative | 10 Numbers, (T1) | the same (`p6/h1`) |
| N5: a name may repeat, also `sq` three times and `ind` | 5 "The same name may occur more than once" | the same (my stress set uses sq:S2 three times) |
| N6: NAME must match as a whole string | 3, 10 | the same; JavaScript's `$` without the flag `m` matches only at the end of the string |
| N8: a `centre` key for a variable that does not occur must still be a base variable name | 10 "Every other key of that object is rejected" | the same (`C01`-`C08`) |
| N9: all eight options may be listed | 4.10 | the same (stress set) |
| N10: the id " " (one blank) is not empty | 7 "a non-empty JSON string" | the same as the Python checker (it rejects only the empty string) |
| N11: a line of blanks only is rejected | 10 "an empty line is rejected" | the same in both checkers (`p6/f11`); such a line holds no JSON object in any case |
| the thirteen stricter readings (A1, A2, A6, A7, A9, A10, A11, A12, A13 and four without a number) | all stated now, except two that the text leaves as they were: the packing file's `side` must be the Sref of section 0; the pin of the packing file (section 11 (5) allows it) | no difference to the final text |

**I found no reading of the author's that differs from the final text.** The author's two tables for (W) and (E) agree with mine
(J2.2, J2.3) clause for clause; the lines are the same functions.

**The author's tests and mine.** The author's are far more numerous than mine (509 inputs with expected messages, 47 faulty copies
of the checker run against them, a literal model, 2,632 random steps, 66 command lines, three real 2.6 trees).
They and mine were made apart; where they overlap they agree. What the author's section 10.9 names as NOT tested and my
runs add (J5):

| not tested by the author (10.9) | here |
|---|---|
| polynomial forms or centres whose denominators have nothing in common | the stress set: 40 steps, centres with up to 65 values over primes, squares of primes, powers of ten and numbers of 40 digits; L equal in three programs |
| JSON nested so deeply that the reader runs out of stack | `j11`: 200,000 nested arrays: FAIL, exit code 1, first line FAIL (both checkers) |
| a second accepted `0` step in a node (`zero_step_L` takes the first): reading only | `z0`, `z1`: two accepted `0` steps with different L in one round and a third in a round that is not evaluated: both checkers report the L of the first |
| - | damaged gzip files (`g04`-`g09`), among them a file cut exactly where a valid certificate ends |

## J8. The last pass: the frozen file against the draft

Status: DONE.

| file | SHA-256 |
|---|---|
| `checker2/wxcheck2_v30.js`, FROZEN (3,818 lines, read-only) | 97210adf74a3ebed7cde021a3cb1ff6ea6380d8d2d55540a2a2a1cb17dc27542 |
| the draft of J1 to J6 (my copy and the author's `checker2/v30/work/wxcheck2_v30_draft_8aa489f4.js`) | 8aa489f4cf88a9af33737d2d89627a16f1d496decc229f244eb0dae5759e0927 |

My own diff of the two (`r30js/DRAFT_to_FROZEN_97210adf.diff`) is byte for byte the author's
`checker2/v30/diff_draft8aa489f4_final.txt`: 12 hunks.

| # | lines (draft -> frozen) | what | kind |
|---|---|---|---|
| 1 | 7 -> 7-10 | header comment: the SHA-256 of the final text; one sentence on the last pass | comment |
| 2 | 918-919 -> 921-923 | comment at the names `sq`, `pol`, `ind`: the wording of the final text | comment |
| 3 | 1502-1503 -> 1506-1508 | comment at (T2): list (W) | comment |
| 4 | after 1579 -> 1585-1593 | `Validator.node`: `if (id.length === 0) reject(...)`, directly after the id has been required to be a string, under both schemas | **the one change of a checking rule** (final text, section 7) |
| 5 | 2318 -> 2332 | comment: "1 <= k <= m" | comment |
| 6 | 2623-2624 -> 2637-2639 | comment at the guard rule: list (E) | comment |
| 7 | after 3637 -> 3653-3655 | constants `SPEC_NAME` = 'SPEC_v3.0.md version 3.0', `SPEC_SHA256` = 0a6dfc2a...aba0 | report only |
| 8, 9 | 3645, after 3655 -> 3663-3665, 3676-3678 | usage text: exit codes; the help option; "An argument that begins with "-" ... is a usage error" | text |
| 10 | 3676-3677 -> 3699-3710 | `--help` / `-h`: `process.exit(2)` (was 0); an argument that begins with `-` and is not an option: usage error, exit 2 (was: only `--`) | driver: exit codes |
| 11 | 3714 -> 3747 | report: `spec: SPEC_NAME, spec_sha256: SPEC_SHA256` | report only |
| 12 | after 3775 -> 3809 | exports of the two constants | tests only |

So against the draft the frozen file differs in one rule and two exits:

- **The empty id.** A node whose `id` is the empty string is rejected when the node is read (frozen line 1592),
  under both schemas. This is the one intended change under "wx-cert-2" against the frozen 2.6 Node file. An
  empty `root`, `parent` or `children` entry is a reference to an id that no node can have, and is rejected by
  the tree conditions as before (`finish`). The id " " is accepted (as by the Python checker).
- **Exit code 0 now has one source** (frozen line 3791, `res.pass` and not `--node`): the help option ends with
  2 (3708), every argument that begins with `-` and is not an option ends with 2 (3709), as do the other usage
  errors (3687, 3712, 3714); FAIL is 1 (3791, 3816), NODE-OK is 3.

Everything else of the file is the draft byte for byte, so J1 to J6 hold for the frozen file with the line
numbers shifted (by 3 after line 7, by 4 after 919, by 5 after 1503, by 14 after 1579, by 15 after 2624, by 18
after 3637, by 20 after 3645, by 23 after 3655, by 33 after 3677, by 34 after 3775).

## J7. Verdict

On the frozen file `checker2/wxcheck2_v30.js`, SHA-256
97210adf74a3ebed7cde021a3cb1ff6ea6380d8d2d55540a2a2a1cb17dc27542:

**SOUND AS FAR AS REVIEWED: KEEP FROZEN.**

- I found no input that the final text rejects and the frozen file accepts. The one such input of the draft, the
  empty node id, and the one exit with code 0 that was not a PASS, the help option, are gone in the frozen file
  (J8); I tested both.
- Under "wx-cert-2" it is the frozen 2.6 Node file (585 of 586 corpus files with identical reports; the 586th is
  F36), apart from the intended points: the string "wx-cert-3" is accepted, the empty id is rejected, the option
  `--ignore-unknown-keys` is gone, the help option ends with 2, and the report has more keys.
- The new arithmetic is exact as far as reading can tell (J3), and three programs written apart give the same L
  on every step I could compare: 40 stress cases, 81 leaves of the real certificate (two programs; ten of them
  three), the 18 exact pairs of the Python review.
- Every test of the final text's lists (W) and (E) is made where the text says and nowhere else (J2).

MUST: none.

SHOULD (nothing here asks for a change of the frozen file):

1. Acceptance script: start `node` with `NODE_OPTIONS` unset; give compressed certificates a name that ends in
   `.gz` (this checker decides by the name, the Python checker by the first two bytes: `g02`, `g03`); compare
   this checker's `certificate_sha256` with the Python report's `certificate_uncompressed_sha256` for a `.gz`
   input; require exit code 0 AND the first output line `PASS` AND the report's `result`, `spec_sha256`,
   `packing_sha256` and `schema`.
2. For the text, at the next occasion: say how a gzip-compressed certificate is recognised, and that a damaged
   or truncated gzip file is rejected (both checkers do; the text says only that a checker "may read" one).
3. For a next version of this file, not for this one: (a) a damaged input (invalid UTF-8, a damaged gzip
   stream, JSON nested too deeply) is reported with the words "internal error (treated as FAIL)"; the verdict is
   right, the words blame the program; (b) `checkNode`, `terminalTest` and the `Validator` methods, when called
   directly from other code, use the label set and schema selected last (J3.4); the command line and
   `CertChecker` are not affected.
4. For the record of the 3.0 acceptance: the report of this file has the keys `schema`, `window_centres`,
   `tube_centres`, `spec_sha256` and `zero_step_L` under "wx-cert-2" too.

What I did not examine:

- The parts of the file that are the frozen 2.6 Node file byte for byte (the facts of 4.0 to 4.8, store bounds,
  the exclusion test, the store update, the tree pass, the reference data): read again here for context,
  reviewed in `REVIEW_26.md`, not re-derived.
- The author's test programs and the author's tables 10.12, 10.13 (every input of the author's 509 and of the lead's 72); I read
  what the author says about them (10.7 to 10.9) and ran none of the author's programs.
- `--paranoid` on the real certificate (the author ran one leaf); the three real 2.6 trees with the frozen file
  (the author's 10.14).
- The Python side of 3.0 beyond `REVIEW_30_PY.md`; the acceptance script; the cross-run of the two frozen files
  (the lead's).
- Node versions other than v25.6.1; certificates much larger than the real one (memory: the real one needs 1.24
  GB here).
- A real "wx-cert-3" certificate with header centres, with seventeen labels or with more than one round per
  node: none exists; these paths are covered by small files only (mine and the author's).
