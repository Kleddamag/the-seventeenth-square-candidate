# Theorem G20S (position 1/5, angle 1/10, the SIXTEEN constrained squares, no condition on the rattler): statement and proof chain

Version of 2026-10-09 00:00, by the lead (draft 2026-10-08 20:31; reviewed versions kept as
`bigbox/THEOREM_G20S_as_reviewed_2210.md` (review part R5) and `bigbox/THEOREM_G20S_as_reviewed_2359.md` (part
R6); the changes since the first are: the corrections of part R5, step 3 with its evidence, and the
corrections N1 to N7 of part R6).
**STATUS: PROVED (2026-10-08 23:59, with the edits of this version).** All three links exist and every
component is reviewed by a reviewer that did not produce it:
(ANN_G20S) and (ANN_HW), steps 1 and 2: exact certificates accepted by both independent checkers, paperwork
reviewed (`reviews/REVIEW_26.md` part R5); the terminal instance on the wide slider box, step 3: passed its
chain and its exact replay (the lead's at 23:24, the reviewer's own on a byte copy at 23:33) and is reviewed
together with the completed chain (`reviews/REVIEW_26.md` part R6, verdict "sound with corrections"; the
reviewer's judgment: the theorem may be called PROVED once its two MUST edits are made, which this version
does). `reviews/REVIEW_26.md` after part R6: 227,683 bytes, sha256
07053a3643af60520dbccc009d041c5be244620fe75ec2fec6e259fa68429734 (its first 162,975 bytes are the R5 state,
bf55cdf1...).
Standing: that of the theorems of `THEOREM.md`: computer-assisted, and resting on Codex's analytic lemmas of
the terminal proof, which are hand proofs and are taken as they stand, as are the earlier reviews (the
terminal method, the coordinate interface, S* and the obligations (1), (1b), the two checkers).
(Before step 3 existed the
THEOREM rested on floating-point evidence only (`bigbox/truth/TRUTH_BIGBOX.md` Q7 (d) and the
searches).) Status words as in `bigbox/THEOREM_G20.md`: COMPUTED / PROVED.

## 1. Setting

As in `THEOREM.md` section 1 (packing file, Sref, S*, packing, frame, labelling, rational coordinates of the
sixteen constrained squares, sliders a = -xi_{2,1}, b = -xi_{11,2}, z = xi_{13,2}, three-slider family, the 45
exact-root core deviations). Sixteen labels; square 4, the rattler, is not used anywhere. Format of the
certificates: `SPEC_v2.5.1.md` (no `labels` field).

## 2. Windows

- G20S: xi_ik in [-1/5, 1/5] for the sixteen labels, except xi_{2,1} in [-39/125, 0] and xi_{13,2} in
  [-1/5, 28/125]; |phi_i| <= 1/10 for all sixteen. In slider notation: a in [0, 39/125], b in [-1/5, 1/5],
  z in [-1/5, 28/125]. The ends b = 1/5 and z = -1/5 are CUTS. (Floating-point evidence, not used in any proof: without
  them the sixteen-square statement fails, side S* - 2.9e-4 at b > 0.2303, z < -0.2066.)
- HW: the 29 core coordinates within 3/20, |phi_i| <= 101/1000, xi_{2,1} in [-8/25, 0], xi_{11,2} in
  [-1/5, 2/25], xi_{13,2} in [-1/5, 1/10] (a in [0, 8/25], b in [-2/25, 1/5], z in [-1/5, 1/10]). This is the
  window H-plus-r015 of `THEOREM.md` with the slider box widened to the cuts.
G20S consists of the sixteen factors that G20 has for the constrained squares. HW is the window H-plus-r015
with three lower slider ends moved out (xi_{2,1} from -1/4 to -8/25, xi_{11,2} from -3/20 to -1/5, xi_{13,2}
from -1/8 to -1/5); it is NOT the box of H-plus-r015. Neither of G20S, HW contains the other (exact check:
`acceptance/compose_G20S.py`).

## 3. Theorem

