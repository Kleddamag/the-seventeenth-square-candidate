# SPEC: branch-and-contract proof engine for the window extension ("WX engine")

Author: window analysis, 2026-10-08. **Version 2.5.1** (12:35; 2.5.1 only makes explicit which evidence each of the two forms of the closure "infeasible" needs, section 10; the cross-test of the two checkers had shown two readings, both sound). Version 2.5 (12:15; 2.5 = 2.4 with the three points H1-H3 of the fourth audit, `reviews/SPEC_AUDIT_4.md`, which found both new lemmas correct: the vectors of 4.8 renamed V^± with a warning, "else 1" in kind Ps, wording). Version 2.4 (12:00) = 2.3 plus two fact families that are exact at an axis direction: wall support facts `wsup` (new section 4.8) and the kind "Ps" of a parallel class (end of section 4.6), with their names in section 10; nothing else changed; the previous version is kept as `SPEC_v2.3.md`). Version 2.3 (10:55; 2.3 = 2.2 plus the five minor points D1-D5 of the third audit, `reviews/SPEC_AUDIT_3.md`, which found nothing a literal checker would accept wrongly). 2.1 added the closure "all 8 options of a pair excluded"; 2.2 incorporates the second audit (`reviews/SPEC_AUDIT_2.md`: one fatal contract hole E4, one critical ambiguity U7, minor points M1-M9, all fixed here) and adds custom linear forms (section 3). Version 1 was audited by an
independent referee (`reviews/SPEC_AUDIT_1.md`: no false mathematical statement; three contract errors E1-E3,
six critical ambiguities U1-U6, four proof gaps G1-G4). Version 2 incorporates every required change of that
audit; the mathematics of the lemmas is unchanged.

This file is the contract between the certificate GENERATOR and the independent CHECKER. Sections 0 to 10 are
normative for the checker. Section 11 says what the application must add. Section 12 is advice for generators.
All numbers in certificates are exact rationals. The only analytic inequality used anywhere is
x - x^3/6 <= sin x <= x for 0 <= x <= pi/2 (section 8); everything else is polynomial algebra, the monotonicity
and concavity of sin and cos on quarter circles, and the separating-axis lemma.

## 0. What is proved

Squares: the 16 "constrained" squares, labels I = {1,...,17} minus {4}, labels = order (1-based) of the
`squares` list of `upper-packing-certificate.json`. Square 4 (the rattler, file centre about (3.1755, 0.5)) is
never used: the 16 constrained squares of a packing of 17 squares form a feasible configuration in the sense
below, so every statement proved for all feasible configurations holds for them.

A CONFIGURATION is a side S > 0 and, for each i in I, a centre q_i in R^2 and a unit vector a_i (the direction
of one side of square i). Put b_i := J a_i, J(x,y) := (-y,x). Square i is {q_i + x a_i + y b_i : |x|,|y| <= 1/2};
its corners are q_i + (e1 a_i + e2 b_i)/2, e1,e2 in {+1,-1}.
FEASIBLE means: (F1) every corner of every square lies in [0,S]^2 (the container has a corner at the origin);
(F2) any two squares of I have disjoint interiors.
A PAIR is a set {i, j} of two DIFFERENT labels of I. Every ordered pair (o,t), option (o, t, axis, eps), class
of a pair, relative arc and pair closure in this SPEC presupposes two different labels of I.

The engine proves statements of the form

    (ANN)  every feasible configuration with S <= Sref that lies in the window W lies in the tube T,

Sref := 4675530093604551/10^15 (the `side` of the packing file). W and T are given by rational data (section 8).
(ANN) is a statement for one frame and one labelling.

## 1. Reference data and coordinates

From the packing file: for each i the rational centre p_i^file and the rational parameter t_i; the reference
direction u_i := ((1-t_i^2)/(1+t_i^2), 2 t_i/(1+t_i^2)), v_i := J u_i.
Reference centres: p_i := p_i^file for i != 13, and p_13 := p_13^file - (T0/3) v_13 with
T0 := u_9x * (u_9x + 4 - Sref)   (u_9x = first coordinate of u_9).
Frames: (e_i1, e_i2) := (u_i, v_i) for i in {11, 13}; (e_i1, e_i2) := ((1,0),(0,1)) for all other i.
Position coordinates of a configuration: xi_ik := e_ik . (q_i - p_i), so q_i = p_i + xi_i1 e_i1 + xi_i2 e_i2.

