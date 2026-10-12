#!/usr/bin/env python3
"""fetch_large.py : puts the 12 large files of this edition under _large/ and verifies each one.

    python3 fetch_large.py                 download the release assets, verify, place
    python3 fetch_large.py --from DIR      take the files from a local folder instead (no network)
    python3 fetch_large.py --list          print what would be fetched and stop

The large files (each above 100 MB, 4.8 GB together) are not in the git repository.  They are assets of
the release `large-files-v1` of the repository; the asset name is the file's base name.  LARGE_FILES.tsv
lists each file with its relative path, size and SHA-256.

For every file: if it is already at _large/<relative path> with the listed size and SHA-256 it is left
alone.  Otherwise it is fetched into a temporary file next to its place, its size and SHA-256 are checked,
and only then is it moved into place.  A wrong size or hash, a failed download or a file that is present
with other bytes stops the script with a message and exit code 1; no half file is left behind.

Two ways to download: plain HTTPS, which needs no account, or the `gh` tool.  When the `gh` tool is installed it is
used (you must then be signed in with `gh auth login`); the option --https uses plain HTTPS instead.
Standard library only.  The script writes only under _large/ in the edition root.
"""
import sys, os, csv, hashlib, shutil, subprocess, argparse, urllib.request

ROOT = os.path.dirname(os.path.realpath(__file__))
REPO = 'Kleddamag/the-seventeenth-square-candidate'
TAG = 'large-files-v1'


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 22), b''):
            h.update(block)
    return h.hexdigest()


def correct(path, row):
    return os.path.isfile(path) and os.path.getsize(path) == int(row['bytes']) and sha256_file(path) == row['sha256']


def stop(message):
    print('FETCH RESULT: FAIL: ' + message)
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description='Fetch and verify the large files listed in LARGE_FILES.tsv.')
    ap.add_argument('--from', dest='source', metavar='DIR', help='take the files from this local folder (by relative path, or by base name) instead of downloading')
    ap.add_argument('--repo', default=REPO, help='repository that holds the release (default %s)' % REPO)
    ap.add_argument('--tag', default=TAG, help='release tag (default %s)' % TAG)
    ap.add_argument('--https', action='store_true', help='download by plain HTTPS even if the gh tool is installed')
    ap.add_argument('--list', action='store_true', help='print the files and stop')
    args = ap.parse_args()
    with open(os.path.join(ROOT, 'LARGE_FILES.tsv'), encoding='utf-8') as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    names = [os.path.basename(r['path']) for r in rows]
    if len(set(names)) != len(names):
        stop('two large files have the same base name; the release assets would collide')
    if args.list:
        for r in rows:
            print('%12s  %s  %s' % (r['bytes'], r['sha256'], r['path']))
        return 0
    gh = None if (args.https or args.source) else shutil.which('gh')
    done = skipped = 0
    for r in rows:
        rel, name = r['path'], os.path.basename(r['path'])
        dest = os.path.join(ROOT, '_large', *rel.split('/'))
        if os.path.exists(dest):
            if correct(dest, r):
                print('present  %s' % rel); skipped += 1; continue
            stop('%s is present under _large/ with another size or SHA-256 than LARGE_FILES.tsv lists. Remove it yourself and run again; this script overwrites nothing.' % rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        part = dest + '.part'
        try:
            if os.path.exists(part):
                os.remove(part)
            if args.source:
                cands = [os.path.join(args.source, *rel.split('/')), os.path.join(args.source, name)]
                src = next((c for c in cands if os.path.isfile(c)), None)
                if src is None:
                    stop('%s was not found in %s (looked for the relative path and for the base name)' % (rel, args.source))
                shutil.copyfile(src, part)
            elif gh:
                tmpdir = dest + '.dir'
                if os.path.isdir(tmpdir):
                    shutil.rmtree(tmpdir)
                os.makedirs(tmpdir)
                try:
                    rc = subprocess.run([gh, 'release', 'download', args.tag, '--repo', args.repo, '--pattern', name, '--dir', tmpdir]).returncode
                    got = os.path.join(tmpdir, name)
                    if rc != 0 or not os.path.isfile(got):
                        stop('`gh release download %s --repo %s --pattern %s` failed (exit %d). The gh tool needs a sign-in (`gh auth login`); or run again with --https, which needs no account.' % (args.tag, args.repo, name, rc))
                    os.replace(got, part)
                finally:
                    shutil.rmtree(tmpdir, ignore_errors=True)
            else:
                url = 'https://github.com/%s/releases/download/%s/%s' % (args.repo, args.tag, name)
                try:
                    with urllib.request.urlopen(url) as resp, open(part, 'wb') as out:
                        shutil.copyfileobj(resp, out, 1 << 22)
                except Exception as e:
                    stop('download of %s failed: %s. Check the network connection, the repository name (--repo) and the release tag (--tag).' % (url, e))
            size = os.path.getsize(part)
            if size != int(r['bytes']):
                stop('%s: fetched %d bytes, LARGE_FILES.tsv lists %s' % (rel, size, r['bytes']))
            h = sha256_file(part)
            if h != r['sha256']:
                stop('%s: fetched file has SHA-256 %s, LARGE_FILES.tsv lists %s' % (rel, h, r['sha256']))
            os.replace(part, dest)
            print('fetched  %s  (%s bytes, SHA-256 verified)' % (rel, r['bytes'])); done += 1
        finally:
            if os.path.exists(part):
                os.remove(part)
    print('FETCH RESULT: PASS (%d large files: %d fetched and verified, %d already present and correct)' % (len(rows), done, skipped))
    return 0


if __name__ == '__main__':
    sys.exit(main())
