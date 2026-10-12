#!/usr/bin/env python3
"""Lead's post-check of an acceptance run under SPEC version 3.0 (schemas wx-cert-2 and wx-cert-3).

usage: h_report30.py CERT.jsonl[.gz] C1.json C2.json EXIT_C1 EXIT_C2 EXPECT.json FROZEN.json

Same as h_report26.py (version 2.6), plus:
  * the THREE FROZEN FILES (Python checker, Node checker, specification text) are named with their SHA-256 in
    FROZEN.json (written by the lead when the checkers are frozen, {"C1": {"file", "sha256"}, "C2": {...},
    "SPEC": {...}}, paths relative to the window-extension folder); this script recomputes the three hashes
    and fails if one differs (in the 2.6 script that comparison was left to the reader of the log);
  * the SCHEMA of the statement (EXPECT.json "schema", absent = "wx-cert-2") must be the header's and the one
    both reports say they checked under;
  * ARC CENTRES of the window and of the tube (SPEC 3.0 section 8): EXPECT.json may give, inside "window" and
    inside "tube", a map "centre": {"<label>": ["g", "s"], ...} for the labels whose centre is not the
    identity; the header's centres (absent = identity for every label) must be exactly these rotations, and
    each report must say whether the header had centre maps (keys "window_centres", "tube_centres");
  * the exact value L of the first accepted `0` step of every leaf that is closed by such a step (report key
    "zero_step_L" of the node, a string "p/q" or "p") must be THE SAME RATIONAL NUMBER in both reports: L is
    determined by the specification, so two independent checkers must agree on it digit for digit. A leaf for
    which only one report has the key is a failure.
Changed 2026-10-09 03:30, after the first run on a wx-cert-2 tree (HW_v30) ended NOT ACCEPTED through a flaw of
THIS script: it demanded the report keys `schema`, `window_centres`, `tube_centres` from the Python checker,
which writes them only under wx-cert-3 (under wx-cert-2 its report has exactly the 2.6 keys). For a wx-cert-2
statement an absent key of C1 now counts as "wx-cert-2" / "no centre maps"; for wx-cert-3 nothing changed (the
acceptance of G20S_SOS was made with the earlier, stricter version). The wording of one check line was
corrected too ("centre maps occur only under wx-cert-3").
Changed again 2026-10-09 03:50 (review reviews/REVIEW_30_ACCEPT.md, case A28b): every string that comes from a
certificate, a report or a path is printed with %r, so that no such text can begin a line of the log (a node id
may contain line feeds). The acceptance script no longer searches the log; it uses this script's exit code.
Added 2026-10-09 06:30 (the lead's draft 01de9471... with the five edits of its review, reviews/REVIEW_30_ACCEPT.md
part R; this text is the reviewer's file reviews/r30acc/rr/proposed/h_report30_rootregion.py): optional EXPECT entry
`root_region` {file, sha256}: the statement is then made for the region of the ROOT NODE (SPEC 3.0 section 7,
induction claim of the proof), and the root node of the certificate is compared exactly with the region file
(box, arcs with centres and end rotations, side interval, empty assumptions, parent null). For this the script
also reads every node line of the certificate (to find the one node with the header's root id). The region file
is read strictly: no repeated key, every compared number a string "p" or "p/q", every shape exact
(review reviews/REVIEW_30_ACCEPT.md part R).
Reads only: the first line (header) of the certificate, the two reports, EXPECT.json, FROZEN.json and the three
frozen files (for their hashes). Standard library only. A crash is never an acceptance.
"""
import gzip
import hashlib
import json
import os
import re
import sys
from fractions import Fraction

PIN = "24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7"
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LABELS = [i for i in range(1, 18) if i != 4]      # replaced in _main() when the statement has 17 labels


