Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line.

# Review of six records of accepted region trees (batch 2, 2026-10-10)

Reviewer: a reviewer of the window side that wrote none of the six records, of the certificates, of
the checkers or of the tools. Texts reviewed: the copies in
`reviews/join_roots/batch2/as_reviewed/` (sha256 below); the six records on disk still had these hashes at 08:15.
Paths are relative to `research/window-extension-20261008/`; paths that begin with `cloud/` or `results/` are
relative to `local-research/claude-20261002/`.

    63dcdcf63cea7d2e76951c5ae4bbec2bee68cff4e8aa30f4471a7a7a5ee6217c  RECORD_EJG_v2.md
    946e380abe9e0bd74cd961d6e5fd29abebeed9e01e29686983ef5c99825dc56d  RECORD_EJPG17m_v5.md
    274ec4fea50876e1a2a483e100567278c81a52caf10c429b759b7889d1046c3d  RECORD_EJPG17p_v5.md
    2add0b2f61345b597b2d41ee0d6b1e8c616bac25c92bc805fc6eb08bd4c2210e  RECORD_EJPG3m_v5.md
    96f763ddb84ebf52df49c054c6fb88d12ede07ad257aa0f621fb5b79f706cfae  RECORD_EJPG15p_v5.md
    bf4735481f059915fe4d3888c72c946e0a08ff1dccab8475cb6bb180d39ffe3c  RECORD_EJPG3p_v2.md

## Verdicts

| # | record | statement | may it be called PROVED |
|---|---|---|---|
| 1 | `RECORD_EJG_v2.md` | (T_JG, v2), tube statement | **yes after the listed corrections** (finding 1 is a condition; finding 2) |
| 2 | `RECORD_EJPG17m_v5.md` | (E_JPG17m, v5) | **yes after the listed correction** (finding 3) |
| 3 | `RECORD_EJPG17p_v5.md` | (E_JPG17p, v5) | **yes after the listed correction** (finding 3); this is the v5 record taken in depth |
| 4 | `RECORD_EJPG3m_v5.md` | (E_JPG3m, v5) | **yes after the listed correction** (finding 3) |
| 5 | `RECORD_EJPG15p_v5.md` | (E_JPG15p, v5) | **yes after the listed correction** (finding 3) |
| 6 | `RECORD_EJPG3p_v2.md` | (E_JPG3p, v2) | **yes** |

All corrections are corrections of wording. No number of an Evidence table or of a table of leaves is wrong, no
hash is wrong, and nothing was found against a certificate, an acceptance run, the terminal leaf, the two
helper-window leaves or the record generator's numbers: 741 checks in seven script runs, none failed. Nothing
was found that touches all trees. For every record the word PROVED must carry the limits sentence of finding 4.

## Findings, sorted by weight

### 1. `RECORD_EJG_v2.md`, Statement: the direction condition of the tube is written with the sine; the tube is a bound on the ANGLE

- The record says: "... and the sine of the angle of a_i from the reference direction of label i is at most 1/10
  in absolute value. This is the window G20S of `bigbox/THEOREM_G20S.md` for the sixteen labels".
