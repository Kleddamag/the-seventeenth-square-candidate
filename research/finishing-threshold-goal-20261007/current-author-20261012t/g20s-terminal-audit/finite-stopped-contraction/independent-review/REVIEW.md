# Independent review: finite stopped contraction, three rounds

**Accepted: a conditional partial contraction of the complete guarded finite-entry box. The target cube is not reached, so this package does not apply the tiny local theorem.** The producer was `Codex`; the independent reviewer was `Codex`.

The input is a packing of seventeen actual unit squares in `[0,S]^2`, with `S <= S*`, one common frame and an injective assignment of the sixteen constrained labels other than4. Physical square4 remains present and unrestricted. The exact corrected rational reference and raw coordinate conventions are those of the sealed rational-entry interface. The29 position core coordinates have absolute value at most1/200 and all16 independent radian rotations have absolute value at most1/400. Unscaled sliders are `a in[0,8/25]`, `b in[-1/20,1/5]`, `z in[-1/5,3/40]`.

The accepted raw stop theorem justifies `b >= -213/25000`, `z <= 33/1000` and `-b-z >= -49/2000` on this entire physical input. The three intervals and the full physical17 premise are essential. In particular the root-reference lower bound `-8517/10^6` is not silently substituted for the raw-reference bound.

## What was independently checked

`independent_model.py` constructs the rational centres, orthonormal axes, all four corners per square, moving slider bases, and the square13 `-T0*v13/3` correction directly from the packing JSON. It imports no producer module. The sparse polynomial engine was adapted from the separately reviewed wider-contraction auditor recorded in `adaptation.json`: only the48 slider-angle products remain, with100 total columns; shared quadratic and relation variables are removed. The ordinary finite model's radius-based parallel remainder is retained exactly.

At each incoming box it independently enumerates all152 directed SAT options, reconstructs the corner Taylor polynomials and their linear/curvature upper envelopes, wall rows, parallel alternatives, coefficient rounding loss, outward right-hand-side rounding and the four factored McCormick rows for each shared product. The analytic remainder lemmas and complete independent-angle/owner coverage are inherited from the hash-bound accepted full-gate and existing finite-kernel proof; the exact polynomial expansion, geometry, option decisions and resulting rows are newly reconstructed. No optimizer, producer `model`, producer `check` or producer `exact_dual` is called.

The first model has597 rows and the following two have761 each: **2,119 independently matched rows**. The increase is legitimate: negative quadratic coefficients use tangents at zero and at the interval midpoint, which coincide initially and separate after asymmetric contraction. Every model includes the new unscaled physical sum row. This is not acceptance by the old unchanged `uniform.check`.

For a saved objective `s*x_i`, each multiplier is checked as an exact nonnegative rational. With `d=s*e_i-A^T lambda`, the checker independently proves the signed lower bound

`lambda·rhs + sum_j d_j*(lower_j if d_j>=0 else upper_j)`.

It checks all92 distinct required objectives, including both signs of every one of45 core coordinates and the side coordinate, once per round. All objectives use the same incoming box. Updates are intersected simultaneously, rounded outwards on the1e-15 grid, and all48 product intervals are freshly computed from all four endpoint products. The outgoing box must be nonempty, contained in its incoming box and contained in the original guarded entry. All276 signed bounds and all456 SAT alternatives passed.

Nine explicit corruption controls reject a negative multiplier, a changed bound, a slider incorrectly substituted for a core objective, deletion or sign reversal of the stop row, root/raw lower-cut confusion, a stale product interval, a missing objective and a false terminal claim. These are tests of this audit interface; dropping a valid row is not asserted to be intrinsically unsound, but would no longer match this particular claimed model.

## Physical side join

The accepted exact root enclosure is checked directly against the rational reference, not inferred from a floating display or only from the square2 centre. It gives the positive exact margin

`Sref - S*_upper = 193463554918067413404931424579936481214129947147027426104376477 / 4000000000000000000000000000000000000000000000000000000000000000000000000000000`.

Hence `S <= S* < Sref`, and the model's side51 upper bound0 is valid. Independently, square8 has raw centre y `p8y+h15`; every oriented unit square has vertical half-support at least1/2. Its top wall gives

`S-Sref >= p8y - 1/200 + 1/2 - Sref > -1/50`.

Thus the entire model side interval is justified without assuming a scalar certified lower bound. All calculations and exact margins are recorded in `receipt.json`. Physical square4 is omitted from the relaxation only; it is still an actual square in the stop theorem and in the stated conclusion.

## Result and limitation

After three rounds the maximum position radius is exactly `2951564640979/10^15`, and the maximum angle radius remains `1/400`. This is larger than the required all45-coordinate `1/10000` bound. The accepted rational-entry theorem is therefore **not applied**.

The complete final box in `receipt.json` is a rigorously verified necessary condition for every packing satisfying the input guards. The small-entry theorem, exact-root rigidity theorem, global capture and optimality are separate and are not newly established by this pilot. No fourth round, model alteration or region investigation was performed.

The additive saved-bound check verifies15,25,25 strictly improved angle endpoints over the rounds. The remaining seven endpoints belong to8 negative,9 positive,10 positive,11 both signs,12 positive and16 negative. This does not establish the sole negative-angle11 normalized face of the small-terminal proof. The producer's suggestion of further rounds is a proposal, not an accepted prediction of closure.

## Cost and replay

Run `python3 research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/finite-stopped-contraction/independent-review/check.py` to replay the frozen audit. The script imports only the independent polynomial module and standard-library arithmetic; its process has a26-second soft/28-second hard CPU cap.

The full exact replay used3.569130 CPU seconds; preparation, saved-bound checking and sealing are separately recorded in `COSTS.json`. No failed execution or mathematical repair occurred. The producer's frozen manifest records5.4331 seconds before the final write, while final telemetry records5.439289; this harmless timing difference is preserved.
