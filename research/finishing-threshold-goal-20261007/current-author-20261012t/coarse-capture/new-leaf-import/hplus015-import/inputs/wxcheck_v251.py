#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wxcheck.py -- independent exact checker for certificates of format "wx-cert-2".

Contract: research/window-extension-20261008/SPEC.md, VERSION 2.5.1
(SHA-256 b8f8e9e510bb78ffb6ca181623802eb811f7d6b950e2a1d1926a79f9a2add896), sections 0 to 10.
This program was written from that text alone.  It never reads generator code.
(2.5.1 = 2.5 with one bullet of section 10 made explicit: which evidence each of the two forms of the
closure "infeasible" needs.  This is the reading that was implemented from the start; see _check_node.)

Against the checker for SPEC 2.3 (frozen as wxcheck_v23.py) this file adds exactly the two fact families
of SPEC 2.4 / 2.5; every added block is marked "[SPEC 2.5]":
    wall support facts  wsup:i:W:p|m          (SPEC 4.8)
    kind "Ps" of a parallel class             (SPEC 4.6, KIND "Ps")
and one changed rule of SPEC 10: a `kappa` key is now ignored (not rejected) in P+ and P- declarations.
Not a change of the mathematics, also marked: a certificate file may be gzip-compressed ("[gzip]").

Usage
    python wxcheck.py CERT.jsonl                 full check; prints PASS or FAIL
                                                 (CERT may be gzip-compressed; it is read line by line)
    python wxcheck.py CERT.jsonl --node ID       stand-alone check of one node (its output never contains
                                                 the word that marks a verified certificate; exit code 10 or 1)
    python wxcheck.py CERT.jsonl --json OUT.json machine-readable result
Exit codes
    0   PASS (whole certificate: every node accepted and the tree pass succeeded)
    10  --node mode only: that node is accepted stand-alone (the certificate is not verified by this)
    1   FAIL / node rejected (also for malformed input and for any internal error)
    2   command-line usage error

Only the Python standard library is used; all arithmetic is exact (fractions.Fraction and int).
Every function that carries soundness names the SPEC paragraph it implements in its docstring.

Layout of this file
    A  errors, strict JSON, numbers, labels, rotations, intervals      (SPEC 1, 10)
    B  polynomials over the base variables                             (SPEC 3, 5)
    C  reference data from the packing file                            (SPEC 1)
    D  names: forms, classes, options, facts                           (SPEC 3, 4, 10)
    E  parsing of header and node objects (well-formedness)            (SPEC 2, 6, 8, 10)
    F  node geometry: store-independent polynomials                    (SPEC 2, 3, 4.1, 4.5, 4.6, 4.8)
    G  the bound store, store bounds SB, EMPTY test                    (SPEC 2, 3, 4.3, 4.8)
    H  exclusion, declarations, facts                                  (SPEC 4.0 - 4.8)
    I  steps, rounds, store updates                                    (SPEC 5)
    J  closure of a node; stand-alone node check                       (SPEC 6, 7, 8)
    K  tree pass                                                       (SPEC 6, 7, 8)
    L  command line
"""

import sys
import io                    # [gzip]
import gzip                  # [gzip]
import zlib                  # [gzip]
import json
import re
import hashlib
import argparse
from fractions import Fraction
from math import gcd

CHECKER_VERSION = "wxcheck 1.2 / SPEC 2.5.1 / wx-cert-2"
SPEC_SHA256 = "b8f8e9e510bb78ffb6ca181623802eb811f7d6b950e2a1d1926a79f9a2add896"

# Python >= 3.11 limits int <-> str conversion to 4300 digits by default.  A certificate may be accepted or
# rejected only for mathematical reasons, identically under every Python version, so the limit is removed.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

# Options that never affect soundness.
#   allow_extra_keys: ignore JSON keys that SPEC 10 does not define (default: such a key rejects).
#   paranoid:         recompute every step with the literal Fraction formula of SPEC 5 and compare.
OPTIONS = {"allow_extra_keys": False, "paranoid": False}

HALF = Fraction(1, 2)
ONE = Fraction(1)
ZERO = Fraction(0)

# ======================================================================================================
# A. errors, strict JSON, numbers, labels, rotations, intervals
# ======================================================================================================


class Reject(Exception):
    """The certificate is not accepted.  str(exception) is the reason.  (SPEC 5, REJECTION.)"""


def _json_no_duplicates(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise Reject("duplicate key %r in a JSON object" % (key,))
        out[key] = value
    return out


def _json_no_constant(name):
    raise Reject("JSON constant %s is not allowed" % (name,))


def _json_no_float(text):
    raise Reject("float literal %s is not allowed (numbers are strings 'p' or 'p/q')" % (text,))


def loads_strict(text, what):
    """Parse JSON; duplicate keys, NaN/Infinity and float literals reject.  (SPEC 10: no floats.)"""
    try:
        return json.loads(text, object_pairs_hook=_json_no_duplicates,
                          parse_constant=_json_no_constant, parse_float=_json_no_float)
    except Reject:
        raise
    except RecursionError:
        raise Reject("%s: JSON nested too deeply" % what)
    except ValueError as exc:
        raise Reject("%s: invalid JSON (%s)" % (what, exc))


_NUM_RE = re.compile(r"(-?[0-9]+)(?:/([0-9]+))?")
_UINT_RE = re.compile(r"0|[1-9][0-9]*")          # "integers without sign or leading zeros" (SPEC 10)


def parse_num(x, what):
    """SPEC 10: a number is a JSON string matching -?[0-9]+ or -?[0-9]+/[0-9]+ with nonzero denominator."""
    if type(x) is not str:
        raise Reject("%s: a number must be a string 'p' or 'p/q', got %s" % (what, type(x).__name__))
    m = _NUM_RE.fullmatch(x)
    if m is None:
        raise Reject("%s: malformed number %r" % (what, x[:60]))
    p = int(m.group(1))
    q = 1 if m.group(2) is None else int(m.group(2))
    if q == 0:
        raise Reject("%s: zero denominator in %r" % (what, x[:60]))
    return Fraction(p, q)


def num_str(x):
    """Canonical text of a rational: lowest terms, 'p' or 'p/q' with q > 1."""
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)


LABELS = tuple(i for i in range(1, 18) if i != 4)       # SPEC 0: I = {1,...,17} minus {4}
LABEL_SET = frozenset(LABELS)
PAIRS = tuple((i, j) for i in LABELS for j in LABELS if i < j)     # SPEC 0: a PAIR is two different labels


def need_dict(x, what, required, optional=()):
    """A JSON object with exactly the required keys plus possibly some optional ones."""
    if type(x) is not dict:
        raise Reject("%s: expected a JSON object" % what)
    for key in required:
        if key not in x:
            raise Reject("%s: missing key %r" % (what, key))
    if not OPTIONS["allow_extra_keys"]:
        for key in x:
            if key not in required and key not in optional:
                raise Reject("%s: unknown key %r" % (what, key))
    return x


def need_list(x, what, length=None):
    if type(x) is not list:
        raise Reject("%s: expected a JSON list" % what)
    if length is not None and len(x) != length:
        raise Reject("%s: expected a list of length %d" % (what, length))
    return x


def need_str(x, what):
    if type(x) is not str:
        raise Reject("%s: expected a string" % what)
    return x


def need_label(x, what):
    """SPEC 10: a label in a field is a JSON integer of I (bool is not an integer)."""
    if type(x) is not int or x not in LABEL_SET:
        raise Reject("%s: %r is not a label of I" % (what, x))
    return x


def label_from_text(s, what):
    """A label inside a name or as a map key: decimal string without sign or leading zeros, in I."""
    if type(s) is not str or _UINT_RE.fullmatch(s) is None or int(s) not in LABEL_SET:
        raise Reject("%s: %r is not a label of I" % (what, s))
    return int(s)


def need_label_map(x, what):
    """SPEC 10: every map keyed by labels has exactly the 16 keys of I.  Returns {label: value}."""
    if type(x) is not dict:
        raise Reject("%s: expected a JSON object keyed by labels" % what)
    out = {}
    for key, value in x.items():
        out[label_from_text(key, what + " key")] = value
    if len(out) != len(LABELS) or len(x) != len(LABELS):
        raise Reject("%s: must have exactly the 16 labels of I as keys" % what)
    return out


def need_choice(x, what, choices):
    """A JSON value that must be one of the given constants, with the same JSON type."""
    for c in choices:
        if type(x) is type(c) and x == c:
            return x
    raise Reject("%s: %r is not one of %r" % (what, x, tuple(choices)))


def need_pair_labels(i, j, what):
    """SPEC 0 / 10: wherever i, j name a pair: i < j, both in I."""
    need_label(i, what + " i")
    need_label(j, what + " j")
    if not i < j:
        raise Reject("%s: a pair needs i < j, got (%d, %d)" % (what, i, j))
    return (i, j)


# ---- vectors and rotations (SPEC 1) -------------------------------------------------------------------

def rot_mul(P, Q):
    """SPEC 1: rotations (and unit vectors) are multiplied as complex numbers g + i s."""
    return (P[0] * Q[0] - P[1] * Q[1], P[0] * Q[1] + P[1] * Q[0])


def rot_conj(P):
    """SPEC 1: conj(g, s) := (g, -s)."""
    return (P[0], -P[1])


def vec_J(v):
    """SPEC 0: J(x, y) := (-y, x)."""
    return (-v[1], v[0])


def vec_dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def vec_scale(c, v):
    return (c * v[0], c * v[1])


ROT_ID = (ONE, ZERO)


def parse_rot(x, what):
    """SPEC 10: a rotation is [g, s] with g^2 + s^2 = 1 (checked for every rotation in the file)."""
    need_list(x, what, 2)
    g = parse_num(x[0], what + " [g]")
    s = parse_num(x[1], what + " [s]")
    if g * g + s * s != 1:
        raise Reject("%s: not a rotation, g^2 + s^2 != 1" % what)
    return (g, s)


def rot_str(P):
    return [num_str(P[0]), num_str(P[1])]


# ---- exact interval arithmetic (SPEC 3) ---------------------------------------------------------------
# An interval is a pair (lo, hi) of Fractions with lo <= hi.  Product and sum of proper intervals are the
# exact ranges of products and sums of independent variables, hence associative and commutative.

def iv_add(X, Y):
    return (X[0] + Y[0], X[1] + Y[1])


def iv_sub(X, Y):
    return (X[0] - Y[1], X[1] - Y[0])


def iv_scale(c, X):
    return (c * X[0], c * X[1]) if c >= 0 else (c * X[1], c * X[0])


def iv_mul(X, Y):
    p = (X[0] * Y[0], X[0] * Y[1], X[1] * Y[0], X[1] * Y[1])
    return (min(p), max(p))


def lcm(a, b):
    return a // gcd(a, b) * b


# ======================================================================================================
# B. polynomials over the base variables (SPEC 3)
# ======================================================================================================
# Base variables are numbered 0..64:  xi_ik (32),  S,  C_i (16),  s_i (16).
# A monomial is a sorted tuple of variable numbers, a variable of exponent e occurring e times; () is 1.
# A polynomial ("poly") is a dict {monomial: Fraction} without zero coefficients.

VAR_NAMES = []           # variable number -> name of the base-variable form
VAR_FORMS = []           # variable number -> parsed base-variable form (section D)
VAR_XI = {}
VAR_C = {}
VAR_s = {}
for _i in LABELS:
    for _k in (1, 2):
        VAR_XI[(_i, _k)] = len(VAR_NAMES)
        VAR_NAMES.append("xi:%d:%d" % (_i, _k))
        VAR_FORMS.append(("xi", _i, _k))
VAR_S = len(VAR_NAMES)
VAR_NAMES.append("S")
VAR_FORMS.append(("S",))
for _i in LABELS:
    VAR_C[_i] = len(VAR_NAMES)
    VAR_NAMES.append("C:%d" % _i)
    VAR_FORMS.append(("C", _i))
for _i in LABELS:
    VAR_s[_i] = len(VAR_NAMES)
    VAR_NAMES.append("s:%d" % _i)
    VAR_FORMS.append(("s", _i))
NVARS = len(VAR_NAMES)          # 65
XI_VARS = frozenset(VAR_XI.values())


def p_const(c):
    c = Fraction(c)
    return {(): c} if c != 0 else {}


def p_var(v):
    return {(v,): ONE}


def p_add(p, q):
    out = dict(p)
    for m, c in q.items():
        c2 = out.get(m, ZERO) + c
        if c2 == 0:
            out.pop(m, None)
        else:
            out[m] = c2
    return out


def p_scale(c, p):
    c = Fraction(c)
    if c == 0:
        return {}
    return {m: c * a for m, a in p.items()}


def p_sub(p, q):
    return p_add(p, p_scale(-1, q))


def p_mul(p, q):
    out = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            m = tuple(sorted(m1 + m2))
            c = out.get(m, ZERO) + c1 * c2
            if c == 0:
                out.pop(m, None)
            else:
                out[m] = c
    return out


def p_lin(*terms):
    """Sum of coef * poly over the given (coef, poly) pairs."""
    out = {}
    for c, p in terms:
        out = p_add(out, p_scale(c, p))
    return out


def p_is_affine_in_xi(p):
    """True iff p = c0 + sum c_ik xi_ik (every monomial is 1 or a single position variable)."""
    for m in p:
        if len(m) > 1 or (len(m) == 1 and m[0] not in XI_VARS):
            return False
    return True


# Integer-scaled form used in the hot loop of SPEC 5:  (den, {monomial: int})  means  (1/den) * sum.

def sp_from_poly(p):
    den = 1
    for c in p.values():
        den = lcm(den, c.denominator)
    return (den, {m: c.numerator * (den // c.denominator) for m, c in p.items()})


def sp_mul(a, b):
    out = {}
    for m1, c1 in a[1].items():
        for m2, c2 in b[1].items():
            m = tuple(sorted(m1 + m2))
            out[m] = out.get(m, 0) + c1 * c2
    return (a[0] * b[0], out)


# ======================================================================================================
# C. reference data from the packing file (SPEC 1)
# ======================================================================================================

SREF_SPEC = Fraction(4675530093604551, 10 ** 15)      # SPEC 0

# SHA-256 of <project root>/upper-packing-certificate.json when this checker was written.  By default the
# packing file that is read must have this hash (and the header must name the same hash); the command
# line option --no-packing-pin removes the pin (the header hash must still equal the file read).
PINNED_PACKING_SHA256 = "24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7"


class Reference(object):
    """SPEC 1: p_i, u_i, v_i, frames e_i1, e_i2, Sref, and the SHA-256 of the packing file."""

    def __init__(self, path):
        try:
            with open(path, "rb") as fh:
                raw = fh.read()
        except (OSError, IOError) as exc:
            raise Reject("cannot read the packing file %r (%s)" % (path, exc))
        self.path = path
        self.sha256 = hashlib.sha256(raw).hexdigest()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            raise Reject("packing file is not UTF-8")
        doc = loads_strict(text, "packing file")
        if type(doc) is not dict or "side" not in doc or "squares" not in doc:
            raise Reject("packing file: keys 'side' and 'squares' are required")
        self.side = parse_num(doc["side"], "packing file side")
        if self.side != SREF_SPEC:
            raise Reject("packing file: side differs from Sref of SPEC section 0")
        squares = need_list(doc["squares"], "packing file squares", 17)
        self.p_file, self.t, self.u, self.v = {}, {}, {}, {}
        for idx, sq in enumerate(squares):
            label = idx + 1                       # SPEC 0: labels = 1-based order of the list
            if type(sq) is not dict:
                raise Reject("packing file: square %d is not an object" % label)
            for key in ("x", "y", "t"):
                if key not in sq:
                    raise Reject("packing file: square %d has no %r" % (label, key))
            x = parse_num(sq["x"], "packing x")
            y = parse_num(sq["y"], "packing y")
            t = parse_num(sq["t"], "packing t")
            den = 1 + t * t
            u = ((1 - t * t) / den, 2 * t / den)                      # SPEC 1
            self.p_file[label], self.t[label], self.u[label], self.v[label] = (x, y), t, u, vec_J(u)
        u9x = self.u[9][0]
        T0 = u9x * (u9x + 4 - self.side)                              # SPEC 1
        self.p = {}
        for i in LABELS:
            self.p[i] = self.p_file[i]
        shift = vec_scale(T0 / 3, self.v[13])
        self.p[13] = (self.p_file[13][0] - shift[0], self.p_file[13][1] - shift[1])
        self.e = {}                                                    # SPEC 1: frames
        for i in LABELS:
            if i in (11, 13):
                self.e[i] = (self.u[i], self.v[i])
            else:
                self.e[i] = ((ONE, ZERO), (ZERO, ONE))


# ======================================================================================================
# D. names: forms, classes, options, facts (SPEC 3, 4, 10)
# ======================================================================================================
# Parsed FORM  (a tuple; the map name -> tuple is injective because integers are canonical):
#   ('xi', i, k)  ('S',)  ('C', i)  ('s', i)  ('Da'|'Db'|'A'|'B', o, t)  ('Cr'|'Sr', i, j)
#   ('al'|'be'|'co'|'si'|'Y', i, j, K)  ('u', NAME)  ('0',)
# Parsed CLASS K: the four-character string, e.g. 'a+b-'.
# Parsed OPTION: (o, t, axis, eps) with axis in 'ab', eps in (1, -1).
# Parsed FACT:
#   ('box', i, k, side)  ('side', side)  ('wall', i, e1, e2, 'x'|'y', side)
#   ('arc', i, which)  ('arctan', i, G, H)  ('rarc', i, j, which)  ('rarctan', i, j, G, H)
#   ('opt', o, t, axis, eps, e1, e2)  ('par', i, j, K, kind, 1|2)  ('asg', i, j, K, sign)
#   ('ivl', FORM, side)  ('cut', FORM, side)  ('circ', i)
#   ('wsup', i, W, sign)                                                    [SPEC 2.5]
# with side in ('lo', 'hi'), which in ARC_WHICH and W in WSUP_WALLS.

_CLS_RE = re.compile(r"[ab][+-][ab][+-]")
_CUSTOM_RE = re.compile(r"[A-Za-z0-9_]+")
ARC_WHICH = ("slo", "shi", "clo", "chi", "chord")
PAR_KINDS = ("P+", "P-", "Pk", "Ps")           # [SPEC 2.5] "Ps": SPEC 4.6, KIND "Ps"
WSUP_WALLS = ("xlo", "ylo", "xhi", "yhi")      # [SPEC 2.5] wall names of wsup facts (SPEC 4.8, 10)
CLASS_FORMS = ("al", "be", "co", "si", "Y")
BASE_FORM_KINDS = ("xi", "S", "C", "s")
_PM = {"p": 1, "m": -1}
_PM_INV = {1: "p", -1: "m"}


def parse_cls(x, what):
    """SPEC 3 / 10: a class is written as four characters matching [ab][+-][ab][+-]."""
    if type(x) is not str or _CLS_RE.fullmatch(x) is None:
        raise Reject("%s: %r is not a class [ab][+-][ab][+-]" % (what, x))
    return x


def cls_parts(K):
    """SPEC 4.6: K = (axis_i, eps_i, axis_j, eps_j)."""
    return (K[0], 1 if K[1] == "+" else -1, K[2], 1 if K[3] == "+" else -1)


def cls_options(i, j, K):
    """SPEC 4.6: the two options of class K:  O_i = (i, j, axis_i, eps_i),  O_j = (j, i, axis_j, -eps_j)."""
    axis_i, eps_i, axis_j, eps_j = cls_parts(K)
    return (i, j, axis_i, eps_i), (j, i, axis_j, -eps_j)


def pair_options(i, j):
    """SPEC 4.5: the 8 options of the pair {i, j} (two different labels)."""
    if i == j:
        raise Reject("internal: pair_options needs two different labels")
    return tuple((o, t, axis, eps) for (o, t) in ((i, j), (j, i)) for axis in ("a", "b") for eps in (1, -1))


def _ordered_pair(tok_o, tok_t, what):
    """SPEC 10: wherever o, t occur: o != t, both in I."""
    o = label_from_text(tok_o, what)
    t = label_from_text(tok_t, what)
    if o == t:
        raise Reject("%s: o and t must be different labels" % what)
    return o, t


def _sorted_pair(tok_i, tok_j, what):
    """SPEC 10: wherever i, j name a pair: i < j, both in I."""
    i = label_from_text(tok_i, what)
    j = label_from_text(tok_j, what)
    if not i < j:
        raise Reject("%s: a pair in a name needs i < j" % what)
    return i, j


def parse_form_tokens(tok, what, custom):
    """SPEC 10, 'Form NAMEs'.  tok: the name split at ':'.  custom: names defined in the node's `forms`
    (None while the `forms` field itself is parsed: then `u:...` is not allowed)."""
    n = len(tok)
    head = tok[0]
    if head == "0" and n == 1:
        return ("0",)
    if head == "S" and n == 1:
        return ("S",)
    if head == "xi" and n == 3:
        i = label_from_text(tok[1], what)
        if tok[2] not in ("1", "2"):
            raise Reject("%s: k must be 1 or 2" % what)
        return ("xi", i, int(tok[2]))
    if head in ("C", "s") and n == 2:
        return (head, label_from_text(tok[1], what))
    if head in ("Da", "Db", "A", "B") and n == 3:
        o, t = _ordered_pair(tok[1], tok[2], what)
        return (head, o, t)
    if head in ("Cr", "Sr") and n == 3:
        i, j = _sorted_pair(tok[1], tok[2], what)
        return (head, i, j)
    if head in CLASS_FORMS and n == 4:
        i, j = _sorted_pair(tok[1], tok[2], what)
        return (head, i, j, parse_cls(tok[3], what))
    if head == "u" and n == 2:
        if custom is None:
            raise Reject("%s: a custom form may not be used here" % what)
        if _CUSTOM_RE.fullmatch(tok[1]) is None or tok[1] not in custom:
            raise Reject("%s: custom form u:%s is not defined in the node's `forms`" % (what, tok[1][:40]))
        return ("u", tok[1])
    raise Reject("%s: unknown form name" % what)


def parse_form_name(name, what, custom):
    if type(name) is not str:
        raise Reject("%s: a form name must be a string" % what)
    return parse_form_tokens(name.split(":"), "%s (form %r)" % (what, name[:60]), custom)


def form_name(form):
    """Inverse of parse_form_name."""
    return ":".join(str(x) for x in form)


def _side(tok, what):
    if tok not in ("lo", "hi"):
        raise Reject("%s: expected lo or hi" % what)
    return tok


def _corner(tok, what):
    if tok not in _PM:
        raise Reject("%s: a sign letter must be p or m" % what)
    return _PM[tok]


def parse_fact_name(name, what, custom, affine_custom):
    """SPEC 10, 'FACT names'.  custom / affine_custom: the node's custom form names / the affine ones."""
    if type(name) is not str:
        raise Reject("%s: a fact name must be a string" % what)
    what = "%s (fact %r)" % (what, name[:80])
    tok = name.split(":")
    n = len(tok)
    head = tok[0]
    if head == "box" and n == 4:
        i = label_from_text(tok[1], what)
        if tok[2] not in ("1", "2"):
            raise Reject("%s: k must be 1 or 2" % what)
        return ("box", i, int(tok[2]), _side(tok[3], what))
    if head == "side" and n == 2:
        return ("side", _side(tok[1], what))
    if head == "wall" and n == 6:
        i = label_from_text(tok[1], what)
        if tok[4] not in ("x", "y"):
            raise Reject("%s: wall coordinate must be x or y" % what)
        return ("wall", i, _corner(tok[2], what), _corner(tok[3], what), tok[4], _side(tok[5], what))
    if head == "arc" and n == 3 and tok[2] in ARC_WHICH:
        return ("arc", label_from_text(tok[1], what), tok[2])
    if head == "arc" and n == 5 and tok[2] == "tan":
        G = parse_num(tok[3], what + " G")
        H = parse_num(tok[4], what + " H")
        if G * G + H * H > 1:
            raise Reject("%s: tangent vector needs G^2 + H^2 <= 1" % what)       # SPEC 4.2 "(checked)"
        return ("arctan", label_from_text(tok[1], what), G, H)
    if head == "rarc" and n == 4 and tok[3] in ARC_WHICH:
        i, j = _sorted_pair(tok[1], tok[2], what)
        return ("rarc", i, j, tok[3])
    if head == "rarc" and n == 6 and tok[3] == "tan":
        i, j = _sorted_pair(tok[1], tok[2], what)
        G = parse_num(tok[4], what + " G")
        H = parse_num(tok[5], what + " H")
        if G * G + H * H > 1:
            raise Reject("%s: tangent vector needs G^2 + H^2 <= 1" % what)       # SPEC 4.3 = 4.2
        return ("rarctan", i, j, G, H)
    if head == "opt" and n == 7:
        o, t = _ordered_pair(tok[1], tok[2], what)
        if tok[3] not in ("a", "b"):
            raise Reject("%s: axis must be a or b" % what)
        return ("opt", o, t, tok[3], _corner(tok[4], what), _corner(tok[5], what), _corner(tok[6], what))
    if head == "par" and n == 6:
        i, j = _sorted_pair(tok[1], tok[2], what)
        K = parse_cls(tok[3], what)
        if tok[4] not in PAR_KINDS or tok[5] not in ("1", "2"):
            raise Reject("%s: expected par:i:j:K:P+|P-|Pk|Ps:1|2" % what)
        return ("par", i, j, K, tok[4], int(tok[5]))
    if head == "asg" and n == 5:
        i, j = _sorted_pair(tok[1], tok[2], what)
        return ("asg", i, j, parse_cls(tok[3], what), _corner(tok[4], what))
    if head == "circ" and n == 2:
        return ("circ", label_from_text(tok[1], what))
    if head == "wsup" and n == 4:                                # [SPEC 2.5] wsup:i:W:p|m  (SPEC 4.8, 10)
        i = label_from_text(tok[1], what)
        if tok[2] not in WSUP_WALLS:
            raise Reject("%s: the wall name of a wsup fact must be xlo, ylo, xhi or yhi" % what)
        return ("wsup", i, tok[2], _corner(tok[3], what))
    if head in ("ivl", "cut") and n >= 3:
        side = _side(tok[-1], what)
        form = parse_form_tokens(tok[1:-1], what, custom)
        if head == "cut":
            if form == ("0",):
                raise Reject("%s: no cut on the form 0" % what)
            return ("cut", form, side)
        if form[0] in ("Da", "Db") or (form[0] == "u" and form[1] in affine_custom):
            return ("ivl", form, side)
        raise Reject("%s: ivl facts exist only for Da, Db and affine custom forms" % what)
    raise Reject("%s: unknown fact name" % what)


