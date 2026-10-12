#!/usr/bin/env node
'use strict';
/*
 * wxcheck2.js -- SECOND, independent exact checker for certificates of format "wx-cert-2" and "wx-cert-3" ([SPEC 3.0] section 10: two schema strings).
 *
 * Specification: research/window-extension-20261008/SPEC_v3.0.md, VERSION 3.0   ([SPEC 3.0]: file, version and hash of the specification)
 * (SHA-256 0a6dfc2ae10ed6f30a21ebe357a6e73dd7355223c521cc67a3f2bdab9549aba0; [SPEC 3.0]: the final text, audited and adopted.  The
 * code was written against the audited candidate, SHA-256 2cec6f72...ca908, and then compared sentence by sentence with the final text; the
 * one change of behaviour that the final text asked for is the rule on node ids in Validator.node.  The constants SPEC_NAME and SPEC_SHA256
 * near the end of this file carry the name and the hash into every --json report.)
 * Written from the specification alone (no generator code, no code of the first checker was read).
 *
 * [SPEC 3.0] This file is wxcheck2_v26.js (the frozen checker for version 2.6, SHA-256 a725c230...a723968)
 * with the changes for version 3.0.  Every changed or added place carries a comment with the mark [SPEC 3.0]
 * and the section of SPEC_v3.0.md it implements (blocks are between ">>> [SPEC 3.0]" and "<<< [SPEC 3.0]"), so
 * that `diff wxcheck2_v26.js wxcheck2_v30.js` shows exactly these places.  Version 3.0 has a second schema
 * string, "wx-cert-3".  The schema is ONE module-level selection (part C, useSchema), made when the header is
 * read and made again before every node of that certificate, like the label set.  Under "wx-cert-2" the flag
 * SCHEMA3 is false and every statement of this file that is new in 3.0 is behind that flag: such a certificate
 * takes the path of wxcheck2_v26.js, and each of the new elements is rejected where it occurs, with the message
 * of the 2.6 file (SCHEMA RULE, section 10).  Under "wx-cert-3" there are four additions:
 *   (a) arc CENTRES of the window and of the tube in the header (sections 8, 10): Validator.region, checkRoot,
 *       terminalTest;
 *   (b) polynomial forms `q:NAME` with the fact `sq:NAME` and the sign-free name `pol:NAME` (sections 3, 4.9,
 *       10): Validator.qform, parseFactName, Validator.factRef, rule (T2) in Validator.round, RoundCtx._fact3;
 *   (c) indicators for a pair (sections 3, 4.5, 4.10, 5, 10): the `ind` declaration with (R1) to (R3) in
 *       Validator.round, its precondition in RoundCtx.declare, the indicator variables of the round (variable
 *       numbers NVAR, NVAR+1, ... of that round), the name `ind:i:j:k`, the GUARD RULE (T3) in RoundCtx.checkStep;
 *   (d) the CENTRED remainder bound (section 5): Validator.stepCentre, RoundCtx.lowerBound3 with _shift3 and
 *       _bound3, and the literal second evaluation lowerBoundReference3 (option --paranoid).
 * Under "wx-cert-3" every step is evaluated by lowerBound3 (one integer coefficient map over one common
 * denominator; no floating point anywhere); under "wx-cert-2" by the unchanged lowerBound of the 2.6 file.
 * One difference to the 2.6 file holds under BOTH schemas: the option --ignore-unknown-keys (Validator option
 * ignoreUnknownKeys) is removed, because the KEYS rule of section 10 is normative in 3.0.  This file has no
 * command-line option, environment variable or mode that relaxes a rule of the SPEC; --node checks one node alone
 * and can only print NODE-OK (exit code 3, report mode "single node (no tree pass)"), never PASS.
 * Every new element is also gated at the point where its value would take effect (checkRoot, terminalTest,
 * RoundCtx.declare, RoundCtx._fact3, RoundCtx.checkStep, Validator.qform, Validator.stepCentre): if one of them
 * ever arrived there under "wx-cert-2", the result would be an internal error, which is a FAIL.
 *
 * [SPEC 2.6] This file is wxcheck2_v251.js (the frozen checker for version 2.5.1, SHA-256 149dc62d...d154c60)
 * with the changes for version 2.6, which is "2.5.1 plus two OPTIONAL header fields and nothing else":
 * `labels` (16 or 17; it fixes the label set I) and `S_floor` (the lower end of the side interval of the
 * statement; default 4).  Every changed or added place carries a comment with the mark [SPEC 2.6] and the
 * section of SPEC.md it implements (blocks are between ">>> [SPEC 2.6]" and "<<< [SPEC 2.6]"), so that
 * `diff wxcheck2_v251.js wxcheck2_v26.js` shows exactly these places.  The label set is ONE module-level
 * selection (part C, useLabels), made when the header is read and made again before every node of that
 * certificate is checked; every rule that speaks of "the labels of I" reads it from there.  A certificate
 * without the two fields is checked exactly as by wxcheck2_v251.js.
 *
 * Version 2.5 = version 2.3 plus two fact families (2.4), with the wording of the fourth audit (2.5).
 * Version 2.5.1 = 2.5 with an explicit rule for the two forms of the closure "infeasible" (section 10).
 * The checker for 2.3 is frozen as wxcheck2_v23.js; everything that 2.4/2.5 add is between the markers
 * ">>> SPEC 2.5" and "<<< SPEC 2.5" in this file (wall support facts `wsup`, SPEC 4.8; kind "Ps" of a
 * parallel class, end of SPEC 4.6), and the one change of 2.5.1 is between ">>> SPEC 2.5.1" and
 * "<<< SPEC 2.5.1" (function checkNode), so that `diff wxcheck2_v23.js wxcheck2.js` shows exactly these blocks.
 * A certificate that uses neither `wsup` facts nor kind "Ps" and has no closure of the form
 * {"kind":"infeasible","pair":[i,j]} is checked exactly as by wxcheck2_v23.js.
 * Three operational changes after the code review of the 2.3 file are between ">>> REVIEW" and "<<< REVIEW"
 * (driver only, no checking rule): F1 a node-only check prints NODE-OK and exits with code 3, never PASS/0;
 * F2 the packing file is pinned by its SHA-256 unless --no-packing-pin is given; F4 the --json report is
 * written before the verdict is printed, and a report that cannot be written makes the verdict FAIL.
 *
 * Plain Node.js (>= 18), built-in modules only.  All arithmetic that carries soundness is exact
 * (BigInt rationals).  Nothing is repaired or skipped: every violation rejects the certificate.
 *
 * Layout (each part cites the SPEC paragraph it implements):
 *   A. rejection, strict JSON parser (repeated keys)            SPEC 10 "A JSON object with a repeated key"
 *   B. exact rationals Q, intervals Iv, rotations Rot           SPEC 1, 3, 10 "Numbers"
 *   C. labels, base variables, monomials, polynomials SPoly     SPEC 0, 3
 *   D. reference data from the packing file                     SPEC 1
 *   E. names of forms and facts                                 SPEC 10 "FACT names", "Form NAMEs"
 *   F. well-formedness of header, node, round, store, split     SPEC 10 "WELL-FORMEDNESS"
 *   G. node context: centres, forms, store-independent facts    SPEC 2, 3, 4.1, 4.5, 4.6
 *   H. store view: store bounds SB, effective relative arcs,
 *      EMPTY test, exclusion of options                         SPEC 2, 3, 4.3, 4.7
 *   I. rounds: declarations, facts, steps, store update         SPEC 4, 5
 *   J. node check and closure                                   SPEC 7(a), 7(b), 8, 6 (local part)
 *   K. tree pass                                                SPEC 6, 7, 8
 *   L. driver and command line
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const zlib = require('zlib');

// ===========================================================================
// A. Rejection and strict JSON
// ===========================================================================

/** A Reject is a violation of the SPEC by the certificate.  Any other exception is an internal error
 *  and is also reported as FAIL by the driver. */
class Reject extends Error {
  constructor(reason) { super(reason); this.name = 'Reject'; }
}
function reject(reason) { throw new Reject(reason); }
function internal(msg) { throw new Error('internal error: ' + msg); }

/** A JSON number token, kept as its raw text (so that "1", "1.0" and "1e0" can be told apart). */
class JNum {
  constructor(raw) { this.raw = raw; }
}

/**
 * Strict JSON parser (RFC 8259).  Objects become Map (insertion order, no prototype traps), arrays
 * become Array, strings become string, numbers become JNum, literals become true/false/null.
 * SPEC 10: "A JSON object with a repeated key is rejected."  (JSON.parse would silently keep the last.)
 */
function parseJsonStrict(text, what) {
  const n = text.length;
  let pos = 0;
  function fail(msg) { reject(`${what}: invalid JSON at offset ${pos}: ${msg}`); }
  function ws() {
    while (pos < n) {
      const c = text.charCodeAt(pos);
      if (c === 0x20 || c === 0x0A || c === 0x0D || c === 0x09) pos++; else break;
    }
  }
  function string() {
    pos++; // opening quote
    let start = pos;
    let out = null;
    for (;;) {
      if (pos >= n) fail('unterminated string');
      const c = text.charCodeAt(pos);
      if (c === 0x22) {
        const s = out === null ? text.slice(start, pos) : out + text.slice(start, pos);
        pos++;
        return s;
      }
      if (c < 0x20) fail('control character in string');
      if (c === 0x5C) {
        out = (out === null ? '' : out) + text.slice(start, pos);
        pos++;
        if (pos >= n) fail('unterminated escape');
        const e = text.charCodeAt(pos);
        switch (e) {
          case 0x22: out += '"'; break;
          case 0x5C: out += '\\'; break;
          case 0x2F: out += '/'; break;
          case 0x62: out += '\b'; break;
          case 0x66: out += '\f'; break;
          case 0x6E: out += '\n'; break;
          case 0x72: out += '\r'; break;
          case 0x74: out += '\t'; break;
          case 0x75: {
            const hex = text.slice(pos + 1, pos + 5);
            if (!/^[0-9a-fA-F]{4}$/.test(hex)) fail('bad \\u escape');
            out += String.fromCharCode(parseInt(hex, 16));
            pos += 4;
            break;
          }
          default: fail('bad escape');
        }
        pos++;
        start = pos;
      } else pos++;
    }
  }
  function number() {
    const start = pos;
    let c;
    if (text.charCodeAt(pos) === 0x2D) pos++;
    if (pos >= n) fail('bad number');
    c = text.charCodeAt(pos);
    if (c === 0x30) pos++;
    else if (c >= 0x31 && c <= 0x39) { while (pos < n && (c = text.charCodeAt(pos)) >= 0x30 && c <= 0x39) pos++; }
    else fail('bad number');
    if (pos < n && text.charCodeAt(pos) === 0x2E) {
      pos++;
      const d0 = pos;
      while (pos < n && (c = text.charCodeAt(pos)) >= 0x30 && c <= 0x39) pos++;
      if (pos === d0) fail('bad number');
    }
    if (pos < n && ((c = text.charCodeAt(pos)) === 0x65 || c === 0x45)) {
      pos++;
      if (pos < n && ((c = text.charCodeAt(pos)) === 0x2B || c === 0x2D)) pos++;
      const d0 = pos;
      while (pos < n && (c = text.charCodeAt(pos)) >= 0x30 && c <= 0x39) pos++;
      if (pos === d0) fail('bad number');
    }
    return new JNum(text.slice(start, pos));
  }
  function object() {
    pos++; // {
    const m = new Map();
    ws();
    if (pos < n && text.charCodeAt(pos) === 0x7D) { pos++; return m; }
    for (;;) {
      ws();
      if (pos >= n || text.charCodeAt(pos) !== 0x22) fail('expected a string key');
      const k = string();
      if (m.has(k)) reject(`${what}: repeated JSON key ${JSON.stringify(k)} (offset ${pos})`);
      ws();
      if (pos >= n || text.charCodeAt(pos) !== 0x3A) fail('expected ":"');
      pos++;
      m.set(k, value());
      ws();
      if (pos >= n) fail('unterminated object');
      const c = text.charCodeAt(pos);
      if (c === 0x2C) { pos++; continue; }
      if (c === 0x7D) { pos++; return m; }
      fail('expected "," or "}"');
    }
  }
  function array() {
    pos++; // [
    const a = [];
    ws();
    if (pos < n && text.charCodeAt(pos) === 0x5D) { pos++; return a; }
    for (;;) {
      a.push(value());
      ws();
      if (pos >= n) fail('unterminated array');
      const c = text.charCodeAt(pos);
      if (c === 0x2C) { pos++; continue; }
      if (c === 0x5D) { pos++; return a; }
      fail('expected "," or "]"');
    }
  }
  function value() {
    ws();
    if (pos >= n) fail('unexpected end of input');
    const c = text.charCodeAt(pos);
    if (c === 0x7B) return object();
    if (c === 0x5B) return array();
    if (c === 0x22) return string();
    if (c === 0x2D || (c >= 0x30 && c <= 0x39)) return number();
    if (text.startsWith('true', pos)) { pos += 4; return true; }
    if (text.startsWith('false', pos)) { pos += 5; return false; }
    if (text.startsWith('null', pos)) { pos += 4; return null; }
    fail('unexpected character');
    return undefined;
  }
  const v = value();
  ws();
  if (pos !== n) fail('trailing characters after the JSON value');
  return v;
}

function decodeUtf8(bytes) {
  return new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(bytes);
}

// ===========================================================================
// B. Exact rationals, intervals, rotations
// ===========================================================================

function babs(x) { return x < 0n ? -x : x; }
/** gcd of two non-negative BigInt (Euclid). */
function bgcd(a, b) {
  while (b !== 0n) { const t = a % b; a = b; b = t; }
  return a;
}
/** lcm of two positive BigInt. */
function blcm(a, b) {
  if (a === b) return a;
  if (a % b === 0n) return a;
  if (b % a === 0n) return b;
  return a / bgcd(a, b) * b;
}

/** Exact rational n/d, always normalised: d > 0, gcd(|n|, d) = 1.  Immutable. */
class Q {
  constructor(n, d) { this.n = n; this.d = d; }
  /** n/d for arbitrary BigInt n, d (d != 0), normalised. */
  static make(n, d) {
    if (d === 0n) internal('zero denominator');
    if (d < 0n) { n = -n; d = -d; }
    if (n === 0n) return Q.ZERO;
    const g = bgcd(babs(n), d);
    return g === 1n ? new Q(n, d) : new Q(n / g, d / g);
  }
  static int(k) { return new Q(BigInt(k), 1n); }
  sign() { return this.n > 0n ? 1 : (this.n < 0n ? -1 : 0); }
  isZero() { return this.n === 0n; }
  neg() { return this.n === 0n ? this : new Q(-this.n, this.d); }
  abs() { return this.n < 0n ? new Q(-this.n, this.d) : this; }
  /** Sum (Knuth 4.5.1: gcd only of the denominators). */
  add(o) {
    if (this.n === 0n) return o;
    if (o.n === 0n) return this;
    if (this.d === o.d) {
      const n = this.n + o.n;
      if (n === 0n) return Q.ZERO;
      if (this.d === 1n) return new Q(n, 1n);
      const g = bgcd(babs(n), this.d);
      return g === 1n ? new Q(n, this.d) : new Q(n / g, this.d / g);
    }
    const g = bgcd(this.d, o.d);
    if (g === 1n) return new Q(this.n * o.d + o.n * this.d, this.d * o.d);
    const td = this.d / g;
    const t = this.n * (o.d / g) + o.n * td;
    if (t === 0n) return Q.ZERO;
    const g2 = bgcd(babs(t), g);
    return g2 === 1n ? new Q(t, td * o.d) : new Q(t / g2, td * (o.d / g2));
  }
  sub(o) { return this.add(o.neg()); }
  /** Product (cross-cancellation, so the result is normalised). */
  mul(o) {
    if (this.n === 0n || o.n === 0n) return Q.ZERO;
    if (this.d === 1n && o.d === 1n) return new Q(this.n * o.n, 1n);
    const g1 = o.d === 1n ? 1n : bgcd(babs(this.n), o.d);
    const g2 = this.d === 1n ? 1n : bgcd(babs(o.n), this.d);
    return new Q((g1 === 1n ? this.n : this.n / g1) * (g2 === 1n ? o.n : o.n / g2),
                 (g2 === 1n ? this.d : this.d / g2) * (g1 === 1n ? o.d : o.d / g1));
  }
  div(o) {
    if (o.n === 0n) internal('division by zero');
    return this.mul(o.n > 0n ? new Q(o.d, o.n) : new Q(-o.d, -o.n));
  }
  cmp(o) {
    if (this.d === o.d) return this.n < o.n ? -1 : (this.n > o.n ? 1 : 0);
    const l = this.n * o.d, r = o.n * this.d;
    return l < r ? -1 : (l > r ? 1 : 0);
  }
  eq(o) { return this.n === o.n && this.d === o.d; }
  lt(o) { return this.cmp(o) < 0; }
  le(o) { return this.cmp(o) <= 0; }
  gt(o) { return this.cmp(o) > 0; }
  ge(o) { return this.cmp(o) >= 0; }
  static min(a, b) { return a.cmp(b) <= 0 ? a : b; }
  static max(a, b) { return a.cmp(b) >= 0 ? a : b; }
  toString() { return this.d === 1n ? this.n.toString() : this.n.toString() + '/' + this.d.toString(); }
  /** Floating-point approximation (messages and tests only; never used in a decision). */
  toNumber() { return ratioToNumber(this.n, this.d); }
}
Q.ZERO = new Q(0n, 1n);
Q.ONE = new Q(1n, 1n);
Q.MONE = new Q(-1n, 1n);
Q.HALF = new Q(1n, 2n);

function ratioToNumber(n, d) {
  if (n === 0n) return 0;
  const neg = n < 0n;
  const a = neg ? -n : n;
  const la = a.toString(16).length * 4, ld = d.toString(16).length * 4;
  const sh = 64 - (la - ld);
  const q = sh >= 0 ? (a << BigInt(sh)) / d : a / (d << BigInt(-sh));
  const x = Number(q) * Math.pow(2, -sh);
  return neg ? -x : x;
}

/** SPEC 10: "Numbers are JSON strings matching -?[0-9]+ or -?[0-9]+/[0-9]+ with a nonzero denominator". */
const NUM_RE = /^-?[0-9]+(?:\/[0-9]+)?$/;
function parseNumString(s) {
  if (!NUM_RE.test(s)) return null;
  const k = s.indexOf('/');
  if (k < 0) return new Q(BigInt(s), 1n);
  const d = BigInt(s.slice(k + 1));
  if (d === 0n) return null;
  return Q.make(BigInt(s.slice(0, k)), d);
}
function parseNum(v, where) {
  if (typeof v !== 'string') {
    reject(`${where}: a number must be a JSON string "p" or "p/q"` +
           (v instanceof JNum ? ` (found the JSON number ${v.raw})` : ''));
  }
  const q = parseNumString(v);
  if (q === null) reject(`${where}: malformed number ${JSON.stringify(v)} (need -?[0-9]+ or -?[0-9]+/[0-9]+ with a nonzero denominator)`);
  return q;
}

/** Closed interval [lo, hi] of rationals (SPEC 3: "interval arithmetic with exact rationals"). */
class Iv {
  constructor(lo, hi) { this.lo = lo; this.hi = hi; }
  add(o) { return new Iv(this.lo.add(o.lo), this.hi.add(o.hi)); }
  sub(o) { return new Iv(this.lo.sub(o.hi), this.hi.sub(o.lo)); }
  neg() { return new Iv(this.hi.neg(), this.lo.neg()); }
  /** product with a rational number */
  scale(q) {
    const s = q.sign();
    if (s === 0) return IV_ZERO;
    const a = this.lo.mul(q), b = this.hi.mul(q);
    return s > 0 ? new Iv(a, b) : new Iv(b, a);
  }
  /** interval product: [min of the four products, max of the four products] */
  mul(o) {
    const a = this.lo.mul(o.lo), b = this.lo.mul(o.hi), c = this.hi.mul(o.lo), d = this.hi.mul(o.hi);
    return new Iv(Q.min(Q.min(a, b), Q.min(c, d)), Q.max(Q.max(a, b), Q.max(c, d)));
  }
  toString() { return `[${this.lo}, ${this.hi}]`; }
}
const IV_ZERO = new Iv(Q.ZERO, Q.ZERO);
const IV_ONE = new Iv(Q.ONE, Q.ONE);
const IV_UNIT = new Iv(Q.MONE, Q.ONE);

/**
 * SPEC 1: "A ROTATION is a pair (g, s) in Q^2 with g^2 + s^2 = 1.  Rotations are multiplied as complex
 * numbers g + i s; conj(g, s) := (g, -s)".  The same class holds rational unit vectors (abar_i, bbar_i).
 */
class Rot {
  constructor(g, s) { this.g = g; this.s = s; }
  mul(o) {
    return new Rot(this.g.mul(o.g).sub(this.s.mul(o.s)), this.g.mul(o.s).add(this.s.mul(o.g)));
  }
  conj() { return new Rot(this.g, this.s.neg()); }
  neg() { return new Rot(this.g.neg(), this.s.neg()); }
  /** J(x, y) := (-y, x)  (SPEC 0), i.e. multiplication by i */
  J() { return new Rot(this.s.neg(), this.g); }
  isUnit() { return this.g.mul(this.g).add(this.s.mul(this.s)).eq(Q.ONE); }
  eq(o) { return this.g.eq(o.g) && this.s.eq(o.s); }
  toString() { return `(${this.g}, ${this.s})`; }
}
Rot.ID = new Rot(Q.ONE, Q.ZERO);

/** cmax of SPEC 3 / 4.2: 1 if sin P^- <= 0 <= sin P^+, else the larger cosine. */
function cmaxOf(Pm, Pp) {
  if (Pm.s.sign() <= 0 && Pp.s.sign() >= 0) return Q.ONE;
  return Q.max(Pm.g, Pp.g);
}

// ===========================================================================
// C. Labels, base variables, monomials, polynomials
// ===========================================================================

// >>> [SPEC 2.6] sections 0 and 10 (the label set I is fixed by the header) and section 3 (base variables of I).
//     SPEC 0: "the LABEL SET I of a certificate is fixed by its header (section 10): I = {1,...,17} minus {4}
//     (sixteen labels; the default, and the only case before version 2.6) or I = {1,...,17} (header field
//     `labels` = 17). ... Everything below is written for an arbitrary label set I; "16 labels" in a format rule
//     means "the labels of I"."
//     Both label sets are constants (LABEL_SETS).  The names LABELS, NL, LIDX, LABEL_KEYS, LABEL_KEY_SET and the
//     variable numbering NVAR, V_S, V_C, V_SN, which the whole file uses, are bound to ONE of the two sets by
//     useLabels(n).  useLabels is called (1) here with 16 (SPEC 10: "absent means 16"), (2) by Validator.header
//     with the value of the header, before any map keyed by labels is read, and (3) by CertChecker.checkNodeText
//     before every node, with the value of that certificate's header; a node is checked synchronously, so one
//     certificate is never checked with the label set of another.  Version 2.5.1 had the sixteen-label values as
//     constants: LABELS = [1,2,3,5,...,17], NL = 16, NVAR = 65, V_S = 32, V_C(li) = 33 + li, V_SN(li) = 49 + li;
//     for sixteen labels the values below are the same numbers.
function makeLabelSet(labels, text) {
  const n = labels.length;
  const keys = labels.map(String);
  return Object.freeze({
    LABELS: Object.freeze(labels), NL: n, LIDX: new Map(labels.map((l, k) => [l, k])),
    LABEL_KEYS: Object.freeze(keys), LABEL_KEY_SET: new Set(keys), LABEL_TEXT: text,
    // SPEC 3: "BASE VARIABLES: xi_ik (32), S, C_i, s_i (32)" (the numbers of sixteen labels); for a label set
    // of n labels: xi_ik has the numbers 0 .. 2n-1, S the number 2n, C_i 2n+1 .. 3n, s_i 3n+1 .. 4n.
    NVAR: 4 * n + 1, V_S: 2 * n, V_C0: 2 * n + 1, V_SN0: 3 * n + 1,
  });
}
const LABEL_SETS = Object.freeze({
  16: makeLabelSet([1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], 'I = {1,...,17} minus {4}'),
  17: makeLabelSet([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], 'I = {1,...,17}'),
});
let LABELS, NL, LIDX, LABEL_KEYS, LABEL_KEY_SET, LABEL_TEXT;
let NVAR, V_S, V_C0, V_SN0;
/** Select the label set of n labels; n must be the number 16 or 17 (anything else is an internal error). */
function useLabels(n) {
  if (n !== 16 && n !== 17) internal('useLabels: the number of labels must be 16 or 17');
  ({ LABELS, NL, LIDX, LABEL_KEYS, LABEL_KEY_SET, LABEL_TEXT, NVAR, V_S, V_C0, V_SN0 } = LABEL_SETS[n]);
}
useLabels(16);
const LABEL_RE = /^[1-9][0-9]*$/;

/** Variable numbers 0 .. NVAR-1 (li = index of a label in LABELS). */
function V_XI(li, k) { return 2 * li + (k - 1); } // k in {1, 2}
function V_C(li) { return V_C0 + li; }
function V_SN(li) { return V_SN0 + li; }
// <<< [SPEC 2.6]
// >>> [SPEC 3.0] "THE TWO SCHEMAS" and section 10, SCHEMA RULE: "A certificate names its schema in its header:
//     "wx-cert-2" or "wx-cert-3" ...  A passage, item or sentence marked (wx-cert-3) applies only to certificates
//     with the schema "wx-cert-3"; for a certificate with the schema "wx-cert-2" it does not exist, and the element
//     it introduces is rejected there".
//     SCHEMA3 is true iff the certificate being read or checked has the schema "wx-cert-3".  useSchema is called
//     (1) by Validator.header, as soon as the schema string has been tested and before anything else of the header
//     is read, and (2) by CertChecker.checkNodeText before every node, with the value of that certificate's header
//     (a node is read and checked synchronously).  It is false when the file is loaded.  Every rule of version 3.0
//     in this file is behind this flag.
//     Section 3, INDICATOR VARIABLES: "In a round of a node there are, besides the base variables, the INDICATOR
//     VARIABLES of that round".  They get the variable numbers NVAR, NVAR + 1, ... of that round (RoundCtx.declare),
//     so that a monomial of an extended polynomial is, as before, the sorted string of its variable numbers.
let SCHEMA3 = false;
/** Select the schema: true for "wx-cert-3", false for "wx-cert-2" (anything else is an internal error). */
function useSchema(is3) {
  if (is3 !== true && is3 !== false) internal('useSchema: the argument must be true or false');
  SCHEMA3 = is3;
}
// <<< [SPEC 3.0]
/** A monomial is the string of its variables (with multiplicity), sorted; '' is the constant monomial 1. */
function MCH(v) { return String.fromCharCode(48 + v); }
function monMul(a, b) {
  const la = a.length, lb = b.length;
  if (la === 0) return b;
  if (lb === 0) return a;
  if (a.charCodeAt(la - 1) <= b.charCodeAt(0)) return a + b;
  if (b.charCodeAt(lb - 1) <= a.charCodeAt(0)) return b + a;
  let i = 0, j = 0, out = '';
  while (i < la && j < lb) {
    if (a.charCodeAt(i) <= b.charCodeAt(j)) out += a[i++]; else out += b[j++];
  }
  return out + a.slice(i) + b.slice(j);
}
function varName(v) {
  // [SPEC 3.0] section 3: an indicator variable of a round has a number >= NVAR; "An indicator variable has NO NAME
  // in a certificate", so this text occurs in messages and tests only (never reached under "wx-cert-2")
  if (v >= NVAR) return `z#${v - NVAR + 1}`;
  // [SPEC 2.6] section 3: the ranges of the variable numbers follow the label set (2.5.1: v < 32, v < 49, v - 33, v - 49)
  if (v < V_S) return `xi:${LABELS[v >> 1]}:${(v & 1) + 1}`;
  if (v === V_S) return 'S';
  if (v < V_SN0) return `C:${LABELS[v - V_C0]}`;
  return `s:${LABELS[v - V_SN0]}`;
}
function monName(key) {
  if (key === '') return '1';
  const out = [];
  for (let i = 0; i < key.length; i++) out.push(varName(key.charCodeAt(i) - 48));
  return out.join('*');
}

/**
 * Sparse polynomial in the base variables with rational coefficients (SPEC 3: "an element of
 * Q[base variables]"), stored exactly as (1/den) * sum of BigInt coefficients (like terms combined, no
 * zero coefficients).  Treated as immutable once built.
 */
