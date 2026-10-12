Editorial copy. Line references refer to the original; exact changes are listed in EDITED_LINES_ROUND2.json.

# G20S terminal: analytic assessment, not a new terminal theorem

Producer: Codex, 8 October 2026. Scope is the proposed terminal only.
No broad tree, solver, model assembly, certificate discovery or replay was run.

## Verdict

The existing box-relaxed terminal method can be re-instantiated for the proposed
slider box without adding square 4 or a new analytic inequality. The method's
analytic prerequisites remain checkable with the same code. **A successful
combined-box contraction is not yet established.** Separate one-endpoint probes
in `TERMINAL_NOTES.md` do not establish it.

The recommended first target is a feasible configuration of the sixteen labels
`{1,...,17}\{4}` in one origin-aligned container, with actual `S<=S*`, the same
corrected rational reference/axes as the accepted terminal, independent angle
increments bounded by `1/400`, and the following coordinate bounds:

| Coordinates | Closed interval |
| --- | --- |
| Every one of the 29 core position coordinates | `[-1/200,1/200]` |
| `xi_(2,1)=-a` | `[-8/25,0]` |
| `xi_(11,2)=-b` | `[-1/5,1/20]` |
| `xi_(13,2)=z` | `[-1/5,3/40]` |

For labels 11 and 13 use the rational `(u_i,v_i)` basis; all other position
coordinates use the standard basis. The corrected reference is
`p13=p13_file-(T0/3)v13`, `T0=u9_x(u9_x+4-Sref)`.
The packing source is SHA256
`24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7`.

For the eventual physical-seventeen theorem, assign sixteen **distinct actual
squares** to these roles; the remaining actual square has no pose restriction.
Non-overlap and containment still apply to all seventeen. The terminal proof
uses only the sixteen, so also proves a sixteen-square conditional statement.
The desired conclusion is `S=S*` and all 45 **exact-root**, not rational-file,
core coordinates vanish. It does not say every point of the slider box is
feasible, nor confine the sliders to the smaller original seventeen-square
family. The latter would need an additional equality-scope argument on this
wider box using the actual seventeenth square. It is unnecessary for the
optimal-side conclusion once global capture is proved.

All labels, frame changes and any container symmetry must be common across
the sixteen poses. The terminal supplies no assignment or global capture.
In `G20S_PLAN.md`, the broad G20S root uses `a<=39/125`;
the intermediate HW window and this terminal use `a<=8/25`. The initial
39/125-terminal assessment is superseded; its tiny check is preserved as
`check_constants-v1.py` and `constants-v1.json`. In particular the root cuts
`b<=1/5`, `z>=-1/5`, `a<=39/125` are hypotheses to be delivered by the broad
tree/capture; the terminal does not prove them from
position radius `1/5`. The terminal also needs the lower `b` and upper `z`
endpoints above. No unproved stop remark substitutes for either endpoint.

## What the light exact check establishes

`check_constants.py` imports only the accepted snapshot's elementary geometry
and interval library. It does not call a model, solve, symbolic audit or old
certificate checker. It reads the already accepted rational root enclosure.
Its receipt `constants.json` records the fractions rather than rounded logs.

1. **Reference parallel signs:** the only changing affine offsets are `-a`,
   `tau_11,12(0)+b`, and `tau_13,14(0)-z`. Apply the new endpoints plus
   `10^-12` padding to the old accepted exact intercept bounds. Every one of
   the eight parallel-pair branches remains valid, and all have
   `|tau|<321/1000`. The positive lower bounds for `(11,12)` and `(13,14)`
   respectively exceed `3/500` and `1/200`.

   These are **reference offsets**. The actual perturbed tangent offset can
   change sign in the proposed entry tube. The accepted parallel lemma does
   not require its sign: it uses
   `|B_actual|<=|tau|+D|m|+dr`, and pays the last two terms in its error.
   These sign checks alone do not prove that the two parallel owner options
   are the only feasible options on the initial tube.

2. **Transfer target:** if a future finite certificate puts all 45 rational
   core coordinates inside `[-1/10000,1/10000]`, while keeping the complete
   proposed slider box, direct projection gives every exact-root core
   coordinate `<1/10000+10^-15<1/5000`. The three root sliders fit the
   usual padded box
   `a in[0,8/25+10^-12]`,
   `b in[-1/20-10^-12,1/5+10^-12]`,
   `z in[-1/5-10^-12,3/40+10^-12]`.
   The raw core reduction is hypothetical here; it has not been computed.

