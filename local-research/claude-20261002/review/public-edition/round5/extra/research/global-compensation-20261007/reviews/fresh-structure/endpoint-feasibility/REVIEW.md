# Independent audit: feasibility at the exact algebraic endpoint

**Accepted.** The specified 17 unit squares form a packing in the closed
square `[0,S*]^2`, where `S*` is the exact algebraic endpoint below. This
establishes the upper bound `L17<=S*`. It supplies no global lower bound.

`check_endpoint.py` imports no producer Python and executes no producer
feasibility routine. It reconstructs the configuration directly, independently
isolates the root using rational interval arithmetic, resolves every support
absolute value, and checks the complete 68-wall/136-pair list. No optimizer,
rational-container-U feasibility claim, or resource-charge computation is
used. The final replay passed in 62.73 seconds.

## Exact target and root identity

The audited construction is precisely the pinned
`research/global-compensation-20261007/checks/endpoint_saturation.py` geometry:
start with the main `bridge.layout(t,beta)`, add `tau*v/3` to square 13, and
replace square 4 by `(S*-3/2,1/2)`. Here

    c=(1-t^2)/(1+t^2), s=2t/(1+t^2),
    d=(1-beta^2)/(1+beta^2), e=2beta/(1+beta^2),
    S*=(6+4t)/(1+2t-t^2), tau=c(c+4-S*), v=(-s,c).

The exact root `(t,beta)` is the unique common zero of the following two
polynomials in the closed box of radius `10^-12` about the stated exact
rational midpoint:

    F1 = (-t^4-t^3+t^2-3t) beta^2
       + (t^5-t^4-t+1) beta + t-3t^2-t^3-t^4,

    F2 = (2t+2t^2) beta^4
       + (-1-5t+4t^2+t^4+t^5) beta^3
       + (4-2t-2t^2+2t^3-2t^4) beta^2
       + (-1+3t-4t^2+t^4+t^5) beta -2t^3-2t^4.

    t0    = 362043893314323383453621978739944164218293243036741520638379 / 10^60
    beta0 = 330948674722739910429808533282915634174672003999685385633441 / 10^60

The checker verifies these polynomial coefficients against both the root
declaration and the literal `POLYNOMIALS` assignment in the pinned bridge;
the latter is read with `ast.literal_eval`, without executing the bridge.
The midpoint agrees exactly with the root declaration and the two rational
angle parameters in `upper-packing-certificate.json`. That rational file is
used only to identify the root seed, not to establish endpoint feasibility.

For `T(x)=x-J(midpoint)^(-1)F(x)`, the checker proves the midpoint Jacobian
invertible and bounds the derivative of T on the whole box. The exact
infinity-norm contraction bound is approximately `6.526e-11`, and the exact
midpoint residual bound eta satisfies

    eta+q*10^-12 < 10^-12,      eta/(1-q) < 10^-50.

Banach's theorem therefore establishes existence and uniqueness of the
specified root, not merely a small polynomial residual. All subsequent
intervals use the resulting root enclosure of radius `10^-50`. In
particular the exact rational bounds imply

    4.67553009360455095163 < S* < 4.67553009360455095164.

The receipt contains the exact rational contraction data and much tighter
side enclosure. All 17 center formulas and their root intervals are recorded
there. The direct square-13 formula is `R(U13,V11-1)`, where
`R(U,V)=(cU-sV,sU+cV)`. The checker proves symbolically that it equals
`R(U13,V11-1-tau/3)+tau*v/3`, so the restored target is identified exactly.

## Unit frames and absolute-value branches

Each square is `P+[-1/2,1/2]a+[-1/2,1/2]b` with its assigned frame:

| Labels | Frame |
| --- | --- |
| 1--8,15,17 | `(ex,ey)` |
| 9--14 | `((c,s),(-s,c))` |
| 16 | `((d,-e),(e,d))` |

For all three classes the checker proves the rational identities
`a·a=b·b=1`, `a·b=0`, and `det(a,b)=1`. Thus all 17 objects are exact unit
squares. Frame and coordinate denominators are separately checked.

For a unit normal n, the half-support is computed from first principles as
`(|a·n|+|b·n|)/2`. All 72 dot-product sign branches are checked: three body
frame classes, two body axes, three normal classes, two normal axes, and
both signs of the normal. Zero branches are exact rational identities;
nonzero branches have strictly one-sided rational interval enclosures.

In particular, the checker proves `c,s,d,e>0` and

    C=cd-se>0,       T=ce+sd>0.

Writing `theta=2 atan(t)` and `phi=2 atan(beta)`, these are the crucial
`cos(theta+phi)` and `sin(theta+phi)` signs. Their approximate values are
0.23465445 and 0.97207885; all sign decisions use rational bounds. Hence the
mixed-frame half-support is `(C+T)/2`. No mixed-angle sign is assumed.

## Complete containment and separation certificate

The checker tests all four containment inequalities for every square and
enumerates every unordered pair exactly once. For each pair it retains all
eight signed edge-axis choices before certifying a separating one. The
results are:

| Inequalities | Strict positive | Rational identity | Root identity | Total |
| --- | ---: | ---: | ---: | ---: |
| Walls | 53 | 15 | 0 | 68 |
| Selected pair separations | 112 | 22 | 2 | 136 |

These are the standard exact support-function inequalities, so nonnegative
gaps imply containment and pairwise interior-disjointness, including allowed
boundary touching. For each of the 24 touching pairs, the checker additionally
proves every signed SAT gap nonpositive, with at least one zero. Point and
edge contacts are retained explicitly.

The two nonrational contact identities simplify to

    gap(12,16; u) = 2 F2 / ((1+beta^2)^2 (1+t) (1+t^2)^2),
    gap(16,17; p) =   F1 / ((1+beta^2) t (1+t) (1+t^2)),

where `u=(c,s)` and `p=(d,-e)`. Both denominators are positive at the isolated
root. Every other selected zero gap is a rational identity. The receipt
records exact numerator quotients by F1 or F2 and checks zero polynomial
remainders, so near-zero floating-point evaluations are never accepted as
contacts. Across all calculations, 42 distinct reduced denominators were
certified nonzero: 17 positive and 25 negative. Interval division correctly
handles both signs.

## Pinned evidence and reproduction

- Checker: `check_endpoint.py`, SHA-256
  `3d49d934f7d66fd42b67feba38db86e1e1435a2620bc6f1b63c282a8236bf9b2`.
- Exact certificate: `endpoint-receipt.json`, SHA-256
  `f75bb799888eee7fbe68cd8ed2a2be4a93e5cff6b164ac61d698a8cc378636b5`.
- Audited endpoint source: SHA-256
  `931943b31aec96325bed92d2d8a3ae99c7bf83889ea6c14ad02a847ebe30010a`.
- Main bridge: SHA-256
  `8d5c2a8253f1aae97a243e907d08b337f334a8f27c66e3235e66a30fd8ae9f10`.
- Root declaration: SHA-256
  `ef8069b30cd1336ae01124d0f54f13b4f69741c14941f997706b7f599c23a0d9`.
- Rational angle-seed source: SHA-256
  `24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7`.

The four input hashes are checked before and after the run. From the
repository root, reproduce with:

```sh
PYTHONPATH=/private/tmp/s17-structural-deps \
  /Users/builder/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  -B research/global-compensation-20261007/reviews/fresh-structure/endpoint-feasibility/check_endpoint.py
```

Only Python's standard library and SymPy exact rational/polynomial arithmetic
are required.