class SPoly {
  constructor(den, m) { this.den = den; this.m = m; this._hot = null; this._f = null; }
  static zero() { return new SPoly(1n, new Map()); }
  static constant(q) {
    const m = new Map();
    if (q.n !== 0n) m.set('', q.n);
    return new SPoly(q.n === 0n ? 1n : q.d, m);
  }
  static variable(v) { return new SPoly(1n, new Map([[MCH(v), 1n]])); }
  isZero() { return this.m.size === 0; }
  neg() {
    const m = new Map();
    for (const [k, c] of this.m) m.set(k, -c);
    return new SPoly(this.den, m);
  }
  /** product with a rational number */
  scaleQ(q) {
    if (q.n === 0n) return SPoly.zero();
    const m = new Map();
    for (const [k, c] of this.m) m.set(k, c * q.n);
    return new SPoly(this.den * q.d, m);
  }
  add(o) { return SPoly._combine(this, o, 1n); }
  sub(o) { return SPoly._combine(this, o, -1n); }
  static _combine(a, b, sgn) {
    let den, fa, fb;
    if (a.den === b.den) { den = a.den; fa = 1n; fb = 1n; }
    else { const g = bgcd(a.den, b.den); fa = b.den / g; fb = a.den / g; den = a.den * fa; }
    const m = new Map();
    for (const [k, c] of a.m) m.set(k, fa === 1n ? c : c * fa);
    fb *= sgn;
    for (const [k, c] of b.m) {
      const x = c * fb;
      const y = m.get(k);
      if (y === undefined) m.set(k, x);
      else { const z = y + x; if (z === 0n) m.delete(k); else m.set(k, z); }
    }
    return new SPoly(den, m);
  }
  mul(o) {
    const m = new Map();
    for (const [ka, ca] of this.m) {
      for (const [kb, cb] of o.m) {
        const k = monMul(ka, kb);
        const x = ca * cb;
        const y = m.get(k);
        if (y === undefined) m.set(k, x);
        else { const z = y + x; if (z === 0n) m.delete(k); else m.set(k, z); }
      }
    }
    return new SPoly(this.den * o.den, m);
  }
  /** product with one base variable */
  mulVar(v) {
    const ch = MCH(v);
    const m = new Map();
    for (const [k, c] of this.m) m.set(monMul(k, ch), c);
    return new SPoly(this.den, m);
  }
  /** Divide out the common factor of the denominator and all coefficients (in place; call once after building). */
  normalize() {
    if (this.m.size === 0) { this.den = 1n; return this; }
    let g = this.den;
    for (const c of this.m.values()) {
      if (g === 1n) break;
      g = bgcd(g, babs(c));
    }
    if (g !== 1n) {
      this.den /= g;
      for (const [k, c] of this.m) this.m.set(k, c / g);
    }
    return this;
  }
  /** coefficient of a monomial as a rational */
  coef(key) {
    const c = this.m.get(key);
    return c === undefined ? Q.ZERO : Q.make(c, this.den);
  }
  /** Floating-point value at a point (tests only). vals: array of NVAR numbers ([SPEC 2.6] section 3; 65 for sixteen labels). */
  evalFloat(vals) {
    let f = this._f;
    if (f === null) {
      f = { keys: [], coefs: [] };
      for (const [k, c] of this.m) { f.keys.push(k); f.coefs.push(ratioToNumber(c, this.den)); }
      this._f = f;
    }
    let sum = 0;
    for (let i = 0; i < f.keys.length; i++) {
      const k = f.keys[i];
      let t = f.coefs[i];
      for (let j = 0; j < k.length; j++) t *= vals[k.charCodeAt(j) - 48];
      sum += t;
    }
    return sum;
  }
  toString() {
    const parts = [];
    for (const [k, c] of this.m) parts.push(`${Q.make(c, this.den)}*${monName(k)}`);
    return parts.length ? parts.join(' + ') : '0';
  }
}

/** Array form of a polynomial for the inner loops of the step check. */
function hotOf(sp) {
  let h = sp._hot;
  if (h === null) {
    h = { den: sp.den, keys: Array.from(sp.m.keys()), coefs: Array.from(sp.m.values()) };
    sp._hot = h;
  }
  return h;
}
function mulHot(a, b) {
  const m = new Map();
  const ak = a.keys, ac = a.coefs, bk = b.keys, bc = b.coefs;
  for (let i = 0; i < ak.length; i++) {
    const ki = ak[i], ci = ac[i];
    for (let j = 0; j < bk.length; j++) {
      const k = monMul(ki, bk[j]);
      const x = ci * bc[j];
      const y = m.get(k);
      m.set(k, y === undefined ? x : y + x);
    }
  }
  return { keys: Array.from(m.keys()), coefs: Array.from(m.values()) };
}
// >>> [SPEC 3.0] section 4.9: "`sq:NAME` := (q:NAME)^2".  The square of a polynomial in the array form (integer
//     coefficients; the caller squares the denominator): sum_i c_i^2 m_i^2 + sum_{i<j} 2 c_i c_j m_i m_j.
function squareHot(a) {
  const m = new Map();
  const ak = a.keys, ac = a.coefs, n = ak.length;
  for (let i = 0; i < n; i++) {
    const ki = ak[i], ci = ac[i];
    let k = monMul(ki, ki);
    let x = ci * ci;
    let y = m.get(k);
    m.set(k, y === undefined ? x : y + x);
    const c2 = ci + ci;
    for (let j = i + 1; j < n; j++) {
      k = monMul(ki, ak[j]);
      x = c2 * ac[j];
      y = m.get(k);
      m.set(k, y === undefined ? x : y + x);
    }
  }
  return { keys: Array.from(m.keys()), coefs: Array.from(m.values()) };
}
/** Binomial coefficient C(e, k) as a BigInt (e, k small non-negative numbers, k <= e). */
function binomBig(e, k) {
  let r = 1n;
  for (let i = 1; i <= k; i++) r = r * BigInt(e - k + i) / BigInt(i);
  return r;
}
// <<< [SPEC 3.0]

// ===========================================================================
// D. Reference data from the packing file (SPEC 1)
// ===========================================================================

const SREF_SPEC = Q.make(4675530093604551n, 10n ** 15n); // SPEC 0: "Sref := 4675530093604551/10^15"

function loadReference(packingPath) {
  const bytes = fs.readFileSync(packingPath);
  const sha256 = crypto.createHash('sha256').update(bytes).digest('hex');
  const doc = parseJsonStrict(decodeUtf8(bytes), 'packing file');
  if (!(doc instanceof Map)) reject('packing file: not a JSON object');
  const side = parseNum(doc.get('side'), 'packing file: side');
  if (!side.eq(SREF_SPEC)) reject('packing file: "side" differs from Sref = 4675530093604551/10^15 of SPEC section 0');
  const sq = doc.get('squares');
  if (!Array.isArray(sq) || sq.length !== 17) reject('packing file: "squares" must be a list of 17 squares');
  // file order, 1-based labels (SPEC 0)
  const pfile = [], t = [], u = [], v = [];
  for (let lab = 1; lab <= 17; lab++) {
    const s = sq[lab - 1];
    if (!(s instanceof Map)) reject(`packing file: square ${lab} is not an object`);
    pfile[lab] = [parseNum(s.get('x'), `packing file: square ${lab} x`), parseNum(s.get('y'), `packing file: square ${lab} y`)];
    t[lab] = parseNum(s.get('t'), `packing file: square ${lab} t`);
    // SPEC 1: "u_i := ((1-t_i^2)/(1+t_i^2), 2 t_i/(1+t_i^2)), v_i := J u_i"
    const t2 = t[lab].mul(t[lab]);
    const den = Q.ONE.add(t2);
    u[lab] = [Q.ONE.sub(t2).div(den), t[lab].add(t[lab]).div(den)];
    v[lab] = [u[lab][1].neg(), u[lab][0]];
  }
  // SPEC 1: "p_13 := p_13^file - (T0/3) v_13 with T0 := u_9x * (u_9x + 4 - Sref)"
  const T0 = u[9][0].mul(u[9][0].add(Q.int(4)).sub(side));
  const T03 = T0.div(Q.int(3));
  // >>> [SPEC 2.6] section 1: reference data "For every i in I, in particular for i = 4 when I has seventeen labels".
  //     The file is read before the header, so the data are laid out once for each of the two label sets:
  //     byN[n].p[li], .u[li], .v[li], .e1[li], .e2[li] with li = index of the label in LABEL_SETS[n].LABELS.
  //     NodeCtx takes byN[NL].  Label 4 gets p_4 := p_4^file and the frame ((1,0),(0,1)) like every label other
  //     than 11 and 13.  The fields p, u, v, e1, e2 of the result remain the sixteen-label arrays of version 2.5.1.
  const byN = {};
  for (const n of [16, 17]) {
    const set = LABEL_SETS[n];
    const d = { p: [], u: [], v: [], e1: [], e2: [] };
    for (let li = 0; li < set.NL; li++) {
      const lab = set.LABELS[li];
      let p = pfile[lab];
      if (lab === 13) p = [p[0].sub(T03.mul(v[13][0])), p[1].sub(T03.mul(v[13][1]))];
      d.p[li] = p;
      d.u[li] = u[lab];
      d.v[li] = v[lab];
      // SPEC 1: "Frames: (e_i1, e_i2) := (u_i, v_i) for i in {11, 13}; ((1,0),(0,1)) for all other i."
      if (lab === 11 || lab === 13) { d.e1[li] = u[lab]; d.e2[li] = v[lab]; }
      else { d.e1[li] = [Q.ONE, Q.ZERO]; d.e2[li] = [Q.ZERO, Q.ONE]; }
    }
    byN[n] = d;
  }
  return { path: packingPath, sha256, side, p: byN[16].p, u: byN[16].u, v: byN[16].v, e1: byN[16].e1, e2: byN[16].e2, T0, byN };
  // <<< [SPEC 2.6]
}

// ===========================================================================
// E. Names of forms and facts (SPEC 10: "FACT names", "Form NAMEs")
// ===========================================================================

const CLS_RE = /^[ab][+-][ab][+-]$/;
const UNAME_RE = /^[A-Za-z0-9_]+$/;

/** Label written in a name: "integers without sign or leading zeros", element of I.  Returns -1 if not. */
function nameLabel(s) {
  if (s.length === 0 || s.length > 2 || !LABEL_RE.test(s)) return -1;
  const x = Number(s);
  return LIDX.has(x) ? x : -1;
}

/** SPEC 4.6: "A CLASS K = (axis_i, eps_i, axis_j, eps_j)", written as four characters, e.g. a+b-. */
function classInfo(cls) {
  return { axI: cls[0], epsI: cls[1] === '+' ? 1 : -1, axJ: cls[2], epsJ: cls[3] === '+' ? 1 : -1 };
}

/**
 * Parse a form name given as its colon-separated parts.  Returns null if it is not in the list
 *   xi:i:k, S, C:i, s:i, Da:o:t, Db:o:t, A:o:t, B:o:t, Cr:i:j, Sr:i:j,
 *   al:i:j:K, be:i:j:K, co:i:j:K, si:i:j:K, Y:i:j:K, u:NAME, 0
 * with the label and pair rules of SPEC 10 (i < j, both in I; o != t, both in I).
 */
function parseFormParts(p) {
  const h = p[0];
  switch (h) {
    case '0':
      return p.length === 1 ? { kind: '0' } : null;
    case 'S':
      return p.length === 1 ? { kind: 'S' } : null;
    case 'xi': {
      if (p.length !== 3) return null;
      const i = nameLabel(p[1]);
      if (i < 0 || (p[2] !== '1' && p[2] !== '2')) return null;
      return { kind: 'xi', i, k: p[2] === '1' ? 1 : 2 };
    }
    case 'C': case 's': {
      if (p.length !== 2) return null;
      const i = nameLabel(p[1]);
      return i < 0 ? null : { kind: h, i };
    }
    case 'Da': case 'Db': case 'A': case 'B': {
      if (p.length !== 3) return null;
      const o = nameLabel(p[1]), t = nameLabel(p[2]);
      if (o < 0 || t < 0 || o === t) return null;
      return { kind: h, o, t };
    }
    case 'Cr': case 'Sr': {
      if (p.length !== 3) return null;
      const i = nameLabel(p[1]), j = nameLabel(p[2]);
      if (i < 0 || j < 0 || !(i < j)) return null;
      return { kind: h, i, j };
    }
    case 'al': case 'be': case 'co': case 'si': case 'Y': {
      if (p.length !== 4) return null;
      const i = nameLabel(p[1]), j = nameLabel(p[2]);
      if (i < 0 || j < 0 || !(i < j) || !CLS_RE.test(p[3])) return null;
      return { kind: h, i, j, cls: p[3] };
    }
    case 'u':
      if (p.length !== 2 || !UNAME_RE.test(p[1])) return null;
      return { kind: 'u', uname: p[1] };
    default:
      return null;
  }
}
function parseFormName(name) {
  const pf = parseFormParts(name.split(':'));
  if (pf !== null) pf.name = name;
  return pf;
}
function isBaseKind(kind) { return kind === 'xi' || kind === 'S' || kind === 'C' || kind === 's'; }

const ARC_SUBS = new Set(['slo', 'shi', 'clo', 'chi', 'chord']);
function pm(s) { return s === 'p' ? 1 : (s === 'm' ? -1 : 0); }

/**
 * Parse a fact name.  Returns an object {kind, ...} or a string (the reason why the name is not in the
 * list of SPEC 10).  The form inside ivl:/cut: names is returned as the string `formName` and resolved
 * by the caller (custom forms depend on the node).
 */
function parseFactName(name) {
  const p = name.split(':');
  const bad = 'unknown or malformed fact name';
  switch (p[0]) {
    case 'box': { // box:i:k:lo|hi
      if (p.length !== 4) return bad;
      const i = nameLabel(p[1]);
      if (i < 0) return 'bad label in fact name';
      if (p[2] !== '1' && p[2] !== '2') return 'k must be 1 or 2';
      if (p[3] !== 'lo' && p[3] !== 'hi') return bad;
      return { kind: 'box', i, k: p[2] === '1' ? 1 : 2, end: p[3] };
    }
    case 'side': // side:lo|hi
      if (p.length !== 2 || (p[1] !== 'lo' && p[1] !== 'hi')) return bad;
      return { kind: 'side', end: p[1] };
    case 'wall': { // wall:i:E1:E2:k:lo|hi
      if (p.length !== 6) return bad;
      const i = nameLabel(p[1]);
      if (i < 0) return 'bad label in fact name';
      const e1 = pm(p[2]), e2 = pm(p[3]);
      if (e1 === 0 || e2 === 0) return 'corner letters must be p or m';
      if (p[4] !== 'x' && p[4] !== 'y') return 'wall coordinate must be x or y';
      if (p[5] !== 'lo' && p[5] !== 'hi') return bad;
      return { kind: 'wall', i, e1, e2, k: p[4], end: p[5] };
    }
    case 'arc': { // arc:i:slo|shi|clo|chi|chord ; arc:i:tan:G:H
      if (p.length !== 3 && p.length !== 5) return bad;
      const i = nameLabel(p[1]);
      if (i < 0) return 'bad label in fact name';
      if (p.length === 3) {
        if (!ARC_SUBS.has(p[2])) return bad;
        return { kind: 'arc', i, sub: p[2] };
      }
      if (p[2] !== 'tan') return bad;
      const G = parseNumString(p[3]), H = parseNumString(p[4]);
      if (G === null || H === null) return 'malformed tangent coefficient';
      // SPEC 4.2: "for any rationals G, H with G^2 + H^2 <= 1 (checked)"
      if (G.mul(G).add(H.mul(H)).gt(Q.ONE)) return 'tangent with G^2 + H^2 > 1';
      return { kind: 'arctan', i, G, H };
    }
    case 'rarc': { // rarc:i:j:slo|shi|clo|chi|chord ; rarc:i:j:tan:G:H
      if (p.length !== 4 && p.length !== 6) return bad;
      const i = nameLabel(p[1]), j = nameLabel(p[2]);
      if (i < 0 || j < 0) return 'bad label in fact name';
      if (!(i < j)) return 'a pair i:j in a name needs i < j';
      if (p.length === 4) {
        if (!ARC_SUBS.has(p[3])) return bad;
        return { kind: 'rarc', i, j, sub: p[3] };
      }
      if (p[3] !== 'tan') return bad;
      const G = parseNumString(p[4]), H = parseNumString(p[5]);
      if (G === null || H === null) return 'malformed tangent coefficient';
      if (G.mul(G).add(H.mul(H)).gt(Q.ONE)) return 'tangent with G^2 + H^2 > 1';
      return { kind: 'rarctan', i, j, G, H };
    }
    case 'opt': { // opt:o:t:axis:EPS:E1:E2
      if (p.length !== 7) return bad;
      const o = nameLabel(p[1]), t = nameLabel(p[2]);
      if (o < 0 || t < 0) return 'bad label in fact name';
      if (o === t) return 'an ordered pair o:t in a name needs o != t';
      if (p[3] !== 'a' && p[3] !== 'b') return 'axis must be a or b';
      const eps = pm(p[4]), e1 = pm(p[5]), e2 = pm(p[6]);
      if (eps === 0) return 'EPS must be p or m';
      if (e1 === 0 || e2 === 0) return 'corner letters must be p or m';
      return { kind: 'opt', o, t, axis: p[3], eps, e1, e2 };
    }
    case 'par': { // par:i:j:K:kind:1|2
      if (p.length !== 6) return bad;
      const i = nameLabel(p[1]), j = nameLabel(p[2]);
      if (i < 0 || j < 0) return 'bad label in fact name';
      if (!(i < j)) return 'a pair i:j in a name needs i < j';
      if (!CLS_RE.test(p[3])) return 'class missing or malformed in the name (need [ab][+-][ab][+-])';
      // >>> SPEC 2.5: kind "Ps"
      if (p[4] !== 'P+' && p[4] !== 'P-' && p[4] !== 'Pk' && p[4] !== 'Ps') return 'kind must be P+, P-, Pk or Ps';
      // <<< SPEC 2.5
      if (p[5] !== '1' && p[5] !== '2') return bad;
      return { kind: 'par', i, j, cls: p[3], pkind: p[4], idx: p[5] === '1' ? 1 : 2 };
    }
    // >>> SPEC 2.5: wall support facts
    case 'wsup': { // wsup:i:W:p|m, W in {xlo, ylo, xhi, yhi}
      if (p.length !== 4) return bad;
      const i = nameLabel(p[1]);
      if (i < 0) return 'bad label in fact name';
      if (p[2] !== 'xlo' && p[2] !== 'ylo' && p[2] !== 'xhi' && p[2] !== 'yhi') return 'wall name of a wsup fact must be xlo, ylo, xhi or yhi';
      const sgn = pm(p[3]);
      if (sgn === 0) return bad;
      return { kind: 'wsup', i, wall: p[2], sgn };
    }
    // <<< SPEC 2.5
    case 'asg': { // asg:i:j:K:p|m
      if (p.length !== 5) return bad;
      const i = nameLabel(p[1]), j = nameLabel(p[2]);
      if (i < 0 || j < 0) return 'bad label in fact name';
      if (!(i < j)) return 'a pair i:j in a name needs i < j';
      if (!CLS_RE.test(p[3])) return 'class missing or malformed in the name (need [ab][+-][ab][+-])';
      const sgn = pm(p[4]);
      if (sgn === 0) return bad;
      return { kind: 'asg', i, j, cls: p[3], sgn };
    }
    case 'ivl': case 'cut': { // ivl:FORM:lo|hi ; cut:FORM:lo|hi
      if (p.length < 3) return bad;
      const end = p[p.length - 1];
      if (end !== 'lo' && end !== 'hi') return bad;
      return { kind: p[0], formName: p.slice(1, -1).join(':'), end };
    }
    case 'circ': { // circ:i
      if (p.length !== 2) return bad;
      const i = nameLabel(p[1]);
      if (i < 0) return 'bad label in fact name';
      return { kind: 'circ', i };
    }
    // >>> [SPEC 3.0] section 10, FACT names: "(wx-cert-3) `sq:NAME`; `pol:NAME` (not a fact: only in a term containing
    //     a `circ` fact); in `sq:NAME` and in `pol:NAME`, NAME matches [A-Za-z0-9_]+ and is the NAME of a key `q:NAME`
    //     of the node's `forms`; `ind:i:j:k` (i < j, both in I; k one digit 1 to 8)".  These are conditions that are
    //     part of a name: list (W), whole file.  SCHEMA RULE: under "wx-cert-2" "a name that begins with `sq:`,
    //     `pol:` or `ind:` (not a fact name)" is rejected: there these cases return what the default case returns,
    //     as in the 2.6 file.  That the form q:NAME is defined is tested by Validator.factRef; k <= m by RoundCtx.
    case 'sq': case 'pol': { // sq:NAME ; pol:NAME
      if (!SCHEMA3) return bad;
      if (p.length !== 2 || !UNAME_RE.test(p[1])) return 'the NAME of a polynomial form must match [A-Za-z0-9_]+';
      return { kind: p[0], qname: p[1] };
    }
    case 'ind': { // ind:i:j:k
      if (!SCHEMA3) return bad;
      if (p.length !== 4) return bad;
      const i = nameLabel(p[1]), j = nameLabel(p[2]);
      if (i < 0 || j < 0) return 'bad label in fact name';
      if (!(i < j)) return 'a pair i:j in a name needs i < j';
      if (!/^[1-8]$/.test(p[3])) return 'the index k of a name ind:i:j:k must be one digit 1 to 8';
      return { kind: 'ind', i, j, k: Number(p[3]) };
    }
    // <<< [SPEC 3.0]
    default:
      return bad;
  }
}

function optKey(o, t, axis, eps) { return `${o}:${t}:${axis}:${eps > 0 ? 'p' : 'm'}`; }
function signKey(i, j, cls, sign) { return `${i}:${j}:${cls}:${sign > 0 ? 'p' : 'm'}`; }
function optText(op) { return `(${op.o}, ${op.t}, ${op.axis}, ${op.eps > 0 ? '+1' : '-1'})`; }
/** The 8 options of the pair {i, j} (SPEC 4.5 SAT LEMMA). */
function eightOptions(i, j) {
  const out = [];
  for (const [o, t] of [[i, j], [j, i]]) for (const axis of ['a', 'b']) for (const eps of [1, -1]) out.push({ o, t, axis, eps });
  return out;
}

// ===========================================================================
// F. Well-formedness (SPEC 10): JSON values -> typed structures
// ===========================================================================

