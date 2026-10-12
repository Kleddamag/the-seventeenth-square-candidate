#!/usr/bin/env python3
"""strip_inputs.py: write, for every statement of STATEMENTS.tsv, the two checker inputs without free text.

    inputs/<id>/classes.json       the class file without  comment  (top level) and without  label  (every slot)
    inputs/<id>/certificate.json   the certificate without  source  (top level); its embedded copy  classes
                                   (where present) without the same  comment  and  label  keys
    inputs/SHA256SUMS              sha256 of every file written (shasum -a 256 -c inputs/SHA256SUMS, run inside inputs/)
    HASH_MAP.tsv                   old -> new sha256 and sizes, per file
    REMOVED_KEYS.tsv               how many keys of each kind were removed, per file (the text itself is not copied)

Why exactly these keys (exact_classes.py 802dc62a..., node/verify_classes.js 72b92624..., node/verify_classes_wb.js 7f6b2347...;
the loaders of the two Node files are identical):
  class file   exact_keys(o, (schema, symmetry, frame, bound, classes), (comment,))        Python l.151, Node l.228
               exact_keys(slot, (centre, angle_tan_half), (label,))                        Python l.173, Node l.249
               comment and label are the ONLY optional keys of the class file, every other key is required, an unknown key
               is refused; after exact_keys neither checker reads o['comment'] or s['label'] again.
  certificate  both checkers read by name only: L, A, normalized_target, coordinate_denominator, weight_denominator,
               budget_units, minimum_units, entries, and sites + features (fixed, mirror_x) or point_orbits +
               threshold_orbits (orbit); 'restriction' must be absent.  Neither reads  source  or  classes.
               classes is kept (stripped like the class file): it is a second copy of the same mathematics, equal
               to the class file before and after stripping.
Everything else is refused by this tool (unknown key, float token, duplicate key, a string that is no rational where a
rational is expected): it never drops a key it does not know.

The tool proves its own work: after writing, original and stripped file are read again from disk and compared as JSON
values by a separate routine (types exact: int / str / list / dict / bool / None; float tokens are refused altogether, so
no number is reformatted): they must be equal except that the original may carry the named keys at the named places,
with string values.  Key order and list order are kept.  The serialisation is json.dumps in the separator style of the
original file; the tool checks that this style reproduces the ORIGINAL bytes from the ORIGINAL value (round trip), so the
stripped bytes are the original writer's bytes of the smaller value.

Optional renaming of classes (OFF unless asked for):  --rename-map FILE  with lines  old_name<TAB>new_name  ('#' lines
and empty lines ignored; an empty file = no renaming).  Applied to classes[].name in the class file and in the
certificate's embedded copy.  Both checkers use a class name only as an identifier (1..64 characters of A-Z a-z 0-9
_ . + -, unique inside a class file; printed in rows and headers); the order of the classes is the file order and the
thresholds, never the names.  Before anything is written the map is checked against ALL class names of ALL statements:
every old name must exist, every new name must be well formed, must not be one of the existing names and must not be
used twice.  The proof routine then allows exactly: the removed keys, and name -> map[name] at classes[].name.

Read only outside its own folder.  No network.  Standard library only.
    python3 strip_inputs.py                                   # all statements, no renaming  -> inputs/
    python3 strip_inputs.py --rename-map RENAME_MAP.proposed.tsv   # all statements, with renaming -> inputs/
    python3 strip_inputs.py [--rename-map F] --out-dir DIR [ID ...]    # trial into DIR (inside this folder); tables go there too
"""
import json, hashlib, os, re, sys
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(HERE)
OUT = os.path.join(HERE, 'inputs')
RAT = re.compile(r'-?[0-9]+(?:/[0-9]+)?')
NAME = re.compile(r'[A-Za-z0-9_.+-]{1,64}')
CERT_READ = ('L', 'A', 'normalized_target', 'coordinate_denominator', 'weight_denominator', 'budget_units', 'minimum_units', 'entries',
             'sites', 'features', 'point_orbits', 'threshold_orbits')
CERT_TEXT = ('source',)          # removed
CERT_COPY = 'classes'            # kept, stripped like the class file
FEATURE_KEYS = {'sites', 'sets', 'weight', 'threshold', 'coefficients', 'winning_masks'}
RENAME = {}                      # old class name -> new class name (empty: no renaming)