(For the reader, not used by the checker: in the notation of the Codex local theorem the three "sliders" are
a = -xi_{2,1}, b = -xi_{11,2}, z = xi_{13,2}; the other 29 position coordinates are its "core" coordinates.)

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

BASE VARIABLES: xi_ik (32), S, C_i, s_i (32). A POLYNOMIAL is an element of Q[base variables]; on a
configuration of F(N) it is evaluated with the true values of xi, S, C_i = cos psi_i, s_i = sin psi_i.

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
- custom forms `u:NAME` (NAME matching [A-Za-z0-9_]+), defined in the node's `forms` field (section 10) as a
  rational linear combination sum_m coef_m * F_m of named forms F_m of the kinds listed above (not `0`, not
  another custom form). A custom form is AFFINE if all its F_m are among `xi:i:k`, `Da:o:t`, `Db:o:t`.
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
The EMPTY test (section 2) is made on the store at the start of every evaluated round and on the final store.
Besides the box, the side interval, the arcs and the cut pairs it covers: every pair that has a stored
relative-arc endpoint and effective endpoints on both sides (sin R^- > sin R^+), and every form that has a cut
in the store, base variables excepted (empty intersection in its SB). (A form without a cut cannot have an
empty SB unless one of its components with a cut has one.)

## 4. Facts

A FACT of N (for a given store) is a named polynomial f with f(x) >= 0 for every x in F(N). Facts are rebuilt
by the checker from the store at the start of each round. Complete list:

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
- `arc:i:tan:G:H` := 1 - G C_i - H s_i for any rationals G, H with G^2 + H^2 <= 1 (checked).
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

## 5. Inference: steps, rounds, store updates

STEP. Given the store at the start of a round and its facts: an objective polynomial g (a named form, or its
negative), and a list of TERMS (lambda_k, [fact names]), each with 1 to 3 fact names. lambda_k must be >= 0,
except that a term whose fact list contains a `circ` fact may have a multiplier of either sign. The checker
computes exactly
    Rem(x) := g(x) - sum_k lambda_k * prod(facts of term k)
and the monomial-wise interval lower bound L of Rem: for Rem = sum_m r_m m(x) (m ranging over monomials,
including the constant monomial 1 with interval [1,1]), L := sum_m min(r_m * lo_m, r_m * hi_m), where
[lo_m, hi_m] is the product, by interval multiplication, of the store-bound intervals SB of the base variables
of m, a variable of exponent e being multiplied e times.
CLAIM: g(x) >= L for all x in F(N).
Proof: every product of facts is >= 0 on F(N) (a product containing `circ` is 0), so g(x) >= Rem(x); each
monomial lies in its interval product; so Rem(x) >= L.
A step with objective F and sense "lo" proves F >= L; with sense "hi" the objective is -F and the step proves
F <= -L. Each step carries a claimed `value` (section 10); it is ACCEPTED iff the claim is implied (lo:
value <= L; hi: value >= -L), and THE CERTIFIED VALUE OF AN ACCEPTED STEP IS ITS `value`. A step with objective
`0`, sense "lo" and L >= value > 0 proves that F(N) is empty.
REJECTION: a step that is not accepted, a store entry that is not accepted, a declaration whose preconditions
fail, a term that names a fact that is not available in its round, or any violation of well-formedness
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
A proposed store lists `S`, all 32 box intervals and all 16 arcs; `rarc` and `cuts` list what is kept.
If a round contains an accepted `0` step, or the store after a round is EMPTY, later rounds of the node are
not evaluated.

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
  option, in order; every option of the pair NOT in Lst is excluded (4.7) on St. Child l has the additional
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
(a) INFEASIBLE: some round contains a step with objective `0` and L > 0; or the store after some round is
    empty in the sense of section 2 (then no further round is evaluated); or, for some pair {i,j} named in the
    closure, all 8 options of the pair are excluded (4.7) on the node's final store (then F(N) is empty by the
    SAT lemma); or
