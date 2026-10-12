# Restricted charge certificates: schema, statement, soundness (8 Oct 2026)

**What changed with the fixed-image extension.**
* Exempt-set generator: the `restriction` object and the kinds `empty`, `slots`, `outside_cells`
  are UNCHANGED. The value for fixed-image certificates is **`"symmetry": "fixed"`** (final). The
  generator's provisional `"none"` stays refused; that one constant has to be changed. All 124 objects under
  `cert_restricted/exempt/` parse (60 of them after that change), including the 843-digit
  coordinates of slot 13.
* Engine side: the fixed-image shape is section 1.4 (features image by image, no orbit closure),
  rows are a chain on u in [0, 1] ending exactly at 1 (1.5), the boundary rule is 1.6 and 1.7.
  Example files: `cert_restricted/examples/`.
* Node twin: section 1 is the complete format; 1.6 and 1.7 are everything the exemption needs.
* Additions only: `symmetry: "fixed"`, kind `mixed`, top-level `sites` / `features`, result fields,
  options `--engine`, `--workers`, `--restriction`, `--merge`. One result field changed type (1.8).
* No soundness problem was found in the earlier symmetric checker (what was re-derived: section 9).

Code: `cert_restricted/exact_restricted.py`. The three files next to it (`boolean_rule.py`,
`integer_sweep.py`, `exact_general.py`) are byte-identical copies of `bounds/4.6601/global_src`;
rectangles, sweep geometry and tree arithmetic come from them unchanged in every mode.
Tests: `cert_restricted/tests/test_restricted.py` (section 8). Python only.

## 1. Certificate format (complete)

A certificate is one JSON object. Every number is a JSON integer or a string `"p/q"` / `"p"`
(exact rational). Floats are refused wherever this note says "rational" or "integer". There are two
shapes: *symmetric* (the published certificate plus a `restriction` object) and *fixed-image*.

### 1.1 Common keys (both shapes)

| key | type | meaning |
|---|---|---|
| `L` | rational | must equal `4613/1000` (side of the certificate container `[0,L]^2`) |
| `A` | rational | side of a rescaled unit square, `0 < A < L`; the statement is about containers of side `S = L/A` |
| `normalized_target` | rational | must equal `L/A` |
| `coordinate_denominator` | integer D > 0 | site coordinates are integers over D; `L*D` must be an integer `LD` |
| `weight_denominator` | integer > 0 | informational (weights are integers in units of 1/this) |
| `budget_units` | integer | must equal the budget recomputed from the features (1.3 / 1.4) |
| `minimum_units` | integer > 0 | the threshold Gamma |
| `entries` | list of rows `[a, b, t, B]` | angle rows (1.5) |
| `restriction` | object | (1.2) |

Unknown top-level keys are ignored (free text such as `source`), except that a fixed-image
certificate must not contain `point_orbits` / `threshold_orbits` and a symmetric one must not
contain `sites` / `features`.

### 1.2 The `restriction` object (unchanged, plus two values)

    "restriction": {
      "schema":   "s17-restricted-v1",
      "k":        17,                          # integer >= 1; k * minimum_units > budget_units is checked
      "symmetry": "orbit" | "core" | "fixed",  # "fixed" is new
      "frame":    {"unit": "unit_square", "center": ["x","y"]},
      "exempt":   {"kind": "empty"}
                | {"kind": "slots", "slots": [ SLOT, ... ]}                       # 1..4096 slots
                | {"kind": "outside_cells", "cells": [ POLYGON, ... ]}            # 1..4096 cells
                | {"kind": "mixed", "slots": [ SLOT, ... ], "cells": [ POLYGON, ... ]},   # new
      "comment":  "..."                        # optional, ignored
    }
    SLOT    = {"centre": {"polygon": POLYGON} | {"disc": {"center": ["x","y"], "radius": "r"}},
               "angle_tan_half": ["lo","hi"],  # optional; omitted = all angles
               "label": "..."}                 # optional, ignored
    POLYGON = [["x","y"], ...]                 # 3..64 vertices

No other keys, no other values. All coordinates are rationals.

* **Frame.** Coordinates of the exempt set are in unit-square lengths. `frame.center` is the frame
  point at which the centre of the container sits. A frame point `e` is the certificate point
  `X = (L/2, L/2) + A (e - center)` (container `[0,L]^2`, squares of side A). A translation only,
  never a rescaling. With `center = (1169/500, 1169/500)` the exempt sets are in the skeleton's frame
  F_U for every cap.
