Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line.

# REVIEW 30: referee report on `SPEC_v3.0.md` (version 3.0 candidate)

The referee, 2026-10-09. Written in parts: A first, then B, C,
D, then E and F (the verdict on the audited candidate), then G (the corrected and the final text) and H (the real
certificate and the Python checker of version 3.0). Folder W = `research/window-extension-20261008`. My
experiments are in `W/reviews/r30/` (index in the appendix).

**In one paragraph.** The mathematics of the four additions of version 3.0 is correct. The audited text had ONE
place where a literal reader accepts a false certificate (a step on the form `0` with sense "hi", inherited from
2.6; no program accepts it) and fourteen places where it was silent or loose; all are corrected (MUST-1 to
MUST-15, SHOULD 1 to 12, R1 to R12), and the final text, `W/SPEC_v3.0.md` with sha256
0a6dfc2ae10ed6f30a21ebe357a6e73dd7355223c521cc67a3f2bdab9549aba0, is accepted as it stands. No program accepted
anything false in any of my runs; my own calculator, written from the text, reproduces the exact L of all 81
leaves of the real certificate, and my own check of its tree finds nothing.

Texts examined (sha256 verified with `shasum -a 256`):

- `W/SPEC_v3.0.md` AS IT WAS UNTIL 02:36, 862 lines, 2cec6f7275580cb7ec71bdfc48d8cc57f988b69f5acedf25f558d5085d0ca908:
  the text under audit. It is kept as `W/SPEC_v3.0_candidate_audited.md` (same hash); ALL LINE NUMBERS of parts A
  to F are lines of that file. Since 02:36 `W/SPEC_v3.0.md` is the final text of part G (885 lines,
  0a6dfc2ae10ed6f30a21ebe357a6e73dd7355223c521cc67a3f2bdab9549aba0).
- `W/SPEC.md`, 584 lines, fa14fe405635d28bb16a66febe1370db766df2b90317d437472af6eb389d8aa3 (version 2.6).
- `W/SPEC_v2.6_ERRATA.md`, 33 lines, 2be2a3981c11331c86e8986aa2a4e16ced777756338aaab957d3e699da1ba0d7 (F1 to F4, as it
  was when I started; during the review the lead added an erratum F5 for my finding B-1, new hash e498cd5f...).
- `diff W/SPEC.md W/SPEC_v3.0.md`: 325 lines added, 47 removed (as announced).

Not read before parts A to D were written: the prototype's source, `proto30/PROTO_NOTES.md`,
`proto30/SPEC_3.0_DELTA.md`, the two superseded drafts. Never read: `checker2/wxcheck2_v30.js`, `checker2/v30/`.

Status of the parts: all written. A, B, C, D, E: the audit of the candidate (B.7 = the table of
readings). F: the verdict, the lead's ten decisions (F.2), the MUST and SHOULD lists with
exact wording (F.3, F.4), what was not examined (F.5). G: the corrected text needed ten exact replacements R1
to R10 (all accepted by the lead); the FINAL text `proto30/SPEC_v3.0_final.md` is ACCEPTED AS IT STANDS (G.5)
and was installed by the lead as `W/SPEC_v3.0.md`. H: all 81 leaves and the tree of the real certificate
checked by my own code, and my corpus through the edited Python checker; nothing unexpected.

One finding was reported to the lead at once (B-1 = MUST-1: a step on the form `0` with sense "hi"). No
program accepted a false certificate in any of my tests.

---

## Part A. Soundness of everything new

Method: for every new passage I first wrote down my own argument from the definitions of sections 0 to 3,
then compared it with the proof in the text. "MINE" is my derivation, "TEXT" the comparison.

Summary of part A (written before the experiments; parts C and D confirmed it and changed nothing): **I found no
false mathematical statement in the new passages.** The LIFTING LEMMA, the TERM LEMMA, the CLAIM (raw and centred) and the two proofs of section 8 are
correct as written, and each of the seven points examined has the answer the author intends. What I found
are contract matters (parts B and C) and a few places where the text proves more or less than it says; they
are numbered A-1, A-2, ... below and are taken up again in part F.

### A.1 Section 3, indicator variables and polynomial forms (lines 114-122, 138-151, 173-174)

MINE. A polynomial form is a sum of entries coef * v_1 ... v_r, r <= 2, every v a base variable name of the
node's label set. So `q:NAME` is an element of Q[base variables] of degree <= 2, and nothing else can be in
it: no named form, no custom form, no indicator (an indicator has no name, so it cannot be written in an
entry). Its value at a configuration is a real number. An indicator variable is a new polynomial variable of
one round; the only way to write one is the name `ind:i:j:k`.

TEXT. Agrees. The sentence "it occurs in no named form, no polynomial form, no objective of a step, no store,
no cut and no `centre`" (lines 120-121) is enforced by the format: the form NAMEs (lines 794-795), the entries
of a `q:` form (line 705), the keys of `cuts` (form NAMEs) and the keys of `centre` (line 715) are closed
lists that contain no indicator. Checked name by name in A.4 (answer to point 2) and by experiment in D.6.

### A.2 Section 4.9, `sq` and `pol` (lines 379-387), point 4 of the seven

MINE. (q)^2 >= 0 at every real point, so `sq:NAME` is a fact on F(N) for every store; no precondition is
needed, and it is even true off F(N). `pol:NAME` has no sign; in a term that also contains `circ:i` the product
is (C_i^2 + s_i^2 - 1) * (other factors). At a configuration C_i = cos psi_i and s_i = sin psi_i are the cosine
and sine of ONE real number psi_i (section 2, line 84: a_i = R(psi_i) abar_i), so the first factor is exactly 0
and the product is 0 provided the other factors are finite real numbers, which they are (polynomials evaluated
at a point). This holds at every configuration, feasible or not, for every label of I, whatever the arc: the
identity does not use the arc, the box, feasibility or the label count. With sixteen labels `circ:4` is not a
name (label rule, line 681) and no variable of label 4 exists, so nothing about square 4 can enter. For a
square with "free" direction (window radius above pi/4, lines 632-634) C_i, s_i are still the cosine and sine
of one angle; `circ` is unaffected.

TEXT. Agrees (lines 199-200, 383-385, TERM LEMMA first sentence, lines 487-488). Answer to point 4: yes,
`circ:i` is an equality at every configuration in the coordinates of sections 1 to 3, for every label of I;
and `pol`/`sq` can contain only a polynomial of degree <= 2 in the base variables of the node.

Remark A-1 (not an error). A term with `circ` is exempt from the sign rule but NOT from (T3) and (T4)
(lines 453-454, 456). That is more than soundness needs (the product is 0 anyway) but it is what makes the
polynomial of the term well defined (a `cut` or `wsup` or `par` name has a polynomial only if it is
available), so it must stay.

### A.3 Section 4.10, the indicator construction (lines 389-439), points 1, 2, 5 of the seven

MINE. Fix a node N, an evaluated round, its start store St, and x in F(N).

(i) What "excluded" proves. By 4.7 (lines 343-357) an option (o,t,axis,eps) HOLDS at x iff
n.(q_t - q_o) >= 1/2 + h(x), h = (|n.a_t| + |n.b_t|)/2 (the minimum of n.(c - q_o) over the four corners c of
t is n.(q_t - q_o) - h). EXCLUDED on St means U < 1/2 + h_lo with U an upper store bound of n.(q_t - q_o) and
h_lo a lower bound of h, both derived from statements of St. Every statement of St is true at every point of
F(N) (store invariant, section 2 lines 93-97 and section 5 lines 532-534). Hence: for EVERY x in F(N) the
option does not hold at x, i.e. some corner c of t has n.(c - q_o) < 1/2. It proves nothing about points
outside F(N) and nothing about the other options.

(ii) Existence of the lifted point. x is feasible, the two labels are different labels of I, so by the SAT
lemma (4.5) at least one of the 8 options holds at x. If the declaration is valid, every option outside the
list holds nowhere on F(N), so the set {k : O_k holds at x} is a nonempty subset of {1..m}; k0 := its minimum.
z*_k := [k = k0] for k < m. Then ind_k(z*) = [k = k0] for k < m by definition and
ind_m(z*) = 1 - sum_{k<m} [k = k0] = [m = k0]. All z* are 0 or 1.

(iii) One point for the whole round. z* is defined pair by pair, from x and the declaration of that pair
alone; the lifted point (x, z*) is the tuple over all declared pairs of the round. It does not depend on the
step. So there is ONE point (x, z*) per round and per x, and every statement below is made at that point.

TEXT. Agrees: LIFTED POINT (lines 417-422), LIFTING LEMMA and proof (lines 423-435). The proof is complete; the
only fact it takes from outside is "an option that is excluded on St holds at no configuration of F(N)", which
is the last sentence of 4.7 together with the store invariant.

Answers to point 1, case by case (one feasible x, one round; "true" = true at the lifted point):

| combination | answer |
|---|---|
| several pairs with `ind` declarations in the round | z* is the product of independent choices; (L1)-(L3) hold pair by pair. Sound. |
| a declared pair and other pairs with option assumptions or `opt` declarations | the `opt` facts of those pairs are facts on F(N) (4.5 VALIDITY), independent of z. Sound. |
| product of guarded corners of two different options of the same pair | needs 4 names (2 corners + 2 guards), a term has at most 3 (line 445): not expressible. If it were, the TERM LEMMA would still hold (one of the two indicators is 0 at the lifted point). With 3 names one can write corner(O_k) * ind_k * ind_l, l != k: it is 0 at the lifted point. Sound. |
| product of guarded corners of two different pairs | same: 4 names, not expressible; would be sound. |
| two corners of the SAME option with one guard | expressible (3 names) and occurs in the real certificate (510 terms `opt, opt, ind` in leaf W01). ind*_k = 1 implies O_k holds, so both corner values are >= 0. Sound. |
| the eliminated last indicator as a guard | `ind:i:j:m` is the polynomial 1 - sum z_k; at the lifted point its value is ind*_m in {0,1} by (L2). The guard argument uses only this value. Sound. |
| a list with one option | precondition: the 7 others excluded; ind_1 = 1, no variable; the guarded corner is the `opt` fact of 2.6 under the "7 others excluded" clause. Sound. |
| a list containing an excluded option | allowed; that option holds nowhere on F(N), so it is never k0, its indicator is 0 at every lifted point and its corner terms vanish there. Sound (it only costs a variable). |
| a list that omits an excluded option | this is the precondition. Sound. |
| a list that omits an option that is NOT excluded | declaration not valid, certificate rejected (lines 404-408). Needed: otherwise k0 need not exist. |

On which store: the store at the START of the round (lines 404-405, 517-518), which is fixed before any step
of the round is looked at. A bound certified by a step of the same round cannot enter the exclusion test, the
facts or the remainder bound of that round: the ROUND paragraph (lines 517-519) says that all steps use the
start store and that certified values are used only to accept entries of the NEW store. A bound certified in
an EARLIER round by a step that used indicators can enter (through the store): that is sound, because by the
CLAIM such a bound is a statement "F >= v on F(N)" about a named form, with no indicator in it. The induction
is: store invariant at the start of round r => lifting lemma for round r => CLAIM for the steps of round r
=> every accepted entry of the next store is true on F(N). No circle.

Remark A-2 (order of events, see also part C). The text fixes the order "start store, facts and declarations
from it, all steps, then the new store" by the two sentences of lines 517-519 and by "at the start of the
round" in every precondition. It does not say in one place what a checker does in an evaluated round, in which
order; I list the sequence I read out of the text in part C and ask that it be written down.

Answer to point 5 (guard rule). It is enough that every corner name of an IND-LISTED option O_k comes with
`ind:i:j:k` of the same pair and the same k in the same term: that is exactly what case (c) of the TERM LEMMA
uses. A declaration in another round does not make a name available (T4, lines 456-460: "in the round"), and
the variables of two rounds are different variables (lines 116-117). A pair with an option assumption in the
node or in an ancestor cannot have an `ind` declaration: the child's `assume` list is the parent's list plus
one item (lines 560-561), so "the node's `assume` list" of (R3) contains the assumptions of all ancestors. A
label that is not in I is rejected wherever a label can occur (lines 677-681, 686-688).

Remark A-3 (R1 to R3 are not soundness conditions, and the text should say which are needed for what).
(R1) is needed for the NAMES to mean one thing: two `ind` declarations of a pair would give two lists for the
same variables z_{ij,k}. (R2) removes a choice: with an `opt` and an `ind` declaration of one pair the corner
name of a listed option would be a fact (usable unguarded) and a guarded name at once; either resolution is
sound (revised after part E: the author's earlier draft allowed both declarations and let the fact win).
(R3) is not needed for anything mathematical: a pair with an option assumption and an `ind` declaration would
still have a lifted point (the exclusion test never uses assumptions). The parenthesis of lines 402-403 says
this for (R3) in other words. Not an error; the text may keep the three rules (SHOULD-5).

### A.4 Section 5, term rules, TERM LEMMA, CLAIM (lines 443-512), points 2, 3, 6 of the seven

MINE. Let (x, z*) be the lifted point. Every name of a term that obeys (T4) is one of: (a) a fact of 4.0 to
4.8 that is available, or `sq`; (b) `ind`; (c) a corner name of an IND-LISTED option; (d) `pol`; (e) `circ`.
If (e) occurs the product is 0. Otherwise (d) does not occur (T2), lambda >= 0 (T1), (a) is >= 0 at x, (b) is
0 or 1 at z*, and for (c) the term contains the (b)-factor ind_k of its own option (T3): if that factor is 0
the product is 0, if it is 1 then O_k holds at x and the corner value is >= 0. So lambda * product >= 0 at
(x, z*). The objective g is a named form or its negative (no z), and Rem := g - sum lambda_k prod_k is an
identity of polynomials in (base variables, z); evaluating at (x, z*): g(x) = Rem(x, z*) + (sum >= 0)
>= Rem(x, z*). Finally Rem(x, z*) >= L if L is a lower bound of Rem on a set that contains (x, z*): the
product of the SB intervals of the base variables (x is in it because the store holds at x) times [0,1] for
every z (z* is in it).

TEXT. TERM LEMMA and proof (lines 483-499) and CLAIM (lines 500-508) agree with this, including for an
objective other than `0`: the conclusion is "g(x) >= L for all x in F(N)", a statement about the named form
alone. So a step's certified value is a bound on its objective at every x of F(N); nothing in it depends on z*
(z* depends on x, L does not).

Answer to point 2. An indicator variable cannot reach:
- a named form or custom form (components are form NAMEs, lines 135-137, 699-700);
- a polynomial form (entries are base variable names);
- an objective (`form` is a form NAME, line 755, lines 794-795; `q:NAME` and indicators are not form NAMEs);
- the store (S, box, arc, rarc, cuts keyed by form NAMEs; lines 757-758); the acceptance rules of lines 520-531
  use certified values only;
- a split, a closure test, the terminal test (they read the final store);
- a later round (T4 "in the round"; the variables belong to the round, lines 116-117, 537-540).
What does pass from an indicator step to later rounds is its certified value, a bound on a named form on F(N).

Answer to point 3 (the remainder bound).
- RAW RULE (lines 465-468). The interval of a monomial is the product, by interval multiplication, of the SB
  intervals of its variables with multiplicity. For real intervals X*Y = {xy} is exactly the interval of the
  four end products, the operation is commutative and associative, so the interval of a monomial is well
  defined and contains the value of the monomial at every point whose coordinates lie in their intervals (the
  same variable taken e times gives X*...*X, which contains {x^e}; for an even power this is not the tight
  range, e.g. [-1,2]*[-1,2] = [-2,4], but it is valid and it is the unique number the rule defines). Summing
  min(r lo, r hi) over the monomials gives a lower bound of Rem on the whole product set
  (SB box) x [0,1]^(number of indicator variables). The lifted point lies in that set.
- The eliminated indicator ind_m = 1 - sum z is NOT in [0,1] on the whole cube (it is 1 - (m-1) at the corner
  z = (1,..,1)). No argument needs it to be: the sign of a term is argued at the lifted point only (where
  ind_m is 0 or 1), and the remainder is bounded as a polynomial in the variables z_1..z_{m-1}, never as a
  polynomial in "ind_m". Correct as written.
- CENTRED RULE (lines 469-479). Rem(c + y) is the same function as Rem under y = v - c; y_v ranges over
  SB(v) - c_v when v ranges over SB(v). So the bound is again a lower bound of Rem on the same product set,
  for EVERY rational c: a centre outside the store interval gives an interval SB - c that does not contain 0
  and a (bad but) valid bound; a centre for a variable that does not occur changes nothing; an empty `centre`
  gives c = 0, hence the raw number; an indicator variable has centre 0 and interval [0,1] and cannot be
  given another centre because it has no name (line 716).
- Both rules define ONE rational number: the monomial expansion of Rem (resp. of Rem(c + y)) is unique and
  the interval product does not depend on the order (lines 480-482). I agree.

Answer to point 6 (degrees). The proof needs no degree limit: the interval bound is valid for monomials of
any degree in the base variables and the z, because every variable has an SB interval. Reachable degrees: a
term has at most 3 names; `sq` has degree <= 4, `pol` <= 2, facts <= 2, `ind` 1 (in z). So a term has degree
at most 12 (`sq*sq*sq`) in the base variables, or e.g. 4 + 2 + 1 for `sq`, corner, `ind`. Named forms have
degree <= 2 and enter only as the objective. Nothing of higher degree than this is reachable, and nothing
would be unsound if it were. (Cost, not soundness: the number of monomials of Rem.)

Remark A-4 (wording of line 381). "`sq:NAME` ... A fact of N in every round and for every store" is true, and
`sq` is the one fact that is also >= 0 outside F(N). Line 102 says "the checker builds no fact from [an EMPTY]
store"; there is no conflict, because an evaluated round never starts with an EMPTY store: after an EMPTY
store no round is evaluated (line 541-542), and the node's data cannot be EMPTY (lo <= hi, S_lo <= S_hi and
sin P^- <= sin P^+ are well-formedness; there is no cut and no stored relative endpoint; and for the default
endpoints of a pair, angle(D^+) - angle(D^-) = (psi_j^+ - psi_j^-) + (psi_i^+ - psi_i^-) >= 0, so if both have
a positive cosine both angles lie in (-pi/2, pi/2) and sin D^- <= sin D^+). SHOULD-11.

