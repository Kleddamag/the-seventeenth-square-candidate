# Credits and sources

This work claims a candidate proof of optimality for the known packing of seventeen unit squares. It does not claim to have
invented the methods it stands on. This file says whose they are. If something is missing or wrong here, that is
an error of ours and we want to hear it.

## The result depends on these, or follows their idea

- **John Bidwell (1998):** the packing itself, found when he was an undergraduate at the University of Hawaii.
  It improved a packing found by Pertti Hämäläinen in 1980. It has no paper of its own that we know of; it is
  reported, as a private communication, in Erich Friedman, *Packing Unit Squares in Squares: A Survey and New
  Results* (Electronic Journal of Combinatorics, Dynamic Survey DS7), which is also our source for the problem and
  its history. Coordinates reconstructed from the drawing in David Ellsworth's catalogue *Squares in Squares*
  (kingbird.myphotos.cc/packing/squares_in_squares.html), which is based on the original compiled by Erich
  Friedman.
- **Thierry Gensane and Philippe Ryckelynck:** the first high-precision analytic description of Bidwell's packing,
  a system of four polynomial equations of degree 7 in the sines and cosines of the two tilt angles (*Improved
  Dense Packings of Congruent Squares in a Square*, Discrete Comput. Geom. 34 (2005) 97-109).
- **David Ellsworth:** the degree-18 polynomial of the side length (4 June 2023, confirmed independently the same
  day by Boris Alexeev), as recorded in his catalogue.
- **Joshua Levy and the squares project (github.com/jlevy/squares):** the charge method in its basic form
  (weighted covering, strict cores, event cells, threshold budgets, two-of-three atoms); the weighted certificate
  itself goes back to Sam Burns and Gustavo Massaccesi, whom the squares project credits. Further: the exact
  algebraic certification of the side L from our rational seed (two polynomials, layout formula, root
  certificate); the core stress and the local-minimum-modulo-sliders recipe (their records H-258, H-261, H-268)
  that our terminal step is built on; the parent-centre contract (first committed 10 September 2026), the prior
  work for the parent-side reduction; and the plan to follow, for n = 17, the three-part shape of the n = 11 proof.
