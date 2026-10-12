<!-- P001 -->
# A candidate certificate proof for packing seventeen unit squares

Marc Leonard Overbeck

The mathematics, the certificates, the checkers and this text were produced by AI systems under his direction and to his instructions (Codex, OpenAI; Claude, Anthropic); see CREDITS.md at the root of the edition.

<!-- P002 -->
Let s(17) be the infimum of side lengths of an axis-parallel square containing seventeen closed unit squares with pairwise disjoint interiors. Their orientations are independent. Tangencies, zero clearances and unused contacts are allowed. We use no stress assumption or claim that scalar numerical proximity implies geometric proximity.

<!-- P003 -->
**Theorem with explicit certificate hypotheses.** Assume the 210 listed obligations, fifteen of which are the mathematical premises named below [file:OBLIGATIONS], with the literal identities, hypotheses and implications specified in this text. Then seventeen unit squares fit in a square of side L, and for every S≥0, existence of such a packing in [0,S]² implies L≤S. In particular s(17)=L. **Scope disclaimer:** uniqueness of an optimal packing is not claimed.

**Status.** This is a conditional composition of those implications. The component artifacts have been checked within the project and accepted in their original scopes; acceptance of an implication does not assert that its antecedents have been proved. No acceptance of the complete assembly by an outside reader is asserted here. This text does not itself certify its imported premises or issue independent acceptance of the complete assembly; that assessment remains required.

<!-- P004 -->
Evidence references of the form [file:GLOSSARY] denote the concrete objects bound in the companion label table. A physical parent is one of the original unit squares. A charge inner core is strictly inside a parent; the rigid-layout core is a vector of position and angle deviations. An all-direction marker and a half-marker are different pose sets. Internal symbols and object names are defined in [file:NOTATION].

<!-- P005 -->
The global implications used are [premise:ALGEBRAIC_ENDPOINT], [premise:UPPER], [premise:ENDPOINT], [premise:CHARGE_SEMANTICS], [premise:FRAME_ASSIGNMENT], [premise:C7_C8_TRANSFER], [premise:WALL_PARTITION], [premise:ROOT_ADMISSION], [premise:SELECTOR_LOGIC], [premise:LOCAL_CHECKER_SOUNDNESS], [premise:LOCAL_CERTIFICATE_IMPORT], [premise:G20S_PHYSICAL], [premise:WALL_CONTRADICTION], [premise:KEY_W_ELIMINATION] and [premise:COARSE_LOOSE_CAPACITY]. Each is used only with its stated hypotheses. Charge semantics here means the minimum-containing-threshold statement in Section 3.

<!-- P006 -->
## 1. The exact endpoint and an attained upper bound

<!-- P007 -->
Put t0=362043893314323383453621978739944164218293243036741520638379/10^60 and b0=330948674722739910429808533282915634174672003999685385633441/10^60. The accepted algebraic root gate gives a unique simultaneous real root (t,b) in the closed radius-10^-12 box about (t0,b0) of

<!-- P008 -->
F = t-3t²-t³-t⁴ + (1-t-t⁴+t⁵)b + (-3t+t²-t³-t⁴)b²,
    G = -2t³-2t⁴ + (-1+3t-4t²+t⁴+t⁵)b
        + (4-2t-2t²+2t³-2t⁴)b²
        + (-1-5t+4t²+t⁴+t⁵)b³ + (2t+2t²)b⁴.

<!-- P009 -->
Define L=(6+4t)/(1+2t−t²). The denominator is positive on the uniqueness box. The tight rational enclosure in [file:ENDPOINT_CASES] is separately established by [file:ENDPOINT_REFINEMENT], which proves a radius-10^-58 box inside the named tight root and side intervals. The upper-construction replay in [file:UPPER_ENDPOINT] instead proves a wider radius-10^-50 root box. That wider refinement already proves L<R<C<U; the radius-10^-12 uniqueness box alone does not prove L<R. The tight-enclosure check adapts the earlier Banach construction; it is not an independently implemented second proof. It also checks that the F and G definitions in [file:ENDPOINT_STATEMENT] equal the pinned polynomial data.

<!-- P010 -->
L < R=4675530093604551/10^15 < C=4675531/10^6 < U=1169/250.

<!-- P011 -->
Numerically L=4.675530093604550951634…; R exceeds it by approximately 4.8366×10^-17. The strict inequalities and the full rational enclosures in [file:ENDPOINT_CASES], certified by [file:ENDPOINT_REFINEMENT], rather than the displayed decimal approximations, are the premises. The separate enclosure-use audit [file:ENDPOINT_ENCLOSURE_AUDIT] distinguishes wide-input geometric checks from the retained tight-input local arithmetic. No scalar lower-bound certificate is assumed in this argument.

<!-- P012 -->
All seventeen centres, side directions and auxiliary formulas of an upper construction are given in [file:UPPER_FORMULAS] and [file:UPPER_LAYOUT]. Put c=(1−t²)/(1+t²), s=2t/(1+t²), d=(1−b²)/(1+b²), e=2b/(1+b²). Axis squares have basis ((1,0),(0,1)); the six theta squares have basis ((c,s),(−s,c)); the beta square has basis ((d,−e),(e,d)). These bases are orthonormal by rational identities. For capture labels 1,…,17 the construction labels are (1,5,2,6,3,7,4,8,9,10,11,12,13,14,15,16,17). These identify positions in the pattern, not equality of rational reference poses with an algebraic family member; the construction specifies its own sliders and pocket-square position.

<!-- P013 -->
The two construction slider coordinates are fixed before checking: with R0=L-3/2, V11=2c+(c²-s²)/2-1, H0=V11-1 and T=c(c+4-L), put a=R0-T/(3s), z=H0-T/3. These are `lambda6` and `lambda13` in [file:UPPER_FORMULAS]. Their three stop clearances are T/(3s), T/3 and T/3; the interval guards give s,T>0. No sampled choice of sliders is used in this construction.

<!-- P014 -->
For an orthonormal square basis (u,v), support in direction n is h(n)=(|n·u|+|n·v|)/2. Containment is equivalent to nonnegative clearances from the four wall supports. Two squares have disjoint interiors if a directed separating axis n satisfies (p_j−p_i)·n−h_i(n)−h_j(n)≥0. The construction in [file:UPPER_FORMULAS] has 68 wall and 136 unordered-pair obligations: 15 identity walls, 53 strict wall bounds, 21 identity pairs and 115 strict pair bounds. The identities reduce to F=G=0; the strict bounds hold throughout its rational root enclosure. Thus every actual root in that enclosure yields a feasible packing, and uniqueness supplies the designated one. This proves s(17)≤L. Its construction arithmetic is imported, not newly replayed by this manuscript. [file:UPPER_CONSTRUCTION_CHECK]

<!-- P015 -->
The primary upper-bound evidence [file:UPPER_ENDPOINT] constructs another specified member of the same family, checks all 68 walls and 136 unordered pairs, and independently isolates the same root. Equality of the defining polynomials, rational midpoint and uniqueness box identifies its side with L. Its separations comprise 53 strict and 15 identity walls, and 112 strict, 22 rational-identity and 2 root-identity pairs. These counts pertain to this member. This establishes an attained packing at L and s(17)≤L. [premise:UPPER] The import checks pins, root identity, saved strict interval signs and complete rosters; it does not claim a new support-arithmetic replay.

