# G20S: position 0.20 x gate 0.10 with SIXTEEN labels and no hypothesis on the rattler (PLAN, nothing computed)

STATUS: PLAN ONLY. No run has been made; every number about feasibility below is from
terminal notes or floating-point searches. Nothing here is proved.

## Why

G20 (seventeen labels) needs the rattler inside a gate of 1/10, which no capture statement can supply (on the
known family at side S* the rattler turns between -0.1025 and +0.1302). G20F (rattler free) is expected by the
pilot to cost about 1e3 extra leaves, because in a seventeen-square tree the sliders reach the slider box of
H-plus-r015 only through a narrow-arc rattler. The other way: let the TERMINAL accept the wide slider box, so
that the tree needs no rattler at all. Then the hypothesis is on the sixteen constrained squares only, the
format is SPEC 2.5.1 and the two frozen 2.5.1 checkers apply.

## Chain

1. Terminal instance "box-wide" (Codex's terminal proof re-instantiated, two changed source lines as for
   box-relaxed): S <= S*, the 29 core position coordinates within r, the 16 angles within r/2,
   a in [0, 8/25], b in [-1/20, 1/5], z in [-1/5, 3/40]  =>  S = S* and all 45 core deviations vanish.
   Planned entry tube r = 1/200. Grounds for expecting it to pass (`terminal/TERMINAL_NOTES.md` 3.3, 3.4):
   the rigidity stage passed one-piece probes at b = 1/5, at z = -1/5 and at a = 2/5, and a combined box
   a [0, 2/5], b [-1/50, 9/50], z [-8/25, 1/16]; the whole chain passed for b up to 9/50 at r = 1/100; the
   relational stage needs roughly b_hi < 0.2303 - 4.9 r, i.e. 0.2058 at r = 1/200 (an estimate; only 0.006 to
   spare). Fallbacks if it fails: r = 1/250, or b_hi = 19/100 with the cut b <= 19/100 in the windows.
   Cost: a few CPU-minutes. Needs a review like `reviews/TERMINAL_REVIEW.md`.
2. Tree HW (sixteen labels, SPEC 2.5.1): window = core position radius 3/20, angle radius 101/1000 for all 16,
   xi_{2,1} in [-8/25, 0], xi_{11,2} in [-1/5, 2/25], xi_{13,2} in [-1/5, 1/10]; tube = entry tube of box-wide
   (core r, angles r/2, xi_{2,1} in [-8/25, r], xi_{11,2} in [-1/5, 1/20], xi_{13,2} in [-1/5, 3/40]).
   This is H-plus-r015 with the slider box widened to the cuts; H-plus-r015 had 555 nodes.
3. Tree G20S (sixteen labels, SPEC 2.5.1): window = the sixteen factors of G20 (position 1/5; xi_{2,1} in
   [-39/125, 0], xi_{11,2} in [-1/5, 1/5], xi_{13,2} in [-1/5, 28/125]; angle 1/10); tube = window of HW with
   the upper end of xi_{2,1} at 1/100. Same cover script as G20 (243 cells).
4. Theorem G20S: a packing with S <= S* whose sixteen constrained squares lie in the G20S window has S = S*
   and lies on the three-slider family. The cuts b <= 1/5 and z >= -1/5 are part of the window (they are in
   the capture side's regions 11 and 13 already).

Float evidence that the statements are true: `bigbox/truth/TRUTH_BIGBOX.md` Q7 (d): sixteen squares with the
two cuts, gates 0.10 to 0.15: nothing below S* found, equality set = the family with a up to 0.311, b up to
0.200, z down to -0.200. Without the cuts the statement is false (S* - 2.9e-4 at b > 0.2303, z < -0.2066).
Codex has an exact sixteen-square packing on the family at a = 33/100, b = 1/10, z = -1/5 (its
`padded-terminal/check_skeleton.py`), so a = 8/25 is inside what the family really reaches.

## What capture must supply for G20S, and the point about label 3

Sixteen statements in ONE frame: the square of region j in its G20 factor, j != 4. If the frame is fixed only
up to the mirror mx, the statement for label 3 reads "region 3's class or its mirror class", and the mirror
class is the rattler's place: it can be satisfied by the rattler alone. A count of two with gates is false
(the rattler turns). A centre-only count "two centres in region 3 united with region 4", with regions too
small for two centres each, locates both squares; region 3's then has free orientation and the tree must
take that ("G20S3": label 3 with a free arc, cut only where needed). Cost unknown; a float search for the
smallest side with label 3 outside its factor is prepared as a separate computation.

## Not decided

Whether to build G20F at all once G20S exists (seventeen labels stay necessary where square 4 bears load,
i.e. around the mirror image of Q's family, but that is a different window).
