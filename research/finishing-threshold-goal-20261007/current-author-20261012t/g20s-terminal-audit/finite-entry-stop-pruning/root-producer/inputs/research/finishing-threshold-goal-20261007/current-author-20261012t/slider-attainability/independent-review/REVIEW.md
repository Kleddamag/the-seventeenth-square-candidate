# Independent mathematical review of the padded-window stop mechanism

8 October 2026. Reviewer `Codex`, separate from the
finite-row producer `Codex` and terminal producer
`Codex`. The requested input is position radius `2/25`, angle
radius `3/100`, and sliders

```
a in [0,33/100], b in [-201/2500,49/300], z in [-41/200,57/400].
```

**PASS for the complete stop-pair implications and their exact constants.
No padded finite contraction or padded all-scale rigidity theorem is proved
by these results.** The new inequalities preserve negative b, independent
angles, both possible normal owners, and all boundary cases.

The read-only external audit `LOCAL_THEOREM_AUDIT.md` correctly identifies the
original slider bounds as extra hypotheses and the two excluded stopping
pairs as a possible remedy. Its numerical slider attainability estimates are
not premises of this review. The original authoritative theorem remains the
unchanged union of its A/B products with its original slider intervals.

## Independent arithmetic

Run from the repository root:

```
python3 -B research/finishing-threshold-goal-20261007/current-author-20261012t/slider-attainability/independent-review/check_mathematics.py
```

This checker imports no producer code. It reconstructs the rational reference
from the pinned packing, including the square-13 correction, then enumerates
the relevant world-coordinate vertices and projects them onto the common
reference axes. It verifies all saved finite constants and every retained or
excluded SAT owner/direction at radii .08, .15 and .25 with the corresponding
radius-padded sliders. Independent unrounded Fraction interval arithmetic on
the already established root's outer box checks the terminal constants.
Its initial run used **0.017407 CPU seconds**, 0.019575958 wall seconds.

The scope of `arithmetic-receipt.json` is deliberately limited. The code does
not replay the terminal's coordinate transfer, all nineteen other contact
rosters, the 52-row model, symbolic skeleton certificate, or weak duals. Their
implementation/replay review is separate.
The analytic implications below do not rely
on a successful padded rigidity replay.

## Full separating-axis coverage

Let `u=(c,s)`, `v=(-s,c)` be the common reference axes of squares 9, 11 and 13.
Their *physical* angles are independent. Write the actual centre difference
as `Delta=Xu-Nv`. Direct substitution into the theorem's centre formulas gives

```
(9,11):  X=X0+h11-u.h9, N=K+b+v.h9;
(11,13): X=X0+h13-h11,  N=K-b-z.
```

All constants in the finite stage are the actual fixed rational constants;
in particular no nearly unit rational K is silently replaced by one.

For each owner `o=i,j`, the four directed candidate axes have projections

```
 +/- [X cos(theta_o)-N sin(theta_o)],
 +/- [-X sin(theta_o)-N cos(theta_o)].
```

The required half-width sum is
`H(eta)=(1+|cos eta|+|sin eta|)/2`, where `eta=theta_j-theta_i`.
The separating-axis theorem for two convex squares says that nonoverlap of
their interiors implies at least one of these eight projections is at least
H. Conversely, a separating axis is sufficient, although only necessity is
used here. No physical contact, contact-point choice or equality is assumed.
Square central symmetry makes the same half-width formula valid for either
owner and either direction. Coincident axes and boundary contact are retained.

For the checked angles, cosine is positive and `H>=1`. If the computed bounds
are `Nlo<=N<=Nhi`, `|X|<=L`, then

```
 |X cos(theta_o)-N sin(theta_o)| <= L+alpha*Nhi,
 -X sin(theta_o)-N cos(theta_o)
     <= alpha*L-Nlo*(1-alpha^2/2).
```

