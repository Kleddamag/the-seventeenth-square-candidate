Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line. This record refers in passing to the working folder of the computation that produced its certificate, named here by a neutral designation (table EARLIER_EXECUTIONS.tsv).

# Record: statement (E_JQ) for the region JQ v1 ("the region JQ v1 is empty"): ACCEPTED 2026-10-09 18:06, PROVED 18:38

Lead of the window side. Status words as in `bigbox/THEOREM_G20.md`: COMPUTED / PROVED.

**STATUS: PROVED (2026-10-09 18:38) as a statement about the numbers of the region file** (status words of
`bigbox/THEOREM_G20.md`): the certificate is accepted by both frozen checkers with the lead's post-check (18:06),
and this record is reviewed by a reviewer that wrote none of it (`reviews/join_roots/REVIEW_JOIN_ROOTS_V2.md` part
G7, sha256 9ac387300a880a0f...: every number confirmed, its own comparison of the certificate with the region
file, its own acceptance run `acceptance/ACCEPT_REVIEW_JR_JQ_v1_jQTwn0.log` with the same result; verdict: may be
called PROVED once the wording of its finding S2 is in, which this version has).
Limits, as the reviewer states them: the soundness of SPEC 3.0 and of the two frozen checkers is taken from their
own reviews (`reviews/REVIEW_30*.md`); nobody but its producer has read the export chain (not needed: the
certificate is checked, not the way it was made). **This is NOT the statement "case Q is empty":** that needs
the sixteen class certificates Q_j of the capture side, which do not exist.

## Statement

(E_JQ, v1). Let seventeen closed unit squares with pairwise disjoint interiors lie in [0, S]^2 with
S <= Sref = 4675530093604551/10^15, labelled 1 to 17, with one side direction a_i chosen for each square.
Then it is NOT the case that every xi_ik lies in the interval [lo_ik, hi_ik] and every a_i lies in the root arc of
label i, where the 34 intervals and the 17 arcs are those of

    bigbox/join/JQ_exact_v1.json   (entries window.box and root_arc)
    sha256 f4d1607eb4378487fcf6d8a8011125855bfb5912a6fa833ad3dcfcd6be14d93e

In words: no packing of seventeen unit squares of side at most Sref lies in the region JQ v1. Coordinates xi_ik and
the frame (container corner at the origin) as in SPEC 3.0 section 1.

This is the EMPTINESS COROLLARY of SPEC 3.0 (`SPEC_v3.0_NOTES.md`, note of 2026-10-09 18:38; the argument of the
root-region corollary of 06:22 with "F(N) is empty" in the place of "in the tube"): the certificate satisfies all
conditions of section 7 and no node is closed as terminal, so the set F(root) is empty; and a configuration that
is feasible for a side S <= Sref is feasible for the side Sref (SPEC 3.0 section 11).

## Evidence

| what | value |
|---|---|
| certificate | `local-research/claude-20261002/cloud/analysis/part3_exact/certs/JQ_v1/jQTw.n0.JQ.cert.jsonl.gz`, sha256 0b2a8ff8a3f9e12d96291643785fdf29ce1e07889b6f3b5ece8190f961c5482e; uncompressed stream 3d4606d12b2305b838adf3f3a91719dc85e4ff91e2e2bc0e38a80ae800069c7b |
| its shape | ONE node: the root is a leaf, closed by a `0` step; 1 step, 48,209 terms |
| exact value of the `0` step | L = 0.006945012... > 0, the same rational number in both checkers' reports (a fraction written with 3,761 characters; sha256 of that string 32f5ba220dc5600aa34924688015c59e24b135a5163ea54d54604ac23a89324e, which is also what the two checker reports of the cloud run record) |
| second copy | copy of the certificate in the result folder of the exact computation that produced it: identical bytes (`cmp`), with the cloud run's own checker reports (both PASS) and `SOURCE_COMMIT.txt` 4144fbf2b0fe657bccf935709555b1624cefa1f8 |
| producer | an exact leaf computation on the audit lead's side. Not made by the window side |
| acceptance run | `acceptance/accept_tree30.sh JQ_v1_jQTwn0 <certificate> bigbox/join/EXPECT_JQ_v1.json`, by the lead, 18:05:25 to 18:06:03 on the Mac |
| log | `acceptance/ACCEPT_JQ_v1_jQTwn0.log`, sha256 d04fa0f0f18576a9ebd5036fea3e6cb87286895078a1b4e3d41f801931caa09d: `RESULT: ACCEPTED` |
| checker reports | `acceptance/JQ_v1_jQTwn0_C1.json` (Python, sha256 3ccc8233...), `acceptance/JQ_v1_jQTwn0_C2.json` (Node, sha256 b8128b2a...) |
| frozen files | `checker/wxcheck_v30.py` cf8db52bfa1cc565..., `checker2/wxcheck2_v30.js` 97210adf74a3ebed..., `SPEC_v3.0.md` 0a6dfc2ae10ed6f3... (`acceptance/FROZEN_30.json`) |
| statement file | `bigbox/join/EXPECT_JQ_v1.json`, sha256 cbd56dcb45a945f4c8c95f96b919f72a6af70d81df8548fd78b8c918173f0ceb: 17 labels, S_floor = Sref, `terminal_leaves` 0, `root_region` = the file above |

Lines of the log that carry the statement: both checkers exit 0 with PASS on the whole file; every node accepted
by both; nodes 1, infeasible 1, terminal leaves 0 (expected 0); the root node has parent null, an empty
assumption list, the region's side interval, the region's box in all 68 interval ends and the region's arc for
every label (centre and both end rotations); "the statement of this record is made for the ROOT REGION of
'bigbox/join/JQ_exact_v1.json'".

Independent of the window side: Codex replayed the same certificate with both frozen checkers and its own binding of
the root to `JQ_exact_v1.json` and accepted "the whole JQ v1 root is EMPTY" at 18:20
(`research/finishing-threshold-goal-20261007/<author reply>`; acceptance file
`window-capture/join-design-1702/jq-one-node-review/ACCEPTED_INTERFACE.json`, sha256 32ef5169ea9e1ee9...).

## What the statement is used for, and what it does not contain

- Case Q of the join design as decided on 2026-10-09 17:47 hands the local side the region `JQ_exact_v2.json`,
  which lies inside JQ v1 (it differs in one end: label 9's upper end of xi_2, -0.124437 against -0.104437). So
  (E_JQ, v1) is the local side's statement for case Q of the decided design, and also for case Q of version 1.
- NOT contained: that the capture side's case Q puts a packing into this region. That is (i) the correctness of
  the region file against the class files (`JOIN_ROOTS.md` sections 2 and 9; reviewed: JQ v1 and JQ v2 are
  confirmed against the class files in both review reports, section 8 there; Codex's audit (d) of 17:52 says that
  all eleven v1 roots contain their literal products), and (ii) the class statements Q_j themselves, which the
  capture side has not certified.