# ======================================================================================================
# E. parsing of header and node objects: well-formedness (SPEC 2, 6, 8, 10)
# ======================================================================================================

def parse_interval(x, what, ordered):
    need_list(x, what, 2)
    lo = parse_num(x[0], what + " lo")
    hi = parse_num(x[1], what + " hi")
    if ordered and lo > hi:
        raise Reject("%s: lo > hi" % what)
    return (lo, hi)


def parse_box(x, what, ordered):
    """{"<label>": [[lo1,hi1],[lo2,hi2]]} for exactly the 16 labels  ->  {(i, k): (lo, hi)}."""
    out = {}
    for i, entry in need_label_map(x, what).items():
        need_list(entry, "%s[%d]" % (what, i), 2)
        for k in (1, 2):
            out[(i, k)] = parse_interval(entry[k - 1], "%s[%d][k=%d]" % (what, i, k), ordered)
    return out


def parse_option(x, what, extra=()):
    """SPEC 4.5 / 10: {"o":o,"t":t,"axis":"a"|"b","eps":1|-1} with o != t, both in I."""
    need_dict(x, what, ("o", "t", "axis", "eps") + tuple(extra))
    o = need_label(x["o"], what + " o")
    t = need_label(x["t"], what + " t")
    if o == t:
        raise Reject("%s: an option needs two different labels (o != t)" % what)
    axis = need_choice(x["axis"], what + " axis", ("a", "b"))
    eps = need_choice(x["eps"], what + " eps", (1, -1))
    return (o, t, axis, eps)


def parse_assumption(x, what):
    """SPEC 6 / 10: ('opt', o, t, axis, eps)  or  ('ysign', i, j, K, sign)."""
    if type(x) is not dict or "kind" not in x:
        raise Reject("%s: an assumption needs a key 'kind'" % what)
    kind = need_choice(x["kind"], what + " kind", ("opt", "ysign"))
    if kind == "opt":
        return ("opt",) + parse_option(x, what, extra=("kind",))
    need_dict(x, what, ("kind", "i", "j", "cls", "sign"))
    i, j = need_pair_labels(x["i"], x["j"], what)
    return ("ysign", i, j, parse_cls(x["cls"], what + " cls"), need_choice(x["sign"], what + " sign", (1, -1)))


def parse_forms(x, what):
    """SPEC 3 / 10 (`forms`): {"NAME": [["coef","FORMNAME"],...]}  ->  {NAME: ((coef, FORM), ...)}.
    Components are built-in form names other than `0` and `u:...`, pairwise different within one form.
    Stricter than the text: a custom form needs at least one component."""
    if type(x) is not dict:
        raise Reject("%s: expected a JSON object" % what)
    out = {}
    for name, comps in x.items():
        w = "%s[%r]" % (what, name[:40])
        if _CUSTOM_RE.fullmatch(name) is None:
            raise Reject("%s: a custom form name must match [A-Za-z0-9_]+" % w)
        need_list(comps, w)
        if len(comps) == 0:
            raise Reject("%s: a custom form needs at least one component" % w)
        parsed, seen = [], set()
        for idx, comp in enumerate(comps):
            need_list(comp, "%s[%d]" % (w, idx), 2)
            coef = parse_num(comp[0], "%s[%d] coefficient" % (w, idx))
            form = parse_form_name(comp[1], "%s[%d]" % (w, idx), None)
            if form == ("0",):
                raise Reject("%s: the form 0 may not be a component" % w)
            if form in seen:
                raise Reject("%s: component %s occurs twice" % (w, form_name(form)))
            seen.add(form)
            parsed.append((coef, form))
        out[name] = tuple(parsed)
    return out


