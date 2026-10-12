# SPEC: branch-and-contract proof engine for the window extension ("WX engine")

**Version 3.0** (2026-10-09; text by the helper "sosproto" for the lead of the window-extension session; audited by the referee "ref30", `reviews/REVIEW_30.md` parts A to G; adopted by the lead as `SPEC_v3.0.md`. It is in force from the moment both checkers of version 3.0 are frozen with the SHA-256 of this file). What changed against version 2.6, completely:
(1) A second schema string, "wx-cert-3" (section 10, SCHEMA RULE). **Under the schema "wx-cert-2" nothing changed**: such a certificate is checked exactly by the rules of version 2.6, and every element of (2) is rejected in it. Old certificates keep their meaning and their checkers. There is ONE input on which this text and a checker of version 2.6 differ: a "wx-cert-2" certificate with an empty node id is rejected by this text (section 7) and by the Python checker of 2.6 and is accepted by the Node checker of 2.6 (erratum F6 of `SPEC_v2.6_ERRATA.md`).
(2) Only under "wx-cert-3", four additions, each marked "(wx-cert-3)" where it stands: (a) ARC CENTRES of the window and of the tube: optional `centre` maps in the header (section 8 with its two tests and their proofs, section 10, section 11 item (4)); (b) POLYNOMIAL FORMS `q:NAME` (section 3) with the fact `sq:NAME` and the sign-free name `pol:NAME` (new section 4.9); (c) INDICATORS FOR A PAIR: `ind` declarations, indicator variables, the name `ind:i:j:k`, the GUARD RULE and the LIFTING LEMMA (sections 3, 4.5, new section 4.10, section 5); (d) the CENTRED remainder bound: an optional `centre` in a step (section 5).
(3) The STEP paragraph of section 5 is rewritten around the TERM RULES (T1) to (T4), a TERM LEMMA and the CLAIM. For a certificate without indicators and without a `centre` in a step it says what the STEP paragraph of 2.6 said: (T1) and (T4) are the old conditions on a term, the RAW RULE is the old bound, and the TERM LEMMA is the old sentence "every product of facts is >= 0 on F(N)".
(4) The wording corrections F1 to F4 of `SPEC_v2.6_ERRATA.md`, which change nothing that a checker accepts: the note on version 2.6 below (F2), the counts that belong to sixteen labels (F3: sections 1, 3 and 5), the first paragraph of section 11 (F1, F4), and what "JSON integer" means (section 10).
(5) The rules that both checkers of version 2.6 enforce and that its text did not state are now stated: KEYS; where each test is made; a `0` step has sense "lo"; the round of a `0` step is evaluated completely; the header ranges; a nonempty custom form; `kappa` on P+/P-; JSON integers; the `tan` condition; no cut for `0`; lists that may repeat; the hash as a string; the file; strings after decoding. One further rule is stated on which the two checkers of version 2.6 DIFFER: a node id is a non-empty string (section 7; the Python checker of 2.6 rejects the empty id, the Node checker of 2.6 accepts it).
No lemma of version 2.6 is changed; section 2 is unchanged word for word; sections 6 and 7 are unchanged except for three sentences that belong to (5): the list of an option split may repeat (section 6), the wording of closure (a) and the rule on node ids (section 7). The new lemmas are the LIFTING LEMMA (4.10), the TERM LEMMA and the CLAIM of section 5, and the two proofs of section 8 with centres. The text of version 2.6 is `SPEC.md` with SHA-256 fa14fe405635d28bb16a66febe1370db766df2b90317d437472af6eb389d8aa3; this file is that text with the changes listed here and nothing else.
Corrected after the audit `reviews/REVIEW_30.md` (MUST-1 to MUST-15, SHOULD 1 to 12, and the ten replacements R1 to R10 of its part G); the audited candidate is `SPEC_v3.0_candidate_audited.md` (SHA-256 2cec6f7275580cb7ec71bdfc48d8cc57f988b69f5acedf25f558d5085d0ca908).

Author of versions 1 to 2.6: lead of the window-extension session, 2026-10-08. Version 2.6 (16:58; 2.6 = 2.5.1 plus two OPTIONAL header fields and nothing else: `labels` (16 or 17: with 17 the square at list position 4 is a label like the others) and `S_floor` (a lower end of the side interval that the statement covers, default 4); they change section 0 (label set, the statement (ANN), "the reference file"), one sentence in section 1, three sentences in section 7 (root conditions, the THEOREM, its proof), the header rules of section 10 and the first paragraph of section 11; every lemma of sections 2 to 8 is unchanged and never depended on the number of labels. A certificate without the two fields means exactly what it meant under 2.5.1, whose text is kept as `SPEC_v2.5.1.md`). Version 2.5.1 (12:35; 2.5.1 only makes explicit which evidence each of the two forms of the closure "infeasible" needs, section 10; the cross-test of the two checkers had shown two readings, both sound). Version 2.5 (12:15; 2.5 = 2.4 with the three points H1-H3 of the fourth audit, `reviews/SPEC_AUDIT_4.md`, which found both new lemmas correct: the vectors of 4.8 renamed V^± with a warning, "else 1" in kind Ps, wording). Version 2.4 (12:00) = 2.3 plus two fact families that are exact at an axis direction: wall support facts `wsup` (new section 4.8) and the kind "Ps" of a parallel class (end of section 4.6), with their names in section 10; nothing else changed; the previous version is kept as `SPEC_v2.3.md`). Version 2.3 (10:55; 2.3 = 2.2 plus the five minor points D1-D5 of the third audit, `reviews/SPEC_AUDIT_3.md`, which found nothing a literal checker would accept wrongly). 2.1 added the closure "all 8 options of a pair excluded"; 2.2 incorporates the second audit (`reviews/SPEC_AUDIT_2.md`: one fatal contract hole E4, one critical ambiguity U7, minor points M1-M9, all fixed here) and adds custom linear forms (section 3). Version 1 was audited by an
independent referee (`reviews/SPEC_AUDIT_1.md`: no false mathematical statement; three contract errors E1-E3,
six critical ambiguities U1-U6, four proof gaps G1-G4). Version 2 incorporates every required change of that
audit; the mathematics of the lemmas is unchanged.

This file is the contract between the certificate GENERATOR and the independent CHECKER. Sections 0 to 10 are
normative for the checker. Section 11 says what the application must add. Section 12 is advice for generators.
All numbers in certificates are exact rationals. The only analytic inequality used anywhere is
x - x^3/6 <= sin x <= x for 0 <= x <= pi/2 (section 8); everything else is polynomial algebra, the monotonicity
and concavity of sin and cos on quarter circles, and the separating-axis lemma.

THE TWO SCHEMAS. A certificate names its schema in its header: "wx-cert-2" or "wx-cert-3" (section 10). A
passage, item or sentence marked (wx-cert-3) applies only to certificates with the schema "wx-cert-3"; for a
certificate with the schema "wx-cert-2" it does not exist, and the element it introduces is rejected there
(SCHEMA RULE, section 10). Everything that is not so marked applies to both.

## 0. What is proved

Squares and labels: the LABEL SET I of a certificate is fixed by its header (section 10): I = {1,...,17} minus
{4} (sixteen labels; the default, and the only case before version 2.6) or I = {1,...,17} (header field
`labels` = 17). Labels = order (1-based) of the `squares` list of the reference file (the file whose SHA-256
is in the header; for the windows around the known packing this is `upper-packing-certificate.json`, whose
square 4, file centre about (3.1755, 0.5), is the rattler). With sixteen labels the square at list position 4
is never used: the sixteen other squares of a packing of 17 squares form a feasible configuration in the
sense below, so every statement proved for all feasible configurations holds for them. With seventeen labels
all squares of the packing are used. Everything below is written for an arbitrary label set I; "16 labels"
in a format rule means "the labels of I".

A CONFIGURATION is a side S > 0 and, for each i in I, a centre q_i in R^2 and a unit vector a_i (the direction
of one side of square i). Put b_i := J a_i, J(x,y) := (-y,x). Square i is {q_i + x a_i + y b_i : |x|,|y| <= 1/2};
its corners are q_i + (e1 a_i + e2 b_i)/2, e1,e2 in {+1,-1}.
FEASIBLE means: (F1) every corner of every square lies in [0,S]^2 (the container has a corner at the origin);
(F2) any two squares of I have disjoint interiors.
A PAIR is a set {i, j} of two DIFFERENT labels of I. Every ordered pair (o,t), option (o, t, axis, eps), class
of a pair, relative arc and pair closure in this SPEC presupposes two different labels of I.

The engine proves statements of the form

    (ANN)  every feasible configuration with S_floor <= S <= Sref that lies in the window W lies in the tube T,

Sref := 4675530093604551/10^15 (the `side` of the packing file); S_floor is the rational number of the header
field `S_floor`, or 4 if the header has no such field (then the condition S_floor <= S holds for every
feasible configuration, because sixteen unit squares with disjoint interiors do not fit into a smaller
square, and (ANN) reads as before version 2.6). W and T are given by rational data (section 8).
(ANN) is a statement for one frame and one labelling.

## 1. Reference data and coordinates

From the packing file: for each i the rational centre p_i^file and the rational parameter t_i; the reference
direction u_i := ((1-t_i^2)/(1+t_i^2), 2 t_i/(1+t_i^2)), v_i := J u_i.
(For every i in I, in particular for i = 4 when I has seventeen labels.)
Reference centres: p_i := p_i^file for i != 13, and p_13 := p_13^file - (T0/3) v_13 with
T0 := u_9x * (u_9x + 4 - Sref)   (u_9x = first coordinate of u_9).
Frames: (e_i1, e_i2) := (u_i, v_i) for i in {11, 13}; (e_i1, e_i2) := ((1,0),(0,1)) for all other i.
Position coordinates of a configuration: xi_ik := e_ik . (q_i - p_i), so q_i = p_i + xi_i1 e_i1 + xi_i2 e_i2.

(For the reader, not used by the checker: in the notation of the Codex local theorem the three "sliders" are
a = -xi_{2,1}, b = -xi_{11,2}, z = xi_{13,2}; the other 29 position coordinates (with sixteen labels; 31 with seventeen) are its "core" coordinates.)

A ROTATION is a pair (g, s) in Q^2 with g^2 + s^2 = 1. Rotations are multiplied as complex numbers g + i s;
conj(g, s) := (g, -s); a rotation acts on a vector as multiplication. For a rotation P write cos P := g,
sin P := s, and angle(P) for its angle in (-pi, pi].

## 2. Nodes

A NODE N is created with the following DATA (all rational):
- a position box: lo_ik <= hi_ik for i in I, k in {1,2};
- for each i in I a CENTRE rotation rho_i and two ENDPOINT rotations P_i^-, P_i^+ with
  cos P_i^- > 0, cos P_i^+ > 0, sin P_i^- <= sin P_i^+;
- a side interval S_lo <= S_hi;
- a list of ASSUMPTIONS (section 6).

Node-centre directions: abar_i := rho_i * u_i, bbar_i := J abar_i (rational unit vectors).
For a configuration and a square i define psi_i by a_i = R(psi_i) abar_i, psi_i taken in (-pi, pi]
(R(x) = rotation by the angle x). The ARC of square i is the set of directions
{R(psi) abar_i : psi^- <= psi <= psi^+}, psi^± := angle(P_i^±); both lie in (-pi/2, pi/2) and psi^- <= psi^+
because of the conditions on P_i^±.

