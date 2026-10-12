Note for this edition: this is a record from the project's sealed record of 8 to 11 October 2026. File names, hashes and line numbers in it refer to that record. Passages about the logistics of the work were removed; the mathematical content is unchanged. Statements of status in it (for example "not certified", "not reviewed") describe the day the record was written, not this edition. The table EDITED_LINES_RECORDS.tsv lists every changed line.

# REVIEW 30 (acceptance): the lead's acceptance scripts and records for specification version 3.0

Reviewer: the reviewer of the 2.6 acceptance (`reviews/REVIEW_26.md` parts R4 and R5) and of the two 3.0
checkers (`reviews/REVIEW_30_PY.md` and `reviews/REVIEW_30_JS.md`). 9 October 2026;
part R, a follow-up on a draft of the report script with a new statement-file entry
(`root_region`), was added at the end and changes nothing in sections 0 to 9. I wrote none of the reviewed files. What I wrote: this file and the folder `reviews/r30acc/`
(scripts, small test certificates, sandboxes, outputs, logs; index in section 9). Folder
W = `research/window-extension-20261008`, R = the repository.

**In one paragraph.** The FINAL scripts, `acceptance/accept_tree30.sh` (sha256 0cd4ff06...) with
`acceptance/h_report30.py` (1c01dda7...), fit: in 55 cases of mine they end with exit code 0 exactly when a
certificate was accepted as a whole by both frozen programs for the stated statement, and never otherwise. They
got there in three rounds. The versions I was first given had two ways to end with exit code 0 for a rejected
certificate (the exit code came from a search of the log, and a node id or a file name can put lines into the
log: cases A28b, A29), and they took `FROZEN_30.json` on trust (A25). The corrected versions had two more (the
five deciding shell variables were never initialised, so with an unwritable log they came from the caller's
environment: B02, B03; and the one Python call that was not isolated decided WHICH program files were run: B12,
B12b). All four were found by running the scripts on copies in a sandbox, all four are corrected in the final
versions, and none of them touched a record: every record was checked here independently of the lead's scripts.
The four final records, made from 04:06 on with the final scripts, are ACCEPTED, and I confirm each of them from
the two reports themselves (section 4 and 5). The sentence for the status file is fair (section 7).

**Answers in short.**

| question | answer |
|---|---|
| (1) exit code 0 without a whole acceptance by both pinned programs? | Final versions: no, in 55 cases (section 1). Earlier versions: yes, four ways, all corrected. |
| (2) the 03:30 change of `h_report30.py` | Right, and no weaker than needed. For wx-cert-3 nothing is accepted that the first version rejected (1,045 changed report pairs, no difference). For wx-cert-2 the absent key cannot hide a disagreement (section 2). The 03:50 change altered the printing only (1,397 pairs, no difference). |
| (3) `EXPECT_G20S_SOS.json` against the statement; `S_floor` | Window and tube are exactly those of (ANN_G20S) and of `EXPECT_G20S.json`; the only differences are name, schema, `S_floor`. The sentence of section 11 of the text, with its two-line proof, is enough (section 3). |
| (4) the record `ACCEPT_G20S_SOS.log` | Everything as it should be: the final record in 58 checks of mine, the first-round record in 49, none wrong (section 4). |
| (5) the three 2.6 trees under 3.0 | The three final records are ACCEPTED, and the 3.0 reports equal the 2.6 acceptance reports node entry for node entry (579, 593, 679 entries; only the new `zero_step_L` is added); the new values L are equal in both reports (224, 195, 237) (section 5). |
| (6) the sentence for the status file | Fair. Nothing is missing for the word PROVED; three precisions in section 7. |

## 0. What was reviewed

SHA-256 verified with `shasum -a 256`; "final" = the state on disk when this report was finished.

| file | SHA-256 | remark |
|---|---|---|
| `acceptance/accept_tree30.sh` first version | 540403a095232f25910678728cf798220f4e69c4fb7527778fc26ab8a63d7f64 | made the first-round records; byte copy in `r30acc/sbx/` |
| second version (03:46) | ffafb155aafda6e1b129a41d7288824e1f12a4aa58b0748a251409877248ef32 | copy `r30acc/accept_tree30_ffafb155.sh` |
| **final (04:04; 85 lines)** | 0cd4ff06497209cb5622d018c34c5e1ad2ef41815b5a9db304974ffd565c1aa5 | = `r30acc/proposed/accept_tree30.sh`, byte for byte; read-only |
| `acceptance/h_report30.py` first version | 9446a23d21185c811d8a0912ab35d3d2fc854892def461032c864304f1e6555d | reconstructed exactly from the 03:30 file and the lead's description (`r30acc/h_report30_first_9446a23d.py`, hash verified against the first-round log) |
| version of 03:30 | 76d16ccda1345e084f9c0f803c3d548deadbcceef1a65b18afb483f090750b50 | byte copy in `r30acc/sbx/` |
| **final (the "03:50" change; file time 03:47; 346 lines)** | 1c01dda73b9ff5814ba52207aa43ef25145ab84baf97c5d580a156adc1c7bc78 | copy `r30acc/h_report30_1c01dda7.py`; read-only |
| `acceptance/FROZEN_30.json` | 6d65a0705c039bbf2f48acabb7f12275871af6b7b8fa308c0671ea6518b30803 | names C1, C2, SPEC below |
| `checker/wxcheck_v30.py` (C1, frozen) | cf8db52bfa1cc565d8610bf13b279d1b5da2f84c91ce2854d15a3b0a88cd096c | reviewed: `REVIEW_30_PY.md` part P9 |
| `checker2/wxcheck2_v30.js` (C2, frozen) | 97210adf74a3ebed7cde021a3cb1ff6ea6380d8d2d55540a2a2a1cb17dc27542 | reviewed: `REVIEW_30_JS.md` part J7 |
| `SPEC_v3.0.md` (final text) | 0a6dfc2ae10ed6f30a21ebe357a6e73dd7355223c521cc67a3f2bdab9549aba0 | audited: `REVIEW_30.md` part G |
| `acceptance/EXPECT_G20S_SOS.json` | 9ab5d78591fa3ef66e75cccbafdd1e73a1f037b1339e159459c31917bf1ad690 | |
| `acceptance/EXPECT_HW.json`, `EXPECT_G20.json`, `EXPECT_G20S.json` | 5f63bf97..., bd9bfde8..., 1447c955... | the hashes named in `REVIEW_26.md` (lines 638, 1165): unchanged since the 2.6 acceptance |
| `proto30/out/tree3/c01/G20S_v3_c01.jsonl.gz` (the new certificate; 160,650,526 bytes) | 989e9738fd34b17cd60f0ee2a01e1f091f1dad7599bdaa873e7f28e354a38273 | uncompressed f678f75a53e164b4ee97c2e3cb6c8536c289311b2bf7576a5e6cfeae13a3da58 |
| `bigbox/gen17/HW_tree.jsonl.gz`, `G20_tree.jsonl.gz`, `G20S_tree.jsonl.gz` | c974a9c5..., 2378109c..., 3275f52a... | the three certificates accepted under 2.6 |
| `bigbox/THEOREM_G20S.md` | ed64ff7ec8aef6ed7256edeb83732046b6eb95e574c77dfd6528403c94aa2a32 | the statement (ANN_G20S), step 1 |
| `acceptance/cross_run30.py`, `acceptance/cross30/final_0310/` | 9dee7dd5...; summary.txt ab02f517..., cross_run.tsv 3cbb3741... | section 6 |
| `acceptance/round1_0316/` | README.md f42d7fac... | the first-round records, moved there by the lead |

The lead's scripts were run only as copies inside
sandboxes in `reviews/r30acc/` (`sbx/`, `sbx2/`, `sbx3/`, `sbx4/`, each a mirror of the folder layout the scripts expect, with byte
copies of the frozen files), never in `acceptance/`.

Order of events, for the reader of the records. First round of acceptance runs (first shell
script; first report script for G20S_SOS, the 03:30 version for the three trees, after the first HW_v30 run had
ended NOT ACCEPTED through a flaw of the report script itself). Then my first round of cases, findings
A28b, A29, A25. Then the second versions. Then my second round, findings B02, B03, B12, B12b, and a
tested replacement. Then the lead installs the replacement exactly, makes both scripts read-only,
moves the first-round records to `acceptance/round1_0316/` and starts the four final runs.

## 1. Question (1): can the scripts end with "RESULT: ACCEPTED" and exit code 0 when they should not?

### 1.1 How the final versions decide

`accept_tree30.sh NAME CERT EXPECT [REFFILE SHA]`, in this order:

1. `FROZEN_30.json` must exist and have the SHA-256 written in the script (6d65a070...); otherwise exit 2.
2. The certificate and the EXPECT file must exist; a reference file must have the stated hash.
3. The three frozen file names are read from `FROZEN_30.json` by an isolated Python call (`python -I -B -c`); the
   three files must exist.
4. `rc1=1; rc2=1; rcr=1; first1=""; first2=""`, and the log must be writable; otherwise exit 2.
5. Reports of an earlier run under the same NAME are removed.
6. Into the log: the hashes of the certificate, of the three frozen files (each beside the value of
   `FROZEN_30.json`), of the packing file, of both scripts, of `FROZEN_30.json` and of the EXPECT file; the
   interpreters.
7. C1 is run in its own folder (`python -I -B`), its output kept in a scratch file: `rc1` = its exit code,
   `first1` = the first line of that file. The same for C2 (`env -u NODE_OPTIONS node`): `rc2`, `first2`.
8. `h_report30.py` (isolated) gets the certificate, the two reports, the two exit codes, the EXPECT file and
   `FROZEN_30.json`: `rcr` = its exit code.
9. Exit code 0 if and only if `rcr` = `rc1` = `rc2` = 0 and `first1` = `first2` = `PASS`. Nothing is read back from the log.

`h_report30.py` ends with `RESULT: ACCEPTED` and exit code 0 only if every one of these holds (I read all 346
lines; any exception ends in `RESULT: NOT ACCEPTED`, exit 1):