(b) TERMINAL: its final store passes the terminal test of section 8; or
(c) SPLIT (section 6) and all its children are closed.
TREE CONDITIONS (checked on the whole certificate): node ids are unique; the root is the node named in the
header; every id in a `children` list exists and that node's `parent` is the splitting node; every node other
than the root occurs in exactly one `children` list, exactly once; every node is reachable from the root; the number of children is 2 for box, arc
and sign splits and the number of listed options (>= 1) for an option split; every node is closed by (a), (b)
or (c).
ROOT CONDITIONS: the root has `parent` = null and an EMPTY assumption list; S_lo <= 4 and S_hi >= Sref (the
header's Sref must equal the `side` of the packing file whose SHA-256 is in the header); its data contain the
window (section 8).
THEOREM. If all conditions hold, every feasible configuration with S <= Sref in the window lies in the tube.
Proof: 16 unit squares with disjoint interiors in [0,S]^2 have S >= 4, so such a configuration lies in
F(root); by induction over the finite tree, every configuration of F(N), N closed, lies in the tube:
(a) F(N) is empty; (b) the final store holds on F(N) and implies the tube; (c) covering (section 6).

## 8. Window and tube as rational data

A WINDOW or TUBE is given by: a box (rational interval for every xi_ik, i in I, k in {1,2}) and a rational
angle radius alpha_i > 0 for every i in I. A configuration lies in it iff every xi_ik is in its interval and
every a_i = R(phi_i) u_i with |phi_i| <= alpha_i. (No slider notation here: sliders are just coordinates
xi_{2,1}, xi_{11,2}, xi_{13,2} with their own intervals; remember a = -xi_{2,1}, b = -xi_{11,2}.)
ROOT CONTAINS WINDOW: the root box contains the window box coordinate-wise; for every i, with the absolute
endpoints Ab^± := rho_i * P_i^±: cos Ab^- > 0, cos Ab^+ > 0, sin Ab^+ >= alpha_i, sin Ab^- <= -alpha_i.
(Then angle(Ab^+) = asin(sin Ab^+) >= sin Ab^+ >= alpha_i, and similarly on the other side.) Requires alpha_i < 1.
TERMINAL TEST for a final store and a tube: the store box is contained in the tube box coordinate-wise; for
every i the absolute endpoints Ab^± := rho_i * P_i^± (store endpoints) satisfy cos Ab^± > 0 and
|sin Ab^±| <= alphaT_i - alphaT_i^3/6. (Then |angle(Ab^±)| <= alphaT_i because sin x >= x - x^3/6 for
0 <= x <= pi/2 and sin is increasing on (-pi/2, pi/2); the arc lies between its endpoints.) Requires
alphaT_i <= 1.

## 9. What the generator is free to choose (never affects soundness)

Which pairs to declare, which facts to use, tangent vectors, objectives, multipliers and their rounding, the
number of rounds, store entries looser than what was certified, split types and split points, centres of
children. The checker rebuilds every fact from the node data, the store and this SPEC and recomputes every
step exactly.

## 10. Certificate format (version wx-cert-2)

All numbers are strings "p" or "p/q" (q > 0). Labels are integers. A rotation is [g, s] with g^2 + s^2 = 1
(checked for every rotation in the file). The certificate is a header object and one object per node
(JSON lines, or one JSON file per node plus an index).

WELL-FORMEDNESS. The checker rejects the certificate if any of the following fails; nothing is repaired or
skipped.
- `schema` equals "wx-cert-2"; the checker computes the SHA-256 of the packing file it reads and requires it to
  equal `packing_sha256`; `Sref` equals the file's `side`.
- Numbers are JSON strings matching `-?[0-9]+` or `-?[0-9]+/[0-9]+` with a nonzero denominator (no floats).
- Labels are integers of I = {1,...,17} minus {4} (JSON integers in fields, their decimal strings as map keys).
  Every map keyed by labels (`box`, `arc`, `alpha` in the header's `window` and `terminal`, `box` and `arc` in
  every node and in every round's `store`) has exactly the 16 keys of I.
- `k` in {1,2}; `axis` in {"a","b"}; `eps` and `sign` in {1,-1} (JSON integers; in names they are written p, m);
  `cls` matches `[ab][+-][ab][+-]`; `kind` in {"P+","P-","Pk","Ps"}; `mode` in {"opt","par"}; `sense` in
  {"lo","hi"}; corner letters in {p,m}; wall coordinate in {x,y}; wall name of a `wsup` fact in {xlo,ylo,xhi,yhi}.
- Wherever i, j name a pair (declarations, `ysign` assumptions and splits, `rarc` keys "i-j", `pair` of an
  option split or of an infeasible closure, names containing `i:j`): i < j, both in I. Wherever o, t occur
  (options, names containing `o:t`): o != t, both in I. In an `opt` declaration {o,t} = {i,j}. Every option
  listed in an option split of the pair [i,j] has {o,t} = {i,j}.
- Every fact name and form name parses by the lists below (integers without sign or leading zeros); unknown
  names are rejected; a custom form name `u:NAME` must be defined in the node's `forms`. A step may only use
  facts that are available in its round.
- Node data: lo <= hi for every box interval, S_lo <= S_hi, cos P^± > 0, sin P^- <= sin P^+, every rotation
  unit; multipliers lambda >= 0 except in terms containing a `circ` fact; every term has 1 to 3 fact names.
- At most one `par` declaration per (i, j, cls, kind) in a round (so that a fact name denotes one polynomial).
- `forms`: NAME matches `[A-Za-z0-9_]+`; every component is a form name of section 3 other than `0` and
  `u:...` and obeys the label and pair rules above; coefficients are numbers; the component names of one custom
  form are pairwise different. `forms` belongs to the node's data: it is the same for all rounds of the node
  and is not inherited by children.
- A JSON object with a repeated key is rejected.
- Well-formedness is checked on the whole file, including rounds that are not evaluated. The final store of a
  node is the store after its last evaluated round.

Header:
```
{"schema":"wx-cert-2", "packing_sha256":"...", "Sref":"4675530093604551/1000000000000000", "root":"<id>",
 "window":   {"box":{"<label>":[[lo1,hi1],[lo2,hi2]],...16 labels}, "alpha":{"<label>":"p/q",...}},
 "terminal": {"box":{...}, "alpha":{...}}}
```
Node:
```
{"id":"...", "parent":null|"...",
 "S":[S_lo,S_hi],
 "box":{"<label>":[[lo1,hi1],[lo2,hi2]],...},
 "arc":{"<label>":{"c":[g,s],"lo":[g,s],"hi":[g,s]},...},          centre; endpoints relative to the centre
 "assume":[ {"kind":"opt","o":o,"t":t,"axis":"a"|"b","eps":1|-1},
            {"kind":"ysign","i":i,"j":j,"cls":"a+b-","sign":1|-1} ],
 "forms":{"NAME":[["coef","FORMNAME"],...], ...},                   optional: custom forms u:NAME (section 3)
 "rounds":[ROUND,...],
 "close":{"kind":"infeasible"} | {"kind":"infeasible","pair":[i,j]} | {"kind":"terminal"}
        | {"kind":"split","how":SPLIT,"children":[ids]}}
```
ROUND:
```
{"pairs":[ {"i":i,"j":j,"mode":"opt","o":o,"t":t,"axis":..,"eps":..},
           {"i":i,"j":j,"mode":"par","cls":"a+a+","kind":"P+"|"P-"|"Pk"|"Ps","kappa":"p/q"}, ... ],
 "steps":[ {"form":NAME,"sense":"lo"|"hi","value":"p/q","terms":[["lambda",[FACT,...]],...]}, ... ],
 "store":{"S":[lo,hi], "box":{...}, "arc":{"<label>":{"lo":[g,s],"hi":[g,s]},...},
          "rarc":{"i-j":{"lo":[g,s]|null,"hi":[g,s]|null},...}, "cuts":{"NAME:lo":"v","NAME:hi":"v",...}}}
```
- `pairs`: declarations for this round. An `opt` declaration makes the four `opt:` facts of that option
  available iff the node assumes the option or the 7 others are excluded on the store at the start of the
  round. A `par` declaration makes the two `par:i:j:K:kind:1|2` facts available iff the preconditions of 4.6
  hold (kappa is required for Pk and Ps and ignored for P+, P-). Several declarations per pair are allowed (at most one per (i,j,cls,kind));
  undeclared pairs carry no `opt`/`par` facts. `asg:i:j:K:p|m` needs no declaration (it needs the matching sign
  assumption).
- step, sense "lo": claims form >= value; accepted iff value <= L (g = form). Sense "hi": claims
  form <= value; accepted iff -value <= L computed with g = -form. Form `0`, sense "lo": accepted iff
  L >= value > 0; it is evidence for the closure "infeasible".
- `store`: the store after the round, accepted entry by entry by the rules of section 5 (the `arc` entries
  have no centre: centres never change). If the new store is empty in the sense of section 2, the node is
  infeasible and must have close kind "infeasible".
- A node with close kind "infeasible" must contain evidence. The form `{"kind":"infeasible"}` is accepted iff
  some evaluated round contains an accepted `0` step or the store after some evaluated round is EMPTY. The form
  `{"kind":"infeasible","pair":[i,j]}` is accepted iff the node's final store is NOT EMPTY and all 8 options of
  the named pair are excluded (4.7) on it (other evidence in the node does not replace this test). A node with
  close kind "terminal" or "split" is checked as such even if it also contains an infeasibility step (a node
  that is empty is correctly closed either way), but its store must never be empty when facts are built.
FACT names: `box:i:k:lo|hi`; `side:lo|hi`; `wall:i:E1:E2:k:lo|hi` (E1, E2 in {p,m} for +1, -1; k in {x,y});
`arc:i:slo|shi|clo|chi|chord`; `arc:i:tan:G:H` (G, H rational strings); `wsup:i:W:p|m` (W in
{xlo,ylo,xhi,yhi}; available without declaration iff the sign conditions of 4.8 hold on the store at the
start of the round); `rarc:i:j:slo|shi|clo|chi|chord`;
`rarc:i:j:tan:G:H`; `opt:o:t:axis:EPS:E1:E2` (EPS in {p,m}; E1,E2 the corner of t); `par:i:j:K:kind:1|2`;
`asg:i:j:K:p|m`; `ivl:FORM:lo|hi` for FORM = `Da:o:t`, `Db:o:t` or an affine custom form `u:NAME`;
`cut:FORM:lo|hi` for any form name except `0`; `circ:i`.
Form NAMEs: `xi:i:k`, `S`, `C:i`, `s:i`, `Da:o:t`, `Db:o:t`, `A:o:t`, `B:o:t`, `Cr:i:j`, `Sr:i:j`,
`al:i:j:K`, `be:i:j:K`, `co:i:j:K`, `si:i:j:K`, `Y:i:j:K`, `u:NAME`, `0`.
SPLIT: `{"type":"box","sq":i,"k":k,"at":"m"}`; `{"type":"arc","sq":i,"at":[g,s]}`;
`{"type":"opt","pair":[i,j],"options":[{"o":..,"t":..,"axis":..,"eps":..},...]}`;
`{"type":"ysign","i":i,"j":j,"cls":"...."}` (children: sign +1 first, then -1).
A node object can be checked alone (result: accepted, with its final store); the tree pass checks the tree,
root, child-containment and terminal conditions of sections 6 to 8.

## 11. What the application must add to (ANN)

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

## 12. Advice for generators (not normative)

Linear programs over lifted variables: use the monomials of the facts and their products as LP columns
(or product variables per (owner,target) form); rows = facts and products of facts; keep the provenance of
every row (which facts were multiplied) so that the LP dual becomes the term list of a step. Leave lifted
columns free and put bounds only on base variables. Round multipliers to rationals with small denominators;
the exact check absorbs the rounding in Rem. Useful products: bound fact of C_o or s_o times `ivl`/`cut` fact of
Da_ot, Db_ot (McCormick); bound facts of two trig variables; `opt`/`par` fact times a bound fact of some s_j
(stress that varies affinely with an angle).