class Validator {
  constructor(opts) {
    // >>> [SPEC 3.0] section 10, KEYS: "Every JSON object of a certificate has exactly the keys that the format
    //     blocks and items of this section give for it, optional ones possibly absent ...  A key that is not defined
    //     for the object rejects the certificate."  The rule is normative in 3.0, for both schemas.  The 2.6 file had
    //     an option (--ignore-unknown-keys, opts.ignoreUnknownKeys) under which such a key was counted and ignored;
    //     it is REMOVED: this file has no option, environment variable or mode that relaxes a rule of the SPEC.
    //     (2.6: this.strictKeys = !(opts && opts.ignoreUnknownKeys);)  The map below is kept for the driver's
    //     report plumbing and always stays empty.
    this.unknownKeys = new Map();
    // <<< [SPEC 3.0]
    this.custom = new Map();
    this.formCache = new Map();
    this.factCache = new Map();
    // [SPEC 3.0] section 3 (polynomial forms of the node: "Polynomial forms and custom forms have separate name
    // spaces") and 4.10 (R3) (the pairs for which the node has an option assumption); both are set per node
    this.qforms = new Map();
    this.assumeOptPairs = new Set();
  }
  obj(v, where, required, optional) {
    if (!(v instanceof Map)) reject(`${where}: expected a JSON object`);
    for (const k of required) if (!v.has(k)) reject(`${where}: missing key "${k}"`);
    for (const k of v.keys()) {
      if (required.includes(k) || (optional && optional.includes(k))) continue;
      // [SPEC 3.0] section 10, KEYS: unconditional (2.6: only "if (this.strictKeys)", else the key was counted and ignored)
      reject(`${where}: unknown key ${JSON.stringify(k)}`);
    }
    return v;
  }
  arr(v, where, len) {
    if (!Array.isArray(v)) reject(`${where}: expected a JSON array`);
    if (len !== undefined && v.length !== len) reject(`${where}: expected a JSON array of length ${len} (found ${v.length})`);
    return v;
  }
  str(v, where) {
    if (typeof v !== 'string') reject(`${where}: expected a JSON string`);
    return v;
  }
  /**
   * SPEC 10: "Labels are integers of I (section 0: {1,...,17} minus {4}, or {1,...,17} if the header says
   * `labels` = 17) (JSON integers in fields ...)".
   * [SPEC 2.6] section 10: the test itself (LIDX) follows the label set; only the two messages changed
   * (LABEL_TEXT is "I = {1,...,17} minus {4}" for sixteen labels, as in 2.5.1, and "I = {1,...,17}" for seventeen).
   */
  label(v, where) {
    if (!(v instanceof JNum) || !LABEL_RE.test(v.raw) || v.raw.length > 2) reject(`${where}: a label must be a JSON integer of ${LABEL_TEXT}`);
    const x = Number(v.raw);
    if (!LIDX.has(x)) reject(`${where}: ${x} is not a label of ${LABEL_TEXT}`);
    return x;
  }
  /** eps, sign in {1, -1} (JSON integers) */
  pmInt(v, where, what) {
    if (!(v instanceof JNum) || (v.raw !== '1' && v.raw !== '-1')) reject(`${where}: ${what} must be the JSON integer 1 or -1`);
    return v.raw === '1' ? 1 : -1;
  }
  /** k in {1, 2} (JSON integer) */
  k12(v, where) {
    if (!(v instanceof JNum) || (v.raw !== '1' && v.raw !== '2')) reject(`${where}: k must be the JSON integer 1 or 2`);
    return v.raw === '1' ? 1 : 2;
  }
  axis(v, where) {
    if (v !== 'a' && v !== 'b') reject(`${where}: axis must be "a" or "b"`);
    return v;
  }
  cls(v, where) {
    if (typeof v !== 'string' || !CLS_RE.test(v)) reject(`${where}: cls must match [ab][+-][ab][+-]`);
    return v;
  }
  /** SPEC 10: "A rotation is [g, s] with g^2 + s^2 = 1 (checked for every rotation in the file)." */
  rot(v, where) {
    this.arr(v, where, 2);
    const r = new Rot(parseNum(v[0], where), parseNum(v[1], where));
    if (!r.isUnit()) reject(`${where}: rotation [g, s] with g^2 + s^2 != 1`);
    return r;
  }
  interval(v, where) {
    this.arr(v, where, 2);
    return [parseNum(v[0], where), parseNum(v[1], where)];
  }
  /**
   * SPEC 10: "Every map keyed by labels ... has exactly the keys of I (16 or 17 of them)."
   * [SPEC 2.6] section 10: the two tests (LABEL_KEY_SET, LABEL_KEYS) follow the label set; only the three
   * messages changed (NL and LABEL_TEXT in place of "16" and "I = {1,...,17} minus {4}").
   */
  labelMap(v, where) {
    if (!(v instanceof Map)) reject(`${where}: expected a JSON object keyed by the ${NL} labels of I`);
    for (const k of v.keys()) if (!LABEL_KEY_SET.has(k)) reject(`${where}: key ${JSON.stringify(k)} is not a label of ${LABEL_TEXT}`);
    for (const k of LABEL_KEYS) if (!v.has(k)) reject(`${where}: label ${k} is missing (the map must have exactly the ${NL} keys of I)`);
    return v;
  }
  /** box map -> [li][k-1] = [lo, hi]; proper: lo <= hi required (node data, window, tube) */
  boxMap(v, where, proper) {
    this.labelMap(v, where);
    const out = new Array(NL);
    for (let li = 0; li < NL; li++) {
      const W = `${where}[${LABEL_KEYS[li]}]`;
      const e = this.arr(v.get(LABEL_KEYS[li]), W, 2);
      const a = this.interval(e[0], W), b = this.interval(e[1], W);
      if (proper && (a[0].gt(a[1]) || b[0].gt(b[1]))) reject(`${W}: interval with lo > hi`);
      out[li] = [a, b];
    }
    return out;
  }
  /** arc map; node data: {c, lo, hi} with cos > 0 and ordered sines (SPEC 2, 10); store: {lo, hi}, unit only */
  arcMap(v, where, isNodeData) {
    this.labelMap(v, where);
    const out = new Array(NL);
    for (let li = 0; li < NL; li++) {
      const W = `${where}[${LABEL_KEYS[li]}]`;
      const e = v.get(LABEL_KEYS[li]);
      if (isNodeData) {
        this.obj(e, W, ['c', 'lo', 'hi'], []);
        const c = this.rot(e.get('c'), `${W}.c`), lo = this.rot(e.get('lo'), `${W}.lo`), hi = this.rot(e.get('hi'), `${W}.hi`);
        if (lo.g.sign() <= 0) reject(`${W}.lo: endpoint with non-positive cosine`);
        if (hi.g.sign() <= 0) reject(`${W}.hi: endpoint with non-positive cosine`);
        if (lo.s.gt(hi.s)) reject(`${W}: sin P^- > sin P^+`);
        out[li] = { c, lo, hi };
      } else {
        this.obj(e, W, ['lo', 'hi'], []);
        out[li] = { lo: this.rot(e.get('lo'), `${W}.lo`), hi: this.rot(e.get('hi'), `${W}.hi`) };
      }
    }
    return out;
  }
  /** window / tube of the header (SPEC 8) */
  region(v, where, isTube) {
    // [SPEC 3.0] section 10: "(wx-cert-3) Optional field `centre` in the header's `window` object and, independently,
    // in its `terminal` object ...  Neither object has another optional field."  Under "wx-cert-2" the list of
    // optional keys is empty as in the 2.6 file, and a `centre` is an unknown key (SCHEMA RULE, KEYS).
    this.obj(v, where, ['box', 'alpha'], SCHEMA3 ? ['centre'] : []);
    const box = this.boxMap(v.get('box'), `${where}.box`, true);
    const am = this.labelMap(v.get('alpha'), `${where}.alpha`);
    const alpha = new Array(NL);
    for (let li = 0; li < NL; li++) {
      const a = parseNum(am.get(LABEL_KEYS[li]), `${where}.alpha[${LABEL_KEYS[li]}]`);
      // SPEC 8: "a rational angle radius alpha_i > 0"; window "Requires alpha_i < 1"; tube "Requires alphaT_i <= 1"
      if (a.sign() <= 0) reject(`${where}.alpha[${LABEL_KEYS[li]}]: angle radius must be > 0`);
      if (isTube ? a.gt(Q.ONE) : a.ge(Q.ONE)) reject(`${where}.alpha[${LABEL_KEYS[li]}]: angle radius must be ${isTube ? '<= 1' : '< 1'}`);
      alpha[li] = a;
    }
    // >>> [SPEC 3.0] sections 8 and 10: "a map keyed by labels with exactly the keys of I; every value is a rotation
    //     [g, s] (g^2 + s^2 = 1, checked).  Absent means the identity for every label."  centre === null stands for
    //     "absent" (always under "wx-cert-2": there the key is never read; this.obj above has rejected it as an
    //     unknown key).
    let centre = null;
    if (SCHEMA3 && v.has('centre')) {
      const cm = this.labelMap(v.get('centre'), `${where}.centre`);
      centre = new Array(NL);
      for (let li = 0; li < NL; li++) centre[li] = this.rot(cm.get(LABEL_KEYS[li]), `${where}.centre[${LABEL_KEYS[li]}]`);
    }
    return { box, alpha, centre };
    // <<< [SPEC 3.0]
  }
  header(h, ref, opts) {
    // [SPEC 2.6] section 10: "Optional header field `labels` ... Optional header field `S_floor` ... The header has
    // no other optional field."  (2.5.1: the list of optional keys was empty; any other key is rejected by obj().)
    this.obj(h, 'header', ['schema', 'packing_sha256', 'Sref', 'root', 'window', 'terminal'], ['labels', 'S_floor']);
    // >>> [SPEC 3.0] section 10: "`schema` equals "wx-cert-2" or "wx-cert-3" (SCHEMA RULE below)".  The schema is
    //     selected here, before anything else of the header is read (2.6: the one string "wx-cert-2"; the message
    //     named that string alone).
    const schema = h.get('schema');
    if (schema !== 'wx-cert-2' && schema !== 'wx-cert-3') reject('header: schema must equal "wx-cert-2" or "wx-cert-3"');
    useSchema(schema === 'wx-cert-3');
    // <<< [SPEC 3.0]
    const sha = this.str(h.get('packing_sha256'), 'header: packing_sha256');
    if (sha !== ref.sha256) reject(`header: packing_sha256 ${JSON.stringify(sha)} differs from the SHA-256 of the packing file read (${ref.sha256})`);
    if (opts && opts.expectPackingSha256 && opts.expectPackingSha256 !== ref.sha256) reject(`packing file: SHA-256 ${ref.sha256} differs from the expected ${opts.expectPackingSha256}`);
    const Sref = parseNum(h.get('Sref'), 'header: Sref');
    if (!Sref.eq(ref.side)) reject(`header: Sref = ${Sref} differs from the "side" of the packing file (${ref.side})`);
    const root = this.str(h.get('root'), 'header: root');
    // >>> [SPEC 2.6] section 10: "Optional header field `labels`: the JSON integer 16 or 17 (anything else is
    //     rejected); absent means 16.  It fixes I for the whole certificate."
    //     A JSON integer is a number token without sign, fraction or exponent, as for labels, k, eps and sign in this
    //     file: exactly the token 16 or 17 ("17", 17.0, 1.7e1, 017, null, true, [17] are rejected).  The label set
    //     is selected here, BEFORE the maps `window` and `terminal` are read, which must have exactly the keys of I.
    let labels = 16;
    if (h.has('labels')) {
      const lv = h.get('labels');
      if (!(lv instanceof JNum) || (lv.raw !== '16' && lv.raw !== '17')) {
        reject('header: labels must be the JSON integer 16 or 17' + (lv instanceof JNum ? ` (found the JSON number ${lv.raw})` : ''));
      }
      labels = lv.raw === '17' ? 17 : 16;
    }
    useLabels(labels);
    //     SPEC 10: "Optional header field `S_floor`: a number string with 4 <= S_floor <= Sref (anything else is
    //     rejected); absent means 4."  A number string is a JSON string "p" or "p/q" (parseNum; a JSON number such
    //     as 4.5 and a string such as "4.5" are rejected); Sref is the header's Sref, which equals the file's `side`.
    let S_floor = Q.int(4);
    const S_floorGiven = h.has('S_floor');
    if (S_floorGiven) {
      S_floor = parseNum(h.get('S_floor'), 'header: S_floor');
      if (S_floor.lt(Q.int(4)) || S_floor.gt(Sref)) reject(`header: S_floor = ${S_floor} is outside [4, Sref] (need 4 <= S_floor <= Sref = ${Sref})`);
    }
    // <<< [SPEC 2.6]
    const window = this.region(h.get('window'), 'header.window', false);
    const terminal = this.region(h.get('terminal'), 'header.terminal', true);
    // [SPEC 2.6] sections 0, 7, 10: the label count and S_floor used are part of the checked header
    // [SPEC 3.0] section 10: the schema of the checked header (string, and the flag that useSchema takes)
    return { Sref, root, window, terminal, labels, S_floor, S_floorGiven, schema, schema3: schema === 'wx-cert-3' };
  }
  /** i, j naming a pair: i < j, both in I (SPEC 10) */
  pairIJ(d, where) {
    const i = this.label(d.get('i'), `${where}: i`), j = this.label(d.get('j'), `${where}: j`);
    if (!(i < j)) reject(`${where}: a pair needs i < j (found i = ${i}, j = ${j})`);
    return [i, j];
  }
  pairArray(v, where) {
    this.arr(v, where, 2);
    const i = this.label(v[0], where), j = this.label(v[1], where);
    if (!(i < j)) reject(`${where}: a pair [i, j] needs i < j (found [${i}, ${j}])`);
    return [i, j];
  }
  /** o, t, axis, eps of an option: o != t, both in I (SPEC 10) */
  optionFields(d, where) {
    const o = this.label(d.get('o'), `${where}: o`), t = this.label(d.get('t'), `${where}: t`);
    if (o === t) reject(`${where}: an option needs o != t (found o = t = ${o})`);
    return { o, t, axis: this.axis(d.get('axis'), where), eps: this.pmInt(d.get('eps'), where, 'eps') };
  }
  assumeItem(a, where) {
    if (!(a instanceof Map)) reject(`${where}: expected a JSON object`);
    const kind = a.get('kind');
    if (kind === 'opt') {
      this.obj(a, where, ['kind', 'o', 't', 'axis', 'eps'], []);
      const op = this.optionFields(a, where);
      return { kind, o: op.o, t: op.t, axis: op.axis, eps: op.eps, key: 'opt|' + optKey(op.o, op.t, op.axis, op.eps) };
    }
    if (kind === 'ysign') {
      this.obj(a, where, ['kind', 'i', 'j', 'cls', 'sign'], []);
      const [i, j] = this.pairIJ(a, where);
      const cls = this.cls(a.get('cls'), where);
      const sign = this.pmInt(a.get('sign'), where, 'sign');
      return { kind, i, j, cls, sign, key: 'ysign|' + signKey(i, j, cls, sign) };
    }
    reject(`${where}: assumption kind must be "opt" or "ysign"`);
    return null;
  }
  /** A form name used in the node: must parse; a custom form must be defined in the node's `forms`. */
  formRef(name, where) {
    if (typeof name !== 'string') reject(`${where}: a form name must be a JSON string`);
    let pf = this.formCache.get(name);
    if (pf !== undefined) return pf;
    pf = parseFormName(name);
    if (pf === null) reject(`${where}: unknown or malformed form name ${JSON.stringify(name)}`);
    if (pf.kind === 'u') {
      const def = this.custom.get(pf.uname);
      if (def === undefined) reject(`${where}: custom form ${JSON.stringify(name)} is not defined in the node's "forms"`);
      pf.def = def;
    }
    this.formCache.set(name, pf);
    return pf;
  }
  factRef(name, where) {
    if (typeof name !== 'string') reject(`${where()}: a fact name must be a JSON string`);
    let pf = this.factCache.get(name);
    if (pf !== undefined) return pf;
    pf = parseFactName(name);
    if (typeof pf === 'string') reject(`${where()}: fact ${JSON.stringify(name)}: ${pf}`);
    pf.name = name;
    // >>> [SPEC 3.0] sections 4.9 and 10: "Both names require that q:NAME is defined in the `forms` of the node;
    //     otherwise the certificate is rejected, also if the name stands in a round that is not evaluated."
    //     (These kinds exist only under "wx-cert-3", see parseFactName.)
    if (pf.kind === 'sq' || pf.kind === 'pol' || pf.kind === 'ind') {
      if (!SCHEMA3) internal('a name of version 3.0 under the schema "wx-cert-2"'); // gate at the point of use
    }
    if (pf.kind === 'sq' || pf.kind === 'pol') {
      const def = this.qforms.get(pf.qname);
      if (def === undefined) reject(`${where()}: name ${JSON.stringify(name)}: the polynomial form "q:${pf.qname}" is not defined in the node's "forms"`);
      pf.qdef = def;
    }
    // <<< [SPEC 3.0]
    if (pf.kind === 'ivl' || pf.kind === 'cut') {
      const f = this.formRef(pf.formName, `${where()}: fact ${JSON.stringify(name)}`);
      pf.form = f;
      if (pf.kind === 'cut') {
        if (f.kind === '0') reject(`${where()}: fact ${JSON.stringify(name)}: no cut fact for the form \`0\``);
      } else {
        // SPEC 4.0 / 10: ivl only for Da:o:t, Db:o:t or an AFFINE custom form
        const ok = f.kind === 'Da' || f.kind === 'Db' || (f.kind === 'u' && f.def.affine);
        if (!ok) reject(`${where()}: fact ${JSON.stringify(name)}: ivl facts exist only for Da:o:t, Db:o:t or an affine custom form`);
      }
    }
    pf.rc = null;
    pf.entry = null;
    this.factCache.set(name, pf);
    return pf;
  }
  /** SPEC 3 / 10 "forms": custom forms of the node */
  forms(v, where) {
    if (!(v instanceof Map)) reject(`${where}: expected a JSON object`);
    for (const [name, comps] of v) {
      // >>> [SPEC 3.0] section 10: "(wx-cert-3) `forms` may also have keys `q:NAME` ...  A key of `forms` that does
      //     not begin with `q:` is the NAME of a custom form as before; a key that begins with `q:` and is not of
      //     the form above is rejected."  Under "wx-cert-2" such a key reaches the test of the 2.6 file below and is
      //     rejected there ("a key of `forms` that begins with `q:` (not a custom form NAME)", SCHEMA RULE).
      if (SCHEMA3 && name.startsWith('q:')) { this.qform(name, comps, where); continue; }
      // <<< [SPEC 3.0]
      if (!UNAME_RE.test(name)) reject(`${where}: custom form NAME ${JSON.stringify(name)} must match [A-Za-z0-9_]+`);
      const W = `${where}.${name}`;
      this.arr(comps, W);
      if (comps.length === 0) reject(`${W}: empty linear combination`);
      const seen = new Set();
      const list = [];
      let affine = true;
      for (let k = 0; k < comps.length; k++) {
        const c = this.arr(comps[k], `${W}[${k}]`, 2);
        const coef = parseNum(c[0], `${W}[${k}] coefficient`);
        const fname = this.str(c[1], `${W}[${k}] form name`);
        const probe = parseFormName(fname);
        if (probe === null) reject(`${W}[${k}]: unknown or malformed form name ${JSON.stringify(fname)}`);
        if (probe.kind === '0' || probe.kind === 'u') reject(`${W}[${k}]: a component of a custom form may not be \`0\` or another custom form (found ${fname})`);
        if (seen.has(fname)) reject(`${W}[${k}]: repeated component ${fname} (the component names of one custom form must be pairwise different)`);
        seen.add(fname);
        if (probe.kind !== 'xi' && probe.kind !== 'Da' && probe.kind !== 'Db') affine = false;
        list.push({ coef, pf: this.formRef(fname, `${W}[${k}]`) });
      }
      this.custom.set(name, { name: 'u:' + name, comps: list, affine });
    }
  }
  // >>> [SPEC 3.0] sections 3 and 10: polynomial forms, the `centre` of a step
  /**
   * The name of a BASE VARIABLE (`xi:i:k`, `S`, `C:i`, `s:i`, labels of I, "written like the form names"): returns
   * its variable number, or -1 if the string is not such a name.
   */
  baseVarNumber(name) {
    if (typeof name !== 'string') return -1;
    const pf = parseFormName(name);
    if (pf === null) return -1;
    switch (pf.kind) {
      case 'xi': return V_XI(LIDX.get(pf.i), pf.k);
      case 'S': return V_S;
      case 'C': return V_C(LIDX.get(pf.i));
      case 's': return V_SN(LIDX.get(pf.i));
      default: return -1;
    }
  }
  /**
   * SPEC 3: "POLYNOMIAL FORMS `q:NAME` (NAME matching [A-Za-z0-9_]+), defined in the node's `forms` field as a
   * nonempty list of ENTRIES [coef, [v_1, ..., v_r]] with r in {0, 1, 2}, coef a rational number and every v_l the
   * name of a base variable ...  The monomials of the entries of one form, taken as multisets {v_1, ..., v_r}, are
   * pairwise different (so [x, y] and [y, x] in one form are rejected); the coefficient 0 is allowed (such an entry
   * contributes nothing, but its monomial counts for this rule)."
   * SPEC 10: "an entry is a list of exactly two elements, a number and a list of 0, 1 or 2 base variable names".
   * The form is kept as {name, keys, coefs}: keys[k] the monomial of entry k (sorted string of variable numbers),
   * coefs[k] its coefficient (Q).  name = the key "q:NAME".
   */
  qform(name, ents, where) {
    if (!SCHEMA3) internal('a polynomial form under the schema "wx-cert-2"'); // gate at the point of use
    const W = `${where}[${JSON.stringify(name)}]`;
    const qn = name.slice(2);
    if (!UNAME_RE.test(qn)) reject(`${W}: a key of "forms" that begins with "q:" must be q:NAME with NAME matching [A-Za-z0-9_]+`);
    this.arr(ents, W);
    if (ents.length === 0) reject(`${W}: a polynomial form needs a nonempty list of entries`);
    const seen = new Set();
    const keys = new Array(ents.length), coefs = new Array(ents.length);
    for (let k = 0; k < ents.length; k++) {
      const e = this.arr(ents[k], `${W}[${k}]`, 2);
      const coef = parseNum(e[0], `${W}[${k}] coefficient`);
      const vl = e[1];
      if (!Array.isArray(vl)) reject(`${W}[${k}]: the second element of an entry must be a JSON array of 0, 1 or 2 base variable names`);
      if (vl.length > 2) reject(`${W}[${k}]: an entry has 0, 1 or 2 variables (found ${vl.length})`);
      let key = '';
      for (let q = 0; q < vl.length; q++) {
        const vn = this.baseVarNumber(vl[q]);
        if (vn < 0) reject(`${W}[${k}]: ${JSON.stringify(vl[q])} is not the name of a base variable (xi:i:k, S, C:i, s:i with labels of I)`);
        key = monMul(key, MCH(vn));
      }
      if (seen.has(key)) reject(`${W}[${k}]: repeated monomial ${monName(key)} (the monomials of the entries of one polynomial form must be pairwise different as multisets of variables)`);
      seen.add(key);
      keys[k] = key;
      coefs[k] = coef;
    }
    this.qforms.set(qn, { name, keys, coefs, den: null });
  }
  /**
   * SPEC 10: "(wx-cert-3) A step may have the optional key `centre`: a JSON object whose keys are names of base
   * variables (`xi:i:k`, `S`, `C:i`, `s:i`; labels of I; written like the form names) and whose values are numbers.
   * Every other key of that object is rejected (in particular the name of any other form; an indicator variable has
   * no name)."  Returns a Map variable number -> Q (possibly empty).
   */
  stepCentre(v, where) {
    if (!SCHEMA3) internal('the centre of a step under the schema "wx-cert-2"'); // gate at the point of use
    if (!(v instanceof Map)) reject(`${where}: the centre of a step must be a JSON object`);
    const c = new Map();
    for (const [key, val] of v) {
      const vn = this.baseVarNumber(key);
      if (vn < 0) reject(`${where}: key ${JSON.stringify(key)} is not the name of a base variable (xi:i:k, S, C:i, s:i with labels of I)`);
      c.set(vn, parseNum(val, `${where}[${JSON.stringify(key)}]`));
    }
    return c;
  }
  // <<< [SPEC 3.0]
  store(v, where) {
    this.obj(v, where, ['S', 'box', 'arc', 'rarc', 'cuts'], []);
    const S = this.interval(v.get('S'), `${where}.S`);
    const box = this.boxMap(v.get('box'), `${where}.box`, false);
    const arc = this.arcMap(v.get('arc'), `${where}.arc`, false);
    const rv = v.get('rarc');
    if (!(rv instanceof Map)) reject(`${where}.rarc: expected a JSON object`);
    const rarc = new Map();
    for (const [key, ent] of rv) {
      const W = `${where}.rarc[${JSON.stringify(key)}]`;
      const mm = /^([0-9]+)-([0-9]+)$/.exec(key);
      if (mm === null) reject(`${W}: key must be "i-j"`);
      const i = nameLabel(mm[1]), j = nameLabel(mm[2]);
      if (i < 0 || j < 0) reject(`${W}: labels must be elements of I written without leading zeros`);
      if (!(i < j)) reject(`${W}: a pair key "i-j" needs i < j`);
      this.obj(ent, W, ['lo', 'hi'], []);
      const lo = ent.get('lo') === null ? null : this.rot(ent.get('lo'), `${W}.lo`);
      const hi = ent.get('hi') === null ? null : this.rot(ent.get('hi'), `${W}.hi`);
      rarc.set(key, { i, j, lo, hi });
    }
    const cv = v.get('cuts');
    if (!(cv instanceof Map)) reject(`${where}.cuts: expected a JSON object`);
    const cuts = new Map();
    for (const [key, val] of cv) {
      const W = `${where}.cuts[${JSON.stringify(key)}]`;
      let end;
      if (key.endsWith(':lo')) end = 'lo'; else if (key.endsWith(':hi')) end = 'hi'; else reject(`${W}: key must be "NAME:lo" or "NAME:hi"`);
      const fname = key.slice(0, -3);
      const pf = this.formRef(fname, W);
      if (pf.kind === '0') reject(`${W}: no cut for the form \`0\``);
      const q = parseNum(val, W);
      let c = cuts.get(fname);
      if (c === undefined) { c = { pf, lo: undefined, hi: undefined }; cuts.set(fname, c); }
      c[end] = q;
    }
    return { S, box, arc, rarc, cuts };
  }
  round(r, where) {
    this.obj(r, where, ['pairs', 'steps', 'store'], []);
    // --- declarations
    const parSeen = new Set();
    const indSeen = new Set(); // [SPEC 3.0] 4.10: the pairs "i:j" with an `ind` declaration in this round
    const pairsIn = this.arr(r.get('pairs'), `${where}.pairs`);
    const pairs = new Array(pairsIn.length);
    for (let k = 0; k < pairsIn.length; k++) {
      const d = pairsIn[k];
      const W = `${where}.pairs[${k}]`;
      if (!(d instanceof Map)) reject(`${W}: expected a JSON object`);
      const mode = d.get('mode');
      if (mode === 'opt') {
        this.obj(d, W, ['i', 'j', 'mode', 'o', 't', 'axis', 'eps'], []);
        const [i, j] = this.pairIJ(d, W);
        const op = this.optionFields(d, W);
        // SPEC 10: "In an `opt` declaration {o,t} = {i,j}."
        if (!((op.o === i && op.t === j) || (op.o === j && op.t === i))) reject(`${W}: an opt declaration needs {o,t} = {i,j}`);
        pairs[k] = { mode, i, j, o: op.o, t: op.t, axis: op.axis, eps: op.eps };
      } else if (mode === 'par') {
        this.obj(d, W, ['i', 'j', 'mode', 'cls', 'kind'], ['kappa']);
        const [i, j] = this.pairIJ(d, W);
        const cls = this.cls(d.get('cls'), W);
        const kind = d.get('kind');
        // >>> SPEC 2.5: kind "Ps"; "kappa is required for Pk and Ps and ignored for P+, P-"
        if (kind !== 'P+' && kind !== 'P-' && kind !== 'Pk' && kind !== 'Ps') reject(`${W}: kind must be "P+", "P-", "Pk" or "Ps"`);
        let kappa = null;
        if (d.has('kappa')) kappa = parseNum(d.get('kappa'), `${W}: kappa`);
        if ((kind === 'Pk' || kind === 'Ps') && kappa === null) reject(`${W}: a ${kind} declaration needs "kappa"`);
        // <<< SPEC 2.5
        const key = `${i}:${j}:${cls}:${kind}`;
        // SPEC 10: "At most one `par` declaration per (i, j, cls, kind) in a round"
        if (parSeen.has(key)) reject(`${W}: more than one par declaration for (${i}, ${j}, ${cls}, ${kind}) in this round`);
        parSeen.add(key);
        // >>> SPEC 2.5: kappa is kept for Pk and Ps
        pairs[k] = { mode, i, j, cls, kind, kappa: (kind === 'Pk' || kind === 'Ps') ? kappa : null, key };
        // <<< SPEC 2.5
      // >>> [SPEC 3.0] sections 4.10 and 10: "(wx-cert-3) An `ind` declaration has exactly the keys `i`, `j`, `mode`,
      //     `options`; `options` is a list of 1 to 8 options {"o":..,"t":..,"axis":..,"eps":..}, pairwise different,
      //     every one with {o,t} = {i,j}.  A round has at most one `ind` declaration per pair (i, j) [R1], and no
      //     `opt` declaration of a pair that has an `ind` declaration in that round [R2, tested after the loop]; a
      //     pair {i,j} for which the node's `assume` list contains an option assumption (an item of kind "opt" with
      //     {o,t} = {i,j}) has no `ind` declaration in any round of the node [R3]".  These are well-formedness:
      //     tested here for every round of the node, evaluated or not.  Under "wx-cert-2" the mode "ind" is "not a
      //     mode" (SCHEMA RULE) and reaches the rejection of the 2.6 file below.
      } else if (SCHEMA3 && mode === 'ind') {
        this.obj(d, W, ['i', 'j', 'mode', 'options'], []);
        const [i, j] = this.pairIJ(d, W);
        const ol = this.arr(d.get('options'), `${W}.options`);
        if (ol.length < 1 || ol.length > 8) reject(`${W}.options: an ind declaration lists 1 to 8 options (found ${ol.length})`);
        const options = new Array(ol.length);
        const listed = new Set();
        for (let q = 0; q < ol.length; q++) {
          const Wo = `${W}.options[${q}]`;
          this.obj(ol[q], Wo, ['o', 't', 'axis', 'eps'], []);
          const op = this.optionFields(ol[q], Wo);
          if (!((op.o === i && op.t === j) || (op.o === j && op.t === i))) reject(`${Wo}: a listed option needs {o,t} = {i,j} = {${i},${j}}`);
          const ok = optKey(op.o, op.t, op.axis, op.eps);
          if (listed.has(ok)) reject(`${Wo}: option ${optText(op)} is listed twice (the options of an ind declaration must be pairwise different)`);
          listed.add(ok);
          options[q] = op;
        }
        const key = `${i}:${j}`;
        if (indSeen.has(key)) reject(`${W}: more than one ind declaration for the pair (${i}, ${j}) in this round (SPEC 4.10, R1)`);
        indSeen.add(key);
        if (this.assumeOptPairs.has(key)) reject(`${W}: ind declaration for the pair (${i}, ${j}), for which the node has an option assumption (SPEC 4.10, R3)`);
        pairs[k] = { mode, i, j, options, key };
      } else if (SCHEMA3) reject(`${W}: mode must be "opt", "par" or "ind"`);
      // <<< [SPEC 3.0]
      else reject(`${W}: mode must be "opt" or "par"`);
    }
    // >>> [SPEC 3.0] 4.10 (R2): "a round does not contain an `opt` declaration and an `ind` declaration of the same pair"
    if (indSeen.size !== 0) {
      for (let k = 0; k < pairs.length; k++) {
        const d = pairs[k];
        if (d.mode === 'opt' && indSeen.has(`${d.i}:${d.j}`)) reject(`${where}.pairs[${k}]: an opt declaration and an ind declaration of the same pair (${d.i}, ${d.j}) in one round (SPEC 4.10, R2)`);
      }
    }
    // <<< [SPEC 3.0]
    // --- steps
    const stepsIn = this.arr(r.get('steps'), `${where}.steps`);
    const steps = new Array(stepsIn.length);
    for (let k = 0; k < stepsIn.length; k++) {
      const s = stepsIn[k];
      const W = `${where}.steps[${k}]`;
      // [SPEC 3.0] section 10: "(wx-cert-3) A step may have the optional key `centre`" (2.6 and "wx-cert-2": no
      // optional key; there a `centre` is an unknown key, SCHEMA RULE)
      this.obj(s, W, ['form', 'sense', 'value', 'terms'], SCHEMA3 ? ['centre'] : []);
      const pf = this.formRef(s.get('form'), `${W}: form`);
      const sense = s.get('sense');
      if (sense !== 'lo' && sense !== 'hi') reject(`${W}: sense must be "lo" or "hi"`);
      const value = parseNum(s.get('value'), `${W}: value`);
      // SPEC 5 / 10 define the form `0` only with sense "lo" (see CHECKER2_NOTES.md, ambiguity A3)
      if (pf.kind === '0' && sense !== 'lo') reject(`${W}: a step with form \`0\` must have sense "lo"`);
      const termsIn = this.arr(s.get('terms'), `${W}.terms`);
      const terms = new Array(termsIn.length);
      for (let m = 0; m < termsIn.length; m++) {
        const t = termsIn[m];
        const Wt = () => `${W}.terms[${m}]`;
        if (!Array.isArray(t) || t.length !== 2) reject(`${Wt()}: a term must be [multiplier, [fact names]]`);
        const lam = typeof t[0] === 'string' ? parseNumString(t[0]) : null;
        if (lam === null) parseNum(t[0], `${Wt()}: multiplier`);
        const fl = t[1];
        if (!Array.isArray(fl)) reject(`${Wt()}: the fact list must be a JSON array`);
        // SPEC 5 / 10: "every term has 1 to 3 fact names"
        if (fl.length < 1 || fl.length > 3) reject(`${Wt()}: a term must have 1 to 3 fact names (found ${fl.length})`);
        const facts = new Array(fl.length);
        let circ = false;
        let pol = false; // [SPEC 3.0] (T2)
        for (let q = 0; q < fl.length; q++) {
          const f = this.factRef(fl[q], Wt);
          facts[q] = f;
          if (f.kind === 'circ') circ = true;
          else if (f.kind === 'pol') pol = true; // [SPEC 3.0] (T2); the kind exists only under "wx-cert-3"
        }
        // SPEC 5 / 10: "multipliers lambda >= 0 except in terms containing a `circ` fact"
        // [SPEC 3.0] section 5: this is rule (T1); it is unchanged and holds for every term, whatever names it has
        if (lam.n < 0n && !circ) reject(`${Wt()}: negative multiplier ${lam} in a term without a circ fact`);
        // [SPEC 3.0] section 5 (T2): "`pol:NAME` may occur only in a term that contains a `circ` fact."  Section 10,
        // WHERE EACH TEST IS MADE, list (W) WHOLE FILE: "the sign rule (T1) and, (wx-cert-3), the rule (T2), for every
        // term whatever its multiplier".
        if (pol && !circ) reject(`${Wt()}: a pol name in a term that contains no circ fact (SPEC 5, rule T2)`);
        terms[m] = { lam, facts };
      }
      // >>> [SPEC 3.0] sections 5 and 10: the optional `centre` of a step (null: the step has no such field and is
      //     evaluated by the RAW RULE; a Map, also an empty one: the CENTRED RULE)
      let centre = null;
      if (SCHEMA3 && s.has('centre')) centre = this.stepCentre(s.get('centre'), `${W}.centre`);
      steps[k] = { pf, sense, value, terms, centre };
      // <<< [SPEC 3.0]
    }
    const store = this.store(r.get('store'), `${where}.store`);
    return { pairs, steps, store };
  }
  close(c, where) {
    if (!(c instanceof Map)) reject(`${where}: expected a JSON object`);
    const kind = c.get('kind');
    if (kind === 'infeasible') {
      this.obj(c, where, ['kind'], ['pair']);
      let pair = null;
      if (c.has('pair')) pair = this.pairArray(c.get('pair'), `${where}.pair`);
      return { kind, pair };
    }
    if (kind === 'terminal') {
      this.obj(c, where, ['kind'], []);
      return { kind };
    }
    if (kind === 'split') {
      this.obj(c, where, ['kind', 'how', 'children'], []);
      const h = c.get('how');
      if (!(h instanceof Map)) reject(`${where}.how: expected a JSON object`);
      const W = `${where}.how`;
      const type = h.get('type');
      let how;
      if (type === 'box') {
        this.obj(h, W, ['type', 'sq', 'k', 'at'], []);
        how = { type, sq: this.label(h.get('sq'), `${W}: sq`), k: this.k12(h.get('k'), W), at: parseNum(h.get('at'), `${W}: at`) };
      } else if (type === 'arc') {
        this.obj(h, W, ['type', 'sq', 'at'], []);
        how = { type, sq: this.label(h.get('sq'), `${W}: sq`), at: this.rot(h.get('at'), `${W}: at`) };
      } else if (type === 'opt') {
        this.obj(h, W, ['type', 'pair', 'options'], []);
        const [i, j] = this.pairArray(h.get('pair'), `${W}.pair`);
        const ol = this.arr(h.get('options'), `${W}.options`);
        // SPEC 6: "with a nonempty list Lst of options of that pair"
        if (ol.length < 1) reject(`${W}.options: an option split needs at least one listed option`);
        const options = ol.map((o, k) => {
          const Wo = `${W}.options[${k}]`;
          this.obj(o, Wo, ['o', 't', 'axis', 'eps'], []);
          const op = this.optionFields(o, Wo);
          // SPEC 10: "Every option listed in an option split of the pair [i,j] has {o,t} = {i,j}."
          if (!((op.o === i && op.t === j) || (op.o === j && op.t === i))) reject(`${Wo}: a listed option needs {o,t} = {i,j} = {${i},${j}}`);
          return op;
        });
        how = { type, i, j, options };
      } else if (type === 'ysign') {
        this.obj(h, W, ['type', 'i', 'j', 'cls'], []);
        const [i, j] = this.pairIJ(h, W);
        how = { type, i, j, cls: this.cls(h.get('cls'), W) };
      } else reject(`${W}: split type must be "box", "arc", "opt" or "ysign"`);
      const ch = this.arr(c.get('children'), `${where}.children`);
      for (let k = 0; k < ch.length; k++) this.str(ch[k], `${where}.children[${k}]`);
      // SPEC 7: "the number of children is 2 for box, arc and sign splits and the number of listed options (>= 1) for an option split"
      const need = how.type === 'opt' ? how.options.length : 2;
      if (ch.length !== need) reject(`${where}.children: a ${how.type} split needs ${need} children (found ${ch.length})`);
      return { kind, how, children: ch.slice() };
    }
    reject(`${where}: close kind must be "infeasible", "terminal" or "split"`);
    return null;
  }
  /** One node object.  Well-formedness is checked on the whole node, including rounds that are not evaluated. */
  node(n) {
    if (!(n instanceof Map)) reject('node: expected a JSON object');
    const id0 = n.get('id');
    const W = typeof id0 === 'string' ? `node ${JSON.stringify(id0)}` : 'node';
    this.obj(n, W, ['id', 'parent', 'S', 'box', 'arc', 'assume', 'rounds', 'close'], ['forms']);
    const id = this.str(id0, 'node: id');
    // >>> [SPEC 3.0] section 7, TREE CONDITIONS: "a node id is a non-empty JSON string, and ids are compared as strings,
    //     character for character".  Under BOTH schemas.  This is the one rule of the final text that changes what this
    //     file does against wxcheck2_v26.js on a "wx-cert-2" certificate: the 2.6 file accepted the empty id (version
    //     note of the SPEC, item (1); SPEC_v2.6_ERRATA.md, F6).  The comparison of ids was and is by string (Map keys,
    //     after the JSON escapes have been decoded by the parser).  The `root` of the header, a `parent` and the entries
    //     of a `children` list are references to ids: an empty one can name no node and is rejected by the tree
    //     conditions as before.
    if (id.length === 0) reject('node: id must be a non-empty JSON string (found the empty string)');
    // <<< [SPEC 3.0]
    const parent = n.get('parent');
    if (parent !== null && typeof parent !== 'string') reject(`${W}: parent must be null or a JSON string`);
    const S = this.interval(n.get('S'), `${W}: S`);
    if (S[0].gt(S[1])) reject(`${W}: S_lo > S_hi`);
    const box = this.boxMap(n.get('box'), `${W}: box`, true);
    const arc = this.arcMap(n.get('arc'), `${W}: arc`, true);
    const assumeIn = this.arr(n.get('assume'), `${W}: assume`);
    const assume = assumeIn.map((a, k) => this.assumeItem(a, `${W}: assume[${k}]`));
    this.custom = new Map();
    this.formCache = new Map();
    this.factCache = new Map();
    // >>> [SPEC 3.0] section 3: "Like the custom forms, the polynomial forms belong to the node's data: they are
    //     the same in all rounds of the node and are not inherited by children."  4.10 (R3): the pairs {i,j} "for
    //     which the node has an option ASSUMPTION" (written "i:j" with i < j), for the test in Validator.round.
    this.qforms = new Map();
    this.assumeOptPairs = new Set();
    for (const a of assume) if (a.kind === 'opt') this.assumeOptPairs.add(`${Math.min(a.o, a.t)}:${Math.max(a.o, a.t)}`);
    // <<< [SPEC 3.0]
    if (n.has('forms')) this.forms(n.get('forms'), `${W}: forms`);
    const roundsIn = this.arr(n.get('rounds'), `${W}: rounds`);
    const rounds = new Array(roundsIn.length);
    for (let k = 0; k < roundsIn.length; k++) rounds[k] = this.round(roundsIn[k], `${W}: rounds[${k}]`);
    const close = this.close(n.get('close'), `${W}: close`);
    return { id, parent, S, box, arc, assume, custom: this.custom, rounds, close, qforms: this.qforms }; // [SPEC 3.0] section 3: qforms
  }
}