F(N) := the set of feasible configurations with: xi_ik in [lo_ik, hi_ik] for all i,k; a_i in the arc of
square i for all i; S in [S_lo, S_hi]; and all assumptions of N satisfied.
**F(N) is defined by the data N has when it is created and never changes.**

The BOUND STORE of N is a collection of statements, each true for every configuration of F(N). It consists of:
a box (intervals for the xi_ik), arc endpoints for each square (rotations relative to the FIXED centre rho_i,
with positive cosine), a side interval, optional relative-arc endpoints for pairs (4.3), and CUTS: bounds
"F >= v" or "F <= v" for named forms F (section 3). The initial store is the node's data with no relative-arc
entries and no cuts. Rounds (section 5) replace store entries by other true statements.
A store is EMPTY if it contains one of these contradictions: lo > hi for a coordinate; S_lo > S_hi;
sin P_i^- > sin P_i^+ for the two endpoints of an arc; sin R^- > sin R^+ for the EFFECTIVE endpoints of a pair
(4.3: both exist and both have positive cosine; default endpoints with non-positive cosine never count); a cut
pair F >= v, F <= w with v > w; or an empty intersection in a store bound (section 3). Then F(N) is empty; the
checker builds no fact from such a store and the node is closed as infeasible (section 7).

For a configuration of F(N) put C_i := cos psi_i, s_i := sin psi_i. Then
    a_i = C_i abar_i + s_i bbar_i,   b_i = C_i bbar_i - s_i abar_i,
and the corner (e1,e2) of square i is q_i + C_i w + s_i J w with w := (e1 abar_i + e2 bbar_i)/2 (the
node-centre corner offset).

## 3. Base variables and named forms

BASE VARIABLES: xi_ik (two for every label of I: 32 with sixteen labels, 34 with seventeen), S, C_i, s_i (again 32 or 34). A POLYNOMIAL is an element of Q[base variables]; on a
configuration of F(N) it is evaluated with the true values of xi, S, C_i = cos psi_i, s_i = sin psi_i.

(wx-cert-3) INDICATOR VARIABLES. In a round of a node there are, besides the base variables, the INDICATOR
VARIABLES of that round: for every pair {i,j}, i < j, that has an `ind` declaration in the round (4.10) with a
list of m options, the m - 1 variables z_{ij,1}, ..., z_{ij,m-1} (none if m = 1). They belong to the round: the
indicator variables of two rounds, also of the same node and the same pair, have nothing to do with each other.
An EXTENDED POLYNOMIAL of the round is an element of Q[base variables, indicator variables of the round]; it is
evaluated at a pair (x, z), x a configuration and z a real number for every indicator variable of the round.
An indicator variable has NO NAME in a certificate: it occurs in no named form, no polynomial form, no
objective of a step, no store, no cut and no `centre`; it enters a step only through the names `ind:i:j:k`
of 4.10.

NAMED FORMS (polynomials; o, t, i, j are labels; "(o,t)" is an ordered pair, "i:j" always has i < j):
- `xi:i:k`, `S`, `C:i`, `s:i`: the base variables.
- `Da:o:t` := abar_o . (q_t - q_o),  `Db:o:t` := bbar_o . (q_t - q_o)   (affine in xi; q = p + xi_1 e_1 + xi_2 e_2).
- `A:o:t` := C_o * Da_ot + s_o * Db_ot      (true value: a_o . (q_t - q_o))
- `B:o:t` := C_o * Db_ot - s_o * Da_ot      (true value: b_o . (q_t - q_o))
- `Cr:i:j` := C_i C_j + s_i s_j              (true value: cos(psi_j - psi_i))
- `Sr:i:j` := C_i s_j - s_i C_j              (true value: sin(psi_j - psi_i))
- class forms of a parallel class K of the pair i<j (4.6): `al:i:j:K`, `be:i:j:K`, `co:i:j:K`, `si:i:j:K`,
  `Y:i:j:K`. A class is K = (axis_i, eps_i, axis_j, eps_j), axis in {a,b}, eps in {+1,-1}; in names it is
  written as four characters, e.g. `a+b-`. The class is part of the name; forms of different classes are
  different polynomials.
- custom forms `u:NAME` (NAME matching [A-Za-z0-9_]+), defined in the node's `forms` field (section 10) as a NONEMPTY list of components [coef_m, F_m], standing for the rational linear
  combination sum_m coef_m * F_m of named forms F_m of the kinds listed above (not `0`, not
  another custom form). A custom form is AFFINE if all its F_m are among `xi:i:k`, `Da:o:t`, `Db:o:t`.
- (wx-cert-3; not a named form) POLYNOMIAL FORMS `q:NAME` (NAME matching [A-Za-z0-9_]+), defined in the
  node's `forms` field (section 10) as a nonempty list of ENTRIES [coef, [v_1, ..., v_r]] with r in {0, 1, 2},
  coef a rational number and every v_l the name of a base variable (`xi:i:k`, `S`, `C:i`, `s:i`, labels of I).
  An entry stands for coef * v_1 * ... * v_r: for r = 0 the constant coef, and v_1 = v_2 is allowed (coef times
  the square of that variable). The form is the sum of its entries, a polynomial of degree at most 2 in the base
  variables. The monomials of the entries of one form, taken as multisets {v_1, ..., v_r}, are pairwise
  different (so [x, y] and [y, x] in one form are rejected); the coefficient 0 is allowed (such an entry
  contributes nothing, but its monomial counts for this rule).
  A polynomial form is NOT a named form of this section: it has no store bound SB, it cannot carry a cut, it
  cannot be the objective of a step or a component of a custom form, and `q:NAME` is not among the form NAMEs
  of section 10. It is used only through the names `sq:NAME` and `pol:NAME` of 4.9. Polynomial forms and custom
  forms have separate name spaces: a node may define `u:X` and `q:X`, and they have nothing to do with each
  other. Like the custom forms, the polynomial forms belong to the node's data: they are the same in all rounds
  of the node and are not inherited by children.
- `0`: the zero polynomial.
For an ordered pair (o,t): cos(psi_t - psi_o) = Cr (of the unordered pair) and sin(psi_t - psi_o) = +Sr_ij if
(o,t) = (i,j), -Sr_ij if (o,t) = (j,i).

STORE BOUNDS. For every named form F the checker computes, from a given store (the store at the start of a
round, or the final store of a node), an interval SB(F) = [SBlo(F), SBhi(F)] that contains F(x) for all x in
F(N), by exactly these rules (interval arithmetic with exact rationals; "cap cut" means: intersect with the cut
values of the store stored under that exact name; if such an intersection is empty, the store is EMPTY in the
sense of section 2). Cuts stored under the name of a base variable (`xi:i:k`, `S`, `C:i`, `s:i`) are NOT used
in SB (the box, the side interval and the arc endpoints carry that information).
- `xi:i:k`: the store box. `S`: the store side interval.
- `s:i`: [sin P_i^-, sin P_i^+]. `C:i`: [min(cos P_i^-, cos P_i^+), cmax] with cmax := 1 if
  sin P_i^- <= 0 <= sin P_i^+, else max(cos P_i^-, cos P_i^+).
- `Da:o:t`, `Db:o:t`: IA := constant + sum over xi of coefficient * SB(xi); SB := IA cap cut.
- `A:o:t`: (SB(C:o) * SB(Da:o:t) + SB(s:o) * SB(Db:o:t)) cap cut.
  `B:o:t`: (SB(C:o) * SB(Db:o:t) - SB(s:o) * SB(Da:o:t)) cap cut.
- `Cr:i:j`, `Sr:i:j`: if the pair has effective relative-arc endpoints R^-, R^+ (4.3):
  SB(Sr) := [sin R^-, sin R^+] cap cut, SB(Cr) := [min(cos R^-, cos R^+), cmax] cap cut with cmax as for `C:i`
  (1 if sin R^- <= 0 <= sin R^+, else the larger cosine); otherwise [-1, 1] cap cut.
- class forms: by the dictionary of 4.6 from SB(A), SB(B), SB(Cr), SB(Sr) with interval arithmetic, then cap cut.
- custom forms `u:NAME`: sum_m coef_m * SB(F_m) (interval arithmetic), then cap cut.
- (wx-cert-3) an indicator variable z_{ij,k} of the round (above): SB := [0, 1], for every store. There is no
  store entry and no cut for an indicator variable, and nothing ever changes this interval.
