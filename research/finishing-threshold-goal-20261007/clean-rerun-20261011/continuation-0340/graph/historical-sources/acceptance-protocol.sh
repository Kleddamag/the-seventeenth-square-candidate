#!/bin/sh
# Lead's acceptance run of one certificate (tree) under SPEC version 3.0 (schema wx-cert-2 or wx-cert-3) with the
# two FROZEN 3.0 checkers. The frozen files (Python checker, Node checker, specification text) and their SHA-256
# are read from acceptance/FROZEN_30.json, which the lead writes when the checkers are frozen; without that file
# nothing is run. See h_report30.py for what is compared.
# usage: accept_tree30.sh NAME CERT.jsonl[.gz] EXPECT.json [REFERENCE_FILE SHA256]
# With REFERENCE_FILE and SHA256 the certificate is checked relative to that reference file instead of the
# packing file (both checkers: --packing FILE --expect-packing-sha256 SHA256); EXPECT.json must then carry the
# same hash as "packing_sha256".
# Writes acceptance/ACCEPT_<NAME>.log, acceptance/<NAME>_C1.json, acceptance/<NAME>_C2.json.
# One process at a time (C1, then C2, then the report). Start it through locks/run_slot.sh.
W="$(cd "$(dirname "$0")/.." && pwd)"
R="$(cd "$W/../.." && pwd)"
PY="$R/local-research/claude-20261002/.venv/bin/python"
NAME="$1"; CERT="$2"; EXPECT="$3"; REFFILE="$4"; REFSHA="$5"
[ -n "$NAME" ] && [ -n "$CERT" ] && [ -n "$EXPECT" ] || { echo "usage: accept_tree30.sh NAME CERT EXPECT.json [REFERENCE_FILE SHA256]" >&2; exit 2; }
case "$CERT" in /*) ;; *) CERT="$(pwd)/$CERT";; esac
case "$EXPECT" in /*) ;; *) EXPECT="$(pwd)/$EXPECT";; esac
if [ -n "$REFFILE" ]; then case "$REFFILE" in /*) ;; *) REFFILE="$(pwd)/$REFFILE";; esac; fi
FROZEN="$W/acceptance/FROZEN_30.json"
[ -f "$FROZEN" ] || { echo "acceptance/FROZEN_30.json missing: the 3.0 checkers are not frozen" >&2; exit 2; }
# FROZEN_30.json itself is pinned here (it names the three frozen files; an edited copy could name others).
FROZEN_SHA="6d65a0705c039bbf2f48acabb7f12275871af6b7b8fa308c0671ea6518b30803"
[ "$(shasum -a 256 "$FROZEN" | cut -d' ' -f1)" = "$FROZEN_SHA" ] || { echo "acceptance/FROZEN_30.json does not have the pinned SHA-256 $FROZEN_SHA" >&2; exit 2; }
[ -f "$CERT" ] || { echo "certificate $CERT missing" >&2; exit 2; }
[ -f "$EXPECT" ] || { echo "expectation file $EXPECT missing" >&2; exit 2; }
REFOPT=""
if [ -n "$REFFILE" ]; then
  [ -n "$REFSHA" ] || { echo "reference file given without its SHA-256" >&2; exit 2; }
  [ "$(shasum -a 256 "$REFFILE" | cut -d' ' -f1)" = "$REFSHA" ] || { echo "reference file does not have the stated SHA-256" >&2; exit 2; }
  REFOPT="--packing $REFFILE --expect-packing-sha256 $REFSHA"
fi
# (python -I -B here too: this call decides WHICH program files are run, and without -I a file json.py in the
# folder the script is started from, or on PYTHONPATH, would answer in place of FROZEN_30.json:
# reviews/REVIEW_30_ACCEPT.md, cases B12, B12b)
fz() { "$PY" -I -B -c 'import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]][sys.argv[3]])' "$FROZEN" "$1" "$2"; }
C1="$W/$(fz C1 file)"; C2="$W/$(fz C2 file)"; SP="$W/$(fz SPEC file)"
[ -f "$C1" ] || { echo "frozen Python checker $C1 missing" >&2; exit 2; }
[ -f "$C2" ] || { echo "frozen Node checker $C2 missing" >&2; exit 2; }
[ -f "$SP" ] || { echo "frozen specification text $SP missing" >&2; exit 2; }
LOG="$W/acceptance/ACCEPT_$NAME.log"
J1="$W/acceptance/${NAME}_C1.json"; J2="$W/acceptance/${NAME}_C2.json"
TMP="$W/acceptance/.tmp_$NAME"
# The five variables that decide the exit code start HERE as "not accepted", and a log that cannot be written
# stops the run: if the redirection of the brace group below fails, sh skips the group and goes on, and variables
# of these names in the caller's environment would otherwise decide (reviews/REVIEW_30_ACCEPT.md, cases B02, B03).
rc1=1; rc2=1; rcr=1; first1=""; first2=""
( : > "$LOG" ) 2>/dev/null || { echo "cannot write the log $LOG" >&2; exit 2; }
rm -f "$J1" "$J2"
{
echo "acceptance run $(date '+%Y-%m-%d %H:%M:%S')  certificate $CERT"
echo "sha256 certificate:        $(shasum -a 256 "$CERT" | cut -d' ' -f1)"
echo "sha256 ${C1#$W/}:  $(shasum -a 256 "$C1" | cut -d' ' -f1)   (FROZEN_30.json: $(fz C1 sha256))"
echo "sha256 ${C2#$W/}:  $(shasum -a 256 "$C2" | cut -d' ' -f1)   (FROZEN_30.json: $(fz C2 sha256))"
echo "sha256 ${SP#$W/}:  $(shasum -a 256 "$SP" | cut -d' ' -f1)   (FROZEN_30.json: $(fz SPEC sha256))"
echo "sha256 packing file:       $(shasum -a 256 "$R/upper-packing-certificate.json" | cut -d' ' -f1)"
echo "sha256 accept_tree30.sh:   $(shasum -a 256 "$0" | cut -d' ' -f1)"
echo "sha256 h_report30.py:      $(shasum -a 256 "$W/acceptance/h_report30.py" | cut -d' ' -f1)"
echo "sha256 FROZEN_30.json:     $(shasum -a 256 "$FROZEN" | cut -d' ' -f1)"
echo "sha256 EXPECT file:        $(shasum -a 256 "$EXPECT" | cut -d' ' -f1)  ${EXPECT#$W/}"
echo "interpreters:              python $("$PY" -I -B -c 'import platform; print(platform.python_version())') ($PY); node $(env -u NODE_OPTIONS node --version) ($(command -v node))"
[ -n "$REFFILE" ] && echo "REFERENCE FILE used instead of the packing file: $REFFILE  sha256 $REFSHA"
echo "--- C1 (python -I -B, isolated mode: no PYTHON* variables, the script's folder not on the module path; options: ${REFOPT:-default})"
( cd "$(dirname "$C1")" && VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1 /usr/bin/time -l "$PY" -I -B "$(basename "$C1")" "$CERT" --json "$J1" $REFOPT ) > "$TMP" 2>&1; rc1=$?
first1="$(head -n 1 "$TMP")"
head -n 10 "$TMP"; grep -E "real|maximum resident" "$TMP"; echo "exit code C1: $rc1"
echo "first output line C1: [$first1]"
echo "--- C2 (node; options: ${REFOPT:-default})"
( cd "$(dirname "$C2")" && /usr/bin/time -l env -u NODE_OPTIONS node --max-old-space-size=12000 "$(basename "$C2")" "$CERT" --json "$J2" $REFOPT ) > "$TMP" 2>&1; rc2=$?
first2="$(head -n 1 "$TMP")"
head -n 10 "$TMP"; grep -E "real|maximum resident" "$TMP"; echo "exit code C2: $rc2"
echo "first output line C2: [$first2]"
rm -f "$TMP"
echo "--- report"
"$PY" -I -B "$W/acceptance/h_report30.py" "$CERT" "$J1" "$J2" "$rc1" "$rc2" "$EXPECT" "$FROZEN"; rcr=$?; echo "exit code report: $rcr"
# An exit code 0 alone is not an acceptance (the help option of the frozen 2.6 programs exits 0 without checking
# anything): the first output line of each program must be exactly PASS, besides the report tests above.
if [ "$first1" = "PASS" ] && [ "$first2" = "PASS" ]; then echo "FIRST LINES: both PASS"; else echo "FIRST LINES: NOT BOTH PASS"; fi
} > "$LOG" 2>&1
tail -n 64 "$LOG" | cut -c1-260
# Exit code: 0 only for an acceptance. Decided from the exit codes and first lines kept in shell variables, NOT by
# searching the log: the log contains text that a certificate controls (a node id may contain line feeds), so a
# line "RESULT: ACCEPTED" somewhere in a log proves nothing; only its LAST lines and this exit code count
# (found by the review reviews/REVIEW_30_ACCEPT.md, case A28b, 2026-10-09; no record made before was affected).
[ "$rcr" = 0 ] && [ "$rc1" = 0 ] && [ "$rc2" = 0 ] && [ "$first1" = "PASS" ] && [ "$first2" = "PASS" ]