<!-- P016 -->
## 2. Normalization at the algebraic endpoint

<!-- P017 -->
Suppose, for contradiction, that a packing exists at a side S0<L. Put d0=(L-S0)/2>0 and translate every physical square by (d0,d0). The resulting packing K lies in [d0,L-d0]^2. It remains strictly inset from all four walls of [0,L]^2 after any one common dihedral symmetry of that container.

<!-- P018 -->
Capture coordinates are in the fixed concentric frame F_U. If p was an original centre, then

<!-- P019 -->
p+(L-S0)(1,1)/2+(U-L)(1,1)/2 = p+(U-S0)(1,1)/2.

<!-- P020 -->
Thus endpoint normalization changes none of the F_U poses. In particular it preserves all polygon memberships, angular memberships, counts and identities of physical parents simultaneously. The proof below may therefore work at actual side L. R and C are bounds for particular checkers; neither is substituted for L in the final physical rigidity theorem.

<!-- P021 -->
This normalization applies to every S0<L. It requires neither an optimal minimizer nor a lower-bound threshold, stress assumption or contact graph. [premise:ENDPOINT]

<!-- P022 -->
## 3. Class budgets and physical square counts

<!-- P023 -->
A class file specifies finite unions of closed convex centre polygons and closed tan-half-angle intervals, with declared symmetry images and square quarter-turn representatives. For a physical pose p define tau_D(p) as the least threshold among the classes of D containing p, or 1 if there is none. This is the literal score printed by the receipts. It is different from tau_k, which later denotes a role's tan-half-angle.

<!-- P024 -->
**Class-row lemma.** Fix a validated certificate with scaled container side L_cert, parent side A_cert, nonnegative integer feature weights, budget M and positive charge scale Γ. Fix a declared centre c, closed pose classes E_j with their prescribed symmetry images and quarter-turn representatives, nonnegative rational thresholds t_j and bound β. Put τ(p)=min{t_j:p∈E_j} when this set is nonempty, and τ(p)=1 otherwise. A fully checked row with angle interval I gives, for every contained unit-square pose with direction in I and every checked cell whose closure contains its centre, a cell level dominating τ(p) and a closed core inside the open physical parent with charge at least Γτ(p). A complete valid row cover therefore gives, for every finite family of contained unit squares with pairwise disjoint interiors in the side-C=L_cert/A_cert square centred at c,

<!-- P025 -->
Γ Σ_p τ(p) ≤ Σ_p χ(K_p) ≤ M < βΓ.

<!-- P026 -->
Thus Στ<β. Different physical parents may use different rows of the complete cover; a single row covers only families whose directions it contains. Closed position and angle boundaries, independently oriented squares and touching parents are included. Authentic complete execution on the bound inputs and sound exact arithmetic are hypotheses of this implication. [file:CLASS_ROW_LEMMA] [file:CLASS_ROW_SOURCES] The independent derivation of record is section (2) of [file:CHARGE_CORE_DERIVATION], with the source-audit and finite-test limits stated there.

<!-- P027 -->
**Capacity of features.** A threshold feature with positive coefficients a_j and threshold k fires on at most floor(Σa_j/k) disjoint cores, because each site occurs in at most one core. Nonempty winning masks with pairwise nonempty intersection have capacity one. Summing with nonnegative integer outer weights yields the recomputed budget M; point weights are singleton capacity-one features. This bound has no square-count hypothesis. Fixed/mirror and orbit validation, including weight nonnegativity and the used symmetry invariance, are part of [file:CLASS_ROW_SOURCES].

<!-- P028 -->
**Row validity and symmetry.** The endpoint tests give a positive core-containment margin throughout the angle interval: cos δ+|sin δ| increases with |δ| on [0,π/4]. Concavity of cos φ+sin φ places every legal centre in the closed row envelope, which has nonempty interior. Fixed rows cover a quarter turn and folded rows cover beyond π/4. For a reflected row, reflect the pose into the checked row and reflect the selected core back into its original parent. The feature potential and class unions are invariant under that symmetry. Disjointness is required for the original physical parents, not for their separately reflected images.

<!-- P029 -->
At a boundary centre choose generic envelope-interior centres converging to it in one checked adjacent cell, avoiding the finite arrangement edges and degenerate atoms. Pass to a subsequence with constant site-hit pattern. Every hit persists in the closed limiting core, which remains strictly inside its physical parent. Monotonicity of the original Boolean features yields χ(K_q)≥m(Q). Limiting cores of distinct parents are disjoint even when their squares touch. Signed Möbius atoms are an evaluation device; their individual monotonicity is not required.

<!-- P030 -->
The cell threshold r uses the largest meeting high threshold if any high class meets the closed centre-cell times parent-angle row; otherwise it uses the least low threshold whose single closed slot contains that entire product, or 1. For every pose p in that product, r>=tau_D(p). If a high class meets, r>1 dominates any low containing threshold and is at least every containing high threshold. Otherwise any recognized low class actually contains p, so minimizing over recognized lows cannot decrease the minimum over all containing classes. If none is recognized, r=1 is still at least tau_D(p). These comparisons include boundaries. Failure to recognize a union of partial low slots is conservative.

<!-- P031 -->
**Sweep arithmetic and strictness.** The Möbius expansion evaluates the original features exactly on generic cells, and the sweep covers a superset of all cells meeting the row envelope. Exact geometry, complete cell partitions and the checked absolute atom bound <2^50 make the bounded integer sums exact. For every checked cell, m(Q)≥Γr is tested by exact cross-products. All inequalities up to the final budget are weak; the strict step is the integer test Mq_β<p_βΓ for β=p_β/q_β. One integer unit of surplus is sufficient; no numerical margin or rounding assumption intervenes in this strict integer comparison. The eight named one-unit receipts are rechecked in [file:ONE_UNIT_SURPLUSES]; this does not replace their full exact executions. [file:CLASS_ROW_SOURCES] The selected Node data also meet the finite index-size safeguards: at most 83,128 sites, 166,260 entries per coordinate array, and a midpoint index sum at most 524,288<2^31. Cell counters can exceed 2^31; their all-row upper bound is 497,556,991,458,000<2^53 and they are not used in the signed midpoint shifts. These data-specific bounds supplement the charge-magnitude bound; they are not a universal guard for future inputs. [file:INDEX_SAFETY]

<!-- P032 -->
For every packing of seventeen unit squares in the declared concentric side-C frame, the named complete receipts give Σ_i τ_D(p_i)≤M/Γ<B. Each physical parent is counted once. All selected executions have C=4675531/1000000 and centre (1169/500,1169/500), with L_cert/A_cert=C and agreement between both receipt statements. The same inequalities hold for an actual side S≤C by concentric containment, with all physical poses and memberships unchanged. [file:LITERAL_STATEMENTS] binds the literal score, class bytes and both receipts for 98 executed inequalities; C7 and C8 are additional derived occupancies, not executed score rows.

