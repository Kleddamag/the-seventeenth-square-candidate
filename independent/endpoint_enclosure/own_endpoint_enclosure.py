#!/usr/bin/env python3
"""Independent exact enclosure of the endpoint root (t*, b*) and of the side L.

Written from scratch by the checker.  Standard library only, Fractions only,
no floats in anything that decides.  Shares no code with
check_endpoint_enclosure.py or check_endpoint.py.

Definitions (F, G, t0, b0, formula for L, claimed decimal bounds) are PARSED
from STATEMENT.md.  Other files are read as DATA for the comparisons only.

Method (component-wise Krawczyk test with exact Taylor bounds):
  * P(m+h) is expanded exactly about a rational centre m (Taylor shift).
    For |h1|,|h2| <= r every entry of the Jacobian J(m+h) differs from J(m)
    by at most  D = sum over the remaining Taylor terms of |coeff| r^deg,
    a proved bound for the WHOLE box (every monomial, absolute values).
  * Y is a rational approximate inverse of J(m), det Y != 0 checked.
    T(x) = x - Y (F,G)(x).  For x, y in the box X (convex)
        T(x) - T(y) = [ integral_0^1 (I - Y J(y+s(x-y))) ds ] (x - y),
    and entrywise |I - Y J(z)| <= |I - Y J(m)| + |Y| D =: Q for all z in X.
  * Test: |Y (F,G)(m)|_i + (Q (r,r))_i < r for i = 1,2.  Then T maps X into
    its interior, the row sums of Q are < 1, T is a sup-norm contraction of
    X, so T has exactly one fixed point in X, and (Y nonsingular) that is
    exactly one common zero of F, G in X.
  * Stage 1: X = statement box, radius 10^-12 about (t0,b0)  -> uniqueness.
    Stage 2: X* = radius 10^-100 about my own Newton centre m*, X* inside X
             -> the unique zero lies in X*.
  * L by outward interval arithmetic on (6+4t)/(1+2t-t^2); no monotonicity.

Usage: own_endpoint_enclosure.py            (the real statement)
       own_endpoint_enclosure.py --control  (F with one coefficient changed by 1)
"""
import hashlib
import json
import re
import sys
from fractions import Fraction as Fr
from math import comb
from pathlib import Path

if not __debug__:
    raise RuntimeError("run without -O")

REPO = Path(__file__).resolve().parents[2]      # the root of the edition, found from this file's own location
STATEMENT = REPO / "STATEMENT.md"
PACKET = REPO / ("research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/"
                 "../second-order-20261010/theorem/EXACT_ENDPOINT_AND_CASES.json")
GATE = REPO / ("research/finishing-threshold-goal-20261007/current-author-20261012t/claude-extension-audit/"
               "terminal-producer/gate-receipt.json")
OLD = REPO / ("research/global-compensation-20261007/reviews/fresh-structure/"
              "endpoint-feasibility/endpoint-receipt.json")
AUTHOR = REPO / ("research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/"
                 "public-edition-round2-20261011/ENDPOINT_ENCLOSURE_CHECK.json")
UPSTREAM = REPO / "research/uniform-capture-20261007/upstream-root-certificate.json"
REFERENCE = REPO / "upper-packing-certificate.json"

CONTROL = "--control" in sys.argv
FAILS = []