class Refuse(Exception):
    pass


def need(ok, what):
    if not ok:
        raise Refuse(what)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def _pairs(pairs):
    out = {}
    for k, v in pairs:
        need(k not in out, 'duplicate key %r' % k)
        out[k] = v
    return out


def _const(t):
    raise Refuse('JSON constant %s' % t)


def load(raw):
    return json.loads(raw.decode('utf-8'), parse_float=Decimal, parse_constant=_const, object_pairs_hook=_pairs)


def has_float(v):
    if isinstance(v, (Decimal, float)):
        return True
    if type(v) is list:
        return any(has_float(x) for x in v)
    if type(v) is dict:
        return any(has_float(x) for x in v.values())
    return False


STYLES = [(sep, tail, asc, ind) for ind in (None, 1, 2, 4) for sep in ((',', ':'), (', ', ': '), (',', ': ')) for tail in ('', '\n') for asc in (True, False)]


def dump(v, style):
    sep, tail, asc, ind = style
    return (json.dumps(v, separators=sep, ensure_ascii=asc, indent=ind) + tail).encode('utf-8')


def style_of(raw, v):
    for st in STYLES:
        if dump(v, st) == raw:
            return st
    return None


# ------------------------------------------------------------------ stripping (builds new objects)
def strip_classes(o, what):
    need(type(o) is dict, what + ': object expected')
    need(set(o) - {'comment'} == {'schema', 'symmetry', 'frame', 'bound', 'classes'}, what + ': keys %r' % sorted(o))
    removed = {'comment': 0, 'label': 0, 'renamed': 0}
    out = {}
    for k, v in o.items():
        if k == 'comment':
            need(type(v) is str, what + ': comment is not a string'); removed['comment'] += 1
        elif k == 'classes':
            need(type(v) is list and v, what + ': classes')
            cl = []
            for ci, c in enumerate(v):
                need(type(c) is dict and set(c) == {'name', 'threshold', 'slots'}, '%s.classes[%d]: keys' % (what, ci))
                c2 = {}
                for ck, cv in c.items():
                    if ck == 'slots':
                        need(type(cv) is list and cv, '%s.classes[%d]: slots' % (what, ci))
                        sl = []
                        for si, s in enumerate(cv):
                            need(type(s) is dict and set(s) - {'label'} == {'centre', 'angle_tan_half'}, '%s.classes[%d].slots[%d]: keys' % (what, ci, si))
                            if 'label' in s:
                                need(type(s['label']) is str, 'label is not a string'); removed['label'] += 1
                            sl.append({sk: sv for sk, sv in s.items() if sk != 'label'})
                        c2[ck] = sl
                    elif ck == 'name' and cv in RENAME:
                        c2[ck] = RENAME[cv]; removed['renamed'] += 1
                    else:
                        c2[ck] = cv
                cl.append(c2)
            out[k] = cl
        else:
            out[k] = v
    return out, removed


def strip_certificate(c, what):
    need(type(c) is dict, what + ': object expected')
    unknown = set(c) - set(CERT_READ) - set(CERT_TEXT) - {CERT_COPY}
    need(not unknown, what + ': unknown top-level keys %r (not dropped; decide by hand)' % sorted(unknown))
    need('restriction' not in c, what + ': restriction')
    removed = {'source': 0, 'classes.comment': 0, 'classes.label': 0, 'classes.renamed': 0}
    out = {}
    for k, v in c.items():
        if k in CERT_TEXT:
            need(type(v) is str, what + ': %s is not a string' % k); removed[k] += 1
        elif k == CERT_COPY:
            out[k], r = strip_classes(v, what + '.classes')
            removed['classes.comment'] = r['comment']; removed['classes.label'] = r['label']; removed['classes.renamed'] = r['renamed']
        else:
            out[k] = v
    return out, removed


