Editorial copy. Line references refer to the original; exact changes are listed in EDITED_LINES_ROUND2.json.

# Class certificates ("thresholds per class"): statement and file format

This file is the specification for the engine (the window side) and
for both exact checkers (the reviewers). Nothing here is proved or built yet.

## 1. Statement

Data: a container side U (the certificate's target), pose classes C_1, ..., C_r (closed sets of
poses), a rational threshold t_c >= 0 for each class, and a rational `bound` b.
Define for every pose p of a unit square inside the container

    tau(p) = min { t_c : p in C_c }   if p lies in at least one class,
    tau(p) = 1                        otherwise.

**Statement proved by a class certificate:** for every family of closed unit squares with pairwise
disjoint interiors inside the square of side U (in the frame of the file),

    sum over the squares s of tau(pose of s)  <  b.

Proof from the certificate: the charge of a pose is at least tau(p) x Gamma (checked cell by cell),
the charges of a family sum to at most the budget M (the capacity argument of the plain
certificates, unchanged), and M < b x Gamma (checked).

Special cases:
- plain exemption "at most k - 1 squares outside E": one class E with t = 0, b = k;
- conditional count "N(M) <= N(T)" for seventeen squares (M, T disjoint): classes M with
  t = 1 + d and T with t = 1 - d, b = 17 + d (take d = 1/2: t = 3/2 and 1/2, b = 35/2). For a family
  of exactly seventeen squares the sum is 17 + d (N(M) - N(T)), so N(M) - N(T) < 1. (For families
  of other sizes the statement says something else and nothing false.)
- orbit count "at least m squares in O" for seventeen squares: one class O with t = 1 - e, b chosen
  so that 17 - e N(O) < b forces N(O) >= m, i.e. b = 17 - e (m - 1).

## 2. File format (extension of the restriction object `s17-restricted-v1`)

    {
      "schema": "s17-classes-v1",
      "symmetry": "fixed" | "mirror_x" | "orbit",
      "frame": {"unit": "unit_square", "center": ["1169/500", "1169/500"]},
      "bound": "35/2",
      "classes": [
        {"name": "M",   "threshold": "3/2", "slots": [ {"centre": {"polygon": [[x, y], ...]},
                                                        "angle_tan_half": [lo, hi], "label": "..."} ]},
        {"name": "T16", "threshold": "1/2", "slots": [ ... ]}
      ]
    }

- A slot is what it is in `s17-restricted-v1`: closed convex polygon of centres (rational
  coordinates as strings, frame as given) x closed interval of the tan-half angle, taken with all
  quarter-turn lifts of the angle (a square has four side directions).
- A class is the union of its slots, united with their images under the symmetry group of the
  file: `fixed`: nothing added; `mirror_x`: the mirror x -> 2 c_x - x (centre mirrored, tan-half
  interval [lo, hi] -> [-hi, -lo]); `orbit`: all eight images of D4.
- The certificate itself keeps the published shape (features, weights, budget_units,
  minimum_units = Gamma, row list). With symmetry `mirror_x` the charge need only be invariant under
  the mirror: features are listed image by image (the fixed-image shape), rows cover side
  directions 0 to 45 degrees with the WHOLE container (a fundamental domain of the mirror, because
  the mirror sends direction theta to 90 degrees - theta).

## 3. What a checker must verify (exact arithmetic)

1. Structure, capacities and budget as for restricted certificates.
2. `budget_units x q_b < p_b x minimum_units` for bound b = p_b / q_b (strict).
3. For every row (angle interval) and every cell of the arrangement: charge of the cell, in units,
   times q >= p x minimum_units, where p / q is the cell's required threshold R(cell):
   - let H = the classes with t_c > 1 that the closed cell x closed row interval MEETS,
     L = the classes with t_c < 1 that CONTAIN the whole closed cell x closed row interval
     (in one slot image; containment in a union of several slots need not be recognised),
   - R = max of t_c over H if H is not empty; otherwise min of t_c over L if L is not empty;
     otherwise 1.  (Classes with t_c = 1 are allowed and change nothing.)
   This is an upper bound of tau on the cell, so the check is conservative.
4. Report: status, the statement in words with the classes and thresholds, k is replaced by the
   bound, hashes of certificate, class file and checker, per-row minima and the number of cells
   decided by each class.

## 4. Soundness notes for reviewers

- tau uses the MINIMUM over the classes that contain p; the cell rule uses a number that is never
  below the maximum of tau on the cell (H before L). If a high class and a low class overlap, the
  statement gives the overlap the low threshold, the checker asks the high one there: sound.
- Closed sets throughout; a cell on the boundary of a low class is inside it only if the whole
  closed cell is; a cell touching a high class gets the high threshold.
- The frame of the file is concentric with the container of side U; for an actual packing of side
  S <= U the squares are placed in the frame by the shift (U - S)/2, as for restricted certificates.
