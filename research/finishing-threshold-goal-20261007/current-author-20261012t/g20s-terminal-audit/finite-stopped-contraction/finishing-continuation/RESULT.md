# Six complete rounds; numerical timeout on the next proposal

The run completed global rounds10–15. A native HiGHS time limit was reached
on round16's second objective, after one exact bound had been recorded. This
is a proposal failure, not physical infeasibility and not failure of an exact
bound. No target claim, retry or extra model follows from this package.

The last complete box is round15: maximum raw position radius
101779367707/10^15 =0.000101779367707, maximum angle radius
107198988591/500000000000000 =0.000214397977182. Thus the all45-core1/10000
target is not reached. The previous persistent negative-angle11 bound began
contracting in round10; all six full models retain11 unique+8 parallel pairs.

| global round | rows | maximum position | maximum angle | CPU seconds |
|---|---:|---:|---:|---:|
|10|773|.001079614796529|.002293062353341|2.106953|
|11|773|.000827079921682|.001750321730253|2.092389|
|12|773|.000547511971755|.001156282690892|2.098731|
|13|773|.000323778192326|.000682629567868|2.136383|
|14|773|.000183336072291|.000386295358342|2.120023|
|15|773|.000101779367707|.000214397977182|2.138027|

Certificate.final_bounds remains exactly the outgoing box of round15. The
partial_round field and model16 file are preserved as provenance, not used
as a simultaneous contraction or continuation seed. The complete six rounds
contain552 signed bounds and4638 rows. Independent acceptance is a separate premise from this producer result.

Total process cost14.945649CPU-s, wall14.945602s.
The failed objective and model preparation are included in that process cost.
The global process cap was not reached; the native per-proposal time setting
was1 second. No diagnosis of the timeout mechanism is asserted here.
