#!/usr/bin/env node
'use strict';
// verify_classes.js
//
// Independent Node.js checker for CLASS certificates (schema s17-classes-v1): a charge certificate in
// the published shape plus a class file (pose classes with rational thresholds, a rational bound).
// Written from cloud/analysis/CLASS_FORMAT.md (statement, format, cell rule) and
// cloud/analysis/RESTRICTED_CHECKER.md (certificate format, rows, arrangement), with the conventions
// of verify_restricted.js (JSON reader, rationals, charge expansion, arrangement and sweep are the
// same code as there). It shares no code with cert_restricted/exact_classes.py.
//
// Statement (CLASS_FORMAT.md section 1): for every family of closed unit squares with pairwise
// disjoint interiors inside the container of side L/A, the sum of tau(pose) is below the bound, where
// tau(pose) is the least threshold among the classes containing the pose, and 1 if none does.
//
// Checked: structure, capacities and budget of the certificate; budget_units * q_b < p_b * minimum_units;
// and for every row and every checked cell: charge * q >= p * minimum_units, p/q = required threshold
// of the cell = the largest threshold among the classes above 1 that the closed cell x closed row
// interval MEETS in one of their slot images; if there is none, the least threshold among the classes
// below 1 with the whole closed cell x closed row interval inside ONE slot image; if none, 1.
// Everything on that path is BigInt / exact integer arithmetic; the charge tree holds integers of
// absolute value below 2^50 in float64 (exact), as in the published checker.
//
//   node verify_classes.js CERT.json --classes CLASSES.json --output OUT.json [--start i] [--count n] [--workers w] [--quiet]
//   node verify_classes.js CERT.json --classes CLASSES.json --output ALL.json --merge S1.json S2.json ...
//
// Exit codes: 0 no row of the range failed; 2 some row failed; 3 merge incomplete; 1 refused.

const fs = require('fs');
const crypto = require('crypto');

class Refused extends Error {}
function need(cond, msg) { if (!cond) throw new Refused(msg); }