The checked inequalities `Nlo>0`, `L<1` and both displayed upper bounds `<1`
exclude both u directions and the positive v direction of **both owners**.
Exactly the two negative-v owner alternatives remain:

```
N cos(theta_o)+X sin(theta_o) >= H(eta), for at least one o in {i,j}.
```

This is a union, not an intersection. Negative b and independent positions do
not invalidate it because all corresponding box vertices were included.

At the requested padded A, the u-exclusion margins exceed .4926 for (9,11)
and .6726 for (11,13). At radius .25 with sliders padded by .25, they still
exceed .0709 and .3224 respectively. These are analytic pair-domain results,
not enlarged local theorem claims.

The producer's claimed first sufficient guard failure is also checked beyond
its three samples. For the radius-padded one-parameter family it occurs at

```
r0 = [1-X0-alpha*(K+1/12)] / [(1+c+s)*(1+alpha)]
   = approximately 0.2785848220873706, alpha=3/100,
```

for the (9,11) u guard. At this exact rational r0 every other stated guard
remains strict, while that guard equals one. Each relevant bound is affine
in r on this range, so its endpoint checks prove the same claims throughout
`0<=r<r0`. This is a limit of this sufficient enclosure only; failure at r0
does not assert an actual new separating option exists there.

## The shared-product rows are valid across the owner union

Set `m=(theta_i+theta_j)/2`, `q=(theta_j-theta_i)/2`, `Q=alpha`.
Since N is positive,

```
N cos(theta_o)+X sin(theta_o)
    <= N+X theta_o+L*alpha^3/6.
```

Maximizing over the two owners gives an upper bound
`N+Xm+L|q|+L*alpha^3/6`. The lower Taylor bound on the support is

```
H(2q) >= 1+|q|-q^2-(2/3)|q|^3.
```

Therefore every nonoverlapping pair in the whole domain satisfies

```
N+Xm-(1-L)|q| >= 1-E,
E=Q^2+(2/3)Q^3+L*alpha^3/6.
```

For `C=1-L>0`, this is equivalent to both rows
`N+Xm+Cq>=1-E` and `N+Xm-Cq>=1-E`. Neither row selects an owner or a tangent
sign. The result uses ordinary Taylor inequalities pointwise; it is valid at
zero relative angle and at the boundary. The midpoint expression in the
producer's formula (4) is also correct: the maximum of the two owner
projections is `Nm cos q+|Tm sin q|`, and
`H(2q)=cos q*(cos q+|sin q|)`.

For (11,13), the tangent changes sign already at padded A: take both angles
zero, b=z=0 and `h13-h11=+/- .16`. Then X has opposite signs while `N=K>1`,
so both pair configurations are strictly separated. These are exact pair
witnesses, not seventeen-square witnesses. Consequently a fixed tangent sign
or a single chosen owner would lose genuine configurations. The proposed two
rows retain them.

An implementation must share the actual core, angle and lifted product
variables across rows. Separate relaxations may safely weaken correlations;
they may not silently substitute a different physical orientation in each
row. Branch-specific owner rows need their full corner roster and remainder
check. The present proof does not audit an implementation of those new rows.

## A useful finite restriction, with its limitation

The simpler consequence `N>=1-alpha L` is valid without fixed angle signs.
At the requested padded A this gives

```
b+z <= 0.032379300989100294... < 32379301/1000000000,
```

compared with the independent input upper bound `367/1200`.
The exact value, rather than its displayed decimal, is in the saved
arithmetic. This is a proved reduction of a complete hypothetical pair
domain. It is neither a bound on b alone nor on z alone, and it does not prove
extendability to seventeen squares.

The uniform lower bound for b at the same initial radius is approximately
-.1267453, weaker than the padded input -.0804. Thus the finite stop lemma
does **not** immediately fix either problematic parallel offset. On the full
padded box both (11,12) and (13,14) offsets may cross zero. A contractor must
handle both, or prove stronger bounds before invoking fixed-sign rows.