- `FROZEN.json` has the entries C1, C2, SPEC, frozen_on; each of the three files, hashed again now, has its hash;
- the EXPECT file has only known entries; the header's schema is the statement's; both reports say they checked
  under it (C1's key may be absent under wx-cert-2 only, section 2); label set and `S_floor` of the header and of
  both reports are the statement's; the header has no unknown field;
- both exit codes are 0; C1's report has verdict PASS and mode full, C2's has result PASS and mode certificate;
- C1's report names the hash of the file (and of the uncompressed stream), C2's the hash of the stream;
- the reference file's hash in the header and in both reports is the statement's (or the pinned packing hash);
- C1's report names the frozen text by its hash; C2's names version 3.0;
- node ids unique in each report and the same set in both; every node accepted in both; every entry has a closure
  kind and the kinds agree node for node;
- the value L of every leaf closed by a `0` step: present in both reports or in neither, equal as rational
  numbers, positive, and as many as each report's own evidence says;
- the number of terminal leaves, if the statement fixes it; each report's counts agree with its node list; the
  numbers of steps, terms and evaluated rounds are equal in both;
- Sref; the root id; the centre flags of both reports; header window = the statement's window and header tube =
  the statement's tube (all intervals, radii, centres, as rational numbers).

What it does not do, by design: it reads only the first line of the certificate and relies on the two PASS
reports for the rest; it does not compare the per-node numbers of rounds or the line numbers of the two reports
(my own record checks do: equal for every node of all four records); it prints, but does not test, the strings
`checker` of the reports.

Is the header it reads the header the programs checked? Yes whenever both say PASS: both frozen programs reject a
header with a repeated key, a second JSON value on line 1, a byte-order mark or an empty first line, and also a
line 1 that holds two headers separated by a carriage return, of which Python's text mode would hand the report
script only the first (9 files `r30acc/certs/hdr_*.jsonl`, all FAIL / FAIL). With CR LF line ends both accept, and
all three readers see the same header (1 file).

### 1.2 The cases

Small certificates from my harnesses of the two code reviews (accepted or rejected by both frozen programs as
stated), each run through the sandbox copy of the shell script exactly as the lead runs it (A15, A16,
B09: the report script by hand). "should end" is what a correct acceptance procedure must do. Script: `r30acc/acc_attack.py`; results
`r30acc/out/attack_results_*.json`; console output `r30acc/out/run_cases_*.txt`.

| case | what | should end | first versions (540403a0, 76d16ccd) | second (ffafb155, 1c01dda7) | FINAL (0cd4ff06, 1c01dda7) |
|---|---|---|---|---|---|
| A01 | control: a wx-cert-3 certificate that both programs accept, the right statement | ACCEPTED, exit 0 | exit 0 | exit 0 | exit 0 |
| A02 | control: a wx-cert-2 certificate that both accept (the path that the 03:30 change opened) | ACCEPTED, exit 0 | exit 0 | exit 0 | exit 0 |
| A03 | control: wx-cert-3 with centre maps in the header, the statement names the centres | ACCEPTED, exit 0 | exit 0 | exit 0 | exit 0 |
| A04 | control: the certificate of A01 gzip-compressed | ACCEPTED, exit 0 | exit 0 | exit 0 | exit 0 |
| A05 | a certificate that both programs reject | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| A06 | accepted certificate, but the statement names another window | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| A07 | accepted wx-cert-3 certificate, the statement says wx-cert-2 (no schema key) | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| A08 | accepted wx-cert-2 certificate, the statement says wx-cert-3 | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| A09 | accepted certificate with S_floor 4, the statement says S_floor = Sref | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| A10 | accepted certificate with centre maps, the statement has none (and another box) | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| A11 | control: blanks in the certificate path and in NAME | ACCEPTED, exit 0 | exit 0 | exit 0 | exit 0 |
| A12 | a rejected certificate at a path with blanks | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| A13 | FROZEN_30.json missing (accepted certificate) | not accepted, exit not 0 | exit 2 | exit 2 | exit 2 |
| A14 | PASS reports of another certificate lie at <NAME>_C1.json, <NAME>_C2.json; the certificate is rejected | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| A15 | h_report30.py by hand: PASS reports of certificate A01, but the certificate file and statement of A02 | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| A16 | control for A15: the same call with the right certificate and statement | ACCEPTED, exit 0 | exit 0 | exit 0 | exit 0 |
| A17 | control: a reference file given (a copy of the packing file), the statement names its hash | ACCEPTED, exit 0 | exit 0 | exit 0 | exit 0 |
| A18 | reference file named 'p.json --node root': both programs run in node-only mode | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| A19 | reference file named 'p.json --help': both programs print their help | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| A20 | reference file named 'p.json --no-packing-pin' (accepted certificate; the smuggled option removes the programs' own pin, the report script still requires the statement's hash) | ACCEPTED, exit 0 | exit 0 | exit 0 | exit 0 |
| A20b | the same with a rejected certificate | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| A21 | accepted certificate, the EXPECT file is not JSON (the report script cannot finish) | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| A22 | accepted certificate, EXPECT without the key terminal_leaves (KeyError inside the report script) | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| A23 | accepted certificate, the report script itself crashes at once | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| A24 | FROZEN_30.json edited: C1 is a program that prints PASS, exits 0 and writes no report | not accepted, exit not 0 | exit 1 | exit 2 | exit 2 |
| A25 | FROZEN_30.json edited to name two weakened copies of the checkers (guard rule off); the certificate violates the guard rule | not accepted, exit not 0 | exit 0 **WRONG** | exit 2 | exit 2 |
| A26 | the real FROZEN_30.json, but checker/wxcheck_v30.py is another file (accepted certificate) | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| A27 | the real FROZEN_30.json, but SPEC_v3.0.md has one more line feed (accepted certificate) | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| A28 | REJECTED certificate (its root does not exist) whose one accepted leaf has an id with line feeds: ...\nRESULT: ACCEPTED\nFIRST LINES: both PASS\n... | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| A28b | REJECTED certificate (its root is missing) whose one leaf, accepted as a node by both programs, has that id; the leaf names "root" as its parent | not accepted, exit not 0 | exit 0 **WRONG** | exit 1 | exit 1 |
| A29 | REJECTED certificate whose FILE NAME contains line feeds: x\nRESULT: ACCEPTED\nFIRST LINES: both PASS\ny.jsonl | not accepted, exit not 0 | exit 0 **WRONG** | exit 1 | exit 1 |
| A30 | plain text under a name that ends in .gz: the Python program accepts it, the Node program rejects it | not accepted, exit not 0 | exit 1 | exit 1 | exit 1 |
| B01 | rejected certificate; the caller's environment has rcr=0 rc1=0 rc2=0 first1=PASS first2=PASS | not accepted, exit not 0 | not run | exit 1 | exit 1 |
| B02 | the same environment, and NAME = nodir/B02: the log cannot be opened (no such folder), so the brace group does not run | not accepted, exit not 0 | not run | exit 0 **WRONG** | exit 2 |
| B02b | NAME = nodir/B02b without those variables in the environment | not accepted, exit not 0 | not run | exit 1 | exit 2 |
| B03 | the same environment, and ACCEPT_<NAME>.log exists read-only (the record of an earlier accepted run): the log cannot be opened | not accepted, exit not 0 | not run | exit 0 **WRONG** | exit 2 |
| B04 | a read-only earlier log under the same NAME, no variables in the environment (rejected certificate) | not accepted, exit not 0 | not run | exit 1 | exit 2 |
| B05 | the scratch file .tmp_<NAME> is a folder: the programs cannot be started with their output kept (a broken run, although the certificate is good) | not accepted, exit not 0 | not run | exit 1 | exit 1 |
| B06 | the scratch file exists read-only and its first line is PASS (rejected certificate) | not accepted, exit not 0 | not run | exit 1 | exit 1 |
| B07 | the file at the frozen path of C1 is a program that prints nothing, writes nothing and ends with 0 (good certificate) | not accepted, exit not 0 | not run | exit 1 | exit 1 |
| B08_0 | rejected certificate; the accepted leaf's id uses '\u2028' as a separator around RESULT: ACCEPTED | not accepted, exit not 0 | not run | exit 1 | exit 1 |
| B08_1 | rejected certificate; the accepted leaf's id uses '\x85' as a separator around RESULT: ACCEPTED | not accepted, exit not 0 | not run | exit 1 | exit 1 |
| B08_2 | rejected certificate; the accepted leaf's id uses '\r' as a separator around RESULT: ACCEPTED | not accepted, exit not 0 | not run | exit 1 | exit 1 |
| B08_3 | rejected certificate; the accepted leaf's id uses '\x1b[2K\r' as a separator around RESULT: ACCEPTED | not accepted, exit not 0 | not run | exit 1 | exit 1 |
| B08_4 | rejected certificate; the accepted leaf's id uses '\x0b' as a separator around RESULT: ACCEPTED | not accepted, exit not 0 | not run | exit 1 | exit 1 |
| B08_5 | rejected certificate; the accepted leaf's id uses '\x0c' as a separator around RESULT: ACCEPTED | not accepted, exit not 0 | not run | exit 1 | exit 1 |
| B09 | h_report30.py by hand on reports whose strings `checker`, `spec`, `evidence` contain line feeds and RESULT: ACCEPTED (and whose verdict is FAIL) | not accepted, exit not 0 | not run | exit 1 | exit 1 |
| B10 | good certificate; C1 does all its work and writes its report but PRINTS NOTHING (its output is thrown away by a wrapper): exit codes 0, both reports right | not accepted, exit not 0 | not run | exit 1 | exit 1 |
| B11 | rejected certificate; a wrapper prints PASS before C1's own output (first line PASS, exit code 1) | not accepted, exit not 0 | not run | exit 1 | exit 1 |
| B11b | good certificate; in place of C1 something that prints PASS, ends with 0 and writes NO report (C2 is the real program and accepts) | not accepted, exit not 0 | not run | exit 1 | exit 1 |
| B12 | FROZEN_30.json untouched; the script is STARTED IN A FOLDER that contains a file json.py (the helper fz runs python -c without -I); the certificate violates the guard rule | not accepted, exit not 0 | not run | exit 0 **WRONG** | exit 1 |
| B12b | the same file json.py reached through the environment variable PYTHONPATH instead of the starting folder | not accepted, exit not 0 | not run | exit 0 **WRONG** | exit 1 |
| B14 | control: good certificate; NODE_OPTIONS in the environment names a script that would stop node at once (it must be ignored) | ACCEPTED, exit 0 | not run | exit 0 | exit 0 |
| B13 | reference file named 'q.json --no-packing-pin' has the stated hash; the programs are thereby given ANOTHER file, q.json (other hash), with their pin removed | not accepted, exit not 0 | not run | exit 1 | exit 1 |
| B13b | the same, and the certificate's header names the hash of that other file (both programs then accept it relative to q.json); the statement names the pinned hash | not accepted, exit not 0 | not run | exit 1 | exit 1 |

Cases run: 32, 55, 55; wrong: 3, 4, 0.

The lead's list, case by case: stale reports A14; a report of another file A15; a node-only run A18; the help
exit A19; a crash of the report script A21, A22, A23; `FROZEN_30.json` missing A13, edited A24, A25; a
certificate path with blanks A11, A12 (and blanks in NAME, A11); a checker that prints PASS but writes no report
A24 (through an edited `FROZEN_30.json`: now exit 2) and B11b (with the true one); the programs or the text not
the pinned ones A25, A26, A27, B07, B12, B12b; the two programs disagreeing A30.

The lead's four further questions on the second version. Can `first1` / `first2` be anything but the first line of the
program's own output: yes, in two ways, neither of which can make an acceptance. If the program prints nothing,
the scratch file begins with the statistics of `/usr/bin/time` (B07, B10: `first output line C1: [        0.11 real ...]`),
never `PASS`. If the scratch file cannot be written, the program is not started, the exit code is 1, and
`first1` is the first line of whatever lies there from before (B06: `[PASS]` from a read-only old file, with
`exit code C1: 1`). A program that prints nothing: B07, B10, exit 1 (B10 is the sharpest form: C1 does all its
work and writes a correct report but its output is discarded; the report part says ACCEPTED, the last line of the
log says `FIRST LINES: NOT BOTH PASS`, exit 1). The scratch file unwritable: B05, B06, exit 1. Blanks in NAME: A11.

### 1.3 The four findings; all are corrected in the final versions

**F1 (first versions; A28b, A29). The exit code came from a search of the log.** The first shell script ended
with `grep -q "^RESULT: ACCEPTED$" "$LOG" && grep -q "^FIRST LINES: both PASS$" "$LOG"`, and the report script
printed the id of the leaf with the smallest L with `%s`. Node ids are arbitrary non-empty JSON strings (SPEC
section 7).
A28b is a certificate that both programs REJECT as a whole (its root is missing) but whose one leaf is accepted
as a node and has the id `"L\nRESULT: ACCEPTED\nFIRST LINES: both PASS\nx"`: the log got both lines, the script
ended with exit code 0, although the log's real last lines said `RESULT: NOT ACCEPTED` and
`FIRST LINES: NOT BOTH PASS`. A29 does the same through the certificate's FILE NAME, which the shell's own
`echo` prints. Evidence: `r30acc/out/logs_540403a0_76d16ccd/ACCEPT_A28b.log`, `ACCEPT_A29.log`. Corrected
twice over: the shell script decides from its variables, and every output line of the report script passes
through one function that writes each control character as an escape, with `%r` for ids, paths and the list of
terminal leaves. Tested with six other characters that some programs take for a line end (B08_0 to B08_5:
U+2028, U+0085, CR, ESC [2K CR, VT, FF): one RESULT line in the report part by any convention, no raw control
character, exit 1.

**F2 (first versions; A25). `FROZEN_30.json` was taken on trust.** An edited copy naming two weakened copies of
the checkers (the guard rule (T3) of the wx-cert-3 format switched off) was accepted with exit code 0 for a
certificate that violates that rule; the log showed the other hashes, but only a reader of its head would see it. Corrected: the
file is pinned by its SHA-256 inside the shell script (A24, A25: exit 2).

**F3 (second version; B02, B03). The five deciding variables were never initialised.** On this Mac `/bin/sh` is
GNU bash 3.2.57. If the redirection of the brace group `{ ... } > "$LOG" 2>&1` fails, sh prints an error, SKIPS
the group and goes on; the last line then tested `rcr`, `rc1`, `rc2`, `first1`, `first2` as inherited from the
caller's environment. With `rcr=0 rc1=0 rc2=0 first1=PASS first2=PASS` exported: NAME = `nodir/B02` (the log's
folder does not exist) gave exit code 0 with nothing run and no log; an existing read-only `ACCEPT_<NAME>.log`
gave exit code 0 and the tail of the OLD accepted log on the screen (B03). Without those variables the exit code
was 1, but the screen still showed the old log's `RESULT: ACCEPTED` (B04). A NAME with a slash is an easy slip.
Corrected: the variables start as "not accepted", and a log that cannot be written stops the run with exit 2
before anything is removed or run (B02, B02b, B03, B04: exit 2 with the message `cannot write the log ...`).

**F4 (second version; B12, B12b). The helper that reads `FROZEN_30.json` was the one Python call without `-I`,
and it decides which files are run.** `python -c 'import json, ...'` puts the starting folder (and PYTHONPATH)
on the module path. With a file `json.py` in the folder the script was started from, the helper answered with
the names of the two weakened copies; these were run on the certificate that violates the guard rule; the report
script, which reads `FROZEN_30.json` itself and hashes the files named THERE (not the files that ran), said
ACCEPTED; exit code 0. This was F2 by another door. Only the head of the log showed it
(`sha256 checker/wxcheck_weak.py: 892de353... (FROZEN_30.json: cf8db52b...)`). Corrected: `python -I -B -c`
(B12, B12b: the real programs run and reject; exit 1).

A fifth edit, not a finding: neither a log nor a report named the interpreters. The final script writes one line,
for example `interpreters: python 3.9.6 (<path>); node v25.6.1 (/opt/homebrew/bin/node)`.

Did any of this touch a record? No. F1 needs a certificate whose node id or path contains a line feed: every node
id of the four certificates consists of letters, digits, `.`, `_`, `-` (checked in both reports of each), the
paths are plain, and in every log of the first round and of the final runs the texts `RESULT:` and
`FIRST LINES:` occur exactly once. F2 and F4 need another `FROZEN_30.json` or a file `json.py`: every log names
the three frozen files with the reviewed hashes beside the values of `FROZEN_30.json` (the hash printed there is
that of the file the script goes on to run) and the pinned hash of `FROZEN_30.json` itself; for G20S_SOS the two
reports also equal my own reports of the same certificate, made with the frozen files directly (section 4), and
for the three trees they equal the 2.6 reports node for node (section 5). F3 needs an unwritable log. The sentence in the script, "no record made before was affected", also holds for the older logs of
`acceptance/`: each of the 18 has exactly one line with `RESULT:`, except `ACCEPT_H.log` (two: the lead's own
re-run of the report on 8 October 13:22, marked as such in the log) and `ACCEPT_v23.log` (an older format without
that line); none contains a control character.

### 1.4 A rule for reading a record

For every log that a run of the shell script wrote (45 in each of the last two rounds):

    exit code 0   <=>   the log ends with the three lines
                        RESULT: ACCEPTED / exit code report: 0 / FIRST LINES: both PASS

Why it holds for the final version in general: `RESULT: ACCEPTED` is printed only together with exit code 0 of
the report script, and only if both exit codes it was given are 0; the third line is printed exactly when
`first1` = `first2` = `PASS`; nothing that a certificate, a report or a path controls is printed after the
RESULT line; and in the report part every such string stands inside a line, with control characters escaped.
The head of a log and the first ten lines of each program's output are still copied as they come: a certificate
PATH with line feeds puts lines of its choice there (A29, final version: two false `RESULT: ACCEPTED` lines, one
in the head and one where C2 prints the path, then the true last lines; exit 1). So a record is read at its END, as the comment in the script says; the
final records contain no such line anywhere.

### 1.5 What the scripts trust, and what may stay as it is

- The environment of the caller: `PATH` (for `node`, `shasum`, `head`, `cut`, `tail`, `env`, `date`, `rm`) and
  exported shell functions. I tested both on this Mac: sh takes a function `head` exported by the caller, and a
  `head` earlier on `PATH`, in place of the real one. No shell script can defend itself against that; the log now
  names the node binary and both versions.
- `$REFOPT` is used unquoted, so a reference-file NAME with blanks smuggles options to both programs. Harmless in
  all six cases (A18, A19, A20, A20b, B13, B13b): node-only mode fails on both exit codes (10 and 3), both first
  lines and both reports' verdict and mode; the help text on both exit codes (2 and 2), both first lines and the
  missing reports; with `--no-packing-pin` smuggled in, the header's hash, both reports' hash of the file actually read and the
  statement's hash must still agree.
- The report script's test of C2's text is weak: `"3.0" in spec` (a report saying "version 13.0" passes) and
  `spec_sha256` may be absent, although the frozen C2 always writes it. Harmless: C2 is pinned by its hash and
  writes `spec_sha256` = 0a6dfc2a... in all four records. In a later version: require equality.
- Among 1,397 changed report pairs (section 2) the final report script accepts 483 that differ from the true
  pair. All are of four harmless kinds: a key the script does not use (`certificate` path, `checker`, `seconds`,
  `compressed`, `reason`, per-node `line`, `rounds`, `steps`, final-store digest, some counts); the same rational
  in another spelling (`S_floor` "4/1", "8/2", "4.0"; L with a leading blank or sign or doubled numerator and
  denominator; `labels` 16.0); the SAME change in both reports (every L replaced by 7/3 in both; a node entry
  removed from both with the counts lowered): the script compares the two reports with each other and with the
  header and cannot know what the programs should have written; and exit-code arguments that `int()` reads as 0
  (" 0", "+0", "00", "0_0", a full-width zero), which the shell never passes. Every change of a key that matters
  in ONE report is rejected: verdict, result, mode, the hashes, the root, labels, schema, centre flags, a node's
  `accepted`, `close`, `id`, `zero_step_L` (absent, 0, negative, another value), a node entry added, removed or
  doubled.
- Two runs under the same NAME at the same time would overwrite each other's files (not tested; the lead's
  chains use different names).
- The frozen files are hashed before the programs run (log) and after (report script), not held in between;
  they are read-only.
- Cosmetic: the time statistics appear twice in the log (once from `head -n 10`, once from `grep`).

## 2. Question (2): the changes of `h_report30.py`

**The 03:30 change** (`r30acc/H_REPORT30_first_to_0330.diff`, 3 hunks): the docstring; the two expressions

    c1_schema = c1.get("schema", "wx-cert-2" if schema == "wx-cert-2" else None)
    c1_wc     = c1.get("window_centres", False if schema == "wx-cert-2" else None)      (and tube_centres)

in place of plain `c1.get(...)`; and the wording of one check line. `schema` here is the STATEMENT's schema.

For a wx-cert-3 statement both defaults are `None`, exactly as before, so nothing can be accepted that the first
version rejected. Tested: on three wx-cert-3 bases (harness T; harness M with centre maps; harness I with a leaf
closed by a `0` step), 1,045 pairs of reports changed in one place: the first and the final version give the
same RESULT line and the same exit code on all 1,045; none is accepted by the final and rejected by the first.
(An earlier test of 37 variants per base with the 03:30 version itself: the same.)

For a wx-cert-2 statement an absent key of C1 counts as "wx-cert-2" / "no centre maps". Can that hide a real
disagreement? No:

- the header's schema is compared with the statement's directly, so the certificate IS a wx-cert-2 certificate;
- C2 writes the three keys always (frozen file line 3751) and they are compared strictly;
- the frozen C1 writes the three keys exactly when it checks under wx-cert-3 (lines 2958 to 2961: `if SCHEMA_V3[0]:`,
  set from the header at line 1217). Had C1 checked under wx-cert-3, the keys would be present, and a present
  key is compared as before: `C1.schema := "wx-cert-3"`, `:= None`, `C1.window_centres := True`, `0`, `1`,
  `"false"`, `None` are all rejected on the wx-cert-2 base; only the absent key and the consistent values
  (`"wx-cert-2"`, `False`) pass.

So the rule is as strict as the facts allow: under wx-cert-2 the only report C1 can write has no such keys, and a
wx-cert-2 header cannot have centre maps (the next check line). The first version rejected every wx-cert-2 pair
of the real programs (0 of 352 variants accepted, the true pair included): that was the flaw behind
`round1_0316/ACCEPT_HW_v30_first_run_script_flaw.log`, whose only FAIL lines are these two tests.

**The 03:50 change** (`r30acc/H_REPORT30_0330_to_1c01dda7.diff`, 18 hunks): the function `out()`, every `print`
replaced by it, `%r` for the certificate path, the id with the smallest L and the list of terminal leaves. By
reading: no test changed. By test: on all 1,397 changed pairs (four bases) the version of 03:30 and the final
version give the same exit code, the same RESULT line and the same sequence of ok/FAIL flags, line for line.
`out()` leaves characters above U+009F as they are; the strings that come from a certificate or a path are
printed with `%r`, which escapes those too (B08_0: `'L\u2028RESULT: ACCEPTED\u2028...'`).

Script: `r30acc/acc_versions2.py`; output `r30acc/out/run_versions2.txt`, `versions2_results.json`,
`versions2_accepted.txt`.

## 3. Question (3): `EXPECT_G20S_SOS.json`, the statement, and `S_floor`

The statement, `bigbox/THEOREM_G20S.md` section 2 and step 1: (ANN_G20S) "every feasible configuration of the
sixteen squares with S <= Sref in G20S lies in the tube T1", G20S: every xi in [-1/5, 1/5] except xi_{2,1} in
[-39/125, 0] and xi_{13,2} in [-1/5, 28/125], |phi| <= 1/10; T1 = the window of HW with the upper end of
xi_{2,1} at 1/100, that is: the 29 core coordinates within 3/20, |phi| <= 101/1000, xi_{2,1} in [-8/25, 1/100],
xi_{11,2} in [-1/5, 2/25], xi_{13,2} in [-1/5, 1/10].

Checked with my own code, the regions written out by hand from the theorem (`acc_record.py`):

- `EXPECT_G20S_SOS.json`, read by my own expansion: its window is G20S and its tube is T1, all 32 intervals and
  16 angle radii each; sixteen labels; no centre maps;
- the header of the new certificate: the same window and tube; schema wx-cert-3; Sref = `S_floor` =
  4675530093604551/10^15; the pinned packing hash; no `labels` field (sixteen); no centre maps;
- the header of the first certificate of the same statement (`bigbox/gen17/G20S_tree.jsonl.gz`, 3275f52a..., the
  hash quoted in the theorem): the same window, tube, Sref and packing hash; the two headers differ in schema,
  `S_floor` and the root's name only;
- `EXPECT_G20S_SOS.json` against `EXPECT_G20S.json`: they differ in exactly three entries: `name`, `schema`
  (absent / "wx-cert-3") and `S_floor` ("4" / Sref). Window, tube, labels, terminal_leaves are equal objects.

**Is "S_floor never weakens a statement" enough?** Yes. The certificate proves (ANN) for S_floor <= S <= Sref with
S_floor = Sref, that is for S = Sref (its root C00 has the side interval [Sref, Sref], no parent, no
assumption). Section 11 of the audited text gives the step to every S <= Sref with its proof, and the proof is
right: let (S, q, a) be feasible with S <= Sref and in the window W. (F1) asks that all corners lie in [0,S]^2,
which is contained in [0,Sref]^2 (the container has its corner at the origin for every S, section 0); (F2) does
not mention S. So (Sref, q, a) is feasible. It lies in W, because W restricts only the coordinates
xi_ik = e_ik . (q_i - p_i) and the directions a_i, and the reference centres p_i, the frames e_ik and the
reference directions u_i are constants of the packing file (section 1; p_13 contains the NUMBER Sref, not the
configuration's side). By (ANN) at S = Sref it lies in the tube T, and T, too, restricts only (q, a) (section 8:
a box, angle radii, centres). Hence (S, q, a) lies in T. I had confirmed the same argument for 2.6
(`REVIEW_26.md` 1.4, finding F1 there, which became this paragraph of the text); the referee of 3.0 read the
paragraph in the final text (`REVIEW_30.md`, lines 328 and 360). The text adds the right warning: the argument
would fail if a later version let a window or a tube depend on S.

One consequence for whoever cites the new certificate in a theorem: the certificate alone states the claim at
S = Sref; the sentence "by SPEC 3.0 section 11 this gives every S <= Sref" belongs beside the citation.

## 4. Question (4): the record of G20S_SOS

Checked independently of the lead's scripts (`acc_record.py sos`; nothing of the lead's code is imported), for the
first-round record (`round1_0316/`, run 03:16 to 03:27, log b4a1791d...) and for the FINAL record
(`acceptance/ACCEPT_G20S_SOS.log`, run 04:06:42 to 04:18:25, 97 lines, sha256 f03b6f0e17e3511e40a4b21d097d2dae37121e0161324112e18604f9783860ed;
`G20S_SOS_C1.json` 9849f302..., `G20S_SOS_C2.json` 5b73b846...). Final record: 58 checks, none wrong
(`r30acc/out/record_final_G20S_SOS.txt`); first-round record: 49 checks, none wrong
(`r30acc/out/record_round1_G20S_SOS.txt`; the checks of the script versions and of the file times apply to final
records only). I also read the 97 lines of the final log one by one. What follows is the final record.

