# Wider-entry raw stop cuts exported

The exact coordinate transfer and composition with the independently
accepted larger-root stop theorem pass. On the complete guarded rational
entry, the exported necessary cuts are

```
b >= -213/25000,   b+z <= 49/2000,   z <= 33/1000.
```

The entry has29 position coordinates bounded by1/200,16 independent
rotation angles bounded by1/400 radians, and unpadded raw sliders
a[0,8/25], b[-1/20,1/5], z[-1/5,3/40]. It uses the same corrected p13,
reference axes and common actual `[0,S]^2` frame,16 distinct constrained
physical squares and the unrestricted but physically present square4.
Actual S<=S* is required. Every guard and exact reference centre/axis is in
`PRUNING.json`; these bounds must not be applied to larger or ungated boxes.

All45 root-core bounds are strictly below501/100000. The maximum is about
.0050000000000000435, and every slider reference error is below1e-15. The
root-a lower bound0 uses the actual square2 right wall; the other endpoint
checks use the exact transfer. The root's existing1e-12 parameter padding
is sufficient.

The composition retains the stronger exact root sum upper from
`T_upper/3+(14/100)*(501/100000)` and its derived z bound. After paying the
signed raw-reference errors, the exact margins to the exported cutoffs are
positive: approximately3e-6 for b,6.08568e-5 for b+z and4.38568e-5 for z.
The exact fractions are saved in `export-receipt.json` and `PRUNING.json`.

The WX-style local coordinate mapping is explicitly mathematical:
xi_(11,2)=-b, xi_(13,2)=z, xi_(2,1)=-a. Thus the equivalent rows are
xi_(11,2)<=213/25000, xi_(13,2)-xi_(11,2)<=49/2000, and
xi_(13,2)<=33/1000. This export makes no claim that a WX checker recognizes
these as a new step schema. Its angle guard is **radian1/400**, not
half-angle tangent1/400; consumer chart containment must be proved.

Accepted root-stop review:
`907071a795d42b92890da0a1894b3a9765635908caf2812044ade6d65d76056e`.
Its producer manifest is
`5a3aab61d2a5f5b08090fc4fc8e0ad67482007b06e370d0cbdc4db255cdf9ead`.
The exact raw-reference data are bound to the earlier accepted mathematical
interface review537811d9...; that earlier radius1/10000 theorem is not
silently extended here. The current entry proof/export await their own
independent review at producer freeze.

No optimizer, model assembly, symbolic system, tree, finite contraction or
new terminal reach was used or proved. The completed small exact-root
rigidity theorem remains separate, at root radius1/5000. These larger-entry
cuts are supplied to help the finite contractor reach it.

Preparation used .004026 CPU seconds. The first transfer calculation used
.022188; adding an explicit existing-interface hash assertion and replaying
used .021900. Exact composition/export used .003115. Including source reads,
metadata and sealing, the total was at most three CPU seconds.