// ------------------------------------------------------------------------------------------
// Exact JSON: integers become BigInt, any other number token becomes a JsonFloat (refused
// wherever a rational or an integer is expected). Duplicate keys are refused.
// ------------------------------------------------------------------------------------------
class JsonFloat { constructor(src) { this.src = src; } }
const NUMBER_RE = /-?(?:0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?/y;

function parseJsonExact(text) {
  let i = 0;
  const n = text.length;
  const fail = (m) => { throw new Refused(`JSON: ${m} at offset ${i}`); };
  function ws() {
    while (i < n) {
      const c = text.charCodeAt(i);
      if (c === 32 || c === 9 || c === 10 || c === 13) i++; else break;
    }
  }
  function str() {
    const s = i;
    i++;
    while (i < n) {
      const c = text.charCodeAt(i);
      if (c === 34) break;
      i += (c === 92) ? 2 : 1;
    }
    if (i >= n) fail('unterminated string');
    i++;
    try { return JSON.parse(text.slice(s, i)); } catch (e) { fail('bad string'); }
    return null;
  }
  function value() {
    ws();
    if (i >= n) fail('unexpected end');
    const c = text[i];
    if (c === '{') {
      i++;
      const o = Object.create(null);
      ws();
      if (text[i] === '}') { i++; return o; }
      for (;;) {
        ws();
        if (text[i] !== '"') fail('key expected');
        const k = str();
        ws();
        if (text[i] !== ':') fail('colon expected');
        i++;
        if (k in o) fail(`duplicate key ${JSON.stringify(k)}`);
        o[k] = value();
        ws();
        if (text[i] === ',') { i++; continue; }
        if (text[i] === '}') { i++; return o; }
        fail('comma or } expected');
      }
    }
    if (c === '[') {
      i++;
      const a = [];
      ws();
      if (text[i] === ']') { i++; return a; }
      for (;;) {
        a.push(value());
        ws();
        if (text[i] === ',') { i++; continue; }
        if (text[i] === ']') { i++; return a; }
        fail('comma or ] expected');
      }
    }
    if (c === '"') return str();
    if (text.startsWith('true', i)) { i += 4; return true; }
    if (text.startsWith('false', i)) { i += 5; return false; }
    if (text.startsWith('null', i)) { i += 4; return null; }
    NUMBER_RE.lastIndex = i;
    const m = NUMBER_RE.exec(text);
    if (!m) fail('value expected');
    i = NUMBER_RE.lastIndex;
    if (m[1] === undefined && m[2] === undefined) return BigInt(m[0]);
    return new JsonFloat(m[0]);
  }
  const v = value();
  ws();
  if (i !== n) fail('trailing characters');
  return v;
}

const isObj = (v) => v !== null && typeof v === 'object' && !Array.isArray(v) && !(v instanceof JsonFloat);
function onlyKeys(o, allowed, what) {
  for (const k of Object.keys(o)) need(allowed.includes(k), `${what}: key ${JSON.stringify(k)} is not allowed`);
}

// ------------------------------------------------------------------------------------------
// Exact rationals [numerator, denominator], denominator > 0, lowest terms.
// ------------------------------------------------------------------------------------------
const abs = (a) => (a < 0n ? -a : a);
function gcd(a, b) { a = abs(a); b = abs(b); while (b) { const r = a % b; a = b; b = r; } return a; }
function lcm(a, b) { return a / gcd(a, b) * b; }
function Q(n, d = 1n) {
  if (d === 0n) throw new Refused('zero denominator');
  if (d < 0n) { n = -n; d = -d; }
  const g = gcd(n, d);
  return g > 1n ? [n / g, d / g] : [n, d];
}
const qadd = (a, b) => Q(a[0] * b[1] + b[0] * a[1], a[1] * b[1]);
const qsub = (a, b) => Q(a[0] * b[1] - b[0] * a[1], a[1] * b[1]);
const qmul = (a, b) => Q(a[0] * b[0], a[1] * b[1]);
const qdiv = (a, b) => Q(a[0] * b[1], a[1] * b[0]);
const qneg = (a) => [-a[0], a[1]];
const qabs = (a) => [abs(a[0]), a[1]];
function qcmp(a, b) { const x = a[0] * b[1], y = b[0] * a[1]; return x < y ? -1 : x > y ? 1 : 0; }
const qlt = (a, b) => qcmp(a, b) < 0;
const qle = (a, b) => qcmp(a, b) <= 0;
const qeq = (a, b) => a[0] === b[0] && a[1] === b[1];
const qsign = (a) => (a[0] > 0n ? 1 : a[0] < 0n ? -1 : 0);
const qstr = (a) => (a[1] === 1n ? String(a[0]) : `${a[0]}/${a[1]}`);
const QI = (n) => [BigInt(n), 1n];
const Q0 = QI(0), Q1 = QI(1), QHALF = [1n, 2n];
function floorDiv(a, b) { const r = a / b; return ((a % b !== 0n) && ((a < 0n) !== (b < 0n))) ? r - 1n : r; }
function ceilDiv(a, b) { return -floorDiv(-a, b); }

const RAT_RE = /^(-?\d+)(?:\/(\d+))?$/;
function rat(v, what) {
  if (typeof v === 'bigint') return [v, 1n];
  if (typeof v === 'string') {
    const m = RAT_RE.exec(v);
    need(m, `${what}: ${JSON.stringify(v.slice(0, 40))} is not a rational "p" or "p/q"`);
    const d = m[2] === undefined ? 1n : BigInt(m[2]);
    need(d > 0n, `${what}: zero denominator`);
    return Q(BigInt(m[1]), d);
  }
  throw new Refused(`${what}: rational expected (JSON integer or string "p/q"); floats are refused`);
}
function int(v, what) {
  need(typeof v === 'bigint', `${what}: JSON integer expected`);
  return v;
}
function trig(x) { // c(x) = (1-x^2)/(1+x^2), s(x) = 2x/(1+x^2)
  const n = x[0], d = x[1], r = d * d + n * n;
  return [Q(d * d - n * n, r), Q(2n * n * d, r)];
}

// ------------------------------------------------------------------------------------------
// The class file (CLASS_FORMAT.md section 2). Read strictly: every rational is a STRING "p" or
// "p/q" (no JSON numbers), no float token anywhere in the file, no unknown key, centre regions are
// polygons, every slot has its gate.
// ------------------------------------------------------------------------------------------
const CLASS_SCHEMA = 's17-classes-v1';
const MAX_ITEMS = 4096;
const MAX_CLASSES = 256;
const SRAT_RE = /^(-?[0-9]+)(?:\/([0-9]+))?$/;
const NAME_RE = /^[A-Za-z0-9_.+-]{1,64}$/;

function srat(v, what) {
  need(typeof v === 'string', `${what}: rational expected as a string "p" or "p/q"`);
  const m = SRAT_RE.exec(v);
  need(m, `${what}: ${JSON.stringify(v.slice(0, 40))} is not a rational "p" or "p/q"`);
  const d = m[2] === undefined ? 1n : BigInt(m[2]);
  need(d > 0n, `${what}: zero denominator`);
  return Q(BigInt(m[1]), d);
}
function hasFloat(v) {
  if (v instanceof JsonFloat) return true;
  if (Array.isArray(v)) return v.some(hasFloat);
  if (isObj(v)) return Object.keys(v).some((k) => hasFloat(v[k]));
  return false;
}
function exactKeys(o, required, optional, what) {
  need(isObj(o), `${what}: object expected`);
  onlyKeys(o, required.concat(optional), what);
  for (const k of required) need(k in o, `${what}: key ${JSON.stringify(k)} is missing`);
}
function parsePoint(v, what) {
  need(Array.isArray(v) && v.length === 2, `${what}: point [x, y] expected`);
  return [srat(v[0], what), srat(v[1], what)];
}
function crossQ(o, a, b) { // (a - o) x (b - o)
  return qsub(qmul(qsub(a[0], o[0]), qsub(b[1], o[1])), qmul(qsub(a[1], o[1]), qsub(b[0], o[0])));
}
function parsePolygon(v, what) {
  need(Array.isArray(v) && v.length >= 3 && v.length <= 64, `${what}: polygon with 3..64 vertices expected`);
  const P = v.map((p) => parsePoint(p, what));
  const m = P.length;
  for (let i = 0; i < m; i++) {
    for (let j = i + 1; j < m; j++) need(!(qeq(P[i][0], P[j][0]) && qeq(P[i][1], P[j][1])), `${what}: repeated vertex`);
  }
  for (let i = 0; i < m; i++) {
    const a = P[i], b = P[(i + 1) % m], c = P[(i + 2) % m];
    need(qsign(crossQ(a, b, c)) > 0, `${what}: not strictly convex and counter-clockwise`);
    for (let j = 0; j < m; j++) need(qsign(crossQ(a, b, P[j])) >= 0, `${what}: vertex on the wrong side of an edge`);
  }
  return P;
}
function parseClassFile(o) {
  need(isObj(o), 'class file: JSON object expected');
  need(!hasFloat(o), 'class file: float number tokens are not allowed anywhere in the file');
  exactKeys(o, ['schema', 'symmetry', 'frame', 'bound', 'classes'], ['comment'], 'class file');
  need(o.schema === CLASS_SCHEMA, `class file: schema must be ${CLASS_SCHEMA}`);
  need(o.symmetry === 'fixed' || o.symmetry === 'mirror_x' || o.symmetry === 'orbit', 'class file: symmetry must be fixed, mirror_x or orbit');
  exactKeys(o.frame, ['unit', 'center'], [], 'class file: frame');
  need(o.frame.unit === 'unit_square', 'class file: frame.unit must be unit_square');
  const center = parsePoint(o.frame.center, 'class file: frame.center');
  const bound = srat(o.bound, 'class file: bound');
  need(qsign(bound) > 0, 'class file: bound must be positive');
  need(Array.isArray(o.classes) && o.classes.length >= 1 && o.classes.length <= MAX_CLASSES, `class file: classes must be a list of 1..${MAX_CLASSES} classes`);
  const names = new Set();
  const classes = o.classes.map((c, ci) => {
    const what = `classes[${ci}]`;
    exactKeys(c, ['name', 'threshold', 'slots'], [], what);
    need(typeof c.name === 'string' && NAME_RE.test(c.name), `${what}: name must be 1..64 characters of A-Z a-z 0-9 _ . + -`);
    need(!names.has(c.name), `${what}: name ${c.name} is used twice`);
    names.add(c.name);
    const threshold = srat(c.threshold, `${what}.threshold`);
    need(qsign(threshold) >= 0, `${what}: threshold must be >= 0`);
    need(Array.isArray(c.slots) && c.slots.length >= 1 && c.slots.length <= MAX_ITEMS, `${what}: slots must be a list of 1..${MAX_ITEMS} slots`);
    const slots = c.slots.map((s, si) => {
      const w = `${what}.slots[${si}]`;
      exactKeys(s, ['centre', 'angle_tan_half'], ['label'], w);
      exactKeys(s.centre, ['polygon'], [], `${w}.centre`);
      const P = parsePolygon(s.centre.polygon, `${w}.polygon`);
      const g = s.angle_tan_half;
      need(Array.isArray(g) && g.length === 2, `${w}: angle_tan_half [lo, hi] expected`);
      const lo = srat(g[0], `${w}.angle_tan_half`), hi = srat(g[1], `${w}.angle_tan_half`);
      need(qlt(QI(-1), lo) && qle(lo, hi) && qlt(hi, Q1), `${w}: need -1 < lo <= hi < 1`);
      return { P, gate: [lo, hi] };
    });
    return { name: c.name, threshold, slots };
  });
  return { symmetry: o.symmetry, center, bound, classes };
}

// ------------------------------------------------------------------------------------------
// Charge: features, Moebius expansion, budget (RESTRICTED_CHECKER.md 1.3, 1.4; published conventions)
// ------------------------------------------------------------------------------------------
const TWO50 = 2n ** 50n;
const expansionCache = new Map();

// Returns {capacity, expansion: [[positions], coefficient], absSum} for one Boolean rule.
function ruleOf(n, coefficientsRaw, thresholdRaw, masksRaw, thresholdDefault, what) {
  need(n >= 1 && n <= 20, `${what}: 1..20 sites expected`);
  let co;
  if (coefficientsRaw === undefined) {
    co = new Array(n).fill(1);
  } else {
    need(Array.isArray(coefficientsRaw) && coefficientsRaw.length === n, `${what}: one coefficient per position expected`);
    co = coefficientsRaw.map((c, j) => {
      const b = int(c, `${what}.coefficients`);
      need(b > 0n && b < 2n ** 40n, `${what}: coefficients must be positive (and below 2^40)`);
      return Number(b);
    });
    for (let j = 1; j < n; j++) need(co[j - 1] >= co[j], `${what}: coefficients must be non-increasing`);
  }
  const total = co.reduce((z, a) => z + a, 0);
  need(Number.isSafeInteger(total), `${what}: coefficient sum too large`);
  let masks = null;
  if (masksRaw !== undefined) {
    need(Array.isArray(masksRaw) && masksRaw.length >= 1, `${what}: winning_masks must be a non-empty list`);
    need(n <= 12, `${what}: winning_masks needs at most 12 sites`);
    masks = masksRaw.map((m) => {
      const b = int(m, `${what}.winning_masks`);
      need(b > 0n && b < (1n << BigInt(n)), `${what}: mask out of range`);
      return Number(b);
    });
    need(new Set(masks).size === masks.length, `${what}: masks must be distinct`);
    for (const a of masks) for (const b of masks) need((a & b) !== 0, `${what}: every two masks must share a bit`);
  }
  // threshold: bounds are checked whenever it is present (or defaulted); with masks it is not used
  let k = null;
  if (thresholdRaw !== undefined) {
    const b = int(thresholdRaw, `${what}.threshold`);
    need(b >= 1n && b <= BigInt(total), `${what}: need 1 <= threshold <= sum of coefficients`);
    k = Number(b);
  } else if (thresholdDefault !== null) {
    k = thresholdDefault;
    need(k >= 1 && k <= total, `${what}: need 1 <= threshold <= sum of coefficients`);
  } else {
    need(masks !== null, `${what}: threshold is required`);
  }
  const key = masks ? `m|${n}|${masks.join(',')}` : `t|${k}|${co.join(',')}`;
  let rule = expansionCache.get(key);
  if (!rule) {
    // indicator on subsets, then Moebius inversion: indicator(S) = sum over T subset of S of c_T
    const size = 1 << n;
    const v = new Int32Array(size);
    for (let mask = 0; mask < size; mask++) {
      if (masks) {
        v[mask] = masks.some((w) => (mask & w) === w) ? 1 : 0;
      } else {
        let z = 0;
        for (let j = 0; j < n; j++) if ((mask >> j) & 1) z += co[j];
        v[mask] = z >= k ? 1 : 0;
      }
    }
    for (let j = 0; j < n; j++) {
      const bit = 1 << j;
      for (let mask = 0; mask < size; mask++) if (mask & bit) v[mask] -= v[mask ^ bit];
    }
    const expansion = [];
    let absSum = 0;
    for (let mask = 1; mask < size; mask++) {
      if (v[mask]) {
        const pos = [];
        for (let j = 0; j < n; j++) if ((mask >> j) & 1) pos.push(j);
        expansion.push([pos, v[mask]]);
        absSum += Math.abs(v[mask]);
      }
    }
    need(v[0] === 0, `${what}: rule fires on the empty set`);
    rule = { capacity: masks ? 1 : Math.floor(total / k), expansion, absSum };
    expansionCache.set(key, rule);
  }
  return { ...rule, co, masks };
}

function siteIndexList(v, count, what) {
  need(Array.isArray(v), `${what}: list of site indices expected`);
  const ids = v.map((x) => {
    const b = int(x, what);
    need(b >= 0n && b < BigInt(count), `${what}: site index out of range`);
    return Number(b);
  });
  need(new Set(ids).size === ids.length, `${what}: site indices must be distinct`);
  return ids;
}
function weightOf(v, what) {
  const w = int(v, what);
  need(w >= 0n, `${what}: weight must be >= 0`);
  need(w < TWO50, `${what}: weight must be below 2^50`);
  return w;
}

// Symmetric shape: point_orbits + threshold_orbits, validated as in the published Node checker.
function buildSymmetric(d, LD) {
  need(Array.isArray(d.point_orbits), 'point_orbits: list expected');
  need(Array.isArray(d.threshold_orbits), 'threshold_orbits: list expected');
  const pts = [], pw = [];
  for (const row of d.point_orbits) {
    need(Array.isArray(row) && row.length === 3, 'point_orbits: rows [x, y, w] expected');
    const x = int(row[0], 'point orbit x'), y = int(row[1], 'point orbit y'), w = weightOf(row[2], 'point orbit weight');
    need(x >= 0n && x <= LD && y >= 0n && y <= LD, 'point orbit outside the container');
    const m = new Map();
    for (const [u, v] of [[x, y], [y, x]]) for (const a of [u, LD - u]) for (const b of [v, LD - v]) m.set(`${a},${b}`, [a, b]);
    const orbit = [...m.values()].sort((a, b) => (a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : a[1] < b[1] ? -1 : a[1] > b[1] ? 1 : 0));
    for (const p of orbit) { pts.push(p); pw.push(w); }
  }
  const lookup = new Map(pts.map((p, i) => [`${p[0]},${p[1]}`, i]));
  need(lookup.size === pts.length, 'sites of different point orbits coincide');
  need(pts.length >= 1, 'at least one site expected');
  let budget = 0n, absolute = 0n;
  const atoms = [];
  for (let i = 0; i < pw.length; i++) {
    budget += pw[i];
    absolute += pw[i];
    if (pw[i] > 0n) atoms.push([[i], Number(pw[i])]);
  }
  d.threshold_orbits.forEach((g, gi) => {
    const what = `threshold_orbits[${gi}]`;
    need(isObj(g), `${what}: object expected`);
    onlyKeys(g, ['sets', 'weight', 'threshold', 'coefficients', 'winning_masks'], what);
    const w = weightOf(g.weight, `${what}.weight`);
    need(Array.isArray(g.sets) && g.sets.length >= 1, `${what}: sets expected`);
    const sets = g.sets.map((s) => siteIndexList(s, pts.length, `${what}.sets`));
    const n = sets[0].length;
    for (const s of sets) need(s.length === n, `${what}: sets of different sizes`);
    const rule = ruleOf(n, g.coefficients, g.threshold, g.winning_masks, 2, what);
    const co = rule.co;
    const canonical = (ids) => (rule.masks
      ? ids.join(',')
      : ids.map((id, j) => [co[j], id]).sort((a, b) => b[0] - a[0] || a[1] - b[1]).map((z) => z[1]).join(','));
    const expected = new Set();
    for (const swap of [false, true]) for (const sx of [false, true]) for (const sy of [false, true]) {
      const image = sets[0].map((i) => {
        let [x, y] = pts[i];
        if (swap) [x, y] = [y, x];
        if (sx) x = LD - x;
        if (sy) y = LD - y;
        const j = lookup.get(`${x},${y}`);
        need(j !== undefined, `${what}: image of a site is not a site`);
        return j;
      });
      expected.add(canonical(image));
    }
    const got = new Set(sets.map(canonical));
    need(got.size === sets.length && expected.size === sets.length && [...got].every((c) => expected.has(c)),
      `${what}: sets are not one complete D4 orbit`);
    budget += w * BigInt(sets.length) * BigInt(rule.capacity);
    absolute += w * BigInt(sets.length) * BigInt(rule.absSum);
    if (w > 0n) {
      const wn = Number(w);
      for (const s of sets) for (const [pos, c] of rule.expansion) atoms.push([pos.map((j) => s[j]), wn * c]);
    }
  });
  return { pts, atoms, budget, absolute, features: pw.filter((w) => w > 0n).length + d.threshold_orbits.reduce((z, g) => z + g.sets.length, 0) };
}

// Fixed-image shape: sites + features, image by image, nothing closed under D4. Keeps the features
// (site ids, rule, weight) for the mirror test.
function buildFixed(d, LD) {
  need(Array.isArray(d.sites) && d.sites.length >= 1, 'sites: non-empty list expected');
  need(Array.isArray(d.features), 'features: list expected');
  const seen = new Set();
  const pts = d.sites.map((s, i) => {
    need(Array.isArray(s) && s.length === 2, `sites[${i}]: [x, y] expected`);
    const x = int(s[0], `sites[${i}]`), y = int(s[1], `sites[${i}]`);
    need(x >= 0n && x <= LD && y >= 0n && y <= LD, `sites[${i}] outside the container`);
    const key = `${x},${y}`;
    need(!seen.has(key), `sites[${i}] repeats an earlier site`);
    seen.add(key);
    return [x, y];
  });
  let budget = 0n, absolute = 0n;
  const atoms = [], feats = [];
  d.features.forEach((f, fi) => {
    const what = `features[${fi}]`;
    need(isObj(f), `${what}: object expected`);
    onlyKeys(f, ['sites', 'weight', 'threshold', 'coefficients', 'winning_masks'], what);
    const ids = siteIndexList(f.sites, pts.length, `${what}.sites`);
    const w = weightOf(f.weight, `${what}.weight`);
    const rule = ruleOf(ids.length, f.coefficients, f.threshold, f.winning_masks, null, what);
    budget += w * BigInt(rule.capacity);
    absolute += w * BigInt(rule.absSum);
    if (w > 0n) {
      const wn = Number(w);
      for (const [pos, c] of rule.expansion) atoms.push([pos.map((j) => ids[j]), wn * c]);
    }
    feats.push({ ids, w, co: rule.co, masks: rule.masks, k: rule.masks ? null : String(f.threshold) });
  });
  return { pts, atoms, budget, absolute, features: d.features.length, feats };
}

// symmetry "mirror_x": the charge must be invariant under the mirror x -> L - x of the container,
// and this is verified on the feature list itself. A feature image is identified by its rule and its
// sites: threshold rule = threshold + the multiset of (coefficient, site); mask rule = the set of
// masks + the sites in their order. Repeated features add their weights. Required: every site of
// every feature (also of weight 0) has its mirror image among the sites, and for every feature the
// total weight listed for its mirror image equals the total weight listed for the feature itself.
// Anything that is not recognised as the mirror image (same rule written differently) is refused.
function checkMirrorInvariance(pts, feats, LD) {
  const lookup = new Map(pts.map((p, i) => [`${p[0]},${p[1]}`, i]));
  const mirrorOf = pts.map((p) => lookup.get(`${LD - p[0]},${p[1]}`));
  const keyOf = (ids, f) => (f.masks
    ? `m|${[...f.masks].sort((a, b) => a - b).join(',')}|${ids.join(',')}`
    : `t|${f.k}|${ids.map((id, j) => [f.co[j], id]).sort((a, b) => b[0] - a[0] || a[1] - b[1]).map((z) => `${z[0]}:${z[1]}`).join(',')}`);
  const total = new Map();
  for (const f of feats) {
    const key = keyOf(f.ids, f);
    total.set(key, (total.get(key) || 0n) + f.w);
  }
  feats.forEach((f, fi) => {
    const image = f.ids.map((id) => mirrorOf[id]);
    need(image.every((j) => j !== undefined), `features[${fi}]: the mirror image of one of its sites is not a site (mirror_x)`);
    const own = total.get(keyOf(f.ids, f)), other = total.get(keyOf(image, f));
    need(other !== undefined && other === own, `features[${fi}]: its mirror image is not listed with the same weight, coefficients and masks (charge not invariant under the mirror)`);
  });
}

// ------------------------------------------------------------------------------------------
// Certificate + class file: whole-file validation
// ------------------------------------------------------------------------------------------
function sha256(buf) { return crypto.createHash('sha256').update(buf).digest('hex'); }

function loadAll(certPath, classPath) {
  const raw = fs.readFileSync(certPath);
  const d = parseJsonExact(raw.toString('utf8'));
  need(isObj(d), 'certificate: JSON object expected');
  need(!('restriction' in d), 'the certificate carries a restriction object; a class check needs a certificate without one');
  const craw = fs.readFileSync(classPath);
  const CL = parseClassFile(parseJsonExact(craw.toString('utf8')));
  return validate(d, CL, sha256(raw), sha256(craw));
}

const TWO53 = 2n ** 53n;

function validate(d, CL, certSha, classSha) {
  const L = rat(d.L, 'L'), A = rat(d.A, 'A');
  need(qeq(L, Q(4613n, 1000n)), 'L must equal 4613/1000');
  need(qsign(A) > 0 && qlt(A, L), 'need 0 < A < L');
  need(qeq(rat(d.normalized_target, 'normalized_target'), qdiv(L, A)), 'normalized_target must equal L/A');
  const D = int(d.coordinate_denominator, 'coordinate_denominator');
  need(D > 0n, 'coordinate_denominator must be positive');
  need((L[0] * D) % L[1] === 0n, 'L * coordinate_denominator must be an integer');
  const LD = L[0] * D / L[1];
  need(int(d.weight_denominator, 'weight_denominator') > 0n, 'weight_denominator must be positive');
  const budgetUnits = int(d.budget_units, 'budget_units');
  const required = int(d.minimum_units, 'minimum_units');
  need(required > 0n, 'minimum_units must be positive');

  // shape of the charge and range of the rows, by the symmetry of the class file:
  //   orbit    : symmetric shape (complete D4 orbits), rows on the folded range
  //   mirror_x : fixed-image shape + mirror test, rows on the folded range (as "orbit")
  //   fixed    : fixed-image shape, rows on the whole range u in [0, 1]
  const orbit = CL.symmetry === 'orbit';
  const fixed = CL.symmetry === 'fixed';
  let charge;
  if (orbit) {
    need(!('sites' in d) && !('features' in d), 'symmetry "orbit" needs the symmetric shape (no sites / features)');
    need('point_orbits' in d && 'threshold_orbits' in d, 'symmetry "orbit" needs point_orbits and threshold_orbits');
    charge = buildSymmetric(d, LD);
  } else {
    need(!('point_orbits' in d) && !('threshold_orbits' in d), `symmetry "${CL.symmetry}" needs the fixed-image shape (no point_orbits / threshold_orbits)`);
    need('sites' in d && 'features' in d, `symmetry "${CL.symmetry}" needs top-level sites and features`);
    charge = buildFixed(d, LD);
    if (CL.symmetry === 'mirror_x') checkMirrorInvariance(charge.pts, charge.feats, LD);
  }
  need(charge.budget === budgetUnits, `budget_units ${budgetUnits} differs from the recomputed budget ${charge.budget}`);
  need(budgetUnits > 0n, 'budget_units must be positive (no feature of positive weight)');
  need(charge.absolute < TWO50, 'integer safety bound 2^50 exceeded');
  need(budgetUnits * CL.bound[1] < CL.bound[0] * required, 'budget inequality budget_units * q_b < p_b * minimum_units fails');

  need(Array.isArray(d.entries) && d.entries.length >= 1, 'entries: non-empty list expected');
  const halfL = qmul(L, QHALF);
  const jobs = [];
  let cursor = Q0;
  d.entries.forEach((e, i) => {
    const what = `entries[${i}]`;
    need(Array.isArray(e) && e.length === 4, `${what}: row [a, b, t, B] expected`);
    const a = rat(e[0], what), b = rat(e[1], what), t = rat(e[2], what), B = rat(e[3], what);
    need(qeq(a, cursor), `${what}: a differs from the end of the previous row (gap or overlap in the chain)`);
    need(qsign(a) >= 0 && qlt(a, b), `${what}: need 0 <= a < b`);
    if (fixed) need(qle(b, Q1), `${what}: need b <= 1`); else need(qlt(b, Q1), `${what}: need b < 1`);
    need(qsign(t) >= 0 && qlt(t, Q1), `${what}: need 0 <= t < 1`);
    need(qsign(B) > 0 && qlt(B, A), `${what}: need 0 < B < A`);
    const [ct, st] = trig(t);
    let maxSupport = null, minWidth = null;
    for (const u of [a, b]) {
      const [cu, su] = trig(u);
      const dot = qadd(qmul(ct, cu), qmul(st, su));
      const cross = qabs(qsub(qmul(ct, su), qmul(st, cu)));
      need(qsign(dot) > 0 && qle(cross, dot), `${what}: angular span`);
      const support = qadd(dot, cross), width = qadd(cu, su);
      if (maxSupport === null || qlt(maxSupport, support)) maxSupport = support;
      if (minWidth === null || qlt(width, minWidth)) minWidth = width;
    }
    need(qsign(qsub(A, qmul(B, maxSupport))) > 0, `${what}: strict core`);
    const r = qmul(qmul(A, minWidth), QHALF);
    need(qle(qmul(qmul(B, qadd(ct, st)), QHALF), r) && qlt(r, halfL), `${what}: parent envelope`);
    jobs.push({ a, b, t, B, H: qsub(halfL, r) });
    cursor = b;
  });
  if (fixed) {
    need(qeq(cursor, Q1), 'fixed-image rows must end exactly at u = 1');
  } else {
    need(qsign(qsub(qadd(qmul(cursor, cursor), qmul(QI(2), cursor)), Q1)) > 0, 'rows do not reach beyond tan(pi/8)');
  }

  // exact data of the classes that do not depend on the row
  const classes = CL.classes.map((c) => ({
    name: c.name,
    threshold: c.threshold,
    kind: qcmp(c.threshold, Q1), // -1: below 1 (containment), 0: exactly 1 (changes nothing), 1: above 1 (meeting)
    slots: c.slots.map((s) => {
      const P = s.P, m = P.length, edges = [];
      for (let i = 0; i < m; i++) {
        const p = P[i], q = P[(i + 1) % m];
        const dx = qsub(q[0], p[0]), dy = qsub(q[1], p[1]);
        const base = qsub(qmul(dx, qsub(CL.center[1], p[1])), qmul(dy, qsub(CL.center[0], p[0])));
        const den = lcm(lcm(dx[1], dy[1]), base[1]);
        edges.push({ DX: dx[0] * (den / dx[1]), DY: dy[0] * (den / dy[1]), BASE: base[0] * (den / base[1]) });
      }
      return { P, edges, gate: s.gate };
    }),
  }));
  // order in which the classes claim the cells of a slab: classes above 1 by decreasing threshold,
  // then classes below 1 by increasing threshold; equal thresholds in file order
  const ids = classes.map((_, i) => i);
  const order = ids.filter((i) => classes[i].kind > 0).sort((x, y) => qcmp(classes[y].threshold, classes[x].threshold) || x - y)
    .concat(ids.filter((i) => classes[i].kind < 0).sort((x, y) => qcmp(classes[x].threshold, classes[y].threshold) || x - y));
  // levels: one per class, then the default level (threshold 1)
  const levels = classes.map((c) => c.threshold).concat([Q1]);
  const needNum = levels.map((t) => { const z = ceilDiv(t[0] * required, t[1]); return z >= TWO53 ? 2 ** 53 : Number(z); });
  return {
    L, A, D, LD, required, budget: budgetUnits, symmetry: CL.symmetry, center: CL.center, bound: CL.bound,
    pts: charge.pts, atoms: charge.atoms, features: charge.features,
    jobs, classes, order, levels, needNum,
    images: orbit ? D4 : CL.symmetry === 'mirror_x' ? [D4[0], D4[5]] : [D4[0]],
    certificate_sha256: certSha, classes_sha256: classSha,
    gamma: required >= TWO53 ? 2 ** 53 : Number(required),
  };
}

// ------------------------------------------------------------------------------------------
// Index intervals [s, e) of cells along v
// ------------------------------------------------------------------------------------------
function normalize(list, lo, hi) { // clip to [lo, hi), sort, merge
  const out = [];
  for (const [s0, e0] of list) {
    const s = s0 < lo ? lo : s0, e = e0 > hi ? hi : e0;
    if (s < e) out.push([s, e]);
  }
  out.sort((x, y) => x[0] - y[0]);
  const merged = [];
  for (const iv of out) {
    const last = merged[merged.length - 1];
    if (last && iv[0] <= last[1]) { if (iv[1] > last[1]) last[1] = iv[1]; } else merged.push([iv[0], iv[1]]);
  }
  return merged;
}
function complement(norm, lo, hi) {
  const out = [];
  let c = lo;
  for (const [s, e] of norm) { if (s > c) out.push([c, s]); c = e; }
  if (c < hi) out.push([c, hi]);
  return out;
}
function intersect(x, y) {
  const out = [];
  let i = 0, j = 0;
  while (i < x.length && j < y.length) {
    const s = Math.max(x[i][0], y[j][0]), e = Math.min(x[i][1], y[j][1]);
    if (s < e) out.push([s, e]);
    if (x[i][1] < y[j][1]) i++; else j++;
  }
  return out;
}
function bisectLeft(arr, v) { // first index with arr[index] >= v
  let lo = 0, hi = arr.length;
  while (lo < hi) { const mid = (lo + hi) >> 1; if (arr[mid] < v) lo = mid + 1; else hi = mid; }
  return lo;
}
function bisectRight(arr, v) { // first index with arr[index] > v
  let lo = 0, hi = arr.length;
  while (lo < hi) { const mid = (lo + hi) >> 1; if (arr[mid] <= v) lo = mid + 1; else hi = mid; }
  return lo;
}

// ------------------------------------------------------------------------------------------
// Symmetries and gates (RESTRICTED_CHECKER.md 1.2, 1.6)
// ------------------------------------------------------------------------------------------
const D4 = [
  [[1n, 0n], [0n, 1n]], [[0n, -1n], [1n, 0n]], [[-1n, 0n], [0n, -1n]], [[0n, 1n], [-1n, 0n]],
  [[1n, 0n], [0n, -1n]], [[-1n, 0n], [0n, 1n]], [[0n, 1n], [1n, 0n]], [[0n, -1n], [-1n, 0n]],
];
const isReflection = (g) => g[0][0] * g[1][1] - g[0][1] * g[1][0] === -1n;

// The three quarter-turn lifts of a gate that can touch a row interval. All numbers are tan(x/2) of
// angles x in (-pi, pi), where tan(x/2) is increasing. A row interval lies in [-1, 1] (angles in
// [-pi/2, pi/2]) and a gate in (-1, 1), so the lifts by 0 and by +-pi/2 are the only candidates.
function gateLifts(gate) {
  const [lo, hi] = gate;
  return [
    [lo, hi],
    [qdiv(qadd(Q1, lo), qsub(Q1, lo)), qdiv(qadd(Q1, hi), qsub(Q1, hi))],
    [qdiv(qsub(lo, Q1), qadd(lo, Q1)), qdiv(qsub(hi, Q1), qadd(hi, Q1))],
  ];
}
// 1.6: the closed interval [a, b] lies inside ONE lift of the gate
function gateContains(gate, a, b) { return gateLifts(gate).some(([l, h]) => qle(l, a) && qle(b, h)); }
// the closed interval [a, b] has a point in common with some lift of the gate
function gateMeets(gate, a, b) { return gateLifts(gate).some(([l, h]) => qle(l, b) && qle(a, h)); }

// ------------------------------------------------------------------------------------------
// One row: published arrangement and sweep, then the cell rule of CLASS_FORMAT.md section 3
// ------------------------------------------------------------------------------------------
function checkRow(ctx, index) {
  const cpu0 = process.cpuUsage();
  const job = ctx.jobs[index];
  const D = ctx.D, LD = ctx.LD, gamma = ctx.gamma;
  const p = job.t[0], q = job.t[1];
  const C = q * q - p * p, S = 2n * p * q, T = q * q + p * p;
  const halfB = Q(job.B[0], 2n * job.B[1]);
  const scale = lcm(lcm(2n * D, halfB[1]), job.H[1]);
  const factor = scale / (2n * D);
  const h = job.H[0] * (scale / job.H[1]);
  const half = halfB[0] * (scale / halfB[1]) * T;
  // sweep coordinates: u = scale (C x' + S y'), v = scale (-S x' + C y'), (x', y') = X - (L/2, L/2)
  const n = ctx.pts.length;
  const U = new Array(n), V = new Array(n);
  for (let i = 0; i < n; i++) {
    const x = 2n * ctx.pts[i][0] - LD, y = 2n * ctx.pts[i][1] - LD;
    U[i] = (C * x + S * y) * factor;
    V[i] = (-S * x + C * y) * factor;
  }
  // rectangle of core centres that capture all sites of an atom; equal rectangles are merged
  const merged = new Map();
  for (const [ids, w] of ctx.atoms) {
    let uMax = U[ids[0]], uMin = uMax, vMax = V[ids[0]], vMin = vMax;
    for (let k = 1; k < ids.length; k++) {
      const u = U[ids[k]], v = V[ids[k]];
      if (u > uMax) uMax = u; if (u < uMin) uMin = u;
      if (v > vMax) vMax = v; if (v < vMin) vMin = v;
    }
    const r0 = uMax - half, r1 = uMin + half, r2 = vMax - half, r3 = vMin + half;
    if (r0 >= r1 || r2 >= r3) continue;
    const key = `${r0},${r1},${r2},${r3}`;
    const z = merged.get(key);
    if (z) z[4] += w; else merged.set(key, [r0, r1, r2, r3, w]);
  }
  const rects = [];
  for (const r of merged.values()) if (r[4] !== 0) rects.push(r);
  // envelope of centres [-H, H]^2 in sweep coordinates
  const poly = [[-h, -h], [h, -h], [h, h], [-h, h]].map(([x, y]) => [C * x + S * y, -S * x + C * y]);
  const xset = new Set(), yset = new Set();
  for (const pt of poly) { xset.add(pt[0]); yset.add(pt[1]); }
  for (const r of rects) { xset.add(r[0]); xset.add(r[1]); yset.add(r[2]); yset.add(r[3]); }
  const cmpBig = (a, b) => (a < b ? -1 : a > b ? 1 : 0);
  const xe = [...xset].sort(cmpBig), ye = [...yset].sort(cmpBig);
  const xi = new Map(), yi = new Map();
  xe.forEach((v, i) => xi.set(v, i));
  ye.forEach((v, i) => yi.set(v, i));
  const events = Array.from({ length: xe.length }, () => []);
  for (const r of rects) {
    const lo = yi.get(r[2]), hi = yi.get(r[3]);
    events[xi.get(r[0])].push(lo, hi, r[4]);
    events[xi.get(r[1])].push(lo, hi, -r[4]);
  }
  const edges = [];
  for (let k = 0; k < 4; k++) {
    let [u, v] = poly[k], [z, w] = poly[(k + 1) % 4];
    if (z === u) continue;
    if (z < u) { [u, z] = [z, u]; [v, w] = [w, v]; }
    edges.push({ u, z, slope: w - v, offset: v * (z - u) - u * (w - v), den: z - u });
  }
  let left = poly[0][0], right = poly[0][0];
  for (const pt of poly) { if (pt[0] < left) left = pt[0]; if (pt[0] > right) right = pt[0]; }

  // lazy minimum tree over the cells along v
  const leaves = Math.max(1, ye.length - 1);
  let size = 1;
  while (size < leaves) size *= 2;
  const mn = new Float64Array(2 * size), lz = new Float64Array(2 * size);
  function update(k, a, b, lo, hi, w) {
    if (hi <= a || b <= lo) return;
    if (lo <= a && b <= hi) { mn[k] += w; lz[k] += w; return; }
    const mid = (a + b) >> 1;
    update(2 * k, a, mid, lo, hi, w);
    update(2 * k + 1, mid, b, lo, hi, w);
    mn[k] = lz[k] + Math.min(mn[2 * k], mn[2 * k + 1]);
  }
  function query(k, a, b, lo, hi) {
    if (hi <= a || b <= lo) return Infinity;
    if (lo <= a && b <= hi) return mn[k];
    const mid = (a + b) >> 1;
    return lz[k] + Math.min(query(2 * k, a, mid, lo, hi), query(2 * k + 1, mid, b, lo, hi));
  }
  // first leaf in [lo, hi) with value < limit, or -1 (acc = sum of lazies of proper ancestors)
  function firstBelow(k, a, b, lo, hi, limit, acc) {
    if (hi <= a || b <= lo || mn[k] + acc >= limit) return -1;
    if (b - a === 1) return a;
    const mid = (a + b) >> 1;
    const r = firstBelow(2 * k, a, mid, lo, hi, limit, acc + lz[k]);
    if (r >= 0) return r;
    return firstBelow(2 * k + 1, mid, b, lo, hi, limit, acc + lz[k]);
  }
  function eachBelow(k, a, b, lo, hi, limit, acc, visit) {
    if (hi <= a || b <= lo || mn[k] + acc >= limit) return;
    if (b - a === 1) { visit(a, mn[k] + acc); return; }
    const mid = (a + b) >> 1;
    eachBelow(2 * k, a, mid, lo, hi, limit, acc + lz[k], visit);
    eachBelow(2 * k + 1, mid, b, lo, hi, limit, acc + lz[k], visit);
  }

  // ---- slot images that can matter in this row ----
  // frame point of the sweep point (u, v) under the image G: e = center + G M (u, v) / K,
  // M = [[C, -S], [S, C]], K = A * scale * T^2 (so G M is T times an orthogonal matrix)
  const K = qmul(ctx.A, QI(scale * T * T));
  const Kn = K[0], Kd = K[1], T2 = T * T;
  const nC = ctx.classes.length;
  const regs = ctx.classes.map(() => []);
  let anyActive = false;
  for (const g of ctx.images) {
    const refl = isReflection(g);
    const ia = refl ? qneg(job.b) : job.a, ib = refl ? qneg(job.a) : job.b;
    const m00 = g[0][0] * C + g[0][1] * S, m01 = -g[0][0] * S + g[0][1] * C;
    const m10 = g[1][0] * C + g[1][1] * S, m11 = -g[1][0] * S + g[1][1] * C;
    ctx.classes.forEach((cl, ci) => {
      if (cl.kind === 0) return;
      for (const s of cl.slots) {
        if (cl.kind < 0) {
          // containment: for every edge  Kd (DX wy - DY wx) + Kn BASE >= 0,  (wx, wy) = G M (u, v)
          if (!gateContains(s.gate, ia, ib)) continue;
          const edges = s.edges.map((e) => {
            let a = Kd * (e.DX * m10 - e.DY * m00), b = Kd * (e.DX * m11 - e.DY * m01), c = Kn * e.BASE;
            const g3 = gcd(gcd(a, b), c);
            if (g3 > 1n) { a /= g3; b /= g3; c /= g3; }
            return { a, b, c };
          });
          regs[ci].push({ edges });
        } else {
          // meeting: the slot polygon in sweep coordinates, (u, v) = (G M)^T K (p - center) / T^2
          if (!gateMeets(s.gate, ia, ib)) continue;
          const us = [], vs = [];
          let N = 1n;
          for (const p of s.P) {
            const px = qmul(K, qsub(p[0], ctx.center[0])), py = qmul(K, qsub(p[1], ctx.center[1]));
            const u = qdiv(qadd(qmul(QI(m00), px), qmul(QI(m10), py)), QI(T2));
            const v = qdiv(qadd(qmul(QI(m01), px), qmul(QI(m11), py)), QI(T2));
            us.push(u); vs.push(v);
            N = lcm(lcm(N, u[1]), v[1]);
          }
          const U = us.map((u) => u[0] * (N / u[1])), V = vs.map((v) => v[0] * (N / v[1]));
          let Umin = U[0], Umax = U[0];
          for (const u of U) { if (u < Umin) Umin = u; if (u > Umax) Umax = u; }
          regs[ci].push({ N, U, V, Umin, Umax });
        }
        anyActive = true;
      }
    });
  }

  // cells j of the slab [u0, u1] with all four corners of [u0, u1] x [ye_j, ye_j+1] in the closed
  // polygon (then the whole closed cell is inside, the polygon being convex)
  function insideInterval(r, u0, u1) {
    let jLow = 0, jEnd = ye.length - 1;
    for (const e of r.edges) {
      const x0 = e.a * u0, x1 = e.a * u1;
      const m = e.c + (x0 < x1 ? x0 : x1);
      if (e.b > 0n) {
        const j = bisectLeft(ye, ceilDiv(-m, e.b)); // ye_j >= -m / b
        if (j > jLow) jLow = j;
      } else if (e.b < 0n) {
        const j = bisectRight(ye, floorDiv(m, -e.b)) - 1; // ye_{j+1} <= m / (-b)
        if (j < jEnd) jEnd = j;
      } else if (m < 0n) {
        return null;
      }
      if (jLow >= jEnd) return null;
    }
    return [jLow, jEnd];
  }
  // cells j whose closed rectangle [u0, u1] x [ye_j, ye_j+1] has a point in common with the closed
  // polygon: those meeting the exact v-range of (polygon intersected with the closed slab)
  function meetInterval(r, u0, u1) {
    const N = r.N, a0 = N * u0, a1 = N * u1;
    if (r.Umax < a0 || r.Umin > a1) return null;
    let minN = null, minD = 1n, maxN = null, maxD = 1n;
    const consider = (n, d) => {
      if (minN === null) { minN = maxN = n; minD = maxD = d; return; }
      if (n * minD < minN * d) { minN = n; minD = d; }
      if (n * maxD > maxN * d) { maxN = n; maxD = d; }
    };
    const m = r.U.length;
    for (let i = 0; i < m; i++) {
      const Ui = r.U[i], Vi = r.V[i], k = (i + 1) % m, Uk = r.U[k], Vk = r.V[k];
      if (Ui >= a0 && Ui <= a1) consider(Vi, N);
      for (const line of [a0, a1]) {
        const di = Ui - line, dk = Uk - line;
        if ((di < 0n && dk > 0n) || (di > 0n && dk < 0n)) {
          let num = Vi * dk - Vk * di, den = N * (dk - di);
          if (den < 0n) { num = -num; den = -den; }
          consider(num, den);
        }
      }
    }
    if (minN === null) return null;
    const jLow = Math.max(0, bisectLeft(ye, ceilDiv(minN, minD)) - 1); // ye_{j+1} >= vmin
    const jEnd = Math.min(ye.length - 1, bisectRight(ye, floorDiv(maxN, maxD))); // ye_j <= vmax
    return jLow < jEnd ? [jLow, jEnd] : null;
  }

  // ---- sweep ----
  const required = ctx.required;
  const fails = (m, level) => BigInt(m) * ctx.levels[level][1] < ctx.levels[level][0] * required;
  const count = new Array(nC + 1).fill(0), least = new Array(nC + 1).fill(Infinity);
  let best = Infinity, cells = 0, deficientSlabs = 0, deficit = Infinity;
  let witness = null;
  for (let i = 0; i < xe.length - 1; i++) {
    const ev = events[i];
    for (let e = 0; e < ev.length; e += 3) update(1, 0, size, ev[e], ev[e + 1], ev[e + 2]);
    const u0 = xe[i], u1 = xe[i + 1];
    if (u0 < left || u1 > right) continue;
    // v-range of the envelope over the slab, from the edges that span it
    let bn = null, bd = 1n, tn = null, td = 1n, crossings = 0;
    for (const e of edges) {
      if (e.u <= u0 && u1 <= e.z) {
        for (const x of [u0, u1]) {
          const num = e.slope * x + e.offset;
          crossings++;
          if (bn === null) { bn = tn = num; bd = td = e.den; continue; }
          if (num * bd < bn * e.den) { bn = num; bd = e.den; }
          if (num * td > tn * e.den) { tn = num; td = e.den; }
        }
      }
    }
    need(crossings === 4, `row ${index}: envelope crossings`);
    const lo = bisectRight(ye, floorDiv(bn, bd)) - 1;
    const hi = bisectLeft(ye, ceilDiv(tn, td));
    need(lo >= 0 && lo < hi && hi <= ye.length - 1, `row ${index}: query limits`);
    const slabMin = query(1, 0, size, lo, hi);
    need(Number.isSafeInteger(slabMin), `row ${index}: integer sweep`);
    if (slabMin < best) best = slabMin;
    cells += hi - lo;
    if (slabMin < gamma) deficientSlabs++;
    // partition of the checked cells of the slab by the class that decides their threshold
    const pieces = [];
    let remaining = [[lo, hi]];
    if (anyActive) {
      for (const ci of ctx.order) {
        if (!regs[ci].length) continue;
        if (!remaining.length) break;
        const high = ctx.classes[ci].kind > 0;
        const list = [];
        for (const r of regs[ci]) {
          const iv = high ? meetInterval(r, u0, u1) : insideInterval(r, u0, u1);
          if (iv) list.push(iv);
        }
        if (!list.length) continue;
        const set = normalize(list, lo, hi);
        if (!set.length) continue;
        for (const iv of intersect(remaining, set)) pieces.push([iv[0], iv[1], ci]);
        remaining = intersect(remaining, complement(set, lo, hi));
      }
    }
    for (const iv of remaining) pieces.push([iv[0], iv[1], nC]);
    pieces.sort((x, y) => x[0] - y[0]);
    let covered = 0;
    for (const [s, e, level] of pieces) {
      const m = (s === lo && e === hi) ? slabMin : query(1, 0, size, s, e);
      need(Number.isSafeInteger(m) && e > s, `row ${index}: integer sweep`);
      covered += e - s;
      count[level] += e - s;
      if (m < least[level]) least[level] = m;
      if (fails(m, level)) {
        if (m < deficit) deficit = m;
        if (witness === null) {
          const j = firstBelow(1, 0, size, s, e, ctx.needNum[level], 0);
          need(j >= s && j < e, `row ${index}: witness search`);
          let charge = null;
          eachBelow(1, 0, size, j, j + 1, Infinity, 0, (a, val) => { charge = val; });
          need(charge !== null && fails(charge, level), `row ${index}: witness charge`);
          const corner = (u, v) => {
            const wx = C * u - S * v, wy = S * u + C * v;
            return [qstr(qadd(ctx.center[0], qdiv(QI(wx), K))), qstr(qadd(ctx.center[1], qdiv(QI(wy), K)))];
          };
          witness = {
            slab: i, cell: j, charge,
            required_threshold: qstr(ctx.levels[level]),
            class: level < nC ? ctx.classes[level].name : null,
            frame_corners: [corner(u0, ye[j]), corner(u1, ye[j]), corner(u1, ye[j + 1]), corner(u0, ye[j + 1])],
          };
        }
      }
    }
    need(covered === hi - lo, `row ${index}: the pieces do not partition the slab`);
  }
  need(cells > 0 && Number.isSafeInteger(best), `row ${index}: no checked cell`);
  need(count.reduce((z, x) => z + x, 0) === cells && Math.min(...least) === best, `row ${index}: class accounting`);
  const cpu = process.cpuUsage(cpu0);
  const part = (level) => ({ cells: count[level], minimum_units: count[level] ? least[level] : null });
  return {
    interval: index,
    minimum_units: best,
    cells,
    passed: witness === null,
    deficient_slabs: deficientSlabs,
    deficit_minimum_units: Number.isFinite(deficit) ? deficit : null,
    default: part(nC),
    classes: ctx.classes.map((c, i) => ({ name: c.name, ...part(i) })),
    witness,
    cpu_seconds: Math.round((cpu.user + cpu.system) / 1e3) / 1e3,
  };
}

// ------------------------------------------------------------------------------------------
// Slices, merge, command line
// ------------------------------------------------------------------------------------------
// Bind the reported identity to this loaded process, and refuse a later source change.
const LOADED_CHECKER_SHA = sha256(fs.readFileSync(__filename));
const CHECKER_SHA = () => ({ 'verify_classes.js': LOADED_CHECKER_SHA });
const PASS = 'PASS_CLASSES_EXACT_COVER', PARTIAL = 'PASS_CLASSES_INTERVAL_PARTITION_ONLY';
const FAILURE = 'CLASSES_EXACT_COVERAGE_FAILURE', INCOMPLETE = 'MERGE_INCOMPLETE';

function header(ctx) {
  return {
    implementation: 'node verify_classes.js',
    schema: CLASS_SCHEMA,
    symmetry: ctx.symmetry,
    bound: qstr(ctx.bound),
    classes: ctx.classes.map((c) => ({ name: c.name, threshold: qstr(c.threshold), slots: c.slots.length })),
    total_intervals: ctx.jobs.length,
    required_units: String(ctx.required),
    budget_units: String(ctx.budget),
    surplus: qstr(qsub(qmul(ctx.bound, [ctx.required, 1n]), [ctx.budget, 1n])),
    certificate_sha256: ctx.certificate_sha256,
    classes_sha256: ctx.classes_sha256,
    checker_sha256: CHECKER_SHA(),
  };
}
function statement(ctx) {
  const which = ctx.symmetry === 'orbit' ? 'the listed slots united with their eight D4 images'
    : ctx.symmetry === 'mirror_x' ? 'the listed slots united with their images under the mirror x -> 2 c_x - x'
      : 'the listed slots exactly as written';
  return `For every family of closed unit squares with pairwise disjoint interiors inside a square of side ${qstr(qdiv(ctx.L, ctx.A))}, `
    + `read in the frame with the container centre at (${qstr(ctx.center[0])}, ${qstr(ctx.center[1])}), the sum of tau(pose) over the squares is less than ${qstr(ctx.bound)}, `
    + 'where tau(pose) is the least threshold among the classes that contain the pose and 1 if no class contains it. '
    + `A class is ${which} (angle gates with all quarter-turn lifts). Classes: `
    + `${ctx.classes.map((c) => `${c.name} threshold ${qstr(c.threshold)} (${c.slots.length} slots)`).join('; ')}.`;
}

// totals over a list of row records: cells decided by each class and the least charge among them
function totals(ctx, rows) {
  const add = (z, p) => ({ cells: z.cells + p.cells, minimum_units: p.minimum_units !== null && (z.minimum_units === null || p.minimum_units < z.minimum_units) ? p.minimum_units : z.minimum_units });
  let def = { cells: 0, minimum_units: null };
  const cls = ctx.classes.map((c) => ({ name: c.name, cells: 0, minimum_units: null }));
  let unrestricted = null, deficit = null;
  for (const r of rows) {
    def = add(def, r.default);
    r.classes.forEach((p, i) => { cls[i] = { name: cls[i].name, ...add(cls[i], p) }; });
    if (unrestricted === null || r.minimum_units < unrestricted) unrestricted = r.minimum_units;
    if (r.deficit_minimum_units !== null && (deficit === null || r.deficit_minimum_units < deficit)) deficit = r.deficit_minimum_units;
  }
  return { unrestricted_minimum_units: unrestricted, deficit_minimum_units: deficit, cells_default: def, cells_by_class: cls };
}

function sliceResult(ctx, start, end, rows, seconds, workers) {
  const failed = rows.filter((r) => !r.passed).map((r) => r.interval);
  const complete = start === 0 && end === ctx.jobs.length;
  const status = failed.length ? FAILURE : complete ? PASS : PARTIAL;
  return {
    status,
    statement: status === PASS ? statement(ctx) : null,
    ...header(ctx),
    start, end_exclusive: end,
    failed_intervals: failed,
    ...totals(ctx, rows),
    workers,
    seconds,
    cpu_seconds_rows: Math.round(rows.reduce((z, r) => z + r.cpu_seconds, 0) * 1e3) / 1e3,
    verified_utc: new Date().toISOString(),
    rows,
  };
}

function rowRecordOk(ctx, r) {
  const partOk = (p) => p !== null && typeof p === 'object' && Number.isInteger(p.cells) && p.cells >= 0
    && (p.minimum_units === null || Number.isInteger(p.minimum_units));
  return r !== null && typeof r === 'object' && Number.isInteger(r.interval) && typeof r.passed === 'boolean'
    && Number.isInteger(r.minimum_units) && Number.isInteger(r.cells)
    && (r.deficit_minimum_units === null || Number.isInteger(r.deficit_minimum_units))
    && r.passed === (r.deficit_minimum_units === null) && r.passed === (r.witness === null)
    && partOk(r.default) && Array.isArray(r.classes) && r.classes.length === ctx.classes.length
    && r.classes.every((p, i) => partOk(p) && p.name === ctx.classes[i].name)
    && r.default.cells + r.classes.reduce((z, p) => z + p.cells, 0) === r.cells;
}

function mergeSlices(ctx, files) {
  const head = header(ctx);
  const total = ctx.jobs.length;
  const kept = new Array(total).fill(null);
  const failed = new Set();
  const problems = [];
  for (const f of files) {
    let s;
    try { s = JSON.parse(fs.readFileSync(f, 'utf8')); } catch (e) { problems.push(`${f}: unreadable`); continue; }
    if (s === null || typeof s !== 'object') { problems.push(`${f}: not a slice`); continue; }
    const bad = Object.keys(head).filter((key) => JSON.stringify(s[key]) !== JSON.stringify(head[key]));
    if (bad.length) { problems.push(`${f}: differs in ${bad.join(', ')}`); continue; }
    if (!Array.isArray(s.rows) || !Number.isInteger(s.start) || !Number.isInteger(s.end_exclusive)
      || s.start < 0 || s.end_exclusive > total || s.rows.length !== s.end_exclusive - s.start) { problems.push(`${f}: malformed slice`); continue; }
    if (!s.rows.every((r, n) => rowRecordOk(ctx, r) && r.interval === s.start + n)) { problems.push(`${f}: malformed rows`); continue; }
    const anyFailed = s.rows.some((r) => !r.passed);
    if (anyFailed !== (s.status === FAILURE) || (!anyFailed && s.status !== PASS && s.status !== PARTIAL)
      || JSON.stringify(s.failed_intervals) !== JSON.stringify(s.rows.filter((r) => !r.passed).map((r) => r.interval))) {
      problems.push(`${f}: status and row flags are inconsistent`); continue;
    }
    for (const r of s.rows) {
      if (!r.passed) failed.add(r.interval);
      const same = (a, b) => ['passed', 'minimum_units', 'cells', 'deficient_slabs', 'deficit_minimum_units', 'default', 'classes'].every((k) => JSON.stringify(a[k]) === JSON.stringify(b[k]));
      if (kept[r.interval] === null) kept[r.interval] = r;
      else if (!same(kept[r.interval], r)) problems.push(`${f}: row ${r.interval} differs from the same row in an earlier slice`);
    }
  }
  const missing = [];
  for (let i = 0; i < total; i++) if (kept[i] === null) missing.push(i);
  const status = failed.size ? FAILURE : (missing.length || problems.length) ? INCOMPLETE : PASS;
  return {
    status,
    statement: status === PASS ? statement(ctx) : null,
    ...head,
    start: 0, end_exclusive: total,
    merged_files: files.length,
    problems,
    missing_intervals: missing.length,
    first_missing_intervals: missing.slice(0, 20),
    failed_intervals: [...failed].sort((a, b) => a - b),
    ...totals(ctx, kept.filter((r) => r !== null)),
    verified_utc: new Date().toISOString(),
  };
}

function runRows(ctx, start, end, log) {
  const begin = Date.now();
  const rows = [];
  for (let i = start; i < end; i++) {
    const row = checkRow(ctx, i);
    rows.push(row);
    if (log && ((i - start) % 16 === 0 || !row.passed)) {
      log(`ROW ${i} min ${row.minimum_units} cells ${row.cells} ${row.passed ? 'pass' : 'FAIL'} deficient_slabs ${row.deficient_slabs} t ${((Date.now() - begin) / 1000).toFixed(1)}`);
    }
  }
  return rows;
}

// An actual child must certify the same context as its parent before rows are used.
function validateWorkerSlice(ctx, expectedHeader, part, start, end, exitCode) {
  const label = `worker for rows ${start}..${end - 1}`;
  need(part !== null && typeof part === 'object' && !Array.isArray(part), `${label}: not a slice`);
  const bad = Object.keys(expectedHeader).filter((key) => JSON.stringify(part[key]) !== JSON.stringify(expectedHeader[key]));
  need(bad.length === 0, `${label}: input/source context differs in ${bad.join(', ')}`);
  need(part.start === start && part.end_exclusive === end && Array.isArray(part.rows)
    && part.rows.length === end - start, `${label}: wrong range`);
  need(part.workers === 1 && part.rows.every((r, i) => rowRecordOk(ctx, r) && r.interval === start + i), `${label}: malformed rows`);
  const failed = part.rows.filter((r) => !r.passed).map((r) => r.interval);
  const expectedStatus = failed.length ? FAILURE : start === 0 && end === ctx.jobs.length ? PASS : PARTIAL;
  need(part.status === expectedStatus && exitCode === (failed.length ? 2 : 0)
    && JSON.stringify(part.failed_intervals) === JSON.stringify(failed), `${label}: inconsistent status`);
  need(part.statement === (expectedStatus === PASS ? statement(ctx) : null), `${label}: wrong statement`);
  const expectedTotals = totals(ctx, part.rows);
  need(Object.keys(expectedTotals).every((key) => JSON.stringify(part[key]) === JSON.stringify(expectedTotals[key])), `${label}: inconsistent totals`);
  return part.rows;
}

// --workers w: w child processes of this file on consecutive parts of the range
async function runWorkers(ctx, expectedHeader, certPath, classPath, start, end, workers) {
  const os = require('os'), path = require('path'), { spawn } = require('child_process');
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'verify-classes-'));
  const n = end - start, w = Math.min(workers, n);
  const jobs = [];
  for (let k = 0; k < w; k++) {
    const s = start + Math.floor(n * k / w), e = start + Math.floor(n * (k + 1) / w);
    const out = path.join(dir, `part${k}.json`);
    jobs.push(new Promise((resolve, reject) => {
      const child = spawn(process.execPath, [__filename, certPath, '--classes', classPath, '--start', String(s), '--count', String(e - s), '--output', out, '--quiet'],
        { stdio: ['ignore', 'ignore', 'inherit'] });
      child.on('error', reject);
      child.on('exit', (code) => ((code === 0 || code === 2) ? resolve([s, e, out, code]) : reject(new Error(`worker for rows ${s}..${e - 1} ended with code ${code}`))));
    }));
  }
  const rows = [];
  try {
    for (const [s, e, out, code] of await Promise.all(jobs)) {
      const part = JSON.parse(fs.readFileSync(out, 'utf8'));
      for (const r of validateWorkerSlice(ctx, expectedHeader, part, s, e, code)) rows.push(r);
    }
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
  rows.forEach((r, k) => { if (r.interval !== start + k) throw new Error('worker rows out of order'); });
  return rows;
}