The EMPTY test (section 2) is made on the store at the start of every evaluated round and on the final store.
Besides the box, the side interval, the arcs and the cut pairs it covers: every pair that has a stored
relative-arc endpoint and effective endpoints on both sides (sin R^- > sin R^+), and every form that has a cut
in the store, base variables excepted (empty intersection in its SB). (A form without a cut cannot have an
empty SB unless one of its components with a cut has one.)
(The start store of an evaluated round is never EMPTY: the node's data cannot be EMPTY, and after an EMPTY store no round is evaluated.)

## 4. Facts

A FACT of N (for a given store) is a named polynomial f with f(x) >= 0 for every x in F(N). Facts are rebuilt
by the checker from the store at the start of each round. Complete list:
(wx-cert-3) Besides facts, a term of a step (section 5) may contain names of three kinds that are NOT facts in
the sense just defined: `pol:NAME` (4.9), which has no sign; `ind:i:j:k` (4.10), which contains indicator
variables; and the corner polynomials of an option listed in an `ind` declaration (4.5, 4.10), which need not
be >= 0 on F(N). The TERM RULES of section 5 say when such a name may stand in a term, and the TERM LEMMA there
is what replaces "f(x) >= 0 on F(N)" for them.

### 4.0 Box, side, interval and cut facts
- `box:i:k:lo` := xi_ik - lo, `box:i:k:hi` := hi - xi_ik (store box). `side:lo` := S - S_lo, `side:hi` := S_hi - S.
- `ivl:F:lo` := F - IAlo(F), `ivl:F:hi` := IAhi(F) - F for an AFFINE form F: `Da:o:t`, `Db:o:t`, or an affine
  custom form `u:NAME`. Here F is first written as c0 + sum_ik c_ik xi_ik (like terms combined) and
  IAlo(F) := c0 + sum_ik min(c_ik lo_ik, c_ik hi_ik), IAhi(F) := c0 + sum_ik max(c_ik lo_ik, c_ik hi_ik) over the
  store box (no cuts).
- `cut:F:lo` := F - v and `cut:F:hi` := v - F for every cut "F >= v" / "F <= v" in the store (F any named form
  except `0`).
- `circ:i` := C_i^2 + s_i^2 - 1. This polynomial is IDENTICALLY ZERO on configurations; it is the only
  "fact" that may be used with a multiplier of either sign (section 5).

### 4.1 Walls (degree 1)
For i in I, corner (e1,e2), coordinate k in {x,y}: X := (p_i + xi_i1 e_i1 + xi_i2 e_i2 + C_i w + s_i J w)_k.
`wall:i:e1:e2:k:lo` := X,   `wall:i:e1:e2:k:hi` := S - X.      Proof: (F1).
(All four corners in [0,S]^2 is equivalent to the square lying in [0,S]^2, by convexity.)

### 4.2 Arc facts (degree 1), from the store endpoints P^- = (g^-, s^-), P^+ = (g^+, s^+) of square i
- `arc:i:slo` := s_i - s^-,  `arc:i:shi` := s^+ - s_i,  `arc:i:clo` := C_i - min(g^-, g^+),
  `arc:i:chi` := cmax - C_i (cmax as in section 3).
- `arc:i:chord` := (C_i - g^-)(s^+ - s^-) - (s_i - s^-)(g^+ - g^-).
- `arc:i:tan:G:H` := 1 - G C_i - H s_i for any rationals G, H with G^2 + H^2 <= 1 (checked as part of the name, section 10).
Proof: psi^- <= psi_i <= psi^+ inside (-pi/2, pi/2); sin is increasing there; cos is concave there, so its
minimum is at an endpoint, and it is monotone if 0 is not in the interval. Chord: with x := psi^+ - psi >= 0,
y := psi - psi^- >= 0, x + y < pi: (P - P^-) x (P^+ - P^-) = sin x + sin y - sin(x+y)
= sin x (1 - cos y) + sin y (1 - cos x) >= 0. Tangent: Cauchy-Schwarz.

### 4.3 Relative arc facts (degree 2), pair i < j
omega := psi_j - psi_i. DEFAULT endpoints from the store arcs: D^- := P_j^- * conj(P_i^+),
D^+ := P_j^+ * conj(P_i^-). The store may hold replaced endpoints St^-, St^+ for the pair (section 5).
EFFECTIVE endpoints R^-, R^+: among the candidates {D^-, St^-} with positive cosine, R^- is the one with the
larger sine; among {D^+, St^+} with positive cosine, R^+ is the one with the smaller sine. If one side has no
candidate with positive cosine, the pair has no effective relative arc (no `rarc` facts, SB = [-1,1]).
Facts, with (Cr, Sr) := (Cr_ij, Sr_ij) and R^± = (g^±, s^±): `rarc:i:j:slo`, `shi`, `clo`, `chi`, `chord`,
`rarc:i:j:tan:G:H`: exactly the polynomials of 4.2 with (Cr, Sr) in place of (C_i, s_i).
Proof: psi_j^- - psi_i^+ and psi_j^+ - psi_i^- are differences of two numbers of (-pi/2, pi/2); they lie in
(-pi, pi) and are the angles of D^- and D^+. On (-pi, pi) the cosine is positive only on (-pi/2, pi/2). So if
cos D^- > 0 then omega >= angle(D^-) > -pi/2, and if cos D^+ > 0 then omega <= angle(D^+) < pi/2. A stored
endpoint St^- is only ever accepted (section 5) when the minus side already has an R^-, so
omega >= angle(R^-) > -pi/2, and either sin St^- <= sin R^-, whence angle(St^-) <= angle(R^-) <= omega, or
sin St^- <= L for a certified bound Sr_ij >= L, whence omega >= angle(St^-) (for omega < pi/2 because sin is
increasing on (-pi/2, pi/2), for omega >= pi/2 trivially). Symmetrically for St^+. Hence
-pi/2 < angle(R^-) <= omega <= angle(R^+) < pi/2, and the proof of 4.2 applies to (cos omega, sin omega).

### 4.4 Products
There are no separate "McCormick" facts: a McCormick inequality is a product of two degree-1 facts (a bound
fact of C_o or s_o times a `box`, `ivl` or `cut` fact) and is covered by the product rule of section 5.

### 4.5 Option facts (degree 2)
SAT LEMMA. If two closed unit squares o', t' have disjoint interiors, then at least one of the 8 OPTIONS
(o, n; t) holds: {o,t} = {o',t'}, n in {a_o, -a_o, b_o, -b_o}, and n . (x - q_o) >= 1/2 for every corner x of
square t.
Proof: write i, j for the two squares. K := square_i - square_j (Minkowski difference) is a convex polygon
with nonempty interior. 0 is not an interior point of K: the set G := int(square_i) - int(square_j) is open,
convex and dense in K, hence G = int K (an open convex set equals the interior of its closure); and 0 in G would
give a common interior point of the two squares. So some edge of K has an outward normal nu with
max_K nu.x <= 0, i.e.
max over square_i of nu.x <= min over square_j of nu.x. Every edge of K is parallel to an edge of square_i or of
square_j, so nu is one of +-a_i, +-b_i, +-a_j, +-b_j. If nu = n in {+-a_i, +-b_i}: max over square_i of n.x =
n.q_i + 1/2, so n.(x - q_i) >= 1/2 on square_j: option (i, n; j). If nu in {+-a_j, +-b_j}: m := -nu satisfies
max over square_j of m.x <= min over square_i of m.x, and max over square_j of m.x = m.q_j + 1/2: option (j, m; i).

An option is written (o, t, axis, eps): n = eps * a_o if axis = a, eps * b_o if axis = b.
Facts of option (o, t, axis, eps), one per corner (e1,e2) of t, with w := (e1 abar_t + e2 bbar_t)/2 and
nbar := eps * abar_o or eps * bbar_o:
`opt:o:t:axis:eps:e1:e2` := eps * (A_ot or B_ot) + (nbar . w) * cos(psi_t - psi_o)
                            + (nbar . J w) * sin(psi_t - psi_o) - 1/2
with cos, sin of the ordered pair expressed by Cr, Sr as in section 3.
Proof that this is n.(corner of t - q_o) - 1/2: n = C_o nbar + s_o J nbar; n.(q_t - q_o) = eps*A_ot or
eps*B_ot; corner offset of t = C_t w + s_t J w; and (C_o nbar + s_o J nbar).(C_t w + s_t J w)
= (C_o C_t + s_o s_t)(nbar.w) + (C_o s_t - s_o C_t)(nbar.Jw), using J nbar . J w = nbar . w and
J nbar . w = - nbar . J w.
VALIDITY: these four polynomials are facts of N only if the option holds on all of F(N): because N ASSUMES it
(section 6), or because the 7 other options of the pair are EXCLUDED (4.7) on the store at the start of the round.
An option is called OPT-AVAILABLE in a round if the round has an `opt` declaration of it (section 10; the
precondition of the declaration is the VALIDITY condition above, and a declaration whose precondition fails
rejects the certificate). (wx-cert-3) An option is called IND-LISTED in a round if it is in the list of an
`ind` declaration of the round (4.10). A pair has declarations of at most one of these two kinds in a round
(4.10, R2), so no option is both. For an IND-LISTED option the four names `opt:o:t:axis:eps:e1:e2` denote the
same four polynomials as above; they are then NOT facts, and they may stand in a term only under the GUARD RULE
(T3) of section 5.

### 4.6 Parallel class facts (degree 2)
Pair i < j, d := q_j - q_i. A CLASS K = (axis_i, eps_i, axis_j, eps_j) defines unit vectors
n_i := eps_i * (a_i or b_i) and n_j := eps_j * (a_j or b_j). ITS TWO OPTIONS are, in the notation of 4.5,
O_i := (i, j, axis_i, eps_i) and O_j := (j, i, axis_j, -eps_j)   (note the sign: O_j has normal -n_j).
Class quantities:  al := n_i . d,  be := n_j . d,  co := n_i . n_j,  si := (J n_i) . n_j,
Y := (J n_i + J n_j) . d.   (So n_j = co n_i + si J n_i.)
Dictionary (polynomials; nbar_i, nbar_j the node-centre versions; cbar := nbar_i . nbar_j,
sbar := (J nbar_i) . nbar_j; Cr, Sr of the pair i<j):
    co = cbar * Cr - sbar * Sr,        si = sbar * Cr + cbar * Sr,
    al = eps_i * A_ij if axis_i = a,   al = eps_i * B_ij if axis_i = b,
    be = - eps_j * A_ji if axis_j = a, be = - eps_j * B_ji if axis_j = b,
    J n_i . d = eps_i * B_ij if axis_i = a,   = - eps_i * A_ij if axis_i = b,
    J n_j . d = - eps_j * B_ji if axis_j = a, = + eps_j * A_ji if axis_j = b,
    Y = (J n_i . d) + (J n_j . d).
Support values: O_i holds iff al >= (1 + |co| + |si|)/2; O_j holds iff be >= (1 + |co| + |si|)/2
(the support function of a unit square in a unit direction n is (|n.a| + |n.b|)/2, and {|n_i.a_j|, |n_i.b_j|}
= {|co|, |si|} = {|n_j.a_i|, |n_j.b_i|}).
Identity: be - al = si * Y / (1 + co) whenever co > -1.
[be - al = (co - 1) al + si (Jn_i.d);  Y = (1 + co)(Jn_i.d) - si al;  si^2 = (1 - co)(1 + co).]

LEMMA P. Let x be a configuration with co > -1 at which O_i or O_j holds. Then:
- (P+) if 0 <= Y <= 1 + co:    be >= (1 + co + si)/2  and  al >= (1 + co - si)/2.
- (P-) if -(1 + co) <= Y <= 0:  al >= (1 + co + si)/2  and  be >= (1 + co - si)/2.
- (Pk) if |Y| <= Ybar, co >= cmin > -1 and 0 <= kappa <= 1 - Ybar/(1 + cmin):
       al + be >= 1 + co + kappa * si   and   al + be >= 1 + co - kappa * si.
Proof. Write m := (1 + co + |si|)/2; note |co| >= co, so O_i gives al >= m and O_j gives be >= m.
(P+): O_i, si >= 0: be = al + si Y/(1+co) >= al >= m = (1+co+si)/2; al >= m >= (1+co-si)/2.
      O_i, si < 0:  al >= m = (1+co-si)/2; be >= (1+co-si)/2 - |si| Y/(1+co) = (1+co+si)/2 + |si|(1 - Y/(1+co)) >= (1+co+si)/2.
      O_j, si <= 0: al = be - si Y/(1+co) >= be >= m = (1+co-si)/2; be >= m >= (1+co+si)/2.
      O_j, si > 0:  be >= m = (1+co+si)/2; al >= (1+co+si)/2 - si Y/(1+co) = (1+co-si)/2 + si(1 - Y/(1+co)) >= (1+co-si)/2.
(P-): O_i, si <= 0: si Y >= 0, so be >= al >= m = (1+co-si)/2; al >= m >= (1+co+si)/2.
      O_i, si > 0:  al >= m = (1+co+si)/2; be >= (1+co+si)/2 + si Y/(1+co) = (1+co-si)/2 + si(1 + Y/(1+co)) >= (1+co-si)/2.
      O_j, si >= 0: -si Y >= 0, so al >= be >= m = (1+co+si)/2; be >= m >= (1+co-si)/2.
      O_j, si < 0:  be >= m = (1+co-si)/2; al = be + |si| Y/(1+co) >= (1+co-si)/2 + |si| Y/(1+co)
                    = (1+co+si)/2 + |si|(1 + Y/(1+co)) >= (1+co+si)/2.
(Pk): al + be = 2 max(al,be) - |be - al| >= 1 + co + |si| - |si||Y|/(1+co) >= 1 + co + |si|(1 - Ybar/(1+cmin))
      >= 1 + co + kappa |si| >= 1 + co ± kappa si   (the last step needs kappa >= 0).

Facts (declared per round, section 10): for class K and kind in {P+, P-, Pk} (kind Ps: see below):
`par:i:j:K:P+:1` := be - (1 + co + si)/2,     `par:i:j:K:P+:2` := al - (1 + co - si)/2,
`par:i:j:K:P-:1` := al - (1 + co + si)/2,     `par:i:j:K:P-:2` := be - (1 + co - si)/2,
`par:i:j:K:Pk:1` := al + be - 1 - co - kappa*si,   `par:i:j:K:Pk:2` := al + be - 1 - co + kappa*si.
PRECONDITIONS, all tested on the store at the start of the round, with cL := SBlo(co:i:j:K) and
[YL, YU] := SB(Y:i:j:K):
- every kind: the 6 options of the pair other than O_i, O_j are excluded (4.7); and cL > 0;
- (P+): YU <= 1 + cL, and (YL >= 0 or N assumes Y >= 0 for this pair and class K);
- (P-): YL >= -(1 + cL), and (YU <= 0 or N assumes Y <= 0 for this pair and class K);
- (Pk): with Ybar := max(|YL|, |YU|): 0 <= kappa <= 1 - Ybar/(1 + cL)  (kappa is given in the declaration).
`asg:i:j:K:p` := +Y_K is a fact of N if N has the sign assumption (i, j, K, +1); `asg:i:j:K:m` := -Y_K if N has
the sign assumption (i, j, K, -1) (section 6).

KIND "Ps" (parallel support facts; added in version 2.4). The facts of kinds P+, P-, Pk contain co, which the
relaxation can lower to the chord of the relative arc; the following two facts do not, and are tight at si = 0.
Additional preconditions (besides those of every kind, and the kappa condition of (Pk) with the declared kappa):
the pair has effective relative-arc endpoints R^-, R^+ on both sides (4.3); with the rotations
E^- := (cbar, sbar) * R^-, E^+ := (cbar, sbar) * R^+:  cos E^- > 0, cos E^+ > 0, sin E^- <= 0 <= sin E^+.
Put kp := (cos E^+ + sin E^+ - 1)/sin E^+ if sin E^+ > 0, else 1; km := (cos E^- - sin E^- - 1)/(-sin E^-) if
sin E^- < 0, else 1 (1 is the limit of g(s)/s at s = 0, g as in the proof below; if sin E^+ = 0 then theta <= 0 on
F(N) and the bound co + si - 1 >= kp si is used only at theta = 0, where it holds for every kp; likewise for km);
cp := kp + kappa - 1, cm := km + kappa - 1; required: cp >= 0 and cm >= 0.
`par:i:j:K:Ps:1` := al + be - 2 - cp * si,      `par:i:j:K:Ps:2` := al + be - 2 + cm * si.
Proof. Let theta be the angle from n_i to n_j, so (co, si) = (cos theta, sin theta), and theta = angle(cbar, sbar)
+ omega with omega in [angle R^-, angle R^+]. theta runs over the counter-clockwise arc from E^- to E^+, of
length < pi; both ends are in the open right half-plane, E^- in the closed lower and E^+ in the closed upper
half; so the arc lies in (-pi/2, pi/2) and contains 0. The function g(s) := sqrt(1 - s^2) + s - 1 is concave on
[0, 1) with g(0) = 0, hence g(s) >= s * g(s^+)/s^+ for 0 <= s <= s^+ := sin E^+, i.e. co + si - 1 >= kp * si for
0 <= theta <= angle(E^+); symmetrically co + |si| - 1 >= km * |si| for angle(E^-) <= theta <= 0. From the proof
of (Pk): al + be >= 1 + |co| + |si| - |si||Y|/(1 + co) >= 1 + co + |si| - (1 - kappa)|si|.
So for si >= 0: al + be >= 2 + (kp + kappa - 1) si = 2 + cp si, which also gives al + be >= 2 >= 2 - cm si;
for si <= 0: al + be >= 2 + (km + kappa - 1)|si| = 2 - cm si, which also gives al + be >= 2 >= 2 + cp si.

### 4.7 Exclusion of an option
Option (o, t, axis, eps), n as in 4.5, requires n.(q_t - q_o) >= 1/2 + h with h := (|n.a_t| + |n.b_t|)/2.
It is EXCLUDED (on a given store) if U < 1/2 + h_lo STRICTLY, where
- U := SBhi of the form eps*A_ot (axis a) or eps*B_ot (axis b)   (for eps = -1: U = -SBlo);
- h_lo: let {i,j} = {o,t}, i < j. If the pair has effective relative-arc endpoints R^-, R^+ (4.3): for
  (o,t) = (i,j) put Q^- := R^-, Q^+ := R^+; for (o,t) = (j,i) put Q^- := conj(R^+), Q^+ := conj(R^-).
  Ebar := abar_t * conj(nbar) (nbar the node-centre version of n), E^- := Ebar * Q^-, E^+ := Ebar * Q^+.
  If cos E^- * cos E^+ >= 0 and sin E^- * sin E^+ >= 0 and cos(E^+ * conj E^-) > 0 and
  sin(E^+ * conj E^-) >= 0, then h_lo := min(|cos E^-| + |sin E^-|, |cos E^+| + |sin E^+|)/2; in every
  other case (including: no effective relative arc) h_lo := 1/2.
Proof: let theta be the angle from n to a_t; h = (|cos theta| + |sin theta|)/2 and theta = angle(Ebar) +
(psi_t - psi_o), so theta runs over the arc from E^- to E^+. (|cos| + |sin|)^2 = 1 + |sin 2x| >= 1 everywhere,
and |cos x| + |sin x| is concave on every closed quadrant. If E^- and E^+ lie in one closed quadrant and the
counter-clockwise arc from E^- to E^+ is shorter than pi/2, the arc stays in that quadrant and the minimum is
at an endpoint. If U < 1/2 + h_lo, then n.(q_t - q_o) <= U < 1/2 + h on F(N): the option holds nowhere on F(N).

### 4.8 Wall support facts (degree 1; added in version 2.4)
For a square i and a store, let V^- := P_i^- * abar_i and V^+ := P_i^+ * abar_i (the direction a_i ITSELF at the
two ends of the store arc; unit vectors in Q^2. These are NOT the rotations Ab^± = rho_i * P_i^± of section 8:
V^± = Ab^± * u_i, and the two agree only if u_i = (1,0)). The facts exist only if the sign conditions
    V^-_x > 0,  V^+_x > 0,  V^-_y <= 0 <= V^+_y        (the arc contains the direction of the x-axis)
hold. For a square whose arc does not contain the x-axis direction (in a small window: every tilted square) there
are no `wsup` facts.
Put kp := (V^+_x + V^+_y - 1)/V^+_y if V^+_y > 0, else 0; km := (V^-_x - V^-_y - 1)/(-V^-_y) if
V^-_y < 0, else 0; sigma := C_i * abar_i,y + s_i * bbar_i,y (the y-component of a_i). For each wall
W in {xlo, ylo, xhi, yhi}, with D_W := q_i,x, q_i,y, S - q_i,x, S - q_i,y respectively (q_i = p_i + xi_i1 e_i1 +
xi_i2 e_i2):
    `wsup:i:W:p` := D_W - 1/2 - (kp/2) * sigma,        `wsup:i:W:m` := D_W - 1/2 + (km/2) * sigma.
Proof. Write a_i = (cos t, sin t). By the sign conditions (and because the arc is the counter-clockwise arc
from V^- to V^+ of length < pi) t runs over [t^-, t^+] inside (-pi/2, pi/2) with t^- <= 0 <= t^+, and
sigma = sin t. (F1) for the wall W says D_W >= (|cos t| + |sin t|)/2: the corners are q_i + (e1 a_i + e2 b_i)/2
with b_i = (-sin t, cos t), so the smallest distance of a corner from each wall is D_W minus that support value.
With g as in 4.6: cos t + sin t >= 1 + kp sin t for 0 <= t <= t^+ and cos t + |sin t| >= 1 + km |sin t| for
t^- <= t <= 0. If sigma >= 0: D_W >= (1 + kp sigma)/2 (first fact), and (1 - km sigma)/2 <= 1/2 <= D_W (second
fact, because |cos t| + |sin t| >= 1). If sigma <= 0: symmetric. kp, km >= 0 because x + |y| >= 1 for every unit vector (x, y) with x >= 0.

### 4.9 Squares and sign-free multipliers (wx-cert-3)
For a polynomial form q:NAME of the node (section 3):
- `sq:NAME` := (q:NAME)^2. A fact of N in every round and for every store, without precondition.
  Proof: the square of a real number is >= 0.
- `pol:NAME` := q:NAME. NOT a fact: it carries no sign. The name may occur only in a term that also contains a
  `circ` fact (section 5, rule (T2)); such a term is zero at every configuration, for all values of the indicator variables, whatever the value of
  q:NAME (TERM LEMMA).
Both names require that q:NAME is defined in the `forms` of the node; otherwise the certificate is rejected,
also if the name stands in a round that is not evaluated.

### 4.10 Indicators for a pair (wx-cert-3)
(For the reader: a pair whose option is not decided on a node can be left undecided inside a step. Each option
of the pair that is still possible gets an indicator, a number that is 1 for one option that holds and 0 for
the others, and a corner inequality of an option is used only multiplied by the indicator of that option. This
replaces an option split by terms of the step.)
DECLARATION. A round may contain, for a pair {i,j}, i < j, an `ind` declaration (section 10) with a list
Lst = (O_1, ..., O_m), 1 <= m <= 8, of pairwise different options of that pair (the pair has the 8 options
(i, j, axis, eps) and (j, i, axis, eps), axis in {a, b}, eps in {+1, -1}).
RESTRICTIONS (well-formedness; a violation rejects the certificate):
(R1) a round has at most one `ind` declaration per pair;
(R2) a round does not contain an `opt` declaration and an `ind` declaration of the same pair;
(R3) a pair for which the node has an option ASSUMPTION (section 6) has no `ind` declaration in any round of
     that node.
(The tree either branches on a pair or keeps it undecided, never both. Sign assumptions and `par` declarations
of the pair are not concerned.)
(The LIFTING LEMMA uses none of (R1) to (R3). (R1) makes the indicator variables of a pair well defined; (R2) and (R3) keep one option from being a fact and a guarded name in the same round or node.)
PRECONDITION. The declaration is VALID iff every option of the pair that is NOT in Lst is EXCLUDED on the store
at the START OF THE ROUND, by the test of 4.7 exactly as it stands (U and h_lo computed from that store: its
box, arcs, stored relative-arc endpoints and cuts). An option of Lst may itself be excluded on that store; this
does not make the declaration invalid. A declaration that is not valid rejects the certificate (section 5,
REJECTION).
INDICATORS. For a valid declaration the pair has the m INDICATOR POLYNOMIALS
    ind_k := z_{ij,k} for 1 <= k < m,        ind_m := 1 - z_{ij,1} - ... - z_{ij,m-1}
(for m = 1: ind_1 := 1, and the pair has no indicator variable). So ind_1 + ... + ind_m = 1 identically. The
LAST option of the list is the one without a variable.
NAME. `ind:i:j:k` := ind_k, available iff the round has an `ind` declaration of the pair {i,j} and
1 <= k <= m. It is an extended polynomial of the round (section 3). There is no other name for an indicator:
none for the product of an indicator with a corner polynomial, and none for ind_k^2 - ind_k.

LIFTED POINT. Let St be the store at the start of the round and x a configuration of F(N). For every pair
{i,j} with an `ind` declaration in the round let k0 be the SMALLEST index k such that the option O_k of its
list holds at x (4.5: n . (c - q_o) >= 1/2 for every corner c of square t), and put
    ind*_k0 := 1,   ind*_k := 0 for k != k0,   z*_{ij,k} := ind*_k for 1 <= k < m.
The LIFTED POINT of x is (x, z*), z* the collection of these numbers over all such pairs. (In a round without
`ind` declarations there are no indicator variables, and the lifted point of x is x.)
LIFTING LEMMA. For every x in F(N) the lifted point exists (k0 exists for every pair with an `ind`
declaration in the round), and at the lifted point:
(L1) every indicator variable has a value in [0, 1];
(L2) for every declared pair and every k = 1, ..., m the polynomial ind_k has the value ind*_k, which is 0 or 1;
(L3) if ind*_k = 1, the option O_k holds at x.
Proof. x is feasible, so squares i and j have disjoint interiors (F2), and by the SAT lemma (4.5) at least one
of the 8 options of the pair holds at x. x lies in F(N), so x satisfies every statement of St (section 2). An
option of the pair that is not in Lst is excluded on St (the declaration is valid), and an option that is
excluded on St holds at no configuration of F(N) (4.7). Hence every option that holds at x is in Lst, at least
one option does hold at x, and k0 exists. (L1): the values are 0 or 1. (L2): for k < m, ind_k is the variable
z_{ij,k}, with value ind*_k; for k = m the value is 1 - sum_{k<m} ind*_k, which is ind*_m because exactly one
of ind*_1, ..., ind*_m is 1 and the others are 0. (L3): the only index with ind*_k = 1 is k0, and O_k0 holds at
x by its choice.
(The lemma needs of the list only that every option left out holds nowhere on F(N). An option of the list that
holds nowhere on F(N), for instance one that the store excludes, does no harm: it is never the option of index
k0, so its indicator is 0 at every lifted point. That is why a listed option may be excluded, and why the
precondition is tested on the store and not on the node's data.)

## 5. Inference: steps, rounds, store updates

STEP. Given the store at the start of a round, its facts and its declarations: an objective polynomial g (a
named form, or its negative; a named form contains no indicator variable), and a list of TERMS
(lambda_k, [names]), each with 1 to 3 names. A name is a fact name or, (wx-cert-3), `pol:NAME` (4.9),
`ind:i:j:k` (4.10) or the corner name `opt:o:t:axis:eps:e1:e2` of an IND-LISTED option (4.5). The same name may
occur more than once in a term.
TERM RULES. They hold for every term, whatever its multiplier, also for the multiplier 0; a term that violates one of them rejects the certificate. (T1) and (T2) are tested on the whole file. (T3) and (T4) are tested in the evaluated rounds, with one exception: a condition that is part of a name (list (W) of section 10; for example that the `q:NAME` of a `sq` or `pol` name is defined in the node's `forms`) is tested on the whole file (section 10, WHERE EACH TEST IS MADE):
(T1) lambda_k >= 0, except that a term which contains a `circ` fact may have a multiplier of either sign.
(T2) (wx-cert-3) `pol:NAME` may occur only in a term that contains a `circ` fact.
(T3) (wx-cert-3) GUARD RULE. For every name `opt:o:t:axis:eps:e1:e2` in the term whose option
     O = (o, t, axis, eps) is IND-LISTED in the round, say O = O_k in the list of the `ind` declaration of the
     pair {i,j} = {o,t}: the term also contains the name `ind:i:j:k` with THAT k. This is required of every
     term, also of a term that contains a `circ` fact. (The indicator of another option of the pair does not
     serve as the guard.)
(T4) AVAILABILITY. Every name is available in the round. A fact name of 4.0 to 4.4 or of 4.6 to 4.8: by the
     rules stated there. A name `opt:o:t:axis:eps:e1:e2`: iff its option is OPT-AVAILABLE (4.5) or,
     (wx-cert-3), IND-LISTED in the round. (wx-cert-3) `sq:NAME` and `pol:NAME`: iff q:NAME is defined in the
     node's `forms`. `ind:i:j:k`: iff the pair {i,j} has an `ind` declaration in the round and 1 <= k <= m, m the
     length of its list.
The checker computes exactly, as a polynomial in the base variables and, (wx-cert-3), the indicator variables
of the round (an extended polynomial, section 3),
    Rem := g - sum_k lambda_k * prod(polynomials named in term k)
and a rational number L by one of two rules.
RAW RULE (a step without the field `centre`). Write Rem = sum_m r_m m, m ranging over the monomials in the
variables (like monomials combined; the constant monomial 1 included, with interval [1, 1]).
L := sum_m min(r_m * lo_m, r_m * hi_m), where [lo_m, hi_m] is the product, by interval multiplication, of the
store-bound intervals SB (section 3) of the variables of m, a variable of exponent e being multiplied e times.
(The rule is meant literally. For an even power it does not give the range of the monomial: x^2 with x in [-a, a] gets [-a^2, a^2], not [0, a^2]. A checker must not tighten it, or its L is another number.)
(wx-cert-3) CENTRED RULE (a step with the field `centre`). The field gives a rational number c_v for some BASE
variables v; c_v := 0 for every base variable it does not give and for every indicator variable. The checker
substitutes v = c_v + y_v for every variable v in Rem, expands exactly and combines like monomials in the new
variables y: Rem(c + y) = sum_m r_m m(y), the constant monomial included.
L := sum_m min(r_m * lo_m, r_m * hi_m), where [lo_m, hi_m] is the product, by interval multiplication, of the
intervals
    [SBlo(v) - c_v, SBhi(v) - c_v]
of the variables y_v of m (so [0, 1] for an indicator variable), a variable of exponent e being multiplied e
times, and [1, 1] for the constant monomial. A step WITH the field is evaluated by the centred rule also if the
field is the empty object; then every c_v is 0 and L is the number of the raw rule. A value given for a
variable that does not occur in Rem has no effect.
(In both rules L is determined by the polynomial Rem, by c and by the store bounds: the expansion of a
polynomial in monomials is unique, and the interval product of given intervals does not depend on the order of
the factors. How a checker computes L is free.)
TERM LEMMA. Let x be in F(N) and (x, z*) its lifted point (4.10; in a certificate with the schema "wx-cert-2",
and in every round without `ind` declarations, there are no indicator variables and (x, z*) is x). For every
term that obeys (T1) to (T4), the number lambda_k * prod(polynomials named in term k), evaluated at (x, z*),
is >= 0.
Proof. If the term contains a `circ` fact, that factor is 0 at every configuration (4.0) and the product is 0,
whatever the multiplier and the other factors. Otherwise lambda_k >= 0 by (T1), there is no `pol` name by
(T2), and every factor is of one of three kinds. (a) A fact of 4.0 to 4.8 that is available in the round (this
includes the corner facts of an OPT-AVAILABLE option), or a square `sq:NAME`: its value is >= 0 because x is in
F(N) (section 4, 4.9), and it contains no indicator variable. (b) `ind:i:j:k`: its value is ind*_k, which is 0
or 1, by (L2). (c) A corner polynomial of an IND-LISTED option O_k; by (T3) the term then contains a factor
`ind:i:j:k` of kind (b) for the same option. Now: if some factor of kind (b) has the value 0, the product is 0.
Otherwise every factor of kind (b) has the value 1; then every factor of kind (c) belongs to an option O_k
with ind*_k = 1, that option holds at x by (L3), and the value of the factor is
n . (corner (e1,e2) of t - q_o) - 1/2 >= 0 (4.5: the identity proved there holds at every configuration, and
that the option holds at x means that this number is >= 0 for every corner of t). So all factors are >= 0,
and so is the product. (Without (wx-cert-3) elements only kind (a) occurs, and the lemma is the sentence of
version 2.6: every product of facts is >= 0 on F(N), and a product containing `circ` is 0.)
CLAIM: g(x) >= L for all x in F(N).
Proof: let (x, z*) be the lifted point of x. g contains no indicator variable, so
g(x) = Rem(x, z*) + sum_k lambda_k * prod(...)(x, z*) >= Rem(x, z*) by the TERM LEMMA. Raw rule: the value of
every base variable at x lies in its SB (section 3) and every z* lies in [0, 1], its SB, by (L1); so every
monomial lies in its interval product (a product of numbers taken from intervals lies in the interval product,
also when one variable is taken several times), and Rem(x, z*) >= L. Centred rule: Rem(c + y) and Rem are the
same polynomial function under y = v - c; put y*_v := (value of v at (x, z*)) - c_v; then y*_v lies in
[SBlo(v) - c_v, SBhi(v) - c_v], every monomial m(y*) lies in its interval product, and
Rem(x, z*) = sum_m r_m m(y*) >= L.
A step with objective F and sense "lo" proves F >= L; with sense "hi" the objective is -F and the step proves
F <= -L. Each step carries a claimed `value` (section 10); it is ACCEPTED iff the claim is implied (lo:
value <= L; hi: value >= -L), and THE CERTIFIED VALUE OF AN ACCEPTED STEP IS ITS `value`. The objective `0` is the exception: it is allowed with the sense "lo" only, and such a step is accepted iff L >= value > 0; it then proves that F(N) is empty (0 = g(x) >= L > 0 holds for no x).
REJECTION: a step that is not accepted, a store entry that is not accepted, a declaration whose preconditions
fail, a term that violates one of the TERM RULES (T1) to (T4), or any violation of well-formedness
(section 10) rejects the whole certificate; nothing is repaired or skipped.

ROUND. All steps of a round are evaluated with the facts and store bounds of the store at the START of the
round. After the steps, the generator proposes a new store. The checker accepts an entry of the new store iff
it is implied as follows (v ranges over the certified values of this round's steps for the stated form):
- box end lo_ik: new <= old, or new <= some certified lower bound of `xi:i:k`. (hi: >=, upper bound.)
- S_lo: new <= old or new <= a certified lower bound of `S`; S_hi: new >= old or new >= a certified upper bound.
- arc endpoint P_i^- (a rotation relative to the unchanged centre rho_i): cos > 0 required; sin(new) <=
  sin(old) or sin(new) <= a certified lower bound of `s:i`. P_i^+: cos > 0; sin(new) >= sin(old) or >= a
  certified upper bound of `s:i`.
- stored relative-arc endpoint St^- of pair i<j: allowed only if, in the old store, D^- or a stored St^- has
  positive cosine (so R^- of 4.3 exists on this side and omega > -pi/2 is known; the plus side is not needed);
  cos(new) > 0 required; sin(new) <= sin(old R^-) or sin(new) <= a certified lower bound of `Sr:i:j`.
  St^+ symmetrically (old D^+ or St^+ with positive cosine; cos(new) > 0; sin(new) >= sin(old R^+) or
  >= a certified upper bound of `Sr:i:j`).
- cut "F >= v": v <= old cut value of the same name, or v <= a certified lower bound of F. Cut "F <= v":
  v >= old value or v >= a certified upper bound of F. A cut that is absent from the new store is dropped.
Every accepted entry is a true statement on F(N) (proofs: an arc endpoint: psi_i lies in (-pi/2, pi/2) on
F(N), and sin psi_i >= L >= sin(new) with cos(new) > 0 gives psi_i >= angle(new); a relative endpoint: 4.3;
otherwise trivial). Rounding outward and loosening are therefore free; nothing is ever used to prove itself.
A proposed store lists `S`, all box intervals and all arcs of the labels of I (32 intervals and 16 arcs with
sixteen labels, 34 and 17 with seventeen); `rarc` and `cuts` list what is kept.
(wx-cert-3) The `ind` declarations of a round, their indicator variables and the lifted point belong to that
round and to the store at its start. A proposed store has no entry that concerns an indicator variable, and no
rule above refers to one: an entry is accepted because of certified values of steps, and a certified value is
a statement about a named form on F(N) (CLAIM).
If a round contains an accepted `0` step, or the store after a round is EMPTY, the LATER rounds of the node are not evaluated. The round itself is evaluated completely: every declaration of it is tested, every step of it (also one that follows the accepted `0` step) must be accepted, and every entry of its proposed store must be accepted. Order in an evaluated round: (1) its start store (the node's data, or the store accepted in the round before) is not EMPTY; (2) every declaration is tested on that store; (3) every step is computed with the facts and store bounds of that same store; (4) every entry of the proposed store is accepted or not from the old store and the certified values of the steps of THIS round; (5) the new store is tested for EMPTY.

## 6. Assumptions and splits

ASSUMPTIONS of a node: a list of items of two kinds:
- option assumption (o, t, axis, eps): "option (o, t, axis, eps) holds";
- sign assumption (i, j, K, sign), i<j, K a class, sign in {+1,-1}: "sign * Y_K >= 0".
A node N with closure SPLIT has children; let St be N's final store. The checker verifies, for each type:
- box split of coordinate (i,k) at a rational m with lo <= m <= hi (St's interval): two children; child 1's
  interval for (i,k) contains [lo, m], child 2's contains [m, hi].
- arc split of square i at a rotation M (relative to N's centre) with cos M > 0 and
  sin P^- <= sin M <= sin P^+ (St's endpoints): two children; child 1's arc contains [P^-, M], child 2's
  contains [M, P^+].
- option split of the pair {i,j} with a nonempty list Lst of options of that pair: one child per listed
  option, in order; the options of Lst need not be pairwise different (a repeated option has one child per occurrence), and Lst may contain excluded options; every option of the pair NOT in Lst is excluded (4.7) on St. Child l has the additional
  option assumption Lst[l].
- sign split (i, j, K): two children with the additional assumptions (i,j,K,+1) and (i,j,K,-1).
"Child 1", "child 2", "child l" refer to the order of the ids in the split's `children` list.
In every case: every child's `assume` list equals N's list, in the same order, followed by the one additional
assumption as its last item (no additional item for box and arc splits); every interval of a child's box other than a split interval contains St's interval; every arc of
a child other than a split arc contains St's arc; the child's side interval contains St's side interval.
A child takes nothing else from N (no cuts, no relative-arc endpoints): its F is defined by its own data.
ARC CONTAINMENT TEST (also used with a changed centre). To test that the arc of square i of a node with centre
rho' and endpoints P'^-, P'^+ contains the arc [A^-, A^+] given relative to a centre rho: let
delta := rho * conj(rho'), At^- := A^- * delta, At^+ := A^+ * delta. Required: cos At^- > 0, cos At^+ > 0,
sin P'^- <= sin At^-, sin At^+ <= sin P'^+.
Covering proof: take x in F(N); it satisfies every statement of St. Box split: xi_ik in [lo,m] or [m,hi].
Arc split: with mu := angle(M) in (-pi/2, pi/2), psi_i <= mu or psi_i >= mu. Option split: by the SAT lemma
some option of the pair holds at x; the unlisted ones hold nowhere on F(N). Sign split: Y_K >= 0 or <= 0.
In each case x satisfies the corresponding child's data and assumptions, so x is in F(child). (Arc test: if
both re-expressed endpoints have positive cosine, the re-expressed arc is the same set of directions and lies
in (-pi/2, pi/2) of the child's frame, where containment is comparison of sines.)

## 7. Closing nodes; the tree; the root

A node is CLOSED if
(a) INFEASIBLE: some evaluated round contains an accepted `0` step (objective `0`, sense "lo", L >= value > 0); or the store after some round is
    empty in the sense of section 2 (then no further round is evaluated); or, for some pair {i,j} named in the
    closure, all 8 options of the pair are excluded (4.7) on the node's final store (then F(N) is empty by the
    SAT lemma); or
(b) TERMINAL: its final store passes the terminal test of section 8; or
(c) SPLIT (section 6) and all its children are closed.
TREE CONDITIONS (checked on the whole certificate): node ids are unique; a node id is a non-empty JSON string, and ids are compared as strings, character for character; the root is the node named in the
header; every id in a `children` list exists and that node's `parent` is the splitting node; every node other
than the root occurs in exactly one `children` list, exactly once; every node is reachable from the root; the number of children is 2 for box, arc
and sign splits and the number of listed options (>= 1) for an option split; every node is closed by (a), (b)
or (c).
ROOT CONDITIONS: the root has `parent` = null and an EMPTY assumption list; S_lo <= S_floor (= 4 without the
header field) and S_hi >= Sref (the
header's Sref must equal the `side` of the packing file whose SHA-256 is in the header); its data contain the
window (section 8).
THEOREM. If all conditions hold, every feasible configuration with S_floor <= S <= Sref in the window lies in
the tube.
Proof: such a configuration has S_lo <= S_floor <= S <= Sref <= S_hi, so it lies in F(root) (for S_floor = 4
the lower condition is automatic: at least 16 unit squares with disjoint interiors in [0,S]^2 have S >= 4); by induction over the finite tree, every configuration of F(N), N closed, lies in the tube:
(a) F(N) is empty; (b) the final store holds on F(N) and implies the tube; (c) covering (section 6).

## 8. Window and tube as rational data

A WINDOW or TUBE is given by: a box (rational interval for every xi_ik, i in I, k in {1,2}), a rational angle
radius alpha_i > 0 for every i in I, and, (wx-cert-3), optionally a CENTRE rotation gamma_i for every i in I (a
rotation in the sense of section 1: a rational pair (g, s) with g^2 + s^2 = 1). If no centres are given, and
always under the schema "wx-cert-2", gamma_i is the identity (1, 0) for every i. A configuration lies in it iff
every xi_ik is in its interval and every a_i = R(phi_i) gamma_i u_i with |phi_i| <= alpha_i, where gamma_i u_i
denotes the rotation gamma_i applied to the reference direction u_i. (No slider notation here: sliders are just
coordinates xi_{2,1}, xi_{11,2}, xi_{13,2} with their own intervals; remember a = -xi_{2,1}, b = -xi_{11,2}.
A configuration comes with one side direction a_i per square; the application chooses which of the four side
directions of a square it is, section 11 item (3).)
ROOT CONTAINS WINDOW: the root box contains the window box coordinate-wise; for every i, with the endpoints
relative to the window's centre  Ab^± := conj(gamma_i) * rho_i * P_i^±  (gamma_i the window's centre for i,
rho_i and P_i^± the root's centre and endpoints; with the identity as centre this is rho_i * P_i^±, the
absolute endpoint of version 2.6): cos Ab^- > 0, cos Ab^+ > 0, sin Ab^+ >= alpha_i, sin Ab^- <= -alpha_i.
Requires alpha_i < 1.
Proof that the root arc then contains the window arc. Let theta0 := angle(conj(gamma_i) * rho_i) and
psi^± := angle(P_i^±), both psi^± in (-pi/2, pi/2), psi^- <= psi^+ (section 2). The root arc is
{R(psi) rho_i u_i : psi^- <= psi <= psi^+} = {R(theta0 + psi) gamma_i u_i : psi^- <= psi <= psi^+}, an arc of
length psi^+ - psi^- < pi. The real numbers e^± := theta0 + psi^± are angles of Ab^±. Both cosines are
positive, so e^- lies in (-pi/2, pi/2) + 2 pi k and e^+ in (-pi/2, pi/2) + 2 pi m for integers k, m; since
0 <= e^+ - e^- < pi, k = m. Subtracting 2 pi k, the root arc is {R(e) gamma_i u_i : e^- <= e <= e^+} with
e^± = angle(Ab^±) in (-pi/2, pi/2). There e^+ = asin(sin Ab^+) >= sin Ab^+ >= alpha_i (asin x >= x for
0 <= x < 1) and e^- <= -alpha_i likewise. So [-alpha_i, alpha_i] is contained in [e^-, e^+].
TERMINAL TEST for a final store and a tube: the store box is contained in the tube box coordinate-wise; for
every i the endpoints relative to the tube's centre  Ab^± := conj(gammaT_i) * rho_i * P_i^±  (gammaT_i the
tube's centre for i, rho_i the node's centre, P_i^± the store endpoints) satisfy cos Ab^± > 0 and
|sin Ab^±| <= alphaT_i - alphaT_i^3/6. Requires alphaT_i <= 1.
Proof. As above the store arc is {R(e) gammaT_i u_i : e^- <= e <= e^+} with e^± = angle(Ab^±) in
(-pi/2, pi/2). From |sin e^±| <= alphaT_i - alphaT_i^3/6 <= sin(alphaT_i) (sin x >= x - x^3/6 for
0 <= x <= pi/2, and alphaT_i <= 1 < pi/2) and the monotonicity of sin on (-pi/2, pi/2): |e^±| <= alphaT_i.
So every direction of the store arc is R(phi) gammaT_i u_i with |phi| <= alphaT_i.
(The ARC CONTAINMENT TEST of section 6, child arcs against the parent's store, is untouched by centres of the
window or the tube. A square with FREE direction needs no rule of its own: a window radius just above pi/4,
for example 393/500, with any centre covers one of the four side directions of every square, and a tube radius of 1 lets a node pass the
terminal test for that label with an arc of up to asin(5/6) on either side.)

## 9. What the generator is free to choose (never affects soundness)

Which pairs to declare, which facts to use, tangent vectors, objectives, multipliers and their rounding, the
number of rounds, store entries looser than what was certified, split types and split points, centres of
children; (wx-cert-3) polynomial forms, the centre of every step, which pairs get an `ind` declaration, which excluded
options are listed besides the ones that must be, and the order of the list. The checker rebuilds every fact from the node data, the store and this SPEC and recomputes every
step exactly.

## 10. Certificate format (schemas wx-cert-2 and wx-cert-3)

All numbers are strings "p" or "p/q" (q > 0). Labels are integers. A rotation is [g, s] with g^2 + s^2 = 1
(checked for every rotation in the file). The certificate is a file of JSON lines in UTF-8 without byte order mark: the header object on the first line, then one node object per line, in any order, at least one node. Every line holds exactly one JSON object, with or without JSON whitespace around it (a carriage return before the line feed is such whitespace); an empty line is rejected, also after the last node; the last line may end with or without a line feed. A checker may read the same lines from a gzip-compressed file.

WELL-FORMEDNESS. The checker rejects the certificate if any of the following fails; nothing is repaired or
skipped.
- `schema` equals "wx-cert-2" or "wx-cert-3" (SCHEMA RULE below); the checker computes the SHA-256 of the packing file it reads and requires the JSON string `packing_sha256` to be its 64 lowercase hexadecimal digits, character for character; `Sref` is a number string whose VALUE equals the value of the file's `side` (not necessarily the same string).
- SCHEMA RULE. Under the schema "wx-cert-2" the certificate is checked by the rules of version 2.6: none of the
  elements marked (wx-cert-3) in this document exists, and each of them rejects the certificate where it
  occurs: a `centre` in the header's `window` or `terminal` and a `centre` in a step (keys that are not
  defined, see KEYS), a key of `forms` that begins with `q:` (not a custom form NAME), a declaration with the
  mode "ind" (not a mode), and a name that begins with `sq:`, `pol:` or `ind:` (not a fact name). Under the
  schema "wx-cert-3" all rules of this document apply. A certificate that uses none of these elements is
  checked in the same way under either string. (So a certificate that uses one of them MUST have the schema
  "wx-cert-3"; and a checker for version 2.6 rejects every certificate with that schema at its header.)
- KEYS. Every JSON object of a certificate has exactly the keys that the format blocks and items of this
  section give for it, optional ones possibly absent: the header, its `window` and its `terminal`, a node, an
  entry of a node's `arc`, an assumption, a round, a declaration, a step, a `store`, an entry of its `arc` and
  of its `rarc`, a split object, a `close` object, an option. A key that is not defined for the object rejects
  the certificate. (The maps keyed by labels, `forms`, `rarc`, `cuts` and the `centre` of a step have the keys
  described for them.) A term is a list of exactly two elements, a number and a list of names. The optional keys are: `labels`, `S_floor` (header); `centre` (window, terminal, step; wx-cert-3); `forms` (node); `kappa` (P+ or P- declaration); `pair` (closure "infeasible"). Every other key of the format blocks is required.
- Optional header field `labels`: the JSON integer 16 or 17 (anything else is rejected); absent means 16. It
  fixes I for the whole certificate. Optional header field `S_floor`: a number string with
  4 <= S_floor <= Sref (anything else is rejected); absent means 4. ("JSON integer" means exactly the number
  token 16 or 17: 17.0, 1.7e1 and "17" are rejected. `S_floor` is any string of the number format of the next
  item, compared by value.) The header has no other optional field.
- (wx-cert-3) Optional field `centre` in the header's `window` object and, independently, in its `terminal`
  object: a map keyed by labels with exactly the keys of I; every value is a rotation [g, s] (g^2 + s^2 = 1,
  checked). Absent means the identity for every label. Neither object has another optional field.
- Header ranges, tested when the header is read, also if the tree has no terminal node: every interval of the `box` of `window` and of `terminal` has lo <= hi; every `alpha` of `window` satisfies 0 < alpha < 1; every `alpha` of `terminal` satisfies 0 < alpha <= 1.
- Numbers are JSON strings matching `-?[0-9]+` or `-?[0-9]+/[0-9]+` with a nonzero denominator (no floats).
- Labels are integers of I (section 0: {1,...,17} minus {4}, or {1,...,17} if the header says `labels` = 17)
  (JSON integers in fields; their decimal strings, without sign and without leading zeros, as map keys and inside names). A JSON integer is a number token without fraction and without exponent: `5.0`, `5e0`, `"5"` and `true` are rejected wherever the format asks for a JSON integer (a label in a field, `k`, `eps`, `sign`, `labels`).
  Every map keyed by labels (`box`, `arc`, `alpha` in the header's `window` and `terminal`, `box` and `arc` in
  every node and in every round's `store`) has exactly the keys of I (16 or 17 of them). With sixteen labels
  the label 4 is rejected wherever a label can occur (maps, fields, fact names, form names), as before.
- `k` in {1,2}; `axis` in {"a","b"}; `eps` and `sign` in {1,-1} (JSON integers; in names they are written p, m);
  `cls` matches `[ab][+-][ab][+-]`; `kind` in {"P+","P-","Pk","Ps"}; `mode` in {"opt","par"} or, (wx-cert-3), "ind"; the index k of a name
  `ind:i:j:k` is one digit 1 to 8; `sense` in
  {"lo","hi"}; corner letters in {p,m}; wall coordinate in {x,y}; wall name of a `wsup` fact in {xlo,ylo,xhi,yhi}.
- Wherever i, j name a pair (declarations, `ysign` assumptions and splits, `rarc` keys "i-j", `pair` of an
  option split or of an infeasible closure, names containing `i:j`): i < j, both in I. Wherever o, t occur
  (options, names containing `o:t`): o != t, both in I. In an `opt` declaration {o,t} = {i,j}. Every option
  listed in an option split of the pair [i,j] has {o,t} = {i,j}.
- Every fact name and form name parses by the lists below (integers without sign or leading zeros); unknown
  names are rejected; a custom form name `u:NAME` must be defined in the node's `forms`. (Availability is the term rule (T4) of section 5; it is not well-formedness: see WHERE EACH TEST IS MADE.) (wx-cert-3) A name `sq:NAME` or `pol:NAME` in any step of the node
  needs the key `q:NAME` in the node's `forms`.
- Node data: lo <= hi for every box interval, S_lo <= S_hi, cos P^± > 0, sin P^- <= sin P^+, every rotation
  unit; multipliers lambda >= 0 except in terms containing a `circ` fact; every term has 1 to 3 names (fact
  names and, (wx-cert-3), `pol`, `ind` and guarded corner names); (wx-cert-3) a `pol` name only in a term
  that contains a `circ` fact.
- At most one `par` declaration per (i, j, cls, kind) in a round (so that a fact name denotes one polynomial).
- `forms`: NAME matches `[A-Za-z0-9_]+`; every component is a form name of section 3 other than `0` and
  `u:...` and obeys the label and pair rules above; coefficients are numbers; the list of components is nonempty; a coefficient may be 0; the component names of one custom
  form are pairwise different. `forms` belongs to the node's data: it is the same for all rounds of the node
  and is not inherited by children.
- (wx-cert-3) `forms` may also have keys `q:NAME`, NAME matching `[A-Za-z0-9_]+`: polynomial forms
  (section 3). The value is a nonempty list of entries; an entry is a list of exactly two elements, a number
  and a list of 0, 1 or 2 base variable names (`xi:i:k`, `S`, `C:i`, `s:i`, obeying the label rules); the
  monomials of the entries of one form are pairwise different as multisets of variables. A key of `forms` that
  does not begin with `q:` is the NAME of a custom form as before; a key that begins with `q:` and is not of
  the form above is rejected.
- (wx-cert-3) An `ind` declaration has exactly the keys `i`, `j`, `mode`, `options`; `options` is a list of
  1 to 8 options {"o":..,"t":..,"axis":..,"eps":..}, pairwise different, every one with {o,t} = {i,j}. A round
  has at most one `ind` declaration per pair (i, j), and no `opt` declaration of a pair that has an `ind`
  declaration in that round; a pair {i,j} for which the node's `assume` list contains an option assumption (an
  item of kind "opt" with {o,t} = {i,j}) has no `ind` declaration in any round of the node (4.10, R1 to R3).
- (wx-cert-3) A step may have the optional key `centre`: a JSON object whose keys are names of base variables
  (`xi:i:k`, `S`, `C:i`, `s:i`; labels of I; written like the form names) and whose values are numbers. Every
  other key of that object is rejected (in particular the name of any other form; an indicator variable has
  no name).
- A JSON object with a repeated key is rejected. Keys are compared after decoding JSON escapes (a key spelled with an escape, for example `labels` with its second letter written as a backslash followed by `u0061`, is the key `labels`); every string of a certificate (a name, a number string, an id, `schema`, `packing_sha256`) is used after decoding.
- WHERE EACH TEST IS MADE. A round of a node is EVALUATED iff no earlier round of the node contains an
  accepted `0` step and the store after every earlier round is not EMPTY (the first round always is). An
  evaluated round is evaluated COMPLETELY: all its declarations, all its steps (also those that follow an
  accepted `0` step) and its proposed store.
  (W) WHOLE FILE. Every item of this list WELL-FORMEDNESS, the shape that the format blocks below give to every object, and every condition that the lists of names below attach to a name, is tested for every node and every round, evaluated or not: KEYS; numbers, labels and pairs; node
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
  4.10); the availability (T4) of every name of every term, whatever its multiplier, as far as it is not a condition of (W) that is part of the name (a `cut` name has its
  cut in the store at the start of the round; an `opt` name has an `opt` declaration of its option in the round or, (wx-cert-3), its option
  stands in the list of an `ind` declaration of the round; a `par` name has its `par` declaration in the round; an
  `asg` name has its sign assumption in the node's `assume` list; a `wsup` name passes the sign conditions
  of 4.8; a `rarc` name has an effective relative arc; (wx-cert-3) an `ind:i:j:k` has an `ind` declaration
  of its pair in the round and k <= m); (wx-cert-3) the guard rule (T3); the acceptance of every step (also
  value > 0 of a `0` step); the acceptance of every entry of the proposed store (also cos > 0 of a proposed
  endpoint: the proposed store of a round that is not evaluated need only have the format).
  The final store of a node is the store after its last evaluated round (the node's data if it has no round).
  For the closure of a node (section 7) only its evaluated rounds count: an accepted `0` step or an EMPTY store must stand in an evaluated round, and every other closure test reads the final store.

Header:
```
{"schema":"wx-cert-2"|"wx-cert-3", "packing_sha256":"...", "Sref":"4675530093604551/1000000000000000", "root":"<id>",
 "labels":17,                 optional (16 or 17; absent = 16)
 "S_floor":"p/q",             optional (4 <= S_floor <= Sref; absent = 4)
 "window":   {"box":{"<label>":[[lo1,hi1],[lo2,hi2]],...all labels of I}, "alpha":{"<label>":"p/q",...},
              "centre":{"<label>":[g,s],...all labels of I}},      centre: optional, (wx-cert-3)
 "terminal": {"box":{...}, "alpha":{...}, "centre":{...}}}          centre: optional, (wx-cert-3)
```
Node:
```
{"id":"...", "parent":null|"...",
 "S":[S_lo,S_hi],
 "box":{"<label>":[[lo1,hi1],[lo2,hi2]],...},
 "arc":{"<label>":{"c":[g,s],"lo":[g,s],"hi":[g,s]},...},          centre; endpoints relative to the centre
 "assume":[ {"kind":"opt","o":o,"t":t,"axis":"a"|"b","eps":1|-1},
            {"kind":"ysign","i":i,"j":j,"cls":"a+b-","sign":1|-1} ],
 "forms":{"NAME":[["coef","FORMNAME"],...],                         optional: custom forms u:NAME (section 3)
          "q:NAME":[["coef",["VARNAME",...]],...], ...},            (wx-cert-3) polynomial forms q:NAME
 "rounds":[ROUND,...],
 "close":{"kind":"infeasible"} | {"kind":"infeasible","pair":[i,j]} | {"kind":"terminal"}
        | {"kind":"split","how":SPLIT,"children":[ids]}}
```
ROUND:
```
{"pairs":[ {"i":i,"j":j,"mode":"opt","o":o,"t":t,"axis":..,"eps":..},
           {"i":i,"j":j,"mode":"par","cls":"a+a+","kind":"P+"|"P-"|"Pk"|"Ps","kappa":"p/q"},
           {"i":i,"j":j,"mode":"ind","options":[{"o":o,"t":t,"axis":..,"eps":..},...]}, ... ],      (wx-cert-3)
 "steps":[ {"form":NAME,"sense":"lo"|"hi","value":"p/q","terms":[["lambda",[NAME,...]],...],
            "centre":{"VARNAME":"p/q",...}}, ... ],                 centre: optional, (wx-cert-3)
 "store":{"S":[lo,hi], "box":{...}, "arc":{"<label>":{"lo":[g,s],"hi":[g,s]},...},
          "rarc":{"i-j":{"lo":[g,s]|null,"hi":[g,s]|null},...}, "cuts":{"NAME:lo":"v","NAME:hi":"v",...}}}
```
- `pairs`: declarations for this round. An `opt` declaration makes the four `opt:` facts of that option
  available iff the node assumes the option or the 7 others are excluded on the store at the start of the
  round. A `par` declaration makes the two `par:i:j:K:kind:1|2` facts available iff the preconditions of 4.6
  hold (`kappa` is required for Pk and Ps; in a P+ or P- declaration it may be absent, and if it is present it must be a number string of the format of this section, whose value is ignored). Several `opt` and `par` declarations per pair are allowed in a round, and an `opt` declaration may be repeated; for `par`: at most one per (i, j, cls, kind);
  undeclared pairs carry no `opt`/`par` facts. `asg:i:j:K:p|m` needs no declaration (it needs the matching sign
  assumption).
- (wx-cert-3) An `ind` declaration makes the names `ind:i:j:k` (k = 1..m, m the length of its list) and the
  corner names `opt:...` of its listed options available, under the TERM RULES of section 5, iff its
  precondition of 4.10 holds on the store at the start of the round; if the precondition fails, the
  certificate is rejected. The k-th option of the list is O_k; the indicator of the LAST option is 1 minus the
  indicator variables of the others.
- step, sense "lo": claims form >= value; accepted iff value <= L (g = form). Sense "hi": claims
  form <= value; accepted iff -value <= L computed with g = -form. A step on the form `0` must have the sense "lo": a step with `form` = `0` and `sense` = "hi" is malformed and rejects the certificate wherever it stands, also in a round that is not evaluated. A step on the form `0` is accepted iff L >= value > 0 (the rule "value <= L" does not apply to it; a `0` step with value <= 0 is not accepted). An accepted `0` step is evidence for the closure "infeasible"; it gives no certified value for a store entry.
- (wx-cert-3) `centre`: with the field the step's L is computed by the CENTRED RULE of section 5, without it
  by the RAW RULE. A base variable that is not a key has the centre 0.
- `store`: A key of `cuts` is `NAME:lo` or `NAME:hi`, NAME a form NAME of the list below other than `0` (there is no cut for the form `0`); a custom form `u:NAME` must be defined in the node's `forms`. The store after the round, accepted entry by entry by the rules of section 5 (the `arc` entries
  have no centre: centres never change). If the new store is empty in the sense of section 2, the node is
  infeasible and must have close kind "infeasible".
- A node with close kind "infeasible" must contain evidence. The form `{"kind":"infeasible"}` is accepted iff
  some evaluated round contains an accepted `0` step or the store after some evaluated round is EMPTY. The form
  `{"kind":"infeasible","pair":[i,j]}` is accepted iff the node's final store is NOT EMPTY and all 8 options of
  the named pair are excluded (4.7) on it (other evidence in the node does not replace this test). A node with
  close kind "terminal" or "split" is checked as such even if it also contains an infeasibility step (a node
  that is empty is correctly closed either way), but its store must never be empty when facts are built.
FACT names: `box:i:k:lo|hi`; `side:lo|hi`; `wall:i:E1:E2:k:lo|hi` (E1, E2 in {p,m} for +1, -1; k in {x,y});
`arc:i:slo|shi|clo|chi|chord`; `arc:i:tan:G:H` (G, H number strings with G^2 + H^2 <= 1; the inequality is part of the name: a `tan` name that violates it is malformed wherever it stands); `wsup:i:W:p|m` (W in
{xlo,ylo,xhi,yhi}; available without declaration iff the sign conditions of 4.8 hold on the store at the
start of the round); `rarc:i:j:slo|shi|clo|chi|chord`;
`rarc:i:j:tan:G:H` (G, H as for `arc`); `opt:o:t:axis:EPS:E1:E2` (EPS in {p,m}; E1,E2 the corner of t); `par:i:j:K:kind:1|2`;
`asg:i:j:K:p|m`; `ivl:FORM:lo|hi` for FORM = `Da:o:t`, `Db:o:t` or an affine custom form `u:NAME`;
`cut:FORM:lo|hi` for any form name except `0`; `circ:i`.
(wx-cert-3) `sq:NAME`; `pol:NAME` (not a fact: only in a term containing a `circ` fact); in `sq:NAME` and in `pol:NAME`, NAME matches [A-Za-z0-9_]+ and is the NAME of a key `q:NAME` of the node's `forms`; `ind:i:j:k` (i < j,
both in I; k one digit 1 to 8).
Form NAMEs: `xi:i:k`, `S`, `C:i`, `s:i`, `Da:o:t`, `Db:o:t`, `A:o:t`, `B:o:t`, `Cr:i:j`, `Sr:i:j`,
`al:i:j:K`, `be:i:j:K`, `co:i:j:K`, `si:i:j:K`, `Y:i:j:K`, `u:NAME`, `0`.
(wx-cert-3) VARIABLE names, only as keys of the `centre` of a step: `xi:i:k`, `S`, `C:i`, `s:i`. The list of
form NAMEs is the same under both schemas: `q:NAME` is not a form NAME, and an indicator variable has no name.
SPLIT: `{"type":"box","sq":i,"k":k,"at":"m"}`; `{"type":"arc","sq":i,"at":[g,s]}`;
`{"type":"opt","pair":[i,j],"options":[{"o":..,"t":..,"axis":..,"eps":..},...]}`;
`{"type":"ysign","i":i,"j":j,"cls":"...."}` (children: sign +1 first, then -1).
A node object can be checked alone (result: accepted, with its final store); the tree pass checks the tree,
root, child-containment and terminal conditions of sections 6 to 8.

## 11. What the application must add to (ANN)

If the header has `S_floor` > 4, (ANN) is stated for S_floor <= S <= Sref only. This never weakens it: a
configuration that is feasible for a side S <= Sref is feasible for the side Sref (condition (F1) only gets
weaker, (F2) does not mention S), and neither the window nor the tube nor the reference data mention S. Hence
(ANN) for S_floor <= S <= Sref implies (ANN) for every S <= Sref, and the application needs no lower bound on S
for it. (This argument would fail if a later version let a window or a tube depend on S.) A generator may
always write the root's side interval as [Sref, Sref]. With `labels` = 17 a tube must contain a factor for
label 4 like for every other label. Where the square at list position 4 is a rattler: the tube box of label 4
contains its window box, and its tube radius is large enough for the terminal test of section 8 to pass on a
leaf whose arc contains the window arc; the tube radius cannot equal the window radius, because the root test
needs sin(arc end) >= alpha and the terminal test |sin(arc end)| <= alphaT - alphaT^3/6 (example: tube radius
1/5 for a window radius 1/10). A square with FREE direction is expressed by a window radius just above pi/4
(393/500 works) and a tube radius of 1; a theorem that uses this must state pi/4 < 393/500 and that the
quarter-turn representative of smallest absolute value is meant.
(ANN) says nothing about S*. To conclude "every packing of 17 unit squares in [0,S]^2 with S <= S* whose 16
constrained squares lie in W has S = S* and lies on the three-slider family" one needs, outside this SPEC:
(1) S* <= Sref (proved by Codex's `bridge.py`: `side_star.hi <= side`).
(1b) side_star.hi < p_2x + 1/2. This is stronger than (1): p_2x + 1/2 = Sref - 5.17e-18 exactly (the file
    leaves 5.17e-18 at each wall). It is true with room (S* is about 4.32e-17 below p_2x + 1/2) and must be
    checked exactly, against the certified enclosure of S*, where the two results are combined.
(2) A terminal theorem for the tube T: "feasible, S <= S*, in T implies S = S* and core = 0". The instance
    intended here is `terminal/instances/box-relaxed/` of this folder (Codex's terminal proof re-instantiated;
    its README and SHA256SUMS identify it): hypotheses S <= S*; the 29 core position coordinates within 1/100;
    the 16 angle increments within 1/200 rad; a = -xi_{2,1} in [0, 1/4], b = -xi_{11,2} in [-1/20, 3/20],
    z = xi_{13,2} in [-1/8, 3/40]. It has no separate floor on S (its side floor S >= Sref - 1/50 is derived
    inside the proof from the position of square 8 at tube radius 1/100). The lower end a >= 0 need not be
    proved by the tree: for a feasible configuration with S <= S* it follows from the right wall
    (x_2 <= S - 1/2 <= S* - 1/2 < p_2x, the last step being (1b)). So the tube T of
    the tree may allow xi_{2,1} up to a small positive number; all other tube bounds must lie inside the
    hypotheses above. The final theorem document must pin the instance by hash and quote these hypotheses.
(3) The frame (container corner at the origin), the labelling (file order) and the choice of the quarter-turn
    representative of each direction are hypotheses of the combined theorem.
(4) (wx-cert-3) If the window or the tube has centres (section 8), the combined theorem must state the window
    and the tube with their centres. Where the tube is the window of an earlier theorem whose arcs are centred
    at the reference directions, the tube's centres are the identity and nothing changes in the composition.
(5) (ANN) is a statement relative to the reference file whose SHA-256 is in the header (`packing_sha256`). A
    checker may in addition require one particular reference file (the checkers written so far require, unless
    an option lifts it, the file with SHA-256
    24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7). The final theorem must quote the hash.

## 12. Advice for generators (not normative)

Linear programs over lifted variables: use the monomials of the facts and their products as LP columns
(or product variables per (owner,target) form); rows = facts and products of facts; keep the provenance of
every row (which facts were multiplied) so that the LP dual becomes the term list of a step. Leave lifted
columns free and put bounds only on base variables. Round multipliers to rationals with small denominators;
the exact check absorbs the rounding in Rem. Useful products: bound fact of C_o or s_o times `ivl`/`cut` fact of
Da_ot, Db_ot (McCormick); bound facts of two trig variables; `opt`/`par` fact times a bound fact of some s_j
(stress that varies affinely with an angle).

Semidefinite leaves (wx-cert-3). A sum-of-squares certificate from a floating-point solver needs no exact
identity: write every Gram matrix as a sum of non-negative multiples of squares of polynomial forms (terms
`[d, ["sq:v"]]`, `[d, ["sq:v", FACT]]`), the multipliers of the equalities C_i^2 + s_i^2 = 1 as terms
`["1", ["circ:i", "pol:p"]]`, round everything to rationals, and let the remainder bound absorb what does not
cancel. Give the step a `centre` (the mid point of the store interval of every base variable): in the raw
variables the residual monomials are multiplied by powers of S and cost far more than the margin (on a small example of the audit `reviews/REVIEW_30.md`, files `reviews/r30/d/T_T1*`, the raw rule gives L = -0.080 and the centred rule L = 0.99994 for the same terms). Leave an
undecided pair to indicators (4.10) instead of splitting on it where the relaxation stays sharp; list its
options in an order that puts the most likely one last (it is the one without a variable). State such trees
with `S_floor` = Sref and every side interval [Sref, Sref] (section 11, first paragraph), so that an
infeasible leaf is one step on the form `0`. A leaf that contains the known family gets no bound steps: a
chain of box splits at the tube's ends, each with one infeasible child, ends in a node whose box lies in the
tube and which is terminal without a step.
