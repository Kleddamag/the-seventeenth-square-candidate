Note for this edition: this is a report of an independent reader on the project's sealed record of 10 and 11 October 2026. File names, item letters and line numbers in it refer to that record. Passages about the logistics of the review were removed; the findings are unchanged. The table EDITED_LINES.tsv lists every changed line.

Columns: tree | checker | certificate sha256 verified | exit | first line | nodes/infeasible/terminal/split/steps/terms now | same of record | comparison | wall | peak memory
JQ | C1 | yes | 0 | PASS | 1/1/0/0/1/48209 | 1/1/0/0/1/48209 | EQUAL | 30 s | 454 MB
JQ | C2 | yes | 0 | PASS | 1/1/0/0/1/48209 | 1/1/0/0/1/48209 | EQUAL | 10 s | 729 MB
JPG15p_v5 | C1 | yes | 0 | PASS | 23/15/0/8/15/502001 | 23/15/0/8/15/502001 | EQUAL | 371 s | 549 MB
JPG15p_v5 | C2 | yes | 0 | PASS | 23/15/0/8/15/502001 | 23/15/0/8/15/502001 | EQUAL | 75 s | 1268 MB
JPG17m_v5 | C1 | yes | 0 | PASS | 31/18/0/13/18/748232 | 31/18/0/13/18/748232 | EQUAL | 531 s | 657 MB
JPG17m_v5 | C2 | yes | 0 | PASS | 31/18/0/13/18/748232 | 31/18/0/13/18/748232 | EQUAL | 110 s | 1316 MB
JPG3m_v5 | C1 | yes | 0 | PASS | 36/22/0/14/22/993869 | 36/22/0/14/22/993869 | EQUAL | 711 s | 729 MB
JPG3m_v5 | C2 | yes | 0 | PASS | 36/22/0/14/22/993869 | 36/22/0/14/22/993869 | EQUAL | 140 s | 1314 MB
JPG3p_v5 | C1 | yes | 0 | PASS | 36/22/0/14/22/988844 | 36/22/0/14/22/988844 | EQUAL | 752 s | 695 MB
JPG3p_v5 | C2 | yes | 0 | PASS | 36/22/0/14/22/988844 | 36/22/0/14/22/988844 | EQUAL | 140 s | 1322 MB
JPG17p_v5 | C1 | yes | 0 | PASS | 48/32/0/16/32/1176714 | 48/32/0/16/32/1176714 | EQUAL | 888 s | 629 MB
JPG17p_v5 | C2 | yes | 0 | PASS | 48/32/0/16/32/1176714 | 48/32/0/16/32/1176714 | EQUAL | 180 s | 1531 MB
JPG15m_v5 | C1 | yes | 0 | PASS | 61/39/0/22/39/1453516 | 61/39/0/22/39/1453516 | EQUAL | 1007 s | 595 MB
JPG15m_v5 | C2 | yes | 0 | PASS | 61/39/0/22/39/1453516 | 61/39/0/22/39/1453516 | EQUAL | 195 s | 1883 MB
G20S | C1 | yes | 0 | PASS | 679/302/38/339/218259/30019872 | 679/302/38/339/218259/30019872 | EQUAL | 626 s | 350 MB
G20S | C2 | yes | 0 | PASS | 679/302/38/339/218259/30019872 | 679/302/38/339/218259/30019872 | EQUAL | 301 s | 2692 MB
HW | C1 | yes | 0 | PASS | 579/289/1/289/156260/22540696 | 579/289/1/289/156260/22540696 | EQUAL | 461 s | 1009 MB
HW | C2 | yes | 0 | PASS | 579/289/1/289/156260/22540696 | 579/289/1/289/156260/22540696 | EQUAL | 210 s | 2529 MB
JG | C1 | yes | 0 | PASS | 113/56/1/56/56/2670577 | 113/56/1/56/56/2670577 | EQUAL | 1594 s | 912 MB
JG | C2 | yes | 0 | PASS | 113/56/1/56/56/2670577 | 113/56/1/56/56/2670577 | EQUAL | 336 s | 2334 MB
JPWS_v4 | C1 | yes | 0 | PASS | 110/70/0/40/70/2982299 | 110/70/0/40/70/2982299 | EQUAL | 1975 s | 691 MB
JPWS_v4 | C2 | yes | 0 | PASS | 110/70/0/40/70/2982299 | 110/70/0/40/70/2982299 | EQUAL | 401 s | 2648 MB
JPW13 | C1 | yes | 0 | PASS | 255/163/0/92/163/7133642 | 255/163/0/92/163/7133642 | EQUAL | 4655 s | 761 MB
JPW13 | C2 | yes | 0 | PASS | 255/163/0/92/163/7133642 | 255/163/0/92/163/7133642 | EQUAL | 957 s | 3412 MB
JPA_v5 | C1 | yes | 0 | PASS | 416/281/0/135/281/12439907 | 416/281/0/135/281/12439907 | EQUAL | 8449 s | 744 MB
JPA_v5 | C2 | yes | 0 | PASS | 416/281/0/135/281/12439907 | 416/281/0/135/281/12439907 | EQUAL | 1674 s | 6997 MB
EQUAL means more than the six counts: every output line of the program (counts incl. accepted, rounds evaluated, zero_steps, declarations, tree depth; root id; packing hash; certificate hash; hash of the uncompressed stream; labels; S_floor; schema) is the same text as in the ACCEPT log of record, apart from the run time and the printed path.