# ------------------------------------------------------------------ what the checkers will ask of the stripped files
def check_classfile_shape(o, what):
    """The key tests and string tests of parse_classes / parseClassFile, with NO optional key left."""
    need(not has_float(o), what + ': float token')
    need(list(sorted(o)) == sorted(('schema', 'symmetry', 'frame', 'bound', 'classes')), what + ': top keys')
    need(o['schema'] == 's17-classes-v1' and o['symmetry'] in ('fixed', 'mirror_x', 'orbit'), what + ': schema / symmetry')
    need(type(o['frame']) is dict and sorted(o['frame']) == ['center', 'unit'] and o['frame']['unit'] == 'unit_square', what + ': frame')
    need(type(o['frame']['center']) is list and len(o['frame']['center']) == 2 and all(type(x) is str and RAT.fullmatch(x) for x in o['frame']['center']), what + ': center')
    need(type(o['bound']) is str and RAT.fullmatch(o['bound']), what + ': bound')
    names = set()
    for c in o['classes']:
        need(sorted(c) == ['name', 'slots', 'threshold'], what + ': class keys')
        need(type(c['name']) is str and NAME.fullmatch(c['name']) and c['name'] not in names, what + ': class name'); names.add(c['name'])
        need(type(c['threshold']) is str and RAT.fullmatch(c['threshold']), what + ': threshold')
        for s in c['slots']:
            need(sorted(s) == ['angle_tan_half', 'centre'] and sorted(s['centre']) == ['polygon'], what + ': slot keys')
            need(all(type(p) is list and len(p) == 2 and all(type(x) is str and RAT.fullmatch(x) for x in p) for p in s['centre']['polygon']), what + ': polygon')
            need(len(s['angle_tan_half']) == 2 and all(type(x) is str and RAT.fullmatch(x) for x in s['angle_tan_half']), what + ': gate')


def only_numbers(v, what, keys_ok):
    """Below the top level of the certificate (outside 'classes'): integers, rational strings, lists, and
    objects with the feature keys only."""
    if type(v) is int:
        return
    if type(v) is str:
        need(RAT.fullmatch(v) is not None, what + ': a string that is no rational: %r' % v[:40]); return
    if type(v) is list:
        for x in v:
            only_numbers(x, what, keys_ok)
        return
    if type(v) is dict:
        need(set(v) <= keys_ok, what + ': keys %r' % sorted(v))
        for x in v.values():
            only_numbers(x, what, keys_ok)
        return
    raise Refuse(what + ': a value of type %s' % type(v).__name__)


def check_certificate_shape(c, cl, what):
    need(not has_float(c), what + ': float token')
    sym = cl['symmetry']
    shape = ('point_orbits', 'threshold_orbits') if sym == 'orbit' else ('sites', 'features')
    other = ('sites', 'features') if sym == 'orbit' else ('point_orbits', 'threshold_orbits')
    for k in ('L', 'A', 'normalized_target', 'coordinate_denominator', 'weight_denominator', 'budget_units', 'minimum_units', 'entries') + shape:
        need(k in c, what + ': key %s is missing' % k)
    need(not any(k in c for k in other), what + ': wrong shape for symmetry ' + sym)
    for k, v in c.items():
        if k != CERT_COPY:
            only_numbers(v, what + '.' + k, FEATURE_KEYS)


# ------------------------------------------------------------------ the proof of the work (separate routine)
def same_except(a, b, allowed, path, found):
    """a = original value, b = stripped value.  Equal with exact types, same key order; the original may carry extra
    keys only as allowed(path) says, with string values.  found counts them."""
    need(type(a) is type(b), '%s: type %s -> %s' % (path, type(a).__name__, type(b).__name__))
    if type(a) is dict:
        extra = allowed(path)
        ka = [k for k in a if not (k in extra and k not in b)]
        need(ka == list(b), '%s: keys differ: %r -> %r' % (path, list(a), list(b)))
        for k in a:
            if k in b:
                same_except(a[k], b[k], allowed, path + (k,), found)
            else:
                need(k in extra and type(a[k]) is str, '%s: key %r lost' % (path, k))
                found[k] = found.get(k, 0) + 1
    elif type(a) is list:
        need(len(a) == len(b), '%s: list length' % (path,))
        for i, (x, y) in enumerate(zip(a, b)):
            same_except(x, y, allowed, path + ('#',), found)
    else:
        need(type(a) in (int, str, bool, type(None)), '%s: value of type %s' % (path, type(a).__name__))
        if type(a) is str and a != b and path[-3:] == ('classes', '#', 'name') and len(path) in (3, 4) and RENAME.get(a) == b:
            found['#renamed'] = found.get('#renamed', 0) + 1
        else:
            need(a == b, '%s: value changed' % (path,))


