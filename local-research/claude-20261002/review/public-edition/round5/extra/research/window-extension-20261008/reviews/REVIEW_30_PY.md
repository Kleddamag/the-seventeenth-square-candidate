# REVIEW 30 (Python): the candidate checker `proto30/wxproto30b.py` for specification version 3.0

Reviewer: an independent reviewer session (the reviewer of the frozen 2.6 checkers, `reviews/REVIEW_26.md`). Started 9 October 2026.
I wrote none of the reviewed files. I had seen neither the code nor its author's notes
before; the notes (`proto30/PROTO_NOTES.md`) were read only for part P6, after P1 to P5.
What I wrote: this file and the folder `reviews/r30py/` (scripts, my own test certificates, outputs, logs).

Reviewed state (SHA-256, verified at the start):

| file | SHA-256 |
|---|---|
| `proto30/wxproto30b.py` (the candidate; 3,294 lines) | 55a74437dfac4648155499be4333935fce8f8ce972c6a717cd180909eee8eed7 |
| `checker/wxcheck_v26.py` (frozen 2.6 checker; 2,637 lines) | 725508302b6711247867cb8feb155f0acdd9c3b4aefc0d23059f1c78b03faaef |
| `SPEC_v3.0.md` (candidate text; 862 lines) | 2cec6f7275580cb7ec71bdfc48d8cc57f988b69f5acedf25f558d5085d0ca908 |
| `SPEC.md` (version 2.6) | fa14fe405635d28bb16a66febe1370db766df2b90317d437472af6eb389d8aa3 |

The parts below are written as they are finished. Status of each part is in its first line.

## P1. The diff against the frozen 2.6 checker, hunk by hunk

Status: DONE (reading); the regression runs that confirm it are in P5.

`diff checker/wxcheck_v26.py proto30/wxproto30b.py` (kept as `r30py/CODE_v26_to_30b.diff`): 57 hunks, 680 lines added,
23 lines of the frozen file replaced, none removed without replacement. I read every hunk and then the whole candidate
file once from top to bottom. Line numbers below are those of the candidate.

"Effect under wx-cert-2" means: can the hunk change the verdict or the report for a certificate whose header has the
schema "wx-cert-2", with the default options. The gate is the module variable `SCHEMA_V3[0]`, set by `parse_header`
(lines 1249 and 1256) before anything else of the certificate is parsed.

