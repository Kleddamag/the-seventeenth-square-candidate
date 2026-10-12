# SPEC version 3.0: notes on the text and on the two frozen programs (not part of the text)

Window analysis. `SPEC_v3.0.md` (sha256
0a6dfc2ae10ed6f30a21ebe357a6e73dd7355223c521cc67a3f2bdab9549aba0) is pinned by both 3.0 checkers and is not
changed. This file collects what the reviews found that concerns its use. Frozen programs:
`checker/wxcheck_v30.py` (cf8db52b...096c), `checker2/wxcheck2_v30.js` (97210adf...7542); see
`acceptance/FROZEN_30.json`.

## 2026-10-09 03:33, from `reviews/REVIEW_30_JS.md` (J5, "things you should know")

- N1, compressed input. Section 10 says "a checker may read the same lines from a gzip-compressed file" and
  does not say how a compressed file is recognised. The two frozen 3.0 programs decide differently: the Node
  checker by the file NAME (ending `.gz`), the Python checker by the first two bytes. On a plain-text file
  named `*.gz` and on a gzip file not named `*.gz` the Node checker rejects and the Python checker accepts
  (reviewer's files `reviews/r30js/certs/misc/g02`, `g03`). RULE OF USE: a compressed certificate is always
  named `*.gz`, an uncompressed one never; then both read the same lines. A certificate accepted by both is
  not affected (the Node side read what its name says, and the hashes of the checked bytes are compared by the
  acceptance script). Damaged gzip files are rejected by both.
- N2, hashes in reports. For a `.gz` input the Node report's `certificate_sha256` is the hash of the
  DECOMPRESSED bytes; the Python report has the hash of the file under that key and the hash of the
  decompressed bytes under `certificate_uncompressed_sha256`. `acceptance/h_report30.py` compares each with
  its own computation.
- N3, report keys under "wx-cert-2". The Python checker writes `schema`, `window_centres`, `tube_centres`
  only under "wx-cert-3" (under "wx-cert-2" its report has exactly the keys of its 2.6 version plus
  `zero_step_L`); the Node checker writes them under both schemas. The text has no section on reports.
- N4, environment. Neither program reads an environment variable. Start the Python one as `python -I -B`
  (isolated mode) and the Node one with `NODE_OPTIONS` unset, so that nothing from outside can replace a
  standard module or change the interpreter's behaviour.
- N5, exit codes. Exit code 0 has one source in each 3.0 program: the PASS of a full run of the whole
  certificate (the help option exits 2). The frozen 2.6 programs exit 0 on the help option without checking
  anything (`SPEC_v2.6_ERRATA.md`, last note): never rely on an exit code alone; the acceptance script requires
  the first output line PASS and the report with the certificate's hash as well.

## 2026-10-09 06:22, a note on USE: the statement for the ROOT REGION (wording of the reviewer, `reviews/REVIEW_30_ACCEPT.md` R.4)

COROLLARY (root region; from the proof of the THEOREM of section 7). If a certificate satisfies all
conditions of section 7, every configuration of F(root) lies in the tube. By section 2 and the root
condition "EMPTY assumption list", F(root) is the set of feasible configurations with S_lo <= S <= S_hi,
every xi_ik in the root's interval [lo_ik, hi_ik] and every a_i in the root's arc
{R(psi) rho_i u_i : angle(P_i^-) <= psi <= angle(P_i^+)}  (S_lo, S_hi, lo, hi, rho, P^-, P^+ the root's data).
Proof: the induction claim of the proof of the THEOREM, for N = root; that induction uses the closing
conditions (a), (b), (c) and the tree conditions only, not the header window.
As in section 11, first paragraph: the root's box and arcs do not mention S, and S_lo <= Sref <= S_hi; so
every feasible configuration with S <= Sref whose positions and directions lie in the root's box and arcs
lies in the tube (it is feasible for the side Sref, hence in F(root)).
A theorem that uses the corollary states its region by the root's data (a file with its hash: side interval,
box, and for every label the centre and the two end rotations of the arc), not by the header window, and its
acceptance record must show that the root node of the certificate is that region (statement-file entry
`root_region`; the record then has the line "the statement of this record is made for the ROOT REGION of ...").

WHY IT IS NEEDED: the root test of section 8 compares the sine of the root end with the window radius, so a
window radius of "any direction" (above pi/4) forces a root arc of at least asin(pi/4) = 0.9033 on either
side, i.e. slivers beyond a quarter turn that a tree would have to cover a second time. With a root arc of
the reference direction +- rot(4147/10000) (half-angle 0.786228 > pi/4; exact test (tau + 1)^2 >= 2) there
are no slivers; the header window radius of such a label is then 7/10, and the theorem is stated for the root
region. FREE DIRECTIONS (belongs into the theorem itself, section 11 item (3)): a configuration has one side
direction a_i per square; the four side directions of a square are a quarter turn apart, so one of them is
R(psi) u_i with |psi| <= pi/4, and the square, its corners and so the feasibility of the configuration do not
depend on which of the four is taken; the theorem speaks about that representative.

## 2026-10-09 08:51, a note on USE: the frame of the wall coordinates

The reference file `upper-packing-certificate.json` is a packing of side Sref - 2 eps placed in [0, Sref]^2 with
every wall square exactly eps = 323264740583067756265381186720884493986257/(625 * 10^56) = 5.172e-18 off its
wall (labels 1, 5, 7: left; 2, 6, 8, 17: right; 1, 2, 3, 4: bottom; 7, 8, 15: top; the same rational for all;
computed exactly by `bigbox/hullh/mk_contract_skeleton.py`). Consequences for every statement whose window, root
or tube ends at xi = 0 in a wall coordinate (the hull roots, the provisional contract root, xi_{2,1} <= 0 in
G20S and HW): (1) S* <= Sref - 2 eps (the file is a packing of that side). (2) A packing of side
S <= Sref - 2 eps TRANSLATED BY (eps, eps) is a feasible configuration for the side Sref in which a square at
the left or bottom wall has x >= 1/2 + eps, i.e. xi >= 0 against a flush reference square, and a square at the
right or top wall has x <= S - 1/2 + eps <= Sref - 1/2 - eps, i.e. xi <= 0. So in this frame the clipped ends
lose nothing. (3) In the frame with the container corner at the origin and NO translation a flush corner square
has xi = -eps < 0 and is outside a box that starts at 0: a theorem on a clipped root must therefore say that
the packing is read translated by (eps, eps), and a capture statement must be made in the same frame. (The
SPEC's feasibility (F1) is about [0, S]^2 with the corner at the origin; a translated packing of smaller side is
feasible for the side Sref, which is all that the certificates, with S fixed at Sref, speak about.)

## 2026-10-09 18:38, a note on USE: the EMPTINESS statement for a root region (`reviews/join_roots/REVIEW_JOIN_ROOTS_V2.md` finding S2; wording of the argument: the reviewer's)

EMPTINESS COROLLARY (root region). If a certificate satisfies all conditions of section 7 and NO node of it is
closed as TERMINAL (closing condition (b)), then F(root) is empty: there is no feasible configuration with
S_lo <= S <= S_hi, every xi_ik in the root's interval and every a_i in the root's arc (the root's data, as in the
corollary of 06:22 above).
Proof: the induction of the proof of the THEOREM of section 7 over the finite tree, with the claim "F(N) is
empty" for every closed node N, using the closing conditions (a) and (c) only. A node closed by (a) has F(N)
empty: an accepted `0` step proves it (section 5), so does an EMPTY store (section 2), so do the excluded options
of a pair (the SAT lemma). A node closed by (c) has F(N) covered by the sets F of its children (section 6), which
are empty by induction. No node is closed by (b). What F(root) is: section 2 and the root condition "EMPTY
assumption list". The header window and the tube are not used.
As in section 11, first paragraph: the root's box and arcs do not mention S, and S_lo <= Sref <= S_hi; so NO
feasible configuration with S <= Sref has its positions and directions in the root's box and arcs (it would be
feasible for the side Sref, hence in F(root)).
A theorem that uses this corollary states its region by the root's data, as for the corollary of 06:22, and its
acceptance record must show both that the root node of the certificate is that region (statement-file entry
`root_region`) and that no leaf is terminal (statement-file entry `terminal_leaves` = 0; the record then has the
line "number of terminal leaves is 0 (expected 0)"). First use: `bigbox/join/RECORD_EJQ_v1.md`. It is the
argument behind every statement (E_X) of `bigbox/join/JOIN_ROOTS.md` section 3.