async function main(argv) {
  const args = { merge: null };
  const positional = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--output') args.output = argv[++i];
    else if (a === '--classes') args.classes = argv[++i];
    else if (a === '--start') args.start = argv[++i];
    else if (a === '--count') args.count = argv[++i];
    else if (a === '--workers') args.workers = argv[++i];
    else if (a === '--quiet') args.quiet = true;
    else if (a === '--merge') { args.merge = argv.slice(i + 1); break; } else if (a.startsWith('--')) throw new Refused(`unknown option ${a}`);
    else positional.push(a);
  }
  need(positional.length === 1 && args.output && args.classes,
    'usage: verify_classes.js CERT.json --classes CLASSES.json --output OUT.json [--start i] [--count n] [--workers w] [--quiet] | --merge S1.json ...');
  const nonneg = (s, name) => { need(/^[0-9]+$/.test(String(s)), `${name}: non-negative integer expected`); return Number(s); };
  const ctx = loadAll(positional[0], args.classes);
  const expectedHeader = header(ctx);
  let result;
  if (args.merge) {
    need(args.merge.length >= 1, '--merge needs slice files');
    result = mergeSlices(ctx, args.merge);
  } else {
    const total = ctx.jobs.length;
    const start = args.start === undefined ? 0 : nonneg(args.start, '--start');
    const count = args.count === undefined ? total : nonneg(args.count, '--count');
    const workers = args.workers === undefined ? 1 : nonneg(args.workers, '--workers');
    const end = Math.min(total, start + count);
    need(start < end, 'row range: need 0 <= start < end');
    need(workers >= 1, '--workers: at least 1');
    const begin = Date.now();
    const rows = workers > 1 && end - start > 1
      ? await runWorkers(ctx, expectedHeader, positional[0], args.classes, start, end, workers)
      : runRows(ctx, start, end, args.quiet ? null : (s) => console.log(s));
    result = sliceResult(ctx, start, end, rows, (Date.now() - begin) / 1000, workers);
  }
  need(sha256(fs.readFileSync(__filename)) === LOADED_CHECKER_SHA, 'checker source changed during verification');
  fs.writeFileSync(args.output, JSON.stringify(result, null, 1));
  const short = { ...result };
  delete short.rows;
  if (!args.quiet) console.log(JSON.stringify(short));
  return result.status === FAILURE ? 2 : result.status === INCOMPLETE ? 3 : 0;
}

module.exports = { Refused, parseJsonExact, parseClassFile, loadAll, validate, checkRow, mergeSlices, main, gateContains, gateMeets };

if (require.main === module) {
  main(process.argv.slice(2)).then((code) => { process.exitCode = code; }, (e) => {
    if (e instanceof Refused) {
      console.error(`REFUSED: ${e.message}`);
      process.exitCode = 1;
    } else {
      throw e;
    }
  });
}
