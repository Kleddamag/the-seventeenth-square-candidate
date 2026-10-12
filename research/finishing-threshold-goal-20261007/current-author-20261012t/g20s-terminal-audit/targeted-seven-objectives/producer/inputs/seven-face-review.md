# Independent acceptance of the seven-face corollary

Accepted as a conditional cover and a finishing criterion. No face
infeasibility, new terminal theorem, capture theorem or optimality theorem
is established by this corollary.

The producer's file is `../SEVEN_FACE_COROLLARY.md`, SHA256
`eae7b83669a7506459d19a92b4ea2012cd1dd96401b267b58506493ef43ca116`.
The independent reviewer is `Codex`. This additive review
depends on the accepted five-round review manifest
`7d9db75869c3bc781ca3a08e892dd12d4c3e5f5140fae3f0577ff32ddee2a901`.

`check_seven_faces.py` reads the sealed final box B5 and checks its exact
rational endpoints. It does not rebuild any model or replay any dual.
The source defining the coordinates and the old candidate file are hash
bound to the accepted review.

The core is precisely `range(51)` with parameters `2,21,25` and dummy model
coordinates `6,7,37` removed. There are 45 core coordinates. Side coordinate
51, product coordinates 52 through 99, and the three unnormalized sliders
are outside the normalization. Thus neither the side's endpoint -1 nor a
slider/product endpoint creates an additional norm face.

The exact endpoint census gives

```
(8,+1), (14,-1), (15,-1), (41,-1), (41,+1), (44,-1), (49,-1).
```

All 45 core intervals lie in [-1,1], and all endpoints for the other 39 core
coordinates lie strictly inside that interval. The bound-coordinate maps
are correct: indices 8,14,15 are square 5 horizontal and square 8 horizontal
and vertical core displacements; angular index `34+(i-1)` gives square 8
at 41, square 11 at 44, and square 16 at 49. The special translational bases
of squares 11 and 13 do not change these angular identities.

For any physical point satisfying the existing normalized analytic
hypotheses, let `R=||h||∞` on exactly those 45 core coordinates. If
`0<R<=1/5000`, the normalized vector `x=h/R` has maximum absolute core
coordinate exactly 1. The previously verified necessary inequalities and
box updates put this same physical point in B5. Since a maximum of a finite
set is attained, one of its coordinates equals +1 or -1. The exact census
forces that equality to be one of the seven listed ones. Therefore B5
intersected with those seven closed faces covers every such normalized
nonzero physical core. No uniqueness of the selected face is needed;
intersections and simultaneous norm equalities must remain covered.

Consequently, separate valid infeasibility proofs for all seven face
relaxations suffice to rule out every `0<R<=1/5000` under these hypotheses.
This is a valid alternative to producing strict coordinate bounds for all
92 signed objectives of a contraction round. It does not promise that any
of the seven relaxations is infeasible or that one LP proposal per face will
succeed.

For a face certificate, its input box must be the actual B5 intersected with
the specified singleton. The physical normalized products still satisfy
`q=w*x_angle`. Recomputing their interval hulls from the face box is sound,
as is reconstructing the box-dependent error bounds using the accepted
kernel. Rows already valid on a broader box may also be retained, but one
cannot claim a tighter product or remainder bound without its valid
reconstruction. Subsequent updates, model digests and residual minima must
bind the correct current face box. An infeasible LP status is only a
proposal; the exact nonnegative-dual/box-residual contradiction must be
checked. A surviving relaxed face is not a physical packing witness.

The physical application retains one common frame and assignment of
sixteen distinct constrained roles, independent orientations, the full
seventeen-square packing, actual `S<=S*`, the padded slider ranges and all
other antecedents of the accepted analytic gate. Physical square 4 is
unconstrained by this terminal relaxation, not fixed or deleted from the
physical packing. The explicit actual-wall justification of lower `a>=0`
continues to be an antecedent when joining a larger tree box to this
terminal domain. The corollary does not discharge finite entry, tree-store
composition, or the common-frame capture problem.

The exact census used 0.004684 CPU-seconds.
No
solver, model replay, new geometric case or additional search was run.
