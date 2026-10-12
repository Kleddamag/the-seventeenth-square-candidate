# R1/R2/S2: capacity of the actual coarse loose regions and JG exemption emptiness

This isolates the geometric lemma independently re-derived in the first frozen-manuscript review and premise reviews C and D. INPUTS.json binds those reports, the earlier small-slot argument, the legacy lemma, and the literal class files. The new exact replay uses 128 subdivisions and the physical cap C=4675531/1000000 throughout. The old 64-subdivision lemma is historical evidence, not the numerical table used here.

Let U=1169/250, delta=(U-C)/2=469/2000000. A packing of side at most C in the fixed concentric frame has every square above y=delta and below y=U-delta. Its centres lie in [delta+1/2,U-delta-1/2]^2. Define the closed coarse centre regions, with every orientation allowed:

| role | x interval | y interval |
|---|---|---|
| 3 | [129/100,2993/1500] | [-1/2,1411/1000] |
| 15 | [19953/10000,26807/10000] | [1623/500,26/5] |
| 17 | [3775331/1000000,5199531/1000000] | [24137/10000,29637/10000] |

**Lemma. Each whole coarse region has capacity at most one for independently oriented unit squares.** For 17, intersect with the physical centre box. The squared bounding diameter is 1851391155161/4000000000000<1. Every unit square contains its open disk of radius 1/2, so distinct packing centres have distance at least 1.

For 3 use the bottom wall and (w,H)=(529/750,2821531/2000000); for 15 reflect in the top wall and use (w,H)=(3427/5000,2859531/2000000). Here w bounds separation along the wall and H bounds each centre's distance from that wall. Suppose two such squares were interior-disjoint. The separating-axis theorem for squares supplies a side-normal axis of one of them. Taking absolute components n=(a,b), a,b>=0, a²+b²=1, the centre separation projected onto it is at most aw+b|dy|. Write d=(a+b)/2; its owning square A has supports 1/2 along n and d normal to the wall.

If A is nearer the wall, |dy|<=H-d, while the other square's support along n is at least 1/2. Separation requires aw+bH-bd>=1. If the other square B is nearer, separation instead requires aw+bH>=1/2+h_B(n)+b h_B(e_y). For B's independent orientation phi modulo pi/2, h_B(n)+b h_B(e_y) is a positive sine/cosine sum, concave between the absolute-value breakpoints 0,alpha,pi/2, where n=(cos(alpha),sin(alpha)). The endpoint values are d+b/2 and 1/2+bd; their difference is (1-b)(a+b-1)/2>=0. Thus h_B(n)+b h_B(e_y)>=1/2+bd, giving the same requirement aw+bH-bd>=1. No equality of the square orientations was assumed.

Put a=(1-u²)/(1+u²), b=2u/(1+u²), 0<=u<=1. Direct multiplication gives

 (1+u²)² [1-aw-bH+b(a+b)/2]
   = (1-w)+(1-2H)u+4u²+(-1-2H)u³+(1+w)u⁴.

On each of 128 equal closed rational subintervals, all five Bernstein coefficients of this quartic are strictly positive; RESULT.json stores them all and check.py recomputes them with fractions. Positivity excludes every separating axis, including all limiting axes and contacts, contradicting interior disjointness. This proves the lemma.

**Identification before using any local root.** FRAME_ASSIGNMENT provides one unique parent in L9. Off-wall it has x9>53/100. The alternative AQ of L3,L4,L15,L17 is contained in L9 and has x<=53/100, hence is empty. Each accepted bound20 and the occupied marker force its small slot S_k to be occupied. For k=3,15,17 that physically clipped slot is contained in its corresponding coarse region. The lemma therefore says: the WHOLE coarse region holds exactly one parent, namely the S_k occupant. L4 additionally supplies the fourth loose root factor. S17 is also contained in the original reflected frame L17, so the two identities coincide. The original frame L17 and coarse17 are different rectangles: coarse17 is shifted by -469/1000000 in x. Their identification is through S17 and capacity, not equality of rectangles.

**JG's entire low exemption X is empty.** The literal C files use three kinds of escape slots: two angular exits on L9, AQ, and the two signed ungated arcs on each of the coarse regions 3,15,17. AQ is empty. Unique L9 with the open current gate cannot lie in either legacy angular exit: the lower endpoint gap is 1/200000 and the upper quarter-turn gap is 974949/14197000000. Each whole coarse region now contains only its identified role. If those three roles obey their open gates -1/20<tau_k<1/20, neither signed closed escape arc can contain any parent, including all square quarter-turn representatives. Thus X is empty as a set of physical parents. The accepted C budgets therefore force their target occupancies. This closes the missing implication from the angle-defined JG case to the original occupancy-defined split.

The seven tilted cases already have genuine parents from the small slots; they do not need coarse capacity merely to define their direction tests. Coarse capacity remains required for the full JG implication and for broader/cut-trigger identification. This argument imports the accepted charge semantics and budgets, frame theorem and root admission; it neither replays their charge arithmetic nor proves final optimality.