def out(text=""):
    """Print ONE line. Every control character of the text (line feed, carriage return, escape, ...) is written
    as an escape, so that no string from a certificate, a report or a path can start a new line of the log or
    hide one (review reviews/REVIEW_30_ACCEPT.md, case A28b)."""
    sys.stdout.write("".join(c if (32 <= ord(c) < 127 or ord(c) > 159) else "\\x%02x" % ord(c) for c in str(text)) + "\n")


def fr(x):
    return Fraction(x)


NUM_FORMAT = re.compile(r"-?[0-9]+(?:/[0-9]+)?")


def num(x):
    """A number of the region file or of the root node, read as both checkers read a certificate (SPEC 3.0
    section 10): a string -?digits or -?digits/digits. Anything else (a JSON number, blanks, a sign +, a decimal
    point, an exponent) is an error, never a silent reading. A zero denominator is an error of Fraction."""
    if type(x) is not str or NUM_FORMAT.fullmatch(x) is None:
        raise ValueError("not a number string of the format p or p/q: %r" % (x,))
    return Fraction(x)


def no_duplicate_keys(pairs):
    """object_pairs_hook: a JSON object with a repeated key is an error (Python's json would keep the last)."""
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError("a JSON object has the key %r twice" % (k,))
        d[k] = v
    return d


def box_ends(e):
    """the four interval ends of a box entry [[lo1, hi1], [lo2, hi2]]; any other shape is an error"""
    if type(e) is not list or len(e) != 2 or any(type(iv) is not list or len(iv) != 2 for iv in e):
        raise ValueError("a box entry must be exactly two intervals [lo, hi]")
    return [num(v) for iv in e for v in iv]


def rotation(p):
    """a rotation [g, s] as a pair of rationals; any other shape is an error (g^2 + s^2 = 1 is tested where used)"""
    if type(p) is not list or len(p) != 2:
        raise ValueError("a rotation must be a list of exactly two numbers")
    return (num(p[0]), num(p[1]))


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def label_keys(m):
    return sorted(m.keys(), key=lambda x: (len(x), x))


def region(d):
    """canonical form of a header window or tube:
    {label: ((lo1, hi1), (lo2, hi2), alpha, (g, s))}; centre absent = identity (1, 0)"""
    out = {}
    want = sorted([str(i) for i in LABELS], key=lambda x: (len(x), x))
    if label_keys(d.get("box", {})) != want or label_keys(d.get("alpha", {})) != want:
        raise ValueError("label keys of box or alpha differ from the label set of the statement")
    if set(d.keys()) - {"box", "alpha", "centre"}:
        raise ValueError("window or terminal object of the header has an unknown key: %s" % sorted(d.keys()))
    cen = d.get("centre")
    if cen is not None and label_keys(cen) != want:
        raise ValueError("label keys of a centre map differ from the label set of the statement")
    for i in LABELS:
        b = d["box"][str(i)]
        c = (Fraction(1), Fraction(0)) if cen is None else (fr(cen[str(i)][0]), fr(cen[str(i)][1]))
        if c[0] * c[0] + c[1] * c[1] != 1:
            raise ValueError("centre of label %d is not a rotation" % i)
        out[i] = ((fr(b[0][0]), fr(b[0][1])), (fr(b[1][0]), fr(b[1][1])), fr(d["alpha"][str(i)]), c)
    return out