| # | lines | what the hunk does | passage of SPEC_v3.0.md | effect under wx-cert-2, default options |
|---|---|---|---|---|
| 1 | 4-49 | docstring: what the prototype adds | none | none |
| 2 | 84 | docstring: exit code 11 | none (prototype mode) | none |
| 3 | 117-119 | `CHECKER_VERSION` string | none | the report key `checker` and the last output line differ (version string) |
| 4 | 131-150 | new module state: `OPTIONS["proto_report"]`, `SCHEMA_V3`, `PROTO_LOG`, `OPTIONS["proto_partial"]`, `OPTIONS["proto_only"]`, `PROTO_NOT_EVALUATED` | section 10, SCHEMA RULE (the gate); the rest is prototype machinery | none (all default to off) |
| 5 | 412-437 | `VAR_Z` (table of indicator variables, reset with the base variables for every certificate); `zvar_number` (number of z_{ij,k}, k = 1..7, given on first use after the base variables); `is_equality_fact` (true for `circ` only) | section 3, INDICATOR VARIABLES; (T1) | none: no indicator variable is ever created; `is_equality_fact(f)` is the old test `f[0] == "circ"` |
| 6 | 613 | `_IND_K`: the digits 1 to 8 | section 10: "the index k of a name ind:i:j:k is one digit 1 to 8" | none |
| 7 | 716-718 | `parse_fact_name` gets the parameter `qnames` (names of the node's polynomial forms) | 4.9 | none |
| 8 | 725-735 | names `sq:NAME`, `pol:NAME` (NAME must be a polynomial form of the node) and `ind:i:j:k` (i < j in I, k one digit 1..8); both branches start with `SCHEMA_V3[0] and` | 4.9, 4.10 NAME, section 10 FACT names | none: the branches are not entered; such a name falls through to "unknown fact name" as in the frozen file |
| 9 | 876-939 | new functions `parse_base_variable`, `parse_qforms`, `parse_centre` | section 3 POLYNOMIAL FORMS; section 10 `forms`, `centre` | none (not called; but see hunk 17) |
| 10 | 942 | `StepData` gets the slot `centre` | section 5 | none |
| 11 | 957 | `NodeData` gets the slot `qforms` | section 3 | none |
| 12 | 1003 | `parse_round` gets the parameter `qnames` | 4.9 | none |
| 13 | 1009 | `seen_ind` (pairs with an `ind` declaration in the round) | 4.10 (R1) | none |
| 14 | 1014-1034 | the `ind` declaration: exactly the keys i, j, mode, options; i < j in I; 1 to 8 options, each an option object of that pair, pairwise different; at most one per pair and round; starts with `SCHEMA_V3[0] and` | 4.10 DECLARATION, (R1); section 10 | none: not entered; the mode "ind" is then rejected by the unchanged `need_choice(..., ("opt", "par"))` |
| 15 | 1060-1064 | (R2): a pair with an `ind` declaration must not have an `opt` declaration in the round | 4.10 (R2) | none (`seen_ind` is empty) |
| 16 | 1068-1069 | a step may have the key `centre`: `optional=(("centre",) if SCHEMA_V3[0] else ())` | section 10, step `centre`; KEYS | none: the call is the frozen call |
| 17 | 1071 | `sd.centre = parse_centre(...) if "centre" in s else None` | section 5, CENTRED RULE | none with the default options, because hunk 16 has rejected the key. **The read itself is not gated** (see below and P4) |
| 18 | 1085-1088 | passes `qnames`; the sign test uses `is_equality_fact` | (T1) | none (same test) |
| 19 | 1090-1091 | (T2) at parse time, in every round: a `pol` name needs a `circ` name in the term | (T2); section 10 last item | none (no `pol` fact can exist) |
| 20 | 1180-1192 | `forms`: under wx-cert-3, if a key begins with `q:`, the `q:` keys go to `parse_qforms` and the others to the unchanged `parse_forms`; gated at the point of use | section 3; section 10 `forms` | none: the else branch is the frozen line; a key `q:X` is rejected by `parse_forms` ("a custom form name must match") |
| 21 | 1196-1197 | passes the names of the polynomial forms to `parse_round` | 4.9 | none (empty set) |
| 22 | 1199-1205 | (R3): a pair with an option assumption of the node has no `ind` declaration in any round | 4.10 (R3) | none (no `ind` declaration can exist) |
| 23 | 1211-1213 | `Region` gets the slots `centre`, `has_centre` | section 8 | none |
| 24 | 1217-1219 | window / tube may have the key `centre`: `optional=(("centre",) if SCHEMA_V3[0] else ())` | section 10; KEYS | none: the call is the frozen call |
| 25 | 1221-1228 | `rg.has_centre = "centre" in x`; the centre map (exactly the labels of I, every value a unit rotation) or the identity for every label | section 8; section 10 | none with the default options: the identity for every label. **The read itself is not gated** (see below and P4) |
| 26 | 1249 | `SCHEMA_V3[0] = False` at the start of every header | SCHEMA RULE | none |
| 27 | 1252-1254 | the schema may be "wx-cert-2" or "wx-cert-3"; the message for any other value is the frozen one | section 10 first item | only for a header with the schema "wx-cert-3", which the frozen checker rejects (expected: `fail/F36.jsonl`) |
| 28 | 1256 | sets the gate | SCHEMA RULE | none |
| 29 | 1660-1661 | `sb` of an indicator variable: [0, 1] | section 3 STORE BOUNDS, last item | none (never reached) |
| 30 | 1778-1779 | `RoundEnv`: `ind_declared`, `ind_index`, new and empty for every round | 4.10; section 3 ("they belong to the round") | none |
| 31 | 1865-1866 | `declare` dispatches an `ind` declaration | 4.10 | none |
| 32 | 1869-1903 | `declare_ind`: valid iff every option of the pair NOT in the list is excluded by the unchanged `excluded()` of 4.7 on the store of this `RoundEnv` (the store at the start of the round); else Reject | 4.10 PRECONDITION | none |
| 33 | 1905-1944 | `ind_poly` (z_k for k < m; 1 - z_1 - ... - z_{m-1} for k = m; 1 for m = 1), `ind_options` (pair declared, 1 <= k <= m), `check_term_rules` (GUARD RULE, no exemption for a term with `circ`) | 4.10 INDICATORS, NAME; (T3); (T4) | none (`ind_index` is empty, so `check_term_rules` does nothing) |
| 34 | 2000-2004 | a corner name is available iff its option is opt-available or listed in an `ind` declaration of this round | (T4); 4.5 | none (second set empty) |
| 35 | 2008-2011 | polynomial of `ind:i:j:k` | 4.10 NAME | none |
| 36 | 2034-2042 | polynomials of `sq:NAME` (the form times itself) and `pol:NAME` (the form) | 4.9 | none |
| 37 | 2089-2090 | `remainder` calls `check_term_rules` for every term before forming anything | (T3) | none |
| 38, 39 | 2147-2320 | the centred bound: `product_nocache`, `remainder_streaming`, `centred_remainder`, `centred_interval`, `lower_bound_centred`, `lower_bound_reference_centred` | section 5 CENTRED RULE | none (reached only for a step that has the key `centre`) |
| 40 | 2350-2355 | `_proto_clock` | none | none (a clock read per step; never used for a decision) |
| 41 | 2364-2365 | sign test of `check_step` with `is_equality_fact` | (T1) | none (same test) |
| 42 | 2369-2386 | `check_step`: (T2) again, `check_term_rules` (T3), then the raw rule for a step without the key and the centred rule for a step with it; the step log of `--proto-report` | (T2), (T3), section 5 | none: the raw path is the frozen call `env.lower_bound(g, step.terms, what)` |
| 43 | 2530-2532 | terminal test: `Ab := conj(gammaT_i) * rho_i * P` | section 8 TERMINAL TEST | none: with the identity, `rot_mul((1,0), X)` returns the two Fractions of X unchanged |
| 44 | 2715-2718 | root test: `Ab^± := conj(gamma_i) * rho_i * P_i^±` | section 8 ROOT CONTAINS WINDOW | none, for the same reason |
| 45 | 2974 | empties the step log | none | none |
| 46, 47 | 2986-3013 | report keys `proto_steps`, `proto_maxrss_bytes_or_kb` with `--proto-report` | none | none without the option |
| 48 | 3050-3053 | report keys `schema`, `window_centres`, `tube_centres`, only under wx-cert-3 | none (report) | none |
| 49 | 3064 | hash of a line, with `--proto-report` | none | none |
| 50 | 3085-3108 | partial mode: with `--proto-partial` a leaf that is not accepted (or, with `--proto-only`, not listed) becomes an "open leaf" and the run goes on | none (prototype mode) | none without the options: the inner `except` re-raises and the frozen handler takes over |
| 51 | 3151-3157 | verdict "PARTIAL" if there are open leaves or `--proto-only` was given | none | none |
| 52, 53 | 3166-3180, 3209-3225 | output for PARTIAL and for the step log | none | none |
| 54 | 3230-3232 | argparse description | none | none |
| 55, 56 | 3248-3269 | options `--proto-partial`, `--proto-only FILE`, `--proto-report` | none | none without them |
| 57 | 3284-3285 | exit code 11 for PARTIAL | none | none |

**Claim.** With the default options, for every input whose first line the frozen checker does not reject because of the
schema value "wx-cert-3", the candidate does what the frozen checker does: the same exit code, the same output lines
except the last (version string), and the same JSON report except the key `checker` (and `seconds`).

**Proof (by reading).** (i) Until the schema test `parse_header` is the frozen code plus `SCHEMA_V3[0] = False`. A schema
value other than the two strings is rejected with the frozen message. For "wx-cert-2" the gate stays False for the
whole certificate. (ii) With the gate False, hunks 8, 14 and 20 are not entered (each is guarded at the point where the
new element would be recognised), and the two `need_dict` calls of hunks 16 and 24 are the frozen calls, so the keys
`centre` are rejected as unknown keys before hunks 17 and 25 read them. Hence no parsed object of a wx-cert-2
certificate contains a `sq`, `pol` or `ind` fact, an `ind` declaration, a polynomial form, a step centre or a region
centre other than the identity. (iii) Every changed line of the evaluation (hunks 15, 18, 19, 22, 33, 34, 37, 41, 42,
43, 44) reduces to the frozen line when those objects do not exist: `seen_ind`, `ind_index` and `qforms` are empty,
`is_equality_fact` is the old test, `check_term_rules` loops over the facts and finds no listed option, a step has
`centre = None` and takes the unchanged `lower_bound`, and the two section-8 tests multiply by `conj((1,0)) = (1,0)`,
which returns the same Fractions. (iv) No new test can raise earlier than a frozen test on wx-cert-2 input: the new
tests of the parsers are behind the gate or loop over empty sets. (v) The report has new keys only under wx-cert-3
(hunk 48) or with the prototype options (hunks 46, 49, 50, 51).
The regression in P5 agrees: all files of `checker/v26/testcerts` give identical exit codes and identical reports with
the two programs, with the one expected exception F36.

**Refuted with the option `--allow-extra-keys`.** That option (it exists in the frozen checker too) switches off the
key test of `need_dict`. Then hunks 17 and 25 read a `centre` under the schema "wx-cert-2" and USE it, where the frozen
checker with the same option ignores the key. Demonstration, my files in `r30py/certs/quick/`:

| file | candidate, default | frozen 2.6, default | candidate `--allow-extra-keys` | frozen 2.6 `--allow-extra-keys` |
|---|---|---|---|---|
| `Q2`: the author's `pass/v2_plain.jsonl` (schema wx-cert-2) with a window centre of label 7 turned by 0.02 and the node centres of label 7 turned with it | FAIL (unknown key 'centre') | FAIL (the same) | **PASS, exit 0** | FAIL (the root arc of square 7 does not contain the window arc) |
| `Q3`: `Q2` without the key `centre` | FAIL (root arc of square 7) | FAIL (the same) | FAIL (the same) | FAIL (the same) |
| `Q4`: `Q2` with the schema "wx-cert-3" | PASS | FAIL (schema) | PASS | FAIL (schema) |

So with that option the candidate prints PASS for a wx-cert-2 certificate whose statement, read as the text defines
it for that schema (identity centres, section 8), is not proved by the file. This is a wrong acceptance; it needs a
non-default option. The same holds for a `centre` in a step under wx-cert-2 (the centred rule is then used; that
bound is mathematically valid, but the SCHEMA RULE rejects the element). The lead was told and has decided
that the option is removed and the two reads are gated; the edits are items M1 and M2 of P4.

## P2. Every new rule of the text against the code: can the code accept what the text rejects?

Status: DONE. Result: with the default options I found no input that the text rejects and the candidate accepts.
The one exception needs the option `--allow-extra-keys` (P1, P4).

How I tested. (i) Reading: the lines named in the table. (ii) My own test certificates, `r30py/certs/attack/`
(143 files, built by `r30py/r30_build.py` from the text and the packing file; manifest with my expectation and the
reason for each in `certs/attack/MANIFEST.json`; results in `r30py/out/attack_results.json`): every one of the 143
files gets the verdict I derived from the text, and every rejection names the defect I planted. (iii) For the rules
that are about a NUMBER (the two rules for L, the indicators, the squares) I wrote my own evaluator of a step from the
text alone, `r30py/r30_eval.py` (it imports nothing of a checker), and built pairs of files: one claims exactly the L
of the text and must pass, the other claims L + 10^-30 and must fail. A checker that computes another L fails one of
the two. The evaluator also reproduces, as exact rational strings, the L of all 14 pass files of the author's corpus
(`proto30/testcerts30/INDEX.json`) and the L of 10 leaves of the real certificate (P5).

Harnesses of my files: T (one node, root and terminal leaf, around the reference packing); I (root closed as
infeasible by a `0` step in round 1, so that every later round is NOT EVALUATED); IO (the root of I with an option
split, both children infeasible); M (header centres: label 3 turned by the rotation (15/17, 8/17) in window, tube and
node, where exactly ONE option of the pair (1,3) is not excluded: a list of length m = 1); S (box split, two leaves);
Y (sign split, two leaves).

| rule of the text | lines of the candidate | my files (prefix in `certs/attack/`) | what happened |
|---|---|---|---|
| (T1) multiplier >= 0 unless the term has `circ` | parse: 1088-1089 (every round); `check_step`: 2365-2366 | `R01` (not-evaluated round), `R20` (guarded corner with a negative multiplier), `X07` (negative multiplier with `circ`, exact L) | rejected / rejected / accepted exactly at L |
| (T2) `pol` only with `circ` | parse: 1090-1091 (every round); `check_step`: 2369-2370 | `R02` (not-evaluated round), P8 `c03d` (multiplier 0, both kinds of round), `X07` | rejected; rejected; accepted exactly at L |
| (T3) GUARD RULE: every corner name of a listed option needs the indicator name of THAT option; also with `circ` | `check_term_rules` 1924-1943, called from `check_step` 2371, `remainder` 2089-2090, `remainder_streaming` 2176-2177 | `R14`, `R21` (multiplier 0), `R22` (indicator of another pair), `R24` (two options, one guard), `R25` (with `circ` and `pol`), `R31` (m = 1), `R23` (one guard, two corners of its option: allowed) | all rejected; `R23` accepted |
| (T3) is tested in evaluated rounds only | `check_term_rules` is reached from `check_step` only; `run_round` (2488) runs for evaluated rounds only | `R03` | accepted, as the last item of section 10 says |
| (T4) corner name: option opt-available or ind-listed IN THIS ROUND | `fact_poly` 1999-2007 (`opt_available`, `ind_index` of this `RoundEnv`) | `R26` (listed in round 1, used in round 2), P8 `c03a`, `c03f` (multiplier 0, raw and centred) | rejected |
| (T4) `ind:i:j:k`: pair declared in this round, k <= m | `ind_options` 1914-1922 via `fact_poly` 2008-2010 | `R27` (declared in another round), `R32` (m = 1, k = 2), P8 `c03g`, `c03g2`; not-evaluated round: `R04a`, `R04b` | rejected; in a not-evaluated round accepted, as the text says |
| (T4) `sq:NAME`, `pol:NAME`: form defined in THIS node; whole file | parse 725-728; `fact_poly` 2034-2042 | `R05`, `R06` (not-evaluated round), `Q03` (defined in the parent only), `Q04` (only a custom form of that name) | rejected |
| names: `ind:i:j:k` with i < j in I and one digit 1..8; no `ind:...:bin`, no `sq:a:b` | 729-735; 725 (`n == 2`) | `R13a`, `R13b` (not-evaluated round), `Q12`, `C08` | rejected |
| (R1) one `ind` declaration per pair and round | parse 1030-1032 (every round); again `declare_ind` 1890-1891 | `R07` (not-evaluated round) | rejected |
| (R2) no `opt` and `ind` declaration of one pair in a round | parse 1060-1064 (every round) | `R08` (not-evaluated round); `R29` (opt in round 1, ind in round 2: allowed) | rejected; accepted |
| (R3) no `ind` declaration for a pair with an option assumption of the node | `parse_node` 1199-1205 (every round) | `R09` (child with the assumption, not-evaluated round); `R30` (a SIGN assumption: allowed) | rejected; accepted |
| shape of an `ind` declaration: exactly i, j, mode, options; 1 to 8 options of that pair, pairwise different | 1014-1034 | `R12` (not-evaluated round), `S10`, `S13`, `S14`, `S15`, `S16`, `S17` | rejected |
| PRECONDITION of an `ind` declaration: every option NOT in the list excluded by the test of 4.7 on the store at the START of the round; a failing declaration rejects even if unused; tested in evaluated rounds only | `declare_ind` 1886-1903 calls `excluded` (1721-1733, the frozen code) of the `RoundEnv`, which `run_round` builds from the store at the start of the round (2492-2494), before any step | `P01` (round 1 LOOSENS the box, so two more options are possible at the start of round 2; the list that was complete on the node's data is rejected in round 2), `P02`, `P03` (controls), `P04`, `P05` (unused), `R33`; `R10` (not-evaluated round: accepted). Added after the referee's report (P6): `certs/excl2/X1`-`X7`, where the omitted option is excluded only by a CUT that round 1 certifies and stores: the declaration is accepted in round 2, rejected in round 1, rejected if the cut is not stored, rejected with the cut at the threshold (the test of 4.7 is strict), accepted just below it; the frozen checker gives the same five verdicts for an `opt` declaration on the same stores (`Y1`-`Y5`). `certs/excl/E1`-`E4`: the declaration on the start store of a 2.6 corpus file that has cuts and relative arc entries | as the text says in all |
| indicator variables belong to the ROUND | a new `RoundEnv` per round (2492): `ind_declared`, `ind_index` and all caches of polynomials are attributes of it (1771-1784) | `X13a` (round 1 list of 2, round 2 list of 3), `X13b` (the reverse): exact L in round 2 | accepted exactly at L, rejected at L + 10^-30 |
| the LAST indicator is 1 minus the others; SB of an indicator variable is [0, 1] | `ind_poly` 1905-1912; `sb` 1660-1661 | `X08` (ind_1 + ind_2 is the constant 1), `X09` (products, squares), `X11` (m = 3), `X12` (list in the other order), `X14` (two pairs) | exact in all |
| m = 1: ind_1 = 1, no variable | `ind_poly` 1909-1912 | `K05`, `X15`, `R31`, `R32` | exact; guard still required; k = 2 rejected |
| polynomial forms: nonempty list of [number, list of 0..2 base variable names of I]; monomials pairwise different as multisets; coefficient 0 allowed; NAME pattern; own name space; per node | `parse_qforms` 892-923, `parse_base_variable` 876-889, `parse_node` 1184-1192 | `Q01` (label 4 with sixteen labels), `Q02` (seventeen labels), `Q05`, `Q06a-c`, `Q07` (repeated key), `Q08`, `Q10`, `Q11`, `Q13` (cut on a polynomial form), `Q14` (component of a custom form), `Q09` (zero form), `Q15` (same NAME in two nodes: each node its own form) | as the text says in all |
| `sq:NAME` := (q:NAME)^2, `pol:NAME` := q:NAME | `fact_poly` 2034-2042; `product_nocache` 2153-2169 (centred path) | `X04`, `X05`, `X06`, `X07`, `X14` | exact |
| RAW RULE with exponents: a variable of exponent e is multiplied e times (the interval of s^2 for s in [-a, a] is [-a^2, a^2]) | `mono_interval` 2049-2058 | `X01` | exact (a checker that takes [0, a^2] accepts the `_above` file; this one rejects it) |
| CENTRED RULE: exact substitution v = c_v + y_v, intervals SB(v) - c_v, indicator variables with centre 0 and [0, 1], exponents by repeated multiplication, any rational centre, a centre for a variable that does not occur | `check_step` 2377-2380; `lower_bound_centred` 2248-2292; `centred_remainder` 2196-2229; `centred_interval` 2231-2246; `remainder_streaming` 2171-2194 | `X02` (empty object: the raw L), `X03`, `X05`, `X06` (centres far outside the intervals), `X07`, `X10`, `X11`, `X14`, `X15`, `X17` (the `0` step with a centre) | exact in all |
| `centre` of a step: an object; keys base variables of I, written canonically; values numbers; checked in every round | `parse_centre` 926-937 | `C01`-`C08`, `R11` (not-evaluated round), `C09` (misspelt key of the step) | rejected |
| header centres: optional, independent in window and tube, exactly the keys of I, unit rotations | `parse_region` 1216-1235 | `D04`, `D05`, `D06`, `D12`; `D07` (a half turn (-1, 0): allowed) | rejected; accepted |
| ROOT CONTAINS WINDOW with `Ab := conj(gamma) rho P` | `root_failure` 2715-2722 | `K05` (control), `D02` (window centre mirrored: `gamma rho` would be the identity, `conj(gamma) rho` is a turn by 56 degrees), `D09` (no window centre) | accepted; rejected; rejected |
| TERMINAL TEST with `Ab := conj(gammaT) rho P` | `terminal_failure` 2530-2536 | `D03` (mirrored), `D08` (no tube centre), `D10` / `D11` (tube radius 6.7e-10 above / 3.3e-10 below what the arc end needs, with a turned tube centre) | rejected; rejected; accepted / rejected |
| SCHEMA RULE: under wx-cert-2 every new element rejects, also in a round that is not evaluated; any other schema string rejects | gates at 725, 729, 1014, 1069, 1185, 1219; `parse_header` 1249-1256 | `S01`-`S06` (new elements under wx-cert-2 in a not-evaluated round or in the header), `S07a-e`, `S08` | rejected (default options) |
| a certificate without new elements is checked alike under both strings | the same code path | P5: the 358 files of the 2.6 corpus with the schema string changed to "wx-cert-3" | 357 reports identical to the frozen checker's on the original; the 358th is F36 |
| KEYS: every object has exactly its keys | `need_dict` 239-250 and its calls for the header, window, tube, node, arc entry, assumption, round, declaration, step, store and its arc and rarc entries, split, close, option | `S09`-`S13`, `C09`, `D05`, `D13` | rejected (default options); **not enforced with `--allow-extra-keys`** |

Two remarks on this table.
- Where the text says a test is made "in the evaluated rounds only" the code does exactly that, and accepts the
  violation in a round that is not evaluated (`R03`, `R04a`, `R04b`, `R10`, P8 `c03h`). This is what the last item of
  WELL-FORMEDNESS says; I note it because a second checker must do the same.
- The docstring of `check_term_rules` (1925-1932) and the comment at 2000-2003 still describe the earlier prototype
  ("in a term WITHOUT an equality fact ..."; "or with an equality fact"): they say a term with `circ` is exempt
  from the guard. The CODE has no such exemption (the comment at 1933-1935 says so, and `R25` is rejected). The stale
  sentences are item S3 of P7.

## P3. Exactness, caches

Status: DONE.

**Numbers.** Every number that enters an acceptance decision is a `fractions.Fraction` or an `int`. The candidate
has no `assert` (so `python -O` removes nothing) and no float in any comparison: `float(` occurs only in `_short`
(text of a message, 2408) and in the `--proto-report` output (3002-3010); `round(` only for seconds. JSON floats are
rejected by the parser (`_json_no_float`). The new arithmetic: `centred_remainder` works with integers (the centre is
written over one common denominator E, the result has the denominator D * E^dmax), `centred_interval` with Fractions,
`lower_bound_centred` sums integers per denominator and returns one Fraction. Every `//` in the new code divides
exactly (by a divisor of an lcm, or after the test `D % d != 0` has enlarged D). I checked the algebra of
`remainder_streaming` and `centred_remainder` by hand, and the numbers against my own evaluator (P2, P5).

**Caches and other state that outlives a step**, with the key and why the key is complete:

| where | lifetime | key | value depends on | complete? |
|---|---|---|---|---|
| `LABELS`, `LABEL_SET`, `PAIRS`, table of base variables (`select_labels`, 219-236; 385-413) | one certificate (reset by `parse_header`) | the header's `labels` | nothing else | yes |
| `SCHEMA_V3[0]` (137) | one certificate (reset at 1249, set at 1256) | the header's schema | nothing else | yes. In library use, code that parses a node without having parsed a header first gets the schema of the previous certificate; the command line always parses the header first |
| `VAR_Z`, and the entries that `zvar_number` appends to `VAR_NAMES`, `VAR_FORMS` (412-429) | one certificate | (i, j, k) | nothing: the entry is only the NUMBER of the variable z_{ij,k} | yes. The number is the same in every round and node; what the variable MEANS (which option) is decided by the `ind_declared` of the round. No polynomial or interval that contains an indicator variable is stored outside a `RoundEnv` (the caches of `NodeGeom` hold named forms only, a store has no such entry, certified values are numbers) |
| `NodeGeom._form_cache`, `_combo_cache` (1301-1302) | one node (`_check_node` 2609) | the form | the node's centres and custom forms | yes |
| `NodeData.qforms` (1184-1192) | one node | NAME | the node's `forms` | yes; test `Q15` |
| `StoreEnv._sb`, `_eff`, `_excl` (1518-1520) | one store (a new object for the store at the start of every round, for every EMPTY test and for the final store) | form; pair; option | the store, which is never changed after it is built (`accept_store` builds a new one) | yes; tests `P01`-`P04` |
| `RoundEnv.opt_available`, `par_available`, `ps_available`, `ind_declared`, `ind_index` (1775-1779) | one round | option; (i, j, K, kind); pair | the declarations of the round, all processed before the first step (2493-2494) | yes |
| `RoundEnv._fact`, `_fact_sp` (1780-1781) | one round | the parsed fact | store, declarations, node; for `ind:i:j:k` also the length m of the list of this round | yes: a fact polynomial is first built in a step, after all declarations; tests `X13a`, `X13b` |
| `RoundEnv._product` (1782) | one round | the sorted tuple of facts of a term | the fact polynomials | yes (raw path only) |
| `RoundEnv._mono`, `_mono_int` (1783-1784) | one round | the monomial | the store bounds | yes |
| `cache` in `lower_bound_centred` (2256) | one step | the monomial | the store bounds and the centre of this step | yes (a new dictionary per call) |
| `PROTO_LOG`, `OPTIONS` | process | - | report only / options | not read by any test, except `OPTIONS["allow_extra_keys"]`, `["paranoid"]`, `["proto_partial"]`, `["proto_only"]` (P4) |

So I found no cache that can return a value computed for another round, node or store.

## P4. Modes, options, exits

Status: DONE. This part is meant to be exhaustive; the edits are numbered for P7.

**Command-line options** (all of `main`, 3229-3290) and what each can do to a verdict:

| option | in the frozen 2.6 file? | can it give PASS / exit 0 where the text rejects, or where something was not checked? | what to do before freezing |
|---|---|---|---|
| `--node ID` | yes | no: verdict "NODE-ACCEPTED", exit 10, the output never contains the word PASS; lines of other nodes are not even parsed | keep |
| `--json FILE` | yes | no (if the file cannot be written: FAIL, exit 1) | keep |
| `--packing FILE`, `--expect-packing-sha256 HEX`, `--no-packing-pin` | yes | they change the REFERENCE FILE, not what is checked: the header's `packing_sha256` must equal the file read, and the report carries that hash. A PASS is then a statement about that file. As in 2.6 the acceptance script must compare the report's `packing_sha256` with 24e296f5... | keep (no change against 2.6) |
| `--keep-going` | yes | no: after a failure `failed` is set and the verdict stays FAIL | keep |
| `--paranoid` | yes | no: it adds a comparison of the fast L with a literal one and rejects if they differ; for a step with a centre it uses `lower_bound_reference_centred` | keep |
| `--allow-extra-keys` | yes | **yes.** (1) KEYS is normative in 3.0, so every undefined key that the option lets through is an acceptance against the text. (2) Under wx-cert-2 a `centre` of the header or of a step is then USED (P1, files `Q2`, `Q3`) | **remove (M1)** |
| `--proto-partial` | no | no PASS: a leaf that is not accepted becomes an "open leaf" and the verdict is "PARTIAL", exit 11. But it is a third verdict, and in this mode ANY exception inside `check_node` of a leaf, also an internal error, is turned into an open leaf (3093-3108) | **remove (M3)** |
| `--proto-only FILE` | no | no PASS: verdict PARTIAL even if every leaf is listed and accepted (3154-3157); leaves not in the file are not evaluated | **remove (M3)** |
| `--proto-report` | no | no: it only records. The dictionary `_info` is filled after L is computed and is read by no test. If the conversion of a number for the report failed, the result would be FAIL, not PASS (the conversion is outside the place where the verdict is set, and `main` prints FAIL for any exception) | remove (S1) |

**Environment.** The program reads no environment variable (no `os.environ`, no `getenv`; `os` is imported only to
find the default packing file). It has no `assert`, so `-O` and `PYTHONOPTIMIZE` change nothing. `PYTHONHASHSEED` can
change which of several defects is reported first in a few places, never a verdict (the loops that decide are over
sorted keys or over lists). The digit limit of newer Pythons is switched off in the program (124-125). What CAN change
the behaviour from outside is what Python itself imports: a file `fractions.py` or `json.py` in the folder of the
script or on `PYTHONPATH` would replace the standard module. I looked: `proto30/`, `checker/`, `checker2/` contain no
file or folder with the name of a standard module the program imports. Advice for the acceptance script, not for the
checker: start it as `python -I -B ...` (isolated mode: no `PYTHON*` variables, the script's folder not on the path).

**Exit codes and words.** `PASS` is printed only for `report["verdict"] == "PASS"`; exit 0 only for that verdict in
mode "full" (3280-3281). The verdict is set to PASS in one place (3158), after: every line parsed, every node
accepted (`failed` is False), not node mode, at least one node, `tree.finish()`, no open leaves, no `--proto-only`.
Any exception anywhere gives FAIL (2977-2984 and 3286-3289).

**Elements read without the schema gate being tested where the value takes effect.** I went through every place
where one of the new elements enters:

| element | where its shape is validated | where its value is read | gate at the point of use? |
|---|---|---|---|
| names `sq:`, `pol:`, `ind:` | `parse_fact_name` 725-735 | the same lines create the parsed fact; nothing else can create one | yes (`SCHEMA_V3[0] and ...`) |
| declaration with the mode "ind" | 1014-1034 | the same lines create the declaration | yes |
| keys `q:NAME` of `forms` | 1185-1190 | the same lines create `qforms` | yes |
| `centre` of a step | `need_dict(..., optional=(("centre",) if SCHEMA_V3[0] else ()))` at 1069 | `sd.centre = parse_centre(...) if "centre" in s else None` at 1071 | **no** |
| `centre` of the header's window / terminal | `need_dict(..., optional=...)` at 1219 | `rg.has_centre = "centre" in x` at 1221, used at 2532 and 2717-2718 | **no** |

These two are the only places of that pattern. I also looked at every other key that is read with `in` or `.get`
instead of through the list of `need_dict` (`kind`, `mode`, `kappa`, `pair`, `forms`, `labels`, `S_floor`, the `c` of
a store arc entry, `id`): none of them belongs to a new element. The evaluation code that uses the two values
(`check_step` 2377-2380, `terminal_failure` 2532, `root_failure` 2717-2718) does not test the schema either; it does
not need to once the reads are gated.

**Edits** (line numbers of the candidate as reviewed):

- **M1.** Remove the option that ignores undefined keys. Delete the `--allow-extra-keys` argument (3246-3247) and
  the line `OPTIONS["allow_extra_keys"] = bool(args.allow_extra_keys)` (3260); in `OPTIONS` (130) delete the key
  `allow_extra_keys` and its comment line (128); in `need_dict` (246-249) replace `if not OPTIONS["allow_extra_keys"]:`
  and its loop by the loop alone, so that a key outside `required` and `optional` always rejects.
- **M2.** Gate the two reads. Line 1071: `sd.centre = parse_centre(s["centre"], w + " centre") if (SCHEMA_V3[0] and "centre" in s) else None`.
  Line 1221: `rg.has_centre = SCHEMA_V3[0] and "centre" in x`.
- **M3.** Remove the partial mode. Delete: docstring line 84; lines 139-150 (`proto_partial`, `proto_only`,
  `PROTO_NOT_EVALUATED`); in `_check_certificate` replace 3087-3108 by the frozen line `res = check_node(node, ref, header)`;
  delete 3151-3157 (the two PARTIAL verdicts), 3166-3180 (output), 3248-3254 (the two arguments), 3262-3269 (their
  handling, including the forced `--keep-going`), 3284-3285 (exit code 11).
- **M4.** The identity of the program. Replace the two prototype docstring blocks (3-49) and the contract paragraph
  (50-66) by a text for version 3.0; `CHECKER_VERSION` (119); `SPEC_SHA256` (120) must be the SHA-256 of the text that
  is adopted (the report key `spec_sha256` of a wx-cert-3 run names the 2.6 text today:
  fa14fe40...); the argparse description (3230-3232), which still says "plus items 1, 2, 5 of SPEC_v3.0_DRAFT.md".
- S1 (should). Remove `--proto-report` and what serves only it: 131-133, 138, the parameter `info` and the block
  2271-2287 of `lower_bound_centred`, `_proto_clock` (2350-2353), 2375-2376 and 2381-2386 of `check_step` (the call
  becomes `L = env.lower_bound_centred(g, step.terms, step.centre, what)`), 2974, 2986-2992, `_proto_step_entry`
  (2996-3011), 3064, 3085-3086, 3209-3225, 3255-3257, 3261.
- S2 (should). Two messages that are wrong under wx-cert-3: `header: schema is not 'wx-cert-2'` (1255) for a schema
  string that is neither of the two, and `... is not one of ('opt', 'par')` (1035) for a bad mode. If the first is
  changed, the report for a header with a third schema string is no longer the frozen checker's word for word (no
  file of the 2.6 corpus has such a header; its only file with another schema string is F36, with "wx-cert-3").
- S3 (should). Stale sentences from the earlier prototype, in a file whose docstrings are supposed to say what is
  implemented: `is_equality_fact` (433-436, "and, draft item 6, ind:i:j:k:bin"); `check_term_rules` (1925-1932, the
  exemption of terms with an equality fact, which the code does not have); the block 1870-1884 ("the facts of this
  section", the equality `ind_k^2 = ind_k`); the comment at 2000-2003 ("or with an equality fact"); "draft item N"
  everywhere should become the section of SPEC 3.0.
- S4 (should). `check_step` reads the centre with `getattr(step, "centre", None)` (2377, 2383). `StepData` always has
  the slot; write `step.centre`.

After M1 to M4 the options of the file are those of the frozen 2.6 checker minus `--allow-extra-keys`.

## P5. Runs

Status: DONE. Interpreter
CPython 3.9.6 of the project environment; default options unless said; outputs in `r30py/out/`, logs in
`r30py/logs/`.

| run | files | result |
|---|---|---|
| regression corpus `checker/v26/testcerts` (INDEX.json), frozen 2.6 checker AND candidate, each as a command with `--json` (`r30_run.py corpus26`) | 358 | exit codes and whole reports identical (apart from `checker`, `seconds`) in **357**; the one difference is `fail/F36.jsonl` (frozen: FAIL, schema; candidate: PASS), as expected. Frozen: 44 PASS, 314 FAIL; candidate: 45 PASS, 313 FAIL |
| the same 358 files with the header's schema string changed to "wx-cert-3", candidate, against the frozen checker's report on the original (`r30_run.py swap26`) | 358 | identical in **357** (apart from the keys that exist only under wx-cert-3 and the hash of the changed file); the 358th is again F36, which has the string "wx-cert-3" already |
| the author's `proto30/testcerts30` (`r30_run.py tests30`) | 72 | all 72 verdicts as in the author's INDEX.json (14 PASS, 58 FAIL), reasons identical; the 8 files with the schema wx-cert-2 give identical reports with the frozen checker |
| the author's 14 pass files, L recomputed by my evaluator | 14 | my L equals the L of INDEX.json as a rational string in all 14 (raw rule and centred rule, lists of 2 and of 8 options) |
| my attack files (`r30_run.py attack`) | 143 | all 143 as I derived from the text (43 PASS, 100 FAIL), every rejection for the planted reason |
| the candidate with `--paranoid` against the candidate without it, on my attack files, the P8 files (wx-cert-3 copies) and the author's 72 (`r30_paranoid.py`) | 304 | the same verdict and the same report in all 304 (69 PASS, 235 FAIL): on every accepted step of these files the fast and the literal evaluation of L agree, raw and centred |
| P8 corner cases (`r30_p8.py`) | 89 cases, 172 files | all as the lead decided, frozen and candidate (P8) |
| the rows of the referee's ambiguity lists for which I had no file (`r30_p6.py`): frozen checker and candidate on the wx-cert-2 copy, candidate on the wx-cert-3 copy | 65 cases, 123 files, 181 runs | all three programs as the reading that the referee reports for the frozen checkers (31 cases allowed, 34 rejected); the frozen checker and the candidate give the same reason in every wx-cert-2 file; report and exit code agree in every run (P6) |
| the `ind` precondition when the exclusion of the omitted option depends on a cut of the start store (`r30_excl2.py`): 7 files with `ind`; the same five situations with `opt` under both schema strings, frozen checker and candidate | 17 | all 17 as expected (7 PASS, 10 FAIL), every rejection names the option that is not excluded; on the five wx-cert-2 files the frozen checker and the candidate give identical reports |
| an `ind` declaration inserted into the accepted 2.6 corpus file `pass/t2_iv_17.jsonl`, on a start store with 7 cuts and 2 relative arc entries; variants with one cut or the relative arcs removed (`r30_excl.py`) | 22 | `ind` list of the one possible option: accepted; of another option: rejected; of all 8: accepted. In this file the declaration does not depend on the cuts (it is valid on the node's data too), which is why `r30_excl2.py` was built; the 10 wx-cert-2 controls give identical reports with the frozen checker |
| the real certificate `proto30/out/tree3/c01/G20S_v3_c01.jsonl.gz` (sha256 989e9738...8273, verified), ONCE, with `--json` | 1 | **PASS**, exit 0, 654.9 s, 260 MB; 153 nodes accepted: 81 infeasible (each by one `0` step), 71 split, 1 terminal; 81 steps, 1,614,692 terms; `certificate_uncompressed_sha256` f678f75a...da58. Report: `r30py/out/G20S_v3_c01.<reviewer>.report.json`. All 153 node entries (closure, evidence, digest of the final store) equal the author's stored `complete.report.json` |
| one leaf of the real certificate, L by my evaluator (`r30_leaf.py`) and by the candidate in node mode | 1 + 9 | see below |

The leaves of the real certificate use only names my evaluator knows (box, arc slo/shi/clo/chi, wall, opt, ind, sq,
circ, pol), one centred step on the form `0` each, with `ind` lists of 2, 3 and 4 options. For the smallest leaf,
`MAIN.X32__xi_16_2__hi` (13,248 terms, 11 indicator variables, 16,786 monomials of degree up to 5), my evaluator
gives an L whose rational string (denominator of 1,169 digits) is **identical** to the L the candidate reports for
that node (`--node`, `--proto-report`) and to the L in the author's stored report; L = 0.0736 >= value = 0.0368 > 0.
The same comparison for nine more leaves, spread over the sizes and including the largest: `r30py/out/leaf/LEAVES_COMPARED.json`
(result below).
The lead reports that the Node checker written from the text agrees with the candidate on the L of all 81 leaves; I
did not look at that checker.

Result for the nine: **L identical as rational strings in 9 of 9** (denominators of 1,159 to 1,170 digits), every one
accepted by the text and by the candidate (NODE-ACCEPTED). They are `MAIN.X17__xi_14_1__lo`, `MAIN.X28__xi_17_1__hi`,
`MAIN.X06__xi_5_1__lo`, `MAIN.X22__xi_15_1__lo`, `MAIN.X59__xi_2_2__hi` (exit leaves, 19,202 to 19,548 terms, 11
indicator variables) and `W19`, `W12`, `W03`, `W01` (wrong-option leaves, 20,032 to 26,370 terms, 13 to 30 indicator
variables; `W01` is the largest leaf of the file; `W03` has L = 5.08e-3 against a claimed 2.54e-3). So for 10 of the
81 leaves the number L was computed three times, by programs that share no code as far as I can see: the candidate,
my evaluator, and (the lead's report) the Node checker.

## P8. Ten corner cases on which the text is silent or loose

Status: DONE. **On all ten points the Python side already does what the lead decided, the frozen `wxcheck_v26.py` and
the candidate alike. No edit follows from this part, and it gives no entry for the 2.6 errata from the Python side.**

Test files: `r30py/certs/p8/`, 89 cases, each as `<name>__v2.jsonl` (schema wx-cert-2: run with the frozen checker and
with the candidate) and `<name>__v3.jsonl` (schema wx-cert-3: candidate); six cases need an element of 3.0 and exist
only as `__v3`. Built by `r30py/r30_p8.py build` on the harnesses of P2 ("ev" = the item stands in an evaluated
round, "un" = in round 2 of harness I, which is not evaluated). Default options. Every row of the full table
`r30py/out/P8_TABLE.md` (89 rows, with the reason each program gives) agrees in all three columns; results as data:
`r30py/out/p8_results.json`. Condensed:

| # | case | tested (file prefix) | frozen 2.6 | candidate, wx-cert-2 | candidate, wx-cert-3 | decided | differs? |
|---|---|---|---|---|---|---|---|
| 1 | `arc:i:tan:G:H`, `rarc:i:j:tan:G:H` with G^2 + H^2 > 1 | `c01a`-`c01d`: both names, ev and un. Controls on the circle (3/5, 4/5): `c01e`, `c01f` | rejected in all four ("tangent vector needs G^2 + H^2 <= 1", when the name is parsed); controls allowed | the same | the same | rejected wherever the name stands | no |
| 2 | two `par` declarations with the same (i, j, cls, kind) | `c02a` ev, un | rejected | rejected | rejected | rejected, whole file | no |
| 2 | `u:NAME` not defined in `forms` | `c02b`: as the step's form (ev, un); inside `cut:u:..:lo`, inside `ivl:u:..:lo`, as a cut key of the proposed store (un) | rejected in all five | the same | the same | rejected, whole file | no |
| 2 | a term with 0 or 4 names | `c02c` ev, un, each | rejected | rejected | rejected | rejected, whole file | no |
| 2 | `ivl:FORM` for a form that is not Da, Db or an affine custom form | `c02d`: `ivl:A:1:3:lo` (ev, un); `ivl:u:w:lo` with w = A:1:3 (un). Control: an affine custom form (ev) | rejected; control allowed | the same | the same | rejected, whole file | no |
| 2 | the name `cut:0:lo` | `c02e` ev, un | rejected | rejected | rejected | rejected, whole file | no |
| 2 | a `0` step with the sense "hi" | `c02f` ev, un | rejected | rejected | rejected | rejected, whole file | no |
| 3 | multiplier 0 with a name that is not available (T4) | evaluated round, raw rule: an undeclared option (`c03a`), a cut the store does not have (`c03b`), an undeclared `par` fact (`c03c`), `asg` without the assumption (`c03c2`) | rejected in all four | rejected | rejected | rejected | no |
| 3 | the same under the centred rule; `ind` names | `c03f` (centre {}), `c03g` (indicator of an undeclared pair), `c03g2` (k > m, with a centre) | - | - | rejected | rejected | no |
| 3 | multiplier 0 with `pol` and no `circ` (T2) | `c03d` ev, un | - | - | rejected in both | rejected | no |
| 3 | multiplier 0 with an unguarded corner name of a listed option (T3) | `c03e` ev (also `R21` of P2) | - | - | rejected | rejected | no |
| 3 | for information: the term of `c03a` in a round that is NOT evaluated | `c03h` | accepted | accepted | accepted | (T3) and (T4) are not tested in such a round for ANY multiplier (section 10, last item); I took the decision to mean evaluated rounds for these two rules | - |
| 4 | a proposed store with the cut key `0:lo` or `0:hi` | `c04`: lo and hi, store of an evaluated round and of a round that is not evaluated | rejected in all four ("no cut on the form 0", when the store is parsed) | the same | the same | rejected | no |
| 5 | `"forms": {"x": []}` | `c05`, two files | rejected ("a custom form needs at least one component") | rejected | rejected | rejected | no |
| 6 | header: a window or tube interval with lo > hi | `c06a`, `c06b` | rejected at the header | the same | the same | rejected at the header | no |
| 6 | header: alpha <= 0 | `c06c` (window 0), `c06d` (window negative), `c06e` (tube 0) | rejected at the header | the same | the same | rejected at the header | no |
| 6 | header: tube alphaT > 1 in a tree without a terminal node | `c06f` (11/10; harness I has only an infeasible root). Control alphaT = 1: `c06g`. For information, window alpha = 1: `c06h` | rejected at the header; control allowed; `c06h` rejected (alpha < 1) | the same | the same | rejected at the header | no |
| 7 | `kappa` on a P+ / P- declaration | absent (`c07a`), "1/2" (`c07b`): allowed and ignored. "abc", the JSON number 1, the float 0.5, null (`c07c`-`c07f`, evaluated round), "1/0" in a round that is not evaluated (`c07g`): rejected. "1/2" in such a round (`c07h`): allowed | as described | the same | the same | absent fine; present and malformed rejected | no |
| 8 | 5.0, 1e0, "1" (and `true`) where an integer is expected | a label field (`sq` of a split: `c08a`; `i` of a declaration in a round that is not evaluated: `c08e`), `k` (`c08b`), `eps` (option of a split: `c08c`; `opt` declaration: `c08f`), `sign` (`c08d`), each with 1.0, 1e0, "1", true; header `labels` 16.0 (`c08g`) | rejected in all 25. A float literal is rejected by the JSON reader wherever it stands in the file; a string or a boolean by the type test of the field | the same | the same | rejected | no |
| 9 | an option split that lists one option twice | `c09a` (three children, two with the same assumption) | allowed (PASS) | allowed | allowed | allowed | no |
| 9 | an `opt` declaration repeated in a round | `c09b` ev (with a corner name in a term), un | allowed | allowed | allowed | allowed | no |
| 10 | `packing_sha256` in upper case | `c10`: all letters upper case; one letter upper case | rejected (string comparison with the digest) | rejected | rejected | rejected | no |

Where the tests are made in the code (the same lines in both files, apart from the shift): 1: `parse_fact_name`
750-765; 2: `parse_round` 1056-1057, `parse_form_tokens` 684-689, `parse_round` 1083-1084, `parse_fact_name` 787-796,
`parse_round` 1074-1075; 3: every term's product is formed before the multiplier is looked at (`remainder` 2092,
`remainder_streaming` 2181), and the tests of `check_step` 2363-2371 do not look at the multiplier; 4: `parse_store`
997-998; 5: `parse_forms` 859-860; 6: `parse_region` 1229-1234 (`parse_box(..., ordered=True)`, alpha > 0),
`parse_header` 1279-1283; 7: `parse_round` 1050-1052; 8: `loads_strict` 182-192, `need_label` 267-271, `need_choice`
293-298; 9: `parse_split` 1115-1123 has no test for repeated options, `declare_opt` 1796 adds to a set; 10:
`parse_header` 1258-1261.


## P6. After reading the author's notes and the referee's report

Status: DONE. Read: `proto30/PROTO_NOTES.md` sections 12 to 17 (sha256 of the file then a19fa14b...68b1;
a section 18 was added later: I only searched it for statements about the checker and found none that changes
anything here) and `reviews/REVIEW_30.md` twice: first (sha256 e1c52b97...9aac, 286 lines, part A only) and
again, while it was still growing (last state read: sha256 78df0a57...7339, 1,031 lines; parts A to D and
F complete, part E written except for one result that is still a placeholder).

**The author's notes.** Nothing in them changes P1 to P5. What they add:

- Sections 12 and 17 explain the history that the stale docstrings come from. The first prototype (`wxproto30.py`)
  had equality facts `ind:i:j:k:bin`, product facts `ind:i:j:k:E1:E2`, centres for indicator variables and an
  exemption from the guard rule for terms with an equality fact. The lead's decisions dropped all four, and
  `wxproto30b.py` is the first prototype with 20 marked replacements. In the file I reviewed none of the four exists:
  the only `ind` name is `ind:i:j:k` (729-735), a `centre` key is a base variable (926-937), `is_equality_fact` is
  `circ` only (437), `check_term_rules` exempts nothing (1936-1943). My tests `C08`, `R25` and the author's
  `no_such_name_*` files agree.
- 17.5 says which rules had no test of their own: (T3) and (T4) in a second round, and a term with indicators of two
  pairs. My files `R26`, `R27`, `X13a`, `X13b`, `X14` are such tests.
- 15.7 and 17.7: a `--paranoid` pass over the complete file was started twice and stopped without a result; "fast =
  literal" was shown by the author on single leaves only. Independent of that: my evaluator on ten leaves (P5), the
  Node checker on all 81 (the lead's word), and `--paranoid` on all small files (table of P5).
- 17.1 says "under wx-cert-2 every new element meets the frozen checker's own code and is rejected with its
  message". That is true with the default options; the notes do not mention `--allow-extra-keys` (P1).
- 16: six `ind` declarations of the real certificate list an option that the leaf's own box already excludes. The
  text allows it (4.10 PRECONDITION) and so does the code (`X11`, `P03`).

**The referee's report, first reading (part A).** At the first reading only part A (soundness) existed. It finds no false
statement. Its remarks that touch a checker, and the reading THIS code implements:

| remark of `REVIEW_30.md` | reading of the candidate | evidence |
|---|---|---|
| A-1: a term with `circ` is exempt from the sign rule, NOT from (T3) and (T4) | the same: `check_term_rules` has no exemption; the polynomial of every name of every term is built, whatever the term contains and whatever its multiplier | `R25`; P8 `c03a`-`c03g2` |
| A-2: the text nowhere lists what a checker does in an evaluated round, in which order | `run_round` (2488-2508) and `_check_node` (2607-2675): (1) the start store (the node's data, or the store accepted in the round before); (2) every declaration of the round in list order, each tested on the start store, a failing one rejects; (3) every step in list order: for each term the sign rule, (T2), (T3); then Rem, which builds the polynomial of every name and so tests (T4); then L and the claim; the certified value of every accepted step that is not a `0` step is noted; (4) the proposed store, entry by entry, against the start store and the certified values of this round; (5) the EMPTY test on the new store. If the round had an accepted `0` step or the new store is EMPTY, later rounds are not evaluated. Note: an accepted `0` step does not end its round; the remaining steps and the proposed store of that round are still tested and can still reject | reading; `R14`, `R15` (a bad step before / after the `0` step of the same round rejects), `R16` (a store entry that is not implied, in the round of the `0` step, rejects) |
| A-4: can a round start with an EMPTY store? | no. The EMPTY test is made on the store after every round (2621) and a positive answer ends the evaluation (2622-2623). The initial store cannot be EMPTY for node data that passed the parser (it has no cuts and no relative-arc entries); the code tests it all the same and would reject with "internal" (2612-2613) | reading |
| A-3: (R1) to (R3) are well-formedness, not soundness | tested when the node is parsed, in every round | `R07`, `R08`, `R09` |
| A.3, table: two corners of one option with one guard; a list with an excluded option; a list of one option; the eliminated indicator as a guard | all accepted, with the L of the text | `R23`; `X11`, `P03`; `K05`, `X15`; `X10`, `X12` |
| A.4, point 6: no limit on the degree | none in the code | `X07` (degree 6) |

**The referee's report, second reading (parts B, C, D, F).** What it says about this program, which the referee used as a
black box with the default options (plus `--proto-report` to read L):

- B.6: on all 1,801 wx-cert-2 test files that exist in the folder the prototype gives the verdict of the frozen
  Python checker in 1,800; the one difference is F36. My 358 files are a subset of the referee's; I compared whole reports, the referee
  compared verdicts on five times as many files.
- C.2: the referee's own calculator, written from the text, gets the program's L in 994 random steps and 96 threshold tests.
  Mine: 14 + 18 pairs + 10 real leaves. Two evaluators written apart, different test sets, the same finding.
- D: 628 runs, no unexpected verdict. The referee's table D.1 names the same load-bearing rules as my P2 (the precondition of
  the declaration, (T3) "with THAT k", (T4) for corner names, (R2), (T1), (T2)).
- None of the referee's runs uses `--allow-extra-keys` or the partial mode. The referee's "nothing false accepted" is a statement about
  the default options, like mine in P2; the finding of P1 stands beside it.

**The ambiguities the referee names, and the reading of this code.** The referee's list is C.3 (the one new sentence with two
readings), C.4 (thirteen inherited sentences) and table B.7; part F turns them into MUST-1 to MUST-15 with a
proposed wording. **In every row this code reads as the frozen Python checker does**: on all my wx-cert-2 files of
this part the two programs give the same verdict with the same reason, and the candidate gives the same verdict on
the wx-cert-3 copy. Files: P8 (`certs/p8/c..`), P2 (`certs/attack/`), and 65 new cases for the rows I had no file
for (`certs/p6/`, 123 files, built and run by `r30py/r30_p6.py`; with the reasons: `r30py/out/P6_TABLE.md`; as
data: `out/p6_results.json`). "un" = the item stands in a round that is not evaluated, "ev" = in an evaluated one.

| referee | the sentence and its two readings | this code | lines | my files |
|---|---|---|---|---|
| MUST-1 (B-1, C.4) | "an accepted `0` step": must a `0` step have the sense "lo"? The other reading is unsound (a `0` step with sense "hi" and value 0 closes any node) | the sense "hi" on the form `0` is malformed, in every round; a `0` step is accepted iff L >= value > 0 | `parse_round` 1074-1075; `check_step` 2387-2392 | P8 `c02f` ev, un: rejected; `b5_zero_step_value_zero_ev` rejected, `_un` allowed |
| MUST-2 (C.3, B-2) | the last item of WELL-FORMEDNESS: are its two lists complete (reading 1), or is every item of WELL-FORMEDNESS whole-file and only the second list complete (reading 2)? | reading 2, with G^2 + H^2 <= 1 and the affinity of an `ivl` form taken as part of the NAME. Whole file = everything `parse_node` tests (it parses every round); evaluated rounds only = everything `run_round` does | `parse_node` 1154-1209 and what it calls; `run_round` 2488-2508, the `declare_*` functions 1787-1905, `fact_poly` 1946 ff. | whole file (all rejected in un): P8 `c01b`, `c01d`, `c02a`-`c02f`, `c04`; `R01`, `R02`, `R05`-`R09`, `R11`-`R13b`; `a5` (label 01), `a7` (Pk without kappa), `b3` (store rotation not unit), `h5`. Evaluated only (allowed in un, rejected in ev): `a1` (`asg`), `a2` (`opt`), `a3` (`par`), `a4` (`cut`), `a6` (`rarc` and `rarc:..:tan` of a pair without effective relative arc; the referee had not tested this clause at my second reading, the referee's later version has `X4_rarc_*` with the same result), `a9` (`wsup` of a tilted square), `a8` (kappa < 0), `R03` (T3), `R04a`, `R04b` (`ind`), `R10` (`ind` precondition), `b1` (store interval), `b2` (cos > 0 of a proposed endpoint), `b4` (a step that is not accepted), `b5` (value of a `0` step) |
| MUST-3 (C.4; A-2) | "later rounds ... are not evaluated": is the round with the accepted `0` step evaluated completely, or does the evaluation stop at that step? | completely: the later steps and the proposed store of that round are tested and can reject | `run_round` 2488-2508, `_check_node` 2607-2675 | `R14`, `R15`, `R16` |
| MUST-4 (C.4) | alpha > 0, tube alpha <= 1, lo <= hi: at the header for every label, or only where the root or terminal test is made? | at the header, always, also in a tree without a terminal node (and window alpha < 1) | `parse_region` 1229-1234, `parse_header` 1279-1283 | P8 `c06a`-`c06h` |
| MUST-5 (C.4) | may a custom form be the empty sum? | no. A zero coefficient is allowed | `parse_forms` 859-860 | P8 `c05`; `e2` |
| MUST-6 (C.4) | `kappa` "ignored" on P+/P-: anything, or well formed if present? | absent, or a well-formed number string | `parse_round` 1050-1052 | P8 `c07a`-`c07h` |
| MUST-7 (C.4; A13) | "JSON integer": a number token without fraction or exponent, or any number with an integer value? | the token rule. A float literal rejects wherever it stands in the file; a string or boolean is rejected by the type test of the field. Labels inside names and as map keys: no sign, no leading zero. Number strings match `-?[0-9]+(/[0-9]+)?` exactly, ASCII digits only ("-0" and leading zeros are allowed, a sign "+", a blank, a trailing newline, other Unicode digits are not); the same function reads the numbers of `centre` and of a `q:` form | 177-192, 195-209, 267-278, 293-298 | P8 `c08` (25 files); `a5`, `C03`; `h1`-`h12` |
| MUST-8 (C.4) | "(checked)" in 4.2: part of the name, or of availability? | part of the name: whole file | `parse_fact_name` 750-765 | P8 `c01a`-`c01f` |
| MUST-9 (C.4) | may `cuts` have a key for the form `0`? | no; nor is there a `cut` name for it | `parse_store` 997-998; 790-792 | P8 `c04` (4 files), `c02e` |
| MUST-10 (A12) | do the term rules look at the multiplier? | no: (T1) to (T4) for every term, also with the multiplier 0 | `check_step` 2363-2371; the product of every term is formed before its multiplier is used (2092, 2181) | P8 `c03a`-`c03g2`; `R21` |
| MUST-11 (C.4) | may the options of an option split repeat, may it list an excluded option, may an `opt` declaration be repeated? | yes, three times (an `ind` list must be pairwise different, as the text says) | `parse_split` 1115-1123 (no such test), `declare_opt` 1796 (a set); `ind`: 1014-1034 | P8 `c09a`, `c09b`; `e1`; `S15` |
| MUST-12 (C.4) | "equal": the hash as a string or without regard to case; Sref as a string or by value? | hash: string comparison with the lower-case digest; Sref: by value | `parse_header` 1258-1264 | P8 `c10` (2 files); `d1` allowed, `d2` rejected |
| MUST-13 (B-3, C.4) | a node id: any string, or a non-empty one? (the two frozen checkers differ) | a non-empty string: the rule of the frozen Python checker; a JSON number is rejected | `parse_node` 1159-1161 | `c1`, `c3` rejected |
| MUST-14 (C.4) | "JSON lines, or one JSON file per node plus an index" | JSON lines only: the header on line 1, one object per line, at least one node; an empty or blank line rejects, also as the last line; CR LF, a missing final newline and JSON whitespace around an object are allowed; strict UTF-8, a byte order mark rejects; a gzip file is recognised by its first two bytes | 2924-2946, 3035-3048, 3131-3133, 3149 | `f01`-`f14` |
| MUST-15 (C.4) | "a repeated key": after decoding the JSON escapes, or byte for byte? | after decoding (the JSON reader hands decoded keys to the test); every string (name, number, id, schema, a `centre` key) is used decoded | 164-170, 182-186 | `g1`-`g7` |

Remarks on this table:

- The wording the referee proposes for MUST-2 has two lists, (W) whole file and (E) evaluated rounds only. I went
  through both clause by clause: each clause is what this code does (my files of the row MUST-2).
  No clause of MUST-1 to MUST-15 as proposed asks for a change of this code, if MUST-13 is decided as "non-empty".
  Should the lead decide "any string", the edit is to delete lines 1160-1161; I advise against it, because it would
  be the one place where the 3.0 Python checker accepts a wx-cert-2 file that the frozen Python checker rejects.
- MUST-14, gzip. The proposed sentence "A checker may read the same lines from a gzip-compressed file" leaves open
  two things that this code decides (as the frozen one): bytes after the end of the compressed stream reject
  (`f13`), and a file of several gzip members is read as the concatenation of their contents (`f14`, accepted; this
  is the behaviour of Python's `gzip` module, not a choice of the author). If the second checker does otherwise the
  two differ on such a file. No reading can make a false statement accepted. The text should say which (SHOULD 8).
- For information: a node id that contains an unpaired surrogate (the JSON escape `\ud800`, which the JSON grammar
  allows) is accepted by both Python programs with a normal report (`c2`). I do not know what the second checker
  does with it.
- The referee's SHOULD-9 (the RAW RULE is literal: x^2 with x in [-a, a] gets [-a^2, a^2]): this code is literal. My pair
  `X01` is exactly that case (s_1 has an interval around 0, the remainder has + s_1^2): the claim at the literal L
  is accepted, at L + 10^-30 rejected. The referee's SHOULD-6 (the pin on the packing file): P4. The referee's SHOULD-8 ("1 <= k"): the
  name pattern, k is one of the digits 1 to 8 (`R13a`, `h11`).
- Of the referee's list "not examined" (F.5): "the exclusion test inside the `ind` precondition on a store WITH stored relative
  arcs or cuts". I had no such file either (`P01`-`P04` change a box), so I built one: `r30py/r30_excl2.py`,
  `certs/excl2/`. A node whose pair 1-3 has two options that are not excluded on the node's data; round 1 certifies
  and stores the cut A:1:3:hi = c, which excludes (1,3,a,+1) iff c < 1; round 2 declares `ind` (1,3) with the list
  [(3,1,a,-1)]. Accepted with c = 999/1000 and with c = 999999/1000000; rejected with c = 1, rejected when the cut is
  certified but not stored, rejected when the declaration stands in round 1; each rejection names (1,3,a,+1). The
  frozen checker gives the same five verdicts for the declaration `opt` (3,1,a,-1) on the same stores. So the `ind`
  precondition is the test of 4.7 on the start store, cuts included. For stored RELATIVE ARCS it remains by reading:
  `declare_ind` (1886-1903) calls `self.excluded` (1721-1733), the function that `declare_opt` (1793) and the
  closures (2561, 2647) call; its only use of relative arcs is `h_lo` (1703-1719) through `effective` (1523-1541).
  `certs/excl/E1`-`E4` run an `ind` precondition on a store that has relative arc entries, but the verdict does not
  depend on them there.

Loose points of the text that I met myself, and the reading of this code (the first seven are P8):

- A step with an EMPTY list of terms is accepted as a step (Rem = g; file `R17`); so in 2.6.
- A `centre` key is accepted only in its canonical spelling; the same variable cannot be given twice (a repeated key
  is rejected by the JSON reader).
- An `ind` declaration and a `par` declaration of one pair in one round are both valid (`R28`), as 4.10 says.
- The words of two messages (S2) and the report keys: `schema`, `window_centres`, `tube_centres` are written under
  wx-cert-3 only; under wx-cert-2 the report has exactly the keys of the frozen checker. The text has no section on
  reports.

## P7. Verdict

**FREEZE AFTER THE LISTED EDITS.**

The code implements the text. With the default options I found no certificate that the text rejects and the program
accepts, by reading the whole diff and the whole file, by 143 + 89 + 65 test cases of my own (143 + 172 + 123
files) and 39 more files on the exclusion test with cuts, by an evaluator of my own that reproduces the program's L exactly (14 author files, 18 pairs of my own at L
and L + 10^-30, 10 leaves of the real certificate), and by the regression: on wx-cert-2 input the program is the frozen 2.6 checker, report for
report (357 of 358, the 358th is F36). The one wrong acceptance needs the option `--allow-extra-keys`; the option
goes (lead's decision).

MUST, before the file is frozen as `checker/wxcheck_v30.py` (exact edits in P4):

1. **M1**: remove `--allow-extra-keys` and `OPTIONS["allow_extra_keys"]`; `need_dict` always rejects an undefined key.
2. **M2**: gate the two reads of `centre` on the schema at the point of use (lines 1071 and 1221).
3. **M3**: remove the partial mode: `--proto-partial`, `--proto-only`, the verdict PARTIAL, exit code 11, the
   handler that turns any exception in a leaf into an "open leaf".
4. **M4**: the program's identity: docstring, `CHECKER_VERSION`, `SPEC_SHA256` = the SHA-256 of the adopted text,
   argparse description.

After these four the program has the options of the frozen 2.6 checker minus one, two verdicts in full mode (PASS,
FAIL) and NODE-ACCEPTED in node mode, as 2.6.

SHOULD:

1. S1: remove `--proto-report` and its code (P4). It cannot change a verdict, but it threads a parameter through
   the function that computes L, and a frozen checker should not carry prototype code. If the lead wants to keep the
   exact L of every step in the report (the comparison of the two checkers on the 81 leaves, the referee's 994
   steps and my leaves all rest on it), keep it as a documented report option under a neutral name instead.
   Evidence that it does not change a verdict today: the real certificate has the same 153 node entries with it
   (the author's stored report) and without it (my run), and my ten leaves in node mode with it are accepted.
2. S2: the two messages that are wrong under wx-cert-3.
3. S3: the stale docstrings and comments of the first prototype (they describe an exemption the code does not have).
4. S4: `step.centre` instead of `getattr`.
5. S5, for the acceptance script, not the checker: start the checker as `python -I -B`; compare the report's
   `packing_sha256`, `spec_sha256` and, under wx-cert-3, `schema`, `window_centres`, `tube_centres` with what is
   expected; treat every exit code other than 0 as not accepted (after M3 there is no code 11 left).
6. S6, for the text: P8 row 3, last line, and P6: say in the last item of WELL-FORMEDNESS that (T3), (T4) and the
   preconditions are not tested in a round that is not evaluated "whatever the multiplier", if that is the decision;
   and write down the order of events of an evaluated round (referee's A-2), including that an accepted `0` step
   does not end its round.
7. After the edits: the same runs again (358 + 358 swapped, 72, my 143, 89, 65 and 39, the real certificate), and
   the edited file reviewed as a diff against this one. My scripts do it: `r30py/r30_run.py`, `r30_p8.py`,
   `r30_p6.py`, `r30_excl.py`, `r30_excl2.py`, `r30_paranoid.py` take the path of the program in one place (`CAND`
   in `r30_run.py`); `job_big.sh` (the real certificate) and `r30_leaves_job.py` (the leaves; it needs the L of
   `--proto-report`, see S1) name the file directly.
8. S8, for the text (P6, remark on MUST-14): say whether a gzip-compressed certificate is one gzip member with
   nothing after it, or what else; this code rejects bytes after the stream and reads several members as one text.

What I did not examine:

- `checker2/wxcheck2_v30.js` and `checker2/v30/`; the agreement of the two checkers on the real
  certificate is the lead's report.
- The mathematics of the new lemmas beyond what is needed to compare text and code (that is the referee's part A; I
  read it and agree with what I followed).
- Part E of the referee's report was read in an unfinished state (one result still a placeholder). It is about the
  author's notes and the mathematics; it names no reading of the code beyond the rows of P6.
- An `ind` precondition whose verdict depends on a stored RELATIVE ARC: by reading only (P6, last remark). With a
  stored cut it is tested (`certs/excl2/`).
- `PROTO_NOTES.md` sections 0 to 11 and 18; `SPEC_3.0_DELTA.md`; the generator side (`assemble_tree.py`,
  `make_candidate.py`, `make_wxproto30b.py`, the pilot's exporter) and how the real certificate was produced.
- The parts of the file that are the frozen 2.6 checker word for word: read again for context here, reviewed in
  `REVIEW_26.md` part R2, not re-derived.
- `--paranoid` on the real certificate (hours; the author's two attempts were stopped). I ran it on the small files
  only.
- Behaviour on certificates much larger than the real one (memory, time).
- Other Python versions: all my runs used CPython 3.9.6 (the author's too, according to the author's notes).

## ADDENDUM of 9 October 2026: the help option exits with code 0 (edit M5)

Found while reviewing the Node checker (`REVIEW_30_JS.md`, part J4), and true of this file as well. P4 above is left
as it was written; this addendum corrects one sentence of it and adds one MUST.

**The sentence of P4** "`PASS` is printed only for `report["verdict"] == "PASS"`; exit 0 only for that verdict in
mode "full" (3280-3281)" is right about the word PASS and WRONG about the exit code. **Corrected:** exit code 0 has
two sources in the candidate: (1) the verdict PASS of a full run (3280-3281), and (2) the help option of `argparse`:
`ap.parse_args` (3258) prints the help text and raises `SystemExit(0)` when the command line contains `-h` or
`--help`, or an abbreviation of it such as `--he`; nothing of the certificate is read. I had gone through the
options that the file defines and overlooked the one that `argparse` adds by itself.

Test (`r30py/certs/attack/R24_T3_two_options_one_guard.jsonl` is a certificate that the candidate rejects):

| command | first output line | exit code |
|---|---|---|
| `python -B proto30/wxproto30b.py R24...jsonl` | `FAIL` | 1 |
| `python -B proto30/wxproto30b.py R24...jsonl -h` | `usage: wxproto30b.py [-h] [--node ID] ...` | **0** |
| `python -B proto30/wxproto30b.py --help` | `usage: ...` | **0** |
| `python -B checker/wxcheck_v26.py --help` (frozen 2.6) | `usage: ...` | **0** |

So a command line that contains the option, or a certificate whose file NAME is `-h` or `--help`, ends with exit
code 0 and no check. The help text does not contain the word PASS, and no `--json` report is written on this path.
It cannot make the program print PASS; it defeats only a caller that looks at the exit code alone.

**M5 (MUST, in addition to M1 to M4).** Exit code 0 must have one source. In `main` (3229-3232):

```python
class _HelpExit2(argparse.Action):
    def __init__(self, option_strings, dest=argparse.SUPPRESS, default=argparse.SUPPRESS, help=None):
        super().__init__(option_strings=option_strings, dest=dest, default=default, nargs=0, help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        parser.exit(2)

ap = argparse.ArgumentParser(description=..., add_help=False, allow_abbrev=False)
ap.add_argument("-h", "--help", action=_HelpExit2, help="show this help and exit with code 2")
```

`add_help=False` removes the action that exits with 0; `allow_abbrev=False` makes an abbreviated option a usage
error (exit code 2) instead of a silent match. After M5 the exit codes are: 0 = PASS of a full run, 1 = FAIL, 2 =
usage or help, 10 = NODE-ACCEPTED. The edited file should come with command-line tests for it: `-h`, `--help`,
`--he` and a certificate named `-h` must all end with a code other than 0.

**The frozen 2.6 checker** `checker/wxcheck_v26.py` has the same property and cannot be edited. What protects an
acceptance run of 2.6 or 3.0 is the caller: require exit code 0 AND the first output line exactly `PASS` AND a
fresh `--json` report with the verdict PASS and the expected hashes, and pass the certificate as an absolute path.
(The lead reports that the acceptance script does all of this and that the property is noted in
`SPEC_v2.6_ERRATA.md`.) This replaces the last clause of S5 in P7, "treat every exit code other than 0 as not
accepted", which is necessary and not sufficient.

The verdict of P7 is unchanged: FREEZE AFTER THE LISTED EDITS, the list now being M1 to M5.

## P9. The edited file `proto30/wxcheck_v30_candidate.py`, reviewed as a diff (9 October 2026)

Status: DONE. Before the freeze.

| file | SHA-256 |
|---|---|
| `proto30/wxcheck_v30_candidate.py` (3,134 lines; to be frozen byte for byte as `checker/wxcheck_v30.py`) | cf8db52bfa1cc565d8610bf13b279d1b5da2f84c91ce2854d15a3b0a88cd096c |
| `proto30/wxproto30b.py` (the file of P1 to P8) | 55a74437dfac4648155499be4333935fce8f8ce972c6a717cd180909eee8eed7 |
| `SPEC_v3.0.md` (the installed final text) | 0a6dfc2ae10ed6f30a21ebe357a6e73dd7355223c521cc67a3f2bdab9549aba0 |

My own `diff proto30/wxproto30b.py proto30/wxcheck_v30_candidate.py` is kept as
`r30py/CODE_30b_to_v30_candidate.diff`: 76 hunks, 155 lines added, 315 removed; it is byte for byte the author's
`proto30/wxcheck_v30_candidate_vs_wxproto30b.diff`. Line numbers below: old = `wxproto30b.py`, new = the edited
file. Edit labels are those of `proto30/WXCHECK_V30_EDITS.md`: M1 to M4 and S1 to S4 (my P4), M5 (the addendum;
called H there), X1 (two reasons for a `sq`/`pol` name), Z (the report key `zero_step_L`).

### P9.1 The diff, hunk by hunk

**Result: every hunk is one of the listed edits and does nothing else. No test, no formula and no order of
evaluation is changed.**

I did this twice, by two methods that do not depend on each other.

(a) By reading all 76 hunks:

| hunks | old lines | new lines | edit | what | code? |
|---|---|---|---|---|---|
| 1-5 | 4-67 | 4-38 | M4 | the docstring: what the program is, its contract, where it comes from, the marks | text |
| 6 | 84 | - | M3 | docstring line on exit code 11 | text |
| 7 | 117-120 | 87-91 | M4 | `CHECKER_VERSION`; `SPEC_SHA256` = 0a6dfc2a...aba0 | constants |
| 8 | - | 93-97 | M4 | new `_require_spec_hash()`: true iff `SPEC_SHA256` is 64 lower-case hexadecimal digits (`re.fullmatch`) | new function |
| 9, 10 | 128, 130-133 | 105 | M1, S1 | `OPTIONS = {"paranoid": False}` | code |
| 11 | 138-150 | - | S1, M3 | `PROTO_LOG`, `proto_partial`, `proto_only`, `PROTO_NOT_EVALUATED` | code removed |
| 12 | 246-249 | 205-207 | M1 | `need_dict`: the loop over the keys without the `if`; an undefined key always rejects | code |
| 13-16 | 412, 417, 433-437, 613 | 370, 375, 391-394, 570 | S3 | comments and the docstring of `is_equality_fact` | text |
| 17 | 726 | 683-687 | X1 | `sq:NAME` / `pol:NAME`: `if A or B: reject(not defined)` becomes `if A: reject(the NAME must match ...)`, `if B: reject(not defined)`; A = the pattern does not match, B = the form is not defined | code: the same inputs are rejected, with two reasons |
| 18-22 | 893, 896, 898, 927, 1009 | 854-859, 888, 970 | S3 | docstrings and a comment | text |
| 23 | 1035 | 996 | S2 | the list of modes in `need_choice` is `("opt", "par", "ind")` under wx-cert-3 | code: the message only (see below) |
| 24 | 1071 | 1032 | M2 | `sd.centre = parse_centre(...) if (SCHEMA_V3[0] and "centre" in s) else None` | code |
| 25-27 | 1086, 1091, 1180 | 1047, 1052, 1141 | S3 | comments | text |
| 28 | 1221 | 1182 | M2 | `rg.has_centre = SCHEMA_V3[0] and "centre" in x` | code |
| 29, 30 | 1252-1255 | 1213-1216 | S2 | the message for a schema string that is neither of the two | message |
| 31-42 | 1660 to 2177 | 1621 to 2130 | S3 | comments; the block comment on indicators; the docstring of `check_term_rules`; the comment at the availability of a corner name. In hunks 35 and 42 the code lines of the function are the same | text |
| 43, 44 | 2248-2251, 2271-2287 | 2201-2204 | S1 | `lower_bound_centred` without the parameter `info` and without the block that filled it | code (report only) |
| 45 | 2295 | 2231 | S3 | docstring | text |
| 46 | 2350-2355 | - | S1 | `_proto_clock` | code removed |
| 47, 48 | 2364, 2371 | 2294, 2301 | S3 | comments on two code lines; the code is the same | text |
| 49, 50 | 2373-2386 | 2303-2308 | S1, S4 | `check_step`: no report dictionary, no clock; `step.centre is None` instead of `getattr(step, "centre", None) is None`; the call of `lower_bound_centred` without `_info` | code |
| 51-55 | 2491-2508 | 2413-2434 | Z | `run_round` returns a third value: the L of the first accepted `0` step of the round | code (report only) |
| 56-60 | 2591-2671 | 2517-2602 | Z | `NodeResult.zero_step_L`; `_check_node` keeps the value of the first round that has an accepted `0` step | code (report only) |
| 61 | - | 2894-2896 | M4 | `check_certificate` raises `RuntimeError` if `SPEC_SHA256` is not a hash | code |
| 62-65 | 2974, 2986-2992, 2996-3013, 3064 | - | S1 | the step log, its report keys, `_proto_step_entry`, the line hash | code removed |
| 66 | 3085-3108 | 2992 | M3, S1 | `_check_certificate`: the one line `res = check_node(node, ref, header)` again | code |
| 67 | - | 3014-3015 | Z | the report key `zero_step_L` | code (report only) |
| 68-70 | 3151-3157, 3166-3180, 3209-3225 | - | M3, S1 | the verdict PARTIAL, its output, the output of the step log | code removed |
| 71, 72 | 3230-3232 | 3076-3092 | M4, M5 | `_HelpExit2`; `ArgumentParser(..., add_help=False, allow_abbrev=False)`; the description | code |
| 73, 75 | 3246-3257, 3260-3269 | - | M1, M3, S1 | the arguments `--allow-extra-keys`, `--proto-partial`, `--proto-only`, `--proto-report` and their handling | code removed |
| 74 | - | 3107-3110 | M4 | `main` returns 2 if `SPEC_SHA256` is not a hash | code |
| 76 | 3284-3285 | - | M3 | exit code 11 | code removed |

(b) By machine, without reading: I compared the two files as token streams with comments, blank lines and
docstrings removed (Python's `tokenize` and `ast`; script `r30py/r30_p9_tokens.py`, output
`r30py/out_v30cand/tokens_compare.txt`). Result: **47 changes of code tokens (indentation counted), each inside
one of the code hunks of the table**; and
of the 156 functions of the old file, 141 have an identical syntax tree in the new file (docstrings ignored), 2
are gone (`_proto_clock`, `_proto_step_entry`), 3 are new (`_require_spec_hash`, `_HelpExit2.__init__`,
`_HelpExit2.__call__`), and 13 differ: `need_dict` (M1), `parse_fact_name` (X1), `parse_round` (M2, S2),
`parse_region` (M2), `parse_header` (S2), `RoundEnv.lower_bound_centred` (S1), `check_step` (S1, S4), `run_round`
(Z), `_check_node` (Z), `check_certificate` (M4, S1), `_check_certificate` (M3, S1, Z), `format_report` (M3, S1),
`main` (M1, M3, M4, M5, S1). So every function that computes a bound, a fact, a store bound, an exclusion, a
store update, the terminal test, the root test or a tree rule is unchanged token for token: `remainder`,
`remainder_streaming`, `lower_bound`, `centred_remainder`, `centred_interval`, `lower_bound_reference_centred`,
`fact_poly`, `check_term_rules`, `declare_opt`, `declare_par`, `declare_ind`, `ind_poly`, `excluded`, `accept_store`,
`terminal_failure`, `root_failure`, `split_failure`, the class `TreeChecker`, the JSON reader and the number
parser among them.

Three hunks deserve a sentence.

- Hunk 23 (S2). `need_choice(d["mode"], ..., ("opt", "par", "ind"))` could look as if the mode "ind" were now let
  through to the code for `par` declarations. It is not: under wx-cert-3 a declaration whose mode is the string
  "ind" is taken by the branch above (new line 975, `if SCHEMA_V3[0] and type(d["mode"]) is str and d["mode"] ==
  "ind":`), which ends with `continue` (995); so the value "ind" never reaches line 996, and the longer list
  changes only the words of the rejection of a wrong mode. Under wx-cert-2 the list is the frozen one.
- Hunk 17 (X1). Old: reject iff A or B. New: reject if A, then reject if B. The set of rejected names is the
  same; only a name with a malformed NAME now gets the reason of A.
- Hunk 66 (M3). The line stands again where the frozen 2.6 file has it, inside the `try` of the node loop, so a
  rejection of a node is again a failure of the certificate and nothing else.

One remark, no edit needed: the docstring's list of exit codes (new lines 52-56) says "2 command-line usage
error"; help and a missing `SPEC_SHA256` also end with 2 (they are in `WXCHECK_V30_EDITS.md`).

### P9.2 The edit Z, the report key `zero_step_L`

`run_round` (new 2410-2434): `zero_L = None` before the loop over the steps; for a step that `check_step`
reports as an accepted `0` step: `if not zero: zero_L = L`, then `zero = True`. So `zero_L` is the L of the FIRST
accepted `0` step of the round; later `0` steps of the same round do not change it. `_check_node` (2534-2604):
`if zero and not zero_step: zero_step_L = zero_L`, then `zero_step = zero_step or zero`, and the loop over the
rounds is left at once when `zero_step` is true. So a value is taken from exactly one round, the first that has
an accepted `0` step, and no later round is evaluated.

- Can it be the L of another step? No: `check_step` returns `(L, True)` only at its line `return L, True`, after
  the test `L >= value > 0` on the form `0` (new 2309-2315), and that L is the number the acceptance was decided
  with (raw or centred rule, new 2305-2308). There is no second computation of it.
- Can it be written for a node that is not closed by a `0` step? No: the key is written only `if res.evidence ==
  "0-step"` (3014), and `evidence` gets that value in one place (`_check_node`: close kind "infeasible", no
  `pair`, `zero_step` true). A terminal or split node that contains an accepted `0` step, and a node closed with
  `pair`, get no key. When the evidence is "0-step", `zero_step` is true, so `zero_step_L` is not None.
- Is the string exact? Yes: L is a `Fraction`; `num_str` (new 172-175) writes numerator and denominator of the
  reduced fraction in full ("p" if the denominator is 1). No float is involved.
- The rule is the same as in the Node file (key present iff the close object is `{"kind":"infeasible"}` without
  `pair` and the node has an accepted `0` step; the value is that of the first such step).
- The key is written under both schemas. So under "wx-cert-2" the report of this file now differs from the
  frozen 2.6 report by this key (and by the values of `checker` and `spec_sha256`), where the file of P1 to P8
  differed by `checker` alone.

### P9.3 Every exit, against the code

`SystemExit` can arise in three places only (searched: `SystemExit`, `sys.exit`, `os._exit`, `exit(`, `quit(`):
`parser.exit(2)` in `_HelpExit2` (3085), argparse's own `parser.error` (code 2), and `sys.exit(main())` (3134).
`main` (3088-3130) returns: 2 if `SPEC_SHA256` is not a hash (3107-3110); else `code`, which is 1 from the start
(3112), 0 only under `report["verdict"] == "PASS" and report["mode"] == "full"` (3122-3123), 10 only for
NODE-ACCEPTED in node mode (3124-3125), and 1 again after any exception (3126-3129). The verdict PASS is set in
one place, the last line of `_check_certificate` (3037), after every line was read, every node accepted, the tree
pass done, and never in node mode. This is the table of `WXCHECK_V30_EDITS.md`, row by row; I found no exit
that it does not list.

My own command-line cases (`r30py/r30_p9.py cli`, run with `python -I -B`, results `out_v30cand/cli_results.json`):

| case | exit code | first output line |
|---|---|---|
| a certificate that passes (also with `--paranoid`, `--keep-going`, `--json FILE`; also the same file under the name `-h`, given as `./-h`) | 0 | `PASS` |
| a certificate that fails (also with `--paranoid`, `--keep-going`) | 1 | `FAIL` |
| `-h`, `--help`, alone, before or after a certificate, with a passing or a failing one | 2 | `usage: ...` |
| a certificate file named `-h`, given as `-h` | 2 | `usage: ...` |
| abbreviations `--he`, `--no-pack`, `--para`, `--keep` | 2 | (nothing on standard output) |
| removed options `--allow-extra-keys`, `--proto-partial`, `--proto-only FILE`, `--proto-report`; `--version`; no argument; two certificates; `--json` without a value | 2 | (nothing) |
| `--json` into a folder that does not exist, on a passing certificate | 1 | `FAIL` |
| `--node ID` on an accepted node (alone, and in a tree of three nodes) | 10 | `NODE ACCEPTED (...)` |
| `--node` with an id that does not exist; `--node` on a node that is rejected | 1 | `FAIL` |
| packing file missing; another packing file (pinned); another packing file with `--no-packing-pin`; `--expect-packing-sha256` with a wrong value; certificate missing; certificate is a folder | 1 | `FAIL` |

37 cases, all as expected. **Exit code 0 occurs in five of them, each a full run with the verdict PASS; a line
`PASS` is printed in exactly those five.**

### P9.4 Reruns with CAND = the edited file

In every run the programs were started as `python -I -B` (job scripts
`r30py/job_big_v30cand.sh`, `job_v30cand.sh`; results in `r30py/out_v30cand/`; the earlier results for
`wxproto30b.py` stay in `r30py/out/`). For the comparison with the frozen 2.6 checker the reports are compared
without `checker`, `seconds`, `certificate` as before and now also without the value of `spec_sha256` and the
key `zero_step_L` of a node entry, the two things the edited file changes under both schemas.

| run | files | result |
|---|---|---|
| 2.6 corpus `checker/v26/testcerts`, frozen checker against the edited file | 358 | reports and exit codes identical in **357**; the 358th is `fail/F36.jsonl` (expected). Frozen 44 PASS, 314 FAIL; edited file 45, 313 |
| the same files with the schema string changed to "wx-cert-3" | 358 | identical in **357**; the 358th is F36 |
| the author's `proto30/testcerts30` | 72 | all 72 verdicts and all 72 reasons as in the author's INDEX.json (14 PASS, 58 FAIL); the 8 wx-cert-2 files give identical reports with the frozen checker |
| my attack files | 143 | all 143 as expected (43 PASS, 100 FAIL), every rejection for the planted reason |
| P8 (the lead's ten corner cases) | 89 cases, 172 files | all as decided, frozen checker and edited file |
| P6 (the referee's ambiguity rows) | 65 cases, 123 files | all as the reading of the frozen checkers; same reason from the frozen checker and the edited file in every wx-cert-2 file |
| exclusion with cuts | 22 + 17 | as before (10 + 5 wx-cert-2 files identical with the frozen checker) |
| `--paranoid` against default, on the wx-cert-3 files of all the above and the author's 72 | 386 | the same verdict and the same report in all 386 (107 PASS, 279 FAIL) |
| my command-line cases (P9.3) | 37 | all as expected |
| the real certificate `proto30/out/tree3/c01/G20S_v3_c01.jsonl.gz`, ONCE, `--json` | 1 | **PASS**, exit 0, 539.3 s, 307 MB; `certificate_sha256` 989e9738...8273, uncompressed f678f75a...da58; 153 nodes accepted (81 infeasible, 71 split, 1 terminal), 81 steps, 1,614,692 terms. Report: `r30py/out_v30cand/G20S_v3_c01.<reviewer>.v30cand.report.json` |

Against the run of the same files with `wxproto30b.py`: over all my files the verdict changes nowhere, and the
REASON text changes in 7 files, all by edit S2 (six files with a third schema string: "header: schema is neither
'wx-cert-2' nor 'wx-cert-3'"; `S14`: "... is not one of ('opt', 'par', 'ind')").

**The real certificate** (`r30py/r30_p9.py big`, output `out_v30cand/run_r30_p9_big.txt`):

- All 153 node entries (line, closure, evidence, rounds, steps, digest of the final store) equal those of my run
  with `wxproto30b.py`; every other report key is equal apart from `checker`, `spec_sha256`, `seconds`.
- `zero_step_L` stands in 81 entries, exactly the 81 nodes closed as infeasible with the evidence "0-step";
  every one is written in lowest terms, all are > 0 (smallest 9.39e-4, largest 4.39e5; denominators of 1,158 to
  1,170 digits).
- Compared AS RATIONALS: equal to the L of my own evaluator for the 10 leaves I had computed (P5); equal to the L
  of the author's stored report (`complete.report.json`, made with `wxproto30b.py --proto-report`) for all 81;
  equal to `zero_step_L` of the Node checker's report `checker2/v30/out/c2_big_first.json` for all 81 (there the
  strings are equal too).

### P9.5 Verdict on the edited file

**Freeze cf8db52bfa1cc565d8610bf13b279d1b5da2f84c91ce2854d15a3b0a88cd096c as it stands.**

The MUST list of P7 and of the addendum (M1 to M5) is done, S1 to S4 are done; the two extra edits (X1, Z) change
a reason and add a report key and nothing else. Open, none of it a reason to wait: the docstring line on exit
code 2 (P9.1, last remark); S5 to S8 of P7 concern the acceptance script and the text, not this file.

Not examined in this part: nothing new was read outside the diff; the 141 functions that are token for token
the old ones were reviewed in P1 to P3 and are covered here by the comparison of P9.1 (b) and by the reruns.
`--paranoid` on the real certificate was again not run.