// ===========================================================================
// G. Node context: centre directions, polynomials of forms and of store-independent facts
// ===========================================================================

class NodeCtx {
  constructor(ref, node) {
    this.ref = ref;
    this.node = node;
    // SPEC 2: "Node-centre directions: abar_i := rho_i * u_i, bbar_i := J abar_i"
    this.abar = new Array(NL);
    this.bbar = new Array(NL);
    // SPEC 1: "q_i = p_i + xi_i1 e_i1 + xi_i2 e_i2"  (two affine polynomials per square)
    this.qx = new Array(NL);
    this.qy = new Array(NL);
    // [SPEC 2.6] section 1: the reference data in the layout of the label set in force (2.5.1: ref.u[li], ref.p[li],
    // ref.e1[li], ref.e2[li], which are the sixteen-label layout); a node with NL arcs gets the data of its NL labels
    const rd = ref.byN[NL];
    if (node.arc.length !== NL || node.box.length !== NL) internal('NodeCtx: the node was not read with the label set in force');
    for (let li = 0; li < NL; li++) {
      const rho = node.arc[li].c;
      const u = new Rot(rd.u[li][0], rd.u[li][1]);
      this.abar[li] = rho.mul(u);
      this.bbar[li] = this.abar[li].J();
      const X1 = SPoly.variable(V_XI(li, 1)), X2 = SPoly.variable(V_XI(li, 2));
      const p = rd.p[li], e1 = rd.e1[li], e2 = rd.e2[li];
      this.qx[li] = SPoly.constant(p[0]).add(X1.scaleQ(e1[0])).add(X2.scaleQ(e2[0])).normalize();
      this.qy[li] = SPoly.constant(p[1]).add(X1.scaleQ(e1[1])).add(X2.scaleQ(e2[1])).normalize();
    }
    this.fp = new Map();     // form name -> SPoly
    this.sfp = new Map();    // store-independent fact name -> SPoly
    this.assumeKeys = new Set(node.assume.map((a) => a.key));
  }
  /** SPEC 6: does the node have the option assumption (o, t, axis, eps)? */
  assumesOption(o, t, axis, eps) { return this.assumeKeys.has('opt|' + optKey(o, t, axis, eps)); }
  /** SPEC 6: does the node have the sign assumption (i, j, K, sign)? */
  assumesSign(i, j, cls, sign) { return this.assumeKeys.has('ysign|' + signKey(i, j, cls, sign)); }

  /** node-centre unit vector nbar = eps * abar (axis a) or eps * bbar (axis b)  (SPEC 4.5, 4.6) */
  nbar(li, axis, eps) {
    const base = axis === 'a' ? this.abar[li] : this.bbar[li];
    return eps > 0 ? base : base.neg();
  }
  /** corner offset w := (e1 abar_i + e2 bbar_i)/2 and J w  (SPEC 2) */
  cornerOffset(li, e1, e2) {
    const a = this.abar[li], b = this.bbar[li];
    const wx = (e1 > 0 ? a.g : a.g.neg()).add(e2 > 0 ? b.g : b.g.neg()).mul(Q.HALF);
    const wy = (e1 > 0 ? a.s : a.s.neg()).add(e2 > 0 ? b.s : b.s.neg()).mul(Q.HALF);
    return { wx, wy, Jwx: wy.neg(), Jwy: wx };
  }
  F(name) {
    let P = this.fp.get(name);
    if (P !== undefined) return P;
    const pf = parseFormName(name);
    if (pf === null) internal('bad internal form name ' + name);
    if (pf.kind === 'u') internal('custom form requested by name');
    return this.formPoly(pf);
  }
  /** Polynomial of a named form (SPEC 3). */
  formPoly(pf) {
    let P = this.fp.get(pf.name);
    if (P !== undefined) return P;
    P = this._buildForm(pf).normalize();
    this.fp.set(pf.name, P);
    return P;
  }
  _buildForm(pf) {
    switch (pf.kind) {
      case '0': return SPoly.zero();
      case 'xi': return SPoly.variable(V_XI(LIDX.get(pf.i), pf.k));
      case 'S': return SPoly.variable(V_S);
      case 'C': return SPoly.variable(V_C(LIDX.get(pf.i)));
      case 's': return SPoly.variable(V_SN(LIDX.get(pf.i)));
      case 'Da': case 'Db': {
        // SPEC 3: Da:o:t := abar_o . (q_t - q_o),  Db:o:t := bbar_o . (q_t - q_o)
        const lo = LIDX.get(pf.o), lt = LIDX.get(pf.t);
        const dx = this.qx[lt].sub(this.qx[lo]), dy = this.qy[lt].sub(this.qy[lo]);
        const nv = pf.kind === 'Da' ? this.abar[lo] : this.bbar[lo];
        return dx.scaleQ(nv.g).add(dy.scaleQ(nv.s));
      }
      case 'A': {
        // SPEC 3: A:o:t := C_o * Da_ot + s_o * Db_ot
        const lo = LIDX.get(pf.o);
        return this.F(`Da:${pf.o}:${pf.t}`).mulVar(V_C(lo)).add(this.F(`Db:${pf.o}:${pf.t}`).mulVar(V_SN(lo)));
      }
      case 'B': {
        // SPEC 3: B:o:t := C_o * Db_ot - s_o * Da_ot
        const lo = LIDX.get(pf.o);
        return this.F(`Db:${pf.o}:${pf.t}`).mulVar(V_C(lo)).sub(this.F(`Da:${pf.o}:${pf.t}`).mulVar(V_SN(lo)));
      }
      case 'Cr': {
        // SPEC 3: Cr:i:j := C_i C_j + s_i s_j
        const li = LIDX.get(pf.i), lj = LIDX.get(pf.j);
        return SPoly.variable(V_C(li)).mulVar(V_C(lj)).add(SPoly.variable(V_SN(li)).mulVar(V_SN(lj)));
      }
      case 'Sr': {
        // SPEC 3: Sr:i:j := C_i s_j - s_i C_j
        const li = LIDX.get(pf.i), lj = LIDX.get(pf.j);
        return SPoly.variable(V_C(li)).mulVar(V_SN(lj)).sub(SPoly.variable(V_SN(li)).mulVar(V_C(lj)));
      }
      case 'al': case 'be': case 'co': case 'si': case 'Y':
        return this._classForm(pf.kind, pf.i, pf.j, pf.cls);
      case 'u': {
        // SPEC 3: custom form = sum_m coef_m * F_m
        let P = SPoly.zero();
        for (const c of pf.def.comps) P = P.add(this.formPoly(c.pf).scaleQ(c.coef));
        return P;
      }
      default: internal('form kind ' + pf.kind);
    }
    return null;
  }
  /** (cbar, sbar) of SPEC 4.6: cbar := nbar_i . nbar_j, sbar := (J nbar_i) . nbar_j, i.e. conj(nbar_i) * nbar_j. */
  classBar(i, j, cls) {
    const K = classInfo(cls);
    const ni = this.nbar(LIDX.get(i), K.axI, K.epsI), nj = this.nbar(LIDX.get(j), K.axJ, K.epsJ);
    const cbar = ni.g.mul(nj.g).add(ni.s.mul(nj.s));
    const Jni = ni.J();
    const sbar = Jni.g.mul(nj.g).add(Jni.s.mul(nj.s));
    return { cbar, sbar };
  }
  /** SPEC 4.6, "Dictionary". */
  _classForm(kind, i, j, cls) {
    const K = classInfo(cls);
    const eI = Q.int(K.epsI), eJ = Q.int(K.epsJ);
    switch (kind) {
      case 'co': case 'si': {
        const { cbar, sbar } = this.classBar(i, j, cls);
        const Cr = this.F(`Cr:${i}:${j}`), Sr = this.F(`Sr:${i}:${j}`);
        // co = cbar * Cr - sbar * Sr,   si = sbar * Cr + cbar * Sr
        return kind === 'co' ? Cr.scaleQ(cbar).sub(Sr.scaleQ(sbar)) : Cr.scaleQ(sbar).add(Sr.scaleQ(cbar));
      }
      case 'al':
        // al = eps_i * A_ij if axis_i = a,  al = eps_i * B_ij if axis_i = b
        return this.F(`${K.axI === 'a' ? 'A' : 'B'}:${i}:${j}`).scaleQ(eI);
      case 'be':
        // be = - eps_j * A_ji if axis_j = a,  be = - eps_j * B_ji if axis_j = b
        return this.F(`${K.axJ === 'a' ? 'A' : 'B'}:${j}:${i}`).scaleQ(eJ.neg());
      case 'Y': {
        // J n_i . d = eps_i * B_ij (axis_i = a), = - eps_i * A_ij (axis_i = b)
        // J n_j . d = - eps_j * B_ji (axis_j = a), = + eps_j * A_ji (axis_j = b)
        const t1 = K.axI === 'a' ? this.F(`B:${i}:${j}`).scaleQ(eI) : this.F(`A:${i}:${j}`).scaleQ(eI.neg());
        const t2 = K.axJ === 'a' ? this.F(`B:${j}:${i}`).scaleQ(eJ.neg()) : this.F(`A:${j}:${i}`).scaleQ(eJ);
        return t1.add(t2);
      }
      default: internal('class form ' + kind);
    }
    return null;
  }
  /** Polynomials of facts that do not depend on the store (cached per node). */
  staticFact(key, build) {
    let P = this.sfp.get(key);
    if (P === undefined) { P = build().normalize(); this.sfp.set(key, P); }
    return P;
  }
  /** SPEC 4.1: X := (p_i + xi_i1 e_i1 + xi_i2 e_i2 + C_i w + s_i J w)_k;  lo := X, hi := S - X. */
  wallPoly(pf) {
    return this.staticFact(pf.name, () => {
      const li = LIDX.get(pf.i);
      const w = this.cornerOffset(li, pf.e1, pf.e2);
      const base = pf.k === 'x' ? this.qx[li] : this.qy[li];
      const X = base.add(SPoly.variable(V_C(li)).scaleQ(pf.k === 'x' ? w.wx : w.wy))
                    .add(SPoly.variable(V_SN(li)).scaleQ(pf.k === 'x' ? w.Jwx : w.Jwy));
      return pf.end === 'lo' ? X : SPoly.variable(V_S).sub(X);
    });
  }
  /**
   * SPEC 4.5: opt:o:t:axis:eps:e1:e2 := eps * (A_ot or B_ot) + (nbar . w) * cos(psi_t - psi_o)
   *                                     + (nbar . J w) * sin(psi_t - psi_o) - 1/2,
   * w := (e1 abar_t + e2 bbar_t)/2, nbar := eps * abar_o or eps * bbar_o;
   * cos(psi_t - psi_o) = C_o C_t + s_o s_t (= Cr of the unordered pair),
   * sin(psi_t - psi_o) = C_o s_t - s_o C_t (= +Sr_ij for (o,t) = (i,j), -Sr_ij for (o,t) = (j,i)).
   */
  optPoly(pf) {
    return this.staticFact(pf.name, () => {
      const lo = LIDX.get(pf.o), lt = LIDX.get(pf.t);
      const nb = this.nbar(lo, pf.axis, pf.eps);
      const w = this.cornerOffset(lt, pf.e1, pf.e2);
      const nw = nb.g.mul(w.wx).add(nb.s.mul(w.wy));
      const nJw = nb.g.mul(w.Jwx).add(nb.s.mul(w.Jwy));
      const base = this.F(`${pf.axis === 'a' ? 'A' : 'B'}:${pf.o}:${pf.t}`).scaleQ(Q.int(pf.eps));
      const Co = SPoly.variable(V_C(lo)), so = SPoly.variable(V_SN(lo));
      const cosrel = Co.mulVar(V_C(lt)).add(so.mulVar(V_SN(lt)));
      const sinrel = Co.mulVar(V_SN(lt)).sub(so.mulVar(V_C(lt)));
      return base.add(cosrel.scaleQ(nw)).add(sinrel.scaleQ(nJw)).sub(SPoly.constant(Q.HALF));
    });
  }
  /** SPEC 4.6, "Facts": the par polynomials of class K and kind P+, P-, Pk. */
  parPoly(pf, kappa) {
    const key = pf.pkind === 'Pk' ? `${pf.name}|${kappa}` : pf.name;
    return this.staticFact(key, () => {
      const sfx = `:${pf.i}:${pf.j}:${pf.cls}`;
      const al = this.F('al' + sfx), be = this.F('be' + sfx), co = this.F('co' + sfx), si = this.F('si' + sfx);
      const one = SPoly.constant(Q.ONE);
      if (pf.pkind === 'P+') {
        // P+:1 := be - (1 + co + si)/2,   P+:2 := al - (1 + co - si)/2
        return pf.idx === 1 ? be.sub(one.add(co).add(si).scaleQ(Q.HALF)) : al.sub(one.add(co).sub(si).scaleQ(Q.HALF));
      }
      if (pf.pkind === 'P-') {
        // P-:1 := al - (1 + co + si)/2,   P-:2 := be - (1 + co - si)/2
        return pf.idx === 1 ? al.sub(one.add(co).add(si).scaleQ(Q.HALF)) : be.sub(one.add(co).sub(si).scaleQ(Q.HALF));
      }
      // Pk:1 := al + be - 1 - co - kappa*si,   Pk:2 := al + be - 1 - co + kappa*si
      const base = al.add(be).sub(one).sub(co);
      return pf.idx === 1 ? base.sub(si.scaleQ(kappa)) : base.add(si.scaleQ(kappa));
    });
  }
  /** SPEC 4.6: asg:i:j:K:p := +Y_K,  asg:i:j:K:m := -Y_K. */
  asgPoly(pf) {
    return this.staticFact(pf.name, () => {
      const Y = this.F(`Y:${pf.i}:${pf.j}:${pf.cls}`);
      return pf.sgn > 0 ? Y.scaleQ(Q.ONE) : Y.neg();
    });
  }
  /** SPEC 4.0: circ:i := C_i^2 + s_i^2 - 1. */
  circPoly(pf) {
    return this.staticFact(pf.name, () => {
      const li = LIDX.get(pf.i);
      return SPoly.variable(V_C(li)).mulVar(V_C(li)).add(SPoly.variable(V_SN(li)).mulVar(V_SN(li))).sub(SPoly.constant(Q.ONE));
    });
  }
  /** SPEC 4.2: arc:i:tan:G:H := 1 - G C_i - H s_i. */
  arcTanPoly(pf) {
    return this.staticFact(pf.name, () => {
      const li = LIDX.get(pf.i);
      return SPoly.constant(Q.ONE).sub(SPoly.variable(V_C(li)).scaleQ(pf.G)).sub(SPoly.variable(V_SN(li)).scaleQ(pf.H));
    });
  }
  /** SPEC 4.3: rarc:i:j:tan:G:H := 1 - G Cr_ij - H Sr_ij. */
  rarcTanPoly(pf) {
    return this.staticFact(pf.name, () =>
      SPoly.constant(Q.ONE).sub(this.F(`Cr:${pf.i}:${pf.j}`).scaleQ(pf.G)).sub(this.F(`Sr:${pf.i}:${pf.j}`).scaleQ(pf.H)));
  }
  // >>> SPEC 2.5
  /** SPEC 4.6, KIND "Ps":  Ps:1 := al + be - 2 - cp * si,   Ps:2 := al + be - 2 + cm * si. */
  parPsPoly(pf, cp, cm) {
    return this.staticFact(`${pf.name}|${pf.idx === 1 ? cp : cm}`, () => {
      const sfx = `:${pf.i}:${pf.j}:${pf.cls}`;
      const base = this.F('al' + sfx).add(this.F('be' + sfx)).sub(SPoly.constant(Q.int(2)));
      const si = this.F('si' + sfx);
      return pf.idx === 1 ? base.sub(si.scaleQ(cp)) : base.add(si.scaleQ(cm));
    });
  }
  /**
   * SPEC 4.8:  wsup:i:W:p := D_W - 1/2 - (kp/2) * sigma,   wsup:i:W:m := D_W - 1/2 + (km/2) * sigma,
   * sigma := C_i * abar_i,y + s_i * bbar_i,y,  D_W := q_i,x, q_i,y, S - q_i,x, S - q_i,y for W = xlo, ylo, xhi, yhi.
   * k is kp (sign p) or km (sign m), computed by the caller from the store.
   */
  wsupPoly(pf, k) {
    return this.staticFact(`${pf.name}|${k}`, () => {
      const li = LIDX.get(pf.i);
      const sigma = SPoly.variable(V_C(li)).scaleQ(this.abar[li].s).add(SPoly.variable(V_SN(li)).scaleQ(this.bbar[li].s));
      let D;
      if (pf.wall === 'xlo') D = this.qx[li];
      else if (pf.wall === 'ylo') D = this.qy[li];
      else if (pf.wall === 'xhi') D = SPoly.variable(V_S).sub(this.qx[li]);
      else D = SPoly.variable(V_S).sub(this.qy[li]);
      const base = D.sub(SPoly.constant(Q.HALF));
      const half = k.mul(Q.HALF);
      return pf.sgn > 0 ? base.sub(sigma.scaleQ(half)) : base.add(sigma.scaleQ(half));
    });
  }
  // <<< SPEC 2.5
  // >>> [SPEC 3.0] section 3: "An entry stands for coef * v_1 * ... * v_r ...  The form is the sum of its entries"
  /** Common denominator of the coefficients of a polynomial form (kept on the definition). */
  qDen(def) {
    if (def.den === null) {
      let den = 1n;
      for (const c of def.coefs) if (c.d !== 1n && den % c.d !== 0n) den = blcm(den, c.d);
      def.den = den;
    }
    return def.den;
  }
  /**
   * The polynomial q:NAME in the array form of the step check: (1/den) * sum coefs[k] * keys[k], integer coefficients.
   * Entries with the coefficient 0 contribute nothing and are left out.  Not cached (a polynomial form is typically
   * used by one term).
   */
  qHot(def) {
    const den = this.qDen(def);
    const keys = [], coefs = [];
    for (let k = 0; k < def.keys.length; k++) {
      const c = def.coefs[k];
      if (c.n === 0n) continue;
      keys.push(def.keys[k]);
      coefs.push(c.d === den ? c.n : c.n * (den / c.d));
    }
    return { den, keys, coefs };
  }
  /** The same polynomial as an SPoly, built entry by entry with rational arithmetic (literal evaluation, --paranoid). */
  qSPoly(def) {
    let P = SPoly.zero();
    for (let k = 0; k < def.keys.length; k++) P = P.add(new SPoly(1n, new Map([[def.keys[k], 1n]])).scaleQ(def.coefs[k]));
    return P;
  }
  // <<< [SPEC 3.0]
}

// ===========================================================================
// H. Store view: store bounds SB, effective relative arcs, EMPTY test, exclusion
// ===========================================================================

/** Signal used inside SB for "empty intersection in a store bound" (SPEC 3). */
class EmptySB {
  constructor(name) { this.name = name; }
}

/** SPEC 2: "The initial store is the node's data with no relative-arc entries and no cuts." */
function initialStore(node) {
  return {
    S: node.S,
    box: node.box,
    arc: node.arc.map((a) => ({ lo: a.lo, hi: a.hi })),
    rarc: new Map(),
    cuts: new Map(),
  };
}