class StepData(object):
    """One step of a round (SPEC 5 / 10)."""
    __slots__ = ("form", "sense", "value", "terms")


class StoreData(object):
    """A bound store (SPEC 2).  box {(i,k): (lo,hi)}; arc {i: (P-, P+)}; rarc {(i,j): (St- or None,
    St+ or None)}; cuts {(FORM, 'lo'|'hi'): value}."""
    __slots__ = ("S", "box", "arc", "rarc", "cuts")


class RoundData(object):
    __slots__ = ("pairs", "steps", "store")


class NodeData(object):
    __slots__ = ("id", "parent", "S", "box", "centre", "arc", "assume", "forms", "affine_custom",
                 "rounds", "close")


def parse_store(x, what, custom):
    """SPEC 5 / 10: a proposed store lists `S`, all 32 box intervals and all 16 arcs; `rarc` and `cuts`
    list what is kept.  Only syntax is checked here; acceptance is section I."""
    need_dict(x, what, ("S", "box", "arc", "rarc", "cuts"))
    st = StoreData()
    st.S = parse_interval(x["S"], what + " S", ordered=False)
    st.box = parse_box(x["box"], what + " box", ordered=False)
    st.arc = {}
    for i, entry in need_label_map(x["arc"], what + " arc").items():
        w = "%s arc[%d]" % (what, i)
        if type(entry) is dict and "c" in entry:
            raise Reject("%s: a store arc entry has no centre (centres never change)" % w)      # SPEC 10
        need_dict(entry, w, ("lo", "hi"))
        st.arc[i] = (parse_rot(entry["lo"], w + " lo"), parse_rot(entry["hi"], w + " hi"))
    st.rarc = {}
    if type(x["rarc"]) is not dict:
        raise Reject("%s rarc: expected a JSON object" % what)
    for key, entry in x["rarc"].items():
        w = "%s rarc[%r]" % (what, key[:40])
        tok = key.split("-")
        if len(tok) != 2:
            raise Reject("%s: key must be 'i-j'" % w)
        i, j = _sorted_pair(tok[0], tok[1], w)
        need_dict(entry, w, ("lo", "hi"))
        lo = None if entry["lo"] is None else parse_rot(entry["lo"], w + " lo")
        hi = None if entry["hi"] is None else parse_rot(entry["hi"], w + " hi")
        st.rarc[(i, j)] = (lo, hi)
    st.cuts = {}
    if type(x["cuts"]) is not dict:
        raise Reject("%s cuts: expected a JSON object" % what)
    for key, value in x["cuts"].items():
        w = "%s cuts[%r]" % (what, key[:60])
        tok = key.split(":")
        if len(tok) < 2:
            raise Reject("%s: key must be 'NAME:lo' or 'NAME:hi'" % w)
        side = _side(tok[-1], w)
        form = parse_form_tokens(tok[:-1], w, custom)
        if form == ("0",):
            raise Reject("%s: no cut on the form 0" % w)
        st.cuts[(form, side)] = parse_num(value, w)
    return st


def parse_round(x, what, custom, affine_custom):
    """SPEC 10, ROUND: declarations, steps, proposed store (syntax and well-formedness only)."""
    need_dict(x, what, ("pairs", "steps", "store"))
    rd = RoundData()
    rd.pairs = []
    seen_par = set()
    for idx, d in enumerate(need_list(x["pairs"], what + " pairs")):
        w = "%s pairs[%d]" % (what, idx)
        if type(d) is not dict or "mode" not in d:
            raise Reject("%s: a declaration needs a key 'mode'" % w)
        mode = need_choice(d["mode"], w + " mode", ("opt", "par"))
        if mode == "opt":
            o, t, axis, eps = parse_option(d, w, extra=("i", "j", "mode"))
            i, j = need_pair_labels(d["i"], d["j"], w)
            if {o, t} != {i, j}:
                raise Reject("%s: an opt declaration needs {o,t} = {i,j}" % w)
            rd.pairs.append(("opt", o, t, axis, eps))
        else:
            if "kind" not in d:
                raise Reject("%s: missing key 'kind'" % w)
            kind = need_choice(d["kind"], w + " kind", PAR_KINDS)
            if kind in ("Pk", "Ps"):                                    # [SPEC 2.5] kappa is required for Pk and Ps
                need_dict(d, w, ("i", "j", "mode", "cls", "kind", "kappa"))
                kappa = parse_num(d["kappa"], w + " kappa")
            else:                                                       # [SPEC 2.5] ... and ignored for P+, P-
                need_dict(d, w, ("i", "j", "mode", "cls", "kind"), optional=("kappa",))
                if "kappa" in d:
                    parse_num(d["kappa"], w + " kappa")                 # it must be a number; its value is not used
                kappa = None
            i, j = need_pair_labels(d["i"], d["j"], w)
            K = parse_cls(d["cls"], w + " cls")
            if (i, j, K, kind) in seen_par:
                raise Reject("%s: second par declaration for the same (i, j, cls, kind) in one round" % w)
            seen_par.add((i, j, K, kind))
            rd.pairs.append(("par", i, j, K, kind, kappa))
    rd.steps = []
    for idx, s in enumerate(need_list(x["steps"], what + " steps")):
        w = "%s steps[%d]" % (what, idx)
        need_dict(s, w, ("form", "sense", "value", "terms"))
        sd = StepData()
        sd.form = parse_form_name(s["form"], w, custom)
        sd.sense = need_choice(s["sense"], w + " sense", ("lo", "hi"))
        if sd.form == ("0",) and sd.sense != "lo":
            raise Reject("%s: a step on the form 0 must have sense lo" % w)
        sd.value = parse_num(s["value"], w + " value")
        sd.terms = []
        for tidx, term in enumerate(need_list(s["terms"], w + " terms")):
            wt = "%s terms[%d]" % (w, tidx)
            need_list(term, wt, 2)
            lam = parse_num(term[0], wt + " multiplier")
            names = need_list(term[1], wt + " facts")
            if not 1 <= len(names) <= 3:
                raise Reject("%s: a term needs 1 to 3 fact names" % wt)            # SPEC 5
            facts = tuple(parse_fact_name(nm, wt, custom, affine_custom) for nm in names)
            if lam < 0 and not any(f[0] == "circ" for f in facts):
                raise Reject("%s: negative multiplier in a term without a circ fact" % wt)   # SPEC 5
            sd.terms.append((lam, facts))
        rd.steps.append(sd)
    rd.store = parse_store(x["store"], what + " store", custom)
    return rd


def parse_split(x, what):
    """SPEC 10, SPLIT.  Returns ('box', i, k, m) | ('arc', i, M) | ('opt', (i, j), options) |
    ('ysign', i, j, K)."""
    if type(x) is not dict or "type" not in x:
        raise Reject("%s: a split needs a key 'type'" % what)
    typ = need_choice(x["type"], what + " type", ("box", "arc", "opt", "ysign"))
    if typ == "box":
        need_dict(x, what, ("type", "sq", "k", "at"))
        return ("box", need_label(x["sq"], what + " sq"), need_choice(x["k"], what + " k", (1, 2)),
                parse_num(x["at"], what + " at"))
    if typ == "arc":
        need_dict(x, what, ("type", "sq", "at"))
        return ("arc", need_label(x["sq"], what + " sq"), parse_rot(x["at"], what + " at"))
    if typ == "opt":
        need_dict(x, what, ("type", "pair", "options"))
        need_list(x["pair"], what + " pair", 2)
        i, j = need_pair_labels(x["pair"][0], x["pair"][1], what + " pair")
        opts = []
        for idx, o in enumerate(need_list(x["options"], what + " options")):
            opt = parse_option(o, "%s options[%d]" % (what, idx))
            if {opt[0], opt[1]} != {i, j}:
                raise Reject("%s options[%d]: not an option of the pair" % (what, idx))
            opts.append(opt)
        if len(opts) == 0:
            raise Reject("%s: an option split needs a nonempty list of options" % what)
        return ("opt", (i, j), tuple(opts))
    need_dict(x, what, ("type", "i", "j", "cls"))
    i, j = need_pair_labels(x["i"], x["j"], what)
    return ("ysign", i, j, parse_cls(x["cls"], what + " cls"))


def parse_close(x, what):
    """SPEC 10, `close`.  Returns ('infeasible', None | (i, j)) | ('terminal',) | ('split', how, ids)."""
    if type(x) is not dict or "kind" not in x:
        raise Reject("%s: the closure needs a key 'kind'" % what)
    kind = need_choice(x["kind"], what + " kind", ("infeasible", "terminal", "split"))
    if kind == "infeasible":
        need_dict(x, what, ("kind",), optional=("pair",))
        if "pair" not in x:
            return ("infeasible", None)
        need_list(x["pair"], what + " pair", 2)
        return ("infeasible", need_pair_labels(x["pair"][0], x["pair"][1], what + " pair"))
    if kind == "terminal":
        need_dict(x, what, ("kind",))
        return ("terminal",)
    need_dict(x, what, ("kind", "how", "children"))
    how = parse_split(x["how"], what + " how")
    children = tuple(need_str(c, what + " children") for c in need_list(x["children"], what + " children"))
    want = len(how[2]) if how[0] == "opt" else 2                                  # SPEC 7
    if len(children) != want:
        raise Reject("%s: a %s split needs %d children, got %d" % (what, how[0], want, len(children)))
    if len(set(children)) != len(children):
        raise Reject("%s: a child id occurs twice" % what)
    return ("split", how, children)


def parse_node(x, what="node"):
    """SPEC 2 / 10: a node object.  All well-formedness that does not need a store is checked here,
    for every round, including rounds that will not be evaluated."""
    need_dict(x, what, ("id", "parent", "S", "box", "arc", "assume", "rounds", "close"), optional=("forms",))
    nd = NodeData()
    nd.id = need_str(x["id"], what + " id")
    if nd.id == "":
        raise Reject("%s: empty node id" % what)
    what = "node %r" % (nd.id[:60],)
    nd.parent = None if x["parent"] is None else need_str(x["parent"], what + " parent")
    nd.S = parse_interval(x["S"], what + " S", ordered=True)                   # S_lo <= S_hi
    nd.box = parse_box(x["box"], what + " box", ordered=True)                  # lo <= hi
    nd.centre, nd.arc = {}, {}
    for i, entry in need_label_map(x["arc"], what + " arc").items():
        w = "%s arc[%d]" % (what, i)
        need_dict(entry, w, ("c", "lo", "hi"))
        nd.centre[i] = parse_rot(entry["c"], w + " c")
        Pm = parse_rot(entry["lo"], w + " lo")
        Pp = parse_rot(entry["hi"], w + " hi")
        if not (Pm[0] > 0 and Pp[0] > 0):
            raise Reject("%s: an arc endpoint has non-positive cosine" % w)    # SPEC 2
        if Pm[1] > Pp[1]:
            raise Reject("%s: sin P^- > sin P^+" % w)                          # SPEC 2
        nd.arc[i] = (Pm, Pp)
    nd.assume = tuple(parse_assumption(a, "%s assume[%d]" % (what, idx))
                      for idx, a in enumerate(need_list(x["assume"], what + " assume")))
    nd.forms = parse_forms(x["forms"], what + " forms") if "forms" in x else {}
    nd.affine_custom = frozenset(name for name, comps in nd.forms.items()
                                 if all(f[0] in ("xi", "Da", "Db") for (_c, f) in comps))     # SPEC 3
    custom = frozenset(nd.forms)
    nd.rounds = [parse_round(r, "%s round %d" % (what, idx + 1), custom, nd.affine_custom)
                 for idx, r in enumerate(need_list(x["rounds"], what + " rounds"))]
    nd.close = parse_close(x["close"], what + " close")
    return nd


class Region(object):
    """SPEC 8: a window or tube: a box and an angle radius alpha_i > 0 for every i."""
    __slots__ = ("box", "alpha")


def parse_region(x, what):
    need_dict(x, what, ("box", "alpha"))
    rg = Region()
    rg.box = parse_box(x["box"], what + " box", ordered=True)
    rg.alpha = {}
    for i, a in need_label_map(x["alpha"], what + " alpha").items():
        rg.alpha[i] = parse_num(a, "%s alpha[%d]" % (what, i))
        if not rg.alpha[i] > 0:
            raise Reject("%s alpha[%d]: an angle radius must be > 0" % (what, i))    # SPEC 8
    return rg


class Header(object):
    __slots__ = ("root", "window", "terminal", "packing_sha256", "Sref")


def parse_header(x, ref):
    """SPEC 10, Header, and the first well-formedness bullet: schema, packing hash, Sref."""
    need_dict(x, "header", ("schema", "packing_sha256", "Sref", "root", "window", "terminal"))
    if type(x["schema"]) is not str or x["schema"] != "wx-cert-2":
        raise Reject("header: schema is not 'wx-cert-2'")
    hd = Header()
    hd.packing_sha256 = need_str(x["packing_sha256"], "header packing_sha256")
    if hd.packing_sha256 != ref.sha256:
        raise Reject("header: packing_sha256 differs from the SHA-256 of the packing file read (%s)"
                     % ref.sha256)
    hd.Sref = parse_num(x["Sref"], "header Sref")
    if hd.Sref != ref.side or hd.Sref != SREF_SPEC:
        raise Reject("header: Sref differs from the side of the packing file")
    hd.root = need_str(x["root"], "header root")
    hd.window = parse_region(x["window"], "header window")
    hd.terminal = parse_region(x["terminal"], "header terminal")
    for i in LABELS:
        if not hd.window.alpha[i] < 1:
            raise Reject("header window alpha[%d]: SPEC 8 requires alpha < 1" % i)
        if not hd.terminal.alpha[i] <= 1:
            raise Reject("header terminal alpha[%d]: SPEC 8 requires alpha <= 1" % i)
    return hd


# ======================================================================================================
# F. node geometry: store-independent polynomials (SPEC 2, 3, 4.1, 4.5, 4.6)
# ======================================================================================================