## Stronger consequence after terminal core contraction

The terminal proposal uses exact-root axes and centres. Its identities can be
checked directly from `bridge.layout`: with `h=(c+s)/2`, square9 has u
coordinate `.5+cs+2s` and v coordinate `2c+(c^2-s^2)/2`; square11 has
coordinates `c+2s+.5` and one less than that v coordinate. Thus its relative
coordinates are `X=c(1-s)`, `N=1+b`. Square13's corresponding coordinates give
`X=c-s`, `N=1+T/3-b-z` relative to square11. These are identities using
`c^2+s^2=1`, not numerical zero tests.

Assume all 45 exact-root core coordinates have modulus at most epsilon, with
`0<epsilon<=1/5000`, and retain the complete padded slider box plus its stated
`10^-12` coordinate-transfer padding. Independent rational interval checks
confirm the terminal's six-option exclusions for both stop pairs, using
`D=6/5, dr=5/2` and `D=4/3, dr=2`. They also confirm actual N remains positive.

Only the surviving negative-v owner can separate the pair. Since square
half-width sums are at least one,

```
1 <= N cos(theta_o)+X sin(theta_o) <= N+epsilon |X|.
```

The exact root interval gives `c+s<1.41`, `c(1-s)<.277`, `c-s<.129`.
For (9,11), `|v.h9|<=1.41 epsilon` and
`|X|<.277+2.41 epsilon`. For (11,13), the normal core displacement is exactly
zero and `|X|<.129+2 epsilon`. Consequently

```
b >= -(17/10)*epsilon,
b+z <= T/3+(13/100)*epsilon.
```

At epsilon=1/5000 this restores `b>=-17/50000=-.00034`, safely inside the old
lower b endpoint `-1/2500`. It also gives
`z<=T/3+(183/100)*epsilon<1/40`. The containing stopped box therefore has
positive (11,12) and (13,14) reference tangential offsets. Independent coarse
root enclosures give, respectively, intervals within
`(.05649869,.22017204)` and `(.05557643,.28557645)`, both strictly inside
`(0,1)`.

These are genuine conditional terminal restrictions. They do **not** restore
the old a upper, b upper or z lower endpoints. They do not prove finite
contraction from the .08/.03 input. They also do not certify any all-scale
weak dual on the wider box merely by restoring the model's sign guards.

## Terminal and remaining proof obligations

The producer reports that exact old-dual reuse retains normalized radius one.
That outcome does not establish strict contraction and is correctly labelled
as such. The later repeated-weight experiment also has no accepted rigidity
claim. A fresh proof must bound every normalized core coordinate strictly
inside the unit cube, for every allowed slider value and every scale, using
valid rows with independently checked exact dual bounds.

The proposed correlation rows are mathematically sound in form: if
`y=b+z` and a normalized angle is x, then the existing physical lifted
variables satisfy `q_y=q_b+q_z=y*x`. McCormick inequalities for the full
certified intervals of y and x remain necessary inequalities. Their actual
coefficients, outward rounding and insertion still need implementation
review and fresh replay. Merely testing slider polygon vertices in separate
LPs would not certify the joint product relaxation.

The sixteen-square witness described in `padded-terminal/PROPOSAL.md` would,
after its separate replay, rule out recovering three old slider endpoints
from the sixteen-square relaxation alone. It would not refute a broader
rigidity theorem: such a theorem may retain a wider family at side S*, and
that is sufficient for the desired optimal-side conclusion. This review has
read the skeleton argument but does not substitute for its dedicated exact
replay or claim a seventeenth square exists.

Before full optimality, the outstanding links remain a proved finite
contraction on the padded window, an accepted padded all-scale terminal,
complete rational-to-root/label/frame interfaces, and global capture of every
packing with actual `S<=S*`. This stop mechanism substantially restricts the
slider domain but closes none of those links by itself.