<!-- P033 -->
For each selected bound-20 or bound-23 implication whose literal file has only thresholds 4 and 0, suppose the asserted target is empty. Its contextual low alternatives WC, AQ or X are empty by the applicable identities and gates. Every parent then scores 1 or 4. An occupied marker gives a total at least 20; an occupied marker and a distinct occupied trigger give a total at least 23. This contradicts the corresponding strict printed bound. For label 12, the marker-minus-target cover places the actual marker parent in the high class when its target is absent. This proves target occupancy. Distinctness follows separately from the complete target-profile geometry; no stronger high-first score is required.

<!-- P034 -->
The three frame pair files have high threshold 5/4 and low threshold 7/8, with strictly disjoint high and low centre unions including the reflection images. Their minimum score is therefore exactly 17+N(high)/4−N(low)/8, counting a parent once even if it lies in several high slots. The orbit marker has a zero class and score 17−N(marker orbit). These are the score identities used below. [file:FRAME_SEPARATIONS]

<!-- P035 -->
Execution provenance is separate from the row lemma: merging agreeing slices does not replay their arithmetic or authenticate them. In particular, merge trusts the stored Boolean row decisions after structural checks; it does not re-derive those decisions from each row's recorded minima and class thresholds. Checking such recorded decisions separately is still different from replaying the cell geometry and charge sweep. Required inputs are authentic stable-source executions on the bound certificate and class bytes, complete row coverage and the strict integer budget. All 98 executions used have complete interval partitions without overlapping ranges. The class argument supplied to a checker, rather than an embedded top-level class value or a short statement name, fixes the score statement. [file:RECEIPT_ROSTER] [file:EXECUTION_BINDINGS] Capacity of capture targets, assignment to distinct physical labels and admission to local roots are separate obligations. The receipt assessment re-decided saved exact row summaries and budgets of the 98 folders and replayed selected rows through both engines. That assessment is not a fresh full sweep-arithmetic replay of every one of the 1,728,000 rows per implementation. Its stated scope and authenticity limitation remain in force. [file:RECEIPT_ASSESSMENT]

<!-- P036 -->
A class-byte alias is permitted only between valid strict-parsed files with the same full typed JSON value, without duplicate keys, nonfinite values, float substitutions, Boolean/integer coercions or omitted fields. The concrete aliases here are 90 single final-newline removals, two exact JSON serializations and six byte-identical files. Marker schema conversion is a separate pose-union equivalence, not an alias. [file:CLASS_ALIASES] [file:MARKER_CONVERSION]

<!-- P037 -->
The Python source hashes in each slice header are computed from files on disk when header() is called after the row loop; merge calls header() again for the merged record. They do not attest modules already loaded into that process or rule out an unrecorded external writer during execution. Authentic execution on the pinned stable checkout is an explicit provenance assumption, not a mathematical property of the recorded hashes. The Node implementation [file:CLASS_NODE_CHECKER] provides load/end source binding. Neither a current disk hash nor two agreeing summaries removes those execution hypotheses for either engine or any slice. [file:CLASS_PYTHON_CHECKER]

<!-- P038 -->
## 4. One frame and distinct physical parents

<!-- P039 -->
The four frame inequalities use their literal symmetry unions: FRAME_MARKER takes all eight D4 images at threshold0 and bound17; FRAME_0506 reflects each class in x→U−x, with BOX threshold5/4, W0/E0 threshold7/8 and bound137/8; FRAME_1114 uses that reflection with HEX threshold5/4, IW/IE threshold7/8 and bound137/8; FRAME_0917 reflects the three threshold5/4 high unions (HEX and both bonus unions) and the threshold7/8 L9/L17 union, at bound145/8. All slot directions have their quarter-turn lifts. Identity-only classes are not the statements used here. [receipt:FRAME_MARKER] [receipt:FRAME_0506] [receipt:FRAME_1114] [receipt:FRAME_0917]

<!-- P040 -->
The orbit-marker inequality forces one of its eight images occupied. Apply the inverse dihedral image to the whole packing. The hexagonal marker is reflection-invariant, so one further common reflection puts the same occupant’s side representative in [0,π/4]. The endpoint ρ=207107/500000 covers that interval because (1+ρ)²>2. The marker has squared bounding-box diameter 493/1250<1, so its capacity is one by the inscribed open disks of unit squares. The class and exempt marker descriptions have the same closed pose union, orbit and frame. [file:MARKER_CONVERSION] [premise:FRAME_ASSIGNMENT]

<!-- P041 -->
For each of pair05_06 and pair11_14 let m be the number of physical parents in its marker high class, t the number in its low union, and q the number in both. The strict disjointness of the high and low unions gives q=0 first; in this half frame the printed minimum-score inequalities therefore give 17+m/4-t/8<137/8. Since m>=1 and all counts are integers, each low union contains at least two parents. Those unions are the two bonus unions in the pair09_17 statement; the exact separations ensure they and the marker supply at least five distinct high parents there. Here h counts the distinct high parents in pair09_17, and N(V) counts physical parents whose centres lie in V=L9 union L17, each once. Its inequality17+h/4-N(V)/8<145/8 forces N(V)>=2. After the capacity bound N(V)<=2, the last inequality also forces h=5 exactly. Physical clipping gives capacity one for each of these two disjoint components. Hence both have exactly one actual parent.

<!-- P042 -->
Thus L9=[−131/250,4501/5000]×[24137/10000,29637/10000] has a unique parent distinct from the marker and L17. This identity is retained through the remaining cases. It is the frame assignment just proved, not a seventeen-way assignment of coarse cells. [premise:FRAME_ASSIGNMENT]

<!-- P043 -->
For each branch, if all target occupancies hold, its targets admit a simultaneous distinct-parent labelling in the associated local root. The selected exact capture statements supply these occupancies for every hypothetical smaller packing in the corresponding case. Label 4 remains a physical square even when the terminal rigidity statement does not constrain it. [premise:ROOT_ADMISSION]

<!-- P044 -->
Every unit square contains its open disk of radius 1/2, regardless of orientation. Centres of distinct physical parents therefore have distance at least 1, so a centre region of diameter <1 has capacity at most one. Clip the source polygons of a fixed branch to the physical centre box in F_U. The three selected wall profiles each have seventeen capacity-one target regions and all 136 cross-label pairs strictly disjoint, including their boundaries. If all targets are occupied, no physical parent serves two labels and the seventeen chosen parents exhaust the packing. The same conditional assignment for the selected off-wall profiles is imported in [premise:ROOT_ADMISSION]. For JPWS the label-11 target is the literal B11 polygon of the file named SL_L11_T020_DH, whose budget statement is named SL11_T020; these names refer to the same pinned class file [file:SLAB11]. One rounded vertex lies about 3.7×10^-8 outside HULL11. The proof directly admits B11 to JPWS_v4 without containment in HULL11; the full HULL11 is not admitted there. These are refined branch-specific targets, not the coarse frame rectangles.

<!-- P045 -->
A target can still overlap its own label's marker region. The label 12 identification uses capacity of the **union** of its target with the marker polygon: in the wall profiles its squared diameter is at most 9437/31250<1. An occupied target12 and occupied marker must consequently have the same physical parent, retaining the one chosen half-frame direction. More generally the geometric hypotheses include high-class shadow and modified marker-minus-target coverage for the occupancy implication. Neither a count of intersecting pose slots nor a separate reflection chosen for each label supplies a valid assignment. [premise:ROOT_ADMISSION]