- Hashes in the log against the files on disk, recomputed: the certificate; C1, C2 and the text (log = value of
  `FROZEN_30.json` in the log = disk = the hashes of my two code reviews and of the audit); the packing file;
  `FROZEN_30.json`; the EXPECT file; both scripts (the final versions; both files older than the start of the
  run, 04:04:37 and 03:47:11 against 04:06:42, and read-only; the report part has the quoted form that only the
  final report script writes); the interpreters line (python 3.9.6, node v25.6.1, the ones my own runs used).
- Shape: exit codes 0, 0, 0; first output lines PASS, PASS; 40 lines beginning with `ok`, none with `FAIL`; the
  log ends with the three lines of 1.4; `RESULT:` and `FIRST LINES:` occur once each; no control character.
  C1 568.5 s and 279 MB, C2 132.2 s and 1.05 GB.
- The two reports against each other, by my own comparison: the same 153 node ids, each once (71 split, 81
  infeasible, 1 terminal `MAIN.T`); every node accepted in both; closure kind, number of rounds, rounds
  evaluated and line number equal for all 153; `zero_step_L` stands in the same 81 nodes in both, exactly the
  leaves closed by a `0` step by each report's own evidence; the 81 values are EQUAL AS RATIONAL NUMBERS
  (denominators of 1,158 to 1,170 digits), all positive, smallest 9.385454e-04 at node `W20`, largest
  4.392372e+05; counts equal (81 steps, 1,614,692 terms, 81 rounds evaluated).
