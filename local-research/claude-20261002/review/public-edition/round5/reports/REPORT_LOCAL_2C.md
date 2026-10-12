Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line.


All six wx-cert-2 controls on the real HW certificate FAIL in both frozen checkers at the altered node. W3 fails at the child, but through a `par` declaration that needed the assumption, not through the assume-list rule.

**Read ranges:** the Node wx-cert-2 lower-bound path (monBound 2506-2515, lowerBound 2525-2612, lowerBoundReference 2614-2629) is inside the range I read against SPEC 5; the Python counterpart was NOT read by me: wxcheck_v30.py 2002-2105 (mono_interval, _mono_interval_int, _fact_scaled, term_product, remainder, lower_bound, lower_bound_reference), also 2106-2257 (centred path), 2286-2326 (check_step) and the polynomial helpers 400-478. I no longer have the text of my finding F4, so I cannot restate it here.

**Setup**
- Source: `bigbox/gen17/HW_tree.jsonl.gz`, sha256 c974a9c5dce91e7d..., header schema wx-cert-2, no `labels` field (sixteen labels).
- Each variant is a full copy of the certificate with one node line changed, written as .gz, run as a normal full-certificate run, then removed. No `--node` was used.
- C1 is `python -I -B checker/wxcheck_v30.py FILE`; C2 is `node --max-old-space-size=6000 checker2/wxcheck2_v30.js FILE`. Unlike the runs of record I passed no `--json` and used 6000 instead of 12000 for the Node heap limit.
- Targets were the earliest nodes in the file whose first round contains the feature.

**Results** (every run: rc 1, first line FAIL, first failing node = the altered node)

| Variant | Node (line) | Change | C1 failing place | C2 failing place | As expected |
|---|---|---|---|---|---|
| W1 | root.1.1.1.1.1.1.1.1.1.1 (244) | round 1 stored cut `A:10:15:hi` set to the smallest certified upper bound of this round minus 1e-18 | round 1 store: cut A:10:15:hi is not implied | rounds[0].store.cuts: cut A:10:15 <= ... is not implied (old cut: none, certified upper bound 400939826845077/281474976710656) | yes |
| W2 | root.1.1.1.2.2.2.1.1.2 (296) | round 1 stored `rarc[1-3].lo` rotated by the rational rotation with t = 1e-12; its sine is 4.0e-13 above both the old R^- and the certified lower bound of Sr:1:3 | round 1 store: St^- of the pair 1-3 is not implied | rounds[0].store.rarc[1-3].lo: sine ... is tighter than certified (old R^- sine and certified bound both printed) | yes |
| W3 | root.1.1.1.2.2.2.1.1.2 (296), child of the sign split root.1.1.1.2.2.2.1.1 (295) | sign of its last (ysign) assumption flipped | round 1 pairs[9]: par declaration (5, 11, a+a+, P-): neither YU <= 0 nor the sign assumption Y <= 0 | rounds[0].pairs[9]: par declaration P- (5, 11, a+a+): neither YU <= 0 nor a sign assumption Y <= 0 | yes for FAIL at the child; no for the rule (see below) |
| W4 | root.1.1.1.2.2.2.1.1.2 (296) | round 1, step 3, term 7: `asg:5:11:a+a+:m` changed to `asg:5:11:a+a+:p` | round 1 step 2: the node has no sign assumption (5, 11, a+a+, +1) | rounds[0].steps[2].terms[6]: fact asg:5:11:a+a+:p is not available: no matching sign assumption | yes |
| W5 | root.1.1.1.1.1.1.1.1.1.1 (244) | round 1, declaration 1: `par` (1,3) kind Pk, class a+a+ changed to b+a+ | round 1 pairs[0]: par declaration (1, 3, b+a+, Pk): option (1, 3, a, +1) is not excluded | rounds[0].pairs[0]: same declaration, option (1, 3, a, +1) is not excluded on the start store | yes |
| W6 | root.1.1.1.1.1.1.1.1.1.1 (244) | round 1, step 1: added term `["0", ["wsup:5:xlo:p"]]`; the arc of label 5 does not contain the x-axis direction | round 1 step 0: the store arc of square 5 does not satisfy the sign conditions of SPEC 4.8: no wsup facts | rounds[0].steps[0].terms[2]: fact wsup:5:xlo:p is not available: sign conditions of SPEC 4.8 do not hold | yes |

W6 also shows that availability is tested for a term with multiplier 0 on the wx-cert-2 path, in both checkers.

**W3 did not reach the assume-list rule.** Both checkers check the node before pairing it with its parent, and this child's first round has a P- declaration that needs the flipped assumption, so the rejection came from that declaration. The tree-level comparison of a sign-split child's assume list is therefore covered only by my wx-cert-3 controls E1 and E3, not on a wx-cert-2 file. That comparison code (checkChild in Node, read by me) has no schema branch.

**Not done**
- A W3b variant on a sign-split child whose rounds do not use the assumption (no `asg` name, no P+/P- declaration of that pair and class), which would hit the assume-list rule itself.
- No control on G20S.
- No `par:` term with its declaration removed (W5 was done at the declaration only).
- No control on kind Ps or on a stored relative-arc `hi` endpoint.
- No W0; the rerun by another reviewer is the positive control.
- No reading of the Python lines named above.

Script and results are in <reviewer scratch>/: `hw_controls.py`, `hw_results.txt`.