### A.5 Section 8 with centres (lines 599-634), point 7 of the seven

MINE. Window with centres gamma_i: a_i = R(phi) gamma_i u_i, |phi| <= alpha_i. The root arc of square i is
{R(psi) rho_i u_i : psi^- <= psi <= psi^+} with psi^± = angle(P_i^±) in (-pi/2, pi/2), psi^- <= psi^+. Put
theta0 := angle(rho_i conj(gamma_i)). Then R(psi) rho_i u_i = R(psi + theta0) gamma_i u_i, and
Ab^± = conj(gamma_i) rho_i P_i^± has the angle theta0 + psi^± (mod 2 pi). The two real numbers
e^± := theta0 + psi^± satisfy 0 <= e^+ - e^- < pi. If cos Ab^- > 0 and cos Ab^+ > 0, each of e^-, e^+ lies in
an interval (-pi/2, pi/2) + 2 pi Z; two different such intervals are more than pi apart, so both lie in the
same one; shift by its multiple of 2 pi. Then e^- <= e^+ are in (-pi/2, pi/2) and the root arc is
{R(e) gamma_i u_i : e^- <= e <= e^+}. With sin e^+ >= alpha_i > 0: e^+ >= sin e^+ >= alpha_i (x >= sin x for
x >= 0). With sin e^- <= -alpha_i: e^- <= -alpha_i. So [-alpha_i, alpha_i] is inside [e^-, e^+] and every
window direction R(phi) gamma_i u_i is R(phi - theta0 + 2 pi k) abar_i with phi - theta0 + 2 pi k in
[psi^-, psi^+], i.e. psi_i in [psi^-, psi^+]: the configuration's a_i lies in the root arc. Same reduction for
the tube and a final store (which is not EMPTY when the terminal test is made, so psi^- <= psi^+ there too):
|sin e^±| <= alphaT - alphaT^3/6 <= sin alphaT (alphaT <= 1 < pi/2) and monotonicity of sin on (-pi/2, pi/2)
give |e^±| <= alphaT, and the arc lies between its ends.

TEXT. Agrees (lines 615-622, 627-630). The new proof also closes a gap that the proof of 2.6 left open (2.6
wrote "angle(Ab^+) = asin(sin Ab^+)" without saying why both ends are on the same branch; the argument
"k = m because the arc is shorter than pi" is now there). The tests under the identity centre are the tests of
2.6 character for character (conj(1,0) = identity).

Answer to point 7. With centres different from the identity the statement proved is (ANN) of section 0 for
the window and the tube AS DEFINED IN SECTION 8 WITH THEIR CENTRES (lines 601-606): section 0 (line 54) says
"W and T are given by rational data (section 8)", so (ANN) is still exactly the statement written, the data
of W and T now including the centres. The root condition is tested against the window's arc with the
window's centre (line 611), the terminal test against the tube's arc with the tube's centre (line 624); the
two centre maps are independent (line 673). Section 11 item (4) (lines 837-839) tells the application that it
must state the centres. Free direction with a centre: the window arc is |phi| <= alpha_i < 1 around
gamma_i u_i, the root test needs sin Ab^± beyond ±alpha_i with positive cosines, so the root arc is shorter
than pi and everything above applies; a window radius just above pi/4 around ANY centre covers one of the four
side directions of every square (the parenthesis of lines 632-634 says "with the identity centre"; it is true
for every centre).

Remark A-5 (statement of the theorem, not an error). (ANN) is a statement about configurations, which come
with one side direction a_i per square; with a window radius above pi/4 the same packing has several
configurations in the window, and the tree must prove the tube for each of them. This is what the text says
(lines 608-609, section 11 lines 816-818) and it was so in 2.6.

### A.6 Where new and old meet

(1) Store updates (lines 517-542). The acceptance rules are those of 2.6; the paragraph of lines 537-540
states that no rule refers to an indicator. Checked: every rule of lines 520-531 compares a proposed entry
with an old entry or with certified values of steps for a NAMED FORM. Sound by the CLAIM.

(2) `0` steps and closures (lines 511-512, 577-581, 779-784). A `0` step with indicators proves 0 >= L > 0 for
every x in F(N), so F(N) is empty; the lifted point is used for each x separately. Sound. The pair closure
and the option split use 4.7 on the final store, which contains no indicator.

(3) `opt` names (lines 264-270, 456-458). An option is OPT-AVAILABLE (a fact, kind (a)) or IND-LISTED (kind
(c), guard needed), never both in one round by (R2). The definition of OPT-AVAILABLE ("the round has an `opt`
declaration of it") is new wording for the rule of 2.6 (section 10: "An `opt` declaration makes the four
`opt:` facts of that option available iff ..."; "undeclared pairs carry no `opt`/`par` facts").

(4) `par` facts of a pair that also has an `ind` declaration (allowed, line 402-403). Their precondition
(4.6) is tested on the start store and makes them facts on F(N) (LEMMA P needs "O_i or O_j holds", which
follows from the exclusion of the 6 others on F(N)); they do not depend on z. Sound.

(5) The schema switch (lines 22-25, 654-661) is examined in part B.

### A.7 Findings of part A

No MUST from the mathematics. Of the remarks, A-2 (the order of events) goes into MUST-3, A-3 into SHOULD-5,
A-4 into SHOULD-11, the "identity centre" of A.5 into SHOULD-4; A-1 and A-5 need no change of the text. The
experiments of parts C and D (994 steps and 81 real leaves recomputed, 54 false certificates) confirmed part A
and changed nothing in it; the one revision, in A-3, is marked.

---

## Part B. Conservativity

Result of part B. **For a certificate with the schema "wx-cert-2" the text of 3.0 accepts what the text of 2.6
accepts**, with the reservations B-1 to B-4 below. Two of them are places where the text (2.6 and 3.0 alike)
does not say what both frozen checkers do, and one of those has a reading under which a false certificate is
accepted (B-1, reported to the lead at once; it is MUST-1). One is a certificate on which the two frozen
checkers give different verdicts (B-3, an empty node id).

All experiments of this part are scripts in `W/reviews/r30/` (`harness.py` runs the three programs as black
boxes); the generated certificates are in `W/reviews/r30/b/`, the tables in `b/*_results.json`.
Reproduce: `cd W/reviews/r30 && W/locks/run_slot.sh PY b_keys.py` (and `b_rounds.py`, `b_readings.py`,
`b_table.py`, `b_corpus.py`), with PY the Python interpreter of the review.

### B.1 The diff, hunk by hunk (everything outside the marked additions)

`diff W/SPEC.md W/SPEC_v3.0.md` has 37 hunks. Outside the passages marked (wx-cert-3):

| lines (3.0) | change | effect under "wx-cert-2" |
|---|---|---|
| 3-11 | version note | none (not normative). Its item (5) is not complete, see B.5 |
| 22-25 | THE TWO SCHEMAS | defines the marking; none |
| 68, 111, 535-536 | counts for seventeen labels (erratum F3) | none; both checkers read it so |
| 264-266 | name OPT-AVAILABLE for "the round has an `opt` declaration of it" | none: it is the rule of 2.6 section 10 ("An `opt` declaration makes the four `opt:` facts ... available iff ..."; "undeclared pairs carry no `opt`/`par` facts"). Tested: `b/R_n03_opt_undeclared_E.jsonl` FAIL, FAIL |
| 443-512 | STEP paragraph rewritten | none, proof in B.2 |
| 446-447 | new sentence "The same name may occur more than once in a term", not marked | none: both frozen checkers accept it (`b/R_n15_repeated_name_E.jsonl`, `R_n15b_repeated_name_x3_E.jsonl`: PASS, PASS; reading A12 of the Node checker) |
| 513-515 | REJECTION names the term rules | none: (T1) was a well-formedness rule of 2.6 (line 479 of `SPEC.md`), (T4) the old "not available" |
| 601-634 | section 8 with centres | none: "always under the schema wx-cert-2, gamma_i is the identity" (line 603-604); with the identity the two tests are the tests of 2.6 (conj(1,0) * X = X). The proofs are longer and close a gap of 2.6 (A.5) |
| 608-609 | new sentence on the choice of the side direction | none (it repeats section 11 item (3)) |
| 644, 652 | "wx-cert-2" or "wx-cert-3" | a header with "wx-cert-3" is no longer rejected by a 3.0 checker (it was the 2.6 test `checker/v26/testcerts/fail/F36.jsonl`); nothing changes for a header with "wx-cert-2" |
| 654-661 | SCHEMA RULE | tested, B.4 |
| 662-667 | KEYS | tested, B.4: states what both frozen checkers do |
| 670-672 | "JSON integer", `S_floor` by value (errata) | none |
| 695-697 | "1 to 3 names (fact names and, (wx-cert-3), ...)" | none |
| 719-725 | last item of WELL-FORMEDNESS rewritten | tested, B.4: agrees with both frozen checkers where it decides; it does NOT decide several cases, and one case reads the other way (B-2) |
| 806-818 | section 11 first paragraph (errata F1, F4) | none for a checker |

Sections 2, 6 and 7 are unchanged word for word, as the version note says (no hunk between lines 74-107 and
none between lines 544-598 of 3.0).

### B.2 The rewritten STEP paragraph gives the number of 2.6

Claim: for a certificate without (wx-cert-3) elements, a step is accepted under 3.0 iff it is accepted under
2.6, with the same L.

Proof. (i) Terms. 2.6: "a list of TERMS (lambda_k, [fact names]), each with 1 to 3 fact names. lambda_k must be
>= 0, except that a term whose fact list contains a `circ` fact may have a multiplier of either sign" and "a
term that names a fact that is not available in its round ... rejects". 3.0: 1 to 3 names; (T1) is the same
sign rule; (T2) and (T3) are marked (wx-cert-3) and concern `pol` names and IND-LISTED options, which do not
exist; (T4) for the names of 4.0 to 4.4 and 4.6 to 4.8 is "by the rules stated there" (unchanged sections) and
for an `opt` name "iff its option is OPT-AVAILABLE", the rule of 2.6. (ii) Rem. Both texts:
Rem = g - sum_k lambda_k * prod(polynomials of the names of term k), a polynomial in the base variables (no
indicator exists). (iii) L. 2.6: "for Rem = sum_m r_m m(x) (m ranging over monomials, including the constant
monomial 1 with interval [1,1]), L := sum_m min(r_m * lo_m, r_m * hi_m), where [lo_m, hi_m] is the product, by
interval multiplication, of the store-bound intervals SB of the base variables of m, a variable of exponent e
being multiplied e times." 3.0 RAW RULE (lines 465-468): the same sentence with "(like monomials combined ...)"
added, which is what "Rem = sum_m r_m m(x), m ranging over monomials" means. A step of a "wx-cert-2"
certificate has no `centre` (it would be an unknown key), so the raw rule applies. (iv) Acceptance (lines
509-512) is unchanged. QED.

Check by experiment: my own calculator `r30/refcalc.py`, written from the 3.0 text alone, gives the L that
the prototype reports for the steps of a 2.6 test certificate (8 steps of
`checker2/v26/inputs/B_t2_iii_terminal.jsonl` with names in my subset: equal as rationals), and on the whole
2.6 corpus the prototype and both frozen checkers give the same verdicts (B.6).

### B.3 The errata are in

F1 (section 11, lines 806-811), F2 (version note, line 11: "section 0 ..., one sentence in section 1, three
sentences in section 7 ..., the header rules of section 10 and the first paragraph of section 11"), F3 (lines
68, 111, 535-536), F4 (lines 811-818), "JSON integer" and `S_floor` (lines 670-672): all present, with the
wording of `SPEC_v2.6_ERRATA.md`. (The erratum F5 that the lead added during the review, on my finding B-1, is of course
not in the audited text.)

### B.4 Experiments: KEYS, rounds that are not evaluated, the schema rule

**KEYS** (`b_keys.py`, 67 certificates, one change each, schema "wx-cert-2"; bases: the 11-node tour
`checker2/v26/inputs/B_t2_v_tour.jsonl` and three one-node certificates). An unknown key in each of the 23
kinds of object that the KEYS item lists (header, window, terminal, node, node arc entry, opt and ysign
assumption, round, opt and par declaration, step, store, store arc entry, store rarc entry, the split object of
each of the four types, a listed option, each of the four forms of `close`); a key that the format gives for
ANOTHER variant of the same object (`kappa` or `cls` in an opt declaration, `o` in a par declaration, `pair`
or `children` in a terminal closure, `how` in an infeasible closure, `pair` in a box split, `sign` in an opt
assumption, `c` in a store arc entry); every key that is not marked optional left out; malformed terms.
Result: **the text, the Python checker and the Node checker agree on all 67** (and the prototype). In
particular every key of the format blocks that is not marked "optional" is REQUIRED by both checkers
(`assume`, `rounds`, `parent`, `pairs`, `steps`, `store`, `rarc`, `cuts`, `terms`, `lo`/`hi` of a rarc entry),
which is what "exactly the keys ..., optional ones possibly absent" says.

One point where the text is looser than the checkers: `kappa` in a P+ declaration. Line 763 says "ignored for
P+, P-"; both checkers accept a well-formed `kappa` there (`b/K33`), and both REJECT a malformed one
(`b/K34_parPplus_kappa_malformed.jsonl`, `b/K35_parPplus_kappa_null.jsonl`: FAIL, FAIL). A reader of "ignored"
would accept those two files. (Decision 7 of the lead; MUST-6.)

**Rounds that are not evaluated** (`b_rounds.py`, 76 variants in two arrangements = 152 certificates; base:
the one-node certificate `B_t2_i_root_wall.jsonl`, closed by an accepted `0` step; arrangement N puts the
variant round AFTER that step, so it is not evaluated; arrangement E puts it before, as a control).
Result: **the two frozen checkers agree on all 152** (and the prototype with them). Against the text of lines
719-725:

