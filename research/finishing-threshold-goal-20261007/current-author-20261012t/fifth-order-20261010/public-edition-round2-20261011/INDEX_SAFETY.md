# Finite-size safeguards for the selected Node executions

The six signed midpoint shifts in `verify_classes_wb.js` require sums of **array indices** below 2^31. They do not require the total number of two-dimensional cells below 2^31. The checker has no universal size guard for arbitrary future inputs; this note supplies a bound for the selected 98 certificates only.

`INDEX_SIZES.json` binds each selected certificate to its roster hash and counts its physical sites and angle rows. The maximum number of sites is **83,128**, attained by PW_2; the maximum row count is **18,000**. No sweep was run.

For one row, all atom rectangle endpoints are site projections plus or minus the same halfwidth: maxima and minima over atom sites are still projections of individual sites. Consequently each coordinate array has at most 2N+4 entries (including the four container-envelope vertices), independent of how many Boolean atoms are expanded or merged. For N<=83,128 this is **166,260**. The bisect midpoint numerator is at most **332,520**, below 2^31.

There are at most 166,259 leaves on the swept coordinate axis. The next power-of-two capacity is at most **262,144**. The allocated tree arrays have at most **524,288** entries, and every recursive midpoint sum is at most 524,288, also below 2^31. The code's child indices use ordinary multiplication/addition, and fit these arrays.

For comparison, the two-dimensional cell count is at most **27,642,055,081 per row**, and its sum over 18,000 rows at most **497,556,991,458,000**, below 2^53. These are rigorous upper bounds, not measured maxima of realized grids. They are large enough that a claim “all cell counts are below 2^31” would be unjustified. Cell counters use Number additions, not signed bit shifts, and these bounds keep those integer sums exactly representable. The separate charge-magnitude safeguard <2^50 remains required.

Verified: all 98 selected certificate SHA256 values and site/row counts; the source formulas at the bound Node checker hash; the integer bounds above. Not verified here: realized maximum grid dimensions across every angle row, or any new charge sweep. The upper bounds already discharge the index-size concern for these data.