class StoreView {
  constructor(ctx, store) {
    this.ctx = ctx;
    this.store = store;
    this._sb = new Map();
    this._eff = new Map();
    this._ex = new Map();
    this._hlo = new Map();
    this._base = new Array(NVAR).fill(null);
  }
  /** SPEC 3: SB of a base variable (number v): box, side interval, [sin P^-, sin P^+], [min cos, cmax]. */
  baseIv(v) {
    let iv = this._base[v];
    if (iv !== null) return iv;
    const st = this.store;
    // [SPEC 2.6] section 3: the ranges of the variable numbers follow the label set (2.5.1: v < 32, v < 49, v - 33, v - 49)
    if (v < V_S) { const b = st.box[v >> 1][v & 1]; iv = new Iv(b[0], b[1]); }
    else if (v === V_S) iv = new Iv(st.S[0], st.S[1]);
    else if (v < V_SN0) { const a = st.arc[v - V_C0]; iv = new Iv(Q.min(a.lo.g, a.hi.g), cmaxOf(a.lo, a.hi)); }
    else { const a = st.arc[v - V_SN0]; iv = new Iv(a.lo.s, a.hi.s); }
    if (iv.lo.gt(iv.hi)) internal('improper base interval (the store should have been found EMPTY)');
    this._base[v] = iv;
    return iv;
  }
  /**
   * SPEC 4.3: default endpoints D^- := P_j^- * conj(P_i^+), D^+ := P_j^+ * conj(P_i^-); "among the
   * candidates {D^-, St^-} with positive cosine, R^- is the one with the larger sine; among {D^+, St^+}
   * with positive cosine, R^+ is the one with the smaller sine."  i < j labels.
   */
  effective(i, j) {
    const key = i * 32 + j;
    let e = this._eff.get(key);
    if (e !== undefined) return e;
    const ai = this.store.arc[LIDX.get(i)], aj = this.store.arc[LIDX.get(j)];
    const Dm = aj.lo.mul(ai.hi.conj());
    const Dp = aj.hi.mul(ai.lo.conj());
    const st = this.store.rarc.get(`${i}-${j}`);
    let minus = null, plus = null;
    if (Dm.g.sign() > 0) minus = Dm;
    if (st !== undefined && st.lo !== null && st.lo.g.sign() > 0 && (minus === null || st.lo.s.gt(minus.s))) minus = st.lo;
    if (Dp.g.sign() > 0) plus = Dp;
    if (st !== undefined && st.hi !== null && st.hi.g.sign() > 0 && (plus === null || st.hi.s.lt(plus.s))) plus = st.hi;
    e = { minus, plus, both: minus !== null && plus !== null };
    this._eff.set(key, e);
    return e;
  }
  /** effective endpoints of a pair for use in SB, facts and exclusion; they must be ordered there */
  effectiveOrdered(i, j) {
    const e = this.effective(i, j);
    if (e.both && e.minus.s.gt(e.plus.s)) internal(`effective relative arc of ${i}-${j} is reversed (the store should have been found EMPTY)`);
    return e;
  }
  /** "cap cut" of SPEC 3: intersect with the cut values stored under that exact name. */
  capCut(iv, name) {
    const c = this.store.cuts.get(name);
    if (c === undefined) return iv;
    let lo = iv.lo, hi = iv.hi;
    if (c.lo !== undefined && c.lo.gt(lo)) lo = c.lo;
    if (c.hi !== undefined && c.hi.lt(hi)) hi = c.hi;
    if (lo.gt(hi)) throw new EmptySB(name);
    return new Iv(lo, hi);
  }
  /** IA of an affine polynomial over the store box: [c0 + sum min(c lo, c hi), c0 + sum max(c lo, c hi)]  (SPEC 3, 4.0) */
  affineRange(P) {
    let lo = Q.ZERO, hi = Q.ZERO;
    for (const [k, c] of P.m) {
      const cq = Q.make(c, P.den);
      if (k === '') { lo = lo.add(cq); hi = hi.add(cq); continue; }
      const v = k.charCodeAt(0) - 48;
      if (k.length !== 1 || v >= V_S) internal('affineRange: not an affine polynomial in xi'); // [SPEC 2.6] section 3: xi has the numbers below V_S (2.5.1: v >= 32)
      const b = this.store.box[v >> 1][v & 1];
      const x = cq.mul(b[0]), y = cq.mul(b[1]);
      if (x.le(y)) { lo = lo.add(x); hi = hi.add(y); } else { lo = lo.add(y); hi = hi.add(x); }
    }
    return new Iv(lo, hi);
  }
  SBn(name) {
    const got = this._sb.get(name);
    if (got !== undefined) return got;
    const pf = parseFormName(name);
    if (pf === null || pf.kind === 'u') internal('SBn ' + name);
    return this.SB(pf);
  }
  /**
   * SPEC 3, "STORE BOUNDS": the interval SB(F) of a named form F, "by exactly these rules".
   * Throws EmptySB if a "cap cut" intersection is empty.
   */
  SB(pf) {
    let iv = this._sb.get(pf.name);
    if (iv !== undefined) return iv;
    iv = this._SB(pf);
    this._sb.set(pf.name, iv);
    return iv;
  }
  _SB(pf) {
    switch (pf.kind) {
      case '0': return IV_ZERO;
      // base variables: no cuts ("Cuts stored under the name of a base variable ... are NOT used in SB")
      case 'xi': return this.baseIv(V_XI(LIDX.get(pf.i), pf.k));
      case 'S': return this.baseIv(V_S);
      case 'C': return this.baseIv(V_C(LIDX.get(pf.i)));
      case 's': return this.baseIv(V_SN(LIDX.get(pf.i)));
      case 'Da': case 'Db':
        // "IA := constant + sum over xi of coefficient * SB(xi); SB := IA cap cut"
        return this.capCut(this.affineRange(this.ctx.formPoly(pf)), pf.name);
      case 'A': {
        // "(SB(C:o) * SB(Da:o:t) + SB(s:o) * SB(Db:o:t)) cap cut"
        const lo = LIDX.get(pf.o);
        const Da = this.SBn(`Da:${pf.o}:${pf.t}`), Db = this.SBn(`Db:${pf.o}:${pf.t}`);
        return this.capCut(this.baseIv(V_C(lo)).mul(Da).add(this.baseIv(V_SN(lo)).mul(Db)), pf.name);
      }
      case 'B': {
        // "(SB(C:o) * SB(Db:o:t) - SB(s:o) * SB(Da:o:t)) cap cut"
        const lo = LIDX.get(pf.o);
        const Da = this.SBn(`Da:${pf.o}:${pf.t}`), Db = this.SBn(`Db:${pf.o}:${pf.t}`);
        return this.capCut(this.baseIv(V_C(lo)).mul(Db).sub(this.baseIv(V_SN(lo)).mul(Da)), pf.name);
      }
      case 'Sr': {
        // "SB(Sr) := [sin R^-, sin R^+] cap cut ... otherwise [-1, 1] cap cut"
        const e = this.effectiveOrdered(pf.i, pf.j);
        return this.capCut(e.both ? new Iv(e.minus.s, e.plus.s) : IV_UNIT, pf.name);
      }
      case 'Cr': {
        // "SB(Cr) := [min(cos R^-, cos R^+), cmax] cap cut ... otherwise [-1, 1] cap cut"
        const e = this.effectiveOrdered(pf.i, pf.j);
        return this.capCut(e.both ? new Iv(Q.min(e.minus.g, e.plus.g), cmaxOf(e.minus, e.plus)) : IV_UNIT, pf.name);
      }
      case 'co': case 'si': {
        // "class forms: by the dictionary of 4.6 from SB(A), SB(B), SB(Cr), SB(Sr) with interval arithmetic, then cap cut"
        const { cbar, sbar } = this.ctx.classBar(pf.i, pf.j, pf.cls);
        const Cr = this.SBn(`Cr:${pf.i}:${pf.j}`), Sr = this.SBn(`Sr:${pf.i}:${pf.j}`);
        const iv = pf.kind === 'co' ? Cr.scale(cbar).sub(Sr.scale(sbar)) : Cr.scale(sbar).add(Sr.scale(cbar));
        return this.capCut(iv, pf.name);
      }
      case 'al': {
        const K = classInfo(pf.cls);
        return this.capCut(this.SBn(`${K.axI === 'a' ? 'A' : 'B'}:${pf.i}:${pf.j}`).scale(Q.int(K.epsI)), pf.name);
      }
      case 'be': {
        const K = classInfo(pf.cls);
        return this.capCut(this.SBn(`${K.axJ === 'a' ? 'A' : 'B'}:${pf.j}:${pf.i}`).scale(Q.int(-K.epsJ)), pf.name);
      }
      case 'Y': {
        const K = classInfo(pf.cls);
        const t1 = K.axI === 'a' ? this.SBn(`B:${pf.i}:${pf.j}`).scale(Q.int(K.epsI)) : this.SBn(`A:${pf.i}:${pf.j}`).scale(Q.int(-K.epsI));
        const t2 = K.axJ === 'a' ? this.SBn(`B:${pf.j}:${pf.i}`).scale(Q.int(-K.epsJ)) : this.SBn(`A:${pf.j}:${pf.i}`).scale(Q.int(K.epsJ));
        return this.capCut(t1.add(t2), pf.name);
      }
      case 'u': {
        // "custom forms u:NAME: sum_m coef_m * SB(F_m) (interval arithmetic), then cap cut"
        let iv = IV_ZERO;
        for (const c of pf.def.comps) iv = iv.add(this.SB(c.pf).scale(c.coef));
        return this.capCut(iv, pf.name);
      }
      default: internal('SB of form kind ' + pf.kind);
    }
    return null;
  }
  /**
   * SPEC 2 "A store is EMPTY if ..." and SPEC 3 "The EMPTY test ...".  Returns null if the store is not
   * EMPTY, otherwise a description of the contradiction.
   */
  emptyReason() {
    const st = this.store;
    for (let li = 0; li < NL; li++) {
      for (let k = 0; k < 2; k++) {
        if (st.box[li][k][0].gt(st.box[li][k][1])) return `lo > hi for xi:${LABELS[li]}:${k + 1}`;
      }
    }
    if (st.S[0].gt(st.S[1])) return 'S_lo > S_hi';
    for (let li = 0; li < NL; li++) {
      if (st.arc[li].lo.s.gt(st.arc[li].hi.s)) return `sin P^- > sin P^+ for the arc of square ${LABELS[li]}`;
    }
    // "every pair that has a stored relative-arc endpoint and effective endpoints on both sides (sin R^- > sin R^+)"
    for (const [key, ent] of st.rarc) {
      if (ent.lo === null && ent.hi === null) continue;
      const e = this.effective(ent.i, ent.j);
      if (e.both && e.minus.s.gt(e.plus.s)) return `sin R^- > sin R^+ for the effective relative arc of the pair ${key}`;
    }
    // "a cut pair F >= v, F <= w with v > w"
    for (const [name, c] of st.cuts) {
      if (c.lo !== undefined && c.hi !== undefined && c.lo.gt(c.hi)) return `cut pair ${name} >= ${c.lo}, ${name} <= ${c.hi}`;
    }
    // "every form that has a cut in the store, base variables excepted (empty intersection in its SB)"
    for (const [name, c] of st.cuts) {
      if (isBaseKind(c.pf.kind)) continue;
      try { this.SB(c.pf); }
      catch (e) {
        if (e instanceof EmptySB) return `empty intersection in the store bound of ${e.name}` + (e.name === name ? '' : ` (component of ${name})`);
        throw e;
      }
    }
    return null;
  }
  /**
   * SPEC 4.7: option (o, t, axis, eps) is EXCLUDED on this store iff U < 1/2 + h_lo STRICTLY.
   */
  excluded(o, t, axis, eps) {
    const key = optKey(o, t, axis, eps);
    let r = this._ex.get(key);
    if (r === undefined) {
      // "U := SBhi of the form eps*A_ot (axis a) or eps*B_ot (axis b)  (for eps = -1: U = -SBlo)"
      const sb = this.SBn(`${axis === 'a' ? 'A' : 'B'}:${o}:${t}`);
      const U = eps > 0 ? sb.hi : sb.lo.neg();
      r = U.lt(Q.HALF.add(this.hlo(o, t, axis, eps)));
      this._ex.set(key, r);
    }
    return r;
  }
  /** h_lo of SPEC 4.7 (the store of a view never changes, so the value is kept) */
  hlo(o, t, axis, eps) {
    const key = optKey(o, t, axis, eps);
    let h = this._hlo.get(key);
    if (h === undefined) { h = this._hloCompute(o, t, axis, eps); this._hlo.set(key, h); }
    return h;
  }
  _hloCompute(o, t, axis, eps) {
    const i = Math.min(o, t), j = Math.max(o, t);
    const e = this.effectiveOrdered(i, j);
    if (!e.both) return Q.HALF; // "in every other case (including: no effective relative arc) h_lo := 1/2"
    // "for (o,t) = (i,j) put Q^- := R^-, Q^+ := R^+; for (o,t) = (j,i) put Q^- := conj(R^+), Q^+ := conj(R^-)"
    let Qm, Qp;
    if (o === i) { Qm = e.minus; Qp = e.plus; }
    else { Qm = e.plus.conj(); Qp = e.minus.conj(); }
    // "Ebar := abar_t * conj(nbar), E^- := Ebar * Q^-, E^+ := Ebar * Q^+"
    const nbar = this.ctx.nbar(LIDX.get(o), axis, eps);
    const Ebar = this.ctx.abar[LIDX.get(t)].mul(nbar.conj());
    const Em = Ebar.mul(Qm), Ep = Ebar.mul(Qp);
    const rel = Ep.mul(Em.conj());
    // "If cos E^- * cos E^+ >= 0 and sin E^- * sin E^+ >= 0 and cos(E^+ * conj E^-) > 0 and sin(E^+ * conj E^-) >= 0"
    if (Em.g.sign() * Ep.g.sign() >= 0 && Em.s.sign() * Ep.s.sign() >= 0 && rel.g.sign() > 0 && rel.s.sign() >= 0) {
      // "h_lo := min(|cos E^-| + |sin E^-|, |cos E^+| + |sin E^+|)/2"
      return Q.min(Em.g.abs().add(Em.s.abs()), Ep.g.abs().add(Ep.s.abs())).mul(Q.HALF);
    }
    return Q.HALF;
  }
}

// ===========================================================================
// I. Rounds: declarations, facts, steps, store update (SPEC 4, 5)
// ===========================================================================