| what stands in the round that is not evaluated | both checkers | the text of lines 719-725 |
|---|---|---|
| unknown name pattern; label 4; i > j; o = t; bad number; negative multiplier without `circ`; 0 or 4 names; unknown key; a `sq`/`pol`/`ind` name, mode "ind", form `q:..` (schema rule) | reject | reject ("name patterns", "shape", (T1)) |
| a `cut` fact without its cut; `opt`, `par` name without declaration; `wsup` of a tilted square; a multiplier 0 on an unavailable name | accept | accept ("availability (T4) of every other name") |
| `asg` name without the sign assumption (`R_n06_asg_no_assumption_N`) | accept | not decided: it depends neither on "the store of a round" nor on "the declarations of a round" |
| a declaration whose precondition fails (`opt`, `par`, also kappa < 0) | accept | accept |
| a step that is not accepted; a `0` step with value <= 0; a store entry that is not implied; a store interval with lo > hi; a proposed endpoint with cos <= 0 (`R_t04*`, `R_t10*`) | accept | accept for the first four; "cos > 0 required" (line 522) is not mentioned |
| `u:NAME` not defined, in an objective, in a `cut`/`ivl` name, in a cut key (`R_n07`, `R_n08`, `R_n09`, `R_t06c`) | reject | not in the list "this covers ..."; a reader who takes the list as complete lands on "availability of every other name": accept |
| `arc:i:tan:G:H`, `rarc:i:j:tan:G:H` with G^2 + H^2 > 1 (`R_n10`, `R_n10b`) | reject | by (T4) such a name is "not available by the rules stated there" (4.2), hence evaluated rounds only: **accept**. Text and checkers differ (B-2) |
| `ivl:u:NAME` of a custom form that is not affine (`R_n11c`) | reject | reject if the list of FACT names (line 790) is read as the pattern |
| a second `par` declaration for the same (i, j, cls, kind) (`R_d05`) | reject | line 698 is an item of WELL-FORMEDNESS, so reject; not in the list "this covers" |
| a Pk declaration without `kappa` | reject | reject ("shape of every declaration") |
| a step on the form `0` with sense "hi" (`R_s02*`), also in an EVALUATED round | reject, as malformed | **no rule at all** (B-1) |
| a store with a missing label, a rotation that is not unit, a bad cut key, a cut key `0:lo` | reject | reject (format) |

**The schema rule** (`b_keys.py` K24-K26, `b_rounds.py` n24-n26, d07, s07, `d_misc.py` cert2_*): a `centre`
in the window, the tube or a step, a `q:` key of `forms`, the mode "ind", a name `sq:`, `pol:`, `ind:`, the
objective `q:..`, all under "wx-cert-2": rejected by both frozen checkers and by the prototype, in evaluated
and in not evaluated rounds. The key `q` (no colon) is a custom form under both schemas (accepted by all
three).

### B.5 Findings of part B

**B-1 (MUST-1; inherited from 2.6; an unsound reading of the text).** Lines 771-773: "Sense "hi": claims
form <= value; accepted iff -value <= L computed with g = -form. Form `0`, sense "lo": accepted iff
L >= value > 0; it is evidence for the closure "infeasible"." Lines 541 and 779-780 then use "an accepted `0`
step" as the trigger that ends the evaluation of a node and as THE evidence of the closure
`{"kind":"infeasible"}` ("accepted iff ..."). Nothing says that a step on the form `0` must have the sense
"lo". Read literally, the step `{"form":"0","sense":"hi","value":"0","terms":[]}` has g = 0, Rem = 0, L = 0, is
accepted by the "hi" rule (-0 <= 0), is "an accepted `0` step", and closes ANY node as infeasible. Only
section 7 (a) ("a step with objective `0` and L > 0") contradicts this, and section 10 says "iff".
Both frozen checkers reject a `0` step with sense "hi" as malformed, everywhere (their recorded readings R5 and
A1), and so does the prototype. Files: `r30/d/F01_zero_hi_value0_3.jsonl`, `F01_zero_hi_value1_3.jsonl` (schema
3) and `..._2.jsonl` (schema 2): a root that contains the feasible reference point (checked exactly,
`r30/refgeom.py`), a tube that does not contain it, one such step: FAIL, FAIL, FAIL with "a step on the form 0
must have sense lo". The hole is in the wording only; the fix is one sentence (part F).

**B-2 (MUST-2, MUST-8).** The new last item of WELL-FORMEDNESS (lines 719-725) is announced as "what both
checkers of version 2.6 enforce" (version note, item (5)). It is that for everything it names, but (a) its
list "this covers ..." is not complete, (b) its criterion "what depends on the store of a round, or on the
declarations of a round being valid" does not classify `asg` (depends on the assumptions), and (c) for the
tangent names it gives, read with (T4), the opposite of what both checkers do. See the table above.

**B-3 (MUST-13; the two frozen checkers differ).** A node whose id is the empty string:
`r30/b/X_empty_id.jsonl` (one node, `"id": ""`, header `"root": ""`) and `r30/b/X_empty_id_leaf.jsonl` (the
tour with one leaf renamed to ""): **Python checker FAIL ("empty node id"), Node checker PASS.** The text
(line 738, `"id":"..."`) does not decide. This is the only certificate of my tests, and of the 1801 files of the
corpus, on which the frozen checkers disagree. It cannot make a false statement accepted. The prototype
follows the Python checker. The text of 3.0 must decide (I propose: an id is a non-empty JSON string).

**B-4 (the version note, item (5), is not complete).** It says "Two rules that both checkers of version 2.6
enforce and that its text did not state are now stated". By the checkers' own notes and my tests there are
more; the full list is B.7.

### B.6 The whole corpus

`b_corpus.py`: all 1801 test certificates that exist in the folder (`checker/v26/testcerts` 358,
`checker2/v26/inputs` 228, `checker/testcerts` 531, `checker2/testcerts` 684; every one "wx-cert-2"; 140 PASS
and 1661 FAIL under the Python checker), each run through the two frozen checkers, the prototype, and the
prototype again after replacing the schema string by "wx-cert-3". Log: `b/corpus_run.log`, table:
`b/corpus_results.json`.

- Python 2.6 = Node 2.6 on all 1801.
- prototype = Python 2.6 on 1800; the one difference is `checker/v26/testcerts/fail/F36.jsonl`, whose defect IS
  the schema string "wx-cert-3" (a 17-label certificate without new elements): FAIL under 2.6, PASS under 3.0,
  as intended.
- prototype with "wx-cert-2" = prototype with the string replaced by "wx-cert-3" on all 1788 files in which
  the string occurs (line 659-660: "A certificate that uses none of these elements is checked in the same way
  under either string").

This says nothing about the text by itself; it says that the one program that implements the 3.0 text did not
change a verdict of 2.6.

### B.7 The readings of the two frozen checkers, row by row, against the 3.0 text

Sources: `checker/CHECKER_NOTES.md` section 4 (R1-R13 and "two
properties"), `checker/v26/NOTES_V26.md` sections 6.1-6.5 and 9.3, `checker2/CHECKER2_NOTES.md` section 4
(A1-A18 and "observations"), section 7 and section 9.5 (B1-B3). "alike" = my test shows the same verdict from
both frozen checkers (file in `r30/b/`); "corpus" = no test of my own, the only evidence is that the two
checkers never differ on the 1801 files of B.6; "3.0" = what `SPEC_v3.0.md` says. STATED = the text now says what
the checkers do; SILENT = the text does not say it; DIFFERENT = the text says something else. Every SILENT or
DIFFERENT row with "alike" has its wording in part F.

| row | the rule both checkers implement | alike (test) | 3.0 | part F |
|---|---|---|---|---|
| R1 = A2 | the round that contains an accepted `0` step is evaluated completely (later steps, proposed store); only LATER rounds are skipped | yes: `X_same_round_bad_step_after_zero`, `X_same_round_bad_store_after_zero` FAIL, FAIL | SILENT (line 541-542 unchanged) | MUST-3 |
| R2 = A3 | closure with "pair" needs the pair test on a final store that is not EMPTY | corpus | STATED (lines 779-782, since 2.5.1) | - |
| R3, A6 | `kappa` on P+/P-: may be absent; if present a well-formed number, value ignored. Required for Pk and Ps | yes: `K33` PASS; `K34`, `K35` FAIL; `K64`, `X2_parPs_no_kappa` FAIL | half STATED ("ignored", line 763); SILENT on well-formedness | MUST-6 |
| R4 = A5 | a key that the format does not define is rejected, in every object | yes: 41 files `K01`-`K26`, `K30`-`K44` | STATED (KEYS, lines 662-667) | - |
| R5 = A1 | a step on the form `0` must have sense "lo"; "hi" is malformed (whole file) | yes: `R_s02*`, `d/F01*` | SILENT, with an unsound reading | MUST-1 |
| A1, 2nd half | a `0` step with value <= 0 is not accepted (rejects where evaluated) | yes: `R_s03*` | STATED in line 772-773; the general sentence of section 5 (line 510-511) says "lo: value <= L" without the exception | MUST-1 |
| R6 = A7 | a custom form has at least one component | yes: `X_empty_custom_form` FAIL, FAIL | SILENT (and for `q:` forms the text says "nonempty", line 139) | MUST-5 |
| R7 | in rounds that are not evaluated: syntax, names, labels, pairs, unit rotations, tangent length, multiplier signs, 1 to 3 names, one `par` declaration per key, custom form names defined, `ivl` only for affine forms; availability, preconditions, acceptance only in evaluated rounds | yes: 152 files `R_*` | PARTLY STATED (lines 719-725); the list is incomplete; DIFFERENT for the tangent length | MUST-2, MUST-8 |
| R8 = A9 | header: every window and tube interval has lo <= hi; every alpha > 0; window alpha < 1; tube alpha <= 1; all tested when the header is read, also in a tree without a terminal node | yes: `X_tube_alpha_2_no_terminal_leaf`, `X_tube_alpha_0`, `X_tube_alpha_negative`, `X_window_alpha_0`, `X_window_alpha_1`, `X_tube_interval_inverted`, `X_window_interval_inverted` FAIL, FAIL; `X2_tube_alpha_exactly_1`, `X2_window_interval_point` PASS, PASS | SILENT on lo <= hi and on alpha > 0 as a test; DIFFERENT in place for alpha <= 1 ("Requires" stands inside the terminal test, line 626: a tree without a terminal node never makes that test) | MUST-4 |
| R9, A6 | `rarc` and `cuts` are required keys of a store (may be empty); `lo`, `hi` required in a rarc entry (may be null); `id, parent, S, box, arc, assume, rounds, close` required in a node; `pairs, steps, store` in a round | yes: `K51`-`K60` | STATED through KEYS (not marked optional = required) | - |
| R10 = A15 | the options of an option split need not be pairwise different (one child each); an excluded option may be listed; an `opt` declaration may be repeated in a round | yes: `X2_optsplit_option_twice`, `X2_optsplit_excluded_option_listed`, `X_opt_decl_twice_evaluated` PASS, PASS | SILENT (the literal text allows it; `ind` lists say "pairwise different") | MUST-11 |
| R11 = A11, Node section 7 | JSON lines only: header on line 1, one node per line; at least one node; no empty line (also not at the end); JSON whitespace around the object and CR before LF allowed; final newline optional; UTF-8, no byte order mark | yes: `X_empty_line`, `X2_blank_line_at_end`, `X2_header_only`, `X2_two_objects_on_a_line`, `X2_trailing_garbage`, `X_bom`, `X2_invalid_utf8` FAIL, FAIL; `X_crlf`, `X_no_final_newline`, `X2_spaces_around` PASS, PASS | DIFFERENT: line 648 still offers "or one JSON file per node plus an index", which no checker reads and the text does not define | MUST-14 |
| R12 | a node id is a non-empty string | **NO: Python FAIL, Node PASS** (`X_empty_id`, `X_empty_id_leaf`) | SILENT | MUST-13 |
| R13, A16 | an EMPTY initial store cannot occur | - | nothing to state (shown in A, remark on line 102) | - |
| "two properties", A4 | no `rarc` name (also no `rarc:..:tan`) for a pair without effective relative arc; tested as availability, in evaluated rounds only | yes: `X4_rarc_slo_no_effective_arc_E`, `X4_rarc_tan_no_effective_arc_E` FAIL, FAIL; the same with `_N` PASS, PASS | STATED (4.3, line 222); where it is tested: MUST-2 | - |
| 6.2, B1, A13 | `labels`: the number token 16 or 17 | corpus (`checker/v26/testcerts/fail/A06`, `A17`-`A21`, `A26`, `A27`) | STATED (lines 670-672) | - |
| A13 | the same token rule for every JSON integer (labels in fields, `k`, `eps`, `sign`); map keys and labels in names are canonical decimal strings; numbers match the pattern exactly ("-0" and leading zeros are allowed by it) | yes: `X2_int_k_1p0`, `int_k_1e0`, `int_sq_1p0`, `int_eps_1p0`, `int_eps_true`, `int_sign_m1p0`, `int_i_string`, `int_o_big`, `int_minus_zero`, `map_key_leading_zero` FAIL, FAIL | SILENT for the fields (the explanation of "JSON integer" stands in the `labels` item only) | MUST-7 |
| 6.4 | keys are compared after decoding JSON escapes; so are all strings | yes: `X2_key_escape_repeated` FAIL, FAIL; `X2_key_escape_single`, `X2_value_escape_in_name`, `X2_number_string_escape`, `X2_sha_escaped` PASS, PASS | SILENT | MUST-15 |
| 6.1, 6.3, 6.5, B2, B3 | `S_floor`, the counts, the rattler's tube | - | STATED (errata F1, F3, F4) | - |
| A8 | a contradictory cut pair makes the store EMPTY also for a base variable; SB of base variables never uses cuts | yes: `X2_cutpair_on_base_variable_empty` PASS, PASS (closure on that EMPTY store) | STATED (lines 98-101, 159-161, 175-179) | - |
| A10 | `Sref` is compared by value; the hash as a string | yes: `X_Sref_other_string` PASS, PASS; `X2_sha_uppercase`, `sha_mixed_case`, `sha_leading_space`, `sha_0x`, `sha_truncated` FAIL, FAIL | SILENT ("equals") | MUST-12 |
| A12 | a name that is not available rejects also when its multiplier is 0; a name may occur twice in a term | yes: `R_n27_zero_lambda_unavailable_E` FAIL, FAIL; `R_n15*` PASS, PASS | STATED for the second (line 446-447); for the first (T4) says "every name" without mentioning the multiplier | MUST-10 |
| A14 | assume lists are compared item by item; repeated items allowed | yes: `X2_assume_item_twice` PASS, PASS | STATED (line 560-561, literal) | - |
| A17 | order in which preconditions are tested | - | not a rule (only the printed reason) | - |
| A18 | a terminal or split node with an accepted `0` step is checked on the store after that round | corpus | STATED (lines 782-784) | - |
| observations | a certified value counts only for the exact form name and only in its round; `0` steps give no certified value; root conditions use the root's data, child rules the parent's final store | corpus | STATED (line 519; sections 6 and 7); for `0`: follows once no cut can be stored under `0` | MUST-9 |
| (mine) | no cut and no `cut` name under the form `0` | yes: `R_n16`, `R_t06b`, `X2_cut_stored_under_zero_after_zero_step` FAIL, FAIL | STATED for the fact name (lines 197-198, 791); SILENT for the key of `cuts` | MUST-9 |
| (mine) | `asg` availability is tested in evaluated rounds only | yes: `R_n06` N: PASS, PASS; E: FAIL, FAIL | SILENT | MUST-2 |
| (mine) | in a proposed store of a round that is not evaluated only the format is tested; cos > 0 and lo <= hi are acceptance | yes: `R_t03`, `R_t04`, `R_t04b`, `R_t05`, `R_t10`, `R_t11` | SILENT | MUST-2 |
| (mine) | a gzip-compressed file of the same lines is read by both | yes: `X2_gzip.jsonl.gz` PASS, PASS | SILENT (the real certificate is a `.gz`) | MUST-14 |
| (mine) | both programs pin the SHA-256 of the packing file by default (options `--expect-packing-sha256`, `--no-packing-pin`) | - | not in the text: the text asks only for header hash = hash of the file read | SHOULD-6 |

Counted: of the rows where the text is silent, loose or different and the checkers agree there are 14; one
row where the checkers disagree (R12).

## Part C. Ambiguity

Result of part C. **Each of the four additions is determined by the text: I found one reading for every
sentence of 4.9, 4.10, the term rules, the two rules for L and section 8, and I could compute L from the text
alone and got the prototype's number every time (C.2).** What is not determined is (a) the new last item of
WELL-FORMEDNESS (lines 719-725), which is the one new sentence with two readings, and (b) sentences inherited
from 2.6 that the frozen checkers read in one way and the text leaves open (table B.7). Exact wording for all of
them is in part F.

### C.1 What the text fixes for each new rule

| rule | tested | on which data | text |
|---|---|---|---|
| shape of a `q:NAME` form (nonempty list; entries [number, list of 0 to 2 base variable names]; monomials pairwise different as multisets; coefficient 0 allowed) | whole file | the node's `forms` | lines 138-151, 703-708 |
| `sq:NAME`, `pol:NAME` need `q:NAME` in the node's own `forms` (not the parent's) | whole file | the node | lines 386-387, 692-693, 721-722 |
| (T1) sign, (T2) `pol` only with `circ` in the same term | whole file | the term | lines 449-450, 720-721 |
| shape of an `ind` declaration (keys i, j, mode, options; 1 to 8 options, pairwise different, each of the pair) | whole file | the declaration | lines 394-396, 709-710 |
| (R1) one `ind` declaration per pair and round, (R2) no `opt` and `ind` declaration of one pair in a round, (R3) no `ind` declaration of a pair with an option assumption in the node's `assume` list | whole file | the round; the node's `assume` | lines 397-401, 710-713, 721 |
| validity of an `ind` declaration (every option not listed is excluded, 4.7) | evaluated rounds, also if no step uses it | the store at the START of the round | lines 404-408, 722-723 |
| `ind:i:j:k` available: `ind` declaration of the pair in the round and k <= m | evaluated rounds | the declarations of the round | lines 413-414, 459-460, 723-724 |
| a corner name available: option OPT-AVAILABLE or IND-LISTED in the round | evaluated rounds | the declarations of the round | lines 457-458 |
| (T3) guard: a corner name of an IND-LISTED option O_k needs `ind:i:j:k` (that k) in the same term | evaluated rounds | the declarations of the round | lines 451-455, 724 |
| shape of `centre` in a step (object; keys base variable names; values numbers) | whole file | the step | lines 714-717, 720 |
| L: RAW RULE without `centre`, CENTRED RULE with it (also `{}`) | evaluated rounds | SB of the base variables from the START store; [0,1] for indicators | lines 465-479 |
| identity of the indicator variables: z_{ij,k} belongs to the k-th listed option, k < m; the m-th option has 1 - z_{ij,1} - ... - z_{ij,m-1}; for m = 1 the constant 1 | - | the list order | lines 409-412, 769-770 |
| `centre` maps of the header (exactly the keys of I; unit rotations; independent for window and tube) | header | - | lines 673-675 |
| root test and terminal test with centres | tree pass | root data; final store | lines 610-614, 623-626 |

The pattern of every new name is closed: `q:NAME` and so `sq:NAME`, `pol:NAME` with NAME in [A-Za-z0-9_]+
(line 138; the list of FACT names, line 792, does not repeat the pattern: SHOULD-3); `ind:i:j:k` with i < j in
I, written without sign or leading zeros, and k ONE digit 1 to 8 (lines 683-684, 792-793); the `centre` keys
`xi:i:k`, `S`, `C:i`, `s:i` (lines 715, 796).

Lists and special values, as the text has them: an `ind` list is nonempty and without repetition; a `q:` form
is nonempty, a monomial may not repeat, a coefficient may be 0; `terms` may be empty, the names of a term may
not; a name may repeat in a term; a term may repeat in a step; the multiplier 0 is allowed and does not excuse
anything (T1 to T4 speak of "a term", not of its multiplier; the lead's decision 3 makes this explicit);
`centre` may be `{}`; a value for a variable that does not occur has no effect; like monomials of Rem are
combined, so a monomial that cancels contributes nothing. An unknown name in a round that is not evaluated
rejects (name patterns are whole-file). All of this is what the prototype does (D.3, D.6).

The order of events in an evaluated round is fixed, but only by sentences that stand in four places (lines
175, 404-405, 517-519, 541-542). As I read them: (1) the start store is the node's data (round 1) or the
store accepted in the round before; it is not EMPTY (else the round is not evaluated); (2) every declaration
of the round is tested on that store, and a failing one rejects the certificate; (3) every step is computed
with the facts and SB of that same store and must be accepted; (4) every entry of the proposed store must be
accepted, using only the old store and the certified values of the steps of THIS round; (5) if the new store
is EMPTY, or the round contained an accepted `0` step, no later round is evaluated. Tested on the prototype in
D.3 (`O_order_*`): a declaration that is valid only on the store that its own round produces is rejected, the
same declaration one round later is accepted. I ask that this sequence be written once (MUST-3 contains it).

### C.2 L is determined: an independent computation

`r30/refcalc.py` is my own program for L, written from sections 1 to 5 of the text and from nothing else
(exact rationals; polynomials as dictionaries; the names `box`, `side`, `arc:*`, `circ`, `wall`, `opt`
corners, `sq`, `pol`, `ind`; objectives `xi`, `S`, `C`, `s`, `Da`, `Db`, `A`, `B`, `Cr`, `Sr`, `0`; both rules;
also the exclusion test of 4.7 on a first-round store). While writing it I met no place where the text left
me a choice. Comparison with the prototype's reported L (`--proto-report --json`; scripts `d_allow.py`,
`d_allow_more.sh`, `d_true.py`; certificates `d/L_compare*.jsonl`):

- 994 steps with random terms of every shape the term rules allow (guarded corners with a third name, two
  corners of one option with one guard, the guard twice, indicators alone up to the third power, `sq` up to
  `sq*sq*sq`, `circ` terms with negative multipliers, `pol`, guarded corners inside a `circ` term), seven `ind`
  declarations with m = 1, 2, 3, 3, 4, 8, 8 and lists that contain excluded options in every position, 705 steps
  with a `centre` (empty, partial, with values far outside the store interval, with keys of variables that do
  not occur): **L equal as a rational number in all 994** (numerators of several hundred digits).
- 96 threshold tests: value = L accepted, value = L + 10^-40 rejected, all as expected.
- The steps of two true proofs that need indicators (D.5): equal.
- The exclusion test: my 4.7 and the prototype's agree on every declaration I tried (which options may be left
  out), including the two-round order test.

