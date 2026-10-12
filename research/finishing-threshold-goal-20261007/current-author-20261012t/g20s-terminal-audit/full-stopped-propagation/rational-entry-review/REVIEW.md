# Accepted rational-reference small-entry corollary

This corollary composes two independently accepted results: the original exact reference-transfer lemma (review seal `ab96060dce2f0e5b17006b52a9a8c0d7b70f6a94897c9dd0f013d9911cfbdd12`) and the newly accepted stopped exact-root rigidity theorem (seal `e5b0819966146f51aef3fae61feaaed0985e70379ed6eb180e6931c8e1f41570`). It needs no new contraction certificate.

Consider 17 contained, pairwise interior-disjoint physical unit squares in `[0,S]^2`, with actual `S<=S*`. In one common frame, assign the 16 labels other than4 to distinct squares. The remaining physical square4 is unrestricted in pose and remains present. Use exactly the corrected rational reference and coordinate map bound in `MATHEMATICAL_INTERFACE.json`:

- Generic centre coordinates are Cartesian displacements from the rational reference centre.
- Square2 has centre `p2-a*(1,0)+h3*(0,1)`.
- Square11 has centre `p11+h20*u11-b*v11`.
- Square13 has centre `p13_corrected+h24*u13+z*v13`, where `p13_corrected=p13_file-T0*v13/3` and `T0=c0*(c0+4-Sref)`.
- Each constrained square has its own independent radian rotation from its rational reference axes. Angles are taken modulo a quarter turn with the stated small representative.

Suppose every one of the 45 core coordinates has absolute value at most `1/10000`, while

`a in [0,8/25], b in [-1/20,1/5], z in [-1/5,3/40]`.

The core contains29 position coordinates and16 radian angle coordinates. It excludes unscaled slider indices2,21,25, the unused square4 indices6,7,37, and any side or lifted-product coordinates. Thus the hypothesis does not make the slider magnitudes small or constrain square4.

**Conclusion:** every exact-root core coordinate is zero and the actual side is `S=S*`. Zero rational-reference core is not asserted.

## Composition proof

The prior transfer review was read together with its independent interval implementation. It reconstructs every centre, both changed orthonormal bases, and all16 orientation shifts from the accepted algebraic root enclosure. Its complete45-coordinate result is

`max |h_exact| < 1/10000 + 10^-15 < 1/5000`.

It encloses the transformed sliders in

`a* in [0,8/25+10^-12]`,
`b* in [-1/20-10^-12,1/5+10^-12]`,
`z* in [-1/5-10^-12,3/40+10^-12]`.

The lower endpoint `a*>=0` is a physical semantic cut, not a consequence of blindly transforming a box. Indeed the exact square2 x coordinate is `S*-1/2-a*`; its unit-square horizontal half-width is at least1/2, so its actual right wall and `S<=S*` imply `a*>=S*-S>=0`. The rational reference also satisfies the previously checked strict inequality `S*<p2x+1/2<Sref`. A larger rational side cap is insufficient for this wall repair.

The accepted exact-root rigidity theorem applies to the same physical assignment and independent rotations after this coordinate change. It gives zero exact core and `S=S*`. No finite propagation is needed because entry into this tiny raw cube is a direct hypothesis. It is not assumed to follow from numerical closeness in side.

`check_corollary.py` checks both frozen acceptance manifests and all listed reviewer file hashes, equality of the original and current rational source files and accepted root enclosure, the exact transfer bound, all three padded parameter inclusions, and the full45-coordinate roster. It exports every constrained rational reference centre/axis exactly and the pose formulas into the mathematical interface. No producer geometry code, optimizer, symbolic checker or new arithmetic chain is run. The established transfer arithmetic is inherited with its hash-bound proof, not represented as a fresh replay.

## Interface and limitations

`MATHEMATICAL_INTERFACE.json` supplies two accepted mathematical scopes: the exact-root radius`1/5000` theorem, and the rational-reference radius`1/10000` corollary. It records all roles, independent radian angle semantics, source hashes, actual-side premise, full17/free4 condition, sliders, index map and conclusions. It is not a new WX certificate format or a declaration that any existing tree's terminal box satisfies this interface.

In particular the position`1/200`, angle`1/400` entry is still unproved by this package. An HW/G20S tree must establish this tiny cube or pass a separately checked finite contraction and exact physical join. Global capture, common-frame assignment, the broader G20S input slider cuts, and classification of the expanded equality family remain separate obligations.

## Replay and cost

```sh
python3 research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/full-stopped-propagation/rational-entry-review/check_corollary.py
```

Measured check: .003238 CPU seconds. No failed executions occurred.