- I found: SPEC 3.0 section 8 defines a tube by an angle radius: a configuration lies in it iff every
  a_i = R(phi_i) gamma_i u_i with |phi_i| <= alpha_i (here no centres, gamma_i the identity, alpha_i = 1/10, for
  label 4: 1). `THEOREM_G20S.md` section 2 defines G20S the same way: "|phi_i| <= 1/10 for all sixteen". So what
  the corollary gives, and what THEOREM G20S needs, is |phi_i| <= 1/10 rad. The set the record describes is
  LARGER: "sine at most 1/10" admits angles up to asin(1/10) = 0.100167 rad (and, read literally, directions near
  the opposite one). The sentence as written is therefore true but weaker than what is proved, it is not the
  window G20S, and with it the hypothesis of THEOREM G20S would not be met. The sine belongs to the TESTS, not
  to the tube: the root test compares the sine of the root's arc end with the window radius, and the terminal
  test demands |sin| <= alpha - alpha^3/6 (= 599/6000 here), which implies |angle| <= alpha.
  The certificate proves the angle form: the one terminal node has every arc end of the sixteen labels within
  0.099916791 rad of the reference direction (exact enclosures; sines at most 40/401 = 0.099750623 against
  599/6000 = 0.099833333). Everything else in the Statement is right: the three special box entries
  (xi_(2,1) in [-39/125, 0]; xi_(13,2) in [-1/5, 28/125]; label 4: its root box
  [-124983/500000, 49987/200000] x [-1/1000000, 124983/500000], radius 1) are the header's `terminal` entry, which
  equals the statement file's `tube` and the region file's `terminal`; the header tube has no centre map, so
  "from the reference direction" is right; "no condition" for label 4 is right (the hypothesis already puts a_4
  within 0.786228 rad < 1 and the box is the root's).
- How checked: reading of SPEC 3.0 sections 2, 7, 8, 11 and of `THEOREM_G20S.md` section 2; `t_tree.py`,
  output `t_JG_v2.out` (parts "header" and "terminal nodes").
- Correction asked: replace the clause by "and the angle phi_i from the reference direction u_i to a_i
  (a_i = R(phi_i) u_i, SPEC 3.0 section 8) satisfies |phi_i| <= 1/10 rad". The same wording stands in
  `acceptance/mk_record.py` (the text of the TUBE branch): correct it there too.

### 2. `RECORD_EJG_v2.md`, "What the statement is used for", first point: the sentence with THEOREM G20S names the wrong source for "has side S*", and no frame

- The record says: "With THEOREM G20S it gives: a packing of side at most S* that lies in the region JG v2 has
  side S* and lies on the three-slider family (`JOIN_ROOTS.md` section 3, the LOCAL THEOREM; not proved here)."
- I found: the LOCAL THEOREM of `JOIN_ROOTS.md` section 3 is about seventeen squares K in [0, S*]^2 (the endpoint
  placement of section 2.1, which is the frame the region file itself names) and concludes only that the sixteen
  squares other than 4 lie on the family. "Has side S*" is not in it: for the endpoint placement it is a further
  step of the composition (case G: on the family label 8 touches two walls; a statement of Codex, not proved).
  For a packing of side S <= S* read with its own container corner at the origin (the frame of this record's
  Statement and of `THEOREM.md` section 1) the sentence does follow, directly from (T_JG, v2) and THEOREM G20S,
  whose conclusion is "S = S* and the sixteen squares on the family"; then nothing of section 3 is needed. The
  sentence mixes the two. It is the sixteen squares other than 4 that lie on the family.
- How checked: reading of `JOIN_ROOTS.md` sections 2.1 and 3, `THEOREM_G20S.md` sections 1 to 3, `THEOREM.md`
  section 1 (frame: container corner at the origin; phi_i the quarter-turn representative of smallest absolute
  value, which the chosen a_i is once |phi_i| <= 1/10).
- Correction asked, for example: "With THEOREM G20S it gives the case-G line of the LOCAL THEOREM (form) of
  `JOIN_ROOTS.md` section 3: seventeen squares in [0, S*]^2 that lie in the region JG v2 have their sixteen squares
  other than 4 on the three-slider family. For a packing of side S <= S* with its own container corner at the
  origin THEOREM G20S also gives S = S*. In the endpoint frame of the join design, S0 = S* is a step of the
  composition (section 3, case G), which is not proved here."

### 3. The four v5 records, "The region in words": label 11 is in the HULL of the two targets, not in their union

- The records say: "**label 11 in the union of its old target PB_11 and its new target HULLW_11** (tag v5:
  xi_(11,1) in [-140801/1000000, 12647/62500], direction in [-0.137499811, +0.204999690])".