- Against geometry, so that "mine = the prototype's" is not a shared misreading (`r30/geom_check.py`, exact
  rationals, node centres rho_i different from the identity, 40 random configurations): my polynomials for
  the corner coordinates (`wall`, 3,840 values), for `Da`, `Db`, `A`, `B`, `Cr`, `Sr` (2,880 values) and for
  the corner polynomials of all 8 options of 480 pairs (15,360 values) equal the quantities they stand for
  (the coordinate of the corner, a_o.(q_t - q_o), n.(corner - q_o) - 1/2, ...); `circ` is 0; an option holds
  iff its four corner polynomials are >= 0. 0 mismatches. In the same script the SAT lemma of 4.5, on which
  the LIFTING LEMMA rests: for 6,000 pairs of unit squares with rational directions (2,000 touching exactly
  along a side of one of them, 2,000 moved in or out by 10^-6) "the area of the intersection is 0" (computed by
  clipping, without any option) holds iff one of the 8 options holds: 0 violations.

Together with the lead's statement that the second checker reproduces the prototype's L on the 81 leaves of the
real certificate, three implementations from the same text give the same numbers (my own recomputation of the
real leaves: E.3).

### C.3 The new sentence with two readings

**Lines 719-725** ("Well-formedness is checked on the whole file ...; this covers ... What depends on the
store of a round, or on the declarations of a round being valid, is tested in the evaluated rounds only: the
precondition of every declaration, the availability (T4) of every other name, including k <= m for
`ind:i:j:k`, and, (wx-cert-3), the guard rule (T3).")

- Reading 1: the two lists are complete; a test that is in neither falls under "availability (T4) of every
  other name" if it concerns a name, and is otherwise undefined. Then in a round that is not evaluated an
  undefined `u:NAME`, a `tan` name with G^2 + H^2 > 1 and an `ivl` name of a form that is not affine are NOT
  rejected, and a second `par` declaration with the same key is undecided.
- Reading 2: every item of WELL-FORMEDNESS above it is whole-file (first sentence), the list "this covers"
  only gives examples; the second list is complete.
- Both readings are sound (a round that is not evaluated contributes nothing to a proof). They give different
  verdicts. Both frozen checkers and the prototype follow reading 2, with `tan` length and `ivl`-affinity
  taken as part of the NAME, and with `asg` availability in the second list.
- A third trap is in the lead's decision 2 as it was put to me ("only what depends on a store is tested in
  evaluated rounds only"): the guard rule (T3), "the pair has a declaration in the round", k <= m and the
  availability of `asg` do not depend on a store, yet the text, the prototype and (for `opt`, `par`, `asg`)
  both frozen checkers test them in evaluated rounds only (`b/R_n03_opt_undeclared_N`, `R_n04_par_undeclared_N`,
  `R_n06_asg_no_assumption_N`: PASS, PASS; `d/O_nev_T3_unguarded_corner_N`, `O_nev_ind_undeclared_pair_N`,
  `O_nev_ind_k_beyond_m_N`: PASS). The replacement must name the two classes rule by rule, not by a criterion.
  Wording: MUST-2.
- The sentence "A step may only use facts that are available in its round" stands inside the list of
  WELL-FORMEDNESS (line 691-692) although it is an availability rule. With "every item of WELL-FORMEDNESS is
  whole-file" it would contradict itself. MUST-2 moves it.

### C.4 Inherited sentences with two readings

These are the SILENT and DIFFERENT rows of table B.7. For each, both readings are sound except the first:

| sentence | reading of both frozen checkers | other reading | sound? | part F |
|---|---|---|---|---|
| lines 541, 771-773, 779-780: "an accepted `0` step" | a `0` step must have sense "lo" | a `0` step with sense "hi" is accepted by the general rule and counts | **the other reading is UNSOUND** | MUST-1 |
| line 541-542: "later rounds ... are not evaluated" | the round with the `0` step is evaluated completely | evaluation stops at the `0` step | both | MUST-3 |
| lines 601-602, 614, 626: alpha > 0, "Requires" | tested at the header for every label | tested where the root or terminal test is made | both | MUST-4 |
| line 135-136: "a rational linear combination" | nonempty | an empty sum (the zero form) is allowed | both | MUST-5 |
| line 763: kappa "ignored for P+, P-" | must be well formed if present | anything | both | MUST-6 |
| lines 677-678, 682: "JSON integers" | number token without fraction or exponent | any JSON number with an integer value (5.0, 5e0) | both | MUST-7 |
| line 211: "(checked)" | part of the name | part of availability | both | MUST-8 |
| line 758: keys of `cuts` | no key for the form `0` | `0:lo` is a key | both (a cut 0 >= v needs v <= 0 unless F(N) is empty) | MUST-9 |
| lines 555-556, 763-764: lists of options, `opt` declarations | may repeat | must be different | both | MUST-11 |
| line 652-653: "equal" | hash: string of 64 lowercase hex digits; Sref: by value | case-insensitive; Sref as a string | both | MUST-12 |
| line 738: `"id":"..."` | Python: non-empty. Node: any string | - | both | MUST-13 |
| line 647-648: "JSON lines, or one JSON file per node plus an index" | JSON lines only, details in B.7 | an index format | both | MUST-14 |
| line 718: "a repeated key" | after decoding escapes | byte-wise | both, but a parser that keeps the last of two keys it thinks different could read another certificate than the other checker | MUST-15 |

## Part D. Attack

Result of part D. **The prototype accepted nothing that the text forbids and nothing false, and it rejected
nothing that the text allows**: 0 unexpected verdicts in 635 prototype runs on certificates of mine (54 false
ones; 4 certificates with 994 steps and 96 threshold runs; 79; 37; 17; 32; 309; 7; listed below; and 14 single
files `d/F0*`, `d/T00*`, `d/M_dropped_*`), on top of the runs of part B. Two verdicts that first looked unexpected were errors in my own files (a wrong guard index in
`T_T4`, a wrong corner in a 2.6 test) and are corrected in the scripts. The only false certificate that the TEXT
admits is the one of B-1, and no program accepts it.

All files are in `W/reviews/r30/d/`; each script prints a table and writes `d/*_results.json`. The prototype
was used as a black box only (`cd W/proto30 && PY wxproto30b.py CERT [--json OUT --proto-report]`).

### D.0 How a false statement is made here

`r30/attack_base.py`, `false_base()`: one node, the root "n" of `checker2/v26/inputs/B_t2_v_tour.jsonl`
(every xi within 1/100 of the reference point, every direction within about 1/1000 of u_i, S in [4, Sref]),
with a tube whose interval for xi_{1,1} is [1/200, 1/50]. The reference point xi = 0, a_i = u_i, S = Sref is
feasible, checked with exact rationals for sixteen and for seventeen labels (`r30/refgeom.py`: all corners in
[0, Sref]^2, every pair separated by one of its 8 options), it lies in the window and not in the tube. So
(ANN) for this header is FALSE, and any accepted certificate with this header proves a false statement; the
only way is to close the root as infeasible. In this window the pair 1-3 has two options that are not excluded,
(1,3,a,+) and (3,1,a,-); the option (1,3,a,-) "square 3 lies to the left of square 1" is false, and its corner
polynomials are about -1 and -2 on the whole box. The pair 5-9 has one option that is not excluded, (5,9,b,+),
and (5,9,b,-) is false with corner polynomials below -0.9. (Exclusion computed with my own 4.7 in
`refcalc.py`; the tour certificate's option split confirms it for the pair 1-3.)

The true twin ("a closure that is true only because of an option assumption"):
`d/T_twin_closure_by_assumption_2.jsonl` is the same root with the true tube, split on the pair 1-3 into three
children; the child that ASSUMES the false option (1,3,a,-) is closed by the one step
`0 >= 1/100` with the term `[1, opt:1:3:a:m:p:p]`. All three programs accept it, rightly: under that assumption
the node is empty. Every file of D.1 with a name `A_G*` tries to put this same step into the root, where
nothing is assumed, by means of indicators.

### D.1 Fifty-four false certificates (`d_attack.py`, files `d/A_*.jsonl`)

Each closes the root by ONE `0` step. The column "L if the rule is ignored" is the L that my own calculator
gives when the named rule is switched off: where it is > 0, a checker that forgets the rule ACCEPTS the false
statement. All 54: prototype FAIL, each with a reason that is the rule I name.

| file | the trick | rule of the text that rejects | L if the rule is ignored |
|---|---|---|---|
| `A_G1_short_list` | list = the false option alone, its corner with the guard `ind:1:3:1` (= 1) | 4.10 PRECONDITION | +1.98 |
| `A_G1b_short_list_one_missing` | one option that is not excluded left out | 4.10 PRECONDITION | -0.04 |
| `A_G2_no_guard` | valid list of three, the false corner without a guard | (T3) | +1.98 |
| `A_G3_guard_of_other_pair_const` | guard = the constant indicator of another pair's one-option list | (T3) | +1.98 |
| `A_G4_partition_of_unity`, `A_G4b_*` | the false corner three times, "guarded" by each of the three indicators of its pair (they sum to 1) | (T3) "with THAT k" | +1.98 |
| `A_G11_guard_is_eliminated_other` | the same with a list of two: z and 1 - z | (T3) "with THAT k" | +2.39 |
| `A_G5_unlisted_option_const_guard`, `A_G5b_*` | corner of an option that is NOT listed, with the indicator of the listed one | (T4) for the `opt` name | +2.39 |
| `A_G6_opt_and_ind_same_pair`, `A_G6b_*` | a valid `opt` declaration of the true option next to an `ind` declaration that lists the false one; the false corner without guard | (R2) | +2.39 |
| `A_G7_two_ind_declarations` | two lists for one pair | (R1) | - |
| `A_G8_guard_from_other_round`, `A_G8b_corner_from_other_round` | indicator or listed corner of the round before | (T4), (T3) | - |
| `A_G9_two_corners_one_guard` | two corners, one indicator | (T3) | - |
| `A_G10_index_beyond_list`, `A_G12_pair_written_reversed`, `A_G13_ind_with_duplicate_option`, `A_G14_option_of_other_pair_in_list`, `A_G15_empty_list` | malformed declarations and names | (T4) k <= m; name pattern; 4.10 | +2.39 for G13 |
| `A_P1_pol_without_circ`, `A_P1b_*`, `A_P1c_*` | `pol` of the form -1 without `circ`, with an indicator instead, with `circ` in another term | (T2) | +1 |
| `A_P2_negative_multiplier_sq`, `A_P2b_*`, `A_P2c_*`, `A_P9_*` | negative multiplier on `sq`, on `ind`, on a true guarded corner, on a product of facts | (T1) | +1, +1, +1.39 |
| `A_P3` to `A_P8` | `sq` of an undefined form; `pol:X` when only `u:X` exists; a `q:` form with a named form, three variables, a repeated monomial, no entry, label 4, a bad name; `q:` or `ind:` as objective; a cut on a `q:` form | 4.9, section 3, form NAMEs | - |
| `A_C1_*` (6 files) | a correct but useless step with a `centre` far outside the store interval (-100, +100, -1000, +1000 for xi, S, C, s) | none: L must be the same for every centre | L = -1/50, -0.6755, -7/25, -2/3610001: the prototype reports exactly these numbers |
| `A_C2_*` (7 files) | `centre` with the key of a named form, of `ind:1:3:1`, of `z:1:3:1`, of label 4; a float, null, a list as value | lines 714-717 | - |
| `A_C3_*` (3 files) | the CORRECT guard on the false corner (eliminated indicator, variable, everything at once) | none: accepted as terms, but L < 0 | -5.06, -0.021, -3.10 |

The rows with a positive number are the load-bearing rules: the precondition of the declaration, (T3) with
"THAT k", (T4) for corner names, (R2), (T1) and (T2). The prototype enforces each of them.

### D.2 What the text allows: L against an independent calculator (`d_allow.py`, `d_allow_more.sh`)

See C.2: on a TRUE statement (`true_base()`: the same root with the original tube, terminal without a round),
four certificates with 76 + 3 x 306 steps using every new element; all accepted; L equal to my calculator's in
all 994 steps; 96 threshold tests as expected.

### D.3 Order of events; rounds that are not evaluated (`d_rounds.py`, 79 files `d/O_*.jsonl`)

On a truly infeasible node (square 1 outside the container). (a) Order: a list for the pair 1-6 that is valid
only on the store produced by round 1 is rejected in round 1 (also when round 1 contains the step and the store
entry that make it valid) and accepted in round 2; the list that is valid on the node data is rejected in
round 2; two different lists for the same pair in two rounds are accepted. (b) Each new rule in a round that
is not evaluated and, as a control, in an evaluated one: (R1), (R2), (R3), (T1), (T2), an undefined `sq` form,
a malformed declaration, a malformed `centre`, the name patterns (k = 0, 9, 01; reversed pair; label 4) reject
in both; a failing precondition, (T3), k > m, an undeclared `ind` name, a step that is not accepted reject only
when evaluated. (R3) was tested in a two-node tree (the child assumes an option of 5-9 and declares `ind` for
5-9: rejected in both arrangements; `ind` for another pair: accepted). 79 of 79 as I read the text.

### D.4 Centres of the window and the tube (`d_header.py`, 37 files `d/H_*.jsonl`)

gamma = rotation by 2 atan(1/200) for label 1. Window, root centre and tube centre all at gamma: accepted; the
same arc written relative to the node centre 1 or gamma^2: accepted; a quarter turn everywhere: accepted. Root
at the identity or at conj(gamma) with the window at gamma, window at conj(gamma) with the root at gamma, a
half and a quarter turn between them: rejected by the root test (isolated in the files `H_iso_root_*`, where the
terminal test passes). Tube at the identity or at conj(gamma) with the node at gamma: rejected by the terminal
test. Format: a map without a label, with label 4, with a rotation that is not unit (also in a tree without
terminal node), null, a list, the key `centres`: rejected. 37 of 37 as I derive them from section 8.

### D.5 True statements that need the new elements (`d_true.py`, 17 files `d/T_*.jsonl`)

- `T_T1_indicator_bound_to_store`: at the tour's root, without any assumption, "Da:1:3 >= 9999/10000" in ONE
  step with the two indicators of the pair 1-3 and a centre at C = 1; the bound is stored as a cut and used in
  round 2; terminal. Accepted; L = 0.999935 equal to mine. With the raw rule the same terms give L = -0.080
  (`T_T1r_*`): this is the effect section 12 describes.
- `T_T2_true_infeasible_by_indicators`: a window with xi_{3,1} <= -1/500 is infeasible (either option of 1-3
  needs q_3x - q_1x >= 1 - 5e-5, the left wall needs xi_{1,1} >= -3e-7); neither option is excluded on the
  node data and no `opt` declaration is valid (`T_T2_opt_declaration_instead`: rejected); one `0` step with
  four guarded corners, two wall facts and one box fact closes it: accepted, L = 0.0019352 equal to mine;
  value = L accepted, L + 10^-30 rejected. The same step in the window without the restriction (the FALSE
  base) has L = -0.0101: rejected (`T_T2f_*`).
- `par` and `ind` declarations of one pair in a round with a `par` fact times an indicator; seventeen labels
  with label 4 in an `ind` declaration, in `circ:4`, in a `q:` form and in `centre` (the same file with
  sixteen labels is rejected); an `opt` declaration of one pair and an `ind` declaration of another, an
  OPT-AVAILABLE corner times a guarded one; a sign assumption on a pair together with an `ind` declaration of it;
  a one-option list used like an `opt` declaration (the two L are the same rational): all accepted.

### D.6 Leaks, the schema string, the precondition (`d_misc.py`, 32 files `d/M_*.jsonl`; `d_excl.py`, 309 runs; `d_store.py`, 7 files)

- A `q:` form, a `sq`, `pol` or `ind` name as component of a custom form, in a `cut` or `ivl` fact name, as key
  of `cuts`; `q:NAME` as a name of a term; a child using a `q:` form of its parent: all rejected. A custom
  form with the key `q` next to `q:q`: accepted.
- Schema strings "wx-cert-4", "WX-CERT-3", "wx-cert-3 " (trailing blank), "wx-cert-2.6", "", the integer 3,
  no key: rejected. Each new element under "wx-cert-2": rejected by the prototype and by both frozen checkers.
- The precondition of an `ind` declaration against my own 4.7, for all 120 pairs and 8 options on the node
  data of the true base: the 653 declarations "all options but one that my test excludes" are accepted (one
  certificate, 8 rounds), the 120 minimal lists are accepted, and each of the 307 declarations "all options
  but one that my test does NOT exclude" is rejected with a reason that names exactly that option.

- The store of the precondition (`d_store.py`, 7 files `d/S_*.jsonl`, on the truly infeasible node, verdicts
  derived by hand from 4.7): a CUT "A:3:1 >= -1/2" stored in round 1 makes (3,1,a,-) excluded, and the
  one-option list for the pair 1-3 is accepted in round 2, rejected in round 1, and rejected in round 2 if the
  cut is not in the store. A STORED RELATIVE-ARC ENDPOINT of the pair 2-6 (sine 0.012) together with a box
  entry (xi_{6,2} <= -7/1000) raises h_lo from 1/2 to 0.50596 and lowers U from 1.0204 to 1.0034, so that all
  8 options of 2-6 are excluded: a one-option list is accepted in round 2; rejected without the rarc entry,
  without the box entry, and in round 1. So the precondition reads "its box, arcs, stored relative-arc
  endpoints and cuts" of the START store (lines 405-406), as the text says.

### D.7 What I tried and could not turn into an attack

- The eliminated indicator. A bound that treated ind_m = 1 - sum z as a quantity in [0,1] would be wrong on
  the cube; I could not build a certificate on which such a bound would differ in SIGN from the correct one
  while the statement is false (with a correct guard a false corner contributes -corner * ind_m, bounded below
  by 0 under the wrong bound and by a negative number under the right one, never by a positive one). The
  comparison of L in D.2 is the real test: 8-option lists with all indices, the last index as guard, powers of
  the last indicator; equal in all steps.
- Sharing of indicator variables between pairs or rounds: would change L; none seen in D.2 (seven pairs in one
  round, same index on different pairs) or in D.3 (two rounds).
- I did not attack the arithmetic (big numbers, deep products) beyond degree 12 and beyond the numbers of the
  real leaves (rationals of about 2,300 digits, E.3).

## Part E. After reading the author's notes

Read only after parts A to D stood in this file: `proto30/PROTO_NOTES.md` sections 12 to 18 and
`proto30/SPEC_3.0_DELTA.md` parts A, C, D, E, F (not its part B, the superseded normative text). Still not
read: the prototype's source, the two drafts, the second checker.

**Result: nothing in the notes changes the verdict. I disagree with the author nowhere in the mathematics and
with myself in one remark (A-3, corrected in place).**

### E.1 The author's proof and mine

PROTO_NOTES 12.2 has the same proof as A.3/A.4: the conditions (D1) to (D3) on the lifted indicators, the
choice "smallest k such that O_k holds", "elimination is the same thing" (the polynomial 1 - sum z takes the
value ind*_m at z*), the term lemma by three kinds of factors, the step claim. The text of 3.0 is this proof
with the two elements removed that the lead dropped (the equality `ind:i:j:k:bin` and the lifted corner fact
`ind:i:j:k:E1:E2`). I had derived it before reading and found the same steps; there is no step where one of us
uses something the other does not.

### E.2 The author's list of decisions (DELTA part D; PROTO_NOTES 17) against my reading

| the author's point | final text | my assessment |
|---|---|---|
| D1 the last indicator is eliminated | lines 409-412 | sound; determined; tested in L (C.2) |
| D2 the list must CONTAIN every option that is not excluded and may contain excluded ones | lines 404-408, 436-439 | sound (A.3). The real certificate uses it: in 3 of the leaves I recomputed (X30, X33, X59) one listed option is excluded on the leaf's data by my own 4.7 |
| D3 the precondition on the store at the START of the round | lines 404-405 | sound and needed for a fixed order of events; tested in D.3 |
| D4, D5 `pol` and free sign with `ind:..:bin`; D6 centres of indicator variables; D7, D15 the lifted corner fact; D16 no guard in a `circ` term | dropped by the lead | the final text has none of them (lines 414-415, 453-455, 716-717) and the prototype rejects each: `d/M_dropped_ind_bin.jsonl`, `M_dropped_ind_bin_with_pol`, `M_dropped_ind_lifted_corner`, `M_dropped_centre_z`, `M_dropped_unguarded_corner_in_circ` FAIL; `M_dropped_guarded_corner_in_circ` PASS |
| D8 to D12 polynomial forms, name spaces, `centre` | section 3, lines 469-479 | as I read the text |
| D13 one `ind` declaration per pair and round; `opt` and `ind` of one pair were ALLOWED in the author's draft (the fact wins), forbidden by the lead | (R1), (R2), (R3) | both versions are sound. I had written in A-3 that (R2) is needed for the names to mean one thing; the author's draft shows it is a choice. Corrected in A-3 |
| D14 the node's assumptions do not enter the precondition | 4.10 "by the test of 4.7 exactly as it stands" | my remark A-3 |
| D17 m = 1; D19 no degree limit, names may repeat | lines 395, 411, 446-447 | A.3, A.4 |
| D18 the schema string | "wx-cert-3" adopted | tested (B.4, D.6) |

### E.3 What the author's self-audit calls untested, and what this review adds

| the author's "no test of its own" (PROTO_NOTES 17.5, DELTA part F) | here |
|---|---|
| (T3) and (T4) in a round after the first | D.1 `A_G8_*`, `A_G8b_*`; D.3 (79 files) |
| a term with indicators of two different pairs | D.1 `A_G3_*`, `A_G9_*`; D.2 (the random terms take indicators of any of seven pairs) |
| "the exclusion test of 4.7 as it stands" is by construction, not by a test | D.6: 960 (pair, option) cases against my own 4.7; the `ind` declarations of the real leaves below |
| SB = [0, 1] and ind_m = 1 - sum are definitions | C.2: L equal to an independent implementation in 994 steps |
| `--paranoid` on the complete file: no result (17.7) | the next paragraph |

**The real certificate.** `r30/real_leaf.py` recomputes the single step of a leaf of
`proto30/out/tree3/c01/G20S_v3_c01.jsonl.gz` with my own code (the polynomials of all names from `refcalc.py`,
the remainder and the CENTRED RULE written again in that script), tests every `ind` declaration of the leaf
with my own 4.7 on the leaf's data, tests (T1), (T2), (T3), the number of names and the availability of every
corner name by my reading, and compares L with the number in the prototype's report
(`proto30/out/tree3/c01/complete.report.json`). Logs: `r30/d/real_leaf_W01.log`, `real_leaf_more.log`,
`real_leaf_rest.log`; one file `d/real_leaf_<node>.json` per leaf.

RESULT (details in part H): **all 81 leaves recomputed; in all 81 my L equals the
prototype's L as a rational number.** 1,614,692 terms; 1,885 `ind` declarations, every one valid by my own
4.7; in six leaves (X30, X33, X34, X40, X45, X59) a listed option is excluded by my 4.7 on the leaf's data, 7
options in all, which is the count the author gives; no term violates (T1), (T2), (T3) or names an unavailable
corner.

### E.4 What the author found in the text of 2.6

PROTO_NOTES 17.4 names two rules that 2.6 does not state (unknown keys; availability in rounds that are not
evaluated). That is where the "Two rules" of the version note come from. The notes of the two checkers
themselves list more (table B.7); the author of the 3.0 text did not have to read them, I did.

### E.5 Section 18 of the notes (written after the audited text)

It is about the generator (the multipliers of `circ` are completed by a division, with terms `[circ, pol]`,
`[circ, pol, pol]`, `[circ, pol, ind]`). These terms obey (T1) to (T4), and the author's sentence "a wrong multiplier
cannot make a checker accept anything: a multiple of `circ` is zero on every configuration; it can only leave
monomials in the remainder and lower L" is A.2. Nothing there touches the text. The author's measurement that a
monomial with s_i^2 costs twice what it would with the range [0, a^2] is the reason for SHOULD-9: the rule
"multiplied e times" is to be kept literal.

## Part F. Verdict

### F.1 Verdict for the text as it stands

**SOUND AFTER THE LISTED CORRECTIONS.**

- The mathematics of everything new is correct as written: 4.9, 4.10 with the LIFTING LEMMA, the term rules,
  the TERM LEMMA, the CLAIM for the raw and the centred rule, and section 8 with centres. I re-derived each,
  found no gap, and found no false certificate that these rules admit (part A, part D).
- As a contract the text has ONE place where a literal reader accepts a false certificate: a step on the form
  `0` with sense "hi" (MUST-1). It is inherited from 2.6 word for word; both frozen checkers, the prototype and,
  by the lead's word, the second 3.0 checker reject it. With MUST-1 the text is sound.
- CONSERVATIVE: yes for "wx-cert-2", with two wrinkles that are not about soundness: the new last item of
  WELL-FORMEDNESS reads the other way than both frozen checkers for `tan` names in rounds that are not
  evaluated (MUST-2, MUST-8), and the frozen checkers disagree with each other on an empty node id (MUST-13).
- UNAMBIGUOUS: the four additions are (C.1, C.2: three independent computations of L agree). Not unambiguous
  are the last item of WELL-FORMEDNESS and thirteen inherited sentences (MUST-2 to MUST-15): under either
  reading only true statements are accepted, but two programmers can return different verdicts.

MUST-1 is needed for soundness. MUST-2 to MUST-15 are needed for "two programmers, working apart, compute the
same verdict"; each states what both frozen checkers do (tests in B.7), except MUST-13, where they differ and
the lead had to choose (the lead chose the rule of the Python checker: a non-empty string; see F.7).

### F.2 The lead's ten decisions (given during the review)

Question (i): is a decision unsound, does it change what "wx-cert-2" accepts against the common behaviour of
the frozen checkers, does it conflict with another sentence. Tests are files of `r30/b/` (verdicts Python 2.6,
Node 2.6).

| # | decision | sound | same as both frozen checkers | conflict with the text | wording |
|---|---|---|---|---|---|
| 1 | G^2 + H^2 <= 1 is part of a `tan` name, whole file | yes (a restriction) | yes: `R_n10*_N`, `R_n10b*_N` FAIL, FAIL | with line 456-457 read with line 723 (availability "by the rules stated there" would be evaluated-only); removed by the wording | MUST-8 |
| 2 | every item of WELL-FORMEDNESS on the whole file; only what depends on a store in evaluated rounds | yes | yes for every item the lead lists (`R_d05`, `R_n07`-`R_n09`, `R_t06c`, `K73`, `K74`, `R_n11*`, `R_n16`, `R_t06b`, `R_s02*`: all FAIL, FAIL in the round that is not evaluated). **But the criterion "depends on a store" must not be the rule:** the guard (T3), "the pair has a declaration in this round", k <= m, and the availability of `asg` do not depend on a store and ARE evaluated-only today, in the text (line 722-724), in the prototype (`d/O_nev_T3_unguarded_corner_N`, `O_nev_ind_undeclared_pair_N`, `O_nev_ind_k_beyond_m_N`: PASS) and, for `opt`, `par`, `asg`, in both frozen checkers (`R_n03_opt_undeclared_N`, `R_n04_par_undeclared_N`, `R_n06_asg_no_assumption_N`: PASS, PASS). Stated as a criterion, decision 2 would turn these six files into FAIL; the three `R_*` files are "wx-cert-2", so it would change what "wx-cert-2" accepts | (a) line 691-692 "A step may only use facts that are available in its round" is an item of WELL-FORMEDNESS and is not whole-file; (b) line 722-724 as above | MUST-2 (two explicit lists) |
| 3 | (T1) to (T4) for every term, whatever its multiplier | yes | yes: `R_n27_zero_lambda_unavailable_E` FAIL, FAIL | none | MUST-10 |
| 4 | no cut under the name `0` | yes | yes: `R_t06b*`, `X2_cut_stored_under_zero_after_zero_step` FAIL, FAIL | none (lines 197-198 and 791 say it for the fact name) | MUST-9 |
| 5 | a custom form is a nonempty list | yes | yes: `X_empty_custom_form` FAIL, FAIL | none | MUST-5 |
| 6 | header: lo <= hi, alpha > 0, alphaT <= 1 for every label, always | yes | yes: `X_tube_alpha_2_no_terminal_leaf`, `X_tube_alpha_0`, `X_window_alpha_0`, `X_tube_interval_inverted`, `X_window_interval_inverted` FAIL, FAIL; `X2_tube_alpha_exactly_1`, `X2_window_interval_point` PASS, PASS. Both checkers also test the window's alpha < 1 at the header (`X_window_alpha_1`); the verdict is the same as with the root test | none | MUST-4 |
| 7 | `kappa` on P+/P-: absent or a well-formed number string | yes | yes: `K33` PASS, PASS; `K34`, `K35` FAIL, FAIL | "ignored" (line 763) | MUST-6 |
| 8 | the token rule for every JSON integer | yes | yes: ten files `X2_int_*`, `X2_map_key_leading_zero` FAIL, FAIL | none | MUST-7 |
| 9 | options of an option split and `opt` declarations may repeat | yes (the covering proof does not use distinctness) | yes: `X2_optsplit_option_twice`, `X_opt_decl_twice_evaluated` PASS, PASS | none | MUST-11 |
| 10 | `packing_sha256` as a string, lowercase hex | yes | yes: `X2_sha_uppercase`, `sha_mixed_case`, `sha_leading_space`, `sha_0x`, `sha_truncated` FAIL, FAIL; the string is taken after JSON decoding (`X2_sha_escaped` PASS, PASS) | none | MUST-12 |

So: none of the ten is unsound; none changes "wx-cert-2" if decision 2 is written as two lists (MUST-2) and not
as a criterion; the conflicts are the two named under decision 2 and the word "ignored" under decision 7.
Four more rules of the same kind are not among the ten: the round with the `0` step is evaluated completely
(MUST-3), ids (MUST-13), the file format (MUST-14), repeated keys after decoding (MUST-15).

### F.3 MUST (line numbers of the audited text, now `SPEC_v3.0_candidate_audited.md`)

**MUST-1. A step on the form `0` has the sense "lo".** (soundness; B-1)
- Section 10, lines 772-773. REPLACE
  `Form `0`, sense "lo": accepted iff L >= value > 0; it is evidence for the closure "infeasible".`
  BY
  `A step on the form `0` must have the sense "lo": a step with `form` = `0` and `sense` = "hi" is malformed and rejects the certificate wherever it stands, also in a round that is not evaluated. A step on the form `0` is accepted iff L >= value > 0 (the rule "value <= L" does not apply to it; a `0` step with value <= 0 is not accepted). An accepted `0` step is evidence for the closure "infeasible"; it gives no certified value for a store entry.`
- Section 5, lines 511-512. REPLACE
  `A step with objective `0`, sense "lo" and L >= value > 0 proves that F(N) is empty.`
  BY
  `The objective `0` is the exception: it is allowed with the sense "lo" only, and such a step is accepted iff L >= value > 0; it then proves that F(N) is empty (0 = g(x) >= L > 0 holds for no x).`

**MUST-2. Where each test is made.** (B-2, C.3; the lead's decisions 1, 2, 3)
- Section 10, lines 719-725. REPLACE the whole item BY
  ```
  - WHERE EACH TEST IS MADE. A round of a node is EVALUATED iff no earlier round of the node contains an
    accepted `0` step and the store after every earlier round is not EMPTY (the first round always is). An
    evaluated round is evaluated COMPLETELY: all its declarations, all its steps (also those that follow an
    accepted `0` step) and its proposed store.
    (W) WHOLE FILE. Every item of this list WELL-FORMEDNESS, the shape that the format blocks below give to every
    object, and every condition that the lists of names below attach to a name, is tested for every node and
    every round, evaluated or not: KEYS; numbers, labels and pairs; node
    data; 1 to 3 names per term; the conditions that are part of a name (G^2 + H^2 <= 1 in a `tan` name;
    `ivl:FORM` only for `Da:o:t`, `Db:o:t` or an AFFINE custom form; no `cut` name and no key of `cuts` for
    the form `0`; a custom form `u:NAME` in an objective, in a fact name or in a key of `cuts` is defined in
    the node's `forms`; (wx-cert-3) the `q:NAME` of a `sq` or `pol` name is defined in the node's `forms`; the
    index of an `ind` name is one digit 1 to 8); the sign rule (T1) and, (wx-cert-3), the rule (T2), for every
    term whatever its multiplier; a step on the form `0` has the sense "lo"; the shape of every declaration
    (with `kappa` for Pk and Ps) and at most one `par` declaration per (i, j, cls, kind) in a round;
    (wx-cert-3) the shape of every `ind` declaration and the restrictions (R1) to (R3); (wx-cert-3) the shape
    of every `centre`; the FORMAT of every proposed store (its keys, exactly the labels of I, numbers, unit
    rotations, the keys of `rarc` and of `cuts`).
    (E) EVALUATED ROUNDS ONLY, and nowhere else: the EMPTY test; the precondition of every declaration of the
    round, whether or not a step uses it (`opt`: 4.5; `par`: 4.6, including 0 <= kappa; (wx-cert-3) `ind`:
    4.10); the availability (T4) of every name of every term, whatever its multiplier, as far as it is not a condition
    of (W) that is part of the name (a `cut` name has its
    cut in the store at the start of the round; an `opt` name has an `opt` declaration of its option in the round or, (wx-cert-3), its option
    stands in the list of an `ind` declaration of the round; a `par` name has its `par` declaration in the round; an
    `asg` name has its sign assumption in the node's `assume` list; a `wsup` name passes the sign conditions
    of 4.8; a `rarc` name has an effective relative arc; (wx-cert-3) an `ind:i:j:k` has an `ind` declaration
    of its pair in the round and k <= m); (wx-cert-3) the guard rule (T3); the acceptance of every step (also
    value > 0 of a `0` step); the acceptance of every entry of the proposed store (also cos > 0 of a proposed
    endpoint: the proposed store of a round that is not evaluated need only have the format).
    The final store of a node is the store after its last evaluated round (the node's data if it has no round).
    For the closure of a node (section 7) only its evaluated rounds count: an accepted `0` step or an EMPTY store
    must stand in an evaluated round, and every other closure test reads the final store.
  ```
  (Final wording after part G: the first sentence of (W), the availability clause of (E) and the last sentence
  were refined there, replacements R5, R6, R7.)
- Section 10, lines 691-692. REPLACE `A step may only use facts that are available in its round.` BY
  `(Availability is the term rule (T4) of section 5; it is not well-formedness: see WHERE EACH TEST IS MADE.)`
- Every clause that concerns "wx-cert-2" is what both frozen checkers do, by the tests named in B.4 and B.7
  (the `rarc` clause: `b/X4_rarc_slo_no_effective_arc_N`, `X4_rarc_tan_no_effective_arc_N` PASS, PASS; the same
  with `_E` FAIL, FAIL).

**MUST-3. The round that contains an accepted `0` step is evaluated completely.** (R1 = A2)
- Section 5, lines 541-542. REPLACE
  `If a round contains an accepted `0` step, or the store after a round is EMPTY, later rounds of the node are not evaluated.`
  BY
  `If a round contains an accepted `0` step, or the store after a round is EMPTY, the LATER rounds of the node are not evaluated. The round itself is evaluated completely: every declaration of it is tested, every step of it (also one that follows the accepted `0` step) must be accepted, and every entry of its proposed store must be accepted. Order in an evaluated round: (1) its start store (the node's data, or the store accepted in the round before) is not EMPTY; (2) every declaration is tested on that store; (3) every step is computed with the facts and store bounds of that same store; (4) every entry of the proposed store is accepted or not from the old store and the certified values of the steps of THIS round; (5) the new store is tested for EMPTY.`

**MUST-4. Header ranges.** (the lead's decision 6; R8 = A9)
- Section 10, INSERT a new item after line 675:
  `- Header ranges, tested when the header is read, also if the tree has no terminal node: every interval of the `box` of `window` and of `terminal` has lo <= hi; every `alpha` of `window` satisfies 0 < alpha < 1; every `alpha` of `terminal` satisfies 0 < alpha <= 1.`

**MUST-5. A custom form is nonempty.** (decision 5; R6 = A7)
- Section 3, lines 135-136. REPLACE `as a rational linear combination sum_m coef_m * F_m of named forms F_m`
  BY `as a NONEMPTY list of components [coef_m, F_m], standing for the rational linear combination sum_m coef_m * F_m of named forms F_m`.
- Section 10, line 700. After `coefficients are numbers;` INSERT `the list of components is nonempty; a coefficient may be 0;`
  (a zero coefficient is accepted by both frozen checkers: `b/X3_custom_form_zero_coefficient.jsonl`).

**MUST-6. `kappa` on P+ and P-.** (decision 7; R3, A6)
- Section 10, line 763. REPLACE `(kappa is required for Pk and Ps and ignored for P+, P-)` BY
  `(`kappa` is required for Pk and Ps; in a P+ or P- declaration it may be absent, and if it is present it must be a number string of the format of this section, whose value is ignored)`.

**MUST-7. JSON integers.** (decision 8; A13)
- Section 10, lines 677-678. REPLACE `(JSON integers in fields, their decimal strings as map keys)` BY
  `(JSON integers in fields; their decimal strings, without sign and without leading zeros, as map keys and inside names). A JSON integer is a number token without fraction and without exponent: `5.0`, `5e0`, `"5"` and `true` are rejected wherever the format asks for a JSON integer (a label in a field, `k`, `eps`, `sign`, `labels`).`

**MUST-8. The length condition of a `tan` name.** (decision 1; R7)
- Section 10, lines 786 and 788-789. REPLACE `` `arc:i:tan:G:H` (G, H rational strings) `` BY
  `` `arc:i:tan:G:H` (G, H number strings with G^2 + H^2 <= 1; the inequality is part of the name: a `tan` name that violates it is malformed wherever it stands) `` and `` `rarc:i:j:tan:G:H` `` BY `` `rarc:i:j:tan:G:H` (G, H as for `arc`) ``.
- Section 4.2, line 211. REPLACE `(checked)` BY `(checked as part of the name, section 10)`.

**MUST-9. No cut for the form `0`.** (decision 4)
- Section 10, line 776 (item `store`). INSERT at its beginning:
  `A key of `cuts` is `NAME:lo` or `NAME:hi`, NAME a form NAME of the list below other than `0` (there is no cut for the form `0`); a custom form `u:NAME` must be defined in the node's `forms`.`

**MUST-10. The term rules do not look at the multiplier.** (decision 3; A12)
- Section 5, line 448. REPLACE `TERM RULES (a term that violates one of them rejects the certificate):` BY
  `TERM RULES. They hold for every term, whatever its multiplier, also for the multiplier 0; a term that violates one of them rejects the certificate. (T1) and (T2) are tested on the whole file. (T3) and (T4) are tested in the evaluated rounds, with one exception: a condition that is part of a name (list (W) of section 10; for example that the `q:NAME` of a `sq` or `pol` name is defined in the node's `forms`) is tested on the whole file (section 10, WHERE EACH TEST IS MADE):`
  (final wording after part G, replacement R4)

**MUST-11. Lists that may repeat.** (decision 9; R10 = A15)
- Section 6, line 555-556. After `one child per listed option, in order;` INSERT
  `the options of Lst need not be pairwise different (a repeated option has one child per occurrence), and Lst may contain excluded options;`
- Section 10, line 763. REPLACE `Several declarations per pair are allowed (at most one per (i,j,cls,kind));` BY
  `Several `opt` and `par` declarations per pair are allowed in a round, and an `opt` declaration may be repeated; for `par`: at most one per (i, j, cls, kind);`

**MUST-12. Hash and Sref.** (decision 10; A10)
- Section 10, lines 652-653. REPLACE
  `the checker computes the SHA-256 of the packing file it reads and requires it to equal `packing_sha256`; `Sref` equals the file's `side`.`
  BY
  `the checker computes the SHA-256 of the packing file it reads and requires the JSON string `packing_sha256` to be its 64 lowercase hexadecimal digits, character for character; `Sref` is a number string whose VALUE equals the value of the file's `side` (not necessarily the same string).`

**MUST-13. Node ids.** (R12; the two frozen checkers differ: B-3)
- Section 7, TREE CONDITIONS, line 584. After `node ids are unique;` INSERT
  `a node id is a non-empty JSON string, and ids are compared as strings, character for character;`
- This is the Python checker's rule and the prototype's. The frozen Node checker accepts the empty id
  (`b/X_empty_id.jsonl`: Python FAIL, Node PASS). If the lead prefers the other rule, the sentence is "a node id
  is any JSON string, the empty string included". Either way the text must say it; and the acceptance record
  of 2.6 should note that the two frozen checkers differ on this one input.

**MUST-14. The file.** (R11 = A11)
- Section 10, lines 647-648. REPLACE
  `The certificate is a header object and one object per node (JSON lines, or one JSON file per node plus an index).`
  BY
  `The certificate is a file of JSON lines in UTF-8 without byte order mark: the header object on the first line, then one node object per line, in any order, at least one node. Every line holds exactly one JSON object, with or without JSON whitespace around it (a carriage return before the line feed is such whitespace); an empty line is rejected, also after the last node; the last line may end with or without a line feed. A checker may read the same lines from a gzip-compressed file.`

**MUST-15. Strings are taken after decoding.** (NOTES_V26 6.4)
- Section 10, line 718. REPLACE `- A JSON object with a repeated key is rejected.` BY
  `- A JSON object with a repeated key is rejected. Keys are compared after decoding JSON escapes (a key spelled with an escape, for example `labels` with its second letter written as a backslash followed by `u0061`, is the key `labels`); every string of a certificate (a name, a number string, an id, `schema`, `packing_sha256`) is used after decoding.`
  (final wording after part G, replacement R8: in the first version of this file the example was an escaped spelling
  that a tool decoded on the way into the file, so that it read "labels" twice and said nothing.)

### F.4 SHOULD

1. Section 7 (a), line 578: `some round contains a step with objective `0` and L > 0` -> `some evaluated round
   contains an accepted `0` step (objective `0`, sense "lo", L >= value > 0)`, so that sections 5, 7 and 10
   say the same thing. (The version note's "section 7 unchanged word for word" then needs a word.)
2. Version note, line 8, item (5): it speaks of "Two rules". After the corrections: "The rules that both
   checkers of version 2.6 enforce and that its text did not state are now stated: KEYS; where each test is
   made; a `0` step has sense "lo"; the round of a `0` step is evaluated completely; the header ranges; a
   nonempty custom form; `kappa` on P+/P-; JSON integers; the `tan` condition; no cut for `0`; lists that may
   repeat; the hash as a string; ids; the file; strings after decoding."
3. Line 792: `` `sq:NAME`; `pol:NAME` `` -> add `(NAME matching [A-Za-z0-9_]+: the NAME of a key `q:NAME` of
   the node's `forms`)`.
4. Lines 632-634: "with the identity centre covers every square" -> "with any centre covers one of the four
   side directions of every square".
5. Lines 402-403: add "(The LIFTING LEMMA uses none of (R1) to (R3). (R1) makes the indicator variables of a
   pair well defined; (R2) and (R3) keep one option from being a fact and a guarded name in the same round or
   node.)" See A-3 and E.2.
6. Section 10 or 11: say that the statement is relative to the reference file whose SHA-256 is in the header,
   that a checker may in addition require one particular file (both frozen checkers and the prototype pin
   24e296f5...fef45f7 by default, an option lifts the pin), and that the final theorem must quote the hash.
7. Lines 384-385: "such a term is zero at every configuration" -> "... at every configuration, for all values
   of the indicator variables".
8. Line 459: "k <= m" -> "1 <= k <= m".
9. Lines 465-468, after the RAW RULE: add "(The rule is meant literally. For an even power it does not give
   the range of the monomial: x^2 with x in [-a, a] gets [-a^2, a^2], not [0, a^2]. A checker must not
   tighten it, or its L is another number.)" The text is already unambiguous ("multiplied e times"); the
   sentence prevents a well-meant improvement. (The author's notes, section 18.2, measure what the literal
   rule costs on s_i^2.)
10. KEYS, lines 662-667: name the optional keys once: `labels`, `S_floor` (header); `centre` (window, terminal,
    step; wx-cert-3); `forms` (node); `kappa` (P+ or P- declaration); `pair` (closure "infeasible"). Every
    other key of the format blocks is required (tested: `b/K51` to `K60`).
11. Line 102 / lines 175-179: add "(The start store of an evaluated round is never EMPTY: the node's data
    cannot be EMPTY, and after an EMPTY store no round is evaluated.)"
12. Section 12, line 855-856: the advice "Give the step a `centre`" could quote the size of the effect; on my
    small example `d/T_T1*` the raw rule gives L = -0.080 and the centred rule 0.99994 for the same terms.

### F.5 Not examined

- The source of the prototype and the second 3.0 checker. The prototype was a black box.
- The lemmas of 2.6 (4.0 to 4.8, sections 6, 7) were not audited again; I used the SAT lemma and 4.7 as stated.
  Of the fact polynomials I re-implemented `box`, `side`, `arc`, `circ`, `wall`, `opt`, `sq`, `pol`, `ind`; NOT
  `par`, `wsup`, `ivl`, `cut`, `asg`, `rarc`, the class forms and custom forms.
- The exclusion test inside the `ind` precondition on a store WITH stored relative-arc endpoints or cuts: only
  the seven hand-derived cases of D.6 (`d_store.py`); my calculator handles the store of a first round.
- Windows with free direction (radius above pi/4) together with centres: reasoned in A.5, not tested.
- (Done after this list was written, part H: the whole real certificate, its tree and all 81 leaves, against the
  mathematics of the text. Not done there either: its format, which my reader does not test.)
- Section 11 (what the application adds), the terminal theorem and the composition with centres; section 12.
- Limits: very large numbers, very deep products, memory, the mode `--paranoid`, JSON beyond the cases of B.7.
- The file format "one JSON file per node plus an index" (no program reads it).

### F.6 Every test of sections 2 to 10 and its class (completeness of the two lists of MUST-2)

Prepared for the re-reading of the corrected text. W = whole file; E = evaluated rounds only; H = when the
header is read; T = tree pass, on the node's data, its evaluated rounds and its final store.

| defined in | test | class |
|---|---|---|
| 2, 10 "Node data" | lo <= hi, S_lo <= S_hi, cos P^± > 0, sin P^- <= sin P^+, unit rotations of a node | W |
| 2, 3 | the EMPTY test of a store (box, side, arcs, effective relative endpoints, cut pairs, an empty SB of a form with a cut) | E |
| 3, 10 `forms` | a custom form: NAME, nonempty, components form NAMEs other than `0` and `u:`, pairwise different, numbers; a `q:` form | W |
| 4.0, 4.1, 4.2 | `box`, `side`, `circ`, `wall`, `arc` names: always available; their pattern; G^2 + H^2 <= 1 of a `tan` name | W |
| 4.0 | `ivl:FORM` only for `Da`, `Db`, an affine custom form | W |
| 4.0 | `cut:FORM:lo/hi`: FORM is not `0`, a custom form is defined | W |
| 4.0 | `cut:FORM:lo/hi`: the cut is in the start store | E |
| 4.3 | a `rarc` name: the pair has an effective relative arc (the `tan` condition: W) | E |
| 4.5 | an `opt` name: OPT-AVAILABLE or IND-LISTED in the round | E |
| 4.5, 4.6, 4.10 | the precondition of an `opt`, `par`, `ind` declaration | E |
| 4.6 | a `par` name: its declaration in the round; an `asg` name: the sign assumption of the node | E |
| 4.6, 10 | `kappa` present for Pk and Ps (and well formed if present); at most one `par` declaration per key | W |
| 4.8 | a `wsup` name: the sign conditions | E |
| 4.9 | `sq`, `pol`: `q:NAME` defined in the node's `forms` | W |
| 4.10 | the shape of an `ind` declaration; (R1), (R2), (R3); the index digit of an `ind` name | W |
| 4.10 | `ind:i:j:k`: declaration of the pair in the round, k <= m | E |
| 5 | the objective is a form NAME (a custom form defined); `0` only with sense "lo" | W |
| 5 | 1 to 3 names per term; (T1); (T2) | W |
| 5 | (T3); (T4) | E |
| 5 | L and the acceptance of a step (lo, hi, `0`) | E |
| 5 | the acceptance of every entry of the proposed store (box, S, arc with cos > 0, relative endpoint with its side condition and cos > 0, cut) | E |
| 5, 10 | the format of a proposed store (keys `S`, `box`, `arc`, `rarc`, `cuts`; exactly the labels of I; numbers; unit rotations; `rarc` keys i-j with i < j in I, values a rotation or null; cut keys `NAME:lo/hi`, NAME not `0`, a custom form defined) | W |
| 6 | the format of a split object | W |
| 6 | the conditions of a split on the final store and on the children | T |
| 7 | closures (a), (b), (c); tree conditions; root conditions | T |
| 8 | header ranges (MUST-4) | H |
| 8 | root contains window; terminal test | T |
| 10 | schema, hash, `Sref`, `labels`, `S_floor`, `centre` maps of the header | H |
| 10 | the file, strings after decoding, repeated keys, KEYS, numbers, JSON integers, labels and map keys, the enumerations (`k`, `axis`, `eps`, `sign`, `cls`, `kind`, `mode`, `sense`, corner letters, wall coordinate, `wsup` wall), pairs | W |
| 10 | the `centre` of a step | W |

With the wording of MUST-2 as it stands above (including the refinement of the `opt` clause)
I find no test that is in neither class.

### F.7 For the record: what the lead decided on this report

MUST-1 to MUST-15 and SHOULD 1 to 12 accepted as worded; MUST-2 as the two explicit lists (W) and (E), with the
refinement of the `opt` clause; MUST-13: a node id is a non-empty JSON string, and the difference between the
two frozen checkers on the empty id is recorded as erratum F6 of 2.6, together with the fourteen silent places.
The author then wrote the corrected text (`proto30/SPEC_v3.0_corrected.md`, with the table
`proto30/SPEC_CORRECTIONS.md`); the audited candidate is kept as `SPEC_v3.0_candidate_audited.md`. Part G
re-reads the corrected text against the audited one and ends with the acceptance of the final text; part H has
the real certificate and the rerun of all certificates of `r30/` through the Python checker of version 3.0.

---

## Part G. The corrected text (`proto30/SPEC_v3.0_corrected.md`)

Read: `proto30/SPEC_v3.0_corrected.md` (886 lines, sha256
97d8c8b578604cfdcec913d72740aea5173f081bbe875731efda8e7be2c157e8, verified), `proto30/SPEC_CORRECTIONS.md`,
`proto30/SPEC_v3.0_corrected_vs_candidate.diff`. Compared with `SPEC_v3.0_candidate_audited.md` (sha256
2cec6f72...a908, the audited text).

**Result of part G: every MUST and every SHOULD is applied; nothing else is changed; TEN exact replacements
remain (R1 to R10 below, R10 optional). Three of them repair wording of MINE that contradicted itself once it
stood in the text (R5, R6, R7), one repairs my garbled example (R8), three answer the author's open points (R1,
R2, R4), three are small (R3, R9, R10). No replacement changes what any program accepts. With R1 to R9 applied
I accept the text.**

### G.1 Every MUST and SHOULD applied as worded; nothing else changed

- `r30/g_check.py` (white space collapsed): the new wording of MUST-1 to MUST-14 is in the corrected text
  character for character and every replaced wording is gone; MUST-15 is there with the example as it stood in
  my file (see G.3, point 2). The SHOULDs I compared by eye: 1 (section 7 (a)), 2, 3, 4, 5, 7, 8, 9, 11 are
  verbatim; 6, 10, 12 and the sentence of the version note are the author's words (G.3, point 4).
- The author's diff file is byte for byte the output of `diff` on the two texts (31 hunks, 65 lines added, 41
  replaced). Every hunk belongs to a MUST or a SHOULD or is the lead's line in the version note:

  | hunk (lines of the audited text) | item |
  |---|---|
  | 8-9 | SHOULD-2; SHOULD-1 (version note); the lead's line |
  | 135-136; 700 | MUST-5 |
  | 179 (after) | SHOULD-11 |
  | 211; 786; 789 | MUST-8 |
  | 384 | SHOULD-7 |
  | 403 (after) | SHOULD-5 |
  | 448 | MUST-10 |
  | 459 | SHOULD-8 |
  | 468 (after) | SHOULD-9 |
  | 511-512; 772-773 | MUST-1 |
  | 541-542 | MUST-3 |
  | 556; 763 (second half) | MUST-11 |
  | 578 | SHOULD-1 |
  | 584 | MUST-13 |
  | 633 | SHOULD-4 |
  | 647-648 | MUST-14 |
  | 652-653 | MUST-12 |
  | 667 | SHOULD-10 |
  | 675 (after) | MUST-4 |
  | 678 | MUST-7 |
  | 691-692; 718-725 (second part) | MUST-2 |
  | 718-725 (first line) | MUST-15 |
  | 763 (first half) | MUST-6 |
  | 776 | MUST-9 |
  | 792 | SHOULD-3 |
  | 839 (after) | SHOULD-6 |
  | 856 | SHOULD-12 |

  No hunk is left over, and no MUST or SHOULD is without a hunk.