<!-- P046 -->
For the ordinary4/4/0 implications, the target-vacancy contradiction of Section3 supplies occupancy. Distinctness of the complete profile is established separately by the cross-label geometry. Label12 remains a separate marker-minus-target argument. First use the special label12 statement to force target12; capacity of its union with the marker identifies its occupant with the chosen marker. Thereafter it is the *target12 region* in the separated seventeen-factor profile, not the entire marker polygon in isolation, that rules out reusing the marker at another label. Similarly the actual trigger is assigned its own profile factor. In JQ this is role9's closed low-wall factor y≤129/50; in JPWS it is role9's middle-wall factor129/50≤y≤13/5, with role11 in its slab factor; in JPW13 it is role9's upper-wall factor13/5≤y≤29637/10000. Each wall profile includes target12 and those role9 factors in the checked seventeen-region separation family. In JPA the actual role9 is in its upper angle-exit factor and target12 is its PB12 factor. In JPG3m/p the actual role3 is in S3 and its signed angle arm; in JPG17m/p it is role17 in S17 and its arm; in JPG15m/p it is role15 in S15 and its arm; each off-wall profile includes that factor and target12 among its seventeen factors. JG uses the gated role9 and the three loose factors, with target12=C12. The profile assignment then identifies every target occupant with a distinct physical parent, including the previously chosen marker and trigger, on closed boundaries as well. This uses the complete profile, after its occupancies have been obtained; it does not assume the whole high union is disjoint from every target, or that a union such as TT has only one occupant.

<!-- P047 -->
E07A first forces the label-7 target. Its high centre hexagon is invariant under x→U−x and its high angle class covers all directions. Reflect the entire packing and apply the implication again. The reflected label-7 target is contained in the label-8 target, and the two targets are disjoint. This yields the two occupancies using the all-direction hexagon; the half-marker need not be reflection-invariant. [premise:C7_C8_TRANSFER]

<!-- P048 -->
## 5. The exhaustive eleven-branch classification

<!-- P049 -->
The KEY_W minimum-score bound 20 and the occupied marker force an occupant of its low gate-or-wall union. By L9 uniqueness and quarter-turn inclusions, an off-wall L9 parent has 30651/100000≤t9≤44941/100000 with side representative θ9∈[0,π/2). Thus the lower angle exit and the interval t9>44941/100000 are impossible. This is an exclusion of actual off-wall cases, not emptiness of an entire padded root extending into the wall branch. The wall-column interval (613/2000,30651/100000) lies in no KEY_W low slot; only the off-wall implication is used. [premise:KEY_W_ELIMINATION]

<!-- P050 -->
The wall triggers are literal closed products in F_U. All use x9 in[-131/250,53/100] and the closed tan-half arc[-rho,rho], rho=207107/500000. With square quarter-turn representatives this covers every direction: rho^2+2rho-1>0, so rho>tan(pi/8). Their y intervals are [24137/10000,129/50] for the twelve rigid Q rows; [24137/10000,13/5] for loose Q3,Q4,Q15,Q17; [129/50,29637/10000] for all twelve PW rows; and [129/50,13/5] for SL11_T020. Each centre polygon is exactly the four corners of the specified rectangle. The object [file:WALL_TRIGGERS] checks all29 literals. Therefore JQ is inside every needed Q trigger, JPWS inside the loose Q/PW/slab triggers, and JPW13 inside the PW triggers. Equality y9=129/50 belongs to JQ and equality y9=13/5 to JPWS; overlapping closed triggers create no missing seam. These trigger memberships do not by themselves prove target occupancy or assignment.

<!-- P051 -->
The decision list in [file:ENDPOINT_CASES] first compares x9≤53/100 with x9>53/100. Equality belongs to the wall case. Its three branches are y9≤129/50, 129/50<y9≤13/5, and y9>13/5. Off-wall use θ9∈[0,π/2) and t9=tan(θ9/2), with the open gate

<!-- P052 -->
61301/200000 < t9 < 591183/1408817.

<!-- P053 -->
The lower exit includes t9=61301/200000 and is excluded because the KEY_W low gate begins at 30651/100000, larger by 1/200000. The upper surviving exit is 591183/1408817≤t9≤44941/100000 and is admitted to JPA. Its closed root arc is a containing interval with upper end below 1; [file:JPA_ADMISSION] binds the exact fractions and strict margins. The upper gate endpoint belongs to JPA, while x9=53/100 belongs to a wall branch. No local theorem for the excluded lower exit is used.

<!-- P054 -->
Before testing the other angles, identify the loose parents. Off-wall, L9 has x9>53/100. The common alternative AQ=[−131/250,53/100]×[24137/10000,13/5] of L3,L15,L17 is contained in L9 and is therefore empty, including its boundary. The strict bound-20 inequalities and occupied half-marker force occupants of S3,S15,S17. Clip to [1000469/2000000,8351531/2000000]², which contains every physical centre at side ≤C in F_U. Their squared diameters are 1097067164761/4000000000000, 799624844761/4000000000000 and 1059571044761/4000000000000, all <1. Thus each has exactly one actual occupant. Their rectangles are pairwise disjoint and disjoint from the marker and L9. S17 lies in the identified reflected frame L17 region. This defines roles 3 and 15 and identifies role 17 without a local root or angular gate. [file:LOOSE_IDENTITIES]

<!-- P055 -->
The physically clipped small slots lie in their whole coarse regions. Coarse regions 3 and 15 have capacity one by the wall-strip proof in Section 6; coarse 17 has squared diameter 1851391155161/4000000000000<1. Each contains exactly its identified small-slot parent. Coarse 17 differs from reflected frame L17 by −469/1000000 in x; their identities agree through S17 and capacity, not equality of rectangles. The clipped frame region is contained in clipped coarse 17. Whole-coarse capacity is needed to exclude extra occupants of the escape set X, whereas a PSS trigger on S3 or S15 is identified directly by its small-slot inequality. [premise:COARSE_LOOSE_CAPACITY] The exact dimensions may not be enlarged without a new capacity proof. The pure WALL_PARTITION and ROOT_ADMISSION implications do not require whole-coarse capacity; their applications receive the occupied small-slot profiles, including L4 where its factor is used.

<!-- P056 -->
If label 9 is gated, choose canonical side directions theta_k∈[-pi/4,pi/4) for k=3,17,15 and set tau_k=tan(theta_k/2). The first failed open gate -1/20<tau_k<1/20, in that order, chooses JPGkm or JPGkp. If none fails, the case is JG. Individual quarter turns only change square-axis representatives; individual reflections of physical squares are never permitted.

<!-- P057 -->
These comparisons form a disjoint exhaustive classification of every common-frame packing after the two proved KEY_W exclusions. Closed outer root regions may overlap, which does not change the case ownership. The tiny differences between C escape arcs and the current gate are checked in the required direction: the lower gap is1/200000 and the upper quarter-turn gap is974949/14197000000. Thus, in the fully gated off-wall case, every escape slot on L9 is empty. AQ is empty too. Each remaining X slot lies on a whole coarse region3,15 or17 with its direction outside that role’s open gate; coarse capacity and the identified gated occupant exclude a second parent there. Consequently the entire literal C exemption X is empty, which is the input to the C occupancy implications. This is stronger than uniqueness in the small S_k slots.

