# Preserved fail-closed binding event

During the preflight, the manifest existed with digest
063acc5c6d6314d9800a9274ebbccb0549186eeca83ec841c89b424f46bbdb87.
The first
independent binding run rejected that digest at its initial manifest assertion
when the producer completed the final metadata seal. No mathematical check was
accepted under the stale pin.

The producer then explicitly froze manifest
5a3aab61d2a5f5b08090fc4fc8e0ad67482007b06e370d0cbdc4db255cdf9ead.
The corrected binder retains and checks the previously inspected exact hashes
of PROOF.md, check_stops.py, dependencies.json, receipt.json and
root-interface.json before auditing the complete final manifest. Those
mathematical inputs are unchanged. This is a preserved source-freeze timing
failure, not an excluded or unhandled geometric case.