Let P be a packing with side S <= S*, in the frame and labelling above, whose sixteen constrained squares lie
in G20S (the rattler is unrestricted). Then S = S*, and the sixteen squares lie on the three-slider family
(all 45 exact-root core deviations vanish). The same for every feasible configuration of the sixteen squares
alone. The same statement holds with HW in place of G20S (steps 2 to 4 alone: the window HW has xi_{2,1} <= 0).
Unlike G20 this needs nothing about the rattler; the price is that the equality set is the family on the
whole slider box (floating-point evidence, not proved: with sixteen squares the sliders are not confined; a up
to 0.312, b up to 0.200, z down to -0.200 at side S*).

## 4. Proof chain

1. (ANN_G20S) Every feasible configuration of the sixteen squares with S <= Sref in G20S lies in the tube
   T1 := window of HW with the upper end of xi_{2,1} at 1/100. Evidence: certificate `bigbox/gen17/G20S_tree.jsonl.gz`, SHA-256 of the file
   3275f52aca2e23e1916744d294bfdca827dd71db7cfe38fede277cca94c68f84, of the uncompressed text
   f17da3bdb241141cfb592110a8e56d9f13eff0cf3f2d5bc26ccf4f134e509e22; plain SPEC 2.5.1 header (no `labels`, no
   `S_floor`); a tree of 679 nodes: 339 splits (242 scripted arc cuts, 97 sign splits) and 340 leaves (38
   terminal, 302 infeasible: 237 by a `0` step, 65 by a pair closure); COMPUTED 21:50 (generator's replay);
   accepted 22:09 by `checker/wxcheck_v26.py` (sha256 72550830...b03faaef, 604 s) and
   `checker2/wxcheck2_v26.js` (sha256 a725c230...2a723968, 303 s), the frozen and reviewed 2.6 checkers, which
   are reviewed checkers for a certificate without the new header fields, which under SPEC 2.6 states exactly
   the 2.5.1 statement (`reviews/REVIEW_26.md` parts R2 and R4, by reading; the two checker reviewers' own
   regression runs, `checker/v26/NOTES_V26.md` and `checker2/CHECKER2_NOTES.md` section 9; and the reviewer's own
   run in part R5: both 2.6 checkers give reports identical to the stored 2.5.1 reports on the H-plus-r015 tree,
   all 555 final-store digests included); record `acceptance/ACCEPT_G20S.log` (sha256
   751215e6e597cc18edc8fd8dd2e219878a835a67d5ac271f2e07d430de556645), reports
   `G20S_C1.json`, `G20S_C2.json`; RESULT: ACCEPTED, both used sixteen labels, reports agree node by node.
   Expected statement, written by the lead before the acceptance run (20:31):
   `acceptance/EXPECT_G20S.json`.
2. (ANN_HW) Every feasible configuration of the sixteen squares with S <= Sref in HW lies in the tube
   T2 := 29 core coordinates within 1/250, |phi_i| <= 1/500, xi_{2,1} in [-8/25, 1/250], xi_{11,2} in
   [-1/5, 1/20], xi_{13,2} in [-1/5, 3/40]. Evidence: certificate `bigbox/gen17/HW_tree.jsonl.gz`, SHA-256 of the file
   c974a9c5dce91e7db0e04fb17a7a5500b477a48448073d7ed29779423bf0be73, of the uncompressed text
   a8cc9689a3cd9cf15b5f198edb597b734039bf8eeededafb05366a85408e426a; plain SPEC 2.5.1 header; a tree of 579
   nodes: 289 splits (242 scripted arc cuts, 47 sign splits) and 290 leaves (1 terminal, 289 infeasible: 224
   by a `0` step, 65 by a pair closure); COMPUTED 21:38; accepted 21:55 by the same two frozen 2.6 checkers
   (436 s and 199 s); record `acceptance/ACCEPT_HW.log` (sha256
   9f16e4fbbcabcb7f483064b0c948826bf9eb23b6853d227d5168eee012211ef4), reports `HW_C1.json`,
   `HW_C2.json`; RESULT: ACCEPTED.
   Expected statement: `acceptance/EXPECT_HW.json`.
3. Terminal instance `terminal/instances/box-wide/` (README, REPLAY.sh, SHA256SUMS there): "feasible, S <= S*,
   the 29 core coordinates within 1/200, the 16 angles within 1/400, a in [0, 8/25], b in [-1/20, 1/5], z in
   [-1/5, 3/40] => S = S* and all 45 exact-root core deviations vanish". It is Codex's terminal proof
   re-instantiated on the wide slider box exactly as `terminal/instances/box-relaxed/` is on the slider box of
   the TUBE of `THEOREM.md` section 4: the same unchanged files (digests in its SHA256SUMS; `verify.py` byte-identical), only the two
   slider lines changed (`CHANGES.diff`: `uniform.py` line 80 and `bridge.py` line 198), made with the instance tools (`terminal/tools/make_instance.py`, `run_instance.sh`, `roster_check.py`, `finalize_instance.py`),
   tube (1/200, 1/400): 17 rounds, final core radius 8.735e-5 < 1/5000; bridge PASS; rigidity stage: 8 rounds,
   ratio 429573630640681/500000000000000 = 0.859 < 1, 52 identities, 19 pairs; unchanged `verify.py` PASS;
   roster check: the full original roster of 52 labels (11 unique-owner pairs, 8 parallel pairs), so no row was
   lost silently on the wider box; `composition_check.py` PASS (obligations (1), (1b), (1c) and the coordinate
   interface); exact replay `REPLAY.sh` exit 0 (`logs/replay.out`). SHA-256: SHA256SUMS
   52082977c296b37711073d4227d569799140381da23484c8060a25646210ac79, proof receipt
   815d54093cf90ea90286eb1fc08342b50e2b231a05ca995e5e0385e669f20e2e. Same standing as the instance box-relaxed:
   computer-assisted; the analytic lemmas are the hand proofs of Codex's `PROOF.md`. Reviewed: `reviews/REVIEW_26.md`
   part R6 (file comparison with box-relaxed and with Codex's originals, own replay on a byte copy, eight mutated
   copies refused, roster and structural limits recomputed from the packing file). Note on the instance's
   README uses generic template attribution. The three diagnostics logs its section 9 names were not run
   for this instance (its section 6 says so). The roster comparison is not part of `REPLAY.sh`; it rests on
   `logs/roster.json` and on the reviewer's recomputation.
   The tube T2 of step 2, cut by xi_{2,1} <= 0 (step 4), lies in this instance's entry conditions: core
   1/250 <= 1/200, angles 1/500 <= 1/400, and the three slider intervals are then equal end for end. (T2 itself
   does not lie in them: xi_{2,1} runs up to 1/250 in T2 and up to 0 in the entry conditions.) Exact check:
   `acceptance/compose_G20S.py`, which reads the instance's `INTERFACE-tube.json`.
4. Composition: S <= S* <= Sref; step 1 puts the sixteen squares into T1; the window gives xi_{2,1} <= 0, so
   they lie in HW; step 2 puts them into T2. T2 alone gives only a >= -1/250; a >= 0 comes from the window G20S (xi_{2,1} <= 0)
   or, independently, from the right wall and obligation (1b) of `THEOREM.md`. Then step 3.
   Exact check of all three inclusions: `acceptance/compose_G20S.py` (consistent).

## 5. What capture has to supply

Sixteen statements in ONE frame: the square of region j in its factor of section 2, j != 4, the cuts
b <= 1/5 and z >= -1/5 included. Nothing about the rattler. With statements that fix the frame only up to the
mirror image the statement for label 3 can be satisfied by the rattler's place alone; then a centre-only
count of two centres in regions 3 and 4 is needed and label 3 has to be taken with free direction (variant
G20S3, not built; floating-point: with the other fifteen in their factors, label 3 turned by 0.10 costs
S* + 0.016).