- I found: the numbers are right. The factor of label 11 is one box and one arc: the box is the union interval
  by interval of the old root's box and HULLW_11's box, the arc runs from HULLW_11's lower end to the old root
  arc's upper end (`JOIN_ROOTS.md` section 11.1 and `ADMISSION_v4.md` section 9 both say "hull"). That is more
  than the union of the two targets, so the words describe a smaller region than the one that is proved empty
  (the safe side; the Statement itself names the file and is not affected).
- How checked: `v_regions.py`, `v_regions.out` parts A and D.
- Correction asked: "label 11 in the hull of its old target PB_11 and its new target HULLW_11 (one box, one arc;
  it contains both)". The text is in `mk_record.py` (variable `regw`).

### 4. All six records, with the change of status: the sentence on limits

When "ACCEPTED, review deferred" becomes PROVED, the status line should say what the word rests on:
- for all six: the soundness of SPEC 3.0 and of the two frozen checkers is taken from their own reviews
  (`reviews/REVIEW_30*.md`), and with it the exact values L of the `0` steps (this review compared them across the
  producer's and the acceptance reports of both programs and did not recompute them); nobody but the producer has
  read how the leaves were made (not needed: the certificate is checked, not the way it was made); it is a
  statement about the numbers of the region file, not about a case of the proof;
- for the v2 region files (records 1 and 6): the region file against the class files is taken from
  `reviews/join_roots/REVIEW_JOIN_ROOTS_V2.md`;
- for the v5 region files (records 2 to 5): outside label 11 they are the reviewed v2 files (exact comparison in
  this review); for label 11 this review checked that the factor contains the v2 factor, the old target PB_11 and
  the new target HULLW_11 (`batch2/v_regions.out`); the v5 generator and `cmp_v5.py` are not reviewed;
- for record 1 in addition: the ruling that a leaf may be larger than the root (`LEAF_HELPERS.md`) was read and
  confirmed in this review (finding 5); THEOREM G20S is taken from its own record; the composition of
  `JOIN_ROOTS.md` section 3 is not proved.

### 5. Not a condition. `LEAF_HELPERS.md` (the ruling) and the record's paragraph on the two helper-window leaves: right and complete

- Is there a condition that a node other than the root lies inside the root or inside the header window? No.
  SPEC 3.0: section 2 (F(N) is defined by the node's own data), section 6 (a child must CONTAIN its piece and
  "takes nothing else from N"), section 7 (closing, tree and root conditions; the induction of the THEOREM uses
  F(N) empty, the terminal test, and covering, never F(child) inside F(parent)), section 8 (the window enters
  only in ROOT CONTAINS WINDOW). The two corollaries of `SPEC_v3.0_NOTES.md` use that induction only. Python
  checker: `header.window` occurs in `root_failure` and in the report, nowhere else; `child_failure(par, child,
  index)` has no header. Node checker: `header.window` occurs in `checkRoot` and in the report;
  `checkChild(P, C, l)` has no header. So the ruling's point 1 holds, and a leaf larger than the root proves the
  emptiness of its own larger node.
- The numbers of the record's paragraph are right: node `ne99e545db0` is the sliver (label 13 from the root's
  lower end -0.099999887576 to rot(-1/20), 8.31e-5 rad wide), an option split of the pair (14, 17) with the two
  options named; its six omitted options are excluded in my implementation of SPEC 3.0 section 4.7 (margins
  0.0506 to 1.7834); the two leaf nodes have label 13 in [-0.120062903, -0.099911074], that is 2.0063e-2 rad
  below the root's end, and 6.498e-6 rad above the root's upper end of label 12; in no other label and in no box
  interval do they leave the root; each contains its piece (my child test) and assumes its option; both
  acceptance reports and both producer's reports accept them. "All 56 leaf nodes reach beyond the root in some
  arc": yes, by 4.257e-6 to 6.498e-6 rad; apart from the two helper leaves nothing exceeds 1e-5 rad, and no
  node exceeds the root in a box interval. "21 leaves of JPG3p v2": yes. "The certificate does not name the
  helper file": no line of it contains `LEAFHELPER` or `13low_v1` (the two node ids carry the letters
  `JGH13low`).
