# Independent program for the tight enclosure of the endpoint root and of L

`own_endpoint_enclosure.py` was written by an independent reader, from scratch, with the standard library and exact rationals only. Its header describes the method (a component-wise Krawczyk test with exact Taylor bounds) and says that it shares no code with the producers' checks `check_endpoint_enclosure.py` and `check_endpoint.py`.

It establishes: exactly one common zero of F and G in the box of `STATEMENT.md`; that zero in a box of radius 10^-100; L strictly inside the tight intervals that the record uses; L > 4, L < R < C < U, R - L - 2 eps > 0. It reads the definitions from `STATEMENT.md` and reads six other files as data for its comparisons.

## What was changed for this edition

File paths only, and nothing else (lines 43 to 52 of the file as it was written):

| Line | As written | In this edition | Why |
|---|---|---|---|
| 43 | `REPO = Path("<absolute path of the repository on the build machine>")` | `REPO = Path(__file__).resolve().parents[2]` | the root is found from the file's own location |
| 44 | the statement file inside the project's earlier package | `REPO / "STATEMENT.md"` | the same bytes (SHA-256 `dd73365b...`), at the root of this edition |
| 45, 46 | `EXACT_ENDPOINT_AND_CASES.json` of the sealed record | `.../second-order-20261010/theorem/EXACT_ENDPOINT_AND_CASES.json` | the sealed record is not in this edition |
| 51, 52 | the producers' receipt at its first, provisional place | `ENDPOINT_ENCLOSURE_CHECK.json` in the producers' packet | the producers' receipt, as listed in their roster |
| 45, 47, 51 | the producers' folder `window-capture/` | `current-author-20261012t/` | the producers reissued their files under this folder name |

## How to run it

```
python3 independent/endpoint_enclosure/own_endpoint_enclosure.py            # must end "RESULT: PROVED ...", 39 lines "[ok]"
python3 independent/endpoint_enclosure/own_endpoint_enclosure.py --control  # F with one coefficient changed by 1: must end "RESULT: NOT PROVED", exit code 1
```

`out_real.txt` and `out_control.txt` are the outputs of these two commands in this edition on the build machine. `check.py` runs both at level 2 (check `independent_endpoint`).