- The sentence "The closure of a node is tested on its evaluated rounds and its final store only" at the end
  of MUST-2 is mine: I added it to this file after I had given MUST-2 to the
  lead, when I compared my two lists with the lead's words "closure evidence". It belongs there (refined by R7).

### G.2 New contradictions between corrected passages; completeness of (W) and (E)

I read sections 4, 5 and 10 of the corrected text again against the table F.6. Three places where corrected
passages contradict each other when read literally, all in or around wording of mine:

1. **(W), first sentence, against (E).** "(W) WHOLE FILE. Every rule of this section ... is tested for every
   node and every round, evaluated or not". Section 10 also contains, after the format blocks, the items
   `pairs`, `step` and `store`, which state preconditions and acceptance rules; those are in (E). So these
   rules stand in BOTH lists. Meant was: the items of the list WELL-FORMEDNESS, the shape of the objects, and
   the conditions attached to names. Replacement R5.
2. **(E) "the availability (T4) of every name ... and nowhere else" against (W).** One clause of (T4) is "`sq:NAME`
   and `pol:NAME`: iff q:NAME is defined in the node's `forms`", and (W) (with 4.9) tests exactly this on the
   whole file. The same holds for what (T4) calls "the rules stated there" where they are conditions of the
   name (`ivl` only for an affine form, no `cut` name for `0`). This is the author's open point 3, seen from the
   other side. Replacements R4 (the sentence of MUST-10) and R6 (the clause of (E)).