def allowed_classfile(path):
    if path == ():
        return ('comment',)
    if path == ('classes', '#', 'slots', '#'):
        return ('label',)
    return ()


def allowed_certificate(path):
    if path == ():
        return ('source',)
    if path[:1] == ('classes',):
        return allowed_classfile(path[1:])
    return ()


# ------------------------------------------------------------------ main
def statements():
    rows = [l.rstrip('\n').split('\t') for l in open(os.path.join(HERE, 'STATEMENTS.tsv'))]
    h = rows[0]
    return [dict(zip(h, r)) for r in rows[1:]]


def one(st):
    sid = st['id']
    need(re.fullmatch(r'[A-Za-z0-9._-]{1,48}', sid) is not None and not sid.startswith('.'), 'id %r' % sid)
    src = os.path.join(W, 'results', st['input_folder'], 'exact')
    dst = os.path.join(OUT, sid)
    need(os.path.realpath(dst).startswith(os.path.realpath(HERE) + os.sep), 'destination outside the tool folder')
    os.makedirs(dst, exist_ok=True)
    rec = []; removed_rows = []; stripped = {}
    for name, fn, want in (('classes.json', strip_classes, st['classes_sha256']), ('certificate.json', strip_certificate, st['certificate_sha256'])):
        raw = open(os.path.join(src, name), 'rb').read()
        need(sha(raw) == want, '%s/%s: sha256 is not the one of STATEMENTS.tsv' % (sid, name))
        v = load(raw)
        need(not has_float(v), '%s/%s: the file has a float token' % (sid, name))
        style = style_of(raw, v)
        need(style is not None, '%s/%s: no known json.dumps style reproduces the original bytes' % (sid, name))
        new, removed = fn(v, sid + '/' + name)
        out = dump(new, style)
        need(all(ch < 128 for ch in out), '%s/%s: non-ASCII byte in the stripped file' % (sid, name))
        tmp = os.path.join(dst, name + '.tmp')
        with open(tmp, 'wb') as f:
            f.write(out)
        os.replace(tmp, os.path.join(dst, name))
        # the proof: both files again from disk
        raw2 = open(os.path.join(src, name), 'rb').read(); out2 = open(os.path.join(dst, name), 'rb').read()
        need(sha(raw2) == want and out2 == out, '%s/%s: files changed while working' % (sid, name))
        a = load(raw2); b = load(out2); found = {}
        same_except(a, b, allowed_classfile if name == 'classes.json' else allowed_certificate, (), found)
        need(sum(found.values()) == sum(removed.values()), '%s/%s: removed-key / renamed-name counts disagree' % (sid, name))
        need(found.get('#renamed', 0) == removed.get('renamed', 0) + removed.get('classes.renamed', 0), '%s/%s: renamed-name counts disagree' % (sid, name))
        need(dump(b, style) == out2, '%s/%s: the stripped file is not in its own style' % (sid, name))
        stripped[name] = b
        sepname = {(',', ':'): 'compact', (', ', ': '): 'default', (',', ': '): 'indented'}[style[0]] + ('' if style[3] is None else '(indent=%d)' % style[3]) + ('+LF' if style[1] else '')
        rec.append((sid, name, sha(raw2), sha(out2), len(raw2), len(out2), sepname))
        removed_rows.append((sid, name, ' '.join('%s=%d' % kv for kv in removed.items()), len(raw2) - len(out2)))
    cl = stripped['classes.json']; c = stripped['certificate.json']
    check_classfile_shape(cl, sid + '/classes.json')
    check_certificate_shape(c, cl, sid + '/certificate.json')
    copy = 'absent'
    if CERT_COPY in c:
        found = {}
        same_except(c[CERT_COPY], cl, lambda p: (), (), found)       # exact equality, key order included
        check_classfile_shape(c[CERT_COPY], sid + '/certificate.json.classes')
        copy = 'equal'
    need(len(c['entries']) == int(st['rows']), '%s: %d rows, STATEMENTS.tsv says %s' % (sid, len(c['entries']), st['rows']))
    return rec, removed_rows, copy