def expected_region(e):
    """EXPECT.json region: {"core": "p/q", "alpha": {"default": "p/q", "<label>": "p/q", ...},
    "box": {"<label>": {"1": [lo, hi], "2": [lo, hi]}}, "centre": {"<label>": ["g", "s"]}}
    (box entries override the core radius; centre entries override the identity)."""
    if set(e.keys()) - {"core", "alpha", "box", "centre"}:
        raise ValueError("EXPECT region has an unknown key: %s" % sorted(e.keys()))
    for sub in ("box", "centre"):
        bad = [k for k in e.get(sub, {}) if k not in [str(i) for i in LABELS]]
        if bad:
            raise ValueError("EXPECT region: %s has entries for labels outside the label set: %s" % (sub, bad))
    bad = [k for k in e["alpha"] if k != "default" and k not in [str(i) for i in LABELS]]
    if bad:
        raise ValueError("EXPECT region: alpha has entries for labels outside the label set: %s" % bad)
    out = {}
    core = fr(e["core"])
    for i in LABELS:
        iv = [(-core, core), (-core, core)]
        ov = e.get("box", {}).get(str(i), {})
        if set(ov.keys()) - {"1", "2"}:
            raise ValueError("EXPECT region: box entry of label %d has a key other than 1, 2" % i)
        for k in ("1", "2"):
            if k in ov:
                iv[int(k) - 1] = (fr(ov[k][0]), fr(ov[k][1]))
        al = fr(e["alpha"].get(str(i), e["alpha"]["default"]))
        c = e.get("centre", {}).get(str(i))
        c = (Fraction(1), Fraction(0)) if c is None else (fr(c[0]), fr(c[1]))
        if c[0] * c[0] + c[1] * c[1] != 1:
            raise ValueError("EXPECT region: centre of label %d is not a rotation" % i)
        out[i] = (iv[0], iv[1], al, c)
    return out


def main():
    if len(sys.argv) != 8:
        out("usage: h_report30.py CERT C1.json C2.json EXIT_C1 EXIT_C2 EXPECT.json FROZEN.json")
        out("RESULT: NOT ACCEPTED")
        sys.exit(2)
    try:
        _main(*sys.argv[1:8])
    except SystemExit:
        raise
    except Exception as exc:                      # a crash is never an acceptance
        out("FAIL  the report could not be completed: %s: %s" % (type(exc).__name__, exc))
        out("RESULT: NOT ACCEPTED")
        sys.exit(1)


