# Independent wider-entry transfer and guarded stop pruning

**Accepted guarded raw-entry pruning.** Independent reviewer `Codex`; entry producer `Codex`. The enlarged physical stop theorem was independently accepted by `Codex`, seal `907071a795d42b92890da0a1894b3a9765635908caf2812044ade6d65d76056e`. The frozen entry package is bound by producer seal `8bcad6ad407458f83bc412d20613d1c09c9e21a7791c7cd89fe4ec0814d37d1b`, and its accepted guarded export is `PRUNING.json`, SHA `0a2655c65353b67cfd22ba05b9e84208e9c03c6664c3900ff3f771326ae9eb34`. This separate record accepts exactly the reviewed claims.

The accepted theorem assumes a physical packing of 17 unit squares in `[0,S]^2` with actual `S<=S*`. Sixteen distinct physical squares in one common frame have roles1..17 except4; square4 remains present, contained and nonoverlapping, with unrestricted pose. Use the hash-bound corrected rational reference (including p13 shifted by `-T0*v13/3`) and own-reference axes for square11 and square13. Bound all29 core position coordinates by1/200 and all16 independent angle deviations by1/400 **radian**. Keep unscaled sliders `a in[0,8/25]`, `b in[-1/20,1/5]`, `z in[-1/5,3/40]`.

The independently reconstructed45-coordinate map places every core coordinate strictly below501/100000 and all three transformed sliders inside the corresponding10^-12 padded root box. The lower endpoint of exact-root a uses the actual right wall of square2 and `S<=S*`; it is not an unconditional box projection. Closed raw endpoints are included. The core excludes the three slider coordinates and the three unused square4 coordinates.

For square11/13, let `delta=p_raw-p_root`, and let `(u0,v0)` and `(u*,v*)` be the raw/root orthonormal axes. With sign s=-1 for square11 and +1 for square13, root-minus-raw slider error is

`e_w = s*v*.delta + s*h*(v*.u0) + w*(v*.v0-1)`.

This preserves the same w when bounding the difference; subtraction of two independent broad slider intervals would destroy the useful bound. All three slider errors have absolute value below10^-15. The independent interval implementation uses a10^-90 outward grid and imports no producer geometry module.

The independently accepted enlarged physical stop theorem supplies its stronger formulas at epsilon501/100000:

`b* >= -(17/10)*epsilon`,
`b*+z* <= T*/3+(14/100)*epsilon`,
`z* <= T*/3+(184/100)*epsilon`.

Then raw bounds are obtained by subtracting the appropriate signed error endpoints. They leave strict slack for the proposed raw conclusions

`b >= -213/25000`, `b+z <=49/2000`, `z <=33/1000`.

The independent exact slack is approximately3e-6,6.08568046e-5 and4.38568046e-5 respectively. The rounded root cut49/2000 alone would not justify transporting the same cutoff; the stronger T*/3 expression is essential.

For the accepted raw coordinate convention, `xi_(2,1)=-a`, `xi_(11,2)=-b`, and `xi_(13,2)=z`. Thus the cuts equivalently read `xi_(11,2)<=213/25000`, `xi_(13,2)<=33/1000`, and `xi_(13,2)-xi_(11,2)<=49/2000`. This is an algebraic coordinate translation only. It is not an assertion that a WX checker has a compatible certificate type, angle chart, or terminal-box join.

These guards stop at the declared raw entry. In particular a tan-half parameter bounded by1/400 does not satisfy the1/400-radian angle guard. Larger position boxes, broader slider ranges, ungated angles, inconsistent images or duplicate role assignments are not covered. The pruning theorem does not contract this entry into the1/10000 rational rigidity tube, establish zero core, or prove side equality/capture/global optimality.


## Independent review coverage

`check_transfer.py` starts from the accepted raw pose file and algebraic root enclosure, reconstructs the layout in separate rational interval code, and checks every one of45 coordinates. Its fine-grid bounds lie inside the producer's wider enclosures. `check_binding.py` then verifies all frozen entry and root-review files, the exact root/interface join, all guarded coordinate intervals, and every exact rational centre/axis inherited from the accepted raw reference. It recomputes the exported margins using the authoritative stronger rational upper bounds from the root review. It checks both the producer's signed error intervals and the independent, tighter error intervals against those same authoritative upper bounds.

All three forms of each cut—named sliders, zero-based indices, and local displacements—are checked algebraically. Eight corruption controls reject a wider position guard, tan-half angle semantics, duplicated physical role, replacement by the rational side cap, flipped b sign, an added finite-contraction claim, strengthened b cutoff, and omission of one closed coordinate guard.

The optional sufficient relative-half-angle gate is valid: for real t, `|2 atan(t)| <= 2|t|`; hence `|t|<=1/800` implies the1/400-radian guard. This is relative to the same stated reference orientation. The1/400 tangent bound is not interchangeable with the1/400-radian bound. No engine arc composition or checker compatibility is certified here.

The source/physical scope in the frozen producer PROOF and RESULT matches the accepted statement. In particular the proof does not assign the free square4 a dummy pose, merge physical parents, silently change the corrected13 chart, impose force assumptions, or replace actual algebraic side containment. No remaining analytic qualification is hidden in the machine export.

## Replay and cost

From the repository root:

```sh
python3 research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/finite-entry-stop-pruning/entry-review/check_transfer.py
python3 research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/finite-entry-stop-pruning/entry-review/check_binding.py 8bcad6ad407458f83bc412d20613d1c09c9e21a7791c7cd89fe4ec0814d37d1b
```

Measured checks: .007641 and .005445 CPU seconds. There were no failed executions, optimizer/model/SymPy calls, or source arithmetic replays of other packages. The existing root SAT proof is inherited through its independent seal, not rerun or claimed as new work here.