class NodeGeom(object):
    """Everything that depends only on the node's centres and custom forms (fixed for the node)."""

    def __init__(self, ref, node):
        self.ref = ref
        self.node = node
        self.abar, self.bbar = {}, {}
        for i in LABELS:
            self.abar[i] = rot_mul(node.centre[i], ref.u[i])      # SPEC 2: abar_i := rho_i * u_i
            self.bbar[i] = vec_J(self.abar[i])                    # SPEC 2: bbar_i := J abar_i
        self._form_cache = {}
        self._combo_cache = {}

    # ---- SPEC 1 / 2 -----------------------------------------------------------------------------------
    def q_poly(self, i):
        """SPEC 1: q_i = p_i + xi_i1 e_i1 + xi_i2 e_i2; returns the two coordinate polynomials."""
        p, (e1, e2) = self.ref.p[i], self.ref.e[i]
        x1, x2 = p_var(VAR_XI[(i, 1)]), p_var(VAR_XI[(i, 2)])
        return tuple(p_lin((1, p_const(p[c])), (e1[c], x1), (e2[c], x2)) for c in (0, 1))

    def corner_offset(self, i, e1, e2):
        """SPEC 2: w := (e1 abar_i + e2 bbar_i)/2, the node-centre corner offset."""
        a, b = self.abar[i], self.bbar[i]
        return ((e1 * a[0] + e2 * b[0]) / 2, (e1 * a[1] + e2 * b[1]) / 2)

    def nbar(self, o, axis, eps):
        """SPEC 4.5: nbar := eps * abar_o (axis a) or eps * bbar_o (axis b)."""
        return vec_scale(eps, self.abar[o] if axis == "a" else self.bbar[o])

    # ---- SPEC 3: named forms --------------------------------------------------------------------------
    def class_combo(self, form):
        """SPEC 4.6, dictionary: a class form as a list of (coefficient, built-in form)."""
        if form in self._combo_cache:
            return self._combo_cache[form]
        kind, i, j, K = form
        axis_i, eps_i, axis_j, eps_j = cls_parts(K)
        nbar_i = self.nbar(i, axis_i, eps_i)
        nbar_j = self.nbar(j, axis_j, eps_j)
        cbar = vec_dot(nbar_i, nbar_j)                   # cbar := nbar_i . nbar_j
        sbar = vec_dot(vec_J(nbar_i), nbar_j)            # sbar := (J nbar_i) . nbar_j
        Cr, Sr = ("Cr", i, j), ("Sr", i, j)
        if kind == "co":
            combo = [(cbar, Cr), (-sbar, Sr)]            # co = cbar*Cr - sbar*Sr
        elif kind == "si":
            combo = [(sbar, Cr), (cbar, Sr)]             # si = sbar*Cr + cbar*Sr
        elif kind == "al":
            combo = [(Fraction(eps_i), ("A", i, j))] if axis_i == "a" else [(Fraction(eps_i), ("B", i, j))]
        elif kind == "be":
            combo = [(Fraction(-eps_j), ("A", j, i))] if axis_j == "a" else [(Fraction(-eps_j), ("B", j, i))]
        elif kind == "Y":
            # J n_i . d = eps_i*B_ij (axis a) | -eps_i*A_ij (axis b)
            first = (Fraction(eps_i), ("B", i, j)) if axis_i == "a" else (Fraction(-eps_i), ("A", i, j))
            # J n_j . d = -eps_j*B_ji (axis a) | +eps_j*A_ji (axis b)
            second = (Fraction(-eps_j), ("B", j, i)) if axis_j == "a" else (Fraction(eps_j), ("A", j, i))
            combo = [first, second]
        else:
            raise Reject("internal: not a class form")
        self._combo_cache[form] = combo
        return combo

    def form_poly(self, form):
        """SPEC 3: the polynomial of a named form."""
        if form in self._form_cache:
            return self._form_cache[form]
        kind = form[0]
        if kind == "0":
            p = {}
        elif kind == "xi":
            p = p_var(VAR_XI[(form[1], form[2])])
        elif kind == "S":
            p = p_var(VAR_S)
        elif kind == "C":
            p = p_var(VAR_C[form[1]])
        elif kind == "s":
            p = p_var(VAR_s[form[1]])
        elif kind in ("Da", "Db"):
            o, t = form[1], form[2]
            if o == t:
                raise Reject("internal: Da/Db need two different labels")
            n = self.abar[o] if kind == "Da" else self.bbar[o]      # Da := abar_o.(q_t - q_o), Db := bbar_o.(..)
            qo, qt = self.q_poly(o), self.q_poly(t)
            p = p_lin((n[0], p_sub(qt[0], qo[0])), (n[1], p_sub(qt[1], qo[1])))
        elif kind in ("A", "B"):
            o, t = form[1], form[2]
            Da, Db = self.form_poly(("Da", o, t)), self.form_poly(("Db", o, t))
            C, s = p_var(VAR_C[o]), p_var(VAR_s[o])
            if kind == "A":
                p = p_add(p_mul(C, Da), p_mul(s, Db))               # A := C_o*Da + s_o*Db
            else:
                p = p_sub(p_mul(C, Db), p_mul(s, Da))               # B := C_o*Db - s_o*Da
        elif kind in ("Cr", "Sr"):
            i, j = form[1], form[2]
            if not i < j:
                raise Reject("internal: Cr/Sr need i < j")
            Ci, si, Cj, sj = p_var(VAR_C[i]), p_var(VAR_s[i]), p_var(VAR_C[j]), p_var(VAR_s[j])
            if kind == "Cr":
                p = p_add(p_mul(Ci, Cj), p_mul(si, sj))             # Cr := C_i C_j + s_i s_j
            else:
                p = p_sub(p_mul(Ci, sj), p_mul(si, Cj))             # Sr := C_i s_j - s_i C_j
        elif kind in CLASS_FORMS:
            p = p_lin(*[(c, self.form_poly(f)) for (c, f) in self.class_combo(form)])
        elif kind == "u":
            p = p_lin(*[(c, self.form_poly(f)) for (c, f) in self.node.forms[form[1]]])
        else:
            raise Reject("internal: unknown form kind %r" % (kind,))
        self._form_cache[form] = p
        return p

    # ---- SPEC 4.1: walls ------------------------------------------------------------------------------
    def wall_poly(self, i, e1, e2, coord, side):
        """SPEC 4.1: X := (q_i + C_i w + s_i J w)_k;  wall..lo := X,  wall..hi := S - X."""
        k = 0 if coord == "x" else 1
        w = self.corner_offset(i, e1, e2)
        Jw = vec_J(w)
        X = p_lin((1, self.q_poly(i)[k]), (w[k], p_var(VAR_C[i])), (Jw[k], p_var(VAR_s[i])))
        return X if side == "lo" else p_sub(p_var(VAR_S), X)

    # ---- SPEC 4.5: option facts -----------------------------------------------------------------------
    def opt_poly(self, o, t, axis, eps, e1, e2):
        """SPEC 4.5: eps*(A_ot | B_ot) + (nbar.w) cos(psi_t - psi_o) + (nbar.Jw) sin(psi_t - psi_o) - 1/2,
        with cos = Cr_ij and sin = +Sr_ij for (o,t) = (i,j), -Sr_ij for (o,t) = (j,i)   (SPEC 3)."""
        if o == t:
            raise Reject("internal: an option needs two different labels")
        w = self.corner_offset(t, e1, e2)
        nbar = self.nbar(o, axis, eps)
        i, j = (o, t) if o < t else (t, o)
        sin_sign = 1 if (o, t) == (i, j) else -1
        base = self.form_poly(("A" if axis == "a" else "B", o, t))
        return p_lin((eps, base),
                     (vec_dot(nbar, w), self.form_poly(("Cr", i, j))),
                     (sin_sign * vec_dot(nbar, vec_J(w)), self.form_poly(("Sr", i, j))),
                     (1, p_const(-HALF)))

    # ---- SPEC 4.6: parallel class facts ---------------------------------------------------------------
    def par_poly(self, i, j, K, kind, idx, kappa, ps=None):
        """SPEC 4.6, 'Facts': the polynomial par:i:j:K:kind:idx (kappa only for Pk;
        [SPEC 2.5] ps = (cp, cm) only for Ps)."""
        al, be = self.form_poly(("al", i, j, K)), self.form_poly(("be", i, j, K))
        co, si = self.form_poly(("co", i, j, K)), self.form_poly(("si", i, j, K))
        one = p_const(1)
        if kind == "Ps":                     # [SPEC 2.5] KIND "Ps"
            cp, cm = ps
            if idx == 1:                     # al + be - 2 - cp*si
                return p_lin((1, al), (1, be), (-2, one), (-cp, si))
            if idx == 2:                     # al + be - 2 + cm*si
                return p_lin((1, al), (1, be), (-2, one), (cm, si))
            raise Reject("internal: unknown par fact")
        if kind == "P+" and idx == 1:        # be - (1 + co + si)/2
            return p_lin((1, be), (-HALF, one), (-HALF, co), (-HALF, si))
        if kind == "P+" and idx == 2:        # al - (1 + co - si)/2
            return p_lin((1, al), (-HALF, one), (-HALF, co), (HALF, si))
        if kind == "P-" and idx == 1:        # al - (1 + co + si)/2
            return p_lin((1, al), (-HALF, one), (-HALF, co), (-HALF, si))
        if kind == "P-" and idx == 2:        # be - (1 + co - si)/2
            return p_lin((1, be), (-HALF, one), (-HALF, co), (HALF, si))
        if kind == "Pk" and idx == 1:        # al + be - 1 - co - kappa*si
            return p_lin((1, al), (1, be), (-1, one), (-1, co), (-kappa, si))
        if kind == "Pk" and idx == 2:        # al + be - 1 - co + kappa*si
            return p_lin((1, al), (1, be), (-1, one), (-1, co), (kappa, si))
        raise Reject("internal: unknown par fact")

    # ---- [SPEC 2.5] SPEC 4.6, KIND "Ps": the rotation (cbar, sbar) of a class ---------------------------
    def class_frame(self, i, j, K):
        """SPEC 4.6: (cbar, sbar) with cbar := nbar_i . nbar_j, sbar := (J nbar_i) . nbar_j
        (a rational unit vector: the rotation from nbar_i to nbar_j)."""
        axis_i, eps_i, axis_j, eps_j = cls_parts(K)
        nbar_i = self.nbar(i, axis_i, eps_i)
        nbar_j = self.nbar(j, axis_j, eps_j)
        return (vec_dot(nbar_i, nbar_j), vec_dot(vec_J(nbar_i), nbar_j))

    # ---- [SPEC 2.5] SPEC 4.8: wall support facts -------------------------------------------------------
    def wsup_poly(self, i, wall, sign, kp, km):
        """SPEC 4.8: wsup:i:W:p := D_W - 1/2 - (kp/2)*sigma,  wsup:i:W:m := D_W - 1/2 + (km/2)*sigma,
        sigma := C_i*abar_i,y + s_i*bbar_i,y (the y-component of a_i),
        D_W := q_i,x | q_i,y | S - q_i,x | S - q_i,y  for W = xlo | ylo | xhi | yhi."""
        qx, qy = self.q_poly(i)
        S = p_var(VAR_S)
        if wall == "xlo":
            D = qx
        elif wall == "ylo":
            D = qy
        elif wall == "xhi":
            D = p_sub(S, qx)
        elif wall == "yhi":
            D = p_sub(S, qy)
        else:
            raise Reject("internal: unknown wall name")
        sigma = p_lin((self.abar[i][1], p_var(VAR_C[i])), (self.bbar[i][1], p_var(VAR_s[i])))
        if sign == 1:
            return p_lin((1, D), (-HALF, p_const(1)), (-kp / 2, sigma))
        if sign == -1:
            return p_lin((1, D), (-HALF, p_const(1)), (km / 2, sigma))
        raise Reject("internal: unknown wsup sign")


# ======================================================================================================
# G. the bound store: store bounds SB, effective relative arcs, EMPTY test (SPEC 2, 3, 4.3)
# ======================================================================================================

class _EmptyBound(Exception):
    """Internal signal: a 'cap cut' intersection (or an effective relative arc) is empty (SPEC 2, 3)."""


def initial_store(node):
    """SPEC 2: the initial store is the node's data with no relative-arc entries and no cuts."""
    st = StoreData()
    st.S = node.S
    st.box = dict(node.box)
    st.arc = dict(node.arc)
    st.rarc = {}
    st.cuts = {}
    return st


def arc_cos_range(Pm, Pp):
    """SPEC 3: [min(cos P^-, cos P^+), cmax], cmax := 1 if sin P^- <= 0 <= sin P^+, else the larger cosine."""
    cmax = ONE if (Pm[1] <= 0 <= Pp[1]) else max(Pm[0], Pp[0])
    return (min(Pm[0], Pp[0]), cmax)


