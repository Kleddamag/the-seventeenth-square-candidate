#!/usr/bin/env python3
# Re-run of the two frozen 3.0 checkers on thirteen accepted trees. Reads the project, writes only into its own folder.
import hashlib, json, os, re, subprocess, sys, time
R = "/Users/builder/Developer/07-math-research/17-squares-certified-bound"
W = R + "/research/window-extension-20261008"
A = R + "/local-research/claude-20261002/results/assembly"
M = os.path.dirname(os.path.abspath(__file__))
PY = R + "/local-research/claude-20261002/.venv/bin/python"
C1 = W + "/checker/wxcheck_v30.py"; C2 = W + "/checker2/wxcheck2_v30.js"
HREP = W + "/acceptance/h_report30.py"; FROZEN = W + "/acceptance/FROZEN_30.json"
PIN = {C1: "cf8db52bfa1cc565d8610bf13b279d1b5da2f84c91ce2854d15a3b0a88cd096c",
       C2: "97210adf74a3ebed7cde021a3cb1ff6ea6380d8d2d55540a2a2a1cb17dc27542",
       HREP: "0314aa1f8f742cd7156cc490764c8a308663ba87f359e0d8b97fb3d7189950db",
       FROZEN: "6d65a0705c039bbf2f48acabb7f12275871af6b7b8fa308c0671ea6518b30803"}
def asm(n): return "%s/%s/%s.cert.jsonl.gz" % (A, n, n)
# name, record name, certificate (pinned path), EXPECT file
CERTS = [
 ("JQ", "JQ_v1_jQTwn0", R + "/local-research/claude-20261002/cloud/analysis/part3_exact/certs/JQ_v1/jQTw.n0.JQ.cert.jsonl.gz", "bigbox/join/EXPECT_JQ_v1.json"),
 ("JPG15p_v5", "JPG15p_v5", asm("JPG15p_v5"), "bigbox/join/EXPECT_JPG15p_v5.json"),
 ("JPG17m_v5", "JPG17m_v5", asm("JPG17m_v5"), "bigbox/join/EXPECT_JPG17m_v5.json"),
 ("JPG3m_v5", "JPG3m_v5", asm("JPG3m_v5"), "bigbox/join/EXPECT_JPG3m_v5.json"),
 ("JPG3p_v5", "JPG3p_v5", asm("JPG3p_v5"), "bigbox/join/EXPECT_JPG3p_v5.json"),
 ("JPG17p_v5", "JPG17p_v5", asm("JPG17p_v5"), "bigbox/join/EXPECT_JPG17p_v5.json"),
 ("JPG15m_v5", "JPG15m_v5", asm("JPG15m_v5"), "bigbox/join/EXPECT_JPG15m_v5.json"),
 ("G20S", "G20S_v30", W + "/bigbox/gen17/G20S_tree.jsonl.gz", "acceptance/EXPECT_G20S.json"),
 ("HW", "HW_v30", W + "/bigbox/gen17/HW_tree.jsonl.gz", "acceptance/EXPECT_HW.json"),
 ("JG", "JG_v2", asm("JG"), "bigbox/join/EXPECT_JG_v2.json"),
 ("JPWS_v4", "JPWS_v4", asm("JPWS_v4"), "bigbox/join/EXPECT_JPWS_v4.json"),
 ("JPW13", "JPW13_v2x", asm("JPW13"), "bigbox/join/EXPECT_JPW13_v2x.json"),
 ("JPA_v5", "JPA_v5", asm("JPA_v5"), "bigbox/join/EXPECT_JPA_v5.json"),
]
BY = {c[0]: c for c in CERTS}
SMALL = [c[0] for c in CERTS[:7]]
QUEUE = [(n, k) for n in SMALL for k in ("C1", "C2")]
# second part: the one long job (JPA_v5 C1, 2.3 h of record) first, the rest in the given order, JPA_v5 C2 last
QUEUE += [("JPA_v5", "C1")] + [(n, k) for n in ("G20S", "HW", "JG", "JPWS_v4", "JPW13") for k in ("C1", "C2")] + [("JPA_v5", "C2")]
SLOTS = 3
TIMELINE = re.compile(r"^\s+[\d.]+ real\s|^\s+\d+\s+(maximum resident|average |page |block |messages |signals |voluntary|involuntary|instructions|cycles|peak memory|swaps)")
def log(s):
    with open(M + "/driver.log", "a") as f: f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + s + "\n")
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""): h.update(b)
    return h.hexdigest()