def check(name, ok, detail=""):
    print(("  [ok]   " if ok else "  [FAIL] ") + name + (("  " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)
    return ok


# ---------------------------------------------------------------- polynomials
def padd(p, q, s=1):
    r = dict(p)
    for k, v in q.items():
        r[k] = r.get(k, 0) + s * v
        if r[k] == 0:
            del r[k]
    return r


def pmul(p, q):
    r = {}
    for (a, b), u in p.items():
        for (c, d), v in q.items():
            k = (a + c, b + d)
            r[k] = r.get(k, 0) + u * v
    return {k: v for k, v in r.items() if v != 0}


def ppow(p, n):
    r = {(0, 0): 1}
    for _ in range(n):
        r = pmul(r, p)
    return r


def parse_poly(text):
    """Recursive descent: expr = ['-'] term (('+'|'-') term)*,
    term = factor factor* (juxtaposition), factor = atom ['^' int],
    atom = int | t | b | '(' expr ')'."""
    toks = re.findall(r"\d+|[tb()+\-^]", text)
    assert "".join(toks) == text, ("unparsed characters", text)
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def take():
        pos[0] += 1
        return toks[pos[0] - 1]

    def atom():
        tk = take()
        if tk == "(":
            v = expr()
            assert take() == ")"
            return v
        if tk == "t":
            return {(1, 0): 1}
        if tk == "b":
            return {(0, 1): 1}
        assert tk.isdigit(), tk
        return {(0, 0): int(tk)}

    def factor():
        v = atom()
        if peek() == "^":
            take()
            v = ppow(v, int(take()))
        return v

    def term():
        v = factor()
        while peek() is not None and peek() not in "+-)":
            v = pmul(v, factor())
        return v

    def expr():
        sign = 1
        if peek() == "-":
            take()
            sign = -1
        v = padd({}, term(), sign)
        while peek() in ("+", "-"):
            s = 1 if take() == "+" else -1
            v = padd(v, term(), s)
        return v

    v = expr()
    assert pos[0] == len(toks)
    return v


def shift(p, m):
    """Exact Taylor coefficients of p about m: p(m+h) = sum a[k,l] h1^k h2^l."""
    a = {}
    for (i, j), c in p.items():
        for k in range(i + 1):
            for l in range(j + 1):
                a[(k, l)] = a.get((k, l), Fr(0)) + c * comb(i, k) * comb(j, l) * m[0] ** (i - k) * m[1] ** (j - l)
    return a


def value(p, x):
    return sum((c * x[0] ** i * x[1] ** j for (i, j), c in p.items()), Fr(0))


def rnd(q, digits):
    d = 10 ** digits
    return Fr((2 * q.numerator * d + q.denominator) // (2 * q.denominator), d)


def dec(q, digits):
    """Truncated decimal string of a positive rational (exact integer arithmetic)."""
    assert q > 0
    n = q.numerator * 10 ** digits // q.denominator
    s = str(n).rjust(digits + 1, "0")
    return s[:-digits] + "." + s[-digits:]


def sci(q):
    """Readable magnitude of a rational, exact truncation, for the printout only."""
    if q == 0:
        return "0"
    s = "-" if q < 0 else ""
    q = abs(q)
    e = 0
    while q >= 10:
        q /= 10
        e += 1
    while q < 1:
        q *= 10
        e -= 1
    return "%s%se%d" % (s, dec(q, 6), e)


# ------------------------------------------------------------ Krawczyk test
def krawczyk(polys, m, r, ydigits=40):
    """Returns dict with ok flag and the proved quantities for the box m +/- r."""
    a = [shift(p, m) for p in polys]
    f = [ap.get((0, 0), Fr(0)) for ap in a]
    J = [[ap.get((1, 0), Fr(0)), ap.get((0, 1), Fr(0))] for ap in a]
    assert f == [value(p, m) for p in polys]            # shift agrees with direct evaluation
    # The shift is a polynomial identity of degree <= 5 in h1 and <= 4 in h2; equality on a
    # 6 x 5 grid of points therefore PROVES it (tensor-product interpolation is unique).
    for p, ap in zip(polys, a):
        assert max(i for i, _ in p) <= 5 and max(j for _, j in p) <= 4
        for u in range(6):
            for v in range(5):
                h = (Fr(u, 7), Fr(v, 7))
                assert value(p, (m[0] + h[0], m[1] + h[1])) == value(ap, h)
    # deviation of each Jacobian entry over the whole box
    D = [[Fr(0), Fr(0)], [Fr(0), Fr(0)]]
    for p_i, ap in enumerate(a):
        for (k, l), c in ap.items():
            if k >= 1 and (k, l) != (1, 0):
                D[p_i][0] += k * abs(c) * r ** (k - 1 + l)
            if l >= 1 and (k, l) != (0, 1):
                D[p_i][1] += l * abs(c) * r ** (k + l - 1)
    det = J[0][0] * J[1][1] - J[0][1] * J[1][0]
    if det == 0:
        return {"ok": False, "why": "singular midpoint Jacobian"}
    Y = [[rnd(J[1][1] / det, ydigits), rnd(-J[0][1] / det, ydigits)],
         [rnd(-J[1][0] / det, ydigits), rnd(J[0][0] / det, ydigits)]]
    detY = Y[0][0] * Y[1][1] - Y[0][1] * Y[1][0]
    Q = [[abs((1 if i == j else 0) - sum(Y[i][k] * J[k][j] for k in (0, 1)))
          + sum(abs(Y[i][k]) * D[k][j] for k in (0, 1)) for j in (0, 1)] for i in (0, 1)]
    q = max(Q[i][0] + Q[i][1] for i in (0, 1))
    disp = [abs(sum(Y[i][k] * f[k] for k in (0, 1))) for i in (0, 1)]
    eta = max(disp)
    inside = [disp[i] + (Q[i][0] + Q[i][1]) * r < r for i in (0, 1)]
    ok = detY != 0 and q < 1 and all(inside)
    out = {"ok": ok, "detY_nonzero": detY != 0, "q": q, "eta": eta, "disp": disp,
           "f": f, "J": J, "det": det, "D": D, "Y": Y, "r": r, "m": m}
    if ok:
        out["banach_radius"] = eta / (1 - q)            # |zero - m|_inf <= eta/(1-q)
        out["K_radius"] = [disp[i] + (Q[i][0] + Q[i][1]) * r for i in (0, 1)]
    return out


def newton(polys, x, steps=14, digits=110):
    for _ in range(steps):
        a = [shift(p, x) for p in polys]
        f = [ap.get((0, 0), Fr(0)) for ap in a]
        J = [[ap.get((1, 0), Fr(0)), ap.get((0, 1), Fr(0))] for ap in a]
        det = J[0][0] * J[1][1] - J[0][1] * J[1][0]
        dx = ((J[1][1] * f[0] - J[0][1] * f[1]) / det, (-J[1][0] * f[0] + J[0][0] * f[1]) / det)
        x = (rnd(x[0] - dx[0], digits), rnd(x[1] - dx[1], digits))
    return x


def side_interval(tlo, thi):
    """Outward interval arithmetic for (6+4t)/(1+2t-t^2) on 0 < tlo <= t <= thi."""
    assert 0 < tlo <= thi
    nlo, nhi = 6 + 4 * tlo, 6 + 4 * thi                 # increasing, exact range
    dlo, dhi = 1 + 2 * tlo - thi * thi, 1 + 2 * thi - tlo * tlo   # t^2 in [tlo^2, thi^2]
    assert nlo > 0 and dlo > 0, "numerator / denominator not proved positive"
    return nlo / dhi, nhi / dlo, dlo


def main():
    print("MODE:", "NEGATIVE CONTROL (F perturbed)" if CONTROL else "REAL STATEMENT")
    text = STATEMENT.read_text()
    print("STATEMENT.md sha256", hashlib.sha256(text.encode()).hexdigest())
    Fs = re.search(r"Define \$F\(t,b\)=([^$]+)\$", text).group(1)
    Gs = re.search(r"Define \$G\(t,b\)=([^$]+)\$", text).group(1)
    t0 = Fr(int(re.search(r"\$t_0=(\d+)/10\^\{60\}\$", text).group(1)), 10 ** 60)
    b0 = Fr(int(re.search(r"\$b_0=(\d+)/10\^\{60\}\$", text).group(1)), 10 ** 60)
    assert "$[t_0-10^{-12},t_0+10^{-12}]\\times[b_0-10^{-12},b_0+10^{-12}]$" in text
    assert "$L=(6+4t_*)/(1+2t_*-t_*^2)$" in text
    st = re.search(r"\$(\d\.\d+)<L<(\d\.\d+)\$", text)
    st_lo, st_hi = Fr(st.group(1)), Fr(st.group(2))
    Fp, Gp = parse_poly(Fs), parse_poly(Gs)

    print("\n[0] definitions")
    # my own hand transcription of the statement, grouped by powers of b (t-coefficients ascending)
    FB = [[0, 1, -3, -1, -1], [1, -1, 0, 0, -1, 1], [0, -3, 1, -1, -1]]
    GB = [[0, 0, 0, -2, -2], [-1, 3, -4, 0, 1, 1], [4, -2, -2, 2, -2], [-1, -5, 4, 0, 1, 1], [0, 2, 2]]
    hand = [{(i, j): c for j, row in enumerate(B) for i, c in enumerate(row) if c} for B in (FB, GB)]
    check("parsed F, G equal my hand transcription of STATEMENT.md", [Fp, Gp] == hand,
          "%d + %d monomials" % (len(Fp), len(Gp)))
    up = json.loads(UPSTREAM.read_text())
    updata = [{(int(a), int(b)): int(c) for a, b, c in p} for p in up["polynomials"]]
    check("F, G equal the polynomial DATA in upstream-root-certificate.json", [Fp, Gp] == updata)
    check("(t0,b0), radius equal the box DATA there",
          (t0, b0) == tuple(map(Fr, up["box"]["midpoint"])) and Fr(up["box"]["radius"]) == Fr(1, 10 ** 12))
    if CONTROL:
        Fp = dict(Fp)
        Fp[(2, 0)] = Fp[(2, 0)] - 1                      # -3 t^2  ->  -4 t^2
        print("  CONTROL: coefficient of t^2 in F changed from -3 to", Fp[(2, 0)])
    polys = [Fp, Gp]
    m0 = (t0, b0)
    r0 = Fr(1, 10 ** 12)

    print("\n[1] uniqueness in the statement box X = (t0,b0) +/- 10^-12")
    k1 = krawczyk(polys, m0, r0)
    if check("Krawczyk/Banach test on X (det Y != 0, q < 1, T(X) inside int X)", k1["ok"],
             "q <= %s, eta = %s" % (sci(k1.get("q", Fr(0))), sci(k1.get("eta", Fr(0))))):
        print("     q   =", k1["q"])
        print("     eta =", k1["eta"])
        print("     Jacobian determinant at (t0,b0) ~", sci(k1["det"]))
        print("     Banach radius eta/(1-q) about (t0,b0):", sci(k1["banach_radius"]))
        check("eta/(1-q) < 10^-58 about the statement midpoint", k1["banach_radius"] < Fr(1, 10 ** 58))
    else:
        print("     residual |F|,|G| at (t0,b0):", sci(abs(k1["f"][0])), sci(abs(k1["f"][1])))

    print("\n[2] own centre m* (rational Newton from (36/100, 33/100)) and box X* = m* +/- 10^-100")
    ms = newton(polys, (Fr(36, 100), Fr(33, 100)))
    rs = Fr(1, 10 ** 100)
    print("     m*_t =", ms[0])
    print("     m*_b =", ms[1])
    k2 = krawczyk(polys, ms, rs)
    check("Krawczyk/Banach test on X* (existence + uniqueness in X*)", k2["ok"],
          "q <= %s, eta = %s" % (sci(k2.get("q", Fr(0))), sci(k2.get("eta", Fr(0)))))
    inX = all(m0[i] - r0 < ms[i] - rs and ms[i] + rs < m0[i] + r0 for i in (0, 1))
    check("X* lies strictly inside X (so the zero in X* is THE zero of the statement)", inX,
          "|m* - (t0,b0)| = %s, %s" % (sci(abs(ms[0] - m0[0])), sci(abs(ms[1] - m0[1]))))
    root_ok = k1["ok"] and k2["ok"] and inX
    if not k2["ok"]:
        print("\nRESULT: NOT PROVED (no certified root)")
        return 1
    T = (ms[0] - rs, ms[0] + rs)
    B = (ms[1] - rs, ms[1] + rs)
    print("     t* in [%s,\n            %s]" % T)
    print("     b* in [%s,\n            %s]" % B)
    print("     t* =", dec(T[0], 66), "..  (lower end)")
    print("     b* =", dec(B[0], 66), "..  (lower end)")
    if k1["ok"]:
        dist_hi = max(abs(ms[i] - m0[i]) + rs for i in (0, 1))
        dist_lo = max(abs(ms[i] - m0[i]) - rs for i in (0, 1))
        print("     sup-distance of the root from (t0,b0) lies in [%s, %s]" % (sci(dist_lo), sci(dist_hi)))
        check("that distance is below my own Banach radius from stage 1", dist_hi <= k1["banach_radius"])
        check("root within 10^-58 of (t0,b0) (second derivation, from X*)", dist_hi < Fr(1, 10 ** 58))

    print("\n[3] side L by outward interval arithmetic (no monotonicity used)")
    Llo, Lhi, dlo = side_interval(*T)
    print("     denominator 1+2t-t^2 >=", sci(dlo), "> 0")
    print("     L_lo =", Llo)
    print("     L_hi =", Lhi)
    print("     width =", sci(Lhi - Llo))
    d_lo, d_hi = dec(Llo, 60), dec(Lhi, 60)
    print("     L_lo to 60 digits (truncated):", d_lo)
    print("     L_hi to 60 digits (truncated):", d_hi)
    if d_lo == d_hi:
        print("     => L = %s... (all 60 decimals proved)" % d_lo)
    # second evaluation, by proved monotonicity: L'(t) = 4(t^2+3t-2)/(1+2t-t^2)^2 < 0 on [T]
    mono = T[1] * T[1] + 3 * T[1] - 2 < 0 < T[0]
    s = lambda t: (6 + 4 * t) / (1 + 2 * t - t * t)
    check("cross-check: monotone evaluation [s(t_hi), s(t_lo)] sits inside the interval-arithmetic result",
          mono and Llo <= s(T[1]) <= s(T[0]) <= Lhi)

    print("\n[4] comparisons (exact rational; every margin must be > 0)")

    def inside(name, lo, hi, a, b):
        """[lo,hi] strictly inside (a,b)"""
        ok = check(name, a < lo and hi < b, "margins %s and %s" % (sci(lo - a), sci(b - hi)))
        print("         exact lower margin", lo - a)
        print("         exact upper margin", b - hi)
        return ok

    check("statement: %s < L < %s" % (st.group(1), st.group(2)), st_lo < Llo and Lhi < st_hi,
          "margins %s and %s" % (sci(Llo - st_lo), sci(st_hi - Lhi)))
    packet = json.loads(PACKET.read_text())["endpoint"]
    gate = json.loads(GATE.read_text())
    pk = tuple(map(Fr, packet["L_interval"]))
    print("     packet L_interval = [%s,\n                          %s]  width %s" % (pk[0], pk[1], sci(pk[1] - pk[0])))
    a_ok = inside("(a) L strictly inside the packet's tight L_interval", Llo, Lhi, *pk)
    for nm, iv, cl in zip("tb", (T, B), packet["tight_root_intervals"]):
        a_ok &= inside("(a) %s* strictly inside the packet's tight root interval" % nm, iv[0], iv[1], Fr(cl[0]), Fr(cl[1]))
    check("packet midpoint/radius data equal the statement box",
          tuple(map(Fr, packet["isolating_box_midpoint"])) == m0 and Fr(packet["isolating_box_radius"]) == r0)
    b_ok = True
    for nm, iv, cl in zip("tb", (T, B), gate["root"]["intervals"]):
        b_ok &= inside("(b) %s* strictly inside the terminal gate's tight root interval" % nm, iv[0], iv[1], Fr(cl[0]), Fr(cl[1]))
    gs = tuple(map(Fr, gate["side_interval"]))
    b_ok &= inside("(b) L strictly inside the terminal gate's side_interval", Llo, Lhi, *gs)
    check("     (gate side_interval is identical to the packet L_interval)", gs == pk)
    R = Fr(4675530093604551, 10 ** 15)
    C = Fr(4675531, 10 ** 6)
    U = Fr(1169, 250)
    eps = Fr(323264740583067756265381186720884493986257, 625 * 10 ** 56)     # literal of proof text P087
    ref = json.loads(REFERENCE.read_text())
    check("eps of P087 equals reference squares[0].x - 1/2 and R equals reference side",
          eps == Fr(ref["squares"][0]["x"]) - Fr(1, 2) and R == Fr(ref["side"]) and eps > 0, "eps = " + sci(eps))
    c_ok = check("(c) L > 4", Llo > 4, "margin %s = %s" % (Llo - 4, sci(Llo - 4)))
    c_ok &= check("(c) L < R", Lhi < R, "margin R - L_hi = %s = %s" % (R - Lhi, sci(R - Lhi)))
    c_ok &= check("(c) R < C < U", R < C < U, "margins %s, %s" % (sci(C - R), sci(U - C)))
    c_ok &= check("(c) R - L - eps > 0   (P087 as written)", R - Lhi - eps > 0, "margin %s = %s" % (R - Lhi - eps, sci(R - Lhi - eps)))
    c_ok &= check("(c) R - L - 2 eps > 0 (stronger)", R - Lhi - 2 * eps > 0,
                  "margin %s = %s" % (R - Lhi - 2 * eps, sci(R - Lhi - 2 * eps)))

    print("\n[5] against the author's receipt ENDPOINT_ENCLOSURE_CHECK.json (data only)")
    au = json.loads(AUTHOR.read_text())
    ar = [tuple(map(Fr, x)) for x in au["new_root_intervals"]]
    aL = tuple(map(Fr, au["new_L_interval"]))
    d_ok = True
    for nm, iv, cl in zip("tb", (T, B), ar):
        d_ok &= check("my %s* interval lies inside the author's (so they intersect)" % nm, cl[0] < iv[0] and iv[1] < cl[1],
                      "margins %s, %s" % (sci(iv[0] - cl[0]), sci(cl[1] - iv[1])))
    d_ok &= check("my L interval lies inside the author's new_L_interval", aL[0] < Llo and Lhi < aL[1],
                  "margins %s, %s; author's width %s" % (sci(Llo - aL[0]), sci(aL[1] - Lhi), sci(aL[1] - aL[0])))
    d_ok &= check("author's new_L_interval lies strictly inside the packet L_interval (as the receipt claims)",
                  pk[0] < aL[0] < aL[1] < pk[1], "margins %s, %s" % (sci(aL[0] - pk[0]), sci(pk[1] - aL[1])))
    d_ok &= check("author's root intervals are (t0,b0) +/- 10^-58",
                  ar == [(m0[i] - Fr(1, 10 ** 58), m0[i] + Fr(1, 10 ** 58)) for i in (0, 1)])
    if k1["ok"]:
        dist_hi = max(abs(ms[i] - m0[i]) + rs for i in (0, 1))
        dist_lo = max(abs(ms[i] - m0[i]) - rs for i in (0, 1))
        aq, aeta, adist = Fr(au["contraction_upper"]), Fr(au["residual_upper"]), Fr(au["root_distance_upper"])
        d_ok &= check("author's root_distance_upper really bounds the root's distance from (t0,b0)", dist_hi <= adist,
                      "true distance in [%s, %s], author's bound %s, mine %s"
                      % (sci(dist_lo), sci(dist_hi), sci(adist), sci(k1["banach_radius"])))
        print("     author's q <= %s, mine <= %s; author's eta <= %s, mine %s"
              % (sci(aq), sci(k1["q"]), sci(aeta), sci(k1["eta"])))
        # the author's eta is |J(mid)^-1 (F,G)(mid)|_inf with the EXACT inverse; recompute that number here
        J, f, det = k1["J"], k1["f"], k1["det"]
        exact_eta = max(abs((J[1][1] * f[0] - J[0][1] * f[1]) / det), abs((-J[1][0] * f[0] + J[0][0] * f[1]) / det))
        d_ok &= check("author's residual_upper equals the exact Newton step at (t0,b0) rounded up to 80 digits",
                      0 <= aeta - exact_eta < Fr(1, 10 ** 80), "exact eta = " + sci(exact_eta))
    old = json.loads(OLD.read_text())
    wide = tuple(map(Fr, old["side_interval"]))
    d_ok &= check("author's P087 margins reproduce from the old wide interval",
                  Fr(au["wide_suffices"]["P087_R_minus_Lhi_minus_eps"]) == R - wide[1] - eps
                  and Fr(au["wide_suffices"]["stronger_R_minus_Lhi_minus_2eps"]) == R - wide[1] - 2 * eps)

    print("\n[6] item 5: the old SymPy replay's receipt (endpoint-receipt.json, data only)")
    print("     old side_interval  W = [%s,\n                             %s]  width %s" % (wide[0], wide[1], sci(wide[1] - wide[0])))
    print("     packet L_interval  P = width %s" % sci(pk[1] - pk[0]))
    check("P is strictly inside W:  W_lo < P_lo and P_hi < W_hi", wide[0] < pk[0] and pk[1] < wide[1],
          "P_lo - W_lo = %s, W_hi - P_hi = %s" % (sci(pk[0] - wide[0]), sci(wide[1] - pk[1])))
    check("W is NOT inside P (the old receipt does not establish the tight interval)",
          not (pk[0] <= wide[0] and wide[1] <= pk[1]))
    check("my L interval is inside W", wide[0] < Llo and Lhi < wide[1])
    orr = [tuple(map(Fr, x)) for x in old["root_receipt"]["root_intervals"]]
    for nm, o, cl, i in zip("tb", orr, packet["tight_root_intervals"], (0, 1)):
        cl = (Fr(cl[0]), Fr(cl[1]))
        check("old %s root interval = %s0 +/- 10^-50, packet tight = %s0 +/- 10^-55, tight strictly inside old" % (nm, nm, nm),
              o == (m0[i] - Fr(1, 10 ** 50), m0[i] + Fr(1, 10 ** 50))
              and cl == (m0[i] - Fr(1, 10 ** 55), m0[i] + Fr(1, 10 ** 55)) and o[0] < cl[0] and cl[1] < o[1])
    # what the old 10^-50 box gives for L, by my interval arithmetic:
    wl, wh, _ = side_interval(m0[0] - Fr(1, 10 ** 50), m0[0] + Fr(1, 10 ** 50))
    pl, ph, _ = side_interval(m0[0] - Fr(1, 10 ** 55), m0[0] + Fr(1, 10 ** 55))
    print("     L over t0 +/- 10^-50 (my arithmetic): width %s; over t0 +/- 10^-55: width %s" % (sci(wh - wl), sci(ph - pl)))
    th = m0[0] + Fr(1, 10 ** 50)
    mono50 = th * th + 3 * th - 2 < 0 < m0[0] - Fr(1, 10 ** 50)      # L decreasing on the old t box
    e_lo, e_hi = s(th), s(m0[0] - Fr(1, 10 ** 50))                    # EXACT range of L over t0 +/- 10^-50
    check("EXACT range of L over the old root box t0 +/- 10^-50 strictly contains P (so no evaluation of the "
          "old 10^-50 box can give P)", mono50 and e_lo < pk[0] and pk[1] < e_hi,
          "exact range half-width %s, overshoot %s and %s" % (sci((e_hi - e_lo) / 2), sci(pk[0] - e_lo), sci(e_hi - pk[1])))
    print("     [info] W equals my interval-arithmetic image of t0 +/- 10^-50 up to 10^-69 outward rounding:",
          0 <= wl - wide[0] < Fr(1, 10 ** 69) and 0 <= wide[1] - wh < Fr(1, 10 ** 69))
    print("     [info] P equals my interval-arithmetic image of t0 +/- 10^-55 up to 10^-78 outward rounding:",
          0 <= pl - pk[0] < Fr(1, 10 ** 78) and 0 <= pk[1] - ph < Fr(1, 10 ** 78))
    print("     [info] exact range of L over t0 +/- 10^-55 has width %s (interval arithmetic overestimates it)"
          % sci(s(m0[0] - Fr(1, 10 ** 55)) - s(m0[0] + Fr(1, 10 ** 55))))

    print()
    tight = root_ok and a_ok and b_ok and c_ok
    if tight and not FAILS:
        print("RESULT: PROVED  unique root in the statement box; root in X*; L strictly inside the packet and gate")
        print("        tight intervals; L > 4, L < R < C < U, R - L - 2 eps > 0.")
        return 0
    print("RESULT: NOT PROVED.  Failed checks (%d):" % len(FAILS))
    for n in FAILS:
        print("   -", n)
    return 1


if __name__ == "__main__":
    sys.exit(main())