<!-- P058 -->
Each predicate in [file:CASE_PARTITION] is a conjunction of comparisons of one coordinate with a rational constant. Cutting each coordinate line at all constants gives singleton endpoints and intervening open intervals; predicates have constant truth on their products. Exact evaluation on these atoms establishes exactly one of thirteen predicates everywhere. The KEY_W implication eliminates the lower exit and the high9 atom, leaving eleven cases. Eight negative controls include loss and double ownership of the exact upper KEY_W endpoint; the check rejects deliberately introduced gaps and double ownership at wall and angle endpoints. This logical partition proof includes seams, but proves neither target occupancy nor root admission and does not replace those premises.

<!-- P059 -->
With the frame premise discharged, the first wall case supplies all sixteen Q target occupancies, including Q13. Together with the unique role-9 parent and the conditional distinct-parent assignment, they form the complete seventeen-square product admitted to JQ. Its EMPTY theorem excludes this actual case, including y9=129/50, for an endpoint-normalized packing. The middle case supplies the four loose-Q occupancies, ordinary PW targets and the SL11_T020 label-11 slab factor, which are admitted to JPWS. At y9=13/5, AQ remains occupied by role 9, so only this middle profile applies. The upper wall case supplies the PW targets and four loose-L occupancies and is admitted to JPW13. Its loose-L consequences require y9>13/5. JPW13 includes its lower boundary as a harmless superset; this does not assign that seam to the upper capture branch. [file:LITERAL_STATEMENTS] [premise:ROOT_ADMISSION]

<!-- P060 -->
The fully gated off-wall case supplies the C/L product and is admitted to JG, with all required C and L consequences, including L17. Sections 7 and 8 exclude that actual case for every hypothetical packing of side below L. This does not exclude the known packing at equality. For the two JPG15 cases all twenty-four target clauses across both signs have their budgets and extra L premises, and both literal v5 roots are EMPTY; distinct-parent admission and fixed-pose enlargement give their contradiction without a signed fallback budget. Each of the other tilted branches supplies its rigid targets by the selected implications of Section 6 and its required loose L premises, and is admitted to its corresponding root. These are capture implications: class definitions or local trees alone do not supply their occupancies. [file:SELECTED_CLAUSES] [premise:ROOT_ADMISSION]

<!-- P061 -->
## 6. Selected capture implications and coarse capacity

<!-- P062 -->
Fix a rigid label j∈{1,2,5,6,7,8,10,11,12,13,14,16} and one of the seven tilted branches. Its actual trigger parent is identified, WC is empty, and the marker is occupied. The trigger union need not have only one occupant. The chosen PS, PSS, HULLW11 or signed PS6 inequality forces its literal target by Section 3, and the complete profile geometry assigns its occupant and admits it to the root. The specific class bytes and bound are essential. [file:SELECTED_CLAUSES] [premise:SELECTOR_LOGIC]

<!-- P063 -->
For PSS_j^k with k=3 or15, L_k gives the unique S_k occupant by Section5. This is the definition of role k and of the parent whose canonical angle tau_k is tested by the decision list. The PSS trigger's centre polygon is exactly S_k; the branch predicate puts this same parent in its specified closed direction arm. With the distinct occupied marker, empty WC and strict bound23, target absence is impossible. The implication is `(L_k AND PSS_j^k AND actual branch hypotheses) => target`. It uses neither the local root nor COARSE_LOOSE_CAPACITY to identify role3 or role15. Coarse capacity remains required for the JG escape-set emptiness step, where X occupies whole coarse arms.

<!-- P064 -->
The k=17 PSS alternatives use the same identification, with L17 required explicitly. Here the physically clipped whole coarse region has squared diameter1851391155161/4000000000000<1, so its capacity one follows directly from the inscribed-disk argument, with no angle coupling. The L17 low slot is physically contained in that region. Thus its forced occupant and the actual trigger parent coincide before any local root has been obtained.

<!-- P065 -->
For the whole coarse regions 3 and 15, use the following wall-strip argument, allowing independent square orientations and either centre ordering. Write a separating axis n=(a,b) with a,b≥0 and a²+b²=1 after coordinate sign choices, and let square A own it. Set d=(a+b)/2. A has support 1/2 along n and support d normal to the wall. If A is nearer the wall, |Δy|≤H−d and the other square has support at least 1/2 along n, so separation requires aw+bH−bd≥1.

<!-- P066 -->
If square B is nearer instead, separation requires aw+bH≥1/2+h_B(n)+b h_B(e_y). For B's orientation phi modulo pi/2, the function h_B(n)+b h_B(e_y) has second derivative equal to minus its positive value, hence is concave between its absolute-value breakpoints0,alpha,pi/2, where alpha is the direction of n. Its endpoint values are d+b/2 at0 andpi/2, and1/2+bd atalpha. Their difference (d+b/2)−(1/2+bd)=(1−b)(a+b−1)/2≥0. Thus h_B(n)+b h_B(e_y)≥1/2+bd in this ordering too, giving the same necessary inequality aw+bH−b(a+b)/2≥1. Square B's orientation has never been tied to A's. Setting a=(1-u²)/(1+u²), b=2u/(1+u²) reduces the strict opposite inequality to positivity on u∈[0,1] of the quartic with power coefficients[1-w,1-2H,4,-1-2H,1+w]. For k3 use(w,H)=(529/750,2821531/2000000); for k15 use(3427/5000,2859531/2000000).  Positivity of every Bernstein coefficient on 128 equal rational subintervals gives respective minima 634043429/125829120000 and 43535731167/8388608000000. The exact tables are [file:COARSE_CAPACITY_TABLES]. This proves capacity for independent orientations. [premise:COARSE_LOOSE_CAPACITY]

<!-- P067 -->
A sign-specific alternative retains only the trigger component for that sign. The canonical branch predicate puts its actual parent in that component. The unchanged target, all high/low interactions, all quarter turns and its root inclusion have been independently checked. The selected signed k=17 options are used only for label 6: ENDm on JPG17m and ENDp on JPG17p. Label 7 uses PS_L07_T17 on both signs. Padding a root arc does not enlarge a trigger hypothesis. [file:SELECTED_CLAUSES]

<!-- P068 -->
The conjunction, over seven branches and twelve rigid labels, of the disjunction of these complete implications suffices for tilted capture. There are 84 clauses. Each includes its required extra L_k premises: a budget without such a premise does not discharge a clause. Independent choices are compatible because simultaneous target-profile assignment and all selected target inclusions have been checked. The v5 label-11 factors contain PB11 and the admitted HULLW11 choices. An accepted v2 local tree alone does not establish emptiness of the larger v5 factor. [premise:SELECTOR_LOGIC]

<!-- P069 -->
The selected signed files are precisely PS_L06_T17_ENDm_H4T4 and PS_L06_T17_ENDp_H4T4, both with bound23. Their retained trigger arms are respectively [-rho,-1/20] and [1/20,rho], with the original coarse17 centre polygon. The S17 parent lies in that polygon after physical clipping, and its actual branch sign puts it in the retained arm. Marker and trigger are distinct; WC is empty. If PB6 were absent, all17 scores would be 1 or4 and the two high parents give sum>=23. Hence PB6 is occupied, and its unchanged literal target is admitted to the corresponding v5 factor. This proves both selected signed implications, for each of the two signs.

