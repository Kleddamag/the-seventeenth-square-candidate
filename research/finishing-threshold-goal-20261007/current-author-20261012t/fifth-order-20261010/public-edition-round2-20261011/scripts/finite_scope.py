"""Small author binding check, no proof-engine/model/solver imports.
Replay in a fresh copy; outputs are part of the submitted addendum.
"""
if __name__ == '__main__' and not globals().get('_S17_PUBLIC_RUNNER_ACTIVE', False):
    raise SystemExit('Use replay_public.py for this check; outputs must be redirected.')
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parents[4]
W = ROOT / 'research/finishing-threshold-goal-20261007/current-author-20261012t'
G = W / 'g20s-terminal-audit'

def pin(p):
    data = p.read_bytes()
    return {'file': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}

def main():
    files = [G / 'full-gate/producer/instance/research/uniform-capture-20261007/uniform.py',
             G / 'full-gate/producer/instance/research/joint-capture-20261007/pilot.py']
    for base, names in [
        ('finite-entry-stop-pruning/root-producer', ['PROOF.md','root-interface.json']),
        ('finite-entry-stop-pruning/root-review', ['REVIEW.md','manifest.json']),
        ('finite-entry-stop-pruning/entry-producer', ['PROOF.md','PRUNING.json']),
        ('finite-entry-stop-pruning/entry-review', ['REVIEW.md','MANIFEST.json','check_transfer.py','check_binding.py']),
        ('full-stopped-propagation/rational-entry-review', ['REVIEW.md','MANIFEST.json','MATHEMATICAL_INTERFACE.json','check_corollary.py']),
        ('sixteen-square-corollary/producer', ['THEOREM.md','MATHEMATICAL_INTERFACE.json']),
        ('sixteen-square-corollary/independent-review', ['REVIEW.md','MANIFEST.json']),
        ('finite-stopped-contraction/independent-review', ['REVIEW.md','MANIFEST.json']),
        ('finite-stopped-contraction/continuation-independent-review', ['REVIEW.md','MANIFEST.json']),
        ('finite-stopped-contraction/finishing-independent-review', ['REVIEW.md','MANIFEST.json']),
        ('finite-stopped-contraction/proposal-timeout-retry-independent-review', ['REVIEW.md','MANIFEST.json']),
    ]:
        files.extend(G / base / name for name in names)
    files.extend([HERE / 'revision-v4/PROOF.md', Path(__file__)])
    pins = [pin(p) for p in files]
    x = json.loads((G / 'finite-entry-stop-pruning/entry-producer/PRUNING.json').read_text())
    upper = F(x['root_transfer']['core_upper'])
    assert upper < F(501,100000)
    assert upper > F(1,200)
    assert x['root_transfer']['nonnegative_root_a_uses_actual_right_wall'] is True
    # Pure rational guard in the expanded mean-frame derivation.
    assert F(1)/(1-F(1,10)**2/2) <= 1+F(1,10)**2
    out = {'status': 'AUTHOR_CLARIFICATION_REQUIRES_SEPARATE_INDEPENDENT_READ',
           'bindings': pins,
           'entry_core_upper': str(upper),
           'entry_margin_to_501_over_100000': str(F(501,100000)-upper),
           'checks': ['small source files hashed', 'core upper strictly inside 501/100000',
                      'nonnegative root a explicitly uses actual right wall',
                      'rational tan remainder guard at q=1/10'],
           'not_replayed': ['finite models', 'duals', 'trees', 'old independent-check scripts']}
    (HERE / 'BINDINGS.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({'sources': len(pins), 'exact_core_comparison': True,
                      'bindings_sha256': pin(HERE/'BINDINGS.json')['sha256']}))

if __name__ == '__main__':
    main()
