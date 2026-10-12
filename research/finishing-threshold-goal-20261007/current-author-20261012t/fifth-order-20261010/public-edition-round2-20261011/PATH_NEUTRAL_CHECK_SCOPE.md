# Checks affected by path-neutral copies

PATH_NEUTRAL_READERS.json gives actual observed reads, not an inferred dependency list. Eleven check entries read affected retained inputs. The final replay uses the neutral inputs.

- `bfbe_pins` hashes the complete bytes of named evidence, including the paths inside logs and JSON. Its expected hashes therefore change; it does not interpret the build account or the session UUID.
- `capacity`, `frame`, and `wall_triggers` read the theorem manifest. They follow and hash selected class/root file references and compare exact geometric data; the neutralized proof-reference paths are not geometric hypotheses.
- `finite_1` to `finite_4` and `finite_join` read the certificates. The changed fields there are runtime executable / diagnostic path metadata. Their input and prefix-certificate hash checks are rebound. Numeric model rows, dual arithmetic, boxes and terminal conclusions are unchanged.
- `normalized_five_rounds` reads preparation metadata and hashes its inputs. The replaced source-directory string is not a numerical parameter.
- `bc_composition` hashes certificate and source bytes and reads three acceptance logs. It compares the fixed log tokens `RESULT: ACCEPTED`, `ok    header tube = expected tube`, and the listed JG terminal-leaf token, and extracts the certificate SHA-256. None contains the replaced account or UUID. Its three path expressions were explicitly changed to select the neutral log copies; PATH_NEUTRAL_LOCATOR_CHANGE.json binds that finite locator edit. All assertions, arithmetic and control flow are unchanged.

This is a bounded inspection of these named entry scripts and their observed replay closure. It is not a new independent audit of every imported source or a proof of the historical executions. The 31 current checks and the exact mathematical projections are separately checked. Raw fresh outputs are retained privately where a public path-neutral copy was necessary; those copies are listed in PATH_NEUTRAL_REPLAY.tsv.