3. **The last sentence of MUST-2**, "The closure of a node is tested on its evaluated rounds and its final
   store only": a split closure is also tested on the data of the children, and the root conditions on the
   root's data. Meant was only: of the node's ROUNDS, only the evaluated ones count. Replacement R7.

With R4 to R7 every test of sections 2 to 10 is in exactly one class of F.6 (whole file, evaluated rounds,
header, tree pass); I find no rule that is in no list and none that is in two. No other pair of corrected
passages contradicts: checked in particular section 5 (MUST-1) with section 7 (a) and the `step` item; MUST-3
with (E) and with the sentence on the EMPTY test in section 3; KEYS with the list of optional keys and the
`pairs` item (`kappa`); MUST-9 with the fact name `cut` (4.0, FACT names); MUST-4 with the two "Requires" of
section 8; MUST-7 with the item on `labels`; MUST-13 with the header's `root`.

### G.3 The author's four open points

1. **"ids" in item (5) of the version note.** The author is right: "rules that both checkers of version 2.6 enforce"
   is false for ids, and with MUST-13 there is one input on which the text and a frozen checker differ.
   Replacements R1 (ids taken out of the list and named as the rule on which the two checkers differ) and R2
   (the one exception, at the sentence "Under the schema "wx-cert-2" nothing changed").
