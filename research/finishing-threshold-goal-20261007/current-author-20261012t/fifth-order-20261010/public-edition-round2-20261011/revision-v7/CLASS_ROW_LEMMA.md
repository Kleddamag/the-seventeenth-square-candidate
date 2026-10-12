# Class-row lemma

All source abbreviations and line references below are bound by full SHA256 in
`../CLASS_ROW_SOURCES_PUBLIC.json` (one folder above). This states the **minimum-score** theorem used by the selected
proof. The independent derivation of record is **CC §(2)**; its source audit and
finite tests have the limits stated in that report. Authentic complete execution
on the bound inputs and sound exact arithmetic are hypotheses, not consequences
of a JSON file saying PASS.

**Statement.** Fix a validated certificate with scaled container side L, parent
side A, nonnegative integer feature weights, budget M, and positive charge scale
Gamma. Fix the declared centre c, closed pose classes E_j (convex centre polygons
times closed angle gates, with their prescribed lifts and symmetry images),
nonnegative rational thresholds t_j and bound beta. Put tau(p)=min{t_j:p in E_j}
when that set is nonempty, and tau(p)=1 otherwise. A fully checked PASS row with
angle interval I asserts: for every contained unit-square pose p with direction
in I, and every checked cell Q whose closure contains its centre, the cell level
R(Q,I) dominates tau(p), and there exists a closed core inside the **open physical
parent** with charge at least Gamma*tau(p). A complete valid row cover therefore
gives, for every finite family of contained unit squares with pairwise disjoint
interiors in the side-C=L/A square centred at c,

    Gamma sum_p tau(p) <= sum_p chi(K_p) <= M < beta Gamma,

hence sum tau<beta. In particular this holds for every packing of seventeen
unit squares in that declared frame. A single row gives this conclusion only
for families whose directions it covers; different parents may use different
rows of the complete cover. Closed position/angle boundaries and touching
parents are included. The four links are as follows.

1. **Capacity.** A threshold feature with positive coefficients a_j and threshold
   k fires on at most floor(sum a_j/k) disjoint cores; each site can occur in at
   most one core. Nonempty winning masks with pairwise nonempty intersection
   instead have capacity one. Summing with nonnegative weights gives the
   recomputed budget M. There is no square-count hypothesis in this bound.
   [RC 251–255; PY 198–224 (fixed/mirror), EG 22–29,46–47 (orbit); CR 15; CC §(2)(i).]

2. **Row validity.** The endpoint tests give a positive core-containment margin
   throughout I: cos(delta)+|sin(delta)| increases with |delta| on [0,pi/4].
   Concavity of cos(phi)+sin(phi) puts every legal centre in the closed row
   envelope, which has nonempty interior. Fixed rows cover a quarter turn;
   folded rows cover beyond pi/4. In the latter case reflect a pose into a
   checked row and reflect its core **back into the original parent**. The
   validated feature potential and class unions are invariant under the used
   symmetry. Disjointness is needed for original parents, never for their
   separately folded images. [RC 257–266; PY 298–313 (rows), 228–251 and 288–289 (mirror validation); EG 24,32–44 (orbit validation); CR 13; CC §(2)(ii).]

3. **Closed-boundary limit and class level.** At a legal boundary centre q,
   choose generic envelope-interior centres converging to q in one checked
   adjacent cell, avoiding the finitely many arrangement edges and degenerate
   atoms. Take a constant site-hit subsequence. Every hit persists in the closed
   limiting core, which remains strictly inside its parent; monotonicity of the
   original Boolean features gives chi(K_q)>=m(Q). High classes are tested by
   closed meeting, low classes by containing the whole closed cell/row product
   in one slot image. Their priority rule gives R>=tau, including overlaps:
   a containing high is detected, an accepted low contains p, and default 1 is
   safe when neither occurs. The stronger high-first score also is dominated,
   but is unnecessary here. [CR 17 is the limiting-core argument; RC 279–288 give the nearby-generic-core variant; HF 5–19; CR 9–17; CC §(2)(iii).]

4. **Sweep, cell arithmetic and strictness.** The Möbius expansion evaluates the
   original features exactly on generic cells; signed atoms themselves need
   not be monotone. The sweep covers a superset of all cells meeting the row
   envelope. Exact geometry, complete cell partitions and the checked absolute
   atom bound <2^50 make the integer sums exact. PASS checks
   m(Q)>=Gamma*R(Q,I) using integer cross-products, for every checked cell.
   All preceding inequalities are weak. The only strict step is the validated
   integer test M*q_beta < p_beta*Gamma. Thus one integer unit of surplus is
   sufficient; no numerical margin or rounding assumption intervenes.
   [RC 268–271; PY 293, 446–490; CR 19; CC §(2)(iv) and CODE READ.]

This lemma supplies a score inequality. Capacity of capture targets, assignment
to distinct physical labels, admission to local roots and receipt provenance
are separate proof obligations.

The source abbreviations and references retain their original line numbering; the edition note in the clean CC copy explains its line edits.

**Finite implementation safeguards for the selected data.** The Node midpoint shifts require index sums below 2^31. For the 98 selected certificates the exact maximum site count is 83,128. Rectangle endpoints are site projections plus/minus the common halfwidth, so each coordinate array has at most 166,260 entries; bisect index sums are at most 332,520. The padded tree has at most 262,144 leaves, arrays of at most 524,288 entries, and midpoint sums at most 524,288. Per-row cells are bounded by 27,642,055,081 and the all-row counter by 497,556,991,458,000<2^53; these counters do not undergo signed shifts. These are certified upper bounds on realized grids, not observed maxima, and apply only to the pinned data. [file:INDEX_SAFETY]

A merged PASS is not itself the fully checked row hypothesis above. Merge trusts stored Boolean row flags and does not re-derive them from recorded minima and class thresholds. Neither a recheck of those recorded decisions nor the index-size bounds is a fresh sweep of the cell geometry.
