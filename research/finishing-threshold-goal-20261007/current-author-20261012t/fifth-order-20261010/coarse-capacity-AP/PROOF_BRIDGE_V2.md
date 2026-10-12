# AP: source-bound coarse capacity and its application (version2)

This is the updated file of record for the existing geometric lemma and its explicitly conditional application. It preserves the old proof and numerical constants. Earlier Z3 is a historical reading aid; its status and manifest timestamp are not current. The pure lemma is independently rechecked in REPORT_CAPACITY_LEMMA.md; this revised application prose still belongs in the final whole-proof review.
The source is coarse-capacity-R/PROOF.md, SHA256
bae9384411086b31ea5a547e40409409e3fd50b514da13078e0c189c3c227a28.
The source and its numerical tables are unchanged. The geometric lemma itself
needs only containment and pairwise interior disjointness. Its JG application
also needs the named marker, frame and loose capture premises below.

## Geometric statement, independent of all capture certificates

Let C=4675531/1000000, U=1169/250 and delta=(U-C)/2. Put any family of closed
unit squares with disjoint interiors concentrically in the side-U frame, with
actual container side <=C. Each of these whole centre regions has capacity at
most one, with arbitrary independent orientations:

| Region | x interval | y interval |
|---|---|---|
|3|[129/100,2993/1500]|[-1/2,1411/1000]|
|15|[19953/10000,26807/10000]|[1623/500,26/5]|
|17|[3775331/1000000,5199531/1000000]|[24137/10000,29637/10000]|

For17, clip to physical centre limits [delta+1/2,U-delta-1/2]. The diameter
squared is1851391155161/4000000000000<1. Distinct squares' open radius1/2
inscribed disks are disjoint, so distinct centres are at distance>=1.

For3 and15, the following wall-strip lemma handles independent orientations.
Suppose two contained centres have wall-parallel separation at most w and each
has distance at most H from the wall. If the two squares are interior-disjoint,
the separating-axis theorem provides a unit side normal of one of the squares.
After sign choices let its absolute components be a,b>=0, a^2+b^2=1, with b
normal to the wall, and put d=(a+b)/2. Its owner A has support1/2 along that
axis and support d against the wall.

If A is the nearer square, the centre difference normal to the wall is at most
H-d and the other square's support along the chosen axis is at least1/2. Thus

    aw+bH-bd >= 1.                                    (1)

If B is nearer, write h_B for its support. Separation and containment require

    aw+bH >= 1/2+h_B(n)+b h_B(e_y).

This does NOT assume B has A's angle. Write n=(cos(alpha),sin(alpha)) with
alpha in [0,pi/2] and vary B's independent angle phi over [0,pi/2]. The
function f(phi)=h_B(n)+b h_B(e_y) is positive and, between its absolute-value
breakpoints0,alpha,pi/2, satisfies f''=-f<0. Its minimum is at a breakpoint.
There its values are d+b/2 and1/2+bd. Their difference is

    (d+b/2)-(1/2+bd)=(1-b)(a+b-1)/2 >= 0.

Hence f>=1/2+bd, and (1) follows in this ordering too. Taking absolute normal
components only enlarges the projected centre bound. For mixed signs, reflection invariance of the support expression replaces alpha by pi/2-alpha modulo a quarter turn; the same two breakpoint values and their comparison apply. The two physical square orientations remain independent. This covers either owner, either ordering, endpoint
axes and tangencies.

Parameterize a=(1-u^2)/(1+u^2), b=2u/(1+u^2), 0<=u<=1. The positive
denominator times the strict failure of (1) is the quartic

    P(u)=(1-w)+(1-2H)u+4u^2+(-1-2H)u^3+(1+w)u^4.

For3 take w=2993/1500-129/100=529/750 and H=1411/1000-delta=2821531/2000000. For15 reflect the entire wall-strip argument in the top wall and take w=26807/10000-19953/10000=3427/5000 and H=U-delta-1623/500=2859531/2000000. These H values are distances from the actual outer allowed wall, not from the frame boundary. Smaller concentric containers only decrease the possible widths/depths. The128 cells subdivide u, the separating-axis direction; position and the other square angle were eliminated analytically. On every
one of128 equal closed rational subintervals all five Bernstein coefficients
of P are strictly positive. The smallest coefficients are respectively
634043429/125829120000 and43535731167/8388608000000. Thus P>0 for all u,
contradicting every possible separating axis. The table is exact arithmetic,
not orientation sampling or a numerical search. It proves the whole regions'
capacity, not merely that of smaller captured slots.

## JG application, conditional on explicit earlier premises

1. FRAME_MARKER and the frame-pair receipts, through FRAME_ASSIGNMENT, identify
   a unique parent in L9. In an off-wall branch x9>53/100.
2. AQ, the alternative low slot in each of L3,L4,L15,L17, is a subset of L9
   with x<=53/100. It therefore contains no physical parent. The accepted
   bound20 for each L row, with the occupied marker and high-first semantics,
   forces an occupant in its actual small slot S_k.
3. The physically clipped S3,S15,S17 lie in the whole coarse regions above.
   The geometric lemma now identifies the only parent in each whole region
   with that small-slot occupant. The clipped frame L17 is a subset of clipped coarse17: its left end18879/5000 exceeds3775331/1000000 by469/1000000, and the y intervals agree. Thus BOTH the FRAME_ASSIGNMENT L17 parent and the captured S17 parent are in coarse17; capacity one identifies them. Coarse17 reflects L9 with constantC; frameL17 usesU. Their uncut x intervals differ byC-U=-469/1000000. They are not silently equated. L4 supplies its own
   remaining loose factor and does not need a new coarse4 lemma.
