#!/usr/bin/env python3
"""merge_select.py: WHICH MERGE COUNTS for a statement (one definition, used by compare_statement.py; importable).

    counting_merge(merged_dir, statement_id, capture_dir) -> None or dict(attempt_id, dir, record, record_sha256)

A merge attempt is a directory  merged_dir/<statement_id>/m<n>/  written by capture/merge_run.sh.  The merge that
counts is the lowest-numbered attempt whose merge_provenance.json
  - is for this statement and this attempt id, with verdict PASS and wrapper exit code the integer 0,
  - names, by sha256, the SOURCE_MANIFEST.json, PLAN_MANIFEST.json and MERGE_MANIFEST.json that lie in capture_dir now,
  - and whose two receipt files have the sha256 and size the record names.
Attempts without a record, with another verdict, or made under other manifests never count; they are left as they are.

    python3 merge_select.py MERGED_DIR CAPTURE_DIR [ID ...]      prints, per statement:  ID  m<n> | none
"""
import json, os, re, sys, hashlib


def _sha(p):
    try:
        return hashlib.sha256(open(p, 'rb').read()).hexdigest()
    except OSError:
        return None


def counting_merge(merged_dir, sid, capture_dir):
    want = {k: _sha(os.path.join(capture_dir, f)) for k, f in (('source_manifest_sha256', 'SOURCE_MANIFEST.json'), ('plan_manifest_sha256', 'PLAN_MANIFEST.json'),
                                                             ('merge_manifest_sha256', 'MERGE_MANIFEST.json'))}
    if None in want.values():
        return None
    base = os.path.join(merged_dir, sid)
    if not os.path.isdir(base):
        return None
    ids = sorted((int(m.group(1)), n) for n in os.listdir(base) for m in [re.fullmatch(r'm([1-9][0-9]{0,2})', n)] if m)
    for _, mid in ids:
        d = os.path.join(base, mid); p = os.path.join(d, 'merge_provenance.json')
        try:
            raw = open(p, 'rb').read(); r = json.loads(raw.decode('utf-8'))
        except (OSError, ValueError, UnicodeDecodeError):
            continue
        if type(r) is not dict or r.get('statement_id') != sid or r.get('merge_attempt_id') != mid or r.get('verdict') != 'PASS':
            continue
        w = (r.get('exits') or {}).get('wrapper') or {}
        if type(w.get('exit_code')) is not int or w['exit_code'] != 0 or any(r.get(k) != v for k, v in want.items()):
            continue
        ok = True
        for role, name in (('python', 'receipt_python.json'), ('node', 'receipt_node.json')):
            o = (r.get('outputs') or {}).get(role)
            f = os.path.join(d, name)
            ok &= type(o) is dict and o.get('file') == name and _sha(f) == o.get('sha256') and type(o.get('bytes')) is int and os.path.getsize(f) == o['bytes']
        if ok:
            return dict(attempt_id=mid, dir=d, record=r, record_sha256=hashlib.sha256(raw).hexdigest())
    return None


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    merged, cap = sys.argv[1:3]
    for sid in (sys.argv[3:] or sorted(os.listdir(merged))):
        c = counting_merge(merged, sid, cap)
        print(sid, c['attempt_id'] if c else 'none')
