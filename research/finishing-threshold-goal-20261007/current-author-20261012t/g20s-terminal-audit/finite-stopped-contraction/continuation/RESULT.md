# Six further rounds completed; one angular face remains

The continuation stopped after global round9, with all six new
rounds complete and no additional model or solver call. The target remains
unreached: maximum raw position radius7336628287/6250000000000
(0.00117386052592), maximum angle radius1/400. All models retain11 unique
pairs and8 parallel pairs, with0 omitted pairs and0 tangential crossings.

| global round | rows | maximum position | maximum angle | CPU seconds |
|---|---:|---:|---:|---:|
|4|761|0.002804686409201|0.0025|2.053882|
|5|773|0.002285977620892|0.0025|2.108562|
|6|773|0.001511947906936|0.0025|2.114561|
|7|773|0.00117476726036|0.0025|2.112407|
|8|773|0.001174165992423|0.0025|2.124326|
|9|773|0.00117386052592|0.0025|2.143884|

Row growth again comes from distinct valid midpoint/zero tangent envelopes
in the unchanged quadratic generator. Each of the4626 saved rows is a replay
obligation; the number773 is not assumed by the proof.

From round5 onward, the only original angular endpoint still attained is
theta11=-1/400 (index44). Round9 theta11 has upper bound
36597225293/200000000000000, about0.000182986126465. Other requested raw
coordinates are:

- h22 in[-13566837587/250000000000000,106361359789/1000000000000000];
- h23 in[-70962756433/1000000000000000,9790021093/125000000000000];
- theta12(index45) in[-24458888731/1000000000000000,17937966831/100000000000000].

The last two rounds still reduce h22 upper .000183619229084 to .000106361359789,
h23 upper .000136082455733 to .000078320168744, and theta12 upper
.00030407256215 to .00017937966831. Side-gap upper falls
.000008603264225 to .00000521584988. Thus many coordinates keep contracting,
even though the global position and negative-angle11 bounds now nearly stall.
All exact endpoint data, including labels/signs, are in bounds-diagnostic.json.

This resembles the sole-angle11 mode in the separate small normalized proof,
but that proof and its face monitor cannot be applied automatically to a raw
finite box of radius.0025. No new transfer, normalized-face premise or
physical infeasibility has been proved by this resemblance.

Process cost12.993185CPU-s, wall12.976690s; plus1CPU-s conservative preparation,
diagnostics and sealing gives a total of13.993185CPU-s.
The certificate contains552 new exact bound proposals, all incoming/outgoing
100-coordinate boxes, every model and native one-thread readback. It binds
the accepted prefix review5fd61399... and restores its complete final box.
This producer record does not supply independent continuation replay; no finite-entry
theorem or global optimality claim is made here.