* **Pose** of a square: its centre and the direction `phi` of a side, modulo pi/2.
* **Polygon**: the closed convex hull of its vertices. Vertices counter-clockwise, strictly convex
  (checked: every consecutive turn is a strict left turn, every vertex is on the closed left side
  of every edge, no vertex repeated). **Disc**: closed, radius > 0.
* **`angle_tan_half = [lo, hi]`**, `-1 < lo <= hi < 1`: the closed set of directions
  `phi = 2 atan(tau) mod pi/2`, `tau in [lo, hi]` (all quarter-turn lifts included). A gate across
  the 0 / 90 degree seam is written with `lo < 0 < hi`; a gate of negative reference angle with
  `lo <= hi < 0`. In the unfolded chart u in [0, 1] of 1.5 the gate `[lo, hi]` with `lo < 0 <= hi` is
  `u in [0, hi]` together with `u in [(1+lo)/(1-lo), 1]`.
* **The exempt set E**: `slots`: union of the slots (centre in the closed region AND direction in
  the gate). `outside_cells`: all poses whose centre is NOT in the union of the closed cells (any
  direction). `mixed`: the union of the two. `empty`: nothing.
* **`symmetry`** says which set E* the statement is about and which charge format is read:
  `orbit`: E* = union of the eight D4 images of E; `core`: E* = intersection of the eight images;
  both need the symmetric shape (1.3) and rows on the folded range. `fixed`: E* = E exactly as
  written, nothing is symmetrised; needs the fixed-image shape (1.4) and rows on the full range.
  D4 acts about the container centre: centre `center + G (e - center)`, G one of the eight signed
  permutation matrices; a rotation keeps the direction modulo pi/2, a reflection sends `tau` to `-tau`.

### 1.3 Charge, symmetric shape (`orbit`, `core`): the published fields, unchanged

`point_orbits`: rows `[x, y, w]` (integers, `0 <= x,y <= LD`, `w >= 0`); the orbit is the set of
distinct points among `(u, v)`, `u in {x', LD-x'}`, `v in {y', LD-y'}`, `(x', y') in {(x,y), (y,x)}`,
sorted by first then second coordinate; all sites are numbered in this order, orbit after orbit,
and each carries weight w as a point feature. `threshold_orbits`: objects with `sets` (a complete
D4 orbit of site-index lists), `weight`, `threshold` (default 2), optional `coefficients`,
`winning_masks`; each set is one feature image as in 1.4, all with the same weight. Validation
and budget exactly as `exact_general.expand` / the published Node checker.

### 1.4 Charge, fixed-image shape (`fixed`): image by image, no orbit closure

    "sites":    [[x, y], ...],        # integers, 0 <= x, y <= LD, pairwise distinct; site i is the
                                      # certificate point (x/D, y/D); at least one site
    "features": [ {"sites": [i0, i1, ...],        # 1..20 distinct site indices (positions 0..n-1)
                   "weight": w,                   # integer >= 0, in units of 1/weight_denominator
                   "threshold": k,                # integer, 1 <= k <= sum of the coefficients
                   "coefficients": [a0, a1, ...], # optional (default all 1): positive integers,
                                                  # non-increasing, one per position
                   "winning_masks": [m, ...]},    # optional: see below
                 ... ]

No other keys in a feature. Each list entry is ONE feature image with its own weight. Nothing is
closed under D4 and nothing is tied: a D4 orbit with a common weight is written as its images, each
with that weight. A point of weight w is the feature `{"sites":[i],"weight":w,"threshold":1}`.
Repeating a feature is allowed (the weights add). Sites used by no feature are allowed.

* A feature **fires** on a closed set K (the core of a square, 1.5) iff
  `sum of a_j over the positions j whose site lies in K  >=  k`;
  with `winning_masks` instead iff K contains all sites of some mask (bit j of a mask = position j).
  With `winning_masks`: at most 12 sites, masks distinct integers with `0 < m < 2^n`, every two masks
  share a bit; `threshold` may then be omitted (if present it must satisfy the same bounds and is
  ignored).
* **Charge** of K = sum of the weights of the features that fire on K.
* **Capacity** of a feature = `floor(sum(a_j) / k)`, or 1 with `winning_masks`.
  `budget_units` must equal `sum over features of weight * capacity`.