class StoreEnv(object):
    """Everything the SPEC computes 'from a given store' of a node: SB (3), effective relative-arc
    endpoints (4.3), the EMPTY test (2, 3), the exclusion test (4.7)."""

    def __init__(self, geom, store):
        self.geom = geom
        self.store = store
        self._sb = {}
        self._eff = {}
        self._excl = {}

    # ---- SPEC 4.3 ---------------------------------------------------------------------------------------
    def effective(self, i, j):
        """SPEC 4.3: effective endpoints (R^-, R^+) of the pair i < j; an entry is None if that side has no
        candidate with positive cosine.  D^- := P_j^- * conj(P_i^+),  D^+ := P_j^+ * conj(P_i^-)."""
        if not i < j:
            raise Reject("internal: effective() needs i < j")
        key = (i, j)
        if key in self._eff:
            return self._eff[key]
        Pi_m, Pi_p = self.store.arc[i]
        Pj_m, Pj_p = self.store.arc[j]
        D_m = rot_mul(Pj_m, rot_conj(Pi_p))
        D_p = rot_mul(Pj_p, rot_conj(Pi_m))
        St_m, St_p = self.store.rarc.get(key, (None, None))
        cand_m = [X for X in (D_m, St_m) if X is not None and X[0] > 0]
        cand_p = [X for X in (D_p, St_p) if X is not None and X[0] > 0]
        R_m = max(cand_m, key=lambda X: X[1]) if cand_m else None      # the larger sine
        R_p = min(cand_p, key=lambda X: X[1]) if cand_p else None      # the smaller sine
        self._eff[key] = (R_m, R_p)
        return (R_m, R_p)

    # ---- [SPEC 2.5] SPEC 4.8: sign conditions and slopes of the wall support facts ------------------------
    def wsup_coefficients(self, i):
        """SPEC 4.8: V^- := P_i^- * abar_i, V^+ := P_i^+ * abar_i: the direction a_i ITSELF at the two ends
        of the store arc (NOT the rotations Ab^± = rho_i * P_i^± of section 8; V^± = Ab^± * u_i).
        Returns None unless  V^-_x > 0,  V^+_x > 0,  V^-_y <= 0 <= V^+_y  (then there are no wsup facts);
        else (kp, km) with
        kp := (V^+_x + V^+_y - 1)/V^+_y if V^+_y > 0, else 0;  km := (V^-_x - V^-_y - 1)/(-V^-_y) if V^-_y < 0, else 0."""
        Pm, Pp = self.store.arc[i]
        V_m = rot_mul(Pm, self.geom.abar[i])
        V_p = rot_mul(Pp, self.geom.abar[i])
        if not (V_m[0] > 0 and V_p[0] > 0 and V_m[1] <= 0 <= V_p[1]):
            return None
        kp = (V_p[0] + V_p[1] - 1) / V_p[1] if V_p[1] > 0 else ZERO
        km = (V_m[0] - V_m[1] - 1) / (-V_m[1]) if V_m[1] < 0 else ZERO
        return (kp, km)

    # ---- [SPEC 2.5] SPEC 4.6, KIND "Ps": the ends of the class angle and the slopes kp, km -----------------
    def ps_slopes(self, i, j, K):
        """SPEC 4.6, KIND "Ps": needs effective endpoints R^-, R^+ on both sides (4.3); with
        E^- := (cbar, sbar) * R^-, E^+ := (cbar, sbar) * R^+ :  cos E^- > 0, cos E^+ > 0, sin E^- <= 0 <= sin E^+.
        Returns a text (the first condition that fails) or the pair (kp, km) with
        kp := (cos E^+ + sin E^+ - 1)/sin E^+ if sin E^+ > 0, else 1;
        km := (cos E^- - sin E^- - 1)/(-sin E^-) if sin E^- < 0, else 1."""
        R_m, R_p = self.effective(i, j)
        if R_m is None or R_p is None:
            return "the pair has no effective relative-arc endpoints on both sides"
        frame = self.geom.class_frame(i, j, K)
        E_m = rot_mul(frame, R_m)
        E_p = rot_mul(frame, R_p)
        if not (E_m[0] > 0 and E_p[0] > 0):
            return "cos E^- > 0 and cos E^+ > 0 fails"
        if not (E_m[1] <= 0 <= E_p[1]):
            return "sin E^- <= 0 <= sin E^+ fails"
        kp = (E_p[0] + E_p[1] - 1) / E_p[1] if E_p[1] > 0 else ONE
        km = (E_m[0] - E_m[1] - 1) / (-E_m[1]) if E_m[1] < 0 else ONE
        return (kp, km)

    # ---- SPEC 3: store bounds ---------------------------------------------------------------------------
    def base_interval(self, v):
        """SPEC 3: SB of the base variable number v (cuts are NOT used for base variables)."""
        return self.sb(VAR_FORMS[v])

    def affine_range(self, poly):
        """SPEC 4.0: for F = c0 + sum c_ik xi_ik (like terms combined):
        IAlo := c0 + sum min(c lo, c hi),  IAhi := c0 + sum max(c lo, c hi)  over the store box (no cuts)."""
        if not p_is_affine_in_xi(poly):
            raise Reject("internal: affine_range of a non-affine polynomial")
        lo = hi = poly.get((), ZERO)
        for m, c in poly.items():
            if m == ():
                continue
            blo, bhi = self.base_interval(m[0])
            lo += min(c * blo, c * bhi)
            hi += max(c * blo, c * bhi)
        return (lo, hi)

    def _cap(self, form, iv):
        """SPEC 3, 'cap cut': intersect with the cuts stored under exactly this name."""
        lo, hi = iv
        v = self.store.cuts.get((form, "lo"))
        if v is not None and v > lo:
            lo = v
        w = self.store.cuts.get((form, "hi"))
        if w is not None and w < hi:
            hi = w
        if lo > hi:
            raise _EmptyBound(form_name(form))
        return (lo, hi)

    def _combo_interval(self, combo):
        """sum_m coef_m * SB(F_m) by interval arithmetic."""
        acc = (ZERO, ZERO)
        for c, f in combo:
            acc = iv_add(acc, iv_scale(c, self.sb(f)))
        return acc

    def sb(self, form):
        """SPEC 3, STORE BOUNDS: the interval SB(form) for this store, by exactly the listed rules.
        Raises _EmptyBound if a 'cap cut' intersection is empty (the store is then EMPTY)."""
        if form in self._sb:
            return self._sb[form]
        st = self.store
        kind = form[0]
        if kind == "xi":
            iv = st.box[(form[1], form[2])]                    # the store box; no cut
        elif kind == "S":
            iv = st.S                                          # the store side interval; no cut
        elif kind == "s":
            Pm, Pp = st.arc[form[1]]
            iv = (Pm[1], Pp[1])                                # [sin P^-, sin P^+]; no cut
        elif kind == "C":
            iv = arc_cos_range(*st.arc[form[1]])               # no cut
        elif kind in ("Da", "Db"):
            iv = self._cap(form, self.affine_range(self.geom.form_poly(form)))
        elif kind == "A":
            o, t = form[1], form[2]
            iv = iv_add(iv_mul(self.sb(("C", o)), self.sb(("Da", o, t))),
                        iv_mul(self.sb(("s", o)), self.sb(("Db", o, t))))
            iv = self._cap(form, iv)
        elif kind == "B":
            o, t = form[1], form[2]
            iv = iv_sub(iv_mul(self.sb(("C", o)), self.sb(("Db", o, t))),
                        iv_mul(self.sb(("s", o)), self.sb(("Da", o, t))))
            iv = self._cap(form, iv)
        elif kind in ("Cr", "Sr"):
            R_m, R_p = self.effective(form[1], form[2])
            if R_m is not None and R_p is not None:
                if R_m[1] > R_p[1]:
                    raise _EmptyBound("relative arc %d-%d" % (form[1], form[2]))
                iv = (R_m[1], R_p[1]) if kind == "Sr" else arc_cos_range(R_m, R_p)
            else:
                iv = (-ONE, ONE)
            iv = self._cap(form, iv)
        elif kind in CLASS_FORMS:
            iv = self._cap(form, self._combo_interval(self.geom.class_combo(form)))
        elif kind == "u":
            iv = self._cap(form, self._combo_interval(self.geom.node.forms[form[1]]))
        else:
            raise Reject("internal: no store bound for form %s" % form_name(form))
        if iv[0] > iv[1]:
            raise _EmptyBound(form_name(form))
        self._sb[form] = iv
        return iv

    # ---- SPEC 2 + 3: the EMPTY test ---------------------------------------------------------------------
    def empty_reason(self):
        """SPEC 2 and the last paragraph of SPEC 3 (STORE BOUNDS): returns None if the store is not EMPTY,
        else a text naming the contradiction.  Covers: box, side interval, arcs, cut pairs, every pair with
        a stored relative-arc endpoint and effective endpoints on both sides, and every form with a cut
        (base variables excepted: empty intersection in its SB)."""
        st = self.store
        for (i, k) in sorted(st.box):
            if st.box[(i, k)][0] > st.box[(i, k)][1]:
                return "box interval of xi:%d:%d has lo > hi" % (i, k)
        if st.S[0] > st.S[1]:
            return "side interval has S_lo > S_hi"
        for i in LABELS:
            if st.arc[i][0][1] > st.arc[i][1][1]:
                return "arc of square %d has sin P^- > sin P^+" % i
        for (form, side) in sorted(st.cuts, key=repr):
            if side == "lo" and (form, "hi") in st.cuts and st.cuts[(form, "lo")] > st.cuts[(form, "hi")]:
                return "cut pair of %s has v > w" % form_name(form)
        for (i, j) in sorted(st.rarc):
            if st.rarc[(i, j)] == (None, None):
                continue
            R_m, R_p = self.effective(i, j)
            if R_m is not None and R_p is not None and R_m[1] > R_p[1]:
                return "effective relative arc of the pair %d-%d has sin R^- > sin R^+" % (i, j)
        for form in sorted(set(f for (f, _side) in st.cuts), key=repr):
            if form[0] in BASE_FORM_KINDS:
                continue
            try:
                self.sb(form)
            except _EmptyBound as exc:
                return "empty intersection in the store bound of %s" % (exc,)
        return None

    # ---- SPEC 4.7: exclusion of an option ----------------------------------------------------------------
    def h_lo(self, o, t, axis, eps):
        """SPEC 4.7: the lower bound h_lo of h = (|n.a_t| + |n.b_t|)/2."""
        i, j = (o, t) if o < t else (t, o)
        R_m, R_p = self.effective(i, j)
        if R_m is None or R_p is None:
            return HALF                                           # no effective relative arc
        if (o, t) == (i, j):
            Q_m, Q_p = R_m, R_p
        else:
            Q_m, Q_p = rot_conj(R_p), rot_conj(R_m)
        Ebar = rot_mul(self.geom.abar[t], rot_conj(self.geom.nbar(o, axis, eps)))   # abar_t * conj(nbar)
        E_m = rot_mul(Ebar, Q_m)
        E_p = rot_mul(Ebar, Q_p)
        turn = rot_mul(E_p, rot_conj(E_m))                                           # E^+ * conj(E^-)
        if E_m[0] * E_p[0] >= 0 and E_m[1] * E_p[1] >= 0 and turn[0] > 0 and turn[1] >= 0:
            return min(abs(E_m[0]) + abs(E_m[1]), abs(E_p[0]) + abs(E_p[1])) / 2
        return HALF

    def excluded(self, opt):
        """SPEC 4.7: option (o, t, axis, eps) is EXCLUDED on this store iff U < 1/2 + h_lo STRICTLY,
        U := SBhi(A_ot | B_ot) for eps = +1,  U := -SBlo(A_ot | B_ot) for eps = -1."""
        if opt in self._excl:
            return self._excl[opt]
        o, t, axis, eps = opt
        if o == t or o not in LABEL_SET or t not in LABEL_SET or axis not in ("a", "b") or eps not in (1, -1):
            raise Reject("internal: malformed option in the exclusion test")          # SPEC 0: a PAIR
        lo, hi = self.sb(("A" if axis == "a" else "B", o, t))
        U = hi if eps == 1 else -lo
        result = bool(U < HALF + self.h_lo(o, t, axis, eps))
        self._excl[opt] = result
        return result


# ======================================================================================================
# H. declarations and facts of a round (SPEC 4.0 - 4.7)
# ======================================================================================================

def arc_fact_poly(C, s, Pm, Pp, which):
    """SPEC 4.2 (and 4.3 with (Cr, Sr) in place of (C_i, s_i)): the polynomial of an arc fact for the
    endpoints P^- = (g^-, s^-), P^+ = (g^+, s^+);  C and s are polynomials."""
    g_m, s_m = Pm
    g_p, s_p = Pp
    if which == "slo":                                   # s - s^-
        return p_lin((1, s), (-s_m, p_const(1)))
    if which == "shi":                                   # s^+ - s
        return p_lin((s_p, p_const(1)), (-1, s))
    cmin, cmax = arc_cos_range(Pm, Pp)
    if which == "clo":                                   # C - min(g^-, g^+)
        return p_lin((1, C), (-cmin, p_const(1)))
    if which == "chi":                                   # cmax - C
        return p_lin((cmax, p_const(1)), (-1, C))
    if which == "chord":                                 # (C - g^-)(s^+ - s^-) - (s - s^-)(g^+ - g^-)
        return p_sub(p_scale(s_p - s_m, p_lin((1, C), (-g_m, p_const(1)))),
                     p_scale(g_p - g_m, p_lin((1, s), (-s_m, p_const(1)))))
    raise Reject("internal: unknown arc fact")


def tangent_fact_poly(C, s, G, H):
    """SPEC 4.2: 1 - G C - H s  for rationals with G^2 + H^2 <= 1."""
    if G * G + H * H > 1:
        raise Reject("tangent vector with G^2 + H^2 > 1")
    return p_lin((1, p_const(1)), (-G, C), (-H, s))