<!-- P070 -->
The two signed implications are bound by [file:SIGNED6_NEGATIVE] and [file:SIGNED6_POSITIVE] to the actual class bytes and trigger arcs. Their abbreviated receipt statements are identical; the class hash and closed arc specify the sign, so one sign’s receipt is not interchangeable with the other’s.

<!-- P071 -->
Every other clause uses its specified file in [file:SELECTED_CLAUSES], including PS5/17 on JPG17p, PS1/17 on JPG17m and PS16/9 on JPA. Unselected alternatives are not hypotheses of this conjunction.

<!-- P072 -->
## 7. Admission and exact local trees

<!-- P073 -->
Admission converts the endpoint physical poses to the rational reference chart with the complete position and independent-angle intervals. It uses square geometry and wall supports. The gated label-9 support cut ξ_(9,1)≥−9897/10^6 requires no scalar lower bound. [premise:ROOT_ADMISSION]

<!-- P074 -->
The chart in [file:LOCAL_SPEC] fixes Sref=R and the rational reference [file:REFERENCE_PACKING]. Put p_i=p_i(file) except p13=p13(file)−(T0/3)v13, where T0=u9x(u9x+4−R). Chart axes are (u_i,v_i) for labels 11 and 13 and Cartesian for every other label. These are fixed orthonormal axes, independent of each unknown physical rotation.

<!-- P075 -->
Explicitly, if c is a centre in F_U, p_i is that rational reference centre, and e_(i,1),e_(i,2) are its fixed orthonormal chart axes, the endpoint coordinates are

<!-- P076 -->
xi_(i,k) = e_(i,k) · (c - (U-L)(1,1)/2 - p_i).

<!-- P077 -->
The axes of this chart do not rotate with a square's unknown physical angle. This is affine in c and L, so its extrema over a convex source polygon and a certified interval for L occur among polygon vertices paired with interval endpoints. The exact admission calculation tests those extrema against every root's two coordinate intervals. In particular the nonzero difference R-L survives this calculation; flush-wall displacements relative to the rational reference can be negative and must not be replaced by0. Whole direction intervals are compared using exact rational rotations and homogeneous half-angle transformations under quarter turns, which preserve all physical orientations even when a tangent chart has a pole. The supported public admission entry point and its complete input set are specified in [file:PUBLIC_ENTRYPOINTS]. The historical audit and generator names quoted in retained source records are provenance references, not public executable dependencies.

<!-- P078 -->
The C12 arc extends to tan-half 4494109/10000000. In JG, the maximum squared distance in the marker hexagon united with the C12 rectangle is <3953/10000<1; the other ten profiles have the separate bound 9437/31250. Thus target 12 and the marker have the same physical parent. Intersect the C12 source arc with the chosen half-marker ending at 207107/500000 before comparing with the JG arc. The uncut source does not fit. [file:C12_UNION_CAPACITY] [file:C12_PROFILE_CAPACITY] [premise:ROOT_ADMISSION]

<!-- P079 -->
For gated label 9, containment gives x9≥(cos θ9+sin θ9)/2 in the first quadrant. The support is concave on the rounded root arc, so its minimum is attained at an endpoint. Exact endpoint evaluation minus p9x is >−9897/10^6. The cut is therefore established before root admission and is valid for JG and all six JPG branches; it assumes neither the other gates nor a stress pattern. [premise:ROOT_ADMISSION]

<!-- P080 -->
The four executed HULLW11 literals used in the seven tilted label-11 clauses have the same closed absolute tan-half arc [1430271/5000000,4828869/10000000]. Its lower admission slack is approximately 2.5738745668×10^-13 in relative tan-half coordinates and 5.1234563526×10^-13 as the sine of the angular gap. The exact rational tests, not these decimal displays, establish inclusion. The two units are related by sin(2 atan(t)−2 atan(r))=2(t−r)(1+tr)/((1+t²)(1+r²)). [file:LABEL11_ARCS] [file:LABEL11_MARGINS]

<!-- P081 -->
For every genuine separating-axis disjunction, the children of a split cover the parent feasible set. An exact infeasibility leaf contradicts its node constraints; a terminal leaf implies its declared physical window. Induction on the complete finite tree gives the root conclusion. An EMPTY conclusion additionally requires zero terminal leaves and equality of the root data with the named region. A TUBE conclusion requires the corresponding root and terminal-window bindings. These conditions are enforced by [file:ROOT_POSTCHECK] in addition to the frozen checker rules [file:LOCAL_SPEC] and [file:LOCAL_SPEC_NOTES]. No unverified option exclusion or omitted child may be supplied by a numerical generator.

<!-- P082 -->
Here is the exact inference behind a leaf (SPEC3 Sections 4.10 and 5). For any physical configuration x in its node, each declared pair has a valid separating option in its retained list: the checker excludes every omitted option. Choose the first valid retained option, set its indicator to1 and all the other indicators to0. This gives a lifted point (x,z*) in the round's bounds. Every permitted term is nonnegative there. A term containing a circle identity is zero, including when its coefficient has either sign; all other coefficients are nonnegative. A sign-free polynomial multiplier requires a circle identity. An undecided option's corner polynomial requires its own indicator as a factor, even in a circle-identity term. The latter is an explicit well-formedness requirement of the frozen specification.

<!-- P083 -->
For objective g the checker forms, over the rationals,

<!-- P084 -->
Rem = g - sum_k lambda_k product_j f_(k,j).

<!-- P085 -->
It expands Rem in raw variables or about the declared rational centres, combines identical monomials, and bounds every monomial by the prescribed interval product. Indicator variables stay in[0,1]; only base variables may have shifted centres. If ell is the resulting rational lower bound, then g(x)>=Rem(x,z*)>=ell. In particular g=0 with ell>=value>0 proves the node EMPTY. The two other infeasibility closures are an empty store and exact exclusion of all eight options of one pair. All steps in a round use the store at the start of that round, and later stores may use only the certified bounds. Thus no step obtains a bound by assuming its own conclusion. This is the imported exact inference theorem, not a claim that the floating relaxation is exact.

<!-- P086 -->
The accepted root records use **S_floor=R and root side interval[R,R]**. Their conclusions nevertheless apply to every physical packing of side S<=R in the stated root poses. Keep all squares fixed in the corner-at-origin chart and enlarge only the containing box from[0,S]^2 to[0,R]^2. Pair separations are unchanged, and the right/top wall constraints become weaker. All reference positions, root intervals and arcs are fixed data independent of S. The same poses therefore lie in the root at side R. An EMPTY conclusion rules them out; a tube conclusion constrains those same unchanged poses and hence also holds when their actual containing side is read as S. This is precisely SPEC3 Section11 and the independently reviewed root-region corollary; no premise S>=R or extra numerical lower bound is needed. In this composition S=L. The enlargement to R is auxiliary, with no translation or recentering. Physical rigidity is then applied at actual L; applying it at R would be invalid because R>L.