class RoundCtx {
  /** view: the StoreView of the store at the START of the round (must not be EMPTY). */
  constructor(ctx, view, opts) {
    this.ctx = ctx;
    this.view = view;
    this.opts = opts || {};
    this.optOK = new Set();   // options whose opt facts are available in this round
    this.parOK = new Map();   // "i:j:cls:kind" -> kappa (Q) or null
    // >>> SPEC 2.5
    this.psOK = new Map();    // kind Ps: "i:j:cls:Ps" -> {cp, cm}
    // <<< SPEC 2.5
    this.monB = new Map();    // monomial -> {lo, hi}
    this.denIds = new Map();  // denominator (hex) -> small integer
    this.denVals = [0n];
    // >>> [SPEC 3.0] sections 3 and 4.10: the `ind` declarations of THIS round and its indicator variables ("They
    //     belong to the round: the indicator variables of two rounds, also of the same node and the same pair, have
    //     nothing to do with each other": a RoundCtx is made for one round and its numbering dies with it).
    this.indDecl = new Map();   // "i:j" (i < j) -> {i, j, m, zbase, entries}: the pair's valid `ind` declaration
    this.indListed = new Map(); // key of an option -> {i, j, k}: the option is O_k of the `ind` declaration of {i,j}
    this.nz = 0;                // number of indicator variables of the round; they have the numbers NVAR .. NVAR+nz-1
    // <<< [SPEC 3.0]
  }
  /** SPEC 4.5 VALIDITY / SPEC 10 `pairs`: check every declaration of the round; a failing one rejects. */
  declare(pairs, where) {
    const ctx = this.ctx, view = this.view;
    for (let k = 0; k < pairs.length; k++) {
      const d = pairs[k];
      if (d.mode === 'opt') {
        // "iff the node assumes the option or the 7 others are excluded on the store at the start of the round"
        if (!ctx.assumesOption(d.o, d.t, d.axis, d.eps)) {
          for (const op of eightOptions(d.i, d.j)) {
            if (op.o === d.o && op.t === d.t && op.axis === d.axis && op.eps === d.eps) continue;
            if (!view.excluded(op.o, op.t, op.axis, op.eps)) {
              reject(`${where}.pairs[${k}]: opt declaration ${optText(d)}: the option is not assumed by the node and the other option ${optText(op)} of the pair is not excluded on the store at the start of the round`);
            }
          }
        }
        this.optOK.add(optKey(d.o, d.t, d.axis, d.eps));
      // >>> [SPEC 3.0] 4.10, PRECONDITION: "The declaration is VALID iff every option of the pair that is NOT in Lst
      //     is EXCLUDED on the store at the START OF THE ROUND, by the test of 4.7 exactly as it stands ...  An
      //     option of Lst may itself be excluded on that store; this does not make the declaration invalid.  A
      //     declaration that is not valid rejects the certificate".  (declare is called for evaluated rounds only;
      //     the mode "ind" exists only under "wx-cert-3", see Validator.round.)
      //     INDICATORS: "ind_k := z_{ij,k} for 1 <= k < m, ind_m := 1 - z_{ij,1} - ... - z_{ij,m-1} (for m = 1:
      //     ind_1 := 1, and the pair has no indicator variable)": the pair gets the m - 1 variable numbers
      //     zbase .. zbase + m - 2.  (R1), tested by Validator.round, makes the key "i:j" unique in the round.
      } else if (d.mode === 'ind') {
        // gate at the point of use: an `ind` declaration cannot exist under "wx-cert-2" (internal error = FAIL)
        if (!SCHEMA3) internal('an ind declaration under the schema "wx-cert-2"');
        const listed = new Set(d.options.map((op) => optKey(op.o, op.t, op.axis, op.eps)));
        for (const op of eightOptions(d.i, d.j)) {
          if (listed.has(optKey(op.o, op.t, op.axis, op.eps))) continue;
          if (!view.excluded(op.o, op.t, op.axis, op.eps)) {
            reject(`${where}.pairs[${k}]: ind declaration of the pair (${d.i}, ${d.j}): the option ${optText(op)} is not in the list and is not excluded on the store at the start of the round`);
          }
        }
        if (this.indDecl.has(d.key)) internal('two ind declarations of one pair in a round (R1 should have rejected)');
        const m = d.options.length;
        this.indDecl.set(d.key, { i: d.i, j: d.j, m, zbase: NVAR + this.nz, entries: new Array(m + 1).fill(null) });
        this.nz += m - 1;
        for (let q = 0; q < m; q++) {
          const op = d.options[q];
          // "The k-th option of the list is O_k" (section 10)
          this.indListed.set(optKey(op.o, op.t, op.axis, op.eps), { i: d.i, j: d.j, k: q + 1 });
        }
      // <<< [SPEC 3.0]
      } else {
        this._declarePar(d, `${where}.pairs[${k}]`);
        this.parOK.set(d.key, d.kappa);
      }
    }
  }
  /** SPEC 4.6 PRECONDITIONS. */
  _declarePar(d, W) {
    const ctx = this.ctx, view = this.view;
    const K = classInfo(d.cls);
    // "ITS TWO OPTIONS are O_i := (i, j, axis_i, eps_i) and O_j := (j, i, axis_j, -eps_j)"
    const Oi = optKey(d.i, d.j, K.axI, K.epsI), Oj = optKey(d.j, d.i, K.axJ, -K.epsJ);
    // >>> SPEC 2.5: kind "Ps" needs an effective relative arc (tested first, so that this reason is reported;
    //     without one, cL > 0 can only hold through a cut on co)
    if (d.kind === 'Ps' && !view.effectiveOrdered(d.i, d.j).both) reject(`${W}: par declaration Ps (${d.i}, ${d.j}, ${d.cls}): the pair has no effective relative arc`);
    // <<< SPEC 2.5
    // "every kind: the 6 options of the pair other than O_i, O_j are excluded (4.7); and cL > 0"
    for (const op of eightOptions(d.i, d.j)) {
      const key = optKey(op.o, op.t, op.axis, op.eps);
      if (key === Oi || key === Oj) continue;
      if (!view.excluded(op.o, op.t, op.axis, op.eps)) {
        reject(`${W}: par declaration (${d.i}, ${d.j}, ${d.cls}, ${d.kind}): precondition fails, option ${optText(op)} is not excluded on the store at the start of the round`);
      }
    }
    const sfx = `:${d.i}:${d.j}:${d.cls}`;
    const cL = view.SBn('co' + sfx).lo;
    if (cL.sign() <= 0) reject(`${W}: par declaration (${d.i}, ${d.j}, ${d.cls}, ${d.kind}): precondition cL > 0 fails (cL = ${cL})`);
    const Y = view.SBn('Y' + sfx);
    const onePlus = Q.ONE.add(cL);
    if (d.kind === 'P+') {
      // "(P+): YU <= 1 + cL, and (YL >= 0 or N assumes Y >= 0 for this pair and class K)"
      if (!Y.hi.le(onePlus)) reject(`${W}: par declaration P+ (${d.i}, ${d.j}, ${d.cls}): precondition YU <= 1 + cL fails (YU = ${Y.hi}, cL = ${cL})`);
      if (!(Y.lo.sign() >= 0 || ctx.assumesSign(d.i, d.j, d.cls, 1))) reject(`${W}: par declaration P+ (${d.i}, ${d.j}, ${d.cls}): precondition fails, neither YL >= 0 (YL = ${Y.lo}) nor a sign assumption Y >= 0`);
    } else if (d.kind === 'P-') {
      // "(P-): YL >= -(1 + cL), and (YU <= 0 or N assumes Y <= 0 for this pair and class K)"
      if (!Y.lo.ge(onePlus.neg())) reject(`${W}: par declaration P- (${d.i}, ${d.j}, ${d.cls}): precondition YL >= -(1 + cL) fails (YL = ${Y.lo}, cL = ${cL})`);
      if (!(Y.hi.sign() <= 0 || ctx.assumesSign(d.i, d.j, d.cls, -1))) reject(`${W}: par declaration P- (${d.i}, ${d.j}, ${d.cls}): precondition fails, neither YU <= 0 (YU = ${Y.hi}) nor a sign assumption Y <= 0`);
    } else {
      // "(Pk): with Ybar := max(|YL|, |YU|): 0 <= kappa <= 1 - Ybar/(1 + cL)"
      const Ybar = Q.max(Y.lo.abs(), Y.hi.abs());
      const bound = Q.ONE.sub(Ybar.div(onePlus));
      // >>> SPEC 2.5: this branch serves kind Pk and kind Ps ("the kappa condition of (Pk) with the declared
      //     kappa"); the two messages name the kind
      if (d.kappa.sign() < 0) reject(`${W}: par declaration ${d.kind} (${d.i}, ${d.j}, ${d.cls}): kappa = ${d.kappa} is negative`);
      if (!d.kappa.le(bound)) reject(`${W}: par declaration ${d.kind} (${d.i}, ${d.j}, ${d.cls}): precondition kappa <= 1 - Ybar/(1 + cL) fails (kappa = ${d.kappa}, Ybar = ${Ybar}, cL = ${cL})`);
      // additional preconditions of KIND "Ps"
      if (d.kind === 'Ps') {
        // "the pair has effective relative-arc endpoints R^-, R^+ on both sides (4.3)"
        const e = view.effectiveOrdered(d.i, d.j);
        if (!e.both) reject(`${W}: par declaration Ps (${d.i}, ${d.j}, ${d.cls}): the pair has no effective relative arc`);
        // "E^- := (cbar, sbar) * R^-, E^+ := (cbar, sbar) * R^+:  cos E^- > 0, cos E^+ > 0, sin E^- <= 0 <= sin E^+"
        const cs = ctx.classBar(d.i, d.j, d.cls);
        const cb = new Rot(cs.cbar, cs.sbar);
        const Em = cb.mul(e.minus), Ep = cb.mul(e.plus);
        if (!(Em.g.sign() > 0 && Ep.g.sign() > 0 && Em.s.sign() <= 0 && Ep.s.sign() >= 0)) {
          reject(`${W}: par declaration Ps (${d.i}, ${d.j}, ${d.cls}): precondition cos E^- > 0, cos E^+ > 0, sin E^- <= 0 <= sin E^+ fails (E^- = (${Em.g.toNumber()}, ${Em.s.toNumber()}), E^+ = (${Ep.g.toNumber()}, ${Ep.s.toNumber()}))`);
        }
        // "kp := (cos E^+ + sin E^+ - 1)/sin E^+ if sin E^+ > 0, else 1;
        //  km := (cos E^- - sin E^- - 1)/(-sin E^-) if sin E^- < 0, else 1"   (version 2.5: "else 1")
        const kp = Ep.s.sign() > 0 ? Ep.g.add(Ep.s).sub(Q.ONE).div(Ep.s) : Q.ONE;
        const km = Em.s.sign() < 0 ? Em.g.sub(Em.s).sub(Q.ONE).div(Em.s.neg()) : Q.ONE;
        // "cp := kp + kappa - 1, cm := km + kappa - 1; required: cp >= 0 and cm >= 0"
        const cp = kp.add(d.kappa).sub(Q.ONE), cm = km.add(d.kappa).sub(Q.ONE);
        if (cp.sign() < 0) reject(`${W}: par declaration Ps (${d.i}, ${d.j}, ${d.cls}): precondition cp >= 0 fails (cp = kp + kappa - 1 = ${cp.toNumber()}, kp = ${kp.toNumber()}, kappa = ${d.kappa})`);
        if (cm.sign() < 0) reject(`${W}: par declaration Ps (${d.i}, ${d.j}, ${d.cls}): precondition cm >= 0 fails (cm = km + kappa - 1 = ${cm.toNumber()}, km = ${km.toNumber()}, kappa = ${d.kappa})`);
        this.psOK.set(d.key, { cp, cm });
      }
      // <<< SPEC 2.5
    }
  }
  /** The polynomial of a fact in this round, with the availability rules of SPEC 4 and 10. */
  fact(pf, where) {
    // [SPEC 3.0] sections 4.9, 4.10: the three kinds of names that exist only under "wx-cert-3"
    if (pf.kind === 'sq' || pf.kind === 'pol' || pf.kind === 'ind') return this._fact3(pf, where);
    if (pf.rc === this) return pf.entry;
    const poly = this._factPoly(pf, where);
    const hot = hotOf(poly);
    const e = { poly, hot, did: this._denId(hot.den) };
    pf.rc = this;
    pf.entry = e;
    return e;
  }
  // >>> [SPEC 3.0] sections 4.9, 4.10 and 5 (T4)
  /**
   * The names `sq:NAME`, `pol:NAME`, `ind:i:j:k` in this round.  (T4): "`sq:NAME` and `pol:NAME`: iff q:NAME is
   * defined in the node's `forms` [tested by Validator.factRef for the whole file].  `ind:i:j:k`: iff the pair {i,j}
   * has an `ind` declaration in the round and 1 <= k <= m, m the length of its list."  (k >= 1 is part of the name.)
   * An entry is {poly, hot, did} like the entry of a fact; for sq and pol, `hot` and `poly` are null and `q` is the
   * definition of the form: the arrays are built when the term is expanded (_hot3, _poly3) and not kept, because
   * the square of a form is large and is typically used once.
   */
  _fact3(pf, where) {
    if (!SCHEMA3) internal('a name of version 3.0 under the schema "wx-cert-2"');
    if (pf.kind === 'ind') {
      const dcl = this.indDecl.get(`${pf.i}:${pf.j}`);
      if (dcl === undefined) reject(`${where()}: name ${pf.name} is not available in this round: the pair (${pf.i}, ${pf.j}) has no ind declaration in this round`);
      if (pf.k > dcl.m) reject(`${where()}: name ${pf.name} is not available in this round: k = ${pf.k} exceeds the length m = ${dcl.m} of the list of the ind declaration of the pair (${pf.i}, ${pf.j})`);
      let e = dcl.entries[pf.k];
      if (e === null) {
        // 4.10: "ind_k := z_{ij,k} for 1 <= k < m, ind_m := 1 - z_{ij,1} - ... - z_{ij,m-1} (for m = 1: ind_1 := 1)"
        let poly;
        if (pf.k < dcl.m) poly = SPoly.variable(dcl.zbase + pf.k - 1);
        else {
          const mm = new Map([['', 1n]]);
          for (let q = 1; q < dcl.m; q++) mm.set(MCH(dcl.zbase + q - 1), -1n);
          poly = new SPoly(1n, mm);
        }
        const hot = hotOf(poly);
        e = { poly, hot, did: this._denId(hot.den), q: null, sq: false };
        dcl.entries[pf.k] = e;
      }
      return e;
    }
    // sq:NAME := (q:NAME)^2 (a fact "in every round and for every store, without precondition"); pol:NAME := q:NAME
    const den = this.ctx.qDen(pf.qdef);
    return { poly: null, hot: null, did: this._denId(pf.kind === 'sq' ? den * den : den), q: pf.qdef, sq: pf.kind === 'sq' };
  }
  /** Array form of the polynomial of an entry (built on demand for sq and pol). */
  _hot3(e) {
    if (e.hot !== null) return e.hot;
    const h = this.ctx.qHot(e.q);
    if (!e.sq) return h;
    const s = squareHot(h);
    return { den: h.den * h.den, keys: s.keys, coefs: s.coefs };
  }
  /** SPoly of the polynomial of an entry, by plain polynomial arithmetic (literal evaluation, --paranoid). */
  _poly3(e) {
    if (e.poly !== null) return e.poly;
    const P = this.ctx.qSPoly(e.q);
    return e.sq ? P.mul(P) : P;
  }
  // <<< [SPEC 3.0]
  /** Small integer (>= 1) naming a denominator value within this round; equal values get equal numbers. */
  _denId(den) {
    const key = den.toString(16);
    let id = this.denIds.get(key);
    if (id === undefined) { id = this.denVals.length; this.denVals.push(den); this.denIds.set(key, id); }
    return id;
  }
  _unavailable(pf, where, why) {
    reject(`${where()}: fact ${pf.name} is not available in this round: ${why}`);
  }
  _factPoly(pf, where) {
    const ctx = this.ctx, st = this.view.store;
    switch (pf.kind) {
      case 'box': {
        // SPEC 4.0: box:i:k:lo := xi_ik - lo, box:i:k:hi := hi - xi_ik (store box)
        const li = LIDX.get(pf.i);
        const b = st.box[li][pf.k - 1];
        const x = SPoly.variable(V_XI(li, pf.k));
        return (pf.end === 'lo' ? x.sub(SPoly.constant(b[0])) : SPoly.constant(b[1]).sub(x)).normalize();
      }
      case 'side': {
        // SPEC 4.0: side:lo := S - S_lo, side:hi := S_hi - S
        const x = SPoly.variable(V_S);
        return (pf.end === 'lo' ? x.sub(SPoly.constant(st.S[0])) : SPoly.constant(st.S[1]).sub(x)).normalize();
      }
      case 'wall':
        return ctx.wallPoly(pf);
      case 'arc': {
        // SPEC 4.2, store endpoints P^- = (g^-, s^-), P^+ = (g^+, s^+) of square i
        const li = LIDX.get(pf.i);
        const a = st.arc[li];
        return this._arcPoly(pf.sub, SPoly.variable(V_C(li)), SPoly.variable(V_SN(li)), a.lo, a.hi).normalize();
      }
      case 'arctan':
        return ctx.arcTanPoly(pf);
      case 'rarc': case 'rarctan': {
        // SPEC 4.3: "If one side has no candidate with positive cosine, the pair has no effective relative arc (no `rarc` facts ...)"
        const e = this.view.effectiveOrdered(pf.i, pf.j);
        if (!e.both) this._unavailable(pf, where, 'the pair has no effective relative arc');
        if (pf.kind === 'rarctan') return ctx.rarcTanPoly(pf);
        return this._arcPoly(pf.sub, ctx.F(`Cr:${pf.i}:${pf.j}`), ctx.F(`Sr:${pf.i}:${pf.j}`), e.minus, e.plus).normalize();
      }
      case 'opt':
        // SPEC 10: "undeclared pairs carry no `opt`/`par` facts"
        // >>> [SPEC 3.0] section 5 (T4): "A name `opt:o:t:axis:eps:e1:e2`: iff its option is OPT-AVAILABLE (4.5) or,
        //     (wx-cert-3), IND-LISTED in the round."  4.5: "For an IND-LISTED option the four names
        //     `opt:o:t:axis:eps:e1:e2` denote the same four polynomials as above; they are then NOT facts, and they
        //     may stand in a term only under the GUARD RULE (T3)", which checkStep tests for every term.
        //     indListed is empty under "wx-cert-2" (no `ind` declaration exists there), and the message of the
        //     2.6 file is kept for a round without `ind` declarations.
        if (!SCHEMA3 && this.indListed.size !== 0) internal('an IND-LISTED option under the schema "wx-cert-2"'); // gate at the point of use
        if (!this.optOK.has(optKey(pf.o, pf.t, pf.axis, pf.eps)) && !(SCHEMA3 && this.indListed.has(optKey(pf.o, pf.t, pf.axis, pf.eps)))) {
          this._unavailable(pf, where, this.indDecl.size === 0 ? 'the option is not declared in this round'
            : 'the option has no opt declaration and is not in the list of an ind declaration of this round');
        }
        // <<< [SPEC 3.0]
        return ctx.optPoly(pf);
      case 'par': {
        const key = `${pf.i}:${pf.j}:${pf.cls}:${pf.pkind}`;
        if (!this.parOK.has(key)) this._unavailable(pf, where, 'no par declaration for this pair, class and kind in this round');
        // >>> SPEC 2.5
        if (pf.pkind === 'Ps') { const c = this.psOK.get(key); return ctx.parPsPoly(pf, c.cp, c.cm); }
        // <<< SPEC 2.5
        return ctx.parPoly(pf, this.parOK.get(key));
      }
      // >>> SPEC 2.5: wall support facts (4.8)
      case 'wsup': {
        // "let V^- := P_i^- * abar_i and V^+ := P_i^+ * abar_i (the direction a_i ITSELF at the two ends of the
        //  store arc ...  These are NOT the rotations Ab^± = rho_i * P_i^± of section 8 ...).  The facts exist only
        //  if the sign conditions  V^-_x > 0,  V^+_x > 0,  V^-_y <= 0 <= V^+_y  hold."
        // (abar_i = rho_i * u_i contains the reference direction u_i; x- and y-component of a unit vector are
        //  the fields g and s of Rot.)
        const li = LIDX.get(pf.i);
        const a = st.arc[li];
        const Vm = a.lo.mul(ctx.abar[li]), Vp = a.hi.mul(ctx.abar[li]);
        if (!(Vm.g.sign() > 0 && Vp.g.sign() > 0 && Vm.s.sign() <= 0 && Vp.s.sign() >= 0)) {
          this._unavailable(pf, where, 'the sign conditions V^-_x > 0, V^+_x > 0, V^-_y <= 0 <= V^+_y of SPEC 4.8 do not hold on the store at the start of the round (the arc does not contain the direction of the x-axis)');
        }
        // "kp := (V^+_x + V^+_y - 1)/V^+_y if V^+_y > 0, else 0; km := (V^-_x - V^-_y - 1)/(-V^-_y) if V^-_y < 0, else 0"
        let k;
        if (pf.sgn > 0) k = Vp.s.sign() > 0 ? Vp.g.add(Vp.s).sub(Q.ONE).div(Vp.s) : Q.ZERO;
        else k = Vm.s.sign() < 0 ? Vm.g.sub(Vm.s).sub(Q.ONE).div(Vm.s.neg()) : Q.ZERO;
        return ctx.wsupPoly(pf, k);
      }
      // <<< SPEC 2.5
      case 'asg':
        // SPEC 4.6: asg needs the matching sign assumption
        if (!ctx.assumesSign(pf.i, pf.j, pf.cls, pf.sgn)) this._unavailable(pf, where, 'the node has no matching sign assumption');
        return ctx.asgPoly(pf);
      case 'ivl': {
        // SPEC 4.0: ivl:F:lo := F - IAlo(F), ivl:F:hi := IAhi(F) - F over the store box (no cuts), like terms combined
        const F = ctx.formPoly(pf.form);
        const r = this.view.affineRange(F);
        return (pf.end === 'lo' ? F.sub(SPoly.constant(r.lo)) : SPoly.constant(r.hi).sub(F)).normalize();
      }
      case 'cut': {
        // SPEC 4.0: cut:F:lo := F - v and cut:F:hi := v - F for every cut in the store
        const c = st.cuts.get(pf.form.name);
        const v = c === undefined ? undefined : c[pf.end];
        if (v === undefined) this._unavailable(pf, where, 'the store at the start of the round has no such cut');
        const F = ctx.formPoly(pf.form);
        return (pf.end === 'lo' ? F.sub(SPoly.constant(v)) : SPoly.constant(v).sub(F)).normalize();
      }
      case 'circ':
        return ctx.circPoly(pf);
      default:
        internal('fact kind ' + pf.kind);
    }
    return null;
  }
  /**
   * SPEC 4.2 (and 4.3 with (Cr, Sr) in place of (C_i, s_i)), endpoints Pm = (g^-, s^-), Pp = (g^+, s^+):
   *   slo := s - s^-,  shi := s^+ - s,  clo := C - min(g^-, g^+),  chi := cmax - C,
   *   chord := (C - g^-)(s^+ - s^-) - (s - s^-)(g^+ - g^-).
   */
  _arcPoly(sub, C, s, Pm, Pp) {
    switch (sub) {
      case 'slo': return s.sub(SPoly.constant(Pm.s));
      case 'shi': return SPoly.constant(Pp.s).sub(s);
      case 'clo': return C.sub(SPoly.constant(Q.min(Pm.g, Pp.g)));
      case 'chi': return SPoly.constant(cmaxOf(Pm, Pp)).sub(C);
      case 'chord':
        return C.sub(SPoly.constant(Pm.g)).scaleQ(Pp.s.sub(Pm.s)).sub(s.sub(SPoly.constant(Pm.s)).scaleQ(Pp.g.sub(Pm.g)));
      default: internal('arc fact ' + sub);
    }
    return null;
  }
  /** SPEC 5: interval of a monomial = interval product of SB of its base variables, exponent e = e factors. */
  monBound(key) {
    let b = this.monB.get(key);
    if (b !== undefined) return b;
    let iv = IV_ONE;
    for (let i = 0; i < key.length; i++) iv = iv.mul(this.view.baseIv(key.charCodeAt(i) - 48));
    if (iv.lo.gt(iv.hi)) internal('improper monomial interval');
    b = { lo: iv.lo, hi: iv.hi, loKey: iv.lo.d.toString(16), hiKey: iv.hi.d.toString(16) };
    this.monB.set(key, b);
    return b;
  }
  /**
   * SPEC 5, STEP:  Rem := g - sum_k lambda_k * prod(facts of term k),  L := sum_m min(r_m lo_m, r_m hi_m).
   * g = gSign * (polynomial gPoly), gSign = +1 for sense "lo", -1 for sense "hi".
   * Returns L exactly as the fraction num/den (den > 0, not reduced).
   *
   * Exact integer arithmetic: every fact polynomial is (integer polynomial)/den.  Terms are collected in
   * groups of equal denominator, then brought to the common denominator D; with B the common denominator
   * of the multipliers, R_m = B * D * r_m is an integer for every monomial m.
   */
  lowerBound(gPoly, gSign, terms, entries) {
    // B := lcm of the denominators of the multipliers
    let B = 1n;
    for (let k = 0; k < terms.length; k++) {
      const b = terms[k].lam.d;
      if (b !== 1n && B % b !== 0n) B = blcm(B, b);
    }
    const groups = new Map(); // key (the denominator ids of the factors) -> {den, acc: Map monomial -> BigInt}
    const dv = this.denVals;
    const groupOf = (d1, d2, d3) => {
      // sort the (at most three) denominator ids; 0 = no factor
      let a = d1, b = d2, c = d3, t;
      if (a > b) { t = a; a = b; b = t; }
      if (b > c) { t = b; b = c; c = t; }
      if (a > b) { t = a; a = b; b = t; }
      const key = a + ',' + b + ',' + c;
      let g = groups.get(key);
      if (g === undefined) {
        let den = dv[c];
        if (b !== 0) den *= dv[b];
        if (a !== 0) den *= dv[a];
        g = { den, acc: new Map() };
        groups.set(key, g);
      }
      return g;
    };
    const accumulate = (acc, keys, coefs, mult) => {
      for (let i = 0; i < keys.length; i++) {
        const x = coefs[i] * mult;
        const y = acc.get(keys[i]);
        acc.set(keys[i], y === undefined ? x : y + x);
      }
    };
    // + B * g
    if (!gPoly.isZero()) {
      const h = hotOf(gPoly);
      const did = this._denId(h.den);
      accumulate(groupOf(0, 0, did).acc, h.keys, h.coefs, gSign > 0 ? B : -B);
    }
    // - B * lambda_k * prod(facts of term k)
    for (let k = 0; k < terms.length; k++) {
      const lam = terms[k].lam;
      if (lam.n === 0n) continue;
      const fe = entries[k];
      const mult = -(lam.d === 1n ? lam.n * B : lam.n * (B / lam.d));
      if (fe.length === 1) {
        accumulate(groupOf(0, 0, fe[0].did).acc, fe[0].hot.keys, fe[0].hot.coefs, mult);
      } else if (fe.length === 2) {
        const P = mulHot(fe[0].hot, fe[1].hot);
        accumulate(groupOf(0, fe[0].did, fe[1].did).acc, P.keys, P.coefs, mult);
      } else {
        const P = mulHot(mulHot(fe[0].hot, fe[1].hot), fe[2].hot);
        accumulate(groupOf(fe[0].did, fe[1].did, fe[2].did).acc, P.keys, P.coefs, mult);
      }
    }
    // common denominator D of the groups
    let D = 1n;
    for (const g of groups.values()) if (D % g.den !== 0n) D = blcm(D, g.den);
    // R_m := B * D * r_m
    const R = new Map();
    for (const g of groups.values()) {
      const cof = D / g.den;
      for (const [key, v] of g.acc) {
        if (v === 0n) continue;
        const x = cof === 1n ? v : v * cof;
        const y = R.get(key);
        R.set(key, y === undefined ? x : y + x);
      }
    }
    // L * B * D = sum_m min(R_m lo_m, R_m hi_m);  since lo_m <= hi_m this is R_m lo_m for R_m >= 0, R_m hi_m for R_m < 0
    const sums = new Map(); // denominator of the bound (hex) -> {d, s: integer sum of R_m * numerator}
    let nMon = 0;
    for (const [key, r] of R) {
      if (r === 0n) continue;
      nMon++;
      const mb = this.monBound(key);
      const b = r > 0n ? mb.lo : mb.hi;
      if (b.n === 0n) continue;
      const dk = r > 0n ? mb.loKey : mb.hiKey;
      const e = sums.get(dk);
      if (e === undefined) sums.set(dk, { d: b.d, s: r * b.n }); else e.s += r * b.n;
    }
    let Dl = 1n;
    for (const e of sums.values()) if (Dl % e.d !== 0n) Dl = blcm(Dl, e.d);
    let num = 0n;
    for (const e of sums.values()) num += e.s * (Dl / e.d);
    return { num, den: B * D * Dl, nMon };
  }
  /** The same L by plain rational polynomial arithmetic, literally as written in SPEC 5 (slow; option --paranoid). */
  lowerBoundReference(gPoly, gSign, terms, entries) {
    let rem = gSign > 0 ? gPoly : gPoly.neg();
    for (let k = 0; k < terms.length; k++) {
      let P = entries[k][0].poly;
      for (let q = 1; q < entries[k].length; q++) P = P.mul(entries[k][q].poly);
      rem = rem.sub(P.scaleQ(terms[k].lam));
    }
    let L = Q.ZERO;
    for (const [key, c] of rem.m) {
      const r = Q.make(c, rem.den);
      let iv = IV_ONE;
      for (let i = 0; i < key.length; i++) iv = iv.mul(this.view.baseIv(key.charCodeAt(i) - 48));
      L = L.add(Q.min(r.mul(iv.lo), r.mul(iv.hi)));
    }
    return L;
  }
  // >>> [SPEC 3.0] section 5: the step check under the schema "wx-cert-3" (TERM RULE (T3), Rem as an extended
  //     polynomial, RAW RULE, CENTRED RULE) and its literal second evaluation
  /**
   * SPEC 5 (T3), GUARD RULE: "For every name `opt:o:t:axis:eps:e1:e2` in the term whose option O = (o, t, axis, eps)
   * is IND-LISTED in the round, say O = O_k in the list of the `ind` declaration of the pair {i,j} = {o,t}: the term
   * also contains the name `ind:i:j:k` with THAT k.  This is required of every term, also of a term that contains a
   * `circ` fact.  (The indicator of another option of the pair does not serve as the guard.)"
   * facts: the parsed names of one term.  Called for the terms of evaluated rounds (section 10, WHERE EACH TEST IS
   * MADE, list (E)), whatever the multiplier of the term (section 5: "They hold for every term, whatever its
   * multiplier, also for the multiplier 0").
   */
  _guardRule(facts, where) {
    for (let q = 0; q < facts.length; q++) {
      const f = facts[q];
      if (f.kind !== 'opt') continue;
      const g = this.indListed.get(optKey(f.o, f.t, f.axis, f.eps));
      if (g === undefined) continue; // an OPT-AVAILABLE option ((R2): no option is both)
      let guarded = false;
      for (let r = 0; r < facts.length; r++) {
        const h = facts[r];
        if (h.kind === 'ind' && h.i === g.i && h.j === g.j && h.k === g.k) { guarded = true; break; }
      }
      if (!guarded) reject(`${where()}: GUARD RULE (SPEC 5, T3): the corner name ${f.name} belongs to the option O_${g.k} of the ind declaration of the pair (${g.i}, ${g.j}), and the term does not contain the name ind:${g.i}:${g.j}:${g.k}`);
    }
  }
  /**
   * SPEC 5, STEP: "The checker computes exactly, as a polynomial in the base variables and, (wx-cert-3), the
   * indicator variables of the round (an extended polynomial, section 3),
   *     Rem := g - sum_k lambda_k * prod(polynomials named in term k)
   * and a rational number L by one of two rules": the RAW RULE (centre === null: "a step without the field `centre`")
   * or the CENTRED RULE (centre: Map variable number -> Q, possibly empty: "a step with the field").
   * g = gSign * gPoly.  Returns L exactly as the fraction num/den (den > 0, not reduced), and nMon, the number of
   * monomials with a non-zero coefficient of the polynomial that the rule sums over.
   *
   * Exact integer arithmetic.  Every polynomial named in a term is (integer polynomial)/denominator.  B := the lcm
   * of the denominators of the multipliers, D := the lcm of the denominator of g and of the denominators of the
   * products of all terms.  Then R_m := B * D * r_m is an integer for every monomial m, and all R_m are collected in
   * ONE map (the 2.6 function kept one map per combination of denominators; with thousands of squares of
   * polynomial forms that would need memory proportional to terms times monomials).
   */
  lowerBound3(gPoly, gSign, terms, entries, centre) {
    const dv = this.denVals;
    let B = 1n;
    for (let k = 0; k < terms.length; k++) {
      const b = terms[k].lam.d;
      if (b !== 1n && B % b !== 0n) B = blcm(B, b);
    }
    // the denominator of the product of a term = the product of the denominators of its (at most three) factors
    const prodDen = new Map(); // the sorted denominator ids of the factors -> {den, cof}
    const denOfTerm = (fe) => {
      let a = 0, b = 0, c = fe[0].did, t;
      if (fe.length > 1) b = fe[1].did;
      if (fe.length > 2) a = fe[2].did;
      if (a > b) { t = a; a = b; b = t; }
      if (b > c) { t = b; b = c; c = t; }
      if (a > b) { t = a; a = b; b = t; }
      const key = a + ',' + b + ',' + c;
      let o = prodDen.get(key);
      if (o === undefined) {
        let den = dv[c];
        if (b !== 0) den *= dv[b];
        if (a !== 0) den *= dv[a];
        o = { den, cof: null };
        prodDen.set(key, o);
      }
      return o;
    };
    const tden = new Array(terms.length).fill(null);
    for (let k = 0; k < terms.length; k++) {
      if (terms[k].lam.n === 0n) continue; // a term with the multiplier 0 contributes nothing to Rem
      if (entries[k].length < 1 || entries[k].length > 3) internal('a term without names or with more than three');
      tden[k] = denOfTerm(entries[k]);
    }
    const gh = gPoly.isZero() ? null : hotOf(gPoly);
    let D = gh === null ? 1n : gh.den;
    for (const o of prodDen.values()) if (D % o.den !== 0n) D = blcm(D, o.den);
    // R_m := B * D * r_m
    const R = new Map();
    const accumulate = (keys, coefs, mult) => {
      for (let i = 0; i < keys.length; i++) {
        const x = coefs[i] * mult;
        const y = R.get(keys[i]);
        R.set(keys[i], y === undefined ? x : y + x);
      }
    };
    // + B * D * g
    if (gh !== null) accumulate(gh.keys, gh.coefs, (gSign > 0 ? B : -B) * (D / gh.den));
    // - B * D * lambda_k * prod(polynomials named in term k)
    for (let k = 0; k < terms.length; k++) {
      const lam = terms[k].lam;
      if (lam.n === 0n) continue;
      const fe = entries[k];
      const td = tden[k];
      if (td.cof === null) td.cof = D / td.den;
      const mult = -(lam.d === 1n ? lam.n * B : lam.n * (B / lam.d)) * td.cof;
      let P = this._hot3(fe[0]);
      for (let q = 1; q < fe.length; q++) P = mulHot(P, this._hot3(fe[q]));
      accumulate(P.keys, P.coefs, mult);
    }
    let Y = R, den = B * D;
    if (centre !== null) {
      // CENTRED RULE
      const sh = this._shift3(R, centre);
      Y = sh.Y;
      den *= sh.Dc;
    }
    return this._bound3(Y, den, centre);
  }
  /**
   * SPEC 5, CENTRED RULE: "The field gives a rational number c_v for some BASE variables v; c_v := 0 for every base
   * variable it does not give and for every indicator variable.  The checker substitutes v = c_v + y_v for every
   * variable v in Rem, expands exactly and combines like monomials in the new variables y:
   * Rem(c + y) = sum_m r_m m(y), the constant monomial included."
   * R: monomial -> integer R_m (the polynomial is (1/den) * sum R_m m).  Returns {Y, Dc} with
   * (1/(den * Dc)) * sum Y_m m(y) = the polynomial at c + y.
   *
   * With c_v = n_v / d_v in lowest terms, a monomial m = prod_v v^e_v becomes
   *   prod_v ((n_v + d_v y_v) / d_v)^e_v = (1 / prod_v d_v^e_v) * prod_v sum_{k=0..e_v} C(e_v, k) n_v^(e_v-k) d_v^k y_v^k
   * (a variable with c_v = 0 is not touched: its factor is y_v^e_v).  Dc is a common multiple of the numbers
   * prod_v d_v^e_v of all monomials: the moved variables are grouped by the VALUE delta of d_v; with
   * t_delta(m) := the sum of e_v over the variables of m with d_v = delta and T_delta := max_m t_delta(m),
   * Dc := prod_delta delta^T_delta, and Dc / prod_v d_v^e_v = prod_delta delta^(T_delta - t_delta(m)) is an integer.
   */
  _shift3(R, centre) {
    const nvar = NVAR + this.nz;
    const cn = new Array(nvar).fill(null), cd = new Array(nvar).fill(null); // numerator and denominator of c_v, for c_v != 0
    const cls = new Int32Array(nvar).fill(-1); // the number of the class delta = d_v of v (only for d_v != 1), else -1
    const deltas = [];                         // the distinct denominators other than 1
    const deltaIdx = new Map();
    let moved = 0;
    for (const [v, c] of centre) {
      if (!(v >= 0 && v < NVAR)) internal('the centre of a step names a variable that is not a base variable');
      if (c.n === 0n) continue; // c_v = 0
      moved++;
      cn[v] = c.n;
      cd[v] = c.d;
      if (c.d !== 1n) {
        const hx = c.d.toString(16);
        let ix = deltaIdx.get(hx);
        if (ix === undefined) { ix = deltas.length; deltas.push(c.d); deltaIdx.set(hx, ix); }
        cls[v] = ix;
      }
    }
    if (moved === 0) return { Y: R, Dc: 1n }; // every c_v is 0: "L is the number of the raw rule"
    const nd = deltas.length;
    const T = new Int32Array(nd), t = new Int32Array(nd);
    if (nd > 0) {
      for (const [key, r] of R) {
        if (r === 0n) continue;
        t.fill(0);
        for (let i = 0; i < key.length; i++) { const ix = cls[key.charCodeAt(i) - 48]; if (ix >= 0) t[ix]++; }
        for (let ix = 0; ix < nd; ix++) if (t[ix] > T[ix]) T[ix] = t[ix];
      }
    }
    const pw = deltas.map((d, ix) => { const a = [1n]; for (let p = 1; p <= T[ix]; p++) a.push(a[p - 1] * d); return a; }); // pw[ix][p] = delta^p
    let Dc = 1n;
    for (let ix = 0; ix < nd; ix++) Dc *= pw[ix][T[ix]];
    const cofCache = new Map(); // the exponents t (as text) -> prod_delta delta^(T_delta - t_delta)
    const wCache = new Map();   // v * 64 + e -> [C(e, k) * n_v^(e-k) * d_v^k for k = 0..e]
    const wOf = (v, e) => {
      if (e >= 64) internal('exponent of a variable too large for the centred rule');
      const id = v * 64 + e;
      let w = wCache.get(id);
      if (w === undefined) {
        w = new Array(e + 1);
        for (let k = 0; k <= e; k++) w[k] = binomBig(e, k) * (cn[v] ** BigInt(e - k)) * (cd[v] ** BigInt(k));
        wCache.set(id, w);
      }
      return w;
    };
    const Y = new Map();
    for (const [key, r] of R) {
      if (r === 0n) continue;
      let c0 = r;
      if (nd > 0) {
        t.fill(0);
        for (let i = 0; i < key.length; i++) { const ix = cls[key.charCodeAt(i) - 48]; if (ix >= 0) t[ix]++; }
        const sig = t.join(',');
        let cf = cofCache.get(sig);
        if (cf === undefined) {
          cf = 1n;
          for (let ix = 0; ix < nd; ix++) cf *= pw[ix][T[ix] - t[ix]];
          cofCache.set(sig, cf);
        }
        if (cf !== 1n) c0 = r * cf;
      }
      // the monomial variable by variable (the key is sorted, so equal variables are adjacent and every new key
      // is again sorted): ks[a] is a monomial in y, cs[a] its integer coefficient
      let ks = [''], cs = [c0];
      const n = key.length;
      let i = 0;
      while (i < n) {
        const ch = key.charCodeAt(i);
        let j = i + 1;
        while (j < n && key.charCodeAt(j) === ch) j++;
        const e = j - i, v = ch - 48;
        if (cn[v] === null) {
          const run = key.slice(i, j);
          for (let a = 0; a < ks.length; a++) ks[a] += run;
        } else {
          const w = wOf(v, e);
          const nks = [], ncs = [];
          for (let a = 0; a < ks.length; a++) {
            for (let k = 0; k <= e; k++) {
              nks.push(k === 0 ? ks[a] : ks[a] + key.slice(i, i + k));
              ncs.push(cs[a] * w[k]);
            }
          }
          ks = nks;
          cs = ncs;
        }
        i = j;
      }
      for (let a = 0; a < ks.length; a++) {
        const y = Y.get(ks[a]);
        Y.set(ks[a], y === undefined ? cs[a] : y + cs[a]);
      }
    }
    return { Y, Dc };
  }
  /**
   * SPEC 5: "L := sum_m min(r_m * lo_m, r_m * hi_m), where [lo_m, hi_m] is the product, by interval multiplication,
   * of the intervals [SBlo(v) - c_v, SBhi(v) - c_v] of the variables y_v of m (so [0, 1] for an indicator variable),
   * a variable of exponent e being multiplied e times, and [1, 1] for the constant monomial."  The RAW RULE is the
   * same sum with the intervals SB(v), i.e. with every c_v = 0 (centre === null or a variable without a value).
   * SPEC 3: "an indicator variable z_{ij,k} of the round: SB := [0, 1], for every store."
   * Y: monomial -> integer Y_m; the polynomial is (1/den) * sum Y_m m.  Returns {num, den, nMon} with L = num/den.
   *
   * Integer arithmetic: the interval of the variable v is written [a_v / q_v, b_v / q_v] with integers a_v <= b_v
   * and q_v > 0.  The interval product of such intervals is [A / Q, B / Q], Q the product of the q_v and [A, B] the
   * interval product of the integer intervals (multiplication by a positive number commutes with min and max).
   * Since A <= B: min(r A, r B) = r A for r > 0 and r B for r < 0.
   */
  _bound3(Y, den, centre) {
    const nvar = NVAR + this.nz;
    const va = new Array(nvar).fill(null), vb = new Array(nvar).fill(null), vq = new Array(nvar).fill(null);
    const setVar = (v) => {
      let lo, hi;
      if (v >= NVAR) { lo = Q.ZERO; hi = Q.ONE; } // indicator variable of the round
      else {
        const iv = this.view.baseIv(v);
        const c = centre === null ? undefined : centre.get(v);
        if (c === undefined || c.n === 0n) { lo = iv.lo; hi = iv.hi; }
        else { lo = iv.lo.sub(c); hi = iv.hi.sub(c); }
      }
      const q = lo.d === hi.d ? lo.d : blcm(lo.d, hi.d);
      va[v] = lo.n * (q / lo.d);
      vb[v] = hi.n * (q / hi.d);
      vq[v] = q;
      if (va[v] > vb[v]) internal('improper interval of a variable');
    };
    const cache = new Map([['', { A: 1n, B: 1n, Q: 1n, hex: '1' }]]); // monomial -> its interval [A/Q, B/Q]; hex = Q in hexadecimal
    const boundOf = (key) => {
      let b = cache.get(key);
      if (b !== undefined) return b;
      const p = boundOf(key.slice(0, -1));
      const v = key.charCodeAt(key.length - 1) - 48;
      if (!(v >= 0 && v < nvar)) internal('a monomial with a variable number that does not exist in this round');
      if (va[v] === null) setVar(v);
      const a = va[v], c = vb[v];
      const x1 = p.A * a, x2 = p.A * c, x3 = p.B * a, x4 = p.B * c;
      let lo = x1, hi = x1;
      if (x2 < lo) lo = x2; else if (x2 > hi) hi = x2;
      if (x3 < lo) lo = x3; else if (x3 > hi) hi = x3;
      if (x4 < lo) lo = x4; else if (x4 > hi) hi = x4;
      const one = vq[v] === 1n;
      const Qn = one ? p.Q : p.Q * vq[v];
      b = { A: lo, B: hi, Q: Qn, hex: one ? p.hex : Qn.toString(16) };
      cache.set(key, b);
      return b;
    };
    const sums = new Map(); // Q (hexadecimal) -> {d: Q, s: sum of Y_m * (A or B)}
    let nMon = 0;
    for (const [key, r] of Y) {
      if (r === 0n) continue;
      nMon++;
      const b = boundOf(key);
      const x = r > 0n ? b.A : b.B;
      if (x === 0n) continue;
      const e = sums.get(b.hex);
      if (e === undefined) sums.set(b.hex, { d: b.Q, s: r * x }); else e.s += r * x;
    }
    let Dl = 1n;
    for (const e of sums.values()) if (Dl % e.d !== 0n) Dl = blcm(Dl, e.d);
    let num = 0n;
    for (const e of sums.values()) num += e.s * (Dl / e.d);
    return { num, den: den * Dl, nMon };
  }
  /**
   * The same L by plain rational arithmetic, literally as written in SPEC 5 (slow; option --paranoid): Rem term by
   * term with rational coefficients (SPoly products, one rational per monomial); for the CENTRED RULE every single
   * occurrence of a variable v in every monomial of Rem is replaced by (c_v + y_v) and multiplied out; then
   * sum_m min(r_m lo_m, r_m hi_m) with the rational intervals [SBlo(v) - c_v, SBhi(v) - c_v] ([0, 1] for an indicator
   * variable).  Shares no code with lowerBound3 beyond the polynomials of the facts of 4.0 to 4.8.
   */
  lowerBoundReference3(gPoly, gSign, terms, entries, centre) {
    const addTo = (map, key, q) => { const y = map.get(key); map.set(key, y === undefined ? q : y.add(q)); };
    const rem = new Map(); // monomial -> Q
    for (const [key, c] of gPoly.m) addTo(rem, key, Q.make(gSign > 0 ? c : -c, gPoly.den));
    for (let k = 0; k < terms.length; k++) {
      let P = this._poly3(entries[k][0]);
      for (let q = 1; q < entries[k].length; q++) P = P.mul(this._poly3(entries[k][q]));
      const mlam = terms[k].lam.neg();
      for (const [key, c] of P.m) addTo(rem, key, Q.make(c, P.den).mul(mlam));
    }
    let poly = rem;
    if (centre !== null) {
      poly = new Map();
      for (const [key, r] of rem) {
        let part = new Map([['', r]]);
        for (let i = 0; i < key.length; i++) {
          const v = key.charCodeAt(i) - 48;
          const c = v < NVAR ? centre.get(v) : undefined; // "c_v := 0 for every base variable it does not give and for every indicator variable"
          const next = new Map();
          for (const [k2, x] of part) {
            addTo(next, monMul(k2, key[i]), x);        // y_v * part
            if (c !== undefined) addTo(next, k2, x.mul(c)); // c_v * part
          }
          part = next;
        }
        for (const [k2, x] of part) addTo(poly, k2, x);
      }
    }
    let L = Q.ZERO;
    for (const [key, r] of poly) {
      let iv = IV_ONE;
      for (let i = 0; i < key.length; i++) {
        const v = key.charCodeAt(i) - 48;
        let b;
        if (v >= NVAR) b = new Iv(Q.ZERO, Q.ONE);
        else {
          b = this.view.baseIv(v);
          const c = centre === null ? undefined : centre.get(v);
          if (c !== undefined) b = new Iv(b.lo.sub(c), b.hi.sub(c));
        }
        iv = iv.mul(b);
      }
      L = L.add(Q.min(r.mul(iv.lo), r.mul(iv.hi)));
    }
    return L;
  }
  // <<< [SPEC 3.0]
  /**
   * SPEC 5 / 10: check one step.  Returns {zero: true} for an accepted `0` step, else {zero: false}.
   * "accepted iff the claim is implied (lo: value <= L; hi: value >= -L)"; "Form `0`, sense "lo":
   * accepted iff L >= value > 0".
   */
  checkStep(step, where, stats) {
    const terms = step.terms;
    const entries = new Array(terms.length);
    for (let k = 0; k < terms.length; k++) {
      const fs_ = terms[k].facts;
      const e = new Array(fs_.length);
      const w = () => `${where}.terms[${k}]`;
      for (let q = 0; q < fs_.length; q++) e[q] = this.fact(fs_[q], w);
      // [SPEC 3.0] section 5 (T3), GUARD RULE, for every term of an evaluated round (after the availability (T4) of
      // its names, which this.fact has just tested); a round without `ind` declarations has no IND-LISTED option
      if (SCHEMA3 && this.indListed.size !== 0) this._guardRule(fs_, w);
      entries[k] = e;
    }
    const gPoly = this.ctx.formPoly(step.pf);
    const gSign = step.sense === 'lo' ? 1 : -1;
    // >>> [SPEC 3.0] section 5: under "wx-cert-3" L is computed by lowerBound3 (RAW RULE for a step without the field
    //     `centre`, CENTRED RULE for a step with it); under "wx-cert-2" by the unchanged function of the 2.6 file.
    //     The literal second evaluation (--paranoid) follows the same selection.
    //     Gate at the point of use: under "wx-cert-2" a step never carries a centre (Validator.round does not read
    //     the key there and rejects it as unknown); if one arrives all the same, that is an internal error (= FAIL).
    if (!SCHEMA3 && step.centre !== null && step.centre !== undefined) internal(`${where}: a step with a centre under the schema "wx-cert-2"`);
    const L = SCHEMA3 ? this.lowerBound3(gPoly, gSign, terms, entries, step.centre) : this.lowerBound(gPoly, gSign, terms, entries);
    if (stats) { stats.terms += terms.length; stats.monomials += L.nMon; }
    if (this.opts.paranoid) {
      const Lr = SCHEMA3 ? this.lowerBoundReference3(gPoly, gSign, terms, entries, step.centre) : this.lowerBoundReference(gPoly, gSign, terms, entries);
      if (L.num * Lr.d !== Lr.n * L.den) internal(`${where}: fast and reference evaluation of L disagree`);
    }
    // <<< [SPEC 3.0]
    // lo: value <= L ;  hi: -value <= L   (L = num/den, den > 0)
    const v = step.value;
    const lhs = (gSign > 0 ? v.n : -v.n) * L.den;
    const rhs = L.num * v.d;
    const showL = () => { const q = Q.make(L.num, L.den); return `${q.toNumber()} (exact ${q.toString().length > 200 ? 'fraction with ' + q.toString().length + ' characters' : q})`; };
    if (step.pf.kind === '0') {
      if (v.sign() <= 0) reject(`${where}: step with form \`0\` is not accepted: its value ${v} is not > 0 (need L >= value > 0)`);
      if (!(lhs <= rhs)) reject(`${where}: step with form \`0\` is not accepted: claimed value ${v} > L = ${showL()}`);
      return { zero: true, L: Q.make(L.num, L.den) }; // [SPEC 3.0] (report only): the L of an accepted `0` step, in lowest terms
    }
    if (!(lhs <= rhs)) {
      if (gSign > 0) reject(`${where}: step is not accepted: claimed ${step.pf.name} >= ${v.toNumber()} (${v}) but the certified lower bound is only L = ${showL()}`);
      else reject(`${where}: step is not accepted: claimed ${step.pf.name} <= ${v.toNumber()} (${v}) but the certified bound is only -L with L = ${showL()}`);
    }
    return { zero: false };
  }
  /**
   * SPEC 5, ROUND: "The checker accepts an entry of the new store iff it is implied as follows".
   * cert: form name -> {lo: largest certified lower bound of this round, hi: smallest certified upper bound}.
   * Returns the new store.
   */
  acceptStore(prop, cert, where) {
    const old = this.view.store, ov = this.view;
    const clo = (name) => { const c = cert.get(name); return c === undefined ? undefined : c.lo; };
    const chi = (name) => { const c = cert.get(name); return c === undefined ? undefined : c.hi; };
    const lowerOK = (nv, oldv, c) => nv.le(oldv) || (c !== undefined && nv.le(c));   // new <= old or new <= certified lower bound
    const upperOK = (nv, oldv, c) => nv.ge(oldv) || (c !== undefined && nv.ge(c));   // new >= old or new >= certified upper bound
    const show = (c) => (c === undefined ? 'none' : String(c));
    // "S_lo: new <= old or new <= a certified lower bound of `S`; S_hi: new >= old or new >= a certified upper bound."
    if (!lowerOK(prop.S[0], old.S[0], clo('S'))) reject(`${where}.S: S_lo = ${prop.S[0]} is not implied (old ${old.S[0]}, certified lower bound of S: ${show(clo('S'))})`);
    if (!upperOK(prop.S[1], old.S[1], chi('S'))) reject(`${where}.S: S_hi = ${prop.S[1]} is not implied (old ${old.S[1]}, certified upper bound of S: ${show(chi('S'))})`);
    // "box end lo_ik: new <= old, or new <= some certified lower bound of `xi:i:k`. (hi: >=, upper bound.)"
    for (let li = 0; li < NL; li++) {
      for (let k = 0; k < 2; k++) {
        const name = `xi:${LABELS[li]}:${k + 1}`;
        const nb = prop.box[li][k], ob = old.box[li][k];
        if (!lowerOK(nb[0], ob[0], clo(name))) reject(`${where}.box: lower end ${nb[0]} of ${name} is tighter than certified (old ${ob[0]}, certified lower bound: ${show(clo(name))})`);
        if (!upperOK(nb[1], ob[1], chi(name))) reject(`${where}.box: upper end ${nb[1]} of ${name} is tighter than certified (old ${ob[1]}, certified upper bound: ${show(chi(name))})`);
      }
    }
    // "arc endpoint P_i^-: cos > 0 required; sin(new) <= sin(old) or sin(new) <= a certified lower bound of `s:i`.
    //  P_i^+: cos > 0; sin(new) >= sin(old) or >= a certified upper bound of `s:i`."
    for (let li = 0; li < NL; li++) {
      const name = `s:${LABELS[li]}`;
      const na = prop.arc[li], oa = old.arc[li];
      if (na.lo.g.sign() <= 0) reject(`${where}.arc[${LABELS[li]}].lo: endpoint with non-positive cosine`);
      if (na.hi.g.sign() <= 0) reject(`${where}.arc[${LABELS[li]}].hi: endpoint with non-positive cosine`);
      if (!lowerOK(na.lo.s, oa.lo.s, clo(name))) reject(`${where}.arc[${LABELS[li]}].lo: sine ${na.lo.s} is tighter than certified (old ${oa.lo.s}, certified lower bound of ${name}: ${show(clo(name))})`);
      if (!upperOK(na.hi.s, oa.hi.s, chi(name))) reject(`${where}.arc[${LABELS[li]}].hi: sine ${na.hi.s} is tighter than certified (old ${oa.hi.s}, certified upper bound of ${name}: ${show(chi(name))})`);
    }
    // "stored relative-arc endpoint St^- of pair i<j: allowed only if, in the old store, D^- or a stored St^- has
    //  positive cosine ...; cos(new) > 0 required; sin(new) <= sin(old R^-) or sin(new) <= a certified lower bound
    //  of `Sr:i:j`.  St^+ symmetrically"
    for (const [key, ent] of prop.rarc) {
      const name = `Sr:${ent.i}:${ent.j}`;
      const oe = ov.effective(ent.i, ent.j);
      if (ent.lo !== null) {
        if (oe.minus === null) reject(`${where}.rarc[${key}].lo: not allowed: in the old store neither D^- nor a stored endpoint has positive cosine`);
        if (ent.lo.g.sign() <= 0) reject(`${where}.rarc[${key}].lo: endpoint with non-positive cosine`);
        if (!lowerOK(ent.lo.s, oe.minus.s, clo(name))) reject(`${where}.rarc[${key}].lo: sine ${ent.lo.s} is tighter than certified (old R^- sine ${oe.minus.s}, certified lower bound of ${name}: ${show(clo(name))})`);
      }
      if (ent.hi !== null) {
        if (oe.plus === null) reject(`${where}.rarc[${key}].hi: not allowed: in the old store neither D^+ nor a stored endpoint has positive cosine`);
        if (ent.hi.g.sign() <= 0) reject(`${where}.rarc[${key}].hi: endpoint with non-positive cosine`);
        if (!upperOK(ent.hi.s, oe.plus.s, chi(name))) reject(`${where}.rarc[${key}].hi: sine ${ent.hi.s} is tighter than certified (old R^+ sine ${oe.plus.s}, certified upper bound of ${name}: ${show(chi(name))})`);
      }
    }
    // "cut "F >= v": v <= old cut value of the same name, or v <= a certified lower bound of F.  Cut "F <= v":
    //  v >= old value or v >= a certified upper bound of F."
    for (const [name, c] of prop.cuts) {
      const oc = old.cuts.get(name);
      if (c.lo !== undefined) {
        const ok = (oc !== undefined && oc.lo !== undefined && c.lo.le(oc.lo)) || (clo(name) !== undefined && c.lo.le(clo(name)));
        if (!ok) reject(`${where}.cuts: cut ${name} >= ${c.lo} is not implied (old cut: ${show(oc === undefined ? undefined : oc.lo)}, certified lower bound: ${show(clo(name))})`);
      }
      if (c.hi !== undefined) {
        const ok = (oc !== undefined && oc.hi !== undefined && c.hi.ge(oc.hi)) || (chi(name) !== undefined && c.hi.ge(chi(name)));
        if (!ok) reject(`${where}.cuts: cut ${name} <= ${c.hi} is not implied (old cut: ${show(oc === undefined ? undefined : oc.hi)}, certified upper bound: ${show(chi(name))})`);
      }
    }
    return { S: prop.S, box: prop.box, arc: prop.arc, rarc: prop.rarc, cuts: prop.cuts };
  }
}

