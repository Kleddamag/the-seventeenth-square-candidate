# Exact formulas for an attained upper packing

These are literal formulas extracted from the already accepted H256 checker. All arithmetic is in the ordered real field containing the isolated root (t,b), and `half=1/2` exactly. The symbol `side` equals the algebraic endpoint L. Python-style `*`, `/`, and tuple notation denote ordinary exact operations; no float evaluation is intended.

**Labels in this table are the original construction labels. They are not the later capture labels.** A separate direct full-seventeen upper certificate uses another member of the family; its contact roster must not be substituted into this construction.

The auxiliary quantities are defined in this order:

```text
half = 1/2
(d_t, d_b) = (1 + t * t, 1 + b * b)
(c, s) = ((1 - t * t) / d_t, 2 * t / d_t)
(d, e) = ((1 - b * b) / d_b, 2 * b / d_b)
k_denom = 1 + 2 * t - t * t
side = (6 + 4 * t) / k_denom
(h, k) = ((c + s) / 2, (d + e) / 2)
(alpha, gamma) = (c * d - s * e, c * e + s * d)
x = half + (2 + c * s + 3 * s - s * side) / c
y = 3 * half + (2 + 3 * c - c * side) / s
aa = d * (x + half) - e * (side - 1) + half
bb = (d + e) * (side - 1) - half
(u10, v10) = (3 * half + c * s + 2 * s, c * (side - 1) - s - half)
(u11, v11) = (c + 2 * s + half, 2 * c + (c * c - s * s) / 2 - 1)
(u12, v12) = (u11 + 1, v10 - 1)
u13 = 2 * c + s + half
(u14, v14) = (u13 + 1, v10 - 2)
(r, hh) = (side - 3 * half, v11 - 1)
ell = c + s / 2 + half
slack = c * (c + 4 - side)
(lambda6, lambda13) = (r - slack / (3 * s), hh - slack / 3)
```

`rotate(uu,vv) = (c * uu - s * vv, s * uu + c * vv)` is the fixed orthogonal map with first axis `(c,s)`. Here `c²+s²=d²+e²=1` by their rational parametrizations.

| Construction label | Centre | Orthonormal side directions |
|---|---|---|
| 1 | `(half, half)` | `(1,0), (0,1)` |
| 2 | `(3 * half, half)` | `(1,0), (0,1)` |
| 3 | `(half, 3 * half)` | `(1,0), (0,1)` |
| 4 | `(half, side - half)` | `(1,0), (0,1)` |
| 5 | `(side - half, half)` | `(1,0), (0,1)` |
| 6 | `(lambda6, half)` | `(1,0), (0,1)` |
| 7 | `(side - half, 3 * half)` | `(1,0), (0,1)` |
| 8 | `(side - half, side - half)` | `(1,0), (0,1)` |
| 9 | `(h, 2 + h)` | `(c,s), (-s,c)` |
| 10 | `rotate(u10, v10)` | `(c,s), (-s,c)` |
| 11 | `rotate(u11, v11)` | `(c,s), (-s,c)` |
| 12 | `rotate(u12, v12)` | `(c,s), (-s,c)` |
| 13 | `rotate(u13, lambda13)` | `(c,s), (-s,c)` |
| 14 | `rotate(u14, v14)` | `(c,s), (-s,c)` |
| 15 | `(x, side - half)` | `(1,0), (0,1)` |
| 16 | `(d * aa + e * bb, -e * aa + d * bb)` | `(d,-e), (e,d)` |
| 17 | `(side - half, y)` | `(1,0), (0,1)` |

The fixed slider choice is `lambda6=r-slack/(3*s)` and `lambda13=hh-slack/3`; the accepted interval guards prove `s>0` and `slack>0`. All containment and separation claims rely on the source-bound accepted wall/pair certificate, not on this syntactic extraction. Tangent pairs and exact wall contacts are included.

Source: `research/finishing-threshold-goal-20261007/current-author-20261012t/contract-stage-20261009-1252/reflection-closed/chirality-coupling/exact-root-extension/producer/inputs/H256_CHECKER.py`, SHA-256 `2d3b9d6e361e8790bb2f6d14cf4f11d44b473fbc828bb080d7d3a1939d5c2145`. The literal `_layout` body is also retained in UPPER_LAYOUT.py.txt.