<!-- P087 -->
No auxiliary translation is used. Every selected left/bottom lower root end is at most −1/1000000; the G20S and HW windows also extend negatively. The flush reference offset is ε=323264740583067756265381186720884493986257/(625·10^56)>0. On right/top zero ends, physical containment at actual L yields ξ≤L−R+ε<0, because the exact enclosure gives R−L−ε>0. In particular square 2 preserves ξ_(2,1)≤0 through both G20S/HW transfers. The chart remains c−(U−L)(1,1)/2. [file:FRAME_CHECK] [file:ENDPOINT_REFINEMENT]

<!-- P088 -->
There is no general containment rule between different roots: JPWS_v4 is smaller than JPWS_v2x and uses the separate B11 slab. A leaf region D may contain a node’s required piece N if every position, independent arc, side and separation assumption of N implies the hypotheses used in D. Infeasibility of D then excludes N; contraction of D contracts N. Every reused node must pass its own numeric proof within the complete certificate and satisfy its parent-child coverage test. Inherited assumptions must equal the parent list plus the specified split assumption, with an empty root assumption list. Every child exists, every non-root is attached once and every node is reachable from the unique root. These rules, not filenames or generation tags, justify reuse. [premise:LOCAL_CHECKER_SOUNDNESS] A PASS label without the complete hypothesis and coverage tests cannot close a different root.

<!-- P089 -->
The eleven root conclusions are: JQ, JPA_v5, JPG3m_v5, JPG3p_v5, JPG17m_v5, JPG17p_v5, JPG15m_v5, JPG15p_v5, JPW13_v2x and JPWS_v4 are EMPTY; JG_v2 enters G20S. Their literal roots, complete certificate executions and region post-checks are respectively [tree:JQ], [tree:JPA_v5], [tree:JPG3m_v5], [tree:JPG3p_v5], [tree:JPG17m_v5], [tree:JPG17p_v5], [tree:JPG15m_v5], [tree:JPG15p_v5], [tree:JPW13_v2x], [tree:JPWS_v4] and [tree:JG_v2]. [premise:LOCAL_CERTIFICATE_IMPORT]

<!-- P090 -->
JG has one checked terminal leaf. Its tube theorem requires all feasible paths to reach validated terminals, without requiring a prescribed positive terminal count; zero terminals would give EMPTY. Its sixteen constrained box endpoints and angle bounds agree with the G20S input. JPWS uses SL11_T020’s B11 factor, not the full PW11/HULL11 target. JPA_v5 has 416 nodes, 415 covered children, 93 option splits and 281 infeasible leaves; JPWS_v4 has 110 nodes and 70 infeasible leaves. Both have zero terminal leaves. The six omitted Case-G options and the seven negative wall ends are covered by the exact certificate rules, not assumed from numerical preparation.

<!-- P091 -->
## 8. From the G tube to physical rigidity

<!-- P092 -->
The JG conclusion gives sixteen constrained parents in G20S: 29 nonslider coordinates in [−1/5,1/5], ξ_(2,1)∈[−39/125,0], ξ_(11,2)∈[−1/5,1/5], ξ_(13,2)∈[−1/5,28/125], and sixteen independent radian rotations with |φ_i|≤1/10. Positive-cosine and rational sine tests establish this angle statement; it is not merely a sine bound. [premise:G20S_PHYSICAL]

<!-- P093 -->
Use G20S→T1→HW→T2→the finite sixteen-square entry→rigidity. The two tree implications are [tree:G20S] and [tree:HW], using the v3.0 specification. Parallel-face-union and unique-owner envelope arguments remain separately bound analytic premises [file:PARALLEL_FACE_UNION] [file:UNIQUE_OWNER_ENVELOPES]. [file:TERMINAL_COMPOSITION]

<!-- P094 -->
G20S gives T1 with 29 nonslider positions within 3/20, all sixteen radian-angle radii 101/1000, ξ_(2,1)∈[−8/25,1/100], ξ_(11,2)∈[−1/5,2/25], ξ_(13,2)∈[−1/5,1/10]. Retain ξ_(2,1)≤0, since the poses do not move; that intersection lies in HW. HW gives T2 with position radius 1/250, angle radius 1/500, ξ_(2,1)∈[−8/25,1/250], ξ_(11,2)∈[−1/5,1/20], ξ_(13,2)∈[−1/5,3/40]. Retain ξ_(2,1)≤0 again. Neither hand-over holds without this retained cut. The area of sixteen unit squares gives S≥4, satisfying the two trees’ lower side guard.

<!-- P095 -->
The resulting closed entry has 29 nonslider positions within 1/200, sixteen independent angles within 1/400 radians, a∈[0,8/25], b_slider∈[−1/20,1/5], z∈[−1/5,3/40], at actual S≤L. These slider ranges are those of T2. The sixteen-square implication [file:SIXTEEN_SQUARE_THEOREM] applies without a physical square 4 or an extendability hypothesis.

<!-- P096 -->
The large-entry coordinate transfer puts every one of the 45 exact-root core coordinates strictly below 501/100000, with slider intervals padded by 10^-12. Nonnegativity of the root a endpoint follows from square 2’s actual right wall and S≤L, not from subtracting independent intervals. The basis change at labels 11 and 13 retains the correlated same-slider terms. The two stop pairs 9/11 and 11/13 then give the raw cuts b_slider≥−213/25000, b_slider+z≤49/2000 and z≤33/1000 after the signed reference errors are included. [file:ENTRY_TRANSFER] [file:STOP_PRUNING] [file:ENDPOINT_REFINEMENT]

<!-- P097 -->
The finite wall, linear-pair, second-order-pair, parallel-pair, product and rounded rows are necessary for the physical entry. Their analytic derivation is a premise independent of agreement between polynomial builders. In particular the parallel-pair remainder has the following derivation. [file:FINITE_ROW_DERIVATION]

<!-- P098 -->
Let J be a positive quarter turn, n a unit separating normal, Δ=d_w+δ_h the centre difference, |d_w|≤D and |δ_h|≤dr. Put μ=(ω_i+ω_j)/2, ε=(ω_j−ω_i)/2, |μ|≤m, |ε|≤q≤1/10, X=n·Δ, τ′=(Jn)·d_w and |τ′|≤τmax<1. Here d_w includes the reference difference and unscaled slider displacement.

<!-- P099 -->
The two retained directed separating alternatives have different owners and reference normal n. With n_m=R(μ)n, X_m=n_m·Δ, τ_m=(Jn_m)·Δ and e=|ε|, their disjunction and the unit-square support formula give

<!-- P100 -->
cos(e) X_m + sin(e)|τ_m| ≥ cos(e)² + sin(e)cos(e).

<!-- P101 -->
Since cos(e)>0 and cos(2ε)>0 on the declared range,

<!-- P102 -->
X_m−1 ≥ cos(e)−1+sin(e)−tan(e)|τ_m|
         ≥ e(1−|τ_m|)−e²/2−e³/6−e³|τ_m|.

<!-- P103 -->
Use cos(e)≥1−e²/2, sin(e)≥e−e³/6 and tan(e)≤e+e³. The last follows from sin(e)≤e, cos(e)≥1−e²/2 and 1/(1−e²/2)≤1+e² for 0≤e≤1/10. These include e=0 without division by e. Taylor’s integral remainder and |R(μ)n−n|≤|μ| give

<!-- P104 -->
|X_m−X−μτ′| ≤ Dm²/2+m·dr,
    |τ_m−τ′| ≤ Dm+dr.