def all_class_names(sts):
    names = {}
    for st in sts:
        o = load(open(os.path.join(W, 'results', st['input_folder'], 'exact', 'classes.json'), 'rb').read())
        for c in o['classes']:
            names.setdefault(c['name'], []).append(st['id'])
    return names


def read_rename_map(path, sts):
    m = {}
    for l in open(path):
        l = l.rstrip('\n')
        if not l.strip() or l.startswith('#'):
            continue
        w = l.split('\t')
        need(len(w) == 2 and w[0] and w[1], 'rename map: line %r is not old<TAB>new' % l)
        need(w[0] not in m, 'rename map: %s listed twice' % w[0])
        m[w[0]] = w[1]
    names = all_class_names(sts)
    for old, new in m.items():
        need(old in names, 'rename map: %s is no class name of any statement' % old)
        need(NAME.fullmatch(new) is not None, 'rename map: %s is no valid class name' % new)
        need(new not in names, 'rename map: %s is already a class name (statements %s)' % (new, ' '.join(names.get(new, []))))
    need(len(set(m.values())) == len(m), 'rename map: a new name is used twice')
    return m, names


def main(argv):
    global OUT
    sts = statements(); tables = HERE; whole = True
    if '--rename-map' in argv:
        i = argv.index('--rename-map'); need(i + 1 < len(argv), '--rename-map needs a file')
        m, names = read_rename_map(argv[i + 1], sts); RENAME.update(m); argv = argv[:i] + argv[i + 2:]
        print('rename map: %d names of %d distinct class names; no collision' % (len(m), len(names)))
    if '--out-dir' in argv:
        i = argv.index('--out-dir'); need(i + 1 < len(argv), '--out-dir needs a name')
        OUT = os.path.join(HERE, argv[i + 1], 'inputs'); tables = os.path.join(HERE, argv[i + 1]); argv = argv[:i] + argv[i + 2:]
        need(os.path.realpath(tables).startswith(os.path.realpath(HERE) + os.sep), '--out-dir must be inside the tool folder')
        os.makedirs(OUT, exist_ok=True)
    if argv:
        whole = False
        sts = [s for s in sts if s['id'] in argv]
    all_rec = []; all_rem = []; copies = {}
    for st in sts:
        rec, rem, copy = one(st)
        all_rec += rec; all_rem += rem; copies[copy] = copies.get(copy, 0) + 1
    if whole or tables != HERE:
        with open(os.path.join(OUT, 'SHA256SUMS'), 'w') as f:
            for sid, name, old, new, ob, nb, style in all_rec:
                f.write('%s  %s/%s\n' % (new, sid, name))
        with open(os.path.join(tables, 'HASH_MAP.tsv'), 'w') as f:
            f.write('id\tfile\told_sha256\tnew_sha256\told_bytes\tnew_bytes\tstyle(original bytes reproduced by re-serialising: yes)\n')
            for r in all_rec:
                f.write('\t'.join(str(x) for x in r) + '\n')
        with open(os.path.join(tables, 'REMOVED_KEYS.tsv'), 'w') as f:
            f.write('id\tfile\tkeys_removed (renamed = class names replaced)\tbytes_removed\n')
            for r in all_rem:
                f.write('\t'.join(str(x) for x in r) + '\n')
    print('statements: %d   files written and proved equal up to the removed keys%s: %d   -> %s' % (len(sts), ' and the name map' if RENAME else '', len(all_rec), OUT))
    print('embedded copy certificate.classes after stripping: %r' % copies)
    print('bytes: %d -> %d' % (sum(r[4] for r in all_rec), sum(r[5] for r in all_rec)))
    print('largest file: %s/%s %d bytes' % max(((r[0], r[1], r[5]) for r in all_rec), key=lambda z: z[2]))
    unchanged = [r[0] + '/' + r[1] for r in all_rec if r[2] == r[3]]
    print('files whose bytes did not change: %d %s' % (len(unchanged), ' '.join(unchanged[:5])))


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except Refuse as e:
        print('REFUSED: %s' % e); sys.exit(1)