// ===========================================================================
// J. Node check and closure (SPEC 5 ROUND, 7(a), 7(b), 8, local part of 6)
// ===========================================================================

/** SPEC 8, TERMINAL TEST for a final store and a tube.  Returns null if passed, else the reason. */
function terminalTest(node, store, tube) {
  for (let li = 0; li < NL; li++) {
    for (let k = 0; k < 2; k++) {
      const b = store.box[li][k], t = tube.box[li][k];
      // "the store box is contained in the tube box coordinate-wise"
      if (b[0].lt(t[0]) || b[1].gt(t[1])) return `the store interval [${b[0]}, ${b[1]}] of xi:${LABELS[li]}:${k + 1} is not contained in the tube interval [${t[0]}, ${t[1]}]`;
    }
  }
  for (let li = 0; li < NL; li++) {
    // "for every i the absolute endpoints Ab^± := rho_i * P_i^± (store endpoints) satisfy cos Ab^± > 0 and
    //  |sin Ab^±| <= alphaT_i - alphaT_i^3/6"
    const a = tube.alpha[li];
    const bound = a.sub(a.mul(a).mul(a).div(Q.int(6)));
    const rho = node.arc[li].c;
    // >>> [SPEC 3.0] section 8, TERMINAL TEST: "for every i the endpoints relative to the tube's centre
    //     Ab^± := conj(gammaT_i) * rho_i * P_i^±  (gammaT_i the tube's centre for i, rho_i the node's centre, P_i^±
    //     the store endpoints) satisfy cos Ab^± > 0 and |sin Ab^±| <= alphaT_i - alphaT_i^3/6."  "If no centres are
    //     given, and always under the schema "wx-cert-2", gamma_i is the identity": then (tube.centre is null or
    //     undefined) Ab^± = rho_i * P_i^± and the two messages are those of the 2.6 file.
    //     Gate at the point of use: centres are used only under "wx-cert-3"; a tube that carries centres under
    //     "wx-cert-2" cannot come from Validator.region and is an internal error (= FAIL), never a silent use.
    if (!SCHEMA3 && tube.centre) internal('terminalTest: a tube with centres under the schema "wx-cert-2"');
    const gamma = SCHEMA3 && tube.centre ? tube.centre[li] : null;
    const rel = gamma === null ? rho : gamma.conj().mul(rho);
    const what = gamma === null ? 'absolute arc endpoint' : 'arc endpoint relative to the tube\'s centre';
    for (const end of ['lo', 'hi']) {
      const Ab = rel.mul(store.arc[li][end]);
      if (Ab.g.sign() <= 0) return `${what} (${end}) of square ${LABELS[li]} has non-positive cosine`;
      if (Ab.s.abs().gt(bound)) return `${what} (${end}) of square ${LABELS[li]} is outside the tube: |sin| = ${Ab.s.abs().toNumber()} > alphaT - alphaT^3/6 = ${bound.toNumber()}`;
    }
    // <<< [SPEC 3.0]
  }
  return null;
}

/**
 * Check one node alone (SPEC 10: "A node object can be checked alone (result: accepted, with its final
 * store)").  env: {ref, header, opts, stats}.  Throws Reject; returns {finalStore, emptyFinal, ...}.
 */
function checkNode(env, node) {
  const W = `node ${JSON.stringify(node.id)}`;
  const stats = env.stats;
  const ctx = new NodeCtx(env.ref, node);
  let store = initialStore(node);
  let view = new StoreView(ctx, store);
  let er = view.emptyReason();
  if (er !== null) internal(`${W}: the initial store is EMPTY (${er}) although the node data are well-formed`);
  let zeroStep = null;   // where an accepted `0` step was found
  let zeroStepL = null;  // [SPEC 3.0] (report only): the L of that step, the FIRST accepted `0` step of the node (Q)
  let emptyAfter = null; // {round, reason} if the store after a round is EMPTY
  let evaluated = 0;
  for (let r = 0; r < node.rounds.length; r++) {
    const round = node.rounds[r];
    const Wr = `${W}: rounds[${r}]`;
    // SPEC 5: "All steps of a round are evaluated with the facts and store bounds of the store at the START of the round."
    const rc = new RoundCtx(ctx, view, env.opts);
    rc.declare(round.pairs, Wr);
    const cert = new Map();
    let zeroHere = false;
    for (let k = 0; k < round.steps.length; k++) {
      const step = round.steps[k];
      const res = rc.checkStep(step, `${Wr}.steps[${k}]`, stats);
      if (res.zero) { zeroHere = true; if (zeroStep === null) { zeroStep = `rounds[${r}].steps[${k}]`; zeroStepL = res.L; /* [SPEC 3.0] report only */ } continue; }
      // SPEC 5: "THE CERTIFIED VALUE OF AN ACCEPTED STEP IS ITS `value`"
      let c = cert.get(step.pf.name);
      if (c === undefined) { c = { lo: undefined, hi: undefined }; cert.set(step.pf.name, c); }
      if (step.sense === 'lo') { if (c.lo === undefined || step.value.gt(c.lo)) c.lo = step.value; }
      else { if (c.hi === undefined || step.value.lt(c.hi)) c.hi = step.value; }
    }
    if (stats) { stats.steps += round.steps.length; stats.declarations += round.pairs.length; }
    store = rc.acceptStore(round.store, cert, `${Wr}.store`);
    view = new StoreView(ctx, store);
    evaluated++;
    er = view.emptyReason();
    // SPEC 5: "If a round contains an accepted `0` step, or the store after a round is EMPTY, later rounds of the
    // node are not evaluated."
    if (er !== null) { emptyAfter = { round: r, reason: er }; break; }
    if (zeroHere) break;
  }
  if (stats) { stats.roundsEvaluated += evaluated; stats.roundsSkipped += node.rounds.length - evaluated; }
  // SPEC 10: "The final store of a node is the store after its last evaluated round."
  const close = node.close;
  const emptyFinal = emptyAfter !== null;
  let evidence = null;
  if (close.kind === 'infeasible') {
    // SPEC 7(a) / 10: "A node with close kind "infeasible" must contain evidence: a `0` step with L > 0, or an
    // empty store after some round, or (form with "pair") all 8 options of the named pair excluded on the final store."
    // >>> SPEC 2.5.1 (section 10): "The form {"kind":"infeasible"} is accepted iff some evaluated round contains an
    //     accepted `0` step or the store after some evaluated round is EMPTY.  The form
    //     {"kind":"infeasible","pair":[i,j]} is accepted iff the node's final store is NOT EMPTY and all 8 options
    //     of the named pair are excluded (4.7) on it (other evidence in the node does not replace this test)."
    //     (wxcheck2_v23.js accepted any of the three kinds of evidence and examined the pair only without the
    //     other two.)
    if (close.pair !== null) {
      const [i, j] = close.pair;
      if (emptyFinal) reject(`${W}: close "infeasible" with pair [${i}, ${j}]: the final store is EMPTY (${emptyAfter.reason}); the pair form needs a final store that is not EMPTY (the form {"kind":"infeasible"} applies)`);
      for (const op of eightOptions(i, j)) {
        if (!view.excluded(op.o, op.t, op.axis, op.eps)) reject(`${W}: close "infeasible" with pair [${i}, ${j}]: option ${optText(op)} is not excluded on the final store (other evidence in the node does not replace this test)`);
      }
      evidence = `all 8 options of the pair [${i}, ${j}] are excluded on the final store`;
    } else if (zeroStep !== null) evidence = `accepted \`0\` step at ${zeroStep}`;
    else if (emptyFinal) evidence = `EMPTY store after rounds[${emptyAfter.round}]: ${emptyAfter.reason}`;
    else reject(`${W}: close "infeasible" without evidence (no accepted \`0\` step, no EMPTY store after a round, no "pair")`);
    // <<< SPEC 2.5.1
  } else {
    // SPEC 10: "If the new store is empty in the sense of section 2, the node is infeasible and must have close kind "infeasible"."
    if (emptyFinal) reject(`${W}: the store after rounds[${emptyAfter.round}] is EMPTY (${emptyAfter.reason}); the node must have close kind "infeasible", not "${close.kind}"`);
    if (close.kind === 'terminal') {
      // SPEC 7(b): "its final store passes the terminal test of section 8"
      const why = terminalTest(node, store, env.header.terminal);
      if (why !== null) reject(`${W}: close "terminal": the terminal test fails: ${why}`);
    } else {
      const h = close.how;
      if (h.type === 'box') {
        // SPEC 6: "box split of coordinate (i,k) at a rational m with lo <= m <= hi (St's interval)"
        const b = store.box[LIDX.get(h.sq)][h.k - 1];
        if (h.at.lt(b[0]) || h.at.gt(b[1])) reject(`${W}: box split of xi:${h.sq}:${h.k} at ${h.at}: the split point is outside the final store interval [${b[0]}, ${b[1]}]`);
      } else if (h.type === 'arc') {
        // SPEC 6: "arc split of square i at a rotation M (relative to N's centre) with cos M > 0 and
        // sin P^- <= sin M <= sin P^+ (St's endpoints)"
        const a = store.arc[LIDX.get(h.sq)];
        if (h.at.g.sign() <= 0) reject(`${W}: arc split of square ${h.sq}: the split rotation has non-positive cosine`);
        if (h.at.s.lt(a.lo.s) || h.at.s.gt(a.hi.s)) reject(`${W}: arc split of square ${h.sq}: sin M = ${h.at.s} is outside [sin P^-, sin P^+] = [${a.lo.s}, ${a.hi.s}] of the final store`);
      } else if (h.type === 'opt') {
        // SPEC 6: "every option of the pair NOT in Lst is excluded (4.7) on St"
        const listed = new Set(h.options.map((op) => optKey(op.o, op.t, op.axis, op.eps)));
        for (const op of eightOptions(h.i, h.j)) {
          if (listed.has(optKey(op.o, op.t, op.axis, op.eps))) continue;
          if (!view.excluded(op.o, op.t, op.axis, op.eps)) reject(`${W}: option split of the pair [${h.i}, ${h.j}]: the unlisted option ${optText(op)} is not excluded on the final store`);
        }
      }
      // ysign split: no condition on the final store (SPEC 6)
    }
  }
  // [SPEC 3.0] (report only, no checking rule): zeroStepL is the L of the first accepted `0` step, as a string "p/q"
  // in lowest terms or "p", if the node is CLOSED AS INFEASIBLE BY that step, i.e. its close object is
  // {"kind":"infeasible"} without "pair" and the evidence used above is the `0` step; otherwise null.
  const zeroClosed = close.kind === 'infeasible' && close.pair === null && zeroStep !== null;
  return { finalStore: store, emptyFinal, evaluated, evidence, zeroStep, zeroStepL: zeroClosed ? zeroStepL.toString() : null };
}

/** Canonical text of a store (for the digest written by --json; see CHECKER2_NOTES.md). */
function canonicalStore(store) {
  const out = [];
  out.push(`S ${store.S[0]} ${store.S[1]}`);
  for (let li = 0; li < NL; li++) {
    const b = store.box[li];
    out.push(`box ${LABELS[li]} ${b[0][0]} ${b[0][1]} ${b[1][0]} ${b[1][1]}`);
  }
  for (let li = 0; li < NL; li++) {
    const a = store.arc[li];
    out.push(`arc ${LABELS[li]} ${a.lo.g} ${a.lo.s} ${a.hi.g} ${a.hi.s}`);
  }
  const rk = Array.from(store.rarc.values()).filter((e) => e.lo !== null || e.hi !== null).sort((x, y) => (x.i - y.i) || (x.j - y.j));
  for (const e of rk) out.push(`rarc ${e.i}-${e.j} ${e.lo === null ? 'null' : e.lo.g + ' ' + e.lo.s} ${e.hi === null ? 'null' : e.hi.g + ' ' + e.hi.s}`);
  const names = Array.from(store.cuts.keys()).sort();
  for (const name of names) {
    const c = store.cuts.get(name);
    if (c.lo !== undefined) out.push(`cut ${name}:lo ${c.lo}`);
    if (c.hi !== undefined) out.push(`cut ${name}:hi ${c.hi}`);
  }
  return out.join('\n') + '\n';
}
function storeDigest(store) {
  return crypto.createHash('sha256').update(canonicalStore(store), 'utf8').digest('hex');
}

// ===========================================================================
// K. Tree pass (SPEC 6, 7, 8)
// ===========================================================================

/**
 * SPEC 6, ARC CONTAINMENT TEST: the arc of a node with centre rho' = cc and endpoints P'^- = cLo, P'^+ = cHi
 * contains the arc [A^-, A^+] given relative to a centre rho.  "delta := rho * conj(rho'), At^- := A^- * delta,
 * At^+ := A^+ * delta.  Required: cos At^- > 0, cos At^+ > 0, sin P'^- <= sin At^-, sin At^+ <= sin P'^+."
 * Returns null if contained, else the reason.
 */
function arcContainment(cc, cLo, cHi, rho, Am, Ap) {
  const delta = rho.mul(cc.conj());
  const Atm = Am.mul(delta), Atp = Ap.mul(delta);
  if (Atm.g.sign() <= 0) return 're-expressed lower endpoint has non-positive cosine';
  if (Atp.g.sign() <= 0) return 're-expressed upper endpoint has non-positive cosine';
  if (cLo.s.gt(Atm.s)) return `lower endpoint not covered (sin P'^- = ${cLo.s.toNumber()} > sin At^- = ${Atm.s.toNumber()})`;
  if (Atp.s.gt(cHi.s)) return `upper endpoint not covered (sin At^+ = ${Atp.s.toNumber()} > sin P'^+ = ${cHi.s.toNumber()})`;
  return null;
}

function assumeText(a) {
  return a.kind === 'opt' ? `opt ${optText(a)}` : `ysign (${a.i}, ${a.j}, ${a.cls}, ${a.sign > 0 ? '+1' : '-1'})`;
}

/**
 * SPEC 6: the rules for child number l (0-based position in the split's `children` list) of a split node.
 * P: {id, assume, arcC (centres), split (how), final (final store)};  C: child node data {id, S, box, arc, assume}.
 */
function checkChild(P, C, l) {
  const W = `node ${JSON.stringify(C.id)} as child ${l + 1} of ${JSON.stringify(P.id)}`;
  const h = P.split, St = P.final;
  // "every child's `assume` list equals N's list, in the same order, followed by the one additional assumption as
  //  its last item (no additional item for box and arc splits)"
  let extra = null;
  if (h.type === 'opt') { const op = h.options[l]; extra = 'opt|' + optKey(op.o, op.t, op.axis, op.eps); }
  else if (h.type === 'ysign') extra = 'ysign|' + signKey(h.i, h.j, h.cls, l === 0 ? 1 : -1); // "children: sign +1 first, then -1"
  const want = P.assume.map((a) => a.key);
  if (extra !== null) want.push(extra);
  const have = C.assume.map((a) => a.key);
  if (have.length < want.length) reject(`${W}: assumption list has ${have.length} items, expected ${want.length} (the parent's list${extra !== null ? ' followed by the split assumption' : ''}): missing assumption`);
  if (have.length > want.length) reject(`${W}: assumption list has ${have.length} items, expected ${want.length} (the parent's list${extra !== null ? ' followed by the split assumption' : ''}): extra assumption`);
  for (let k = 0; k < want.length; k++) {
    if (have[k] !== want[k]) reject(`${W}: assumption ${k + 1} is ${assumeText(C.assume[k])}, expected ${want[k].replace('|', ' ')} (the parent's list in the same order${extra !== null ? ', then the split assumption' : ''})`);
  }
  // "the child's side interval contains St's side interval"
  if (C.S[0].gt(St.S[0]) || C.S[1].lt(St.S[1])) reject(`${W}: side interval [${C.S[0]}, ${C.S[1]}] does not contain the parent's final side interval [${St.S[0]}, ${St.S[1]}]`);
  // box
  for (let li = 0; li < NL; li++) {
    for (let k = 0; k < 2; k++) {
      let lo = St.box[li][k][0], hi = St.box[li][k][1];
      if (h.type === 'box' && LIDX.get(h.sq) === li && h.k === k + 1) {
        // "child 1's interval for (i,k) contains [lo, m], child 2's contains [m, hi]"
        if (l === 0) hi = h.at; else lo = h.at;
      }
      const c = C.box[li][k];
      if (c[0].gt(lo) || c[1].lt(hi)) reject(`${W}: box interval [${c[0]}, ${c[1]}] of xi:${LABELS[li]}:${k + 1} does not contain [${lo}, ${hi}] (smaller than the parent's final store)`);
    }
  }
  // arcs (ARC CONTAINMENT TEST, centres may differ)
  for (let li = 0; li < NL; li++) {
    let Am = St.arc[li].lo, Ap = St.arc[li].hi;
    if (h.type === 'arc' && LIDX.get(h.sq) === li) {
      // "child 1's arc contains [P^-, M], child 2's contains [M, P^+]"
      if (l === 0) Ap = h.at; else Am = h.at;
    }
    const why = arcContainment(C.arc[li].c, C.arc[li].lo, C.arc[li].hi, P.arcC[li], Am, Ap);
    if (why !== null) reject(`${W}: arc of square ${LABELS[li]} does not contain the required arc of the parent's final store: ${why}`);
  }
}

