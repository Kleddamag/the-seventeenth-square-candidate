---
title: H-256 — exact n17 endpoint feasibility with interior sliders
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-256
  kind: hypothesis
  claim: The H254 reconstruction at the unique H255 root, using the fixed centroid of its slider triangle, is a feasible packing of 17 unit squares at the exact chart side.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: Complete exact identity and strict interval discharge of68 wall and 136 pair obligations, with fixed sliders, accepted root enclosure and all denominator/support guards.
    direction: Confirm only if all 15 wall identities,21 pair identities,53 remaining strict wall inequalities and115 remaining strict pair separations pass, synthetic controls pass and independent mathematical/code/output review finds no blocking defect. Failure of an enclosure or identity is unresolved endpoint feasibility, not a refutation of the root or global optimality. No slider adjustment, root refinement or alternative reconstruction is allowed in this round.
    threshold: Exact zero for declared identities; strictly positive lower interval bounds for all remaining obligations and branch/denominator guards.
  instrument: devtools.check_n17_endpoint_feasibility; exact symbolic identities and Fraction interval inequalities, to be independently reviewed and frozen before target use.
  instrument_ready: true
  regime: Existing Sympy for exact symbolic cancellation and standard-library Fraction intervals; one worker, no floating acceptance, no source-slider fitting, no root search and no new dependencies.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: One 20-minute controlled implementation/review slice; one target run capped at180seconds, one worker and10 MiB per output, followed by independent output audit.
  prereqs: [think-bj81, think-ndyz, think-r8ns]
  replication: false
  registered: '2026-10-01'
  notes: This is endpoint feasibility for Bidwell's known construction, not a new packing discovery or a global optimality proof. The H254 conditional minimum applies only within its declared orientation/branch/parameter class.
---
# H-256: Exact n17 Endpoint Feasibility

[H-255](H-255-n17-exact-polynomial-root.md) establishes a unique exact root of the two
contact-chart polynomials.
[H-254](H-254-n17-contact-chart-fidelity.md) supplies the reconstruction formulas and
contact table. This round tests whether those formulas produce an actual packing at the
root, including the two sliding squares.
The criterion is frozen before endpoint target arithmetic.

## Fixed Root and Sliders

Use the accepted
[exp-237 certificate](../series/series-000-smoke-and-calibration/results/exp-237-n17-polynomial-root/run-001/certificate.json)
retained at commit `7866e2623`, with its unchanged source midpoint, polynomials and
original radius. Validate that certificate using the separate H255 checker.
For geometric interval arithmetic use the coordinatewise box $m_i\pm\eta_i$ from its
accepted inclusion bounds.
Every fixed point lies in this box; using it is a consequence of the accepted proof, not
another root solve or radius trial.
Set $S=(6+4t)/(1+2t-t^2)$ and retain every H254 reconstruction formula.

For the two slider coordinates $a=\lambda_6$ and $z=\lambda_{13}$, define

$$
R=S-3/2,\quad H=V_{11}-1,\quad L_0=c+s/2+1/2,\quad
T=H+sR-L_0=c(c+4-S).
$$

The last identity follows from $F_1=0$ and $c^2+s^2=1$. Use the fixed triangle centroid

$$
a=R-\frac{T}{3s},\qquad z=H-\frac{T}{3}.
$$

Its three boundary clearances are $R-a=T/(3s)$, $H-z=T/3$ and $z+sa-L_0=T/3$. Require
strict positivity of $s,T$ and all reconstruction denominators on the entire root
enclosure, including $D,E,K,c,s,t,1+t$ and the positive normalization factors.
This choice is independent of the source slider values and is fixed without testing
alternative positions.

## Complete Geometric Obligations

Every square is represented by its centre and exact orthonormal basis from H254. Check
the rational identities giving unit length and orthogonality of the bases.
Retain positive support-branch signs $c,s,d,e,\alpha,\gamma$ and all denominators.
Each unit square has four wall support clearances, giving 68 obligations.
Each unordered pair has one nonoverlap obligation, giving 136.