4. In JG these actual parents pass the open gates |tau_k|<1/20. Therefore the
   two signed closed escape slots on each of their whole coarse regions
   contain no parent. A second square in such a slot is forbidden by coarse
   capacity; saying only “the chosen parent's angle is gated” would not suffice.
5. The other three literal C escape slots are AQ and the two L9 angular exits.
   AQ is already empty. Unique L9 and its current open gate exclude both old
   exits, including quarter-turn representatives: the rational lower gap is
   1/200000, the upper transformed gap974949/14197000000. Thus the entire X
   union contains no physical parent. Every accepted C budget forces its own
   target via the reviewed high-first score consequence.

The ten CURRENT classes_JD C files recut AQ's arc to
[613/2000,4197/10000]; this slot is not literally the old all-direction AQ
slot. The other eight escape geometries match the old files exactly. Step2
proves that the entire AQ centre polygon is empty, irrespective of angle, so
the recut causes no gap in this application. No claim that the two full X
unions are equal is needed. verify_readonly.py explicitly checks these current bytes without modifying the historical inputs or outputs. Historical R/RESULT.json C_escape_files_equal concerns old C_L files only and is not the binding for current classes_JD.

Only then are the targets simultaneously assigned and admitted to JG. The JG local contraction is not an assumption in any of steps1–5. FRAME_MARKER and FRAME_ASSIGNMENT are COUNTED in the pinned AP snapshot (0216de42...). The accepted marker class receipt/conversion is marker-import-AD/IMPORT.json. The conditional application still lists those premises explicitly; their present satisfaction is not a hypothesis of the pure lemma.

## Evidence and remaining review

The earlier manuscript, frame and join reviews independently derive the
wall-strip inequality. The frame review checks the128-cell exact parameters
and the coarse17 diameter and identifies the JG implication used above.
Those reports precede this supplementary argument and do not review this file.
Their accepted scopes and reports remain pinned. Independent acceptance of
this composition and its dependency links is a separate premise; these earlier
reviews do not supply it. The coarse-capacity argument uses the existing
charge certificates and local trees.

## Exact source of the label9 gate

The literal accepted PS_L01_T09.json (SHA256 cf863943c8ad07d46ec51c7211e89c366108e935329a22615ce0c2a11c2ddb7a) has T9 slot tan-half interval[a,b]=[-408817/1000000,61301/200000]. In the canonical first-quadrant chart, this closed slot and its quarter-turn lifts contain the exits t<=b and t>=(1+a)/(1-a). The latter endpoint equals591183/1408817 exactly. Its complement is therefore the OPEN gate (61301/200000,591183/1408817). These are derived from the slot, not arbitrary constants in a checker. The same gate appears in the accepted branch partition and b-case-g-producer/PROOF.md. The two C exit arcs end613/2000 and, in the negative quarter-turn chart, start-5803/14197. Their strict gaps are1/200000 and974949/14197000000 as in the exact replay. KEY_W's separate narrow admissible interval is used for branch elimination, not to redefine this gate.

## Wall cases and the limits of this application

The pure capacity lemma is valid without a case assumption. The JG application above is off-wall (x9>53/100); it is not a proof of all wall-case identifications. Their source is the accepted WALL_PARTITION loose-only interface (1af452ea...) and root-admission interfaces, as expanded in the current branch profiles.

- JQ: x9<=53/100, y9<=129/50. Its all-non9 target assignments are the accepted Q consequences and their distinct-parent profile.
- JPWS: x9<=53/100, 129/50<y9<=13/5. The loose labels3,4,15,17 use the OLD-through13/5 Q statements; rigid labels use PW, except label11 is placed by SL11_T020. Do not infer S_k occupancy from the L rows here, since AQ may be occupied. The profile has its own reviewed disjoint-capacity and marker/target12 identification.
- JPW13: x9<=53/100, y9>13/5. AQ is empty because it lies inside the unique L9 region and ends at13/5, strictly below its actual occupant. Thus L rows may force S3,S4,S15,S17 in this upper wall branch, followed by the same pure capacity lemma where needed. Rigid labels use PW and their reviewed joint assignment.

The wall seams have the ownership shown above. This clarifies where the arguments are used; no wall target, cap or root is widened.

## Frozen geometric dimensions

These exact regions, w and H are part of the theorem. No later region enlargement is licensed. The independent reader estimates failure after increases of about0.005 in w or H for regions3/15; those sensitivity estimates are not padding promises and are not used as proof. A proposed larger region requires new exact capacity/admission evidence. All128 intervals and endpoints are closed and strictly positive for the present dimensions.

## Scope and replay

ACCEPTED_INTERFACE_V2.json and PURE_LEMMA_SCOPE_V2.json carry the IDENTICAL pure geometric statement for any family of unit squares in the specified concentric container. The separate conditional_composition field contains the off-wall charge/identity application and does not enlarge what the fresh geometric reader reviewed. Old acceptance files remain immutable. verify_readonly.py prints a fresh report to stdout, with deterministic arithmetic fields; it never writes RESULT.json or INPUTS.json. The old check.py and replay.py are historical generators and must not be invoked in their pinned directories. The only optional output is shell redirection to a NEW file in this folder. No charge arithmetic or local tree is replayed.