<!-- P105 -->
Set E=Dm²/2+m·dr+q²/2+q³/6+τmax·q³+(Dm+dr)(q+q³). Then X−1+μτ′+E≥e(1−|τ′|). Since 1−|τ′|>0, both necessary rows are

<!-- P106 -->
X−1+μτ′+sε(1−|τ′|)+E ≥ 0,   s∈{−1,+1}.

<!-- P107 -->
On a box where τ′ has constant sign σ, substitute |τ′|=στ′. Expanding μ and ε gives the coefficients (1+sσ)/2 and (1−sσ)/2 on slider times ω_i and ω_j in the two implemented rows. Their true products satisfy the McCormick relaxations. If the constant-sign or τmax<1 guard fails, the pair is omitted. No contact, stress, common-angle or local-minimality assumption is used. [file:FINITE_PARALLEL_DERIVATION]

<!-- P108 -->
The stop derivation uses only squares 9, 11 and 13. The root a≥0 repair uses square 2 and its right wall; the finite side floor uses square 8 and its top wall. Other raw-to-root calculations are separate affine and angular coordinate changes for each of the sixteen labels. No step uses the presence, pose, non-overlap or extendability of square 4. Actual S≤L, distinct physical labels, independent rotations, the specified p13 reference and the complete closed slider boxes are retained. [file:SIXTEEN_SQUARE_THEOREM]

<!-- P109 -->
Four exact stage drivers cover complete rounds 1–3, 4–9, 10–15 and 16–17. Their common independent polynomial builder reconstructs the necessary rows from the reference, incoming bounds, pair geometry and product hulls; comparison with each saved model, rational dual replay and simultaneous updates give the seventeen-round induction. The final raw radius is 64007486789/10^15<1/10000. The small transfer gives exact-root radius <1/5000, preserving the wall-derived a≥0. [file:FINITE_STAGES] [file:SMALL_ENTRY_TRANSFER] [file:ENDPOINT_REFINEMENT]

<!-- P110 -->
The normalized stopped contraction has ratio 159201934153319/200000000000000<1. A nonzero core could be rescaled to normalized maximum 1, contradicting that strict contraction. Thus the exact-root core vanishes. This is stronger than a finite smallness conclusion and applies to the sixteen-parent physical system at actual S≤L. [file:NORMALIZED_RIGIDITY]

<!-- P111 -->
Apply that theorem to the normalized packing at actual side L. The input chart uses the rational reference positions and axes; the zero-deviation conclusion instead uses the exact algebraic-root reference positions and axes. There are32 centre coordinates for sixteen parents; omit the three slider coordinates xi_(2,1), xi_(11,2), xi_(13,2), leaving29 position deviations, then include16 independent angle deviations: these are the45 rigid-layout core coordinates. The free parameters are a=−xi_(2,1), b_slider=−xi_(11,2), z=xi_(13,2); their names do not denote the polynomial root b in Section1. The theorem fixes all45 exact-root core deviations to zero on the sixteen-parent system; label 4 is not used in this rigidity argument. In particular nonslider role 8 has centre(L-1/2,L-1/2) and horizontal/vertical axes. It touches both the right and top endpoint walls. This contradicts Section 2, which put every point of the packing strictly inside those walls. The common dihedral image merely changes which two walls are touched. [premise:WALL_CONTRADICTION]

<!-- P112 -->
The contradiction is physical wall contact with the strictly inset normalized packing. A conclusion merely repeating that the containing side is L would not suffice. LOCAL_JG is the separate local-root implication supplying the G20S input; the terminal theorem is applied at actual L, never at the larger rational tree cap. No charge inequality at an irrational cap is required. [premise:ENDPOINT] [premise:G20S_PHYSICAL] [premise:WALL_CONTRADICTION]

<!-- P113 -->
## 9. Composition and the evidence boundary

<!-- P114 -->
Every hypothetical packing at S0<L normalizes to a packing at actual L in one common frame. The class inequalities and geometric implications place it in one of eleven roots. Each non-G root is EMPTY. The G root yields the wall-contact contradiction of Section 8. Hence no packing exists below L. The explicit packing of Section 1 attains L. Under the certificate hypotheses stated above, these implications establish the theorem. This manuscript composes those hypotheses and is not an independent seal of the completed argument; an independent assessment of the assembly remains required.

<!-- P115 -->
The dependency graph [file:DEPENDENCY_GRAPH] has 328 nodes, 1,537 edges and 210 obligation identifiers: 100 literal identifiers, 12 mathematical-lemma identifiers prefixed only in DEPENDENCY_GRAPH.json (the three further premise identifiers FRAME_ASSIGNMENT, C7_C8_TRANSFER and KEY_W_ELIMINATION remain unprefixed, giving 15 premises in total) and 98 budget identifiers. Name binding need not put an entire applied claim at its pure conditional node. WALL_PARTITION, ROOT_ADMISSION, SELECTOR_LOGIC and WALL_CONTRADICTION identify pure implications; SL11_T020 identifies its budget. Applied content lies in the small-slot identities, escape-set emptiness, occupancy, branch and admission nodes, the G contradiction and slab-occupancy implication. In particular EXCLUDE_JG includes LOCAL_JG, and OCC_JPWS_SL11_T020 includes FRAME_ASSIGNMENT. This does not assert that every direct user of a pure lemma needs all global application premises. Acyclicity or an identifier count alone proves none of the claims. [file:OBLIGATION_BINDINGS]

<!-- P116 -->
Independent assembly must bind all completed evidence used in this implication: the endpoint enclosures, including the separate tight refinement [file:ENDPOINT_REFINEMENT], and upper constructions of Section 1; the 98 literal score statements and two derived occupancies [file:LITERAL_STATEMENTS]; the authentic complete executions required by Section 3 [file:RECEIPT_ROSTER], with the finite index-size safeguards [file:INDEX_SAFETY] and the row-decision versus geometry-replay distinction of P035; the selected 84 clauses [file:SELECTED_CLAUSES]; the exact marker conversion [file:MARKER_CONVERSION], JPA admission [file:JPA_ADMISSION], and case partition [file:CASE_PARTITION], wall triggers [file:WALL_TRIGGERS], loose identities [file:LOOSE_IDENTITIES], coarse capacity tables [file:COARSE_CAPACITY_TABLES], both C12 union-capacity calculations [file:C12_UNION_CAPACITY] [file:C12_PROFILE_CAPACITY], frame check [file:FRAME_CHECK], root-admission calculation [file:ROOT_ADMISSION_CALCULATION] [file:ROOT_ADMISSION_OUTPUT], and label-11 arcs [file:LABEL11_ARCS] of Sections 4–7; the whole-root conclusions of Section 7; and the G20S and HW trees, both preserved-cut handovers, finite-entry transfer and stops, all seventeen finite rounds, small-entry transfer and normalized rigidity of Section 8. Their actual identities, side/frame agreement, sound inference rules and all stated mathematical hypotheses must be established. A printed status, PASS summary or this manuscript cannot discharge a missing antecedent.

The four supplementary label records ENVELOPE_REVIEW, ENVELOPE_SOURCE, FINITE_ROW_KERNEL and JOINT_ROW_CONSTRUCTOR identify supporting sources; they are not additional premises or missing proof references.