3. **Physical side premises:** exact old root/ref data give
   `S*<p2x+1/2<Sref`. Thus actual containment and `S<=S*` force rational
   `a>0`; the exact-root right wall gives `a*>=0` despite its unpadded lower
   endpoint. These implications are false if `S<=Sref` replaces `S<=S*`.
   Square 8's horizontal reach is at least `1/2` independently of angle.
   The proposed input gives `S>=p8x+1/2-1/200>Sref-1/50`, with a margin
   greater than `149/10000`. No external scalar lower bound is needed.

4. **One explicit finite-option check:** for pair `(5,11)`, the competing
   owner-5 `+x` axis has a first-order gap upper bound
   `-0.0090770465174... < -9/1000` over the proposed entry and full slider
   box. Here the exact signed corner gap is

   `R(theta5)n . (d(b)+dh) - 1/2 - n . R(theta11-theta5)v`.

   Take the reference support corner of square 11 for `n=(1,0)`. Its linear
   upper bound is maximized over both `b` endpoints and the independent
   centre/angle endpoints. Add
   `D alpha^2/2 + alpha dr + ||v|| (2alpha)^2/2`.
   This is a rigorous exclusion of **that one option**. For position `1/100`
   and angle `1/200`, the same sufficient bound is positive
   `0.0013620838662...`; that does not prove the option feasible. It explains
   choosing the narrower first entry without assuming numerical closeness.

The first (39/125) check cost was `0.022841` CPU-seconds; the updated
8/25 target cost is recorded in `constants.json`. This proves constant/conditional
transfer lemmas, not the desired rigidity theorem. All other initial options,
the combined-box dual contraction, and actual terminal joins remain unchecked.

## What must be regenerated and checked

Exactly two source constants change from the accepted box-relaxed instance:
the slider tuple in `uniform.initial_bounds`, and its padded copy in
`bridge.run`. Change both together. `rigidity.initial` derives its box from
the former; unchanged `verify.py` compares it with the latter. The finite
header changes to radius `1/200`, angle factor `1/2`, parameter scale `1`.
`rigidity.py`, `relational.py`, `root_geometry.py`, `verify.py`, the packing
reference and root certificate need no mathematical or schema change.

The 52 exact identities are slider-independent affine identities. Their
coefficient/remainder implementation is already audited, including the full
two-owner parallel union, independent angles, shared products, closed SAT
coverage and contact corners. All norm bounds `D`, product endpoints,
coefficient suprema, McCormick bounds and remainders must nevertheless be
rebuilt for this box. Every all-scale error has nonnegative powers of the
physical core norm `R`; `R<=epsilon=1/5000` is substituted after exact base
gap cancellation. Square 8 gives normalized `-1<=(S-S*)/R<=0`. No uncertain
constant is divided by an arbitrarily small `R`.

The complete gate is:

- Compare the **exact 52-label roster** with the accepted original roster,
  including 11 unique-owner and 8 parallel pairs. Counts alone are inadequate:
  `tight_labels()` derives its roster from the changed finite model and can
  silently lose a row. `option_audit` can then report 19 pairs without that
  unique-owner constraint. A dropped row is safe for enclosure but does not
  establish this intended mechanism.
- Check all 152 owner/axis/sign possibilities on the padded root box and
  epsilon cube; independently audit the fixed-sign reference offsets and
  all 52 symbolic identities. Reconstruct the normalized model independently.
- Discover and exactly replay a fresh all-scale certificate with maximum
  core ratio **strictly below one**. Do this before finite capture;
  the combined widening may weaken the relaxation despite separate successful
  endpoint probes. Old saved dual weights may only be reused after full
  recomputation of every residual on the new model.
- Discover and replay finite capture from the proposed entry to core
  `<=1/10000`; replay the actual bridge output and padded-slider inclusion;
  run unchanged `verify.py` on the complete new chain.
- Independently bind the actual broad-tree final stores/arcs and header to
  this new entry. The accepted frozen WX2.5.1 sixteen-label checkers can
  express it. Terminal arc tests must use their actual composed endpoints
  and `|sin endpoint|<=alpha-alpha^3/6`, with positive cosine; a nominal angle
  label alone is not a join proof. Merely replacing the old terminal header
  invalidates previous tree terminal tests unless they are checked anew.

No contact-force positivity, local-minimum assumption or zero-force contact
omission is used in the terminal reasoning: all its rows are necessary
conditions for actual non-overlap/containment. Additional contacts, degenerate
contacts, and an arbitrary free square can only restrict feasible packings.
This does not justify using omitted zero-force contacts to prove local
minimality; no such conclusion is needed here.

## Limits of the method

A narrower entry helps the finite stage but cannot by itself repair a normalized
combined-box obstruction. Splitting the `a` interval also requires padding its
positive lower endpoint: unchanged `bridge.py` assumes that endpoint is zero.
Broad-tree certificates and their complete independent checks are separate
obligations from this terminal assessment.