2. **The example of MUST-15.** My error of transport: I had written an escaped spelling of `labels`, and the
   tool with which I wrote this file decoded the escape, so that the example read "labels" is the key `labels`.
   Replacement R8 gives the example in words, with no escape sequence in the text.
3. **MUST-10 against (W).** Replacement R4 (and R6, see G.2).
4. **Four passages in the author's words.**
   - Version note, the sentence on sections 2, 6 and 7: correct in substance (section 2 has no hunk; section 6
     has one sentence, section 7 two). I replace only "three sentences of (5): lists that may repeat" by words
     that say what the three sentences are (R3).
   - SHOULD-6, the new item (5) of section 11: ACCEPTED as it stands. (The hash in it is the `packing_sha256` of
     every certificate of the folder; I compared the 64 digits.)
   - SHOULD-10, the frame around the list of optional keys: ACCEPTED as it stands.
   - SHOULD-12, the parenthesis in section 12: the two numbers are right (my L: 0.999935424 and -0.080064); the
     files are `reviews/r30/d/T_T1*`, not `d/T_T1*` (R9).

One more place, optional (R10): the parenthesis of SHOULD-3 now stands after the parenthesis of `pol:NAME` and
can be read as speaking of `pol:NAME` alone.

Not mine to word, for the lead before the hash is pinned: line 3 of the text still says "Version 3.0 CANDIDATE
(... a proposal: in force only once the lead adopts it as `SPEC_v3.0.md`)". And in `SPEC_CORRECTIONS.md` (not
part of the text) the evidence named for MUST-1 is my file `R_d05`, which is the test of two `par`
declarations; the tests of the `0` step with sense "hi" are `b/R_s02_*` and `d/F01_*`.

### G.4 The replacements still to make (exact; also in `r30/g_replacements.py`, which checks that each OLD
string occurs exactly once in the corrected text)

White space and line breaks are free. OLD is the wording of `proto30/SPEC_v3.0_corrected.md`.

- **R1** (version note, item (5)). OLD: `lists that may repeat; the hash as a string; ids; the file; strings after decoding.`
  NEW: `lists that may repeat; the hash as a string; the file; strings after decoding. One further rule is stated on which the two checkers of version 2.6 DIFFER: a node id is a non-empty string (section 7; the Python checker of 2.6 rejects the empty id, the Node checker of 2.6 accepts it).`
- **R2** (version note, item (1)). OLD: `and every element of (2) is rejected in it. Old certificates keep their meaning and their checkers.`
  NEW: `and every element of (2) is rejected in it. Old certificates keep their meaning and their checkers. There is ONE input on which this text and a checker of version 2.6 differ: a "wx-cert-2" certificate with an empty node id is rejected by this text (section 7) and by the Python checker of 2.6 and is accepted by the Node checker of 2.6 (erratum F6 of `SPEC_v2.6_ERRATA.md`).`
- **R3** (version note). OLD: `sections 6 and 7 are unchanged except for three sentences of (5): lists that may repeat (section 6), the wording of closure (a) and the rule on node ids (section 7).`
  NEW: `sections 6 and 7 are unchanged except for three sentences that belong to (5): the list of an option split may repeat (section 6), the wording of closure (a) and the rule on node ids (section 7).`