Pinned post-check h_report30.py (0314aa1f...), with the new --json files, the EXPECT file of record and FROZEN_30.json: tree | exit | last line | ok lines | lines that are not ok
JQ | 0 | RESULT: ACCEPTED | 50 | none
JPG15p_v5 | 0 | RESULT: ACCEPTED | 50 | none
JPG17m_v5 | 0 | RESULT: ACCEPTED | 50 | none
JPG3m_v5 | 0 | RESULT: ACCEPTED | 50 | none
JPG3p_v5 | 0 | RESULT: ACCEPTED | 50 | none
JPG17p_v5 | 0 | RESULT: ACCEPTED | 50 | none
JPG15m_v5 | 0 | RESULT: ACCEPTED | 50 | none
G20S | 0 | RESULT: ACCEPTED | 40 | none (one information line more than the record: "root region: not part of this statement (the statement is the header window)")
HW | 0 | RESULT: ACCEPTED | 40 | none (the same one information line more)
JG | 0 | RESULT: ACCEPTED | 49 | none
JPWS_v4 | 0 | RESULT: ACCEPTED | 50 | none
JPW13 | 0 | RESULT: ACCEPTED | 50 | none
JPA_v5 | 0 | RESULT: ACCEPTED | 50 | none
"None" means: every line that does not begin with "ok" is an information line (certificate, hashes, statement, counts, smallest zero_step_L, terminal leaves, centres, RESULT). For the eleven trees whose record was made with the pinned script, the new post-check output is line for line the report section of the ACCEPT log (0 differing lines, printed path set aside; JG has 49 ok lines in the record too). For G20S and HW (record made with script 1c01dda7...) it is the record's 53 lines plus the one information line above; 40 ok lines in both.

Per-node entries: in all 26 new --json reports the key "nodes" has the same number of entries as the report of record (1, 23, 31, 36, 36, 48, 61, 679, 579, 113, 110, 255, 416) and 0 entries differ. The only top-level keys that differ at all are "seconds" (all 26) and "certificate" (the printed path, for the ten assembly trees; for JPWS_v4 and JPA_v5 the record was run from a scratch path, the rerun from the pinned path, same sha256).

Copy: 60 files copied into local-research/claude-20261002/results/rerun_trees_20261011/; the ten G20S / HW files already there were NOT overwritten and are byte-identical to mine (cmp, all ten). The folder now holds 26 .out, 26 .json, 13 _report.out, results.tsv, reports.tsv, driver.py, driver2.py, driver.log, the audit lead's SHA256_G20S_HW.txt and SHA256_ALL.txt (71 lines, every other file of the folder; shasum -c: all OK). sha256 of SHA256_ALL.txt: ac5138fbe0baa915b9432679c54c51dcf49c6470beae79e042659386a567a8e6.
Nothing failed, nothing was skipped.