class RoundEnv(StoreEnv):
    """The store at the START of a round together with the node's assumptions and the declarations of
    the round: which facts are available, their polynomials, and the lower bound L of a step."""

    def __init__(self, geom, store):
        StoreEnv.__init__(self, geom, store)
        self.assumed_opt = set(a[1:] for a in geom.node.assume if a[0] == "opt")
        self.assumed_ysign = set(a[1:] for a in geom.node.assume if a[0] == "ysign")
        self.opt_available = set()             # options whose four opt facts are available
        self.par_available = {}                # (i, j, K, kind) -> kappa (None unless Pk or Ps)
        self.ps_available = {}                 # [SPEC 2.5] (i, j, K) -> (cp, cm) of a valid Ps declaration
        self._fact = {}
        self._fact_sp = {}
        self._product = {}
        self._mono = {}
        self._mono_int = {}

    # ---- SPEC 4.5 VALIDITY, SPEC 10 `pairs` ---------------------------------------------------------------
    def declare_opt(self, opt, what):
        """An `opt` declaration is valid iff the node assumes the option or the 7 other options of the
        pair are excluded (4.7) on this store.  An invalid declaration rejects (SPEC 5, REJECTION)."""
        o, t = opt[0], opt[1]
        if opt not in self.assumed_opt:
            for other in pair_options(min(o, t), max(o, t)):
                if other != opt and not self.excluded(other):
                    raise Reject("%s: opt declaration %r is neither assumed nor unique: option %r is not "
                                 "excluded" % (what, opt, other))
        self.opt_available.add(opt)

    # ---- SPEC 4.6 PRECONDITIONS --------------------------------------------------------------------------
    def par_failure(self, i, j, K, kind, kappa):
        """SPEC 4.6, PRECONDITIONS: None if they hold on this store, else the first failing condition."""
        O_i, O_j = cls_options(i, j, K)
        for other in pair_options(i, j):
            if other != O_i and other != O_j and not self.excluded(other):
                return "option %r is not excluded" % (other,)
        cL = self.sb(("co", i, j, K))[0]
        if not cL > 0:
            return "cL = SBlo(co) is not > 0"
        YL, YU = self.sb(("Y", i, j, K))
        if kind == "P+":
            if not YU <= 1 + cL:
                return "YU <= 1 + cL fails"
            if not (YL >= 0 or (i, j, K, 1) in self.assumed_ysign):
                return "neither YL >= 0 nor the sign assumption Y >= 0"
        elif kind == "P-":
            if not YL >= -(1 + cL):
                return "YL >= -(1 + cL) fails"
            if not (YU <= 0 or (i, j, K, -1) in self.assumed_ysign):
                return "neither YU <= 0 nor the sign assumption Y <= 0"
        elif kind == "Pk":
            if kappa is None:
                return "kappa missing"
            Ybar = max(abs(YL), abs(YU))
            if not (0 <= kappa <= 1 - Ybar / (1 + cL)):
                return "0 <= kappa <= 1 - Ybar/(1 + cL) fails"
        elif kind == "Ps":                                   # [SPEC 2.5] KIND "Ps"
            if kappa is None:
                return "kappa missing"
            Ybar = max(abs(YL), abs(YU))
            if not (0 <= kappa <= 1 - Ybar / (1 + cL)):      # "the kappa condition of (Pk) with the declared kappa"
                return "the kappa condition of (Pk), 0 <= kappa <= 1 - Ybar/(1 + cL), fails"
            coefficients = self.ps_coefficients(i, j, K, kappa)
            if type(coefficients) is str:
                return coefficients
        else:
            return "unknown kind"
        return None

    def ps_coefficients(self, i, j, K, kappa):
        """[SPEC 2.5] SPEC 4.6, KIND "Ps": cp := kp + kappa - 1, cm := km + kappa - 1; required cp >= 0 and
        cm >= 0.  Returns a text (the condition that fails) or the pair (cp, cm)."""
        slopes = self.ps_slopes(i, j, K)
        if type(slopes) is str:
            return slopes
        kp, km = slopes
        cp = kp + kappa - 1
        cm = km + kappa - 1
        if not (cp >= 0 and cm >= 0):
            return "cp >= 0 and cm >= 0 fails"
        return (cp, cm)

    def declare_par(self, i, j, K, kind, kappa, what):
        if (i, j, K, kind) in self.par_available:
            raise Reject("%s: second par declaration for (%d, %d, %s, %s)" % (what, i, j, K, kind))
        why = self.par_failure(i, j, K, kind, kappa)
        if why is not None:
            raise Reject("%s: par declaration (%d, %d, %s, %s): precondition fails: %s"
                         % (what, i, j, K, kind, why))
        self.par_available[(i, j, K, kind)] = kappa
        if kind == "Ps":                                     # [SPEC 2.5] keep (cp, cm) for the two facts
            self.ps_available[(i, j, K)] = self.ps_coefficients(i, j, K, kappa)

    def declare(self, decl, what):
        if decl[0] == "opt":
            self.declare_opt(decl[1:], what)
        else:
            self.declare_par(decl[1], decl[2], decl[3], decl[4], decl[5], what)

    # ---- SPEC 4: the facts of this round ------------------------------------------------------------------
    def fact_poly(self, fact, what="fact"):
        """SPEC 4.0 - 4.6: the polynomial of a fact that is AVAILABLE for this store, these assumptions and
        these declarations; a fact that is not available rejects."""
        if fact in self._fact:
            return self._fact[fact]
        geom, st = self.geom, self.store
        kind = fact[0]
        if kind == "box":                                              # 4.0
            _, i, k, side = fact
            lo, hi = st.box[(i, k)]
            x = p_var(VAR_XI[(i, k)])
            p = p_lin((1, x), (-lo, p_const(1))) if side == "lo" else p_lin((hi, p_const(1)), (-1, x))
        elif kind == "side":                                           # 4.0
            S = p_var(VAR_S)
            p = p_lin((1, S), (-st.S[0], p_const(1))) if fact[1] == "lo" else p_lin((st.S[1], p_const(1)), (-1, S))
        elif kind == "ivl":                                            # 4.0
            _, form, side = fact
            if not (form[0] in ("Da", "Db") or (form[0] == "u" and form[1] in geom.node.affine_custom)):
                raise Reject("%s: ivl fact of a form that is not affine" % what)
            F = geom.form_poly(form)
            lo, hi = self.affine_range(F)
            p = p_lin((1, F), (-lo, p_const(1))) if side == "lo" else p_lin((hi, p_const(1)), (-1, F))
        elif kind == "cut":                                            # 4.0
            _, form, side = fact
            if form == ("0",):
                raise Reject("%s: no cut on the form 0" % what)
            if (form, side) not in st.cuts:
                raise Reject("%s: the store at the start of the round has no cut %s:%s"
                             % (what, form_name(form), side))
            v = st.cuts[(form, side)]
            F = geom.form_poly(form)
            p = p_lin((1, F), (-v, p_const(1))) if side == "lo" else p_lin((v, p_const(1)), (-1, F))
        elif kind == "circ":                                           # 4.0: C_i^2 + s_i^2 - 1
            C, s = p_var(VAR_C[fact[1]]), p_var(VAR_s[fact[1]])
            p = p_lin((1, p_mul(C, C)), (1, p_mul(s, s)), (-1, p_const(1)))
        elif kind == "wall":                                           # 4.1
            p = geom.wall_poly(fact[1], fact[2], fact[3], fact[4], fact[5])
        elif kind == "arc":                                            # 4.2
            i = fact[1]
            p = arc_fact_poly(p_var(VAR_C[i]), p_var(VAR_s[i]), st.arc[i][0], st.arc[i][1], fact[2])
        elif kind == "arctan":                                         # 4.2
            i = fact[1]
            p = tangent_fact_poly(p_var(VAR_C[i]), p_var(VAR_s[i]), fact[2], fact[3])
        elif kind in ("rarc", "rarctan"):                              # 4.3
            i, j = fact[1], fact[2]
            R_m, R_p = self.effective(i, j)
            if R_m is None or R_p is None:
                raise Reject("%s: the pair %d-%d has no effective relative arc: no rarc facts" % (what, i, j))
            Cr, Sr = geom.form_poly(("Cr", i, j)), geom.form_poly(("Sr", i, j))
            if kind == "rarc":
                p = arc_fact_poly(Cr, Sr, R_m, R_p, fact[3])
            else:
                p = tangent_fact_poly(Cr, Sr, fact[3], fact[4])
        elif kind == "opt":                                            # 4.5
            if fact[1:5] not in self.opt_available:
                raise Reject("%s: option %r is not declared (or its declaration is not valid) in this round"
                             % (what, fact[1:5]))
            p = geom.opt_poly(fact[1], fact[2], fact[3], fact[4], fact[5], fact[6])
        elif kind == "par":                                            # 4.6
            _, i, j, K, pkind, idx = fact
            if (i, j, K, pkind) not in self.par_available:
                raise Reject("%s: no valid par declaration for (%d, %d, %s, %s) in this round"
                             % (what, i, j, K, pkind))
            if pkind == "Ps":                                          # [SPEC 2.5]
                p = geom.par_poly(i, j, K, pkind, idx, self.par_available[(i, j, K, pkind)],
                                  ps=self.ps_available[(i, j, K)])
            else:
                p = geom.par_poly(i, j, K, pkind, idx, self.par_available[(i, j, K, pkind)])
        elif kind == "wsup":                                           # [SPEC 2.5] 4.8: wall support facts
            _, i, wall, sign = fact
            slopes = self.wsup_coefficients(i)
            if slopes is None:
                raise Reject("%s: the store arc of square %d does not satisfy the sign conditions of SPEC 4.8: "
                             "no wsup facts" % (what, i))
            p = geom.wsup_poly(i, wall, sign, slopes[0], slopes[1])
        elif kind == "asg":                                            # 4.6: +Y (p) / -Y (m)
            _, i, j, K, sign = fact
            if (i, j, K, sign) not in self.assumed_ysign:
                raise Reject("%s: the node has no sign assumption (%d, %d, %s, %+d)" % (what, i, j, K, sign))
            p = p_scale(sign, geom.form_poly(("Y", i, j, K)))
        else:
            raise Reject("%s: unknown fact kind" % what)
        self._fact[fact] = p
        return p

    # ---- SPEC 5: STEP -------------------------------------------------------------------------------------
    def mono_interval(self, m):
        """SPEC 5: [lo_m, hi_m] := product, by interval multiplication, of the SB of the base variables of
        m, a variable of exponent e being multiplied e times; the constant monomial has [1, 1]."""
        if m in self._mono:
            return self._mono[m]
        iv = (ONE, ONE)
        for v in m:
            iv = iv_mul(iv, self.sb(VAR_FORMS[v]))
        self._mono[m] = iv
        return iv

    def _mono_interval_int(self, m):
        """The interval of mono_interval(m) written as (a, b, e): [a/e, b/e] with integers and e > 0."""
        if m in self._mono_int:
            return self._mono_int[m]
        lo, hi = self.mono_interval(m)
        e = lcm(lo.denominator, hi.denominator)
        out = (lo.numerator * (e // lo.denominator), hi.numerator * (e // hi.denominator), e)
        self._mono_int[m] = out
        return out

    def _fact_scaled(self, fact, what):
        if fact not in self._fact_sp:
            self._fact_sp[fact] = sp_from_poly(self.fact_poly(fact, what))
        return self._fact_sp[fact]

    def term_product(self, facts, what):
        """prod(facts of a term), as an integer-scaled polynomial (cached per round)."""
        key = tuple(sorted(facts, key=repr))
        if key not in self._product:
            prod = self._fact_scaled(key[0], what)
            for f in key[1:]:
                prod = sp_mul(prod, self._fact_scaled(f, what))
            self._product[key] = prod
        return self._product[key]

    def remainder(self, g, terms, what="step"):
        """SPEC 5, STEP:  Rem := g - sum_k lambda_k * prod(facts of term k), expanded exactly.
        g: polynomial {monomial: Fraction};  terms: list of (lambda, tuple of facts).
        Returns (D, R) with Rem = (1/D) * sum_m R[m] * m, D a positive integer, R[m] integers."""
        g_den, g_coef = sp_from_poly(g)
        prods = [(lam, self.term_product(facts, what)) for (lam, facts) in terms]
        D = g_den
        for lam, (den, _coef) in prods:
            D = lcm(D, lam.denominator * den)
        R = {}
        scale = D // g_den
        for m, c in g_coef.items():
            R[m] = c * scale
        for lam, (den, coef) in prods:
            scale = lam.numerator * (D // (lam.denominator * den))       # lambda/den = scale/D
            if scale == 0:
                continue
            for m, c in coef.items():
                R[m] = R.get(m, 0) - scale * c
        return D, R

    def lower_bound(self, g, terms, what="step"):
        """SPEC 5, STEP:  L := sum over the monomials m of Rem of min(r_m * lo_m, r_m * hi_m).  Exact.
        With Rem = (1/D) sum_m R_m m (D > 0) and [lo_m, hi_m] = [a_m/e_m, b_m/e_m] (e_m > 0):
        min(r_m lo_m, r_m hi_m) = min(R_m a_m, R_m b_m) / (D e_m)."""
        D, R = self.remainder(g, terms, what)
        groups = {}                               # e_m -> sum of min(R_m a_m, R_m b_m)
        for m, r in R.items():
            if r == 0:
                continue
            a, b, e = self._mono_interval_int(m)
            x, y = r * a, r * b
            groups[e] = groups.get(e, 0) + (x if x <= y else y)
        E = 1
        for e in groups:
            E = lcm(E, e)
        total = 0
        for e, v in groups.items():
            total += v * (E // e)
        L = Fraction(total, E * D)
        if OPTIONS["paranoid"]:
            L_ref = self.lower_bound_reference(g, terms, what)
            if L_ref != L:
                raise Reject("internal: fast and reference evaluation of L disagree (%s)" % what)
        return L

    def lower_bound_reference(self, g, terms, what="step"):
        """SPEC 5, STEP, literally and slowly with Fractions (used by --paranoid and by the tests)."""
        rem = dict(g)
        for lam, facts in terms:
            prod = p_const(1)
            for f in facts:
                prod = p_mul(prod, self.fact_poly(f, what))
            rem = p_sub(rem, p_scale(lam, prod))
        L = ZERO
        for m, r in rem.items():
            lo, hi = self.mono_interval(m)
            L += min(r * lo, r * hi)
        return L


# ======================================================================================================
# I. steps, rounds, store updates (SPEC 5)
# ======================================================================================================

class Certified(object):
    """Certified values of the accepted steps of one round (SPEC 5: the certified value of an accepted
    step is its `value`)."""

    def __init__(self):
        self.lower = {}        # FORM -> largest certified lower bound
        self.upper = {}        # FORM -> smallest certified upper bound

    def add(self, form, sense, value):
        if sense == "lo":
            if form not in self.lower or value > self.lower[form]:
                self.lower[form] = value
        else:
            if form not in self.upper or value < self.upper[form]:
                self.upper[form] = value

    def lower_ok(self, new, old, form):
        """new lower end is implied: new <= old, or new <= some certified lower bound of `form`."""
        return (old is not None and new <= old) or (form in self.lower and new <= self.lower[form])

    def upper_ok(self, new, old, form):
        """new upper end is implied: new >= old, or new >= some certified upper bound of `form`."""
        return (old is not None and new >= old) or (form in self.upper and new >= self.upper[form])


def check_step(env, step, what):
    """SPEC 5 STEP and SPEC 10 'step'.  Returns (L, is_zero_step); a step that is not accepted rejects.
    sense lo: g = form, accepted iff value <= L.   sense hi: g = -form, accepted iff -value <= L.
    form `0` (sense lo): accepted iff L >= value > 0."""
    g = env.geom.form_poly(step.form)
    if step.sense == "hi":
        g = p_scale(-1, g)
    for lam, facts in step.terms:
        if lam < 0 and not any(f[0] == "circ" for f in facts):
            raise Reject("%s: negative multiplier in a term without a circ fact" % what)
        if not 1 <= len(facts) <= 3:
            raise Reject("%s: a term needs 1 to 3 facts" % what)
    L = env.lower_bound(g, step.terms, what)
    if step.form == ("0",):
        if step.sense != "lo":
            raise Reject("%s: a step on the form 0 must have sense lo" % what)
        if not (L >= step.value and step.value > 0):
            raise Reject("%s: step on the form 0 not accepted: needs L >= value > 0, L = %s, value = %s"
                         % (what, _short(L), _short(step.value)))
        return L, True
    if step.sense == "lo":
        if not step.value <= L:
            raise Reject("%s: claim %s >= %s not accepted: L = %s"
                         % (what, form_name(step.form), _short(step.value), _short(L)))
    else:
        if not -step.value <= L:
            raise Reject("%s: claim %s <= %s not accepted: -L = %s"
                         % (what, form_name(step.form), _short(step.value), _short(-L)))
    return L, False


def _short(x):
    """A rational for messages: exact if short, else a decimal approximation."""
    text = num_str(x)
    return text if len(text) <= 40 else "%.12g (approx.)" % float(x)


def accept_store(env, new, cert, what):
    """SPEC 5 ROUND: the proposed store `new` is accepted entry by entry against the old store (the store
    of `env`) and the certified values `cert` of this round.  Returns the new store; any entry that is
    not implied rejects."""
    old = env.store
    out = StoreData()
    # side interval
    if not cert.lower_ok(new.S[0], old.S[0], ("S",)):
        raise Reject("%s: new S_lo is not implied" % what)
    if not cert.upper_ok(new.S[1], old.S[1], ("S",)):
        raise Reject("%s: new S_hi is not implied" % what)
    out.S = new.S
    # box
    if set(new.box) != set(old.box):
        raise Reject("%s: the proposed store must list all 32 box intervals" % what)
    for (i, k) in sorted(old.box):
        lo, hi = new.box[(i, k)]
        if not cert.lower_ok(lo, old.box[(i, k)][0], ("xi", i, k)):
            raise Reject("%s: new lower end of xi:%d:%d is not implied" % (what, i, k))
        if not cert.upper_ok(hi, old.box[(i, k)][1], ("xi", i, k)):
            raise Reject("%s: new upper end of xi:%d:%d is not implied" % (what, i, k))
    out.box = dict(new.box)
    # arcs (centres never change: a proposed store has no centre field)
    if set(new.arc) != set(old.arc):
        raise Reject("%s: the proposed store must list all 16 arcs" % what)
    for i in LABELS:
        Pm, Pp = new.arc[i]
        if not (Pm[0] > 0 and Pp[0] > 0):
            raise Reject("%s: new arc endpoint of square %d has non-positive cosine" % (what, i))
        if not cert.lower_ok(Pm[1], old.arc[i][0][1], ("s", i)):
            raise Reject("%s: new endpoint P^- of square %d is not implied" % (what, i))
        if not cert.upper_ok(Pp[1], old.arc[i][1][1], ("s", i)):
            raise Reject("%s: new endpoint P^+ of square %d is not implied" % (what, i))
    out.arc = dict(new.arc)
    # stored relative-arc endpoints
    out.rarc = {}
    for (i, j) in sorted(new.rarc):
        St_m, St_p = new.rarc[(i, j)]
        R_m, R_p = env.effective(i, j)                       # effective endpoints of the OLD store
        if St_m is not None:
            if R_m is None:
                raise Reject("%s: St^- of the pair %d-%d: the old store has no R^- on this side" % (what, i, j))
            if not St_m[0] > 0:
                raise Reject("%s: St^- of the pair %d-%d has non-positive cosine" % (what, i, j))
            if not cert.lower_ok(St_m[1], R_m[1], ("Sr", i, j)):
                raise Reject("%s: St^- of the pair %d-%d is not implied" % (what, i, j))
        if St_p is not None:
            if R_p is None:
                raise Reject("%s: St^+ of the pair %d-%d: the old store has no R^+ on this side" % (what, i, j))
            if not St_p[0] > 0:
                raise Reject("%s: St^+ of the pair %d-%d has non-positive cosine" % (what, i, j))
            if not cert.upper_ok(St_p[1], R_p[1], ("Sr", i, j)):
                raise Reject("%s: St^+ of the pair %d-%d is not implied" % (what, i, j))
        if St_m is not None or St_p is not None:
            out.rarc[(i, j)] = (St_m, St_p)
    # cuts
    out.cuts = {}
    for (form, side) in sorted(new.cuts, key=repr):
        v = new.cuts[(form, side)]
        if form == ("0",):
            raise Reject("%s: no cut on the form 0" % what)
        old_v = old.cuts.get((form, side))
        ok = cert.lower_ok(v, old_v, form) if side == "lo" else cert.upper_ok(v, old_v, form)
        if not ok:
            raise Reject("%s: cut %s:%s is not implied" % (what, form_name(form), side))
        out.cuts[(form, side)] = v
    return out


class NodeStats(object):
    __slots__ = ("rounds", "steps", "terms", "zero_steps")

    def __init__(self):
        self.rounds = self.steps = self.terms = self.zero_steps = 0


def run_round(geom, store, rd, what, stats):
    """SPEC 5 ROUND: declarations, steps and the store update of one round, all evaluated with the facts
    and store bounds of `store`, the store at the START of the round.
    Returns (new store, True iff the round contains an accepted `0` step)."""
    env = RoundEnv(geom, store)
    for idx, decl in enumerate(rd.pairs):
        env.declare(decl, "%s pairs[%d]" % (what, idx))
    cert = Certified()
    zero = False
    for idx, step in enumerate(rd.steps):
        _L, is_zero = check_step(env, step, "%s step %d" % (what, idx))
        stats.steps += 1
        stats.terms += len(step.terms)
        if is_zero:
            zero = True
            stats.zero_steps += 1
        else:
            cert.add(step.form, step.sense, step.value)
    new_store = accept_store(env, rd.store, cert, what + " store")
    stats.rounds += 1
    return new_store, zero


# ======================================================================================================
# J. closure of a node; the stand-alone node check (SPEC 6, 7, 8, 10)
# ======================================================================================================

def terminal_failure(node, final, tube):
    """SPEC 8, TERMINAL TEST for a final store and a tube: None if it passes, else the reason.
    Store box inside the tube box; for every i the absolute endpoints Ab^± := rho_i * P_i^± have
    cos > 0 and |sin Ab^±| <= alphaT_i - alphaT_i^3/6;  requires 0 < alphaT_i <= 1."""
    for (i, k) in sorted(final.box):
        lo, hi = final.box[(i, k)]
        tlo, thi = tube.box[(i, k)]
        if not (tlo <= lo and hi <= thi):
            return "store interval of xi:%d:%d is not inside the tube" % (i, k)
    for i in LABELS:
        aT = tube.alpha[i]
        if not (0 < aT <= 1):
            return "tube angle radius of square %d is not in (0, 1]" % i
        bound = aT - aT * aT * aT / 6
        for P in final.arc[i]:
            Ab = rot_mul(node.centre[i], P)
            if not Ab[0] > 0:
                return "absolute arc endpoint of square %d has non-positive cosine" % i
            if not abs(Ab[1]) <= bound:
                return "absolute arc endpoint of square %d: |sin| > alphaT - alphaT^3/6" % i
    return None


def split_failure(node, env_final):
    """SPEC 6, the conditions of a split that concern the splitting node N and its final store St only:
    box split: lo <= m <= hi;  arc split: cos M > 0 and sin P^- <= sin M <= sin P^+;
    option split: every option of the pair NOT in the list is excluded (4.7) on St."""
    how = node.close[1]
    st = env_final.store
    if how[0] == "box":
        _, i, k, m = how
        lo, hi = st.box[(i, k)]
        if not (lo <= m <= hi):
            return "box split point of xi:%d:%d is outside the final interval" % (i, k)
    elif how[0] == "arc":
        _, i, M = how
        Pm, Pp = st.arc[i]
        if not M[0] > 0:
            return "arc split rotation has non-positive cosine"
        if not (Pm[1] <= M[1] <= Pp[1]):
            return "arc split rotation of square %d is outside the final arc" % i
    elif how[0] == "opt":
        _, (i, j), opts = how
        for other in pair_options(i, j):
            if other not in opts and not env_final.excluded(other):
                return "option split of the pair %d-%d omits option %r, which is not excluded" % (i, j, other)
    elif how[0] == "ysign":
        pass
    else:
        return "unknown split type"
    return None


def store_canonical(st):
    """Canonical JSON-able form of a store (rationals in lowest terms); used for the digest."""
    return {
        "S": [num_str(st.S[0]), num_str(st.S[1])],
        "box": dict((str(i), [[num_str(st.box[(i, 1)][0]), num_str(st.box[(i, 1)][1])],
                              [num_str(st.box[(i, 2)][0]), num_str(st.box[(i, 2)][1])]]) for i in LABELS),
        "arc": dict((str(i), {"lo": rot_str(st.arc[i][0]), "hi": rot_str(st.arc[i][1])}) for i in LABELS),
        "rarc": dict(("%d-%d" % ij, {"lo": None if e[0] is None else rot_str(e[0]),
                                     "hi": None if e[1] is None else rot_str(e[1])})
                     for ij, e in st.rarc.items() if e != (None, None)),
        "cuts": dict(("%s:%s" % (form_name(f), side), num_str(v)) for (f, side), v in st.cuts.items()),
    }


def store_digest(st):
    text = json.dumps(store_canonical(st), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class NodeResult(object):
    """Result of the stand-alone check of an ACCEPTED node."""
    __slots__ = ("node", "final_store", "evaluated_rounds", "zero_step", "empty_reason", "evidence", "stats")


def check_node(node, ref, header):
    """SPEC 10, last paragraph: a node object checked alone.  Returns a NodeResult if the node is
    accepted; raises Reject otherwise.  Order of work:
      1. initial store (SPEC 2); EMPTY test at the start of every evaluated round and on the final store;
      2. rounds in order (SPEC 5); after an accepted `0` step or an EMPTY store later rounds are not
         evaluated; the final store is the store after the last evaluated round;
      3. the closure claim (SPEC 7 (a), (b); for (c) the conditions that concern this node alone)."""
    try:
        return _check_node(node, ref, header)
    except _EmptyBound as exc:
        raise Reject("node %r: internal: empty store bound outside the EMPTY test (%s)" % (node.id, exc))


def _check_node(node, ref, header):
    what = "node %r" % (node.id[:60],)
    geom = NodeGeom(ref, node)
    stats = NodeStats()
    store = initial_store(node)
    if StoreEnv(geom, store).empty_reason() is not None:
        raise Reject("%s: internal: the initial store is EMPTY" % what)     # impossible for valid node data
    zero_step = False
    empty_reason = None
    evaluated = 0
    for r, rd in enumerate(node.rounds):
        store, zero = run_round(geom, store, rd, "%s round %d" % (what, r + 1), stats)
        evaluated = r + 1
        zero_step = zero_step or zero
        empty_reason = StoreEnv(geom, store).empty_reason()
        if zero_step or empty_reason is not None:
            break                                # SPEC 5: later rounds of the node are not evaluated
    final = store
    kind = node.close[0]
    evidence = None
    if kind == "infeasible":
        pair = node.close[1]
        if pair is None:
            if zero_step:
                evidence = "0-step"
            elif empty_reason is not None:
                evidence = "empty store: " + empty_reason
            else:
                raise Reject("%s: close kind infeasible without evidence (no accepted 0 step, no EMPTY "
                             "store, no pair)" % what)
        else:
            # stricter reading: the form with "pair" must be justified by the pair itself
            if empty_reason is not None:
                raise Reject("%s: pair closure, but the final store is EMPTY (use the closure without "
                             "pair)" % what)
            i, j = pair
            if not (i < j and i in LABEL_SET and j in LABEL_SET):
                raise Reject("%s: the pair of the closure is not a pair" % what)
            env = StoreEnv(geom, final)
            for opt in pair_options(i, j):
                if not env.excluded(opt):
                    raise Reject("%s: pair closure %d-%d: option %r is not excluded on the final store"
                                 % (what, i, j, opt))
            evidence = "pair %d-%d: all 8 options excluded" % (i, j)
    else:
        if empty_reason is not None:
            raise Reject("%s: the store after round %d is EMPTY (%s): the close kind must be infeasible"
                         % (what, evaluated, empty_reason))
        if kind == "terminal":
            if header is None:
                raise Reject("%s: terminal closure cannot be checked without the header" % what)
            why = terminal_failure(node, final, header.terminal)
            if why is not None:
                raise Reject("%s: terminal test fails: %s" % (what, why))
        elif kind == "split":
            why = split_failure(node, StoreEnv(geom, final))
            if why is not None:
                raise Reject("%s: %s" % (what, why))
        else:
            raise Reject("%s: unknown close kind" % what)
    res = NodeResult()
    res.node = node
    res.final_store = final
    res.evaluated_rounds = evaluated
    res.zero_step = zero_step
    res.empty_reason = empty_reason
    res.evidence = evidence
    res.stats = stats
    return res


# ======================================================================================================
# K. tree pass (SPEC 6, 7, 8)
# ======================================================================================================

def arc_contains(rho_child, Pc_m, Pc_p, rho, A_m, A_p):
    """SPEC 6, ARC CONTAINMENT TEST: does the arc of a node with centre rho' = rho_child and endpoints
    P'^- = Pc_m, P'^+ = Pc_p contain the arc [A^-, A^+] given relative to the centre rho?
    delta := rho * conj(rho'), At^± := A^± * delta; required: cos At^- > 0, cos At^+ > 0,
    sin P'^- <= sin At^-, sin At^+ <= sin P'^+."""
    delta = rot_mul(rho, rot_conj(rho_child))
    At_m = rot_mul(A_m, delta)
    At_p = rot_mul(A_p, delta)
    return bool(At_m[0] > 0 and At_p[0] > 0 and Pc_m[1] <= At_m[1] and At_p[1] <= Pc_p[1])


def root_failure(node, header):
    """SPEC 7 ROOT CONDITIONS and SPEC 8 ROOT CONTAINS WINDOW: None if they hold, else the reason."""
    if node.id != header.root:
        return "not the root named in the header"
    if node.parent is not None:
        return "the root must have parent = null"
    if len(node.assume) != 0:
        return "the root must have an empty assumption list"
    if not node.S[0] <= 4:
        return "the root needs S_lo <= 4"
    if not node.S[1] >= header.Sref:
        return "the root needs S_hi >= Sref"
    win = header.window
    for (i, k) in sorted(node.box):
        lo, hi = node.box[(i, k)]
        wlo, whi = win.box[(i, k)]
        if not (lo <= wlo and whi <= hi):
            return "the root box does not contain the window interval of xi:%d:%d" % (i, k)
    for i in LABELS:
        alpha = win.alpha[i]
        if not (0 < alpha < 1):
            return "window angle radius of square %d is not in (0, 1)" % i
        Ab_m = rot_mul(node.centre[i], node.arc[i][0])
        Ab_p = rot_mul(node.centre[i], node.arc[i][1])
        if not (Ab_m[0] > 0 and Ab_p[0] > 0):
            return "an absolute arc endpoint of square %d of the root has non-positive cosine" % i
        if not (Ab_p[1] >= alpha and Ab_m[1] <= -alpha):
            return "the root arc of square %d does not contain the window arc" % i
    return None


class ParentInfo(object):
    """What the tree pass keeps of a split node until all its children are verified."""
    __slots__ = ("id", "assume", "centre", "final", "how", "children", "open")


class ChildInfo(object):
    """Creation data of a node (SPEC 2), kept until its parent is known."""
    __slots__ = ("id", "parent", "S", "box", "centre", "arc", "assume")


def child_failure(par, child, index):
    """SPEC 6: everything the checker verifies about child number `index` (0-based position in the
    split's `children` list) of the split node `par` with final store St = par.final:
    the assumption list, the box, the arcs (with the ARC CONTAINMENT TEST) and the side interval.
    Returns None if all hold, else the reason."""
    if child.parent != par.id:
        return "its `parent` is not the splitting node"
    how, St = par.how, par.final
    extra = ()
    split_box = split_arc = None
    if how[0] == "box":
        _, i, k, m = how
        lo, hi = St.box[(i, k)]
        split_box = ((i, k), (lo, m) if index == 0 else (m, hi))        # child 1: [lo, m]; child 2: [m, hi]
    elif how[0] == "arc":
        _, i, M = how
        Pm, Pp = St.arc[i]
        split_arc = (i, (Pm, M) if index == 0 else (M, Pp))             # child 1: [P^-, M]; child 2: [M, P^+]
    elif how[0] == "opt":
        extra = (("opt",) + tuple(how[2][index]),)                      # child l assumes Lst[l]
    elif how[0] == "ysign":
        extra = (("ysign", how[1], how[2], how[3], 1 if index == 0 else -1),)   # +1 first, then -1
    else:
        return "unknown split type"
    if tuple(child.assume) != tuple(par.assume) + extra:
        return "its `assume` list is not the parent's list followed by the split assumption"
    for (i, k) in sorted(St.box):
        lo, hi = St.box[(i, k)]
        if split_box is not None and split_box[0] == (i, k):
            lo, hi = split_box[1]
        clo, chi = child.box[(i, k)]
        if not (clo <= lo and hi <= chi):
            return "its interval of xi:%d:%d does not contain the required interval" % (i, k)
    for i in LABELS:
        A_m, A_p = St.arc[i]
        if split_arc is not None and split_arc[0] == i:
            A_m, A_p = split_arc[1]
        if not arc_contains(child.centre[i], child.arc[i][0], child.arc[i][1], par.centre[i], A_m, A_p):
            return "its arc of square %d does not contain the required arc" % i
    if not (child.S[0] <= St.S[0] and St.S[1] <= child.S[1]):
        return "its side interval does not contain the parent's final side interval"
    return None


class TreeChecker(object):
    """SPEC 7 TREE CONDITIONS and ROOT CONDITIONS, SPEC 6 child conditions.  Nodes are added one by one
    (in any order) after they were accepted stand-alone; finish() must be called at the end.
    Every (parent, child) edge is verified exactly once by child_failure()."""

    def __init__(self, header):
        self.header = header
        self.kind = {}                # id -> close kind
        self.children = {}            # id -> tuple of child ids (split nodes only)
        self.parent_of = {}           # id -> the node's `parent` field
        self.listed_in = {}           # child id -> id of the split node that lists it
        self.verified = set()         # child ids whose edge has been verified
        self.waiting_parents = {}     # id -> ParentInfo (split nodes with unverified children)
        self.waiting_children = {}    # id -> ChildInfo (nodes whose parent has not been added yet)
        self.root_checked = False

    def _verify(self, par, child):
        index = par.children.index(child.id)
        why = child_failure(par, child, index)
        if why is not None:
            raise Reject("node %r (child %d of %r): %s" % (child.id, index + 1, par.id, why))
        self.verified.add(child.id)
        par.open -= 1
        if par.open == 0:
            del self.waiting_parents[par.id]

    def add(self, res):
        node = res.node
        nid = node.id
        if nid in self.kind:
            raise Reject("node id %r occurs twice" % (nid,))                       # ids are unique
        self.kind[nid] = node.close[0]
        self.parent_of[nid] = node.parent
        if nid == self.header.root:
            why = root_failure(node, self.header)
            if why is not None:
                raise Reject("root %r: %s" % (nid, why))
            self.root_checked = True
        else:
            if node.parent is None:
                raise Reject("node %r: only the root may have parent = null" % (nid,))
            if node.parent == nid:
                raise Reject("node %r: a node cannot be its own parent" % (nid,))
            ci = ChildInfo()
            ci.id, ci.parent, ci.S, ci.box = nid, node.parent, node.S, node.box
            ci.centre, ci.arc, ci.assume = node.centre, node.arc, node.assume
            if node.parent in self.kind:
                # the parent was added before: it must be a split node that lists this node and still waits
                par = self.waiting_parents.get(node.parent)
                if par is None or nid not in par.children or nid in self.verified:
                    raise Reject("node %r: its parent %r does not list it as a child" % (nid, node.parent))
                self._verify(par, ci)
            else:
                self.waiting_children[nid] = ci
        if node.close[0] == "split":
            how, kids = node.close[1], node.close[2]
            self.children[nid] = kids
            par = ParentInfo()
            par.id, par.assume, par.centre, par.final = nid, node.assume, node.centre, res.final_store
            par.how, par.children, par.open = how, kids, len(kids)
            self.waiting_parents[nid] = par
            for cid in kids:
                if cid == self.header.root:
                    raise Reject("node %r lists the root as a child" % (nid,))
                if cid in self.listed_in:
                    raise Reject("node %r occurs in two `children` lists (%r and %r)"
                                 % (cid, self.listed_in[cid], nid))
                self.listed_in[cid] = nid
            for cid in kids:
                if cid in self.kind:                                   # the child was added before
                    ci = self.waiting_children.pop(cid, None)
                    if ci is None:
                        raise Reject("node %r: child %r does not name it as parent" % (nid, cid))
                    self._verify(par, ci)

    def finish(self):
        """The conditions that need the whole certificate (SPEC 7)."""
        root = self.header.root
        if root not in self.kind or not self.root_checked:
            raise Reject("the root %r named in the header is not in the certificate" % (root,))
        for cid, pid in sorted(self.listed_in.items()):
            if cid not in self.kind:
                raise Reject("node %r lists the child %r, which does not exist" % (pid, cid))
        if self.waiting_children:
            cid = sorted(self.waiting_children)[0]
            raise Reject("node %r: its parent %r does not exist or does not list it"
                         % (cid, self.waiting_children[cid].parent))
        if self.waiting_parents:
            pid = sorted(self.waiting_parents)[0]
            raise Reject("split node %r has children that were not verified" % (pid,))
        for nid in sorted(self.kind):
            if nid == root:
                if nid in self.listed_in:
                    raise Reject("the root occurs in a `children` list")
            elif nid not in self.listed_in or nid not in self.verified:
                raise Reject("node %r does not occur in exactly one `children` list" % (nid,))
            elif self.parent_of[nid] != self.listed_in[nid]:
                raise Reject("node %r: `parent` differs from the node that lists it" % (nid,))
        # every node is reachable from the root
        seen = set([root])
        stack = [root]
        while stack:
            cur = stack.pop()
            for cid in self.children.get(cur, ()):
                if cid in seen:
                    raise Reject("node %r is reached twice from the root" % (cid,))
                seen.add(cid)
                stack.append(cid)
        if len(seen) != len(self.kind):
            missing = sorted(set(self.kind) - seen)[0]
            raise Reject("node %r is not reachable from the root" % (missing,))


# ======================================================================================================
# L. driver and command line
# ======================================================================================================

def default_packing_path():
    """<project root>/upper-packing-certificate.json, three directories above this file."""
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, "..", "..", "..", "upper-packing-certificate.json"))


class _HashingRaw(io.RawIOBase):
    """[gzip] A raw byte stream that passes on the bytes of a file and hashes every byte it delivers, so
    that the SHA-256 reported for a compressed certificate is the hash of the file on disk."""

    def __init__(self, fh, digest):
        io.RawIOBase.__init__(self)
        self._fh = fh
        self._digest = digest

    def readable(self):
        return True

    def readinto(self, b):
        data = self._fh.read(len(b))
        n = len(data)
        b[:n] = data
        self._digest.update(data)
        return n


def _certificate_lines(fh, compressed):
    """Yields the lines of the certificate one at a time (nothing else is kept in memory).
    [gzip] Errors of the decompression reject the certificate."""
    while True:
        try:
            raw = fh.readline()
        except (OSError, EOFError, zlib.error) as exc:
            raise Reject("cannot read the %scertificate (%s: %s)"
                         % ("gzip-compressed " if compressed else "", type(exc).__name__, exc))
        if raw == b"":
            return
        yield raw


def _decode_line(raw, lineno):
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise Reject("line %d: not UTF-8" % lineno)
    text = text.rstrip("\r\n")
    if text.strip() == "":
        raise Reject("line %d: empty line (every line must be a JSON object)" % lineno)
    return text


def _describe(exc):
    """Reason text for any exception; never raises."""
    if isinstance(exc, Reject):
        return str(exc)
    return "internal error (%s: %s)" % (type(exc).__name__, str(exc)[:200])


def check_certificate(cert_path, packing_path=None, keep_going=False, only_node=None,
                      expect_packing_sha256=PINNED_PACKING_SHA256):
    """Checks a certificate file (JSON lines: header first, then one node per line).
    Returns a report dict; report["verdict"] is "PASS" only if every node is accepted and the tree
    pass succeeds (never in --node mode, where the verdict is "NODE-ACCEPTED" or "FAIL").
    expect_packing_sha256: required hash of the packing file (None: no pin)."""
    import time
    t_start = time.time()
    report = {
        "checker": CHECKER_VERSION, "spec_sha256": SPEC_SHA256,
        "mode": "full" if only_node is None else "node",
        "certificate": cert_path, "certificate_sha256": None, "packing_sha256": None, "root": None,
        "verdict": "FAIL", "reason": None, "first_failure": None,
        "counts": {"nodes": 0, "accepted": 0, "infeasible": 0, "terminal": 0, "split": 0,
                   "rounds_evaluated": 0, "steps": 0, "terms": 0, "zero_steps": 0},
        "nodes": [],
    }
    try:
        _check_certificate(report, cert_path, packing_path, keep_going, only_node, expect_packing_sha256)
    except BaseException as exc:                 # nothing may escape as an apparent success
        if isinstance(exc, (KeyboardInterrupt, SystemExit)):
            report["verdict"] = "FAIL"
            report["reason"] = "interrupted"
            raise
        report["verdict"] = "FAIL"
        if report["reason"] is None:
            report["reason"] = _describe(exc)
    report["seconds"] = round(time.time() - t_start, 3)
    return report


def _fail_node(report, node_id, lineno, exc):
    reason = _describe(exc)
    entry = {"id": node_id, "line": lineno, "accepted": False, "reason": reason}
    report["nodes"].append(entry)
    if report["first_failure"] is None:
        report["first_failure"] = {"node": node_id, "line": lineno, "reason": reason}
        report["reason"] = "node %r (line %d): %s" % (node_id, lineno, reason)


def _check_certificate(report, cert_path, packing_path, keep_going, only_node, expect_sha):
    ref = Reference(packing_path if packing_path is not None else default_packing_path())
    report["packing_sha256"] = ref.sha256
    if expect_sha is not None and ref.sha256 != expect_sha:
        raise Reject("the packing file read has SHA-256 %s, expected %s" % (ref.sha256, expect_sha))
    digest = hashlib.sha256()                    # SHA-256 of the lines read (= of the file if not compressed)
    disk_digest = hashlib.sha256()               # [gzip] SHA-256 of the compressed file on disk
    try:
        raw_fh = open(cert_path, "rb")
    except (OSError, IOError) as exc:
        raise Reject("cannot read the certificate %r (%s)" % (cert_path, exc))
    with raw_fh:
        compressed = raw_fh.read(2) == b"\x1f\x8b"          # [gzip] magic bytes of a gzip file
        raw_fh.seek(0)
        if compressed:
            hashing = _HashingRaw(raw_fh, disk_digest)
            fh = gzip.GzipFile(fileobj=io.BufferedReader(hashing, 1 << 20), mode="rb")
        else:
            fh = raw_fh
        report["compressed"] = compressed
        lines = _certificate_lines(fh, compressed)
        first = next(lines, b"")
        if first == b"":
            raise Reject("the certificate is empty")
        digest.update(first)
        header = parse_header(loads_strict(_decode_line(first, 1), "line 1 (header)"), ref)
        report["root"] = header.root
        tree = TreeChecker(header)
        ids = set()
        failed = False
        found = False
        lineno = 1
        for raw in lines:
            lineno += 1
            digest.update(raw)
            node_id = None
            try:
                text = _decode_line(raw, lineno)
                if only_node is not None and json.dumps(only_node)[1:-1] not in text \
                        and only_node not in text:
                    continue                              # cheap pre-filter; the id is compared below
                obj = loads_strict(text, "line %d" % lineno)
                raw = text = None                     # one node at a time: release the text of the line
                if type(obj) is dict and type(obj.get("id")) is str:
                    node_id = obj["id"]
                if only_node is not None and node_id != only_node:
                    continue
                if node_id is not None and node_id in ids:
                    raise Reject("node id %r occurs twice" % (node_id,))
                if node_id is not None:
                    ids.add(node_id)
                found = True
                report["counts"]["nodes"] += 1
                node = parse_node(obj, "line %d" % lineno)
                obj = None                            # ... and its JSON form
                res = check_node(node, ref, header)
                if only_node is None and not failed:
                    tree.add(res)
            except Exception as exc:
                failed = True
                _fail_node(report, node_id, lineno, exc)
                raw = text = obj = node = res = None
                if not keep_going:
                    break
                continue
            c = report["counts"]
            c["accepted"] += 1
            c[node.close[0]] += 1
            c["rounds_evaluated"] += res.evaluated_rounds
            c["steps"] += res.stats.steps
            c["terms"] += res.stats.terms
            c["zero_steps"] += res.stats.zero_steps
            report["nodes"].append({
                "id": node.id, "line": lineno, "accepted": True, "close": node.close[0],
                "evidence": res.evidence, "rounds": len(node.rounds),
                "rounds_evaluated": res.evaluated_rounds, "steps": res.stats.steps,
                "final_store_sha256": store_digest(res.final_store)})
            node = res = None                         # nothing of the node is kept except what TreeChecker holds
        if compressed and (not failed or keep_going):
            while hashing.read(1 << 20):         # [gzip] bytes after the end of the gzip stream, if any
                pass
    # the hash is complete only if the loop read the whole file (no early stop at a failure)
    complete = (not failed or keep_going)
    if compressed:                               # [gzip] certificate_sha256 is always the hash of the file on disk
        report["certificate_sha256"] = disk_digest.hexdigest() if complete else None
        report["certificate_uncompressed_sha256"] = digest.hexdigest() if complete else None
    else:
        report["certificate_sha256"] = digest.hexdigest() if complete else None
    if failed:
        return
    if only_node is not None:
        if not found:
            raise Reject("node %r not found in the certificate" % (only_node,))
        report["verdict"] = "NODE-ACCEPTED"
        return
    if report["counts"]["nodes"] == 0:
        raise Reject("the certificate has no nodes")
    tree.finish()
    report["verdict"] = "PASS"


def format_report(report):
    c = report["counts"]
    lines = []
    if report["verdict"] == "PASS":
        lines.append("PASS")
    elif report["verdict"] == "NODE-ACCEPTED":
        entry = report["nodes"][-1]
        lines.append("NODE ACCEPTED (stand-alone check of this one node only; the certificate as a whole "
                     "was not checked)")
        lines.append("node=%r close=%s final_store_sha256=%s"
                     % (entry["id"], entry["close"], entry["final_store_sha256"]))
    else:
        lines.append("FAIL")
        ff = report["first_failure"]
        if ff is not None:
            lines.append("first failing node: %r (line %s)" % (ff["node"], ff["line"]))
            lines.append("reason: %s" % ff["reason"])
        else:
            lines.append("reason: %s" % report["reason"])
        nfail = sum(1 for n in report["nodes"] if not n["accepted"])
        if nfail > 1:
            lines.append("rejected nodes: %d" % nfail)
    lines.append("nodes=%d accepted=%d infeasible=%d terminal=%d split=%d rounds_evaluated=%d steps=%d "
                 "terms=%d zero_steps=%d" % (c["nodes"], c["accepted"], c["infeasible"], c["terminal"],
                                             c["split"], c["rounds_evaluated"], c["steps"], c["terms"],
                                             c["zero_steps"]))
    lines.append("root=%r packing_sha256=%s certificate_sha256=%s"
                 % (report["root"], report["packing_sha256"], report["certificate_sha256"]))
    if report.get("compressed"):                 # [gzip]
        lines.append("gzip input: certificate_sha256 is the hash of the compressed file; uncompressed_sha256=%s"
                     % report.get("certificate_uncompressed_sha256"))
    lines.append("checker: %s; %.1f s" % (report["checker"], report.get("seconds", 0.0)))
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Exact checker for wx-cert-2 certificates (SPEC.md 2.5.1).")
    ap.add_argument("certificate", help="JSON lines: header on the first line, one node per line; "
                                        "may be gzip-compressed")
    ap.add_argument("--node", metavar="ID", help="check only this node, stand-alone (no tree pass)")
    ap.add_argument("--json", metavar="FILE", help="write a machine-readable result")
    ap.add_argument("--packing", metavar="FILE", help="packing file (default: upper-packing-certificate.json "
                                                      "of the project root)")
    ap.add_argument("--expect-packing-sha256", metavar="HEX", default=PINNED_PACKING_SHA256,
                    help="required SHA-256 of the packing file (default: the hash pinned in this program)")
    ap.add_argument("--no-packing-pin", action="store_true",
                    help="do not require a particular packing file (the header hash must still match the file)")
    ap.add_argument("--keep-going", action="store_true", help="check all nodes even after a failure")
    ap.add_argument("--paranoid", action="store_true",
                    help="recompute every step with the literal Fraction formula and compare (slow)")
    ap.add_argument("--allow-extra-keys", action="store_true",
                    help="ignore JSON keys that the SPEC does not define (default: reject)")
    args = ap.parse_args(argv)
    OPTIONS["paranoid"] = bool(args.paranoid)
    OPTIONS["allow_extra_keys"] = bool(args.allow_extra_keys)
    code = 1
    try:
        report = check_certificate(args.certificate, args.packing, args.keep_going, args.node,
                                   None if args.no_packing_pin else args.expect_packing_sha256)
        text = format_report(report)
        if args.json:
            with open(args.json, "w") as fh:
                json.dump(report, fh, indent=1, sort_keys=True)
                fh.write("\n")
        print(text)
        if report["verdict"] == "PASS" and report["mode"] == "full":
            code = 0
        elif report["verdict"] == "NODE-ACCEPTED" and report["mode"] == "node":
            code = 10
    except Exception as exc:                     # e.g. the JSON result cannot be written
        print("FAIL")
        print("reason: %s" % _describe(exc))
        code = 1
    return code


if __name__ == "__main__":
    sys.exit(main())