- `LEAFHELPER_JG_13low_v1.json` (1689a9e8...) is `JG_exact_v2.json` with the root arc of label 13 changed and
  nothing else of S, window, terminal or the sixteen other arcs; its arc of label 13 is
  [-0.199337304984, +0.199999917014], as `LEAF_HELPERS.md` says (`w_helper.out`). Not looked at: the test
  `proto30/out/v4reuse/` of the ruling's point 2.

### 6. Remarks, no change needed

- (a) Units. The five generated records give the resident sizes in binary units under the names MB and GB
  (790,085,632 bytes as "753 MB", 1,554,497,536 as "1.45 GB"); record 6 uses decimal units ("708 MB" for
  707,837,952 bytes). Both are right in their unit.
- (b) "ABOVE its gate, [+0.099917, ...]" and "BELOW its gate, [..., -0.099917]": the root arc ends 9.3e-10 rad
  inside the gate (label 17 in JPG17m / JPG17p, label 3 in JPG3m / JPG3p, label 15 in JPG15p). The region is that
  much larger: the safe side, as in the reviewed record of JPG17m v2. "Inside its gate" is exactly rot(-1/20) to
  rot(1/20) for the labels 3, 15, 17; "any direction" is exactly rot(-4147/10000) to rot(4147/10000).
- (c) `acceptance/JPG3p_v2_facts.out` (03:06) was written by the earlier version of `region_facts.py` and has no
  list of nodes beyond the root; the "21" that record 1 and `LEAF_HELPERS.md` quote is confirmed by my own count.
- (d) The last point of the four v5 records says the v5 files are "not reviewed by a helper". After this review
  it can say what finding 4 says for the v5 files.
- (e) Record 1 says it has "the form of `RECORD_EJPG17m_v2.md`, which was reviewed"; the TUBE form of the
  Statement is new with this record.
- (f) My own slip: a loop without word splitting started the slot wrapper four times with a wrong tag. It left
  eight files `proto30/out/contain/rev2_JPG... RECORD_....md_.stdout` / `.stderr` (names with blanks; empty or a
  usage error) and four lines with exit 1 in `proto30/out/contain/runs.jsonl`.

## Confirmed

On the logic. (T_JG, v2) is the conclusion of the COROLLARY (root region) for the root's data written as the
region file, with section 11 for S <= Sref; its hypotheses are what the log shows: both frozen checkers, default
options, exit 0, PASS on the whole file; root node = region file; header tube = the statement file's tube. The
statement file leaves `terminal_leaves` open (null, "not fixed by the statement"), which is right for a tube
statement: the corollary does not depend on how many nodes are closed as terminal. The five emptiness statements
are the EMPTINESS COROLLARY as in the reviewed record of JPG17m v2; each statement file demands 0 terminal
leaves and each tree has none.

The same script (`t_tree.py`, the earlier reviewer's `b_cert.py`, `c_leaves.py`, `g_exclusion.py`, `i_passes.py`
and `a_hashes.py` made into one program with parameters; added: box splits, terminal nodes, nodes against the
root, every option split) ran on all six certificates, each read line by line:

| region | checks | nodes: splits (arc, box, option), leaves, terminal | children tested | option splits tested | nodes beyond the root (largest excess) |
|---|---|---|---|---|---|
| JG v2 | 131 | 113: 56 (21, 7, 28), 56, 1 | 112 | 28 | 56 (2.0063e-2 rad, the two helper leaves; else 6.498e-6) |
| JPG17m v5 | 115 | 31: 13 (11, 0, 2), 18, 0 | 30 | 2 | 18 (6.112e-6) |
| JPG17p v5 | 117 | 48: 16 (9, 0, 7), 32, 0 | 47 | 7 | 32 (6.112e-6) |
| JPG3m v5 | 116 | 36: 14 (9, 0, 5), 22, 0 | 35 | 5 | 21 (5.260e-6) |
| JPG15p v5 | 114 | 23: 8 (5, 0, 3), 15, 0 | 22 | 3 | 14 (6.112e-6) |
| JPG3p v2 | 103 | 36: 14 (9, 0, 5), 22, 0 | 35 | 5 | 21 (5.260e-6) |