/** SPEC 7 ROOT CONDITIONS and SPEC 8 ROOT CONTAINS WINDOW. */
function checkRoot(node, header) {
  const W = `root node ${JSON.stringify(node.id)}`;
  if (node.parent !== null) reject(`${W}: the root must have parent = null`);
  if (node.assume.length !== 0) reject(`${W}: the root must have an EMPTY assumption list (found ${node.assume.length} assumptions)`);
  // [SPEC 2.6] section 7, ROOT CONDITIONS: "S_lo <= S_floor (= 4 without the header field)" (2.5.1: "S_lo <= 4").
  // header.S_floor is the value read by Validator.header (4 if the field is absent); without the field the
  // message is the one of 2.5.1.
  if (!(header.S_floor instanceof Q)) internal('checkRoot: the header carries no S_floor (it was not read by Validator.header)');
  if (node.S[0].gt(header.S_floor)) reject(`${W}: the root needs S_lo <= ${header.S_floorGiven ? 'S_floor = ' : ''}${header.S_floor} (found ${node.S[0]})`);
  if (node.S[1].lt(header.Sref)) reject(`${W}: the root needs S_hi >= Sref (found S_hi = ${node.S[1]})`);
  const win = header.window;
  for (let li = 0; li < NL; li++) {
    for (let k = 0; k < 2; k++) {
      // "the root box contains the window box coordinate-wise"
      const b = node.box[li][k], w = win.box[li][k];
      if (b[0].gt(w[0]) || b[1].lt(w[1])) reject(`${W}: the root box does not contain the window: xi:${LABELS[li]}:${k + 1} root [${b[0]}, ${b[1]}], window [${w[0]}, ${w[1]}]`);
    }
  }
  for (let li = 0; li < NL; li++) {
    // "with the absolute endpoints Ab^± := rho_i * P_i^±: cos Ab^- > 0, cos Ab^+ > 0, sin Ab^+ >= alpha_i, sin Ab^- <= -alpha_i"
    const a = node.arc[li];
    // >>> [SPEC 3.0] section 8, ROOT CONTAINS WINDOW: "for every i, with the endpoints relative to the window's centre
    //     Ab^± := conj(gamma_i) * rho_i * P_i^±  (gamma_i the window's centre for i, rho_i and P_i^± the root's centre
    //     and endpoints; with the identity as centre this is rho_i * P_i^±, the absolute endpoint of version 2.6):
    //     cos Ab^- > 0, cos Ab^+ > 0, sin Ab^+ >= alpha_i, sin Ab^- <= -alpha_i."  Without centres (win.centre is
    //     null or undefined; always under "wx-cert-2") the two products are those of the 2.6 file:
    //     2.6: const Abm = a.c.mul(a.lo), Abp = a.c.mul(a.hi);
    //     Gate at the point of use: centres are used only under "wx-cert-3" (the schema of THIS header, which must be
    //     the schema in force); a window that carries centres under "wx-cert-2" cannot come from Validator.region
    //     and is an internal error (= FAIL), never a silent use.
    if (header.schema3 !== undefined && header.schema3 !== SCHEMA3) internal('checkRoot: the schema in force is not the schema of this header');
    if (!SCHEMA3 && win.centre) internal('checkRoot: a window with centres under the schema "wx-cert-2"');
    const gamma = SCHEMA3 && win.centre ? win.centre[li] : null;
    const rel = gamma === null ? a.c : gamma.conj().mul(a.c);
    const Abm = rel.mul(a.lo), Abp = rel.mul(a.hi);
    if (gamma !== null) {
      if (Abm.g.sign() <= 0 || Abp.g.sign() <= 0) reject(`${W}: the root does not contain the window: an arc endpoint of square ${LABELS[li]} relative to the window's centre has non-positive cosine`);
    }
    // <<< [SPEC 3.0]
    if (Abm.g.sign() <= 0 || Abp.g.sign() <= 0) reject(`${W}: the root does not contain the window: an absolute arc endpoint of square ${LABELS[li]} has non-positive cosine`);
    if (Abp.s.lt(win.alpha[li])) reject(`${W}: the root does not contain the window: sin Ab^+ = ${Abp.s.toNumber()} < alpha = ${win.alpha[li]} for square ${LABELS[li]}`);
    if (Abm.s.gt(win.alpha[li].neg())) reject(`${W}: the root does not contain the window: sin Ab^- = ${Abm.s.toNumber()} > -alpha = -${win.alpha[li]} for square ${LABELS[li]}`);
  }
}

// ===========================================================================
// L. Driver
// ===========================================================================

class CertChecker {
  constructor(ref, opts) {
    this.ref = ref;
    this.opts = opts || {};
    this.V = new Validator(this.opts);
    this.header = null;
    this.nodes = new Map();      // id -> {parent, kind, children, line}
    this.occ = new Map();        // id -> number of occurrences in `children` lists
    this.waitParent = new Map(); // id of a split node -> {id, assume, arcC, split, final, children, left}
    this.waitChild = new Map();  // id of a node -> its creation data, until its parent has been seen
    this.rootSeen = false;
    this.results = [];
    this.stats = { nodes: 0, infeasible: 0, terminal: 0, split: 0, roundsEvaluated: 0, roundsSkipped: 0, steps: 0, terms: 0, monomials: 0, declarations: 0 };
  }
  feedHeader(text) {
    this.header = this.V.header(parseJsonStrict(text, 'header'), this.ref, this.opts);
  }
  _env() { return { ref: this.ref, header: this.header, opts: this.opts, stats: this.stats }; }
  /** Parse, validate and check one node line alone (no tree bookkeeping). */
  checkNodeText(text, what) {
    if (this.header === null) internal('node before header');
    // [SPEC 2.6] section 10 ("It fixes I for the whole certificate"): every node is read and checked with the label
    // set of THIS certificate's header.  Everything from here to the end of feedNode (well-formedness, node check,
    // root and child rules) is synchronous, so no other certificate can change the selection in between.
    useLabels(this.header.labels);
    // [SPEC 3.0] "THE TWO SCHEMAS", section 10 SCHEMA RULE: likewise every node is read and checked under the schema
    // of THIS certificate's header
    useSchema(this.header.schema3);
    const node = this.V.node(parseJsonStrict(text, what));
    const res = checkNode(this._env(), node);
    return { node, res };
  }
  /** One node line of the certificate: node check plus the tree rules that can be checked now. */
  feedNode(text, lineNo) {
    const { node, res } = this.checkNodeText(text, `line ${lineNo}`);
    const id = node.id;
    // SPEC 7 TREE CONDITIONS: "node ids are unique"
    if (this.nodes.has(id)) reject(`node ${JSON.stringify(id)} (line ${lineNo}): duplicate node id (first at line ${this.nodes.get(id).line})`);
    const kind = node.close.kind;
    this.nodes.set(id, { parent: node.parent, kind, children: kind === 'split' ? node.close.children : null, line: lineNo });
    this.stats.nodes++;
    this.stats[kind]++;
    if (this.opts.collect) {
      this.results.push({ id, line: lineNo, accepted: true, close: kind, rounds: node.rounds.length, rounds_evaluated: res.evaluated,
                          evidence: res.evidence, final_store_empty: res.emptyFinal, final_store_sha256: storeDigest(res.finalStore),
                          final_store: this.opts.dumpStores ? canonicalStore(res.finalStore) : undefined,
                          // [SPEC 3.0] (report only): present only in the entry of a node that is closed as infeasible by a `0` step
                          zero_step_L: res.zeroStepL === null ? undefined : res.zeroStepL });
    }
    // root (SPEC 7: "the root is the node named in the header")
    if (id === this.header.root) { checkRoot(node, this.header); this.rootSeen = true; }
    const data = { id, parent: node.parent, S: node.S, box: node.box, arc: node.arc, assume: node.assume };
    // this node as a child
    if (node.parent !== null) {
      const P = this.waitParent.get(node.parent);
      if (P !== undefined) this._pair(P, data);
      else this.waitChild.set(id, data);
    }
    // this node as a splitting node
    if (kind === 'split') {
      const ch = node.close.children;
      const P = { id, assume: node.assume, arcC: node.arc.map((a) => a.c), split: node.close.how, final: res.finalStore, children: ch, left: ch.length };
      this.waitParent.set(id, P);
      for (const c of ch) {
        // "every node other than the root occurs in exactly one `children` list, exactly once"
        const n = (this.occ.get(c) || 0) + 1;
        this.occ.set(c, n);
        if (n > 1) reject(`node ${JSON.stringify(c)} occurs more than once in \`children\` lists (again in node ${JSON.stringify(id)})`);
      }
      for (const c of ch) {
        const cd = this.waitChild.get(c);
        if (cd !== undefined) { this.waitChild.delete(c); this._pair(P, cd); }
        else if (this.nodes.has(c)) {
          // the child was seen before and is not waiting: it named another parent (or is the root)
          const rec = this.nodes.get(c);
          if (rec.parent !== id) reject(`node ${JSON.stringify(c)} is listed as a child of ${JSON.stringify(id)} but its parent is ${JSON.stringify(rec.parent)}`);
        }
      }
    }
  }
  _pair(P, childData) {
    // "every id in a `children` list exists and that node's `parent` is the splitting node"
    if (childData.parent !== P.id) reject(`node ${JSON.stringify(childData.id)} is listed as a child of ${JSON.stringify(P.id)} but its parent is ${JSON.stringify(childData.parent)}`);
    const l = P.children.indexOf(childData.id);
    if (l < 0) reject(`node ${JSON.stringify(childData.id)} names the parent ${JSON.stringify(P.id)}, which does not list it in \`children\``);
    checkChild(P, childData, l);
    P.left--;
    if (P.left === 0) this.waitParent.delete(P.id);
  }
  /** SPEC 7 TREE CONDITIONS that need the whole certificate. */
  finish() {
    if (this.header === null) reject('certificate: no header');
    const rootId = this.header.root;
    if (!this.nodes.has(rootId)) reject(`the root ${JSON.stringify(rootId)} named in the header does not exist`);
    if (!this.rootSeen) internal('root not checked');
    // every listed child exists, with the right parent
    for (const [id, rec] of this.nodes) {
      if (rec.children === null) continue;
      for (const c of rec.children) {
        const cr = this.nodes.get(c);
        if (cr === undefined) reject(`node ${JSON.stringify(id)}: the child id ${JSON.stringify(c)} does not exist`);
        if (cr.parent !== id) reject(`node ${JSON.stringify(c)} is listed as a child of ${JSON.stringify(id)} but its parent is ${JSON.stringify(cr.parent)}`);
      }
    }
    // every node other than the root occurs in exactly one children list, exactly once; the root in none
    for (const [id, rec] of this.nodes) {
      const n = this.occ.get(id) || 0;
      if (id === rootId) {
        if (n !== 0) reject(`the root ${JSON.stringify(id)} occurs in a \`children\` list`);
      } else if (n !== 1) {
        reject(`node ${JSON.stringify(id)} (line ${rec.line}) occurs in ${n} \`children\` lists (every node other than the root must occur in exactly one, exactly once)`);
      }
    }
    // every node is reachable from the root
    const seen = new Set([rootId]);
    const stack = [rootId];
    let maxDepth = 0;
    const depth = new Map([[rootId, 0]]);
    while (stack.length) {
      const id = stack.pop();
      const rec = this.nodes.get(id);
      if (rec.children === null) continue;
      for (const c of rec.children) {
        if (seen.has(c)) reject(`node ${JSON.stringify(c)} is reached twice from the root (the node graph is not a tree)`);
        seen.add(c);
        const d = depth.get(id) + 1;
        depth.set(c, d);
        if (d > maxDepth) maxDepth = d;
        stack.push(c);
      }
    }
    for (const [id, rec] of this.nodes) {
      if (!seen.has(id)) reject(`node ${JSON.stringify(id)} (line ${rec.line}) is not reachable from the root`);
    }
    if (this.waitChild.size !== 0 || this.waitParent.size !== 0) internal('unpaired parent/child records after the tree conditions passed');
    this.stats.maxDepth = maxDepth;
  }
}

/** Lines of a (possibly gzip-compressed) file as strings, strict UTF-8.  Also feeds a SHA-256 of the bytes read. */
async function* readLines(file, hash) {
  const src = fs.createReadStream(file, { highWaterMark: 1 << 20 });
  let stream = src;
  if (file.endsWith('.gz')) {
    const gz = zlib.createGunzip();
    src.on('error', (e) => gz.destroy(e));
    stream = src.pipe(gz);
  }
  let parts = [];
  let lineNo = 0;
  const emit = () => {
    const buf = parts.length === 1 ? parts[0] : Buffer.concat(parts);
    parts = [];
    lineNo++;
    return { lineNo, text: decodeUtf8(buf) };
  };
  for await (const chunk of stream) {
    if (hash) hash.update(chunk);
    let start = 0;
    for (;;) {
      const nl = chunk.indexOf(0x0A, start);
      if (nl < 0) { if (start < chunk.length) parts.push(chunk.subarray(start)); break; }
      parts.push(chunk.subarray(start, nl));
      yield emit();
      start = nl + 1;
    }
  }
  if (parts.length) yield emit();
}

/** Extract the id of a node line for error messages without trusting the line. */
function peekId(text) {
  const m = /"id"\s*:\s*"((?:[^"\\]|\\.)*)"/.exec(text.length > 4096 ? text.slice(0, 4096) : text);
  return m ? m[1] : null;
}

/**
 * Check a certificate given as an (async or sync) iterable of {lineNo, text}.
 * Returns {pass, reason, failNode, failLine, stats, results, ...}; never throws.
 */
async function checkLines(lines, ref, opts) {
  opts = opts || {};
  const t0 = process.hrtime.bigint();
  const chk = new CertChecker(ref, opts);
  const out = { pass: false, reason: null, failNode: null, failLine: null, internalError: false, failures: 0 };
  const fail = (e, line, id) => {
    out.failures++;
    if (out.reason === null) {
      out.reason = e instanceof Reject ? e.message : `internal error (treated as FAIL): ${e && e.stack ? e.stack : e}`;
      out.internalError = !(e instanceof Reject);
      out.failLine = line;
      out.failNode = id;
    }
  };
  let headerOK = false, any = false;
  try {
    // >>> REVIEW F2: the packing file is pinned.  Its SHA-256 must equal PACKING_SHA256_PIN (or the value given
    //     with --expect-packing-sha256) unless the option --no-packing-pin (opts.noPackingPin) removes the pin.
    //     (The comparison of the header's `packing_sha256` with the file read is a separate, unconditional check.)
    if (!opts.noPackingPin) {
      const pin = opts.expectPackingSha256 || PACKING_SHA256_PIN;
      if (ref.sha256 !== pin) reject(`packing file: its SHA-256 ${ref.sha256} differs from the pinned ${pin} (the option --no-packing-pin removes the pin)`);
    }
    // <<< REVIEW F2
    for await (const { lineNo, text } of lines) {
      any = true;
      if (lineNo === 1) {
        try { chk.feedHeader(text); headerOK = true; }
        catch (e) { fail(e, 1, null); break; }
        continue;
      }
      if (text.trim() === '') { fail(new Reject(`line ${lineNo}: empty line (one node object per line expected)`), lineNo, null); break; }
      if (opts.nodeId !== undefined) {
        // --node ID: check this node alone
        if (!text.includes(JSON.stringify(opts.nodeId))) continue;
        let parsedId = null;
        try {
          const v = parseJsonStrict(text, `line ${lineNo}`);
          parsedId = v instanceof Map ? v.get('id') : null;
        } catch (e) { fail(e, lineNo, peekId(text)); break; }
        if (parsedId !== opts.nodeId) continue;
        try {
          const { node, res } = chk.checkNodeText(text, `line ${lineNo}`);
          chk.stats.nodes++;
          chk.stats[node.close.kind]++;
          out.single = { id: node.id, close: node.close.kind, rounds_evaluated: res.evaluated, evidence: res.evidence,
                         final_store_sha256: storeDigest(res.finalStore), final_store: canonicalStore(res.finalStore) };
          chk.results.push({ id: node.id, line: lineNo, accepted: true, close: node.close.kind, rounds: node.rounds.length, rounds_evaluated: res.evaluated,
                             evidence: res.evidence, final_store_empty: res.emptyFinal, final_store_sha256: storeDigest(res.finalStore),
                             zero_step_L: res.zeroStepL === null ? undefined : res.zeroStepL }); // [SPEC 3.0] (report only)
        } catch (e) { fail(e, lineNo, opts.nodeId); }
        break;
      }
      try { chk.feedNode(text, lineNo); }
      catch (e) {
        const id = peekId(text);
        fail(e, lineNo, id);
        if (opts.collect) chk.results.push({ id, line: lineNo, accepted: false, reason: e instanceof Reject ? e.message : String(e) });
        if (!opts.keepGoing) break;
      }
    }
    if (out.reason === null) {
      if (!any) fail(new Reject('certificate: empty file'), null, null);
      else if (opts.nodeId !== undefined) {
        if (!out.single) fail(new Reject(`node ${JSON.stringify(opts.nodeId)} not found`), null, opts.nodeId);
      } else if (headerOK) {
        try { chk.finish(); } catch (e) { fail(e, null, null); }
      }
    }
  } catch (e) {
    fail(e, null, null);
  }
  out.pass = out.reason === null;
  out.stats = chk.stats;
  out.results = chk.results;
  out.unknownKeys = Array.from(chk.V.unknownKeys.entries());
  out.header = chk.header;
  out.seconds = Number(process.hrtime.bigint() - t0) / 1e9;
  return out;
}

/** Convenience for tests: a certificate given as a string (lines separated by "\n"). */
function linesOfText(text) {
  const parts = text.split('\n');
  if (parts.length && parts[parts.length - 1] === '') parts.pop();
  return parts.map((t, k) => ({ lineNo: k + 1, text: t }));
}
async function checkText(text, ref, opts) {
  return checkLines(linesOfText(text), ref, opts);
}

const DEFAULT_PACKING = path.resolve(__dirname, '..', '..', '..', 'upper-packing-certificate.json');
// [SPEC 3.0] the specification this file implements: its name with the version, and the SHA-256 of the file (report keys `spec`, `spec_sha256`)
const SPEC_NAME = 'SPEC_v3.0.md version 3.0';
const SPEC_SHA256 = '0a6dfc2ae10ed6f30a21ebe357a6e73dd7355223c521cc67a3f2bdab9549aba0';
// >>> REVIEW F2: the SHA-256 of upper-packing-certificate.json (the reference data of SPEC section 1)
const PACKING_SHA256_PIN = '24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7';
// <<< REVIEW F2

function usage() {
  return [
    'usage: node wxcheck2.js CERT.jsonl[.gz] [options]',
    // [SPEC 3.0] (driver only; code review of the 3.0 draft): the exit codes, and that --help is a usage exit
    '  exit code: 0 = PASS of a full run of the whole certificate (and nothing else), 1 = FAIL, 2 = usage (also --help),',
    '             3 = NODE-OK (a node-only check with --node, never a PASS)',
    '  --packing FILE              packing file (default: ../../../upper-packing-certificate.json next to this script)',
    '  --expect-packing-sha256 H   pin the packing file to the SHA-256 H instead of the built-in value',
    '  --no-packing-pin            do not pin the packing file (its hash must still equal the header\'s packing_sha256)',
    '  --node ID                   check only the node ID (alone, without the tree pass): NODE-OK or FAIL',
    '  --json OUT                  write a JSON report (per node: accepted, digest of the final store)',
    '  --dump-stores               include the canonical text of every final store in the JSON report',
    '  --paranoid                  recompute every L by plain rational arithmetic and compare (slow)',
    // [SPEC 3.0] section 10, KEYS: the option --ignore-unknown-keys of the 2.6 file is removed (it relaxed a rule of the SPEC)
    '  --keep-going                continue after the first failing node (the result is still FAIL)',
    '  --quiet                     print only the verdict line',
    // [SPEC 3.0] (driver only; code review of the 3.0 draft): the help option is a usage exit; no argument that begins with "-" is a file
    '  --help, -h                  print this text and exit with code 2 (nothing is checked)',
    '  An argument that begins with "-" and is not one of these options is a usage error (a file of such a name: ./NAME).',
  ].join('\n');
}

async function main(argv) {
  const opts = { collect: false };
  let cert = null, packing = DEFAULT_PACKING, jsonOut = null, quiet = false;
  for (let k = 0; k < argv.length; k++) {
    const a = argv[k];
    const need = () => { if (k + 1 >= argv.length) { console.error(`missing argument of ${a}\n` + usage()); process.exit(2); } return argv[++k]; };
    if (a === '--packing') packing = need();
    else if (a === '--expect-packing-sha256') opts.expectPackingSha256 = need();
    else if (a === '--no-packing-pin') opts.noPackingPin = true; // REVIEW F2
    else if (a === '--node') opts.nodeId = need();
    else if (a === '--json') { jsonOut = need(); opts.collect = true; }
    else if (a === '--dump-stores') opts.dumpStores = true;
    else if (a === '--paranoid') opts.paranoid = true;
    // [SPEC 3.0] section 10, KEYS: no option --ignore-unknown-keys any more (2.6: opts.ignoreUnknownKeys = true); the
    // word is now an unknown option (usage error, exit code 2), like every other word that begins with "--"
    else if (a === '--keep-going') opts.keepGoing = true;
    else if (a === '--quiet') quiet = true;
    // >>> [SPEC 3.0] (driver only, no checking rule; code review of the 3.0 draft, instruction of the lead): EXIT CODE 0
    //     HAS EXACTLY ONE SOURCE in this program, the PASS verdict of a full run of the whole certificate (the last
    //     statement of main).  The 2.6 file left with code 0 after --help / -h without checking anything; now the help
    //     option prints the usage and exits with the usage code 2.  And an argument that begins with "-" and is not an
    //     option is a usage error, never the certificate (2.6: only arguments beginning with "--" were refused, so
    //     "-x" was taken for the certificate file).  The other ways out: process.exit(2) for every usage error (here,
    //     in `need`, and for a missing or a second certificate argument); process.exitCode = 3 for NODE-OK and 1 for
    //     FAIL at the end of main (a missing file, an unreadable packing file, a report that cannot be written and
    //     every internal error are FAIL); 1 in the handler of an exception that escapes main.
    else if (a === '--help' || a === '-h') { console.log(usage()); process.exit(2); }
    else if (a.startsWith('-')) { console.error(`unknown option ${a}\n` + usage()); process.exit(2); }
    // <<< [SPEC 3.0]
    else if (cert === null) cert = a;
    else { console.error('more than one certificate file\n' + usage()); process.exit(2); }
  }
  if (cert === null) { console.error(usage()); process.exit(2); }
  let res, ref = null;
  const hash = crypto.createHash('sha256');
  try {
    ref = loadReference(packing);
    res = await checkLines(readLines(cert, hash), ref, opts);
  } catch (e) {
    res = { pass: false, reason: e instanceof Reject ? e.message : `internal error (treated as FAIL): ${e && e.stack ? e.stack : e}`,
            failNode: null, failLine: null, stats: null, results: [], unknownKeys: [], seconds: 0 };
  }
  let certSha = null;
  try { certSha = hash.digest('hex'); } catch (e) { certSha = null; }
  const s = res.stats;
  const counts = s ? `nodes ${s.nodes} (infeasible ${s.infeasible}, terminal ${s.terminal}, split ${s.split}), rounds evaluated ${s.roundsEvaluated}` +
    ` (not evaluated ${s.roundsSkipped}), declarations ${s.declarations}, steps ${s.steps}, terms ${s.terms}` : 'no counts';
  // >>> REVIEW F4: the --json report is written BEFORE the verdict is printed; if it cannot be written, the
  //     verdict is FAIL and no PASS line is printed.
  const nodeOnly = opts.nodeId !== undefined;
  // >>> [SPEC 2.6] (driver and report only, no checking rule): the label count and the S_floor that were USED,
  //     i.e. those of the accepted header (sections 0, 7, 10): labels is the number 16 or 17, S_floor the rational
  //     in lowest terms as a string ("4" when the field is absent).  Both are null if no header was accepted.
  const usedLabels = res.header ? res.header.labels : null;
  const usedSfloor = res.header ? res.header.S_floor.toString() : null;
  // <<< [SPEC 2.6]
  // >>> [SPEC 3.0] (driver and report only, no checking rule): the schema string of the accepted header, and whether
  //     its `window` and its `terminal` object have the field `centre` (section 8; true or false).  All three are
  //     null if no header was accepted.
  const usedSchema = res.header ? res.header.schema : null;
  const windowCentres = res.header ? res.header.window.centre !== null : null;
  const tubeCentres = res.header ? res.header.terminal.centre !== null : null;
  // <<< [SPEC 3.0]
  if (jsonOut !== null) {
    const rep = {
      checker: 'wxcheck2.js', spec: SPEC_NAME, spec_sha256: SPEC_SHA256, result: res.pass ? (nodeOnly ? 'NODE-OK' : 'PASS') : 'FAIL', // [SPEC 3.0] name and version of the specification; new key: its SHA-256
      mode: nodeOnly ? 'single node (no tree pass)' : 'certificate',
      certificate: cert, certificate_sha256: certSha, packing_sha256: ref ? ref.sha256 : null,
      labels: usedLabels, S_floor: usedSfloor, // [SPEC 2.6] two new report keys
      schema: usedSchema, window_centres: windowCentres, tube_centres: tubeCentres, // [SPEC 3.0] three new report keys
      reason: res.reason, first_failing_node: res.failNode, first_failing_line: res.failLine,
      counts: s, seconds: res.seconds, nodes: res.results,
    };
    try { fs.writeFileSync(jsonOut, JSON.stringify(rep, null, 1) + '\n'); }
    catch (e) {
      const why = `the --json report could not be written to ${jsonOut}: ${e && e.message ? e.message : e}`;
      if (res.pass) { res.pass = false; res.reason = why; res.failNode = null; res.failLine = null; }
      else res.reason = `${res.reason} [also: ${why}]`;
    }
  }
  // <<< REVIEW F4
  // >>> REVIEW F1: a node-only check never prints PASS and never exits with code 0
  if (res.pass) {
    console.log(nodeOnly ? `NODE-OK (node ${JSON.stringify(opts.nodeId)} alone; the tree, root and child conditions were NOT checked; this is not a PASS of the certificate)` : 'PASS');
  } else {
    console.log('FAIL');
  }
  // <<< REVIEW F1
  if (!quiet) {
    // [SPEC 2.6] (output only): one extra line, directly after the verdict line and not indented, with the label
    // count and the S_floor that were used (null: no header was accepted)
    console.log(`labels=${usedLabels} S_floor=${usedSfloor}`);
    // [SPEC 3.0] (output only): one more line, directly after it and not indented, with the schema string of the
    // accepted header (null: no header was accepted)
    console.log(`schema=${usedSchema}`);
    console.log(`  certificate: ${cert}` + (certSha && res.pass ? `  (SHA-256 of the checked bytes ${certSha})` : ''));
    if (ref) console.log(`  packing file: ${ref.path}  (SHA-256 ${ref.sha256}; Sref = ${ref.side})`);
    console.log(`  ${counts}` + (s && s.maxDepth !== undefined ? `, tree depth ${s.maxDepth}` : ''));
    if (!res.pass) {
      console.log(`  first failing node: ${res.failNode === null ? '(none: header or tree level)' : JSON.stringify(res.failNode)}` + (res.failLine ? ` (line ${res.failLine})` : ''));
      console.log(`  reason: ${res.reason}`);
      if (opts.keepGoing) console.log(`  failures in total: ${res.failures}`);
    }
    if (res.single) console.log(`  node ${JSON.stringify(res.single.id)}: close ${res.single.close}, rounds evaluated ${res.single.rounds_evaluated}, final store SHA-256 ${res.single.final_store_sha256}`);
    // [SPEC 3.0] section 10, KEYS: the line "unknown keys ignored (--ignore-unknown-keys): ..." of the 2.6 file is gone with the option
    if (opts.paranoid && res.pass) console.log('  paranoid mode: every L was recomputed by plain rational arithmetic and agreed');
    console.log(`  time: ${res.seconds.toFixed(2)} s`);
  }
  // >>> REVIEW F1, F4: (the report was written above); exit code 3 for a successful node-only check
  process.exitCode = res.pass ? (nodeOnly ? 3 : 0) : 1;
  // <<< REVIEW F1, F4
}

module.exports = {
  Reject, JNum, parseJsonStrict, Q, Iv, Rot, SPoly, cmaxOf, bgcd, blcm, ratioToNumber, parseNumString,
  // [SPEC 2.6] sections 0, 3, 10: LABELS, NL, LIDX, NVAR, V_S depend on the label set in force and are exported as
  // getters (2.5.1: constants; right after loading they have the sixteen-label values of 2.5.1); useLabels and
  // LABEL_SETS are exported for tests
  get LABELS() { return LABELS; }, get NL() { return NL; }, get LIDX() { return LIDX; }, get NVAR() { return NVAR; },
  get V_S() { return V_S; }, useLabels, LABEL_SETS,
  // [SPEC 3.0] the schema selection and the helpers of the new step check, exported for tests
  get SCHEMA3() { return SCHEMA3; }, useSchema, squareHot, binomBig, hotOf, mulHot,
  V_XI, V_C, V_SN, MCH, monMul, monName, varName,
  loadReference, parseFormName, parseFactName, classInfo, eightOptions, optKey, signKey,
  Validator, NodeCtx, StoreView, RoundCtx, EmptySB, initialStore, terminalTest, checkNode, canonicalStore, storeDigest,
  arcContainment, checkChild, checkRoot, CertChecker, readLines, checkLines, checkText, linesOfText, DEFAULT_PACKING, SREF_SPEC,
  PACKING_SHA256_PIN,
  SPEC_NAME, SPEC_SHA256, // [SPEC 3.0]
};

if (require.main === module) {
  main(process.argv.slice(2)).catch((e) => {
    console.log('FAIL');
    console.log(`  reason: internal error (treated as FAIL): ${e && e.stack ? e.stack : e}`);
    process.exitCode = 1;
  });
}