def flag(name, text=""):
    with open(M + "/" + name, "a") as f: f.write(text + "\n")
def norm(lines):
    out = []
    for l in lines:
        l = l.rstrip("\n")
        if TIMELINE.search(l) or l.startswith("  time:"): continue
        l = re.sub(r"; [\d.]+ s$", "", l)
        if l.startswith("  certificate:"): l = "  certificate: " + l[l.find("(SHA-256"):]
        out.append(l)
    return out
def record(rec):
    """lines of record for C1 and C2 from ACCEPT_<rec>.log, and the certificate hash of record"""
    sec = {"C1": [], "C2": []}; cur = None; csha = None
    for l in open(W + "/acceptance/ACCEPT_%s.log" % rec, errors="replace"):
        if l.startswith("sha256 certificate:"): csha = l.split()[2]
        if l.startswith("--- C1"): cur = "C1"; continue
        if l.startswith("--- C2"): cur = "C2"; continue
        if l.startswith("exit code C") or l.startswith("--- report"): cur = None
        if cur: sec[cur].append(l)
    return {k: norm(v) for k, v in sec.items()}, csha
def counts(lines, kind):
    for l in lines:
        if kind == "C1" and l.startswith("nodes="):
            d = dict(x.split("=") for x in l.split())
            return "/".join(d[k] for k in ("nodes", "infeasible", "terminal", "split", "steps", "terms"))
        if kind == "C2" and l.startswith("  nodes "):
            m = re.search(r"nodes (\d+) \(infeasible (\d+), terminal (\d+), split (\d+)\).*steps (\d+), terms (\d+)", l)
            return "/".join(m.groups())
    return "?"
def jsondiff(a, b):
    try:
        x = json.load(open(a)); y = json.load(open(b))
        if isinstance(x, dict) and isinstance(y, dict):
            return ",".join(sorted(k for k in set(x) | set(y) if x.get(k, "<absent>") != y.get(k, "<absent>"))) or "none"
        return "none" if x == y else "whole"
    except Exception as e:
        return "error:%s" % e
def start(n, k):
    cert = BY[n][2]; out = open("%s/%s_%s.out" % (M, n, k), "w"); j = "%s/%s_%s.json" % (M, n, k)
    env = dict(os.environ)
    if k == "C1":
        env["VECLIB_MAXIMUM_THREADS"] = "1"; env["OMP_NUM_THREADS"] = "1"
        cmd = ["/usr/bin/time", "-l", PY, "-I", "-B", os.path.basename(C1), cert, "--json", j]; cwd = os.path.dirname(C1)
    else:
        env.pop("NODE_OPTIONS", None)
        cmd = ["/usr/bin/time", "-l", "node", "--max-old-space-size=12000", os.path.basename(C2), cert, "--json", j]; cwd = os.path.dirname(C2)
    p = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    log("START %s %s pid %d: %s" % (n, k, p.pid, " ".join(cmd)))
    return {"n": n, "k": k, "p": p, "t0": time.time(), "out": out}
def finish(job, shaok, rc_of):
    n, k = job["n"], job["k"]; rc = job["p"].returncode; job["out"].close(); wall = time.time() - job["t0"]
    lines = open("%s/%s_%s.out" % (M, n, k), errors="replace").read().split("\n")
    first = lines[0] if lines else ""
    rss = "?"
    for l in lines:
        if "maximum resident set size" in l: rss = "%.0f MB" % (int(l.split()[0]) / 1e6)
    new = norm(lines); rec, _ = record(BY[n][1]); rec = rec[k]
    while new and new[-1] == "": new.pop()
    same = (new[:len(rec)] == rec) and len(rec) >= 3
    cn, cr = counts(new, k), counts(rec, k)
    jd = jsondiff("%s/%s_%s.json" % (M, n, k), "%s/acceptance/%s_%s.json" % (W, BY[n][1], k))
    ok = (rc == 0 and first == "PASS" and same and cn == cr and cn != "?")
    row = [n, k, "yes" if shaok[n] else "no", str(rc), first[:40], cn, cr, "EQUAL" if (same and cn == cr) else "DIFFERENT", "%.0f s" % wall, rss, jd]
    with open(M + "/results.tsv", "a") as f: f.write("\t".join(row) + "\n")
    log("END   %s %s exit %d first [%s] wall %.0f s peak %s now %s record %s %s json-keys-differing: %s" % (n, k, rc, first[:40], wall, rss, cn, cr, row[7], jd))
    rc_of[(n, k)] = rc
    if not ok:
        d = [(a, b) for a, b in zip(new, rec) if a != b]
        flag("FAIL", "%s %s: exit %d, first line [%s], counts now %s record %s, output lines differing from the record: %r" % (n, k, rc, first, cn, cr, d[:4]))
    return ok