For each of the six (outputs `t_<region>_<tag>.out`):
- size, sha256 and stream hash of the certificate; every other hash the record gives (statement file, log, C1,
  C2, facts output, description, `run.json`, the three frozen files, `hull_tree.py`); no hash string of a record
  is left unexplained;
- header: schema, 17 labels, Sref = S_floor, packing hash; header window and tube = the statement file's;
- counts (nodes, depth, splits by type, leaves, steps, terms, declarations) from my own reading, equal to the
  record, to C1, to C2 and to the assembler report; every leaf has one round with one `0` step of positive value;
  no split or terminal node has a round;
- tree conditions of SPEC 3.0 section 7; root node = region file (side interval, 68 box ends, 51 rotations);
  root contains the header window; the certificate's tree = the producer's description; no `recentre`;
- every cut as the record words it (arc cuts as tan-half from the reference direction; box cuts; option splits
  by pair and number of children);
- child test of SPEC 3.0 section 6 for every edge (my code): all pass; the split nodes and the terminal node are
  exactly their pieces; every leaf is larger than its piece, in arcs only;
- every option split: all omitted options excluded on the node's own data (SPEC 3.0 section 4.7 written from the
  text; smallest margin 0.0506 in JG, between 0.1302 and 0.9527 in the five other trees), including the nested ones of JPG17p v5 (pairs
  (4, 14) with five children, (4, 6), (3, 4), (12, 15));
- every split node has the root's centres; label 11: never cut and the root's box and arc in every node (five
  emptiness trees); cut twice in JG, as its record says;
- both acceptance reports: PASS, the certificate's hashes, every node accepted, closure kinds and line numbers
  as in the file, final store hashes recomputed from the file for every node in each program's own format; the
  producer's two reports agree with them node by node (closure, final store hash, evidence, L);
- the table of leaves, every row (leaf, file hash, terms from my own count, L to seven places, sha256 of L,
  options, order); L the same string in C1, C2 and the assembler report, its hash in `run.json`; terms add up;
- the log: every hash it names against the disk, default options, exit codes, RESULT: ACCEPTED, the lines that
  carry the statement, start time, the two times and sizes.

Record 1 in addition:
- the terminal node `td0f7ae2afe` (line 72, depth 28, first child of the box split of xi_(17,2) at 1/5, no
  assumption, no round): my own terminal test of SPEC 3.0 section 8 passes on its data (box in the tube box in all
  68 ends; smallest slack in sine 8.27e-5), and every arc end is within alpha of the reference direction by exact
  enclosure of the angle; both acceptance reports: accepted, closure terminal, no round;
- header tube = the region file's `terminal`; the tube against `THEOREM_G20S.md` section 2 (by reading);
- the helper leaves and the helper file (finding 5; `w_helper.out`).

Records 2 to 5 and 6 in addition (`v_regions.py`, `v_regions.out`, 45 checks):
- each v5 file against its v2 file (also JPG3p): side interval, box and arcs of the sixteen labels other than 11
  equal; label 11 of v5 contains label 11 of v2; its lower end of xi_1, its xi_2 and its upper arc end are the v2
  file's numbers; v5 is larger by 46247/1000000 in xi_(11,1) and by 3.749992e-2 rad at the lower arc end; all ten
  hashes stand in the tables of `JOIN_ROOTS.md`;