def _main(cert, c1p, c2p, x1, x2, expp, frozenp):
    ok = True

    def check(cond, text):
        nonlocal ok
        out(("ok    " if cond else "FAIL  ") + text)
        if not cond:
            ok = False

    # --- the frozen files
    frozen = json.load(open(frozenp))
    check(set(frozen.keys()) == {"C1", "C2", "SPEC", "frozen_on", "note"} or set(frozen.keys()) == {"C1", "C2", "SPEC", "frozen_on"},
          "FROZEN.json has the entries C1, C2, SPEC, frozen_on (and at most a note)")
    for key, what in (("C1", "Python checker"), ("C2", "Node checker"), ("SPEC", "specification text")):
        ent = frozen[key]
        p = os.path.join(W, ent["file"])
        got = sha_file(p)
        check(got == ent["sha256"], "frozen %s %s has the SHA-256 %s... of FROZEN.json (found %s...)"
              % (what, ent["file"], ent["sha256"][:16], got[:16]))

    sha = sha_file(cert)
    out("certificate %r" % cert)
    out("sha256      %s" % sha)
    is_gz = cert.endswith(".gz")
    opener = gzip.open if is_gz else open
    with opener(cert, "rt", encoding="utf-8") as f:
        header = json.loads(f.readline())
    if is_gz:
        h = hashlib.sha256()
        with gzip.open(cert, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        sha_stream = h.hexdigest()
        out("sha256 of the uncompressed stream %s" % sha_stream)
    else:
        sha_stream = sha
    exp = json.load(open(expp))
    c1 = json.load(open(c1p))
    c2 = json.load(open(c2p))
    known = {"name", "schema", "labels", "S_floor", "tube_name", "terminal_leaves", "terminal_leaves_note",
             "window", "tube", "packing_sha256", "root_region"}
    check(set(exp.keys()) <= known, "EXPECT.json has only known entries (unknown: %s)"
          % sorted(set(exp.keys()) - known))

    # --- schema, label set and side floor, from the STATEMENT (EXPECT.json)
    global LABELS
    schema = exp.get("schema", "wx-cert-2")
    assert schema in ("wx-cert-2", "wx-cert-3"), "EXPECT schema must be wx-cert-2 or wx-cert-3"
    nlab = exp.get("labels", 16)
    assert nlab in (16, 17), "EXPECT labels must be 16 or 17"
    if nlab == 17:
        LABELS = list(range(1, 18))
    floor = fr(exp.get("S_floor", "4"))
    out("statement: schema %s, %d labels, S_floor = %s" % (schema, nlab, floor))
    check(header.get("schema") == schema, "header schema %r, expected %r" % (header.get("schema"), schema))
    # Under "wx-cert-2" the Python checker writes a report with exactly the keys of its 2.6 version (no `schema`,
    # no `window_centres`, no `tube_centres`: reviews/REVIEW_30_PY.md P6); under "wx-cert-3" it writes them. So an
    # absent key is accepted from C1 only for a wx-cert-2 statement; the Node checker writes them always.
    c1_schema = c1.get("schema", "wx-cert-2" if schema == "wx-cert-2" else None)
    check(c1_schema == schema and c2.get("schema") == schema,
          "both reports: schema checked under = %r (C1 %r%s, C2 %r)"
          % (schema, c1.get("schema"), " = key absent, as in every wx-cert-2 report of C1" if "schema" not in c1 else "",
             c2.get("schema")))
    check(header.get("labels", 16) == nlab and type(header.get("labels", 16)) is int,
          "header label set: %r (absent = 16), expected %d" % (header.get("labels"), nlab))
    check(fr(header.get("S_floor", "4")) == floor, "header S_floor: %r (absent = 4), expected %s"
          % (header.get("S_floor"), floor))
    check(set(header.keys()) <= {"schema", "packing_sha256", "Sref", "root", "window", "terminal", "labels", "S_floor"},
          "header has no field outside SPEC 3.0 section 10")
    check(c1.get("labels") == nlab and c2.get("labels") == nlab,
          "both reports: label set used = %d (C1 %r, C2 %r)" % (nlab, c1.get("labels"), c2.get("labels")))
    f1, f2 = c1.get("S_floor"), c2.get("S_floor")
    check(isinstance(f1, str) and isinstance(f2, str) and fr(f1) == floor and fr(f2) == floor,
          "both reports: S_floor used = %s (C1 %r, C2 %r)" % (floor, f1, f2))

    check(int(x1) == 0, "C1 exit code %s" % x1)
    check(int(x2) == 0, "C2 exit code %s" % x2)
    check(c1.get("verdict") == "PASS" and c1.get("mode") == "full", "C1 report: verdict %r, mode %r"
          % (c1.get("verdict"), c1.get("mode")))
    check(c2.get("result") == "PASS" and c2.get("mode") == "certificate", "C2 report: result %r, mode %r"
          % (c2.get("result"), c2.get("mode")))
    check(c1.get("certificate_sha256") == sha and (not is_gz or c1.get("certificate_uncompressed_sha256") == sha_stream),
          "C1 checked this file (hash of the file%s)" % (" and of the uncompressed stream" if is_gz else ""))
    check(c2.get("certificate_sha256") == sha_stream,
          "C2 checked this file (hash of the %s)" % ("uncompressed stream" if is_gz else "file"))
    pin = exp.get("packing_sha256", PIN)
    check(c1.get("packing_sha256") == pin and c2.get("packing_sha256") == pin and header.get("packing_sha256") == pin,
          "reference file hash %s in the header and in both reports" % pin[:12])
    out("C1: %s; C2: %s %s" % (c1.get("checker"), c2.get("checker"), c2.get("spec")))
    # the specification each program says it implements: the frozen text (review REVIEW_30_PY.md, S5)
    spec_sha = frozen["SPEC"]["sha256"]
    check(c1.get("spec_sha256") == spec_sha, "C1 report names the frozen text by its hash (spec_sha256 %s...)"
          % str(c1.get("spec_sha256"))[:16])
    check(c2.get("spec_sha256") in (None, spec_sha) and "3.0" in str(c2.get("spec")),
          "C2 report names version 3.0 (spec %r; spec_sha256 %s)" % (c2.get("spec"), str(c2.get("spec_sha256"))[:16]))

    # --- nodes
    n1 = {n["id"]: n for n in c1["nodes"]}
    n2 = {n["id"]: n for n in c2["nodes"]}
    check(len(n1) == len(c1["nodes"]) and len(n2) == len(c2["nodes"]), "node ids unique in both reports")
    check(set(n1) == set(n2), "same node ids in both reports (%d, %d)" % (len(n1), len(n2)))
    check(all(n["accepted"] is True for n in c1["nodes"]) and all(n["accepted"] is True for n in c2["nodes"]),
          "every node accepted by both")
    check(all("close" in n for n in c1["nodes"]) and all("close" in n for n in c2["nodes"]),
          "every node entry of both reports has a closure kind (a rejected node has none)")
    diff = [i for i in n1 if i in n2 and n1[i].get("close") != n2[i].get("close")]
    check(not diff, "same closure kind per node in both reports (differences: %d)" % len(diff))
    kinds = {}
    for n in c1["nodes"]:
        kinds[n.get("close")] = kinds.get(n.get("close"), 0) + 1
    out("nodes %d: %s" % (len(n1), ", ".join("%s %d" % (str(k), v) for k, v in sorted(kinds.items(), key=lambda kv: str(kv[0])))))
    ev1 = {}
    for n in c1["nodes"]:
        if n.get("close") == "infeasible":
            ev1[str(n.get("evidence"))] = ev1.get(str(n.get("evidence")), 0) + 1
    out("C1 evidence of the infeasible leaves: %s" % ", ".join("%s %d" % kv for kv in sorted(ev1.items())))
    ev2 = {}
    for n in c2["nodes"]:
        if n.get("close") == "infeasible":
            e = str(n.get("evidence"))
            key = "0-step" if "`0` step" in e else ("EMPTY" if "EMPTY" in e or "empty" in e else ("pair" if "pair" in e or "option" in e else e[:40]))
            ev2[key] = ev2.get(key, 0) + 1
    out("C2 evidence of the infeasible leaves: %s" % ", ".join("%s %d" % kv for kv in sorted(ev2.items())))

    # --- the exact value L of the closing `0` steps: the same rational number in both reports
    both = only1 = only2 = 0
    unequal = []
    smallest = None
    for i in sorted(n1):
        if i not in n2 or n1[i].get("close") != "infeasible":
            continue
        l1, l2 = n1[i].get("zero_step_L"), n2[i].get("zero_step_L")
        if l1 is None and l2 is None:
            continue
        if l1 is None or l2 is None:
            only1 += l2 is None
            only2 += l1 is None
            continue
        both += 1
        v1, v2 = fr(l1), fr(l2)
        if v1 != v2:
            unequal.append(i)
        if smallest is None or v1 < smallest[0]:
            smallest = (v1, i)
    n0 = ev1.get("0-step", 0)
    check(only1 == 0 and only2 == 0, "no leaf has zero_step_L in only one report (only C1: %d, only C2: %d)" % (only1, only2))
    check(not unequal, "zero_step_L is the same rational number in both reports for all %d leaves that have it (different: %s)"
          % (both, unequal[:6]))
    check(both == n0 and ev2.get("0-step", 0) == n0,
          "every leaf closed by a `0` step has zero_step_L in both reports (%d leaves by C1's evidence, %d by C2's, %d with both values)"
          % (n0, ev2.get("0-step", 0), both))
    if smallest is not None:
        check(smallest[0] > 0, "every zero_step_L is positive")
        out("      smallest zero_step_L: %.6e at node %r" % (float(smallest[0]), smallest[1]))

    term = sorted(i for i in n1 if n1[i].get("close") == "terminal")
    out("terminal leaves: %r" % (term if len(term) <= 12 else "%d leaves" % len(term)))
    if exp["terminal_leaves"] is None:
        out("      number of terminal leaves: %d (not fixed by the statement)" % len(term))
    else:
        check(len(term) == exp["terminal_leaves"], "number of terminal leaves is %d (expected %d)"
              % (len(term), exp["terminal_leaves"]))
    for c, name in ((c1, "C1"), (c2, "C2")):
        cc = c["counts"]
        check(cc["nodes"] == len(n1) and cc["infeasible"] == kinds.get("infeasible", 0)
              and cc["terminal"] == kinds.get("terminal", 0) and cc["split"] == kinds.get("split", 0),
              "%s counts agree with its node list" % name)
    check(c1["counts"]["steps"] == c2["counts"]["steps"] and c1["counts"]["terms"] == c2["counts"]["terms"],
          "same number of steps and terms evaluated (%d, %d)" % (c1["counts"]["steps"], c1["counts"]["terms"]))
    r1, r2 = c1["counts"].get("rounds_evaluated"), c2["counts"].get("roundsEvaluated")
    check(r1 is not None and r2 is not None and r1 == r2,
          "same number of rounds evaluated (C1 %r, C2 %r)" % (r1, r2))

    # --- header = statement
    check(fr(header["Sref"]) == Fraction(4675530093604551, 10 ** 15), "Sref = 4675530093604551/10^15")
    check(header.get("root") == c1.get("root"), "root id %r (header against the Python report; the Node report has no root key)" % header.get("root"))
    w, t = region(header["window"]), region(header["terminal"])
    wc, tc = "centre" in header["window"], "centre" in header["terminal"]
    check(schema == "wx-cert-3" or not (wc or tc), "centre maps occur only under wx-cert-3 (header: window %r, tube %r)" % (wc, tc))
    c1_wc = c1.get("window_centres", False if schema == "wx-cert-2" else None)
    c1_tc = c1.get("tube_centres", False if schema == "wx-cert-2" else None)
    check(c1_wc is wc and c2.get("window_centres") is wc
          and c1_tc is tc and c2.get("tube_centres") is tc,
          "both reports: centre maps present in the header: window %r, tube %r (C1 %r %r, C2 %r %r)"
          % (wc, tc, c1.get("window_centres"), c1.get("tube_centres"), c2.get("window_centres"), c2.get("tube_centres")))
    we = expected_region(exp["window"])
    if exp["tube"] == "disjoint":
        sep = [(i, k + 1) for i in LABELS for k in (0, 1) if t[i][k][0] > w[i][k][1] or t[i][k][1] < w[i][k][0]]
        check(bool(sep), "header tube is disjoint from the window (coordinates with disjoint intervals: %s)" % sep[:4])
        te = t
    else:
        te = expected_region(exp["tube"])
    check(w == we, "header window = expected window %r (boxes, angle radii and centres)" % exp.get("name"))
    if w != we:
        for i in LABELS:
            if w[i] != we[i]:
                out("      label %d: header %s expected %s" % (i, w[i], we[i]))
    check(t == te, "header tube = expected tube %r (boxes, angle radii and centres)" % exp.get("tube_name"))
    if t != te:
        for i in LABELS:
            if t[i] != te[i]:
                out("      label %d: header %s expected %s" % (i, t[i], te[i]))
    nc_w = [i for i in LABELS if w[i][3] != (1, 0)]
    nc_t = [i for i in LABELS if t[i][3] != (1, 0)]
    out("labels with a centre other than the identity: window %s, tube %s" % (nc_w, nc_t))

    # --- ROOT REGION (optional; EXPECT.json "root_region": {"file": path relative to the session folder,
    # "sha256": ...}). A statement may be made for the region of the ROOT NODE instead of the header window
    # (SPEC 3.0 section 7: the proof shows that every feasible configuration of F(root) lies in the tube). Then
    # the root node of the certificate must BE the stated region: its box, every arc (centre and both end
    # rotations), its side interval, an empty assumption list and parent null are compared exactly with the
    # region file (keys "window"."box", "root_arc", "S"). The root node is read from the certificate by this
    # script (the line whose id is the header's root); both checkers have checked the same bytes (hashes above)
    # and take the root from the same header field.
    rr = exp.get("root_region")
    if "root_region" not in exp:
        out("root region: not part of this statement (the statement is the header window)")
    else:
        check(isinstance(rr, dict) and set(rr.keys()) == {"file", "sha256"}, "EXPECT root_region has exactly the keys file, sha256")
        rpath = os.path.join(W, rr["file"])
        got = sha_file(rpath)
        check(got == rr["sha256"], "root region file %r has the stated SHA-256 %s... (found %s...)"
              % (rr["file"], str(rr["sha256"])[:16], got[:16]))
        reg = json.load(open(rpath), object_pairs_hook=no_duplicate_keys)
        rootid = header.get("root")
        rootnode = None
        nfound = 0
        # newline="\n": a line ends at a line feed only, as for both checkers (a carriage return is JSON white space)
        with opener(cert, "rt", encoding="utf-8", newline="\n") as f:
            f.readline()
            for line in f:
                if not line.strip():
                    continue
                # every node line is parsed in full (no shortcut: a filter on the raw text could miss a node)
                node = json.loads(line)
                if node.get("id") == rootid:
                    nfound += 1
                    rootnode = json.loads(line, object_pairs_hook=no_duplicate_keys)
        check(nfound == 1 and isinstance(rootid, str), "the certificate has exactly one node with the header's root id %r (found %d)" % (rootid, nfound))
        if rootnode is not None:
            want = sorted([str(i) for i in LABELS], key=lambda x: (len(x), x))
            check(rootnode.get("parent") is None, "root node: parent is null")
            check(rootnode.get("assume") == [], "root node: empty assumption list")
            check(label_keys(rootnode.get("box", {})) == want and label_keys(rootnode.get("arc", {})) == want
                  and label_keys(reg["window"]["box"]) == want and label_keys(reg["root_arc"]) == want,
                  "root node and region file have exactly the labels of the statement")
            rs, gs = rootnode.get("S"), reg.get("S")
            check(type(rs) is list and type(gs) is list and len(rs) == 2 and len(gs) == 2
                  and num(rs[0]) == num(gs[0]) and num(rs[1]) == num(gs[1]),
                  "root node: side interval %r = the region's %r" % (rs, gs))
            badbox = [i for i in LABELS if box_ends(rootnode["box"][str(i)]) != box_ends(reg["window"]["box"][str(i)])]
            check(not badbox, "root node: box = the region's box, all %d interval ends (labels that differ: %s)"
                  % (4 * len(LABELS), sorted(set(badbox))))
            badarc = []
            for i in LABELS:
                a, b = rootnode["arc"][str(i)], reg["root_arc"][str(i)]
                if type(a) is not dict or type(b) is not dict or set(a.keys()) != {"c", "lo", "hi"} or set(b.keys()) != {"c", "lo", "hi"}:
                    badarc.append(i)
                    continue
                for key in ("c", "lo", "hi"):
                    pa, pb = rotation(a[key]), rotation(b[key])
                    if pa != pb or pa[0] ** 2 + pa[1] ** 2 != 1:
                        badarc.append(i)
            check(not badarc, "root node: every arc (centre and both end rotations) = the region's root arc (labels that differ: %s)"
                  % sorted(set(badarc)))
            out("      the statement of this record is made for the ROOT REGION of %r (its entries S, window.box and root_arc)" % rr["file"])
    out("RESULT: %s" % ("ACCEPTED" if ok else "NOT ACCEPTED"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