def main():
    for p, h in PIN.items():
        if sha(p) != h: flag("FAIL", "frozen file %s does not have the pinned hash" % p); log("pinned hash wrong: " + p); return
    log("frozen files have the pinned hashes; queue of %d jobs, %d slots" % (len(QUEUE), SLOTS))
    q = list(QUEUE); run = []; reps = []; shaok = {}; rc_of = {}; repdone = set(); stop = False; peak = 0; tick = 0
    while q or run or reps:
        for job in list(run):
            if job["p"].poll() is not None:
                run.remove(job)
                if not finish(job, shaok, rc_of): stop = True
                n = job["n"]
                if not stop and (n, "C1") in rc_of and (n, "C2") in rc_of and n not in repdone:
                    repdone.add(n); o = open("%s/%s_report.out" % (M, n), "w")
                    cmd = [PY, "-I", "-B", HREP, BY[n][2], "%s/%s_C1.json" % (M, n), "%s/%s_C2.json" % (M, n), str(rc_of[(n, "C1")]), str(rc_of[(n, "C2")]), W + "/" + BY[n][3], FROZEN]
                    reps.append({"n": n, "p": subprocess.Popen(cmd, cwd=M, stdout=o, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL), "out": o})
                    log("REPORT start %s" % n)
        for r in list(reps):
            if r["p"].poll() is not None:
                reps.remove(r); r["out"].close(); n = r["n"]
                ls = [l for l in open("%s/%s_report.out" % (M, n), errors="replace").read().split("\n") if l]
                last = ls[-1] if ls else ""; nok = sum(1 for l in ls if l.startswith("ok ")); bad = [l for l in ls if not re.match(r"^(ok |certificate |sha256|statement|C1|C2|nodes |terminal leaves|labels with| {6}|RESULT)", l)]
                with open(M + "/reports.tsv", "a") as f: f.write("\t".join([n, str(r["p"].returncode), last, "%d ok lines" % nok, "other lines: %r" % bad[:3]]) + "\n")
                log("REPORT end %s exit %d last line [%s] ok lines %d" % (n, r["p"].returncode, last, nok))
                if r["p"].returncode != 0 or last != "RESULT: ACCEPTED":
                    stop = True; flag("FAIL", "%s report: exit %d, last line [%s]" % (n, r["p"].returncode, last))
                if all(os.path.exists("%s/%s_report.out" % (M, s)) for s in SMALL) and not any(x["n"] in SMALL for x in reps) and all(s in repdone for s in SMALL) and not os.path.exists(M + "/SMALL_DONE") and not stop:
                    flag("SMALL_DONE"); log("the seven small trees are done")
        while q and not stop and len(run) < SLOTS:
            n, k = q.pop(0)
            if n not in shaok:
                _, want = record(BY[n][1]); got = sha(BY[n][2]); shaok[n] = (got == want)
                log("SHA   %s %s record %s %s" % (n, got, want, "equal" if shaok[n] else "DIFFERENT"))
                if not shaok[n]:
                    stop = True; flag("FAIL", "%s: certificate sha256 %s, record %s" % (n, got, want)); break
            run.append(start(n, k))
        if stop and q:
            log("stopped: %d jobs not started: %s" % (len(q), q)); flag("NOT_STARTED", repr(q)); q = []
        tick += 1
        if tick % 6 == 0 and run:
            try:
                ps = subprocess.run(["ps", "-Ao", "ppid=,rss="], capture_output=True, text=True).stdout.split("\n")
                mine = {str(j["p"].pid) for j in run}; tot = sum(int(l.split()[1]) for l in ps if l.split() and l.split()[0] in mine) / 1e6
                if tot > peak: peak = tot; log("resident memory of the running checkers, new maximum: %.1f GB (%s)" % (tot, ", ".join(j["n"] + " " + j["k"] for j in run)))
                if tot > 28 and not stop: stop = True; flag("FAIL", "resident memory %.1f GB above the limit; no new jobs started" % tot)
            except Exception as e: log("memory sample failed: %s" % e)
        time.sleep(5)
    log("queue finished; stop flag %s" % stop); flag("DONE")
main()