- label 11 is the same data in the five v2 files and in the five v5 files (record 6's claim);
- "the region in words" of all six records, number by number (the classification of `mk_record.py` gives the
  right words; remark 6b);
- the targets: for k = 3, 15, 17 the class PB_j is the same data in PT_j, PM_j, PS_j^k and PSS_j^k for all twelve
  rigid labels, and the class HULLW_11 the same in PTW37_L11, PSW37_L11_Tkk and PSSW37_L11_Tkk; all files have
  the hashes of their folders' pin lists; one k per root as the records say (`ADMISSION_v4.md` section 9);
- my own transport (`JOIN_ROOTS.md` section 2.2): the v5 factor of label 11 contains PB_11 (room 6.3e-7 in the
  box) and HULLW_11 (room 9.5e-7 in the box, 5.1e-13 rad below, 7.2e-11 rad above); the v2 factor contains PB_11
  and not HULLW_11;
- record 6: the cells of its five option splits, the cut at tan-half 563/2500 = +0.443010 rad under the option
  8:17:b:m, the producer's times, "12 checks".

`acceptance/region_facts.py` and `acceptance/mk_record.py` were read once. I found no flaw that makes a number
wrong: every number they put into a record was compared with my own. The two texts to correct in the generator
are those of findings 1 and 3. `h_report30.py` in use (0314aa1f...) is the version proposed and tested in
`reviews/REVIEW_30_ACCEPT.md`; the same two acceptance scripts made all six logs.

## Limits

Not checked by me:
- The two frozen checkers were not rerun and the acceptance script was not rerun. The arithmetic
  of the 165 `0` steps, that is the exact values L, is the checkers'. Of the checkers' tests I wrote again: tree
  and root conditions, the child test, the exclusion of an option, the terminal test. Nothing about rounds and
  steps.
- The leaf files: only their hashes as the producer's reports give them. How the leaves, the description and the
  certificates were made: not read (`regiontree.py`, `hull_tree.py`, the exporter, `mk_leafhelper_JG13low.py`).
- THEOREM G20S, its chain and the terminal theorem: taken from `bigbox/THEOREM_G20S.md` (status PROVED there).
- Nothing of the capture side: no class statement, not the composition of `JOIN_ROOTS.md` sections 3 and 9.3,
  not "none certified".
- `cmp_v5.py` and the v5 generator: not read, not run. In part D of `v_regions.py` the enclosure of S* is taken
  from the region file's `constants`, the frame rule and the rule for directions from `JOIN_ROOTS.md` sections
  2.2 and 2.4.
- The three v5 records other than JPG17p were read as differences from it; their trees had the full script.

Taken from earlier reviews: the soundness of SPEC 3.0, of the two corollaries' ingredients and of the two
checkers (`reviews/REVIEW_30*.md`); the acceptance scripts (`reviews/REVIEW_30_ACCEPT.md`); the v2 region files
against the class files (`reviews/join_roots/REVIEW_JOIN_ROOTS_V2.md`); the earlier reviewer's library
`rjlib.py` and that reviewer's tests, which I copied and extended (`reviews/join_roots/REVIEW_EJPG17m_v2.md`).

How the work was done: the six runs that read a certificate went
through `proto30/out/contain/run.sh` (tags `rev2_JG_v2`, `rev2_JPG17m_v5`, `rev2_JPG17p_v5`, `rev2_JPG3m_v5`,
`rev2_JPG15p_v5`, `rev2_JPG3p_v2`; 37 to 67 s each, at most 536 MB); standard library only, exact comparisons
with fractions, floats only for printing.

sha256 of my scripts and outputs (`reviews/join_roots/batch2/`):

    04622c7f42ab1fe3...  t_tree.py          727ecbed27cb4e43...  v_regions.py       1ecc5cea24fa7c50...  rjlib.py (copy)
    31b246eaa14dfeda...  t_JG_v2.out        0533ba5199ea815e...  t_JPG17m_v5.out    3ddde1a1b5238e8e...  t_JPG17p_v5.out
    dd0d06134ac18412...  t_JPG3m_v5.out     be4f7714eeec8011...  t_JPG15p_v5.out    5e1e471dd39d42f0...  t_JPG3p_v2.out
    cd18e4bcb3ef3ea1...  v_regions.out      5b1867e1538d3438...  w_helper.out