1. Prove the 15 H254 wall-anchor clearances are identically zero.
2. Prove the 17 defining H254 pair-contact gaps are identically zero, and the three
   closing gaps equal $F_1,F_2,F_3$. Verify their exact identities and positive
   normalizations to the two H255 polynomials after substituting $S(t)$:
   $\Pi_2=t(1+t)(1+t^2)(1+b^2)F_2$ and $\Pi_3=(1+t)(1+t^2)^2(1+b^2)^2F_3/2$, while $F_1$
   vanishes identically.
3. Prove the additional 2/3 corner contact exactly.
   Its centres are $(3/2,1/2)$ and $(1/2,3/2)$, so the directed $2\to3$ gap along $e_y$
   is zero, as is the $3\to2$ gap along $e_x$.
4. Require strict positive interval lower bounds for the other 53 wall clearances.
5. For each of the other 115 pairs, require a strict positive directed separating
   projection gap along at least one axis in the fixed list
   $\pm e_x,\pm e_y,\pm u,\pm v,\pm p,\pm q$. Evaluate support radii with rigorous
   interval absolute values.
   Selecting the first successful axis from this finite list does not alter the
   geometry. In particular, the 14/16 pair needs the $q$ direction; omitting it would
   leave valid geometry unproved.
6. Check exact unique coverage: 15 plus53 wall obligations and21 plus115 pair
   obligations, with no missing, duplicate or extra labels.
   Record how each was discharged, every selected axis and exact interval endpoints.

An interval containing zero is not a proof of a contact identity or strict clearance.
Symbolic cancellation proves the contact identities; the accepted root equations then
make the closing gaps zero.
Inequalities use exact rational intervals over the whole root enclosure.
No numerical tolerance is an acceptance rule.

## Controls, Review and Limits

Before target evaluation, test signed interval multiplication, division with a
zero-denominator refusal, absolute-value bounds, exact rotated support sums and a
synthetic overlapping pair.
Test a deliberately displaced anchor/contact, a changed closing identity, missing or
duplicated coverage and a tampered root certificate.
Synthetic symbolic controls must not read the target certificate or source midpoint.
Independent Astra max reviews the identity derivations, all geometric coverage and the
code, then checks the retained target output before acceptance.

Commit the criterion, instrument and controls before the single target run.
Use one worker, a 180-second wall ceiling and10 MiB per output file, with an
optional1GiB data memory limit where supported.
Retain unsupported guards explicitly.
Report symbolic preparation, exact geometry, checker and orchestration costs separately.
No retries change the sliders, root enclosure, identities or acceptance thresholds.

An accepted result certifies a packing at the chart root and closes the endpoint
feasibility obligation.
Together with the reviewed conditional minimum, it establishes optimality only within
the stated necessary orientation/branch/parameter class.
Capture of split orientations, other contact branches and the global packing space
remains open.

## Accepted Result

[exp-238](../series/series-000-smoke-and-calibration/experiments/exp-238-h256-n17-endpoint-feasibility.md)
passes the complete frozen criterion.
Independent review confirms the exact endpoint packing, with the conditional minimum
attained in the stated class.
Global capture is not established.
The original pretarget record below is retained as provenance.

## Pretarget Review Record

Two Astra max reviews approved the centroid algebra, root-enclosure consequence,
identity roster and complete coverage before target evaluation.
The independent symbolic review checks both basis unit identities and orthogonality, all
wall and pair identities, closing normalizations and equality of the polynomial
coefficients with H255’s accepted system.

During instrument development, one synthetic coverage control evaluated the chart at
$(t,b)=(0.365,0.335)$, inside the broad H254 angle rectangle but distinct from the
frozen H256 source midpoint and root.
Its side-domain guard failed.
No source or root certificate bytes were read, and no criterion or slider choice was
selected from that control.
The control was moved to unrelated angles $(1/3,1/5)$ to keep the pretarget boundary
unambiguous. The actual H256 target remains unevaluated at this checkpoint.

The completed instrument passed nine synthetic controls, Ruff and BasedPyright.
A separate Astra max reviewer replayed the controls serially after the producer author’s
run: 25.61 seconds, with no target input reads.
Static review approved the complete identity and interval arithmetic, source binding,
exact coverage and root-only scope of closing-contact zero values.
Bounded decimal serialization handles long exact fractions without changing arithmetic
or relaxing input parsing; both per-number and full-output limits are tested.
No target measurement has occurred before this freeze.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
