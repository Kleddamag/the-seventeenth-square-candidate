Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line. This report reviewed the earlier executions of the capture computation, named here by neutral designations (table EARLIER_EXECUTIONS.tsv); the audit of the execution carried in this edition and the complete row comparison with the earlier ones are separate evidence.

REPORT on the S6 joins: four signed forms (state of the files from 17:26 to 17:32)

VERDICTS
1. PS_5^17 ENDp -> BRANCH_JPG17p_L05: FOLLOWS WITH CONDITION (C1). Clause: "tau17 >= 1/20" (theta17 in [-pi/4, pi/4)). Form: T17 slot "[1/20, 207107/500000]". The seam 1/20 is owned by p and the slot is closed there; the upper end exceeds tan(pi/8).
2. PS_6^17 ENDm -> BRANCH_JPG17m_L06: FOLLOWS WITH CONDITION (C1). Clause: "tau17 <= -1/20". Slot: "[-207107/500000, -1/20]". The seam -1/20 and the 45-degree seam (owned by m) are inside.
3. PS_16^9 ENDa -> BRANCH_JPA_L16, region JPA_exact_v5: FOLLOWS WITH CONDITION (C1, C2). Clause: "x9 > 53/100 and 591183/1408817 <= t9 <= 44941/100000" (17:22 packet; older text "< 1"). Slot: "[-408817/1000000, 0]", whose quarter-turn image is t9 in [591183/1408817, 1]. Lower ends coincide exactly; both versions of the predicate are contained, without KEY_W.
4. PS_1^17 ENDm -> BRANCH_JPG17m_L01: FOLLOWS WITH CONDITION (C1, W3). Clause and slot as in 2. Inventory 1726 already lists the form with this clause and root, but as incomplete.

CHECKED FOR ALL FOUR (exact fractions; copy of D's adm.py plus my own script)
- Against the original two-sign file: M, target and WC slots are identical, and the trigger polygon is identical. Only the trigger angle is cut to one sign or end.
- Thresholds are 4, 4, 0, 0 and bound 23, as in the original; 4 + 4 + 15 = 23. Receipts give 23 minus 22, 1, 19, 17 units, all strict.
- The parent's centre set (S_17 clipped; label 9's off-wall rectangle) lies inside the trigger polygon. M, trigger and parent set are strictly separated from the target. T9 touches WC only on x = 53/100, which the wall owns.
- Target admitted: JPG17p 11b68ec1... and JPG17m 18550e41... (the hashes in RECORD_EJPG17p_v5 / RECORD_EJPG17m_v5, STATUS PROVED), JPA adcf0d1b... (manifest pin). Least margins: 4.7e-8, 4.3e-17, 1.9e-7, 9.5e-7.
- Three negative controls (wrong label, widened arc, shifted box) fail as they should.
- Pins: both receipts name the stored exact/classes.json (an alias hash), not the join's hash. I confirmed JSON equality with the joined bytes for all four. The alias is documented in each README and, for forms 1 to 3, in Codex's audit.
- Certificate hashes and bounds in the inventory equal the receipts (forms 1 to 3).

FINDINGS
C1. GAP, shared, not caused by signing. All four need the half-marker occupied (class M). FRAME_MARKER is "RECEIPT OPEN" (Q1) in the 17:22 packet, yet FRAME_ASSIGNMENT, which depends on it, is COUNTED. L_17, KEY_W and COARSE_LOOSE_CAPACITY are COUNTED.
C2. GAP. JPA_exact_v5 has no PROVED record (no RECORD_EJPA_v5; manifest "RECEIPT OPEN"). Form 3 discharges the clause, not the region.
W1. WEAK. "extra_premises: []" and the comment "All original extra L premises retained" are vacuous: the originals list none. L_17, label 9's frame and the marker are used all the same (D's S1).
W2. WEAK. The comment "high thresholds changed" is false for H4T4. Harmless.
W3. WEAK. Form 4 has no Codex budget audit and is not complete in inventory 1726.
W4. WEAK. The option-lemma acceptances are Codex reviewing Codex.
No opposite sign and no enlarged target is used anywhere.

(e) REMAINING OF THE FIVE PAIRS
- PS_1^17: p side (JPG17p_L01).
- PS_5^17: m side (JPG17m_L05).
- PS_6^17: p side (JPG17p_L06).
- PSS_16^3: both sides (JPG3m_L16, JPG3p_L16).
- PS_16^9: nothing. No JPB clause exists; the lower exit is removed by KEY_W.
Correction to the list: the 17:22 packet also lists JPG17m/p_L02 and JPG3m/p_L11 as open, and I found no receipt folder for either. JPG3m/p_L07 has an exact two-sign receipt (first execution of CLASS_PSS_L07_T03, 17:22).

NOT CHECKED
- Receipts and certificates were not re-run.
- The checkers' reading of quarter-turn lifts.
- The proofs of FRAME_ASSIGNMENT, KEY_W, L_17.
- The contents of the acceptance replays.
- Whether labels 2 and 11 were closed somewhere I did not look.

Scripts: s6.py, ctl.py, adm_copy.py in <reviewer scratch>/