* **Integer safety**: `sum over features of weight * (sum of |c| over the Moebius terms of its
  indicator)` must be `< 2^50`, where the terms are those of the published expansion
  (`boolean_rule.expansion`: the indicator as an integer combination of "all sites of a subset
  captured").

### 1.5 Rows

`entries` is a list of rows `[a, b, t, B]` (rationals). A row says: for every pose whose side
direction is `phi = 2 atan(u)` with `u in [a, b]`, the *core* is the concentric closed square of
side B with side direction `theta = 2 atan(t)`. With `c(x) = (1-x^2)/(1+x^2)`, `s(x) = 2x/(1+x^2)`
the checks per row are, exactly as published:

    0 <= a < b,   0 <= t < 1,   0 < B < A,   a = b of the previous row (a = 0 for the first)
    for u in {a, b}:  dot = c(t)c(u) + s(t)s(u) > 0,   cross = |c(t)s(u) - s(t)c(u)| <= dot
    A - B * max over u in {a, b} of (dot + cross) > 0                       (strict core)
    r = A * min over u in {a, b} of (c(u) + s(u)) / 2,   B (c(t) + s(t)) / 2 <= r < L/2
    job = (t, B, H) with H = L/2 - r      (the centre envelope is [r, L-r]^2)

(`t < 1` also in a row that ends at `u = 1`: the core direction stays below 90 degrees.) The range:

* symmetric shape: `b < 1` in every row and the chain ends at an `e` with `e^2 + 2e > 1`
  (beyond tan(pi/8), the folded range), as published;
* fixed-image shape: `b <= 1` and the chain ends EXACTLY at `1`: the rows cover `u in [0, 1]`,
  i.e. all directions `phi in [0, pi/2]`, with no folding. A row ending at `u = 1` is allowed
  (`c(1) = 0, s(1) = 1`); `certlib.make_row` computes t and B correctly for it but its own check
  refuses `b = 1`.

Row index = position in `entries` (0-based) in both shapes. The row is swept with the published
routine: `exact_general.geometry(sites, site_weights, features, feature_weights, D, t, B, H)` then
`integer_sweep.accumulate` (in the fixed-image shape all site weights are 0 and every feature is
the tuple `(site indices, k, coefficients, masks)` with its own weight).

### 1.6 When a row uses a slot (angle rule)

For a row `[a, b]` and a slot with gate `[lo, hi]`: the slot is *active* in the row iff the whole
closed interval lies in one quarter-turn lift of the gate, i.e. iff for one m in {-1, 0, 1}

    l_m <= a  and  b <= h_m,   (l_0, h_0) = (lo, hi),
    (l_1, h_1) = ((1+lo)/(1-lo), (1+hi)/(1-hi)),   (l_-1, h_-1) = ((lo-1)/(lo+1), (hi-1)/(hi+1)).

(All values are tan(x/2) of angles in (-pi, pi), where tan(x/2) is increasing.) A slot without a
gate is active in every row. A row that straddles an end of the gate does not use the slot at all.
In the symmetric modes the interval tested for the image under a reflection is `[-b, -a]`.

### 1.7 When a cell is exempt (centre rule), and when a row passes

Sweep coordinates of a row (published code): with `t = p/q` in lowest terms, `C = q^2 - p^2`,
`S = 2pq`, `R = q^2 + p^2`, and `scale = lcm(2D, denominator(B/2), denominator(H))`, a certificate
point X has `u = scale * (C x' + S y')`, `v = scale * (-S x' + C y')`, `(x', y') = X - (L/2, L/2)`.
The frame point of sweep point `(u, v)` is

    e(u, v) = center + (C u - S v, S u + C v) / K,     K = A * scale * R^2.

The cells are the rectangles `[xe_k, xe_{k+1}] x [ye_j, ye_{j+1}]` of the published arrangement
(all rectangle edges and envelope vertices); the checked cells of slab k are `first_k <= j < last_k`
as published. All `xe`, `ye` are integers.

A checked cell is **exempt** iff the closed set (closed cell) x (closed row interval) is certainly
inside E*. For `fixed` this is decided for E as written:

* by a slot: the slot is active in the row (1.6) and all four corners `e(u, v)` of the cell lie in
  the closed centre region (polygon: on the closed inner side of every edge; disc: distance to the
  centre <= radius). ONE slot must contain the whole cell; a cell covered by two slots together
  but by neither alone is not exempt;
* by the cells of `outside_cells` / `mixed`: the closed cell is disjoint from every closed polygon
  of the list (equivalently: for every polygon there is a strictly separating line parallel to a
  side of the cell or to an edge of the polygon); touching is not disjoint;
* `mixed`: either of the two; `empty`: never.

For `orbit` (`core`) the same test is made for the eight images `G(cell x interval)`,
`e_G(u, v) = center + G (C u - S v, S u + C v) / K`, interval `[a, b]` for rotations and `[-b, -a]`
for reflections, and the cell is exempt iff the test succeeds for one (for every) G. The order of
the eight matrices does not matter.

**A row passes** iff every checked cell with charge `< minimum_units` is exempt. Equivalently: the
minimum of the charge over the checked cells that are not exempt is `>= minimum_units`. Every
comparison on this path is exact (integers or rationals).

### 1.8 Running, slices, results

    python exact_restricted.py CERT.json --output OUT.json [--start i] [--count n] [--workers w]
                               [--engine fast|reference] [--audit] [--restriction R.json]
    python exact_restricted.py CERT.json --output ALL.json --merge OUT1.json OUT2.json ...

`--start/--count`: rows `i .. i+n-1` (default: all). `--workers w`: w forked processes (numba is
compiled in the parent first). `--restriction R.json`: take the `restriction` object from that file
(the object itself, or any JSON object with a key `restriction`, e.g. `exempt/A/C01.json`); the
certificate must then contain none. `--engine`, `--audit`: section 7. Every run validates the WHOLE certificate first (structure, budget, row chain).
Exit code 0 = no row of the range failed, 2 = some row failed; a refused certificate ends with a
`ValueError`. Result file:

| key | meaning |
|---|---|
| `status` | `PASS_RESTRICTED_EXACT_COVER` (all rows of the certificate, all passed), `PASS_RESTRICTED_INTERVAL_PARTITION_ONLY` (a slice, all passed), `RESTRICTED_EXACT_COVERAGE_FAILURE` |
| `statement` | the proved sentence, only with the first status; otherwise null |
| `schema`, `k`, `symmetry`, `exempt_kind`, `start`, `end_exclusive`, `total_intervals`, `required_units`, `budget_units`, `surplus` (= k * minimum_units - budget_units), `failed_intervals`, `minimum_margin`, `certificate_sha256`, `restriction_sha256` (with `--restriction`), `checker_sha256` (the four source files), `seconds` | as named |
| `unrestricted_minimum_units` | least published row minimum in the range (all checked cells) |
| `rows` | per row: `interval`, `minimum_units` (published minimum), `cells`, `passed`, `engine`, `deficient_slabs` (checked slabs whose minimum is below the threshold), `deficit_minimum_units` (exact minimum over the non-exempt checked cells if that is below `minimum_units`, else null; fast engine only), `witness` (the first failing cell in sweep order, frame coordinates of its corners), `cpu_seconds`. `deficient_cells`, `deficient_runs`, `exemption_tests` are counted by the reference engine only; for a row decided by the fast engine alone the first two are null (CHANGE: they were always integers before) |

`--merge` validates the certificate again and accepts the slices only if they carry this
certificate's sha256, identical `checker_sha256`, `k`, `symmetry`, `required_units`, and together
contain every row `0 .. total_intervals-1`; its status is `PASS_RESTRICTED_EXACT_COVER` only if
every row passed in every slice that holds it, otherwise `RESTRICTED_EXACT_COVERAGE_FAILURE` or
`MERGE_INCOMPLETE` (exit 3).

## 2. Statement proved

Let S = L/A, M = `budget_units`, Gamma = `minimum_units`, and E* as in 1.2 (`orbit`: union of the
eight images of E, `core`: their intersection, `fixed`: E itself). If the checker returns
`PASS_RESTRICTED_EXACT_COVER` (one complete run, or `--merge` of slices), then

> in every family of closed unit squares with pairwise disjoint interiors inside a square of side
> S, read in the frame with the container centre at `frame.center` (hence in every family inside a
> smaller concentric square), at most k-1 members have a pose outside E*. For k = 17: every
> 17-packing of side <= S has a member whose pose lies in E*.

This is L2 of PROOF_SKELETON.md. Sections 3 to 5 prove it; section 6 is the transport lemma L3.

## 3. One row: what the published routine gives, on the whole range u in [0, 1]

Notation: container C = [0, L]^2 with centre o; squares of side A ("parents"); a pose is (centre q,
side direction phi mod pi/2); Pi(q, phi) is the closed parent. For a closed set K the charge
chi(K) is the sum of the weights of the features that fire on K (1.4; in the symmetric shape the
published charge). Nothing in this section uses D4.

**R1 (budget).** For pairwise disjoint sets K_1, ..., K_n: sum chi(K_i) <= M. Proof: a feature with
coefficients a_j and threshold k fires on K only if the sites of total coefficient >= k lie in K;
the K_i are disjoint, so it fires on at most floor(sum a_j / k) of them; with pairwise intersecting
masks on at most one. Sum with the nonnegative weights; the checker recomputes this sum and demands
equality with `budget_units`. No symmetry, no bound on n, any sets.

**R2 (row geometry).** Let a row (a, b, t, B) pass the checks of 1.5, theta = 2 atan(t), and let
(q, phi) be a pose with Pi(q, phi) inside C and phi = 2 atan(u), u in [a, b] (so phi in [0, pi/2]).
(i) q lies in the closed envelope Env = [r, L-r]^2: the bounding box of the parent has half-width
A (cos phi + sin phi)/2 for phi in [0, pi/2], and cos + sin is concave there, so its minimum over
[phi_a, phi_b] is at an end; that is r. (ii) The checks `dot > 0`, `cross <= dot` say
|theta - phi| <= pi/4 at both ends, hence on the whole interval; there cos d + |sin d| increases
with |d|, so `A - B max(dot + cross) > 0` gives: the closed square K(q') of side B, direction theta,
centre q' lies in the OPEN parent for all q' in a neighbourhood of q. (i) and (ii) use only
0 <= phi <= pi/2 and are the published arguments; they do not use phi <= pi/4. A row ending at
u = 1 (phi = pi/2) is covered (cos = 0, sin = 1).

**R3 (sweep).** The published routine computes for every open cell Q of the arrangement that
meets Env (it checks a superset of these) an integer m(Q) with chi(K(q')) = m(Q) for every q' in Q
outside finitely many segments. Exact: rational geometry in Python integers, tree sums in int64
under the 2^50 bound, which the checker verifies with the per-image weights.

**R4 (cell rule).** The row passes iff every checked cell Q with m(Q) < Gamma is exempt, and Q is
exempt only if (closure of Q) x [a, b] is inside E* (1.7; the tests are containment of the four
corners in a closed convex region, or strict separation from every closed cell polygon; both are
exact and both imply containment of the whole closed rectangle times the closed interval, the gate
part by 1.6).

**Row lemma.** If the row passes, then every pose (q, phi) with u in [a, b], parent inside C and
pose NOT in E* has a closed square K inside the open parent with chi(K) >= Gamma.
Proof. q is in Env (R2 i). Env is a square with non-empty interior (r < L/2), so points of the
interior of Env, off all arrangement lines and off the finitely many exceptional segments, exist
arbitrarily close to q; each lies in an open cell meeting Env, i.e. a checked cell. There are
finitely many cells, so one checked cell Q has such points q' -> q, and q is in the closure of Q.
If Q were exempt, (closure Q) x [a, b], which contains the pose, would lie in E*: contradiction.
So m(Q) >= Gamma, and K = K(q') for q' close enough to q is inside the open parent (R2 ii) with
chi(K) = m(Q) >= Gamma. This covers centres on envelope and cell boundaries, contacts and both
ends of the interval; exemption is never granted by rounding because there is none.

Conservative losses (safe): a cell covered by two slots but by neither alone; a gate longer than a
quarter turn; a row straddling a gate end (no exemption at all in that row: the effective gate is
shorter by up to one row width at each end, skeleton G10); cells of the conservative envelope
cover that contain no legal centre.

## 4. Symmetric modes (`orbit`, `core`): unchanged

The format forces a D4-invariant charge (complete orbits, one weight) and rows on [0, e],
e > tan(pi/8). E* is D4-invariant by construction. For a pose p outside E* pick G in D4 with the
direction of Gp in [0, pi/4]; Gp is outside E* and has a row; the row lemma gives K' in the open
parent of Gp; K = G^-1 K' is in the open parent of p and chi(K) = chi(K') by invariance. Then
section 5, last step. For an invariant charge "charge >= Gamma outside E" is equivalent to the same
outside the intersection of the images; hence the two readings and nothing else:

* `core`: exempt only what lies in all eight images. Proves the statement for E itself.
* `orbit`: exempt what lies in some image. Proves the statement for the UNION of the eight images
  of E, not for E; the result's `statement` says so. Feeding a set that is not D4-invariant to a
  symmetric mode is therefore never a proof about that set: `core` rejects unless the under-charged
  cells lie in all images, `orbit` answers about the union. A fixed-image file is refused in both.

## 5. Fixed-image L2: statement, hypotheses, proof

**Statement.** Let a fixed-image certificate (1.4, 1.5) with exempt set E pass on all its rows.
Then in every family F of closed unit squares with pairwise disjoint interiors inside a square of
side S' <= S = L/A, placed concentrically in the frame, at most k-1 members have a pose outside E.

**Hypotheses, and where each is checked.**
(H1) weights are integers >= 0, the budget M is the recomputed sum of weight x capacity,
k Gamma > M (validation); (H2) the rows form a gapless chain of closed intervals from u = 0 to
u = 1, each passing the checks of 1.5 (validation); (H3) every row passes in the sense of R4 with
E* = E, identity image only (the sweeps); (H4) the published routine is correct as used (R3:
same code, same int64 bound); (H5) E is a set of poses modulo pi/2: the gate of a slot is read with
all its quarter-turn lifts (1.6). Not assumed: any symmetry of the charge, of E or of the family;
any orbit structure of the features.

**What tiles what.** The pose space is {(q, phi mod pi/2)}; every direction has exactly one
representative phi in [0, pi/2), i.e. u = tan(phi/2) in [0, 1). Row i covers the poses with
u in [a_i, b_i] and ALL centres (R2 i: the whole envelope, not a quadrant). By (H2) the closed
intervals cover [0, 1]. So every pose lies in at least one row; poses on a common end of two rows
lie in both. The 0 / 90 degree seam: direction 0 is u = 0 in the first row; directions just below
90 degrees are u just below 1 in the last row; u = 1 is the same direction as u = 0 and is covered
twice. There is no 45 degree fold: tan(pi/8) is an interior point of the chain like any other. No
reduction to a fundamental domain is made and no image of the charge is taken: the published row
routine never used phi <= pi/4 (R2), so one call per row suffices. (The folded alternative, rows on
[0, pi/4] run twice, once with all sites and E transposed, is equivalent and was not implemented;
the engine exports the unfolded chain.)

**Proof.** Scale by A about the frame centre: the family becomes parents of side A with disjoint
interiors inside a concentric square of side A S' <= L, hence inside C; frame poses and certificate
poses correspond by 1.2. Let p = (q, phi) be the pose of a member with p not in E, phi in [0, pi/2),
u = tan(phi/2) in [0, 1). By (H2) some row has u in [a, b]. By (H3) and the row lemma there is a
closed square K_p inside the open parent with chi(K_p) >= Gamma. (H5) is what makes "p not in E"
independent of the representative: the row test asks whether [a, b] lies in SOME lift of the gate.
The sets K_p of different members lie in disjoint open parents, so they are pairwise disjoint and
by R1 their charges sum to at most M. If n members have a pose outside E then n Gamma <= M <
k Gamma, so n <= k-1.

The statement does not see the actual side S': it holds for every S' <= S, in particular at the
optimum and above it (skeleton 2.4).

## 6. Transport (L3)

**Statement.** Let a fixed-image certificate prove: "every family as in section 5 has at most k-1
members with pose outside E". Then for every G in D4 the same holds with E^G in place of E, where
D4 acts about `frame.center` and E^G = { G p : p in E } (1.2: centre `center + G(e - center)`,
direction kept by rotations and negated by reflections, modulo pi/2). No second certificate.

**Proof.** Let F be such a family and G in D4. G^-1 F is again a family of closed unit squares with
disjoint interiors inside the same concentric square. If s in F has pose p, then G^-1 s has pose
G^-1 p. p outside E^G iff G^-1 p outside E. So the members of F with pose outside E^G correspond
to the members of G^-1 F with pose outside E: at most k-1.

**What has to be true of the checker for this to hold** (and only this):
1. The proved statement quantifies over ALL families in the container, with no reduction of the
   family or of the pose space by symmetry. True in `fixed` mode: section 5 covers every pose.
2. The class of admissible families is D4-invariant about `frame.center`: the container is an
   axis-parallel square centred there. True by construction ([0, L]^2 with o at `frame.center`).
3. The pose of the image square is the image pose, with the action the user applies to E. The
   checker's pose is (centre, side direction mod pi/2) and E is read modulo pi/2 (H5), so E is a
   well-defined subset of that pose space and E^G is its image: polygons mapped by
   `center + G(. - center)`, a gate [lo, hi] kept by a rotation and replaced by [-hi, -lo] by a
   reflection. `exact_restricted.image_exempt(exempt, center, g)` writes E^G in the schema.
4. Nothing about the charge: it need not be symmetric, and the checker is NOT required to accept
   the image certificate. (It does: test "transport" maps sites, E and rows by each G and gets the
   same verdicts and minima row by row. This is a consistency check, not a premise.)
Not transported: the cap (the statement is for the container of side S only) and anything about
E^G for a map G outside D4.

With E_j = What_j ∪ Z_id (L6): (E_j)^G = What_j^G ∪ Z_G, because (M^H)^G = M^{GH} and H -> GH maps
{H != id} onto {H != G}.

## 7. Two engines, one rule

Both decide R4. `reference` (the earlier code): a second tree sweep lists every checked cell below
the threshold as runs along v; runs are tested as rectangles and bisected down to single cells.
`fast` (default; `reference` if the exempt set has a disc or is `empty`):

1. the published sweep; if its minimum is >= Gamma the row passes (as before);
2. a sweep that records the minimum of every slab; slabs with minimum < Gamma are "deficient";
3. for each deficient slab [u0, u1] the exempt y-cells are computed as index intervals:
   for a slot polygon, the cells with all four corners inside: with the integer edge forms
   a u + b v + c >= 0 of the row and m = c + min(a u0, a u1): `ye_j >= ceil(-m/b)` for b > 0,
   `ye_{j+1} <= floor(m/(-b))` for b < 0, `m >= 0` for b = 0, located by bisection in `ye`;
   for a cell polygon, the cells meeting it: those meeting the exact v-range of
   (polygon ∩ slab), taken over its vertices in the slab and its edge crossings with u = u0, u1;
   exempt = union of the slot intervals and, with cell polygons, the complement of the union of
   their intervals; `orbit` / `core`: union / intersection over the eight images;
4. the published sweep once more, with the query range of each deficient slab replaced by the
   complement of its exempt intervals; other slabs are queried whole. The row passes iff the
   minimum of everything queried is >= Gamma.

Step 4 alone decides; step 2 only selects where step 3 is needed. Step 3 is the same predicate as
the reference rectangle test restricted to single cells: for polygons literally the same forms;
for cell polygons by the separating-axis theorem (a closed rectangle and a closed convex polygon
are disjoint iff a line parallel to a side of one of them separates them strictly, which is what
the reference test tries). Denominators are cleared once per row and region; per slab only Python
integer arithmetic (floor division, comparisons) and bisection; the tree is int64 under the 2^50
bound. No float anywhere. The cost no longer depends on the number of deficient cells.

Built-in cross-checks: the slab sweep must reproduce the published minimum and cell count; every
failing cell reported by the fast engine is re-tested with the reference rectangle test and must
not be exempt. `--audit` runs both engines plus a direct enumeration and demands the same first
failing cell and, for rows with at most 20,000 deficient cells, the same exemption cell by cell.

## 8. Tests and measurements

`../.venv/bin/python tests/test_restricted.py` (all 8 groups: 133 checks, all passing, about 2 CPU-minutes; one process, except that `cli` starts two workers for a 4-row certificate):
* old groups `units`, `tiny`, `published`: unchanged and passing; `tiny` now runs both engines.
* `fixed_units` (27): refusals (wrong shape for the mode, chains that stop at 1/2 or at the
  folded end or have a gap, budget, k, weights, sites, masks, 2^50), capacities, `image_exempt`.
* `fixed_tiny` (24): (c) 225 grid points image by image, one point of weight 0 at (1, 1/3): every
  core of side 1/2 holds a point of weight 1 unless its centre is within 0.4 of that point; a box
  around it passes on u in [0, 1], cross-checked by float sampling of 6,000 poses; (b1) the exact
  closed deficient square passes, 1e-9 smaller or shifted fails; (b4) each of the seven other images
  of E fails; a full orbit of holes needs all eight boxes; (b2) one box under `core` fails, under
  `orbit` passes with the statement about the union, fixed-image file relabelled is refused; (b3) a
  gate up to u = 1/2 leaves rows 2, 3 failing; seam and 45-degree gates; `mixed`; transport for the
  eight G.
* `engines`: 960 rows with random polygons, gates and cells in the three modes and three kinds:
  identical verdict, first failing cell and exemption of each of 1,434,840 deficient cells.
* `cli`: slices, `--merge` (incomplete, complete, other certificate, failed rows), `--restriction`,
  `--workers 2`.
* `fixed_real` (a): fin473a written image by image (43,300 sites, 9,132 features, 17,999 rows on
  [0, 1], budget equal to the published one). Rows 0, 3000, 8000 with the threshold at the row
  minimum + 1 and one box with the row's gate: `orbit` (one box), `core` (eight boxes), `fixed`
  (eight boxes) give identical verdict, minimum, cell count, deficient slabs, deficit minimum, both
  for a passing and for a cut box; the mirror row beyond 45 degrees agrees; `fixed` with the one
  box fails. E empty: rows beyond 45 degrees, the bridging row and the row ending at u = 1 pass with
  the minima of their mirror rows.

Speed (the build machine under load, CPU seconds of one process, fin473a image by image, 25-row slices,
exempt sets of entry A): no deficient cell 0.69 to 0.82 s per row (73 to 87 rows per minute per
core; this is the published `geometry()` + sweep). Threshold raised so that 4,760 to 9,300 slabs
per row are deficient: C13 (slot 13 with 843-digit coordinates and three marker images active)
1.00 s, C01 at both ends of the seam 0.96 to 1.06 s, `orbit` C00 / S13 1.04 s (57 to 62 rows per
minute per core). The exemption adds at most 0.25 s per row; `--audit` 3.7 s per row. Cores of a second machine
were measured earlier at one third to two thirds of a core of the build machine. A slice:

    python exact_restricted.py CERT.json --restriction exempt/A/C13.json --output s07.json --start 12600 --count 1800 --workers 4

## 9. Not proved, not covered, doubts

* Argued, not machine-checked: sections 3, 5, 6 are prose proofs. R2 and R3 are the published
  arguments re-read for phi in [0, pi/2]; the published checkers were only ever run on [0, pi/4].
  Evidence for the upper half: mirror rows reproduce the folded minima and cell counts exactly.
* One implementation. Until the Node twin exists a fixed-image PASS has one checker. The two
  engines share the forms, the parser and the published sweep, so they are not independent.
* Re-derived in the earlier code without finding an error: the similarity N = M W and K, the edge
  forms, the disc test, bounding boxes, the angle chart with its three lifts, the completeness of
  the deficient-cell listing, `orbit` / `core` logic, the cell selection argument. Not re-derived:
  the published `geometry` / sweep themselves.
* The symmetric shape still parses `L`, `A` and the rows with `Fraction(...)` as published (floats
  would be read exactly); the fixed-image shape refuses floats.
* `fixed` + `outside_cells` / `mixed` is implemented and tested on tiny instances only; with
  deficient cells in every slab the per-slab integer work is about 15 microseconds per polygon
  touching the slab (estimated several seconds per row at real size, not measured).
* Disc regions: reference engine only (slow with millions of deficient cells; refusal above 2^24
  runs per row). The skeleton's sets are polygons.
* No bonus / count form; no regions that depend on the angle or on the side; gates only as rational
  tan-half intervals; L = 4613/1000 hard-coded.
* The frame is taken on trust: the checker proves the statement for the stored E in the stored
  frame; that E is inside the theorem's windows is X5 of the skeleton.
* `--merge` trusts the `passed` flags of the slice files (it checks sha256 of certificate,
  restriction and the four checker sources, the row coverage and consistency of the flags).
* Not done: the acceptance run of a 300-row engine export (no export existed yet), any run
  on Linux / Python 3.11, any real fixed-image certificate.