- **Manasseh Ahmed (github.com/Queuingtheorydotcom), 11SquaresOptimal** (github.com/Queuingtheorydotcom/11SquaresOptimal): the proof shape
  (global exclusion, capture, local theorem; the local isolation theorem it uses is the squares project's). Its
  Lean formalization, 11SquaresFormalized, is a joint work of the people named in its ACKNOWLEDGEMENTS.md. What
  that repository says about its own sources (its README, section "Attribution", and
  its THIRD_PARTY_NOTICES.md): the packing is credited to Walter Trump; the exact construction and the local
  isolation theorem are taken from jlevy/squares at revision c55726e1e885227f63110131c0a914665175ff89; the
  reconstruction diagram is credited to David Ellsworth; no new licence is asserted. Its folder
  src/evidence/research/phase3/upstream-notices/ keeps the ATTRIBUTION.md and AUTHORS.md of this project's earlier
  work on eleven squares. Its manuscript cites Stromquist 2003.
- **Charges with a threshold.** The threshold atom in general form is defined in the squares project's record
  T-025 (the squares project; certificate first committed 9 September 2026, claim sheet 11 September), which uses it two-of-three.
- **Mira-acc / 17squares:** the weighted certificate for the lower bound 4.613 (its measure starts from Joshua
  Levy's 4.59 certificate) and the parent-aware certificate 18452/3999 (about 4.614153) in the same container
  4613/1000, the file our first certificates were built from. Our capture certificates still live in its frame.
- **Guzhou0806 (N17 project, github.com/Guzhou0806/n17-square-packing):** the angle catalogue, the
  parent-side reduction and the first exact JavaScript checker that ours descend from; and the continuation of our
  4.66001 charge to 4.66044275.
- **Semidefinite leaves:** the idea came from a write-up we were pointed to: Muhammad Maaz, *Proving
  polynomial inequalities with sum-of-squares certificates* (mmaaz.ca/writings/sostactic.html, 3 April 2026). The
  classical results behind the method: M. Putinar, *Positive polynomials on compact semi-algebraic sets*, Indiana
  Univ. Math. J. 42 (1993) 969-984; J. B. Lasserre, *Global optimization with polynomials and the problem of
  moments*, SIAM J. Optim. 11 (2001) 796-817.

## Context and earlier bounds

- **Trevor Green:** the lower bound for s(17) reported before 2026, (40*sqrt(2)+19)/17 = 4.4452 (Friedman's
  survey, Table 2 and Figure 34; private communication, 2000). The squares project records that the published
  argument for it is incomplete (its issue 308, October 2026).
- **Sam Burns and Gustavo Massaccesi (August 2026):** the first weighted-point lower bounds for s(17). Burns,
  *Proposing a Better Lower Bound for n=17 Square Packing* (sam-burns.com, 6 August 2026; s(17) >= 4.4811,
  certificate credited by him to ChatGPT). Massaccesi, *Another Better Lower Bound for n=17 Square Packing*
  (gus-massa.blogspot.com, 21 August 2026; s(17) >= 4.5058, which he marks "(?)", weights by linear programming,
  on Burns's certificate). Both are blog posts; there is no journal or preprint. Burns's 4.677648 arrangement
  (*n=17 Square Packing: A Near-Record Arrangement*, 5 August 2026) is a member of our second family of
  near-optimal packings.
- **The other lower bounds of 2026** (Kim Brandwijk, 89/20 = 4.45; David R. MacIver, 4.4502; Stanislav Fort,
  4.456575; anabologyco-maker, 4.5705; Joshua Levy, 4.59, the ancestor of Mira's 4.613) are listed in
  CONTRIBUTORS.md of Mira-acc/17squares and in packing/frontier/n-017.md of the squares project.
- **Walter Stromquist:** *Packing 10 or 11 Unit Squares in a Square*, Electron. J. Combin. 10 (2003) #R8, and the
  unpublished manuscript *Packing Unit Squares Inside Squares III* (1984), as listed in Friedman's survey.
- **Hiroshi Nagamochi:** *Packing Unit Squares in a Rectangle*, Electron. J. Combin. 12 (2005) #R37.
- **Wolfram Bentz:** *Optimal Packings of 13 and 46 Unit Squares in a Square*, Electron. J. Combin. 17 (2010) #R126.
- **Walter Trump:** the packing of eleven squares, as reported in Friedman's survey.
- **David R. MacIver:** the Center-Area Lemma (*The Center-Area Lemma*, author-hosted manuscript with a Lean 4
  formalization, 2026, github.com/DRMacIver/square-packing-research; not journal-published), and a lower bound
  s(17) > (40*sqrt(2)+19)/17 + 1/200 = 4.4502 (*A New Lower Bound for Packing 17 Unit Squares*, manuscript dated
  8 August 2026).
- **wand125 (Hiroaki Hosono, by his public profile):** certificates, a native kernel and an independent verifier
  for the squares project's sub-pattern exclusions.

As far as we know, no result in this section is a premise of the proof. They are named because they are the
history of the problem and because the squares project's records, which we did build on, cite them.

## What is ours

- The lower bounds 461300/99853 (about 4.6198), 4.640020, 4.66001 and 4.6601 (published September 2026) and their
  checkers: larger k-of-n, weighted and intersecting-subset charge rules. We make no claim that these general ideas
  were new. The bound 4.613 is not ours (see Mira-acc above).
- The cutting-plane / pricing engine that took the bound to 4.674 (unpublished) and the repair step.
- The capture stage: charge certificates per pose class, the marker that fixes the labelling, the frame, the
  decision list of eleven cases, the admission of every case into a root region.
- The window engine: the specification of the tree certificates, exact leaves including semidefinite ones, and
  two independent exact checkers.
- The terminal step at the actual side, on the squares project's endpoint polynomials and recipe.
- The join of all parts into one statement, and its audit.

## Who did the work

Marc Leonard Overbeck (ORCID 0009-0008-8607-8197) conceived and led the project: he set the goal, designed how the work
was organised and checked, and made the decisions about goal, organisation and release. The mathematics, the engines, the
certificates, the checkers, the reviews and the text were produced by AI systems under his direction and to his
instructions: **Codex (OpenAI)** for the published bounds, the terminal and local theorems, the capture audits and the
proof text, and **Claude (Anthropic)** for the engine from 4.661 to 4.674, the class statements, the window engine,
the join and the final audit. They are named here and are not authors.

## Software

HiGHS (highspy), Clarabel, SCS, numba, NumPy, SymPy, PySAT / Glucose4, Python `fractions`, Node.js BigInt.

## Not yet established

Open points of attribution that we know of:

- Who first used general k-of-m charges. As far as we found, it was this project's own earlier result for eleven
  squares, s(11) >= 31/8 (22 September 2026), which the row T-037 of the squares project's table of results records
  with the words "point and k-of-m threshold charges".
- Whether any final capture statement uses the squares project's cover cells as class regions.
- How much of the terminal contraction is new relative to their ratio test.