- **R4** (section 5, TERM RULES). OLD: `(T1) and (T2) are tested on the whole file, (T3) and (T4) in the evaluated rounds (section 10, WHERE EACH TEST IS MADE):`
  NEW: `(T1) and (T2) are tested on the whole file. (T3) and (T4) are tested in the evaluated rounds, with one exception: a condition that is part of a name (list (W) of section 10; for example that the `q:NAME` of a `sq` or `pol` name is defined in the node's `forms`) is tested on the whole file (section 10, WHERE EACH TEST IS MADE):`
- **R5** (section 10, list (W)). OLD: `(W) WHOLE FILE. Every rule of this section, and every condition that the lists of names below attach to a name, is tested for every node and every round, evaluated or not:`
  NEW: `(W) WHOLE FILE. Every item of this list WELL-FORMEDNESS, the shape that the format blocks below give to every object, and every condition that the lists of names below attach to a name, is tested for every node and every round, evaluated or not:`
- **R6** (section 10, list (E)). OLD: `the availability (T4) of every name of every term, whatever its multiplier (a `cut` name has its`
  NEW: `the availability (T4) of every name of every term, whatever its multiplier, as far as it is not a condition of (W) that is part of the name (a `cut` name has its`
- **R7** (section 10, end of WHERE EACH TEST IS MADE). OLD: `The closure of a node is tested on its evaluated rounds and its final store only.`
  NEW: `For the closure of a node (section 7) only its evaluated rounds count: an accepted `0` step or an EMPTY store must stand in an evaluated round, and every other closure test reads the final store.`
- **R8** (section 10, repeated keys). OLD: `Keys are compared after decoding JSON escapes ("labels" is the key `labels`);`
  NEW: `Keys are compared after decoding JSON escapes (a key spelled with an escape, for example `labels` with its second letter written as a backslash followed by `u0061`, is the key `labels`);`
- **R9** (section 12). OLD: `(on a small example of the audit `reviews/REVIEW_30.md`, files `d/T_T1*`, the raw rule gives L = -0.080 and the centred rule 0.99994 for the same terms)`
  NEW: `(on a small example of the audit `reviews/REVIEW_30.md`, files `reviews/r30/d/T_T1*`, the raw rule gives L = -0.080 and the centred rule L = 0.99994 for the same terms)`
- **R10**, optional (section 10, FACT names). OLD: `` `pol:NAME` (not a fact: only in a term containing a `circ` fact) (NAME matching [A-Za-z0-9_]+: the NAME of a key `q:NAME` of the node's `forms`); ``
  NEW: `` `pol:NAME` (not a fact: only in a term containing a `circ` fact); in `sq:NAME` and in `pol:NAME`, NAME matches [A-Za-z0-9_]+ and is the NAME of a key `q:NAME` of the node's `forms`; ``

### G.5 Last step: the final text `proto30/SPEC_v3.0_final.md`

**ACCEPTED AS IT STANDS: `proto30/SPEC_v3.0_final.md`, 885 lines, SHA-256
0a6dfc2ae10ed6f30a21ebe357a6e73dd7355223c521cc67a3f2bdab9549aba0** (checked with `r30/g_final.py`).

- R1 to R10: for each, the old wording is gone and the new wording occurs exactly once.
- I applied R1 to R10 myself to `SPEC_v3.0_corrected.md` (in memory) and compared with the final text line by
  line: exactly two lines differ, and they are the lead's two replacements: line 3 (the status line, now
  "**Version 3.0** (2026-10-09; text by the helper "sosproto" ...; audited by the referee "ref30" ...; adopted
  by the lead as `SPEC_v3.0.md`. It is in force from the moment both checkers of version 3.0 are frozen with the
  SHA-256 of this file)") and line 10 (the last line of the version note, which names R1 to R10 and gives the
  hash 2cec6f72...a908 of the audited candidate; the hash is right). Twelve replacements and nothing else.
- `diff SPEC_v3.0_corrected.md SPEC_v3.0_final.md` has 9 hunks; read one by one they are: line 3 with R2; R1,
  R3 and the last line of the note; R4; R8; R5; R6; R7; R10; R9.
- The final wording of every MUST (F.3) is in the text.
- With these the points of G.2 are closed: every test of sections 2 to 10 is in exactly one class of F.6, and I
  know of no pair of passages of the final text that contradict each other.

What this acceptance covers: the text. It says nothing about the two checkers of version 3.0, which I have
not seen.

### G.6 The corpus through the programs again

Done in part H.3 (`r30/h_rerun.py`, which replaced the prepared `r30/rerun_all.py` for the run; it takes the
prototype's verdict in the same pass instead of a stored baseline).

---

## Part H. The real certificate checked completely; my corpus through the Python checker of version 3.0

After the final text was installed: (1) the 81 leaves to the end, (2) my own
check of the tree, (3) the rerun of my corpus through the edited Python checker.

### H.1 The 81 leaves of `proto30/out/tree3/c01/G20S_v3_c01.jsonl.gz` (`r30/real_leaf.py`)

For every leaf the script reads the node, builds with my own code (`refcalc.py`) the polynomial of every name
of the one step, forms Rem, applies the CENTRED RULE with the step's `centre` and the store bounds of the node's
data, and compares L with the number in the prototype's report (`complete.report.json`, key `proto_steps`). It
also tests, by my reading of the text: every `ind` declaration of the leaf with my own exclusion test 4.7;
every `opt` declaration (the node must assume the option); for every term (T1), (T2), (T3), 1 to 3 names and
the availability of every corner name. Logs: `d/real_leaf_W01.log`, `d/real_leaf_more.log`,
`d/real_leaf_rest.log`; one result file `d/real_leaf_<id>.json` per leaf (81 files).

| | |
|---|---|
| leaves | 81 (21 wrong-option leaves W01 to W21, 60 exit leaves MAIN.X01 to X60) |
| **L equal to the prototype's, as a rational number** | **81 of 81** |
| claimed value <= L | 81 of 81 |
| terms | 1,614,692 in all (13,248 to 26,370 per leaf) |
| monomials of Rem(c + y) | 16,176 to 25,581 per leaf, degree 5; the same count as the prototype reports |
| `ind` declarations | 1,885 (22 to 32 per leaf); a non-excluded option left out: 0 |
| listed options that my 4.7 excludes on the leaf's data (allowed) | 7, in the six leaves X30, X33, X34, X40, X45, X59 |
| `opt` declarations | all of options that the node assumes |
| terms violating (T1), (T2), (T3), the number of names, or naming an unavailable corner | 0 |
| smallest L | 0.000938545 (W20) |
| time | 31 to 66 s per leaf, 3,213 s in all |

So the L of all 81 closing steps has now been computed three times, by programs that share no code: the
prototype, the second checker (the lead's statement), and `refcalc.py`/`real_leaf.py`.

### H.2 The tree of the same certificate (`r30/real_tree.py`, log `d/real_tree.log`, result `d/real_tree_result.json`)

My own code for sections 2, 5 (store update), 6, 7 and 8, one pass over the file (8 s): **153 nodes, 0
problems.**

- header: schema, `Sref` = the side of the packing file, the packing hash, `S_floor` (= Sref), the ranges of
  MUST-4;
- node data of all 153 nodes (intervals, side interval, unit rotations, cos P > 0, sin P^- <= sin P^+);
- tree conditions: ids unique and non-empty, the root, parent and children consistent, every node but the root
  in exactly one `children` list, every node reachable;
- root conditions: no parent, no assumption, S_lo <= S_floor, S_hi >= Sref, ROOT CONTAINS WINDOW for all 16
  labels;
- the 60 box splits: the split point inside the interval of the final store, the two children's intervals;
- the 11 option splits: one child per listed option with that option as its additional assumption, and
  EVERY option that is not listed (56 in all) EXCLUDED by my own 4.7 on the node's final store;
- for every child: its `assume` list, and that its box, its side interval and its arcs (ARC CONTAINMENT TEST)
  contain the parent's final store;
- the terminal node `MAIN.T`: the TERMINAL TEST;
- the 81 leaves: one round with one step on `0`, sense "lo", value > 0, L from H.1 with value <= L; the
  proposed store accepted entry by entry (nothing tighter than the node's data), no `rarc`, no `cuts`.

The script is not vacuous: on the small twin of the tree (`G20S_v3_c01_structure.jsonl`) it reports 0 problems,
and it reports each of 8 mutations I made of that twin (an option dropped from a split list, a split point
outside the interval, a child's interval shrunk, a child's assumption changed, the window wider than the root
arc, the tube too narrow, a child's arc centre turned, S_floor below the root's side interval).

**What H.1 and H.2 together are:** a check of the whole certificate G20S_v3_c01 (153 nodes) against the
mathematics of the text, by code written from the text by the referee: the tree, every split, every exclusion,
the root and the terminal test, every declaration, every guard, and the exact L of every closing step. What
they are NOT: a check of the format. My reader is Python's `json`; it does not test KEYS, number syntax,
repeated keys or the name patterns, and it knows only the names that the certificate uses (`box`, `arc`, `wall`,
`circ`, `opt`, `sq`, `pol`, `ind`). The format is the business of the two checkers.

### H.3 My corpus through the edited Python checker (`r30/h_rerun.py`, log `h/rerun_candidate.log`)

Program: `proto30/wxcheck_v30_candidate.py`, sha256
cf8db52bfa1cc565d8610bf13b279d1b5da2f84c91ce2854d15a3b0a88cd096c (by the lead's word the bytes to be frozen as
`checker/wxcheck_v30.py`), used as a black box; its reports name the installed text (`spec_sha256` 0a6dfc2a...).
428 s. **Nothing unexpected.**

| | what | result |
|---|---|---|
| (a) | all 553 certificates of `r30/b` and `r30/d` | 143 PASS, 410 FAIL; the same verdict as the prototype `wxproto30b.py` on all 553; of the 506 files that have an expectation of mine under the final text, 505 as expected, and the one other is a file of mine with a wrong name (below) |
| (b) | `zero_step_L`, the exact L that the program reports for a node it closes by a `0` step: 95 nodes in 95 accepted files (wall facts, option facts under an assumption, the indicator proofs of D.5) | equal to the L of my own calculator as a rational number in all 95 |
| (c) | the 994 steps of `d/L_compare*.jsonl` (the program no longer reports the L of a step that does not close a node, so by thresholds): the four certificates with every claimed value replaced by MY L; and each step alone with my L + 10^-40 | the four are accepted; each of the 994 single steps is rejected as "not accepted". So for every one of the 994 steps the program's L lies in [my L, my L + 10^-40) |
| (d) | the precondition of `ind` declarations, 120 pairs and 8 options, against my own 4.7 | the 653 valid declarations (one certificate, 8 rounds) accepted; each of the 307 that leave out an option my test does not exclude rejected, the reason naming that option |
| (e) | the 1801 certificates of the old test suites ("wx-cert-2") | the verdict of the frozen Python checker 2.6 on 1800; the one other is `checker/v26/testcerts/fail/F36.jsonl`, whose only defect under 2.6 is the schema string "wx-cert-3"; with the schema string replaced by "wx-cert-3" no verdict changes in any of the 1788 files that have the string |

Under (a): the empty node id is rejected (`b/X_empty_id.jsonl`, `b/X_empty_id_leaf.jsonl`: "empty node id"),
the `0` step with sense "hi" is rejected in all eight files (`b/R_s02*`, `d/F01*`), all 54 false certificates of
D.1 are rejected.

The file with the wrong name: `d_misc.py` had written the schema-string tests under names that contain the
string, and this file system does not distinguish `'wx-cert-3'` from `'WX-CERT-3'`, so the second test
overwrote the first. The file `d/M_schema_'wx-cert-3'.jsonl` therefore held the certificate with the schema
"WX-CERT-3", which every program rightly rejects, while my table expected PASS for its name. I replaced it by
`d/M_schema_lowercase_wx-cert-3.jsonl` (PASS, as expected) and `d/M_schema_uppercase_WX-CERT-3_as_text.jsonl`
(FAIL, as expected) and corrected the script. No verdict of any program was wrong at any time; my verdict table
of D.6 was right (each row had been run before the next file was written). The folder now has 554 certificates.

Not mine: the lead reports that its cross-run put the same 553 files through both drafts of the 3.0 checkers,
with the same verdict in all but the two empty-id files and the same L on 94 closing steps. I have not seen the
Node checker or that run.

### H.4 Where the audit stands

- The text: `W/SPEC_v3.0.md`, sha256 0a6dfc2ae10ed6f30a21ebe357a6e73dd7355223c521cc67a3f2bdab9549aba0, is the
  audited candidate with MUST-1 to MUST-15, SHOULD 1 to 12 and R1 to R12; accepted as it stands (G.5).
- The mathematics of the four additions: correct (part A); not one false certificate accepted by any program
  in any run of this review.
- The contract: one hole with an unsound reading, inherited from 2.6 and closed (MUST-1); fourteen places where
  the text was silent or loose and is now explicit; one input on which the frozen checkers of 2.6 differ (the
  empty node id), now decided and named in the text.
- The only certificate of the new kind, G20S_v3_c01: checked completely against the mathematics of the text
  by my own code (H.1, H.2).
- The Python checker of version 3.0 (candidate cf8db52b...): as a black box it gives on all my certificates
  the verdicts I expect under the final text, and on the old test suites the verdicts of the frozen Python
  checker of 2.6.
- Still not examined: the list of F.5, with two items now done (the tree of the real certificate, and stores
  with cuts or stored relative arcs in the `ind` precondition, the latter by seven hand-derived cases only).
  The source of no checker was read by me at any time.

---

## Appendix. The files of `W/reviews/r30/` and how to run them

PY = the Python interpreter of the review; every script is run from `W/reviews/r30/`.
All three programs are used as black boxes (`harness.py`).

| file | what it is | writes |
|---|---|---|
| `harness.py` | runs the frozen Python checker 2.6, the frozen Node checker 2.6 and the prototype on a certificate | - |
| `refgeom.py` | reference data of sections 0 and 1 from the text; exact feasibility test; run alone it shows that the reference point is feasible | - |
| `refcalc.py` | my own calculator: polynomials of names, store bounds, L by the raw and the centred rule, the exclusion test 4.7 on a first-round store | - |
| `geom_check.py` | `refcalc.py` against geometry; the SAT lemma on 6,000 exact pairs of squares | prints |
| `attack_base.py` | the FALSE base and the TRUE base of the attack certificates | - |
| `b_keys.py`, `b_rounds.py`, `b_readings.py`, `b_table.py` | part B: KEYS; rounds that are not evaluated; the readings of the two frozen checkers | `b/K*`, `b/R_*`, `b/X_*`, `b/X2_*`, `b/*_results.json` (`b/X3_*`, `b/X4_*` and `b/X_id_*` were made by hand-typed commands of the same kind) |
| `b_corpus.py` | the 1801 old test certificates through the three programs | `b/corpus_results.json`, `b/corpus_run.log` |
| `d_attack.py` | part D.1: 54 false certificates | `d/A_*`, `d/attack_results.json` |
| `d_allow.py`, `d_allow_more.sh` | parts C.2, D.2: L against my calculator, 994 steps | `d/L_compare*` |
| `d_rounds.py`, `d_header.py`, `d_true.py`, `d_misc.py`, `d_excl.py`, `d_store.py` | parts D.3 to D.6 | `d/O_*`, `d/H_*`, `d/T_*`, `d/M_*`, `d/E_*`, `d/S_*`, `d/*_results.json` |
| `real_leaf.py`, `real_tree.py` | parts E.3, H.1, H.2: the real certificate | `d/real_leaf_*.json`, `d/real_leaf_*.log`, `d/real_tree.log`, `d/real_tree_result.json` |
| `g_check.py`, `g_replacements.py`, `g_final.py` | part G: the wording of every MUST in a text; the replacements R1 to R10; the last check of the final text | print |
| `h_rerun.py` | part H.3: everything through the Python checker of version 3.0 | `h/a_verdicts.json`, `h/summary_*.json`, `h/rerun_candidate.log` |
| `rerun_all.py` | expectations table used by `h_rerun.py` (its own baseline mode was not needed) | - |
| `wait_until.sh`, `wait_log.sh` | wait for a run of mine to end | - |
