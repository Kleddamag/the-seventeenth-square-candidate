Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line.

VERDICT: SAME STATEMENT (no WRONG, no GAP; two WEAK, documentary). State of the files at 18:31, 10 Oct.

(1) POSE SETS. Own script: marker.json (520ce3ce, byte-identical to restriction.json) and FRAME_MARKER_CLASS.json (aa8b1410) have equal slots as rationals: same six vertices, gate [-207107/500000, 207107/500000], frame centre (1169/500, 1169/500), symmetry orbit. Hexagon strictly convex, mirror-invariant, so 4 distinct D4 images. Gate: r^2+2r-1 = 309449/250000000000 > 0; the three quarter-turn lifts cover [-1,1], so "any direction". Python code read at source: ClassRow inherits the restricted checker's `_angles_inside`, `_forms`, `_slot_interval`, same D4 tuple, same (-b,-a) pairing; closed polygon x closed arc in both.

(2) INEQUALITY. Original: "at most 16 squares have a pose outside E*", needs k*Gamma > M, k=17. Class: "sum of tau(pose) ... is less than 17", threshold 0 inside, 1 outside. Identical count, same strictness, same side 4675531/1000000. Threshold 0 gives kind -1: exempt only if the whole closed cell x row interval lies in ONE slot image, the restricted rule. No weakening.

(3) CERTIFICATE. Both receipts name 4f6fd341 and aa8b1410 (= REQUEST.json pins); they differ only in implementation, checker hash, timestamp. Certificate: 9,000 rows, gapless from 0 to exactly 207107/500000, every row and its mirror inside a gate lift, 17g-M = 13. Slices: 12+12 tile 0..8999, all passed, Python = Node per row. Against the historical restricted slices: unrestricted minimum, cell count and deficient slabs equal in 9000/9000 rows. Least default charge 999999994 >= Gamma 998328901.

(4) USE. FRAME_L9.md: "The accepted orbit-marker exclusion forces a marker image occupied"; the half-marker comes from reflection, not from the marker row. Exactly the receipt's consequence. 173 manifest class files carry the literal hexagon as high class.

FINDINGS
- WEAK-1: verify_conversion_identity.py asserts only JSON equality and 17g-M=13; its "identical ... orbit and quarter-turn semantics" is not computed. It holds by the Python code above; Node twin only skimmed.
- WEAK-2: CONVERSION.md predates the receipts ("No spatial row charge sweep was run here"); it is no proof of the executed statement by itself.
- Note: Node receipt key "verify_classes.js" carries 7f6b2347, the hash of verify_classes_wb.js.

(5) REMAINING FOR IMPORT
- Run audit_marker_class_receipt.py (17f0f09b, "PREPARED_NOT_EXECUTED_NO_RECEIPT_ACCEPTANCE") on the receipt folder.
- Manifest: FRAME_MARKER is "RECEIPT OPEN", accepted_by null, pins lack the class file and receipts 9fa41211 / 0943e2ea; marker_checker_scope_Q "OPEN_CLASS_RECHECK_ALREADY_REQUESTED"; REQUEST.json status pending; all CONDITIONAL_ON_FRAME_MARKER flags; PROOF_TEXT line 64 "[OPEN: ...]".
- Record the join: class slots = literal marker.json, which FRAME_L9.json still binds.

NOT CHECKED: authenticity of the twelve cloud slices (refs.txt commits); Node class checker line by line; no row re-executed; the adapter not run.

Scripts (<reviewer scratch>/): conv_check.py, use_check.py, minima_check.py.