- Against my own reports of the same file, made during the two code reviews with the frozen files directly
  (`r30py/out_v30cand/`, `r30js/out_frozen/`): the lead's C1 report equals mine in every key except the running
  time and the path, and so does the lead's C2 report: all 153 node entries, evidence, final-store digests, counts,
  hashes.
- Against the first round: both reports of the final run equal the first round's in every key but the running
  time. The two logs differ, apart from digits in time and memory lines, in: the date, the two script hashes,
  the new interpreters line, the two quoted forms, and the one check line reworded at 03:30.
- Header and statement: section 3.

The referee's report adds a check that owes nothing to either program: the referee's own calculator, written from the
text, reproduces the exact L of all 81 leaves (`REVIEW_30.md`, part H).

## 5. Question (5): the three 2.6 trees under the 3.0 programs

The four FINAL records, as read from the files themselves (`r30acc/acc_summary.py`); runs 04:06:42 to 04:35:10,
two chains, both scripts with file times 04:04:37 and 03:47:11 and read-only:

| record | sha256 of the log | start | nodes | split / infeasible / terminal | leaves closed by a `0` step + by a pair closure | L equal in both reports | smallest L (node) | steps | terms | rounds evaluated | C1 | C2 | reports C1 / C2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ACCEPT_G20S_SOS.log` | f03b6f0e17e3511e... | 04:06:42 | 153 | 71 / 81 / 1 | 81 + 0 | 81 of 81 | 9.3855e-04 (`W20`) | 81 | 1,614,692 | 81 | 568 s, 279 MB | 132 s, 1.05 GB | 9849f302... / 5b73b846... |
| `ACCEPT_HW_v30.log` | 4a740cdb7b31baf4... | 04:06:42 | 579 | 289 / 289 / 1 | 224 + 65 | 224 of 224 | 6.1657e-07 (`root.1.1.1.1.1.1.2.1.1`) | 156,260 | 22,540,696 | 1,776 | 522 s, 1013 MB | 238 s, 1.69 GB | 1adbfa63... / b59776fa... |
| `ACCEPT_G20_v30.log` | 8f8f631cd73b3ed0... | 04:19:26 | 593 | 296 / 238 / 59 | 195 + 43 | 195 of 195 | 4.1755e-07 (`root.1.2.2.1.2.2.1.2`) | 207,387 | 28,395,870 | 2,548 | 625 s, 466 MB | 286 s, 1.83 GB | a24333ee... / d6b7ebe9... |
| `ACCEPT_G20S_v30.log` | 8c0565d1c379ff0e... | 04:18:26 | 679 | 339 / 302 / 38 | 237 + 65 | 237 of 237 | 1.8334e-06 (`root.1.2.1.1.2.2.2.1.2`) | 218,259 | 30,019,872 | 3,006 | 677 s, 356 MB | 323 s, 1.62 GB | e2dd61c0... / 3536f909... |

Full hashes of the four logs: f03b6f0e17e3511e40a4b21d097d2dae37121e0161324112e18604f9783860ed (G20S_SOS),
4a740cdb7b31baf4f42a7f13c8be5b06787093ddbca4d74a9c2a6d2ab46289f7 (HW_v30),
8f8f631cd73b3ed06fe1edf6f87a21b170ba7acc51cd944d22934d8997945d19 (G20_v30),
8c0565d1c379ff0e75e5d3efc985f261bde7900db4ebde8d413190190d868059 (G20S_v30): the same as the lead
stated. Each ends with the three lines of 1.4.

For each of the three trees `acc_record.py tree NAME` makes 51 checks; none is wrong for HW, G20 or G20S
(`r30acc/out/record_final_HW_v30.txt`, `..._G20_v30.txt`, `..._G20S_v30.txt`). The first-round records of the
three trees: 42 checks each, none wrong (`r30acc/out/record_round1_*.txt`). For the final records:

- **The log**, as in section 4: every hash against the disk (certificate, C1, C2, text, packing file,
  `FROZEN_30.json`, the statement file `EXPECT_HW.json` / `EXPECT_G20.json` / `EXPECT_G20S.json`, both scripts in
  their final versions and older than the start of the run); the interpreters line; the quoted form; exit codes
  0, 0, 0; first lines PASS, PASS; 40 `ok` lines, no `FAIL` line; one `RESULT:` line; the three last lines; no
  control character; statement schema wx-cert-2.
- **The two 3.0 reports against each other**: the same node ids, each once; every node accepted in both; closure
  kind, number of rounds, rounds evaluated and line number equal for every node (579, 593, 679); the counts equal;
  C1 has no key `schema` (as it must under wx-cert-2), C2 says "wx-cert-2"; `zero_step_L` stands in the same nodes
  in both, exactly the leaves closed by a `0` step, and the values are equal as rational numbers: 224, 195, 237,
  all positive.
- **The 3.0 reports against the 2.6 acceptance reports of the same programs**, node entry for node entry. The 2.6
  reports are the files whose hashes `REVIEW_26.md` names (`HW_C1.json` b13854c2..., `HW_C2.json` dbf80dee...,
  `G20_C1.json` 2ed92dcd..., `G20_C2.json` 911cc9b5..., `G20S_C1.json` 74bb9aa9..., `G20S_C2.json` a43cde52...),
  PASS reports of the same certificate files. C1: all 579 / 593 / 679 node entries are equal, in the same order,
  in every key the 2.6 report has (id, line, accepted, close, evidence, rounds, rounds_evaluated, steps,
  final_store_sha256); the 3.0 entries ADD `zero_step_L` in the leaves closed by a `0` step and nothing else; the
  other keys of the report differ only in `checker`, `spec_sha256`, `seconds`. C2: all node entries equal in the
  same order (id, line, accepted, close, rounds, rounds_evaluated, evidence, final_store_empty,
  final_store_sha256), again with `zero_step_L` added; the other keys differ only in `spec`, `spec_sha256`,
  `seconds` and the three new keys `schema`, `window_centres`, `tube_centres`. So on these three certificates the
  3.0 programs did, node for node, what the 2.6 programs did: the same closures by the same evidence, the same
  numbers of steps and rounds, and the same final store at every node (equal digests).
- **Against the first round** (`acceptance/round1_0316/`): both reports of each final run equal the first round's
  in every key but the running time; the logs differ, apart from digits in time and memory lines, only in the
  date, the two script hashes, the interpreters line and the quoted forms; the 40 `ok` lines are the same
  character for character.

Two remarks. The first-round log of G20S_v30 shows what the final runs avoid: it names the report script
76d16ccd... (the hash is taken at the START of a run, 03:42) while its report part has the quoted form of
1c01dda7... (installed 03:47, used at the END, 03:58); the lead's README there says so. And one cosmetic point of
the final report script: with more than twelve terminal leaves it prints `terminal leaves: '59 leaves'`, with
quotes the line does not need (G20, G20S).

## 6. The cross-run record

`acceptance/cross_run30.py` (159 lines, read in full: it runs both programs on every file, each with a JSON
report, and compares verdict, exit code, node ids, closure kinds and `zero_step_L` as `Fraction`s) and its record
`acceptance/cross30/final_0310/`. Recounted from `cross_run.tsv` with my own code (`r30acc/out/crossrun_check.txt`):
2,560 rows; the two programs agree on all 2,560; 573 both PASS (exit codes 0, 0), 1,987 both FAIL (1, 1); 425
values L compared, all equal; `disagreements.txt` is "none". By folder: checker2/v30/inputs 509, reviews/r30py/certs
839, reviews/r30/b 306, reviews/r30/d 248, proto30/testcerts30 72, checker/v26/testcerts 358, checker2/v26/inputs
228. The Python program of the cross-run is `proto30/wxcheck_v30_candidate.py`, byte for byte the frozen file.
Against my own runs of the two code reviews: of the files of `r30py/certs`, 477 are in the cross-run, and its
verdicts equal mine on all 477, for each program. The 8 files with an empty node id (on which the two frozen 2.6
checkers had differed, `REVIEW_30.md` B-3) are FAIL / FAIL.

Not in the cross-run: my later files `r30js/certs/` (stress and file tests of the Node review), among them the
two on which the frozen programs differ BY DESIGN of their file reading: a gzip stream under a name without
`.gz`, and plain text under a name with `.gz` (C1 looks at the first bytes, C2 at the name; `REVIEW_30_JS.md`).
Case A30 shows what the acceptance procedure does with such a file: NOT ACCEPTED. The lead's rule "compressed
certificates are always named `*.gz`" settles it; the report script reads the header by the name, like C2.

## 7. Question (6): the sentence for the status file

"(ANN_G20S) has a second certificate, of the new kind, accepted by two independent frozen checkers under an
audited specification, all components reviewed" is a fair statement of what the files show:

- the certificate: `proto30/out/tree3/c01/G20S_v3_c01.jsonl.gz`, 989e9738..., schema wx-cert-3, 153 nodes, 81
  leaves each closed by ONE step on the form `0` (the new kind), one terminal leaf;
- accepted: the final record `acceptance/ACCEPT_G20S_SOS.log` (f03b6f0e...), made by the reviewed script
  versions, RESULT: ACCEPTED; confirmed here from the two reports and from my own two reports of the same file;
- two independent frozen checkers: C1 cf8db52b... (Python) and C2 97210adf... (JavaScript), pinned by
  `FROZEN_30.json`, itself pinned in the script; different languages, no shared code, different authors (C2's
  author wrote every rule from the text before opening the test files and ran the other program only as a black
  box: `checker2/CHECKER2_NOTES.md` section 10, "Independence"); they agree on 2,560 test files and to the last
  digit on the 81 values L;
- an audited specification: `SPEC_v3.0.md` 0a6dfc2a..., accepted as it stands by the referee (`REVIEW_30.md`
  part G); both reports of the record name this hash;
- all components reviewed, each by a reviewer that did not write it: the text (`REVIEW_30.md`), C1
  (`REVIEW_30_PY.md` part P9: "freeze cf8db52b... as it stands"), C2 (`REVIEW_30_JS.md` part J7: "sound as far
  as reviewed: keep frozen"), the acceptance scripts and records (this file). The note in `FROZEN_30.json` asked
  for the verdict of the Node review before the word PROVED: it exists.

Nothing is missing for the word PROVED. Three precisions belong with it:

1. The certificate states the claim at S = Sref (`S_floor` = Sref); (ANN_G20S) for every S <= Sref follows by
   section 11 of the audited text (section 3 above). (ANN_G20S) itself has been PROVED since 8 October through
   the first certificate; `bigbox/THEOREM_G20S.md` does not cite the second one, and need not.
2. "All components reviewed" does not include the generator, and need not: a certificate is checked, not
   trusted. It does not include the interpreters (CPython 3.9.6, Node v25.6.1) or the tools of the system, which
   every such record takes as given. The 3.0 part of C1 and the certificate come from the same author
   (`proto30/PROTO_NOTES.md` section 19), so the independence that counts for this certificate is that of C2,
   of the referee's calculator and of the reviews. The two code reviews and this review are by one reviewer; the
   audit of the text is by another.
3. The records that count are the final ones in `acceptance/` (run from 04:06 on); the first-round records in
   `acceptance/round1_0316/` were made with script versions that this review found wanting, and say the same.

A sentence that carries the first precision, if the lead wants one: "(ANN_G20S) has a second certificate, of the
new kind (wx-cert-3: 81 leaves, each closed by one step on the form `0`), accepted on 9 October 2026 by the two
independent frozen 3.0 checkers under the audited text `SPEC_v3.0.md`; text, both checkers and the acceptance
procedure are each reviewed by a reviewer that did not write them; the certificate speaks about the side Sref, and
section 11 of the text gives the statement for every S <= Sref."

## 8. What I did not examine

- The mathematics of the certificate beyond what the two programs and the referee's calculator establish; the
  generator.
- The scripts on another machine or another sh: finding F3 rests on the behaviour of bash 3.2.57 as `/bin/sh`,
  and the correction (initialised variables, a tested log) does not depend on it.
- `accept_tree30.sh` with a real reference file other than the packing file on a large certificate (only the small
  cases A17 to A20b, B13, B13b).
- Deliberate interference by a process with write access to `acceptance/` during a run (replacing a report or
  the scratch file between two commands of the script).
- The older acceptance scripts and records of `acceptance/` (2.3 to 2.6) beyond the count of `RESULT:` lines in
  their logs; `REVIEW_26.md` covers the 2.6 ones.

## 9. The files of `reviews/r30acc/`

| file | what |
|---|---|
| `acc_attack.py` | builds a sandbox (`setup`), runs the 55 cases (`cases`), compares two versions of the report script on 37 variants (`versions`); the sandbox folder is chosen with `ACC_SBX` (nothing is removed) |
| `acc_fix2.py` | makes `proposed/accept_tree30.sh` from the second version by three exact replacements (`make`), puts it into a sandbox (`install`); `proposed/ACCEPT_TREE30_ffafb155_to_proposed.diff` |
| `acc_fix.py` | the two edits I proposed for the FIRST versions, tried on copies (superseded by the lead's own correction) |
| `acc_versions2.py` | three versions of the report script on 1,397 changed report pairs |
| `acc_record.py` | the records, independently: `sos`, `tree HW`, `tree G20`, `tree G20S`; with a last argument `round1` the first-round records |
| `acc_tables.py`, `acc_summary.py` | the table of section 1.2 from the result files; the table of section 5 from the final records |
| `sbx/`, `sbx2/`, `sbx3/`, `sbx4/` | sandboxes: first versions; second versions; second with two edits (df243ae0..., an intermediate proposal); FINAL versions. They contain, for the cases A25 and B12, deliberately WEAKENED copies of the two checkers (`checker/wxcheck_weak.py`, `checker2/wxcheck2_weak.js`), a file `hostile_cwd/json.py` and a `hook.js`: test objects, never to be used for checking |
| `certs/` | the small certificates and EXPECT files of the cases |
| `h_report30_first_9446a23d.py`, `h_report30_1c01dda7.py`, `accept_tree30_ffafb155.sh`, `H_REPORT30_*.diff` | versions and diffs |
| `out/run_cases_*.txt`, `out/attack_results_*.json`, `out/logs_*/` | console output and results of the three rounds (540403a0_76d16ccd; ffafb155_1c01dda7; proposed_0cd4ff06_1c01dda7 = FINAL; proposed_df243ae0 = the intermediate proposal); kept logs of the first two rounds; the logs of the final round lie in `sbx4/research/wx/acceptance/` |
| `out/run_versions2.txt`, `out/versions2_*.{json,txt}`, `out/run_versions_76d16ccd.txt` | section 2 |
| `out/record_round1_*.txt`, `out/record_final_*.txt` | sections 4 and 5 |
| `out/crossrun_check.txt` | section 6 |
| `logs/runs.log` | start and end of every run of mine |

To repeat the cases on the scripts now on disk: `ACC_SBX=<new name> python -B acc_attack.py setup`, then
`ACC_SBX=<the same> python -B acc_attack.py cases` (one minute).

## Part R. The draft with the statement-file entry `root_region` (9 October 2026)

After the acceptance of the four records: a draft of the report script that lets a statement be
made for the region of the ROOT NODE instead of the header window, for the tree of the hard window (seventeen
labels, five of them with free direction). Everything of mine is in `reviews/r30acc/`
(`rr_tests.py`, `rr_fix.py`, `rr_real2.py`, `rr_table.py`, folder `rr/`, sandbox `sbx5/`, outputs `out/rr_*`).

| file | SHA-256 |
|---|---|
| `acceptance/h_report30_rootregion_draft.py` (413 lines; the DRAFT) | 01de947164812f8830bffe1422a21f027098952a85029a35e9c729283e9c8f1f |
| `acceptance/h_report30.py` (the reviewed version it starts from) | 1c01dda73b9ff5814ba52207aa43ef25145ab84baf97c5d580a156adc1c7bc78 |
| `bigbox/hullh/HULLH_exact_v2.json` (the region file) | 08e736e9d712e89d98ad86661724b705c82bafaa01f6e1c8d44711f5d138340c |
| `bigbox/hullh/HULLH_exact.json` (version 1) | 5e7315162221f52e7fe6579c771925b1f780bcd4e47e5374fcce4f1341363e20 |
| `bigbox/hullh/mk_exact_window.py` | 19e5f131d82f07b6545b4b7e6be7fa19d840142d58f11adc7fd20cdf1dd657cf |
| `acceptance/EXPECT_HULLH_v2.json` | 03fd1f5ed622ff3d4af4567579d134654646f6be6d17c619a56eb789e3266ab7 |
| `proto30/out/hullh/v2/HULLH_v2.jsonl.gz` (the PARTIAL certificate; 222 node lines) | 37c57e894540ef119905c9ce32663b0ef2adf40381cbfa1beda1b376da7f20b4 |
| `r30acc/rr/proposed/h_report30_rootregion.py` (452 lines; MY PROPOSAL: the draft with five small edits) | 0314aa1f8f742cd7156cc490764c8a308663ba87f359e0d8b97fb3d7189950db |

**Verdict. Draft 01de9471... fits.** It is the reviewed script plus 68 added lines and 1 changed line, in three
places (5 lines of the docstring; the entry name in the set of known entries; a block of 62 lines directly
before the RESULT line; `rr/H_REPORT30_1c01dda7_to_rootregion_01de9471.diff`). Without the entry it behaves as the
reviewed version on every input I have; with it I found no way to end ACCEPTED for a certificate whose root, as
the two programs checked it, is not the region of the file. I still recommend the proposed file 0314aa1f...
instead: the draft reads the REGION FILE more loosely than a certificate is read (seven cases), takes
`"root_region": null` for "no entry", and refuses one kind of good certificate. None of these nine cases is a
wrong acceptance of a certificate, and none can occur with the real region file, which is well formed.

### R.1 Question (1): without the entry

The draft against the reviewed version, each run by hand as the shell script runs it (`rr_tests.py q1`,
`out/rr_q1_draft_01de9471.txt`): on the 1,397 changed report pairs of section 2 (four bases) the exit code, the
RESULT line and the whole sequence of ok/FAIL flags are the same in all 1,397; the draft's whole output, after
removing its one new line `root region: not part of this statement (the statement is the header window)`,
equals the reviewed version's output character for character in all 1,397; the new line always stands directly
before the RESULT line. The same on 50 further runs (eleven statement files, among them a wrong window, a wrong
schema, a file that is not JSON, against four certificates; reports of another certificate; a missing report,
certificate or `FROZEN.json`; a wrong number of arguments). On two real records (G20S_SOS and G20_v30, with
their final reports): the same again (`out/rr_real2_proposed_0314aa1f.txt`, for the proposed file).

### R.2 Question (2): with the entry

59 cases (`rr_tests.py q2`). Base: my two-level harness (a root split into two terminal leaves), with the header
window made smaller than the root in one interval and one radius, as in the intended use. For each case both
frozen programs are run on the certificate and then the script by hand with their exit codes; "accepted" is the
shell script's rule (three exit codes 0, both first lines PASS).

| case | what | should be accepted | C1, C2 | draft 01de9471 | proposed 0314aa1f |
|---|---|---|---|---|---|
| R01 | control: both programs accept; the region file is the root node's data (root larger than the header window) | yes | PASS, PASS | ACCEPTED | ACCEPTED |
| R02 | control: the same, gzip | yes | PASS, PASS | ACCEPTED | ACCEPTED |
| R03 | the region file writes every number differently (p/q as 3p/3q): equal as rationals | yes | PASS, PASS | ACCEPTED | ACCEPTED |
| R04 | control without the entry root_region (the statement is the header window) | yes | PASS, PASS | ACCEPTED | ACCEPTED |
| R05 | region file: one interval end larger than the root's (xi_{7,2} up to 1/999) | no | PASS, PASS | not accepted | not accepted |
| R06 | region file: one interval end smaller than the root's | no | PASS, PASS | not accepted | not accepted |
| R07 | region file: the arc centre of one label is another rotation | no | PASS, PASS | not accepted | not accepted |
| R08 | region file: the lower arc end of one label is another rotation | no | PASS, PASS | not accepted | not accepted |
| R09 | region file: the upper arc end of one label is another rotation | no | PASS, PASS | not accepted | not accepted |
| R10 | region file: side interval [Sref, Sref], the root has [4, Sref] | no | PASS, PASS | not accepted | not accepted |
| R11 | EXPECT names a wrong SHA-256 for the region file | no | PASS, PASS | not accepted | not accepted |
| R12 | the region file does not exist | no | PASS, PASS | not accepted | not accepted |
| R13 | root_region is a string (the path), not an object | no | PASS, PASS | not accepted | not accepted |
| R14 | root_region has a third key | no | PASS, PASS | not accepted | not accepted |
| R15 | root_region lacks the key sha256 | no | PASS, PASS | not accepted | not accepted |
| R16 | root_region: null in the statement file (the reviewed version rejects the unknown entry) | no | PASS, PASS | ACCEPTED **(not as it should)** | not accepted |
| R17 | region file with other keys beside S, window.box, root_arc (as the real file has): ignored | yes | PASS, PASS | ACCEPTED | ACCEPTED |
| R18 | region file: a box entry for a label outside the label set (label 4 with sixteen labels) | no | PASS, PASS | not accepted | not accepted |
| R19 | region file: no arc for label 17 | no | PASS, PASS | not accepted | not accepted |
| R20 | region file: an arc entry with a fourth key | no | PASS, PASS | not accepted | not accepted |
| R21 | region file: a box entry with THREE intervals (the third is not looked at) | no | PASS, PASS | ACCEPTED **(not as it should)** | not accepted |
| R22 | region file: an interval with THREE ends (the third is not looked at) | no | PASS, PASS | ACCEPTED **(not as it should)** | not accepted |
| R23 | region file: a rotation with THREE numbers (the third is not looked at) | no | PASS, PASS | ACCEPTED **(not as it should)** | not accepted |
| R24 | region file: an interval end as the JSON number 0.001 where the root has "1/1000" (a float is another number) | no | PASS, PASS | not accepted | not accepted |
| R25 | region file: ends written " -1/1000" and "+1/1000 " (not the number format of the specification; equal for Python's Fraction) | no | PASS, PASS | ACCEPTED **(not as it should)** | not accepted |
| R26 | region file: ends written "-0.001" and "1e-3" (decimal strings; equal for Python's Fraction) | no | PASS, PASS | ACCEPTED **(not as it should)** | not accepted |
| R27 | region file with the key S twice (the first [0, 0], the second the root's): Python takes the last | no | PASS, PASS | ACCEPTED **(not as it should)** | not accepted |
| R28 | certificate: a second node with the id of the root (a copy of a child, renamed) | no | FAIL, FAIL | not accepted | not accepted |
| R29 | certificate: the root's line a second time, at the end | no | FAIL, FAIL | not accepted | not accepted |
| R30 | certificate: the root's id written with a JSON escape ("ro\u006ft") in its own line: the same id after decoding | yes | PASS, PASS | ACCEPTED | ACCEPTED |
| R31 | certificate: the header's root is the JSON number 5, and so is the root's id | no | FAIL, FAIL | not accepted | not accepted |
| R32 | certificate: the header names a CHILD as the root; the region file is the true root's data | no | FAIL, FAIL | not accepted | not accepted |
| R33 | certificate: the header names a CHILD as the root; the region file is that child's data | no | FAIL, FAIL | not accepted | not accepted |
| R34 | certificate: the root's line has the key box TWICE (the true box, then a larger one); the region file is the larger box, which Python's json reads | no | FAIL, FAIL | not accepted | not accepted |
| R35 | certificate: inside the root's box the label key "1" stands twice | no | FAIL, FAIL | not accepted | not accepted |
| R36 | certificate: the root has a key the format does not define ("note") | no | FAIL, FAIL | not accepted | not accepted |
| R37 | certificate: the root has a round (one harmless step): its region is still its own data | yes | PASS, PASS | ACCEPTED | ACCEPTED |
| R38 | certificate and region file: the same arc centre (1, 1/1000), which is not a rotation | no | FAIL, FAIL | not accepted | not accepted |
| R39 | certificate: two ends of the root's box are JSON numbers (-0.001, 0.001) | no | FAIL, FAIL | not accepted | not accepted |
| R40 | certificate: the root writes -1/1000 and 1/1000 as "-2/2000" and "3/3000"; the region file has them in lowest terms | yes | PASS, PASS | ACCEPTED | ACCEPTED |
| R41 | certificate: leading zeros ("-001/1000", "1/01000"), which the number format allows | yes | PASS, PASS | ACCEPTED | ACCEPTED |
| R42a | certificate: an interval end of the root written ' 1/1000' (Python's Fraction would read it; not the number format) | no | FAIL, FAIL | not accepted | not accepted |
| R42b | certificate: an interval end of the root written '+1/1000' (Python's Fraction would read it; not the number format) | no | FAIL, FAIL | not accepted | not accepted |
| R42c | certificate: an interval end of the root written '1e-3' (Python's Fraction would read it; not the number format) | no | FAIL, FAIL | not accepted | not accepted |
| R42d | certificate: an interval end of the root written '0.001' (Python's Fraction would read it; not the number format) | no | FAIL, FAIL | not accepted | not accepted |
| R42e | certificate: an interval end of the root written '1/1000 ' (Python's Fraction would read it; not the number format) | no | FAIL, FAIL | not accepted | not accepted |
| R42f | certificate: an interval end of the root written '1_0/10000' (Python's Fraction would read it; not the number format) | no | FAIL, FAIL | not accepted | not accepted |
| R42g | certificate: an interval end of the root written '\uff11/1000' (Python's Fraction would read it; not the number format) | no | FAIL, FAIL | not accepted | not accepted |
| R43 | certificate: a carriage return between two keys of the root's line (legal JSON white space; Python's text mode ends a line there) | yes | PASS, PASS | not accepted **(not as it should)** | ACCEPTED |
| R44 | certificate with CR LF line ends | yes | PASS, PASS | ACCEPTED | ACCEPTED |
| R45 | certificate: the root has no key parent | no | FAIL, FAIL | not accepted | not accepted |
| R46 | certificate: the root carries an assumption (and its children too) | no | FAIL, FAIL | not accepted | not accepted |
| R47 | control: one node, root = terminal leaf; window, tube and root as in my harness T | yes | PASS, PASS | ACCEPTED | ACCEPTED |
| R48 | the header window lies in the tube, the ROOT box is wider than the tube in xi_{7,2}, and the root claims to be terminal | no | FAIL, FAIL | not accepted | not accepted |
| R49 | the header window lies in the tube, the ROOT arc of label 7 reaches beyond the tube radius, and the root claims to be terminal | no | FAIL, FAIL | not accepted | not accepted |
| R50 | region file: an interval end "1/0" | no | PASS, PASS | not accepted | not accepted |
| R51 | region file: an interval end as the JSON integer 1 (the root has "1/1000") | no | PASS, PASS | not accepted | not accepted |
| R52 | region file: the lower side end as the JSON integer 4 where the root has the string "4" | no | PASS, PASS | ACCEPTED **(not as it should)** | not accepted |
| R53 | certificate: a second node whose id is the root's after decoding only (written "ro\u006ft") | no | FAIL, FAIL | not accepted | not accepted |

Cases: 59; not as they should be: draft 9, proposed version 0. Accepted by the proposed version: 12.

The lead's list: a second node with the root's id, R28, R29, R53 (both programs reject a repeated id, "node id
'root' occurs twice" / "duplicate node id (first at line 2)", and the script counts two); an id that differs
only after decoding, R30 (the same id for all three readers, rightly accepted) and R53; a root with other keys,
R36 (an undefined key: both reject), R37 (rounds: accepted, by design; `forms` is the only optional key of a
node); numbers written differently, R03, R40, R41 (accepted: equal as rationals, which is also how both programs
compare; I agree); an arc centre that is not a rotation, R38 (both reject; the script too); a region file with
other keys, R17 (ignored, as the real file needs: it has seventeen top-level entries), R18 to R20 (another label
set or another arc key: refused); the header's root not a string, R31 (both reject; the script too); a first
line that is not the header the programs read: the ten header files of section 1.1, and R44.

Why the node the script compares is the node both programs took as the root, for every certificate they accept:
- the bytes: each report's hash of the certificate is compared with the script's own, as before;
- the id: taken from the same header field (compared with C1's report; both programs reject a root that is not a
  string); ids are JSON strings compared after decoding, character for character, by all three; both programs
  reject a repeated id, so exactly one line has it;
- the content of that line: Python's `json` reads what the programs read. The one difference, a repeated key
  (Python keeps the last value, both programs reject the line: R34, R35), is excluded by their PASS. Numbers:
  both programs accept only strings `-?[0-9]+` or `-?[0-9]+/[0-9]+` (R39, R42a to R42g), and Python's Fraction
  reads those with the same value;
- the lines: both programs end a line at a line feed only. The draft's text mode also ends one at a carriage
  return. That can only make it stop with an error (R43): a piece of a one-object line cut at a carriage return
  is never a complete JSON value.

The nine cases where the draft is not as it should be:

| cases | what | what the proposed file does |
|---|---|---|
| R21, R22, R23 | a third interval, a third interval end, a third number of a rotation in the REGION file is not looked at | every shape must be exact |
| R25, R26, R52 | numbers of the REGION file that are not in the specification's format (blanks, a sign `+`, "1e-3", "-0.001", the JSON integer 4) are read by Python's Fraction | a number must be a string `p` or `p/q`, on both sides |
| R27 | a repeated key in the REGION file: the last one counts | a repeated key is an error |
| R16 | `"root_region": null` counts as "no entry" (the reviewed version rejects the unknown entry) | a present entry must be an object |
| R43 | a good certificate with a carriage return inside a node line is refused | lines end at line feeds only |

### R.3 Question (3): is "exactly equal to the region file" the right comparison?

Yes. Section 2 of the text: "F(N) := the set of feasible configurations with: xi_ik in [lo_ik, hi_ik] for all
i,k; a_i in the arc of square i for all i; S in [S_lo, S_hi]; and all assumptions of N satisfied. F(N) is defined
by the data N has when it is created and never changes." The root has no assumptions (root condition). So
F(root) is given by the root's side interval, box and arcs (centre and both end rotations of each label) and by
nothing else of the root: not by its rounds, its closure or its `forms`. I agree about the rounds: they change
the store, which is a set of statements true on F(root), never F(root) itself (R37; the roots of the real
certificates have `rounds` and `close` as their only other keys). The draft compares exactly these data, plus
`parent` = null and the label set. Equality as rational numbers is right. Equality of the three rotations
(c, lo, hi) is sufficient and a little more than necessary (the same arc has other descriptions; a region
smaller than the root is refused although its statement would be true, R06). The label set and the reference
file enter F(root) through the coordinates and are pinned as before (`labels`, the packing hash). The header
window need not be compared for the root-region statement; keeping the test "header window = EXPECT window" is
harmless and keeps the record complete (both programs test that the root contains it).

One thing the new statement depends on in a way the old one did not: that both programs test the node
conditions of the root on the root's OWN data and use the header window for nothing but the comparison "root
contains window". Checked in the code: C1 `initial_store(node)` (lines 1455 to 1463) takes the node's data only;
the window occurs only in the header's validation, in `root_failure` (2624 to 2654, which compares and changes
nothing) and in a report key; inside a node's check the header is used for the tube alone (2586 to 2588). C2
`initialStore(node)` (1928 to 1936); the window only in the header's validation, in `checkRoot` (3332 to 3375,
which compares and changes nothing) and in a report key; a node's check uses the header for the tube alone
(line 3203). Checked by test: R48 and R49 (the header window lies in the tube, the root reaches beyond the tube
in one interval, or in one arc, and claims to be terminal): both programs reject.

### R.4 Question (4): does the sentence of the proof carry the statement?

As mathematics, yes. The proof of the THEOREM of section 7 says "by induction over the finite tree, every
configuration of F(N), N closed, lies in the tube: (a) F(N) is empty; (b) the final store holds on F(N) and
implies the tube; (c) covering (section 6)". The induction uses the closing conditions and the tree conditions
only, never the window or the other root conditions; it holds for N = root; and section 2 says what F(root) is.
But it is a claim inside a proof, and the THEOREM as stated speaks about the window. A theorem document should
not have to cite a sentence of a proof: the text being frozen, a note on use in `SPEC_v3.0_NOTES.md` is the
right place. Wording I would stand behind:

    COROLLARY (root region; from the proof of the THEOREM of section 7). If a certificate satisfies all
    conditions of section 7, every configuration of F(root) lies in the tube. By section 2 and the root
    condition "EMPTY assumption list", F(root) is the set of feasible configurations with S_lo <= S <= S_hi,
    every xi_ik in the root's interval [lo_ik, hi_ik] and every a_i in the root's arc
    {R(psi) rho_i u_i : angle(P_i^-) <= psi <= angle(P_i^+)}  (S_lo, S_hi, lo, hi, rho, P^-, P^+ the root's data).
    Proof: the induction claim of the proof of the THEOREM, for N = root; that induction uses the closing
    conditions (a), (b), (c) and the tree conditions only, not the header window.
    As in section 11, first paragraph: the root's box and arcs do not mention S, and S_lo <= Sref <= S_hi; so
    every feasible configuration with S <= Sref whose positions and directions lie in the root's box and arcs
    lies in the tube (it is feasible for the side Sref, hence in F(root)).
    A theorem that uses the corollary states its region by the root's data (a file with its hash: side interval,
    box, and for every label the centre and the two end rotations of the arc), not by the header window, and its
    acceptance record must show that the root node of the certificate is that region (statement-file entry
    `root_region`).

The remark on free directions belongs in the theorem itself, as section 11 item (3) asks: a configuration has one
side direction a_i per square; the four side directions of a square are a quarter turn apart, so one of them is
R(psi) u_i with |psi| <= pi/4, and the square, its corners and so the feasibility of the configuration do not
depend on which of the four is taken. The theorem then speaks about that representative.

### R.5 Question (5): the exact claims of `mk_exact_window.py` for the free labels

Recomputed with my own rational arithmetic (`rr_tests.py real`, `out/rr_real.txt`), on the version 2 file:

- the five free labels are 3, 4, 9, 15, 17; their root arc has centre the identity and ends rot(-+tau),
  tau = 4147/10000, that is (cos, sin) = (82802391/117197609, -+82940000/117197609): as in the file;
- "at least a quarter turn": (tau + 1)^2 = 200137609/100000000 >= 2. With 0 < tau < 1 this is the half-angle
  2 atan(tau) >= pi/4 (tan(pi/8) = sqrt(2) - 1) and < pi/2. The test is sharp: it fails for 4142/10000 and holds
  from 4143/10000 on. (The script's `assert (free_tau + 1) ** 2 >= 2` alone would also pass for tau <= -1 - sqrt(2);
  the root test in the same loop, cos > 0 and sin >= alpha > 0, gives 0 < tau < 1. Fine for these numbers.)
- the root test: cos > 0 and sin = 82940000/117197609 = 0.707694 >= 7/10, the header window radius of the five
  labels. And 7/10 < pi/4: the header window of a free label is less than a quarter turn, which is why the
  statement must be the root region's;
- label 4 against the tube: tube radius 1 (allowed: <= 1); sin = 0.707694 <= 1 - 1/6 = 5/6; cos > 0; the tube
  box of label 4 is its root box. So a node whose data for label 4 are still the root's passes the terminal
  test for label 4, and nothing is asked of the rattler. (The script does not test this; it holds.)
- the tube of the sixteen other labels is the window G20S of `bigbox/THEOREM_G20S.md` (all 32 intervals, radius
  1/10, no centres): the four other free labels must end within 1/10, like every other.

Also: versions 1 and 2 of the region file have the same box, window centres, tube, S, Sref, S_floor, and differ
in `root_arc` and `window.alpha` for exactly the labels 3, 4, 9, 15, 17. In version 2 all 172 numbers of S,
`window.box` and `root_arc` are strings of the specification's format, every shape is exact, every rotation is
a unit rotation, no key is repeated. Made again with a copy of the script from the skeleton
(`rr/regen_HULLH_exact_v2.json`): fifteen entries equal the file on disk; the file on disk has two more that the
script does not write, `version_note` and `root_arc_as_angles_floats` (information only). `EXPECT_HULLH_v2.json`
equals the script's output except for its name; its window and tube, expanded by my own code, are those of the
region file.

The partial certificate, read by my own code: 222 node lines, exactly one with the header's root id `K00`;
parent null, no assumption, seventeen labels; root node = the region of version 2 in the side interval, all 68
interval ends and all 17 arcs; against version 1 the arcs differ for exactly the labels 3, 4, 9, 15, 17; header
window and tube = those of the version 2 file. The draft and the proposed file say the same on it (all root lines
ok with version 2; one FAIL line with version 1, naming those five labels; 7 seconds): the lead's test,
reproduced.

### R.6 The proposed file

`r30acc/rr/proposed/h_report30_rootregion.py`, sha256
0314aa1f8f742cd7156cc490764c8a308663ba87f359e0d8b97fb3d7189950db: the draft with 54 lines added and 15 removed
(`rr/proposed/H_REPORT30_ROOTREGION_01de9471_to_proposed.diff`; made by `rr_fix.py make` from the draft by exact
replacements):

1. the region file is read strictly (no repeated key; every compared number, of the region file and of the root
   node, a string `p` or `p/q`; every box entry exactly two intervals of two ends, every rotation exactly two
   numbers), and the root's own line is parsed once more with the same strict reader;
2. the entry `root_region`, if the key is present, must be an object;
3. node lines end at line feeds only (`newline="\n"`), as for both programs;
4. wording: the last line of the block names the entries of the region file that ARE the region
   ("... the ROOT REGION of '<file>' (its entries S, window.box and root_arc)"): the file's `window` also holds
   the header window's radii and centres, which are not part of the root region;
5. wording: the docstring no longer calls the file a draft; it says where the text comes from.

Tested under this hash: without the entry, the 1,397 report pairs and the 50 further runs: identical to the
reviewed version apart from the one line (`out/rr_q1_proposed_0314aa1f.txt`); the 59 cases: all as they should
be, 12 accepted (`out/rr_q2_proposed_0314aa1f.txt`); two REAL accepted certificates with their final reports
(G20S_SOS, 153 node lines, wx-cert-3; G20_v30, 593 node lines, seventeen labels) and a region file taken from
their own root by my code (`rr_real2.py`, `out/rr_real2_proposed_0314aa1f.txt`): ACCEPTED with exit code 0, all
nine lines of the block ok; with one interval end of the region changed: NOT ACCEPTED, exit code 1; the partial
hard-window certificate as above, also with the region file given by a path relative to the working folder
(`out/rr_real_report_*_0314aa1f.txt`). Two earlier states of the proposal (fc0666ad..., fddcb5f6...: without
edits 4 and 5, without edit 5) passed the same tests; their outputs are kept beside these.

### R.7 For the use

- `acceptance/EXPECT_HULLH_v2.json` has NO entry `root_region` yet (the script that writes it does not write
  one). A record made with it as it is states the header window only, whose radius 7/10 for the free labels is
  less than a quarter turn. The entry: `"root_region": {"file": "bigbox/hullh/HULLH_exact_v2.json", "sha256":
  "08e736e9d712e89d98ad86661724b705c82bafaa01f6e1c8d44711f5d138340c"}`.
- How to read a record: with the entry the report part has, directly before the RESULT line, nine more ok lines
  and the line "the statement of this record is made for the ROOT REGION of ..."; without it, the line "root
  region: not part of this statement (the statement is the header window)". A record for the hard window must
  have the former.
- `accept_tree30.sh` (0cd4ff06...) calls `acceptance/h_report30.py` by that name and need not change: the new
  version can replace that file (by write and rename, with no acceptance run in progress); every later log then
  names the new hash, and for a statement without the entry the result is the reviewed one.

### R.8 Not examined

The generator of the hard-window tree and the tree itself (it is not finished: the partial certificate has open
nodes, and both programs say FAIL on it, as they must); the 29 self-checks of `mk_exact_window.py` for the labels
that are not free (only that the script reproduces the file); the skeleton it starts from; the theorem that will
use the record.

Files of this part: `rr_tests.py` (`setup`, `q1`, `q2`, `real`), `rr_fix.py` (`make`, `install`), `rr_real2.py`,
`rr_table.py`; `rr/R01` ... `rr/R53` (certificate, region file and statement file of each case), `rr/real/`,
`rr/proposed/`, `rr/h_report30_rootregion_draft_01de9471.py`, `rr/mk_exact_window_19e5f131.py`; `sbx5/` (sandbox:
the reviewed script, the proposed file under the draft's name, the draft as `..._draft_orig.py`, a copy of the
region file); `out/rr_*.txt`,
`out/rr_q2_results_*.json`, `out/table_rr_cases.md`.
